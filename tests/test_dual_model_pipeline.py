import asyncio
import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from src.ai.analyzer import ContentAnalyzer
from src.ai.cache import AnalysisCache
from src.ai.enricher import ContentEnricher
from src.ai.prompts import CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER
from src.ai.tokens import (
    AIRequestBudgetExceeded,
    configure_usage_limits,
    ensure_request_allowed,
    record_request,
    reset_usage,
)
from src.models import AIRoutingConfig, Config, ContentItem, SourceType, stage_ai_config


def _item(index: int, *, content: str = "Substantive product update") -> ContentItem:
    return ContentItem(
        id=f"rss:item:{index}",
        source_type=SourceType.RSS,
        title=f"Product {index}",
        url=f"https://example.com/{index}",
        content=content,
        author="Builder",
        published_at=datetime(2026, 7, 25, tzinfo=timezone.utc),
    )


def _candidate_result(item: ContentItem, score: float = 8.2) -> dict:
    return {
        "id": item.id,
        "score": score,
        "category": "product",
        "region": "global",
        "source_tier": 1,
        "is_first_party": True,
        "is_new_event": True,
        "has_substantive_update": False,
        "is_promotional": False,
        "event_key": f"event-{item.id}",
        "reason": "有真实产品增量",
        "summary_zh": "团队发布了产品；它简化了一项具体工作。",
        "tags": ["AI 产品"],
        "follow_up": "查看用户反馈",
        "intelligence_type": "product_case",
        "evidence_status": "first_party",
        "product_name": f"Product {item.id}",
        "github_project": None,
    }


def _deep_result(item: ContentItem) -> str:
    return json.dumps(
        {
            "title_zh": item.title,
            "what_it_is": "一个帮助用户整理资料的 AI 产品",
            "product_name": item.title,
            "target_users": "刚开始使用 AI 的产品新人",
            "user_problem": "资料多且难以整理",
            "usage_flow": ["输入资料", "检查生成结果"],
            "ai_role": "把资料分类并生成摘要",
            "implementation_idea": "先读取文本，再按固定 JSON 字段输出",
            "learning_points": ["结构化输出", "上下文窗口"],
            "hands_on_exercise": "用 5 条新闻生成一份 JSON 清单",
            "limitations_or_uncertainties": "需要人工检查事实",
            "evidence_status": "first_party",
            "sources": [str(item.url)],
        },
        ensure_ascii=False,
    )


def test_production_config_uses_fixed_dual_model_routes(monkeypatch):
    monkeypatch.setenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
    monkeypatch.setenv("KIMI_MODEL_ID", "kimi-k2.6")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    monkeypatch.setenv("DEEPSEEK_CANDIDATE_MODEL", "deepseek-v4-flash")
    monkeypatch.setenv("DEEPSEEK_FALLBACK_MODEL", "deepseek-v4-pro")

    raw = json.loads(open("data/config.github.json", encoding="utf-8").read())
    raw_text = json.dumps(raw)
    for name in (
        "KIMI_BASE_URL",
        "KIMI_MODEL_ID",
        "DEEPSEEK_BASE_URL",
        "DEEPSEEK_CANDIDATE_MODEL",
        "DEEPSEEK_FALLBACK_MODEL",
    ):
        raw_text = raw_text.replace(f"${{{name}}}", __import__("os").environ[name])
    config = Config.model_validate_json(raw_text)

    assert isinstance(config.ai, AIRoutingConfig)
    assert stage_ai_config(config.ai, "candidate_analysis").model == "deepseek-v4-flash"
    assert stage_ai_config(config.ai, "semantic_dedup").model == "deepseek-v4-flash"
    assert stage_ai_config(config.ai, "deep_analysis").model == "kimi-k2.6"
    assert stage_ai_config(config.ai, "deep_analysis_fallback").model == "deepseek-v4-pro"
    assert all(
        route.thinking and route.thinking.type == "disabled"
        for route in (
            config.ai.candidate_analysis,
            config.ai.semantic_dedup,
            config.ai.deep_analysis,
            config.ai.deep_analysis_fallback,
        )
    )


def test_40_candidates_are_scored_in_four_requests():
    items = [_item(index) for index in range(40)]
    calls = 0

    async def complete(**kwargs):
        nonlocal calls
        start = calls * 10
        calls += 1
        return json.dumps(
            {"items": [_candidate_result(item) for item in items[start : start + 10]]},
            ensure_ascii=False,
        )

    client = SimpleNamespace(
        model="deepseek-v4-flash",
        config=SimpleNamespace(analysis_batch_size=10, analysis_concurrency=1),
        complete=complete,
    )

    asyncio.run(ContentAnalyzer(client).analyze_batch(items))

    assert calls == 4
    assert all(item.ai_score == 8.2 for item in items)


