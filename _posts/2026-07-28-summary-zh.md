---
layout: default
title: "AI产品情报 · 2026-07-28"
date: 2026-07-28
lang: zh
---

**日期**：2026-07-28　 **更新时间**：2026-07-28 11:50 北京时间

> 从 130 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Vercel 发布 DeepsecBench 基准，评估模型查找代码漏洞的能力，提供召回率、精度、成本等指标。
- 微软推出首个网络安全 AI 模型和新的代理网络安全系统。
- Artificial Analysis 评测了 Thinking Machines Lab 的 Inkling 在 agentic 知识工作上的表现，值得关注其产品能力。
- Lovable 分享运行 AI 黑客代理群组进行自我安全测试的实践经验。
- Maddie Reese 分享了她从零编程背景到使用 Cursor 和 Raspberry Pi 构建硬件产品的经验，展示了 AI 在硬件开发中的实际应用。

<a id="product-teardown"></a>
## 产品拆解

### 1. [DeepsecBench：让 AI 模型比一比谁能更快更省地找出代码里的安全漏洞](https://vercel.com/blog/deepsecbench-evaluating-model-performance-in-finding-cybersecurity-vulnerabilities){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Vercel 发布 DeepsecBench 基准，评估模型查找代码漏洞的能力，提供召回率、精度、成本等指标。

**评分**：8.0 / 10　 **证据**：一手信息

**产品 / 团队**：DeepsecBench / Eric Dodds

**目标用户**：需要在代码上线前自动扫描安全漏洞的开发团队、安全工程师，以及想挑选合适 AI 模型的 AI 产品经理

**它是什么**：Vercel 发布的一个公开排行榜，专门测试各种大语言模型在真实开源代码里找安全漏洞的能力，同时告诉你花多少钱、用多少时间。

**用户问题**：以前不知道哪个 AI 模型查漏洞又快又准又便宜，只能盲目选最贵的；而且漏掉漏洞代价极高，误报太多又会浪费工程师时间

**使用流程**：
1. 在 DeepsecBench 网页查看各模型的排行榜，对比分数、成本、耗时
2. 根据你的代码复杂度和预算，选择 1-3 个模型组合（比如高精准+低成本搭配）
3. 通过 Vercel AI Gateway 调用选中的模型，扫描自己的代码仓库
4. 根据报告修复漏洞，定期重新扫描或调整模型配置

**AI 在做什么**：AI 负责读取代码、分析潜在安全漏洞、输出问题位置和类型；另一个 AI 裁判负责判断 AI 找到的漏洞是否真实存在

**怎么实现**：核心思路是&#x27;考前不泄题&#x27;：找一个真实开源项目，截取&#x27;漏洞刚被修复前&#x27;的那个代码版本，人工标记出 231 个真实漏洞作为标准答案。模型来考试，看它找回多少标准答案（召回率），以及额外报的漏洞有多少是真的（精确率）。为了防止模型靠记忆作弊，考卷内容保密，不公开是哪个项目、哪个版本。

**需要理解的知识点**：
1. 召回率（Recall）：模型找出了多少真实存在的漏洞，漏掉就是风险；精确率（Precision）：模型报的漏洞里有多少是真的，误报就是浪费人力
2. F2 分数：一种给召回率&#x27;加权重&#x27;的算法，因为安全场景里漏掉漏洞比误报更危险，所以召回率比精确率重要两倍
3. AI Gateway：一个统一入口，让你可以像切换水电一样，在同一个接口换不同的 AI 模型，方便比价和组合使用

**动手练习**：访问 https://vercel.com/ai-gateway/leaderboards/deepsecbench ，对比 GPT-5.6 Sol（最高分$55.98）和 Grok 4.5（$5.60）的分数、召回率、精确率、时间。假设你每月预算$100、代码量中等，写一段 200 字的选型建议，说明你会选哪个模型、什么配置、多久扫一次，并解释为什么。

