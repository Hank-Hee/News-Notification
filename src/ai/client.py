"""AI client abstraction supporting multiple providers."""

import logging
import os
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from openai import AsyncAzureOpenAI, AsyncOpenAI
from anthropic import AsyncAnthropic
from google import genai
from google.genai import types


from ..models import AIConfig, AIProvider, AI_PROVIDER_DEFAULTS
from ..redaction import redact_secrets
from rich import print as rich_print
from .tokens import ensure_request_allowed, record_request


logger = logging.getLogger(__name__)


_ENV_VAR_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_SECRET_PREFIXES = (
    "sk-",
    "sk_",
    "AIza",
    "xai-",
    "gsk_",
    "hf_",
)
_DEFAULT_API_KEY_ENVS = {
    AIProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
    AIProvider.OPENAI: "OPENAI_API_KEY",
    AIProvider.AZURE: "AZURE_OPENAI_API_KEY",
    AIProvider.ALI: "DASHSCOPE_API_KEY",
    AIProvider.GEMINI: "GOOGLE_API_KEY",
    AIProvider.DOUBAO: "DOUBAO_API_KEY",
    AIProvider.MINIMAX: "MINIMAX_API_KEY",
    AIProvider.DEEPSEEK: "DEEPSEEK_API_KEY",
}


def _resolve_api_key(config: AIConfig, *, fallback: Optional[str] = None) -> str:
    api_key = os.getenv(config.api_key_env)
    if api_key:
        return api_key
    if fallback is not None:
        return fallback
    raise ValueError(_missing_api_key_message(config))


def _missing_api_key_message(config: AIConfig) -> str:
    expected_env = _DEFAULT_API_KEY_ENVS.get(config.provider)
    if expected_env:
        setup_hint = (
            f"Set {expected_env}=your_api_key in .env or your shell, then set "
            f'ai.api_key_env to "{expected_env}" in data/config.json.'
        )
    else:
        setup_hint = (
            "Set the provider API key in .env or your shell, then set "
            "ai.api_key_env to that environment variable name in data/config.json."
        )

    if _looks_like_api_key_value(config.api_key_env):
        return (
            "Missing API key: ai.api_key_env must be an environment variable "
            f"name, not the API key value. {setup_hint}"
        )

    return (
        "Missing API key environment variable configured by ai.api_key_env. "
        "ai.api_key_env should contain the environment variable name, not the "
        f"key value. {setup_hint}"
    )


def _looks_like_api_key_value(value: str) -> bool:
    if value.startswith(_SECRET_PREFIXES):
        return True
    return not bool(_ENV_VAR_RE.fullmatch(value))


def _normalize_ollama_base_url(base_url: str) -> str:
    normalized = base_url.strip().rstrip("/")
    if "://" not in normalized:
        normalized = f"http://{normalized}"
    if normalized.endswith("/v1"):
        return normalized
    return f"{normalized}/v1"


