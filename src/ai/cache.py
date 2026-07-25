"""Persistent, stage-aware cache for validated AI analysis results."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Optional

from .._file_utils import _atomic_write_text
from ..models import ContentItem


_SPACE_RE = re.compile(r"\s+")


def _normalize(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or ""))
    return _SPACE_RE.sub(" ", text).strip().casefold()


class AnalysisCache:
    """Load, query, and atomically persist successful model outputs."""

    def __init__(
        self,
        path: str | Path = "data/history/analysis_cache.json",
        *,
        enabled: bool = True,
        max_records: int = 5000,
    ) -> None:
        self.path = Path(path)
        self.enabled = enabled
        self.max_records = max_records
        self.records: dict[str, dict[str, Any]] = {}
        self.dirty = False

    def load(self) -> "AnalysisCache":
        if not self.enabled:
            return self
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            records = payload.get("entries", payload) if isinstance(payload, dict) else {}
            if isinstance(records, dict):
                self.records = {
                    str(key): value
                    for key, value in records.items()
                    if isinstance(value, dict) and isinstance(value.get("result"), dict)
                }
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            self.records = {}
        return self

    @staticmethod
    def key(
        item: ContentItem,
        *,
        stage: str,
        model_id: str,
        prompt_version: str,
    ) -> str:
        material = "\n".join(
            (
                _normalize(item.url),
                _normalize(item.title),
                _normalize(item.content),
                _normalize(stage),
                _normalize(model_id),
                _normalize(prompt_version),
            )
        )
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def get(
        self,
        item: ContentItem,
        *,
        stage: str,
        model_id: str,
        prompt_version: str,
    ) -> Optional[dict[str, Any]]:
        if not self.enabled:
            return None
        cache_key = self.key(
            item,
            stage=stage,
            model_id=model_id,
            prompt_version=prompt_version,
        )
        entry = self.records.get(cache_key)
        result = entry.get("result") if isinstance(entry, dict) else None
        return dict(result) if isinstance(result, dict) else None

    def put(
        self,
        item: ContentItem,
        result: dict[str, Any],
        *,
        stage: str,
        model_id: str,
        prompt_version: str,
    ) -> None:
        if not self.enabled or not result:
            return
        cache_key = self.key(
            item,
            stage=stage,
            model_id=model_id,
            prompt_version=prompt_version,
        )
        self.records[cache_key] = {
            "stage": stage,
            "model": model_id,
            "prompt_version": prompt_version,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "result": result,
        }
        self.dirty = True

    def save(self) -> None:
        if not self.enabled or not self.dirty:
            return
        if len(self.records) > self.max_records:
            ordered = sorted(
                self.records.items(),
                key=lambda pair: str(pair[1].get("created_at", "")),
                reverse=True,
            )
            self.records = dict(ordered[: self.max_records])
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": 1, "entries": self.records}
        _atomic_write_text(
            self.path,
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        self.dirty = False
