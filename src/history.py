"""Lightweight seven-day event index for cross-run deduplication."""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from ._file_utils import _atomic_write_text
from .models import ContentItem
from .prefilter import normalize_title


def _normalize_url(value: object) -> str:
    return str(value or "").strip().rstrip("/").casefold()


def _content_hash(item: ContentItem) -> str:
    normalized = " ".join(str(item.content or "").split()).casefold()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest() if normalized else ""


@dataclass
class HistoryFilterResult:
    items: list[ContentItem]
    excluded: int = 0
    allowed_updates: int = 0


class EventHistoryIndex:
    """Read, filter, and atomically persist a small event index."""

    def __init__(self, path: str | Path = "data/history/event_index.json") -> None:
        self.path = Path(path)
        self.records: dict[str, dict[str, object]] = {}

    def load(self) -> "EventHistoryIndex":
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            records = raw.get("events", raw) if isinstance(raw, dict) else {}
            if isinstance(records, dict):
                self.records = {
                    str(key): value
                    for key, value in records.items()
                    if isinstance(value, dict)
                }
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            self.records = {}
        return self

    @staticmethod
    def event_key(item: ContentItem) -> str:
        candidate = str(item.metadata.get("event_key") or "").strip().casefold()
        return candidate or normalize_title(item.title)

    def filter_recent(
        self,
        items: list[ContentItem],
        *,
        today: date | None = None,
        days: int = 7,
    ) -> HistoryFilterResult:
        if days <= 0:
            return HistoryFilterResult(items=list(items))
        today = today or datetime.now(timezone.utc).date()
        cutoff = today - timedelta(days=days)
        kept: list[ContentItem] = []
        excluded = 0
        allowed_updates = 0

        for item in items:
            key = self.event_key(item)
            normalized_title = normalize_title(item.title)
            normalized_url = _normalize_url(item.url)
            record = self.records.get(key)
            if not record:
                record = next(
                    (
                        candidate
                        for candidate_key, candidate in self.records.items()
                        if candidate_key == normalized_title
                        or str(candidate.get("normalized_title") or "") == normalized_title
                        or str(candidate.get("normalized_url") or "") == normalized_url
                        or str(candidate.get("source_id") or "") == item.id
                    ),
                    None,
                )
            if not record:
                kept.append(item)
                continue
            try:
                last_seen = date.fromisoformat(str(record.get("last_seen")))
            except (TypeError, ValueError):
                kept.append(item)
                continue
            if last_seen < cutoff:
                kept.append(item)
                continue
            previous_hash = str(record.get("content_hash") or "")
            current_hash = _content_hash(item)
            if bool(item.metadata.get("has_substantive_update")) or (
                previous_hash and current_hash and previous_hash != current_hash
            ):
                allowed_updates += 1
                item.metadata["has_substantive_update"] = True
                kept.append(item)
                continue
            excluded += 1

        return HistoryFilterResult(
            items=kept,
            excluded=excluded,
            allowed_updates=allowed_updates,
        )

    def update(self, items: list[ContentItem], *, today: date | None = None) -> None:
        today = today or datetime.now(timezone.utc).date()
        today_text = today.isoformat()
        for item in items:
            key = self.event_key(item)
            if not key:
                continue
            existing = self.records.get(key, {})
            first_seen = str(existing.get("first_seen") or today_text)
            self.records[key] = {
                "event_key": key,
                "title": item.title,
                "first_seen": first_seen,
                "last_seen": today_text,
                "url": str(item.url),
                "normalized_url": _normalize_url(item.url),
                "normalized_title": normalize_title(item.title),
                "source_id": item.id,
                "content_hash": _content_hash(item),
                "latest_update": item.ai_summary or item.title,
            }

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": 1, "events": self.records}
        _atomic_write_text(
            self.path,
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
