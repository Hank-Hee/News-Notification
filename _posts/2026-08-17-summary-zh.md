---
layout: default
title: "AI产品情报 · 2026-08-17"
date: 2026-08-17
lang: zh
---

**日期**：2026-08-17　 **更新时间**：2026-08-17 09:56 北京时间

> 从 136 条内容中筛选出 12 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- ChatGPT macOS 桌面应用新增 Computer History 功能，记录点击和键盘操作，用于学习用户习惯并建议自动化。
- 开发者展示了一个所有用户共享记忆的 AI，旨在提高团队协作效率，但需警惕滥用风险。
- browser-use 发布 0.13.8，修复了多个 Agent 和 DOM 处理问题，并更新了 Cerebras 模型支持。
- PyScrappy 是一个自愈式网页抓取选择器，并提供 MCP 服务器，解决选择器失效问题。
- 开发者将 DeepSeek V4 Flash 压缩至 57GB 并在 Mac 上运行，成功编写编译器，展示了本地运行大模型的可能性。

<a id="product-teardown"></a>
## 产品拆解

### 1. [ChatGPT macOS 桌面应用新增 Computer History：记录点击和按键来训练 AI](https://www.theverge.com/ai-artificial-intelligence/980742/chatgpts-computer-history-tracks-your-clicks-and-keystrokes){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：ChatGPT macOS 桌面应用新增 Computer History 功能，记录点击和键盘操作，用于学习用户习惯并建议自动化。

**评分**：8.5 / 10　 **证据**：媒体报道

**产品 / 团队**：ChatGPT macOS 桌面应用 / Terrence O’Brien

**目标用户**：macOS 系统下的 ChatGPT 桌面应用用户，需要自动化重复工作流程的人

**它是什么**：ChatGPT macOS 桌面版的一个新功能，自动记录用户在电脑上的点击和键盘操作，生成时间线，让 AI 学习你的工作方式并推荐自动化操作。

**用户问题**：用户每天重复大量手动操作（点击、输入、切换应用），AI 不了解你的工作上下文，无法主动帮你完成或续接未做完的任务

**使用流程**：
1. 在 macOS 上安装并开启 ChatGPT 桌面应用的 Computer History 功能
2. 正常使用电脑，功能后台记录点击、按键等操作，生成个人活动时间线
3. 向 ChatGPT 或 Codex 发起请求时，AI 参考你的操作历史理解上下文
4. AI 根据学习到的习惯，主动推荐自动化流程或续接你未完成的工作

**AI 在做什么**：分析用户的操作时间线，学习行为模式，在收到请求时结合历史上下文理解意图，并生成自动化建议或续接任务

**怎么实现**：在本地持续监听用户的点击和键盘事件，把操作序列按时间整理成结构化日志；当用户提问时，将这些日志作为上下文（类似 RAG，即检索增强生成：先搜你的历史再回答）喂给模型，让 AI 推断出用户的习惯和工作流，再调用自动化工具执行。

**需要理解的知识点**：
1. RAG（检索增强生成）：AI 回答前先从你的个人操作记录里检索相关信息，而不是只靠训练时的记忆
2. AI Agent（AI 代理）：AI 不仅能回答问题，还能观察环境、做决定并执行实际操作
3. Function Calling（函数调用）：AI 判断需要做什么后，调用系统功能来完成自动化，比如模拟点击或执行脚本

**动手练习**：30 分钟体验：打开 macOS 的&#x27;屏幕使用时间&#x27;或任意按键记录工具，手动记录自己 1 小时内的重复操作（如打开固定网站、复制粘贴固定内容）；然后尝试用 ChatGPT 的 Codex 或任何自动化工具（如 Apple Shortcuts）写一个简单脚本完成其中一个重复任务，体会&#x27;让 AI 学习行为再自动化&#x27;的思路。

**已知限制**：该功能的具体隐私政策、数据存储位置（本地还是云端）、用户是否可选择性关闭/删除记录、是否支持所有 macOS 应用还是仅限部分应用，均未公开；目前仅为 The Verge 报道的产品功能更新，尚未确认是否已向所有用户推送。

