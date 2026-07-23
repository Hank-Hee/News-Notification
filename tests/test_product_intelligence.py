import csv
import json
from datetime import date, datetime, timezone

from src.models import ContentItem, ProductIntelligenceConfig, SourceType
from src.product_intelligence import ProductIntelligenceDatabase


def _item(event_key: str = "product-launch") -> ContentItem:
    item = ContentItem(
        id=f"rss:item:{event_key}",
        source_type=SourceType.RSS,
        title="Acme AI launches a research workflow",
        url="https://example.com/acme",
        author="Acme Team",
        content="AI product launch",
        published_at=datetime(2026, 7, 24, 1, 0, tzinfo=timezone.utc),
        metadata={
            "event_key": event_key,
            "intelligence_type": "product_case",
            "product_name": "Acme AI",
            "builder_name": "Acme Team",
            "product_stage": "early_growth",
            "evidence_status": "first_party",
            "target_user": "市场研究员",
            "user_problem": "手工整理情报耗时",
            "product_signal": "把采集、分类与交付串成工作流",
            "market_signal": "已有首批付费用户",
            "original_workflow": ["手工搜索", "复制到表格"],
            "product_workflow": ["输入关注主题", "自动生成结构化记录"],
            "tool_stack": ["LLM", "RSS"],
            "transferable_lessons": ["先验证单一角色的高频任务"],
            "mvp_path": ["访谈 5 名研究员"],
            "skill_signals": ["用户研究", "工作流设计"],
            "verticals": ["知识管理"],
            "region": "global",
        },
    )
    item.ai_score = 9.1
    item.ai_summary = "Acme AI 把市场情报整理变成自动工作流。"
    item.ai_tags = ["AI 产品", "Research"]
    return item


def _database(tmp_path):
    return ProductIntelligenceDatabase(
        ProductIntelligenceConfig(
            enabled=True,
            json_path=str(tmp_path / "data/product-intelligence.json"),
            csv_path=str(tmp_path / "data/product-intelligence.csv"),
            publish_directory=str(tmp_path / "docs/data"),
        )
    )


def test_database_upserts_stable_product_and_publishes_json_csv(tmp_path):
    database = _database(tmp_path)
    assert database.upsert([_item()], date(2026, 7, 24)) == 1
    published_json, published_csv = database.save_and_publish()

    payload = json.loads(published_json.read_text(encoding="utf-8"))
    assert len(payload["products"]) == 1
    product = payload["products"][0]
    assert product["product_name"] == "Acme AI"
    assert product["target_user"] == "市场研究员"
    assert product["mvp_path"] == ["访谈 5 名研究员"]

    rows = list(csv.DictReader(published_csv.open(encoding="utf-8")))
    assert rows[0]["product_name"] == "Acme AI"
    assert rows[0]["skill_signals"] == "用户研究 | 工作流设计"


def test_database_rerun_does_not_duplicate_same_event(tmp_path):
    database = _database(tmp_path)
    database.upsert([_item()], date(2026, 7, 24))
    database.save_and_publish()

    restored = _database(tmp_path).load()
    restored.upsert([_item()], date(2026, 7, 24))
    product = restored.products[0]

    assert product["occurrence_count"] == 1
    assert len(product["updates"]) == 1
    assert len(product["sources"]) == 1


def test_database_keeps_distinct_product_updates(tmp_path):
    database = _database(tmp_path)
    database.upsert([_item("launch")], date(2026, 7, 24))
    database.upsert([_item("pricing")], date(2026, 7, 25))

    product = database.products[0]
    assert product["occurrence_count"] == 2
    assert [update["update_id"] for update in product["updates"]] == [
        "launch",
        "pricing",
    ]
