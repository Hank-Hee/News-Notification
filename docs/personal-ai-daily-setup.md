---
layout: default
title: AI 产品机会与 Builder 情报：部署与密钥配置 SOP
---

# AI 产品机会与 Builder 情报：部署与密钥配置 SOP

这套配置每天在 GitHub Actions 中运行，使用 Kimi Platform 分析产品情报、使用 Apify 抓取 X/Twitter 一手来源，生成中文日报和结构化产品数据库并部署到 GitHub Pages。本机无需保持开机。

## 1. 仓库与权限

目标仓库为 `Hank-Hee/News-Notification`。如果在其他仓库复用，请先 Fork 上游 `Thysrael/Horizon`，再复制本分支的改动。

进入 GitHub 仓库的 **Settings → Actions → General**：

1. 在 **Actions permissions** 中允许 GitHub Actions 运行。
2. 在 **Workflow permissions** 中选择 **Read and write permissions**。
3. 保存设置。工作流需要写入 `gh-pages` 分支，但不会把 API Key 写入该分支。

## 2. 添加 Kimi API Key（Repository Secret）

不要把真实 API Key 粘贴到代码、配置文件、Issue、PR 或聊天内容中。

1. 打开仓库 **Settings**。
2. 进入 **Secrets and variables → Actions**。
3. 选择 **Secrets** 标签页。
4. 点击 **New repository secret**。
5. `Name` 准确填写：`MOONSHOT_API_KEY`。
6. `Secret` 粘贴你在 Kimi Platform 控制台创建的 API Key。
7. 点击 **Add secret**。

Secret 保存后不能在 GitHub 页面再次查看明文，只能覆盖更新。工作流通过 `${{ secrets.MOONSHOT_API_KEY }}` 注入运行时环境；代码只读取环境变量 `MOONSHOT_API_KEY`。

Secret 或 Variable 只会在任务启动时读取。覆盖 `MOONSHOT_API_KEY`、`KIMI_BASE_URL` 或 `KIMI_MODEL_ID` 后，需要重新运行一次工作流；已经结束或正在运行的旧任务不会自动使用新值。

## 3. 添加 Kimi Variables

仍在 **Settings → Secrets and variables → Actions**，切换到 **Variables** 标签页，分别创建：

| Name | Value |
|---|---|
| `KIMI_BASE_URL` | `https://api.moonshot.cn/v1` |
| `KIMI_MODEL_ID` | `kimi-k2.6` |

工作流在 Variable 缺失时也会默认使用 `kimi-k2.6`；保留该 Variable 是为了以后显式升级模型。当前调用固定发送 `thinking.type=disabled`、`response_format={"type":"json_object"}` 和 `max_completion_tokens`。如果 SDK 或模型拒绝禁用 Thinking，任务会明确失败，不会删除该参数后静默进入思考模式。`KIMI_BASE_URL` 和 `KIMI_MODEL_ID` 不是密钥，使用 Repository Variables 即可。

GitHub 自动生成的 `GITHUB_TOKEN` 用于读取公开 GitHub 数据和发布 Pages，无需手动创建。

## 4. 添加 Apify Token（Repository Secret）

1. 在 Apify 控制台打开 **Settings → Integrations → API & Integrations**，复制 Personal API token。
2. 回到 GitHub 仓库 **Settings → Secrets and variables → Actions → Secrets**。
3. 点击 **New repository secret**。
4. `Name` 准确填写：`APIFY_TOKEN`。
5. `Secret` 粘贴 Apify Token 并保存。

