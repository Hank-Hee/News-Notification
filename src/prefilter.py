"""Deterministic first-stage filtering before any AI request."""

from __future__ import annotations

import html
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .models import ContentItem, FilteringConfig, SourceType


_TRACKING_NAMES = {
    "fbclid", "gclid", "mc_cid", "mc_eid", "msclkid", "ref", "source",
}
_AI_TERMS = {
    " ai ", "agent", "artificial intelligence", "llm", "large language model",
    "machine learning", "deep learning", "neural", "transformer", "reasoning",
    "multimodal", "rag", "mcp", "inference", "embedding", "computer vision",
    "speech model", "language model", "openai", "anthropic", "deepmind", "gemini",
    "chatgpt", "claude", "copilot", "generative ai", "ai-powered", "ai product",
    "automation", "voice agent", "vibe coding", "computer use",
    "meta ai", "llama", "mistral", "hugging face", "huggingface", "kimi",
    "moonshot", "deepseek", "qwen", "glm", "autogen", "semantic kernel", "vllm",
    "transformers", "通义", "千问", "豆包", "文心", "混元", "智谱",
    "minimax", "阶跃星辰", "零一万物", "人工智能", "大模型", "智能体",
    "机器学习", "深度学习", "推理模型", "多模态", "知识库", "具身智能",
    "智能产品", "智能助手", "工作流自动化", "生成式", "人工智能产品",
}
_TITLE_TOKEN_RE = re.compile(r"[^\w\u3400-\u9fff]+", re.UNICODE)


@dataclass
class PrefilterStats:
    total: int = 0
    dropped_outside_window: int = 0
    dropped_missing_identity: int = 0
    dropped_too_short: int = 0
    dropped_non_ai: int = 0
    dropped_low_engagement: int = 0
    duplicate_url: int = 0
    duplicate_title: int = 0
    source_limited: int = 0
    candidate_limited: int = 0
    kept: int = 0

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass
class PrefilterResult:
    items: list[ContentItem]
    stats: PrefilterStats


def normalize_title(title: str) -> str:
    """Create a conservative exact-title identity key."""
    return _TITLE_TOKEN_RE.sub(" ", html.unescape(title).casefold()).strip()


def clean_url(url: str) -> str:
    """Remove common tracking parameters while preserving meaningful query data."""
    parsed = urlsplit(url.strip())
    query = [
        (name, value)
        for name, value in parse_qsl(parsed.query, keep_blank_values=True)
        if not name.casefold().startswith("utm_")
        and name.casefold() not in _TRACKING_NAMES
    ]
    host = (parsed.hostname or "").casefold()
    if parsed.port and not (
        (parsed.scheme.casefold() == "https" and parsed.port == 443)
        or (parsed.scheme.casefold() == "http" and parsed.port == 80)
    ):
        host = f"{host}:{parsed.port}"
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.casefold(), host, path, urlencode(query), ""))


def _is_ai_related(item: ContentItem) -> bool:
    metadata = item.metadata
    haystack = " ".join(
        str(value)
        for value in (
            item.title,
            (item.content or "")[:1500],
            metadata.get("category", ""),
            metadata.get("description", ""),
            metadata.get("collection_names", ""),
            metadata.get("gn_query", ""),
        )
    ).casefold()
    padded = f" {haystack} "
    return any(term in padded for term in _AI_TERMS)


def _is_low_engagement(item: ContentItem, threshold: int) -> bool:
    if item.source_type not in {SourceType.HACKERNEWS, SourceType.REDDIT}:
        return False
    raw = item.metadata.get("score", 0)
    try:
        return int(raw or 0) < threshold
    except (TypeError, ValueError):
        return True


def _source_key(item: ContentItem) -> str:
    metadata = item.metadata
    subsource = (
        metadata.get("feed_name")
        or metadata.get("source_name")
        or metadata.get("twitter_handle")
        or metadata.get("subreddit")
        or metadata.get("repo")
        or metadata.get("domain")
        or item.source_type.value
    )
    return f"{item.source_type.value}:{subsource}"


def prefilter_items(
    items: Iterable[ContentItem],
    *,
    since: datetime,
    config: FilteringConfig,
) -> PrefilterResult:
    """Apply the 24h/rule/dedup/source-cap/candidate-cap stage."""
    stats = PrefilterStats()
    candidates: list[ContentItem] = []
    seen_urls: dict[str, int] = {}
    seen_titles: dict[str, int] = {}
    source_counts: Counter[str] = Counter()
    if since.tzinfo is None:
        since = since.replace(tzinfo=timezone.utc)

    ordered_items = list(items)
    if config.source_priority:
        priority = {
            source_name: index
            for index, source_name in enumerate(config.source_priority)
        }
        ordered_items.sort(
            key=lambda item: priority.get(item.source_type.value, len(priority))
        )

    for original in ordered_items:
        stats.total += 1
        title = (original.title or "").strip()
        url = str(original.url).strip() if original.url else ""
        if not title or not url:
            stats.dropped_missing_identity += 1
            continue
        published_at = original.published_at
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)
        if published_at < since:
            stats.dropped_outside_window += 1
            continue
        content = (original.content or "").strip()
        if len(title) < 12 and len(content) < config.min_content_chars:
            stats.dropped_too_short += 1
            continue
        if not _is_ai_related(original):
            stats.dropped_non_ai += 1
            continue
        if _is_low_engagement(original, config.community_min_score):
            stats.dropped_low_engagement += 1
            continue

        normalized_url = clean_url(url)
        normalized_title = normalize_title(title)
        if normalized_url in seen_urls:
            stats.duplicate_url += 1
            existing = candidates[seen_urls[normalized_url]]
            if len(content) > len(existing.content or ""):
                replacement = original.model_copy(deep=True)
                replacement.metadata["normalized_url"] = normalized_url
                candidates[seen_urls[normalized_url]] = replacement
            continue
        if normalized_title and normalized_title in seen_titles:
            stats.duplicate_title += 1
            existing = candidates[seen_titles[normalized_title]]
            if len(content) > len(existing.content or ""):
                replacement = original.model_copy(deep=True)
                replacement.metadata["normalized_url"] = normalized_url
                candidates[seen_titles[normalized_title]] = replacement
            continue

        source_key = _source_key(original)
        if source_counts[source_key] >= config.per_source_limit:
            stats.source_limited += 1
            continue
        if len(candidates) >= config.candidate_limit:
            stats.candidate_limited += 1
            continue

        item = original.model_copy(deep=True)
        item.metadata["normalized_url"] = normalized_url
        item.metadata["normalized_title"] = normalized_title
        seen_urls[normalized_url] = len(candidates)
        if normalized_title:
            seen_titles[normalized_title] = len(candidates)
        source_counts[source_key] += 1
        candidates.append(item)

    stats.kept = len(candidates)
    return PrefilterResult(items=candidates, stats=stats)
