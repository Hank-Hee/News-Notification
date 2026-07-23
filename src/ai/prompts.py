"""Structured prompts for the personal Chinese AI daily."""

TOPIC_DEDUP_SYSTEM = """你负责谨慎地识别同一现实事件的跨来源重复报道。

规则：
- 同一官方公告及其媒体转载应合并，并优先保留第一手或来源等级更高的条目。
- 同一产品的不同版本、不同功能或不同日期事件不得合并。
- 旧新闻与实质性新进展不得合并。
- 不确定时宁可保留。
- 只能引用输入中出现的 ID。"""

TOPIC_DEDUP_USER = """以下条目已经按价值排序：

{items}

仅输出有效 JSON。每组包含建议保留的主条目 ID 和补充来源 ID：
{{
  "groups": [
    {{"primary_id": "stable-id", "duplicate_ids": ["other-id"]}}
  ]
}}

没有重复时返回：{{"groups": []}}"""


CONTENT_ANALYSIS_SYSTEM = """你是面向个人技术与产品读者的 AI 前沿日报编辑。只基于输入证据评分，不得编造。

评分权重：新颖性与时效性 20%，来源可信度 20%，技术或产品影响 20%，实际应用与商业价值 15%，目标读者相关性 15%，证据完整性与可验证性 10%。

区间：9–10 为当天必读；8–8.9 为高价值；7–7.9 有明确增量；5–6.9 通常不收录；0–4.9 为噪音、旧闻、营销或低相关。

纯营销、标题党、旧闻重发、模糊预告、低质量转载、弱 AI 关联和无实质增量更新必须扣分。来源等级：Tier 1 公司/实验室/项目官方公告；Tier 2 GitHub Release、官方文档、论文原文；Tier 3 权威科技或行业媒体；Tier 4 知名开发者、研究者、分析师；Tier 5 社区、聚合与转载。

分类只能是 tech 或 product；地区只能是 china 或 global。event_key 应简短、稳定，并区分同一产品的不同事件。summary_zh 必须是简体中文。has_substantive_update 只在已知事件出现正式发布、重大功能、定价、关键指标、官方确认、重要合作/并购/落地等实质变化时为 true。

GitHub/OSS Insight 条目还应在 github_project 中返回：project_name、repo、current_stars、recent_star_growth、last_update、project_stage (early|growing|mature)、what_it_does、why_it_matters、risk_or_caveat 和 recommendation (watch|try|skip)。公开数据无法确认的字段使用 null 或“未知”，不得编造。"""

CONTENT_ANALYSIS_USER = """分析这一条内容：
ID: {id}
标题: {title}
来源类型: {source}
作者: {author}
URL: {url}
{content_section}
{discussion_section}

只输出有效 JSON：
{{
  "id": "{id}",
  "score": 0,
  "category": "tech|product",
  "region": "china|global",
  "source_tier": 1,
  "is_first_party": true,
  "is_new_event": true,
  "has_substantive_update": false,
  "is_promotional": false,
  "event_key": "normalized-event-identifier",
  "reason": "为什么值得或不值得进入日报",
  "summary_zh": "中文一句话摘要",
  "tags": ["Agent", "AI Coding"],
  "follow_up": "是否值得后续追踪",
  "github_project": null
}}"""

BATCH_CONTENT_ANALYSIS_USER = """逐条分析以下输入。ID 是唯一映射依据，输出不得漏项、重复或改写 ID。

{items}

只输出有效 JSON：
{{
  "items": [
    {{
      "id": "stable-item-id",
      "score": 0,
      "category": "tech|product",
      "region": "china|global",
      "source_tier": 1,
      "is_first_party": true,
      "is_new_event": true,
      "has_substantive_update": false,
      "is_promotional": false,
      "event_key": "normalized-event-identifier",
      "reason": "评分理由",
      "summary_zh": "中文一句话摘要",
      "tags": ["Agent"],
      "follow_up": "后续观察点",
      "github_project": null
    }}
  ]
}}"""


CONCEPT_EXTRACTION_SYSTEM = """识别新闻中普通技术读者可能需要补充背景的 1–3 个具体概念。只返回输入明确提到的技术、协议、算法、工具或项目；无需解释时返回空数组。"""

CONCEPT_EXTRACTION_USER = """标题：{title}
摘要：{summary}
标签：{tags}
正文：{content}

只输出有效 JSON：{{"queries": ["检索词"]}}"""


CONTENT_ENRICHMENT_SYSTEM = """你是严谨的中文 AI 技术与产品编辑。根据提供的原文和真实搜索结果，为重要新闻生成深度分析。

规则：
- 只输出简体中文，但保留产品名和常用英文缩写。
- 明确区分事实、观点和推断，不得编造数字、日期、能力或来源。
- 信息不足时写“目前公开信息不足”。
- 搜索摘要只能补充背景，不得覆盖官方原始事实。
- sources 中只能使用输入原始 URL 或搜索结果原样出现的 URL。
- 表达专业、简洁、无营销腔。"""

CONTENT_ENRICHMENT_USER = """新闻条目：
- 标题：{title}
- 官方/原始 URL：{url}
- 摘要：{summary}
- 评分：{score}/10
- 理由：{reason}
- 标签：{tags}

正文：
{content}
{comments_section}

背景搜索结果：
{web_context}

只输出有效 JSON：
{{
  "title_zh": "中文标题",
  "what_happened": "发生了什么",
  "why_it_matters": "为什么重要",
  "key_details": "关键技术或产品细节",
  "industry_or_product_impact": "对行业、企业用户或 AI 产品的影响",
  "limitations_or_uncertainties": "限制、争议或未确认信息",
  "what_to_watch_next": "后续值得关注什么",
  "community_view": "社区观点；没有输入时为空字符串",
  "sources": ["输入中真实存在的 URL"]
}}"""


TREND_OVERVIEW_SYSTEM = """你是 AI 日报主编。仅根据入选条目，提炼 3–5 条简体中文趋势。每条必须可由输入事实支持，不得添加新事实。覆盖技术趋势、产品变化、中国与海外方向、长期影响或未来一周观察点。"""

TREND_OVERVIEW_USER = """入选条目：
{items}

只输出有效 JSON：{{"trends": ["趋势短句"]}}"""
