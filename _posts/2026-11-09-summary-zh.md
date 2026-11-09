---
layout: default
title: "AI产品情报 · 2026-11-09"
date: 2026-11-09
lang: zh
---

**日期**：2026-11-09　 **更新时间**：2026-11-09 14:24 北京时间

> 从 90 条内容中筛选出 10 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Moomoo 报道 DeepSeek Harness 每日活跃用户 154 万，每日消耗 Token 约 92 万亿，数据与其它来源一致。
- Figma 产品经理 Ezra Mechaber 把个人 Claude Code 配置做成团队共享的 PM OS，包含 31 个技能，帮助产品经理用 AI 处理 Slack、写代码和做增长实验，展示了 AI 在日常产品工作中的真实用法。
- Lenny 采访了 Gemini 产品负责人 Tulsee Doshi，讨论为什么产品经理在 AI 时代再次变得重要；内容涉及前沿产品构建经验，对初学者有启发。
- Latent.Space 采访了斯坦福 CS146S 讲师 Mihail Eric，介绍课程如何让学生通过修改开源项目来学习 AI 原生工程；这对理解 AI 时代的产品开发技能有启发。
- Simon Willison 发现 AI 编码代理写的 PR 描述过于详尽，建议用 HTML details 标签折叠；这展示了 AI 辅助开发中的实际工作流问题。

<a id="product-teardown"></a>
## 产品拆解

### 1. [DeepSeek Harness 日活 154 万，单日消耗约 92 万亿 Token](https://news.google.com/rss/articles/CBMiXEFVX3lxTFBPY1dPWjZtQlYtM0RWWHMxVkJBZG5HNzZEUUFydG1hM2FjcVd4MXNMNjF6MUxPX2FSWkxXY1F3WUZiNmpyY1RpSFN4ZmdFdTVaWVZBX0Y1Ml9pNnN0?oc=5){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Moomoo 报道 DeepSeek Harness 每日活跃用户 154 万，每日消耗 Token 约 92 万亿，数据与其它来源一致。

**评分**：8.0 / 10　 **证据**：媒体报道

**产品 / 团队**：DeepSeek Harness / Moomoo

**目标用户**：开发者、想搭建自定义 AI 工作流的技术用户，以及使用现成插件的普通用户

**它是什么**：DeepSeek 开源的插件化 AI Agent（智能体）运行框架，用户可在桌面或网页端运行，通过安装插件扩展功能。

**用户问题**：用户想调用大模型完成复杂任务（如查资料、写代码、自动操作软件），但单一 AI 对话窗口功能固定，无法灵活组合不同能力

**使用流程**：
1. 安装 DeepSeek Harness（桌面应用或从代码启动网页版）
2. 在插件市场浏览并安装需要的插件（已有约 3.5 万个第三方插件）
3. 通过对话或配置让 Harness 调用一个或多个插件协作完成任务
4. Harness 自动调度插件、调用大模型，返回结果给用户

**AI 在做什么**：作为中央调度器，理解用户意图，决定调用哪些插件、如何组合它们，并生成最终回复

**怎么实现**：核心思路是&#x27;万物皆插件&#x27;——把每个功能（搜索、代码执行、文件读写等）都封装成独立插件，由一个叫 Cordis 的系统自动安装和解决插件之间的依赖关系。用户不用改 Harness 本体代码，装插件就能换能力。

**需要理解的知识点**：
1. Agent（智能体）：不只是聊天，而是能自主规划步骤、调用工具的 AI 系统
2. Function Calling（函数调用）：让大模型学会判断&#x27;现在该调用哪个外部工具&#x27;的机制
3. 开源生态：框架代码公开，第三方开发者可以写插件、扩功能，形成正循环

**动手练习**：访问 https://www.deepseek.com/en/harness/ 下载桌面版，安装后尝试从插件市场添加 1-2 个插件（如网页搜索或代码执行），输入一个需要多步骤的指令（例如&#x27;搜索今天科技新闻并总结成三点&#x27;），观察 Harness 是否会自动调用插件协作完成

**已知限制**：92 万亿 Token/日的具体统计口径未公开（是否包含所有插件内部调用、是否去重）；154 万日活的数据来源为媒体报道，非 DeepSeek 官方直接披露；第三方插件质量、审核机制未公开；Moomoo 作为金融资讯平台，其科技报道的原始信源链条不清晰

