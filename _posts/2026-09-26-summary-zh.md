---
layout: default
title: "AI产品情报 · 2026-09-26"
date: 2026-09-26
lang: zh
---

**日期**：2026-09-26　 **更新时间**：2026-09-26 12:58 北京时间

> 从 116 条内容中筛选出 10 条重要资讯。


<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- 开发者 Christian Mat 开源了让 AI 实时玩《宝可梦红》的项目并直播 token 消耗，用来测试模型在复杂游戏里的长程决策能力，评论区反馈它便宜快速但会卡在重复动作里，值得看是因为它直观展示了当前模型做 Agent 的真实短板。
- Anthropic 发布 Claude Code v2.1.283，新增提示词审计命令、模型精确匹配与禁用设置、网关请求分组和工具调用日志，解决企业里模型治理和旧提示词迁移的问题，值得产品经理参考。
- 有 20 年金融经验的开发者做了 Ekselio，用 LLM 按文件结构编排金融工作流、实际计算在浏览器本地执行，工作流可保存后零 token 重复运行，值得看是因为它示范了 AI 在金融场景里只做编排、把执行和透明度留给用户的落地思路。
- 微软正式发布 Copilot 超级应用，把聊天、编程和 agent 合并到一个界面，并把 Scout 助手改名为 Autopilot。
- 有人做了 Ollaya，把 Jev 风格的决策模型做成像 Ollama 一样本地运行的开源工具，Hacker News 上讨论热烈，涉及开源快速复制商业创新的问题。

<a id="product-teardown"></a>
## 产品拆解

### 1. [Jev 实时直播玩《宝可梦红》：一个开源 AI Agent 游戏 Demo](https://jev-pokemon.vercel.app/){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：开发者 Christian Mat 开源了让 AI 实时玩《宝可梦红》的项目并直播 token 消耗，用来测试模型在复杂游戏里的长程决策能力，评论区反馈它便宜快速但会卡在重复动作里，值得看是因为它直观展示了当前模型做 Agent 的真实短板。

**评分**：8.2 / 10　 **证据**：已核验

**产品 / 团队**：Jev（决策模型）/ jev-pokemon（项目名） / pancomplex

**目标用户**：对 AI Agent 能力边界感兴趣的开发者、LLM 初学者、游戏 AI 研究者

**它是什么**：一个把 AI 决策模型接入经典游戏《宝可梦红》，实时直播游玩过程并公开 token 消耗与成本的开源项目。

**用户问题**：想了解当前 LLM 在需要长程规划、记忆和复杂决策的真实任务中到底能做到什么程度，以及实际要花多少钱

**使用流程**：
1. 打开直播页面，观看 AI 实时操作游戏画面
2. 同时看到右侧/旁边的 token 消耗和成本数据实时更新
3. 去 GitHub 下载开源代码，本地运行或修改
4. 对比社区反馈，观察 AI 在哪些场景陷入死循环

**AI 在做什么**：AI 负责分析当前游戏画面和状态，决定下一步按哪个按钮（上/下/左/右/A/B/Start/Select），相当于一个&#x27;只输出按键指令&#x27;的 Agent（Agent：让 AI 不只是回答问题，而是能自主感知环境、做决定并执行动作的自动化程序）

**怎么实现**：作者搭了一个&#x27;脚手架&#x27;（harness）把游戏画面转成文字描述，加上路径导航提示和任务里程碑，让 AI 模型根据这些信息做按键决策；游戏画面和 AI 的思考过程都实时推流到网页上。

**需要理解的知识点**：
1. Agent：LLM 不只能聊天，还能&#x27;看&#x27;屏幕、做决策、按按钮，形成感知-决策-执行的闭环
2. Token 成本可视化：大模型每做一次决策都要消耗 token，实时展示成本能让开发者直观评估 Agent 的经济可行性
3. 长程决策的短板：模型容易陷入&#x27;进门-出门-再进门&#x27;的局部循环，说明缺乏真正的长期记忆和目标坚持能力

**动手练习**：30 分钟：打开 https://jev-pokemon.vercel.app/ 看 10 分钟直播，记录 AI 做了几个决策、花了多少美元；再去 GitHub 看 README 里作者自己列的&#x27;harness 包含哪些辅助&#x27;，对比评论区 stusmall 和 ac2u 的批评，写下：如果去掉路径导航辅助，你认为 AI 会在哪个城镇最先卡住？

