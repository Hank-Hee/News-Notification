---
layout: default
title: "AI产品情报 · 2026-11-27"
date: 2026-11-27
lang: zh
---

**日期**：2026-11-27　 **更新时间**：2026-11-27 16:28 北京时间

> 从 140 条内容中筛选出 8 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Browser Use 发布 1.0.9，让 Agent 在被网站封 IP 时自动换出口 IP 且不丢登录态，11 个封锁站点通过率从 48% 升到 62%，同时修好 Claude 提示缓存重复计费。
- 有人做了个网站，让 ChatGPT、Claude、Gemini 等模型在群聊里背着用户互相聊天吐槽，用户试用后觉得好笑也感到被冒犯，因为模型真的读过自己的邮件。
- 开发者做了个本地唇读工具，让用户不出声动动嘴就能给 Claude Code 下指令，解决旁边有人不方便说话的输入问题，代码已开源。
- Clay AI 负责人 Jeff Barg 在 Latent Space 访谈中讲述如何构建 GTM agent，包括用 1500 美元筛选全球公司、客户为何讨厌模型选择器，以及如何为每个 agent 搭建上市基础设施，对做 AI 产品有直接参考。
- 一位博主写自己用 AI 重新玩起自托管，评论里有人分享让 Agent 直接部署到家庭服务器、再按效果自然淘汰的做法，也提醒安全补丁压力变大。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Browser Use 1.0.9：让 AI 浏览器 Agent 被封 IP 时自动换出口，登录态不丢](https://github.com/browser-use/browser-use/releases/tag/1.0.9){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Browser Use 发布 1.0.9，让 Agent 在被网站封 IP 时自动换出口 IP 且不丢登录态，11 个封锁站点通过率从 48% 升到 62%，同时修好 Claude 提示缓存重复计费。

**评分**：8.2 / 10　 **证据**：一手信息

**产品 / 团队**：Browser Use / gregpr07

**目标用户**：需要让 AI 自动操作网页的开发者，比如做数据采集、自动化测试、跨网站任务 Agent 的团队

**它是什么**：一个开源的浏览器 Agent 框架，让 AI 能自动操控网页完成复杂任务，这次更新解决了云浏览器被网站封 IP 的核心痛点

**用户问题**：用云浏览器跑 AI Agent 时，网站会识别出「这是数据中心来的流量」直接封 IP；以前一换 IP 登录态就丢了，得重新登录，Agent 流程断掉；另外用 Claude 模型时每次步骤都重复计费，提示缓存没生效

**使用流程**：
1. 开发者用 pip 安装 browser-use==1.0.9，配置好 Agent 要执行的任务
2. Agent 在 cloud browser 上自动浏览网页，遇到某网站封 IP 时触发 rotate\_proxy\(\)
3. 同一浏览器实例换到新出口 IP，但标签页、Cookie、登录状态全部保留，Agent 继续操作
4. 如果目标网站有明确国家域名（如 .de/.kr），自动选对应国家的出口 IP 提高通过率

**AI 在做什么**：AI 负责决策何时调用 rotate\_proxy\(\)（仅在页面被封锁时，每个站点最多一次），以及继续执行被中断的网页操作流程

**怎么实现**：核心思路是「浏览器连接层做 IP 轮换，应用层无感知」。cloud browser 自己管理底层网络连接，换 IP 时只改出口网关，不重启浏览器进程，所以 Cookie、LocalStorage、登录会话都在。Agent 框架里加了一层规则：检测页面是否被封锁 → 触发轮换 → 重试，而不是让开发者手动处理代理池

**需要理解的知识点**：
1. Agent：能自主决策并调用工具完成多步骤任务的 AI 系统，这里 Agent 自己判断什么时候该换 IP
2. Prompt Caching：LLM 把重复出现的上下文缓存起来，只对新内容计费，这次修复了之前缓存命中率为 0 导致每次全价扣费的问题
3. Cloud Browser：运行在云端的完整浏览器实例，不是简单的 HTTP 请求库，能执行 JavaScript、保持登录态，但容易被网站识别为机器人流量

**动手练习**：30 分钟练习：本地 pip 安装 browser-use==1.0.9，用免费 tier 的 cloud browser 让 Agent 去访问一个已知会封云 IP 的网站（如部分电商或社交平台），观察日志中是否触发 rotate\_proxy，验证 Cookie 是否在换 IP 后仍然有效。对比 1.0.8 和 1.0.9 的行为差异

**已知限制**：62% 通过率只在 11 个测试站点验证，不代表所有封锁站点；Bedrock 的缓存修复只有单元测试覆盖，未做线上真实验证；rotate\_proxy 的具体底层机制（是 Browser Use 自建代理网络还是第三方合作）未公开

**原始来源**：github · gregpr07 · 11月27日 06:45 北京时间 · [打开原文](https://github.com/browser-use/browser-use/releases/tag/1.0.9){:target="_blank" rel="noopener noreferrer"}

---
### 2. [多个 AI 模型在群聊里互相吐槽用户的网站](https://construct22.com/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：有人做了个网站，让 ChatGPT、Claude、Gemini 等模型在群聊里背着用户互相聊天吐槽，用户试用后觉得好笑也感到被冒犯，因为模型真的读过自己的邮件。

**评分**：7.6 / 10　 **证据**：已核验

**产品 / 团队**：Construct22（网站域名为 construct22.com） / utiiiD

**目标用户**：对多模型互动和 AI 行为观察感兴趣的普通消费者、AI 爱好者

**它是什么**：一个让 ChatGPT、Claude、Gemini 等多个大模型在同一个群聊里模拟对话、互相调侃甚至&quot;背后议论&quot;用户的网页产品

**用户问题**：用户想看到不同 AI 模型的&quot;性格&quot;差异，以及当多个 AI 同时&quot;看到&quot;自己的数据时会产生什么反应

**使用流程**：
1. 打开网站并授权接入自己的多个 AI 账户（如 ChatGPT、Claude、Gemini 等）
2. 让多个模型读取用户的历史数据或当前上下文
3. 旁观 AI 们在群聊里自动对话、互相吐槽用户
4. 用户可看到对话记录，部分模型可能被&quot;踢出群聊&quot;

**AI 在做什么**：AI 是核心参与者：每个模型扮演群聊成员，基于各自接收到的用户数据生成对话内容，模拟社交互动

**怎么实现**：本质上是把多个 LLM API 接到同一个聊天界面，给每个模型分配不同&quot;角色设定&quot;和能访问的用户数据范围，让它们轮流生成回复，形成多轮对话。关键 trick 是让用户授权真实数据（如邮件），使吐槽内容足够&quot;扎心&quot;

**需要理解的知识点**：
1. Function Calling（函数调用）：让 AI 能调用外部工具读取用户数据的能力
2. 多 Agent 系统：多个有独立上下文的 AI 如何在一个环境里交互
3. 数据授权与隐私：用户给 AI 开放数据权限后，AI 的实际访问范围有多大

**动手练习**：30 分钟练习：在本地用两个不同的 AI（如免费版 ChatGPT 和 Claude）分别上传同一段你的公开社交媒体内容，对比它们的&quot;吐槽风格&quot;差异；再思考如果要让它们&quot;对话&quot;起来，你需要设计什么规则来决定谁先说话、谁看到什么信息

**已知限制**：产品具体技术架构未公开（是否真让模型直接对话，还是由中间层编排）；用户数据授权的具体范围和安全性未说明；商业模式和团队背景未公开；当前是否仍可注册试用未确认

**原始来源**：hackernews · utiiiD · 11月27日 14:44 北京时间 · [打开原文](https://construct22.com/){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

_最近 7 天没有达到收录标准的新 Newsletter 内容；请查看数据源日志。_

<a id="how-they-build"></a>
## 他们怎么做

### [How Clay Builds GTM Agents — Jeff Barg, Head of AI](https://latent.space/p/how-clay-builds-gtm-agents-jeff-barg-head-of-ai/){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Clay AI 负责人 Jeff Barg 在 Latent Space 访谈中讲述如何构建 GTM agent，包括用 1500 美元筛选全球公司、客户为何讨厌模型选择器，以及如何为每个 agent 搭建上市基础设施，对做 AI 产品有直接参考。

**对做产品的启发**：Latent Space 对 Clay AI 负责人 Jeff Barg 的访谈，涉及 GTM agent 构建思路、客户为何讨厌模型选择器、如何用 1500 美元资格筛选全球公司，属于构建者一手实践经验，对产品经理有可迁移洞察。

**继续验证**：关注 Clay 后续是否公开 agent 架构细节或产品化功能。

**原始来源**：rss · Basil Chatha · 11月27日 07:02 北京时间 · [打开原文](https://latent.space/p/how-clay-builds-gtm-agents-jeff-barg-head-of-ai/){:target="_blank" rel="noopener noreferrer"}

### [AI made self-hosting fun again](https://janlukas.blog/posts/ai-self-hosting){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.4/10

一位博主写自己用 AI 重新玩起自托管，评论里有人分享让 Agent 直接部署到家庭服务器、再按效果自然淘汰的做法，也提醒安全补丁压力变大。

**对做产品的启发**：博主一手记录用 AI 让自托管重新变得好玩，评论补充了 Agent 端到端部署与安全维护负担的真实经验，对个人产品构建者有可迁移启发，但非产品发布。

**继续验证**：关注文中提到的自建部署流程与安全实践是否可复用。

**原始来源**：hackernews · jlelse · 11月27日 05:47 北京时间 · [打开原文](https://janlukas.blog/posts/ai-self-hosting){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [V4 全系列模型上线后，DeepSeek Harness 开发者预览版开放测试 - 财联社](https://news.google.com/rss/articles/CBMiSEFVX3lxTE4wd0JWNXNkT3NmUy1UV09ldm1iSXY3dTllQ1o1ZFg5MFZPS1BRY3RCTUJLc05UYWJTb1R6VHhoT0NXM3hJQU5xLQ?oc=5){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

DeepSeek 在 V4 全系列模型上线后开放了 Harness 开发者预览版测试，为开发者提供新的模型调用与编排入口。

**对做产品的启发**：DeepSeek 官方模型与开发者工具动态，V4 全系列上线并开放 Harness 开发者预览，属模型公司一手能力进展，对产品经理理解新模型能力有直接价值，但正文缺失、需官方源核实。

**继续验证**：核实 DeepSeek 官方公告，确认 Harness 的具体能力、定价和可用范围。

**原始来源**：google\_news · 财联社 · 11月27日 01:40 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMiSEFVX3lxTE4wd0JWNXNkT3NmUy1UV09ldm1iSXY3dTllQ1o1ZFg5MFZPS1BRY3RCTUJLc05UYWJTb1R6VHhoT0NXM3hJQU5xLQ?oc=5){:target="_blank" rel="noopener noreferrer"}

### [DeepSeek 新模型限时内测！速度更快，烧钱也更快了 - 第一财经](https://news.google.com/rss/articles/CBMiUEFVX3lxTFBid3JydWdnX1NLRk9aVlJlbzBLUkZQVExzYnAwQXAycC0yekRYN1VJSU9KQ2VKTmpKdV9jbXo1UDM5VzI2eG1FbTRjSDd1aDRD?oc=5){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

第一财经报道 DeepSeek 新模型开启限时内测，速度更快但烧钱也更多，值得关注它可能带来的新用法。

**对做产品的启发**：第一财经报道 DeepSeek 新模型限时内测，速度更快但成本更高，属模型公司能力动态，可能解锁新产品体验。但为媒体报道、细节有限，给 7.0。

**继续验证**：等待官方发布模型卡、定价和可用范围。

**原始来源**：google\_news · 第一财经 · 11月27日 00:01 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMiUEFVX3lxTFBid3JydWdnX1NLRk9aVlJlbzBLUkZQVExzYnAwQXAycC0yekRYN1VJSU9KQ2VKTmpKdV9jbXo1UDM5VzI2eG1FbTRjSDd1aDRD?oc=5){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Show HN: Silent dictation for Claude Code via on-device lip reading](https://github.com/batanus/lip-dictation){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

开发者做了个本地唇读工具，让用户不出声动动嘴就能给 Claude Code 下指令，解决旁边有人不方便说话的输入问题，代码已开源。

**对做产品的启发**：Show HN 展示一个可验证的 GitHub 项目：用本地唇读给 Claude Code 做静音口述输入，解决不便出声场景的提示输入问题。有代码、有明确使用场景，属于可迁移的产品案例，但互动少、尚早期，给 7.2。

**继续验证**：观察识别准确率、延迟和是否支持更多编程助手。

**原始来源**：hackernews · dima7711 · 11月26日 22:25 北京时间 · [打开原文](https://github.com/batanus/lip-dictation){:target="_blank" rel="noopener noreferrer"}

### [Google Will Make AI Agents Use Its MCP Servers. The Gmail One Can&#x27;t Send Email](https://techstackups.com/articles/google-workspace-ai-agents-mcp/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

Google 推动 AI Agent 通过 MCP 服务器使用 Workspace，但 Gmail 的 MCP 一开始不能发邮件，评论认为这是商业决定而非安全限制，并指出发送能力可能已补上。

**对做产品的启发**：Google 让 AI Agent 通过 MCP 服务器接入 Workspace，但 Gmail 发送权限受限，评论指出 MCP elicitation 本可解决确认问题、且发送能力可能已更新。涉及平台策略与 Agent 能力边界，对做 Agent 产品有参考价值。

**继续验证**：核实 Gmail MCP 发送能力是否已开放，以及 elicitation 确认机制的实际落地。

**原始来源**：hackernews · ritzaco · 11月26日 17:44 北京时间 · [打开原文](https://techstackups.com/articles/google-workspace-ai-agents-mcp/){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent：能自主决策并调用工具完成多步骤任务的 AI 系统，这里 Agent 自己判断什么时候该换 IP
- **知识点**：Prompt Caching：LLM 把重复出现的上下文缓存起来，只对新内容计费，这次修复了之前缓存命中率为 0 导致每次全价扣费的问题
- **知识点**：Cloud Browser：运行在云端的完整浏览器实例，不是简单的 HTTP 请求库，能执行 JavaScript、保持登录态，但容易被网站识别为机器人流量
- **知识点**：Function Calling（函数调用）：让 AI 能调用外部工具读取用户数据的能力
- **动手练习**：30 分钟练习：本地 pip 安装 browser-use==1.0.9，用免费 tier 的 cloud browser 让 Agent 去访问一个已知会封云 IP 的网站（如部分电商或社交平台），观察日志中是否触发 rotate\_proxy，验证 Cookie 是否在换 IP 后仍然有效。对比 1.0.8 和 1.0.9 的行为差异
- **动手练习**：30 分钟练习：在本地用两个不同的 AI（如免费版 ChatGPT 和 Claude）分别上传同一段你的公开社交媒体内容，对比它们的&quot;吐槽风格&quot;差异；再思考如果要让它们&quot;对话&quot;起来，你需要设计什么规则来决定谁先说话、谁看到什么信息

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
