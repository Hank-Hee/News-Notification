"""Fetch public newsletter archives through Apify Website Content Crawler."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import os
from urllib.parse import urlsplit

import httpx

from ..models import ContentItem, NewsletterConfig, NewsletterSourceConfig, SourceType


class NewsletterScraper:
    """Run one bounded crawl for all configured free newsletter archives."""

    API_BASE = "https://api.apify.com/v2"

    def __init__(self, config: NewsletterConfig, client: httpx.AsyncClient):
        self.config = config
        self.client = client

    async def fetch(self, since: datetime) -> list[ContentItem]:
        if not self.config.enabled:
            return []
        token = os.getenv(self.config.apify_token_env)
        if not token:
            raise ValueError(
                f"Apify token not found in env var '{self.config.apify_token_env}'"
            )
        sources = [source for source in self.config.sources if source.enabled]
        if not sources:
            return []

        run = await self._start_run(token, sources)
        run_id = str(run.get("id") or "")
        dataset_id = str(run.get("defaultDatasetId") or "")
        if not run_id:
            raise RuntimeError("Newsletter crawler did not return an Apify run ID")
        run = await self._wait_for_run(token, run_id, run)
        dataset_id = str(run.get("defaultDatasetId") or dataset_id)
        if not dataset_id:
            raise RuntimeError("Newsletter crawler did not return a dataset ID")
        rows = await self._fetch_dataset(token, dataset_id)
        return self._to_items(rows, sources, since)

    async def _start_run(
        self, token: str, sources: list[NewsletterSourceConfig]
    ) -> dict:
        include_globs = [
            glob for source in sources for glob in source.include_url_globs
        ]
        payload = {
            "startUrls": [{"url": str(source.start_url)} for source in sources],
            "includeUrlGlobs": include_globs,
            "crawlerType": "playwright:adaptive",
            "maxCrawlDepth": self.config.max_crawl_depth,
            "maxCrawlPages": self.config.max_crawl_pages,
            "maxResults": self.config.max_crawl_pages,
            "saveMarkdown": True,
            "useSitemaps": False,
            "respectRobotsTxtFile": True,
            "blockMedia": True,
            "proxyConfiguration": {"useApifyProxy": True},
        }
        response = await self.client.post(
            f"{self.API_BASE}/acts/{self.config.actor_id}/runs",
            params={"maxTotalChargeUsd": self.config.max_total_charge_usd},
            headers=self._auth_headers(token),
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()
        body = response.json()
        return body.get("data", body)

    async def _wait_for_run(
        self, token: str, run_id: str, initial: dict
    ) -> dict:
        run = initial
        for _ in range(30):
            status = str(run.get("status") or "").upper()
            if status == "SUCCEEDED":
                return run
            if status in {"FAILED", "ABORTED", "TIMED-OUT"}:
                message = str(run.get("statusMessage") or "unknown error")
                raise RuntimeError(f"Newsletter Apify run {status}: {message}")
            await asyncio.sleep(5)
            response = await self.client.get(
                f"{self.API_BASE}/actor-runs/{run_id}",
                headers=self._auth_headers(token),
                timeout=15.0,
            )
            response.raise_for_status()
            body = response.json()
            run = body.get("data", body)
        raise TimeoutError("Newsletter Apify run did not finish within 150 seconds")

    async def _fetch_dataset(self, token: str, dataset_id: str) -> list[dict]:
        response = await self.client.get(
            f"{self.API_BASE}/datasets/{dataset_id}/items",
            params={"clean": "true", "format": "json", "limit": 50},
            headers=self._auth_headers(token),
            timeout=30.0,
        )
        response.raise_for_status()
        rows = response.json()
        return rows if isinstance(rows, list) else []

    @classmethod
    def _to_items(
        cls,
        rows: list[dict],
        sources: list[NewsletterSourceConfig],
        since: datetime,
    ) -> list[ContentItem]:
        by_host = {cls._hostname(str(source.start_url)): source for source in sources}
        start_urls = {cls._url_identity(str(source.start_url)) for source in sources}
        items: list[ContentItem] = []
        seen_urls: set[str] = set()
        for row in rows:
            if not isinstance(row, dict):
                continue
            url = str(row.get("url") or row.get("loadedUrl") or "").strip()
            normalized_url = cls._url_identity(url)
            if not url or normalized_url in start_urls or normalized_url in seen_urls:
                continue
            source = by_host.get(cls._hostname(url))
            if source is None:
                continue
            metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
            published_at = cls._parse_datetime(
                row.get("publishedAt")
                or row.get("datePublished")
                or metadata.get("publishedAt")
                or metadata.get("datePublished")
            )
            if published_at is not None and published_at < since:
                continue
            published_at = published_at or datetime.now(timezone.utc)
            title = str(
                row.get("title")
                or metadata.get("title")
                or urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
                or source.name
            ).strip()
            content = str(row.get("markdown") or row.get("text") or "").strip()
            if not content:
                continue
            native_id = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
            items.append(
                ContentItem(
                    id=f"newsletter:page:{native_id}",
                    source_type=SourceType.NEWSLETTER,
                    title=title,
                    url=url,
                    content=content,
                    author=source.name,
                    published_at=published_at,
                    metadata={
                        "feed_name": source.name,
                        "category": source.category,
                        "is_public_archive": True,
                    },
                )
            )
            seen_urls.add(normalized_url)
        return items

    @staticmethod
    def _parse_datetime(value: object) -> datetime | None:
        text = str(value or "").strip()
        if not text:
            return None
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            try:
                parsed = parsedate_to_datetime(text)
            except (TypeError, ValueError):
                return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)

    @staticmethod
    def _auth_headers(token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    @staticmethod
    def _hostname(url: str) -> str:
        return (urlsplit(url).hostname or "").lower().removeprefix("www.")

    @classmethod
    def _url_identity(cls, url: str) -> str:
        parsed = urlsplit(url)
        path = parsed.path.rstrip("/") or "/"
        return f"{cls._hostname(url)}{path}"
