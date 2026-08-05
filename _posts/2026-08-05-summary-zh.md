---
layout: default
title: "AI产品情报 · 2026-08-05"
date: 2026-08-05
lang: zh
---

**日期**：2026-08-05　 **更新时间**：2026-08-05 11:33 北京时间

> 从 181 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- 外部重构了 ChatGPT Work 的 Agent 能力，帮助理解其如何解决复杂任务自动化问题。
- eve agent 新增浏览器扩展，使其能像人类一样浏览和操作网页。
- Wrinkles 是一款 AI 音频导览应用，通过揭示身边地点的隐藏历史故事，为用户提供沉浸式旅游体验。
- skills.sh 推出技能包功能，可打包分享多个 Agent 技能，简化技能分发。
- Simon Willison 发布 LLM 0.32，新增推理轨迹显示、服务端工具和 OpenAI Responses 支持，提升 AI 应用开发效率。

<a id="product-teardown"></a>
## 产品拆解

### 1. [拆解 ChatGPT Work：面向十亿用户的 Agent 长什么样](https://www.latent.space/p/unpacking-chatgpt-work){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：外部重构了 ChatGPT Work 的 Agent 能力，帮助理解其如何解决复杂任务自动化问题。

**评分**：8.5 / 10　 **证据**：媒体报道

**产品 / 团队**：ChatGPT Work / Shlok Khemani

**目标用户**：需要自动化复杂工作流的团队和企业用户

**它是什么**：一篇第三方博客文章，从外部反推 ChatGPT Work 的 Agent 能力设计，包括记忆、主动执行、定时任务、浏览器操作等模块

**用户问题**：日常工作中信息分散在各处（笔记、草稿、邮件、文档），需要手动切换工具、重复整理，项目推进靠人盯着

**使用流程**：
1. 用户授权 ChatGPT Work 接入团队工具（如文档、日历、项目管理软件）
2. 用自然语言描述目标，例如&#x27;每周一整理上周销售数据并邮件发给团队&#x27;
3. AI 自主规划步骤：调取数据、分析、生成报告、发送邮件
4. 用户收到结果通知，必要时介入确认或修正

**AI 在做什么**：作为&#x27;执行代理&#x27;（Agent），理解目标后自主决策调用哪些工具、何时执行、如何记住上下文，而非等用户逐句指挥

**怎么实现**：核心思路是把大模型当成&#x27;会思考的项目经理&#x27;：先用记忆模块记住用户偏好和业务背景，再用调度模块安排定时任务，需要时调用浏览器或插件去外部系统取数据/操作，最后把结果汇总回来。作者是从产品外部观察这些模块如何配合，而非看内部代码

**需要理解的知识点**：
1. Agent：不只是回答问题，而是能自主规划多步骤并调用工具完成目标的 AI 系统
2. Function Calling：大模型&#x27;伸出触角&#x27;——识别需要调外部工具时，生成结构化指令让程序去执行
3. RAG（检索增强生成）：AI 先从外部知识库找相关信息，再基于找来的内容回答或行动，避免瞎编

**动手练习**：30 分钟：打开 ChatGPT 的&#x27;任务&#x27;功能（若已开放）或任何支持定时提醒的 AI 工具，设置一个重复任务如&#x27;每天早上 9 点总结我的日历并建议优先级&#x27;，观察它如何调用日历、生成摘要、是否需要你确认

**已知限制**：文章为外部重构，非 OpenAI 官方技术文档；GPT-5.6 型号、具体发布时间、企业定价、安全审计机制均未公开；&#x27;Proactivity&#x27;（主动执行）的实际边界和错误回滚策略未知