**原始来源**：google\_news · Moomoo · 11月9日 10:56 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMiXEFVX3lxTFBPY1dPWjZtQlYtM0RWWHMxVkJBZG5HNzZEUUFydG1hM2FjcVd4MXNMNjF6MUxPX2FSWkxXY1F3WUZiNmpyY1RpSFN4ZmdFdTVaWVZBX0Y1Ml9pNnN0?oc=5){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Figma 产品经理如何把 Claude Code 变成团队共享的 PM OS](https://www.lennysnewsletter.com/p/how-figmas-pms-actually-use-ai-every){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Figma 产品经理 Ezra Mechaber 把个人 Claude Code 配置做成团队共享的 PM OS，包含 31 个技能，帮助产品经理用 AI 处理 Slack、写代码和做增长实验，展示了 AI 在日常产品工作中的真实用法。

**评分**：8.6 / 10　 **证据**：一手信息

**产品 / 团队**：PM OS / Claire Vo

**目标用户**：Figma 内部产品经理；概念可迁移至其他产品团队

**它是什么**：Figma 增长 PM Ezra Mechaber 把个人 Claude Code 配置打包成 31 个可复用技能的共享代码仓库，供全公司 60-70 名产品经理日常使用

**用户问题**：PM 日常被 Slack 淹没、写代码门槛高、增长实验手动操作慢，且团队各自用 AI 没有统一标准，导致好经验无法复用

**使用流程**：
1. 在 Claude Code 中加载 PM OS 仓库，选择对应技能（如整理 Slack、写代码、做实验）
2. AI 读取上下文（Slack 线程、代码库、实验数据）自动执行或生成草稿
3. 人工检查关键节点（如 AutoXP 实验需一人确认后才上线）
4. 输出结果直接发到 Slack、Figma 或代码库，同时把新经验沉淀为新技能

**AI 在做什么**：AI 是&#x27;执行助手+初稿生成器&#x27;：按预定义技能处理重复劳动（如每天 6 次整理 Slack），但关键决策保留人工检查点

**怎么实现**：把 prompt 和工具调用封装成&#x27;技能&#x27;存进 Git 仓库，PM 像装 App 一样按需调用；不同技能可以组合（如先用&#x27;读 Slack&#x27;技能提取信息，再用&#x27;写代码&#x27;技能生成脚本），团队通过 PR 评审来迭代技能质量

**需要理解的知识点**：
1. Claude Code：Anthropic 出的命令行 AI 编程助手，可以直接操作你的代码仓库和文件系统
2. MCP（Model Context Protocol）：一种让 AI 安全连接外部工具的标准接口，比如让 AI 直接读写 Figma 文件
3. Function Calling：AI 不只是聊天，还能主动调用你定义的函数去执行实际操作（如发 Slack 消息、跑实验代码）

**动手练习**：用 Claude Code 或 Cursor 创建一个个人&#x27;每日启动&#x27;技能：写一段 prompt 让 AI 读取你指定的 3 个信息源（如邮件摘要、日历、一个文档），生成今日待办优先级，保存为可重复加载的配置文件

**已知限制**：31 个技能的具体 prompt 内容未公开；AutoXP 首次实验的&#x27;huge win&#x27;具体指标未披露；Jev 写作助手的实际采用率未公开；PM OS 是否开源或对外发布未说明

**原始来源**：newsletter · Claire Vo · 11月2日 21:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-figmas-pms-actually-use-ai-every){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [Figma 产品经理如何把 Claude Code 变成团队共享的 PM OS](https://www.lennysnewsletter.com/p/how-figmas-pms-actually-use-ai-every){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.6/10

Figma 产品经理 Ezra Mechaber 把个人 Claude Code 配置做成团队共享的 PM OS，包含 31 个技能，帮助产品经理用 AI 处理 Slack、写代码和做增长实验，展示了 AI 在日常产品工作中的真实用法。

**对做产品的启发**：Figma 产品经理 Ezra Mechaber 将个人 Claude Code 配置变成团队共享的 PM OS（31 个技能），有具体实践、工具和自动化增长实验案例，属于可迁移的构建者经验，对 AI 产品经理有直接参考价值。

**继续验证**：关注 PM OS 是否开源或公开技能列表，以及 AutoXP 实验的具体结果。

**原始来源**：newsletter · Claire Vo · 11月2日 21:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-figmas-pms-actually-use-ai-every){:target="_blank" rel="noopener noreferrer"}

### [Why PMs are suddenly valuable again \| Tulsee Doshi \(Head of Product, Gemini\)](https://www.lennysnewsletter.com/p/what-it-actually-takes-to-build-frontier){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Lenny 采访了 Gemini 产品负责人 Tulsee Doshi，讨论为什么产品经理在 AI 时代再次变得重要；内容涉及前沿产品构建经验，对初学者有启发。

**对做产品的启发**：Lenny 的 Newsletter 访谈 Gemini 产品负责人 Tulsee Doshi，讨论 AI 时代产品经理的价值，属于高信噪比行业观察，对转型 AI 产品经理有直接参考价值。

**继续验证**：关注访谈中提到的具体产品决策案例。

**原始来源**：newsletter · Lenny Rachitsky · 11月8日 21:31 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/what-it-actually-takes-to-build-frontier){:target="_blank" rel="noopener noreferrer"}

