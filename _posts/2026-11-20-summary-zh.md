---
layout: default
title: "AI产品情报 · 2026-11-20"
date: 2026-11-20
lang: zh
---

**日期**：2026-11-20　 **更新时间**：2026-11-20 15:13 北京时间

> 从 165 条内容中筛选出 9 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Google Gemini macOS 应用新增 computer use 功能，能帮用户跨本地文件和桌面应用完成多步任务，展示了 AI agent 在个人电脑上的实际落地。
- 微软在 Foundry 推出可信任的自主 Agent：给 Agent 独立身份和权限，并指定负责人；解决企业不敢让 Agent 干活的问题，值得看企业 Agent 的产品设计。
- Google 在搜索首页加入可折叠的 AI 聊天侧边栏，让用户直接查看和继续 AI 对话，展示 AI 搜索入口的产品化尝试。
- ChatPRD 创始人 Claire Vo 公开分享产品遭遇大量 token 欺诈，有人循环使用免费试用转售 AI 用量，为 AI 产品设计防滥用机制提供真实案例。
- Linear COO Cristina Cordova 在播客中分享如何将 GTM 做到 1 亿美元 ARR，并透露超过一半工单由 AI agent 撰写，展示 AI 在客户支持中的实际应用。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Gemini Mac 版新增「computer use」功能：AI 能直接操作用户电脑](https://www.theverge.com/tech/1037902/google-gemini-macos-ai-computer-use){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Google Gemini macOS 应用新增 computer use 功能，能帮用户跨本地文件和桌面应用完成多步任务，展示了 AI agent 在个人电脑上的实际落地。

**评分**：8.0 / 10　 **证据**：一手信息

**产品 / 团队**：Gemini macOS 应用 / Jay Peters

**目标用户**：Mac 电脑用户，需要处理跨应用、跨文件的多步骤办公或日常任务的人

**它是什么**：Google 的 Gemini macOS 应用新增一项功能，让 AI 可以直接查看和操作用户电脑上的本地文件、桌面应用和网页，帮用户完成需要多步骤的复杂任务。

**用户问题**：用户需要在不同软件、文件和网页之间来回切换，手动完成填表、做 PPT、整理资料等繁琐的多步骤任务，耗时且容易出错

**使用流程**：
1. 用户在 Gemini Mac 应用中用自然语言描述想完成的任务，比如「帮我根据这份 Excel 数据做一份 PPT」
2. Gemini 自动识别并访问相关本地文件、打开需要的桌面应用或网页
3. AI 跨多个工具执行多步操作（如读取数据、生成图表、填入幻灯片）
4. 用户检查并确认最终结果，必要时补充修改

**AI 在做什么**：理解用户意图后，自主规划步骤序列，并实际调用电脑上的文件、应用和网页接口来完成任务——这就是 AI Agent（AI 智能体）：不只是回答问题，而是能动手执行任务的 AI。

**怎么实现**：未公开

**需要理解的知识点**：
1. AI Agent：不只是聊天回复，而是能感知环境、做决策、执行动作的 AI 系统
2. Computer Use / 计算机使用能力：让 AI 像人一样看屏幕、操作鼠标键盘、调用软件接口
3. 多模态理解：AI 需要同时看懂文字、界面布局、图片等多种信息才能正确操作电脑

**动手练习**：30 分钟体验：在 Mac 上安装 Gemini 应用（需确认该功能已对你开放），尝试用一句话指令让 AI 帮你完成一个真实小任务，例如「把桌面上的 resume.pdf 里的工作经历部分整理成表格，存成新的 Word 文档」，观察 AI 是否能正确找到文件、理解内容、跨应用操作，并记录它在哪一步出错或需要人工介入。

**已知限制**：未公开：具体支持哪些 macOS 版本、是否需要特定硬件（如 Apple Silicon）、权限申请的具体范围、是否所有桌面应用都能被调用，还是仅限特定合作应用；该功能是否已全量推送或仅部分用户可用也未说明。

**原始来源**：rss · Jay Peters · 11月20日 02:21 北京时间 · [打开原文](https://www.theverge.com/tech/1037902/google-gemini-macos-ai-computer-use){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Microsoft Foundry 推出可信任自主 Agent，让企业敢把 AI 交给它独立干活](https://devblogs.microsoft.com/foundry/build-trusted-autonomous-agents-for-your-team-with-microsoft-foundry/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：微软在 Foundry 推出可信任的自主 Agent：给 Agent 独立身份和权限，并指定负责人；解决企业不敢让 Agent 干活的问题，值得看企业 Agent 的产品设计。

**评分**：7.5 / 10　 **证据**：一手信息

**产品 / 团队**：Microsoft Foundry / Amanda Foster

**目标用户**：企业 IT 管理员、开发团队、需要在 Microsoft 365 环境中部署 AI Agent 的组织

**它是什么**：微软发布的一套企业级 Agent 构建方案，让 AI Agent 在 Microsoft 365 里拥有独立身份、权限和明确负责人，解决企业不敢放手让 AI 自动执行的问题。

**用户问题**：企业虽然想上 AI Agent，但不敢让它真正独立干活——怕它乱操作、怕出事了找不到人负责，导致投入 AI 但看不到实际回报（ROI 没跟上）

**使用流程**：
1. 在 Microsoft Foundry 平台创建 Agent，给它分配独立身份和权限范围
2. 指定一个真人经理（manager）对这个 Agent 的行为负责
3. Agent 在 Microsoft 365 里自主执行任务，比如处理文档、协调会议等
4. 经理通过审计日志监控 Agent 行为，必要时介入或调整权限

**AI 在做什么**：以独立身份在授权范围内自主执行办公任务，不再是被动等用户下指令的工具

**怎么实现**：核心思路是给 AI 做&#x27;企业入职&#x27;——像给员工发工牌一样，给 Agent 注册独立账号、分配角色权限、绑定直属领导，让它能在 Teams/Outlook 等场景里以&#x27;同事&#x27;身份行动，同时所有操作留痕可审计。

**需要理解的知识点**：
1. Agent（智能体）：不只是回答问题，而是能自主规划步骤、调用工具完成任务的 AI 程序
2. Function Calling（函数调用）：AI 判断&#x27;我需要查日历&#x27;或&#x27;我要发邮件&#x27;，并调用对应系统功能的能力
3. 身份与权限治理：企业级 AI 不是技术问题，而是&#x27;谁批准、谁担责、怎么管&#x27;的管理问题

**动手练习**：用 Microsoft 365 开发者账号（免费申请）登录 Microsoft Foundry，创建一个测试 Agent，尝试给它分配&#x27;只读邮件&#x27;权限并绑定自己的账号为负责人，观察权限控制面板和审计日志界面。

**已知限制**：未公开具体定价、是否所有 Microsoft 365 订阅都可用、Agent 能操作的具体应用范围、与第三方系统的集成深度；&#x27;自主&#x27;的实际程度（完全无人值守还是需人工审批关键步骤）未明确。

**原始来源**：rss · Amanda Foster · 11月20日 03:53 北京时间 · [打开原文](https://devblogs.microsoft.com/foundry/build-trusted-autonomous-agents-for-your-team-with-microsoft-foundry/){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

_最近 7 天没有达到收录标准的新 Newsletter 内容；请查看数据源日志。_

<a id="how-they-build"></a>
## 他们怎么做

### [Token fraud is here and it’s BAD \(YouTube\)](https://simonwillison.net/2026/Nov/20/token-fraud-is-here-and-its-bad/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.5/10

ChatPRD 创始人 Claire Vo 公开分享产品遭遇大量 token 欺诈，有人循环使用免费试用转售 AI 用量，为 AI 产品设计防滥用机制提供真实案例。

**对做产品的启发**：ChatPRD 创始人 Claire Vo 公开讲述产品被免费试用 token 欺诈的真实案例，包含具体滥用方式和运营挑战，对构建 AI 产品有直接借鉴意义。

**继续验证**：关注 Claire Vo 后续如何调整试用和防滥用策略。

**原始来源**：rss · Simon Willison · 11月20日 10:49 北京时间 · [打开原文](https://simonwillison.net/2026/Nov/20/token-fraud-is-here-and-its-bad/){:target="_blank" rel="noopener noreferrer"}

### [Scaling Linear’s GTM to $100M ARR — Cristina Cordova, COO](https://latent.space/p/linear-scaling/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Linear COO Cristina Cordova 在播客中分享如何将 GTM 做到 1 亿美元 ARR，并透露超过一半工单由 AI agent 撰写，展示 AI 在客户支持中的实际应用。

**对做产品的启发**：Linear COO 分享 GTM 策略和 AI 预算细节，提到超过 50% 工单由 agent 撰写，属于有数据的一手运营经验，但偏销售增长而非产品构建，对初学者迁移价值中等。

**继续验证**：关注 Linear 后续是否披露更多 AI agent 在工单处理中的细节。

**原始来源**：rss · Basil Chatha · 11月20日 07:58 北京时间 · [打开原文](https://latent.space/p/linear-scaling/){:target="_blank" rel="noopener noreferrer"}

### [How OpenAI’s Performance Factory keeps ChatGPT fast](https://openai.com/index/how-openai-performance-factory-keeps-chatgpt-fast){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

OpenAI 介绍 Performance Factory：用 Codex 自动找并修 ChatGPT 性能问题；这是 AI 参与工程流程的一手实践，对理解 AI 在开发环节的作用有参考。

**对做产品的启发**：OpenAI 官方披露用 Codex 驱动的工作流自动发现并修复性能问题，属构建者工程实践，可迁移到 AI 辅助开发流程；但偏底层性能，非产品体验，给 7.2。

**继续验证**：关注是否有更详细的工作流拆解或开源工具

**原始来源**：rss · OpenAI News · 11月19日 16:00 北京时间 · [打开原文](https://openai.com/index/how-openai-performance-factory-keeps-chatgpt-fast){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude solves two open problems in the physics of black holes](https://www.anthropic.com/research/claude-black-hole-physics){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Anthropic 称 Claude 解决了两个黑洞物理开放问题，展示模型在科研推理上的能力，但离产品应用较远。

**对做产品的启发**：Anthropic 官方发布 Claude 解决黑洞物理开放问题的研究，属于模型能力展示，但偏学术且缺乏产品化路径，对产品经理的直接可迁移增量有限。

**继续验证**：观察是否有后续产品化或开发者可复用的推理能力。

**原始来源**：hackernews · cybermango · 11月20日 01:30 北京时间 · [打开原文](https://www.anthropic.com/research/claude-black-hole-physics){:target="_blank" rel="noopener noreferrer"}

### [Introducing Tool Retrieval in the Gemini API](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

Google 在 Gemini API 推出工具检索；让模型自动挑选可用工具，可能简化 Agent 开发，但细节少，需看文档。

**对做产品的启发**：Gemini API 新增工具检索能力，属模型能力更新，可能解锁 Agent 工具选择的新产品体验；但正文仅图片，信息量有限，给 7.0。

**继续验证**：查看官方文档确认工具检索的具体用法和限制

**原始来源**：rss · Nora Kassner · 11月20日 02:00 北京时间 · [打开原文](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/){:target="_blank" rel="noopener noreferrer"}

### [openai/codex released rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

OpenAI Codex 发布 0.171.0 版本，新增 GPT-6.2 Sol 和 Astra 模型、默认 TUI 工作区、远程会话和撤销重做等多项功能，提升开发者使用体验。

**对做产品的启发**：Codex 正式版本更新，新增 GPT-6.2 Sol 和 Astra 模型目录、TUI 工作区、远程会话等多项功能，属于模型能力与产品功能结合的真实增量，但偏开发者工具细节。

**继续验证**：关注新模型在 Codex 中的实际表现和用户反馈。

**原始来源**：github · github-actions\[bot\] · 11月20日 08:44 北京时间 · [打开原文](https://github.com/openai/codex/releases/tag/rust-v0.171.0){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Google is putting AI chats right on the homepage](https://www.theverge.com/tech/1038059/google-search-homepage-ai-chats){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Google 在搜索首页加入可折叠的 AI 聊天侧边栏，让用户直接查看和继续 AI 对话，展示 AI 搜索入口的产品化尝试。

**对做产品的启发**：Google 首页集成 AI 聊天侧边栏，是产品交互层面的真实更新，可观察大厂如何将 AI 融入核心入口，但缺乏用户反馈和深度拆解。

**继续验证**：关注该功能上线后的用户使用数据和交互设计细节。

**原始来源**：rss · Emma Roth · 11月20日 04:05 北京时间 · [打开原文](https://www.theverge.com/tech/1038059/google-search-homepage-ai-chats){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：AI Agent：不只是聊天回复，而是能感知环境、做决策、执行动作的 AI 系统
- **知识点**：Computer Use / 计算机使用能力：让 AI 像人一样看屏幕、操作鼠标键盘、调用软件接口
- **知识点**：多模态理解：AI 需要同时看懂文字、界面布局、图片等多种信息才能正确操作电脑
- **知识点**：Agent（智能体）：不只是回答问题，而是能自主规划步骤、调用工具完成任务的 AI 程序
- **动手练习**：30 分钟体验：在 Mac 上安装 Gemini 应用（需确认该功能已对你开放），尝试用一句话指令让 AI 帮你完成一个真实小任务，例如「把桌面上的 resume.pdf 里的工作经历部分整理成表格，存成新的 Word 文档」，观察 AI 是否能正确找到文件、理解内容、跨应用操作，并记录它在哪一步出错或需要人工介入。
- **动手练习**：用 Microsoft 365 开发者账号（免费申请）登录 Microsoft Foundry，创建一个测试 Agent，尝试给它分配&#x27;只读邮件&#x27;权限并绑定自己的账号为负责人，观察权限控制面板和审计日志界面。

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
