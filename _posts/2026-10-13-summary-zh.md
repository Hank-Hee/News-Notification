---
layout: default
title: "AI产品情报 · 2026-10-13"
date: 2026-10-13
lang: zh
---

**日期**：2026-10-13　 **更新时间**：2026-10-13 14:47 北京时间

> 从 157 条内容中筛选出 9 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- Vishnu 发布 Agent37，用低成本沙箱帮用户跑 AI Agent，每个沙箱月均约 0.37 美元、免费用户基础设施成本仅 0.05–0.10 美元，并公开了从套壳到自建基础设施的省钱做法，适合想学 Agent 产品落地与成本控制的人拆解。
- 开发者开源 Janas，用 SSD 流式加载专家权重让显存和内存装不下的大模型也能跑起来，评论区有用户实测 8–62 tok/s，适合想理解本地大模型部署的产品经理参考。
- Meta 的 AI Agent Muse 设计负责人 Alex Cornell 公开讲了他怎么把 Muse 做成像发消息而不是 AI 应用，以及三层状态显示和生成式界面背后的设计取舍。
- Simon Willison 用 Codex 生成并发布了 web-edit 0.1a0，一个通过 Tailscale 在手机上浏览和编辑文件夹文件的网页工具，解决不想把凭据经手 LLM 的问题。
- GitHub 官方发了一篇 Copilot 入门教程，教你怎么用自定义指令、自定义 Agent 和 MCP 服务器让 Copilot 理解你的代码库。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Agent37：月费 0.37 美元的 AI Agent 沙箱，YC F26 创始人公开省钱做法](https://news.ycombinator.com/item?id=50059096){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Vishnu 发布 Agent37，用低成本沙箱帮用户跑 AI Agent，每个沙箱月均约 0.37 美元、免费用户基础设施成本仅 0.05–0.10 美元，并公开了从套壳到自建基础设施的省钱做法，适合想学 Agent 产品落地与成本控制的人拆解。

**评分**：8.6 / 10　 **证据**：一手信息

**产品 / 团队**：Agent37 / vishnukool

**目标用户**：需要云端运行 AI Agent 的开发者，尤其是做消息类 Agent、想用免费档测试的个人用户

**它是什么**：一个帮开发者在云端低成本运行 AI Agent（如 Claude Code、Hermes）的隔离沙箱服务，比主流厂商便宜 90% 以上。

**用户问题**：主流云沙箱太贵，个人开发者或小团队负担不起；想提供免费档获客，但基础设施成本压不下来

**使用流程**：
1. 注册账号，选择免费档或付费档
2. 在沙箱里部署想跑的 Agent（如 Hermes、OpenClaw、Claude Code）
3. Agent 在隔离环境中执行任务（浏览网页、写代码等）
4. 按实际使用付费，付费档月均约 $0.37/沙箱

**AI 在做什么**：AI Agent 本身由用户自选并部署，Agent37 只提供运行它的隔离环境，不直接参与 AI 推理

**怎么实现**：核心思路是&#x27;合租服务器&#x27;：用 gVisor（一种轻量级隔离技术，比传统虚拟机更省内存）把多个用户的沙箱塞进同一台物理机，跳过 AWS 等中间商直接租 Hetzner/OVH 的便宜机器，再根据 Agent &#x27;burst 型 CPU + 常驻内存&#x27;的特点，优先买大内存而非高 CPU 的配置。

**需要理解的知识点**：
1. 沙箱（Sandbox）：给程序一个&#x27;关起来的游乐场&#x27;，让它随便折腾但伤不到主机和其他用户
2. Agent：能自主调用工具（如浏览器、代码执行器）完成多步骤任务的 AI，不只是聊天
3. gVisor：Google 开源的&#x27;安全罩&#x27;，比虚拟机轻、启动快，但兼容性有牺牲（比如不支持 Docker 里再跑 Docker）

**动手练习**：30 分钟：在本地用 Docker 跑一个开源 Agent（如 OpenClaw 或 Claude Code 的社区版），同时开系统监控（htop 或活动监视器）观察：①启动时 CPU 是否飙升后回落 ②内存是否一直占用。体会为什么&#x27;大内存+低 CPU&#x27;的机型更适合这类负载。

**已知限制**：未公开具体技术架构细节（如 gVisor 版本、主机规格）；免费档是否有功能限制未说明；不支持 Docker-in-Docker 和 Android 模拟器；目前仅信用卡付款，无 PayPal；社区质疑长期能否抵抗大厂降价竞争

**原始来源**：hackernews · vishnukool · 10月13日 00:46 北京时间 · [打开原文](https://news.ycombinator.com/item?id=50059096){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Janas：用 SSD 流式加载专家权重，让普通设备跑超大模型](https://github.com/prabanta-dev/janas){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：开发者开源 Janas，用 SSD 流式加载专家权重让显存和内存装不下的大模型也能跑起来，评论区有用户实测 8–62 tok/s，适合想理解本地大模型部署的产品经理参考。

**评分**：7.2 / 10　 **证据**：已核验

**产品 / 团队**：Janas / khalidkhair

**目标用户**：想在本机跑大模型但硬件受限的开发者、本地 AI 部署爱好者

**它是什么**：一个开源工具，让显存和内存不够的普通电脑，也能运行参数量远超硬件容量的大语言模型。

**用户问题**：大模型动辄几十 GB 到上百 GB，显存/内存根本装不下，普通用户没法本地运行

**使用流程**：
1. 准备一台有 SSD 的普通电脑，安装 Janas
2. 下载一个 MoE 架构的大模型（如 Qwen 系列）
3. Janas 自动把当前需要的&#x27;专家&#x27;权重从 SSD 流式加载到显存/内存
4. 模型开始输出文本，不需要的专家留在 SSD 不占用内存

**AI 在做什么**：未公开具体模型支持细节；Janas 本身是推理加速框架，不训练模型，只负责在推理时智能调度哪些专家权重该进内存

**怎么实现**：MoE（Mixture of Experts，混合专家）模型的一大特点是：每次推理只激活一小部分&#x27;专家&#x27;网络，而不是用整个模型。Janas 利用这一点，不把全部专家存在内存里，而是像&#x27;按需取货&#x27;一样，从 SSD 临时读取当前要用的专家，用完就换。相当于把 SSD 当成超大号&#x27;虚拟内存&#x27;，但比无脑换页更聪明——它知道模型结构，只加载必要的部分。

**需要理解的知识点**：
1. MoE（混合专家）：一种模型架构，把大模型拆成很多&#x27;专家&#x27;小网络，每次只调用少数几个，用更少算力获得大模型能力
2. 内存瓶颈 vs 存储瓶颈：AI 推理速度受限于&#x27;数据在哪&#x27;——显存最快、内存次之、SSD 最慢，Janas 用速度换容量
3. 专家并行/选择性加载：不是所有参数都同等重要，智能调度比&#x27;全加载&#x27;或&#x27;全不加载&#x27;更高效

**动手练习**：30 分钟：访问 https://github.com/prabanta-dev/janas，按 README 安装；如果你有 16GB 内存的电脑，尝试下载一个 30B+ 的 MoE 模型（如 Qwen2.5-14B/32B 的 MoE 版本），记录首次 token 延迟和稳定后的 tok/s，对比&#x27;能跑起来&#x27;和&#x27;完全加载到内存&#x27;两种模式的资源占用差异。没有合适硬件可先看 Issues 区的用户报告。

**已知限制**：官方 README 技术细节未公开；具体支持哪些模型、SSD 最低速度要求、是否支持 Windows/Mac、与 llama.cpp 的现有 SSD 卸载功能差异多大，均未明确说明。评论区 62 tok/s 的测试环境（硬件、模型大小、量化精度）未公开。

**原始来源**：hackernews · khalidkhair · 10月13日 06:05 北京时间 · [打开原文](https://github.com/prabanta-dev/janas){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [🎙️ How I AI: How Meta designed Muse with Alex Cornell](https://www.lennysnewsletter.com/p/how-i-ai-how-meta-designed-muse-with){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Meta 的 AI Agent Muse 设计负责人 Alex Cornell 公开讲了他怎么把 Muse 做成像发消息而不是 AI 应用，以及三层状态显示和生成式界面背后的设计取舍。

**对做产品的启发**：Meta 消费级 AI Agent Muse 的设计负责人 Alex Cornell 在 Lenny 播客中公开讲解产品设计思路，包括为什么做成消息形态、三层状态显示、生成式 UI 等，属于构建者一手实践分享，对做 AI 产品的人有直接可迁移的设计经验。

**继续验证**：关注 Muse 后续是否开放更多用户反馈，以及 Alex Cornell 在 Threads 上继续公开的设计细节。

**原始来源**：newsletter · Lenny Rachitsky · 10月12日 23:00 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-i-ai-how-meta-designed-muse-with){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [web-edit 0.1a0](https://simonwillison.net/2026/Oct/12/web-edit/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.4/10

Simon Willison 用 Codex 生成并发布了 web-edit 0.1a0，一个通过 Tailscale 在手机上浏览和编辑文件夹文件的网页工具，解决不想把凭据经手 LLM 的问题。

**对做产品的启发**：构建者一手发布的小工具，有明确问题（手机上改凭据文件不想经过 LLM）、明确做法（让 Codex 生成 Web UI、走 Tailscale）和可验证 GitHub Release，属可迁移的构建实践；但体量小、非 AI 核心能力。

**继续验证**：是否加入权限控制与更多文件操作能力

**原始来源**：rss · Simon Willison · 10月12日 23:54 北京时间 · [打开原文](https://simonwillison.net/2026/Oct/12/web-edit/){:target="_blank" rel="noopener noreferrer"}

### [GitHub Copilot app for Beginners: How to teach Copilot about your codebase](https://github.blog/ai-and-ml/github-copilot/github-copilot-app-for-beginners-how-to-teach-copilot-about-your-codebase/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

GitHub 官方发了一篇 Copilot 入门教程，教你怎么用自定义指令、自定义 Agent 和 MCP 服务器让 Copilot 理解你的代码库。

**对做产品的启发**：GitHub 官方教程，讲怎么给仓库加自定义指令和技能、用自定义 Agent、接 Playwright 等 MCP 服务器，属于官方文档级的一手实践指南，对初学者理解 Copilot 怎么被教会理解代码库有直接帮助。

**继续验证**：关注 GitHub 是否把自定义指令和 MCP 支持扩展到更多 Copilot 入口。

**原始来源**：rss · Christopher Harrison · 10月13日 01:43 北京时间 · [打开原文](https://github.blog/ai-and-ml/github-copilot/github-copilot-app-for-beginners-how-to-teach-copilot-about-your-codebase/){:target="_blank" rel="noopener noreferrer"}

### [How Anthropic’s Dynamic Workflows Coordinate Claude Agents](https://www.latent.space/p/claude-dynamic-workflows){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

Anthropic 在 AI Engineer New York 分享了如何用动态工作流协调多个 Claude Agent，借鉴 Unix 和 Linux 的思路让 Agent 承接更大项目而不压垮开发者。

**对做产品的启发**：Anthropic 在 AI Engineer New York 讲多 Agent 编排，借鉴 Unix/Linux 经验，对理解 Agent 产品架构有增量；但为会议演讲转述，无代码与实测数据。

**继续验证**：是否有公开文档或示例代码可复现该编排方式

**原始来源**：rss · Richard MacManus · 10月13日 02:18 北京时间 · [打开原文](https://www.latent.space/p/claude-dynamic-workflows){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude Discovers Novel Enzyme System](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Anthropic 官方称 Claude 发现了一种新的酶系统，展示大模型在生物科学发现中的实际用途，值得关注 AI 在医药研发场景的产品化可能。

**对做产品的启发**：Anthropic 官方发布 Claude 发现新酶系统的研究更新，属模型公司一手动态，且展示了模型在科学发现这一新场景中的实际能力，对探索垂直 AI 产品（尤其医药/生物）有直接启发。但正文仅有占位描述，缺少可验证细节与用户使用路径，故未进入 9 分区间。

**继续验证**：等待官方补充实验细节、可复现方法或合作方信息，判断是否可迁移为垂直科研产品。

**原始来源**：public\_web · Anthropic News · 10月13日 08:18 北京时间 · [打开原文](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"}

### [GLM-Legal](https://z.ai/blog/glm-legal){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

智谱发布法律垂直模型 GLM-Legal，想让 AI 处理合同审阅等法律工作，Hacker News 上有人分享用 Claude 改合同的实际体验，值得看垂直模型在强合规场景怎么落地。

**对做产品的启发**：智谱发布法律垂直模型 GLM-Legal，属官方一手发布，且法律是与医疗同类的强合规垂直场景，对垂直 AI 产品有直接参考价值；但正文为社区讨论，缺少模型能力细节与产品形态说明，故未进 8 分档。

**继续验证**：模型卡、可用入口与真实合同审阅效果；此前工作区快照隐私争议的后续

**原始来源**：hackernews · ilreb · 10月13日 00:11 北京时间 · [打开原文](https://z.ai/blog/glm-legal){:target="_blank" rel="noopener noreferrer"}

### [V4 全系列模型上线后，DeepSeek Harness 开发者预览版开放测试 - 财联社](https://news.google.com/rss/articles/CBMiSEFVX3lxTE4wd0JWNXNkT3NmUy1UV09ldm1iSXY3dTllQ1o1ZFg5MFZPS1BRY3RCTUJLc05UYWJTb1R6VHhoT0NXM3hJQU5xLQ?oc=5){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

DeepSeek 在 V4 全系列模型上线后开放了 Harness 开发者预览版测试，为开发者提供新的模型调用与编排入口。

**对做产品的启发**：DeepSeek 官方模型与开发者工具动态，V4 全系列上线并开放 Harness 开发者预览，属模型公司一手能力进展，对产品经理理解新模型能力有直接价值，但正文缺失、需官方源核实。

**继续验证**：核实 DeepSeek 官方公告，确认 Harness 的具体能力、定价和可用范围。

**原始来源**：google\_news · 财联社 · 10月13日 06:02 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMiSEFVX3lxTE4wd0JWNXNkT3NmUy1UV09ldm1iSXY3dTllQ1o1ZFg5MFZPS1BRY3RCTUJLc05UYWJTb1R6VHhoT0NXM3hJQU5xLQ?oc=5){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：沙箱（Sandbox）：给程序一个&#x27;关起来的游乐场&#x27;，让它随便折腾但伤不到主机和其他用户
- **知识点**：Agent：能自主调用工具（如浏览器、代码执行器）完成多步骤任务的 AI，不只是聊天
- **知识点**：gVisor：Google 开源的&#x27;安全罩&#x27;，比虚拟机轻、启动快，但兼容性有牺牲（比如不支持 Docker 里再跑 Docker）
- **知识点**：MoE（混合专家）：一种模型架构，把大模型拆成很多&#x27;专家&#x27;小网络，每次只调用少数几个，用更少算力获得大模型能力
- **动手练习**：30 分钟：在本地用 Docker 跑一个开源 Agent（如 OpenClaw 或 Claude Code 的社区版），同时开系统监控（htop 或活动监视器）观察：①启动时 CPU 是否飙升后回落 ②内存是否一直占用。体会为什么&#x27;大内存+低 CPU&#x27;的机型更适合这类负载。
- **动手练习**：30 分钟：访问 https://github.com/prabanta-dev/janas，按 README 安装；如果你有 16GB 内存的电脑，尝试下载一个 30B+ 的 MoE 模型（如 Qwen2.5-14B/32B 的 MoE 版本），记录首次 token 延迟和稳定后的 tok/s，对比&#x27;能跑起来&#x27;和&#x27;完全加载到内存&#x27;两种模式的资源占用差异。没有合适硬件可先看 Issues 区的用户报告。

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
