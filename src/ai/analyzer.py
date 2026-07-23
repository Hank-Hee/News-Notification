"""Structured, batched AI scoring for the personal daily pipeline."""

from __future__ import annotations

import asyncio
import json
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ValidationError, model_validator
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn
from tenacity import retry, stop_after_attempt, wait_exponential

from .client import AIClient
from .prompts import (
    BATCH_CONTENT_ANALYSIS_USER,
    CONTENT_ANALYSIS_SYSTEM,
    CONTENT_ANALYSIS_USER,
)
from .tokens import usage_stage
from .utils import parse_json_response
from ..models import ContentItem
from ..redaction import is_fatal_ai_error, redact_secrets


DEFAULT_THROTTLE_SEC = 0.0


class AnalysisResult(BaseModel):
    """Validated per-item scoring result returned by the model."""

    id: Optional[str] = None
    score: float = Field(ge=0, le=10, allow_inf_nan=False)
    category: Literal["tech", "product"] = "tech"
    region: Literal["china", "global"] = "global"
    source_tier: int = Field(default=5, ge=1, le=5)
    is_first_party: bool = False
    is_new_event: bool = True
    has_substantive_update: bool = False
    is_promotional: bool = False
    event_key: str = ""
    reason: str
    summary_zh: Optional[str] = None
    summary: Optional[str] = None
    tags: list[str]
    follow_up: str = ""
    github_project: Optional[dict] = None

    @model_validator(mode="after")
    def require_summary(self) -> "AnalysisResult":
        if not (self.summary_zh or self.summary):
            raise ValueError("summary_zh is required")
        return self


