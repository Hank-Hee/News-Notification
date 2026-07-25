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
            "evidence_status": "first_party",
            "target_user": "市场研究员",
            "user_problem": "手工整理情报耗时",
            "what_it_is": "自动整理 AI 情报的产品",
            "usage_flow": ["输入关注主题", "自动生成结构化记录"],
            "ai_role": "把新闻分类并生成摘要",
            "implementation_idea": "先抓取 RSS，再让模型输出固定 JSON",
            "learning_points": ["结构化输出", "提示词"],
            "hands_on_exercise": "用 5 条 RSS 新闻生成 JSON",
            "limitations_or_uncertainties": "还没有长期稳定性数据",
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
    assert product["hands_on_exercise"] == "用 5 条 RSS 新闻生成 JSON"

    rows = list(csv.DictReader(published_csv.open(encoding="utf-8")))
    assert rows[0]["product_name"] == "Acme AI"
    assert rows[0]["learning_points"] == "结构化输出 | 提示词"


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


def test_database_load_removes_retired_deep_analysis_fields(tmp_path):
    database = _database(tmp_path)
    database.json_path.parent.mkdir(parents=True)
    database.json_path.write_text(
        json.dumps(
            {
                "version": 1,
                "products": [
                    {
                        "product_id": "product-old",
                        "product_name": "Old Product",
                        "tool_stack": ["legacy"],
                        "business_model": "legacy",
                        "market_reaction": "legacy",
                        "transferable_lessons": ["legacy"],
                        "mvp_path": ["legacy"],
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    restored = database.load()

    product = restored.products[0]
    assert product["product_name"] == "Old Product"
    for retired in (
        "tool_stack",
        "business_model",
        "market_reaction",
        "transferable_lessons",
        "mvp_path",
    ):
        assert retired not in product