### [🎙️ How I AI: Grok vs. Dot vs. Muse vs. Duet + How Figma’s PMs actually use AI every day](https://www.lennysnewsletter.com/p/how-i-ai-grok-vs-dot-vs-muse-vs-duet){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Lenny Rachitsky 在播客中对比 Grok、Dot、Muse 和 Claude Duet 等 AI 产品，并讨论 Figma 产品经理日常如何使用 AI，适合了解产品使用场景但缺少一手构建细节。

**对做产品的启发**：Lenny 的播客对比多个 AI 产品，属于从业者分析，但内容为音频/视频，文字摘要有限，缺乏可验证的产品细节或构建过程；对产品经理有参考价值但增量有限。

**继续验证**：等待文字版详细拆解或产品经理的具体工作流案例。

**原始来源**：newsletter · Lenny Rachitsky · 11月3日 00:02 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-grok-vs-dot-vs-muse-vs-duet){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [\[One Million AI Engineer Special\] How Stanford Teaches AI-Native Engineering — Mihail Eric, Monaco](https://latent.space/p/one_million_ai_engineer_special_how_stanford_teaches_ai-native_engineering_mihail_eric_monaco/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Latent.Space 采访了斯坦福 CS146S 讲师 Mihail Eric，介绍课程如何让学生通过修改开源项目来学习 AI 原生工程；这对理解 AI 时代的产品开发技能有启发。

**对做产品的启发**：Latent.Space 访谈斯坦福 CS146S 课程讲师 Mihail Eric，讨论如何教授 AI 原生工程，包括让学生参与开源项目，属于高信噪比的教育与实践洞察。

**继续验证**：关注课程材料是否公开。

**原始来源**：rss · Latent.Space · 11月9日 05:23 北京时间 · [打开原文](https://latent.space/p/one_million_ai_engineer_special_how_stanford_teaches_ai-native_engineering_mihail_eric_monaco/){:target="_blank" rel="noopener noreferrer"}

### [Hide your slop PR descriptions behind &lt;details&gt;&lt;summary&gt;](https://simonwillison.net/2026/Nov/9/details-summary/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Simon Willison 发现 AI 编码代理写的 PR 描述过于详尽，建议用 HTML details 标签折叠；这展示了 AI 辅助开发中的实际工作流问题。

**对做产品的启发**：Simon Willison 分享使用 AI 编码代理生成 PR 描述的经验，并提出用 details 标签隐藏冗长描述，属于构建者的一手实践，对 AI 产品经理有迁移价值。

**继续验证**：观察其他开发者是否采纳类似做法。

**原始来源**：rss · Simon Willison · 11月9日 12:25 北京时间 · [打开原文](https://simonwillison.net/2026/Nov/9/details-summary/){:target="_blank" rel="noopener noreferrer"}

### [The Web Is More Than Enough, by Paul Ford](https://ftrain.com/aboard-the-web-is-more-than-enough){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Paul Ford 撰文认为 Web 技术已足够强大，HN 讨论中开发者分享用 Web 技术快速构建功能的经验；对理解产品开发趋势有参考价值。

**对做产品的启发**：Paul Ford 的文章讨论 Web 技术的能力，HN 讨论中有开发者分享使用 Web 技术构建产品的经验，对产品构建有间接启发。

**继续验证**：关注 Web 技术在新产品中的应用案例。

**原始来源**：hackernews · edward · 11月9日 03:48 北京时间 · [打开原文](https://ftrain.com/aboard-the-web-is-more-than-enough){:target="_blank" rel="noopener noreferrer"}

### [parse\_number\(\) as a SQLite extension: C vs Rust](https://simonwillison.net/2026/Nov/8/sqlite-parse-number-c-vs-rust/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Simon Willison 用 Claude 探索用 C 和 Rust 编写 SQLite 扩展的差异，并记录了代码大小和性能对比；这体现了 AI 辅助技术调研的实践。

**对做产品的启发**：Simon Willison 记录用 Claude 辅助研究 SQLite 扩展在 C 与 Rust 中的实现对比，展示了 AI 辅助技术调研的过程，对初学者有参考价值。

**继续验证**：关注该研究是否产出可复用的扩展。

**原始来源**：rss · Simon Willison · 11月9日 06:26 北京时间 · [打开原文](https://simonwillison.net/2026/Nov/8/sqlite-parse-number-c-vs-rust/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [openai/openai-agents-python released v0.24.0-alpha.7](https://github.com/openai/openai-agents-python/releases/tag/v0.24.0-alpha.7){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

OpenAI 发布 Agents SDK v0.24.0-alpha.7，让开发者能把对话存在自己存储里、给 Agent 加语音和文件搜索等工具，并控制上下文和用量，适合想动手搭 Agent 产品的人参考。

**对做产品的启发**：OpenAI Agents SDK 官方 alpha 发布，新增自定义存储会话、语音与托管工具、上下文与用量控制等能力，属于可迁移的 Agent 构建基础设施更新；但为 alpha 版本且偏工程细节，对初学者产品理解增量有限。

**继续验证**：关注正式版是否稳定 CustomStorage 与 voice 接口，以及是否有基于该 SDK 的公开产品案例。

**原始来源**：github · markstuart-oai · 11月8日 15:05 北京时间 · [打开原文](https://github.com/openai/openai-agents-python/releases/tag/v0.24.0-alpha.7){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Goldman Sachs is pulling Claude Code from its bankers and traders](https://www.thestateofai.com/news/goldman-sachs-claude-code-traders-bankers){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

高盛把 Claude Code 从银行家和交易员机器上撤下，HN 讨论指出编码 Agent 放在能接触客户和交易信息的电脑上太危险，同时按量计费也让企业难以控制成本。

**对做产品的启发**：高盛撤下 Claude Code 是真实企业落地信号，评论区揭示安全边界和按量计费痛点，对 AI 产品经理理解企业采用障碍有迁移价值；但非一手信源且无产品细节。

**继续验证**：关注高盛是否改用其他编码 Agent，以及 Anthropic 是否推出企业级隔离和计费方案。

**原始来源**：hackernews · TheWiggles · 11月9日 02:16 北京时间 · [打开原文](https://www.thestateofai.com/news/goldman-sachs-claude-code-traders-bankers){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent（智能体）：不只是聊天，而是能自主规划步骤、调用工具的 AI 系统
- **知识点**：Function Calling（函数调用）：让大模型学会判断&#x27;现在该调用哪个外部工具&#x27;的机制
- **知识点**：开源生态：框架代码公开，第三方开发者可以写插件、扩功能，形成正循环
- **知识点**：Claude Code：Anthropic 出的命令行 AI 编程助手，可以直接操作你的代码仓库和文件系统
- **动手练习**：访问 https://www.deepseek.com/en/harness/ 下载桌面版，安装后尝试从插件市场添加 1-2 个插件（如网页搜索或代码执行），输入一个需要多步骤的指令（例如&#x27;搜索今天科技新闻并总结成三点&#x27;），观察 Harness 是否会自动调用插件协作完成
- **动手练习**：用 Claude Code 或 Cursor 创建一个个人&#x27;每日启动&#x27;技能：写一段 prompt 让 AI 读取你指定的 3 个信息源（如邮件摘要、日历、一个文档），生成今日待办优先级，保存为可重复加载的配置文件

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
