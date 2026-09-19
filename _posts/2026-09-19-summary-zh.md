---
layout: default
title: "AI产品情报 · 2026-09-19"
date: 2026-09-19
lang: zh
---

**日期**：2026-09-19　 **更新时间**：2026-09-19 12:37 北京时间

> 从 109 条内容中筛选出 6 条重要资讯。

> 今日高质量增量有限，因此未使用低质量内容补足数量。

<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Anthropic 的 Thariq Shihipar 宣布 Claude Code 2.1.277 起支持 AGENTS.md，并基于即将推出的 mods 机制实现，源码已公开。
- TypeSafe AI 的 Jev 在 Vercel AI Gateway 上线 24 小时内成为采用最快模型，近 13% 付费团队使用，它专门做软件内的结构化决策并返回带概率的类型化答案。
- AEXGrid 在 Product Hunt 发布，主打从任何地方协调 AI agents，适合观察多 agent 协作类产品的早期形态。
- Wombo 在 Product Hunt 发布 AI 游戏工作室，帮开发者生成 2D 图形、音效和 sfx，适合观察 AI 在游戏素材生产中的落地方式。
- 两位 Grok Bot 设计师在播客里讲他们怎么用 AI agent 做个人网站和产品原型，对想动手做产品的人有直接参考价值。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Claude Code 新增 AGENTS.md 支持：用 mods 机制自定义项目指令](https://simonwillison.net/2026/Sep/18/thariq-shihipar/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Anthropic 的 Thariq Shihipar 宣布 Claude Code 2.1.277 起支持 AGENTS.md，并基于即将推出的 mods 机制实现，源码已公开。

**评分**：7.5 / 10　 **证据**：一手信息

**产品 / 团队**：Claude Code / Simon Willison

**目标用户**：使用 Claude Code 终端工具的开发者，尤其是需要团队协作统一 AI 编码规范的人

**它是什么**：Anthropic 官方为终端编码工具 Claude Code 新增的配置文件支持，让 AI 编码助手能读取项目级的 AGENTS.md 文件来理解项目规则。

**用户问题**：以前只能用 CLAUDE.md 给 AI 写项目指令，但团队想换用更通用的 AGENTS.md 标准（跨工具共享），或者想自定义指令逻辑却受限于硬编码

**使用流程**：
1. 在 Claude Code 2.1.277 及以上版本中，进入项目文件夹
2. 若文件夹里没有 CLAUDE.md，新建一个 AGENTS.md 写入项目规则（如代码风格、测试要求）
3. Claude Code 启动时会自动读取 AGENTS.md 作为项目指令
4. 进阶：以后可通过 mods 机制自己写自定义版本的项目指令逻辑

**AI 在做什么**：读取 AGENTS.md 中的规则，在编码、改代码、跑命令时按这些规则行动

**怎么实现**：未公开

**需要理解的知识点**：
1. AGENTS.md：一种社区推动的通用配置文件，想让不同 AI 编码工具（不只是 Claude）都能读懂同一套项目规则
2. Mod/模块系统：把软件的一部分功能拆成可替换的「插件」，这里 Claude Code 把「读项目指令」这件事做成了可自定义的模块
3. Function Calling（功能调用）：AI 模型不只会聊天，还能按规则调用工具（如读文件、跑命令），项目指令就是给这些工具调用定规矩

**动手练习**：30 分钟练习：①安装/更新 Claude Code 到 2.1.277+（运行 claude update）；②在一个测试项目里删掉 CLAUDE.md（如果有），新建 AGENTS.md 写入「所有函数必须加类型注解，提交前跑 pytest」；③让 Claude Code 写一个新函数，观察它是否遵守规则；④去 GitHub 看 anthropic/claude-code/tree/main/mods/agents-md 的源码，对比你写的 AGENTS.md 是怎么被解析的

**已知限制**：Bedrock、Vertex、Foundry 平台尚未支持此功能；mods 系统的完整自定义能力还未正式发布，目前只有这个内置 mod 可用；AGENTS.md 的具体语法规范未在原文中详细说明

**原始来源**：rss · Simon Willison · 9月19日 03:09 北京时间 · [打开原文](https://simonwillison.net/2026/Sep/18/thariq-shihipar/){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Jev 成为 Vercel AI Gateway 史上采用速度最快的模型](https://vercel.com/blog/ai-gateway-jev-model-launch){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：TypeSafe AI 的 Jev 在 Vercel AI Gateway 上线 24 小时内成为采用最快模型，近 13% 付费团队使用，它专门做软件内的结构化决策并返回带概率的类型化答案。

**评分**：7.5 / 10　 **证据**：一手信息

**产品 / 团队**：Jev / Eric Dodds

**目标用户**：需要让 AI 在软件里做快速判断的开发者，比如决定 Agent 下一步调用什么工具、要不要拦截风险操作、是否让人工复核等场景。

**它是什么**：Jev 是一个专门做&quot;结构化决策&quot;的 AI 模型，不返回长文本，而是返回代码能直接用的类型化结果（比如选 A 还是选 B、打几分、true/false），并附带概率值。

**用户问题**：通用大模型输出的是自然语言，开发者得自己解析、校验、担心格式不对；而且大模型做简单判断又慢又贵，像用大炮打蚊子。

**使用流程**：
1. 开发者通过 Vercel AI Gateway 接入 Jev，传入上下文和一组问题
2. Jev 并行评估这些问题，返回类型化的选择、分数或布尔值 + 概率
3. 代码直接消费这些结构化结果，驱动后续逻辑（如调用工具、继续工作流、人工复核）

**AI 在做什么**：AI 负责把&quot;模糊的业务场景&quot;转化为&quot;确定性的结构化决策&quot;，替代开发者自己写规则引擎或调用大模型做简单判断。

**怎么实现**：Jev 本质上是一个&quot;概率分类器&quot;，针对软件里常见的决策点预做了优化。它跳过生成自然语言的步骤，直接输出定义好的数据类型（类似 API 的响应格式），所以比通用 LLM 快几十倍、便宜几百倍。可以把它理解为：不是让 AI &quot;写作文&quot;，而是让 AI &quot;做选择题并给出把握有多大&quot;。

**需要理解的知识点**：
1. Function Calling（函数调用）：让 AI 输出结构化数据而不是自由文本，方便代码直接处理
2. Agent（智能体）：能自主决定下一步动作的 AI 系统，Jev 专门负责 Agent 的&quot;决策大脑&quot;环节
3. Embedding（嵌入）：未直接涉及，但理解 LLM 的不同输出形态有助于选型

**动手练习**：30 分钟练习：在 Vercel AI Gateway 注册账号，找到 Jev 的试用入口，用 curl 或 Postman 发一个请求，让它帮你做一个简单判断（比如&quot;这条用户评论是咨询、投诉还是广告？&quot;），观察返回的 JSON 格式和概率字段，对比你调用 GPT-4 做同样任务的速度和成本。

**已知限制**：TypeSafe AI 自称的&quot;194 倍更快、445 倍更便宜&quot;是厂商自己跑的工作流评测，未公开第三方复现方法；24 小时采用率数据来自 Vercel 官方，但&quot;付费团队&quot;的具体定义和样本量未公开；早期采用热度能否持续仍是未知数。

**原始来源**：rss · Eric Dodds · 9月18日 15:00 北京时间 · [打开原文](https://vercel.com/blog/ai-gateway-jev-model-launch){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [🎙️ How I AI: How two SpaceXAI designers use Grok Bot to do their jobs](https://www.lennysnewsletter.com/p/how-i-ai-how-two-spacexai-designers){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

两位 Grok Bot 设计师在播客里讲他们怎么用 AI agent 做个人网站和产品原型，对想动手做产品的人有直接参考价值。

**对做产品的启发**：Lenny Newsletter 的 How I AI 栏目，由 Grok Bot 设计师讲如何用 AI agent 搭建个人站点与产品原型，属于可迁移的构建者实践；但正文仅含节目预告与要点列表，缺少完整方法与证据，故未达 8 分。

**继续验证**：等完整节目/文字稿发布后，拆解其无 CMS、无 Figma 的具体工作流。

**原始来源**：newsletter · Lenny Rachitsky · 9月14日 23:03 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-how-two-spacexai-designers){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

_今天没有达到标准的一线构建实践；不会用泛泛观点补位。_

<a id="model-company-news"></a>
## 模型公司动态

### [WebMCP support now available in mcp-handler](https://vercel.com/changelog/webmcp-mcp-handler){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Vercel 的 mcp-handler 2.2.0 实验性支持 WebMCP，加一个 script 标签就能把已有 MCP 工具暴露给浏览器内 Agent，并以登录用户身份代理调用。

**对做产品的启发**：Vercel 官方为 mcp-handler 加入 WebMCP 实验支持，让网页工具可被浏览器内 Agent 调用，是可直接上手的 Agent 产品能力增量。

**继续验证**：关注 WebMCP 标准推进情况，以及浏览器端 Agent 调用工具的实际体验。

**原始来源**：rss · Boris Besemer · 9月19日 02:00 北京时间 · [打开原文](https://vercel.com/changelog/webmcp-mcp-handler){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [AEXGrid](https://www.producthunt.com/products/aexgrid){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

AEXGrid 在 Product Hunt 发布，主打从任何地方协调 AI agents，适合观察多 agent 协作类产品的早期形态。

**对做产品的启发**：Product Hunt 上的新产品发布，定位为跨地点协调 AI agents，属于可验证的 AI 产品案例，但输入只有一句话描述，缺少用户反馈与具体使用流程，给 7.2。

**继续验证**：查看产品页与讨论区，确认它如何调度 agent、面向什么用户、是否有真实使用反馈。

**原始来源**：rss · ivan delicio · 9月18日 13:42 北京时间 · [打开原文](https://www.producthunt.com/products/aexgrid){:target="_blank" rel="noopener noreferrer"}

### [Wombo](https://www.producthunt.com/products/wombo-the-ai-game-studio){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Wombo 在 Product Hunt 发布 AI 游戏工作室，帮开发者生成 2D 图形、音效和 sfx，适合观察 AI 在游戏素材生产中的落地方式。

**对做产品的启发**：Product Hunt 上的 AI 游戏素材生成产品，面向 2D 图形、音效和 sfx，属于垂直 AI 产品案例，但输入信息过少，缺少用户反馈与工作流细节，给 7.0。

**继续验证**：查看产品页，确认生成质量、定价和游戏开发者的真实使用反馈。

**原始来源**：rss · Armin Catovic · 9月18日 13:40 北京时间 · [打开原文](https://www.producthunt.com/products/wombo-the-ai-game-studio){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：AGENTS.md：一种社区推动的通用配置文件，想让不同 AI 编码工具（不只是 Claude）都能读懂同一套项目规则
- **知识点**：Mod/模块系统：把软件的一部分功能拆成可替换的「插件」，这里 Claude Code 把「读项目指令」这件事做成了可自定义的模块
- **知识点**：Function Calling（功能调用）：AI 模型不只会聊天，还能按规则调用工具（如读文件、跑命令），项目指令就是给这些工具调用定规矩
- **知识点**：Function Calling（函数调用）：让 AI 输出结构化数据而不是自由文本，方便代码直接处理
- **动手练习**：30 分钟练习：①安装/更新 Claude Code 到 2.1.277+（运行 claude update）；②在一个测试项目里删掉 CLAUDE.md（如果有），新建 AGENTS.md 写入「所有函数必须加类型注解，提交前跑 pytest」；③让 Claude Code 写一个新函数，观察它是否遵守规则；④去 GitHub 看 anthropic/claude-code/tree/main/mods/agents-md 的源码，对比你写的 AGENTS.md 是怎么被解析的
- **动手练习**：30 分钟练习：在 Vercel AI Gateway 注册账号，找到 Jev 的试用入口，用 curl 或 Postman 发一个请求，让它帮你做一个简单判断（比如&quot;这条用户评论是咨询、投诉还是广告？&quot;），观察返回的 JSON 格式和概率字段，对比你调用 GPT-4 做同样任务的速度和成本。

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