6. 打开 [Scweet Twitter/X Scraper](https://console.apify.com/actors/EvFXOhwR6wsOWmdSK)，点击运行或权限审批入口，阅读权限范围并批准。Apify 规定需要完整权限的 Actor 必须由用户在 Console 人工批准，API 和 GitHub Actions 不能代替这一步。

工作流会先调用 Apify 用户接口验证 Token、确认 Actor 可见，再启动 X/Twitter Actor。Token 缺失或无效时任务明确失败；权限未批准时会显示 `full-permission-actor-not-approved` 和审批链接，不会静默跳过 X 来源。覆盖 Token 或完成审批后需要手动重跑一次。

## 5. 手动验证工作流

1. 打开仓库 **Actions**。
2. 左侧选择 **Daily Horizon AI Summary**。
3. 点击 **Run workflow**，选择需要验证的分支；正式使用时选择 `main`。
4. 打开本次运行，确认 `Validate Kimi configuration`、`Validate Apify configuration`、`Generate Chinese AI daily` 和 `Deploy to GitHub Pages` 均成功。

`Validate Kimi configuration` 会通过 `/models` 验证 Secret、国内 API 地址和 `kimi-k2.6` 权限；它成功就说明变量与 Key 的组合真实可用。日志还会显示输入 Token、输出 Token、总 Token、AI 请求次数、分析阶段请求次数和深度分析阶段请求次数。若 Provider 没有返回 usage，会明确显示“Provider 未返回 Token 用量”。日志不会输出 API Key。

## 6. 启用 GitHub Pages

首次工作流成功后会出现 `gh-pages` 分支。然后：

1. 打开 **Settings → Pages**。
2. 在 **Build and deployment** 的 `Source` 选择 **Deploy from a branch**。
3. `Branch` 选择 `gh-pages`，目录选择 `/(root)`。
4. 点击 **Save**，等待 GitHub 显示站点地址。

本仓库的默认地址通常为：`https://hank-hee.github.io/News-Notification/`。首页展示最新日报，文章按日期保留历史归档；`/products/` 展示可搜索、可筛选的产品数据库。

### 6.1 隐私说明：Pages 默认不是私人网页

GitHub Pages 站点默认可被互联网上任何人访问；即使把源仓库改成 Private，普通 Pages 站点仍然公开。只是不主动分享链接，不能视为访问控制。

真正把 Pages 设为仅仓库读者可见，需要由组织所有的 Private/Internal 仓库，并使用 GitHub Enterprise Cloud 的 Pages Access Control。个人账号或普通套餐没有同等的私有 Pages 开关。

如果日报只供自己查看，推荐路径是：先在 **Settings → Pages** 取消发布，不再把 `gh-pages` 当公开网站；再把工作流改为上传仅登录后可下载的 Actions Artifact，或改用带身份认证的私有托管。当前工作流仍按公开 Pages 发布，本 SOP 只说明选择，不会替你自动关闭现有站点。

官方说明：

- [GitHub Pages 发布源与公开性说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub Enterprise Cloud 私有 Pages 访问控制](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)

## 7. 自动运行时间

工作流 cron 为 `0 1 * * *`，即每天 UTC 01:00、北京时间 09:00 触发。GitHub 的计划任务可能有少量排队延迟。

## 8. 修改信源与筛选规则

主要配置位于 `data/config.github.json`：

- `sources.twitter`：约 65 个全球官方、Builder、产品和医疗 AI 账号，通过 Apify 抓取；
- `sources.rss`：官方产品、产品媒体、Builder 和产品经理方法来源；
- `sources.github`：Agent、AI SDK、自动化和工作流产品构建工具 Release；
- `sources.hackernews`：产品发布、Builder 讨论、市场反馈和失败案例；Reddit 配置暂时关闭，因为 GitHub runner 上抓取不稳定；
- `sources.google_news`：中国 AI 产品、创业、医疗、医药和中医相关补充入口；
- ArXiv、OSS Insight 和泛 GDELT 当前关闭；
- `filtering.ai_score_threshold`：默认 `7.0`；
- `filtering.candidate_limit`：最多 `60` 条进入 Kimi 初筛；
- `filtering.final_min_items` / `final_max_items`：目标 `8` / `12`；
- `filtering.deep_analysis_limit`：默认 `3`，对应 Top 3 产品拆解；
- `filtering.history_dedup_days`：默认 `7`；
- `product_intelligence`：JSON、CSV、发布目录和最多保存记录数。

质量优先于数量。阈值以上不足 8 条时，页面会正常发布较短日报，不会用低质量条目填充。调整兴趣时先优化来源和提示词，最后才调整阈值。

## 9. 结构化数据库在哪里、怎样查看

数据库是运行产物，保存在 `gh-pages`，不会每天提交到 `main`：

- 网页：`https://hank-hee.github.io/News-Notification/products/`；
- JSON：`https://hank-hee.github.io/News-Notification/data/product-intelligence.json`；
- CSV：`https://hank-hee.github.io/News-Notification/data/product-intelligence.csv`。

网页适合日常搜索和筛选；CSV 适合用 Excel/Numbers 分析；JSON 适合以后接程序、数据库或知识平台。首次合入新版代码后必须成功运行一次工作流，以上数据文件才会生成。

## 10. 常见故障排查

- **Missing repository secret: MOONSHOT_API_KEY**：Secret 名称拼写错误、未创建或创建在 Environment 而非 Repository。
- **Kimi Thinking disablement is incompatible**：当前 SDK 或模型不能确认关闭 Thinking；系统会安全停止，不会切换到思考模式。确认模型为 `kimi-k2.6`，并检查 Kimi API 的兼容性公告。
- **Kimi API preflight failed**：优先检查 `MOONSHOT_API_KEY` Secret、`KIMI_BASE_URL=https://api.moonshot.cn/v1` 和 `KIMI_MODEL_ID=kimi-k2.6`；修改后必须新开一次运行。
- **Webhook URL is empty**：说明运行的是合并前的旧版默认分支工作流；合并本 PR 后，新配置不会启用 Webhook，也不会读取 `HORIZON_WEBHOOK_URL`。
- **401 / authentication / invalid API key**：在 Kimi Platform 检查 Key 状态，然后覆盖 `MOONSHOT_API_KEY` Secret。
- **Missing repository secret: APIFY_TOKEN / Apify API preflight failed**：确认 Token 来自 Apify、Secret 名字完全一致，并覆盖更新。
- **`full-permission-actor-not-approved` / 403**：Token 本身有效，但 Scweet Actor 权限还没有在 Apify Console 人工批准；打开日志中的审批链接，批准后重新运行。
- **Twitter 抓取为 0**：检查 Apify Actor run；可能是最近 24 小时账号无更新、账号名失效或 Actor 返回空结果。
- **quota / billing / 额度不足**：在 Kimi Platform 检查余额与配额。此类错误会让工作流明确失败，不会发布误导性空日报。
- **429 / rate limit**：稍后手动重跑；当前分析与增强并发均已设为 `1`，若仍持续限流，应检查账户配额或缩小候选数量。
- **JSON 解析失败**：只有 Provider 已成功返回、但内容结构不合规时，系统才自动缩小批次并最终降级为单条分析；API、认证、额度与限流错误不会触发拆分重试。
- **AI analysis produced no valid results**：任务会停止且不发布空日报；这表示模型调用或结构化输出整体异常，不代表当天没有重要新闻。
- **单一 RSS 或搜索失败**：其他来源会继续运行；所有来源均失败时工作流失败。
- **产品数据库页面或文件 404**：合入新版后先成功运行一次工作流；确认 Pages 来源为 `gh-pages` 的 `/(root)`。
- **修改 Secret 或 Variable 后是否要重跑**：要。旧运行不会自动读取新值，在 Actions 中手动 Run workflow 一次。

## 11. 同步上游 Horizon

`Hank-Hee/News-Notification` 创建时是普通空仓库，不属于 GitHub 的 Fork 网络。本次导入的上游基线为 `Thysrael/Horizon@1e2fdc7ccb177f33c59aef2082c4093e1e82b22c`。为避免无共同历史导致整仓冲突，后续应把“上次同步点到最新上游”的差异应用到单独分支：

```bash
git remote add upstream https://github.com/Thysrael/Horizon.git  # 仅首次需要
git fetch upstream
git switch -c codex/sync-upstream main
git diff --binary 1e2fdc7ccb177f33c59aef2082c4093e1e82b22c..upstream/main | git apply -3
git add -A
git commit -m "sync Horizon upstream"
git push -u origin codex/sync-upstream
```

随后为该分支创建 PR。下一次同步时，把命令中的旧 SHA 替换为本次实际同步到的最新上游 SHA。重点检查 `src/orchestrator.py`、`src/ai/`、`data/config.github.json`、工作流和 `docs/` 的冲突。

## 12. 本地运行（可选）

复制 `.env.example` 为 `.env`，只在本机 `.env` 中填写真实值，然后：

```bash
cp data/config.github.json data/config.json
uv sync
uv run horizon --hours 24
```

`.env` 已被 Git 忽略。提交前仍应运行 `git diff --cached`，确认没有真实 Secret。

本地如果没有 `APIFY_TOKEN`，Twitter 抓取会跳过；正式 GitHub Actions 会在预检阶段要求它存在。
