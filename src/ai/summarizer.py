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
    escaped = html.escape(html.unescape(str(value)), quote=True)
    escaped = _MARKDOWN_SPECIAL.sub(r"\\\1", escaped)
    # html.escape represents apostrophes as ``&#x27;``. Markdown escaping must
    # not insert a backslash into that numeric entity (``&\#x27;``), otherwise
    # Jekyll renders the entity literally instead of showing an apostrophe.
    escaped = re.sub(r"&\\#([xX]?[0-9A-Fa-f]+);", r"&#\1;", escaped)
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
            "本次运行没有产出日报条目，这不等于今天没有 AI 新闻。\n\n"
            "请按运行日志依次确认：\n"
            "1. `Fetched` 是否大于 0：为 0 说明来源抓取失败或时间窗口内无内容\n"
            "2. `Prefilter statistics` 的 `kept` 是否大于 0：为 0 说明规则预筛过严\n"
            "3. `Analyzed` 和 Kimi 请求数是否大于 0：为 0 说明模型未实际调用\n"
            "4. `items scored` 是否大于 0：为 0 才考虑调整评分提示词或阈值\n\n"
            "工作流会在 Kimi 配置或全部来源异常时直接失败，不会把故障静默写成“今日平静”。\n"
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
        """Render the personalized AI product-intelligence layout."""
        updated = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M 北京时间")
        scarcity = (
            "\n> 今日高质量增量有限，因此未使用低质量内容补足数量。\n"
            if len(items) < 8
            else ""
        )
        lines = [
            "# AI产品情报",
            "",
            f"**日期**：{_escape_markdown(date)}　 **更新时间**：{updated}",
            "",
            f"> {labels['selected_items'].format(total=total_fetched, selected=len(items))}",
            scarcity.rstrip(),
            "",
            '<nav class="daily-toc">',
            '<a href="#daily-focus">今日重点</a> · '
            '<a href="#product-teardown">产品拆解</a> · '
            '<a href="#how-they-build">他们怎么做</a> · '
            '<a href="#model-company-news">模型公司动态</a> · '
            '<a href="#learn-today">今天学什么</a> · '
            '<a href="{{ \'/products/\' | relative_url }}">产品情报库</a> · '
            '<a href="#archives">历史日报</a>',
            "</nav>",
            "",
            '<a id="daily-focus"></a>',
            "## 今日重点",
            "",
        ]
        trends = trend_overview or [
            f"今天从 {total_fetched} 条公开信息中保留 {len(items)} 条可用于产品判断的增量。"
        ]
        lines.extend(f"- {_pangu(_escape_markdown(trend))}" for trend in trends[:5])
        lines.append("")

        top_items = items[:2]
        remainder = items[2:]
        lines.extend(
            [
                '<a id="product-teardown"></a>',
                "## 产品拆解",
                "",
            ]
        )
        for index, item in enumerate(top_items, start=1):
            lines.append(self._product_teardown(item, index).rstrip())

        builder_items = [
            item
            for item in remainder
            if item.metadata.get("intelligence_type") == "builder_insight"
        ]
        model_items = [
            item
            for item in remainder
            if item.metadata.get("intelligence_type") == "model_capability"
        ]
        used_ids = {item.id for item in [*builder_items, *model_items]}
        market_items = [item for item in remainder if item.id not in used_ids]

        lines.extend(
            [
                "",
                '<a id="how-they-build"></a>',
                "## 他们怎么做",
                "",
            ]
        )
        lines.extend(self._intelligence_item(item) for item in builder_items)
        if not builder_items:
            lines.append("_今天没有达到标准的一线构建实践；不会用泛泛观点补位。_")

        lines.extend(
            [
                "",
                '<a id="model-company-news"></a>',
                "## 模型公司动态",
                "",
            ]
        )
        lines.extend(self._intelligence_item(item) for item in model_items)
        if not model_items:
            lines.append("_今天没有值得单独展开的模型公司一手动态。_")

        if market_items:
            lines.extend(["", "### 其他值得留意", ""])
            lines.extend(self._intelligence_item(item) for item in market_items)

        lines.extend(
            [
                "",
                '<a id="learn-today"></a>',
                "## 今天学什么",
                "",
            ]
        )
        learning_points: list[str] = []
        exercises: list[str] = []
        for item in top_items:
            learning_points.extend(self._metadata_list(item, "learning_points"))
            exercise = str(item.metadata.get("hands_on_exercise") or "").strip()
            if exercise and exercise != "未公开":
                exercises.append(exercise)
        learning_points = list(dict.fromkeys(learning_points))[:4]
        exercises = list(dict.fromkeys(exercises))[:2]
        if learning_points:
            lines.extend(
                f"- **知识点**：{_pangu(_escape_markdown(point))}"
                for point in learning_points
            )
        if exercises:
            lines.extend(
                f"- **动手练习**：{_pangu(_escape_markdown(exercise))}"
                for exercise in exercises
            )
        if not learning_points and not exercises:
            lines.append("_今天没有足够信息生成可靠的学习任务。_")

        lines.extend(
            [
                "",
                "## 数据与筛选说明",
                "",
                "- 每天 08:30（北京时间）处理最近 24 小时的公开来源；先程序预筛和历史去重，再由 DeepSeek 批量评分。",
                "- 优先级依次为：真实 AI 产品、构建实践、模型公司核心人员、新能力、精选 Newsletter。",
                "- 纯算力、GPU、底层推理优化和学术论文默认降权，除非能直接解释新的产品机会。",
                "- Top 2 由 Kimi 做初学者版产品拆解；失败时只对该条使用 DeepSeek Pro，所有模型均关闭思考。",
                "- 同一事件执行语义去重和最近 7 天历史去重；结果缓存并同步到 JSON、CSV 和可筛选数据库页面。",
                "",
                "[打开产品情报数据库]({{ '/products/' | relative_url }}) · "
                "[下载 JSON]({{ '/data/product-intelligence.json' | relative_url }}) · "
                "[下载 CSV]({{ '/data/product-intelligence.csv' | relative_url }})",
                "",
                '<a id="archives"></a>',
                "## 历史日报",
                "",
                "[返回首页查看按日期归档]({{ '/' | relative_url }})",
            ]
        )
        return "\n".join(line for line in lines if line is not None).strip() + "\n"

    @staticmethod
    def _metadata_list(item: ContentItem, key: str) -> list[str]:
        value = item.metadata.get(key)
        if not isinstance(value, list):
            return []
        return [str(entry).strip() for entry in value if str(entry).strip()]

    def _product_teardown(self, item: ContentItem, index: int) -> str:
        meta = item.metadata
        title = _pangu(_escape_markdown(meta.get("title_zh") or item.title))
        url = _safe_url(item.url)
        title_link = (
            f'[{title}]({url}){{:target="_blank" rel="noopener noreferrer"}}'
            if url
            else title
        )
        evidence_labels = {
            "first_party": "一手信息",
            "verified": "已核验",
            "reported": "媒体报道",
            "early_signal": "早期信号",
        }
        lines = [
            f"### {index}. {title_link}",
            "",
            f"**一句话看懂**：{_pangu(_escape_markdown(item.ai_summary or '未公开'))}",
            "",
            f"**评分**：{item.ai_score or '?'} / 10　 "
            f"**证据**：{evidence_labels.get(str(meta.get('evidence_status')), '未公开')}",
            "",
            f"**产品 / 团队**：{_pangu(_escape_markdown(meta.get('product_name') or '未公开'))} / "
            f"{_pangu(_escape_markdown(meta.get('builder_name') or item.author or '未公开'))}",
            "",
            f"**目标用户**：{_pangu(_escape_markdown(meta.get('target_user') or '未公开'))}",
            "",
            f"**它是什么**：{_pangu(_escape_markdown(meta.get('what_it_is') or item.ai_summary or '未公开'))}",
            "",
            f"**用户问题**：{_pangu(_escape_markdown(meta.get('user_problem') or '未公开'))}",
        ]
        self._append_steps(lines, "使用流程", self._metadata_list(item, "usage_flow"))
        lines.extend(
            [
                "",
                f"**AI 在做什么**：{_pangu(_escape_markdown(meta.get('ai_role') or '未公开'))}",
                "",
                f"**怎么实现**：{_pangu(_escape_markdown(meta.get('implementation_idea') or '未公开'))}",
            ]
        )
        self._append_steps(lines, "需要理解的知识点", self._metadata_list(item, "learning_points"))
        lines.extend(
            [
                "",
                f"**动手练习**：{_pangu(_escape_markdown(meta.get('hands_on_exercise') or '未公开'))}",
                "",
                f"**已知限制**：{_pangu(_escape_markdown(meta.get('limitations_or_uncertainties') or '未公开'))}",
            ]
        )
        lines.extend(["", self._source_links(item), "", "---", ""])
        return "\n".join(lines)

    @staticmethod
    def _append_steps(lines: list[str], label: str, values: list[str]) -> None:
        lines.extend(["", f"**{label}**："])
        if not values:
            lines.append("- 未公开")
            return
        lines.extend(
            f"{index}. {_pangu(_escape_markdown(value))}"
            for index, value in enumerate(values, start=1)
        )

    def _intelligence_item(self, item: ContentItem) -> str:
        meta = item.metadata
        title = _pangu(_escape_markdown(meta.get("title_zh") or item.title))
        url = _safe_url(item.url)
        link = (
            f'[{title}]({url}){{:target="_blank" rel="noopener noreferrer"}}'
            if url
            else title
        )
        insight = (
            meta.get("builder_insight")
            or meta.get("product_signal")
            or meta.get("market_signal")
            or item.ai_reason
            or "未公开"
        )
        follow_up = meta.get("follow_up")
        result = [
            f"### {link} ⭐️ {item.ai_score or '?'}/10",
            "",
            _pangu(_escape_markdown(item.ai_summary or "未公开")),
            "",
            f"**对做产品的启发**：{_pangu(_escape_markdown(insight))}",
        ]
        if follow_up:
            result.extend(["", f"**继续验证**：{_pangu(_escape_markdown(follow_up))}"])
        result.extend(["", self._source_links(item), ""])
        return "\n".join(result)

    @staticmethod
    def _source_links(item: ContentItem) -> str:
        safe_url = _safe_url(item.url)
        author = _pangu(_escape_markdown(item.author or item.source_type.value))
        published = item.published_at.astimezone(ZoneInfo("Asia/Shanghai"))
        source = f"{_escape_markdown(item.source_type.value)} · {author} · "
        source += f"{published.month}月{published.day}日 {published:%H:%M} 北京时间"
        if safe_url:
            source += (
                f' · [打开原文]({safe_url})'
                '{:target="_blank" rel="noopener noreferrer"}'
            )
        return f"**原始来源**：{source}"

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
                    ("它是什么", "what_it_is"),
                    ("AI 在做什么", "ai_role"),
                    ("怎么实现", "implementation_idea"),
                    ("动手练习", "hands_on_exercise"),
                    ("限制与不确定性", "limitations_or_uncertainties"),
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
