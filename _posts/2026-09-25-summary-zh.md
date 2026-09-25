---
layout: default
title: "AI产品情报 · 2026-09-25"
date: 2026-09-25
lang: zh
---

**日期**：2026-09-25　 **更新时间**：2026-09-25 12:57 北京时间

> 从 153 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- 四位开发者做了开源桌面工具 Whiteboard，让人类和 AI Agent 在同一画布上一起设计软件，解决白板讨论后理解无法落到代码的问题，值得看它如何把 Agent 输出直接连回代码。
- Meta 推出 Horizon Create 手机应用和 Horizon Studio 浏览器工具，让用户用 AI 提示词直接做游戏，值得看的是 UGC 平台如何把 AI 生成变成低门槛创作入口。
- Google Photos 把 AI 虚拟衣橱功能从 Android 扩展到 iOS 全量上线，用户可用自己照片自动生成虚拟衣橱，值得看的是消费级照片 AI 如何落到具体生活场景。
- 微软 Foundry 的 Routines 功能正式可用，让 Agent 能监控 GitHub issue、Teams 消息等事件并持续执行任务，推动 Agent 从聊天走向自动化。
- Warp 的 CEO 讲了他们怎么用 AI 软件工厂每月产出 2000 个 PR，值得看是因为它把从 Slack 提需求到合并代码的完整流程讲清楚了。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Whiteboard：让人类和 AI 在同一画布上协作设计软件的开源桌面工具](https://github.com/devdotfast/whiteboard){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：四位开发者做了开源桌面工具 Whiteboard，让人类和 AI Agent 在同一画布上一起设计软件，解决白板讨论后理解无法落到代码的问题，值得看它如何把 Agent 输出直接连回代码。

**评分**：8.6 / 10　 **证据**：一手信息

**产品 / 团队**：Whiteboard / sidharthkmenon

**目标用户**：使用 AI 编程工具（如 Claude Code、Codex）的开发者，以及需要评审架构或规格级代码变更的团队（已有 Salesforce、Modal 等公司在试用）

**它是什么**：一个基于 CodeOSS（VS Code 开源内核）构建的桌面应用，让人类和 AI Agent 在同一个可视化画布上共同设计软件架构，并把图表直接链接到代码。

**用户问题**：用 AI Agent 写代码越来越快，但开发者看不懂 Agent 做了什么决定、为什么改，积累&#x27;认知债务&#x27;——合并的 PR 越来越多，人对系统的理解越来越少，最后连自己写的项目都参与不进去

**使用流程**：
1. 开发者启动 Whiteboard，接入自己用的 AI 工具（如 Claude Code）
2. AI Agent 在画布上绘制架构图、时序图等，解释自己的设计思路
3. 开发者点击图表中的任何元素，直接跳转到对应代码位置；反向浏览代码时也能看到相关设计图
4. 用内置的语义 diff 工具评审变更，Decision Log 追溯 Agent 的自主决策过程

**AI 在做什么**：AI 通过 SDK 在画布上&#x27;画图说话&#x27;，把内部推理过程（trace）可视化，并自动记录决策日志供人审查；不是只输出最终代码，而是暴露设计过程

**怎么实现**：把&#x27;白板讨论&#x27;和&#x27;代码编辑&#x27;焊在一起：底层用 VS Code 的开源版本保证代码导航和语法支持，上层加一个画布让 AI 画画；再用 Rust 写了一个懂代码结构的 diff 工具，能折叠测试、文档等噪音，只显示关键变更

**需要理解的知识点**：
1. Agent：能自主执行多步任务的 AI，不只是回答一次问题，而是能调用工具、写代码、做决策；这里 Agent 被赋予&#x27;画画&#x27;的能力来向人类解释自己
2. LSP（Language Server Protocol）：让编辑器理解代码的&#x27;通用翻译层&#x27;，Whiteboard 继承自 VS Code，所以点击代码能跳转、能补全，不用自己重做
3. Semantic diff：不是按行对比文本，而是按代码结构（AST）对比，知道&#x27;这是个函数&#x27;、&#x27;这是个测试文件&#x27;，从而智能折叠不重要的变更

**动手练习**：30 分钟：在 Mac/Linux 上从 https://install.dev.fast 安装 Whiteboard，连接 Claude Code 让它帮你实现一个小功能（如写一个 API 端点），观察 Agent 是否在画布生成图表，然后点击图表看能否跳转到对应代码；最后打开 Decision Log 看 Agent 记录了哪些决策

**已知限制**：目前不能直接在 Whiteboard 里编辑文件（icar 评论确认）；Windows 版本未提及；Copilot CLI 支持被询问但官方未回应；&#x27;认知债务&#x27;概念引用自 Geoffrey Litt 的博客，非团队原创术语

**原始来源**：hackernews · sidharthkmenon · 9月25日 01:21 北京时间 · [打开原文](https://github.com/devdotfast/whiteboard){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Meta 推出手机 AI 游戏创作工具：说话就能做游戏](https://www.theverge.com/games/999972/meta-horizon-create-studio-ai-games){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Meta 推出 Horizon Create 手机应用和 Horizon Studio 浏览器工具，让用户用 AI 提示词直接做游戏，值得看的是 UGC 平台如何把 AI 生成变成低门槛创作入口。

**评分**：7.8 / 10　 **证据**：媒体报道

**产品 / 团队**：Horizon Create（手机 App）、Horizon Studio（浏览器工具） / Jay Peters

**目标用户**：没有编程或美术基础的普通用户、想快速做 UGC（用户生成内容）游戏的创作者

**它是什么**：Meta 为 Horizon 社交平台推出的两套 AI 游戏开发工具，手机端叫 Horizon Create，浏览器端叫 Horizon Studio，用户用自然语言描述就能生成游戏内容。

**用户问题**：传统游戏开发需要学编程、买游戏电脑、装复杂软件，门槛高、周期长，普通人想做游戏但无从下手

**使用流程**：
1. 在手机或浏览器打开工具，用自然语言描述想要的游戏（如&#x27;做一个太空射击游戏，敌人是外星人&#x27;）
2. AI 根据描述生成可玩的游戏基础版本
3. 在 Horizon Studio 里用可视化编辑器微调细节（如改颜色、调难度、加关卡）
4. 发布到 Horizon 平台，其他用户可以搜到并玩

**AI 在做什么**：把用户的自然语言描述转换成可运行的游戏代码和资源，相当于&#x27;翻译官&#x27;：你说人话，它出游戏

**怎么实现**：核心是&#x27;提示词生成&#x27;（Prompt-to-Game）：底层用 LLM 理解用户想做什么游戏，再调用代码生成和素材生成能力，把文字变成可执行的游戏逻辑和 3D/2D 内容。浏览器端的 Studio 额外加了可视化层，让用户能手动拖拽修改 AI 生成的结果。

**需要理解的知识点**：
1. Prompt Engineering（提示词工程）：怎么跟 AI 说清楚你要什么游戏，直接影响生成质量
2. UGC 平台：用户自己生产内容、平台负责分发，AI 在这里是&#x27;降低生产门槛&#x27;的杠杆
3. 多模态生成：LLM 不只输出文字，还能联动生成代码、3D 模型、音效等游戏素材

**动手练习**：打开任意免费 AI 工具（如 ChatGPT/Claude），尝试用 3 句不同详细程度的提示词描述同一个简单游戏（如&#x27;打砖块&#x27;），对比 AI 给出的差异；然后思考：如果要把这个结果变成真能玩的游戏，还需要补充哪些信息？

**已知限制**：未公开具体支持的输出格式、是否限制游戏类型、AI 生成后的二次编辑自由度、以及用户实际测试后的反馈；目前仅为官方发布和媒体报道，尚无普通用户验证体验。

**原始来源**：rss · Jay Peters · 9月25日 01:52 北京时间 · [打开原文](https://www.theverge.com/games/999972/meta-horizon-create-studio-ai-games){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [How Warp ships 2,000 PRs a month with AI factories \| Zach Lloyd \(CEO, Warp\)](https://www.lennysnewsletter.com/p/how-warp-ships-2000-prs-a-month-with){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Warp 的 CEO 讲了他们怎么用 AI 软件工厂每月产出 2000 个 PR，值得看是因为它把从 Slack 提需求到合并代码的完整流程讲清楚了。

**对做产品的启发**：Warp CEO Zach Lloyd 在 Lenny 播客中公开讲软件工厂如何把 Slack 想法一路做到合并 PR，并给出每月 2000 个 PR 的具体指标和 Slack→Linear→GitHub→QA 的公开工作流。属于构建者一手实践，对理解 AI 编码产品如何嵌入真实研发流程有直接参考价值。

**继续验证**：关注 Warp 软件工厂的公开工作流细节、QA 环节如何自动化，以及 2000 PR 的合并率与返工率。

**原始来源**：newsletter · Claire Vo · 9月21日 20:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-warp-ships-2000-prs-a-month-with){:target="_blank" rel="noopener noreferrer"}

### [Opus 5.5 vs. GPT-6 Sol: which model won my blind taste test?](https://www.lennysnewsletter.com/p/opus-55-vs-gpt-6-sol-which-model){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

Claire Vo 用邮件、PRD、前端原型等真实工作任务盲测 Opus 5.5、GPT-6 等新模型，给出个人选型结论，可帮初学者理解不同模型在实际产品工作流中的差异。

**对做产品的启发**：作者用真实工作任务（邮件、PRD、前端原型、后端、长时 Agent、SVG、视频剪辑）对多个新模型做盲测，属于有身份可核验的从业者一手实践，对 AI 产品经理理解模型选型有可迁移增量。但本质是个人评测，非产品发布，且无客观指标，故未达 8 分。

**继续验证**：关注其评测方法与结论是否被其他从业者复现，以及是否沉淀为可复用的模型选型框架。

**原始来源**：newsletter · Claire Vo · 9月23日 07:12 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/opus-55-vs-gpt-6-sol-which-model){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [Show HN: Koi.rest – watch some fish and regain your balance](https://koi.rest/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

一位不会 JavaScript 的开发者用 AI 做出看锦鲤放松的网站 koi.rest，解决自己失业焦虑下的放松需求，值得看普通人如何靠 AI 把想法变成上线产品。

**对做产品的启发**：独立开发者用 AI 做出虚拟锦鲤池 koi.rest，公开讲述自己不会 JavaScript、用 AI 完成产品的真实过程，HN 153 分 40 评论，是初学者可迁移的“用 AI 做个人产品”一手案例，但产品本身较简单。

**继续验证**：观察作者是否公开更多用 AI 开发的具体工具链和迭代细节。

**原始来源**：hackernews · hxii · 9月25日 05:33 北京时间 · [打开原文](https://koi.rest/){:target="_blank" rel="noopener noreferrer"}

### [When chat is the wrong UI](https://github.blog/ai-and-ml/github-copilot/when-chat-is-the-wrong-ui/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.4/10

GitHub 官方提出聊天框并非所有场景的最佳界面，并介绍 canvas 这种更具体的交互形态，对设计 AI 产品界面有启发。

**对做产品的启发**：GitHub 官方博客讨论“聊天不是正确 UI”并引出 canvas 形态，属产品思路类一手内容，对 AI 产品经理理解交互设计有可迁移增量。但正文仅一句话，缺少具体产品功能与用户反馈，故未达 8 分。

**继续验证**：关注 GitHub Copilot 是否正式上线 canvas 功能及其用户反馈。

**原始来源**：rss · Burke Holland · 9月25日 04:00 北京时间 · [打开原文](https://github.blog/ai-and-ml/github-copilot/when-chat-is-the-wrong-ui/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude Discovers Novel Enzyme System](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Anthropic 官方称 Claude 发现了一种新的酶系统，展示大模型在生物科学发现中的实际用途，值得关注 AI 在医药研发场景的产品化可能。

**对做产品的启发**：Anthropic 官方发布 Claude 发现新酶系统的研究更新，属模型公司一手动态，且展示了模型在科学发现这一新场景中的实际能力，对探索垂直 AI 产品（尤其医药/生物）有直接启发。但正文仅有占位描述，缺少可验证细节与用户使用路径，故未进入 9 分区间。

**继续验证**：等待官方补充实验细节、可复现方法或合作方信息，判断是否可迁移为垂直科研产品。

**原始来源**：public\_web · Anthropic News · 9月24日 18:25 北京时间 · [打开原文](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"}

### [Introducing Gemini 3.8 Live with Live Avatar](https://deepmind.google/blog/introducing-gemini-38-live-with-live-avatar/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Google DeepMind 发布 Gemini 3.8 Live 并引入 Live Avatar，可能带来实时数字人交互的新产品形态，但官方正文缺失，需等更多细节。

**对做产品的启发**：Google DeepMind 官方发布 Gemini 3.8 Live 与 Live Avatar，属模型公司一手新能力动态，实时数字人交互可能解锁新的产品体验。但正文为空，仅有标题，无法判断具体能力边界与可用性，故按 early\_signal 处理并压低分数。

**继续验证**：等待官方补充 Live Avatar 的能力说明、API 可用性与 Demo，判断能否用于实时客服、陪伴类产品。

**原始来源**：rss · Google DeepMind · 9月25日 00:20 北京时间 · [打开原文](https://deepmind.google/blog/introducing-gemini-38-live-with-live-avatar/){:target="_blank" rel="noopener noreferrer"}

### [Opus 5.5 is good at explainer videos](https://launchvideo.io/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

有人发帖称 Opus 5.5 擅长做讲解视频并推广 launchvideo.io，但缺少可验证细节，评论区提醒对模型发布 Demo 保持怀疑。

**对做产品的启发**：帖子标题称 Opus 5.5 擅长做讲解视频并指向 launchvideo.io，但正文只有评论，缺少可验证的模型发布信息与产品细节，评论区还提醒对模型发布 Demo 保持怀疑，属于带推广性质的弱证据内容。

**继续验证**：等待 Anthropic 官方或可复现 Demo 确认 Opus 5.5 的视频生成能力。

**原始来源**：hackernews · iacguy · 9月25日 04:28 北京时间 · [打开原文](https://launchvideo.io/){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Google Photos ‘Clueless’-inspired virtual closet is now available on Android and iOS](https://techcrunch.com/2026/09/24/google-photos-clueless-inspired-virtual-closet-is-now-available-on-android-and-ios/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Google Photos 把 AI 虚拟衣橱功能从 Android 扩展到 iOS 全量上线，用户可用自己照片自动生成虚拟衣橱，值得看的是消费级照片 AI 如何落到具体生活场景。

**对做产品的启发**：Google Photos 的 AI 虚拟衣橱功能从 Android 扩展到 iOS 全量上线，属于已发布产品的真实功能增量，有明确使用场景（从照片自动构建虚拟衣橱），对做垂直 AI 产品的初学者有可迁移参考；但报道为媒体转述，无用户反馈数据，故未进 8 分档。

**继续验证**：观察用户实际使用反馈、是否开放更多地区、是否与电商/穿搭推荐打通。

**原始来源**：rss · Sarah Perez · 9月25日 01:00 北京时间 · [打开原文](https://techcrunch.com/2026/09/24/google-photos-clueless-inspired-virtual-closet-is-now-available-on-android-and-ios/){:target="_blank" rel="noopener noreferrer"}

### [From Chatbots to Automated Agents: Routines in Microsoft Foundry Are Now Generally Available](https://devblogs.microsoft.com/foundry/from-chatbots-to-automated-assistants-routines-in-microsoft-foundry-are-now-generally-available/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

微软 Foundry 的 Routines 功能正式可用，让 Agent 能监控 GitHub issue、Teams 消息等事件并持续执行任务，推动 Agent 从聊天走向自动化。

**对做产品的启发**：微软 Foundry 的 Routines 正式 GA，让 Agent 从被动聊天转向监控事件、持续执行任务，是 Agent 产品形态的重要增量，对做自动化 Agent 产品有参考。但正文为摘要式介绍，缺少具体客户案例与效果数据。

**继续验证**：关注是否有客户落地案例与效果指标，以及该模式对国内 Agent 产品的借鉴意义。

**原始来源**：rss · Linda Li · 9月24日 23:00 北京时间 · [打开原文](https://devblogs.microsoft.com/foundry/from-chatbots-to-automated-assistants-routines-in-microsoft-foundry-are-now-generally-available/){:target="_blank" rel="noopener noreferrer"}

### [Muse sure looks a lot like OpenClaw](https://www.theverge.com/report/1000180/muse-openclaw-instinct-lookalike){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.4/10

Meta 的消费级 AI Agent Muse 上线后登上 App Store 榜首、美国日活约 60 万，并与 OpenClaw、Instinct 等产品形态相似，值得看的是消费级 Agent 赛道的真实用户量级。

**对做产品的启发**：报道 Meta 消费级 AI Agent Muse 上线后登顶 App Store、美国日活约 60 万（Apptopia 估算），并对比 Instinct 等竞品，属于有真实用户指标的 Agent 产品动态；但数据为第三方估算、无一手产品细节，故 7 分档。

**继续验证**：关注日活是否可持续、与 OpenClaw 的功能差异、以及 Instinct 融资进展。

**原始来源**：rss · Hayden Field · 9月25日 01:10 北京时间 · [打开原文](https://www.theverge.com/report/1000180/muse-openclaw-instinct-lookalike){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent：能自主执行多步任务的 AI，不只是回答一次问题，而是能调用工具、写代码、做决策；这里 Agent 被赋予&#x27;画画&#x27;的能力来向人类解释自己
- **知识点**：LSP（Language Server Protocol）：让编辑器理解代码的&#x27;通用翻译层&#x27;，Whiteboard 继承自 VS Code，所以点击代码能跳转、能补全，不用自己重做
- **知识点**：Semantic diff：不是按行对比文本，而是按代码结构（AST）对比，知道&#x27;这是个函数&#x27;、&#x27;这是个测试文件&#x27;，从而智能折叠不重要的变更
- **知识点**：Prompt Engineering（提示词工程）：怎么跟 AI 说清楚你要什么游戏，直接影响生成质量
- **动手练习**：30 分钟：在 Mac/Linux 上从 https://install.dev.fast 安装 Whiteboard，连接 Claude Code 让它帮你实现一个小功能（如写一个 API 端点），观察 Agent 是否在画布生成图表，然后点击图表看能否跳转到对应代码；最后打开 Decision Log 看 Agent 记录了哪些决策
- **动手练习**：打开任意免费 AI 工具（如 ChatGPT/Claude），尝试用 3 句不同详细程度的提示词描述同一个简单游戏（如&#x27;打砖块&#x27;），对比 AI 给出的差异；然后思考：如果要把这个结果变成真能玩的游戏，还需要补充哪些信息？

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
