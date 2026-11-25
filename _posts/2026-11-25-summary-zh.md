---
layout: default
title: "AI产品情报 · 2026-11-25"
date: 2026-11-25
lang: zh
---

**日期**：2026-11-25　 **更新时间**：2026-11-25 16:30 北京时间

> 从 178 条内容中筛选出 9 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- 沃尔玛与 Meta 合作，让顾客通过 Meta 的 AI 代理 Muse 购买黑五促销商品；这展示了 AI 代理直接参与零售交易的一种落地方式，值得关注其实际体验和转化效果。
- Anthropic 给 Claude Code 加了从 MCP 服务器加载技能的能力，让外部工具能直接变成斜杠命令，方便构建者把第三方服务接进编码 Agent。
- Canva 发布 MCP 接口，让任何 AI agent 都能调用 Canva 做设计，解决 agent 生成视觉内容的问题。
- Vercel 宣布所有 Sandbox 运行时改用托管镜像，默认包含 Node.js、Python 和 Claude Code 等编码 Agent，方便开发者快速搭建 Agent 运行环境。
- Simon Willison 在主题演讲中总结过去一年 LLM 和编码 Agent 的三个能力拐点，用 Claude Opus 4.5 等实例说明模型如何从玩具变成可交付工具。

<a id="product-teardown"></a>
## 产品拆解

### 1. [沃尔玛与 Meta 合作，让用户通过 AI 代理 Muse 购买黑五促销商品](https://techcrunch.com/2026/11/24/walmart-teams-up-with-meta-to-bring-black-friday-deals-to-ai-agent-muse/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：沃尔玛与 Meta 合作，让顾客通过 Meta 的 AI 代理 Muse 购买黑五促销商品；这展示了 AI 代理直接参与零售交易的一种落地方式，值得关注其实际体验和转化效果。

**评分**：7.2 / 10　 **证据**：媒体报道

**产品 / 团队**：Muse（Meta 的 AI 代理） / Lauren Forristal

**目标用户**：在 Meta 平台（如 Facebook、Messenger、Instagram）上购物的消费者

**它是什么**：沃尔玛接入 Meta 的 AI 代理 Muse，让用户可以直接在对话中完成黑五促销商品的浏览和购买

**用户问题**：黑五期间促销信息分散，用户需要在多个平台比价、切换 App、手动下单，流程繁琐

**使用流程**：
1. 用户在 Meta 平台（如 Messenger）打开 Muse 对话
2. 用自然语言告诉 Muse 想买的黑五商品（如&#x27;找 50 寸电视的最优折扣&#x27;）
3. Muse 展示沃尔玛的黑五促销商品，用户确认选择
4. 在对话内完成下单或跳转至沃尔玛完成支付

**AI 在做什么**：AI 代理（Agent，指能自主理解目标、调用工具并完成多步骤任务的 AI 系统）负责理解购物意图、检索商品信息、推荐匹配选项，并协助完成交易流程

**怎么实现**：Muse 作为 Meta 的 AI 代理，背后连接了沃尔玛的商品数据库和库存系统；用户用日常说话的方式表达需求，Muse 把这句话翻译成系统能理解的查询指令，找到对应商品后返回给用户，并在获得确认后推进下单。本质是把&#x27;搜索-比价-下单&#x27;的多个网页操作，压缩成一段对话完成

**需要理解的知识点**：
1. AI Agent：不只是回答问题，还能调用外部工具（如查库存、创建订单）并自主完成多步骤任务的 AI 系统
2. Function Calling：LLM 识别到&#x27;需要查商品&#x27;时，自动调用预设的 API 函数去外部系统取数据，而不是凭空编造答案
3. 电商接入 LLM 的核心难点：如何把自然语言（&#x27;便宜的红色羽绒服&#x27;）准确映射到商品数据库的筛选条件（价格区间、颜色、品类）

