"""Grounded Chinese deep analysis for the highest-ranked daily items."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from typing import List, Literal

from ddgs import DDGS
from pydantic import BaseModel, Field, ValidationError
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .client import AIClient
from .prompts import (
    CONCEPT_EXTRACTION_SYSTEM,
    CONCEPT_EXTRACTION_USER,
    CONTENT_ENRICHMENT_SYSTEM,
    CONTENT_ENRICHMENT_USER,
    TREND_OVERVIEW_SYSTEM,
    TREND_OVERVIEW_USER,
)
from .tokens import usage_stage
from .utils import parse_json_response
from ..models import ContentItem
from ..redaction import is_fatal_ai_error, redact_secrets


class DeepAnalysisResult(BaseModel):
    title_zh: str
    what_happened: str
    why_it_matters: str
    key_details: str
    industry_or_product_impact: str
    limitations_or_uncertainties: str
    what_to_watch_next: str
    community_view: str = ""
    product_name: str = "未公开"
    target_users: str = "未公开"
    user_problem: str = "未公开"
    original_workflow: list[str] = Field(default_factory=list)
    product_workflow: list[str] = Field(default_factory=list)
    input_process_output: dict[str, str] = Field(default_factory=dict)
    tool_stack: list[str] = Field(default_factory=list)
    business_model: str = "未公开"
    product_stage: Literal[
        "validated", "early_growth", "proof_of_concept", "not_applicable"
    ] = "not_applicable"
    traction_evidence: list[str] = Field(default_factory=list)
    market_reaction: str = "未公开"
    transferable_lessons: list[str] = Field(default_factory=list)
    mvp_path: list[str] = Field(default_factory=list)
    skill_signals: list[str] = Field(default_factory=list)
    evidence_status: Literal[
        "first_party", "verified", "reported", "early_signal"
    ] = "reported"
    sources: list[str] = Field(default_factory=list)


class TrendOverviewResult(BaseModel):
    trends: list[str] = Field(min_length=3, max_length=5)


class ContentEnricher:
    """Enriches selected Top items while degrading safely when search fails."""

    def __init__(self, ai_client: AIClient):
        self.client = ai_client

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
                    if is_fatal_ai_error(error):
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

    async def _extract_concepts(self, item: ContentItem, content_text: str) -> list[str]:
        try:
            with usage_stage("deep_analysis"):
                response = await self.client.complete(
                    system=CONCEPT_EXTRACTION_SYSTEM,
                    user=CONCEPT_EXTRACTION_USER.format(
                        title=item.title,
                        summary=item.ai_summary or item.title,
                        tags=", ".join(item.ai_tags),
                        content=content_text[:1200],
                    ),
                    max_tokens=512,
                )
            parsed = parse_json_response(response) or {}
            queries = parsed.get("queries", [])
            return [str(query) for query in queries[:3] if str(query).strip()]
        except Exception as error:
            if is_fatal_ai_error(error):
                raise
            return []

    @retry(
        retry=retry_if_exception_type(ValueError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=2, max=10),
        reraise=True,
    )
    async def _enrich_item(self, item: ContentItem) -> None:
        content_text = item.content or ""
        comments_text = ""
        if "--- Top Comments ---" in content_text:
            content_text, comments_text = content_text.split("--- Top Comments ---", 1)
        content_text = content_text.strip()[:5000]
        comments_text = comments_text.strip()[:2000]

        results: list[dict[str, str]] = []
        for query in await self._extract_concepts(item, content_text):
            results.extend(await self._web_search(query))
        web_context = "\n".join(
            f"- {result['title']} | {result['url']} | {result['body']}" for result in results
        ) or "没有可用的背景搜索结果。"
        available_urls = {str(item.url): item.title}
        available_urls.update(
            {result["url"]: result["title"] for result in results if result["url"]}
        )

        with usage_stage("deep_analysis"):
            response = await self.client.complete(
                system=CONTENT_ENRICHMENT_SYSTEM,
                user=CONTENT_ENRICHMENT_USER.format(
                    title=item.title,
                    url=str(item.url),
                    summary=item.ai_summary or item.title,
                    score=item.ai_score or 0,
                    reason=item.ai_reason or "",
                    tags=", ".join(item.ai_tags),
                    content=content_text or "目前没有抓取到正文。",
                    comments_section=(
                        f"\n社区讨论：\n{comments_text}" if comments_text else ""
                    ),
                    web_context=web_context,
                ),
                max_tokens=4096,
            )
        parsed = parse_json_response(response)
        try:
            result = DeepAnalysisResult.model_validate(parsed)
        except ValidationError as error:
            raise ValueError("Deep analysis response failed validation") from error

        item.metadata.update(
            {
                "title_zh": result.title_zh,
                "what_happened": result.what_happened,
                "why_it_matters": result.why_it_matters,
                "key_details": result.key_details,
                "industry_or_product_impact": result.industry_or_product_impact,
                "limitations_or_uncertainties": result.limitations_or_uncertainties,
                "what_to_watch_next": result.what_to_watch_next,
                "community_view": result.community_view,
                "product_name": result.product_name,
                "target_user": result.target_users,
                "user_problem": result.user_problem,
                "original_workflow": result.original_workflow,
                "product_workflow": result.product_workflow,
                "input_process_output": result.input_process_output,
                "tool_stack": result.tool_stack,
                "business_model": result.business_model,
                "product_stage": result.product_stage,
                "traction_evidence": result.traction_evidence,
                "market_reaction": result.market_reaction,
                "transferable_lessons": result.transferable_lessons,
                "mvp_path": result.mvp_path,
                "skill_signals": result.skill_signals,
                "evidence_status": result.evidence_status,
                "deep_analysis": True,
            }
        )
        valid_sources = [url for url in result.sources if url in available_urls][:3]
        item.metadata["sources"] = [
            {"url": url, "title": available_urls[url]} for url in valid_sources
        ]

    async def generate_trend_overview(self, items: list[ContentItem]) -> list[str]:
        if not items:
            return []
        payload = [
            {
                "title": item.metadata.get("title_zh") or item.title,
                "summary": item.ai_summary,
                "category": item.metadata.get("category"),
                "intelligence_type": item.metadata.get("intelligence_type"),
                "product_name": item.metadata.get("product_name"),
                "target_user": item.metadata.get("target_user"),
                "product_signal": item.metadata.get("product_signal"),
                "market_signal": item.metadata.get("market_signal"),
                "builder_insight": item.metadata.get("builder_insight"),
                "skill_signals": item.metadata.get("skill_signals", []),
                "region": item.metadata.get("region"),
                "score": item.ai_score,
            }
            for item in items
        ]
        try:
            with usage_stage("trend_overview"):
                response = await self.client.complete(
                    system=TREND_OVERVIEW_SYSTEM,
                    user=TREND_OVERVIEW_USER.format(
                        items=json.dumps(payload, ensure_ascii=False, indent=2)
                    ),
                    max_tokens=1024,
                )
            result = TrendOverviewResult.model_validate(parse_json_response(response))
            return result.trends
        except Exception as error:
            if is_fatal_ai_error(error):
                raise
            return self._fallback_trends(items)

    @staticmethod
    def _fallback_trends(items: list[ContentItem]) -> list[str]:
        types = {str(item.metadata.get("intelligence_type", "")) for item in items}
        trends = [f"今日筛选出 {len(items)} 条可用于产品判断的 AI 情报。"]
        if "product_case" in types:
            trends.append("今日有可进一步拆解的 AI 产品或真实工作流案例。")
        if "builder_insight" in types:
            trends.append("Builder 的一手方法提供了可以迁移到个人产品的实现路径。")
        if "market_signal" in types:
            trends.append("用户反馈与商业信号可用于判断哪些方向已经得到市场验证。")
        if "model_capability" in types:
            trends.append("新模型能力的重点是它能解锁怎样的新产品体验。")
        return trends[:5]
