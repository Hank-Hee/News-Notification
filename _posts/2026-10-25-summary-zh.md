---
layout: default
title: "AI产品情报 · 2026-10-25"
date: 2026-10-25
lang: zh
---

**日期**：2026-10-25　 **更新时间**：2026-10-25 12:39 北京时间

> 从 100 条内容中筛选出 3 条重要资讯。

> 今日高质量增量有限，因此未使用低质量内容补足数量。

<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- DeepSeek 在 V4 全系列模型上线后开放了 Harness 开发者预览版测试，为开发者提供新的模型调用与编排入口。
- Latent Space 报道 Kimi 3.1 Pro 发布开放权重模型并推出 2-3 倍速高速 API，称开源与闭源 AI 差距缩小到约一个月，值得关注新模型能力。
- Hacker News 讨论用 GVS5H Harness 让五个 Qwen3.8-27B 模型达到 Fable 5 水平，本地运行成本低但耗时约 10 倍，值得关注开源模型组合方案。

<a id="product-teardown"></a>
## 产品拆解

### 1. [DeepSeek Harness 开发者预览版开放测试](https://news.google.com/rss/articles/CBMiSEFVX3lxTE4wd0JWNXNkT3NmUy1UV09ldm1iSXY3dTllQ1o1ZFg5MFZPS1BRY3RCTUJLc05UYWJTb1R6VHhoT0NXM3hJQU5xLQ?oc=5){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：DeepSeek 在 V4 全系列模型上线后开放了 Harness 开发者预览版测试，为开发者提供新的模型调用与编排入口。

**评分**：7.8 / 10　 **证据**：媒体报道

**产品 / 团队**：DeepSeek Harness / 财联社

**目标用户**：AI 应用开发者、需要编排多模型/多工具流程的技术团队

**它是什么**：DeepSeek 官方推出的开源 AI Agent 编排框架，用「插件化」思路让开发者像搭积木一样组合模型能力

**用户问题**：开发者想快速搭建能调用多种工具、多步骤协作的 AI 应用时，常要自己写大量胶水代码，重复造轮子

**使用流程**：
1. 安装 Harness 桌面端或从代码启动 Web 界面
2. 按需选择/开发插件（如搜索、代码执行、数据库连接等）
3. 用 Harness 编排插件与 DeepSeek 模型的交互流程
4. 运行并调试 Agent 任务，观察多步骤执行结果

**AI 在做什么**：DeepSeek 大模型作为「大脑」理解任务、决策调用哪个插件，并生成最终回复

**怎么实现**：把每个功能（搜索、计算器、文件读取等）都做成独立插件，Harness 作为总调度器，根据用户输入让模型判断该激活哪些插件、按什么顺序执行，再把结果传回模型继续下一步

**需要理解的知识点**：
1. Agent：让 AI 不仅能聊天，还能自主决定「用什么工具、分几步完成」的系统
2. Function Calling（工具调用）：模型识别用户意图后，输出结构化指令去调用外部 API 或插件，而非直接生成答案
3. 插件化架构：把复杂系统拆成可插拔的小模块，方便复用和扩展

**动手练习**：30 分钟：访问 DeepSeek Harness 官网，按文档安装桌面版；尝试运行一个内置示例（如「搜索网页并总结」），观察模型何时触发搜索插件、如何把搜索结果融入最终回答

**已知限制**：「V4 全系列模型上线」这一说法在提供的原始链接和搜索结果中均未找到官方直接确认，仅见于财联社新闻标题；Harness 与 V4 模型的具体兼容细节、预览版功能边界未公开

