---
layout: default
title: "AI产品情报 · 2026-10-24"
date: 2026-10-24
lang: zh
---

**日期**：2026-10-24　 **更新时间**：2026-10-24 12:35 北京时间

> 从 166 条内容中筛选出 8 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Simon Willison 用 Claude 提示词做出 Quick Study 工具，上传照片几秒内用画布模拟油画笔触，展示了 AI 辅助快速构建产品的过程。
- Dify 发布 1.18.0，让 Agent 能根据条件选择工作流分支，并支持应用打包迁移和知识库，方便非开发者搭建 AI 应用。
- OpenAI Codex CLI 发布 v0.164.0，新增可复用提示预设、内联模型参数、终端图像预览和企业 MCP 认证等功能。
- 有人做了个本地 AI 搜索工具 Instant Search，帮你在自己电脑文件里快速精确查找，适合看小产品怎么切场景。
- Vercel 介绍其 Agent 如何安全访问生产环境：先只读调查，再提出包含所需权限的计划，用户批准后才执行，避免过度授权。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Quick Study：用 Claude 提示词 5 分钟做出照片转油画工具](https://simonwillison.net/2026/Oct/23/quick-study-painter/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Simon Willison 用 Claude 提示词做出 Quick Study 工具，上传照片几秒内用画布模拟油画笔触，展示了 AI 辅助快速构建产品的过程。

**评分**：8.3 / 10　 **证据**：一手信息

**产品 / 团队**：Quick Study / Simon Willison

**目标用户**：想快速把照片变成油画风格的人；想学习用 AI 辅助写代码的初学者

**它是什么**：一个网页小工具，上传照片后几秒内在画布上用模拟油画笔触重绘出来

**用户问题**：普通照片想有手绘油画感，但用 Photoshop 或专业软件操作复杂、耗时长

**使用流程**：
1. 打开网页，上传一张照片
2. 工具自动分析照片边缘（Sobel 边缘检测）
3. 几秒内用画布逐笔模拟油画效果
4. 保存生成的油画图片

**AI 在做什么**：Claude Opus 5.5 High 根据一句提示词生成完整代码，人类只需复制运行

**怎么实现**：核心就两步：先用 Sobel 算法找出照片里物体轮廓在哪，然后让画笔沿着轮廓和颜色区域一笔一笔画，笔触粗细和方向跟着边缘走，不用任何现成画图库，纯浏览器原生代码搞定

**需要理解的知识点**：
1. Prompt Engineering（提示词工程）：用一句自然语言让 AI 生成可运行代码，关键是描述清楚输入、输出和限制条件
2. Sobel 边缘检测：一种找图片里&#x27;哪里是边界&#x27;的数学方法，像给照片描边
3. Canvas 绘图：浏览器自带的画图板，可以直接用代码控制像素和笔触

**动手练习**：打开 Claude 或任意 LLM，输入类似提示词：&#x27;写一个网页，上传照片后用 Canvas 把它变成点画风格，用圆点代替笔触&#x27;，把生成的 HTML 文件保存到本地双击运行，对比 Quick Study 的效果差异

**已知限制**：未公开具体运行性能（大图是否卡顿）；未公开是否支持调整笔触大小、油画厚度等参数；Claude Opus 5.5 High 是否为真实版本号存疑（常见版本为 Opus 3、Sonnet 3.5 等）

**原始来源**：rss · Simon Willison · 10月24日 05:35 北京时间 · [打开原文](https://simonwillison.net/2026/Oct/23/quick-study-painter/){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Dify 1.18.0 发布：Agent 能自己选工作流分支，应用可打包带走](https://github.com/langgenius/dify/releases/tag/1.18.0){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Dify 发布 1.18.0，让 Agent 能根据条件选择工作流分支，并支持应用打包迁移和知识库，方便非开发者搭建 AI 应用。

**评分**：8.2 / 10　 **证据**：一手信息

**产品 / 团队**：Dify / laipz8200

**目标用户**：产品经理、业务人员、低代码开发者；需要快速搭建 AI 应用但不想写大量代码的团队

**它是什么**：Dify 是一个低代码平台，让不懂编程的人也能搭建 AI Agent（能自主调用工具、完成任务的 AI 助手）和工作流应用，支持自托管或云端部署。

**用户问题**：以前 Agent 只能按固定路径执行工作流，遇到不同情况不会自动分叉；迁移应用到新环境时要手动重建知识库、技能等资源，容易遗漏；嵌套工作流出了问题只能看到黑盒结果，没法逐层排查

**使用流程**：
1. 在可视化画布上拖拽节点，搭建工作流，开启 Agent 的「Output Routes」功能
2. 为每个分支设置条件（如「用户问题能直接回答」走 A 路，「需要转人工」走 B 路）
3. 导出应用为 .ifpkg 文件，在新工作空间一键导入，自动重建所有依赖资源
4. 运行后打开执行历史，逐层展开嵌套工作流，查看每一步的输入输出

**AI 在做什么**：Agent（AI 代理）根据用户输入和预设条件，实时判断该走哪个工作流分支，并能在执行中调用知识库、工具等能力

**怎么实现**：核心是给 Agent 加一个「路由决策层」：每个分支配一个选择条件，Agent 输出时同时返回一个只读的 switch 字段，告诉系统选了哪条路。打包迁移则是把应用本体、Agent 配置、技能文件等压缩成 .ifpkg 格式，导入时自动解析并重映射资源引用。嵌套工作流的可见性是把子工作流也当成独立的图来执行，父子之间用统一的暂停/恢复/停止协议协调。

**需要理解的知识点**：
1. Agent：一种能根据环境反馈自主决定下一步行动的 AI，不只是回答问题，还能调用工具、选择路径
2. 工作流（Workflow）：把任务拆成多个步骤，按顺序或条件执行的流程图，低代码平台通常用拖拽方式搭建
3. RAG（检索增强生成）：让 AI 先查知识库再回答，Agent Knowledge Base 就是给 Agent 配的专属知识库

**动手练习**：30 分钟练习：在 Dify Cloud 或本地部署 1.18.0，创建一个最简单的客服工作流——用户输入问题后，Agent 判断「是否包含订单号」：包含则查询订单状态，不包含则引导用户补充信息。然后导出为 .ifpkg，尝试导入到另一个工作空间验证完整性。

**已知限制**：Agent Knowledge Base 标注为 Beta 且需单独部署服务和数据库，云端版尚未上线；嵌套工作流的用量统计在暂停/停止后可能不准确；本地 Agent 沙箱现在强制要求非空认证令牌，旧版本快照需自动转换。

**原始来源**：github · laipz8200 · 10月23日 14:33 北京时间 · [打开原文](https://github.com/langgenius/dify/releases/tag/1.18.0){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

_最近 7 天没有达到收录标准的新 Newsletter 内容；请查看数据源日志。_

<a id="how-they-build"></a>
## 他们怎么做

### [How Vercel Agent accesses production safely](https://vercel.com/blog/how-vercel-agent-accesses-production-safely){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

Vercel 介绍其 Agent 如何安全访问生产环境：先只读调查，再提出包含所需权限的计划，用户批准后才执行，避免过度授权。

**对做产品的启发**：Vercel 官方博客详解 Agent 安全访问生产环境的权限设计，包含“先调查、再提计划、按计划授权”的实践思路，对构建 AI Agent 产品有可迁移的权限设计经验。

**继续验证**：关注该权限模型在真实生产事故中的表现和用户反馈。

**原始来源**：rss · Tom Dale · 10月24日 04:29 北京时间 · [打开原文](https://vercel.com/blog/how-vercel-agent-accesses-production-safely){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Introducing Kimi K3.1 Pro](https://simonwillison.net/2026/Oct/23/kimi-k31-pro/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.6/10

Moonshot 发布 Kimi K3.1 Pro API，性能接近 Claude Opus 5.5 且价格更低，承诺 11 月 4 日开源权重，值得关注其产品化机会。

**对做产品的启发**：Kimi K3.1 Pro 发布，提供 API 和定价，承诺开源权重，基准接近前沿模型，属于模型公司核心能力动态，可能解锁新产品体验，对产品经理有参考价值。

**继续验证**：关注开源权重发布后的社区应用和实际产品集成案例。

**原始来源**：rss · Simon Willison · 10月24日 03:40 北京时间 · [打开原文](https://simonwillison.net/2026/Oct/23/kimi-k31-pro/){:target="_blank" rel="noopener noreferrer"}

### [Jack Dorsey’s Block made an AI model that talks to you like an awkward new friend](https://www.theverge.com/ai-artificial-intelligence/1017906/jack-dorsey-block-dessa-ai-voice-speech){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Jack Dorsey 的 Block 做了个语音模型 Dessa，只用人类对话训练，说话像新朋友有点笨拙，展示了不一样的对话体验。

**对做产品的启发**：Block 发布只用人类对话训练的语音模型 Dessa，并展示真实对话样例，属于模型公司核心动态且有可感知的产品体验，对做对话产品有迁移价值，接近 8 分。

**继续验证**：看 Dessa 是否开放 API 或集成到 Block 产品，以及用户真实反馈。

**原始来源**：rss · Jay Peters · 10月24日 03:32 北京时间 · [打开原文](https://www.theverge.com/ai-artificial-intelligence/1017906/jack-dorsey-block-dessa-ai-voice-speech){:target="_blank" rel="noopener noreferrer"}

### [Donating Agent Skills To The Agentic Ai Foundation](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Anthropic 把 Agent Skills 捐给 Agentic AI Foundation，想让 Agent 技能有统一标准，值得关注 Agent 生态怎么变。

**对做产品的启发**：Anthropic 官方宣布将 Agent Skills 捐赠给 Agentic AI Foundation，属于 Agent 生态标准化的一手动态，对构建者理解 Agent 能力复用有迁移价值，但缺少具体产品体验和用户反馈。

**继续验证**：关注基金会成员、技能规范细节和是否有产品采用。

**原始来源**：public\_web · Anthropic News · 10月23日 01:48 北京时间 · [打开原文](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [openai/codex released rust-v0.164.0](https://github.com/openai/codex/releases/tag/rust-v0.164.0){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

OpenAI Codex CLI 发布 v0.164.0，新增可复用提示预设、内联模型参数、终端图像预览和企业 MCP 认证等功能。

**对做产品的启发**：OpenAI Codex CLI 发布新版本，新增预设提示、模型参数内联设置、图像预览、企业 MCP 认证等，属于开发者工具迭代，对构建 AI 产品有参考但非核心产品案例。

**继续验证**：关注新功能在实际编码工作流中的采用和反馈。

**原始来源**：github · github-actions\[bot\] · 10月23日 12:48 北京时间 · [打开原文](https://github.com/openai/codex/releases/tag/rust-v0.164.0){:target="_blank" rel="noopener noreferrer"}

### [Instant Search](https://www.producthunt.com/products/instant-search-2){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

有人做了个本地 AI 搜索工具 Instant Search，帮你在自己电脑文件里快速精确查找，适合看小产品怎么切场景。

**对做产品的启发**：Product Hunt 上线的本地 AI 文件搜索产品，有明确使用场景和产品页，但信息量少、无用户反馈细节，属于可迁移的小产品案例，刚过 7 分。

**继续验证**：看是否有用户评价和实际检索效果演示。

**原始来源**：rss · Dmitry Dolgopolov · 10月23日 13:36 北京时间 · [打开原文](https://www.producthunt.com/products/instant-search-2){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Prompt Engineering（提示词工程）：用一句自然语言让 AI 生成可运行代码，关键是描述清楚输入、输出和限制条件
- **知识点**：Sobel 边缘检测：一种找图片里&#x27;哪里是边界&#x27;的数学方法，像给照片描边
- **知识点**：Canvas 绘图：浏览器自带的画图板，可以直接用代码控制像素和笔触
- **知识点**：Agent：一种能根据环境反馈自主决定下一步行动的 AI，不只是回答问题，还能调用工具、选择路径
- **动手练习**：打开 Claude 或任意 LLM，输入类似提示词：&#x27;写一个网页，上传照片后用 Canvas 把它变成点画风格，用圆点代替笔触&#x27;，把生成的 HTML 文件保存到本地双击运行，对比 Quick Study 的效果差异
- **动手练习**：30 分钟练习：在 Dify Cloud 或本地部署 1.18.0，创建一个最简单的客服工作流——用户输入问题后，Agent 判断「是否包含订单号」：包含则查询订单状态，不包含则引导用户补充信息。然后导出为 .ifpkg，尝试导入到另一个工作空间验证完整性。

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