**已知限制**：Vercel 未公开具体使用哪个开源仓库和哪个 commit，无法独立验证&#x27;防作弊&#x27;效果；排行榜中部分模型名称（如 GPT-5.6 Sol、Claude Opus 5、Grok 4.5）与主流公开命名不一致，是否为内部代号或笔误未确认；Anthropic 的 Fable 5 模型因拒绝安全相关工作未参与测试；文中提到&#x27;GPT-5.6 Sol 中等配置得 25.10 分&#x27;但表格未展示该行数据

**原始来源**：rss · Eric Dodds · 7月27日 12:00 北京时间 · [打开原文](https://vercel.com/blog/deepsecbench-evaluating-model-performance-in-finding-cybersecurity-vulnerabilities){:target="_blank" rel="noopener noreferrer"}

---
### 2. [微软推出首个网络安全 AI 模型和代理式网络安全系统](https://techcrunch.com/2026/07/27/microsoft-launches-its-first-cyber-model-and-a-new-agentic-cybersecurity-system/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：微软推出首个网络安全 AI 模型和新的代理网络安全系统。

**评分**：7.5 / 10　 **证据**：媒体报道

**产品 / 团队**：未公开（官方未给出独立产品名，属于 Microsoft Security Copilot 生态扩展） / Lucas Ropek

**目标用户**：企业安全团队、安全分析师

**它是什么**：微软发布的首个专门用于网络安全的 AI 模型，以及一个能自主执行安全任务的代理系统

**用户问题**：安全分析师面对海量告警和复杂攻击时，手动调查耗时数小时，难以快速识别威胁和响应

**使用流程**：
1. 安全分析师用自然语言描述可疑事件或提问
2. AI 模型分析安全数据并生成威胁摘要与调查建议
3. 代理系统自动执行预设的安全操作（如隔离设备、收集证据）
4. 分析师审核结果并决定后续行动

**AI 在做什么**：AI 负责解析自然语言查询、关联安全数据生成洞察，并由代理自主执行标准化安全任务

**怎么实现**：把网络安全领域的日志、告警、威胁情报等数据&#x27;喂&#x27;给专门训练的 AI 模型，让它学会识别攻击模式；同时给 AI 配备&#x27;代理&#x27;身份，在限定权限内能自己调用安全工具干活，不用每件事都等人批准

**需要理解的知识点**：
1. Agent（代理）：AI 不只是回答问题，还能被授权在系统里实际执行操作，比如自动封禁可疑账号
2. 垂直领域模型：通用 AI 不懂安全行话，需要在专门的安全数据上训练才能看懂告警日志
3. Function Calling（函数调用）：AI 判断该做什么后，通过调用预定义的安全工具函数来完成实际操作

**动手练习**：注册 Microsoft Security Copilot 免费试用（需企业身份），输入一个模拟告警的自然语言描述，观察 AI 如何解析并给出调查步骤；对比手动查阅原始日志的效率差异

**已知限制**：新模型的具体参数量、训练数据来源、代理系统的权限边界和误操作防护机制均未公开；与现有 Security Copilot 的功能重叠程度不明

**原始来源**：rss · Lucas Ropek · 7月28日 02:32 北京时间 · [打开原文](https://techcrunch.com/2026/07/27/microsoft-launches-its-first-cyber-model-and-a-new-agentic-cybersecurity-system/){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [From zero coding background to hardware hacker: How Cursor + a Raspberry Pi makes AI fun](https://www.lennysnewsletter.com/p/from-zero-coding-background-to-hardware){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Maddie Reese 分享了她从零编程背景到使用 Cursor 和 Raspberry Pi 构建硬件产品的经验，展示了 AI 在硬件开发中的实际应用。

**对做产品的启发**：零编程背景的 Maddie Reese 使用 Cursor 和 Raspberry Pi 构建硬件项目，展示了 AI 辅助硬件开发的真实案例，对产品经理有启发。

**继续验证**：关注 Maddie Reese 的具体项目细节和 Cursor 在硬件开发中的更多案例。

**原始来源**：newsletter · Claire Vo · 7月27日 20:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/from-zero-coding-background-to-hardware){:target="_blank" rel="noopener noreferrer"}

### [Anthropic’s first technical PM on token maxing, the jagged edge, and living in the future \| Dianne Penn](https://www.lennysnewsletter.com/p/anthropics-first-technical-pm-on){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Anthropic 首位技术 PM Dianne Penn 分享了她对 token maxing、jagged edge 等概念的理解，以及如何生活在未来。

**对做产品的启发**：Anthropic 首位技术 PM Dianne Penn 的访谈，涉及 token maxing、jagged edge 等产品理念，对 AI 产品经理有高价值。

**继续验证**：关注 Dianne Penn 的具体产品方法论和 Anthropic 的产品方向。

**原始来源**：newsletter · Lenny Rachitsky · 7月26日 20:32 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/anthropics-first-technical-pm-on){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [How We Run Swarms Of Ai Hacking Agents Against Ourselves](https://lovable.dev/blog/how-we-run-swarms-of-ai-hacking-agents-against-ourselves){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Lovable 分享运行 AI 黑客代理群组进行自我安全测试的实践经验。

**对做产品的启发**：Lovable 官方博客分享如何运行 AI 黑客代理群组进行自我测试，对构建安全 Agent 有实践参考价值。

**继续验证**：关注具体技术细节和效果

**原始来源**：public\_web · Lovable Blog · 7月24日 22:30 北京时间 · [打开原文](https://lovable.dev/blog/how-we-run-swarms-of-ai-hacking-agents-against-ourselves){:target="_blank" rel="noopener noreferrer"}

### [The harness is all you need \(mostly\)](https://github.blog/ai-and-ml/github-copilot/the-harness-is-all-you-need-mostly/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

GitHub 官方博客介绍使用 Copilot 进行原型设计、规划、实现和审查的实用工作流。

**对做产品的启发**：GitHub 官方博客，提供 Copilot 实用工作流，对初学者有参考价值，但非新产品发布。

**继续验证**：可关注后续是否有更多实战案例。

**原始来源**：rss · Burke Holland · 7月28日 02:00 北京时间 · [打开原文](https://github.blog/ai-and-ml/github-copilot/the-harness-is-all-you-need-mostly/){:target="_blank" rel="noopener noreferrer"}

### [GitHub Copilot app for Beginners: Getting started](https://github.blog/ai-and-ml/github-copilot/github-copilot-app-for-beginners-getting-started/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

GitHub Copilot 应用入门指南，教初学者如何开始项目、使用 AI 代理和画布。

**对做产品的启发**：GitHub 官方入门指南，适合初学者，但内容偏教程，增量信息有限。

**继续验证**：无。

**原始来源**：rss · Christopher Harrison · 7月28日 00:00 北京时间 · [打开原文](https://github.blog/ai-and-ml/github-copilot/github-copilot-app-for-beginners-getting-started/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [moonshotai/Kimi-K3](https://simonwillison.net/2026/Jul/27/kimi-k3/#atom-everything){:target="_blank" rel="noopener noreferrer"} ⭐️ 9.0/10

月之暗面发布 Kimi K3 模型权重，2.8 万亿参数，开源许可变更，值得关注其能力与合规要求。

**对做产品的启发**：月之暗面正式发布 Kimi K3 模型权重，2.8 万亿参数，1.56TB，开源许可从修改版 MIT 改为更严格的单独协议。这是模型公司核心研发一手动态，直接解锁新产品能力，对 AI 产品经理有极高参考价值。

**继续验证**：关注 K3 实际性能评测及社区应用案例

**原始来源**：rss · Simon Willison · 7月28日 07:39 北京时间 · [打开原文](https://simonwillison.net/2026/Jul/27/kimi-k3/#atom-everything){:target="_blank" rel="noopener noreferrer"}

### [Claude Opus 5](https://www.anthropic.com/news/claude-opus-5){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

Anthropic 发布 Claude Opus 5 模型，引发基准测试和编码代理性能讨论。

**对做产品的启发**：Anthropic 官方发布 Claude Opus 5 模型，结合 newsletter 确认是正式发布，对产品构建者有直接参考价值。

**继续验证**：关注模型性能评测及实际应用反馈

**原始来源**：public\_web · Anthropic News · 7月25日 10:03 北京时间 · [打开原文](https://www.anthropic.com/news/claude-opus-5){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [How Thinking Machines Lab S Inkling Performs On Agentic Knowledge Work](https://artificialanalysis.ai/articles/how-thinking-machines-lab-s-inkling-performs-on-agentic-knowledge-work){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Artificial Analysis 评测了 Thinking Machines Lab 的 Inkling 在 agentic 知识工作上的表现，值得关注其产品能力。

**对做产品的启发**：Thinking Machines Lab 的 Inkling 产品在 agentic 知识工作上的性能评测，有具体数据和对比，但来源为第三方媒体，非一手。

**继续验证**：关注 Inkling 的正式发布和用户反馈。

**原始来源**：public\_web · Artificial Analysis · 7月22日 08:00 北京时间 · [打开原文](https://artificialanalysis.ai/articles/how-thinking-machines-lab-s-inkling-performs-on-agentic-knowledge-work){:target="_blank" rel="noopener noreferrer"}

### [Our position on open-weights models](https://www.anthropic.com/news/position-open-weights-models){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

Anthropic 发布开放权重模型立场文章，讨论安全与政策，引发社区争议。

**对做产品的启发**：Anthropic 官方发布关于开放权重模型的立场，涉及政策讨论，但内容本身不直接提供产品构建增量，且评论区有争议。

**继续验证**：观察后续政策影响及社区反应

**原始来源**：hackernews · surprisetalk · 7月28日 06:03 北京时间 · [打开原文](https://www.anthropic.com/news/position-open-weights-models){:target="_blank" rel="noopener noreferrer"}

### [HeyZoku](https://www.producthunt.com/products/heyzoku){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

HeyZoku 允许用户通过语音指挥一群编码代理。

**对做产品的启发**：Product Hunt 新产品，用语音编排编码代理，概念有趣但缺乏详细信息和用户反馈。

**继续验证**：关注产品页面是否有更多细节和用户评价。

**原始来源**：rss · Priyanshu Dangi · 7月27日 14:25 北京时间 · [打开原文](https://www.producthunt.com/products/heyzoku){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：召回率（Recall）：模型找出了多少真实存在的漏洞，漏掉就是风险；精确率（Precision）：模型报的漏洞里有多少是真的，误报就是浪费人力
- **知识点**：F2 分数：一种给召回率&#x27;加权重&#x27;的算法，因为安全场景里漏掉漏洞比误报更危险，所以召回率比精确率重要两倍
- **知识点**：AI Gateway：一个统一入口，让你可以像切换水电一样，在同一个接口换不同的 AI 模型，方便比价和组合使用
- **知识点**：Agent（代理）：AI 不只是回答问题，还能被授权在系统里实际执行操作，比如自动封禁可疑账号
- **动手练习**：访问 https://vercel.com/ai-gateway/leaderboards/deepsecbench ，对比 GPT-5.6 Sol（最高分$55.98）和 Grok 4.5（$5.60）的分数、召回率、精确率、时间。假设你每月预算$100、代码量中等，写一段 200 字的选型建议，说明你会选哪个模型、什么配置、多久扫一次，并解释为什么。
- **动手练习**：注册 Microsoft Security Copilot 免费试用（需企业身份），输入一个模拟告警的自然语言描述，观察 AI 如何解析并给出调查步骤；对比手动查阅原始日志的效率差异

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
