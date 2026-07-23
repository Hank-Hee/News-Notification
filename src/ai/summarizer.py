"""Daily summary generation — pure programmatic rendering."""

import html
import re
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import quote, urlsplit
from zoneinfo import ZoneInfo

from ..models import ContentItem


_CJK = r"[\u4e00-\u9fff\u3400-\u4dbf]"
_ASCII = r"[A-Za-z0-9]"
_MARKDOWN_SPECIAL = re.compile(r"([\\`*_{}\[\]()<>#!|])")
_MARKDOWN_BLOCK_START = re.compile(r"(?m)^( {0,3})(>|[-+] |\d+[.)] )")
_URL_SAFE_CHARS = ":/?#[]@!$&'*,;=~%+"


def _escape_markdown(value: object) -> str:
    """Render untrusted text literally while retaining its readable content."""
    escaped = html.escape(str(value), quote=True)
    escaped = _MARKDOWN_SPECIAL.sub(r"\\\1", escaped)
    return _MARKDOWN_BLOCK_START.sub(r"\1\\\2", escaped)


def _safe_url(value: object) -> Optional[str]:
    """Return an HTML/Markdown-safe HTTP(S) URL, or None for unsafe URLs."""
    raw = str(value).strip()
    if not raw or any(ord(char) < 32 or ord(char) == 127 for char in raw):
        return None
    try:
        parsed = urlsplit(raw)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
            return None
        parsed.port
    except (TypeError, ValueError):
        return None
    encoded = quote(raw, safe=_URL_SAFE_CHARS)
    return html.escape(encoded, quote=True)


def _pangu(text: str) -> str:
    """Insert a space between CJK and ASCII letters/digits (Pangu spacing)."""
    text = re.sub(rf"({_CJK})({_ASCII})", r"\1 \2", text)
    text = re.sub(rf"({_ASCII})({_CJK})", r"\1 \2", text)
    return text


LABELS = {
    "en": {
        "header": "Horizon Daily",
        "source": "Source",
        "background": "Background",
        "discussion": "Discussion",
        "references": "References",
        "tags": "Tags",
        "selected_items": "From {total} items, {selected} important content pieces were selected",
        "empty_analyzed": "Analyzed {total} items, but none met the importance threshold.",
        "empty_body": (
            "No significant developments today. This might indicate:\n"
            "- A quiet day in your tracked sources\n"
            "- The AI score threshold is too high\n"
            "- Your information sources need expansion\n\n"
            "Consider:\n"
            "1. Lowering the `ai_score_threshold` in config.json\n"
            "2. Adding more diverse information sources\n"
            "3. Checking if the AI model is working correctly\n"
        ),
    },
    "zh": {
        "header": "Horizon 每日速递",
        "source": "来源",
        "background": "背景",
        "discussion": "社区讨论",
        "references": "参考链接",
        "tags": "标签",
        "selected_items": "从 {total} 条内容中筛选出 {selected} 条重要资讯。",
        "empty_analyzed": "已分析 {total} 条内容，但没有达到重要性阈值的条目。",
        "empty_body": (
            "今日暂无重要动态，可能原因：\n"
            "- 今天关注的信息源较平静\n"
            "- AI 评分阈值设置过高\n"
            "- 信息源种类有待扩充\n\n"
            "建议：\n"
            "1. 在 config.json 中降低 `ai_score_threshold`\n"
            "2. 添加更多多样化的信息源\n"
            "3. 检查 AI 模型是否正常工作\n"
        ),
    },
}


