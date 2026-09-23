---
layout: default
title: "AI产品情报 · 2026-09-23"
date: 2026-09-23
lang: zh
---

**日期**：2026-09-23　 **更新时间**：2026-09-23 12:44 北京时间

> 从 153 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Rabbit 推出无需自家硬件的 AI agent 操作系统 OS3，云端运行但可跨 Windows、Mac 和 Linux 本地操作，试图摆脱 R1 失败阴影。
- OpenAI 的编码工具 Codex 发布 rust-v0.156.0，新增全屏界面、默认开启的语音对话、用量分析面板、worktree 会话和多种主题，让编码 Agent 更像一个完整工作台。
- OpenAI 官方称 Parallel 用 GPT-6 Astra 做劳动力市场数据研究，时间和成本都减半，是一个可参考的 agent 落地案例。
- Hamel Husain 在 Lenny 的 Newsletter 讲进阶 evals，教产品团队如何找出并修复 AI 产品里隐藏的失败，对刚转 AI 产品经理的人很实用。
- Claire Vo 离开 Claude 数月后因 Opus 5.5 回归，用一周真实工作验证其更便宜、更快，并指出仍有两个让人抓狂的点，值得产品人参考。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Rabbit 推出跨平台 AI Agent 操作系统 OS3，不再绑定 R1 硬件](https://www.theverge.com/ai-artificial-intelligence/999094/rabbit-ai-agent-os3){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Rabbit 推出无需自家硬件的 AI agent 操作系统 OS3，云端运行但可跨 Windows、Mac 和 Linux 本地操作，试图摆脱 R1 失败阴影。

**评分**：7.8 / 10　 **证据**：媒体报道

**产品 / 团队**：rabbit OS3 / Emma Roth

**目标用户**：想在电脑上用自然语言指令让 AI 自动完成跨网页、跨应用任务的用户；未公开具体是否面向开发者或普通消费者

**它是什么**：Rabbit 公司发布的云端 AI Agent 操作系统，能在 Windows、Mac、Linux 上本地操作，用户不用买它的 R1 设备也能用

**用户问题**：R1 硬件口碑差、销量低迷，用户不想为单一设备买单；同时现有 AI 工具多为聊天框，不能真正动手帮用户操作电脑完成任务

**使用流程**：
1. 用户在任意平台（网页、Telegram、R1 或连接的电脑）用自然语言说出想做的事
2. OS3 解析意图，调度支持的 AI 模型和技能
3. AI 在云端规划步骤，连接到用户授权的电脑或网页执行
4. 用户收到结果，可继续追问或调整

**AI 在做什么**：理解用户意图、拆解任务步骤、调用模型和技能、在连接的电脑或网页上实际执行操作

**怎么实现**：云端有个&#x27;指挥中心&#x27;，用户说话过来后，AI 先理解要干嘛，再像远程助手一样登录你的电脑或打开网页，一步步点按钮、填表格、下指令，最后把结果拿回来给你。本质是把&#x27;聊天&#x27;变成&#x27;动手做&#x27;

**需要理解的知识点**：
1. Agent（智能体）：不只是回答你，还能自己决定下一步动作、调用工具去执行任务的 AI 系统
2. Function Calling（函数调用）：AI 判断&#x27;现在该调用某个功能&#x27;的能力，比如&#x27;现在该打开浏览器搜价格&#x27;或&#x27;现在该写进表格&#x27;
3. 云端+本地混合：AI 大脑在云端思考，但手脚伸进你的本地设备操作，需要解决安全和权限问题

**动手练习**：30 分钟体验：打开 rabbit.tech 官网，找到 OS3 入口，尝试用自然语言发一个简单任务（如&#x27;查今天纽约天气并总结成一句话&#x27;），观察它是直接给答案、还是真的执行了多步操作；同时对比你平时用 ChatGPT/Claude 的同样提问，记录两者在&#x27;动手执行&#x27;上的差异

**已知限制**：官方声称支持 Windows/Mac/Linux 本地操作，但目前缺乏第三方用户实际录屏验证；&#x27;本地操作&#x27;的具体权限范围、是否需要安装客户端、是否收费均未公开；The Verge 报道为早期发布消息，尚无大规模用户反馈

**原始来源**：rss · Emma Roth · 9月23日 04:52 北京时间 · [打开原文](https://www.theverge.com/ai-artificial-intelligence/999094/rabbit-ai-agent-os3){:target="_blank" rel="noopener noreferrer"}

---
### 2. [OpenAI Codex 终端编码 Agent 发布 v0.156.0：全屏界面、语音默认开启、用量分析](https://github.com/openai/codex/releases/tag/rust-v0.156.0){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：OpenAI 的编码工具 Codex 发布 rust-v0.156.0，新增全屏界面、默认开启的语音对话、用量分析面板、worktree 会话和多种主题，让编码 Agent 更像一个完整工作台。

**评分**：7.5 / 10　 **证据**：一手信息

**产品 / 团队**：OpenAI Codex CLI / github-actions\[bot\]

**目标用户**：习惯终端操作的开发者、需要快速原型或批量处理代码的工程师

**它是什么**：Codex 是 OpenAI 出品的终端内运行的轻量级编码 Agent（AI 编程助手），能在命令行里理解自然语言指令、读写代码、执行命令。

**用户问题**：开发者在终端里写代码时，需要在编辑器、浏览器、AI 聊天窗口之间来回切换；无法直观看到 AI 用了多少 token、调用了哪些工具；多人协作或复杂项目里会话管理混乱

**使用流程**：
1. 安装后运行 codex，用 /tui 进入全屏界面，支持鼠标选择和右键复制
2. 直接说话或打字给 AI 下指令（语音默认开启，按 F8 切换）
3. AI 自动读写文件、运行测试、调用工具，结果直接显示在终端
4. 用 /usage 查看 token 消耗和插件活动，用 /daemon 管理本地后台服务

**AI 在做什么**：AI 负责解析自然语言指令、生成/修改代码、调用外部工具（如测试运行器、文件系统）、在多轮对话中保持上下文，并通过 worktree 隔离不同任务

**怎么实现**：Codex 在本地启动一个后台服务（daemon），通过终端 UI 与用户交互；用户输入经 LLM 解析后，AI 决定调用哪些工具（Function Calling，即 AI 选择调用外部函数来完成任务），结果流式返回终端。语音功能通过本地音频运行时处理，worktree 用 Git 工作树机制隔离不同会话的文件状态。

**需要理解的知识点**：
1. Agent：能自主规划步骤、调用工具、完成多轮任务的 AI，不只是单次问答
2. Function Calling：LLM 识别需要外部工具时，生成结构化调用指令（如读文件、运行命令），而非直接回答
3. Worktree：Git 功能，让同一仓库同时存在多个独立工作目录，避免不同任务互相污染代码

**动手练习**：30 分钟动手：安装 Codex CLI（需 OpenAI API 密钥），用 /tui 进入全屏模式，让 AI 写一个 Python 脚本并运行；然后用 /usage 查看本次消耗的 token 数；最后开两个 worktree 会话，让 AI 分别在两个目录做不相关的修改，验证文件是否隔离

**已知限制**：语音功能的具体模型（是否为 Whisper 实时 API）未公开；用量分析面板的数据延迟和精确计费规则未公开；MCP（Model Context Protocol）凭证刷新机制的具体实现细节未公开；sandbox 隔离的完整安全审计报告未公开

**原始来源**：github · github-actions\[bot\] · 9月23日 03:51 北京时间 · [打开原文](https://github.com/openai/codex/releases/tag/rust-v0.156.0){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [Advanced evals: How to find \(and fix\) hidden AI failures in your product](https://www.lennysnewsletter.com/p/advanced-evals-how-to-find-and-fix){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Hamel Husain 在 Lenny 的 Newsletter 讲进阶 evals，教产品团队如何找出并修复 AI 产品里隐藏的失败，对刚转 AI 产品经理的人很实用。

**对做产品的启发**：Hamel Husain 讲如何在产品中发现并修复隐藏的 AI 失败，属高信噪比方法论内容，直接服务 AI 产品经理的评测实践，可迁移性强。

**继续验证**：整理其评测流程，尝试套用到自己的产品原型上。

**原始来源**：newsletter · Hamel Husain · 9月22日 20:45 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/advanced-evals-how-to-find-and-fix){:target="_blank" rel="noopener noreferrer"}

### [I left Claude for months. Opus 5.5 is why I&#x27;m back](https://www.lennysnewsletter.com/p/i-left-claude-for-months-opus-55){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Claire Vo 离开 Claude 数月后因 Opus 5.5 回归，用一周真实工作验证其更便宜、更快，并指出仍有两个让人抓狂的点，值得产品人参考。

**对做产品的启发**：Claire Vo 用一周真实工作（四个长时 agent 任务、ChatPRD 首页改版、SVG 基准）评测 Opus 5.5，属有身份可核验的从业者实践，含具体使用场景与吐槽，对产品经理有可迁移增量。

**继续验证**：关注其提到的两个缺点是否在后续版本修复。

**原始来源**：newsletter · Claire Vo · 9月23日 03:06 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/i-left-claude-for-months-opus-55){:target="_blank" rel="noopener noreferrer"}

### [Opus 5.5 vs. GPT-6 Sol: which model won my blind taste test?](https://www.lennysnewsletter.com/p/opus-55-vs-gpt-6-sol-which-model){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

Claire Vo 把 Opus 5.5、GPT-6 Sol/Astra 等模型放进真实工作流做盲测，结论是 Astra 讨喜、Opus 5.5 更实用，给产品人选模型提供了实操参考。

**对做产品的启发**：Claire Vo 用真实工作任务（邮件、PRD、前端原型、长时 agent）对 Opus 5.5、GPT-6 Sol/Astra 做盲测，属有身份可核验的从业者一手实践，对 AI 产品经理理解模型选型有可迁移价值，但非产品构建案例。

**继续验证**：关注其盲测方法与评分维度能否复用到自己的产品评测中。

**原始来源**：newsletter · Claire Vo · 9月23日 07:12 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/opus-55-vs-gpt-6-sol-which-model){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [SF October 14th: A Birds of a Feather Session on Agentic Engineering](https://simonwillison.net/2026/Sep/23/bof-agentic-engineering/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Simon Willison 与 Jesse Vincent 将于 10 月 14 日在旧金山举办 Agentic Engineering 交流活动，鼓励构建者分享未公开的奇怪实验和未完成项目。

**对做产品的启发**：Simon Willison 主办 Agentic Engineering 线下交流活动，面向构建者分享未公开的奇怪实验和未完成项目，属于构建者社区一手动态，对 AI 产品经理有启发，但为活动预告而非产品发布，故 7.5 分。

**继续验证**：关注活动后是否有公开的分享记录或项目 Demo。

**原始来源**：rss · Simon Willison · 9月23日 10:53 北京时间 · [打开原文](https://simonwillison.net/2026/Sep/23/bof-agentic-engineering/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude Opus 5.5, GPT-6 Sol, GPT-6 Luna, and a new price war](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.8/10

Simon Willison 分析 Anthropic 和 OpenAI 同日发布新模型，指出 GPT-6 Sol 和 Luna 价格仅为 GPT-5.6 同级的一半，引发新一轮价格战。

**对做产品的启发**：Simon Willison 一手分析 Claude Opus 5.5、GPT-6 Sol/Luna 发布及价格战，包含具体定价对比和开发者视角，对 AI 产品经理理解模型成本与选型有高价值，故 8.8 分。

**继续验证**：关注后续模型实测对比及对 AI 应用成本结构的影响。

**原始来源**：rss · Simon Willison · 9月23日 07:46 北京时间 · [打开原文](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/){:target="_blank" rel="noopener noreferrer"}

### [Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Anthropic 发布 Claude Opus 5.5，价格比 Opus 5 降约 40% 并改进表达风格，官方称其为“放缓前沿”呼吁后的首个发布，值得关注其对日常 AI 工作流成本的影响。

**对做产品的启发**：Anthropic 官方发布 Claude Opus 5.5，含明确降价（输入 $4、输出 $20）、沟通风格改进等一手信息，HN 1346 分高热度讨论，属模型公司核心动态，对产品选型有直接价值。

**继续验证**：观察 Opus 5.5 在 OpenRouter 等平台的真实使用量与开发者迁移情况。

**原始来源**：hackernews · km144 · 9月23日 00:29 北京时间 · [打开原文](https://www.anthropic.com/claude-opus-5-5){:target="_blank" rel="noopener noreferrer"}

### [OpenAI launches GPT-6 Sol and Luna, boasting lower cost and fewer mistakes](https://techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

OpenAI 发布 GPT-6 Sol 和 Luna 两个新模型，称成本更低、错误更少，与 Astra 同源，可能降低 AI 产品开发成本。

**对做产品的启发**：OpenAI 发布两个新模型，宣称成本更低、错误更少，属于模型公司核心能力动态，能直接催生新产品，对 AI 产品经理有高价值，但来源为媒体报道而非官方一手，故 8.2 分。

**继续验证**：关注官方技术报告、定价细节及开发者实测反馈。

**原始来源**：rss · Lucas Ropek · 9月23日 02:00 北京时间 · [打开原文](https://techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna/){:target="_blank" rel="noopener noreferrer"}

### [anthropics/claude-code released v2.1.280](https://github.com/anthropics/claude-code/releases/tag/v2.1.280){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Anthropic 的编码工具 Claude Code 更新到 v2.1.280，把 Claude Opus 5.5 设为默认模型，支持 100 万上下文、每百万 token 输入 4 美元输出 20 美元，并修复了自动模式反复重试等问题。

**对做产品的启发**：Anthropic 官方 Claude Code 发布 v2.1.280，将 Claude Opus 5.5 设为默认 Opus 模型并给出 1M 上下文与 $4/$20 定价，同时修复自动模式反复重试等安全问题，是编码 Agent 产品与模型能力结合的一手增量。

**继续验证**：观察 Opus 5.5 在 Claude Code 中的实际表现与成本反馈，以及 MCP 描述长度限制调整的影响。

**原始来源**：github · ashwin-ant · 9月23日 00:38 北京时间 · [打开原文](https://github.com/anthropics/claude-code/releases/tag/v2.1.280){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Parallel cut research time and cost in half with GPT‑6 Astra](https://openai.com/index/parallel-cuts-time-and-cost-with-astra){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.4/10

OpenAI 官方称 Parallel 用 GPT-6 Astra 做劳动力市场数据研究，时间和成本都减半，是一个可参考的 agent 落地案例。

**对做产品的启发**：OpenAI 官方客户案例，Parallel 用 GPT-6 Astra 把劳动力市场数据研究的时间与成本各减半，属一手客户落地证据，但内容极短且带官方营销性质，故扣分。

**继续验证**：寻找 Parallel 侧更详细的技术或产品说明以验证效果。

**原始来源**：rss · OpenAI News · 9月22日 20:00 北京时间 · [打开原文](https://openai.com/index/parallel-cuts-time-and-cost-with-astra){:target="_blank" rel="noopener noreferrer"}

### [🎙️ How I AI: Meta’s Muse review + How Warp ships 2,000 PRs a month with AI factories](https://www.lennysnewsletter.com/p/how-i-ai-metas-muse-review-how-warp){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Lenny 的播客评测了 Meta 个人 Agent Muse 的消费级体验，并拆解 Warp 如何用 AI 工厂每月交付 2000 个 PR，适合学习 Agent 产品设计和工程实践。

**对做产品的启发**：Lenny 的 Newsletter 同时包含 Meta Muse 个人 Agent 的真实上手评测和 Warp 用 AI 工厂每月交付 2000 个 PR 的实践，有具体使用场景和构建流程，对产品经理有可迁移增量。

**继续验证**：追踪 Muse 的权限模型和 Warp 的 Slack→Linear→GitHub 工作流细节。

**原始来源**：newsletter · Lenny Rachitsky · 9月21日 23:03 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-metas-muse-review-how-warp){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent（智能体）：不只是回答你，还能自己决定下一步动作、调用工具去执行任务的 AI 系统
- **知识点**：Function Calling（函数调用）：AI 判断&#x27;现在该调用某个功能&#x27;的能力，比如&#x27;现在该打开浏览器搜价格&#x27;或&#x27;现在该写进表格&#x27;
- **知识点**：云端+本地混合：AI 大脑在云端思考，但手脚伸进你的本地设备操作，需要解决安全和权限问题
- **知识点**：Agent：能自主规划步骤、调用工具、完成多轮任务的 AI，不只是单次问答
- **动手练习**：30 分钟体验：打开 rabbit.tech 官网，找到 OS3 入口，尝试用自然语言发一个简单任务（如&#x27;查今天纽约天气并总结成一句话&#x27;），观察它是直接给答案、还是真的执行了多步操作；同时对比你平时用 ChatGPT/Claude 的同样提问，记录两者在&#x27;动手执行&#x27;上的差异
- **动手练习**：30 分钟动手：安装 Codex CLI（需 OpenAI API 密钥），用 /tui 进入全屏模式，让 AI 写一个 Python 脚本并运行；然后用 /usage 查看本次消耗的 token 数；最后开两个 worktree 会话，让 AI 分别在两个目录做不相关的修改，验证文件是否隔离

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
