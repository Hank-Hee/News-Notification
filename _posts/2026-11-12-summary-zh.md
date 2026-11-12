---
layout: default
title: "AI产品情报 · 2026-11-12"
date: 2026-11-12
lang: zh
---

**日期**：2026-11-12　 **更新时间**：2026-11-12 15:09 北京时间

> 从 110 条内容中筛选出 8 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Latent Space 报道 Jev 创建者 Diogo Almeida 在 AI Engineer Code Summit 上呼吁开发者把一切自动化，并介绍 Glean 等公司如何用 Jev 的 System One 模型；值得看因为它展示了决策模型在真实公司里的用法。
- AWS 公开一个由自主 AI Agent 写出的 AWS 模拟器并开源到 GitHub，用来在本地模拟云服务；值得看因为它是“Agent 参与真实工程交付”的可验证案例，评论区也指出其安全测试边界有限。
- Browser-use 发布了 1.0.3 候选版，修复了 CLI 和容器中浏览器连接等问题，让开发者更容易构建浏览器自动化 Agent。
- 数学教育者 Scott Farrar 用 Claude Code 加 Obsidian 搭了一个家庭 AI 大脑，管理家电、保单和待办，解决 AI 聊天记不住上下文的问题，值得看它如何把 AI 嵌进日常家务流程。
- Simon Willison 用 AI 加 tree-sitter 分析自己 244 个随手做的小工具，按 JavaScript 库和浏览器 API 生成标签云方便浏览；值得看因为它示范了个人开发者如何用 AI 快速给自己的产品加可用功能。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Jev 的 System One 模型：工程师正在用它做什么](https://latent.space/p/jev-revolution/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Latent Space 报道 Jev 创建者 Diogo Almeida 在 AI Engineer Code Summit 上呼吁开发者把一切自动化，并介绍 Glean 等公司如何用 Jev 的 System One 模型；值得看因为它展示了决策模型在真实公司里的用法。

**评分**：7.8 / 10　 **证据**：媒体报道

**产品 / 团队**：Jev / Richard MacManus

**目标用户**：企业开发者和工程师，尤其是需要把业务流程自动化的公司（如 Glean）

**它是什么**：Jev 是 TypeSafe AI 公司开发的一种&quot;决策型 AI 模型&quot;，不生成文字或代码，而是专门做判断和决策。

**用户问题**：传统 LLM 擅长写文字、写代码，但企业里很多决策场景（比如&quot;要不要批准这笔报销&quot;&quot;这个工单该派给谁&quot;）需要可靠的判断，而不是一段文字输出，现有工具不好直接用。

**使用流程**：
1. 开发者把公司里的决策规则或场景接入 Jev
2. Jev 接收输入信息，直接输出决策结果（是/否、分类、数值等）
3. 企业系统根据 Jev 的决策自动执行下一步操作
4. 开发者监控决策质量，必要时调整规则

**AI 在做什么**：AI 负责做判断/决策这一步，替代原来需要人工审批或硬编码规则的地方

**怎么实现**：把 AI 从&quot;写作文&quot;重新定位为&quot;做选择题&quot;——不是生成一段文字让你读，而是直接给你一个确定的决定，方便嵌入到自动化工作流里。

**需要理解的知识点**：
1. System One 模型：一种专门做快速、直觉式判断的 AI，区别于生成文字的 LLM
2. Function Calling（函数调用）：让 AI 能调用外部工具或系统执行操作的白话说法，就是 AI 决定&quot;现在该调用哪个功能&quot;
3. Agent（智能体）：能自主感知环境、做决策并采取行动的系统，不只是回答问题

**动手练习**：找一个你工作中需要反复做判断的场景（比如&quot;邮件是不是垃圾邮件&quot;&quot;这个需求优先级高不高&quot;），用任何 LLM（ChatGPT/Claude）试做：先让它生成一段分析文字，再改成只输出一个判断结果（是/否/数字），体会&quot;生成型&quot;和&quot;决策型&quot;的区别。

**已知限制**：Jev 的具体技术细节、准确率数据、定价、以及 Glean 等公司具体怎么用均未公开；目前信息主要来自会议演讲和媒体报道，非一手产品文档。

**原始来源**：rss · Richard MacManus · 11月12日 13:08 北京时间 · [打开原文](https://latent.space/p/jev-revolution/){:target="_blank" rel="noopener noreferrer"}

---
### 2. [AWS 开源本地云模拟器：由 AI Agent 自动编写的工程案例](https://github.com/aws/aws-emulator){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：AWS 公开一个由自主 AI Agent 写出的 AWS 模拟器并开源到 GitHub，用来在本地模拟云服务；值得看因为它是“Agent 参与真实工程交付”的可验证案例，评论区也指出其安全测试边界有限。

**评分**：7.6 / 10　 **证据**：一手信息

**产品 / 团队**：AWS Emulator / super\_linear

**目标用户**：在 AWS 上开发、测试云应用的工程师；需要本地快速验证而不用开真实 AWS 账户或产生费用的团队

**它是什么**：AWS Emulator 是一个能在你电脑上本地运行、模拟 AWS 云服务的开源工具，让你不用连真云就能开发和测试。

**用户问题**：开发 AWS 应用时，每次测试都要连真实云端、配置账户、可能产生费用，而且网络慢、反馈周期长；现有第三方模拟器（如 LocalStack）不是官方出品，兼容性和维护不确定

**使用流程**：
1. 本地安装启动 Emulator（命令行运行，无图形界面）
2. 设置环境变量，把 AWS CLI 或 SDK 指向本地模拟地址
3. 用熟悉的 AWS CLI、SDK 或 Terraform 像操作真云一样开发测试
4. 查看持久化状态，确认资源创建和配置效果

**AI 在做什么**：AWS 称该模拟器主要由自主 AI Agent（自主 AI 智能体，指能自己规划步骤、调用工具、完成多轮任务的大模型程序）自动编写代码完成，人类工程师负责审查和把关

**怎么实现**：在本地跑一个假扮成 AWS 的 API 服务器，拦截你对 S3、DynamoDB 等服务的调用，在本地模拟响应和存储状态，而不是真的去 AWS 数据中心操作

**需要理解的知识点**：
1. Agent（智能体）：不只是回答问题，而是能自己分解任务、写代码、调试、提交的大模型自动化程序
2. 云模拟器/本地仿真：在本地伪造云服务的 API 行为，用于快速开发和节省成本
3. Function Calling（函数调用）：大模型通过调用外部工具（如写文件、运行测试）来完成复杂工程任务，是 Agent 能写代码的关键机制

**动手练习**：30 分钟动手：从 https://github.com/aws/aws-emulator 克隆项目，按 README 启动 Emulator，用 AWS CLI 执行 \`aws s3 mb s3://test-bucket --endpoint-url http://localhost:8080\` 创建一个本地模拟的 S3 存储桶，再用 \`aws s3 ls --endpoint-url http://localhost:8080\` 验证是否能列出，对比与真实 AWS 的行为差异

**已知限制**：AWS 官方安全文档明确标注：不支持测试 IAM 策略、权限边界、KMS 密钥策略、跨账户/跨区域访问等安全控制；模拟器对 IAM 的评估方式与真实 AWS 不同，且不会拒绝用它自己签名的请求。社区质疑这是否仅为实验项目，还是会长期维护的产品。代码风格和质量存在争议。

**原始来源**：hackernews · super\_linear · 11月12日 02:21 北京时间 · [打开原文](https://github.com/aws/aws-emulator){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [Claude Code + Obsidian: My family’s AI brain \| Scott Farrar](https://www.lennysnewsletter.com/p/claude-code-obsidian-my-familys-ai){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.6/10

数学教育者 Scott Farrar 用 Claude Code 加 Obsidian 搭了一个家庭 AI 大脑，管理家电、保单和待办，解决 AI 聊天记不住上下文的问题，值得看它如何把 AI 嵌进日常家务流程。

**对做产品的启发**：构建者一手讲述用 Claude Code + Obsidian 搭建家庭 AI 大脑的真实案例，有具体使用场景（保险、维修、共享、墙面展示），对初学者理解“解决什么问题、AI 在哪一步发挥作用”很有迁移价值。

**继续验证**：关注他如何组织 Markdown 文件结构、如何与家人共享，以及是否有可复用的模板或开源仓库。

**原始来源**：newsletter · Claire Vo · 11月11日 21:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/claude-code-obsidian-my-familys-ai){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [Browse tools.simonwillison.net by tag](https://simonwillison.net/2026/Nov/11/tools-tags/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.4/10

Simon Willison 用 AI 加 tree-sitter 分析自己 244 个随手做的小工具，按 JavaScript 库和浏览器 API 生成标签云方便浏览；值得看因为它示范了个人开发者如何用 AI 快速给自己的产品加可用功能。

**对做产品的启发**：Simon Willison 用 AI 辅助为 244 个 vibe-coded 小工具做标签浏览，展示了“用 LLM 分析自己代码库再生成产品功能”的构建过程，对个人产品探索者有可迁移做法，但规模小、增量有限。

**继续验证**：观察这种标签化浏览是否被其他个人工具集复用，以及 AI 生成分类的准确度。

**原始来源**：rss · Simon Willison · 11月12日 02:42 北京时间 · [打开原文](https://simonwillison.net/2026/Nov/11/tools-tags/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Gemini Decisions API](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

Google 发布 Gemini Decisions API，让模型直接给出带概率的决策结果，解决 LLM 置信度不可靠的问题，值得看它能否催生需要概率输出的新 AI 产品。

**对做产品的启发**：Google 官方发布 Gemini Decisions API，让模型输出决策和概率而非纯文本，属于能解锁新交互的产品能力；HN 讨论热度高，但评论多为疑问，产品落地案例尚少。

**继续验证**：观察开发者是否用它做出实际产品，以及定价和音视频输入场景的落地案例。

**原始来源**：hackernews · iamdelirium · 11月12日 02:32 北京时间 · [打开原文](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [browser-use/browser-use released 1.0.3rc1](https://github.com/browser-use/browser-use/releases/tag/1.0.3rc1){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Browser-use 发布了 1.0.3 候选版，修复了 CLI 和容器中浏览器连接等问题，让开发者更容易构建浏览器自动化 Agent。

**对做产品的启发**：Browser-use 发布 1.0.3 候选版，包含多项 CLI 和容器环境修复，对构建浏览器 Agent 的开发者有明确可迁移的实践价值。

**继续验证**：关注正式版 1.0.3 的发布及社区反馈。

**原始来源**：github · gregpr07 · 11月12日 10:11 北京时间 · [打开原文](https://github.com/browser-use/browser-use/releases/tag/1.0.3rc1){:target="_blank" rel="noopener noreferrer"}

### [Adobe’s AI experiments let you walk around in photos and interview your characters](https://www.theverge.com/tech/1031505/adobe-max-2026-sneaks-experiments-ai){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.3/10

Adobe 在 Max 大会公布实验性 AI 功能，能把照片变成可走动的 3D 场景、通过对话设计角色、把修图变成复制粘贴，值得看 AI 如何改变创作工具。

**对做产品的启发**：Adobe Max 公布实验性 AI 功能：照片变可探索 3D 场景、对话设计 AI 角色、复制粘贴式修图，有明确产品形态和 Demo 展示，但仍是实验阶段。

**继续验证**：关注这些实验功能何时进入正式产品，以及是否有公开 Demo 可试用。

**原始来源**：rss · Jess Weatherbed · 11月11日 22:00 北京时间 · [打开原文](https://www.theverge.com/tech/1031505/adobe-max-2026-sneaks-experiments-ai){:target="_blank" rel="noopener noreferrer"}

### [Try Tabletop: Customizable, collaborative spaces for groups to plan, play and do more together.](https://blog.google/innovation-and-ai/models-and-research/google-labs/tabletop/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Google Labs 推出 Tabletop 实验，用户描述需求就能生成行程、投票等小组协作工具，解决家庭和朋友一起规划的问题，值得看 AI 生成协作应用的产品形态。

**对做产品的启发**：Google Labs 官方发布 Tabletop 实验，用 AI 生成可定制的协作空间（行程、投票、对阵表），属于有明确产品形态的新实验，但仍在 waitlist 阶段，无用户反馈。

**继续验证**：关注 waitlist 开放后的实际生成效果、可定制程度和是否支持多人实时协作。

**原始来源**：rss · Roman Nurik · 11月12日 00:00 北京时间 · [打开原文](https://blog.google/innovation-and-ai/models-and-research/google-labs/tabletop/){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：System One 模型：一种专门做快速、直觉式判断的 AI，区别于生成文字的 LLM
- **知识点**：Function Calling（函数调用）：让 AI 能调用外部工具或系统执行操作的白话说法，就是 AI 决定&quot;现在该调用哪个功能&quot;
- **知识点**：Agent（智能体）：能自主感知环境、做决策并采取行动的系统，不只是回答问题
- **知识点**：Agent（智能体）：不只是回答问题，而是能自己分解任务、写代码、调试、提交的大模型自动化程序
- **动手练习**：找一个你工作中需要反复做判断的场景（比如&quot;邮件是不是垃圾邮件&quot;&quot;这个需求优先级高不高&quot;），用任何 LLM（ChatGPT/Claude）试做：先让它生成一段分析文字，再改成只输出一个判断结果（是/否/数字），体会&quot;生成型&quot;和&quot;决策型&quot;的区别。
- **动手练习**：30 分钟动手：从 https://github.com/aws/aws-emulator 克隆项目，按 README 启动 Emulator，用 AWS CLI 执行 \`aws s3 mb s3://test-bucket --endpoint-url http://localhost:8080\` 创建一个本地模拟的 S3 存储桶，再用 \`aws s3 ls --endpoint-url http://localhost:8080\` 验证是否能列出，对比与真实 AWS 的行为差异

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
