---
layout: default
title: "AI产品情报 · 2026-08-28"
date: 2026-08-28
lang: zh
---

**日期**：2026-08-28　 **更新时间**：2026-08-28 19:25 北京时间

> 从 137 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Google 在 AI Mode 中新增航班价格追踪和酒店预订功能，将 AI 从信息搜索升级为旅行代理，值得关注其如何改变用户旅行规划方式。
- Claude Code 发布 v2.1.248，新增受限模式、缓存 TTL 配置和自托管 runner 标签覆盖等功能，提升安全性和企业可用性。
- Google 的 AI 笔记应用 Gemini Notebook 新增 Expert Intelligence 功能，可导入 Google Play Books 书籍并提问、生成计划等。
- Vercel 宣布 Claude Managed Agents 现可通过 Chat SDK 运行，支持流式响应、活动源和跨平台部署。
- Vercel 的 AI SDK harness 层新增 Cursor 适配器，允许通过统一接口运行 Cursor 等编码代理。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Google 搜索 AI Mode 新增三种旅行规划与预订方式](https://blog.google/products-and-platforms/products/search/book-travel-ai-mode/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Google 在 AI Mode 中新增航班价格追踪和酒店预订功能，将 AI 从信息搜索升级为旅行代理，值得关注其如何改变用户旅行规划方式。

**评分**：8.5 / 10　 **证据**：一手信息

**产品 / 团队**：Google AI Mode / James Byers

**目标用户**：需要规划旅行、预订航班和酒店的 Google 搜索用户；目前主要面向美国 Google One AI Premium 订阅用户

**它是什么**：Google 搜索里的 AI Mode（AI 模式）新增了订机票、追价格、订酒店的功能，让 AI 不只是帮你搜信息，还能帮你处理旅行事务。

**用户问题**：以前搜旅行信息时，AI 只能给一堆链接和摘要，用户还得自己跳转到订票网站比价、下单；价格变了也不会提醒，得反复手动查询。

**使用流程**：
1. 用户在 Google 搜索中打开 AI Mode，用自然语言描述旅行需求（如&#x27;下周去东京的便宜航班&#x27;）
2. AI 展示航班或酒店选项，用户可直接选择并追踪价格变动
3. 价格达到预期时，AI 主动通知用户
4. 用户通过 AI Mode 完成预订流程，无需跳转多个网站

**AI 在做什么**：AI 作为&#x27;旅行代理&#x27;（Agent，能自主执行任务的 AI 助手），负责理解需求、检索实时信息、比较选项、执行预订动作，并持续监控价格变化主动提醒用户。

**怎么实现**：底层用 Gemini 模型做理解和推理，把用户的口语化请求转成结构化查询；再调用航班/酒店的实时数据 API 获取价格和空房信息；最后用 Function Calling（让 AI 能调用外部工具完成具体动作，比如下单、设提醒）来实际执行预订和追踪任务。

**需要理解的知识点**：
1. Agent：不只是回答问题，还能自己动手完成任务的 AI，比如这里 AI 自己去查价、下单、发提醒
2. Function Calling：给 AI 配&#x27;工具箱&#x27;，让它能调用外部系统的功能（如订票接口），从&#x27;说&#x27;变成&#x27;做&#x27;
3. RAG（检索增强生成）：AI 不是瞎编航班信息，而是实时去查最新的数据库/网页，再组织成回答

**动手练习**：打开 Google 搜索（需美国 IP 和 Google 账号），尝试用 AI Mode 输入一个具体旅行问题，对比它和普通搜索的结果差异；然后换不同问法（如加入预算、日期限制），观察 AI 如何调整回答，记录它是否给出了可点击的预订链接或追踪按钮。

**已知限制**：未公开具体覆盖哪些航空公司/酒店平台、是否收取服务费、价格追踪的精确频率、以及美国以外地区的上线时间；目前仍为实验性功能，依赖 Search Labs 逐步开放。

**原始来源**：rss · James Byers · 8月28日 00:00 北京时间 · [打开原文](https://blog.google/products-and-platforms/products/search/book-travel-ai-mode/){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Claude Code v2.1.248：新增受限模式、缓存配置与企业部署增强](https://github.com/anthropics/claude-code/releases/tag/v2.1.248){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Claude Code 发布 v2.1.248，新增受限模式、缓存 TTL 配置和自托管 runner 标签覆盖等功能，提升安全性和企业可用性。

**评分**：8.5 / 10　 **证据**：一手信息

**产品 / 团队**：Claude Code / ashwin-ant

**目标用户**：开发者、企业 IT/安全团队、需要自托管部署的组织

**它是什么**：Anthropic 开发的命令行 AI 编程助手，能在终端里理解代码库、改文件、跑命令

**用户问题**：AI 编程工具权限太大（能随便执行命令、访问网络），企业不敢用；多会话协作困难；缓存策略不可控；自托管 runner 标识混乱

**使用流程**：
1. 安装 Claude Code CLI，用 \`claude\` 启动会话
2. 需要安全环境时加 \`--restricted\` 启动，限制 AI 只能读写工作目录内的文件
3. 在 agent 配置文件的 frontmatter 里加 \`experimental.cacheTtl\` 控制提示缓存多久失效
4. 企业用户用 \`claude self-hosted-runner --client-label\` 给自托管 runner 打自定义标签，方便识别

**AI 在做什么**：在受限模式下，AI 只能做文件操作（读、写、搜索），不能执行系统命令或抓取网页；用户明确授权后才解除限制

**怎么实现**：通过启动参数和环境变量做&#x27;能力开关&#x27;——\`--restricted\` 相当于给 AI 一把&#x27;受限钥匙&#x27;，内部把危险工具（执行命令、网页抓取）从可用列表里删掉；缓存 TTL 是每次发请求时告诉模型&#x27;这段对话记忆保留多久&#x27;；runner 标签覆盖是在注册时把默认的主机名换成自定义标识，方便企业在面板里辨认

**需要理解的知识点**：
1. Agent（智能体）：让 AI 不仅能聊天，还能调用工具（如读文件、执行命令）自主完成任务的系统
2. Prompt Cache（提示缓存）：把已经处理过的长对话上下文存起来，下次直接复用，省时间和算钱；TTL 是&#x27;存活时间&#x27;，到期就扔掉重算
3. Function Calling（函数调用）：AI 不直接干活，而是生成&#x27;我要调用某某工具&#x27;的结构化请求，由外部系统安全地执行

**动手练习**：30 分钟动手：安装 Claude Code，创建一个测试文件夹，用 \`claude --restricted\` 启动，尝试让 AI 读文件夹内的文件（应该成功），再让它执行 \`ls\` 命令或访问网页（应该被拒绝），体验受限模式的安全边界；然后查看 \`~/.claude/CLAUDE.md\` 了解 frontmatter 配置格式

**已知限制**：未公开 \`--restricted\` 模式在企业 SSO/审计场景下的具体合规认证；\`experimental.cacheTtl\` 的&#x27;5m&#x27;/&#x27;1h&#x27; 之外是否支持其他时长未明确；跨会话消息（\`SendMessage\`/\`ListAgents\`）的 Bedrock/Vertex 实现细节未公开

**原始来源**：github · ashwin-ant · 8月28日 06:12 北京时间 · [打开原文](https://github.com/anthropics/claude-code/releases/tag/v2.1.248){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [not much happened today](https://news.smol.ai/issues/26-08-26-not-much/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Z.ai 正式发布 GLM-5.3-Flash，原生多模态，1M 上下文，320B 参数，MIT 许可，提供权重和 API。

**对做产品的启发**：AI 新闻简报报道 GLM-5.3-Flash 正式发布，包含模型参数、上下文窗口、MIT 许可等关键信息，属于新模型能力动态。

**继续验证**：关注模型实际性能和应用案例。

**原始来源**：newsletter · AI News · 8月26日 13:44 北京时间 · [打开原文](https://news.smol.ai/issues/26-08-26-not-much/){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [Breaking Claude Code Opus 5 Auto Mode](https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/){:target="_blank" rel="noopener noreferrer"} ⭐️ 9.0/10

研究者发现针对 Claude Code Auto Mode 的提示注入攻击，成功率 80%，可绕过安全机制执行恶意代码。

**对做产品的启发**：Simon Willison 报道了针对 Claude Code Auto Mode 的提示注入攻击，由知名研究者发现，涉及安全漏洞，对构建者重要。

**继续验证**：关注 Anthropic 的修复措施和 Auto Mode 的改进。

**原始来源**：rss · Simon Willison · 8月28日 06:50 北京时间 · [打开原文](https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Previewing the Model Hardware Standard](https://www.anthropic.com/news/model-hardware-standard-research-preview){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

Anthropic 预览模型硬件标准，让 AI 代理通过标准化命令控制硬件设备，但标准尚未公开，需申请访问。

**对做产品的启发**：Anthropic 发布模型硬件标准预览，是官方一手动态，且社区讨论指出标准尚未公开，需申请访问，属于早期信号但具有高价值，能解锁新的硬件交互产品体验。

**继续验证**：关注标准何时开源、具体实现细节及首批支持设备。

**原始来源**：hackernews · surprisetalk · 8月28日 02:04 北京时间 · [打开原文](https://www.anthropic.com/news/model-hardware-standard-research-preview){:target="_blank" rel="noopener noreferrer"}

### [Gemini Omni 1.1 Flash](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Google 发布 Gemini Omni 1.1 Flash，但用户反馈其无法将生成视频同步到已有音频，模型能力有局限，但仍是重要更新。

**对做产品的启发**：Google 发布 Gemini Omni 1.1 Flash，是模型能力更新，但评论指出其无法同步生成视频到已有音频，存在局限，但仍是重要模型动态。

**继续验证**：关注后续版本是否解决音频同步问题，以及开发者实际应用案例。

**原始来源**：hackernews · saretup · 8月28日 01:06 北京时间 · [打开原文](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/){:target="_blank" rel="noopener noreferrer"}

### [Agnes Ai Releases Agnes 2 5 Pro Beta](https://artificialanalysis.ai/articles/agnes-ai-releases-agnes-2-5-pro-beta){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Agnes AI 发布 Agnes 2.5 Pro Beta，但具体能力未详述。

**对做产品的启发**：Artificial Analysis 报道 Agnes AI 发布 Agnes 2.5 Pro Beta，属于第三方报道，但涉及新模型发布，可能解锁新能力，但缺乏具体细节，故评分中等。

**继续验证**：关注模型具体能力、基准测试及产品应用。

**原始来源**：public\_web · Artificial Analysis · 8月27日 08:00 北京时间 · [打开原文](https://artificialanalysis.ai/articles/agnes-ai-releases-agnes-2-5-pro-beta){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Google’s AI note-taking app now allows you to interact with books](https://www.theverge.com/tech/985567/google-gemini-notebook-expert-sources-books){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Google 的 AI 笔记应用 Gemini Notebook 新增 Expert Intelligence 功能，可导入 Google Play Books 书籍并提问、生成计划等。

**对做产品的启发**：Google Gemini Notebook 新增从 Google Play Books 导入书籍并交互的功能，是具体产品功能更新，有明确用户场景。

**继续验证**：观察该功能实际使用反馈及对学习场景的影响。

**原始来源**：rss · Emma Roth · 8月28日 03:30 北京时间 · [打开原文](https://www.theverge.com/tech/985567/google-gemini-notebook-expert-sources-books){:target="_blank" rel="noopener noreferrer"}

### [Run Claude Managed Agents with Chat SDK](https://vercel.com/changelog/claude-managed-agents-with-chat-sdk){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Vercel 宣布 Claude Managed Agents 现可通过 Chat SDK 运行，支持流式响应、活动源和跨平台部署。

**对做产品的启发**：Vercel 官方发布，Claude Managed Agents 与 Chat SDK 集成，提供具体功能，对开发者构建 agent 应用有直接帮助。

**继续验证**：观察开发者采用情况和实际应用案例。

**原始来源**：rss · Ben Sabic · 8月28日 08:00 北京时间 · [打开原文](https://vercel.com/changelog/claude-managed-agents-with-chat-sdk){:target="_blank" rel="noopener noreferrer"}

### [Cursor is now available in the AI SDK harness layer](https://vercel.com/changelog/cursor-ai-sdk-harness-adapter){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Vercel 的 AI SDK harness 层新增 Cursor 适配器，允许通过统一接口运行 Cursor 等编码代理。

**对做产品的启发**：Vercel 官方发布，AI SDK harness 层支持 Cursor，提供统一接口切换不同编码代理，对开发者有实际价值。

**继续验证**：关注更多 harness 适配器及开发者反馈。

**原始来源**：rss · Felix Arntz · 8月27日 22:47 北京时间 · [打开原文](https://vercel.com/changelog/cursor-ai-sdk-harness-adapter){:target="_blank" rel="noopener noreferrer"}

### [Expanding Support For Scientists](https://www.anthropic.com/news/expanding-support-for-scientists){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Anthropic 官方宣布扩展对科学家的支持，但具体内容未详述，值得关注其后续细节。

**对做产品的启发**：Anthropic 官方发布面向科学家的支持扩展，属于官方一手动态，可能涉及新产品或合作，但内容摘要过于简略，缺乏具体细节，故评分略低于 8。

**继续验证**：关注具体支持形式、合作机构及对科研 AI 产品的影响。

**原始来源**：public\_web · Anthropic News · 8月28日 18:42 北京时间 · [打开原文](https://www.anthropic.com/news/expanding-support-for-scientists){:target="_blank" rel="noopener noreferrer"}

### [Advancing Claude For Education](https://www.anthropic.com/news/advancing-claude-for-education){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Anthropic 宣布推进 Claude 在教育领域的应用，但具体功能或合作未详述。

**对做产品的启发**：Anthropic 官方推进 Claude 在教育领域的应用，属于官方一手动态，但内容摘要过于简略，缺乏具体细节，故评分中等偏上。

**继续验证**：关注教育场景的具体产品功能、合作院校及用户反馈。

**原始来源**：public\_web · Anthropic News · 8月27日 23:13 北京时间 · [打开原文](https://www.anthropic.com/news/advancing-claude-for-education){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent：不只是回答问题，还能自己动手完成任务的 AI，比如这里 AI 自己去查价、下单、发提醒
- **知识点**：Function Calling：给 AI 配&#x27;工具箱&#x27;，让它能调用外部系统的功能（如订票接口），从&#x27;说&#x27;变成&#x27;做&#x27;
- **知识点**：RAG（检索增强生成）：AI 不是瞎编航班信息，而是实时去查最新的数据库/网页，再组织成回答
- **知识点**：Agent（智能体）：让 AI 不仅能聊天，还能调用工具（如读文件、执行命令）自主完成任务的系统
- **动手练习**：打开 Google 搜索（需美国 IP 和 Google 账号），尝试用 AI Mode 输入一个具体旅行问题，对比它和普通搜索的结果差异；然后换不同问法（如加入预算、日期限制），观察 AI 如何调整回答，记录它是否给出了可点击的预订链接或追踪按钮。
- **动手练习**：30 分钟动手：安装 Claude Code，创建一个测试文件夹，用 \`claude --restricted\` 启动，尝试让 AI 读文件夹内的文件（应该成功），再让它执行 \`ls\` 命令或访问网页（应该被拒绝），体验受限模式的安全边界；然后查看 \`~/.claude/CLAUDE.md\` 了解 frontmatter 配置格式

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
