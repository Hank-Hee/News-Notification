---
layout: default
title: "AI产品情报 · 2026-10-05"
date: 2026-10-05
lang: zh
---

**日期**：2026-10-05　 **更新时间**：2026-10-05 13:38 北京时间

> 从 66 条内容中筛选出 5 条重要资讯。

> 今日高质量增量有限，因此未使用低质量内容补足数量。

<nav class="daily-toc">
<a href="#daily-focus">今日重点</a> · <a href="#product-teardown">产品拆解</a> · <a href="#newsletter-picks">Newsletter 精选</a> · <a href="#how-they-build">他们怎么做</a> · <a href="#model-company-news">模型公司动态</a> · <a href="#learn-today">今天学什么</a> · <a href="{{ '/products/' | relative_url }}">产品情报库</a> · <a href="#archives">历史日报</a>
</nav>

<a id="daily-focus"></a>
## 今日重点

- 开发者发布 macOS 上的本地 AI 搜索工具 SCM，能对照片和视频逐帧做语义检索，解决海量素材找不到的问题，代码已开源。
- 有人做了个叫 Strata 的开源项目，让 125B 的大模型能在单张 RTX 4090 上跑到 100 tokens/s，值得看是因为它降低了本地跑大模型的门槛，但评论区也指出量化后质量会下降。
- OpenAI 的 ChatGPT 负责人 Tibo Sottiaux 在 Lenny 的播客里讲 ChatGPT 下一步怎么走，值得看是因为这是产品一号位直接讲思路，但正文只有视频链接，需要点进去听。
- DeepSeek 的 Harness 产品把“一切皆插件”作为立项基因，让用户能按需扩展能力，值得关注其产品设计思路。
- DeepSeek 在国庆假期发布新版本，其 90 后负责人表示目标是做出让全球 AI 巨头跟进的创新。

<a id="product-teardown"></a>
## 产品拆解

### 1. [SCM：macOS 上的本地 AI 照片与视频逐帧搜索工具](https://github.com/allenv0/SCM){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：开发者发布 macOS 上的本地 AI 搜索工具 SCM，能对照片和视频逐帧做语义检索，解决海量素材找不到的问题，代码已开源。

**评分**：8.2 / 10　 **证据**：已核验

**产品 / 团队**：SCM / allenleee

**目标用户**：macOS 用户，尤其是本地囤积大量照片/视频素材、靠关键词或文件夹找不到内容的人

**它是什么**：一个开源的 macOS 应用，让你用自然语言搜索本地照片和视频里的内容，比如输入

**用户问题**：照片和视频存了几千几万条后，靠文件名、日期或文件夹根本找不到想要的内容；云端 AI 搜索（如 Google Photos）有隐私顾虑或需要上传

**使用流程**：
1. 把本地照片/视频文件夹拖进 SCM
2. 工具自动在后台提取画面内容并转成可搜索的语义信息
3. 在搜索框输入自然语言，比如
4. 点击结果，直接跳转到对应照片或视频的对应帧

**AI 在做什么**：AI 负责把图片/视频帧的像素内容转成

**怎么实现**：核心思路是

**需要理解的知识点**：
1. Embedding（嵌入）：把图片、文字变成同一套数字坐标，意思相近的内容坐标也相近，这样才能
2. RAG（检索增强生成）：这里不是生成回答，而是借用同样的思路——先把内容转成向量存起来，搜索时把用户的文字也转成向量，找最近的邻居
3. 本地运行 vs 云端：所有计算在 Mac 本地完成，数据不出设备，这是用开源模型+本地推理框架实现的

**动手练习**：30 分钟练习：在 GitHub 下载 SCM 仓库，按 README 跑起来；用手机拍 5 张照片（猫、咖啡杯、书本、窗外、鞋子），用 SCM 搜索

**已知限制**：未公开具体使用的视觉模型和 Embedding 模型版本；未公开视频帧采样策略（是每秒抽一帧还是只抽关键帧）；未公开 M1/M2 不同芯片上的速度差异；社区讨论提到 OCR 目前用 Tesseract 而非 Apple Vision，作者未回应是否计划切换

