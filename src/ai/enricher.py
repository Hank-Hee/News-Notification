"""Grounded Chinese deep analysis for the highest-ranked daily items."""

from __future__ import annotations

import asyncio
import os
import sys
from typing import List

from ddgs import DDGS
from pydantic import BaseModel, Field, ValidationError, model_validator
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn

from .cache import AnalysisCache
from .client import AIClient
from .prompts import (
    CONTENT_ENRICHMENT_SYSTEM,
    CONTENT_ENRICHMENT_USER,
)
from .tokens import (
    AIRequestBudgetExceeded,
    record_cache_hit,
    record_retry,
    record_validation_failure,
    usage_stage,
)
from .utils import parse_json_response
from ..models import ContentItem
from ..redaction import is_fatal_ai_error, redact_secrets


class DeepAnalysisResult(BaseModel):
    title_zh: str
    what_it_is: str
    product_name: str = "未公开"
    target_users: str = "未公开"
    user_problem: str = "未公开"
    usage_flow: list[str] = Field(default_factory=list)
    ai_role: str = "未公开"
    implementation_idea: str = "未公开"
    learning_points: list[str] = Field(default_factory=list)
    hands_on_exercise: str = "未公开"
    limitations_or_uncertainties: str
    evidence_status: str = "reported"
    sources: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def normalize_sparse_output(cls, value):
        if not isinstance(value, dict):
            return value
        normalized = dict(value)
        for field in (
            "title_zh",
            "what_it_is",
            "product_name",
            "target_users",
            "user_problem",
            "ai_role",
            "implementation_idea",
            "hands_on_exercise",
            "limitations_or_uncertainties",
        ):
            if normalized.get(field) is None:
                normalized[field] = "未公开"
        for field in ("usage_flow", "learning_points", "sources"):
            if normalized.get(field) is None:
                normalized[field] = []
        if normalized.get("evidence_status") not in {
            "first_party", "verified", "reported", "early_signal"
        }:
            normalized["evidence_status"] = "reported"
        return normalized


