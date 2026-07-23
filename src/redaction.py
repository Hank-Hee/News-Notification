"""Helpers for keeping credentials out of logs and error messages."""

from __future__ import annotations

import os
import re
from collections.abc import Iterable


_AUTH_HEADER_RE = re.compile(
    r"(?i)\b(authorization|api[-_ ]?key)\b\s*[:=]\s*([^\s,;]+)"
)


def redact_secrets(message: object, extra_values: Iterable[str] = ()) -> str:
    """Return a log-safe representation with likely credential values removed."""
    text = str(message)
    values = {
        value
        for name, value in os.environ.items()
        if value
        and len(value) >= 6
        and any(marker in name.upper() for marker in ("KEY", "TOKEN", "SECRET", "PASSWORD"))
    }
    values.update(value for value in extra_values if value and len(value) >= 6)
    for value in sorted(values, key=len, reverse=True):
        text = text.replace(value, "[REDACTED]")
    return _AUTH_HEADER_RE.sub(lambda match: f"{match.group(1)}: [REDACTED]", text)


def is_fatal_ai_error(error: BaseException) -> bool:
    """Return whether an AI failure must abort instead of producing a fake digest."""
    message = str(error).lower()
    fatal_markers = (
        "401",
        "402",
        "authentication",
        "unauthorized",
        "invalid api key",
        "incorrect api key",
        "insufficient_quota",
        "quota exceeded",
        "billing",
        "payment required",
        "error code: 400",
        "badrequesterror",
        "invalid_request_error",
        "kimi thinking disablement",
        "kimi json mode was rejected",
        "kimi rejected max_completion_tokens",
    )
    return any(marker in message for marker in fatal_markers)