**原始来源**：hackernews · allenleee · 10月4日 17:24 北京时间 · [打开原文](https://github.com/allenv0/SCM){:target="_blank" rel="noopener noreferrer"}

---
### 2. [Strata：让 125B 大模型在 RTX 4090 上跑到 100 tokens/s 的开源推理框架](https://github.com/Niko1221/Strata){:target="_blank" rel="noopener noreferrer"}

**一句话看懂**：有人做了个叫 Strata 的开源项目，让 125B 的大模型能在单张 RTX 4090 上跑到 100 tokens/s，值得看是因为它降低了本地跑大模型的门槛，但评论区也指出量化后质量会下降。

**评分**：7.4 / 10　 **证据**：已核验

**产品 / 团队**：Strata / snehesht

**目标用户**：想在本地跑大模型但买不起专业显卡的开发者、极客用户、隐私敏感型用户

**它是什么**：一个开源的本地 LLM 推理引擎，通过极致量化+内存分层技术，让超大模型在消费级显卡上高速运行

**用户问题**：125B 参数的大模型通常需要多张 A100/H100 专业显卡（显存 80GB+），普通用户只有 24GB 显存的 RTX 4090，根本跑不动或速度极慢

**使用流程**：
1. 下载 Strata 推理引擎和对应量化版模型文件（GGUF 格式）
2. 配置分层存储：把部分模型层放显卡显存，其余放系统内存甚至 SSD
3. 运行推理，根据硬件自动调度计算资源
4. 对比输出质量与速度，调整量化精度（2-bit 到 4-bit）

**AI 在做什么**：未公开（Strata 是推理工具本身，不直接提供 AI 服务；用户加载的 Qwen 3.8 Flash Next 才是 AI 模型）

**怎么实现**：把模型&#x27;减肥&#x27;到极低精度（2-bit 量化，类似把高清视频压成低码率），同时把显存放不下的部分&#x27;借&#x27;用系统内存，像 CPU 和 GPU 接力干活，避免一次性加载全部参数

**需要理解的知识点**：
1. 量化（Quantization）：把模型权重从高精度浮点数换成低精度整数，牺牲少许质量换取大幅缩小的显存占用，类似把 WAV 转成 MP3
2. GGUF 格式：llama.cpp 生态的模型文件标准，支持分层量化和跨平台推理
3. 内存分层（Memory Hierarchy/Offloading）：显存不够时把部分计算&#x27;卸货&#x27;到内存或硬盘，用带宽换容量

**动手练习**：30 分钟：在 Google Colab 免费 T4 GPU（16GB 显存）上，用 llama.cpp 加载一个 Qwen 2.5 7B 的 Q4\_K\_M 量化模型，对比 FP16 原版与量化版的显存占用和生成速度，再用 perplexity 指标粗略感受质量损失

**已知限制**：量化质量损失的具体程度因任务而异：视觉定位任务中 Strata 误差显著高于 llama.cpp（中位误差 154.8 vs 46.5 像素），但文本生成任务用户反馈&#x27; surprisingly well&#x27;；2-bit 量化的通用质量下限未公开系统评测；作者未说明是否支持多卡或 Windows/Mac

**原始来源**：hackernews · snehesht · 10月4日 20:51 北京时间 · [打开原文](https://github.com/Niko1221/Strata){:target="_blank" rel="noopener noreferrer"}

---

<a id="newsletter-picks"></a>
## Newsletter 精选

### [OpenAI’s Head of ChatGPT: We’re entering a new era of AI \(again\) \| Tibo Sottiaux](https://www.lennysnewsletter.com/p/openais-head-of-chatgpt-were-entering){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

OpenAI 的 ChatGPT 负责人 Tibo Sottiaux 在 Lenny 的播客里讲 ChatGPT 下一步怎么走，值得看是因为这是产品一号位直接讲思路，但正文只有视频链接，需要点进去听。

**对做产品的启发**：OpenAI ChatGPT 负责人 Tibo Sottiaux 在 Lenny&#x27;s Newsletter 的一手访谈，属于模型公司核心研发/产品负责人的直接发言，符合兴趣优先级第三条；但正文抓取内容仅为图片与视频链接，缺少可验证的产品细节与数据，无法确认具体增量，因此不给 8 分以上。对初学者理解 ChatGPT 产品方向有参考价值，但需回看原视频才能提取可迁移信息。

**继续验证**：回看 YouTube 原视频，提取 Sottiaux 关于 ChatGPT 新形态、Agent 化与产品路线的一手表述，判断是否有可迁移的产品设计思路。

**原始来源**：newsletter · Lenny Rachitsky · 10月4日 20:32 北京时间 · [打开原文](https://www.lennysnewsletter.com/p/openais-head-of-chatgpt-were-entering){:target="_blank" rel="noopener noreferrer"}


<a id="how-they-build"></a>
## 他们怎么做

_今天没有达到标准的一线构建实践；不会用泛泛观点补位。_

<a id="model-company-news"></a>
## 模型公司动态

### [DeepSeek Harness：“一切皆插件” 是刻在立项之初的产品基因 - 新浪财经](https://news.google.com/rss/articles/CBMipwFBVV95cUxPQXdXNkxhNkFqZnZwSkJxQ1hFZ3ZyWmNGMXhjRmU0YlFFYjJadDVCLUZaZi1uMkdZRE5CbFZ0MjdMeFp5c0dUU0JNX2hvamx0MndhSUIxUEpSU2d2Zi13TVNLQ3pGNHlPMW5ocHVqM3NjMVdiekpWLXhJNWlrcmZuTGJHRjctMks0dE1qd28wdTJodUZST0VodE5NYkkwU0VtS0xCXy1iOA?oc=5){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.6/10

DeepSeek 的 Harness 产品把“一切皆插件”作为立项基因，让用户能按需扩展能力，值得关注其产品设计思路。

**对做产品的启发**：DeepSeek 官方产品 Harness 的架构理念报道，强调“一切皆插件”从立项之初就是产品基因，属于模型公司核心产品的一手动态，对理解 AI 产品设计有迁移价值；但为媒体转述，非官方原文。

**继续验证**：等待 DeepSeek 官方发布 Harness 的插件文档或 Demo，验证实际扩展方式。

**原始来源**：google\_news · 新浪财经 · 10月5日 11:18 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMipwFBVV95cUxPQXdXNkxhNkFqZnZwSkJxQ1hFZ3ZyWmNGMXhjRmU0YlFFYjJadDVCLUZaZi1uMkdZRE5CbFZ0MjdMeFp5c0dUU0JNX2hvamx0MndhSUIxUEpSU2d2Zi13TVNLQ3pGNHlPMW5ocHVqM3NjMVdiekpWLXhJNWlrcmZuTGJHRjctMks0dE1qd28wdTJodUZST0VodE5NYkkwU0VtS0xCXy1iOA?oc=5){:target="_blank" rel="noopener noreferrer"}

### [DeepSeek 国庆假期上新！DeepSeek90 后负责人回应：希望做出让世界 AI 巨头跟进的创新 - 新浪财经](https://news.google.com/rss/articles/CBMihAFBVV95cUxNbVNnV3FpN0JaMVltMWh4bHJPZTFNY1ltLXFuNlJhOEgtVVdPa25LOF91cHFBSm16WnBFU0lfSEp4ZHpfSUpISWhsUnlxWHh6Y0lIXzlwaUZhZWxKQzZWQ0x5NXYyS2J6REJvZjNKUVY1eExZOHNfMUYwTkZFc0laSDVEZlU?oc=5){:target="_blank" rel="noopener noreferrer"} ⭐️ 7.0/10

DeepSeek 在国庆假期发布新版本，其 90 后负责人表示目标是做出让全球 AI 巨头跟进的创新。

**对做产品的启发**：DeepSeek 国庆假期上新，90 后负责人回应希望做出让世界 AI 巨头跟进的创新，属于模型公司核心人员的一手动态，对理解其产品节奏有参考价值；但为媒体转述，细节有限。

**继续验证**：关注新版本的具体能力变化和第三方实测。

**原始来源**：google\_news · 新浪财经 · 10月5日 09:14 北京时间 · [打开原文](https://news.google.com/rss/articles/CBMihAFBVV95cUxNbVNnV3FpN0JaMVltMWh4bHJPZTFNY1ltLXFuNlJhOEgtVVdPa25LOF91cHFBSm16WnBFU0lfSEp4ZHpfSUpISWhsUnlxWHh6Y0lIXzlwaUZhZWxKQzZWQ0x5NXYyS2J6REJvZjNKUVY1eExZOHNfMUYwTkZFc0laSDVEZlU?oc=5){:target="_blank" rel="noopener noreferrer"}


<a id="learn-today"></a>
## 今天学什么

- **知识点**：Embedding（嵌入）：把图片、文字变成同一套数字坐标，意思相近的内容坐标也相近，这样才能
- **知识点**：RAG（检索增强生成）：这里不是生成回答，而是借用同样的思路——先把内容转成向量存起来，搜索时把用户的文字也转成向量，找最近的邻居
- **知识点**：本地运行 vs 云端：所有计算在 Mac 本地完成，数据不出设备，这是用开源模型+本地推理框架实现的
- **知识点**：量化（Quantization）：把模型权重从高精度浮点数换成低精度整数，牺牲少许质量换取大幅缩小的显存占用，类似把 WAV 转成 MP3
- **动手练习**：30 分钟练习：在 GitHub 下载 SCM 仓库，按 README 跑起来；用手机拍 5 张照片（猫、咖啡杯、书本、窗外、鞋子），用 SCM 搜索
- **动手练习**：30 分钟：在 Google Colab 免费 T4 GPU（16GB 显存）上，用 llama.cpp 加载一个 Qwen 2.5 7B 的 Q4\_K\_M 量化模型，对比 FP16 原版与量化版的显存占用和生成速度，再用 perplexity 指标粗略感受质量损失

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