**原始来源**：rss · Shlok Khemani · 8月5日 02:20 北京时间 · [打开原文](https://www.latent.space/p/unpacking-chatgpt-work){:target="_blank" rel="noopener noreferrer"}

---
### 2. [给 eve Agent 装上浏览器：让它像人一样上网](https://vercel.com/changelog/give-your-eve-agent-a-browser){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：eve agent 新增浏览器扩展，使其能像人类一样浏览和操作网页。

**评分**：8.0 / 10　 **证据**：一手信息

**产品 / 团队**：eve（@agent-browser/eve 扩展） / Chris Tate

**目标用户**：开发 eve Agent 的工程师，需要让 AI 自动完成网页交互任务（如数据采集、自动化测试、表单填写）

**它是什么**：Vercel 旗下 eve 平台的一个浏览器扩展，让 AI Agent 能打开网页、点击、填表、截图，像人类一样操作浏览器。

**用户问题**：Agent 原本只能调用 API 或处理文本，遇到需要操作网页界面的任务就束手无策，开发者得自己写复杂的浏览器自动化脚本。

**使用流程**：
1. 安装 @agent-browser/eve 扩展包
2. 把扩展挂载到 agent/extensions/ 目录
3. Agent 自动获得 browser\_\_navigate 等工具，用 browser\_\_snapshot 查看页面后，通过 @e12 这类引用精准点击或填写
4. 通过 allowedDomains 等配置限制访问范围，保护敏感凭据

**AI 在做什么**：AI 负责&#x27;看&#x27;页面（snapshot）、理解元素位置（通过 ref 引用）、决定下一步操作（点击/填写/截图），并在 sandbox 里实际执行浏览器命令

**怎么实现**：给 Agent 配了一个&#x27;沙盒里的 Chrome&#x27;，Agent 看到的不是原始 HTML，而是带编号标记的页面快照（snapshot），它说&#x27;点 @e12&#x27;，扩展就把这个引用翻译成真实元素去执行，避免 AI 直接碰原始 DOM 和 Cookie。

**需要理解的知识点**：
1. Agent：能自主规划步骤、调用工具完成任务的 AI 系统，不只是聊天
2. Sandbox（沙盒）：把危险操作关进隔离环境，即使浏览器被攻击也不会影响到你的主程序
3. Function Calling：AI 不直接生成代码，而是输出&#x27;调用某某工具、参数是什么&#x27;的结构化指令，由系统代为执行

**动手练习**：跟着官方 example（GitHub 上的 Next.js 项目）跑起来，让 eve Agent 自动完成一个任务：打开一个测试网页 → 截图保存 → 点击按钮 → 填写表单 → 再截图对比，全程观察 Agent 怎么通过 snapshot 和 ref 一步步决策。

**已知限制**：未公开具体定价、性能基准（页面加载多快、并发多少）、是否支持非 Chromium 浏览器、企业级安全审计细节；&#x27;Credential protection&#x27;的具体实现机制（是系统级拦截还是工具层屏蔽）未详细说明。

**原始来源**：rss · Chris Tate · 8月4日 12:00 北京时间 · [打开原文](https://vercel.com/changelog/give-your-eve-agent-a-browser){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [🎙️ How I AI: ChatGPT Codex Voice + browser + Sites: an expert’s AI workflow \| Nick Baumann \(OpenAI\)](https://www.lennysnewsletter.com/p/how-i-ai-chatgpt-codex-voice-browser){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

OpenAI 专家 Nick Baumann 演示 ChatGPT Codex 的语音、浏览器和 Sites 功能，展示 AI 辅助工作流，值得学习其实际应用。

**对做产品的启发**：Lenny Rachitsky 的播客，邀请 OpenAI 开发者体验团队成员分享 ChatGPT Codex 的语音、浏览器和 Sites 功能，属于高信噪比行业观察，有具体产品功能演示，评分 8.0。

**继续验证**：关注 Codex 新功能的实际使用体验和更多案例。

**原始来源**：newsletter · Lenny Rachitsky · 8月3日 23:02 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-chatgpt-codex-voice-browser){:target="_blank" rel="noopener noreferrer"}

### [Qwen 3.8 Max](https://news.smol.ai/issues/26-08-03-qwen-38/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

阿里发布 Qwen3.8-Max 旗舰模型，2.4T 参数，主打编码和长程 agent，并宣布下周开源权重。

**对做产品的启发**：阿里发布 Qwen3.8-Max 旗舰模型，2.4T 参数，聚焦编码、长程 agent 和多模态推理，并承诺下周开源权重，是重要的模型能力动态。

**继续验证**：关注开源权重发布及实际性能表现。

**原始来源**：newsletter · AI News · 8月3日 13:44 北京时间 · [打开原文](https://news.smol.ai/issues/26-08-03-qwen-38/){:target="_blank" rel="noopener noreferrer"}

### [Latest open artifacts \(\#23\): Laguna S2.1, Inkling, &amp; Kimi K3 show the utility of open models on the Pareto frontier](https://www.interconnects.ai/p/latest-open-artifacts-23-laguna-s21){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

行业观察指出开放模型在帕累托前沿的实用性，并以 Thinking Machines 的开放微调服务为例说明其商业价值。

**对做产品的启发**：行业观察，讨论开放模型在帕累托前沿的价值，提及 Thinking Machines 的开放微调服务收入，但缺乏具体产品细节和用户反馈，属于高信噪比行业分析。

**继续验证**：关注 Thinking Machines 开放微调服务的具体产品形态和用户反馈。

**原始来源**：newsletter · Florian Brand · 8月2日 21:01 北京时间 · [打开原文](https://www.interconnects.ai/p/latest-open-artifacts-23-laguna-s21){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging](https://simonwillison.net/2026/Aug/4/new-release-of-llm/#atom-everything){:target="_blank" rel="noopener noreferrer"} ⭐️ 9.0/10

Simon Willison 发布 LLM 0.32，新增推理轨迹显示、服务端工具和 OpenAI Responses 支持，提升 AI 应用开发效率。

**对做产品的启发**：Simon Willison 发布 LLM 0.32，新增推理轨迹显示、OpenAI Responses 支持、服务端工具等，对开发者构建 AI 应用有直接价值，属于高价值工具更新。

**继续验证**：关注新版本在实际项目中的应用反馈。

**原始来源**：rss · Simon Willison · 8月5日 07:58 北京时间 · [打开原文](https://simonwillison.net/2026/Aug/4/new-release-of-llm/#atom-everything){:target="_blank" rel="noopener noreferrer"}

### [llm-anthropic 0.26](https://simonwillison.net/2026/Aug/4/llm-anthropic/#atom-everything){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

llm-anthropic 0.26 发布，新增 Claude 5 系列模型和服务端工具，支持 LLM 0.32 新特性。

**对做产品的启发**：llm-anthropic 插件更新，新增 Claude 5 系列模型和服务端工具，与 LLM 0.32 配合，对开发者有直接价值。

**继续验证**：关注新模型的实际表现和工具使用案例。

**原始来源**：rss · Simon Willison · 8月5日 06:00 北京时间 · [打开原文](https://simonwillison.net/2026/Aug/4/llm-anthropic/#atom-everything){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [PipeNetwork/minimax-h3-mlx](https://simonwillison.net/2026/Aug/4/minimax-h3-mlx/#atom-everything){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

MiniMax-H3 多模态模型被移植到 MLX，可在 Apple Silicon 上生成带音频的视频，Simon Willison 演示了运行过程。

**对做产品的启发**：MiniMax-H3 多模态模型被移植到 MLX，Simon Willison 在 Apple Silicon 上成功运行，展示了新模型能力，对产品创新有启发。

**继续验证**：关注 MiniMax-H3 的更多应用场景和性能表现。

**原始来源**：rss · Simon Willison · 8月5日 03:10 北京时间 · [打开原文](https://simonwillison.net/2026/Aug/4/minimax-h3-mlx/#atom-everything){:target="_blank" rel="noopener noreferrer"}

### [Deepseek V4 Flash 0731 Scores 50 On The Artificial Analysis Intelligence Index 10 Points Above Previous Deepseek V4 Flash](https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

DeepSeek V4 Flash 0731 在 Artificial Analysis 智能指数上得分 50，比上一版高 10 分，显示模型能力提升。

**对做产品的启发**：DeepSeek V4 Flash 新版本在 Artificial Analysis Intelligence Index 得分提升 10 分，属于模型能力基准测试更新，对模型选型有参考价值，但非产品案例。

**继续验证**：关注该版本的实际应用效果和 API 定价。

**原始来源**：public\_web · Artificial Analysis · 7月31日 08:00 北京时间 · [打开原文](https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Meet Wrinkles, an app that uncovers the hidden stories of the places around you](https://techcrunch.com/2026/08/04/meet-wrinkles-an-ai-app-that-uncovers-the-hidden-stories-of-the-places-around-you/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Wrinkles 是一款 AI 音频导览应用，通过揭示身边地点的隐藏历史故事，为用户提供沉浸式旅游体验。

**对做产品的启发**：AI 音频导览应用，有明确产品形态和用户场景，但缺乏用户反馈和构建细节，属于产品案例但增量有限。

**继续验证**：关注用户评价和实际使用效果。

**原始来源**：rss · Aisha Malik · 8月5日 03:34 北京时间 · [打开原文](https://techcrunch.com/2026/08/04/meet-wrinkles-an-ai-app-that-uncovers-the-hidden-stories-of-the-places-around-you/){:target="_blank" rel="noopener noreferrer"}

### [Skill packs are now available on skills.sh](https://vercel.com/changelog/skill-packs-are-now-available){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

skills.sh 推出技能包功能，可打包分享多个 Agent 技能，简化技能分发。

**对做产品的启发**：skills.sh 推出技能包功能，可打包和分享多个 Agent 技能，提升 Agent 技能复用性，对 Agent 开发有实际价值。

**继续验证**：关注技能包生态发展和采用情况

**原始来源**：rss · Andrew Qu · 8月4日 12:00 北京时间 · [打开原文](https://vercel.com/changelog/skill-packs-are-now-available){:target="_blank" rel="noopener noreferrer"}

### [Introducing our Artifacts Hub and Adoption Dashboard](https://www.interconnects.ai/p/introducing-our-artifacts-hub-and){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Interconnects 推出 Artifacts Hub 和采用率仪表盘，追踪开源模型趋势，帮助了解模型生态动态。

**对做产品的启发**：Interconnects 推出 Artifacts Hub 和 Adoption Dashboard，提供开源模型生态数据，对行业观察有价值，但非直接产品案例，评分 7.0。

**继续验证**：关注这些工具对模型选择的影响。

**原始来源**：newsletter · Nathan Lambert · 8月3日 22:03 北京时间 · [打开原文](https://www.interconnects.ai/p/introducing-our-artifacts-hub-and){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent：不只是回答问题，而是能自主规划多步骤并调用工具完成目标的 AI 系统
- **知识点**：Function Calling：大模型&#x27;伸出触角&#x27;——识别需要调外部工具时，生成结构化指令让程序去执行
- **知识点**：RAG（检索增强生成）：AI 先从外部知识库找相关信息，再基于找来的内容回答或行动，避免瞎编
- **知识点**：Agent：能自主规划步骤、调用工具完成任务的 AI 系统，不只是聊天
- **动手练习**：30 分钟：打开 ChatGPT 的&#x27;任务&#x27;功能（若已开放）或任何支持定时提醒的 AI 工具，设置一个重复任务如&#x27;每天早上 9 点总结我的日历并建议优先级&#x27;，观察它如何调用日历、生成摘要、是否需要你确认
- **动手练习**：跟着官方 example（GitHub 上的 Next.js 项目）跑起来，让 eve Agent 自动完成一个任务：打开一个测试网页 → 截图保存 → 点击按钮 → 填写表单 → 再截图对比，全程观察 Agent 怎么通过 snapshot 和 ref 一步步决策。

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
