"""Persistent, GitHub Pages-friendly AI product intelligence database."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

from ._file_utils import _atomic_write_text
from .models import ContentItem, ProductIntelligenceConfig


_UNKNOWN = {"", "未公开", "未知", "不适用", "none", "null", "n/a"}
_LIST_FIELDS = (
    "usage_flow",
    "learning_points",
    "verticals",
    "tags",
)
_LEGACY_FIELDS_TO_DROP = {
    "original_workflow",
    "product_workflow",
    "input_process_output",
    "tool_stack",
    "business_model",
    "product_stage",
    "traction_evidence",
    "market_reaction",
    "transferable_lessons",
    "mvp_path",
    "skill_signals",
    "product_signal",
    "market_signal",
    "builder_insight",
}
_CSV_FIELDS = (
    "product_id",
    "product_name",
    "builder_name",
    "first_seen",
    "last_seen",
    "occurrence_count",
    "intelligence_type",
    "evidence_status",
    "target_user",
    "user_problem",
    "what_it_is",
    "usage_flow",
    "ai_role",
    "implementation_idea",
    "learning_points",
    "hands_on_exercise",
    "limitations_or_uncertainties",
    "verticals",
    "region",
    "score",
    "tags",
    "title",
    "url",
)


def _is_known(value: object) -> bool:
    return str(value or "").strip().casefold() not in _UNKNOWN


def _list_value(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(entry).strip() for entry in value if _is_known(entry)]


def _stable_product_id(product_name: str, builder_name: str) -> str:
    identity = unicodedata.normalize(
        "NFKC", f"{product_name}|{builder_name}"
    ).casefold()
    identity = re.sub(r"\s+", " ", identity).strip()
    return "product-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]


class ProductIntelligenceDatabase:
    """Load, upsert, export, and publish product intelligence records."""

    def __init__(self, config: ProductIntelligenceConfig):
        self.config = config
        self.json_path = Path(config.json_path)
        self.csv_path = Path(config.csv_path)
        self.publish_directory = Path(config.publish_directory)
        self.payload: dict[str, object] = {
            "version": 1,
            "updated_at": None,
            "products": [],
        }

    def load(self) -> "ProductIntelligenceDatabase":
        if not self.json_path.exists():
            return self
        try:
            raw = json.loads(self.json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return self
        if isinstance(raw, dict) and isinstance(raw.get("products"), list):
            for record in raw["products"]:
                if isinstance(record, dict):
                    for field in _LEGACY_FIELDS_TO_DROP:
                        record.pop(field, None)
            self.payload = raw
        return self

    @property
    def products(self) -> list[dict[str, object]]:
        products = self.payload.setdefault("products", [])
        return products if isinstance(products, list) else []

    def upsert(self, items: Iterable[ContentItem], observed_on: date) -> int:
        by_id = {
            str(record.get("product_id")): record
            for record in self.products
            if isinstance(record, dict) and record.get("product_id")
        }
        changed = 0
        for item in items:
            record = self._record_from_item(item, observed_on)
            if record is None:
                continue
            product_id = str(record["product_id"])
            existing = by_id.get(product_id)
            if existing is None:
                by_id[product_id] = record
                changed += 1
                continue
            self._merge_record(existing, record)
            changed += 1

        products = sorted(
            by_id.values(),
            key=lambda record: (
                str(record.get("last_seen", "")),
                float(record.get("score") or 0),
            ),
            reverse=True,
        )[: self.config.max_records]
        self.payload["products"] = products
        self.payload["updated_at"] = datetime.now(timezone.utc).isoformat()
        return changed

    def save_and_publish(self) -> tuple[Path, Path]:
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        self.publish_directory.mkdir(parents=True, exist_ok=True)

        json_text = json.dumps(self.payload, ensure_ascii=False, indent=2) + "\n"
        csv_text = self._render_csv()
        _atomic_write_text(self.json_path, json_text)
        _atomic_write_text(self.csv_path, csv_text)

        published_json = self.publish_directory / "product-intelligence.json"
        published_csv = self.publish_directory / "product-intelligence.csv"
        _atomic_write_text(published_json, json_text)
        _atomic_write_text(published_csv, csv_text)
        return published_json, published_csv

    def _record_from_item(
        self, item: ContentItem, observed_on: date
    ) -> dict[str, object] | None:
        metadata = item.metadata
        intelligence_type = str(metadata.get("intelligence_type") or "early_signal")
        product_name = str(metadata.get("product_name") or "").strip()
        if not _is_known(product_name):
            if intelligence_type != "product_case":
                return None
            product_name = str(metadata.get("title_zh") or item.title).strip()

        builder_name = str(metadata.get("builder_name") or item.author or "").strip()
        product_id = _stable_product_id(product_name, builder_name)
        observed = observed_on.isoformat()
        update_id = str(metadata.get("event_key") or item.id)
        source = {
            "url": str(item.url),
            "title": item.title,
            "source_type": item.source_type.value,
            "published_at": item.published_at.isoformat(),
        }
        sources = [source]
        known_source_urls = {str(item.url)}
        for candidate in [
            *(metadata.get("sources") or []),
            *(metadata.get("supplemental_sources") or []),
        ]:
            if not isinstance(candidate, dict):
                continue
            candidate_url = str(candidate.get("url") or "").strip()
            if not candidate_url or candidate_url in known_source_urls:
                continue
            sources.append(
                {
                    "url": candidate_url,
                    "title": str(candidate.get("title") or candidate_url),
                    "source_type": str(candidate.get("source_type") or "supplemental"),
                    "published_at": str(candidate.get("published_at") or ""),
                }
            )
            known_source_urls.add(candidate_url)
        record: dict[str, object] = {
            "product_id": product_id,
            "product_name": product_name,
            "builder_name": builder_name or "未公开",
            "first_seen": observed,
            "last_seen": observed,
            "occurrence_count": 1,
            "intelligence_type": intelligence_type,
            "evidence_status": metadata.get("evidence_status", "reported"),
            "target_user": metadata.get("target_user") or "未公开",
            "user_problem": metadata.get("user_problem") or "未公开",
            "what_it_is": metadata.get("what_it_is") or item.ai_summary or "",
            "ai_role": metadata.get("ai_role") or "未公开",
            "implementation_idea": metadata.get("implementation_idea") or "未公开",
            "hands_on_exercise": metadata.get("hands_on_exercise") or "未公开",
            "limitations_or_uncertainties": (
                metadata.get("limitations_or_uncertainties") or "未公开"
            ),
            "region": metadata.get("region", "global"),
            "score": item.ai_score,
            "summary": item.ai_summary or "",
            "title": metadata.get("title_zh") or item.title,
            "url": str(item.url),
            "sources": sources,
            "updates": [
                {
                    "update_id": update_id,
                    "date": observed,
                    "title": metadata.get("title_zh") or item.title,
                    "summary": item.ai_summary or "",
                    "score": item.ai_score,
                    "url": str(item.url),
                }
            ],
        }
        for field in _LIST_FIELDS:
            source_value = item.ai_tags if field == "tags" else metadata.get(field)
            record[field] = _list_value(source_value)
        return record

    def _merge_record(
        self, existing: dict[str, object], current: dict[str, object]
    ) -> None:
        existing["last_seen"] = current["last_seen"]
        updates = existing.setdefault("updates", [])
        known_updates = {
            str(update.get("update_id"))
            for update in updates
            if isinstance(update, dict)
        }
        current_updates = [
            update
            for update in current.get("updates", [])
            if isinstance(update, dict)
        ]
        has_new_update = any(
            str(update.get("update_id")) not in known_updates
            for update in current_updates
        )
        if has_new_update:
            existing["occurrence_count"] = int(existing.get("occurrence_count") or 0) + 1
        for key, value in current.items():
            if key in {"product_id", "first_seen", "occurrence_count", "sources", "updates"}:
                continue
            if isinstance(value, list):
                existing_values = _list_value(existing.get(key))
                existing[key] = list(dict.fromkeys([*existing_values, *value]))
            elif isinstance(value, dict):
                if value:
                    existing[key] = value
            elif _is_known(value):
                existing[key] = value

        sources = existing.setdefault("sources", [])
        known_urls = {
            str(source.get("url"))
            for source in sources
            if isinstance(source, dict)
        }
        for source in current.get("sources", []):
            if isinstance(source, dict) and str(source.get("url")) not in known_urls:
                sources.append(source)

        for update in current_updates:
            if isinstance(update, dict) and str(update.get("update_id")) not in known_updates:
                updates.append(update)
        existing["updates"] = updates[-self.config.max_updates_per_product :]

    def _render_csv(self) -> str:
        buffer = io.StringIO(newline="")
        writer = csv.DictWriter(buffer, fieldnames=_CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for record in self.products:
            row = dict(record)
            for field in _LIST_FIELDS:
                row[field] = " | ".join(_list_value(row.get(field)))
            writer.writerow(row)
        return buffer.getvalue()