def _require_resolved(value: Optional[str], field_name: str) -> None:
    """Fail clearly when a required AI setting still contains an unset ${VAR}."""
    if not value:
        return
    match = re.search(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", value)
    if match:
        raise ValueError(
            f"Missing environment variable {match.group(1)} required by ai.{field_name}"
        )


class AIClient(ABC):
    """Abstract base class for AI clients."""

    @abstractmethod
    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion from AI model.

        Args:
            system: System prompt
            user: User prompt
            temperature: Optional sampling temperature override
            max_tokens: Optional maximum tokens override

        Returns:
            str: Generated completion text
        """
        pass


class AnthropicClient(AIClient):
    """Client for Anthropic-compatible models."""

    def __init__(self, config: AIConfig):
        """Initialize Anthropic client.

        Args:
            config: AI configuration
        """
        self.config = config

        api_key = _resolve_api_key(config)

        kwargs = {"api_key": api_key}
        if config.base_url:
            kwargs["base_url"] = config.base_url

        self.client = AsyncAnthropic(**kwargs)
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion using Claude.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            str: Generated text
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        try:
            ensure_request_allowed()
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[{"role": "user", "content": user}]
            )
        except Exception:
            record_request(self.config.provider.value, model=self.model)
            raise
        usage = getattr(message, "usage", None)
        if usage is not None:
            record_request(
                self.config.provider.value,
                input_tokens=getattr(usage, "input_tokens", 0),
                output_tokens=getattr(usage, "output_tokens", 0),
                model=self.model,
                cached_tokens=getattr(usage, "cache_read_input_tokens", 0),
                input_cost_per_million_cny=self.config.input_cost_per_million_cny,
                output_cost_per_million_cny=self.config.output_cost_per_million_cny,
            )
        else:
            record_request(self.config.provider.value, model=self.model)
        return message.content[0].text


class OpenAIClient(AIClient):
    """Client for OpenAI-compatible APIs."""

    _BASE_URL_ENVS = {
        "ollama": (
            "HORIZON_OLLAMA_BASE_URL",
            "OLLAMA_BASE_URL",
            "OLLAMA_HOST",
        ),
    }

    # Providers that don't support response_format
    _NO_RESPONSE_FORMAT = {"minimax"}

    # Providers that need temperature clamped to (0, 1]
    _TEMP_CLAMP = {"minimax"}

    # Newer reasoning-series / GPT-5 family models reject legacy `max_tokens`
    # and require `max_completion_tokens` instead.
    _MODELS_REQUIRING_MAX_COMPLETION_TOKENS = (
        "o1",
        "o3",
        "o4",
        "gpt-5",
        "kimi-k2.6",
    )

    def __init__(self, config: AIConfig):
        """Initialize OpenAI-compatible client.

        Args:
            config: AI configuration
        """
        self.config = config

        _require_resolved(config.model, "model")
        _require_resolved(config.base_url, "base_url")

        fallback = "no_key" if config.provider == AIProvider.OLLAMA else None
        api_key = _resolve_api_key(config, fallback=fallback)

        kwargs = {"api_key": api_key}
        base_url = self._resolve_base_url(config)
        if base_url:
            kwargs["base_url"] = base_url

        self.client = AsyncOpenAI(**kwargs)
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_completion_tokens or config.max_tokens
        self.provider = config.provider.value
        self.thinking = config.thinking.model_dump() if config.thinking else None
        self._strict_kimi_k26 = config.model == "kimi-k2.6"
        # Some newer models (e.g. Claude Opus 4.7 on Bedrock Converse) reject
        # `temperature`. We learn this on first 400 and stop sending it.
        # Kimi K2.6 uses a fixed temperature (0.6 in non-thinking mode) and its
        # API documentation recommends omitting the parameter entirely.
        self._supports_temperature = not self._strict_kimi_k26
        self._supports_response_format = self.provider not in self._NO_RESPONSE_FORMAT
        self._supports_token_limit = True
        self._use_max_completion_tokens = any(
            config.model.startswith(prefix)
            for prefix in self._MODELS_REQUIRING_MAX_COMPLETION_TOKENS
        ) or config.max_completion_tokens is not None

    @classmethod
    def _resolve_base_url(cls, config: AIConfig) -> Optional[str]:
        base_url = (config.base_url or "").strip()
        if not base_url:
            for env_name in cls._BASE_URL_ENVS.get(config.provider.value, ()):
                base_url = os.getenv(env_name, "").strip()
                if base_url:
                    break
        if not base_url:
            base_url = AI_PROVIDER_DEFAULTS.get(config.provider, {}).get("base_url") or ""

        if config.provider == AIProvider.OLLAMA and base_url:
            return _normalize_ollama_base_url(base_url)
        return base_url or None

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion using OpenAI-compatible API.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            str: Generated text
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        # Clamp temperature for providers that require it
        if self.provider in self._TEMP_CLAMP and temperature <= 0:
            temperature = 0.01

        for _ in range(6):
            try:
                response = await self._do_request(
                    system=system,
                    user=user,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    include_temperature=self._supports_temperature,
                    include_response_format=self._supports_response_format,
                    include_token_limit=self._supports_token_limit,
                    use_max_completion_tokens=self._use_max_completion_tokens,
                )
                break
            except Exception as exc:
                message = str(exc)
                if self.thinking and self._is_thinking_control_unsupported(message):
                    logger.error(
                        "Cannot guarantee that Thinking is disabled for %s; "
                        "refusing to retry without the thinking control: %s",
                        self.model,
                        redact_secrets(message),
                    )
                    raise RuntimeError(
                        f"Thinking disablement is incompatible with {self.model} or "
                        "the current SDK. The request was stopped instead of "
                        "retrying with Thinking enabled."
                    ) from exc
                if (
                    self._supports_response_format
                    and self._is_response_format_unsupported(message)
                ):
                    if self._strict_kimi_k26:
                        raise RuntimeError(
                            "Kimi JSON mode was rejected for kimi-k2.6; the request "
                            "was stopped instead of dropping response_format."
                        ) from exc
                    self._supports_response_format = False
                    continue
                if self._supports_temperature and self._is_temperature_unsupported(message):
                    self._supports_temperature = False
                    continue
                token_fallback = self._token_fallback_mode(message)
                if self._supports_token_limit and token_fallback is not None:
                    if self._strict_kimi_k26:
                        raise RuntimeError(
                            "Kimi rejected max_completion_tokens for kimi-k2.6; "
                            "the request was stopped instead of using deprecated "
                            "max_tokens or omitting the completion limit."
                        ) from exc
                    if token_fallback == self._use_max_completion_tokens:
                        self._supports_token_limit = False
                    else:
                        self._use_max_completion_tokens = token_fallback
                    continue
                raise
        else:  # pragma: no cover - all supported fallbacks converge before this
            raise RuntimeError("AI optional-parameter compatibility fallback did not converge")
        return response.choices[0].message.content

    async def _do_request(
        self,
        *,
        system: str,
        user: str,
        temperature: float,
        max_tokens: int,
        include_temperature: bool,
        include_response_format: bool,
        include_token_limit: bool,
        use_max_completion_tokens: bool,
    ):
        request_kwargs = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        if include_token_limit:
            token_param = "max_completion_tokens" if use_max_completion_tokens else "max_tokens"
            request_kwargs[token_param] = max_tokens
        if include_temperature:
            request_kwargs["temperature"] = temperature
        if include_response_format:
            request_kwargs["response_format"] = {"type": "json_object"}
        if self.thinking:
            request_kwargs["extra_body"] = {"thinking": dict(self.thinking)}
        try:
            ensure_request_allowed()
            response = await self.client.chat.completions.create(**request_kwargs)
        except Exception:
            record_request(self.provider, model=self.model)
            raise
        usage = getattr(response, "usage", None)
        if usage is None:
            record_request(self.provider, model=self.model)
        else:
            details = getattr(usage, "prompt_tokens_details", None)
            record_request(
                self.provider,
                input_tokens=getattr(usage, "prompt_tokens", 0),
                output_tokens=getattr(usage, "completion_tokens", 0),
                model=self.model,
                cached_tokens=getattr(details, "cached_tokens", 0) if details else 0,
                input_cost_per_million_cny=self.config.input_cost_per_million_cny,
                output_cost_per_million_cny=self.config.output_cost_per_million_cny,
            )
        return response

    @staticmethod
    def _is_response_format_unsupported(message: str) -> bool:
        lowered = message.lower()
        return (
            "response_format" in lowered or "json mode" in lowered
        ) and any(
            marker in lowered
            for marker in ("not support", "unsupported", "unknown", "unrecognized", "invalid")
        )

    @staticmethod
    def _is_temperature_unsupported(message: str) -> bool:
        lowered = message.lower()
        return "temperature" in lowered and (
            "deprecated" in lowered
            or "not support" in lowered
            or "unsupported" in lowered
            or "invalid" in lowered
            or "fixed" in lowered
            or "must be" in lowered
        )

    @staticmethod
    def _is_thinking_control_unsupported(message: str) -> bool:
        lowered = message.lower()
        mentions_control = "extra_body" in lowered or "thinking" in lowered
        incompatibility = any(
            marker in lowered
            for marker in (
                "unexpected keyword",
                "not support",
                "unsupported",
                "unknown",
                "unrecognized",
                "invalid",
            )
        )
        return mentions_control and incompatibility

    @staticmethod
    def _is_max_tokens_unsupported(message: str) -> bool:
        lowered = message.lower()
        return "max_tokens" in lowered and "max_completion_tokens" in lowered

    @staticmethod
    def _token_fallback_mode(message: str) -> Optional[bool]:
        """Return desired token parameter, or the current mode when it should be omitted."""
        lowered = message.lower()
        rejection = any(
            marker in lowered
            for marker in ("not support", "unsupported", "unknown", "unrecognized", "invalid")
        )
        if "max_tokens" in lowered and "max_completion_tokens" in lowered:
            if "max_completion_tokens" in lowered and (
                "use max_completion_tokens" in lowered or "instead" in lowered
            ):
                return True
            if "use max_tokens" in lowered:
                return False
            return True
        if "max_completion_tokens" in lowered and rejection:
            return True
        if "max_tokens" in lowered and rejection:
            return False
        return None


class AzureOpenAIClient(AIClient):
    """Client for Azure OpenAI deployments.

    Uses the native AsyncAzureOpenAI client, which requires the deployment
    name (passed as `model`), azure_endpoint (resource base URL), and
    api_version. The deployment path is assembled internally by the SDK.
    """

    # Newer reasoning-series models reject legacy `max_tokens` and require
    # `max_completion_tokens` instead. Azure uses deployment names as `model`,
    # so a best-effort guess can be wrong for custom deployment aliases.
    _MODELS_REQUIRING_MAX_COMPLETION_TOKENS = ("o1", "o3", "o4", "gpt-5")

    def __init__(self, config: AIConfig):
        """Initialize Azure OpenAI client.

        Args:
            config: AI configuration
        """
        self.config = config

        api_key = _resolve_api_key(config)
        if not config.azure_endpoint_env:
            raise ValueError("azure_endpoint_env is required for azure provider")
        azure_endpoint = os.getenv(config.azure_endpoint_env)
        if not azure_endpoint:
            raise ValueError(f"Missing Azure endpoint: {config.azure_endpoint_env}")
        if not config.api_version:
            raise ValueError("api_version is required for azure provider")

        self.client = AsyncAzureOpenAI(
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=config.api_version,
        )
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
        self._use_max_completion_tokens = any(
            config.model.startswith(prefix)
            for prefix in self._MODELS_REQUIRING_MAX_COMPLETION_TOKENS
        )

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion using Azure OpenAI.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            str: Generated text
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        try:
            response = await self._create_completion(
                system=system,
                user=user,
                temperature=temperature,
                max_tokens=max_tokens,
                use_max_completion_tokens=self._use_max_completion_tokens,
            )
        except Exception as exc:
            fallback = self._token_fallback_mode(str(exc))
            if fallback is None:
                raise

            self._use_max_completion_tokens = fallback
            response = await self._create_completion(
                system=system,
                user=user,
                temperature=temperature,
                max_tokens=max_tokens,
                use_max_completion_tokens=fallback,
            )

        usage = getattr(response, "usage", None)
        if usage is not None:
            record_request(
                "openai",
                input_tokens=getattr(usage, "prompt_tokens", 0),
                output_tokens=getattr(usage, "completion_tokens", 0),
                model=self.model,
                input_cost_per_million_cny=self.config.input_cost_per_million_cny,
                output_cost_per_million_cny=self.config.output_cost_per_million_cny,
            )
        else:
            record_request("openai", model=self.model)
        return response.choices[0].message.content

    async def _create_completion(
        self,
        *,
        system: str,
        user: str,
        temperature: float,
        max_tokens: int,
        use_max_completion_tokens: bool,
    ):
        tokens_kwarg = (
            {"max_completion_tokens": max_tokens}
            if use_max_completion_tokens
            else {"max_tokens": max_tokens}
        )
        ensure_request_allowed()
        return await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            response_format={"type": "json_object"},
            **tokens_kwarg,
        )

    @staticmethod
    def _token_fallback_mode(message: str) -> Optional[bool]:
        lowered = message.lower()
        if "max_completion_tokens" in lowered and "max_tokens" in lowered:
            return True
        if "max_tokens" in lowered and "max_completion_tokens" not in lowered:
            return False
        return None


class GeminiClient(AIClient):
    """Client for Google Gemini models."""

    def __init__(self, config: AIConfig):
        """Initialize Gemini client.

        Args:
            config: AI configuration
        """
        self.config = config

        api_key = _resolve_api_key(config)

        self.client = genai.Client(api_key=api_key)
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion using Gemini.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            str: Generated text
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        ensure_request_allowed()
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=user,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
                max_output_tokens=max_tokens,
                response_mime_type="application/json"
            )
        )
        usage = getattr(response, "usage_metadata", None)
        if usage is not None:
            total = getattr(usage, "total_token_count", 0) or 0
            prompt = getattr(usage, "prompt_token_count", 0) or 0
            completion = max(0, total - prompt)
            record_request(
                "gemini",
                input_tokens=prompt,
                output_tokens=completion,
                model=self.model,
                input_cost_per_million_cny=self.config.input_cost_per_million_cny,
                output_cost_per_million_cny=self.config.output_cost_per_million_cny,
            )
        else:
            record_request("gemini", model=self.model)
        return response.text


def _uses_anthropic_compatible_api(config: AIConfig) -> bool:
    """Return whether MiniMax is configured for its Anthropic-compatible API."""
    base_url = (config.base_url or "").rstrip("/")
    return config.provider == AIProvider.MINIMAX and base_url.endswith("/anthropic")


def _create_single_client(config: AIConfig) -> AIClient:
    """Create a single AI client instance."""
    if (
        config.provider == AIProvider.ANTHROPIC
        or _uses_anthropic_compatible_api(config)
    ):
        return AnthropicClient(config)
    elif config.provider == AIProvider.AZURE:
        return AzureOpenAIClient(config)
    elif config.provider == AIProvider.GEMINI:
        return GeminiClient(config)
    elif config.provider in {
        AIProvider.OPENAI,
        AIProvider.ALI,
        AIProvider.DOUBAO,
        AIProvider.MINIMAX,
        AIProvider.DEEPSEEK,
        AIProvider.OLLAMA,
    }:
        return OpenAIClient(config)
    else:
        raise ValueError(f"Unsupported AI provider: {config.provider}")


class ChainedAIClient(AIClient):
    """Chain multiple AI clients with automatic fallback.

    When a provider fails with a retryable error (rate limit, auth/quota,
    service unavailable, or empty response), automatically falls back to
    the next provider in the chain.

    Clients are created lazily so that missing API keys for downstream
    providers do not block startup when the primary provider works.
    """

    def __init__(
        self,
        configs: List[AIConfig],
        clients: Optional[List[AIClient]] = None,
        client_factory: Optional[Any] = None,
    ):
        self.configs = configs
        self._client_factory = client_factory or _create_single_client
        self._client_cache: Dict[int, AIClient] = {}
        # Allow tests to inject pre-built clients directly
        if clients is not None:
            for idx, client in enumerate(clients):
                self._client_cache[idx] = client

    def _get_client(self, index: int) -> AIClient:
        if index not in self._client_cache:
            self._client_cache[index] = self._client_factory(self.configs[index])
        return self._client_cache[index]

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        last_error: Optional[Exception] = None
        for i in range(len(self.configs)):
            try:
                client = self._get_client(i)
                result = await client.complete(system, user, temperature, max_tokens)
                if not result or not result.strip():
                    raise ValueError("Empty response from provider")
                return result
            except Exception as exc:
                if not self._should_fallback(exc):
                    raise
                last_error = exc
                if i < len(self.configs) - 1:
                    rich_print(
                        f"\n[yellow]Provider {self.configs[i].provider.value} failed ({exc}), "
                        f"falling back to {self.configs[i + 1].provider.value}...[/yellow]"
                    )
        raise RuntimeError(f"All providers failed. Last error: {last_error}")

    @staticmethod
    def _should_fallback(exc: Exception) -> bool:
        """Determine if an error warrants fallback to the next provider."""
        msg = str(exc).lower()
        if "429" in msg or "rate limit" in msg:
            return True
        if "401" in msg or "403" in msg or "quota" in msg or "exceeded" in msg:
            return True
        if "502" in msg or "503" in msg or "service unavailable" in msg:
            return True
        if "empty response" in msg:
            return True
        return False


def _create_chained_client(config: AIConfig) -> ChainedAIClient:
    """Build a ChainedAIClient from a comma-separated provider chain."""
    provider_chain = config.provider_chain or ""
    provider_names = [p.strip() for p in provider_chain.split(",") if p.strip()]
    if not provider_names:
        raise ValueError("provider_chain is empty")

    chain_configs: List[AIConfig] = []
    for name in provider_names:
        try:
            provider = AIProvider(name)
        except ValueError:
            raise ValueError(f"Unsupported AI provider in chain: {name}")

        defaults = AI_PROVIDER_DEFAULTS.get(provider, {})
        base_url = config.base_url if provider == config.provider else defaults.get("base_url")
        cfg = AIConfig(
            provider=provider,
            model=defaults.get("model", config.model),
            api_key_env=defaults.get("api_key_env", config.api_key_env),
            base_url=base_url,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            throttle_sec=config.throttle_sec,
            analysis_concurrency=config.analysis_concurrency,
            enrichment_concurrency=config.enrichment_concurrency,
            languages=config.languages,
            azure_endpoint_env=(
                config.azure_endpoint_env or defaults.get("azure_endpoint_env")
                if provider == AIProvider.AZURE
                else None
            ),
            api_version=(
                config.api_version or defaults.get("api_version")
                if provider == AIProvider.AZURE
                else None
            ),
        )
        chain_configs.append(cfg)

    return ChainedAIClient(chain_configs)


def create_ai_client(config: AIConfig) -> AIClient:
    """Factory function to create appropriate AI client.

    Args:
        config: AI configuration

    Returns:
        AIClient: Initialized AI client

    Raises:
        ValueError: If provider is not supported
    """
    if config.provider_chain:
        return _create_chained_client(config)
    return _create_single_client(config)
