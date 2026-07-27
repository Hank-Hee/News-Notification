"""Tests for the bounded public-newsletter Apify scraper."""

import asyncio
import json
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from src.models import NewsletterConfig, NewsletterSourceConfig
from src.scrapers.newsletter import NewsletterScraper


def _config(**overrides) -> NewsletterConfig:
    values = {
        "enabled": True,
        "max_total_charge_usd": 0.3,
        "max_crawl_pages": 15,
        "max_crawl_depth": 1,
        "sources": [
            NewsletterSourceConfig(
                name="Example Letter",
                start_url="https://www.example.com/archive",
                include_url_globs=["https://www.example.com/p/**"],
                category="builder-newsletter",
            )
        ],
    }
    values.update(overrides)
    return NewsletterConfig(**values)


def _scraper(config: NewsletterConfig, client: httpx.AsyncClient) -> NewsletterScraper:
    return NewsletterScraper(config, config.sources[0], client)


def test_disabled_newsletter_does_not_require_token(monkeypatch):
    monkeypatch.delenv("APIFY_TOKEN", raising=False)
    client = httpx.AsyncClient(transport=httpx.MockTransport(lambda request: None))

    items = asyncio.run(
        _scraper(_config(enabled=False), client).fetch(
            datetime.now(timezone.utc) - timedelta(days=1)
        )
    )
    asyncio.run(client.aclose())

    assert items == []


def test_missing_apify_token_is_explicit(monkeypatch):
    monkeypatch.delenv("APIFY_TOKEN", raising=False)
    client = httpx.AsyncClient(transport=httpx.MockTransport(lambda request: None))

    with pytest.raises(ValueError, match="APIFY_TOKEN"):
        asyncio.run(
            _scraper(_config(), client).fetch(
                datetime.now(timezone.utc) - timedelta(days=1)
            )
        )
    asyncio.run(client.aclose())


def test_newsletter_run_is_bounded_and_token_stays_in_header(monkeypatch):
    monkeypatch.setenv("APIFY_TOKEN", "test-token")
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and "/runs" in request.url.path:
            captured["payload"] = json.loads(request.content)
            captured["authorization"] = request.headers.get("Authorization")
            captured["max_total_charge"] = request.url.params.get(
                "maxTotalChargeUsd"
            )
            captured["token_in_url"] = "token" in request.url.params
            return httpx.Response(
                200,
                json={
                    "data": {
                        "id": "run-1",
                        "status": "SUCCEEDED",
                        "defaultDatasetId": "dataset-1",
                    }
                },
            )
        if "/datasets/" in request.url.path:
            return httpx.Response(200, json=[])
        raise AssertionError(f"Unexpected request: {request.url}")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    asyncio.run(
        _scraper(_config(), client).fetch(
            datetime.now(timezone.utc) - timedelta(days=1)
        )
    )
    asyncio.run(client.aclose())

    assert captured["authorization"] == "Bearer test-token"
    assert captured["max_total_charge"] == "0.3"
    assert captured["token_in_url"] is False
    assert captured["payload"]["startUrls"] == [
        {"url": "https://www.example.com/archive"}
    ]
    assert captured["payload"]["includeUrlGlobs"] == [
        "https://www.example.com/p/**"
    ]
    assert captured["payload"]["maxCrawlPages"] == 15
    assert captured["payload"]["maxResults"] == 15
    assert captured["payload"]["maxCrawlDepth"] == 1
    assert captured["payload"]["respectRobotsTxtFile"] is True
    assert captured["payload"]["crawlerType"] == "cheerio"


