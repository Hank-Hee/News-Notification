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


def test_source_priority_keeps_public_web_before_candidate_limit():
    config = FilteringConfig(
        rule_prefilter_enabled=True,
        min_content_chars=0,
        candidate_limit=1,
        source_priority=["public_web", "rss"],
    )
    rss = _item(
        "rss",
        "AI product story from a media feed",
        "https://example.com/rss",
        content="AI product details",
    )
    official = _item(
        "official",
        "OpenAI publishes a new AI product workflow",
        "https://openai.com/news/product-workflow",
        content="AI workflow details",
        source=SourceType.PUBLIC_WEB,
    )

    result = prefilter_items([rss, official], since=NOW - timedelta(hours=24), config=config)

    assert [item.id for item in result.items] == ["official"]


def test_public_web_per_source_limit_is_applied_per_named_source():
    config = FilteringConfig(
        rule_prefilter_enabled=True,
        min_content_chars=0,
        per_source_limit=1,
    )
    first = _item(
        "first",
        "OpenAI publishes an AI product launch",
        "https://openai.com/news/product-launch",
        content="AI product details",
        source=SourceType.PUBLIC_WEB,
    )
    first.metadata["source_name"] = "OpenAI News"
    second = _item(
        "second",
        "Anthropic publishes an AI product launch",
        "https://anthropic.com/news/product-launch",
        content="AI product details",
        source=SourceType.PUBLIC_WEB,
    )
    second.metadata["source_name"] = "Anthropic News"

    result = prefilter_items([first, second], since=NOW - timedelta(hours=24), config=config)

    assert [item.id for item in result.items] == ["first", "second"]


def test_newsletter_uses_seven_day_window_while_rss_remains_24_hours():
    config = FilteringConfig(
        rule_prefilter_enabled=True,
        min_content_chars=0,
        source_time_window_hours={"newsletter": 168},
    )
    newsletter = _item(
        "newsletter",
        "AI builder explains a new product workflow",
        "https://example.com/newsletter",
        content="Detailed AI product workflow",
        published_at=NOW - timedelta(days=6),
        source=SourceType.NEWSLETTER,
    )
    rss = _item(
        "rss-old",
        "AI media reports a new product workflow",
        "https://example.com/rss-old",
        content="Detailed AI product report",
        published_at=NOW - timedelta(days=2),
    )

    result = prefilter_items(
        [newsletter, rss],
        since=NOW - timedelta(hours=24),
        config=config,
        reference_time=NOW,
    )

    assert [item.id for item in result.items] == ["newsletter"]
    assert result.stats.dropped_outside_window == 1