def test_candidate_prompt_is_lightweight_and_content_is_capped():
    prompt = CONTENT_ANALYSIS_SYSTEM + CONTENT_ANALYSIS_USER
    for removed in (
        "skill_signals",
        "original_workflow",
        "product_workflow",
        "tool_stack",
        "business_model",
        "mvp_path",
    ):
        assert removed not in prompt

    payload = ContentAnalyzer._item_payload(_item(1, content="x" * 2000))
    assert payload["content_section"] == "正文: " + "x" * 1200


def test_valid_candidate_result_is_reused_from_persistent_cache(tmp_path):
    item = _item(1)
    calls = 0

    async def complete(**kwargs):
        nonlocal calls
        calls += 1
        return json.dumps(_candidate_result(item), ensure_ascii=False)

    client = SimpleNamespace(
        model="deepseek-v4-flash",
        config=SimpleNamespace(analysis_batch_size=1, analysis_concurrency=1),
        complete=complete,
    )
    cache = AnalysisCache(tmp_path / "analysis_cache.json").load()
    asyncio.run(ContentAnalyzer(client, cache=cache).analyze_batch([item]))
    cache.save()

    cached_item = _item(1)
    restored = AnalysisCache(cache.path).load()
    asyncio.run(ContentAnalyzer(client, cache=restored).analyze_batch([cached_item]))

    assert calls == 1
    assert cached_item.ai_score == 8.2


def test_cache_invalidates_when_model_or_prompt_version_changes(tmp_path):
    item = _item(1)
    calls = 0

    async def complete(**kwargs):
        nonlocal calls
        calls += 1
        return json.dumps(_candidate_result(item), ensure_ascii=False)

    cache = AnalysisCache(tmp_path / "analysis_cache.json").load()
    first = SimpleNamespace(
        model="deepseek-v4-flash",
        config=SimpleNamespace(analysis_batch_size=1, analysis_concurrency=1),
        complete=complete,
    )
    asyncio.run(ContentAnalyzer(first, cache=cache).analyze_batch([item]))
    second = SimpleNamespace(
        model="deepseek-v4-pro",
        config=first.config,
        complete=complete,
    )
    asyncio.run(ContentAnalyzer(second, cache=cache).analyze_batch([_item(1)]))
    asyncio.run(
        ContentAnalyzer(
            first, cache=cache, prompt_version="candidate-v3"
        ).analyze_batch([_item(1)])
    )

    assert calls == 3


def test_invalid_candidate_result_is_not_cached(tmp_path):
    item = _item(1)

    async def complete(**kwargs):
        return "not-json"

    client = SimpleNamespace(
        model="deepseek-v4-flash",
        config=SimpleNamespace(analysis_batch_size=1, analysis_concurrency=1),
        complete=complete,
    )
    cache = AnalysisCache(tmp_path / "analysis_cache.json").load()

    with pytest.raises(RuntimeError, match="no valid results"):
        asyncio.run(ContentAnalyzer(client, cache=cache).analyze_batch([item]))

    assert cache.records == {}
    assert not cache.dirty


def test_only_failed_deep_item_uses_fallback(monkeypatch):
    items = [_item(index) for index in range(3)]
    primary_calls: list[str] = []
    fallback_calls: list[str] = []

    async def primary_complete(**kwargs):
        primary_calls.append(kwargs["user"])
        if "Product 1" in kwargs["user"]:
            raise RuntimeError("temporary Kimi failure")
        item = items[0] if "Product 0" in kwargs["user"] else items[2]
        return _deep_result(item)

    async def fallback_complete(**kwargs):
        fallback_calls.append(kwargs["user"])
        return _deep_result(items[1])

    async def no_search(self, query, max_results=3):
        return []

    monkeypatch.setattr(ContentEnricher, "_web_search", no_search)
    primary = SimpleNamespace(
        model="kimi-k2.6",
        config=SimpleNamespace(enrichment_concurrency=1),
        complete=primary_complete,
    )
    fallback = SimpleNamespace(
        model="deepseek-v4-pro",
        config=SimpleNamespace(enrichment_concurrency=1),
        complete=fallback_complete,
    )

    asyncio.run(ContentEnricher(primary, fallback_client=fallback).enrich_batch(items))

    assert len(primary_calls) == 4
    assert len(fallback_calls) == 1
    assert "Product 1" in fallback_calls[0]
    assert all(item.metadata.get("deep_analysis") is True for item in items)


def test_request_safety_valve_stops_thirteenth_call():
    reset_usage()
    configure_usage_limits(max_requests=12, max_cost_cny=2.0)
    for _ in range(12):
        record_request("deepseek", model="deepseek-v4-flash")

    with pytest.raises(AIRequestBudgetExceeded, match="12/12"):
        ensure_request_allowed()
    reset_usage()
