---
layout: default
title: "AI产品情报 · 2026-10-29"
date: 2026-10-29
lang: zh
---

**日期**：2026-10-29　 **更新时间**：2026-10-29 13:46 北京时间

> 从 127 条内容中筛选出 9 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Claire Vo 用九个真实任务（Slack 回复、修 bug、Figma 缩略图、收件箱整理等）横向评测 Grok Bot、Dot、Muse 和 Claude Duet 四款个人 Agent，并给出工作与生活场景的信任建议；适合看 Agent 产品在真实任务中的表现差异。
- Legora 利用 OpenAI 模型、ChatGPT 和 Codex 打造法律工作 Agent 操作系统，加速合同分析等流程，让律师专注高价值工作；是法律垂直 AI 产品的一手案例。
- GitHub Copilot 推出 Fusion 功能，自动编排 Anthropic 和 OpenAI 模型来平衡性能与成本；值得看多模型路由如何影响产品体验和成本结构。
- 微软在 Foundry Agent Service 中推出 Copilot harness，把模型推理所需的上下文、工具和执行环境打包成统一 Agent 运行框架，值得看它如何降低构建 Agent 的门槛。
- OpenAI 与 ServiceNow 扩大合作，把 OpenAI 模型和 Agent 引入 ServiceNow 工作流，同时让 ServiceNow 能力进入 ChatGPT 和 Codex；可观察企业软件与 AI Agent 的融合路径。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Grok Bot、Dot、Muse、Claude Duet 四款个人 Agent 实战横评：谁更能打？](https://www.lennysnewsletter.com/p/grok-vs-dot-vs-muse-vs-claude-duet){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Claire Vo 用九个真实任务（Slack 回复、修 bug、Figma 缩略图、收件箱整理等）横向评测 Grok Bot、Dot、Muse 和 Claude Duet 四款个人 Agent，并给出工作与生活场景的信任建议；适合看 Agent 产品在真实任务中的表现差异。

**评分**：8.2 / 10　 **证据**：已核验

**产品 / 团队**：Grok Bot / Dot / Meta Muse / Claude Duet / Claire Vo

**目标用户**：想找一个能代理日常事务的 AI 助手的个人用户，尤其是产品经理、开发者、需要兼顾工作的家长

**它是什么**：AI 产品经理 Claire Vo 设计的个人 Agent 基准测试，用 9 个真实任务对比 Grok Bot、Dot、Muse、Claude Duet 的实际表现，并给出工作/生活场景的信任建议。

**用户问题**：市面上个人 Agent 太多，宣传都很强，但真放到写 Slack 回复、修 bug、做 Figma 图、整理收件箱等具体任务里，表现参差不齐，用户不知道怎么选、敢不敢信

**使用流程**：
1. 用户给 Agent 一个自然语言任务指令（如&#x27;帮我草拟 Slack 回复&#x27;、&#x27;从 Sentry 报错修 bug&#x27;）
2. Agent 自主调用工具（浏览器、代码执行、Figma API 等）完成任务
3. Claire Vo 用另一套 AI（Claude 操作 Dot，Codex 操作其余）实时评分
4. 对比各 Agent 的完成质量、速度、可靠性，得出最终分数板

**AI 在做什么**：Agent 是执行者：理解任务→规划步骤→调用外部工具→输出结果；评分 AI 是裁判：按预设标准给每个任务打分

**怎么实现**：核心是&#x27;计算机使用（Computer Use）&#x27;——让 AI 能直接操控电脑界面或 API，像人一样打开软件、读报错、写代码、做设计。评测者用另一套 AI 当&#x27;监考&#x27;，避免人为主观打分。

**需要理解的知识点**：
1. Agent（智能体）：不只是聊天，而是能自主规划、调用工具完成多步骤任务的 AI 系统
2. Computer Use：让 AI 像人一样看屏幕、点鼠标、输文字，是 Agent 落地的关键技术之一
3. 基准测试（Benchmark）：用固定任务集横向对比产品，比看宣传文案更能反映真实能力

**动手练习**：选一个你常用的 Agent（如 Claude、ChatGPT 或 Grok），给它同一个复杂任务（例如&#x27;整理我本周邮件并列出待办&#x27;），记录它实际做了什么、哪里卡壳、结果是否可用，对比官方宣传的能力描述

**已知限制**：评测由 Claire Vo 个人设计任务和评分标准，非第三方独立机构；9 个任务覆盖有限，未公开各 Agent 具体版本号和运行日期；Codex 作为评分者可能存在偏向性未公开

**原始来源**：newsletter · Claire Vo · 10月28日 20:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/grok-vs-dot-vs-muse-vs-claude-duet){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Legora：用 OpenAI 模型打造法律工作的 Agent 操作系统](https://openai.com/index/legora){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Legora 利用 OpenAI 模型、ChatGPT 和 Codex 打造法律工作 Agent 操作系统，加速合同分析等流程，让律师专注高价值工作；是法律垂直 AI 产品的一手案例。

**评分**：8.0 / 10　 **证据**：一手信息

**产品 / 团队**：Legora / OpenAI News

**目标用户**：律师事务所律师、企业法务团队（in-house legal）

**它是什么**：一个面向律师和法律团队的 AI 协作平台，把合同审查、法律研究、文书起草等重复工作交给 AI Agent 自动处理。

**用户问题**：律师大量时间耗在合同逐条审阅、法律检索、文书格式调整等重复性事务上，挤占了高价值策略分析和客户沟通的时间。

**使用流程**：
1. 上传合同或法律文档到 Legora 平台
2. AI Agent 自动分析内容、标注风险条款、提取关键信息
3. 律师审阅 AI 生成的分析结果，做最终判断和修改
4. 直接导出修订版文档或生成新文书

**AI 在做什么**：AI 负责合同分析、法律研究、文书起草的初稿生成；律师保留最终决策权。

**怎么实现**：底层调用 OpenAI 的 GPT 模型做语言理解和生成，用 Codex 处理需要精确逻辑或代码化的规则匹配，再把多个任务串成能自动流转的 Agent 工作流——相当于给法律工作配了一个能自己跑任务的智能助理。

**需要理解的知识点**：
1. Agent：能自主分解任务、调用工具、按步骤执行的 AI，不只是单次问答
2. 垂直行业 AI：把通用大模型能力封装进特定职业的工作流，解决该领域特有的重复劳动
3. 人机协作：AI 做初筛和草稿，人类做把关和决策，不是完全替代

**动手练习**：用 ChatGPT 上传一份租房合同，让 AI 标出对你不利的条款并解释原因，然后对比它漏掉了哪些你自己能发现的风险点——体会 AI 辅助审查的边界。

**已知限制**：未公开具体使用哪些 OpenAI 模型版本、Codex 在法律场景中的具体调用方式、定价模式、以及 AI 生成内容的法律责任归属如何界定。

**原始来源**：rss · OpenAI News · 10月28日 17:30 北京时间 · [打开原文](https://openai.com/index/legora){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [Grok Bot、Dot、Muse、Claude Duet 四款个人 Agent 实战横评：谁更能打？](https://www.lennysnewsletter.com/p/grok-vs-dot-vs-muse-vs-claude-duet){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Claire Vo 用九个真实任务（Slack 回复、修 bug、Figma 缩略图、收件箱整理等）横向评测 Grok Bot、Dot、Muse 和 Claude Duet 四款个人 Agent，并给出工作与生活场景的信任建议；适合看 Agent 产品在真实任务中的表现差异。

**对做产品的启发**：Claire Vo 用九个真实任务横向评测 Grok Bot、Dot、Muse、Claude Duet 四款个人 Agent，有具体任务、操作方式和评分，属于高信噪比产品实践对比，对 AI 产品经理理解 Agent 落地很有价值。

**继续验证**：关注评测方法细节、各 Agent 的失败案例和后续迭代。

**原始来源**：newsletter · Claire Vo · 10月28日 20:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/grok-vs-dot-vs-muse-vs-claude-duet){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [The October inflection point for vibe game development](https://simonwillison.net/2026/Oct/28/vibe-game-development/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Simon Willison 认为 2026 年 10 月是 vibe coding 游戏开发的拐点，并列举多个 AI 生成游戏案例；展示 AI 如何降低游戏创作门槛。

**对做产品的启发**：Simon Willison 基于多个可玩 Demo 提出 2026 年 10 月是 vibe coding 游戏开发拐点，列举具体游戏案例，属于构建者一手观察，能帮助初学者理解 AI 在游戏开发中的作用，但部分链接未展开，故给 8.2 分。

**继续验证**：关注文中列举游戏的用户反馈和可玩性，以及后续更多案例。

**原始来源**：rss · Simon Willison · 10月28日 21:55 北京时间 · [打开原文](https://simonwillison.net/2026/Oct/28/vibe-game-development/){:target="_blank" rel="noopener noreferrer"}

### [Why Agents Love Supabase](https://latent.space/p/supabase/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Latent Space 播客邀请 Supabase 创始人谈为 AI 智能体构建后端；帮助理解智能体产品的基础设施选择。

**对做产品的启发**：Latent Space 播客讨论 Supabase 如何成为 AI 智能体的后端，涉及构建者一手经验，对理解 AI 产品基础设施有迁移价值，但仅有标题和简短描述，缺乏详细内容，故给 7.8 分。

**继续验证**：收听播客全文，关注 Supabase 在智能体场景的具体功能和案例。

**原始来源**：rss · swyx .ai · 10月29日 03:48 北京时间 · [打开原文](https://latent.space/p/supabase/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Google launches Gemini 4 Carbon with a ‘significant leap’ in cybersecurity](https://www.theverge.com/tech/1021339/google-gemini-4-carbon-cybersecurity-frontier){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Google 发布 Gemini 4 Carbon 模型，称在编码、智能体任务和网络安全上有显著提升；对关注新模型能力如何催生产品的人值得留意。

**对做产品的启发**：Google 发布新前沿模型 Gemini 4 Carbon，宣称在编码、智能体任务和网络安全上有显著提升，并引用基准排名。属于模型公司能力动态，但报道来自媒体转述，缺乏一手细节和产品体验证据，对产品经理的直接迁移价值有限，故给 7.5 分。

**继续验证**：关注官方公告、模型卡、API 定价及实际产品集成案例。

**原始来源**：rss · Emma Roth · 10月29日 04:03 北京时间 · [打开原文](https://www.theverge.com/tech/1021339/google-gemini-4-carbon-cybersecurity-frontier){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Github Copilot Fusion Orchestrates Anthropic And Openai Models To Balance Performance And Cost](https://artificialanalysis.ai/articles/github-copilot-fusion-orchestrates-anthropic-and-openai-models-to-balance-performance-and-cost){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

GitHub Copilot 推出 Fusion 功能，自动编排 Anthropic 和 OpenAI 模型来平衡性能与成本；值得看多模型路由如何影响产品体验和成本结构。

**对做产品的启发**：GitHub Copilot 融合编排 Anthropic 与 OpenAI 模型以平衡性能与成本，属于产品级模型路由实践，对 AI 产品经理有可迁移的架构思路，但来源为第三方分析。

**继续验证**：观察 Fusion 的实际用户反馈、定价变化和路由策略细节。

**原始来源**：public\_web · Artificial Analysis · 10月28日 08:00 北京时间 · [打开原文](https://artificialanalysis.ai/articles/github-copilot-fusion-orchestrates-anthropic-and-openai-models-to-balance-performance-and-cost){:target="_blank" rel="noopener noreferrer"}

### [Introducing the Microsoft Copilot harness in Foundry Agent Service](https://devblogs.microsoft.com/foundry/microsoft-copilot-harness-in-foundry/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

微软在 Foundry Agent Service 中推出 Copilot harness，把模型推理所需的上下文、工具和执行环境打包成统一 Agent 运行框架，值得看它如何降低构建 Agent 的门槛。

**对做产品的启发**：微软官方发布 Foundry Agent Service 中的 Copilot harness，属于 Agent 执行框架的一手产品更新，能让初学者理解 Agent 需要上下文、工具和执行环境，但正文截断且无用户反馈，给 7.6。

**继续验证**：关注 harness 支持哪些模型、定价和实际开发者反馈。

**原始来源**：rss · Jeff, Viswajeeet Balaji, Anthony Chu · 10月29日 00:45 北京时间 · [打开原文](https://devblogs.microsoft.com/foundry/microsoft-copilot-harness-in-foundry/){:target="_blank" rel="noopener noreferrer"}

### [OpenAI and ServiceNow expand partnership across enterprise workflows](https://openai.com/index/openai-servicenow-partnership-expansion){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

OpenAI 与 ServiceNow 扩大合作，把 OpenAI 模型和 Agent 引入 ServiceNow 工作流，同时让 ServiceNow 能力进入 ChatGPT 和 Codex；可观察企业软件与 AI Agent 的融合路径。

**对做产品的启发**：OpenAI 与 ServiceNow 扩大合作，将模型和 Agent 嵌入企业工作流，属于企业级产品集成动态，对理解 Agent 落地场景有参考，但缺乏具体产品细节和用户反馈。

**继续验证**：关注具体集成功能、定价和客户案例。

**原始来源**：rss · OpenAI News · 10月28日 21:15 北京时间 · [打开原文](https://openai.com/index/openai-servicenow-partnership-expansion){:target="_blank" rel="noopener noreferrer"}

### [Akai is embracing vibe-coded mods with an open-source MPC](https://www.theverge.com/gadgets/1021405/akai-open-source-mpc-sample-key){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Akai 在正式发布前向改装社区开放开源固件的 MPC Sample Key，社区用 vibe coding 做自定义 mod，展示了硬件产品借助 AI 编程社区做生态的早期做法。

**对做产品的启发**：Akai 尚未正式发布 MPC Sample Key，但已向改装社区开放早期设备并采用开源固件，社区用 vibe coding 做 mod，属于有构建过程的一手案例雏形，但产品未正式发布，按 early\_signal 给 7.2。

**继续验证**：关注正式发布后的固件开放程度和社区 mod 质量。

**原始来源**：rss · Terrence O’Brien · 10月29日 05:34 北京时间 · [打开原文](https://www.theverge.com/gadgets/1021405/akai-open-source-mpc-sample-key){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent（智能体）：不只是聊天，而是能自主规划、调用工具完成多步骤任务的 AI 系统
- **知识点**：Computer Use：让 AI 像人一样看屏幕、点鼠标、输文字，是 Agent 落地的关键技术之一
- **知识点**：基准测试（Benchmark）：用固定任务集横向对比产品，比看宣传文案更能反映真实能力
- **知识点**：Agent：能自主分解任务、调用工具、按步骤执行的 AI，不只是单次问答
- **动手练习**：选一个你常用的 Agent（如 Claude、ChatGPT 或 Grok），给它同一个复杂任务（例如&#x27;整理我本周邮件并列出待办&#x27;），记录它实际做了什么、哪里卡壳、结果是否可用，对比官方宣传的能力描述
- **动手练习**：用 ChatGPT 上传一份租房合同，让 AI 标出对你不利的条款并解释原因，然后对比它漏掉了哪些你自己能发现的风险点——体会 AI 辅助审查的边界。

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