**原始来源**：rss · Terrence O’Brien · 8月16日 22:56 北京时间 · [打开原文](https://www.theverge.com/ai-artificial-intelligence/980742/chatgpts-computer-history-tracks-your-clicks-and-keystrokes){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Show HN: 一个所有用户共享记忆的公共 AI](https://wildstatic.com/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：开发者展示了一个所有用户共享记忆的 AI，旨在提高团队协作效率，但需警惕滥用风险。

**评分**：8.5 / 10　 **证据**：早期信号

**产品 / 团队**：WildStatic / adjohu

**目标用户**：开发团队、小团队协作场景；目前未公开更明确的用户画像

**它是什么**：WildStatic 是一个公共聊天界面，所有人跟同一个 AI 对话，且 AI 会把所有对话历史当作共享记忆，后续用户能继承之前聊过的上下文。

**用户问题**：团队成员各自开独立 AI 会话时，重复问相似问题、提示词冗余重叠，导致 AI 学习效率低、团队接受度差

**使用流程**：
1. 打开公共网页，直接进入同一个共享会话
2. 像聊天一样输入问题，AI 基于之前所有用户的对话历史回答
3. 后续用户提问时，AI 自动引用已积累的记忆，减少重复解释
4. 高流量时 AI 可能选择性忽略部分消息（开发者正在调整）

**AI 在做什么**：作为团队的&#x27;公共终端&#x27;，持续学习所有人的对话，把历史上下文用于回答新用户的问题

**怎么实现**：本质上是把通常&#x27;每个用户隔离&#x27;的聊天会话，改成&#x27;所有人共用同一份对话历史&#x27;。AI 每次回复时能看到之前所有用户说过的话，就像一块公共白板，所有人都在上面写字，后来者能看到前面写的内容。开发者 adjohu 提到会面临流量压力和 token 限制问题，说明底层仍是调用 LLM API，只是会话层做了共享设计。

**需要理解的知识点**：
1. 上下文窗口（Context Window）：LLM 能&#x27;记住&#x27;的最近文字量有限，共享记忆多了会撑爆这个窗口，导致 AI 丢信息或选择性忽略
2. 提示词注入/滥用风险：公共记忆意味着恶意用户可以通过对话给 AI&#x27;洗脑&#x27;，类似 2016 年微软 Tay.ai 被用户教坏的事件
3. RAG（检索增强生成）：一种让 AI 查外部数据库来补充记忆的技术，但 WildStatic 目前未公开是否用了 RAG，可能只是直接把历史对话塞进上下文

**动手练习**：用任意 LLM（ChatGPT/Claude/国产大模型）做对比实验：先新建一个对话问&#x27;我们团队做电商网站，推荐技术栈&#x27;，然后另开一个新对话问&#x27;继续，怎么部署&#x27;，观察 AI 是否记得&#x27;电商网站&#x27;；再在原对话里继续问，对比两种体验。思考：如果 10 个人共享同一个对话，好处和麻烦各是什么？

**已知限制**：未公开技术架构（是否用 RAG、向量数据库、如何防篡改共享记忆）；未公开商业模式；高流量下的选择性忽略是临时限制还是设计取舍未说明；无独立第三方验证其&#x27;学习效率更高&#x27;的说法

**原始来源**：hackernews · adjohu · 8月16日 21:21 北京时间 · [打开原文](https://wildstatic.com/){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [OpenAI’s Head of Design: This is the best time in history to be a designer \| Ian Silber](https://www.lennysnewsletter.com/p/openais-head-of-design-this-is-the){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

OpenAI 设计负责人 Ian Silber 访谈，讨论设计师在 AI 时代的最佳机遇，对 AI 产品设计有启发。

**对做产品的启发**：OpenAI 设计负责人 Ian Silber 的访谈，提供设计在 AI 产品中的角色和最佳实践，对产品设计有启发，但无具体产品案例或数据。

**继续验证**：关注访谈中提到的具体设计方法和案例。

**原始来源**：newsletter · Lenny Rachitsky · 8月16日 20:31 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/openais-head-of-design-this-is-the){:target="_blank" rel="noopener noreferrer"}

### [not much happened today](https://news.smol.ai/issues/26-08-10-not-much/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Meta 发布开源多模态模型 Muse Glimmer 并预告 Spark 1.2，值得关注其开源策略。

**对做产品的启发**：Meta 发布 Muse Glimmer 30B 开源模型并承诺发布 Spark 1.2 权重，属于模型能力更新，但信息来自 newsletter，非一手，评分 7.0。

**继续验证**：关注 Spark 1.2 权重发布及 Muse Glimmer 的实际应用。

**原始来源**：newsletter · AI News · 8月10日 13:44 北京时间 · [打开原文](https://news.smol.ai/issues/26-08-10-not-much/){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [Show HN: I shrank DeepSeek V4 Flash to 57GB and it wrote a compiler on my Mac](https://huggingface.co/steadfastgaze/DeepSeek-V4-Flash-0731-Coder-56.8GB-MoEspressoV2){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

开发者将 DeepSeek V4 Flash 压缩至 57GB 并在 Mac 上运行，成功编写编译器，展示了本地运行大模型的可能性。

**对做产品的启发**：构建者展示了将 DeepSeek V4 Flash 压缩到 57GB 并在 Mac 上运行，成功编写编译器，有 Demo 和代码，展示了模型压缩和本地部署的可行性。

**继续验证**：关注压缩后的模型性能损失和实际应用场景。

**原始来源**：hackernews · hacklas · 8月17日 01:13 北京时间 · [打开原文](https://huggingface.co/steadfastgaze/DeepSeek-V4-Flash-0731-Coder-56.8GB-MoEspressoV2){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Qwen 3.8 27B is excellent, but it defaults to wildly overthinking things](https://simonwillison.net/2026/Aug/16/qwen-38-27b/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

阿里 Qwen 3.8 27B 模型发布，Simon Willison 实测发现其性能优秀但默认过度思考。

**对做产品的启发**：Qwen 3.8 27B 发布，Apache 2.0 许可，Simon Willison 实测指出其过度思考问题，提供一手体验，对本地模型部署有参考价值。

**继续验证**：关注独立基准测试和后续版本对过度思考的优化。

**原始来源**：rss · Simon Willison · 8月17日 06:00 北京时间 · [打开原文](https://simonwillison.net/2026/Aug/16/qwen-38-27b/){:target="_blank" rel="noopener noreferrer"}

### [Claude: System Prompts](https://platform.claude.com/docs/en/release-notes/system-prompts){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

Anthropic 更新了 Claude 的系统提示词，揭示了模型行为细节，对开发者有重要参考价值。

**对做产品的启发**：Anthropic 官方发布 Claude 系统提示词更新，对理解模型行为、构建 Agent 有直接参考价值，且 simonw 提供了 diff 便于追踪变化。

**继续验证**：关注提示词变化对下游应用的影响。

**原始来源**：hackernews · tosh · 8月16日 20:48 北京时间 · [打开原文](https://platform.claude.com/docs/en/release-notes/system-prompts){:target="_blank" rel="noopener noreferrer"}

### [openai/openai-agents-python released v0.21.1](https://github.com/openai/openai-agents-python/releases/tag/v0.21.1){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

OpenAI Agents Python SDK v0.21.1 发布，新增模型调用超时和沙箱工作目录等特性。

**对做产品的启发**：OpenAI Agents Python SDK 发布 v0.21.1，新增模型调用超时、沙箱工作目录等多项功能，对 Agent 开发有实际价值。

**继续验证**：关注新特性在 Agent 开发中的应用。

**原始来源**：github · seratch · 8月17日 06:28 北京时间 · [打开原文](https://github.com/openai/openai-agents-python/releases/tag/v0.21.1){:target="_blank" rel="noopener noreferrer"}

### [国家超算互联网上线 DeepSeek V4 Pro 正式版 - 观点网](https://news.google.com/rss/articles/CBMiYkFVX3lxTFBEd2wyVVJmVFRTcHJsUG5uMVRaLXJMZWVLd1J3aHRhNDhQXzh5UzhvQ25jczlxcW1zWUJJWGhKWUE5UXY3U3pfUXhPWF9XLTd4S2FuSElpdXhmbFJPQ0F1VEJB?oc=5){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

国家超算互联网上线了 DeepSeek V4 Pro 正式版，提供更强大的算力支持。

**对做产品的启发**：国家超算互联网上线 DeepSeek V4 Pro 正式版，是模型部署的重要进展，但缺乏细节。

**继续验证**：关注该部署对模型使用和性能的影响。

**原始来源**：google\_news · 观点网 · 8月17日 07:48 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMiYkFVX3lxTFBEd2wyVVJmVFRTcHJsUG5uMVRaLXJMZWVLd1J3aHRhNDhQXzh5UzhvQ25jczlxcW1zWUJJWGhKWUE5UXY3U3pfUXhPWF9XLTd4S2FuSElpdXhmbFJPQ0F1VEJB?oc=5){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [browser-use/browser-use released 0.13.8](https://github.com/browser-use/browser-use/releases/tag/0.13.8){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

browser-use 发布 0.13.8，修复了多个 Agent 和 DOM 处理问题，并更新了 Cerebras 模型支持。

**对做产品的启发**：browser-use 是活跃的开源 AI Agent 项目，本次发布包含多项修复和模型支持更新，对使用该库的开发者有直接价值，但属于常规迭代，增量有限。

**继续验证**：关注后续版本是否引入新功能或重大变更。

**原始来源**：github · gregpr07 · 8月17日 02:48 北京时间 · [打开原文](https://github.com/browser-use/browser-use/releases/tag/0.13.8){:target="_blank" rel="noopener noreferrer"}

### [Show HN: PyScrappy, self-healing web scraping selectors plus an MCP server](https://github.com/mldsveda/PyScrappy){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.5/10

PyScrappy 是一个自愈式网页抓取选择器，并提供 MCP 服务器，解决选择器失效问题。

**对做产品的启发**：PyScrappy 是自愈式网页抓取选择器并带 MCP 服务器，有明确产品形态和代码，但评论少，成熟度待验证。

**继续验证**：关注其缓存策略和实际使用反馈。

**原始来源**：hackernews · vedaant00 · 8月16日 15:46 北京时间 · [打开原文](https://github.com/mldsveda/PyScrappy){:target="_blank" rel="noopener noreferrer"}

### [DeepSeek 调价今日正式生效 涨幅最高达 1100% 空闲时段价格为高峰的一半 - 东方财富](https://news.google.com/rss/articles/CBMiZkFVX3lxTFBYS2Vuc2dZcjJZb1NIVkR5NkNQMU9peldUbm1TNXdzU2dNOTlxQU9pQ29ZM0VjS3dqV0V1ZTdLYnFWV09lSVZrbmZreFJlNHVHdHFTZkZXOEZRWlVFdzA3cXg2eVZ3Zw?oc=5){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

DeepSeek API 调价正式生效，最高涨幅达 1100%，空闲时段价格减半，影响开发者成本。

**对做产品的启发**：DeepSeek 调价正式生效，涨幅最高达 1100%，采用峰谷定价，对开发者成本有重大影响。

**继续验证**：关注调价后开发者的反应和模型使用量变化。

**原始来源**：google\_news · 东方财富 · 8月17日 09:08 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMiZkFVX3lxTFBYS2Vuc2dZcjJZb1NIVkR5NkNQMU9peldUbm1TNXdzU2dNOTlxQU9pQ29ZM0VjS3dqV0V1ZTdLYnFWV09lSVZrbmZreFJlNHVHdHFTZkZXOEZRWlVFdzA3cXg2eVZ3Zw?oc=5){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：RAG（检索增强生成）：AI 回答前先从你的个人操作记录里检索相关信息，而不是只靠训练时的记忆
- **知识点**：AI Agent（AI 代理）：AI 不仅能回答问题，还能观察环境、做决定并执行实际操作
- **知识点**：Function Calling（函数调用）：AI 判断需要做什么后，调用系统功能来完成自动化，比如模拟点击或执行脚本
- **知识点**：上下文窗口（Context Window）：LLM 能&#x27;记住&#x27;的最近文字量有限，共享记忆多了会撑爆这个窗口，导致 AI 丢信息或选择性忽略
- **动手练习**：30 分钟体验：打开 macOS 的&#x27;屏幕使用时间&#x27;或任意按键记录工具，手动记录自己 1 小时内的重复操作（如打开固定网站、复制粘贴固定内容）；然后尝试用 ChatGPT 的 Codex 或任何自动化工具（如 Apple Shortcuts）写一个简单脚本完成其中一个重复任务，体会&#x27;让 AI 学习行为再自动化&#x27;的思路。
- **动手练习**：用任意 LLM（ChatGPT/Claude/国产大模型）做对比实验：先新建一个对话问&#x27;我们团队做电商网站，推荐技术栈&#x27;，然后另开一个新对话问&#x27;继续，怎么部署&#x27;，观察 AI 是否记得&#x27;电商网站&#x27;；再在原对话里继续问，对比两种体验。思考：如果 10 个人共享同一个对话，好处和麻烦各是什么？

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
