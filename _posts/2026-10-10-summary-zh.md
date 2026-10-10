---
layout: default
title: "AI产品情报 · 2026-10-10"
date: 2026-10-10
lang: zh
---

**日期**：2026-10-10　 **更新时间**：2026-10-10 13:52 北京时间

> 从 113 条内容中筛选出 10 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Instinct 用邀请制和短信界面做出热门 AI agent，现在要面对 Muse 的竞争，值得看它如何靠产品体验而非营销获客。
- Vercel 让 agent 能通过 CLI 搜索和购买域名，但最终确认权留给人，展示了 agent 权限设计的一种实用模式。
- OpenAI 发布 Sophos 使用 Daybreak 的案例，称威胁调查时间缩短 96%、52% 的 MDR 案件实现自动化并保留人工审核。
- OpenAI 称 Asana 用其模型在 Codex 中把浏览器 Agent 成本降低 76 倍、速度提升 5 倍，以向客户提供更强模型。
- OpenAI 产品负责人 Kath Korevec 讲她如何用 ChatGPT Sites 给团队搭事故指挥站点，并接入 Slack、Notion 连接器，展示了 AI 产品里连接器与插件机制怎么真正落地。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Instinct：不靠营销的短信 AI Agent，能否顶住 Muse 的竞争](https://www.theverge.com/tech/1008254/instinct-agent-ai-hands-on-muse-dots){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Instinct 用邀请制和短信界面做出热门 AI agent，现在要面对 Muse 的竞争，值得看它如何靠产品体验而非营销获客。

**评分**：8.2 / 10　 **证据**：媒体报道

**产品 / 团队**：Instinct / Allison Johnson

**目标用户**：想要简单、无学习成本地使用 AI 完成日常任务的人；未公开具体画像

**它是什么**：一个 2024 年 8 月发布的、靠邀请制和短信界面走红的 AI Agent 产品，没有官网和营销，用户通过发短信与 AI 互动让它执行任务。

**用户问题**：其他 AI 工具界面复杂、需要下载 App 或学习新操作方式，用户不想被功能淹没，只想像发短信一样自然地让 AI 做事

**使用流程**：
1. 获得邀请后，用手机短信或类似短信的界面与 Instinct 对话
2. 用自然语言告诉它想做什么（比如查信息、安排事项、执行线上任务）
3. Instinct 作为 Agent 自主拆解步骤并执行，过程中可能回复确认或结果
4. 用户继续对话或结束，无需打开其他应用

**AI 在做什么**：作为 Agent（智能体：能自主规划、调用工具、多步执行任务的 AI，不只是回答问题）接收指令、理解意图、自动完成线上操作或信息处理，通过短信返回结果

**怎么实现**：未公开。从体验反推，核心是把大语言模型的理解能力和任务执行能力，封装成用户最熟悉的短信交互形式，隐藏所有技术细节，让用户感觉像在跟一个人发短信办事。

**需要理解的知识点**：
1. Agent：不只是聊天的 AI，而是能自己决定步骤、调用工具（如搜索、订日历、发邮件）来完成你交给它的任务
2. 产品形态选择：同样的底层模型，用「短信界面」vs「复杂仪表盘」，面向的是完全不同的用户门槛和场景
3. 冷启动策略：邀请制+零营销可以在早期筛选高匹配用户、制造稀缺感，但长期能否规模化未验证

**动手练习**：打开你常用的 ChatGPT/Claude/通义千问，尝试用一条消息让它帮你完成一个多步骤任务（例如：&#x27;查明天北京天气，如果下雨就提醒我带伞，并把提醒加到日历&#x27;），观察它是否能自动拆解步骤、是否需要你手动确认。对比这种体验和你平时一问一答的区别。

**已知限制**：未公开具体技术架构（是否调用外部 API、是否使用 RAG、模型来源）；未公开用户规模和留存数据；与 Muse 的竞争结果尚无结论；短信界面的具体功能边界（能做什么、不能做什么）原文未详细展开

**原始来源**：rss · Allison Johnson · 10月9日 22:00 北京时间 · [打开原文](https://www.theverge.com/tech/1008254/instinct-agent-ai-hands-on-muse-dots){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Vercel CLI 新增 Agent 域名购买能力：可搜索比价，但花钱需人确认](https://vercel.com/changelog/agents-can-now-buy-domains-with-the-vercel-cli){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Vercel 让 agent 能通过 CLI 搜索和购买域名，但最终确认权留给人，展示了 agent 权限设计的一种实用模式。

**评分**：8.0 / 10　 **证据**：媒体报道

**产品 / 团队**：Vercel CLI / Esteban Suárez

**目标用户**：使用 Vercel 部署网站的开发者，以及正在构建 AI Agent 工作流的技术团队

**它是什么**：Vercel 官方给命令行工具加了一套 Agent 专用接口，让 AI 能帮你查域名、比价格、发起购买，但最终付款必须经你同意。

**用户问题**：开发者想让 Agent 自动完成

**使用流程**：
- 未公开

**AI 在做什么**：未公开

**怎么实现**：未公开

**需要理解的知识点**：
- 未公开

**动手练习**：未公开

**已知限制**：未公开

**原始来源**：rss · Esteban Suárez · 10月10日 04:24 北京时间 · [打开原文](https://vercel.com/changelog/agents-can-now-buy-domains-with-the-vercel-cli){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [How OpenAI uses ChatGPT Sites \(live at DevDay\!\) \| Kath Korevec \(Product Lead\)](https://www.lennysnewsletter.com/p/how-openai-uses-chatgpt-sites-live){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.6/10

OpenAI 产品负责人 Kath Korevec 讲她如何用 ChatGPT Sites 给团队搭事故指挥站点，并接入 Slack、Notion 连接器，展示了 AI 产品里连接器与插件机制怎么真正落地。

**对做产品的启发**：OpenAI 产品负责人一手讲述 ChatGPT Sites 内部构建与使用过程，含 Plugin Insights、MCP 插件托管、约 60 个连接器生态等具体实践，属于高价值构建者经验，可直接迁移到个人产品设计。

**继续验证**：跟进 Plugin Insights 与连接器生态的开放范围，以及个人开发者能否复用该模式。

**原始来源**：newsletter · Claire Vo · 10月5日 20:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-openai-uses-chatgpt-sites-live){:target="_blank" rel="noopener noreferrer"}

### [🎙️ How I AI: 8 real Jev use cases + How OpenAI uses ChatGPT Sites \(live at DevDay\!\) + Claire’s DevDay recap](https://www.lennysnewsletter.com/p/how-i-ai-8-real-jev-use-cases-how){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Lenny 汇总 8 个 Jev 真实用例和 OpenAI 内部用 ChatGPT Sites 的做法，帮初学者看清 AI 产品实际怎么被用起来。

**对做产品的启发**：Lenny 的 Newsletter 汇总 8 个 Jev 真实使用案例、OpenAI 如何用 ChatGPT Sites 以及 DevDay 复盘，属于有实践证据的构建者经验，对初学者理解‘解决什么问题、怎么用’有迁移价值；但为聚合型内容，非单一深度一手案例。

**继续验证**：跟进 Jev 用例中可复现的产品模式，以及 ChatGPT Sites 是否开放给普通开发者。

**原始来源**：newsletter · Lenny Rachitsky · 10月5日 23:03 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-8-real-jev-use-cases-how){:target="_blank" rel="noopener noreferrer"}

### [I expect rapid progress but not towards general superintelligence](https://www.interconnects.ai/p/i-expect-rapid-progress-but-not-towards){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Nathan Lambert 撰文判断 AI 会在工程与基础设施能力上快速进步但不会走向通用超级智能，提醒读者未来好想法比好执行更值钱。

**对做产品的启发**：Nathan Lambert 是知名 AI 研究者与 Newsletter 作者，本文提出一个可迁移的判断框架：模型在基础设施与工程能力上会快速超人，但模型本质不会因此剧变，好想法将比好执行更值钱。对 AI 产品经理理解&#x27;模型能力边界在哪、产品机会在哪&#x27;有直接启发，属于高信噪比行业观察，但无产品、代码或用户反馈等一手实践证据，故未达 8 分。

**继续验证**：关注作者后续是否给出更具体的产品/研究方向建议，以及社区对该判断的反驳。

**原始来源**：newsletter · Nathan Lambert · 10月10日 05:33 北京时间 · [打开原文](https://www.interconnects.ai/p/i-expect-rapid-progress-but-not-towards){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [A new feature for my blog, built using my voice](https://simonwillison.net/2026/Oct/9/built-using-my-voice/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

Simon Willison 用 Codex 语音模式边做饭边聊天，给自己的博客上线了 Newsletters 页面，展示了语音驱动开发的真实工作流。

**对做产品的启发**：Simon Willison 用 ChatGPT 桌面版 Codex 语音模式，几乎全程靠语音对话在本地开发环境里给自己的博客上线了 Newsletters 页面。属于构建者一手实践，清楚展示了 AI 在哪一步发挥作用、如何用语音驱动开发，对初学者理解 AI 辅助编程有高可迁移增量。

**继续验证**：关注 Codex 语音模式的更多实际使用案例，以及这种开发方式对产品原型的效率提升。

**原始来源**：rss · Simon Willison · 10月9日 20:54 北京时间 · [打开原文](https://simonwillison.net/2026/Oct/9/built-using-my-voice/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude Discovers Novel Enzyme System](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Anthropic 官方称 Claude 发现了一种新的酶系统，展示大模型在生物科学发现中的实际用途，值得关注 AI 在医药研发场景的产品化可能。

**对做产品的启发**：Anthropic 官方发布 Claude 发现新酶系统的研究更新，属模型公司一手动态，且展示了模型在科学发现这一新场景中的实际能力，对探索垂直 AI 产品（尤其医药/生物）有直接启发。但正文仅有占位描述，缺少可验证细节与用户使用路径，故未进入 9 分区间。

**继续验证**：等待官方补充实验细节、可复现方法或合作方信息，判断是否可迁移为垂直科研产品。

**原始来源**：public\_web · Anthropic News · 10月7日 16:55 北京时间 · [打开原文](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"}

### [Why AlphaFold Didn&#x27;t Solve Protein Folding — Pushmeet Kohli, Google DeepMind &amp; Sal Candido, Biohub](https://www.latent.space/p/biohub-deepmind){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

DeepMind 和 Biohub 的研究者讨论 AlphaFold 为何没有真正解决蛋白质折叠，帮助理解 AI 在生物医药中的真实能力边界。

**对做产品的启发**：DeepMind 的 Pushmeet Kohli 和 Biohub 的 Sal Candido 讨论 AlphaFold 为何没有真正解决蛋白质折叠，属于医药健康垂直 AI 的一手研发视角，对理解 AI 在生物医药中的真实边界有增量，但内容偏研究讨论，产品落地证据有限。

**继续验证**：关注该讨论中提到的未解问题和后续是否有新产品或工具落地。

**原始来源**：rss · Latent Space · 10月10日 08:31 北京时间 · [打开原文](https://www.latent.space/p/biohub-deepmind){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Sophos cuts threat investigation time by 96% with OpenAI Daybreak](https://openai.com/index/sophos){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

OpenAI 发布 Sophos 使用 Daybreak 的案例，称威胁调查时间缩短 96%、52% 的 MDR 案件实现自动化并保留人工审核。

**对做产品的启发**：OpenAI 官方客户案例，给出可量化指标：威胁调查时间缩短 96%、52% 的 MDR 用例自动化并保留人工监督。属于有真实客户与关键指标的落地案例，对理解&#x27;AI 在安全运营哪一步发挥作用&#x27;有参考价值；但本质是官方营销型案例，缺少用户侧独立验证与实现细节，故扣分至 7 分区间。

**继续验证**：关注是否有第三方复现或 Sophos 侧更详细的技术说明，以及 Daybreak 的产品定位与定价。

**原始来源**：rss · OpenAI News · 10月9日 15:00 北京时间 · [打开原文](https://openai.com/index/sophos){:target="_blank" rel="noopener noreferrer"}

### [Asana cuts model costs 76x in browser tests with GPT-6.1 Sol](https://openai.com/index/asana-browser-agent){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

OpenAI 称 Asana 用其模型在 Codex 中把浏览器 Agent 成本降低 76 倍、速度提升 5 倍，以向客户提供更强模型。

**对做产品的启发**：OpenAI 官方客户案例，给出模型成本降低 76 倍、速度提升 5 倍的可量化结果，涉及浏览器 Agent 这一产品形态，对做 Agent 产品的初学者有成本结构层面的启发。但正文极短、无实现细节，且标题中模型名称前后不一致（GPT-6.1 Sol / GPT-6 Astra），信息可靠性存疑，属官方营销内容，故压在 7 分。

**继续验证**：核实模型名称与版本，关注 Asana 是否公开浏览器 Agent 的技术实现与真实用户反馈。

**原始来源**：rss · OpenAI News · 10月9日 15:00 北京时间 · [打开原文](https://openai.com/index/asana-browser-agent){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent：不只是聊天的 AI，而是能自己决定步骤、调用工具（如搜索、订日历、发邮件）来完成你交给它的任务
- **知识点**：产品形态选择：同样的底层模型，用「短信界面」vs「复杂仪表盘」，面向的是完全不同的用户门槛和场景
- **知识点**：冷启动策略：邀请制+零营销可以在早期筛选高匹配用户、制造稀缺感，但长期能否规模化未验证
- **动手练习**：打开你常用的 ChatGPT/Claude/通义千问，尝试用一条消息让它帮你完成一个多步骤任务（例如：&#x27;查明天北京天气，如果下雨就提醒我带伞，并把提醒加到日历&#x27;），观察它是否能自动拆解步骤、是否需要你手动确认。对比这种体验和你平时一问一答的区别。

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
