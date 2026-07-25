---
layout: default
title: "AI产品情报 · 2026-07-26"
date: 2026-07-26
lang: zh
---

**日期**：2026-07-26　 **更新时间**：2026-07-26 00:39 北京时间

> 从 107 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- OpenAI 宣布 ChatGPT Work agent 现在可以登录需要认证的网站，用户接管云浏览器登录后 agent 可继续任务，登录状态跨会话保持。
- Claude Code v2.1.219 新增 Opus 5 模型支持、网络沙箱白名单等多项功能。
- OpenAI 宣布 ChatGPT 自定义宠物现在支持分享链接，用户可创建链接让朋友领养宠物。
- OpenAI 在 ChatGPT 中推出个人健康伴侣功能，提供健康相关对话支持。
- OpenComputer 发布托管代理部署服务，简化 AI 代理的部署流程。

<a id="product-teardown"></a>
## 产品拆解

### 1. [ChatGPT Work agent 现在能登录需要账号的网站了](https://twitter.com/OpenAIDevs/status/tweet-2080707685448847418){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：OpenAI 宣布 ChatGPT Work agent 现在可以登录需要认证的网站，用户接管云浏览器登录后 agent 可继续任务，登录状态跨会话保持。

**评分**：8.5 / 10　 **证据**：一手信息

**产品 / 团队**：ChatGPT Work / OpenAI Developers

**目标用户**：企业团队、需要让 AI 处理涉及登录网站的工作流的用户

**它是什么**：OpenAI 给企业团队用的 ChatGPT Work 产品里，AI agent（智能体，能自主执行多步骤任务的 AI）新增了一项能力：可以像真人一样登录需要用户名密码的网站，而且只需登录一次，之后跨会话都能保持登录状态。

**用户问题**：以前 AI agent 遇到需要登录的网站就卡住了，用户要么自己手动操作完再交给 AI，要么干脆用不了这类网站；每次新开对话还得重新登录，很麻烦。

**使用流程**：
1. 用户在 ChatGPT Work 里给 agent 布置任务，agent 遇到需要登录的网站时暂停
2. 用户接管云浏览器，自己输入账号密码完成登录
3. 用户把控制权交还给 agent，agent 继续执行后续任务
4. 下次再用时，登录状态还在，不用重新登录

**AI 在做什么**：agent 负责在登录前后执行主要任务；遇到登录障碍时暂停并通知用户接管；登录完成后自动恢复任务流

**怎么实现**：OpenAI 在云端给每个用户运行了一个浏览器（类似远程控制的 Chrome），用户和 agent 轮流操作这个浏览器。用户登录时，cookie 和登录凭证存在云端，所以下次开新会话还能用。

**需要理解的知识点**：
1. Agent：不只是回答问题，还能自主决定步骤、调用工具、执行多步任务的 AI 系统
2. 云浏览器/远程浏览器：AI 在云端开的真实浏览器，让 AI 能操作网页就像真人一样
3. 会话持久化：把登录状态存下来，打破&#x27;每次对话从零开始&#x27;的限制

**动手练习**：找一个你日常需要登录的网站（比如公司内部系统或某个数据分析平台），手动记录完成一个重复任务需要点击几次、输入什么；然后对比：如果 AI 能自动登录并执行，哪些步骤可以省掉？写下 3 个你最想让 agent 自动化的登录后任务。

**已知限制**：未公开支持哪些具体网站类型（是否支持 SSO、企业内网、两步验证等）；未说明登录凭证的加密存储细节和安全审计情况；未公开该功能是否额外收费或仅限特定套餐。

