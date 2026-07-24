"""Main orchestrator coordinating the entire workflow."""

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Dict, List, Literal, Optional
from urllib.parse import unquote_plus, urlsplit
from zoneinfo import ZoneInfo
import httpx
from rich.console import Console

from .models import Config, ContentItem
from .storage.manager import StorageManager, safe_output_path
from ._file_utils import _atomic_write_text
from .history import EventHistoryIndex
from .prefilter import prefilter_items
from .product_intelligence import ProductIntelligenceDatabase
from .redaction import is_fatal_ai_error, redact_secrets
from .services.email import EmailManager
from .services.webhook import WebhookNotifier
from .scrapers.github import GitHubScraper
from .scrapers.hackernews import HackerNewsScraper
from .scrapers.rss import RSSScraper
from .scrapers.reddit import RedditScraper
from .scrapers.telegram import TelegramScraper
from .scrapers.twitter import TwitterScraper
from .scrapers.twitter_playwright import TwitterPlaywrightScraper
from .scrapers.openbb import OpenBBScraper
from .scrapers.ossinsight import OSSInsightScraper
from .scrapers.gdelt import GDELTScraper
from .scrapers.google_news import GoogleNewsScraper
from .ai.client import create_ai_client
from .ai.analyzer import ContentAnalyzer
from .ai.summarizer import DailySummarizer
from .ai.enricher import ContentEnricher
from .ai.tokens import get_usage_snapshot, reset_usage, usage_stage


_TRACKING_QUERY_PARAMETERS = {
    "_ga",
    "dclid",
    "fbclid",
    "gclid",
    "igshid",
    "li_fat_id",
    "mc_cid",
    "mc_eid",
    "msclkid",
    "ttclid",
    "twclid",
    "vero_id",
}


def _deduplication_url_key(url: str) -> tuple[str, str, str, str, Optional[int], str, str]:
    """Return a conservative URL identity key for cross-source deduplication."""
    parsed = urlsplit(url)
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    port = parsed.port
    if (scheme, port) in {("http", 80), ("https", 443)}:
        port = None

    path = parsed.path.rstrip("/") or "/"
    query_parts = []
    for part in parsed.query.split("&") if parsed.query else []:
        name = unquote_plus(part.partition("=")[0]).lower()
        if name.startswith("utm_") or name in _TRACKING_QUERY_PARAMETERS:
            continue
        query_parts.append(part)

    return (
        scheme,
        parsed.username or "",
        parsed.password or "",
        host,
        port,
        path,
        "&".join(query_parts),
    )


@dataclass
class BalancedDigestResult:
    """Items and selection statistics from balanced digest filtering."""

    items: List[ContentItem]
    enabled: bool = False
    group_counts: Dict[str, int] = field(default_factory=dict)
    group_limits: Dict[str, Optional[int]] = field(default_factory=dict)
    duplicate_categories: List[str] = field(default_factory=list)


@dataclass
class FilteringPipelineResult:
    """Items and statistics from score, topic, and digest filtering."""

    items: List[ContentItem]
    threshold_count: int
    topic_dedup_count: int
    topic_dedup_removed: int
    balanced_digest: BalancedDigestResult


@dataclass
class SourceFetchOutcome:
    """Result of fetching one configured source."""

    source_name: str
    status: Literal["success", "empty", "failure"]
    items: List[ContentItem] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        result: Dict[str, object] = {
            "source": self.source_name,
            "status": self.status,
            "item_count": len(self.items),
        }
        if self.error is not None:
            result["error"] = self.error
        return result


@dataclass
class FetchReport:
    """Aggregate diagnostics for one fetch across configured sources."""

    outcomes: List[SourceFetchOutcome] = field(default_factory=list)

    @property
    def status(self) -> Literal["not_attempted", "success", "partial_failure", "failure"]:
        if not self.outcomes:
            return "not_attempted"
        if self.failed_count == len(self.outcomes):
            return "failure"
        if self.failed_count:
            return "partial_failure"
        return "success"

    @property
    def failed_count(self) -> int:
        return sum(outcome.status == "failure" for outcome in self.outcomes)

    @property
    def all_failed(self) -> bool:
        return bool(self.outcomes) and self.failed_count == len(self.outcomes)

    def failure_message(self) -> str:
        failures = "; ".join(
            f"{outcome.source_name}: {outcome.error or 'unknown error'}"
            for outcome in self.outcomes
            if outcome.status == "failure"
        )
        return f"All {len(self.outcomes)} attempted sources failed ({failures})"

    def to_dict(self) -> Dict[str, object]:
        return {
            "status": self.status,
            "attempted": len(self.outcomes),
            "successful": len(self.outcomes) - self.failed_count,
            "empty": sum(outcome.status == "empty" for outcome in self.outcomes),
            "failed": self.failed_count,
            "item_count": sum(len(outcome.items) for outcome in self.outcomes),
            "sources": [outcome.to_dict() for outcome in self.outcomes],
        }


