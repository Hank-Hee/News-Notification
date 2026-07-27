---
layout: default
title: "AI产品情报 · 2026-07-27"
date: 2026-07-27
lang: zh
---

**日期**：2026-07-27　 **更新时间**：2026-07-27 12:16 北京时间

> 从 34 条内容中筛选出 3 条重要资讯。

> 今日高质量增量有限，因此未使用低质量内容补足数量。

<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- 文章展示用 Lean 证明 zstd 压缩算法正确性，讨论 AI 自动化证明，并提及 OpenATP 工具。
- OpenAI 发布 agents-python v0.19.0，新增程序化工具调用，让模型生成 JavaScript 协调工具，提升 Agent 能力。
- 调查揭示中国 LLM token 转售市场，利用开源代理软件 one-api/new-api 提供折扣 API 访问。

<a id="product-teardown"></a>
## 产品拆解

### 1. [AI 自动定理证明：用 Lean 验证 zstd 压缩算法的正确性](https://www.imperialviolet.org/2026/07/26/zstd-lean.html){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：文章展示用 Lean 证明 zstd 压缩算法正确性，讨论 AI 自动化证明，并提及 OpenATP 工具。

**评分**：7.0 / 10　 **证据**：早期信号

**产品 / 团队**：OpenATP / zdw

**目标用户**：形式化验证研究者、编译器/密码学开发者、对 AI+数学证明感兴趣的工程师

**它是什么**：一篇技术博客，展示如何用 Lean（一种数学证明语言）+ AI 自动化工具，来形式化验证 zstd 压缩算法的实现没有 bug。

**用户问题**：传统写代码靠测试找 bug，但测试无法覆盖所有情况；关键系统（如压缩、加密）一旦出错后果严重，需要数学级别的&quot;绝对正确&quot;保证，但人工写形式化证明极其耗时、门槛极高。

**使用流程**：
1. 开发者用 Lean 写出算法实现的&quot;规格说明&quot;（即数学上什么算正确）
2. AI Agent（如 OpenATP 调用的模型）尝试自动生成证明步骤
3. Lean 的验证器检查每一步是否逻辑严谨，不通过则反馈给 AI 继续尝试
4. 证明通过后，代码获得形式化保证，可部署到生产环境

**AI 在做什么**：AI 充当&quot;证明搜索助手&quot;：在巨大的证明策略空间里尝试构造证明步骤，替代人类手动试错；人类负责定义目标和审查关键步骤。

**怎么实现**：核心思路是&quot;证明即搜索&quot;：把数学证明看成在规则树里找路径的游戏，AI 用类似下棋的思路预测下一步该用什么定理/变换；Lean 作为&quot;裁判&quot;实时判定每一步是否合法，形成 AI 提议→验证器检查→反馈迭代的闭环。OpenATP 把这个流程打包成可 benchmark 不同 AI 模型的工具。

**需要理解的知识点**：
1. Lean：一种编程语言，写代码的同时可以写数学证明，编译器会严格检查证明是否成立——可以理解为&quot;不会说谎的代码+数学笔记本&quot;
2. Agent：这里指能自主调用工具（如 Lean 验证器）、根据反馈调整行动的 AI 系统，不只是单次问答
3. Function Calling：AI 调用外部程序（如 Lean 或 Docker 里的验证环境）的能力，让 AI 能&quot;动手做实验&quot;验证自己的猜测

**动手练习**：30 分钟体验：安装 Lean 4（https://lean-lang.org/theorem\_proving\_in\_lean4/），跟着官方教程完成第 1 章&quot;依赖类型入门&quot;，手写一个简单的加法交换律证明（a+b=b+a），感受&quot;代码即证明&quot;的交互过程；有余力可浏览 OpenATP GitHub 看其如何封装模型调用。

**已知限制**：原文正文未抓取到，无法确认 zstd 证明的具体完成度和 AI 自动化程度（是全自动还是人机协作）；OpenATP 的成熟度、支持的模型列表未在输入中详述；社区评论提到的 $150k API 成本和一周推理时间暗示当前成本极高，非普遍可用。