**已知限制**：Jev 模型的具体版本和参数量未公开；&#x27;harness&#x27;的辅助程度有多大争议（评论区认为辅助过多，接近&#x27;攻略代打&#x27;）；目前未确认是否真的能通关全 8 个徽章；成本数据是实时累计但单步决策的具体延迟未公开

**原始来源**：hackernews · pancomplex · 9月25日 22:28 北京时间 · [打开原文](https://jev-pokemon.vercel.app/){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Claude Code v2.1.283：企业级 AI 编程工具新增提示词审计与模型治理功能](https://github.com/anthropics/claude-code/releases/tag/v2.1.283){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：Anthropic 发布 Claude Code v2.1.283，新增提示词审计命令、模型精确匹配与禁用设置、网关请求分组和工具调用日志，解决企业里模型治理和旧提示词迁移的问题，值得产品经理参考。

**评分**：7.6 / 10　 **证据**：一手信息

**产品 / 团队**：Claude Code / ashwin-ant

**目标用户**：企业开发团队、AI 产品经理、需要集中管控模型使用的组织

**它是什么**：Anthropic 推出的终端 AI 编程助手（Coding Agent），让开发者用自然语言指挥 AI 写代码、改代码、查 Bug，这次更新主要加了企业管控和排查工具。

**用户问题**：企业里旧提示词在新模型上表现变差却没人知道；管理员没法精确控制员工能调用哪个模型版本；LLM 网关（gateway，企业流量入口）看不到哪些请求属于同一用户指令，排错困难。

**使用流程**：
1. 开发者/管理员开启审计：运行 \`/doctor prompt-audit\` 扫描本地的 CLAUDE.md、skills、agents 等配置
2. 查看报告：发现哪些提示词写法是面向旧模型的，按建议修改
3. 管理员通过 \`availableModelsMatch\` 和 \`deniedModels\` 设置精确放行/禁用特定模型版本
4. 开启网关追踪：设置 \`CLAUDE\_CODE\_GATEWAY\_HINT\_HEADERS=1\`，让网关通过 \`x-claude-code-prompt-id\` 把同一用户指令的多次请求归为一组，方便监控

**AI 在做什么**：执行代码任务的同时，其请求流量可被企业网关识别和分组；自身提示词体系可被审计工具扫描，标记出对旧模型的依赖

**怎么实现**：在请求头里埋一个提示词 ID（类似快递单号），让网关知道哪些 LLM 请求其实来自同一句用户指令；用规则引擎比对模型名称做精确匹配或黑名单拦截；用静态扫描工具检查提示词文件里的模式，匹配已知的旧模型优化写法。

**需要理解的知识点**：
1. Coding Agent：一种能自主执行编程任务（读文件、改代码、运行命令）的 AI 工具，不只是聊天回答
2. 提示词迁移（Prompt Migration）：换用新模型时，原来针对旧模型调优的提示词可能失效，需要审计和重写
3. OpenTelemetry：一种开源标准，用来追踪分布式系统里的请求链路，这里用来记录 AI 工具调用了什么外部工具、输出了什么结果

**动手练习**：30 分钟体验：安装 Claude Code（需有 Anthropic API 权限），创建一个 \`CLAUDE.md\` 文件写入一段带 &#x27;You are Claude 2&#x27; 的提示词，运行 \`/doctor prompt-audit\`，观察它是否被标记为旧模型提示词；然后在终端设置 \`CLAUDE\_CODE\_GATEWAY\_HINT\_HEADERS=1\`，发起一次请求，用 \`curl -v\` 或代理工具查看请求头里是否出现 \`x-claude-code-prompt-id\`。

**已知限制**：未公开 \`/doctor prompt-audit\` 具体覆盖哪些旧模型版本、未公开企业网关 hint headers 的完整字段列表、未公开 \`load\_test\_mode\` 的 canned reply 内容格式。

**原始来源**：github · ashwin-ant · 9月26日 05:50 北京时间 · [打开原文](https://github.com/anthropics/claude-code/releases/tag/v2.1.283){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [How Warp ships 2,000 PRs a month with AI factories \| Zach Lloyd \(CEO, Warp\)](https://www.lennysnewsletter.com/p/how-warp-ships-2000-prs-a-month-with){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Warp 的 CEO 讲了他们怎么用 AI 软件工厂每月产出 2000 个 PR，值得看是因为它把从 Slack 提需求到合并代码的完整流程讲清楚了。

**对做产品的启发**：Warp CEO Zach Lloyd 在 Lenny 播客中公开讲软件工厂如何把 Slack 想法一路做到合并 PR，并给出每月 2000 个 PR 的具体指标和 Slack→Linear→GitHub→QA 的公开工作流。属于构建者一手实践，对理解 AI 编码产品如何嵌入真实研发流程有直接参考价值。

**继续验证**：关注 Warp 软件工厂的公开工作流细节、QA 环节如何自动化，以及 2000 PR 的合并率与返工率。

**原始来源**：newsletter · Claire Vo · 9月21日 20:04 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/how-warp-ships-2000-prs-a-month-with){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

### [State of agent skills](https://vercel.com/blog/state-of-agent-skills){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.6/10

Vercel 发布 skills.sh 注册表首份报告：七个月积累一百万 agent 技能、近 2.8 亿次安装，说明把个人经验写成 skill 就能让通用 agent 学会具体工作。

**对做产品的启发**：Vercel 官方基于 skills.sh 注册表数据发布 agent skills 市场报告：七个月一百万技能、近 2.8 亿次安装，并解释 skill 是把个人/团队经验变成可复用软件，属于一手数据加产品思路，对做 agent 产品的初学者很有迁移价值。

**继续验证**：关注 skills.sh 的安装分布、热门技能类型，以及 skill 变现与质量筛选机制。

**原始来源**：rss · Jonathan Hefner · 9月25日 14:00 北京时间 · [打开原文](https://vercel.com/blog/state-of-agent-skills){:target="_blank" rel="noopener noreferrer"}

### [Quoting John Gruber](https://simonwillison.net/2026/Sep/25/john-gruber/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.8/10

John Gruber 评论 Meta Muse：每个用户获得独立持久 Linux VM，是首个消费级 agent 系统，但普通用户可能没意识到它有多危险。

**对做产品的启发**：John Gruber 对 Meta Muse 的评论被 Simon Willison 引用，指出每个用户获得独立持久 Linux VM、是首个消费级 agent 系统，同时提醒用户低估其危险性，属于高信噪比从业者观察，对理解 agent 产品形态有帮助。

**继续验证**：关注 Muse 的权限模型与消费级 agent 安全讨论是否形成产品规范。

**原始来源**：rss · Simon Willison · 9月26日 01:22 北京时间 · [打开原文](https://simonwillison.net/2026/Sep/25/john-gruber/){:target="_blank" rel="noopener noreferrer"}

### [GitHub Copilot app for Beginners: How to build custom workflows with canvases](https://github.blog/ai-and-ml/github-copilot/github-copilot-app-for-beginners-how-to-build-custom-workflows-with-canvases/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

GitHub 官方教初学者用自然语言描述需求，让 Copilot 的 canvas 生成可用的自定义工作界面，减少适配工具的时间。

**对做产品的启发**：GitHub 官方博客面向初学者讲解 Copilot 的 canvas 自定义工作流，属于官方一手教程，能让初学者理解“用自然语言描述界面、由 agent 生成可用界面”的产品用法，可迁移到个人产品设计，但内容偏教学、无用户反馈数据。

**继续验证**：观察 canvas 是否开放给个人开发者做自定义产品界面，以及是否有真实用户案例。

**原始来源**：rss · Kayla Cinnamon · 9月26日 02:00 北京时间 · [打开原文](https://github.blog/ai-and-ml/github-copilot/github-copilot-app-for-beginners-how-to-build-custom-workflows-with-canvases/){:target="_blank" rel="noopener noreferrer"}


<a id="model-company-news"></a>
## 模型公司动态

### [Claude Discovers Novel Enzyme System](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"} ⭐️ 8.2/10

Anthropic 官方称 Claude 发现了一种新的酶系统，展示大模型在生物科学发现中的实际用途，值得关注 AI 在医药研发场景的产品化可能。

**对做产品的启发**：Anthropic 官方发布 Claude 发现新酶系统的研究更新，属模型公司一手动态，且展示了模型在科学发现这一新场景中的实际能力，对探索垂直 AI 产品（尤其医药/生物）有直接启发。但正文仅有占位描述，缺少可验证细节与用户使用路径，故未进入 9 分区间。

**继续验证**：等待官方补充实验细节、可复现方法或合作方信息，判断是否可迁移为垂直科研产品。

**原始来源**：public\_web · Anthropic News · 9月24日 18:25 北京时间 · [打开原文](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system){:target="_blank" rel="noopener noreferrer"}


### 其他值得留意

### [Show HN: Ekselio – Loveable for finance workflows \(local first\)](https://www.gptbeyond.com/try?home=1){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

有 20 年金融经验的开发者做了 Ekselio，用 LLM 按文件结构编排金融工作流、实际计算在浏览器本地执行，工作流可保存后零 token 重复运行，值得看是因为它示范了 AI 在金融场景里只做编排、把执行和透明度留给用户的落地思路。

**对做产品的启发**：有 20 年金融与并购经验的构建者发布面向金融工作流的 local-first 工具，LLM 只负责按文件 schema 编排工作流，实际执行在浏览器完成，可查看画布、节点预览和 SQL 代码，工作流保存后下月可零 token 重跑。属于有明确构建思路和产品形态的一手案例，能让初学者理解 AI 在金融场景中“只做编排、不做执行”的落地方式，但 HN 仅 12 分 2 评论，反馈证据薄弱，故不给 8 分以上。

**继续验证**：观察是否有真实金融用户反馈、工作流模板数量和本地执行与 LLM 编排的边界如何演进。

**原始来源**：hackernews · kdautaj · 9月26日 05:09 北京时间 · [打开原文](https://www.gptbeyond.com/try?home=1){:target="_blank" rel="noopener noreferrer"}

### [Microsoft thinks its new Copilot ‘super app’ will be as influential as Office](https://www.theverge.com/news/1000532/microsoft-copilot-super-app-chat-coding-autopilot){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.4/10

微软正式发布 Copilot 超级应用，把聊天、编程和 agent 合并到一个界面，并把 Scout 助手改名为 Autopilot。

**对做产品的启发**：微软正式发布 Copilot 超级应用，把聊天、编程、agent 合并到一个界面，并改名 Autopilot，属于大厂 agent 产品形态的重要变化，对产品经理有参考价值，但报道为媒体转述、无一手细节。

**继续验证**：关注超级应用的实际使用反馈、定价与 agent 权限设计。

**原始来源**：rss · Tom Warren · 9月25日 20:00 北京时间 · [打开原文](https://www.theverge.com/news/1000532/microsoft-copilot-super-app-chat-coding-autopilot){:target="_blank" rel="noopener noreferrer"}

### [Ollaya – Ollama for open-source, Jev-style decision models](https://ollaya.dev/){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.2/10

有人做了 Ollaya，把 Jev 风格的决策模型做成像 Ollama 一样本地运行的开源工具，Hacker News 上讨论热烈，涉及开源快速复制商业创新的问题。

**对做产品的启发**：Ollaya 是一个开源项目，把 Jev 风格的决策模型做成类似 Ollama 的本地运行体验，Hacker News 讨论热度高（379 分、105 评论），评论涉及开源快速复制商业创新、Jev 方法的技术价值等。有产品页面和可验证的定位，属于有明确构建思路的产品案例，但来源是社区聚合，且项目本身身份和成熟度需进一步核验，因此给 7.2 分。

**继续验证**：核验 Ollaya 项目仓库和实际可用性，观察 Jev 风格决策模型是否有真实用户反馈。

**原始来源**：hackernews · Ardakilic · 9月26日 02:33 北京时间 · [打开原文](https://ollaya.dev/){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Agent：LLM 不只能聊天，还能&#x27;看&#x27;屏幕、做决策、按按钮，形成感知-决策-执行的闭环
- **知识点**：Token 成本可视化：大模型每做一次决策都要消耗 token，实时展示成本能让开发者直观评估 Agent 的经济可行性
- **知识点**：长程决策的短板：模型容易陷入&#x27;进门-出门-再进门&#x27;的局部循环，说明缺乏真正的长期记忆和目标坚持能力
- **知识点**：Coding Agent：一种能自主执行编程任务（读文件、改代码、运行命令）的 AI 工具，不只是聊天回答
- **动手练习**：30 分钟：打开 https://jev-pokemon.vercel.app/ 看 10 分钟直播，记录 AI 做了几个决策、花了多少美元；再去 GitHub 看 README 里作者自己列的&#x27;harness 包含哪些辅助&#x27;，对比评论区 stusmall 和 ac2u 的批评，写下：如果去掉路径导航辅助，你认为 AI 会在哪个城镇最先卡住？
- **动手练习**：30 分钟体验：安装 Claude Code（需有 Anthropic API 权限），创建一个 \`CLAUDE.md\` 文件写入一段带 &#x27;You are Claude 2&#x27; 的提示词，运行 \`/doctor prompt-audit\`，观察它是否被标记为旧模型提示词；然后在终端设置 \`CLAUDE\_CODE\_GATEWAY\_HINT\_HEADERS=1\`，发起一次请求，用 \`curl -v\` 或代理工具查看请求头里是否出现 \`x-claude-code-prompt-id\`。

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
