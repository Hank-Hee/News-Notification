"""Fetch free newsletters exclusively through their public RSS/Atom feeds."""

from __future__ import annotations

import calendar
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
from urllib.parse import urlsplit

import feedparser
import httpx

from ..models import ContentItem, NewsletterConfig, NewsletterSourceConfig, SourceType


class NewsletterScraper:
    """Fetch one newsletter without paid crawlers, login, or paywalled content."""

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

        failures: list[str] = []
        feed_urls = [
            url
            for url in [self.source.feed_url, *self.source.fallback_feed_urls]
            if url is not None
        ]
        if not feed_urls:
            raise RuntimeError(f"No public feed configured for {self.source.name}")

        for feed_url in feed_urls:
            try:
                return await self._fetch_public_feed(str(feed_url), since)
            except Exception as exc:
                failures.append(f"{feed_url}: {type(exc).__name__}: {exc}")

        raise RuntimeError(
            f"All public feeds failed for {self.source.name}: " + "; ".join(failures)
        )

    async def _fetch_public_feed(
        self,
        feed_url: str,
        since: datetime,
    ) -> list[ContentItem]:
        response = await self.client.get(
            feed_url,
            follow_redirects=True,
            timeout=30.0,
            headers={"User-Agent": "Horizon-Aggregator/1.0"},
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
            native_id = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
            items.append(
                ContentItem(
                    id=f"newsletter:feed:{native_id}",
                    source_type=SourceType.NEWSLETTER,
                    title=str(entry.get("title") or self.source.name).strip(),
                    url=url,
                    content=self._entry_content(entry).strip(),
                    author=str(entry.get("author") or self.source.name),
                    published_at=published_at,
                    metadata={
                        "feed_name": self.source.name,
                        "source_name": self.source.name,
                        "category": self.source.category,
                        "is_public_archive": True,
                        "fetch_method": "public_feed",
                    },
                )
            )
            seen_urls.add(normalized_url)
            if len(items) >= self.source.max_items:
                break
        return items

    @staticmethod
    def _entry_datetime(entry: dict) -> datetime | None:
        for field in ("published", "updated", "created"):
            parsed = entry.get(f"{field}_parsed")
            if parsed:
                return datetime.fromtimestamp(calendar.timegm(parsed), tz=timezone.utc)
            value = entry.get(field)
            if value:
                try:
                    result = parsedate_to_datetime(str(value))
                    if result.tzinfo is None:
                        result = result.replace(tzinfo=timezone.utc)
                    return result.astimezone(timezone.utc)
                except (TypeError, ValueError, OverflowError):
                    continue
        return None

    @staticmethod
    def _entry_content(entry: dict) -> str:
        content = entry.get("content")
        if isinstance(content, list) and content:
            return str(content[0].get("value") or "")
        return str(entry.get("summary") or entry.get("description") or "")

    @staticmethod
    def _url_identity(url: str) -> str:
        parsed = urlsplit(url)
        return f"{parsed.scheme.casefold()}://{parsed.netloc.casefold()}{parsed.path.rstrip('/')}"
