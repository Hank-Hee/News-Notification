"""Lightweight token usage tracker shared across AI clients.

This module keeps a simple in-memory counter of tokens used during a single
Horizon run, so the orchestrator can print a summary at the end.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Dict, Iterator, Optional


@dataclass
class ProviderUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    requests: int = 0
    usage_reported_requests: int = 0
    cached_tokens: int = 0
    estimated_cost_cny: float = 0.0

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class TokenUsageSnapshot:
    total_input_tokens: int
    total_output_tokens: int
    per_provider: Dict[str, ProviderUsage] = field(default_factory=dict)
    requests_by_stage: Dict[str, int] = field(default_factory=dict)
    per_route: Dict[str, ProviderUsage] = field(default_factory=dict)
    cache_hits_by_stage: Dict[str, int] = field(default_factory=dict)
    retries_by_stage: Dict[str, int] = field(default_factory=dict)
    validation_failures_by_stage: Dict[str, int] = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    @property
    def total_requests(self) -> int:
        return sum(usage.requests for usage in self.per_provider.values())

    @property
    def usage_reported_requests(self) -> int:
        return sum(usage.usage_reported_requests for usage in self.per_provider.values())

    @property
    def estimated_cost_cny(self) -> float:
        return sum(usage.estimated_cost_cny for usage in self.per_provider.values())

    @property
    def total_cache_hits(self) -> int:
        return sum(self.cache_hits_by_stage.values())


_provider_usage: Dict[str, ProviderUsage] = {}
_route_usage: Dict[str, ProviderUsage] = {}
_requests_by_stage: Dict[str, int] = {}
_cache_hits_by_stage: Dict[str, int] = {}
_retries_by_stage: Dict[str, int] = {}
_validation_failures_by_stage: Dict[str, int] = {}
_current_stage: ContextVar[str] = ContextVar("horizon_ai_stage", default="other")
_max_requests: Optional[int] = None
_max_cost_cny: Optional[float] = None


class AIRequestBudgetExceeded(RuntimeError):
    """Raised before a request that would exceed the configured safety valve."""


def _nonnegative_number(value: object) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return 0.0
    return max(0.0, float(value))


def configure_usage_limits(*, max_requests: int, max_cost_cny: float) -> None:
    global _max_requests, _max_cost_cny
    _max_requests = max_requests
    _max_cost_cny = max_cost_cny


def ensure_request_allowed() -> None:
    snapshot = get_usage_snapshot()
    if _max_requests is not None and snapshot.total_requests >= _max_requests:
        raise AIRequestBudgetExceeded(
            f"AI request limit reached ({snapshot.total_requests}/{_max_requests})"
        )
    if _max_cost_cny is not None and snapshot.estimated_cost_cny >= _max_cost_cny:
        raise AIRequestBudgetExceeded(
            "Estimated AI cost limit reached "
            f"(¥{snapshot.estimated_cost_cny:.4f}/¥{_max_cost_cny:.4f})"
        )


@contextmanager
def usage_stage(stage: str) -> Iterator[None]:
    """Attribute AI calls in this context to a named pipeline stage."""
    token = _current_stage.set(stage)
    try:
        yield
    finally:
        _current_stage.reset(token)


def record_request(
    provider: str,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    *,
    model: str = "unknown",
    cached_tokens: int = 0,
    input_cost_per_million_cny: float = 0.0,
    output_cost_per_million_cny: float = 0.0,
) -> None:
    """Record one completed provider request and optional reported usage."""
    usage = _provider_usage.setdefault(provider, ProviderUsage())
    usage.requests += 1
    stage = _current_stage.get()
    _requests_by_stage[stage] = _requests_by_stage.get(stage, 0) + 1
    route_key = f"{stage} / {provider} / {model}"
    route = _route_usage.setdefault(route_key, ProviderUsage())
    route.requests += 1
    if input_tokens is not None or output_tokens is not None:
        usage.usage_reported_requests += 1
        usage.input_tokens += max(0, input_tokens or 0)
        usage.output_tokens += max(0, output_tokens or 0)
        route.usage_reported_requests += 1
        route.input_tokens += max(0, input_tokens or 0)
        route.output_tokens += max(0, output_tokens or 0)
    cached = int(_nonnegative_number(cached_tokens))
    usage.cached_tokens += cached
    route.cached_tokens += cached
    cost = (
        _nonnegative_number(input_tokens) * input_cost_per_million_cny
        + _nonnegative_number(output_tokens) * output_cost_per_million_cny
    ) / 1_000_000
    usage.estimated_cost_cny += cost
    route.estimated_cost_cny += cost


def record_cache_hit(stage: str) -> None:
    _cache_hits_by_stage[stage] = _cache_hits_by_stage.get(stage, 0) + 1


def record_retry(stage: str) -> None:
    _retries_by_stage[stage] = _retries_by_stage.get(stage, 0) + 1


def record_validation_failure(stage: str) -> None:
    _validation_failures_by_stage[stage] = (
        _validation_failures_by_stage.get(stage, 0) + 1
    )


def record_usage(provider: str, input_tokens: int = 0, output_tokens: int = 0) -> None:
    """Accumulate token usage for a given provider.

    Args:
        provider: Provider identifier, e.g. "openai", "anthropic".
        input_tokens: Prompt / input tokens used.
        output_tokens: Completion / output tokens used.
    """
    if input_tokens <= 0 and output_tokens <= 0:
        return

    usage = _provider_usage.setdefault(provider, ProviderUsage())
    usage.input_tokens += max(0, input_tokens)
    usage.output_tokens += max(0, output_tokens)


def get_usage_snapshot() -> TokenUsageSnapshot:
    """Return a snapshot of accumulated token usage."""
    total_in = sum(u.input_tokens for u in _provider_usage.values())
    total_out = sum(u.output_tokens for u in _provider_usage.values())
    return TokenUsageSnapshot(
        total_input_tokens=total_in,
        total_output_tokens=total_out,
        per_provider=dict(_provider_usage),
        requests_by_stage=dict(_requests_by_stage),
        per_route=dict(_route_usage),
        cache_hits_by_stage=dict(_cache_hits_by_stage),
        retries_by_stage=dict(_retries_by_stage),
        validation_failures_by_stage=dict(_validation_failures_by_stage),
    )


def reset_usage() -> None:
    """Reset all accumulated usage (useful for tests)."""
    global _max_requests, _max_cost_cny
    _provider_usage.clear()
    _route_usage.clear()
    _requests_by_stage.clear()
    _cache_hits_by_stage.clear()
    _retries_by_stage.clear()
    _validation_failures_by_stage.clear()
    _max_requests = None
    _max_cost_cny = None
