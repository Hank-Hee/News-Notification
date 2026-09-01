---
layout: default
title: "AI产品情报 · 2026-09-01"
date: 2026-09-01
lang: zh
---

**日期**：2026-09-01　 **更新时间**：2026-09-01 14:14 北京时间

> 从 104 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Almanac 发布了一款能了解公司一切信息的 AI 代理，解决企业知识管理难题，值得关注其产品设计和市场验证。
- Polimill 利用 OpenAI GPT 和 Codex 为日本市政构建公共 AI 基础设施，提升行政知识检索效率。
- PM Daniel Blum 分享用 Claude 自动化 70-80%工作的方法，展示个人 AI 基础设施的构建实践。
- 作者用 BirdNET-Go 和现有安全摄像头构建了自动鸟类识别系统，展示了 AI 在边缘设备上的实际应用。
- ChatGPT Work 产品负责人 Tara Seshan 分享 AI 第三时代：持久化 AI 同事的崛起，探讨产品趋势。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Almanac：能记住公司一切的 AI 代理，YC S26 新品](https://usealmanac.com/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Almanac 发布了一款能了解公司一切信息的 AI 代理，解决企业知识管理难题，值得关注其产品设计和市场验证。

**评分**：8.5 / 10　 **证据**：一手信息

**产品 / 团队**：Almanac / kushagrchitkar

**目标用户**：需要管理大量分散信息的知识工作者、创业公司团队、以及想减少重复沟通的小企业

**它是什么**：一个开箱即用的 AI 代理（Agent，能自主执行任务的 AI 程序），自动整合你的邮件、日历、文档等信息，形成个人和公司两本&quot;活百科&quot;，让你不用反复交代背景就能提问和自动化任务。

**用户问题**：创始人想搭建一个懂公司上下文的 AI（Hermes），结果要自己逐个接 OAuth、手动喂数据、还要解决 AI 记不住事的默认缺陷；同批 YC 创始人都遇到同样麻烦

**使用流程**：
1. 注册后一键连接现有账户（Gmail、Calendar、PostHog 等）
2. 系统自动从连接源提取信息，生成&quot;个人百科&quot;和&quot;公司百科&quot;
3. 向 AI 提问或让它执行任务，它基于两本百科作答
4. 后台持续监控可自动化的任务，主动推送建议（如&quot;已草拟好融资 PPT，要看吗？&quot;）

**AI 在做什么**：持续维护两本动态百科（记忆层），并基于百科内容回答问题、执行长周期任务、主动推荐自动化

**怎么实现**：核心思路是&quot;预编译知识层&quot;：不是每次提问时临时去各平台抓信息，而是提前花算力把分散信息整理成结构化的 wiki，让 AI 有稳定的长期记忆。这样 AI 能跨天追踪项目进度，而不是聊完就忘。

**需要理解的知识点**：
1. Agent（AI 代理）：不只是回答问题的聊天机器人，是能调用工具、执行多步骤任务的 AI 程序
2. RAG（检索增强生成）：AI 回答前先查外部知识库，Almanac 的 wiki 就是一种高度结构化的 RAG 数据源
3. 长期记忆 vs 会话记忆：普通 AI 每次对话重新开始，Almanac 用 wiki 实现跨会话的持续记忆

**动手练习**：用免费工具复刻最小版 Almanac：1）在 Notion 建两页——&quot;关于我&quot;和&quot;关于我的工作&quot;；2）手动粘贴最近 5 封邮件主题、3 个日历事件、1 个项目文档摘要；3）用任意 AI（ChatGPT/Claude）上传这两页作为&quot;系统提示&quot;；4）测试问&quot;我这周优先级是什么&quot;&quot;项目卡在哪了&quot;，观察 AI 是否需要反复追问背景。30 分钟完成。

**已知限制**：未公开底层使用哪个 LLM 模型（社区 jedberg 追问未获答复）；未公开预编译 wiki 的具体更新频率和成本；多模型支持未确认；企业级安全审计细节未公开；与 Claude Desktop 功能重叠程度待用户实测对比

**原始来源**：hackernews · kushagrchitkar · 8月31日 23:34 北京时间 · [打开原文](https://usealmanac.com/){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Polimill 用 GPT 和 Codex 帮日本地方政府建公共 AI 知识库](https://openai.com/index/polimill){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Polimill 利用 OpenAI GPT 和 Codex 为日本市政构建公共 AI 基础设施，提升行政知识检索效率。

**评分**：7.5 / 10　 **证据**：一手信息

**产品 / 团队**：Polimill（未公开具体产品子名称） / OpenAI News

**目标用户**：日本地方政府（市町村）的行政人员、政策制定者

**它是什么**：一个帮日本地方政府把分散的议会会议记录统一整理、加上标签，变成能跨城市搜索的行政知识基础设施

**用户问题**：日本各地议会的会议记录格式不统一、分散在各处，行政人员想查其他城市的类似案例或政策依据时，找不到、搜不准、耗时长

**使用流程**：
1. Polimill 从各地方政府收集原始的议会会议记录
2. 用 AI 自动给这些记录加标签、标准化格式，建立统一的知识库
3. 行政人员用自然语言搜索，跨城市查找相关政策和先例
4. 开发人员用 Codex 加速构建基于这些数据的政务应用

**AI 在做什么**：GPT 负责理解会议记录内容并生成结构化标签（metadata），让搜索更精准；Codex 帮助开发者写代码，加快整个系统的开发速度

**怎么实现**：核心思路是&#x27;先统一数据，再让 AI 读懂数据&#x27;——把各地格式各异的会议记录变成机器能理解的结构化信息，这样搜索时就能匹配到真正相关的内容，而不是只靠关键词撞运气

**需要理解的知识点**：
1. RAG（检索增强生成）：先让 AI 从大量文档里找到相关片段，再回答问题，比直接让 AI 瞎猜更准确
2. Embedding（嵌入）：把文字变成数字向量，让语义相近的内容在数学上&#x27;离得更近&#x27;，实现&#x27;找意思相关的&#x27;而不是&#x27;找字一样的&#x27;
3. Function Calling（函数调用）：让 LLM 不只是聊天，还能触发查数据库、调搜索等外部工具，完成实际任务

**动手练习**：用 ChatGPT 上传 3 份不同格式的会议记录，让 AI 提取&#x27;议题、决议、负责部门&#x27;三个字段并统一成表格，然后测试用自然语言提问（如&#x27;去年关于预算调整的决议&#x27;）能否准确找到对应内容

**已知限制**：未公开具体覆盖的地方政府数量、会议记录总量、AI 标注的准确率数据、是否已大规模上线运行还是试点阶段、Codex 的具体使用场景和占比

**原始来源**：rss · OpenAI News · 8月31日 15:00 北京时间 · [打开原文](https://openai.com/index/polimill){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [🎙️ How I AI: How this PM uses Claude to handle 70% to 80% of his workday](https://www.lennysnewsletter.com/p/how-i-ai-how-this-pm-uses-claude){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

PM Daniel Blum 分享用 Claude 自动化 70-80%工作的方法，展示个人 AI 基础设施的构建实践。

**对做产品的启发**：Lenny Rachitsky 的播客，PM Daniel Blum 分享如何用 Claude 处理 70-80%工作，包含具体工作流和系统构建，对 AI 产品经理有高参考价值。

**继续验证**：深入了解其自改进循环和 Workstation 插件的具体实现。

**原始来源**：newsletter · Lenny Rachitsky · 8月31日 23:01 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-how-this-pm-uses-claude){:target="_blank" rel="noopener noreferrer"}

### [AI’s third era: the rise of persistent AI coworkers \| Tara Seshan \(Product Lead ChatGPT Work\)](https://www.lennysnewsletter.com/p/ais-third-era-the-rise-of-persistent){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

ChatGPT Work 产品负责人 Tara Seshan 分享 AI 第三时代：持久化 AI 同事的崛起，探讨产品趋势。

**对做产品的启发**：ChatGPT Work 产品负责人 Tara Seshan 讨论 AI 第三时代：持久化 AI 同事，提供行业趋势和产品视角，对理解 AI 产品演进有增量价值。

**继续验证**：关注 ChatGPT Work 如何实现持久化 AI 同事。

**原始来源**：newsletter · Lenny Rachitsky · 8月30日 20:31 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/ais-third-era-the-rise-of-persistent){:target="_blank" rel="noopener noreferrer"}

### [not much happened today](https://news.smol.ai/issues/26-08-26-not-much/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Z.ai 正式发布 GLM-5.3-Flash，原生多模态，1M 上下文，320B 参数，MIT 许可，提供权重和 API。

**对做产品的启发**：AI 新闻简报报道 GLM-5.3-Flash 正式发布，包含模型参数、上下文窗口、MIT 许可等关键信息，属于新模型能力动态。

**继续验证**：关注模型实际性能和应用案例。

**原始来源**：newsletter · AI News · 8月26日 13:44 北京时间 · [打开原文](https://news.smol.ai/issues/26-08-26-not-much/){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [I turned my security cameras into an automatic bird identification system](https://jasontucker.blog/how-i-turned-my-security-cameras-into-an-automatic-bird-identification-system-with-birdnet-go/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

作者用 BirdNET-Go 和现有安全摄像头构建了自动鸟类识别系统，展示了 AI 在边缘设备上的实际应用。

**对做产品的启发**：一手构建案例，展示如何用 BirdNET-Go 和现有摄像头实现自动鸟类识别，有具体技术细节和用户反馈，对初学者有启发。

**继续验证**：关注作者后续是否分享更多优化细节或扩展应用。

**原始来源**：hackernews · speckx · 9月1日 00:47 北京时间 · [打开原文](https://jasontucker.blog/how-i-turned-my-security-cameras-into-an-automatic-bird-identification-system-with-birdnet-go/){:target="_blank" rel="noopener noreferrer"}

### [Introducing wrapture](https://simonwillison.net/2026/Aug/31/introducing-wrapture/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Graham Dumpleton 发布 Wrapture，扩展 wrapt 实现函数包装、测试和追踪，支持 OpenTelemetry。

**对做产品的启发**：构建者发布新工具，提供测试和追踪能力，对 AI 应用调试有实用价值。

**继续验证**：关注社区采用和文档完善。

**原始来源**：rss · Simon Willison · 9月1日 07:59 北京时间 · [打开原文](https://simonwillison.net/2026/Aug/31/introducing-wrapture/){:target="_blank" rel="noopener noreferrer"}

### [ChatGPT Work Tool and Skill Reference](https://codex-tool-reference.simonw.chatgpt.site/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Simon Willison 整理并分享了 ChatGPT Work 的工具和技能参考，其中控制浏览器的技能展示了如何通过 Playwright 实现自动化操作。

**对做产品的启发**：Simon Willison 分享的 ChatGPT Work 工具和技能参考，包含控制浏览器的技能，对理解 Agent 工具使用有实际价值。

**继续验证**：关注该参考的更新和社区反馈。

**原始来源**：hackernews · ijidak · 8月31日 22:07 北京时间 · [打开原文](https://codex-tool-reference.simonw.chatgpt.site/){:target="_blank" rel="noopener noreferrer"}

### [Show HN: SlideOps – slides from a repo that flag when they drift from the code](https://github.com/glukicov/slideops){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

SlideOps 将代码仓库转化为带溯源信息的幻灯片，并自动检测代码漂移，解决 AI 文档维护难题，值得借鉴其思路。

**对做产品的启发**：开发者展示 SlideOps，解决 AI 生成文档与代码漂移问题，提供可验证的 GitHub 项目和详细技术说明，属于高价值构建者实践。

**继续验证**：关注其在不同 AI 编码工具中的兼容性和实际使用效果。

**原始来源**：hackernews · lukicov · 8月31日 20:15 北京时间 · [打开原文](https://github.com/glukicov/slideops){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Improving Alignment Security Efforts](https://www.anthropic.com/news/improving-alignment-security-efforts){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Anthropic 官方宣布改进 AI 对齐安全措施，提升模型安全性，值得关注其后续技术细节。

**对做产品的启发**：Anthropic 官方发布对齐安全改进，属于模型能力安全层面的重要更新，但未提供具体技术细节或产品案例，对初学者可迁移性有限。

**继续验证**：关注具体技术方案和实际效果评估。

**原始来源**：public\_web · Anthropic News · 9月1日 06:39 北京时间 · [打开原文](https://www.anthropic.com/news/improving-alignment-security-efforts){:target="_blank" rel="noopener noreferrer"}

### [Model Hardware Standard Research Preview](https://www.anthropic.com/news/model-hardware-standard-research-preview){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Anthropic 发布模型硬件标准研究预览，探索硬件与模型协同设计，可能为未来 AI 产品提供新基础。

**对做产品的启发**：Anthropic 官方发布的研究预览，涉及模型硬件标准，可能影响未来 AI 产品部署方式，但缺乏具体细节和产品落地证据，作为早期信号值得关注。

**继续验证**：关注后续详细技术文档和产品化进展

**原始来源**：public\_web · Anthropic News · 8月29日 18:57 北京时间 · [打开原文](https://www.anthropic.com/news/model-hardware-standard-research-preview){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Harvard Law dropout raises $6M for Blue Voice to build a ‘Harvey for police officers’](https://techcrunch.com/2026/08/31/harvard-law-dropout-raises-6m-for-blue-voice-to-build-a-harvey-for-police-officers/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

哈佛法学院辍学生为 Blue Voice 融资 600 万美元，打造面向警察的 AI 助手，解决通用 AI 无法访问部门特定法规的问题。

**对做产品的启发**：垂直领域 AI 产品（面向警察），有融资和明确产品定位，但缺乏用户反馈和产品细节，属于早期信号。

**继续验证**：关注产品是否上线及用户反馈。

**原始来源**：rss · Marina Temkin · 9月1日 02:35 北京时间 · [打开原文](https://techcrunch.com/2026/08/31/harvard-law-dropout-raises-6m-for-blue-voice-to-build-a-harvey-for-police-officers/){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent（AI 代理）：不只是回答问题的聊天机器人，是能调用工具、执行多步骤任务的 AI 程序
- **知识点**：RAG（检索增强生成）：AI 回答前先查外部知识库，Almanac 的 wiki 就是一种高度结构化的 RAG 数据源
- **知识点**：长期记忆 vs 会话记忆：普通 AI 每次对话重新开始，Almanac 用 wiki 实现跨会话的持续记忆
- **知识点**：RAG（检索增强生成）：先让 AI 从大量文档里找到相关片段，再回答问题，比直接让 AI 瞎猜更准确
- **动手练习**：用免费工具复刻最小版 Almanac：1）在 Notion 建两页——&quot;关于我&quot;和&quot;关于我的工作&quot;；2）手动粘贴最近 5 封邮件主题、3 个日历事件、1 个项目文档摘要；3）用任意 AI（ChatGPT/Claude）上传这两页作为&quot;系统提示&quot;；4）测试问&quot;我这周优先级是什么&quot;&quot;项目卡在哪了&quot;，观察 AI 是否需要反复追问背景。30 分钟完成。
- **动手练习**：用 ChatGPT 上传 3 份不同格式的会议记录，让 AI 提取&#x27;议题、决议、负责部门&#x27;三个字段并统一成表格，然后测试用自然语言提问（如&#x27;去年关于预算调整的决议&#x27;）能否准确找到对应内容

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
