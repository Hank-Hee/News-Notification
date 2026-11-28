---
layout: default
title: "AI产品情报 · 2026-11-28"
date: 2026-11-28
lang: zh
---

**日期**：2026-11-28　 **更新时间**：2026-11-28 15:46 北京时间

> 从 104 条内容中筛选出 6 条重要资讯。

> 今日高质量增量有限，因此未使用低质量内容补足数量。

<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- The Verge 记者用 Android 的 Gemini 生成自定义小组件来查公交到站，展示了普通用户如何让 AI 直接做出解决自己小问题的工具，值得看它把 AI 能力落到具体生活场景的方式。
- Convex 的 AI 编程插件被用户发现会把应用想法悄悄传到远程服务器，CEO 在 GitHub issue 里回应称这是 quickstart 功能所需，并提到前身产品 Convex Chef 已关停，提醒做 AI 编程产品的人注意数据边界。
- 开发者发布 52KB WebAssembly 引擎，可在浏览器标签页运行 Qwen3.5-2B 模型；展示轻量端侧 LLM 部署可能性，值得关注产品化场景。
- 虎嗅网报道 DeepSeek 安卓端新增对话 Token 计费统计，免费额度收紧引发付费模式猜测，值得关注 AI 产品如何量化使用成本。
- Simon Willison 发布 datasette-charts 0.4a0，他先让 Claude 写一个实验插件来测试新钩子，发现设计摩擦后改进接口并补上教程网站，展示了用 AI 快速验证产品设计的具体做法。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Android 用 Gemini 让用户说话就能做小组件：等公交不用翻 App 了](https://www.theverge.com/tech/1041801/android-intelligence-create-my-widget-gemini){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：The Verge 记者用 Android 的 Gemini 生成自定义小组件来查公交到站，展示了普通用户如何让 AI 直接做出解决自己小问题的工具，值得看它把 AI 能力落到具体生活场景的方式。

**评分**：7.6 / 10　 **证据**：媒体报道

**产品 / 团队**：Android Intelligence / Create my widget（Gemini 驱动） / Allison Johnson

**目标用户**：不想折腾代码、但想快速解决个人小问题的普通 Android 用户，比如通勤族

**它是什么**：Android 手机的一项功能，让用户用自然语言描述需求，由 Gemini AI 直接生成可放在桌面的自定义小组件

**用户问题**：记者每天等公交时，需要点开特定 App、找到对应站点、查看实时到站，步骤繁琐，容易错过车

**使用流程**：
1. 用户用口语告诉 Gemini 想要什么小组件，例如&#x27;显示我家附近公交站的实时到站&#x27;
2. Gemini 理解意图并生成对应的小组件
3. 用户把小组件放到手机桌面
4. 之后直接在桌面看到实时信息，无需再打开 App

**AI 在做什么**：把用户的自然语言需求翻译成可运行的小组件，包括理解意图、调用数据接口、生成界面

**怎么实现**：用户说话 → Gemini 解析出&#x27;要做什么+数据来源+怎么展示&#x27; → 自动生成一个轻量级桌面组件。本质是把&#x27;写代码做 App&#x27;变成&#x27;说话出结果&#x27;，类似用 AI 当翻译，把你的需求转成机器能执行的界面。

**需要理解的知识点**：
1. Function Calling（函数调用）：AI 听懂人话后，去调用外部工具（如公交 API）拿数据的白话解释
2. Agent（智能体）：AI 不只是聊天，还能动手帮你完成多步骤任务的白话解释
3. RAG（检索增强生成）：AI 可能需要实时查公交数据，而不是只靠训练时的旧知识

**动手练习**：打开你手机的 Gemini 或类似 AI 助手，尝试用一句话描述一个你日常的小需求（如&#x27;显示今天天气&#x27;或&#x27;倒计时到周末&#x27;），观察 AI 能否直接生成结果或给出可执行的步骤。记录它理解了什么、哪里出错。

**已知限制**：未公开具体支持的数据源范围、小组件能否长期稳定运行、是否需要特定 Android 版本或 Google 服务；The Verge 为媒体体验，非开发者的一手技术拆解

**原始来源**：rss · Allison Johnson · 11月27日 22:00 北京时间 · [打开原文](https://www.theverge.com/tech/1041801/android-intelligence-create-my-widget-gemini){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Convex AI 插件被曝未经告知上传用户应用想法，CEO 回应系 quickstart 功能所需](https://github.com/convex/convex-backend-skill/issues/64){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Convex 的 AI 编程插件被用户发现会把应用想法悄悄传到远程服务器，CEO 在 GitHub issue 里回应称这是 quickstart 功能所需，并提到前身产品 Convex Chef 已关停，提醒做 AI 编程产品的人注意数据边界。

**评分**：7.2 / 10　 **证据**：一手信息

**产品 / 团队**：Convex / MickyTheMouse

**目标用户**：需要快速搭建全栈应用的开发者，尤其是使用 AI 辅助编程（vibe coding）的人

**它是什么**：Convex 是一个帮开发者构建和托管全栈应用的平台（数据库+服务器端函数+实时同步），其 AI 编程插件被发现会把用户在本地输入的应用想法自动传到远程服务器

**用户问题**：用户以为自己在本地 IDE 里随便试想法，结果插件悄悄把 prompt 发到 Convex 服务器，用户事前没看到明确提示，担心隐私泄露和创意被收集

**使用流程**：
1. 用户在编辑器里安装 Convex 的 AI 编程插件（如 VS Code 扩展）
2. 用户输入自然语言描述想做的应用（例如&#x27;做一个带实时聊天的 todo 列表&#x27;）
3. 插件自动将这段描述发到 Convex 远程服务器，生成可运行的项目骨架（quickstart）
4. 用户在本地获得生成的代码，但可能没意识到自己的原始想法已上传

**AI 在做什么**：AI 负责把用户的自然语言描述转成可运行的 Convex 项目代码和配置，属于&#x27;代码生成&#x27;环节

**怎么实现**：插件端捕获用户的文本输入，通过 API 发到云端，云端用 LLM 生成对应数据库 schema、服务器函数和前端代码，再打包返回给用户。关键点在于这个网络请求没有显式弹窗确认，被用户误认为纯本地操作。

**需要理解的知识点**：
1. Function Calling（函数调用）：LLM 不只是聊天，还能触发外部工具——这里 LLM 生成代码后，插件自动调用 Convex 的远程 API 来创建项目
2. Embedding（嵌入）：未确认 Convex 是否用了，但 AI 编程产品常把用户 prompt 转成向量存起来做检索或分析，是隐私敏感点
3. 数据边界：AI 产品的&#x27;本地感&#x27;不等于&#x27;本地算&#x27;，用户输入可能经过多个服务器，需要看清隐私政策里的数据流向

**动手练习**：30 分钟验证：打开 Chrome DevTools 的网络面板（或 VS Code 的 Output &gt; Extension Host），安装任意一个 AI 编程插件（如 Convex、Copilot、Claude Code），输入一个假想的应用想法，观察 Network 标签里有没有出现未预期的出站请求，记录域名和请求体大小，判断哪些数据离开了你的电脑

**已知限制**：未公开：该上传行为具体发生在哪个插件版本、是否有开关可以关闭、上传数据是否被用于模型训练、Convex Chef 关停的具体用户量数据；CEO 称是 quickstart 功能所需，但未展示该功能的产品内提示文案截图

**原始来源**：hackernews · MickyTheMouse · 11月28日 02:02 北京时间 · [打开原文](https://github.com/convex/convex-backend-skill/issues/64){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

_最近 7 天没有达到收录标准的新 Newsletter 内容；请查看数据源日志。_

<a id="how-they-build"></a>
## 他们怎么做

### [datasette-charts 0.4a0](https://simonwillison.net/2026/Nov/27/datasette-charts/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Simon Willison 发布 datasette-charts 0.4a0，他先让 Claude 写一个实验插件来测试新钩子，发现设计摩擦后改进接口并补上教程网站，展示了用 AI 快速验证产品设计的具体做法。

**对做产品的启发**：Simon Willison 一手发布 datasette-charts 0.4a0，明确记录用 Claude Opus 5.5 先写实验插件来检验插件钩子设计、再据摩擦点改进 API 的过程，是“用 AI 辅助开发并反哺产品设计”的可迁移实践；但属小版本迭代，影响面有限。

**继续验证**：观察后续是否有第三方基于该钩子做出图表插件，以及 Claude 生成代码在真实项目中的返工比例。

**原始来源**：rss · Simon Willison · 11月28日 07:57 北京时间 · [打开原文](https://simonwillison.net/2026/Nov/27/datasette-charts/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [V4 全系列模型上线后，DeepSeek Harness 开发者预览版开放测试 - 财联社](https://news.google.com/rss/articles/CBMiSEFVX3lxTE4wd0JWNXNkT3NmUy1UV09ldm1iSXY3dTllQ1o1ZFg5MFZPS1BRY3RCTUJLc05UYWJTb1R6VHhoT0NXM3hJQU5xLQ?oc=5){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

DeepSeek 在 V4 全系列模型上线后开放了 Harness 开发者预览版测试，为开发者提供新的模型调用与编排入口。

**对做产品的启发**：DeepSeek 官方模型与开发者工具动态，V4 全系列上线并开放 Harness 开发者预览，属模型公司一手能力进展，对产品经理理解新模型能力有直接价值，但正文缺失、需官方源核实。

**继续验证**：核实 DeepSeek 官方公告，确认 Harness 的具体能力、定价和可用范围。

**原始来源**：google\_news · 财联社 · 11月28日 08:54 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMiSEFVX3lxTE4wd0JWNXNkT3NmUy1UV09ldm1iSXY3dTllQ1o1ZFg5MFZPS1BRY3RCTUJLc05UYWJTb1R6VHhoT0NXM3hJQU5xLQ?oc=5){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Show HN: A 52 KB WebAssembly engine that runs Qwen3.5-2B in a browser tab](https://tesseracted.com/experiments-llm-os/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

开发者发布 52KB WebAssembly 引擎，可在浏览器标签页运行 Qwen3.5-2B 模型；展示轻量端侧 LLM 部署可能性，值得关注产品化场景。

**对做产品的启发**：Show HN 展示可运行 Qwen3.5-2B 的 52KB WebAssembly 引擎，有可验证 Demo 和代码，属于产品案例，能让初学者理解浏览器端 LLM 部署，但互动少、技术偏底层，对产品经理迁移价值中等。

**继续验证**：观察该引擎的 GitHub 仓库、性能数据和实际应用案例。

**原始来源**：hackernews · kkm · 11月28日 08:16 北京时间 · [打开原文](https://tesseracted.com/experiments-llm-os/){:target="_blank" rel="noopener noreferrer"}

### [DeepSeek 安卓端新增对话 Token 计费统计，免费额度收紧引付费模式猜测 - 虎嗅网](https://news.google.com/rss/articles/CBMiVEFVX3lxTFBwMC1PWFdqaGIzdS1lVXMxc3czYWdoYjJicl92d29leGhQR0NIUlY5d0ppN0lrZE16SDdqMDVGWGJmRmY3LXAzUlY1WkYxNlZlVlBIWA?oc=5){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

虎嗅网报道 DeepSeek 安卓端新增对话 Token 计费统计，免费额度收紧引发付费模式猜测，值得关注 AI 产品如何量化使用成本。

**对做产品的启发**：虎嗅报道 DeepSeek 安卓端新增对话 Token 计费统计，免费额度收紧引发付费猜测，属于具体产品功能变化，对理解 AI 产品商业化有迁移价值，但缺乏官方确认和用户反馈。

**继续验证**：关注 DeepSeek 官方是否正式推出付费模式及用户反馈。

**原始来源**：google\_news · 虎嗅网 · 11月27日 18:36 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMiVEFVX3lxTFBwMC1PWFdqaGIzdS1lVXMxc3czYWdoYjJicl92d29leGhQR0NIUlY5d0ppN0lrZE16SDdqMDVGWGJmRmY3LXAzUlY1WkYxNlZlVlBIWA?oc=5){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Function Calling（函数调用）：AI 听懂人话后，去调用外部工具（如公交 API）拿数据的白话解释
- **知识点**：Agent（智能体）：AI 不只是聊天，还能动手帮你完成多步骤任务的白话解释
- **知识点**：RAG（检索增强生成）：AI 可能需要实时查公交数据，而不是只靠训练时的旧知识
- **知识点**：Function Calling（函数调用）：LLM 不只是聊天，还能触发外部工具——这里 LLM 生成代码后，插件自动调用 Convex 的远程 API 来创建项目
- **动手练习**：打开你手机的 Gemini 或类似 AI 助手，尝试用一句话描述一个你日常的小需求（如&#x27;显示今天天气&#x27;或&#x27;倒计时到周末&#x27;），观察 AI 能否直接生成结果或给出可执行的步骤。记录它理解了什么、哪里出错。
- **动手练习**：30 分钟验证：打开 Chrome DevTools 的网络面板（或 VS Code 的 Output &gt; Extension Host），安装任意一个 AI 编程插件（如 Convex、Copilot、Claude Code），输入一个假想的应用想法，观察 Network 标签里有没有出现未预期的出站请求，记录域名和请求体大小，判断哪些数据离开了你的电脑

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
