"""Tests for bounded, key-less public web intelligence sources."""

import asyncio
from datetime import datetime, timedelta, timezone

import httpx

from src.models import PublicWebSourceConfig
from src.scrapers.public_web import PublicWebScraper


def _run(source: PublicWebSourceConfig, handler):
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    items = asyncio.run(
        PublicWebScraper(source, client).fetch(
            datetime.now(timezone.utc) - timedelta(days=7)
        )
    )
    asyncio.run(client.aclose())
    return items


def test_sitemap_filters_prefix_date_exclusions_and_limit():
    recent = datetime.now(timezone.utc).isoformat()
    xml = f"""<?xml version="1.0"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://example.com/news/ai-product</loc><lastmod>{recent}</lastmod></url>
      <url><loc>https://example.com/news/gpu-chip</loc><lastmod>{recent}</lastmod></url>
      <url><loc>https://example.com/about</loc><lastmod>{recent}</lastmod></url>
    </urlset>"""
    source = PublicWebSourceConfig(
        name="Example News",
        kind="sitemap",
        url="https://example.com/sitemap.xml",
        url_prefix="https://example.com/news/",
        exclude_url_contains=["gpu"],
        max_items=1,
        category="official-ai",
    )

    items = _run(source, lambda request: httpx.Response(200, text=xml))

    assert len(items) == 1
    assert str(items[0].url) == "https://example.com/news/ai-product"
    assert items[0].metadata["source_name"] == "Example News"
    assert items[0].source_type.value == "public_web"


def test_html_changelog_extracts_recent_release():
    recent = datetime.now(timezone.utc).isoformat()
    html = f"""
    <article><h2>AI Agent mode is available</h2>
      <a href="/en-US/changelog/agent-mode">Details</a>
      <time datetime="{recent}">today</time>
      <p>A new AI agent workflow for builders.</p>
    </article>"""
    source = PublicWebSourceConfig(
        name="Cursor Changelog",
        kind="html_changelog",
        url="https://cursor.com/en-US/changelog",
    )

    items = _run(source, lambda request: httpx.Response(200, text=html))

    assert len(items) == 1
    assert items[0].title == "AI Agent mode is available"
    assert str(items[0].url).endswith("/en-US/changelog/agent-mode")


def test_openrouter_public_models_api_creates_one_top_five_event():
    rows = [
        {"id": f"vendor/model-{index}", "name": f"AI Model {index}", "description": "AI model"}
        for index in range(1, 7)
    ]
    source = PublicWebSourceConfig(
        name="OpenRouter Rankings",
        kind="openrouter_rankings",
        url="https://openrouter.ai/api/v1/models?sort=most-popular",
        public_url="https://openrouter.ai/rankings",
        max_items=5,
    )

    items = _run(source, lambda request: httpx.Response(200, json={"data": rows}))

    assert len(items) == 1
    assert "5. AI Model 5" in (items[0].content or "")
    assert "AI Model 6" not in (items[0].content or "")


def test_github_file_update_uses_existing_repository_token(monkeypatch):
    recent = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    captured = {}
    monkeypatch.setenv("GITHUB_TOKEN", "repository-token")
    source = PublicWebSourceConfig(
        name="LMArena",
        kind="github_file_updates",
        url="https://api.github.com/repos/lmarena/arena-catalog/commits?path=data.json",
        public_url="https://arena.ai/leaderboard",
    )

    def handler(request: httpx.Request) -> httpx.Response:
        captured["authorization"] = request.headers.get("Authorization")
        return httpx.Response(
            200,
            json=[
                {
                    "sha": "abc123",
                    "html_url": "https://github.com/lmarena/arena-catalog/commit/abc123",
                    "commit": {
                        "message": "Update leaderboard",
                        "author": {"date": recent},
                    },
                }
            ],
        )

    items = _run(source, handler)

    assert len(items) == 1
    assert captured["authorization"] == "Bearer repository-token"
    assert items[0].title == "LMArena: Update leaderboard"