def test_per_source_apify_charge_is_rounded_to_currency_precision(monkeypatch):
    monkeypatch.setenv("APIFY_TOKEN", "test-token")
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            captured["max_total_charge"] = request.url.params.get(
                "maxTotalChargeUsd"
            )
            return httpx.Response(
                200,
                json={
                    "data": {
                        "id": "run-1",
                        "status": "SUCCEEDED",
                        "defaultDatasetId": "dataset-1",
                    }
                },
            )
        if "/datasets/" in request.url.path:
            return httpx.Response(200, json=[])
        raise AssertionError(f"Unexpected request: {request.url}")

    config = _config()
    config.sources.extend(
        [
            NewsletterSourceConfig(
                name="Second Letter",
                start_url="https://second.example.com/archive",
            ),
            NewsletterSourceConfig(
                name="Third Letter",
                start_url="https://third.example.com/archive",
            ),
        ]
    )
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    asyncio.run(
        _scraper(config, client).fetch(
            datetime.now(timezone.utc) - timedelta(days=7)
        )
    )
    asyncio.run(client.aclose())

    assert captured["max_total_charge"] == "0.1"


def test_dataset_keeps_recent_articles_and_normalizes_www_host(monkeypatch):
    monkeypatch.setenv("APIFY_TOKEN", "test-token")
    now = datetime.now(timezone.utc)
    rows = [
        {
            "url": "https://example.com/archive",
            "title": "Archive",
            "markdown": "Archive index",
        },
        {
            "url": "https://example.com/p/new-product",
            "title": "How we built an AI product",
            "markdown": "A public article describing the product workflow.",
            "publishedAt": now.isoformat(),
        },
        {
            "url": "https://example.com/p/old-product",
            "title": "Old article",
            "markdown": "This should be filtered by date.",
            "publishedAt": (now - timedelta(days=3)).isoformat(),
        },
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(
                200,
                json={
                    "data": {
                        "id": "run-1",
                        "status": "SUCCEEDED",
                        "defaultDatasetId": "dataset-1",
                    }
                },
            )
        if "/datasets/" in request.url.path:
            return httpx.Response(200, json=rows)
        raise AssertionError(f"Unexpected request: {request.url}")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    items = asyncio.run(
        _scraper(_config(), client).fetch(now - timedelta(days=1))
    )
    asyncio.run(client.aclose())

    assert len(items) == 1
    assert items[0].title == "How we built an AI product"
    assert items[0].source_type.value == "newsletter"
    assert items[0].metadata == {
        "feed_name": "Example Letter",
        "category": "builder-newsletter",
        "is_public_archive": True,
        "fetch_method": "apify",
    }


def test_public_feed_is_primary_and_does_not_require_apify_token(monkeypatch):
    monkeypatch.delenv("APIFY_TOKEN", raising=False)
    now = datetime.now(timezone.utc)
    published = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0"><channel><title>Example Letter</title>
      <item><title>New AI product workflow</title>
      <link>https://example.com/p/new-ai-product</link>
      <pubDate>{published}</pubDate>
      <description>An AI builder explains the product workflow.</description></item>
    </channel></rss>"""
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, text=feed, headers={"content-type": "application/xml"})

    config = _config()
    config.sources[0].feed_url = "https://example.com/feed"
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    items = asyncio.run(_scraper(config, client).fetch(now - timedelta(days=7)))
    asyncio.run(client.aclose())

    assert len(items) == 1
    assert items[0].metadata["fetch_method"] == "public_feed"
    assert [request.method for request in requests] == ["GET"]


def test_feed_failure_falls_back_to_apify(monkeypatch):
    monkeypatch.setenv("APIFY_TOKEN", "test-token")
    methods = []

    def handler(request: httpx.Request) -> httpx.Response:
        methods.append(request.method)
        if request.method == "GET" and request.url.path == "/feed":
            return httpx.Response(403, text="blocked")
        if request.method == "POST":
            return httpx.Response(
                200,
                json={
                    "data": {
                        "id": "run-1",
                        "status": "SUCCEEDED",
                        "defaultDatasetId": "dataset-1",
                    }
                },
            )
        if "/datasets/" in request.url.path:
            return httpx.Response(200, json=[])
        raise AssertionError(f"Unexpected request: {request.url}")

    config = _config()
    config.sources[0].feed_url = "https://example.com/feed"
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    items = asyncio.run(
        _scraper(config, client).fetch(datetime.now(timezone.utc) - timedelta(days=7))
    )
    asyncio.run(client.aclose())

    assert items == []
    assert methods == ["GET", "POST", "GET"]