class DailySummarizer:
    """Generates daily Markdown summaries from pre-analyzed content items."""

    def __init__(self):
        pass

    async def generate_summary(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
        trend_overview: Optional[List[str]] = None,
    ) -> str:
        """Generate daily summary in Markdown format.

        Items are rendered in score-descending order (already sorted by orchestrator).

        Args:
            items: High-scoring content items (already enriched)
            date: Date string (YYYY-MM-DD)
            total_fetched: Total number of items fetched before filtering
            language: Output language, either "en" or "zh"

        Returns:
            str: Markdown formatted summary
        """
        labels = LABELS.get(language, LABELS["en"])

        if not items:
            return self._generate_empty_summary(date, total_fetched, labels)

        if language == "zh":
            return self._generate_chinese_daily(
                items,
                date,
                total_fetched,
                trend_overview or [],
                labels,
            )

        header = (
            f"# {labels['header']} - {date}\n\n"
            f"> {labels['selected_items'].format(total=total_fetched, selected=len(items))}\n\n"
            "---\n\n"
        )

        # TOC
        toc_entries = []
        for i, item in enumerate(items):
            _t = item.metadata.get(f"title_{language}") or item.title
            t = _escape_markdown(_t)
            if language == "zh":
                t = _pangu(t)
            score = item.ai_score or "?"
            toc_entries.append(f"{i + 1}. [{t}](#item-{i + 1}) \u2b50\ufe0f {score}/10")
        toc = "\n".join(toc_entries) + "\n\n---\n\n"

        parts = [self._format_item(item, labels, language, i + 1) for i, item in enumerate(items)]

        return header + toc + "".join(parts)

    def _generate_chinese_daily(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        trend_overview: List[str],
        labels: dict,
    ) -> str:
        """Render the research-brief layout used by GitHub Pages."""
        updated = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M 北京时间")
        scarcity = (
            "\n> 今日高质量增量有限，因此未使用低质量内容补足数量。\n"
            if len(items) < 10
            else ""
        )
        lines = [
            "# Horizon AI Daily",
            "",
            f"**日期**：{_escape_markdown(date)}　 **更新时间**：{updated}",
            "",
            f"> {labels['selected_items'].format(total=total_fetched, selected=len(items))}",
            scarcity.rstrip(),
            "",
            '<nav class="daily-toc">',
            '<a href="#trend-overview">今日趋势概览</a> · '
            '<a href="#top-five">今日必读 Top 5</a> · '
            '<a href="#tech-frontier">模型与技术前沿</a> · '
            '<a href="#product-business">AI 产品与商业动态</a> · '
            '<a href="#github-trends">GitHub 开源趋势</a> · '
            '<a href="#watch-next">继续关注</a> · '
            '<a href="#methodology">数据与筛选说明</a> · '
            '<a href="#archives">历史日报</a>',
            "</nav>",
            "",
            '<a id="trend-overview"></a>',
            "## 今日趋势概览",
            "",
        ]
        trends = trend_overview or [
            f"今日从 {total_fetched} 条候选中保留 {len(items)} 条高价值 AI 增量。"
        ]
        lines.extend(f"- {_pangu(_escape_markdown(trend))}" for trend in trends[:5])

        lines.extend(["", '<a id="top-five"></a>', "## 今日必读 Top 5", ""])
        for index, item in enumerate(items[:5], start=1):
            lines.append(self._format_item(item, labels, "zh", index).rstrip())

        remainder = items[5:]
        github_items = [
            item
            for item in items
            if item.source_type.value in {"github", "ossinsight"}
            or str(item.metadata.get("category", "")).startswith("github")
        ]
        tech_items = [
            item
            for item in remainder
            if item.metadata.get("category") == "tech" and item not in github_items
        ]
        product_items = [
            item
            for item in remainder
            if item.metadata.get("category") == "product" and item not in github_items
        ]

        lines.extend(["", '<a id="tech-frontier"></a>', "## 模型与技术前沿", ""])
        lines.extend(self._compact_item(item) for item in tech_items)
        if not tech_items:
            lines.append("_今日没有额外达到阈值的技术条目。_")

        lines.extend(["", '<a id="product-business"></a>', "## AI 产品与商业动态", ""])
        lines.extend(self._compact_item(item) for item in product_items)
        if not product_items:
            lines.append("_今日没有额外达到阈值的产品与商业条目。_")

        lines.extend(["", '<a id="github-trends"></a>', "## GitHub 开源趋势", ""])
        lines.extend(self._github_item(item) for item in github_items[:3])
        if not github_items:
            lines.append("_今日没有达到入选标准的 GitHub 项目。_")

        follow_up = [item for item in items if str(item.metadata.get("follow_up", "")).strip()]
        lines.extend(["", '<a id="watch-next"></a>', "## 继续关注", ""])
        for item in follow_up[:5]:
            title = _pangu(_escape_markdown(item.metadata.get("title_zh") or item.title))
            note = _pangu(_escape_markdown(item.metadata.get("follow_up", "")))
            lines.append(f"- **{title}**：{note}")
        if not follow_up:
            lines.append("_暂无需要单独列出的后续观察点。_")

        lines.extend(
            [
                "",
                '<a id="methodology"></a>',
                "## 数据与筛选说明",
                "",
                "- 仅处理最近 24 小时的稳定公开来源；先程序预筛选，再由 Kimi 评分。",
                "- 默认阈值为 7.5；质量优先于数量和比例，高质量不足时允许少于 10 条。",
                "- 技术/产品、中国/海外均采用软配额；同一事件执行语义去重和最近 7 天历史去重。",
                "- Top 5 使用背景搜索与深度分析，其余条目保留简要摘要。",
                "",
                '<a id="archives"></a>',
                "## 历史日报",
                "",
                "[返回首页查看按日期归档]({{ '/' | relative_url }})",
            ]
        )
        return "\n".join(line for line in lines if line is not None).strip() + "\n"

    def _compact_item(self, item: ContentItem) -> str:
        title = _pangu(_escape_markdown(item.metadata.get("title_zh") or item.title))
        url = _safe_url(item.url)
        link = f"[{title}]({url}){{:target=\"_blank\" rel=\"noopener noreferrer\"}}" if url else title
        summary = _pangu(_escape_markdown(item.ai_summary or "目前公开信息不足"))
        reason = _pangu(_escape_markdown(item.ai_reason or ""))
        meta = item.metadata
        tier = meta.get("source_tier", "?")
        region = "中国" if meta.get("region") == "china" else "海外"
        category = "技术" if meta.get("category") == "tech" else "产品/商业"
        tags = "、".join(_escape_markdown(tag) for tag in item.ai_tags)
        return (
            f"### {link} ⭐️ {item.ai_score or '?'}/10\n\n"
            f"{summary}\n\n"
            f"**重要性**：{reason or '见评分与来源信息。'}  \n"
            f"**元数据**：Tier {tier} · {category} · {region} · {_escape_markdown(item.published_at.isoformat())}"
            + (f" · {tags}" if tags else "")
            + "\n"
        )

    def _github_item(self, item: ContentItem) -> str:
        base = self._compact_item(item)
        project = item.metadata.get("github_project")
        if not isinstance(project, dict):
            growth = item.metadata.get("stars_gained", "未知")
            repo = item.metadata.get("repo", "未知")
            return base + f"\n**项目指标**：仓库 { _escape_markdown(repo) } · 近期 Star 增长 { _escape_markdown(growth) }\n"
        fields = [
            ("项目阶段", project.get("project_stage", "未知")),
            ("用途", project.get("what_it_does", "未知")),
            ("价值", project.get("why_it_matters", "未知")),
            ("风险", project.get("risk_or_caveat", "未知")),
            ("建议", project.get("recommendation", "未知")),
        ]
        return base + "\n" + "  \n".join(
            f"**{label}**：{_pangu(_escape_markdown(value))}" for label, value in fields
        ) + "\n"

    def generate_webhook_overview(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
    ) -> str:
        """Generate a compact overview for multi-message webhook delivery."""
        labels = LABELS.get(language, LABELS["en"])
        if not items:
            return self._generate_empty_summary(date, total_fetched, labels)

        if language == "zh":
            header = (
                f"# {labels['header']} - {date}\n\n"
                f"> 从 {total_fetched} 条内容中筛选出 {len(items)} 条重要资讯。\n\n"
                "下面会按新闻逐条发送详情，你可以只看感兴趣的标题。\n\n"
            )
        else:
            header = (
                f"# {labels['header']} - {date}\n\n"
                f"> Selected {len(items)} important items from {total_fetched} fetched items.\n\n"
                "Details will be sent item by item so you can read only the topics you care about.\n\n"
            )

        entries = []
        for i, item in enumerate(items, start=1):
            title = _escape_markdown(item.metadata.get(f"title_{language}") or item.title)
            if language == "zh":
                title = _pangu(title)
            score = item.ai_score or "?"
            url = _safe_url(item.url)
            title_link = f"[{title}]({url})" if url else title
            entries.append(f"{i}. {title_link} \u2b50\ufe0f {score}/10")

        return header + "\n".join(entries)

    def generate_webhook_item(
        self,
        item: ContentItem,
        language: str,
        index: int,
        total: int,
    ) -> str:
        """Generate one item message for multi-message webhook delivery."""
        labels = LABELS.get(language, LABELS["en"])
        prefix = f"第 {index}/{total} 条\n\n" if language == "zh" else f"Item {index}/{total}\n\n"
        return prefix + self._format_item(item, labels, language, index).rstrip("-\n ")

    def _format_item(self, item: ContentItem, labels: dict, language: str, index: int) -> str:
        """Format a single ContentItem into Markdown."""
        _title = item.metadata.get(f"title_{language}") or item.title
        title = _escape_markdown(_title)
        raw_url = str(item.url)
        url = _safe_url(raw_url)
        score = item.ai_score or "?"
        meta = item.metadata

        summary = (
            meta.get("what_happened")
            or meta.get(f"detailed_summary_{language}")
            or meta.get("detailed_summary")
            or item.ai_summary
            or ""
        )
        background = meta.get(f"background_{language}") or meta.get("background") or ""
        discussion = (
            meta.get("community_view")
            or meta.get(f"community_discussion_{language}")
            or meta.get("community_discussion")
            or ""
        )

        summary = _escape_markdown(summary)
        background = _escape_markdown(background)
        discussion = _escape_markdown(discussion)

        if language == "zh":
            title = _pangu(title)
            summary = _pangu(summary)
            background = _pangu(background)
            discussion = _pangu(discussion)

        # Source line with parts joined by " · ", link appended at end
        source_type = item.source_type.value
        source_parts = [_escape_markdown(source_type)]
        if meta.get("subreddit"):
            source_parts.append(_escape_markdown(f"r/{meta['subreddit']}"))
        if meta.get("feed_name"):
            source_parts.append(_escape_markdown(meta["feed_name"]))
        else:
            source_parts.append(_escape_markdown(item.author or "unknown"))
        if item.published_at:
            if language == "zh":
                source_parts.append(
                    f"{item.published_at.month}月{item.published_at.day}日 "
                    f"{item.published_at:%H:%M}"
                )
            else:
                day = item.published_at.strftime("%d").lstrip("0")
                source_parts.append(item.published_at.strftime(f"%b {day}, %H:%M"))
        source_line = " \u00b7 ".join(source_parts)  # ·

        discussion_url = meta.get("discussion_url")
        if discussion_url:
            safe_discussion_url = _safe_url(discussion_url)
            if safe_discussion_url and str(discussion_url) != raw_url:
                source_line += f' · [{labels["discussion"]}]({safe_discussion_url})'

        title_link = f"[{title}]({url})" if url else title
        if language == "zh" and url:
            title_link += '{:target="_blank" rel="noopener noreferrer"}'

        lines = [
            f'<a id="item-{index}"></a>',
            f"## {title_link} \u2b50\ufe0f {score}/10",  # ⭐️
            "",
            summary,
            "",
            source_line,
        ]

        if language == "zh":
            category = "技术" if meta.get("category") == "tech" else "产品/商业"
            region = "中国" if meta.get("region") == "china" else "海外"
            tier = meta.get("source_tier", "?")
            lines.extend(
                [
                    "",
                    f"**来源等级**：Tier {tier} · **分类**：{category} · **地区**：{region}",
                ]
            )
            if meta.get("deep_analysis"):
                for label, key in (
                    ("为什么重要", "why_it_matters"),
                    ("关键细节", "key_details"),
                    ("行业与产品影响", "industry_or_product_impact"),
                    ("限制与不确定性", "limitations_or_uncertainties"),
                    ("后续观察", "what_to_watch_next"),
                ):
                    value = meta.get(key)
                    if value:
                        lines.extend(["", f"**{label}**：{_pangu(_escape_markdown(value))}"])

        if background:
            lines.append("")
            lines.append(f"**{labels['background']}**: {background}")

        sources = [
            *(meta.get("sources") or []),
            *(meta.get("supplemental_sources") or []),
        ]
        if sources:
            reference_items = []
            for source in sources:
                reference_title = html.escape(str(source.get("title", "")), quote=True)
                reference_url = _safe_url(source.get("url", ""))
                if reference_url:
                    reference_items.append(
                        f'<li><a href="{reference_url}" target="_blank" '
                        f'rel="noopener noreferrer">{reference_title}</a></li>\n'
                    )
                else:
                    reference_items.append(f"<li>{reference_title}</li>\n")
            items_html = "".join(reference_items)
            lines += [
                "",
                f'<details><summary>{labels["references"]}</summary>\n<ul>\n{items_html}\n</ul>\n</details>',
            ]

        if discussion:
            lines.append("")
            lines.append(f"**{labels['discussion']}**: {discussion}")

        if item.ai_tags:
            tags_str = ", ".join([f"`#{_escape_markdown(t)}`" for t in item.ai_tags])
            lines.append("")
            lines.append(f"**{labels['tags']}**: {tags_str}")

        lines.append("")
        lines.append("---")

        return "\n".join(lines) + "\n\n"

    def _generate_empty_summary(self, date: str, total_fetched: int, labels: dict) -> str:
        """Generate summary when no high-scoring items were found."""
        return (
            f"# {labels['header']} - {date}\n\n"
            f"> {labels['empty_analyzed'].format(total=total_fetched)}\n\n"
            + labels["empty_body"]
        )