**动手练习**：打开 ChatGPT 或 Claude，尝试用 Function Calling 模拟一个购物助手：先写一段提示词让 AI 识别&#x27;买手机&#x27;意图，然后手动模拟调用一个虚构的&#x27;查库存 API&#x27;（用 JSON 格式返回假数据），观察 AI 如何整合 API 结果回复你。30 分钟即可体验&#x27;对话式电商&#x27;的核心逻辑

**已知限制**：具体技术对接方式（API 还是深度集成）、支付是否在 Meta 站内完成、用户实际转化率、是否支持退换货等售后流程，均未公开；报道来自 TechCrunch，无沃尔玛或 Meta 官方技术博客佐证

**原始来源**：rss · Lauren Forristal · 11月25日 05:32 北京时间 · [打开原文](https://techcrunch.com/2026/11/24/walmart-teams-up-with-meta-to-bring-black-friday-deals-to-ai-agent-muse/){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Claude Code v2.1.332：外部工具变斜杠命令，MCP 技能接入进入 Beta](https://github.com/anthropics/claude-code/releases/tag/v2.1.332){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Anthropic 给 Claude Code 加了从 MCP 服务器加载技能的能力，让外部工具能直接变成斜杠命令，方便构建者把第三方服务接进编码 Agent。

**评分**：7.2 / 10　 **证据**：一手信息

**产品 / 团队**：Claude Code / claude-code-publisher\[bot\]

**目标用户**：有 Claude 订阅的开发者，需要在终端或 VS Code 里用 AI 辅助写代码、跑项目的人

**它是什么**：Anthropic 的终端/IDE 编码 Agent，能读代码、改文件、跑命令，这次更新让第三方服务通过 MCP 协议变成可直接调用的「技能」

**用户问题**：以前 Claude Code 只能用它内置的工具，开发者想把自家 API、数据库、监控等外部服务接进来，得自己写复杂集成；现在第三方服务只要提供 MCP 服务器，就能像原生功能一样用

**使用流程**：
1. 找一个支持 MCP 的外部服务（比如文件系统、数据库、API），启动它的 MCP 服务器
2. 在 Claude Code 里配置连接该 MCP 服务器，技能自动出现在 \`/\` 菜单里，格式为 \`server:skill\`
3. 编码时按 \`/\` 选对应的技能，像用内置命令一样调用外部工具
4. 如果需要管控权限，用新增的 \`PreSkillShellCommand\` 钩子，在技能加载时拦截或拒绝危险 shell 命令

**AI 在做什么**：Claude 作为编码 Agent，理解用户意图后，自动调用合适的 MCP 技能执行操作（如查数据库、调 API），并把结果带回对话继续推理

**怎么实现**：MCP（Model Context Protocol，模型上下文协议）是 Anthropic 推的开放标准，相当于给 AI 工具定了「USB-C 接口」。第三方服务按 MCP 标准暴露功能，Claude Code 作为客户端去连，把对方的能力翻译成用户看得懂的斜杠命令。这次更新就是把这个连接器从实验状态推进到 Beta，让用户可用了

**需要理解的知识点**：
1. MCP：一种让 AI 应用统一接入外部工具的开放协议，类似 AI 世界的「USB-C」，避免每个工具都要写定制集成
2. Agent 工具生态：编码 Agent 不只是聊天，它需要「手」去操作外部世界，MCP 让这些「手」可以即插即用
3. Hook/钩子机制：在 AI 执行动作前插一道检查，用来做安全管控，比如拦住可能删库的命令

**动手练习**：30 分钟练习：① 安装 Claude Code CLI 并登录；② 找一个开源 MCP 服务器（如官方示例的 filesystem 或 sqlite）；③ 按 MCP 文档启动服务器，在 Claude Code 的 \`/\` 菜单里看到它；④ 尝试用该技能查一个本地文件或数据库，观察 AI 如何调用外部工具并返回结果

**已知限制**：MCP 技能功能标记为 beta，稳定性未承诺；PreSkillShellCommand 钩子的具体配置语法和权限粒度未在 release note 中详述；需要用户自行寻找或搭建 MCP 服务器，官方未提供统一市场或目录

**原始来源**：github · claude-code-publisher\[bot\] · 11月25日 09:32 北京时间 · [打开原文](https://github.com/anthropics/claude-code/releases/tag/v2.1.332){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

_最近 7 天没有达到收录标准的新 Newsletter 内容；请查看数据源日志。_

<a id="how-they-build"></a>
## 他们怎么做

### [Three LLM inflection points in twelve months](https://simonwillison.net/2026/Nov/24/llm-inflection-points/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.6/10

Simon Willison 在主题演讲中总结过去一年 LLM 和编码 Agent 的三个能力拐点，用 Claude Opus 4.5 等实例说明模型如何从玩具变成可交付工具。

**对做产品的启发**：Simon Willison 一手长文，系统梳理过去 12 个月 LLM 与编码 Agent 的三个拐点，包含 Claude Opus 4.5 等具体案例和亲历观察，对初学者理解能力演进和产品机会有高迁移价值，给 8.6 分。

**继续验证**：阅读全文并对照三个拐点，思考哪些能力可转化为个人产品机会。

**原始来源**：rss · Simon Willison · 11月25日 07:02 北京时间 · [打开原文](https://simonwillison.net/2026/Nov/24/llm-inflection-points/){:target="_blank" rel="noopener noreferrer"}

### [PenGPT: A Generative Transformer for Handwriting and Sketches](https://greydanus.github.io/2026/11/12/pengpt/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

研究者 Sam Greydanus 做了个能生成手写和涂鸦的模型 PenGPT 并公开了过程和 Demo，他坦言八成精力花在清洗数据上，给想动手做产品的人一个可复制的实践样本。

**对做产品的启发**：作者一手长文，公开了 PenGPT 的构建过程、数据策略和可交互 Demo，作者在评论区亲自说明把精力放在数据质量而非架构，符合构建者实践经验优先，对初学者理解“数据比技巧重要”很有迁移价值。

**继续验证**：关注作者后续是否开源代码或数据管线，以及社区复现反馈。

**原始来源**：hackernews · smusamashah · 11月25日 08:54 北京时间 · [打开原文](https://greydanus.github.io/2026/11/12/pengpt/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [GPT-6 models demonstrate intrinsic protein-design capabilities](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

OpenAI 展示 GPT-6.2 能根据蛋白质三维结构写代码设计 minibinder，再用专业模型补全序列，说明通用模型可参与专业科研流程。

**对做产品的启发**：OpenAI 官方发布 GPT-6 模型在蛋白质设计上的能力展示，属于模型公司一手动态；HN 讨论中有对实际设计环节的质疑，但整体展示了通用模型写代码解决专业问题的路径，对 AI 产品经理理解模型能力边界有参考价值。

**继续验证**：关注后续是否有实验室验证结果和完整技术报告，以及社区对设计有效性的讨论。

**原始来源**：hackernews · acossta · 11月25日 05:02 北京时间 · [打开原文](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/){:target="_blank" rel="noopener noreferrer"}

### [\[AINews\] Gemini 4 Neon marks GDM&#x27;s full return as a Frontier Lab](https://latent.space/p/ainews-gemini-4-neon-marks-gdm-s-full-return-as-a-frontier-lab/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Latent Space 报道 Gemini 4 Neon 在 LiveBench 上击败 Astra 和 Fable，并将 TS Rust 基准运行时间缩短 48.6%，标志 Google DeepMind 回归前沿实验室。

**对做产品的启发**：Latent Space 的 AINews 汇总 Gemini 4 Neon 发布及基准表现，属于模型能力动态，但为聚合 newsletter 且信息简短，给 7.8 分。

**继续验证**：关注 Gemini 4 Neon 的实际产品集成和开发者反馈，判断是否解锁新体验。

**原始来源**：rss · swyx .ai · 11月25日 12:29 北京时间 · [打开原文](https://latent.space/p/ainews-gemini-4-neon-marks-gdm-s-full-return-as-a-frontier-lab/){:target="_blank" rel="noopener noreferrer"}

### [Ternary Bonsai 2.5 27B](https://prismml.com/news/bonsai-2-5-27b){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

PrismML 发布三值量化小模型 Bonsai 2.5 27B，用户实测在 Mac 上能跑出 20 多 token/秒并支持长上下文，让个人开发者低成本做 Agent 编码成为可能。

**对做产品的启发**：小模型 Ternary Bonsai 2.5 27B 发布，HN 上有用户实测速度与 SWE-bench 表现，属于可验证的模型能力增量，对探索本地/低成本 Agent 产品有迁移价值，但证据来自社区实测而非官方基准。

**继续验证**：跟踪官方基准与更多真实 Agent 任务反馈，判断是否适合个人产品原型。

**原始来源**：hackernews · b0m · 11月25日 04:08 北京时间 · [打开原文](https://prismml.com/news/bonsai-2-5-27b){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Canva MCP](https://www.producthunt.com/products/canva){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Canva 发布 MCP 接口，让任何 AI agent 都能调用 Canva 做设计，解决 agent 生成视觉内容的问题。

**对做产品的启发**：Canva 推出 MCP 集成，让 AI agent 直接调用 Canva 创意能力，属于大产品的新功能发布，有明确使用场景，但描述简短，缺乏用户反馈。

**继续验证**：关注 MCP 文档和实际集成案例，评估对 agent 产品的影响。

**原始来源**：rss · Kate Ramakaieva · 11月24日 23:05 北京时间 · [打开原文](https://www.producthunt.com/products/canva){:target="_blank" rel="noopener noreferrer"}

### [All Sandbox runtimes now use Vercel Managed Images](https://vercel.com/changelog/all-sandbox-runtimes-now-use-vercel-managed-images){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Vercel 宣布所有 Sandbox 运行时改用托管镜像，默认包含 Node.js、Python 和 Claude Code 等编码 Agent，方便开发者快速搭建 Agent 运行环境。

**对做产品的启发**：Vercel 官方更新，Sandbox 运行时统一使用托管镜像并内置 Claude Code 等编码 Agent，属于开发者基础设施增量，对构建 Agent 产品有直接帮助，但偏底层，给 7 分。

**继续验证**：试用新镜像，评估其对个人 Agent 产品部署效率的提升。

**原始来源**：rss · Luke Phillips-Sheard · 11月25日 02:00 北京时间 · [打开原文](https://vercel.com/changelog/all-sandbox-runtimes-now-use-vercel-managed-images){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：AI Agent：不只是回答问题，还能调用外部工具（如查库存、创建订单）并自主完成多步骤任务的 AI 系统
- **知识点**：Function Calling：LLM 识别到&#x27;需要查商品&#x27;时，自动调用预设的 API 函数去外部系统取数据，而不是凭空编造答案
- **知识点**：电商接入 LLM 的核心难点：如何把自然语言（&#x27;便宜的红色羽绒服&#x27;）准确映射到商品数据库的筛选条件（价格区间、颜色、品类）
- **知识点**：MCP：一种让 AI 应用统一接入外部工具的开放协议，类似 AI 世界的「USB-C」，避免每个工具都要写定制集成
- **动手练习**：打开 ChatGPT 或 Claude，尝试用 Function Calling 模拟一个购物助手：先写一段提示词让 AI 识别&#x27;买手机&#x27;意图，然后手动模拟调用一个虚构的&#x27;查库存 API&#x27;（用 JSON 格式返回假数据），观察 AI 如何整合 API 结果回复你。30 分钟即可体验&#x27;对话式电商&#x27;的核心逻辑
- **动手练习**：30 分钟练习：① 安装 Claude Code CLI 并登录；② 找一个开源 MCP 服务器（如官方示例的 filesystem 或 sqlite）；③ 按 MCP 文档启动服务器，在 Claude Code 的 \`/\` 菜单里看到它；④ 尝试用该技能查一个本地文件或数据库，观察 AI 如何调用外部工具并返回结果

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
