---
layout: default
title: "AI产品情报 · 2026-09-28"
date: 2026-09-28
lang: zh
---

**日期**：2026-09-28　 **更新时间**：2026-09-28 13:23 北京时间

> 从 98 条内容中筛选出 7 条重要资讯。

> 今日高质量增量有限，因此未使用低质量内容补足数量。

<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- 音乐创业公司 Thoughtful Things 在 Kickstarter 发布 Engram 采样器，用 AI 把音频变形甚至生成幻觉声音，适合看 AI 如何嵌入硬件创作工具。
- OpenAI Codex 发布 rust-v0.158.0，新增 MCP OAuth 客户端密钥、图像透明背景生成、终端审批默认开启等功能，适合关注编码 Agent 工具链的人。
- 开发者把 DSPy 完整移植到 Erlang/BEAM 平台并发布成 Hex 包，让用 Elixir 的人也能用编程方式搭 LLM 应用。
- Simon Willison 引用 Muse AI Agent 替用户处理二手交易时自动回复出错、导致对方给差评的真实记录，适合看 Agent 产品在真实场景中的失败点。
- Anthropic 官方称 Claude 发现了一种新的酶系统，展示大模型在生物科学发现中的实际用途，值得关注 AI 在医药研发场景的产品化可能。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Engram：把 AI 音频幻觉变成音乐的采样器](https://www.theverge.com/ai-artificial-intelligence/1001193/engram-sampler-ai-hallucinations-music){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：音乐创业公司 Thoughtful Things 在 Kickstarter 发布 Engram 采样器，用 AI 把音频变形甚至生成幻觉声音，适合看 AI 如何嵌入硬件创作工具。

**评分**：7.2 / 10　 **证据**：早期信号

**产品 / 团队**：Engram / Terrence O’Brien

**目标用户**：电子音乐制作人、采样爱好者、想用手动硬件探索 AI 声音变形的音乐人

**它是什么**：一款带 AI 的硬件采样器/节奏机，能把输入的音频变形，甚至凭空生成新的声音

**用户问题**：传统采样器只能剪辑和回放已有声音，无法自动把音频扭曲成全新质感，或从&#x27;错误&#x27;中生成意外声音

**使用流程**：
1. 把外部音频（如人声、乐器）输入 Engram
2. 用旋钮/按键选择 AI 变形模式，让声音被拉伸、破碎或重组
3. 触发采样 pads 编排节奏和旋律
4. 导出或现场演奏最终片段

**AI 在做什么**：实时把输入音频进行非线性变形，或在低语义控制下&#x27;幻觉&#x27;出原输入里没有的新声音

**怎么实现**：未公开。推测是在本地或边缘设备上运行小型生成/变换模型，把音频特征空间里的&#x27;偏差&#x27;或采样噪声当作创意输出，而非像 Suno 那样直接生成完整歌曲

**需要理解的知识点**：
1. AI 幻觉：LLM 或生成模型输出与事实不符的内容；在这里被重新定义为&#x27;有用的错误&#x27;，变成声音设计的原料
2. 采样器（Sampler）：一种把声音录下来、切成片段、再用键盘或打击垫触发的电子乐器
3. Groovebox：集成了采样、音序器、效果器的 standalone 创作设备，不用电脑就能做节拍

**动手练习**：用免费网页工具（如 Google Magenta 的 Tone.js demo 或 Ableton Live 的 Spectral Resonator）导入一段人声，把参数推到极端值，记录 3 种&#x27;破音&#x27;效果，思考哪些&#x27;错误&#x27;可以变成音乐元素

**已知限制**：众筹阶段，无用户实测反馈；AI 模型大小、是否联网、本地/云端运算未公开；&#x27;幻觉&#x27;是营销用语还是技术术语不明确

**原始来源**：rss · Terrence O’Brien · 9月28日 04:46 北京时间 · [打开原文](https://www.theverge.com/ai-artificial-intelligence/1001193/engram-sampler-ai-hallucinations-music){:target="_blank" rel="noopener noreferrer"}

---
### 2. [OpenAI Codex 发布 Rust 版 v0.158.0：MCP OAuth 密钥、透明背景图像生成、终端审批默认开启](https://github.com/openai/codex/releases/tag/rust-v0.158.0){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：OpenAI Codex 发布 rust-v0.158.0，新增 MCP OAuth 客户端密钥、图像透明背景生成、终端审批默认开启等功能，适合关注编码 Agent 工具链的人。

**评分**：7.0 / 10　 **证据**：一手信息

**产品 / 团队**：OpenAI Codex / github-actions\[bot\]

**目标用户**：需要 AI 辅助编程的开发者，尤其是使用命令行工具或 IDE 插件、关注自动化编码工作流的技术团队

**它是什么**：OpenAI Codex 是一个能自动写代码、修 Bug 的 AI 编程助手（Agent），这次是其命令行工具（CLI）的 Rust 版本更新。

**用户问题**：开发者想让 AI 自动执行代码任务，但担心安全问题（比如 AI 执行高权限命令需要反复确认）、连接外部工具时认证麻烦、以及 AI 生成图像背景无法透明等细节控制不足

**使用流程**：
1. 安装 Codex CLI 并配置项目环境
2. 用自然语言描述需求（如&#x27;给这个函数加单元测试&#x27;），Codex 自动规划并执行
3. 高权限命令（如 sudo）默认需要终端审批，确认后 AI 继续运行
4. 需要时连接外部 MCP 服务（如数据库、API），通过 OAuth 密钥安全认证

**AI 在做什么**：理解用户意图后，自动编写/修改代码、调用工具、执行终端命令，并在敏感操作前等待人类确认

**怎么实现**：Codex 本质上是一个&#x27;有手脚的 LLM&#x27;——它把大模型的推理能力包装成可执行的动作循环：接收任务→规划步骤→调用工具（读文件、跑命令、连外部服务）→返回结果。这次更新主要加固了安全边界（默认审批、沙箱修复）和扩展了工具连接能力（MCP OAuth、WebSocket 认证）。MCP（Model Context Protocol）是一种让 AI 统一调用外部工具的标准协议，类似&#x27;AI 的 USB 接口&#x27;。

**需要理解的知识点**：
1. Agent：不只是聊天，而是能自主规划、执行多步骤任务并调用工具的 AI 系统
2. MCP（Model Context Protocol）：让 AI 以统一方式连接外部数据源和工具的开放协议，避免每个工具都要单独适配
3. Function Calling：LLM 识别需要调用外部功能时，输出结构化指令（如&#x27;运行 git status&#x27;）而非纯文本，让 AI 能实际操作软件

**动手练习**：30 分钟体验：在 GitHub Codespaces 或本地安装 Codex CLI（rust-v0.158.0），让它帮你给一个小项目（如 Python 计算器）添加单元测试，故意触发一个需要 sudo 权限的命令（如安装依赖），观察终端审批提示；然后尝试用 &#x27;codex mcp add&#x27; 连接一个公开的 MCP 服务（如文件系统工具），体验 OAuth 配置流程

**已知限制**：未公开具体支持的 MCP 服务列表；未公开透明背景图像生成背后的模型版本（DALL-E 3 或 4？）；未公开 WebSocket bearer token 的具体加密方案细节；&#x27;多 Agent v2 直接消息&#x27;功能标注为可禁用，但未公开其默认行为与稳定性

**原始来源**：github · github-actions\[bot\] · 9月28日 13:07 北京时间 · [打开原文](https://github.com/openai/codex/releases/tag/rust-v0.158.0){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

_最近 7 天没有达到收录标准的新 Newsletter 内容；请查看数据源日志。_

<a id="how-they-build"></a>
## 他们怎么做

### [Quoting Muse AI Agent](https://simonwillison.net/2026/Sep/28/muse-ai-agent/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Simon Willison 引用 Muse AI Agent 替用户处理二手交易时自动回复出错、导致对方给差评的真实记录，适合看 Agent 产品在真实场景中的失败点。

**对做产品的启发**：Simon Willison 引用 Muse AI Agent 真实运行记录，展示 Agent 自动回复出错、造成负面评价的具体案例，对理解 Agent 产品边界和失败模式很有价值，属于高信噪比一手实践观察。

**继续验证**：关注 Muse Agent 是否调整自动回复策略，以及更多真实运行案例。

**原始来源**：rss · Simon Willison · 9月28日 12:01 北京时间 · [打开原文](https://simonwillison.net/2026/Sep/28/muse-ai-agent/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude Discovers Novel Enzyme System](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Anthropic 官方称 Claude 发现了一种新的酶系统，展示大模型在生物科学发现中的实际用途，值得关注 AI 在医药研发场景的产品化可能。

**对做产品的启发**：Anthropic 官方发布 Claude 发现新酶系统的研究更新，属模型公司一手动态，且展示了模型在科学发现这一新场景中的实际能力，对探索垂直 AI 产品（尤其医药/生物）有直接启发。但正文仅有占位描述，缺少可验证细节与用户使用路径，故未进入 9 分区间。

**继续验证**：等待官方补充实验细节、可复现方法或合作方信息，判断是否可迁移为垂直科研产品。

**原始来源**：public\_web · Anthropic News · 9月24日 18:25 北京时间 · [打开原文](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"}

### [Ember-1](https://fireworks.ai/blog/ember-1){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Fireworks 发布了自研模型 Ember-1，让开发者多了一个可选的模型供应商，值得关注它是否带来新的产品体验。

**对做产品的启发**：Fireworks 发布自研模型 Ember-1，属于模型公司的一手能力动态，HN 400 分 199 评论说明有真实讨论；但正文缺失，只能从评论间接判断，且评论中夹杂大量无关内容，因此给到 7 分档而非更高。对初学者理解“模型公司自研模型”有增量。

**继续验证**：确认 Ember-1 的具体能力、定价与是否开放权重，以及是否有开发者用它做出产品。

**原始来源**：hackernews · gmays · 9月28日 01:31 北京时间 · [打开原文](https://fireworks.ai/blog/ember-1){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Imp is a full port of DSPy to the BEAM](https://github.com/deepfates/imp){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

开发者把 DSPy 完整移植到 Erlang/BEAM 平台并发布成 Hex 包，让用 Elixir 的人也能用编程方式搭 LLM 应用。

**对做产品的启发**：有人把 DSPy 完整移植到 BEAM 生态并发布到 Hex，属于有代码、有发布页的一手构建案例，对想理解“用编程而不是提示词来搭 LLM 应用”的初学者有参考价值；但受众偏窄，给到 7 分。

**继续验证**：看是否有真实项目用 Imp 落地，以及作者是否补充使用示例。

**原始来源**：hackernews · mpweiher · 9月28日 03:28 北京时间 · [打开原文](https://github.com/deepfates/imp){:target="_blank" rel="noopener noreferrer"}

### [2026 in LLMs \(so far\)](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Simon Willison 发布 2026 年 LLM 进展演讲的注释幻灯片，按时间线梳理今年关键趋势，适合初学者快速建立全局认知。

**对做产品的启发**：Simon Willison 的年度 LLM 趋势演讲笔记，属于高信噪比行业观察，能帮初学者建立年度脉络；但偏综述，非具体产品案例，给 7 分档。

**继续验证**：关注演讲中提到的具体产品案例和可复现的实践方法。

**原始来源**：rss · Simon Willison · 9月28日 07:54 北京时间 · [打开原文](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：AI 幻觉：LLM 或生成模型输出与事实不符的内容；在这里被重新定义为&#x27;有用的错误&#x27;，变成声音设计的原料
- **知识点**：采样器（Sampler）：一种把声音录下来、切成片段、再用键盘或打击垫触发的电子乐器
- **知识点**：Groovebox：集成了采样、音序器、效果器的 standalone 创作设备，不用电脑就能做节拍
- **知识点**：Agent：不只是聊天，而是能自主规划、执行多步骤任务并调用工具的 AI 系统
- **动手练习**：用免费网页工具（如 Google Magenta 的 Tone.js demo 或 Ableton Live 的 Spectral Resonator）导入一段人声，把参数推到极端值，记录 3 种&#x27;破音&#x27;效果，思考哪些&#x27;错误&#x27;可以变成音乐元素
- **动手练习**：30 分钟体验：在 GitHub Codespaces 或本地安装 Codex CLI（rust-v0.158.0），让它帮你给一个小项目（如 Python 计算器）添加单元测试，故意触发一个需要 sudo 权限的命令（如安装依赖），观察终端审批提示；然后尝试用 &#x27;codex mcp add&#x27; 连接一个公开的 MCP 服务（如文件系统工具），体验 OAuth 配置流程

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
