"""Key-less first-party web sources that do not expose a conventional feed."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import os
import re
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

from bs4 import BeautifulSoup
import httpx

from .base import BaseScraper
from ..models import ContentItem, PublicWebSourceConfig, SourceType


class PublicWebScraper(BaseScraper):
    """Fetch one bounded public source using a source-specific parser."""

    def __init__(self, source: PublicWebSourceConfig, client: httpx.AsyncClient):
        super().__init__(source.model_dump(), client)
        self.source = source

    async def fetch(self, since: datetime) -> list[ContentItem]:
        if not self.source.enabled:
            return []
        source_since = max(
            self._aware(since),
            datetime.now(timezone.utc) - timedelta(hours=self.source.lookback_hours),
        )
        handlers = {
            "sitemap": self._fetch_sitemap,
            "html_changelog": self._fetch_html_changelog,
            "openrouter_rankings": self._fetch_openrouter_rankings,
            "github_file_updates": self._fetch_github_file_updates,
        }
        return await handlers[self.source.kind](source_since)

    async def _get(self, url: str, **kwargs) -> httpx.Response:
        headers = {"User-Agent": "Horizon-Aggregator/1.0"}
        headers.update(kwargs.pop("headers", {}))
        response = await self.client.get(
            url,
            follow_redirects=True,
            timeout=60.0,
            headers=headers,
            **kwargs,
        )
        response.raise_for_status()
        return response

    async def _fetch_sitemap(self, since: datetime) -> list[ContentItem]:
        response = await self._get(str(self.source.url))
        root = ElementTree.fromstring(response.content)
        records: list[tuple[datetime, str]] = []
        prefix = self.source.url_prefix or ""
        excluded = [part.casefold() for part in self.source.exclude_url_contains]
        for node in root.iter():
            if not node.tag.endswith("url"):
                continue
            loc_node = next((child for child in node if child.tag.endswith("loc")), None)
            date_node = next((child for child in node if child.tag.endswith("lastmod")), None)
            url = (loc_node.text or "").strip() if loc_node is not None else ""
            if not url or (prefix and not url.startswith(prefix)):
                continue
            if any(part in url.casefold() for part in excluded):
                continue
            published_at = self._parse_datetime(date_node.text if date_node is not None else None)
            if not published_at or published_at < since:
                continue
            records.append((published_at, url))

        records.sort(reverse=True)
        return [
            self._item(
                subtype="sitemap",
                native_id=url,
                title=self._title_from_url(url),
                url=url,
                content=f"{self.source.name} official AI product or research update.",
                published_at=published_at,
                fetch_method="public_sitemap",
            )
            for published_at, url in records[: self.source.max_items]
        ]

    async def _fetch_html_changelog(self, since: datetime) -> list[ContentItem]:
        response = await self._get(str(self.source.url))
        soup = BeautifulSoup(response.text, "html.parser")
        items: list[ContentItem] = []
        seen_urls: set[str] = set()
        for time_node in soup.find_all("time"):
            published_at = self._parse_datetime(time_node.get("datetime") or time_node.get_text(" ", strip=True))
            if not published_at or published_at < since:
                continue
            container = time_node
            link = None
            for _ in range(6):
                if container is None:
                    break
                link = container.find("a", href=re.compile(r"/changelog/"))
                if link:
                    break
                container = container.parent
            if not link:
                continue
            url = str(httpx.URL(str(self.source.url)).join(str(link.get("href"))))
            if url in seen_urls:
                continue
            heading = container.find(["h1", "h2", "h3", "h4"]) if container else None
            title = (heading or link).get_text(" ", strip=True)
            content = container.get_text(" ", strip=True)[:2000] if container else title
            items.append(
                self._item(
                    subtype="changelog",
                    native_id=url,
                    title=title or self._title_from_url(url),
                    url=url,
                    content=content,
                    published_at=published_at,
                    fetch_method="official_changelog",
                )
            )
            seen_urls.add(url)
            if len(items) >= self.source.max_items:
                break
        return items

    async def _fetch_openrouter_rankings(self, since: datetime) -> list[ContentItem]:
        response = await self._get(str(self.source.url))
        rows = response.json().get("data", [])[: self.source.max_items]
        if not rows:
            return []
        lines = []
        for index, row in enumerate(rows, start=1):
            name = row.get("name") or row.get("id") or "unknown"
            lines.append(f"{index}. {name}: {str(row.get('description') or '').strip()[:240]}")
        content = "\n".join(lines)
        return [
            self._item(
                subtype="ranking",
                native_id="openrouter-popular-models",
                title="OpenRouter AI 模型热度 Top 5",
                url=str(self.source.public_url or self.source.url),
                content=content,
                published_at=datetime.now(timezone.utc),
                fetch_method="public_api",
                extra={"event_key": "openrouter-popular-models"},
            )
        ]

    async def _fetch_github_file_updates(self, since: datetime) -> list[ContentItem]:
        headers = {"Accept": "application/vnd.github+json"}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        response = await self._get(
            str(self.source.url),
            headers=headers,
            params={"since": since.isoformat(), "per_page": self.source.max_items},
        )
        items: list[ContentItem] = []
        for row in response.json()[: self.source.max_items]:
            commit = row.get("commit") or {}
            author = commit.get("author") or {}
            published_at = self._parse_datetime(author.get("date"))
            if not published_at or published_at < since:
                continue
            sha = str(row.get("sha") or "")
            message = str(commit.get("message") or "Leaderboard data updated").splitlines()[0]
            items.append(
                self._item(
                    subtype="file-update",
                    native_id=sha,
                    title=f"{self.source.name}: {message}",
                    url=str(row.get("html_url") or self.source.public_url or self.source.url),
                    content=f"Official AI leaderboard data changed. Commit: {message}",
                    published_at=published_at,
                    fetch_method="github_public_api",
                )
            )
        return items

    def _item(
        self,
        *,
        subtype: str,
        native_id: str,
        title: str,
        url: str,
        content: str,
        published_at: datetime,
        fetch_method: str,
        extra: dict | None = None,
    ) -> ContentItem:
        digest = hashlib.sha256(native_id.encode("utf-8")).hexdigest()[:20]
        metadata = {
            "source_name": self.source.name,
            "category": self.source.category,
            "fetch_method": fetch_method,
            "is_public_source": True,
        }
        metadata.update(extra or {})
        return ContentItem(
            id=self._generate_id(SourceType.PUBLIC_WEB.value, subtype, digest),
            source_type=SourceType.PUBLIC_WEB,
            title=title,
            url=url,
            content=content,
            author=self.source.name,
            published_at=published_at,
            metadata=metadata,
        )

    @staticmethod
    def _parse_datetime(value: object) -> datetime | None:
        if not value:
            return None
        raw = str(value).strip().replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(raw)
        except ValueError:
            try:
                parsed = datetime.strptime(raw, "%B %d, %Y")
            except ValueError:
                return None
        return PublicWebScraper._aware(parsed)

    @staticmethod
    def _aware(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def _title_from_url(url: str) -> str:
        slug = unquote(urlsplit(url).path.rstrip("/").split("/")[-1])
        return re.sub(r"[-_]+", " ", slug).strip().title() or "Official AI update"
