from datetime import datetime, timedelta, timezone

from src.models import ContentItem, FilteringConfig, SourceType
from src.prefilter import clean_url, normalize_title, prefilter_items


NOW = datetime(2026, 7, 23, 12, 0, tzinfo=timezone.utc)


def _item(item_id, title, url, *, content="", published_at=NOW, source=SourceType.RSS, score=None):
    metadata = {"score": score} if score is not None else {}
    return ContentItem(
        id=item_id,
        source_type=source,
        title=title,
        url=url,
        content=content,
        published_at=published_at,
        metadata=metadata,
    )


def test_prefilter_applies_time_ai_quality_and_community_rules():
    config = FilteringConfig(
        rule_prefilter_enabled=True,
        min_content_chars=20,
        community_min_score=50,
    )
    items = [
        _item("keep", "New AI agent framework released", "https://example.com/keep", content="Detailed agent release information."),
        _item("old", "Old AI model story", "https://example.com/old", content="Old details", published_at=NOW - timedelta(hours=30)),
        _item("off-topic", "A new database migration guide", "https://example.com/db", content="Database-only engineering details."),
        _item("low", "AI discussion with little evidence", "https://news.ycombinator.com/item?id=1", content="A short AI discussion.", source=SourceType.HACKERNEWS, score=5),
    ]

    result = prefilter_items(items, since=NOW - timedelta(hours=24), config=config)

    assert [item.id for item in result.items] == ["keep"]
    assert result.stats.dropped_outside_window == 1
    assert result.stats.dropped_non_ai == 1
    assert result.stats.dropped_low_engagement == 1


def test_title_and_tracking_url_duplicates_are_removed():
    config = FilteringConfig(rule_prefilter_enabled=True, min_content_chars=0)
    items = [
        _item("first", "OpenAI releases a new AI agent", "https://example.com/story?utm_source=x", content="AI details"),
        _item("url-dup", "A different AI headline", "https://example.com/story", content="Longer AI details from the same URL"),
        _item("title-dup", "OpenAI releases a new AI agent!", "https://other.example/story", content="AI copy"),
    ]

    result = prefilter_items(items, since=NOW - timedelta(hours=24), config=config)

    assert len(result.items) == 1
    assert result.items[0].id == "url-dup"
    assert result.stats.duplicate_url == 1
    assert result.stats.duplicate_title == 1
    assert clean_url("https://example.com/story?utm_source=x") == "https://example.com/story"
    assert normalize_title(items[0].title) == normalize_title(items[2].title)
