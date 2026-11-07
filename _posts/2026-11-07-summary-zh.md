---
layout: default
title: "AI产品情报 · 2026-11-07"
date: 2026-11-07
lang: zh
---

**日期**：2026-11-07　 **更新时间**：2026-11-07 13:58 北京时间

> 从 112 条内容中筛选出 7 条重要资讯。

> 今日高质量增量有限，因此未使用低质量内容补足数量。

<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Vercel 让 Chat SDK 代理用 json-render 流式生成表格、图表、按钮等 UI 卡片，解决跨平台消息格式维护问题，适合构建者学习如何让 AI 输出结构化界面。
- Hightouch 让一个小模型 Jev 在不确定时向 Opus 求助，在身份解析任务上以约四分之一成本达到 Opus 的准确率，展示了多模型编排的产品思路。
- Meta 在 Muse AI 助手中推出 spaces 功能，用户可让 AI 生成购物中心、学校仪表盘等定制化应用式体验，值得看大厂如何把助手变成可搭建产品的入口。
- Vercel AI Gateway 新增 DeepSeek Search 和 Fetch 工具，让任意支持工具调用的模型用同一 API key 完成搜索和网页抓取，解决多模型切换时搜索工具不统一的问题。
- Anthropic 发布 Claude Code v2.1.319，让 MCP 工具调用可后台运行并新增权限拒绝设置，帮助开发者更顺畅地构建终端 Agent 工作流。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Chat SDK Agent 现在能用 json-render 流式生成 UI 卡片](https://vercel.com/changelog/json-render-and-chat-sdk-agents){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Vercel 让 Chat SDK 代理用 json-render 流式生成表格、图表、按钮等 UI 卡片，解决跨平台消息格式维护问题，适合构建者学习如何让 AI 输出结构化界面。

**评分**：8.2 / 10　 **证据**：一手信息

**产品 / 团队**：Chat SDK + json-render（Vercel 官方） / Ben Sabic

**目标用户**：开发跨平台聊天机器人、AI 客服、内部工具的工程师和构建者

**它是什么**：Vercel 给 Chat SDK 加了一套机制，让 AI Agent（能自动调用工具的 AI 程序）输出 JSON 格式的界面描述，实时转成 Slack、Teams 等平台能直接显示的消息卡片，不用为每个平台单独写代码。

**用户问题**：以前想让 AI 在 Slack 显示表格、在 Teams 显示图表，得分别学 Block Kit、Adaptive Cards 等不同格式，维护多套代码；AI 生成界面时也没法边生成边显示，用户要等很久才能看到结果。

**使用流程**：
1. 开发者在代码里定义一套组件目录（表格、图表、按钮等），告诉 Agent 有哪些 UI 可用
2. Agent 根据对话内容，写出一段 JSON 格式的界面规格说明
3. json-render 把 JSON 转成 Chat SDK 的通用卡片，同时 streamCard 边生成边推送给用户（最快每 500ms 更新一次）
4. Chat SDK 的 adapter 把卡片转成 Slack/Teams/Discord 等平台的原生格式发出去，超出平台限制时自动降级或报错

**AI 在做什么**：Agent 负责根据用户请求，选择合适的组件并写出正确的 JSON 规格；如果写错了，开发者可以把错误列表发回给 AI 让它自行修正。

**怎么实现**：核心思路是&quot;写一次 JSON，到处渲染&quot;。中间加了一层抽象：左边是 AI 懂的组件目录（用 TypeScript 类型约束），右边是各平台的适配器。AI 只和中间层打交道，不用知道 Slack 和 Teams 的具体语法。流式更新靠一个计时器控制频率，避免消息闪得太快。

**需要理解的知识点**：
1. Agent：一种能自主决定下一步行动的 AI 程序，不只是回答问题，还能调用工具、生成文件或界面
2. 流式生成（Streaming）：AI 边想边输出，不用等全部想完才显示，用户体验更接近真人打字
3. 结构化输出 / JSON Schema：用固定的 JSON 格式约束 AI 的输出，让程序能可靠地解析，比让 AI 自由写代码更安全

**动手练习**：30 分钟：访问 https://chat-sdk-demo.json-render.dev 试用 playground，观察 AI 如何生成表格/图表；再花 30 分钟读 https://json-render.dev/docs/api/chat 的文档，尝试在本地用 Chat SDK 跑一个最简单的 streamCard 示例，把 AI 生成的 JSON 改成故意写错一个字段，看 toCard 会不会抛出 CardSpecError。

**已知限制**：未公开：具体支持哪些平台 adapter 的完整清单、组件目录目前有多少内置组件、是否支持自定义组件的详细规则、生产环境性能数据（延迟、并发）、定价模式。

**原始来源**：rss · Ben Sabic · 11月7日 05:00 北京时间 · [打开原文](https://vercel.com/changelog/json-render-and-chat-sdk-agents){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Hightouch 用「小模型+大模型」组合，把身份解析成本降到四分之一](https://hightouch.com/blog/llm-judges-identity-resolution){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Hightouch 让一个小模型 Jev 在不确定时向 Opus 求助，在身份解析任务上以约四分之一成本达到 Opus 的准确率，展示了多模型编排的产品思路。

**评分**：8.1 / 10　 **证据**：一手信息

**产品 / 团队**：Jev（TypeSafe AI 的小模型）+ Claude Opus（Anthropic 的大模型），由 Hightouch 集成使用 / theanomaly

**目标用户**：需要批量做身份解析（把不同来源的零碎用户数据拼成同一个人）的数据工程师、CDP/营销技术团队

**它是什么**：Hightouch 在自家产品里做的一个模型编排实验：让小模型 Jev 处理常规任务，没把握时再去问 Claude Opus，结果在身份解析任务上省了约 75% 的钱，准确率却没掉。

**用户问题**：用大模型做身份解析，准确率高但 API 账单贵；用小模型便宜但容易认错人。怎么不花冤枉钱又能保证准度？

**使用流程**：
1. 把多条来源的用户记录丢给 Jev，让它判断是不是同一个人
2. Jev 自己打分：如果很确定，直接给答案；如果不确定，触发「向上求助」
3. Jev 把难题包装好，发给 Claude Opus 做最终判断
4. 返回结果，同时记录这次 escalated（升级）花了多少成本

**AI 在做什么**：Jev 是第一道关卡，负责快速筛选和决策是否升级；Opus 是后备专家，只处理 Jev 没把握的硬案例。这种分工叫「模型编排」（Model Orchestration），白话就是「让合适的模型干合适的活」。

**怎么实现**：核心思路是「分级诊疗」：小病小医院看，大病转三甲。Jev 被训练/提示成能判断自己的不确定程度——如果输入模糊、字段缺失、或涉及复杂规则，就自动转交。关键是让 Jev「知道自己不知道」，而不是瞎猜。Hightouch 还给了 Jev 一份「Opus 能力说明书」，帮它更准地决定什么时候该升级。

**需要理解的知识点**：
1. 模型编排（Model Orchestration）：不只用一个大模型，而是把多个模型串起来，像流水线一样分工，省钱又保效果
2. Agent：这里 Jev 就是一个简单 Agent——不只是回答问题，还能自己做决策（要不要调用外部工具/模型），Agent 白话就是「能自己动起来的 AI，不只是你问一句它答一句」
3. Function Calling：Jev 决定升级时，其实就是在调用另一个模型当工具，Function Calling 白话就是「让 AI 决定什么时候调用外部功能，比如查数据库或调用另一个 AI」

**动手练习**：30 分钟动手：用你熟悉的编程语言（Python/JS 都行），写一个两层路由脚本。第一层用便宜模型（如 GPT-3.5 或本地小模型），让它判断问题难度 1-5 分；4-5 分的问题转发给 GPT-4/Claude 3.5。准备 10 个真实问题跑一遍，对比「全部用大模型」和「分层路由」的成本与准确率差异。可以用 OpenRouter 统一 API 方便比价。

**已知限制**：实验仅限「身份解析」这一个任务，不能推广到通用场景；Jev 的「不确定度判断」具体怎么训练/提示的未公开；社区有人质疑校准图表解读可能有误（Luna 的校准误差可能比 Jev 更低）；Jev 本身信息极少，Wikipedia 显示其为 TypeSafe AI 的 proprietary 模型，2026 年才有限开放，但当前日期为 2025 年，该信息存疑。

**原始来源**：hackernews · theanomaly · 11月7日 03:48 北京时间 · [打开原文](https://hightouch.com/blog/llm-judges-identity-resolution){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [🎙️ How I AI: Grok vs. Dot vs. Muse vs. Duet + How Figma’s PMs actually use AI every day](https://www.lennysnewsletter.com/p/how-i-ai-grok-vs-dot-vs-muse-vs-duet){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Lenny Rachitsky 在播客中对比 Grok、Dot、Muse 和 Claude Duet 等 AI 产品，并讨论 Figma 产品经理日常如何使用 AI，适合了解产品使用场景但缺少一手构建细节。

**对做产品的启发**：Lenny 的播客对比多个 AI 产品，属于从业者分析，但内容为音频/视频，文字摘要有限，缺乏可验证的产品细节或构建过程；对产品经理有参考价值但增量有限。

**继续验证**：等待文字版详细拆解或产品经理的具体工作流案例。

**原始来源**：newsletter · Lenny Rachitsky · 11月3日 00:02 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-grok-vs-dot-vs-muse-vs-duet){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [Beyond code generation: A developer’s guide to agentic engineering](https://github.blog/ai-and-ml/github-copilot/beyond-code-generation-a-developers-guide-to-agentic-engineering/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

GitHub 发布开发者指南，说明如何用 Copilot 完成规划、写代码、审查和排查生产问题，并指出哪些环节仍需人工判断，帮助理解 Agent 工程的实际用法。

**对做产品的启发**：GitHub 官方博客发布开发者指南，讲如何用 Copilot 做规划、写代码、审查和排查生产问题，并指出哪些工作仍需人工判断，属于构建者实践经验，对初学者理解 Agent 工作流有迁移价值，但偏教程而非产品发布。

**继续验证**：观察 Copilot 在 Agent 工作流中是否推出具体新功能或用户案例。

**原始来源**：rss · Nick Liffen · 11月7日 06:15 北京时间 · [打开原文](https://github.blog/ai-and-ml/github-copilot/beyond-code-generation-a-developers-guide-to-agentic-engineering/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

_今天没有值得单独展开的模型公司一手动态。_

### 其他值得留意

### [Meta’s Muse AI can create custom ‘spaces’ for the version of the app you need right now](https://www.theverge.com/tech/1028871/meta-muse-ai-spaces){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Meta 在 Muse AI 助手中推出 spaces 功能，用户可让 AI 生成购物中心、学校仪表盘等定制化应用式体验，值得看大厂如何把助手变成可搭建产品的入口。

**对做产品的启发**：Meta 在 Muse 助手中推出可定制 app-like 体验的 spaces 功能，属于大厂 AI 产品新形态，有明确产品功能增量，但报道非一手且缺少用户反馈。

**继续验证**：观察 spaces 的实际使用案例、用户反馈和是否开放第三方组件。

**原始来源**：rss · Emma Roth · 11月7日 02:10 北京时间 · [打开原文](https://www.theverge.com/tech/1028871/meta-muse-ai-spaces){:target="_blank" rel="noopener noreferrer"}

### [AI Gateway adds DeepSeek Search and Fetch tools](https://vercel.com/changelog/ai-gateway-adds-deepseek-search-and-fetch-tools){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

Vercel AI Gateway 新增 DeepSeek Search 和 Fetch 工具，让任意支持工具调用的模型用同一 API key 完成搜索和网页抓取，解决多模型切换时搜索工具不统一的问题。

**对做产品的启发**：Vercel 官方更新，AI Gateway 新增 DeepSeek Search 和 Fetch 工具，有明确定价和接入方式，对构建带搜索能力的 AI 产品有可迁移增量，但属于基础设施功能。

**继续验证**：观察开发者用 Search/Fetch 组合构建的检索类产品案例。

**原始来源**：rss · Zachary Chen · 11月7日 05:00 北京时间 · [打开原文](https://vercel.com/changelog/ai-gateway-adds-deepseek-search-and-fetch-tools){:target="_blank" rel="noopener noreferrer"}

### [anthropics/claude-code released v2.1.319](https://github.com/anthropics/claude-code/releases/tag/v2.1.319){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Anthropic 发布 Claude Code v2.1.319，让 MCP 工具调用可后台运行并新增权限拒绝设置，帮助开发者更顺畅地构建终端 Agent 工作流。

**对做产品的启发**：Claude Code 官方发布，新增 MCP 任务后台化、权限拒绝替代提示、API 延迟优化命令等，属于 Agent 工具链的实用功能更新，对构建 AI 产品有可迁移参考，但为常规版本迭代，非重大能力突破。

**继续验证**：观察 MCP 任务后台化在实际 Agent 产品中的采用情况，以及权限拒绝设置对安全性的影响。

**原始来源**：github · claude-code-publisher\[bot\] · 11月7日 01:04 北京时间 · [打开原文](https://github.com/anthropics/claude-code/releases/tag/v2.1.319){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent：一种能自主决定下一步行动的 AI 程序，不只是回答问题，还能调用工具、生成文件或界面
- **知识点**：流式生成（Streaming）：AI 边想边输出，不用等全部想完才显示，用户体验更接近真人打字
- **知识点**：结构化输出 / JSON Schema：用固定的 JSON 格式约束 AI 的输出，让程序能可靠地解析，比让 AI 自由写代码更安全
- **知识点**：模型编排（Model Orchestration）：不只用一个大模型，而是把多个模型串起来，像流水线一样分工，省钱又保效果
- **动手练习**：30 分钟：访问 https://chat-sdk-demo.json-render.dev 试用 playground，观察 AI 如何生成表格/图表；再花 30 分钟读 https://json-render.dev/docs/api/chat 的文档，尝试在本地用 Chat SDK 跑一个最简单的 streamCard 示例，把 AI 生成的 JSON 改成故意写错一个字段，看 toCard 会不会抛出 CardSpecError。
- **动手练习**：30 分钟动手：用你熟悉的编程语言（Python/JS 都行），写一个两层路由脚本。第一层用便宜模型（如 GPT-3.5 或本地小模型），让它判断问题难度 1-5 分；4-5 分的问题转发给 GPT-4/Claude 3.5。准备 10 个真实问题跑一遍，对比「全部用大模型」和「分层路由」的成本与准确率差异。可以用 OpenRouter 统一 API 方便比价。

## 数据与筛选说明

- 每天 08:30（北京时间）处理公开来源；Newsletter 回看 7 天，其他来源回看 24 小时。
- 优先级依次为：真实 AI 产品、构建实践、模型公司核心人员、新能力、精选 Newsletter。
- 纯算力、GPU、底层推理优化和学术论文默认降权，除非能直接解释新的产品机会。
- Top 2 由 Kimi 做初学者版产品拆解；失败时只对该条使用 DeepSeek Pro，所有模型均关闭思考。
- 同一事件执行语义去重和最近 7 天历史去重；结果缓存并同步到 JSON、CSV 和可筛选数据库页面。

[打开产品情报数据库]({{ '/products/' | relative_url }}) · [下载 JSON]({{ '/data/product-intelligence.json' | relative_url }}) · [下载 CSV]({{ '/data/product-intelligence.csv' | relative_url }})

<a id="archives"></a>
## 历史日报

[返回首页查看按日期归档]({{ '/' | relative_url }})
