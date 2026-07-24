import asyncio
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

import src.ai.client as client_module
from src.ai.client import OpenAIClient
from src.models import AIConfig
from src.redaction import is_fatal_ai_error, redact_secrets
from src.storage.manager import StorageManager


def _config(**overrides):
    values = {
        "provider": "openai",
        "model": "kimi-k2.6",
        "base_url": "https://api.moonshot.cn/v1",
        "api_key_env": "MOONSHOT_API_KEY",
        "max_completion_tokens": 8192,
        "thinking": {"type": "disabled"},
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

    assert client.model == "kimi-k2.6"
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
    client = OpenAIClient(
        _config(
            model="generic-openai-model",
            max_completion_tokens=None,
            thinking=None,
        )
    )
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


def test_kimi_request_disables_thinking_and_uses_modern_json_parameters(monkeypatch):
    monkeypatch.setenv("MOONSHOT_API_KEY", "moonshot-test-secret")
    client = OpenAIClient(_config())
    create = AsyncMock(return_value=_response('{"ok": true}'))
    client.client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )

    result = asyncio.run(client.complete("Return JSON.", "Classify this item."))

    assert result == '{"ok": true}'
    request = create.call_args.kwargs
    assert request["extra_body"] == {"thinking": {"type": "disabled"}}
    assert request["response_format"] == {"type": "json_object"}
    assert request["max_completion_tokens"] == 8192
    assert "max_tokens" not in request
    assert "temperature" not in request


def test_kimi_omits_temperature_even_when_caller_requests_override(monkeypatch):
    monkeypatch.setenv("MOONSHOT_API_KEY", "moonshot-test-secret")
    client = OpenAIClient(_config(temperature=0.2))
    create = AsyncMock(return_value=_response('{"ok": true}'))
    client.client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )

    asyncio.run(client.complete("Return JSON.", "Classify.", temperature=0.2))

    assert "temperature" not in create.call_args.kwargs


def test_kimi_thinking_incompatibility_fails_closed(monkeypatch, caplog):
    monkeypatch.setenv("MOONSHOT_API_KEY", "moonshot-test-secret")
    client = OpenAIClient(_config())
    create = AsyncMock(
        side_effect=TypeError("unexpected keyword argument 'extra_body'")
    )
    client.client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )

    with pytest.raises(RuntimeError, match="Thinking disablement"):
        asyncio.run(client.complete("system", "user"))

    assert create.call_count == 1
    assert "refusing to retry" in caplog.text

    assert is_fatal_ai_error(RuntimeError("Kimi Thinking disablement is incompatible"))


def test_kimi_never_falls_back_to_deprecated_max_tokens(monkeypatch):
    monkeypatch.setenv("MOONSHOT_API_KEY", "moonshot-test-secret")
    client = OpenAIClient(_config())
    create = AsyncMock(
        side_effect=RuntimeError(
            "Unsupported max_completion_tokens; use max_tokens instead"
        )
    )
    client.client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )

    with pytest.raises(RuntimeError, match="deprecated max_tokens"):
        asyncio.run(client.complete("system", "user"))

    assert create.call_count == 1
    assert "max_tokens" not in create.call_args.kwargs


def test_personal_config_and_workflow_pin_kimi_and_node24_actions():
    root = Path(__file__).resolve().parents[1]
    config = json.loads(
        (root / "data/config.github.json").read_text(encoding="utf-8")
    )
    workflow = (root / ".github/workflows/daily-summary.yml").read_text(
        encoding="utf-8"
    )

    assert config["ai"]["thinking"] == {"type": "disabled"}
    assert config["ai"]["temperature"] == 0.6
    assert config["ai"]["max_completion_tokens"] == 8192
    assert config["ai"]["analysis_concurrency"] == 1
    assert config["ai"]["enrichment_concurrency"] == 1
    assert "max_tokens" not in config["ai"]
    assert "kimi-k2.6" in workflow
    assert "actions/setup-python@v7" in workflow
    assert "astral-sh/setup-uv@v9.0.0" in workflow
    assert '"${KIMI_BASE_URL%/}/models"' in workflow
    assert "Kimi API preflight passed" in workflow
    assert "APIFY_TOKEN: ${{ secrets.APIFY_TOKEN }}" in workflow
    assert "Apify API preflight passed" in workflow
    assert 'cron: "0 1 * * *"' in workflow
    assert config["filtering"]["deep_analysis_limit"] == 3
    assert config["filtering"]["source_priority"][0] == "twitter"
    assert config["sources"]["twitter"]["enabled"] is True
    assert config["product_intelligence"]["enabled"] is True
    assert 'paths:\n      - ".github/workflows/daily-summary.yml"' in workflow
    assert "HORIZON_WEBHOOK_URL" not in workflow


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