class ContentAnalyzer:
    """Scores items in validated batches with recursive parsing fallback."""

    def __init__(self, ai_client: AIClient):
        self.client = ai_client

    @staticmethod
    def _parse_json_response(response: str) -> Optional[dict]:
        return parse_json_response(response)

    def _get_throttle_sec(self) -> float:
        config = getattr(self.client, "config", None)
        return max(getattr(config, "throttle_sec", DEFAULT_THROTTLE_SEC), 0.0)

    def _get_concurrency(self) -> int:
        config = getattr(self.client, "config", None)
        return max(getattr(config, "analysis_concurrency", 1), 1)

    def _get_batch_size(self) -> int:
        config = getattr(self.client, "config", None)
        return max(1, min(getattr(config, "analysis_batch_size", 1), 20))

    async def analyze_batch(self, items: List[ContentItem]) -> List[ContentItem]:
        if not items:
            return []
        batch_size = self._get_batch_size()
        if batch_size <= 1:
            return await self._analyze_singly(items)

        chunks = [items[index : index + batch_size] for index in range(0, len(items), batch_size)]
        semaphore = asyncio.Semaphore(self._get_concurrency())

        async def process(chunk: list[ContentItem], progress_task: int) -> None:
            async with semaphore:
                await self._analyze_with_fallback(chunk)
            progress.advance(progress_task, advance=len(chunk))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Analyzing", total=len(items))
            await asyncio.gather(*(process(chunk, task) for chunk in chunks))
        return items

    async def _analyze_singly(self, items: List[ContentItem]) -> List[ContentItem]:
        throttle_sec = self._get_throttle_sec()
        semaphore = asyncio.Semaphore(self._get_concurrency())

        async def process(item: ContentItem, index: int, progress_task: int) -> ContentItem:
            async with semaphore:
                try:
                    await self._analyze_item(item)
                except Exception as error:
                    if is_fatal_ai_error(error):
                        raise
                    print(f"Error analyzing item {item.id}: {redact_secrets(error)}")
                    self._apply_fallback(item)
                if throttle_sec > 0 and index < len(items) - 1:
                    await asyncio.sleep(throttle_sec)
            progress.advance(progress_task)
            return item

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Analyzing", total=len(items))
            return await asyncio.gather(
                *(process(item, index, task) for index, item in enumerate(items))
            )

    async def _analyze_with_fallback(self, items: list[ContentItem]) -> None:
        try:
            await self._analyze_chunk(items)
            return
        except Exception as error:
            if is_fatal_ai_error(error):
                raise
            if len(items) == 1:
                try:
                    await self._analyze_item(items[0])
                except Exception as single_error:
                    if is_fatal_ai_error(single_error):
                        raise
                    print(
                        f"Error analyzing item {items[0].id}: "
                        f"{redact_secrets(single_error)}"
                    )
                    self._apply_fallback(items[0])
                return

        midpoint = len(items) // 2
        await self._analyze_with_fallback(items[:midpoint])
        await self._analyze_with_fallback(items[midpoint:])

    async def _analyze_chunk(self, items: list[ContentItem]) -> None:
        blocks = [self._item_payload(item) for item in items]
        with usage_stage("analysis"):
            response = await self.client.complete(
                system=CONTENT_ANALYSIS_SYSTEM,
                user=BATCH_CONTENT_ANALYSIS_USER.format(
                    items=json.dumps(blocks, ensure_ascii=False, indent=2)
                ),
            )
        parsed = self._parse_json_response(response)
        raw_results = parsed.get("items") if isinstance(parsed, dict) else None
        if not isinstance(raw_results, list):
            raise ValueError("Batch analysis response did not contain an items list")

        expected = {item.id: item for item in items}
        validated: dict[str, AnalysisResult] = {}
        for raw in raw_results:
            result = AnalysisResult.model_validate(raw)
            if not result.id or result.id not in expected or result.id in validated:
                raise ValueError("Batch analysis returned an unknown or duplicate item ID")
            validated[result.id] = result
        if set(validated) != set(expected):
            raise ValueError("Batch analysis response did not map every input item ID")
        for item_id, result in validated.items():
            self._apply_result(expected[item_id], result)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    async def _analyze_item(self, item: ContentItem) -> None:
        payload = self._item_payload(item)
        with usage_stage("analysis"):
            response = await self.client.complete(
                system=CONTENT_ANALYSIS_SYSTEM,
                user=CONTENT_ANALYSIS_USER.format(**payload),
            )
        parsed = self._parse_json_response(response)
        try:
            result = AnalysisResult.model_validate(parsed) if parsed is not None else None
        except ValidationError:
            result = None
        if result is None:
            print(f"Warning: could not parse analysis response for {item.id}, using defaults")
            self._apply_fallback(item)
            return
        if result.id and result.id != item.id:
            raise ValueError("Single-item analysis returned the wrong item ID")
        self._apply_result(item, result)

    @staticmethod
    def _item_payload(item: ContentItem) -> dict[str, str]:
        content_text = item.content or ""
        content_section = f"正文: {content_text[:2500]}" if content_text else "正文: 无"
        engagement = {
            key: item.metadata[key]
            for key in (
                "score", "descendants", "favorite_count", "retweet_count", "reply_count",
                "views", "bookmarks", "upvote_ratio", "stars_gained", "repo",
            )
            if item.metadata.get(key) is not None
        }
        discussion_section = (
            "互动与项目指标: " + json.dumps(engagement, ensure_ascii=False)
            if engagement
            else "互动与项目指标: 无"
        )
        return {
            "id": item.id,
            "title": item.title,
            "source": item.source_type.value,
            "author": item.author or "Unknown",
            "url": str(item.url),
            "content_section": content_section,
            "discussion_section": discussion_section,
        }

    @staticmethod
    def _apply_result(item: ContentItem, result: AnalysisResult) -> None:
        item.ai_score = result.score
        item.ai_reason = result.reason
        item.ai_summary = result.summary_zh or result.summary or item.title
        item.ai_tags = result.tags
        item.metadata.update(
            {
                "category": result.category,
                "region": result.region,
                "source_tier": result.source_tier,
                "is_first_party": result.is_first_party,
                "is_new_event": result.is_new_event,
                "has_substantive_update": result.has_substantive_update,
                "is_promotional": result.is_promotional,
                "event_key": result.event_key or item.id,
                "follow_up": result.follow_up,
                "summary_zh": result.summary_zh or result.summary or item.title,
            }
        )
        if result.github_project:
            item.metadata["github_project"] = result.github_project

    @staticmethod
    def _apply_fallback(item: ContentItem) -> None:
        item.ai_score = 0.0
        item.ai_reason = "Analysis response parse failed"
        item.ai_summary = item.title
        item.ai_tags = []
