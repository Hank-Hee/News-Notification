"""Hacker News scraper implementation."""

import logging
import re
from datetime import datetime, timezone
from typing import List, Optional
import asyncio
import httpx

from .base import BaseScraper
from ..models import ContentItem, SourceType, HackerNewsConfig

logger = logging.getLogger(__name__)

# Max top-level comments to fetch per story
TOP_COMMENTS_LIMIT = 5


class HackerNewsScraper(BaseScraper):
    """Scraper for Hacker News stories with top comments."""

    def __init__(self, config: HackerNewsConfig, http_client: httpx.AsyncClient):
        super().__init__(config.model_dump(), http_client)
        self.base_url = "https://hacker-news.firebaseio.com/v0"

    async def fetch(self, since: datetime) -> List[ContentItem]:
        if not self.config.get("enabled", True):
            return []

        try:
            stream_specs = [
                (
                    "topstories",
                    self.config.get("fetch_top_stories", 30),
                    self.config.get("min_score", 100),
                    "Hacker News Top",
                    self.config.get("category"),
                ),
                (
                    "showstories",
                    self.config.get("fetch_show_stories", 0),
                    self.config.get("show_min_score", 5),
                    "Show HN",
                    self.config.get("show_category"),
                ),
            ]
            stream_results = await asyncio.gather(
                *[
                    self._fetch_stream(*spec, since)
                    for spec in stream_specs
                    if spec[1] > 0
                ]
            )
            items: List[ContentItem] = []
            seen_ids: set[str] = set()
            for stream_items in stream_results:
                for item in stream_items:
                    if item.id not in seen_ids:
                        seen_ids.add(item.id)
                        items.append(item)
            return items

        except httpx.HTTPError as e:
            logger.warning("Error fetching Hacker News stories: %s", e)
            return []

    async def _fetch_stream(
        self,
        endpoint: str,
        fetch_count: int,
        min_score: int,
        source_name: str,
        category: Optional[str],
        since: datetime,
    ) -> List[ContentItem]:
        response = await self.client.get(f"{self.base_url}/{endpoint}.json")
        response.raise_for_status()
        story_ids = response.json()[:fetch_count]
        stories = await asyncio.gather(
            *[self._fetch_story(story_id) for story_id in story_ids],
            return_exceptions=True,
        )
        valid_stories = []
        comment_tasks = []
        for story in stories:
            if isinstance(story, Exception) or story is None:
                continue
            if story.get("score", 0) < min_score:
                continue
            published_at = datetime.fromtimestamp(story["time"], tz=timezone.utc)
            if published_at < since:
                continue
            valid_stories.append(story)
            comment_tasks.append(
                self._fetch_comments(story.get("kids", [])[:TOP_COMMENTS_LIMIT])
            )
        all_comments = await asyncio.gather(*comment_tasks, return_exceptions=True)
        items = []
        for story, comments in zip(valid_stories, all_comments):
            if isinstance(comments, Exception):
                comments = []
            item = self._parse_story(story, comments, source_name, category)
            if item:
                items.append(item)
        return items

    async def _fetch_story(self, story_id: int) -> Optional[dict]:
        try:
            response = await self.client.get(f"{self.base_url}/item/{story_id}.json")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None

    async def _fetch_comments(self, comment_ids: List[int]) -> List[dict]:
        """Fetch multiple comments concurrently."""
        if not comment_ids:
            return []

        tasks = [self._fetch_story(cid) for cid in comment_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        comments = []
        for r in results:
            if isinstance(r, dict) and r.get("text") and not r.get("deleted") and not r.get("dead"):
                comments.append(r)
        return comments

    def _parse_story(
        self,
        story: dict,
        comments: List[dict],
        source_name: str = "Hacker News Top",
        category: Optional[str] = None,
    ) -> ContentItem:
        story_id = story["id"]
        title = story.get("title", "")
        url = story.get("url", f"https://news.ycombinator.com/item?id={story_id}")
        author = story.get("by", "unknown")
        published_at = datetime.fromtimestamp(story["time"], tz=timezone.utc)

        # Build content: original text + top comments
        parts = []
        if story.get("text"):
            parts.append(story["text"])

        if comments:
            parts.append("\n--- Top Comments ---")
            for c in comments:
                commenter = c.get("by", "anon")
                text = c.get("text", "")
                # Strip HTML tags roughly
                text = re.sub(r'<[^>]+>', ' ', text).strip()
                # Truncate very long comments
                if len(text) > 500:
                    text = text[:497] + "..."
                parts.append(f"[{commenter}]: {text}")

        content = "\n\n".join(parts)
        hn_discussion_url = f"https://news.ycombinator.com/item?id={story_id}"

        return ContentItem(
            id=self._generate_id("hackernews", "story", str(story_id)),
            source_type=SourceType.HACKERNEWS,
            title=title,
            url=url,
            content=content,
            author=author,
            published_at=published_at,
            metadata={
                "score": story.get("score", 0),
                "descendants": story.get("descendants", 0),
                "type": story.get("type", "story"),
                "discussion_url": hn_discussion_url,
                "comment_count": len(comments),
                "source_name": source_name,
                "category": category if category is not None else self.config.get("category"),
            }
        )