class HorizonOrchestrator:
    """Orchestrates the complete workflow for content aggregation and analysis."""

    def __init__(self, config: Config, storage: StorageManager):
        """Initialize orchestrator.

        Args:
            config: Application configuration
            storage: Storage manager
        """
        self.config = config
        self.storage = storage
        self.console = Console()
        self.email_manager = EmailManager(config.email, console=self.console) if config.email else None
        self.webhook_notifier = (
            WebhookNotifier(config.webhook, console=self.console)
            if config.webhook and config.webhook.enabled
            else None
        )
        self.last_fetch_report: Optional[FetchReport] = None
        self.history_index = EventHistoryIndex().load()

    async def run(self, force_hours: int = None) -> None:
        """Execute the complete workflow.

        Args:
            force_hours: Optional override for time window in hours
        """
        reset_usage()
        self.console.print("[bold cyan]🌅 Horizon - Starting aggregation...[/bold cyan]\n")

        # Check email subscriptions if configured
        if (
            self.email_manager
            and self.config.email
            and self.config.email.enabled
            and self.config.email.imap_enabled
        ):
            self.console.print("📧 Checking for new email subscriptions...")
            self.email_manager.check_subscriptions(self.storage)

        try:
            # 1. Determine time window
            since = self._determine_time_window(force_hours)
            self.console.print(f"📅 Fetching content since: {since.strftime('%Y-%m-%d %H:%M:%S')}\n")

            # 2. Fetch content from all sources
            all_items = await self.fetch_all_sources(since)
            self.console.print(f"📥 Fetched {len(all_items)} items from all sources\n")

            if self.last_fetch_report and self.last_fetch_report.all_failed:
                raise RuntimeError(self.last_fetch_report.failure_message())

            twitter_config = getattr(
                getattr(self.config, "sources", None), "twitter", None
            )
            if (
                self.last_fetch_report
                and twitter_config
                and twitter_config.enabled
                and twitter_config.required
            ):
                twitter_outcome = next(
                    (
                        outcome
                        for outcome in self.last_fetch_report.outcomes
                        if outcome.source_name == "Twitter"
                    ),
                    None,
                )
                if twitter_outcome and twitter_outcome.status == "failure":
                    raise RuntimeError(
                        "Required source Twitter failed; refusing to publish a digest "
                        f"without first-party X intelligence. {twitter_outcome.error}"
                    )

            if not all_items:
                self.console.print("[yellow]No new content found. Exiting.[/yellow]")
                return

            # 3. Deterministic prefilter before spending any model tokens.
            if self.config.filtering.rule_prefilter_enabled:
                prefilter_result = prefilter_items(
                    all_items,
                    since=since,
                    config=self.config.filtering,
                )
                self.console.print(
                    "🧹 Prefilter statistics: "
                    + json.dumps(prefilter_result.stats.to_dict(), ensure_ascii=False)
                    + "\n"
                )
                if not prefilter_result.items:
                    self.console.print(
                        "[yellow]No candidates survived the deterministic prefilter.[/yellow]"
                    )
                    return
                prefiltered_items = prefilter_result.items
            else:
                prefiltered_items = all_items

            # 4. Merge any remaining cross-source duplicates.
            merged_items = self.merge_cross_source_duplicates(prefiltered_items)
            if len(merged_items) < len(prefiltered_items):
                self.console.print(
                    f"🔗 Merged {len(prefiltered_items) - len(merged_items)} cross-source duplicates "
                    f"→ {len(merged_items)} unique items\n"
                )

            # 5. Batch-score with Kimi.
            analyzed_items = await self._analyze_content(merged_items)
            self.console.print(f"🤖 Analyzed {len(analyzed_items)} items with AI\n")

            # 6. Threshold and semantic deduplication.
            filtering_result = await self.filter_items(
                analyzed_items,
                apply_balance=False,
            )
            important_items = filtering_result.items

            history_result = self.history_index.filter_recent(
                important_items,
                days=self.config.filtering.history_dedup_days,
            )
            important_items = history_result.items
            self.console.print(
                f"🗓️ History dedup excluded {history_result.excluded}; "
                f"allowed substantive updates {history_result.allowed_updates}\n"
            )

            # 5.5 Optional second-stage Twitter reply expansion + targeted re-analysis
            await self._expand_twitter_discussion(important_items)

            # 5.6 Apply digest limits after any targeted re-analysis changes scores.
            important_items = self.apply_balanced_digest(important_items).items
            important_items = self._prioritize_product_intelligence(important_items)

            # Show per-sub-source selection breakdown
            selected_counts: Dict[str, int] = defaultdict(int)
            for item in important_items:
                key = f"{item.source_type.value}/{self._sub_source_label(item)}"
                selected_counts[key] += 1
            for source_key, count in sorted(selected_counts.items()):
                self.console.print(f"      • {source_key}: {count}")
            self.console.print("")

            # 7. Search and deep-analyze Top N only, then summarize daily trends once.
            trend_overview = await self._enrich_important_items(important_items)

            # 8. Generate and save the Chinese daily.
            today = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")
            for lang in self.config.ai.languages:
                summarizer = DailySummarizer()
                summary = await summarizer.generate_summary(
                    important_items,
                    today,
                    len(all_items),
                    language=lang,
                    trend_overview=trend_overview,
                )

                # Save to data/summaries/
                summary_path = self.storage.save_daily_summary(today, summary, language=lang)
                self.console.print(f"💾 Saved {lang.upper()} summary to: {summary_path}\n")

                dest_path = self._write_pages_post(today, summary, lang)
                self.console.print(
                    f"📄 Copied {lang.upper()} summary to GitHub Pages: {dest_path}\n"
                )

                # Send email if configured
                if self.email_manager and self.config.email and self.config.email.enabled:
                    self.console.print(f"📧 Sending {lang.upper()} email summary...")
                    subscribers = self.storage.load_subscribers()
                    subject = f"Horizon Summary ({lang.upper()}) - {today}"
                    self.email_manager.send_daily_summary(summary, subject, subscribers)

                # Send webhook notification if configured
                if self.webhook_notifier:
                    await self.webhook_notifier.send_daily_summary(
                        summary=summary,
                        important_items=important_items,
                        all_items_count=len(all_items),
                        date=today,
                        lang=lang,
                        summarizer=summarizer,
                    )

            if self.config.product_intelligence.enabled:
                database = ProductIntelligenceDatabase(
                    self.config.product_intelligence
                ).load()
                changed = database.upsert(
                    important_items,
                    observed_on=datetime.strptime(today, "%Y-%m-%d").date(),
                )
                published_json, published_csv = database.save_and_publish()
                self.console.print(
                    f"🗂️ Updated {changed} product intelligence records: "
                    f"{published_json}, {published_csv}\n"
                )

            self.history_index.update(
                important_items,
                today=datetime.strptime(today, "%Y-%m-%d").date(),
            )
            self.history_index.save()
            self._copy_history_for_pages()

            self.console.print("[bold green]✅ Horizon completed successfully![/bold green]")
            usage = get_usage_snapshot()
            self.console.print(
                f"\n🧮 AI requests: {usage.total_requests} "
                f"(analysis: {usage.requests_by_stage.get('analysis', 0)}, "
                f"deep analysis: {usage.requests_by_stage.get('deep_analysis', 0)})"
            )
            self.console.print(
                f"   Token usage: input {usage.total_input_tokens}, "
                f"output {usage.total_output_tokens}, total {usage.total_tokens}"
            )
            if usage.usage_reported_requests < usage.total_requests:
                self.console.print("   Provider 未返回 Token 用量（部分或全部请求）")
            for provider, provider_usage in sorted(usage.per_provider.items()):
                self.console.print(
                    f"   • {provider}: {provider_usage.requests} requests, "
                    f"{provider_usage.total} tokens"
                )

        except Exception as e:
            safe_error = redact_secrets(e)
            self.console.print(f"[bold red]❌ Error: {safe_error}[/bold red]")

            # Send webhook failure notification if configured
            if self.webhook_notifier:
                await self.webhook_notifier.send_failure(
                    date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    error_message=safe_error,
                )

            raise

    @staticmethod
    def _write_pages_post(today: str, summary: str, language: str) -> Path:
        """Write a Jekyll post atomically and return its path."""
        posts_dir = Path("docs/_posts")
        posts_dir.mkdir(parents=True, exist_ok=True)
        destination = safe_output_path(
            posts_dir,
            f"{today}-summary-{language}.md",
        )
        front_matter = (
            "---\n"
            "layout: default\n"
            f'title: "AI 产品机会与 Builder 情报 · {today}"\n'
            f"date: {today}\n"
            f"lang: {language}\n"
            "---\n\n"
        )
        summary_content = summary
        first_line = summary_content.strip().split("\n")[0]
        if first_line.startswith("# "):
            parts = summary_content.split("\n", 1)
            summary_content = parts[1].strip() if len(parts) > 1 else ""
        _atomic_write_text(destination, front_matter + summary_content + "\n")
        return destination

    def _copy_history_for_pages(self) -> Path:
        """Publish the history index with the static site for the next Action run."""
        destination_dir = Path("docs/data/history")
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = safe_output_path(destination_dir, "event_index.json")
        content = self.history_index.path.read_text(encoding="utf-8")
        _atomic_write_text(destination, content)
        return destination

    def _determine_time_window(self, force_hours: int = None) -> datetime:
        if force_hours:
            since = datetime.now(timezone.utc) - timedelta(hours=force_hours)
        else:
            hours = self.config.filtering.time_window_hours
            since = datetime.now(timezone.utc) - timedelta(hours=hours)
        return since

    async def fetch_all_sources(self, since: datetime) -> List[ContentItem]:
        """Fetch content from all configured sources.

        This is a stable stage entry point for integrations such as MCP.

        Args:
            since: Fetch items published after this time

        Returns:
            List[ContentItem]: All fetched items
        """
        self.last_fetch_report = None
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = []

            # GitHub sources
            if self.config.sources.github:
                github_scraper = GitHubScraper(self.config.sources.github, client)
                tasks.append(self._fetch_with_progress("GitHub", github_scraper, since))

            # Hacker News
            if self.config.sources.hackernews.enabled:
                hn_scraper = HackerNewsScraper(self.config.sources.hackernews, client)
                tasks.append(self._fetch_with_progress("Hacker News", hn_scraper, since))

            # RSS feeds
            if self.config.sources.rss:
                from .extractors import ExtractorRegistry
                rss_scraper = RSSScraper(
                    self.config.sources.rss,
                    client,
                    ExtractorRegistry(self.config.extractors),
                )
                tasks.append(self._fetch_with_progress("RSS Feeds", rss_scraper, since))

            # Reddit
            if self.config.sources.reddit.enabled:
                reddit_scraper = RedditScraper(self.config.sources.reddit, client)
                tasks.append(self._fetch_with_progress("Reddit", reddit_scraper, since))

            # Telegram
            if self.config.sources.telegram.enabled:
                telegram_scraper = TelegramScraper(self.config.sources.telegram, client)
                tasks.append(self._fetch_with_progress("Telegram", telegram_scraper, since))

            # Twitter (Apify or Playwright mode)
            if self.config.sources.twitter and self.config.sources.twitter.enabled:
                tw_cfg = self.config.sources.twitter
                if tw_cfg.mode == "playwright":
                    twitter_scraper = TwitterPlaywrightScraper(tw_cfg)
                else:
                    twitter_scraper = TwitterScraper(tw_cfg, client)
                tasks.append(self._fetch_with_progress("Twitter", twitter_scraper, since))

            # OpenBB (financial news / filings via the OpenBB Platform SDK)
            if self.config.sources.openbb and self.config.sources.openbb.enabled:
                openbb_scraper = OpenBBScraper(self.config.sources.openbb, client)
                tasks.append(self._fetch_with_progress("OpenBB", openbb_scraper, since))

            # OSS Insight trending repos
            if self.config.sources.ossinsight and self.config.sources.ossinsight.enabled:
                oss_scraper = OSSInsightScraper(self.config.sources.ossinsight, client)
                tasks.append(self._fetch_with_progress("OSS Insight", oss_scraper, since))

            # GDELT 2.0 DOC API (key-less global news)
            if self.config.sources.gdelt and self.config.sources.gdelt.enabled:
                gdelt_scraper = GDELTScraper(self.config.sources.gdelt, client)
                tasks.append(self._fetch_with_progress("GDELT", gdelt_scraper, since))

            # Google News RSS (key-less news search)
            if self.config.sources.google_news and self.config.sources.google_news.enabled:
                gn_scraper = GoogleNewsScraper(self.config.sources.google_news, client)
                tasks.append(self._fetch_with_progress("Google News", gn_scraper, since))

            # Fetch all concurrently
            outcomes = await asyncio.gather(*tasks)
            self.last_fetch_report = FetchReport(outcomes=list(outcomes))

            # Flatten successful and empty outcomes; failures remain in the report.
            all_items: List[ContentItem] = []
            for outcome in outcomes:
                all_items.extend(outcome.items)

            return all_items

    async def _fetch_with_progress(
        self, name: str, scraper, since: datetime
    ) -> SourceFetchOutcome:
        """Fetch from a scraper with progress indication.

        Args:
            name: Source name for display
            scraper: Scraper instance
            since: Fetch items after this time

        Returns:
            SourceFetchOutcome: Named fetch result and diagnostics
        """
        self.console.print(f"🔍 Fetching from {name}...")
        try:
            items = await scraper.fetch(since)
        except Exception as exc:
            error = redact_secrets(f"{type(exc).__name__}: {exc}")
            self.console.print(f"[red]   Failed to fetch {name}: {error}[/red]")
            return SourceFetchOutcome(
                source_name=name,
                status="failure",
                error=error,
            )

        self.console.print(f"   Found {len(items)} items from {name}")

        # Show per-sub-source breakdown when there are multiple sub-sources
        sub_counts: Dict[str, int] = defaultdict(int)
        for item in items:
            sub_counts[self._sub_source_label(item)] += 1
        if len(sub_counts) > 1:
            for sub, count in sorted(sub_counts.items()):
                self.console.print(f"      • {sub}: {count}")

        return SourceFetchOutcome(
            source_name=name,
            status="success" if items else "empty",
            items=items,
        )

    @staticmethod
    def _sub_source_label(item: ContentItem) -> str:
        """Return a human-readable sub-source label for an item."""
        meta = item.metadata
        if meta.get("subreddit"):
            return f"r/{meta['subreddit']}"
        if meta.get("feed_name"):
            return meta["feed_name"]
        if meta.get("channel"):
            return f"@{meta['channel']}"
        if meta.get("period") and meta.get("repo"):
            return f"ossinsight:{meta.get('primary_language', 'all')}"
        if meta.get("repo"):
            return meta["repo"]
        if meta.get("watchlist"):
            return meta["watchlist"]
        if meta.get("source_name"):
            return meta["source_name"]
        if meta.get("twitter_handle"):
            return f"@{meta['twitter_handle']}"
        if meta.get("gn_query"):
            return f"google_news:{meta['gn_query']}"
        if meta.get("domain"):
            return meta["domain"]
        return item.author or "unknown"

    def merge_cross_source_duplicates(self, items: List[ContentItem]) -> List[ContentItem]:
        """Merge items that point to the same URL from different sources.

        This is a stable stage helper for integrations such as MCP.

        Keeps the item with the richest content and combines metadata.

        Args:
            items: Items to deduplicate

        Returns:
            List[ContentItem]: Deduplicated items
        """
        # Group by normalized URL
        url_groups: Dict[tuple[str, str, str, str, Optional[int], str, str], List[ContentItem]] = {}
        for item in items:
            key = _deduplication_url_key(str(item.url))
            url_groups.setdefault(key, []).append(item)

        merged = []
        for group in url_groups.values():
            group_copies = [item.model_copy(deep=True) for item in group]
            if len(group) == 1:
                merged.append(group_copies[0])
                continue

            # Pick the item with the richest content as primary
            primary = max(group_copies, key=lambda x: len(x.content or ""))

            # Merge metadata and source info from other items
            all_sources = []
            for item in group_copies:
                if item.source_type.value not in all_sources:
                    all_sources.append(item.source_type.value)
                # Merge metadata (engagement, discussion, etc.)
                for mk, mv in item.metadata.items():
                    if mk not in primary.metadata or not primary.metadata[mk]:
                        primary.metadata[mk] = mv

                # Append content (e.g., comments from another source)
                if item is not primary and item.content:
                    if primary.content and item.content not in primary.content:
                        primary.content = (primary.content or "") + f"\n\n--- From {item.source_type.value} ---\n" + item.content

            primary.metadata["merged_sources"] = all_sources
            merged.append(primary)

        return merged

    async def merge_topic_duplicates(
        self,
        items: List[ContentItem],
        *,
        log: bool = True,
    ) -> List[ContentItem]:
        """Merge items covering the same topic using AI semantic deduplication.

        This is a stable stage helper for integrations such as MCP.

        Sends all item titles, tags, and summaries to AI in a single call.
        Items must already be sorted by ai_score descending so that the first
        item in each duplicate group is always the highest-scored one.
        Content (comments) from duplicate items is merged into the primary.

        Falls back to returning items unchanged if the AI call fails.
        """
        if len(items) <= 1:
            return items

        from .ai.prompts import TOPIC_DEDUP_SYSTEM, TOPIC_DEDUP_USER
        from .ai.utils import parse_json_response

        # Build the item list for the prompt using stable IDs.
        lines = []
        for item in items:
            tags = ", ".join(item.ai_tags) if item.ai_tags else "—"
            summary = item.ai_summary or "—"
            lines.append(
                f"ID: {item.id}\n"
                f"Title: {item.title}\n"
                f"Tier: {item.metadata.get('source_tier', 5)}; "
                f"First party: {item.metadata.get('is_first_party', False)}\n"
                f"Tags: {tags}\nSummary: {summary}"
            )
        items_text = "\n\n".join(lines)

        try:
            ai_client = create_ai_client(self.config.ai)
            with usage_stage("semantic_dedup"):
                response = await ai_client.complete(
                    system=TOPIC_DEDUP_SYSTEM,
                    user=TOPIC_DEDUP_USER.format(items=items_text),
                    max_tokens=2048,
                )
            result = parse_json_response(response)
            if result is None:
                if log:
                    self.console.print("[yellow]  dedup: could not parse AI response, skipping[/yellow]")
                return items

            duplicate_groups = result.get("groups", [])
        except Exception as e:
            if is_fatal_ai_error(e):
                raise
            if log:
                self.console.print(
                    f"[yellow]  dedup: AI call failed ({redact_secrets(e)}), skipping[/yellow]"
                )
            return items

        if not duplicate_groups:
            return items

        by_id = {item.id: item for item in items}
        drop_ids: set[str] = set()
        for group in duplicate_groups:
            if not isinstance(group, dict):
                continue
            candidate_ids = [group.get("primary_id"), *(group.get("duplicate_ids") or [])]
            candidate_ids = [candidate_id for candidate_id in candidate_ids if candidate_id in by_id]
            if len(candidate_ids) < 2:
                continue
            primary_id = max(
                candidate_ids,
                key=lambda candidate_id: (
                    bool(by_id[candidate_id].metadata.get("is_first_party")),
                    -int(by_id[candidate_id].metadata.get("source_tier", 5)),
                    len(by_id[candidate_id].content or ""),
                    by_id[candidate_id].ai_score or 0,
                ),
            )
            primary = by_id[primary_id]
            supplemental = list(primary.metadata.get("supplemental_sources") or [])
            for duplicate_id in candidate_ids:
                if duplicate_id == primary_id:
                    continue
                dup = by_id[duplicate_id]
                if dup.content:
                    if not primary.content or dup.content not in primary.content:
                        label = dup.source_type.value
                        primary.content = (primary.content or "") + f"\n\n--- From {label} ---\n{dup.content}"
                supplemental.append(
                    {
                        "title": dup.title,
                        "url": str(dup.url),
                        "source_tier": dup.metadata.get("source_tier", 5),
                    }
                )
                if log:
                    self.console.print(
                        f"   [dim]dedup: keep {primary.id} {primary.title}[/dim]\n"
                        f"   [dim]       drop {dup.id} {dup.title}[/dim]"
                    )
                drop_ids.add(duplicate_id)
            primary.metadata["supplemental_sources"] = supplemental

        return [item for item in items if item.id not in drop_ids]

    async def filter_items(
        self,
        items: List[ContentItem],
        *,
        threshold: Optional[float] = None,
        topic_dedup: bool = True,
        apply_balance: bool = True,
        log: bool = True,
    ) -> FilteringPipelineResult:
        """Apply score thresholding, optional topic dedup, and digest balancing."""
        effective_threshold = (
            threshold
            if threshold is not None
            else self.config.filtering.ai_score_threshold
        )
        threshold_items = [
            item
            for item in items
            if item.ai_score is not None and item.ai_score >= effective_threshold
        ]
        threshold_items.sort(key=lambda item: item.ai_score or 0, reverse=True)

        if log:
            self.console.print(
                f"⭐️ {len(threshold_items)} items scored ≥ {effective_threshold}\n"
            )

        deduped_items = threshold_items
        if topic_dedup and deduped_items:
            deduped_items = await self.merge_topic_duplicates(deduped_items, log=log)
        topic_dedup_removed = len(threshold_items) - len(deduped_items)

        if log and topic_dedup_removed:
            self.console.print(
                f"🧹 Removed {topic_dedup_removed} topic duplicates "
                f"→ {len(deduped_items)} unique items\n"
            )

        balanced_digest = (
            self.apply_balanced_digest(deduped_items, log=log)
            if apply_balance
            else BalancedDigestResult(items=deduped_items)
        )
        return FilteringPipelineResult(
            items=balanced_digest.items,
            threshold_count=len(threshold_items),
            topic_dedup_count=len(deduped_items),
            topic_dedup_removed=topic_dedup_removed,
            balanced_digest=balanced_digest,
        )

    def apply_balanced_digest(
        self,
        items: List[ContentItem],
        *,
        log: bool = True,
    ) -> BalancedDigestResult:
        """Apply configured category quotas and the final item cap.

        Categories are read from ``item.metadata["category"]``. If a category
        appears in more than one configured group, the first group in config
        order wins.
        """
        filtering = self.config.filtering
        groups = filtering.category_groups
        balance = getattr(self.config, "balance", None)
        if balance is not None and not getattr(balance, "enabled", True):
            balance = None
        max_items = filtering.max_items
        if max_items is None and balance is not None:
            max_items = filtering.final_max_items

        if not groups and max_items is None and balance is None:
            return BalancedDigestResult(items=items)

        sorted_items = sorted(
            items,
            key=lambda item: item.ai_score or 0,
            reverse=True,
        )

        category_to_group: Dict[str, str] = {}
        duplicate_categories: List[str] = []
        for group_key, group in groups.items():
            for category in group.categories:
                if category in category_to_group:
                    if category_to_group[category] != group_key:
                        duplicate_categories.append(category)
                    continue
                category_to_group[category] = group_key

        if log:
            for category in sorted(set(duplicate_categories)):
                first_group = category_to_group[category]
                self.console.print(
                    f"[yellow]Warning: category '{category}' is configured in multiple "
                    f"groups; using '{first_group}'.[/yellow]"
                )

        selected: List[tuple[ContentItem, str]] = []
        group_counts: Dict[str, int] = defaultdict(int)
        default_group = filtering.default_group

        for item in sorted_items:
            category = item.metadata.get("category")
            group_key = (
                category_to_group.get(category, default_group)
                if isinstance(category, str)
                else default_group
            )

            if group_key in groups:
                limit = groups[group_key].limit
            else:
                limit = filtering.default_group_limit

            if limit is not None and group_counts[group_key] >= limit:
                continue

            selected.append((item, group_key))
            group_counts[group_key] += 1

        if max_items is not None:
            if balance is not None:
                selected = self._select_soft_balanced(selected, max_items, balance)
            else:
                selected = selected[:max_items]

        final_counts: Dict[str, int] = defaultdict(int)
        for _, group_key in selected:
            final_counts[group_key] += 1

        group_limits: Dict[str, Optional[int]] = {
            group_key: group.limit for group_key, group in groups.items()
        }
        group_limits.setdefault(default_group, filtering.default_group_limit)

        if log:
            self.console.print(
                f"⚖️ Balanced digest selected {len(selected)}/{len(items)} items"
            )
            for group_key, group in groups.items():
                label = group.name or group_key
                self.console.print(
                    f"      • {label}: {final_counts.get(group_key, 0)}/{group.limit}"
                )
            if (
                final_counts.get(default_group, 0)
                or filtering.default_group_limit is not None
            ):
                limit_label = (
                    str(filtering.default_group_limit)
                    if filtering.default_group_limit is not None
                    else "unlimited"
                )
                self.console.print(
                    f"      • {default_group}: "
                    f"{final_counts.get(default_group, 0)}/{limit_label}"
                )
            self.console.print("")

        return BalancedDigestResult(
            items=[item for item, _ in selected],
            enabled=True,
            group_counts=dict(final_counts),
            group_limits=group_limits,
            duplicate_categories=sorted(set(duplicate_categories)),
        )

    @staticmethod
    def _prioritize_product_intelligence(
        items: List[ContentItem],
    ) -> List[ContentItem]:
        """Put product cases first, followed by builders and productizable capabilities."""
        sorted_items = sorted(items, key=lambda item: item.ai_score or 0, reverse=True)
        type_priority = {
            "product_case": 0,
            "builder_insight": 1,
            "model_capability": 2,
            "market_signal": 3,
            "business_policy": 4,
            "early_signal": 5,
        }
        product_cases = [
            item
            for item in sorted_items
            if item.metadata.get("intelligence_type") == "product_case"
        ][:3]
        top_ids = {item.id for item in product_cases}
        fillers = [item for item in sorted_items if item.id not in top_ids]
        fillers.sort(
            key=lambda item: (
                type_priority.get(
                    str(item.metadata.get("intelligence_type")), 99
                ),
                -(item.ai_score or 0),
            )
        )
        top_items = [*product_cases, *fillers[: max(0, 3 - len(product_cases))]]
        top_ids = {item.id for item in top_items}
        remainder = [item for item in sorted_items if item.id not in top_ids]
        remainder.sort(
            key=lambda item: (
                type_priority.get(
                    str(item.metadata.get("intelligence_type")), 99
                ),
                -(item.ai_score or 0),
            )
        )
        return [*top_items, *remainder]

    @staticmethod
    def _select_soft_balanced(selected, max_items: int, balance):
        """Prefer the requested mix without adding anything below the score threshold."""
        remaining = list(selected)
        if len(remaining) <= max_items:
            return remaining

        target = {
            "tech": round(max_items * balance.tech_target_ratio),
            "product": round(max_items * balance.product_target_ratio),
            "china": round(max_items * balance.china_target_ratio),
            "global": round(max_items * balance.global_target_ratio),
        }
        available_github = sum(
            item.source_type.value in {"github", "ossinsight"}
            for item, _ in remaining
        )
        github_target = min(2, available_github, max_items)
        counts: Dict[str, int] = defaultdict(int)
        result = []

        while remaining and len(result) < max_items:
            def priority(entry):
                item, _ = entry
                category = item.metadata.get("category")
                region = item.metadata.get("region")
                deficit_matches = int(
                    category in {"tech", "product"}
                    and counts[category] < target[category]
                )
                deficit_matches += int(
                    region in {"china", "global"}
                    and counts[region] < target[region]
                )
                if (
                    item.source_type.value in {"github", "ossinsight"}
                    and counts["github"] < github_target
                ):
                    deficit_matches += 1
                return deficit_matches, item.ai_score or 0

            best = max(remaining, key=priority)
            remaining.remove(best)
            item, _ = best
            category = item.metadata.get("category")
            region = item.metadata.get("region")
            if category in {"tech", "product"}:
                counts[category] += 1
            if region in {"china", "global"}:
                counts[region] += 1
            if item.source_type.value in {"github", "ossinsight"}:
                counts["github"] += 1
            result.append(best)
        return result

    async def _expand_twitter_discussion(self, items: List[ContentItem]) -> None:
        """Second-stage: fetch reply text for important Twitter items and re-analyze.

        Only runs when sources.twitter.fetch_reply_text is True.
        Bounded by max_tweets_to_expand to control cost.
        """
        tw_cfg = self.config.sources.twitter
        if not tw_cfg or not tw_cfg.enabled or not tw_cfg.fetch_reply_text:
            return

        from .models import SourceType

        twitter_items = [
            item for item in items
            if item.source_type == SourceType.TWITTER
        ][:tw_cfg.max_tweets_to_expand]

        if not twitter_items:
            return

        self.console.print(
            f"💬 Fetching reply text for {len(twitter_items)} Twitter items..."
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            if tw_cfg.mode == "playwright":
                self.console.print(
                    "   [yellow]Reply expansion not yet supported in Playwright mode.[/yellow]"
                )
                return
            scraper = TwitterScraper(tw_cfg, client)
            expanded = []
            for item in twitter_items:
                try:
                    reply_lines = await scraper.fetch_replies_for_item(item)
                    if TwitterScraper.append_discussion_content(item, reply_lines):
                        expanded.append(item)
                        self.console.print(
                            f"   💬 {len(reply_lines)} replies added to: {item.title[:60]}"
                        )
                except Exception as exc:
                    self.console.print(
                        f"   [yellow]⚠️  Reply fetch failed for {item.id}: {exc}[/yellow]"
                    )

        if not expanded:
            return

        self.console.print(
            f"   Re-analyzing {len(expanded)} Twitter items with reply context...\n"
        )
        ai_client = create_ai_client(self.config.ai)
        analyzer = ContentAnalyzer(ai_client)
        await analyzer.analyze_batch(expanded)

    async def _enrich_important_items(self, items: List[ContentItem]) -> List[str]:
        """Enrich items with background knowledge (2nd AI pass).

        For each item that passed the score threshold, call AI to generate
        background knowledge based on the item's actual content.

        Args:
            items: Important items to enrich (modified in-place)
        """
        if not items:
            return []

        deep_limit = self.config.filtering.deep_analysis_limit
        deep_items = items[:deep_limit]
        self.console.print(f"📚 Deep-analyzing Top {len(deep_items)} items...")
        ai_client = create_ai_client(self.config.ai)
        enricher = ContentEnricher(ai_client)
        await enricher.enrich_batch(deep_items)
        self.console.print(f"   Deep-analyzed {len(deep_items)} items\n")
        return await enricher.generate_trend_overview(items)

    async def _analyze_content(self, items: List[ContentItem]) -> List[ContentItem]:
        """Analyze content items with AI.

        Args:
            items: Items to analyze

        Returns:
            List[ContentItem]: Analyzed items
        """
        self.console.print("🤖 Analyzing content with AI...")

        ai_client = create_ai_client(self.config.ai)
        analyzer = ContentAnalyzer(ai_client)

        return await analyzer.analyze_batch(items)

    async def _generate_summary(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
    ) -> str:
        """Generate daily summary.

        Args:
            items: Important items to include (already enriched with background/related)
            date: Date string
            total_fetched: Total items fetched
            language: Output language ("en" or "zh")

        Returns:
            str: Markdown summary
        """
        self.console.print("📝 Generating daily summary...")

        summarizer = DailySummarizer()

        return await summarizer.generate_summary(items, date, total_fetched, language=language)
