---
layout: default
title: "AI产品情报 · 2026-11-14"
date: 2026-11-14
lang: zh
---

**日期**：2026-11-14　 **更新时间**：2026-11-14 14:20 北京时间

> 从 138 条内容中筛选出 7 条重要资讯。

> 今日高质量增量有限，因此未使用低质量内容补足数量。

<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- 记者实测 Anthropic 面向普通消费者的 Claude Duet 智能体，记录它主动帮忙写稿等真实体验，值得看消费级 agent 到底好不好用。
- OpenAI 推出 ChatGPT Wallet，让 ChatGPT Work、Codex 和 dots 里的 Agent 在用户批准后用已有银行卡完成购买；这解决了 Agent 代付的安全与授权问题，是 Agent 商业化的重要产品案例。
- Shield 用 OpenAI 的 Forge Agent 帮 IT 技术员在旧系统门户里自动完成交接操作；这解决了旧系统操作繁琐的问题，是 Agent 落地企业工作流的具体案例。
- OpenAI Codex 发布 0.169.0，新增终端多侧聊标签、历史任务搜索和自定义模型提供商，让编码 agent 更好用。
- Vercel Token Pass 月费不变但额度从 80 美元提到 150 美元，覆盖 Kimi、GLM、DeepSeek 等开源模型，降低个人开发者跑 agent 的成本。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Claude Duet 实测：一个有点神经质但意外好用的消费级 AI Agent](https://www.theverge.com/ai-artificial-intelligence/1032518/claude-duet-ai-agent-hands-on){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：记者实测 Anthropic 面向普通消费者的 Claude Duet 智能体，记录它主动帮忙写稿等真实体验，值得看消费级 agent 到底好不好用。

**评分**：8.6 / 10　 **证据**：已核验

**产品 / 团队**：Claude Duet / Allison Johnson

**目标用户**：不会编程的普通消费者，需要 AI 主动帮忙处理日常数字任务的人

**它是什么**：Anthropic 推出的面向普通消费者的 AI Agent，能在云端虚拟机上自主运行，帮用户完成写文档、整理资料等日常任务，不需要用户会写代码。

**用户问题**：普通用户想用上 AI Agent 自动做事，但市面上的 Agent 大多面向程序员，需要写代码或操作终端，门槛太高

**使用流程**：
1. 用户通过消息告诉 Duet 需要什么（比如&#x27;帮我写篇体验文章&#x27;）
2. Duet 在云端自己的虚拟机上独立工作，无需用户实时盯着
3. Duet 可以调用用户已连接的应用程序来收集信息或执行操作
4. 完成后把结果返回给用户

**AI 在做什么**：作为主动干活的&#x27;代理&#x27;——理解任务后自主规划步骤、操作云端电脑、调用应用、生成内容，全程不需要用户逐步指令

**怎么实现**：给 AI 配了一台&#x27;云端的个人电脑&#x27;，它能像人一样打开软件、浏览网页、写文档。用户只需要像发微信一样交代任务，AI 自己决定怎么一步步做完。

**需要理解的知识点**：
1. Agent（智能体）：不只是回答问题的聊天机器人，而是能自主行动、调用工具完成多步骤任务的 AI
2. Function Calling（函数调用）：AI 判断需要时主动调用外部工具或应用的能力，比如打开文档软件或查资料
3. 云端虚拟机运行：AI 不在你本地电脑操作，而是在服务商的远程电脑上工作，保证安全和隔离

**动手练习**：打开 Claude 官网的 Claude Duet 页面（claude.com/product/claude-duet），阅读官方功能说明；然后用 Claude 免费版尝试用一句话描述一个多步骤任务（如&#x27;帮我查明天北京天气并写一段出行建议&#x27;），观察 AI 是否能自主拆分步骤，对比&#x27;普通问答&#x27;和&#x27;Agent 模式&#x27;的体验差异。约 30 分钟。

**已知限制**：具体定价、支持的应用连接清单、单次任务最长运行时间、与 Claude Code 的功能重叠边界均未公开；The Verge 评测为记者个人体验，非大规模用户验证

**原始来源**：rss · Allison Johnson · 11月13日 22:00 北京时间 · [打开原文](https://www.theverge.com/ai-artificial-intelligence/1032518/claude-duet-ai-agent-hands-on){:target="_blank" rel="noopener noreferrer"}

---
### 2. [OpenAI 推出 ChatGPT Wallet：让 AI Agent 帮你在用户批准后代付款](https://openai.com/index/introducing-chatgpt-wallet){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：OpenAI 推出 ChatGPT Wallet，让 ChatGPT Work、Codex 和 dots 里的 Agent 在用户批准后用已有银行卡完成购买；这解决了 Agent 代付的安全与授权问题，是 Agent 商业化的重要产品案例。

**评分**：8.5 / 10　 **证据**：一手信息

**产品 / 团队**：ChatGPT Wallet / OpenAI News

**目标用户**：美国 ChatGPT Pro 订阅用户，18 岁及以上，使用美国账单地址和符合条件的美国发行信用卡（American Express、Chase、Mastercard、Visa）

**它是什么**：ChatGPT Wallet 是 OpenAI 推出的支付功能，让 ChatGPT Work、Codex 和 dots 里的 AI Agent（智能体，能自主执行任务的 AI 程序）在用户明确批准后，用用户已有的信用卡完成购买。

**用户问题**：AI Agent 想帮用户买东西时，要么没法直接支付，要么让用户把银行卡信息交给 AI 不安全；用户也不放心让 AI 自主花钱，怕 unauthorized charge（未经授权的扣款）。

**使用流程**：
1. 用户在 ChatGPT 中添加符合条件的美国信用卡到 Wallet
2. 在 ChatGPT Work、Codex 或 dots 中让 Agent 执行需要购买的任务
3. Agent 结账时弹出请求，用户明确批准这笔交易
4. 用现有银行卡完成支付，享受原有卡片的欺诈保护和退款政策

**AI 在做什么**：Agent 负责找到商品、填好订单信息、发起支付请求；但最终扣款必须等用户点确认，AI 不能自己直接刷钱。

**怎么实现**：OpenAI 没有自建新支付网络，而是复用用户已有的信用卡体系，加上一层&#x27;人工审批&#x27;的权限控制——Agent 生成支付请求 → 用户确认 → 通过现有卡组织通道完成交易。这样既让 Agent 能&#x27;干活&#x27;，又把最终花钱的决定权留在用户手里。

**需要理解的知识点**：
1. Agent（智能体）：不只是聊天回复，而是能调用工具、执行多步骤任务的 AI，比如这里它能浏览商品、填表、发起支付
2. Function Calling（函数调用）：AI 判断&#x27;现在该调用支付功能了&#x27;，但系统设计上强制要求人类确认这一步，不是 AI 想调就调
3. 人机协同的权限设计：Agent 商业化的关键不是让 AI 多强，而是让用户敢用——明确谁对钱负责、出事了找谁

**动手练习**：打开 ChatGPT（需 Pro 订阅且在美国），检查设置里是否出现 Wallet 入口；如果没有，说明还没轮到你。然后观察你让 GPT-4o 或 o1 执行任何涉及&#x27;购买&#x27;&#x27;订阅&#x27;&#x27;下单&#x27;的任务时，它的回复是否主动拒绝或提示无法支付——对比有 Wallet 和没 Wallet 时的行为差异，理解&#x27;Agent 能力&#x27;和&#x27;支付权限&#x27;是怎么解耦的。

**已知限制**：目前仅向美国 Pro 用户限量推出；未公开是否支持非美国地区、非 Pro 用户、企业账户；未公开 OpenAI 是否从交易中抽成；未公开用户批准的具体交互细节（是弹窗、验证码还是生物识别）；未公开交易纠纷时 OpenAI 和银行的责任划分。

**原始来源**：rss · OpenAI News · 11月13日 23:00 北京时间 · [打开原文](https://openai.com/index/introducing-chatgpt-wallet){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

_最近 7 天没有达到收录标准的新 Newsletter 内容；请查看数据源日志。_

<a id="how-they-build"></a>
## 他们怎么做

### [browser-use/browser-use released 1.0.4](https://github.com/browser-use/browser-use/releases/tag/1.0.4){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

browser-use 发布 1.0.4，通过批量清理旧截图保住模型缓存，在基准分数不变的情况下把单任务成本从 0.434 美元降到 0.208 美元，做浏览器 Agent 的人可以直接借鉴这个省钱做法。

**对做产品的启发**：browser-use 1.0.4 给出了具体工程做法：批量丢弃旧截图以保住 provider 的 prompt cache，并附 BU Bench v2.1 数据（同分 76.1，单任务成本从 $0.434 降到 $0.208）。这是可验证的 Agent 成本优化实践，对做浏览器 Agent 的构建者有明确迁移价值，但属于优化而非新能力，给 7.6。

**继续验证**：观察该缓存策略在更长任务和不同模型供应商上的稳定性，以及 BU Bench 后续版本。

**原始来源**：github · gregpr07 · 11月14日 04:50 北京时间 · [打开原文](https://github.com/browser-use/browser-use/releases/tag/1.0.4){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [llama.cpp v1.0.0 : A stronger foundation for the local AI ecosystem](https://huggingface.co/blog/ggml-org/llama-cpp-v1){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

llama.cpp 发布 v1.0.0，为本地运行 AI 模型提供更稳定的基础；这对做本地化 AI 产品的开发者有直接帮助，但属于底层工具更新。

**对做产品的启发**：llama.cpp 发布 v1.0.0，是本地 AI 推理生态的重要基础设施里程碑，对做本地化 AI 产品的开发者有明确价值，但属于底层推理工具，非产品案例，且正文内容缺失。

**继续验证**：关注 v1.0.0 的具体变更、性能提升和生态兼容性。

**原始来源**：rss · Hugging Face · 11月13日 22:05 北京时间 · [打开原文](https://huggingface.co/blog/ggml-org/llama-cpp-v1){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Shield helps technicians hand off legacy portal work with OpenAI](https://openai.com/business/customer-stories/shield){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Shield 用 OpenAI 的 Forge Agent 帮 IT 技术员在旧系统门户里自动完成交接操作；这解决了旧系统操作繁琐的问题，是 Agent 落地企业工作流的具体案例。

**对做产品的启发**：OpenAI 官方客户案例，描述 Shield 用 Forge Agent 在旧版门户中替技术员完成交接工作，有明确问题、使用方式和 AI 介入环节，属于可迁移的垂直工作流 Agent 案例，但为厂商营销性质案例，证据以官方叙述为主。

**继续验证**：关注 Forge 的技术实现方式、准确率指标和更多客户案例。

**原始来源**：rss · OpenAI News · 11月13日 16:00 北京时间 · [打开原文](https://openai.com/business/customer-stories/shield){:target="_blank" rel="noopener noreferrer"}

### [openai/codex released rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.4/10

OpenAI Codex 发布 0.169.0，新增终端多侧聊标签、历史任务搜索和自定义模型提供商，让编码 agent 更好用。

**对做产品的启发**：官方 Release，含多标签侧聊、任务搜索、自定义模型提供商等具体功能，对理解编码 agent 产品形态演进有可迁移增量。

**继续验证**：关注自定义网关和云连接功能的实际体验。

**原始来源**：github · github-actions\[bot\] · 11月13日 16:37 北京时间 · [打开原文](https://github.com/openai/codex/releases/tag/rust-v0.169.0){:target="_blank" rel="noopener noreferrer"}

### [Token Pass now includes $150 in tokens for $30/month](https://vercel.com/changelog/vercel-token-pass-now-includes-one-hundred-fifty-dollars-of-monthly-tokens){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Vercel Token Pass 月费不变但额度从 80 美元提到 150 美元，覆盖 Kimi、GLM、DeepSeek 等开源模型，降低个人开发者跑 agent 的成本。

**对做产品的启发**：官方定价更新，30 美元月费含 150 美元开源权重模型额度，对个人产品试错成本有直接影响，但属于平台促销型变更。

**继续验证**：关注额度用尽后的回退行为和名额限制。

**原始来源**：rss · Roman Olynyk · 11月14日 02:42 北京时间 · [打开原文](https://vercel.com/changelog/vercel-token-pass-now-includes-one-hundred-fifty-dollars-of-monthly-tokens){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent（智能体）：不只是回答问题的聊天机器人，而是能自主行动、调用工具完成多步骤任务的 AI
- **知识点**：Function Calling（函数调用）：AI 判断需要时主动调用外部工具或应用的能力，比如打开文档软件或查资料
- **知识点**：云端虚拟机运行：AI 不在你本地电脑操作，而是在服务商的远程电脑上工作，保证安全和隔离
- **知识点**：Agent（智能体）：不只是聊天回复，而是能调用工具、执行多步骤任务的 AI，比如这里它能浏览商品、填表、发起支付
- **动手练习**：打开 Claude 官网的 Claude Duet 页面（claude.com/product/claude-duet），阅读官方功能说明；然后用 Claude 免费版尝试用一句话描述一个多步骤任务（如&#x27;帮我查明天北京天气并写一段出行建议&#x27;），观察 AI 是否能自主拆分步骤，对比&#x27;普通问答&#x27;和&#x27;Agent 模式&#x27;的体验差异。约 30 分钟。
- **动手练习**：打开 ChatGPT（需 Pro 订阅且在美国），检查设置里是否出现 Wallet 入口；如果没有，说明还没轮到你。然后观察你让 GPT-4o 或 o1 执行任何涉及&#x27;购买&#x27;&#x27;订阅&#x27;&#x27;下单&#x27;的任务时，它的回复是否主动拒绝或提示无法支付——对比有 Wallet 和没 Wallet 时的行为差异，理解&#x27;Agent 能力&#x27;和&#x27;支付权限&#x27;是怎么解耦的。

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
