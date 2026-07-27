"""Fetch one public newsletter via its feed, with an isolated Apify fallback."""

from __future__ import annotations

import asyncio
import calendar
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import os
from urllib.parse import urlsplit

import feedparser
import httpx

from ..models import ContentItem, NewsletterConfig, NewsletterSourceConfig, SourceType


class NewsletterScraper:
    """Fetch one free newsletter without login or paywalled content."""

    API_BASE = "https://api.apify.com/v2"

    def __init__(
        self,
        config: NewsletterConfig,
        source: NewsletterSourceConfig,
        client: httpx.AsyncClient,
    ):
        self.config = config
        self.source = source
        self.client = client

    async def fetch(self, since: datetime) -> list[ContentItem]:
        if not self.config.enabled or not self.source.enabled:
            return []

        feed_failures: list[str] = []
        feed_urls = [
            url
            for url in [self.source.feed_url, *self.source.fallback_feed_urls]
            if url is not None
        ]
        for feed_url in feed_urls:
            try:
                items = await self._fetch_public_feed(str(feed_url), since)
                print(
                    f"   Used public feed for {self.source.name}: "
                    f"{len(items)} item(s) in lookback window"
                )
                return items
            except Exception as exc:
                failure = f"{type(exc).__name__}: {exc}"
                feed_failures.append(failure)
                print(
                    f"   Public feed unavailable for {self.source.name} "
                    f"({failure})"
                )

        feed_error_detail = "; ".join(feed_failures)
        if feed_failures:
            print(f"   All public feeds failed for {self.source.name}; using Apify fallback")

        token = os.getenv(self.config.apify_token_env)
        if not token:
            detail = (
                f" after public feeds failed ({feed_error_detail})"
                if feed_failures
                else ""
            )
            raise ValueError(
                f"Apify token not found in env var '{self.config.apify_token_env}'{detail}"
            )

        try:
            items = await self._fetch_with_apify(token, since)
        except Exception as exc:
            if feed_failures:
                raise RuntimeError(
                    f"public feeds failed ({feed_error_detail}); "
                    f"Apify fallback failed ({type(exc).__name__}: {exc})"
                ) from exc
            raise
        print(
            f"   Used Apify fallback for {self.source.name}: "
            f"{len(items)} item(s) in lookback window"
        )
        return items

    async def _fetch_public_feed(
        self,
        feed_url: str,
        since: datetime,
    ) -> list[ContentItem]:
        response = await self.client.get(
            feed_url,
            follow_redirects=True,
            timeout=30.0,
        )
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        if not feed.version and not feed.entries:
            detail = str(getattr(feed, "bozo_exception", "invalid feed"))
            raise ValueError(f"invalid RSS/Atom response: {detail}")

        items: list[ContentItem] = []
        seen_urls: set[str] = set()
        for entry in feed.entries:
            url = str(entry.get("link") or "").strip()
            normalized_url = self._url_identity(url)
            published_at = self._entry_datetime(entry)
            if (
                not url
                or not published_at
                or published_at < since
                or normalized_url in seen_urls
            ):
                continue
            title = str(entry.get("title") or self.source.name).strip()
            content = self._entry_content(entry).strip()
            if not content:
                continue
            native_id = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
            items.append(
                ContentItem(
                    id=f"newsletter:feed:{native_id}",
                    source_type=SourceType.NEWSLETTER,
                    title=title,
                    url=url,
                    content=content,
                    author=str(entry.get("author") or self.source.name),
                    published_at=published_at,
                    metadata={
                        "feed_name": self.source.name,
                        "category": self.source.category,
                        "is_public_archive": True,
                        "fetch_method": "public_feed",
                    },
                )
            )
            seen_urls.add(normalized_url)
        return items

    async def _fetch_with_apify(
        self, token: str, since: datetime
    ) -> list[ContentItem]:
        run = await self._start_run(token)
        run_id = str(run.get("id") or "")
        dataset_id = str(run.get("defaultDatasetId") or "")
        if not run_id:
            raise RuntimeError("Newsletter crawler did not return an Apify run ID")
        run = await self._wait_for_run(token, run_id, run)
        dataset_id = str(run.get("defaultDatasetId") or dataset_id)
        if not dataset_id:
            raise RuntimeError("Newsletter crawler did not return a dataset ID")
        rows = await self._fetch_dataset(token, dataset_id)
        return self._to_items(rows, self.source, since)

    async def _start_run(self, token: str) -> dict:
        enabled_count = max(
            1,
            sum(source.enabled for source in self.config.sources),
        )
        # Apify rejects values infinitesimally below its USD minimum.  For
        # example, 0.3 / 3 serializes as 0.09999999999999999 without rounding.
        per_source_charge = round(
            self.config.max_total_charge_usd / enabled_count,
            2,
        )
        payload = {
            "startUrls": [{"url": str(self.source.start_url)}],
            "includeUrlGlobs": self.source.include_url_globs,
            "crawlerType": "cheerio",
            "maxCrawlDepth": self.config.max_crawl_depth,
            "maxCrawlPages": self.config.max_crawl_pages,
            "maxResults": self.config.max_crawl_pages,
            "saveMarkdown": True,
            "useSitemaps": False,
            "respectRobotsTxtFile": True,
            "proxyConfiguration": {"useApifyProxy": True},
        }
        response = await self.client.post(
            f"{self.API_BASE}/acts/{self.config.actor_id}/runs",
            params={"maxTotalChargeUsd": per_source_charge},
            headers=self._auth_headers(token),
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()
        body = response.json()
        return body.get("data", body)

    async def _wait_for_run(self, token: str, run_id: str, initial: dict) -> dict:
        run = initial
        loop = asyncio.get_running_loop()
        deadline = loop.time() + self.config.max_wait_seconds
        while True:
            status = str(run.get("status") or "").upper()
            if status == "SUCCEEDED":
                return run
            if status in {"FAILED", "ABORTED", "TIMED-OUT"}:
                message = str(run.get("statusMessage") or "unknown error")
                raise RuntimeError(f"Newsletter Apify run {status}: {message}")
            if loop.time() >= deadline:
                raise TimeoutError(
                    "Newsletter Apify run did not finish within "
                    f"{self.config.max_wait_seconds} seconds"
                )
            await asyncio.sleep(min(5, max(0, deadline - loop.time())))
            response = await self.client.get(
                f"{self.API_BASE}/actor-runs/{run_id}",
                headers=self._auth_headers(token),
                timeout=15.0,
            )
            response.raise_for_status()
            body = response.json()
            run = body.get("data", body)

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
        source: NewsletterSourceConfig,
        since: datetime,
    ) -> list[ContentItem]:
        start_url = cls._url_identity(str(source.start_url))
        items: list[ContentItem] = []
        seen_urls: set[str] = set()
        for row in rows:
            if not isinstance(row, dict):
                continue
            url = str(row.get("url") or row.get("loadedUrl") or "").strip()
            normalized_url = cls._url_identity(url)
            if not url or normalized_url == start_url or normalized_url in seen_urls:
                continue
            if cls._hostname(url) != cls._hostname(str(source.start_url)):
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
                        "fetch_method": "apify",
                    },
                )
            )
            seen_urls.add(normalized_url)
        return items

    @staticmethod
    def _entry_datetime(entry: dict) -> datetime | None:
        for field in ("published", "updated", "created"):
            parsed = entry.get(f"{field}_parsed")
            if parsed:
                return datetime.fromtimestamp(calendar.timegm(parsed), tz=timezone.utc)
            value = entry.get(field)
            if value:
                result = NewsletterScraper._parse_datetime(value)
                if result:
                    return result
        return None

    @staticmethod
    def _entry_content(entry: dict) -> str:
        content = entry.get("content")
        if isinstance(content, list) and content:
            value = content[0].get("value")
            if value:
                return str(value)
        return str(entry.get("summary") or entry.get("description") or "")

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