**原始来源**：hackernews · zdw · 7月27日 04:53 北京时间 · [打开原文](https://www.imperialviolet.org/2026/07/26/zstd-lean.html){:target="_blank" rel="noopener noreferrer"}

---
### 2. [OpenAI Agents SDK v0.19.0：让模型自己写 JavaScript 来协调工具](https://github.com/openai/openai-agents-python/releases/tag/v0.19.0){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：OpenAI 发布 agents-python v0.19.0，新增程序化工具调用，让模型生成 JavaScript 协调工具，提升 Agent 能力。

**评分**：9.0 / 10　 **证据**：一手信息

**产品 / 团队**：OpenAI Agents SDK \(openai-agents-python\) / seratch

**目标用户**：用 Python 开发 AI Agent 的工程师，需要模型自动编排多步骤工具调用的场景

**它是什么**：OpenAI 官方 Python SDK 的一个新版本，新增「程序化工具调用」功能，让 AI 模型能生成 JavaScript 代码来串联多个工具完成任务

**用户问题**：以前 Agent 调用工具是&quot;一步一请示&quot;：模型想查天气→调用天气 API→等结果→再决定下一步。步骤多、延迟高，复杂任务需要来回很多次。用户希望模型能一次性规划好整个工具调用流程，减少往返

**使用流程**：
1. 开发者在代码里注册多个工具（如查天气、订机票、发邮件），并标记哪些工具允许被程序化调用
2. 用 \`ProgrammaticToolCallingTool\` 包装这些工具，让模型看到它们的描述和参数
3. 用户提出复杂请求（如&#x27;查北京天气，如果下雨就给我订明天去上海的机票&#x27;），模型自动生成一段 JavaScript 来编排这些工具的调用顺序和条件判断
4. SDK 执行这段 JavaScript，按模型写的逻辑调用工具，返回最终结果

**AI 在做什么**：AI 不再只是&quot;选哪个工具&quot;，而是写一段 JavaScript 代码来当&quot;导演&quot;，决定什么时候调用哪个工具、怎么处理中间结果、什么条件下走分支

**怎么实现**：相当于给模型发了一张&quot;工具清单&quot;和一张&quot;空白剧本纸&quot;。模型根据用户请求，写一段 JavaScript 剧本（比如：先查天气→如果 rain=true 则调用订票→把结果拼成消息）。这段剧本在受控环境里运行，只能调用你允许的工具，跑完把结果还给用户。开发者可以设&quot;谁能被调用&quot;（allowed\_callers）、加审批规则、看执行日志

**需要理解的知识点**：
1. Tool Calling（工具调用）：模型不只会聊天，还能根据你的描述选择并调用外部功能，比如查数据库或发邮件
2. Agent（智能体）：一个能自主规划、调用工具、完成多步骤任务的 AI 系统，不只是单次问答
3. Runner streaming / RunState：SDK 里管任务执行和状态追踪的机制，让你能看到 Agent 每一步在干嘛、中途打断或恢复

**动手练习**：30 分钟动手：从 GitHub 拉 openai-agents-python v0.19.0，跑通官方 examples 里的 tool calling 示例。然后自己写两个假工具（一个返回随机天气，一个返回假机票信息），用 ProgrammaticToolCallingTool 包装，让模型写一段 JS 来根据天气决定是否&quot;订票&quot;，观察生成的 JavaScript 和执行日志

**已知限制**：未公开：具体哪些 OpenAI Responses 模型支持此功能；JavaScript 执行环境的沙箱隔离细节；allowed\_callers 的权限粒度是否支持到用户级别；与第三方 LLM（AnyLLM/LiteLLM）配合时此功能是否可用

**原始来源**：github · seratch · 7月27日 12:10 北京时间 · [打开原文](https://github.com/openai/openai-agents-python/releases/tag/v0.19.0){:target="_blank" rel="noopener noreferrer"}

---

<a id="how-they-build"></a>
## 他们怎么做

_今天没有达到标准的一线构建实践；不会用泛泛观点补位。_

<a id="model-company-news"></a>
## 模型公司动态

_今天没有值得单独展开的模型公司一手动态。_

### 其他值得留意

### [An Inside Look at the Relay Market Powering Token Resellers and Fraud](https://simonwillison.net/2026/Jul/26/relay-market/#atom-everything){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

调查揭示中国 LLM token 转售市场，利用开源代理软件 one-api/new-api 提供折扣 API 访问。

**对做产品的启发**：揭露 LLM token 转售市场，涉及中国代理软件 one-api/new-api，有开源项目链接，对理解 AI 产品生态有增量。

**继续验证**：关注 one-api/new-api 的后续发展及监管动态。

**原始来源**：rss · Simon Willison · 7月27日 03:30 北京时间 · [打开原文](https://simonwillison.net/2026/Jul/26/relay-market/#atom-everything){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Lean：一种编程语言，写代码的同时可以写数学证明，编译器会严格检查证明是否成立——可以理解为&quot;不会说谎的代码+数学笔记本&quot;
- **知识点**：Agent：这里指能自主调用工具（如 Lean 验证器）、根据反馈调整行动的 AI 系统，不只是单次问答
- **知识点**：Function Calling：AI 调用外部程序（如 Lean 或 Docker 里的验证环境）的能力，让 AI 能&quot;动手做实验&quot;验证自己的猜测
- **知识点**：Tool Calling（工具调用）：模型不只会聊天，还能根据你的描述选择并调用外部功能，比如查数据库或发邮件
- **动手练习**：30 分钟体验：安装 Lean 4（https://lean-lang.org/theorem\_proving\_in\_lean4/），跟着官方教程完成第 1 章&quot;依赖类型入门&quot;，手写一个简单的加法交换律证明（a+b=b+a），感受&quot;代码即证明&quot;的交互过程；有余力可浏览 OpenATP GitHub 看其如何封装模型调用。
- **动手练习**：30 分钟动手：从 GitHub 拉 openai-agents-python v0.19.0，跑通官方 examples 里的 tool calling 示例。然后自己写两个假工具（一个返回随机天气，一个返回假机票信息），用 ProgrammaticToolCallingTool 包装，让模型写一段 JS 来根据天气决定是否&quot;订票&quot;，观察生成的 JavaScript 和执行日志

## 数据与筛选说明

- 每天 08:30（北京时间）处理最近 24 小时的公开来源；先程序预筛和历史去重，再由 DeepSeek 批量评分。
- 优先级依次为：真实 AI 产品、构建实践、模型公司核心人员、新能力、精选 Newsletter。
- 纯算力、GPU、底层推理优化和学术论文默认降权，除非能直接解释新的产品机会。
- Top 2 由 Kimi 做初学者版产品拆解；失败时只对该条使用 DeepSeek Pro，所有模型均关闭思考。
- 同一事件执行语义去重和最近 7 天历史去重；结果缓存并同步到 JSON、CSV 和可筛选数据库页面。

[打开产品情报数据库]({{ '/products/' | relative_url }}) · [下载 JSON]({{ '/data/product-intelligence.json' | relative_url }}) · [下载 CSV]({{ '/data/product-intelligence.csv' | relative_url }})

<a id="archives"></a>
## 历史日报

[返回首页查看按日期归档]({{ '/' | relative_url }})
