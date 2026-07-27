"""Tests for free public newsletter feeds."""

import asyncio
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from src.models import NewsletterConfig, NewsletterSourceConfig
from src.scrapers.newsletter import NewsletterScraper


def _config(**overrides) -> NewsletterConfig:
    values = {
        "enabled": True,
        "sources": [
            NewsletterSourceConfig(
                name="Example Letter",
                start_url="https://example.com/archive",
                feed_url="https://example.com/feed",
                category="builder-newsletter",
                max_items=1,
            )
        ],
    }
    values.update(overrides)
    return NewsletterConfig(**values)


def _run(config: NewsletterConfig, handler, since: datetime):
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    items = asyncio.run(NewsletterScraper(config, config.sources[0], client).fetch(since))
    asyncio.run(client.aclose())
    return items


def _feed(now: datetime, *, title: str = "New AI product workflow") -> str:
    published = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0"><channel><title>Example Letter</title>
      <item><title>{title}</title>
      <link>https://example.com/p/new-ai-product</link>
      <pubDate>{published}</pubDate>
      <description>An AI builder explains the product workflow.</description></item>
    </channel></rss>"""


def test_disabled_newsletter_makes_no_request():
    now = datetime.now(timezone.utc)

    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("disabled source must not make a request")

    assert _run(_config(enabled=False), handler, now - timedelta(days=1)) == []


def test_public_feed_returns_bounded_items_with_source_metadata():
    now = datetime.now(timezone.utc)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=_feed(now), headers={"content-type": "application/xml"})

    items = _run(_config(), handler, now - timedelta(days=7))

    assert len(items) == 1
    assert items[0].source_type.value == "newsletter"
    assert items[0].metadata["source_name"] == "Example Letter"
    assert items[0].metadata["fetch_method"] == "public_feed"


def test_alternate_feed_is_used_after_primary_failure():
    now = datetime.now(timezone.utc)
    requested = []
    config = _config()
    config.sources[0].fallback_feed_urls = ["https://example.com/fallback.xml"]

    def handler(request: httpx.Request) -> httpx.Response:
        requested.append(str(request.url))
        if request.url.path == "/feed":
            return httpx.Response(503, text="unavailable")
        return httpx.Response(200, text=_feed(now))

    items = _run(config, handler, now - timedelta(days=7))

    assert len(items) == 1
    assert requested == ["https://example.com/feed", "https://example.com/fallback.xml"]


def test_all_feed_failures_are_explicit():
    now = datetime.now(timezone.utc)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, text="blocked")

    with pytest.raises(RuntimeError, match="All public feeds failed.*Example Letter"):
        _run(_config(), handler, now - timedelta(days=7))
