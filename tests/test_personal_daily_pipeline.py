import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import src.orchestrator as orchestrator_module
from src.ai.summarizer import DailySummarizer
from src.ai.prompts import CONTENT_ENRICHMENT_USER
from src.models import (
    AIConfig,
    BalanceConfig,
    Config,
    ContentItem,
    FilteringConfig,
    SourceType,
    SourcesConfig,
)
from src.orchestrator import HorizonOrchestrator


def _item(index, category, region, score, source=SourceType.RSS):
    item = ContentItem(
        id=f"item-{index}",
        source_type=source,
        title=f"AI item {index}",
        url=f"https://example.com/{index}",
        content="Substantive AI information.",
        author="official",
        published_at=datetime(2026, 7, 23, 8, 0, tzinfo=timezone.utc),
        metadata={
            "category": category,
            "region": region,
            "source_tier": 1,
            "follow_up": "继续观察后续采用。",
        },
    )
    item.ai_score = score
    item.ai_summary = f"条目 {index} 的中文摘要。"
    item.ai_reason = "存在可验证的实质增量。"
    item.ai_tags = ["Agent"]
    return item


def _orchestrator(filtering=None, balance=None):
    config = Config(
        ai=AIConfig(provider="openai", model="test", api_key_env="TEST_KEY", languages=["zh"]),
        sources=SourcesConfig(),
        filtering=filtering or FilteringConfig(),
        balance=balance or BalanceConfig(),
    )
    return HorizonOrchestrator(config, SimpleNamespace())


def test_soft_quota_balances_tech_product_and_china_global():
    orchestrator = _orchestrator(FilteringConfig(final_max_items=12))
    items = [
        *[_item(i, "tech", "global", 10 - i / 20) for i in range(8)],
        *[_item(i + 8, "product", "china", 8.0 - i / 20) for i in range(8)],
    ]

    result = orchestrator.apply_balanced_digest(items, log=False).items

    assert len(result) == 12
    assert sum(item.metadata["category"] == "tech" for item in result) == 6
    assert sum(item.metadata["category"] == "product" for item in result) == 6
    assert sum(item.metadata["region"] == "china" for item in result) == 6
    assert sum(item.metadata["region"] == "global" for item in result) == 6


def test_quality_shortage_does_not_fill_below_threshold_or_minimum():
    orchestrator = _orchestrator(
        FilteringConfig(ai_score_threshold=7.5, final_min_items=10, final_max_items=12)
    )
    items = [
        *[_item(i, "tech", "global", 8.0) for i in range(7)],
        *[_item(i + 7, "product", "china", 6.0) for i in range(5)],
    ]

    result = asyncio.run(orchestrator.filter_items(items, topic_dedup=False, log=False))

    assert len(result.items) == 7
    assert all((item.ai_score or 0) >= 7.5 for item in result.items)


def test_only_top_five_receive_deep_analysis(monkeypatch):
    orchestrator = _orchestrator(FilteringConfig(deep_analysis_limit=5))
    items = [_item(i, "tech", "global", 9.0 - i / 10) for i in range(8)]
    enriched = []

    class FakeEnricher:
        def __init__(self, client, **kwargs):
            pass

        async def enrich_batch(self, selected):
            enriched.extend(item.id for item in selected)

        async def generate_trend_overview(self, selected):
            return ["趋势一", "趋势二", "趋势三"]

    monkeypatch.setattr(orchestrator_module, "create_ai_client", lambda config: object())
    monkeypatch.setattr(orchestrator_module, "ContentEnricher", FakeEnricher)

    trends = asyncio.run(orchestrator._enrich_important_items(items))

    assert enriched == [item.id for item in items[:5]]
    assert trends == ["趋势一", "趋势二", "趋势三"]


def test_chinese_daily_renders_product_intelligence_sections_and_shortage_notice():
    items = [_item(i, "tech" if i % 2 == 0 else "product", "china" if i % 2 else "global", 8.5) for i in range(7)]
    items[0].metadata.update(
        {
            "deep_analysis": True,
            "what_happened": "发布了新的 Agent 能力。",
            "why_it_matters": "降低了复杂任务的使用门槛。",
            "key_details": "目前公开信息不足。",
            "industry_or_product_impact": "可能推动企业采用。",
            "limitations_or_uncertainties": "尚缺少长期数据。",
            "what_to_watch_next": "关注正式定价。",
        }
    )

    result = asyncio.run(
        DailySummarizer().generate_summary(
            items,
            "2026-07-23",
            80,
            language="zh",
            trend_overview=["Agent 产品继续向复杂任务扩展。", "中国与海外均有更新。", "开源基础设施保持活跃。"],
        )
    )

    assert "# AI产品情报" in result
    assert "今日高质量增量有限" in result
    assert "## 今日重点" in result
    assert "## 产品拆解" in result
    assert "## Newsletter 精选" in result
    assert "最近 7 天没有达到收录标准" in result
    assert "## 他们怎么做" in result
    assert "## 模型公司动态" in result
    assert "## 今天学什么" in result
    assert "**用户问题**" in result
    assert "商业模式" not in result
    assert "工具栈" not in result


def test_github_pages_post_generation_is_atomic_and_has_front_matter(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    path = HorizonOrchestrator._write_pages_post(
        "2026-07-23",
        "# Horizon AI Daily\n\n日报正文",
        "zh",
    )

    content = path.read_text(encoding="utf-8")
    assert path == tmp_path / "docs/_posts/2026-07-23-summary-zh.md"
    assert 'title: "AI产品情报 · 2026-07-23"' in content
    assert "lang: zh" in content
    assert "日报正文" in content
    assert "# Horizon AI Daily" not in content


def test_product_enrichment_prompt_formats_nested_json_example():
    prompt = CONTENT_ENRICHMENT_USER.format(
        title="Acme AI",
        url="https://example.com/acme",
        summary="Acme AI 发布了产品。",
        score=9.0,
        reason="有真实用户工作流。",
        tags="AI 产品",
        content="原文内容",
        comments_section="",
        web_context="没有可用的背景搜索结果。",
    )

    assert '"usage_flow": ["用户使用步骤，最多 4 步"]' in prompt
    assert '"hands_on_exercise": "一个 30–60 分钟可以完成的小练习"' in prompt
    assert "business_model" not in prompt
