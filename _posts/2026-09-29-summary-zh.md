---
layout: default
title: "AI产品情报 · 2026-09-29"
date: 2026-09-29
lang: zh
---

**日期**：2026-09-29　 **更新时间**：2026-09-29 13:44 北京时间

> 从 116 条内容中筛选出 9 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Claire Vo 实测 TypeSafe AI 的决策模型 Jev，用它在五个真实项目上做分类和打分，1700 个 PR 只花 9 美分。
- 有人在家训练了一个 0.8B 的决策小模型 Jeff，兼容 Jev 接口、响应约 30 毫秒，用户实测分类准确率 70% 不如 Jev 的 94%，但展示了小模型替代大模型做分类的可能性。
- 有人做了个 MicroLLM Lab 网站，能在浏览器里直接试 7 个小模型，用户反馈界面太挤、小模型算 2+2 都会出错，适合初学者直观感受小模型的能力边界。
- Anthropic 的 Thariq Shihipar 在 Latent Space 播客讲 Claude Code 下一阶段，涉及 Opus/Sonnet 5.5、Mods、Plugins、Projects 等新功能，是理解编码 Agent 产品演进的一手材料。
- 开发者做了一个 Pac-Bench 网站，用同一句提示词让各家模型一次性生成吃豆人游戏并对比效果，值得看是因为它用可玩 Demo 直观比较了模型的代码生成能力。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Jev 入门：怎么用、能搭什么——Claire Vo 的 5 个真实项目实测](https://www.lennysnewsletter.com/p/jev-for-beginners-how-to-use-it-and){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Claire Vo 实测 TypeSafe AI 的决策模型 Jev，用它在五个真实项目上做分类和打分，1700 个 PR 只花 9 美分。

**评分**：8.2 / 10　 **证据**：已核验

**产品 / 团队**：Jev \(TypeSafe AI\) / Claire Vo

**目标用户**：需要低成本、高并发做分类/打分/决策的开发者、AI 产品经理，以及想把 LLM 当&quot;评分器&quot;而非&quot;写手&quot;用的人。

**它是什么**：TypeSafe AI 推出的决策模型，不生成文本，直接返回类型安全的结构化结果（选项、分数、概率），定价为 4 美分/百万输入 token，不收输出费。

**用户问题**：用传统 LLM 做分类或打分时，需要解析生成的文本，容易格式错乱、成本高；输出 token 按量计费，大规模跑数据账单不可控。

**使用流程**：
1. 定义输出结构（比如：category 选 A/B/C，confidence 打 0-1 分）
2. 把原始数据（PR 标题、邮件、评论等）丢给 Jev
3. 拿到结构化结果，直接进数据库或下游流程
4. 必要时搭配其他 LLM 做后续生成或回复

**AI 在做什么**：AI 充当&quot;自动评分员+分类器&quot;，把非结构化输入变成程序可直接用的结构化数值，省去解析文本的麻烦。

**怎么实现**：本质上是个&quot;输入→结构化判断&quot;的函数。你像调用 API 一样传一段文本，Jev 内部做推理后，按你预定的格式返回 JSON 式的确定值，不走生成文本那条路，所以又快又便宜。

**需要理解的知识点**：
1. 结构化输出（Structured Output）：让模型返回固定格式的数据而非自由文本，方便程序直接消费
2. 决策模型 vs 生成模型：前者专精&quot;判断和打分&quot;，后者专精&quot;写东西&quot;，选型要看任务类型
3. Token 计费方式：输入/输出分开计价，不收输出费对大批量推理成本影响极大

**动手练习**：用 Jev 或任何支持结构化输出的模型，拿 50 条你自己的邮件或聊天记录做分类实验：先手写 10 条标注好类别，让模型分类剩余 40 条，对比准确率并算总 token 成本。

**已知限制**：Jev 的模型规模、训练数据、是否支持多语言、延迟具体数值、与主流框架的集成方式均未公开；Claire Vo 提到&quot;不再单独用 Jev&quot;，说明复杂场景仍需搭配其他模型。

**原始来源**：newsletter · Claire Vo · 9月28日 20:03 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/jev-for-beginners-how-to-use-it-and){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Jeff：在家训练的 0.8B 决策小模型，兼容 Jev 接口，延迟约 30 毫秒](https://github.com/firelex/jeff){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：有人在家训练了一个 0.8B 的决策小模型 Jeff，兼容 Jev 接口、响应约 30 毫秒，用户实测分类准确率 70% 不如 Jev 的 94%，但展示了小模型替代大模型做分类的可能性。

**评分**：8.2 / 10　 **证据**：已核验

**产品 / 团队**：Jeff / firelex

**目标用户**：想在自己的应用里嵌入快速分类/决策能力、又不想调用昂贵大模型 API 的开发者；对「小模型能做什么」感兴趣的学习者

**它是什么**：一个由个人开发者在家训练、开源的 8 亿参数小型决策模型，能替代大模型做简单的分类判断，响应速度比大模型快得多。

**用户问题**：调用大模型做简单分类任务太贵、太慢；开发者想知道「能不能用一个极小的本地模型搞定同样的活」

**使用流程**：
1. 把 Jeff 模型下载到本地或部署到服务器
2. 像调用 Jev API 一样发请求（输入文本，要求做分类/决策）
3. 模型在约 30 毫秒内返回判断结果
4. 把结果接入自己的业务逻辑（如过滤、路由、标记）

**AI 在做什么**：接收输入后直接输出分类或决策结果，不做长篇生成，只做一个快速的「是/否」或「A/B/C」判断

**怎么实现**：用远小于 GPT-4 的神经网络（8 亿参数，约是 GPT-4 的千分之一）专门训练做「二选一」或「多选一」的判断题。因为任务单一，模型可以很小；因为模型小，普通电脑就能跑，响应也只要几十毫秒。

**需要理解的知识点**：
1. 模型参数规模：B 是 Billion（十亿），0.8B 就是 8 亿个可调数值，规模越小跑得越快但能力越窄
2. Embedding（嵌入）：把文字转成数字向量的技术，有人讨论能不能干脆不用完整模型、只用嵌入向量做分类，这是更轻量的替代思路
3. Function Calling（函数调用）：大模型的一种能力，让 AI 决定调用哪个外部工具；Jeff 这类决策模型做的就是类似的「路由判断」，但用更小更快的方案实现

**动手练习**：30 分钟：去 https://github.com/firelex/jeff 下载代码，按 README 跑通本地推理，拿一段你自己的文本测试分类效果，记录延迟和准确率；再对比调用一次免费大模型 API 做同样任务的速度和成本差异。

**已知限制**：Jev 本身的架构细节未公开（社区用户质疑「没有清晰实现细节」）；Jeff 的 70% 准确率仅来自一位用户 \[AgentMasterRace\] 的实测反馈，非系统性评测；训练数据、具体任务范围、是否支持多语言均未公开；目前只是个人实验项目，非商业产品。

**原始来源**：hackernews · firelex · 9月29日 04:23 北京时间 · [打开原文](https://github.com/firelex/jeff){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [Jev 入门：怎么用、能搭什么——Claire Vo 的 5 个真实项目实测](https://www.lennysnewsletter.com/p/jev-for-beginners-how-to-use-it-and){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Claire Vo 实测 TypeSafe AI 的决策模型 Jev，用它在五个真实项目上做分类和打分，1700 个 PR 只花 9 美分。

**对做产品的启发**：Claire Vo 一手实践：TypeSafe AI 的 Jev 返回类型安全的结构化值（选择、分数、概率）而非生成文本，4 美分/百万输入 token 且不收输出费；她在五个真实项目上跑通（PR 分类、Claude/Codex 会话元分析、Gmail 分拣、ChatPRD 洞察图、4500 条 YouTube 评论实时看板），并给出 1700 个 PR 花 9 美分的具体成本，属于有真实反馈的产品案例，对做 AI 产品选型很有迁移价值。

**继续验证**：关注 Jev 在分类/打分场景相比通用 LLM 的准确率对比，以及是否开放 API 试用。

**原始来源**：newsletter · Claire Vo · 9月28日 20:03 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/jev-for-beginners-how-to-use-it-and){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [Claude Code’s Next Era — Thariq Shihipar, Anthropic](https://www.latent.space/p/thariq){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.0/10

Anthropic 的 Thariq Shihipar 在 Latent Space 播客讲 Claude Code 下一阶段，涉及 Opus/Sonnet 5.5、Mods、Plugins、Projects 等新功能，是理解编码 Agent 产品演进的一手材料。

**对做产品的启发**：Anthropic Claude Code 负责人 Thariq Shihipar 在 Latent Space 谈 Opus/Sonnet 5.5、Mods、Plugins、Projects 等新形态，属构建者一手产品思路，对 AI 产品经理高价值。

**继续验证**：播客中提到的 Mods/Plugins/Projects 具体形态与发布时间。

**原始来源**：rss · Latent Space · 9月29日 09:48 北京时间 · [打开原文](https://www.latent.space/p/thariq){:target="_blank" rel="noopener noreferrer"}

### [Show HN: Pac-Bench – How well can models one-shot a Pac-Man game?](https://jonclegg.github.io/pacman-bakeoff/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

开发者做了一个 Pac-Bench 网站，用同一句提示词让各家模型一次性生成吃豆人游戏并对比效果，值得看是因为它用可玩 Demo 直观比较了模型的代码生成能力。

**对做产品的启发**：作者自建可验证 Demo，用同一句提示词让各模型一次性生成吃豆人游戏并公开对比结果，属构建者一手实践，能让初学者直观理解模型代码生成能力差异；但热度较低、方法争议存在。

**继续验证**：关注作者是否补充更多模型结果，以及社区对提示词过短导致评测偏差的讨论。

**原始来源**：hackernews · thefourthchime · 9月29日 06:43 北京时间 · [打开原文](https://jonclegg.github.io/pacman-bakeoff/){:target="_blank" rel="noopener noreferrer"}

### [Quoting @joedaroo](https://simonwillison.net/2026/Sep/28/joedaroo/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

OpenAI Agent Security 的 @joedaroo 反思模型在网络安全、群体行为等能力上突然跃升，远超团队预期，提醒各组织提前准备人员、流程和应急响应，做 Agent 产品的人值得一读。

**对做产品的启发**：OpenAI Agent Security 人员一手反思模型能力突跳带来的安全与组织挑战，对做 Agent 产品的人有可迁移的工程与流程启示。

**继续验证**：OpenAI 是否公开 Agent 安全事件响应框架或工具。

**原始来源**：rss · Simon Willison · 9月29日 03:11 北京时间 · [打开原文](https://simonwillison.net/2026/Sep/28/joedaroo/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude Discovers Novel Enzyme System](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Anthropic 官方称 Claude 发现了一种新的酶系统，展示大模型在生物科学发现中的实际用途，值得关注 AI 在医药研发场景的产品化可能。

**对做产品的启发**：Anthropic 官方发布 Claude 发现新酶系统的研究更新，属模型公司一手动态，且展示了模型在科学发现这一新场景中的实际能力，对探索垂直 AI 产品（尤其医药/生物）有直接启发。但正文仅有占位描述，缺少可验证细节与用户使用路径，故未进入 9 分区间。

**继续验证**：等待官方补充实验细节、可复现方法或合作方信息，判断是否可迁移为垂直科研产品。

**原始来源**：public\_web · Anthropic News · 9月24日 18:25 北京时间 · [打开原文](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"}

### [Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Anthropic 发布 Claude Sonnet 5.5，用户实测它能一次生成可玩的吃豆人游戏，值得看是因为这直接展示了当前模型写代码的实际水平。

**对做产品的启发**：Anthropic 官方发布 Sonnet 5.5，属模型公司一手能力动态，HN 698 分高热讨论，评论中给出可验证的 one-shot Pac-Man 实测链接，对初学者理解模型能力边界有直接参考价值。

**继续验证**：关注 Sonnet 5.5 与 Opus 5.5 的定价与使用场景差异，以及社区 one-shot 编码基准的横向对比结果。

**原始来源**：hackernews · D2OQZG8l5BI1S06 · 9月29日 01:58 北京时间 · [打开原文](https://www.anthropic.com/claude-sonnet-5-5){:target="_blank" rel="noopener noreferrer"}

### [anthropics/claude-code released v2.1.284](https://github.com/anthropics/claude-code/releases/tag/v2.1.284){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

Anthropic 在 Claude Code 里把新的 Claude Sonnet 5.5 设为默认模型，支持 100 万上下文并给出明确价格，还加了花费显示和 MCP 一键重连，让开发者用起来更省心。

**对做产品的启发**：Claude Code 发布 v2.1.284，新增 Claude Sonnet 5.5 并设为默认 Sonnet 模型，1M 上下文、$2/$10 定价，同时加入用量花费显示、MCP 批量重连等实用功能，属于模型能力与产品体验的真实增量。

**继续验证**：观察 Sonnet 5.5 在真实编码任务中的表现与成本对比，以及 1M 上下文对长代码库场景的实际价值。

**原始来源**：github · ashwin-ant · 9月29日 02:02 北京时间 · [打开原文](https://github.com/anthropics/claude-code/releases/tag/v2.1.284){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [MicroLLM Lab – Try 7 tiny LLM&#x27;s in the browser](https://stateofutopia.com/experiments/microllmlab/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

有人做了个 MicroLLM Lab 网站，能在浏览器里直接试 7 个小模型，用户反馈界面太挤、小模型算 2+2 都会出错，适合初学者直观感受小模型的能力边界。

**对做产品的启发**：MicroLLM Lab 是一个可在浏览器里直接试用 7 个小模型的产品，有真实用户反馈（界面太密、小模型算术出错等），对初学者理解“小模型能做什么、产品体验如何”有直接参考价值。

**继续验证**：观察作者是否根据反馈优化界面，以及小模型在浏览器端的产品化路径。

**原始来源**：hackernews · logicallee · 9月29日 02:58 北京时间 · [打开原文](https://stateofutopia.com/experiments/microllmlab/){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：结构化输出（Structured Output）：让模型返回固定格式的数据而非自由文本，方便程序直接消费
- **知识点**：决策模型 vs 生成模型：前者专精&quot;判断和打分&quot;，后者专精&quot;写东西&quot;，选型要看任务类型
- **知识点**：Token 计费方式：输入/输出分开计价，不收输出费对大批量推理成本影响极大
- **知识点**：模型参数规模：B 是 Billion（十亿），0.8B 就是 8 亿个可调数值，规模越小跑得越快但能力越窄
- **动手练习**：用 Jev 或任何支持结构化输出的模型，拿 50 条你自己的邮件或聊天记录做分类实验：先手写 10 条标注好类别，让模型分类剩余 40 条，对比准确率并算总 token 成本。
- **动手练习**：30 分钟：去 https://github.com/firelex/jeff 下载代码，按 README 跑通本地推理，拿一段你自己的文本测试分类效果，记录延迟和准确率；再对比调用一次免费大模型 API 做同样任务的速度和成本差异。

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
