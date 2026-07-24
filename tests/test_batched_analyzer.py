import asyncio
import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from src.ai.analyzer import ContentAnalyzer
from src.models import ContentItem, SourceType


def _item(index):
    return ContentItem(
        id=f"rss:item:{index}",
        source_type=SourceType.RSS,
        title=f"AI agent release {index}",
        url=f"https://example.com/{index}",
        content="A substantive AI agent product release.",
        published_at=datetime(2026, 7, 23, tzinfo=timezone.utc),
    )


def _result(item_id, score):
    return {
        "id": item_id,
        "score": score,
        "category": "tech",
        "region": "global",
        "source_tier": 1,
        "is_first_party": True,
        "is_new_event": True,
        "has_substantive_update": False,
        "is_promotional": False,
        "event_key": f"event-{item_id}",
        "reason": "有明确技术增量",
        "summary_zh": f"条目 {item_id} 的中文摘要。",
        "tags": ["Agent"],
        "follow_up": "观察采用情况",
    }


def test_batch_results_map_by_stable_item_id_not_response_order():
    items = [_item(1), _item(2)]

    async def complete(**kwargs):
        return json.dumps({"items": [_result(items[1].id, 8.2), _result(items[0].id, 9.1)]})

    client = SimpleNamespace(
        config=SimpleNamespace(analysis_batch_size=10, analysis_concurrency=1),
        complete=complete,
    )

    result = asyncio.run(ContentAnalyzer(client).analyze_batch(items))

    assert [item.id for item in result] == [items[0].id, items[1].id]
    assert [item.ai_score for item in result] == [9.1, 8.2]
    assert result[0].metadata["event_key"] == f"event-{items[0].id}"


def test_batch_parse_failure_recursively_falls_back_to_smaller_batches():
    items = [_item(1), _item(2)]
    calls = []

    async def complete(**kwargs):
        calls.append(kwargs["user"])
        if len(calls) == 1:
            return "not-json"
        item = items[len(calls) - 2]
        return json.dumps({"items": [_result(item.id, 8.0)]})

    client = SimpleNamespace(
        config=SimpleNamespace(analysis_batch_size=10, analysis_concurrency=1),
        complete=complete,
    )

    asyncio.run(ContentAnalyzer(client).analyze_batch(items))

    assert len(calls) == 3
    assert [item.ai_score for item in items] == [8.0, 8.0]


def test_batch_api_error_aborts_without_recursive_retry_storm():
    items = [_item(1), _item(2)]
    calls = 0

    async def complete(**kwargs):
        nonlocal calls
        calls += 1
        raise RuntimeError("Error code: 400 - invalid temperature")

    client = SimpleNamespace(
        config=SimpleNamespace(analysis_batch_size=10, analysis_concurrency=1),
        complete=complete,
    )

    with pytest.raises(RuntimeError, match="invalid temperature"):
        asyncio.run(ContentAnalyzer(client).analyze_batch(items))

    assert calls == 1


def test_all_invalid_ai_responses_abort_instead_of_publishing_empty_digest():
    items = [_item(1), _item(2)]

    async def complete(**kwargs):
        return "not-json"

    client = SimpleNamespace(
        config=SimpleNamespace(analysis_batch_size=10, analysis_concurrency=1),
        complete=complete,
    )

    with pytest.raises(RuntimeError, match="no valid results"):
        asyncio.run(ContentAnalyzer(client).analyze_batch(items))

    assert [item.ai_score for item in items] == [0.0, 0.0]


def test_null_optional_fields_do_not_discard_valid_analysis():
    item = _item(1)
    payload = _result(item.id, 8.4)
    payload.update(
        {
            "product_name": None,
            "builder_name": None,
            "target_user": None,
            "market_signal": None,
            "skill_signals": None,
            "verticals": None,
            "github_project": [],
        }
    )

    async def complete(**kwargs):
        return json.dumps({"items": [payload]})

    client = SimpleNamespace(
        config=SimpleNamespace(analysis_batch_size=5, analysis_concurrency=1),
        complete=complete,
    )

    asyncio.run(ContentAnalyzer(client).analyze_batch([item]))

    assert item.ai_score == 8.4
    assert item.metadata["product_name"] == ""
    assert item.metadata["skill_signals"] == []
    assert "github_project" not in item.metadata