**原始来源**：twitter · OpenAI Developers · 7月25日 01:32 北京时间 · [打开原文](https://twitter.com/OpenAIDevs/status/tweet-2080707685448847418){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Claude Code v2.1.219：新增 Opus 5 模型支持与网络沙箱白名单](https://github.com/anthropics/claude-code/releases/tag/v2.1.219){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Claude Code v2.1.219 新增 Opus 5 模型支持、网络沙箱白名单等多项功能。

**评分**：8.0 / 10　 **证据**：一手信息

**产品 / 团队**：Claude Code / ashwin-ant

**目标用户**：需要在终端/命令行环境下编写、修改、调试代码的开发者

**它是什么**：Anthropic 出品的命令行 AI 编程助手，能在终端里理解代码库、改文件、跑命令

**用户问题**：开发者想直接用自然语言指挥 AI 改代码、跑测试，但担心 AI 自动执行命令时连到不该连的网络地址，或模型能力不够处理大代码库

**使用流程**：
1. 在终端安装并启动 claude，用自然语言描述需求（如&#x27;给这个项目加登录功能&#x27;）
2. AI 自动分析代码库，必要时用 /add-dir 添加更多目录到上下文
3. AI 提出修改方案，经确认后自动编辑文件、运行命令
4. 开发者检查 git diff，确认无误后提交代码

**AI 在做什么**：理解代码库结构 → 生成修改方案 → 执行文件编辑和终端命令 → 汇报结果

**怎么实现**：把大语言模型包进命令行工具，通过 MCP（Model Context Protocol，一种让 AI 调用外部工具的通用接口）连接文件系统、代码库和外部服务；用沙箱限制 AI 执行命令时的网络访问，白名单机制让管理员预先批准可信域名

**需要理解的知识点**：
1. Context window（上下文窗口）：模型一次能&#x27;看&#x27;多少字，Opus 5 的 1M 约等于能塞进整本《三体》第一部，让 AI 分析大型代码库不丢线索
2. Agent（智能体）：不只是聊天回复，而是能自主决定&#x27;我要先读哪个文件、再改哪行、然后跑测试&#x27;的 AI 系统
3. Function calling（函数调用）：模型不直接生成答案，而是输出结构化指令（如&#x27;调用 read\_file 工具&#x27;），由外部程序执行后再把结果喂回模型

**动手练习**：30 分钟练习：安装 Claude Code，找一个自己的 Python 项目，用 /add-dir 把项目根目录加进去，然后问&#x27;这个项目的依赖结构有什么风险&#x27;，观察它如何分析；接着在设置里打开 sandbox.network.strictAllowlist，尝试让 AI 访问一个未白名单的 URL，看是否被拦截

**已知限制**：Opus 5 的 &#x27;$10/$50 per Mtok&#x27; 具体指输入/输出哪端定价未在 release note 中明示；&#x27;fast mode&#x27; 的具体速度提升幅度未公开；嵌套 subagent 的 depth-3 限制是否会导致复杂任务中的上下文爆炸需用户自行验证

**原始来源**：github · ashwin-ant · 7月25日 01:14 北京时间 · [打开原文](https://github.com/anthropics/claude-code/releases/tag/v2.1.219){:target="_blank" rel="noopener noreferrer"}

---

<a id="how-they-build"></a>
## 他们怎么做

_今天没有达到标准的一线构建实践；不会用泛泛观点补位。_

<a id="model-company-news"></a>
## 模型公司动态

### [Quoting Boris Cherny](https://simonwillison.net/2026/Jul/25/boris-cherny/#atom-everything){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Anthropic 工程师称 Opus 5 是最难被提示注入的模型，安全性显著提升。

**对做产品的启发**：Anthropic 工程师 Boris Cherny 透露 Opus 5 是最难被提示注入的模型，一手信息，高价值。

**继续验证**：关注 Opus 5 安全性的实际验证。

**原始来源**：rss · Simon Willison · 7月25日 08:42 北京时间 · [打开原文](https://simonwillison.net/2026/Jul/25/boris-cherny/#atom-everything){:target="_blank" rel="noopener noreferrer"}

### [Introducing Claude Opus 5](https://simonwillison.net/2026/Jul/24/introducing-claude-opus-5/#atom-everything){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Claude Opus 5 发布，性能接近 Fable 5，价格减半，在 Artificial Analysis 排行榜领先。

**对做产品的启发**：Simon Willison 汇总 Opus 5 发布信息，包括定价、性能领先等，高信噪比。

**继续验证**：关注 Opus 5 实际应用案例。

**原始来源**：rss · Simon Willison · 7月25日 07:48 北京时间 · [打开原文](https://simonwillison.net/2026/Jul/24/introducing-claude-opus-5/#atom-everything){:target="_blank" rel="noopener noreferrer"}

### [vercel/ai released @ai-sdk/anthropic@4.0.20](https://github.com/vercel/ai/releases/tag/%40ai-sdk/anthropic%404.0.20){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Vercel AI SDK 的 Anthropic 包 v4.0.20 新增 Claude Opus 5 模型、安全回退和对话中工具变更支持。

**对做产品的启发**：Vercel AI SDK 的 Anthropic 包新增 Claude Opus 5 模型支持、安全分类器回退和对话中工具变更功能，对构建 AI 产品有直接价值。

**继续验证**：关注 Claude Opus 5 在实际产品中的表现和定价。

**原始来源**：github · github-actions\[bot\] · 7月25日 01:25 北京时间 · [打开原文](https://github.com/vercel/ai/releases/tag/%40ai-sdk/anthropic%404.0.20){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [@OpenAIDevs: Your Pet is ready to meet other builders.  On Chat...](https://twitter.com/OpenAIDevs/status/tweet-2080747505474736162){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

OpenAI 宣布 ChatGPT 自定义宠物现在支持分享链接，用户可创建链接让朋友领养宠物。

**对做产品的启发**：OpenAI 官方宣布 ChatGPT 自定义宠物（Pet）新增分享功能，用户可创建可分享链接让朋友领养。这是 ChatGPT 个性化功能的小更新，但展示了社交化玩法，对产品经理有启发。

**继续验证**：观察用户分享和领养数据，评估社交功能对用户粘性的影响。

**原始来源**：twitter · OpenAI Developers · 7月25日 04:10 北京时间 · [打开原文](https://twitter.com/OpenAIDevs/status/tweet-2080747505474736162){:target="_blank" rel="noopener noreferrer"}

### [Health in ChatGPT](https://www.producthunt.com/products/openai){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

OpenAI 在 ChatGPT 中推出个人健康伴侣功能，提供健康相关对话支持。

**对做产品的启发**：ChatGPT 新增健康伴侣功能，属于产品新能力，但信息简短缺乏细节。

**继续验证**：关注具体功能细节和用户反馈。

**原始来源**：rss · Justin Jincaid · 7月25日 08:38 北京时间 · [打开原文](https://www.producthunt.com/products/openai){:target="_blank" rel="noopener noreferrer"}

### [OpenComputer](https://www.producthunt.com/products/opencomputer){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

OpenComputer 发布托管代理部署服务，简化 AI 代理的部署流程。

**对做产品的启发**：新产品 OpenComputer 提供托管代理部署，但信息简短缺乏细节。

**继续验证**：关注产品文档和用户反馈。

**原始来源**：rss · Utpal Nadiger 👋📈 · 7月25日 09:43 北京时间 · [打开原文](https://www.producthunt.com/products/opencomputer){:target="_blank" rel="noopener noreferrer"}

### [I tried out OpenAI’s new AI keypad — which will be fun for some coders and slightly mystifying to everyone else](https://techcrunch.com/2026/07/24/i-tried-out-openais-new-ai-keypad-which-will-be-fun-for-coders-and-slightly-mystifying-to-everyone-else/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

TechCrunch 试用 OpenAI 新 AI 键盘，认为对程序员有趣但对其他人可能神秘。

**对做产品的启发**：OpenAI 新硬件产品 AI 键盘，有试用体验，属于新产品发布。

**继续验证**：关注正式发布和用户反馈。

**原始来源**：rss · Lucas Ropek · 7月25日 08:23 北京时间 · [打开原文](https://techcrunch.com/2026/07/24/i-tried-out-openais-new-ai-keypad-which-will-be-fun-for-coders-and-slightly-mystifying-to-everyone-else/){:target="_blank" rel="noopener noreferrer"}

### [ARC-AGI Leaderboard](https://arcprize.org/leaderboard){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

ARC-AGI 排行榜显示 Claude Opus 5 取得高分，社区讨论其真实能力与基准测试的差距。

**对做产品的启发**：ARC-AGI 排行榜显示 Claude Opus 5 取得高分，引发社区讨论模型真实能力与基准测试的关系，对评估模型能力有参考价值。

**继续验证**：关注 Claude Opus 5 在更多基准测试和实际任务中的表现。

**原始来源**：hackernews · rzk · 7月25日 14:31 北京时间 · [打开原文](https://arcprize.org/leaderboard){:target="_blank" rel="noopener noreferrer"}

### [@sama: RT @pashmerepat: A billion users can now create an...](https://twitter.com/sama/status/tweet-2080713767122591863){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Sam Altman 转发称 10 亿用户现在可以用 ChatGPT Work 从手机创建和发布网站。

**对做产品的启发**：Sam Altman 转发他人推文，称 10 亿用户现在可以用 ChatGPT Work 从手机创建和发布网站。虽然是转发，但来自 CEO，有一定信号价值，但缺乏具体细节。

**继续验证**：观察 ChatGPT Work 网站创建功能的具体实现和用户反馈。

**原始来源**：twitter · Sam Altman · 7月25日 01:56 北京时间 · [打开原文](https://twitter.com/sama/status/tweet-2080713767122591863){:target="_blank" rel="noopener noreferrer"}

### [Why Cognition bought Poke: AI personality is becoming a competitive advantage](https://techcrunch.com/2026/07/24/why-cognition-bought-poke-ai-personality-is-becoming-a-competitive-advantage/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Cognition 收购 Poke，将对话风格融入编程代理 Devin，提升 AI 交互体验。

**对做产品的启发**：Cognition 收购 Poke 以增强 Devin 的对话个性，反映 AI 助手交互风格成为竞争差异。有明确产品案例和构建思路，但细节有限。

**继续验证**：关注 Devin 集成 Poke 后的用户反馈和交互效果。

**原始来源**：rss · Sarah Perez · 7月25日 02:07 北京时间 · [打开原文](https://techcrunch.com/2026/07/24/why-cognition-bought-poke-ai-personality-is-becoming-a-competitive-advantage/){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent：不只是回答问题，还能自主决定步骤、调用工具、执行多步任务的 AI 系统
- **知识点**：云浏览器/远程浏览器：AI 在云端开的真实浏览器，让 AI 能操作网页就像真人一样
- **知识点**：会话持久化：把登录状态存下来，打破&#x27;每次对话从零开始&#x27;的限制
- **知识点**：Context window（上下文窗口）：模型一次能&#x27;看&#x27;多少字，Opus 5 的 1M 约等于能塞进整本《三体》第一部，让 AI 分析大型代码库不丢线索
- **动手练习**：找一个你日常需要登录的网站（比如公司内部系统或某个数据分析平台），手动记录完成一个重复任务需要点击几次、输入什么；然后对比：如果 AI 能自动登录并执行，哪些步骤可以省掉？写下 3 个你最想让 agent 自动化的登录后任务。
- **动手练习**：30 分钟练习：安装 Claude Code，找一个自己的 Python 项目，用 /add-dir 把项目根目录加进去，然后问&#x27;这个项目的依赖结构有什么风险&#x27;，观察它如何分析；接着在设置里打开 sandbox.network.strictAllowlist，尝试让 AI 访问一个未白名单的 URL，看是否被拦截

## 数据与筛选说明

- 每天 08:30（北京时间）处理最近 24 小时的公开来源；先程序预筛和历史去重，再由 DeepSeek 批量评分。
- 优先级依次为：真实 AI 产品、构建实践、模型公司核心人员、新能力、精选 Newsletter。
- 纯算力、GPU、底层推理优化和学术论文默认降权，除非能直接解释新的产品机会。
- Top 2 由 Kimi 做初学者版产品拆解；失败时只对该条使用 DeepSeek Pro，所有模型均关闭思考。
- 同一事件执行语义去重和最近 7 天历史去重；结果缓存并同步到 JSON、CSV 和可筛选数据库页面。

[打开产品情报数据库]({{ '/products/' | relative_url }}) · [下载 JSON]({{ '/data/product-intelligence.json' | relative_url }}) · [下载 CSV]({{ '/data/product-intelligence.csv' | relative_url }})

<a id="archives"></a>
## 历史日报

[返回首页查看按日期归档]({{ '/' | relative_url }})