**原始来源**：google\_news · 财联社 · 10月25日 02:27 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMiSEFVX3lxTE4wd0JWNXNkT3NmUy1UV09ldm1iSXY3dTllQ1o1ZFg5MFZPS1BRY3RCTUJLc05UYWJTb1R6VHhoT0NXM3hJQU5xLQ?oc=5){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Kimi 3.1 Pro 开放权重与高速 API 发布](https://latent.space/p/ainews-kimi-31/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Latent Space 报道 Kimi 3.1 Pro 发布开放权重模型并推出 2-3 倍速高速 API，称开源与闭源 AI 差距缩小到约一个月，值得关注新模型能力。

**评分**：7.5 / 10　 **证据**：媒体报道

**产品 / 团队**：Kimi 3.1 Pro / swyx .ai

**目标用户**：开发者、需要自建模型或调用 API 的企业用户、AI 研究者

**它是什么**：Moonshot 发布的开源大模型（1040 亿参数、2.8 万亿 token 训练）及配套高速 API，号称性能接近闭源顶尖模型

**用户问题**：闭源模型（如 GPT-4、Claude）性能好但无法本地部署或二次开发；开源模型通常落后闭源半年以上，且推理速度慢

**使用流程**：
1. 在 Kimi.ai 网页端或 Kimi Work/Kimi Code 中选择 kimi-k3.1-pro 模型
2. 如需更快响应，切换至 kimi-k3.1-pro-highspeed API 端点
3. 开发者通过 API 将模型接入自己的应用或 Agent 工作流
4. 计划 11 月 4 日下载完整权重，本地部署或微调

**AI 在做什么**：作为底层引擎，根据用户输入生成代码、分析文档、执行多步骤任务（Agentic 工作流）

**怎么实现**：用大量数据训练出一个超大规模 Transformer 模型，然后把训练好的参数文件公开，任何人都能下载运行；同时官方提供云端加速版本，通过优化推理引擎让响应快 2-3 倍

**需要理解的知识点**：
1. 开放权重（Open Weights）：把训练好的模型参数公开，你可以下载到本地运行，但通常不公开训练数据和代码
2. API 端点（API Endpoint）：一个网络地址，你的程序把问题发过去，服务器上的模型算完再把答案发回来
3. Agentic 工作流：让 AI 不只是回答一次，而是能自主分解任务、调用工具、多轮执行完成复杂目标

**动手练习**：访问 kimi.ai，用自然语言描述一个简单需求（如&#x27;写一个 Python 爬虫抓取新闻标题&#x27;），分别对比默认模式和 /model 切换到 K3.1 Pro 后的回答质量与速度差异；如有 API 权限，用 curl 调用 kimi-k3.1-pro-highspeed 测试响应时间

**已知限制**：完整权重文件尚未实际发布（承诺 11 月 4 日开放）；&#x27;差距缩小到 1 个月&#x27;是 Newsletter 作者观点，非独立基准测试验证；&#x27;Fable-5.1-Class&#x27;为调侃式类比，无官方定义；高速 API 的具体优化技术未公开

**原始来源**：rss · swyx .ai · 10月24日 15:18 北京时间 · [打开原文](https://latent.space/p/ainews-kimi-31/){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

_最近 7 天没有达到收录标准的新 Newsletter 内容；请查看数据源日志。_

<a id="how-they-build"></a>
## 他们怎么做

_今天没有达到标准的一线构建实践；不会用泛泛观点补位。_

<a id="model-company-news"></a>
## 模型公司动态

### [Five Qwen3.8-27B models match Fable 5 Using GVS5H Harness](https://github.com/slee-persis/GVS5H){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Hacker News 讨论用 GVS5H Harness 让五个 Qwen3.8-27B 模型达到 Fable 5 水平，本地运行成本低但耗时约 10 倍，值得关注开源模型组合方案。

**对做产品的启发**：Hacker News 讨论五个 Qwen3.8-27B 模型通过 GVS5H Harness 匹配 Fable 5，涉及开源模型本地部署和成本优势，有 GitHub 项目可验证，但来源为匿名社区、评论指出耗时 10 倍，给 7 分。

**继续验证**：关注 GVS5H Harness 的复现结果和实际耗时成本。

**原始来源**：hackernews · rzk · 10月25日 11:56 北京时间 · [打开原文](https://github.com/slee-persis/GVS5H){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent：让 AI 不仅能聊天，还能自主决定「用什么工具、分几步完成」的系统
- **知识点**：Function Calling（工具调用）：模型识别用户意图后，输出结构化指令去调用外部 API 或插件，而非直接生成答案
- **知识点**：插件化架构：把复杂系统拆成可插拔的小模块，方便复用和扩展
- **知识点**：开放权重（Open Weights）：把训练好的模型参数公开，你可以下载到本地运行，但通常不公开训练数据和代码
- **动手练习**：30 分钟：访问 DeepSeek Harness 官网，按文档安装桌面版；尝试运行一个内置示例（如「搜索网页并总结」），观察模型何时触发搜索插件、如何把搜索结果融入最终回答
- **动手练习**：访问 kimi.ai，用自然语言描述一个简单需求（如&#x27;写一个 Python 爬虫抓取新闻标题&#x27;），分别对比默认模式和 /model 切换到 K3.1 Pro 后的回答质量与速度差异；如有 API 权限，用 curl 调用 kimi-k3.1-pro-highspeed 测试响应时间

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
