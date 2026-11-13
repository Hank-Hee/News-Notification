---
layout: default
title: "AI产品情报 · 2026-11-13"
date: 2026-11-13
lang: zh
---

**日期**：2026-11-13　 **更新时间**：2026-11-13 14:43 北京时间

> 从 116 条内容中筛选出 11 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Replit Agent 新增用 Link 和 Visa 采购物资、用 Google Ads 触达客户的功能，帮助创业者扩展业务。
- Amplitude 用 OpenAI 模型构建产品代理 Wave，帮团队判断该做什么、用编码代理快速上线并衡量效果；对想理解 AI 如何嵌入产品工作流的初学者有参考价值。
- ArtCraft 用 AI 将 Photoshop 重写为开源软件，CEO Brandon Thomas 有更大愿景，访谈披露产品思路。
- Google 搜索接入 Gemini 4 Hydrogen 进行重大升级；让搜索体验用上新模型能力；对观察模型能力如何直接改变产品交互有参考价值。
- Gondola 用 Codex 和 ChatGPT 提升创意人才匹配平台的开发效率，首席工程师产出提高 50%、收入翻倍；可作为小团队用 AI 编码代理的参考案例。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Replit Agent 新增采购和广告投放功能，帮创业者搞定生意琐事](https://replit.com/blog/replit-agent-ads-commerce){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Replit Agent 新增用 Link 和 Visa 采购物资、用 Google Ads 触达客户的功能，帮助创业者扩展业务。

**评分**：8.5 / 10　 **证据**：一手信息

**产品 / 团队**：Replit Agent / Replit Blog

**目标用户**：不会写代码但想创业的人，以及会写代码但不擅长运营、采购、推广的创始人

**它是什么**：Replit Agent 是一个能用自然语言帮你写代码、建网站的 AI 助手，现在还能帮你采购办公物资和投放 Google 广告。

**用户问题**：很多人能用 AI 做出产品，但后续还要面对公司注册、服务器维护、找客户、买物资、打广告等一系列杂事，每件事都是新门槛，拖慢业务增长

**使用流程**：
1. 用自然语言描述你想做的产品，Replit Agent 帮你写出代码并上线
2. 把 Stripe 接入你的应用，开始收钱
3. 告诉 Agent 需要买什么物资，它通过 Link/Visa 完成采购
4. 告诉 Agent 你的目标客户，它在 Google Ads 上帮你投广告

**AI 在做什么**：AI 扮演&#x27;全能队友&#x27;：写代码、接支付、采购、投广告，但每笔花钱操作都要经过你确认

**怎么实现**：核心思路是&#x27;Agent 即服务&#x27;——一个主智能体（Agent，能自主规划和执行任务的 AI 程序）拆解你的大白话需求，再调用不同子系统：写代码用 Replit 自己的开发环境，付钱走 Stripe Link + Visa 的支付接口，广告投放走 Google Ads API。关键是&#x27;人在回路&#x27;，花钱前必须你点确认。

**需要理解的知识点**：
1. Agent（智能体）：不只是聊天回答，而是能自己规划步骤、调用工具、完成多环节任务的 AI 程序
2. Function Calling（函数调用）：AI 判断&#x27;现在该调用哪个外部 API&#x27;的能力，比如识别&#x27;我要买服务器&#x27;→调用 Stripe 支付接口
3. RAG（检索增强生成）：虽然本文未直接提及，但这类商业 Agent 通常需要实时查库存、查广告政策，把外部信息&#x27;喂&#x27;给 AI 再生成决策，避免胡说

**动手练习**：去 replit.com 免费注册，用一句话让 Replit Agent 做一个&#x27;收集用户邮箱的落地页&#x27;，部署上线后，尝试在设置里找到 Stripe 连接入口（无需真绑定），体验&#x27;从想法到可收钱的产品&#x27;全流程，记录 Agent 每一步问了什么问题、做了什么决定。

**已知限制**：未公开具体支持哪些国家/地区的 Visa 支付；未公开 Google Ads 投放是否需要用户自己先有广告账户；未公开&#x27;九倍增长&#x27;的具体基数和统计口径；未说明采购功能是否覆盖非美国供应商

**原始来源**：rss · Replit Blog · 11月13日 00:45 北京时间 · [打开原文](https://replit.com/blog/replit-agent-ads-commerce){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Amplitude 如何用 OpenAI 在 1-2 天内交付产品改进](https://openai.com/business/customer-stories/amplitude){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Amplitude 用 OpenAI 模型构建产品代理 Wave，帮团队判断该做什么、用编码代理快速上线并衡量效果；对想理解 AI 如何嵌入产品工作流的初学者有参考价值。

**评分**：8.2 / 10　 **证据**：一手信息

**产品 / 团队**：Wave / OpenAI News

**目标用户**：Amplitude 内部产品团队（产品经理、工程师）

**它是什么**：Amplitude 基于 OpenAI 模型构建的主动式产品 Agent（代理）Wave，能自动发现该做什么功能、辅助编码上线、并衡量效果。Agent 指让 AI 自主完成多步骤任务的系统，不只是单次问答。

**用户问题**：传统产品迭代周期长，从发现需求到上线往往需要数周；团队难以快速判断该优先做什么、快速编码验证、并及时衡量上线效果

**使用流程**：
1. Wave 分析数据，主动识别该构建什么功能
2. 团队确认方向后，Wave 调用编码 Agent 辅助写代码、快速上线
3. 上线后 Wave 自动衡量该改动对产品指标的实际影响

**AI 在做什么**：全程参与：需求识别（分析数据→建议）、编码执行（生成/辅助代码）、效果衡量（追踪指标变化）

**怎么实现**：把 LLM 包装成一个&#x27;能干活&#x27;的代理：先让它读产品数据做判断，再让它调用工具写代码，最后让它追踪结果——本质是&#x27;观察→行动→验证&#x27;的闭环，不是一次性聊天。

**需要理解的知识点**：
1. Agent：不只是问 AI 问题，而是让 AI 能自主调用工具、做多步决策的系统
2. Function Calling：让 LLM 决定调用哪个外部工具（如查数据、写代码）的机制，是 Agent 的&#x27;手脚&#x27;
3. RAG（检索增强生成）：Agent 可能需要先查内部数据再做判断，把相关数据&#x27;喂&#x27;给模型再生成答案

**动手练习**：用任意 LLM（如 GPT-4）尝试：① 给它一段模拟的产品数据，让它分析并提出一个功能建议；② 要求它输出一段可运行的 Python 代码来实现该功能；③ 手动运行代码，把结果再丢给 LLM 让它评估效果是否达标。全程用自然语言对话完成，体会&#x27;观察→行动→验证&#x27;的 Agent 思路。

**已知限制**：未公开 Wave 具体使用哪个 OpenAI 模型、编码 Agent 的实现细节（是否完全自主或人机协作）、实际 1-2 天的成功率/覆盖场景比例、以及是否有外部用户验证过这些数字；原文为 OpenAI 官方客户故事，属于营销内容，无独立第三方验证

**原始来源**：rss · OpenAI News · 11月13日 04:00 北京时间 · [打开原文](https://openai.com/business/customer-stories/amplitude){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

_最近 7 天没有达到收录标准的新 Newsletter 内容；请查看数据源日志。_

<a id="how-they-build"></a>
## 他们怎么做

### [Build once, run on any agent: A practical guide to agent skills](https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

GitHub 发布 agent skills 实践指南，教团队把重复工程工作写成可审查复用的文件；帮助初学者理解如何让 AI 代理稳定执行任务。

**对做产品的启发**：GitHub 官方博客的 agent skills 实践指南，讲如何把可重复工程工作沉淀为可复用文件，属于构建者方法论；但偏教程、缺少真实产品案例和用户反馈，对产品经理的可迁移增量中等，给 7.6。

**继续验证**：关注 agent skills 的实际采用案例和跨代理复用的真实效果。

**原始来源**：rss · Andrea Griffiths · 11月13日 06:54 北京时间 · [打开原文](https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude 4](https://www.anthropic.com/news/claude-4){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

Anthropic 官方发布 Claude 4 模型；为开发者提供新一代基础模型能力；值得关注其可能解锁的新产品体验。

**对做产品的启发**：Anthropic 官方发布 Claude 4，属于模型公司核心能力动态，对产品经理理解新模型能力边界有直接价值，但正文信息极简，缺少具体能力细节和产品体验描述，因此未达 9 分。

**继续验证**：关注 Claude 4 的具体能力参数、定价、API 可用性及首批产品案例。

**原始来源**：public\_web · Anthropic News · 11月13日 05:02 北京时间 · [打开原文](https://www.anthropic.com/news/claude-4){:target="_blank" rel="noopener noreferrer"}

### [anthropics/claude-code released v2.1.323](https://github.com/anthropics/claude-code/releases/tag/v2.1.323){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

Anthropic 给 Claude Code 加了实验性 Code Mode，让模型写 JavaScript 来调用工具，解决工具编排方式单一的问题，值得看它如何改变 Agent 的开发体验。

**对做产品的启发**：Claude Code 新增实验性 Code Mode，让 Claude 写 JavaScript 调用工具，这是 Agent 工具调用范式的可迁移变化；同时有插件版本约束、TypeScript 钩子校验等工程化改进，对构建者有参考价值。

**继续验证**：观察 Code Mode 的实际使用反馈、是否默认开启，以及社区是否出现基于它的新工作流。

**原始来源**：github · claude-code-publisher\[bot\] · 11月13日 06:12 北京时间 · [打开原文](https://github.com/anthropics/claude-code/releases/tag/v2.1.323){:target="_blank" rel="noopener noreferrer"}

### [llm-gemini 0.37](https://simonwillison.net/2026/Nov/12/llm-gemini/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Simon Willison 发布 llm-gemini 0.37，支持 Gemini 4 Hydrogen 模型，并指出其定价复杂。

**对做产品的启发**：Simon Willison 发布 llm-gemini 插件更新，支持新模型，属于开发者工具的一手更新，但内容主要是版本发布和定价困惑，对产品经理增量有限。

**继续验证**：观察该插件在开发者中的采用情况。

**原始来源**：rss · Simon Willison · 11月13日 06:55 北京时间 · [打开原文](https://simonwillison.net/2026/Nov/12/llm-gemini/){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [AI Ambition: ArtCraft Cloned Photoshop and Now Wants to &quot;Rebuild Everything&quot;](https://latent.space/p/artcraft/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

ArtCraft 用 AI 将 Photoshop 重写为开源软件，CEO Brandon Thomas 有更大愿景，访谈披露产品思路。

**对做产品的启发**：ArtCraft 用 AI 重写 Photoshop 为开源软件，属于有产品、有构建过程的一手案例，对产品经理有迁移价值，但来源为 Newsletter 访谈，非直接一手。

**继续验证**：关注 ArtCraft 开源产品的用户反馈和迭代。

**原始来源**：rss · Richard MacManus · 11月13日 12:17 北京时间 · [打开原文](https://latent.space/p/artcraft/){:target="_blank" rel="noopener noreferrer"}

### [Google Search gets a major upgrade with Gemini 4 Hydrogen](https://blog.google/products-and-platforms/products/search/gemini-4-hydrogen-search-upgrade/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Google 搜索接入 Gemini 4 Hydrogen 进行重大升级；让搜索体验用上新模型能力；对观察模型能力如何直接改变产品交互有参考价值。

**对做产品的启发**：Google 官方博客宣布搜索接入 Gemini 4 Hydrogen，属于模型能力落地到具体产品的官方更新；但正文仅为轮播卡片描述，缺少功能细节和用户反馈，营销属性明显，给 7.5。

**继续验证**：关注搜索升级的具体功能、用户实际体验反馈和与竞品的差异。

**原始来源**：rss · Robby Stein · 11月13日 02:00 北京时间 · [打开原文](https://blog.google/products-and-platforms/products/search/gemini-4-hydrogen-search-upgrade/){:target="_blank" rel="noopener noreferrer"}

### [Gondola doubles revenue as its team builds more with Codex](https://openai.com/business/customer-stories/gondola){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Gondola 用 Codex 和 ChatGPT 提升创意人才匹配平台的开发效率，首席工程师产出提高 50%、收入翻倍；可作为小团队用 AI 编码代理的参考案例。

**对做产品的启发**：OpenAI 官方客户案例，提到 Codex 让首席工程师产出提升 50%、收入翻倍，属于有指标的一手实践；但内容偏营销，缺少产品细节和可验证方法，对产品经理的可迁移增量有限，给 7.2。

**继续验证**：关注 Gondola 的具体工作流、Codex 使用方式和收入增长的归因证据。

**原始来源**：rss · OpenAI News · 11月12日 20:00 北京时间 · [打开原文](https://openai.com/business/customer-stories/gondola){:target="_blank" rel="noopener noreferrer"}

### [openai/codex released rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

OpenAI Codex 发布 rust-v0.168.0，新增模型提供者选择、侧边对话、音频附件和 GIF 生成等功能。

**对做产品的启发**：OpenAI Codex 正式版本发布，包含多项新功能（模型提供者选择、侧边对话、音频附件等），对开发者有直接价值，但属于工具更新，对产品经理增量中等。

**继续验证**：关注这些功能对编程工作流的影响。

**原始来源**：github · github-actions\[bot\] · 11月13日 11:54 北京时间 · [打开原文](https://github.com/openai/codex/releases/tag/rust-v0.168.0){:target="_blank" rel="noopener noreferrer"}

### [Brave Search API now accepts agentic payments via the x402 protocol](https://brave.com/blog/search-api-agentic-payments/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Brave 让搜索 API 接受 Agent 通过 x402 协议按次付费，解决 AI Agent 调用搜索服务时的自动支付问题，值得看它能否成为 Agent 付费的新模式。

**对做产品的启发**：Brave 搜索 API 支持 x402 协议让 Agent 用加密货币按次付费，是 Agent 商业化支付路径的新尝试，HN 讨论有真实观点碰撞；但尚属早期信号，实际采用情况未知，对产品经理有启发但非成熟案例。

**继续验证**：观察是否有开发者实际接入、定价与结算体验，以及是否引发其他搜索或 API 服务跟进。

**原始来源**：hackernews · sjdh76 · 11月13日 11:08 北京时间 · [打开原文](https://brave.com/blog/search-api-agentic-payments/){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent（智能体）：不只是聊天回答，而是能自己规划步骤、调用工具、完成多环节任务的 AI 程序
- **知识点**：Function Calling（函数调用）：AI 判断&#x27;现在该调用哪个外部 API&#x27;的能力，比如识别&#x27;我要买服务器&#x27;→调用 Stripe 支付接口
- **知识点**：RAG（检索增强生成）：虽然本文未直接提及，但这类商业 Agent 通常需要实时查库存、查广告政策，把外部信息&#x27;喂&#x27;给 AI 再生成决策，避免胡说
- **知识点**：Agent：不只是问 AI 问题，而是让 AI 能自主调用工具、做多步决策的系统
- **动手练习**：去 replit.com 免费注册，用一句话让 Replit Agent 做一个&#x27;收集用户邮箱的落地页&#x27;，部署上线后，尝试在设置里找到 Stripe 连接入口（无需真绑定），体验&#x27;从想法到可收钱的产品&#x27;全流程，记录 Agent 每一步问了什么问题、做了什么决定。
- **动手练习**：用任意 LLM（如 GPT-4）尝试：① 给它一段模拟的产品数据，让它分析并提出一个功能建议；② 要求它输出一段可运行的 Python 代码来实现该功能；③ 手动运行代码，把结果再丢给 LLM 让它评估效果是否达标。全程用自然语言对话完成，体会&#x27;观察→行动→验证&#x27;的 Agent 思路。

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
