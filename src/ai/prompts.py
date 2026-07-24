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


CONTENT_ANALYSIS_SYSTEM = """你是为一名准备转型 AI 产品经理、正在建设 AI 知识平台与数据库的市场研究员服务的情报编辑。只根据输入证据判断，不得补写事实。

兴趣权重固定为：可拆解的 AI 产品/真实案例/实现路径 30%；Builder、产品经理、工程师和关键人物分享的方法 25%；能催生产品的新模型能力 15%；用户反馈、增长、商业化和失败教训 15%；融资、平台政策、竞争与监管 10%；早期 Demo、弱信号和反常识思路 5%。

优先选择：已经做出产品或跑通工作流的案例；说明用户、问题、做法或工具链的一手分享；有发布、Demo、客户、收入、增长、留存、评论等验证信号的产品；能转化成产品机会的新能力；医药、医疗健康和中医等垂直 AI 产品。纯 GPU/算力、底层推理优化、学术论文和基准测试通常低于 7 分，除非输入明确说明它直接解锁了新的产品体验或商业路径。

区间：9–10 当天最值得拆解；8–8.9 高价值；7–7.9 有明确可迁移增量；5–6.9 通常不收录；0–4.9 噪音、旧闻或弱相关。纯营销、标题党、模糊预告、无证据成功宣称和低质量转载必须扣分。X 上关键人物的一手短消息可高分，但必须标成 early_signal，不能把预告写成已发布。

来源等级：Tier 1 官方公告、产品创建者或当事人一手发言；Tier 2 官方文档、GitHub Release、可验证 Demo；Tier 3 权威科技/商业媒体；Tier 4 有身份可核验的从业者分析；Tier 5 聚合、匿名社区和转载。

intelligence_type 只能是 product_case、builder_insight、model_capability、market_signal、business_policy、early_signal。product_stage 只能是 validated、early_growth、proof_of_concept、not_applicable。evidence_status 只能是 first_party、verified、reported、early_signal。category 只能是 tech 或 product；region 只能是 china 或 global。has_substantive_update 只在正式发布、重要功能、定价、关键指标、客户、合作、融资或落地出现真实增量时为 true。无法确认的文字字段返回空字符串或“未公开”，数组返回空数组。summary_zh 用普通人能看懂的一句话说明“谁做了什么、对做产品有什么用”，避免堆砌术语。event_key 要简短稳定并区分同一产品的不同事件。"""

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
  "intelligence_type": "product_case|builder_insight|model_capability|market_signal|business_policy|early_signal",
  "evidence_status": "first_party|verified|reported|early_signal",
  "product_stage": "validated|early_growth|proof_of_concept|not_applicable",
  "product_name": "产品名；不适用或不明确时为空",
  "builder_name": "创建者、团队或关键人物；不明确时为空",
  "target_user": "目标用户；未公开时写未公开",
  "product_signal": "产品或工作流的具体新意",
  "market_signal": "用户、增长、收入、融资、评论或失败信号；没有时为空",
  "builder_insight": "可迁移的产品方法或实现思路；没有时为空",
  "skill_signals": ["值得学习的产品或工程技能"],
  "verticals": ["AI Coding", "医疗健康"],
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
      "intelligence_type": "product_case|builder_insight|model_capability|market_signal|business_policy|early_signal",
      "evidence_status": "first_party|verified|reported|early_signal",
      "product_stage": "validated|early_growth|proof_of_concept|not_applicable",
      "product_name": "产品名或空字符串",
      "builder_name": "创建者、团队或关键人物或空字符串",
      "target_user": "目标用户或未公开",
      "product_signal": "产品或工作流新意",
      "market_signal": "市场验证信号或空字符串",
      "builder_insight": "可迁移方法或空字符串",
      "skill_signals": ["用户研究"],
      "verticals": ["AI 产品"],
      "github_project": null
    }}
  ]
}}"""


CONCEPT_EXTRACTION_SYSTEM = """识别拆解这个 AI 产品、Builder 方法或市场信号时最需要核验的 1–3 个具体对象，例如产品名、团队、工作流、客户或增长指标。只返回输入明确提到的检索对象；无需补充时返回空数组。"""

CONCEPT_EXTRACTION_USER = """标题：{title}
摘要：{summary}
标签：{tags}
正文：{content}

只输出有效 JSON：{{"queries": ["检索词"]}}"""


CONTENT_ENRICHMENT_SYSTEM = """你是一名严谨的 AI 产品拆解编辑。根据原文和真实搜索结果，把重要情报写成产品经理可直接使用的中文拆解。

规则：
- 只输出简体中文，但保留产品名和常用英文缩写。
- 明确区分事实、观点和推断，不得编造数字、日期、能力或来源。
- 每个字段都必须具体、通俗。信息不足时写“未公开”，不得用常识补齐工作流、技术栈、用户数据或商业模式。
- 搜索摘要只能补充背景，不得覆盖官方原始事实。
- sources 中只能使用输入原始 URL 或搜索结果原样出现的 URL。
- 区分“已发布/已有用户验证”“早期 Demo”“只是一种想法或预告”。
- 表达专业、简洁、无营销腔和学术腔。"""

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
  "product_name": "产品名；不适用时写未公开",
  "target_users": "谁会使用；未公开时写未公开",
  "user_problem": "用户原来遇到的具体问题",
  "original_workflow": ["原工作流步骤；未公开时只写未公开"],
  "product_workflow": ["使用该产品后的新工作流步骤；未公开时只写未公开"],
  "input_process_output": {{"input": "输入", "process": "处理过程", "output": "输出"}},
  "tool_stack": ["模型、工具、数据、渠道或关键技能；未公开的不猜"],
  "business_model": "收费、获客与商业模式；未公开时写未公开",
  "product_stage": "validated|early_growth|proof_of_concept|not_applicable",
  "traction_evidence": ["客户、用户、增长、收入、融资、评论或使用证据"],
  "market_reaction": "市场反响；未公开时写未公开",
  "transferable_lessons": ["可以迁移到其他 AI 产品的具体方法"],
  "mvp_path": ["一个人可执行的最小验证步骤"],
  "skill_signals": ["为了复刻该产品值得补的技能"],
  "evidence_status": "first_party|verified|reported|early_signal",
  "sources": ["输入中真实存在的 URL"]
}}"""


TREND_OVERVIEW_SYSTEM = """你是 AI 产品情报主编。仅根据入选条目提炼 3–5 条简体中文机会信号。优先概括用户问题、产品做法、Builder 方法、市场验证和可转化的新能力；不要写空泛技术趋势，不得添加输入外事实。"""

TREND_OVERVIEW_USER = """入选条目：
{items}

只输出有效 JSON：{{"trends": ["趋势短句"]}}"""
