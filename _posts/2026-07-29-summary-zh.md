---
layout: default
title: "AI产品情报 · 2026-07-29"
date: 2026-07-29
lang: zh
---

**日期**：2026-07-29　 **更新时间**：2026-07-29 09:54 北京时间

> 从 139 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Perplexity 将其 AI 代理工具 Personal Computer 扩展到 Windows，使 Windows 电脑能作为本地 AI 系统运行，访问本地文件和应用。
- OpenAI 发布报告展示科学家如何使用 AI 编码代理加速科学计算和软件开发。
- Lamoom 让你在 Claude 中运行或销售代理应用。
- Vercel Sandbox 新增 fork 功能，允许从快照分支创建新沙箱，便于代理开发和多租户场景。
- OpenAI Codex 发布 rust-v0.146.0，新增会话管理、Agent 插件支持和 WebSocket 远程连接等功能。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Perplexity 把 AI 代理工具 Personal Computer 带到 Windows](https://www.theverge.com/ai-artificial-intelligence/971750/perplexity-personal-computer-windows-ai-agents){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Perplexity 将其 AI 代理工具 Personal Computer 扩展到 Windows，使 Windows 电脑能作为本地 AI 系统运行，访问本地文件和应用。

**评分**：8.0 / 10　 **证据**：媒体报道

**产品 / 团队**：Personal Computer for Windows / Jess Weatherbed

**目标用户**：需要在 Windows 电脑上自动化处理本地文件、Excel、PPT、Word、Outlook、OneDrive 等任务的用户

**它是什么**：Perplexity 推出的本地 AI 代理工具，让 Windows 电脑变成能操作本地文件和微软办公软件的&quot;数字员工&quot;

**用户问题**：用户要在多个本地文件和微软应用之间手动切换、整理信息、执行重复操作，费时且容易出错

**使用流程**：
1. 在 Windows 电脑上下载安装 Perplexity 的 Personal Computer 工具
2. 授权 AI 访问本地文件和指定的微软应用（Excel、Word 等）
3. 用自然语言下达任务指令，比如&quot;把这份 Excel 数据汇总成 PPT&quot;
4. AI 自动在后台跨应用执行操作，用户检查并确认结果

**AI 在做什么**：作为&quot;通用数字员工&quot;，理解用户指令后，自主调用本地文件和应用程序完成跨软件任务

**怎么实现**：在用户的 Windows 电脑上常驻运行一个 AI 代理（Agent，即&quot;能自主行动的智能程序&quot;），它通过操作系统层面的权限直接读写本地文件、操控已安装的微软办公软件，而不是把所有数据上传到云端处理

**需要理解的知识点**：
1. Agent（智能代理）：不只是回答问题，还能自己决定调用什么工具、执行什么动作来完成目标的 AI 程序
2. 本地运行 vs 云端运行：数据留在自己电脑里处理，降低隐私泄露风险，但对电脑性能有要求
3. Function Calling（函数调用）：AI 不直接动手，而是学会&quot;调用&quot;外部程序或 API 来完成任务，就像人学会按遥控器开空调

**动手练习**：30 分钟体验：打开 Perplexity 官网的 Personal Computer for Windows 页面，对比它和 Mac 版的功能描述；再打开自己电脑的 Copilot 或任意 AI 助手，尝试用一句话指令让它帮你整理桌面某个文件夹的内容，观察 AI 能否直接操作本地文件——如果不行，思考还需要什么权限或工具才能实现

**已知限制**：未公开具体技术架构（是否完全本地运行模型、还是云端模型+本地执行）；未公开定价模式；未公开支持的具体 Windows 版本和硬件要求；The Verge 报道为第三方媒体信息，非 Perplexity 官方技术白皮书

**原始来源**：rss · Jess Weatherbed · 7月28日 20:30 北京时间 · [打开原文](https://www.theverge.com/ai-artificial-intelligence/971750/perplexity-personal-computer-windows-ai-agents){:target="_blank" rel="noopener noreferrer"}

---
### 2. [OpenAI 发布报告：科学家如何用 AI 编码代理加速科学计算](https://openai.com/index/scientific-computing-agentic-ai){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：OpenAI 发布报告展示科学家如何使用 AI 编码代理加速科学计算和软件开发。

**评分**：7.0 / 10　 **证据**：一手信息

**产品 / 团队**：Codex（OpenAI 的编码代理） / OpenAI News

**目标用户**：从事科学计算的科研人员（如基因组学等领域），以及需要编写、维护科研软件的工程团队

**它是什么**：OpenAI 发布的一份实地报告，展示科学家使用 AI 编码代理（Coding Agent）来现代化科学计算流程，加速软件开发和科研发现。

**用户问题**：传统科学计算软件开发周期长、维护成本高，科研人员需要同时精通领域知识和编程技能，难以快速迭代实验代码

**使用流程**：
1. 科学家在本地 IDE 或云端部署 OpenAI Codex 编码代理
2. 向代理描述科研计算任务（如基因组数据分析、算法实现）
3. 代理自动生成、重构或审查代码，并行处理多个子任务
4. 科学家验证结果，将代码集成到研究流程中

**AI 在做什么**：AI 编码代理负责理解自然语言描述的科学任务，自动编写、调试、重构和审查科研代码，相当于一个 24 小时在线的编程助手

**怎么实现**：核心思路是让 AI 代理像人类程序员一样工作：接收任务描述后，自主规划步骤、读写代码文件、运行测试、修复错误。Agent（智能代理）指能自主决策、调用工具并完成多步骤任务的 AI 系统，不同于单次问答的聊天机器人。

**需要理解的知识点**：
1. Agent（智能代理）：能自主规划、调用工具、完成多步骤任务的 AI 系统，不只是回答问题，而是能动手做事
2. Function Calling（函数调用）：AI 判断何时需要调用外部工具（如运行代码、查数据库）来完成任务的能力
3. RAG（检索增强生成）：AI 先从外部知识库检索相关信息，再生成回答，减少编造——科研场景中对准确性要求极高

**动手练习**：30 分钟体验：访问 OpenAI Codex（https://github.com/openai/codex），本地安装后，尝试让 Codex 完成一个简单科学计算任务，例如&#x27;用 Python 读取一个 CSV 文件，计算平均值并画出直方图&#x27;，观察它如何分解步骤、生成代码、运行并反馈结果

**已知限制**：报告未公开具体加速倍数、参与科学家数量、实验对照组设置；未说明 Codex 在科学计算中的错误率或幻觉（编造代码/数据）情况；基因组学之外的&#x27;等领域&#x27;具体涉及哪些学科未详细展开

**原始来源**：rss · OpenAI News · 7月29日 01:00 北京时间 · [打开原文](https://openai.com/index/scientific-computing-agentic-ai){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [Open models recap: more on Kimi K3, Qwen 3.8, Xi&#x27;s WAIC speech, distillation, the open-closed gap, and what&#x27;s next](https://www.interconnects.ai/p/open-models-recap-more-on-kimi-k3){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Nathan Lambert 和 Florian 讨论了开源模型的最新进展，包括 Kimi K3、GLM 5.2 等，以及中美模型竞争。

**对做产品的启发**：Nathan Lambert 对开源模型的深度回顾，涵盖 Kimi K3、Qwen 3.8 等，有行业洞察，但偏技术讨论。

**继续验证**：关注开源模型生态变化和具体模型发布。

**原始来源**：newsletter · Nathan Lambert · 7月22日 22:09 北京时间 · [打开原文](https://www.interconnects.ai/p/open-models-recap-more-on-kimi-k3){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [Codex from 0 to 10M Users: Building ChatGPT Work — Akshay Nathan, OpenAI](https://www.latent.space/p/chatgpt-work){:target="_blank" rel="noopener noreferrer"} ⭐️ 9.0/10

OpenAI 产品负责人 Akshay Nathan 分享 ChatGPT Work 从 0 到 1000 万用户的构建历程，涵盖 Sites、Memory、Subagents 等关键功能。

**对做产品的启发**：OpenAI 产品工程负责人分享 ChatGPT Work 从 0 到 1000 万用户的构建经验，包含具体功能如 Sites、Memory、Subagents 等，对产品经理极有价值。

**继续验证**：关注 ChatGPT Work 后续功能更新

**原始来源**：rss · Latent Space · 7月28日 23:26 北京时间 · [打开原文](https://www.latent.space/p/chatgpt-work){:target="_blank" rel="noopener noreferrer"}

### [Anatomy of a Frontier Lab Agent Intrusion: A Technical Timeline of the July 2026 Incident](https://simonwillison.net/2026/Jul/28/anatomy-of-a-frontier-lab-agent-intrusion/#atom-everything){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Hugging Face 详细披露了 OpenAI 代理入侵其基础设施的技术时间线，作为现代安全攻击的案例研究。

**对做产品的启发**：Hugging Face 发布详细技术时间线，分析 OpenAI 代理入侵事件，对安全实践有高价值，但非产品。

**继续验证**：关注 OpenAI 的后续修复措施

**原始来源**：rss · Simon Willison · 7月29日 05:28 北京时间 · [打开原文](https://simonwillison.net/2026/Jul/28/anatomy-of-a-frontier-lab-agent-intrusion/#atom-everything){:target="_blank" rel="noopener noreferrer"}

### [Quoting Akshat Bubna](https://simonwillison.net/2026/Jul/28/akshat-bubna/#atom-everything){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Modal CTO 解释其平台未被入侵，而是客户未认证端点被利用，强调安全实践。

**对做产品的启发**：Modal CTO 对 OpenAI 代理入侵事件的评论，涉及安全实践，对构建者有一定参考价值，但非直接产品。

**继续验证**：关注 OpenAI 的详细报告

**原始来源**：rss · Simon Willison · 7月29日 06:05 北京时间 · [打开原文](https://simonwillison.net/2026/Jul/28/akshat-bubna/#atom-everything){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude Opus 5](https://www.anthropic.com/news/claude-opus-5){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

Anthropic 发布 Claude Opus 5 模型，引发基准测试和编码代理性能讨论。

**对做产品的启发**：Anthropic 官方发布 Claude Opus 5 模型，结合 newsletter 确认是正式发布，对产品构建者有直接参考价值。

**继续验证**：关注模型性能评测及实际应用反馈

**原始来源**：public\_web · Anthropic News · 7月25日 10:03 北京时间 · [打开原文](https://www.anthropic.com/news/claude-opus-5){:target="_blank" rel="noopener noreferrer"}

### [Discovering Cryptographic Weaknesses with Claude](https://www.anthropic.com/research/discovering-cryptographic-weaknesses){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Anthropic 使用 Claude 成功发现密码学弱点，每次实验 API 成本约 10 万美元，展示了前沿模型能力。

**对做产品的启发**：Anthropic 官方研究展示 Claude 发现密码学弱点，成本约 10 万美元，属于模型能力前沿，但非直接产品，且成本高，初学者参考有限。

**继续验证**：关注该方法是否可复现或产品化

**原始来源**：hackernews · gslin · 7月29日 01:22 北京时间 · [打开原文](https://www.anthropic.com/research/discovering-cryptographic-weaknesses){:target="_blank" rel="noopener noreferrer"}

### [Gemini API Managed Agents: 3.6 Flash, hooks, and more](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Google 推出 Gemini API Managed Agents 新功能，支持 3.6 Flash 模型和 Hooks/Triggers。

**对做产品的启发**：Google 发布 Gemini API Managed Agents 更新，包含 3.6 Flash、Hooks 和 Triggers，属于产品功能更新，对构建 AI 代理有直接帮助。

**继续验证**：关注开发者社区的实际使用反馈。

**原始来源**：rss · Mariano Cocirio · 7月29日 00:00 北京时间 · [打开原文](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Lamoom](https://www.producthunt.com/products/lamoom){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Lamoom 让你在 Claude 中运行或销售代理应用。

**对做产品的启发**：Lamoom 是一个允许在 Claude 内运行代理应用或销售自己代理应用的产品，有明确产品描述和 Product Hunt 讨论，对初学者理解 AI 代理产品形态有参考价值。

**继续验证**：关注用户评价和实际使用案例。

**原始来源**：rss · Kate Yanchenko · 7月28日 13:45 北京时间 · [打开原文](https://www.producthunt.com/products/lamoom){:target="_blank" rel="noopener noreferrer"}

### [Vercel Sandbox supports forking](https://vercel.com/changelog/vercel-sandbox-supports-forking){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Vercel Sandbox 新增 fork 功能，允许从快照分支创建新沙箱，便于代理开发和多租户场景。

**对做产品的启发**：Vercel Sandbox 新增 fork 功能，对构建 AI 代理的开发者有实用价值，但属于基础设施更新，非直接面向用户的产品。

**继续验证**：关注社区使用案例

**原始来源**：rss · Harpreet Arora · 7月28日 12:00 北京时间 · [打开原文](https://vercel.com/changelog/vercel-sandbox-supports-forking){:target="_blank" rel="noopener noreferrer"}

### [openai/codex released rust-v0.146.0](https://github.com/openai/codex/releases/tag/rust-v0.146.0){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

OpenAI Codex 发布 rust-v0.146.0，新增会话管理、Agent 插件支持和 WebSocket 远程连接等功能。

**对做产品的启发**：OpenAI Codex 发布新版本，新增会话管理、Agent 插件、WebSocket 远程连接等功能，属于产品更新，有明确变更内容，但非全新产品，评分 7。

**继续验证**：关注 Agent 插件生态和远程执行能力对产品体验的影响。

**原始来源**：github · github-actions\[bot\] · 7月29日 09:42 北京时间 · [打开原文](https://github.com/openai/codex/releases/tag/rust-v0.146.0){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent（智能代理）：不只是回答问题，还能自己决定调用什么工具、执行什么动作来完成目标的 AI 程序
- **知识点**：本地运行 vs 云端运行：数据留在自己电脑里处理，降低隐私泄露风险，但对电脑性能有要求
- **知识点**：Function Calling（函数调用）：AI 不直接动手，而是学会&quot;调用&quot;外部程序或 API 来完成任务，就像人学会按遥控器开空调
- **知识点**：Agent（智能代理）：能自主规划、调用工具、完成多步骤任务的 AI 系统，不只是回答问题，而是能动手做事
- **动手练习**：30 分钟体验：打开 Perplexity 官网的 Personal Computer for Windows 页面，对比它和 Mac 版的功能描述；再打开自己电脑的 Copilot 或任意 AI 助手，尝试用一句话指令让它帮你整理桌面某个文件夹的内容，观察 AI 能否直接操作本地文件——如果不行，思考还需要什么权限或工具才能实现
- **动手练习**：30 分钟体验：访问 OpenAI Codex（https://github.com/openai/codex），本地安装后，尝试让 Codex 完成一个简单科学计算任务，例如&#x27;用 Python 读取一个 CSV 文件，计算平均值并画出直方图&#x27;，观察它如何分解步骤、生成代码、运行并反馈结果

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
