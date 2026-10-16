---
layout: default
title: "AI产品情报 · 2026-10-16"
date: 2026-10-16
lang: zh
---

**日期**：2026-10-16　 **更新时间**：2026-10-16 12:31 北京时间

> 从 168 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Bluesky 的 Attie 现在能让用户做游戏、投票、仪表盘等小应用并作为网站分享，CEO 在采访中解释了这一方向，值得看 AI 生成内容如何与社交分发结合。
- ChatGPT 的 Chrome 扩展现在能读取你已打开的浏览器标签页，让 AI 直接基于当前网页上下文回答，值得看它怎么解决“让 AI 看到你正在看什么”的问题。
- Vercel 在 Ship 2026 上发布面向智能体的基础设施，让 coding agent 能直接部署软件并运行自建 agent，值得看部署层如何为 AI 产品重新设计。
- Simon Willison 用 Claude Code 做出一个靠手机麦克风“啾啾”声传数据的双人 Pong 游戏，展示了如何用 AI 把一个奇怪想法快速变成可玩 Demo。
- Meta 的 AI Agent Muse 设计负责人 Alex Cornell 公开讲了他怎么把 Muse 做成像发消息而不是 AI 应用，以及三层状态显示和生成式界面背后的设计取舍。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Bluesky 的 AI 工具 Attie 让用户做小游戏和 App，直接当网站分享到社交圈](https://www.theverge.com/tech/1012374/bluesky-ai-attie-small-social-games-apps){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Bluesky 的 Attie 现在能让用户做游戏、投票、仪表盘等小应用并作为网站分享，CEO 在采访中解释了这一方向，值得看 AI 生成内容如何与社交分发结合。

**评分**：8.0 / 10　 **证据**：媒体报道

**产品 / 团队**：Attie / Jay Peters

**目标用户**：Bluesky 普通用户，尤其是没有编程基础、想快速做互动内容的人

**它是什么**：Bluesky 平台内置的 AI 工具，最初用来生成个性化信息流（feed），现在扩展为让用户用自然语言生成小游戏、投票、仪表盘等轻量应用，并生成独立网站链接供社交分享。

**用户问题**：普通人想做小游戏、投票或数据看板，但不懂写代码，也不知道怎么部署成可分享的网页

**使用流程**：
1. 在 Bluesky 里打开 Attie，用日常语言描述你想做什么（比如&#x27;做一个猜拳游戏&#x27;）
2. AI 生成可运行的轻量应用，并自动部署成一个独立网站
3. 把生成的网站链接发到 Bluesky 或其他社交平台，别人点开就能用

**AI 在做什么**：把用户的自然语言描述转成可运行的前端代码（HTML/CSS/JS 等），并自动完成部署

**怎么实现**：本质上属于&#x27;vibe coding&#x27;——用户只描述&#x27;感觉/效果&#x27;，AI 负责写代码和上线。类似让 ChatGPT 写个网页，但 Attie 把&#x27;生成→部署→分享&#x27;整条链路包圆了，而且和 Bluesky 社交账号打通。

**需要理解的知识点**：
1. vibe coding：不用学编程语法，用大白话描述需求，AI 帮你写代码
2. Function Calling（功能调用）：AI 不只是聊天，还能触发&#x27;生成网页&#x27;&#x27;部署网站&#x27;等外部工具
3. 社交分发：AI 生成的内容不再是孤岛，而是通过链接在社交网络里传播

**动手练习**：打开 Attie（需 Bluesky 账号），尝试用一句话生成一个&#x27;随机决定今天吃什么&#x27;的小工具，分享到 Bluesky 观察互动数据；如果暂时没有权限，可用 Claude/GPT 生成同样功能的 HTML 文件，手动托管到 GitHub Pages 对比体验差异

**已知限制**：未公开具体技术栈（是否用特定前端框架）、生成应用的复杂度上限、是否支持自定义域名、免费额度与付费模式、CEO 采访中的&#x27;small apps&#x27;具体指多大规模

**原始来源**：rss · Jay Peters · 10月16日 03:57 北京时间 · [打开原文](https://www.theverge.com/tech/1012374/bluesky-ai-attie-small-social-games-apps){:target="_blank" rel="noopener noreferrer"}

---
### 2. [ChatGPT Chrome 扩展现在能读取你已打开的标签页](https://www.theverge.com/ai-artificial-intelligence/1012510/openai-chatgpt-google-chrome-tabs){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：ChatGPT 的 Chrome 扩展现在能读取你已打开的浏览器标签页，让 AI 直接基于当前网页上下文回答，值得看它怎么解决“让 AI 看到你正在看什么”的问题。

**评分**：7.6 / 10　 **证据**：媒体报道

**产品 / 团队**：ChatGPT Chrome extension / Stevie Bonifield

**目标用户**：已在 Chrome（及 Edge、Brave、Opera、Vivaldi）安装 ChatGPT 扩展、并在桌面端或网页端使用 ChatGPT 的用户

**它是什么**：OpenAI 给 ChatGPT 官方 Chrome 扩展加了新功能，让 ChatGPT 能在你授权后读取浏览器里已打开的标签页内容，用来回答问题时参考当前网页上下文

**用户问题**：以前问 ChatGPT 关于当前网页的问题时，需要手动复制粘贴网页内容或链接，AI 看不到你浏览器里已经打开的其他标签页，上下文断层

**使用流程**：
1. 在 Chrome 安装/更新 ChatGPT 官方扩展
2. 在 ChatGPT 网页或桌面端输入问题时，@ 提及 Chrome（tag Chrome）
3. 扩展获取你已打开标签页的上下文
4. ChatGPT 基于这些网页内容回答你的问题

**AI 在做什么**：接收用户问题 + 浏览器标签页上下文，生成基于当前网页内容的回答；也可在已登录的网站上执行操作（如 LinkedIn、Gmail 等）

**怎么实现**：浏览器扩展作为&#x27;桥梁&#x27;：它常驻在浏览器后台，当被 ChatGPT 调用时，读取当前打开标签页的标题和内容，打包成上下文传给 AI。这相当于给 LLM 装了一双能看浏览器的&#x27;眼睛&#x27;，解决了 AI 和用户屏幕之间的信息断层

**需要理解的知识点**：
1. 上下文（Context）：LLM 回答问题时能参考的信息范围，越多相关上下文，回答越准
2. RAG（检索增强生成）：让 AI 不瞎编，先从外部来源（这里是你的浏览器标签）拉取信息，再基于这些信息回答
3. Function Calling（函数调用）：LLM 判断&#x27;现在需要调用浏览器扩展来获取标签页&#x27;，而不是直接瞎猜答案

**动手练习**：30 分钟练习：安装 ChatGPT Chrome 扩展，打开 3 个不同网页（如一篇新闻、一个 GitHub 仓库、一封 Gmail），在 ChatGPT 桌面端输入&#x27;@Chrome 总结这三个页面的共同点&#x27;，观察 AI 是否能正确引用各页内容；然后尝试在已登录的网站上让它执行简单操作（如&#x27;帮我在 LinkedIn 搜索某人&#x27;），记录哪些操作成功、哪些需要额外授权

**已知限制**：具体支持哪些浏览器版本未完全公开；扩展读取标签页时是否需要每次手动确认授权机制未公开；Opera 是否支持 side chat 功能未明确（官方文档称 Chrome/Edge/Brave/Vivaldi 支持 side chat，Opera 未列入）；&#x27;Atlas browser&#x27;项目已取消，与当前扩展的关系未公开

**原始来源**：rss · Stevie Bonifield · 10月16日 06:43 北京时间 · [打开原文](https://www.theverge.com/ai-artificial-intelligence/1012510/openai-chatgpt-google-chrome-tabs){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [🎙️ How I AI: How Meta designed Muse with Alex Cornell](https://www.lennysnewsletter.com/p/how-i-ai-how-meta-designed-muse-with){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Meta 的 AI Agent Muse 设计负责人 Alex Cornell 公开讲了他怎么把 Muse 做成像发消息而不是 AI 应用，以及三层状态显示和生成式界面背后的设计取舍。

**对做产品的启发**：Meta 消费级 AI Agent Muse 的设计负责人 Alex Cornell 在 Lenny 播客中公开讲解产品设计思路，包括为什么做成消息形态、三层状态显示、生成式 UI 等，属于构建者一手实践分享，对做 AI 产品的人有直接可迁移的设计经验。

**继续验证**：关注 Muse 后续是否开放更多用户反馈，以及 Alex Cornell 在 Threads 上继续公开的设计细节。

**原始来源**：newsletter · Lenny Rachitsky · 10月12日 23:00 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-how-meta-designed-muse-with){:target="_blank" rel="noopener noreferrer"}

### [Meta’s new ‘Muse Wonder’ model: good for AI agents, bad for design](https://www.lennysnewsletter.com/p/metas-new-muse-wonder-model-good){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Claire Vo 用自建评测集实测 Meta 新模型 Muse Wonder，发现它在 agent 任务上表现好但设计输出差，帮产品经理判断该模型适合做什么。

**对做产品的启发**：Claire Vo 用自建 How I AI bench 对 Meta Muse Wonder 做近 20 项任务实测，覆盖原型、agent 工作流、编码、写作与创意，并给出评分与结论，属于有方法、有反馈的高信噪比一手评测，对产品经理理解模型适用边界有明确迁移价值。

**继续验证**：关注完整评测数据、active focus mode 的真实效果与设计类任务失败原因

**原始来源**：newsletter · Claire Vo · 10月14日 20:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/metas-new-muse-wonder-model-good){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [Chirp Pong](https://simonwillison.net/2026/Oct/15/chirp-pong/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.6/10

Simon Willison 用 Claude Code 做出一个靠手机麦克风“啾啾”声传数据的双人 Pong 游戏，展示了如何用 AI 把一个奇怪想法快速变成可玩 Demo。

**对做产品的启发**：Simon Willison 用 Claude Code 做出一个用手机麦克风音频传输游戏状态的双人 Pong 实验，附可访问工具链接和完整提示词，是构建者一手实践，能让初学者看到“一个想法如何用 AI 变成可玩 Demo”。

**继续验证**：看该工具的实际可玩性与代码是否开源，以及类似音频联网玩法的延伸。

**原始来源**：rss · Simon Willison · 10月16日 03:47 北京时间 · [打开原文](https://simonwillison.net/2026/Oct/15/chirp-pong/){:target="_blank" rel="noopener noreferrer"}

### [What’s new in Microsoft Foundry \| September 2026](https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-september-2026/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

微软 Foundry 发布九月更新，新增 Routines、Tool Search、Model Router 等能力，并用两个 agent 协作把公开发布自动整理成开发者更新日志，值得看的是平台级 agent 工作流怎么搭。

**对做产品的启发**：Microsoft Foundry 官方月度更新，介绍新模型、Routines、Tool Search、Model Router 与 Insights，并用双 agent 工作流演示把公开发布转成开发者 changelog，属于可迁移的构建实践与平台能力更新。

**继续验证**：关注 Routines 与 Model Router 的实际用法、定价与文档

**原始来源**：rss · Nick Brady · 10月16日 10:04 北京时间 · [打开原文](https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-september-2026/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude Discovers Novel Enzyme System](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Anthropic 官方称 Claude 发现了一种新的酶系统，展示大模型在生物科学发现中的实际用途，值得关注 AI 在医药研发场景的产品化可能。

**对做产品的启发**：Anthropic 官方发布 Claude 发现新酶系统的研究更新，属模型公司一手动态，且展示了模型在科学发现这一新场景中的实际能力，对探索垂直 AI 产品（尤其医药/生物）有直接启发。但正文仅有占位描述，缺少可验证细节与用户使用路径，故未进入 9 分区间。

**继续验证**：等待官方补充实验细节、可复现方法或合作方信息，判断是否可迁移为垂直科研产品。

**原始来源**：public\_web · Anthropic News · 10月13日 08:18 北京时间 · [打开原文](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"}

### [Introducing Vercel Drives: persistent storage for agents](https://vercel.com/blog/introducing-vercel-drives-persistent-storage-for-agents){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

Vercel 发布 Drives，让 AI Agent 换运行环境后还能接着用之前的文件，不用从头再来。

**对做产品的启发**：Vercel 正式发布 Vercel Drives，为 Agent 提供跨执行环境的持久化文件存储，解决 Agent 换环境后文件丢失的问题。属于官方产品发布，有明确技术方案和代码示例，对构建 Agent 产品有直接可迁移价值，但偏基础设施，故 7.6。

**继续验证**：关注 Drives 在真实 Agent 产品中的使用案例、定价和与竞品（如 E2B、Modal）的对比。

**原始来源**：rss · Elisabeth Rülke · 10月15日 15:00 北京时间 · [打开原文](https://vercel.com/blog/introducing-vercel-drives-persistent-storage-for-agents){:target="_blank" rel="noopener noreferrer"}

### [Meta launches an open-weight AI model that runs on Macs](https://techcrunch.com/2026/10/15/meta-launches-an-open-weight-model-that-runs-on-macs/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Meta 与 Apple 合作发布开放权重模型 Muse Spark Open，可在 Apple 芯片 Mac 上本地运行，让初学者能直接体验本地 AI 产品形态。

**对做产品的启发**：Meta 发布可在 Apple Silicon 本地运行的开放权重模型，属于新模型能力落地，对探索本地 AI 产品有直接参考价值；但报道来自 TechCrunch，非官方一手，且缺少模型参数、性能、许可等关键细节，因此未进入 8 分以上区间。

**继续验证**：值得追踪：等待 Meta 官方模型卡、许可条款、参数规模和实际 Demo 反馈。

**原始来源**：rss · Lucas Ropek · 10月16日 04:04 北京时间 · [打开原文](https://techcrunch.com/2026/10/15/meta-launches-an-open-weight-model-that-runs-on-macs/){:target="_blank" rel="noopener noreferrer"}

### [openai/codex released rust-v0.163.0](https://github.com/openai/codex/releases/tag/rust-v0.163.0){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

OpenAI Codex 发布 v0.163.0，新增配置搜索、响应中追加指令、并行只读工具等功能，并默认开启 Daybreak。

**对做产品的启发**：OpenAI Codex 正式版 v0.163.0 发布，包含多项新功能：/config 搜索、响应中追加指令、leader key、后台服务重启、并行只读工具、Daybreak 默认开启等。属于官方 Release，有明确功能增量，对使用 Codex 的开发者有直接价值，但属于常规迭代，故 7.2。

**继续验证**：关注 Daybreak 默认开启后的实际体验变化，以及并行工具调用对 Agent 效率的提升。

**原始来源**：github · github-actions\[bot\] · 10月16日 05:30 北京时间 · [打开原文](https://github.com/openai/codex/releases/tag/rust-v0.163.0){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Vercel Ship 2026 recap](https://vercel.com/blog/vercel-ship-2026-recap){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Vercel 在 Ship 2026 上发布面向智能体的基础设施，让 coding agent 能直接部署软件并运行自建 agent，值得看部署层如何为 AI 产品重新设计。

**对做产品的启发**：Vercel 官方发布面向智能体的基础设施方向，含 200+ CLI 命令供 agent 操作平台等具体能力，对做 AI 产品的人理解部署与 agent 基础设施有参考；但整体是大会宣传稿，营销成分明显，需扣分。

**继续验证**：看这些 agent 基础设施的实际文档、定价与真实用户案例。

**原始来源**：rss · Amelia Charles · 10月16日 00:00 北京时间 · [打开原文](https://vercel.com/blog/vercel-ship-2026-recap){:target="_blank" rel="noopener noreferrer"}

### [Open weight takes 71.5% of tokens and 23% of spend](https://vercel.com/blog/ai-gateway-production-index-october-2026){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.4/10

Vercel 的 AI Gateway 月度报告显示开源权重模型已占其网关七成以上 token 但只占约四分之一支出，值得看企业实际用模型的结构变化。

**对做产品的启发**：Vercel 基于真实网关流量发布月度生产指数，给出开源权重模型占 token 71.5%、占支出 23% 等可验证数据，属于高信噪比行业观察，能帮助判断模型选型趋势。

**继续验证**：跟踪后续月份开源模型支出占比是否继续上升及中国模型使用变化。

**原始来源**：rss · Harpreet Arora · 10月15日 15:00 北京时间 · [打开原文](https://vercel.com/blog/ai-gateway-production-index-october-2026){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：vibe coding：不用学编程语法，用大白话描述需求，AI 帮你写代码
- **知识点**：Function Calling（功能调用）：AI 不只是聊天，还能触发&#x27;生成网页&#x27;&#x27;部署网站&#x27;等外部工具
- **知识点**：社交分发：AI 生成的内容不再是孤岛，而是通过链接在社交网络里传播
- **知识点**：上下文（Context）：LLM 回答问题时能参考的信息范围，越多相关上下文，回答越准
- **动手练习**：打开 Attie（需 Bluesky 账号），尝试用一句话生成一个&#x27;随机决定今天吃什么&#x27;的小工具，分享到 Bluesky 观察互动数据；如果暂时没有权限，可用 Claude/GPT 生成同样功能的 HTML 文件，手动托管到 GitHub Pages 对比体验差异
- **动手练习**：30 分钟练习：安装 ChatGPT Chrome 扩展，打开 3 个不同网页（如一篇新闻、一个 GitHub 仓库、一封 Gmail），在 ChatGPT 桌面端输入&#x27;@Chrome 总结这三个页面的共同点&#x27;，观察 AI 是否能正确引用各页内容；然后尝试在已登录的网站上让它执行简单操作（如&#x27;帮我在 LinkedIn 搜索某人&#x27;），记录哪些操作成功、哪些需要额外授权

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
