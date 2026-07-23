import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import src.ai.client as client_module
from src.ai.client import OpenAIClient
from src.models import AIConfig
from src.redaction import redact_secrets
from src.storage.manager import StorageManager


def _config(**overrides):
    values = {
        "provider": "openai",
        "model": "kimi-test-model",
        "base_url": "https://api.moonshot.cn/v1",
        "api_key_env": "MOONSHOT_API_KEY",
    }
    values.update(overrides)
    return AIConfig(**values)


def _response(content="{}"):
    return SimpleNamespace(
        usage=None,
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
    )


def test_kimi_openai_compatible_configuration_uses_moonshot_env(monkeypatch):
    monkeypatch.setenv("MOONSHOT_API_KEY", "moonshot-test-secret")
    mocked_openai = MagicMock()
    monkeypatch.setattr(client_module, "AsyncOpenAI", mocked_openai)

    client = OpenAIClient(_config())

    assert client.model == "kimi-test-model"
    mocked_openai.assert_called_once_with(
        api_key="moonshot-test-secret",
        base_url="https://api.moonshot.cn/v1",
    )


def test_kimi_model_and_base_url_expand_from_environment(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "config.json").write_text(
        """{
          "ai": {
            "provider": "openai",
            "model": "${KIMI_MODEL_ID}",
            "base_url": "${KIMI_BASE_URL}",
            "api_key_env": "MOONSHOT_API_KEY"
          },
          "sources": {},
          "filtering": {}
        }""",
        encoding="utf-8",
    )
    monkeypatch.setenv("KIMI_MODEL_ID", "console-model-id")
    monkeypatch.setenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1")

    config = StorageManager(str(data_dir)).load_config()

    assert config.ai.model == "console-model-id"
    assert config.ai.base_url == "https://api.moonshot.cn/v1"


def test_response_format_incompatibility_retries_without_parameter(monkeypatch):
    monkeypatch.setenv("MOONSHOT_API_KEY", "moonshot-test-secret")
    client = OpenAIClient(_config())
    create = AsyncMock(
        side_effect=[
            RuntimeError("Unsupported parameter: response_format"),
            _response('{"ok": true}'),
        ]
    )
    client.client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )

    result = asyncio.run(client.complete("system", "user"))

    assert result == '{"ok": true}'
    assert "response_format" in create.call_args_list[0].kwargs
    assert "response_format" not in create.call_args_list[1].kwargs
    assert client._supports_response_format is False


def test_api_key_is_redacted_from_log_messages(monkeypatch):
    secret = "moonshot-secret-that-must-not-leak"
    monkeypatch.setenv("MOONSHOT_API_KEY", secret)

    result = redact_secrets(f"Authorization: Bearer {secret}")

    assert secret not in result
    assert "[REDACTED]" in result


def test_unset_model_variable_fails_with_clear_name(monkeypatch):
    monkeypatch.setenv("MOONSHOT_API_KEY", "moonshot-test-secret")
    config = _config(model="${KIMI_MODEL_ID}")

    try:
        OpenAIClient(config)
    except ValueError as error:
        assert "KIMI_MODEL_ID" in str(error)
    else:  # pragma: no cover
        raise AssertionError("expected unresolved model variable to fail")
