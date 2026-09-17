---
layout: default
title: "AI产品情报 · 2026-09-17"
date: 2026-09-17
lang: zh
---

**日期**：2026-09-17　 **更新时间**：2026-09-17 12:52 北京时间

> 从 157 条内容中筛选出 8 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Claire Vo 实测 Meta 新个人 AI Agent Muse，从注册、日历管理到购物和权限模型逐项体验，说明消费级 Agent 的产品体验该怎么做，对做个人 AI 产品的人可直接借鉴。
- Anthropic 把 Claude Cowork 和 Chat 合并成一个 Claude，解决用户在不同模式间切换的问题，值得看合并后产品体验和用户反馈。
- OpenAI 发布 AI 广告新形态 Sponsored Agents，并接入 HubSpot 和 Shopify，解决品牌在 AI 对话中触达用户的问题，对做 AI 商业化产品的人值得关注。
- Mem0 上架 Vercel Marketplace，让 AI Agent 记住用户偏好和上下文，并提供免费额度和每月 20 美元方案。
- GitHub 官方讲述如何用 Copilot 把 Copilot agent 运行时迁移到 80 万行生产级 Rust，展示 AI 在大型工程重构中具体承担什么工作，值得看它如何把 AI 嵌入真实开发流程。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Meta Muse 实测：一个把消费级体验做对的个人 AI Agent](https://www.lennysnewsletter.com/p/muse-review-the-personal-ai-agent){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Claire Vo 实测 Meta 新个人 AI Agent Muse，从注册、日历管理到购物和权限模型逐项体验，说明消费级 Agent 的产品体验该怎么做，对做个人 AI 产品的人可直接借鉴。

**评分**：8.6 / 10　 **证据**：已核验

**产品 / 团队**：Muse / Claire Vo

**目标用户**：注重生活管理的普通消费者，尤其是有家庭日程协调、个人目标追踪需求的用户；对消费级 AI 产品设计感兴趣的产品经理和开发者。

**它是什么**：Meta 推出的个人 AI Agent，能帮用户管理日历、生成家庭简报、设定个人目标、浏览器购物，并配有可自定义的动画虚拟形象。

**用户问题**：现有 AI 工具要么太技术化、需要手动拼接多个工具，要么在权限控制上让用户不放心，导致个人生活管理场景用起来不顺畅。

**使用流程**：
1. 注册并连接日历、新闻源等第三方服务，选择或自定义动画虚拟形象
2. 用自然语言下达任务，如&#x27;生成家庭早报 PDF&#x27;或&#x27;删除下周的足球训练&#x27;
3. 在 Activity Feed 中查看 AI 执行的每一步操作和工具调用记录
4. 对敏感操作（如购物、删日程）逐一确认或授权

**AI 在做什么**：AI 作为个人助理，理解自然语言指令后，自主调用日历、浏览器、文档生成等工具链完成任务，并通过可视化界面向用户透明展示每一步动作。

**怎么实现**：本质是一个&#x27;带透明操作日志的 Agent 编排层&#x27;——用户说一句话，Muse 拆解成多步子任务，每步调用对应工具（日历 API、网页浏览、PDF 生成），同时把&#x27;我在想什么、调了什么接口&#x27;实时展示给用户看，让用户觉得可控。

**需要理解的知识点**：
1. Agent（智能体）：不只是聊天，而是能自主规划步骤、调用工具帮你完成多环节任务的 AI 系统
2. Function Calling（函数调用）：AI 判断&#x27;现在该调日历 API 了&#x27;或&#x27;该打开浏览器了&#x27;的决策机制，是 Agent 能动手干活的关键
3. 权限模型：AI 执行敏感操作前要不要人确认，怎么设计既方便又安全，是消费级产品的核心体验问题

**动手练习**：用你常用的 AI（ChatGPT/Claude）模拟 Muse 的一个场景：给它你的真实或模拟日程，要求它&#x27;生成一份周末家庭活动简报 PDF 格式&#x27;，观察它是否能自主拆解步骤、是否需要你手动干预，对比 Muse 评测中提到的&#x27;Activity Feed 透明化&#x27;体验，记录 3 个让你感到&#x27;失控&#x27;或&#x27;放心&#x27;的瞬间。

**已知限制**：浏览器购物功能表现不稳定（买鞋失败、买票成功）；未公开 Muse 底层模型版本、是否使用 RAG 检索个人文档、企业级安全审计细节；动画虚拟形象的技术方案（预渲染/实时生成）未公开；目前为早期测试阶段，未公开正式商用时间。

**原始来源**：newsletter · Claire Vo · 9月16日 20:02 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/muse-review-the-personal-ai-agent){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Claude 合并聊天与工作模式：Cowork 和 Chat 合二为一](https://claude.com/blog/cowork-is-now-claude){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Anthropic 把 Claude Cowork 和 Chat 合并成一个 Claude，解决用户在不同模式间切换的问题，值得看合并后产品体验和用户反馈。

**评分**：7.6 / 10　 **证据**：一手信息

**产品 / 团队**：Claude / vertigoruntime

**目标用户**：需要既闲聊问答又做文档、幻灯片、代码等深度任务的知识工作者；未公开具体企业规模限制

**它是什么**：Anthropic 把之前分开的 Claude Chat（日常对话）和 Claude Cowork（深度工作/自动化）两个入口合并成单一产品界面

**用户问题**：用户得提前判断对话是&#x27;简单聊天&#x27;还是&#x27;复杂工作&#x27;，选错模式会得到差异很大的回答质量，还得在不同界面间来回切换

**使用流程**：
1. 打开统一后的 Claude，直接开始对话，不用选模式
2. Claude 根据对话内容自动判断需要调用本地文件、App 还是云端继续执行
3. 需要时直接使用 Claude Design/Docs/Slides 等功能输出成品
4. 关闭电脑后，Claude 可在云端继续运行任务，多端同步

**AI 在做什么**：自动识别对话意图，动态切换&#x27;轻量聊天&#x27;和&#x27;深度工作&#x27;两种行为策略，无需用户手动选择

**怎么实现**：本质是把两个产品的前端入口和后端调度逻辑打通，让同一个模型实例根据上下文自动加载不同的系统提示（system prompt）和工具集；合盖后继续运行则依赖云端持久化会话状态

**需要理解的知识点**：
1. System prompt：给 AI 的&#x27;隐形指令&#x27;，决定它是&#x27;闲聊语气&#x27;还是&#x27;严谨工作模式&#x27;
2. Agent：AI 能自主决定调用工具、多步骤执行，不只是你问一句它答一句
3. Function calling：AI 识别&#x27;我需要操作文件/生成幻灯片&#x27;并触发对应功能的能力

**动手练习**：打开 Claude，用同一个对话线程先问一个开放式问题（如&#x27;解释量子计算&#x27;），再让它基于回答生成一份简易幻灯片大纲，观察它是否自动切换行为风格；若无法访问，用任意 AI 对比&#x27;直接提问&#x27;和&#x27;加上请详细逐步分析&#x27;两种问法的效果差异

**已知限制**：合并后两种模式的具体触发机制未公开；Claude Design/Docs/Slides 是否全量开放、定价是否变化未公开；&#x27;合盖后继续工作&#x27;的云端环境细节和安全性说明未公开

**原始来源**：hackernews · vertigoruntime · 9月17日 00:26 北京时间 · [打开原文](https://claude.com/blog/cowork-is-now-claude){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [Meta Muse 实测：一个把消费级体验做对的个人 AI Agent](https://www.lennysnewsletter.com/p/muse-review-the-personal-ai-agent){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.6/10

Claire Vo 实测 Meta 新个人 AI Agent Muse，从注册、日历管理到购物和权限模型逐项体验，说明消费级 Agent 的产品体验该怎么做，对做个人 AI 产品的人可直接借鉴。

**对做产品的启发**：Claire Vo 对 Meta Muse 个人 AI Agent 做了数小时真实上手测试，覆盖 onboarding、日历、目标设定、家庭简报、浏览器购物与权限模型，属有真实使用反馈的产品评测，符合高价值标准。

**继续验证**：Muse 的权限模型与一次性生成能力是否可复用到其他个人 Agent 产品。

**原始来源**：newsletter · Claire Vo · 9月16日 20:02 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/muse-review-the-personal-ai-agent){:target="_blank" rel="noopener noreferrer"}

### [🎙️ How I AI: How two SpaceXAI designers use Grok Bot to do their jobs](https://www.lennysnewsletter.com/p/how-i-ai-how-two-spacexai-designers){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

两位 Grok Bot 设计师在播客里讲他们怎么用 AI agent 做个人网站和产品原型，对想动手做产品的人有直接参考价值。

**对做产品的启发**：Lenny Newsletter 的 How I AI 栏目，由 Grok Bot 设计师讲如何用 AI agent 搭建个人站点与产品原型，属于可迁移的构建者实践；但正文仅含节目预告与要点列表，缺少完整方法与证据，故未达 8 分。

**继续验证**：等完整节目/文字稿发布后，拆解其无 CMS、无 Figma 的具体工作流。

**原始来源**：newsletter · Lenny Rachitsky · 9月14日 23:03 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-how-two-spacexai-designers){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [Migrating the GitHub Copilot runtime to Rust, using Copilot](https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.6/10

GitHub 官方讲述如何用 Copilot 把 Copilot agent 运行时迁移到 80 万行生产级 Rust，展示 AI 在大型工程重构中具体承担什么工作，值得看它如何把 AI 嵌入真实开发流程。

**对做产品的启发**：GitHub 官方一手长文，讲用 Copilot 把 agent runtime 迁移到 80 万行生产级 Rust 的真实工程过程，属于构建者实践与产品开发过程，对初学者理解 AI 在真实工程中如何被使用有直接价值。

**继续验证**：关注迁移后的性能、稳定性数据以及 Copilot 在重构中的具体分工细节。

**原始来源**：rss · Stephen Toub · 9月17日 08:26 北京时间 · [打开原文](https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Google will now let any AI agent run your smart home](https://www.theverge.com/tech/996310/google-home-mcp-integration-agentic-ai-smart-home-price-release-date){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Google 通过 MCP 让 Claude 等第三方 AI agent 控制智能家居设备并分析家庭数据，解决 agent 接入真实设备的问题，值得看标准化协议如何打开新体验。

**对做产品的启发**：Google Home 开放 MCP 集成，允许第三方 AI agent 控制智能家居，属于新模型能力解锁的新产品体验，对做 AI 产品的人有直接参考价值。

**继续验证**：关注实际支持的 agent 列表、权限模型和用户实测反馈。

**原始来源**：rss · Jennifer Pattison Tuohy · 9月17日 01:00 北京时间 · [打开原文](https://www.theverge.com/tech/996310/google-home-mcp-integration-agentic-ai-smart-home-price-release-date){:target="_blank" rel="noopener noreferrer"}

### [\[AINews\] Jev: a “System One Model” that only decides/classifies/routes/scores — &gt;100x faster, &gt;200x cheaper than small frontier LLMs](https://www.latent.space/p/ainews-jev-a-system-one-model-that){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

TypeSafe 推出 Jev，一个只负责决策、分类、路由和打分的小模型，号称比小尺寸前沿模型快 100 倍、便宜 200 倍。

**对做产品的启发**：Jev 是只做决策、分类、路由和打分的“System One”小模型，宣称比小尺寸前沿 LLM 快 100 倍以上、便宜 200 倍以上，属于能直接催生新产品架构的模型能力方向；但正文只有一句祝贺，缺少可验证基准与使用方式，因此给 7.2 分。

**继续验证**：查找 Jev 的官方发布页与基准数据，验证速度与成本宣称，并观察是否可用于 Agent 前置路由。

**原始来源**：rss · Latent Space · 9月16日 19:09 北京时间 · [打开原文](https://www.latent.space/p/ainews-jev-a-system-one-model-that){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Reimagining advertising with AI](https://openai.com/index/reimagining-advertising-with-ai){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

OpenAI 发布 AI 广告新形态 Sponsored Agents，并接入 HubSpot 和 Shopify，解决品牌在 AI 对话中触达用户的问题，对做 AI 商业化产品的人值得关注。

**对做产品的启发**：OpenAI 推出 Sponsored Agents 等 AI 广告体验并接入 HubSpot、Shopify，属官方新产品形态发布，对做 AI 产品商业化的人有增量，但内容偏营销宣传，扣分后 7.2。

**继续验证**：Sponsored Agents 的实际形态、计费方式与商家接入门槛。

**原始来源**：rss · OpenAI News · 9月16日 21:00 北京时间 · [打开原文](https://openai.com/index/reimagining-advertising-with-ai){:target="_blank" rel="noopener noreferrer"}

### [Mem0 joins the Vercel Marketplace](https://vercel.com/changelog/mem0-joins-the-vercel-marketplace){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Mem0 上架 Vercel Marketplace，让 AI Agent 记住用户偏好和上下文，并提供免费额度和每月 20 美元方案。

**对做产品的启发**：Mem0 以原生集成方式进入 Vercel Marketplace，为 AI Agent 提供跨会话长期记忆，并附带免费额度和 20 美元/月方案，还有可直接部署的 eve Memory Agent 模板，属于可上手的产品案例；但本质是集成上架，创新增量有限，给 7.0 分。

**继续验证**：试用 eve Memory Agent 模板，评估长期记忆在个人产品中的实际效果与成本。

**原始来源**：rss · Tony Pan · 9月17日 01:00 北京时间 · [打开原文](https://vercel.com/changelog/mem0-joins-the-vercel-marketplace){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent（智能体）：不只是聊天，而是能自主规划步骤、调用工具帮你完成多环节任务的 AI 系统
- **知识点**：Function Calling（函数调用）：AI 判断&#x27;现在该调日历 API 了&#x27;或&#x27;该打开浏览器了&#x27;的决策机制，是 Agent 能动手干活的关键
- **知识点**：权限模型：AI 执行敏感操作前要不要人确认，怎么设计既方便又安全，是消费级产品的核心体验问题
- **知识点**：System prompt：给 AI 的&#x27;隐形指令&#x27;，决定它是&#x27;闲聊语气&#x27;还是&#x27;严谨工作模式&#x27;
- **动手练习**：用你常用的 AI（ChatGPT/Claude）模拟 Muse 的一个场景：给它你的真实或模拟日程，要求它&#x27;生成一份周末家庭活动简报 PDF 格式&#x27;，观察它是否能自主拆解步骤、是否需要你手动干预，对比 Muse 评测中提到的&#x27;Activity Feed 透明化&#x27;体验，记录 3 个让你感到&#x27;失控&#x27;或&#x27;放心&#x27;的瞬间。
- **动手练习**：打开 Claude，用同一个对话线程先问一个开放式问题（如&#x27;解释量子计算&#x27;），再让它基于回答生成一份简易幻灯片大纲，观察它是否自动切换行为风格；若无法访问，用任意 AI 对比&#x27;直接提问&#x27;和&#x27;加上请详细逐步分析&#x27;两种问法的效果差异

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