class ContentEnricher:
    """Enriches selected Top items while degrading safely when search fails."""

    def __init__(
        self,
        ai_client: AIClient,
        *,
        fallback_client: AIClient | None = None,
        cache: AnalysisCache | None = None,
        prompt_version: str = "deep-v3-beginner",
        max_retries: int = 1,
    ):
        self.client = ai_client
        self.fallback_client = fallback_client
        self.cache = cache
        self.prompt_version = prompt_version
        self.max_retries = max(0, max_retries)

    def _get_concurrency(self) -> int:
        config = getattr(self.client, "config", None)
        return max(getattr(config, "enrichment_concurrency", 1), 1)

    async def enrich_batch(self, items: List[ContentItem]) -> None:
        semaphore = asyncio.Semaphore(self._get_concurrency())

        async def process(item: ContentItem, progress_task: int) -> None:
            async with semaphore:
                try:
                    await self._enrich_item(item)
                except Exception as error:
                    if is_fatal_ai_error(error) and not isinstance(
                        error, AIRequestBudgetExceeded
                    ):
                        raise
                    print(
                        f"Error enriching item {item.id}: {redact_secrets(error)}; "
                        "keeping the scored Chinese summary"
                    )
            progress.advance(progress_task)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Enriching Top items", total=len(items))
            await asyncio.gather(*(process(item, task) for item in items))

    async def _web_search(self, query: str, max_results: int = 3) -> list[dict[str, str]]:
        try:
            stderr = sys.stderr
            sys.stderr = open(os.devnull, "w")
            try:
                results = await asyncio.to_thread(DDGS().text, query, max_results=max_results)
            finally:
                sys.stderr.close()
                sys.stderr = stderr
        except Exception:
            return []
        return [
            {
                "title": str(result.get("title", "")),
                "url": str(result.get("href", "")),
                "body": str(result.get("body", "")),
            }
            for result in (results or [])
        ]

    @staticmethod
    def build_search_queries(item: ContentItem) -> list[str]:
        candidates = [
            str(item.metadata.get("product_name", "")).strip(),
            str(item.author or "").strip(),
            str(item.title).strip(),
        ]
        return list(dict.fromkeys(value for value in candidates if value))[:2]

    def _get_cached_result(
        self, item: ContentItem, client: AIClient, stage: str
    ) -> DeepAnalysisResult | None:
        if self.cache is None:
            return None
        model_id = str(getattr(client, "model", "unknown"))
        payload = self.cache.get(
            item,
            stage=stage,
            model_id=model_id,
            prompt_version=self.prompt_version,
        )
        if payload is None:
            return None
        try:
            result = DeepAnalysisResult.model_validate(payload)
        except ValidationError:
            record_validation_failure(stage)
            return None
        record_cache_hit(stage)
        return result

    def _cache_result(
        self,
        item: ContentItem,
        result: DeepAnalysisResult,
        client: AIClient,
        stage: str,
    ) -> None:
        if self.cache is None:
            return
        self.cache.put(
            item,
            result.model_dump(mode="json"),
            stage=stage,
            model_id=str(getattr(client, "model", "unknown")),
            prompt_version=self.prompt_version,
        )

    async def _enrich_item(self, item: ContentItem) -> None:
        cached = self._get_cached_result(item, self.client, "deep_analysis")
        if cached is not None:
            self._apply_result(item, cached, {str(item.url): item.title})
            return
        if self.fallback_client is not None:
            fallback_cached = self._get_cached_result(
                item, self.fallback_client, "deep_analysis_fallback"
            )
            if fallback_cached is not None:
                self._apply_result(item, fallback_cached, {str(item.url): item.title})
                return

        content_text = item.content or ""
        comments_text = ""
        if "--- Top Comments ---" in content_text:
            content_text, comments_text = content_text.split("--- Top Comments ---", 1)
        content_text = content_text.strip()[:5000]
        comments_text = comments_text.strip()[:2000]

        results: list[dict[str, str]] = []
        for query in self.build_search_queries(item):
            results.extend(await self._web_search(query))
        web_context = "\n".join(
            f"- {result['title']} | {result['url']} | {result['body']}" for result in results
        ) or "没有可用的背景搜索结果。"
        available_urls = {str(item.url): item.title}
        available_urls.update(
            {result["url"]: result["title"] for result in results if result["url"]}
        )

        prompt = CONTENT_ENRICHMENT_USER.format(
            title=item.title,
            url=str(item.url),
            summary=item.ai_summary or item.title,
            score=item.ai_score or 0,
            reason=item.ai_reason or "",
            tags=", ".join(item.ai_tags),
            content=content_text or "目前没有抓取到正文。",
            comments_section=(f"\n社区讨论：\n{comments_text}" if comments_text else ""),
            web_context=web_context,
        )

        result: DeepAnalysisResult | None = None
        primary_error: Exception | None = None
        for attempt in range(1 + self.max_retries):
            try:
                result = await self._request_result(
                    self.client, prompt, stage="deep_analysis"
                )
                self._cache_result(item, result, self.client, "deep_analysis")
                break
            except Exception as error:
                primary_error = error
                if attempt < self.max_retries:
                    record_retry("deep_analysis")

        if result is None and self.fallback_client is not None:
            print(
                "Kimi deep analysis failed after one retry; using DeepSeek "
                f"fallback for {item.id}: {redact_secrets(primary_error or '')}"
            )
            try:
                result = await self._request_result(
                    self.fallback_client, prompt, stage="deep_analysis_fallback"
                )
                self._cache_result(
                    item, result, self.fallback_client, "deep_analysis_fallback"
                )
            except Exception as fallback_error:
                raise ValueError(
                    "Both Kimi and DeepSeek fallback deep analysis failed"
                ) from fallback_error

        if result is None:
            raise ValueError("Deep analysis failed without an available fallback")

        self._apply_result(item, result, available_urls)

    @staticmethod
    async def _request_result(
        client: AIClient, prompt: str, *, stage: str
    ) -> DeepAnalysisResult:
        with usage_stage(stage):
            response = await client.complete(
                system=CONTENT_ENRICHMENT_SYSTEM,
                user=prompt,
                max_tokens=4096,
            )
        parsed = parse_json_response(response)
        try:
            return DeepAnalysisResult.model_validate(parsed)
        except ValidationError as error:
            record_validation_failure(stage)
            raise ValueError("Deep analysis response failed validation") from error

    @staticmethod
    def _apply_result(
        item: ContentItem,
        result: DeepAnalysisResult,
        available_urls: dict[str, str],
    ) -> None:

        item.metadata.update(
            {
                "title_zh": result.title_zh,
                "what_it_is": result.what_it_is,
                "limitations_or_uncertainties": result.limitations_or_uncertainties,
                "product_name": result.product_name,
                "target_user": result.target_users,
                "user_problem": result.user_problem,
                "usage_flow": result.usage_flow,
                "ai_role": result.ai_role,
                "implementation_idea": result.implementation_idea,
                "learning_points": result.learning_points,
                "hands_on_exercise": result.hands_on_exercise,
                "evidence_status": result.evidence_status,
                "deep_analysis": True,
            }
        )
        valid_sources = [url for url in result.sources if url in available_urls][:3]
        item.metadata["sources"] = [
            {"url": url, "title": available_urls[url]} for url in valid_sources
        ]

    async def generate_trend_overview(self, items: list[ContentItem]) -> list[str]:
        """Use already generated one-line summaries; this stage is model-free."""
        trends: list[str] = []
        for item in items:
            summary = str(item.ai_summary or item.title).strip()
            if summary and summary not in trends:
                trends.append(summary)
            if len(trends) == 5:
                break
        return trends

    @staticmethod
    def _fallback_trends(items: list[ContentItem]) -> list[str]:
        return [
            str(item.ai_summary or item.title).strip()
            for item in items[:5]
            if str(item.ai_summary or item.title).strip()
        ]
