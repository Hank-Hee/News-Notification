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

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class TokenUsageSnapshot:
    total_input_tokens: int
    total_output_tokens: int
    per_provider: Dict[str, ProviderUsage] = field(default_factory=dict)
    requests_by_stage: Dict[str, int] = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    @property
    def total_requests(self) -> int:
        return sum(usage.requests for usage in self.per_provider.values())

    @property
    def usage_reported_requests(self) -> int:
        return sum(usage.usage_reported_requests for usage in self.per_provider.values())


_provider_usage: Dict[str, ProviderUsage] = {}
_requests_by_stage: Dict[str, int] = {}
_current_stage: ContextVar[str] = ContextVar("horizon_ai_stage", default="other")


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
) -> None:
    """Record one completed provider request and optional reported usage."""
    usage = _provider_usage.setdefault(provider, ProviderUsage())
    usage.requests += 1
    stage = _current_stage.get()
    _requests_by_stage[stage] = _requests_by_stage.get(stage, 0) + 1
    if input_tokens is not None or output_tokens is not None:
        usage.usage_reported_requests += 1
        usage.input_tokens += max(0, input_tokens or 0)
        usage.output_tokens += max(0, output_tokens or 0)


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
    )


def reset_usage() -> None:
    """Reset all accumulated usage (useful for tests)."""
    _provider_usage.clear()
    _requests_by_stage.clear()
