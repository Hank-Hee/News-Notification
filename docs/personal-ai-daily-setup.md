# Horizon AI Daily 部署与密钥配置 SOP

这套配置每天在 GitHub Actions 中运行：DeepSeek V4 Flash 负责批量评分和语义去重，Kimi K2.6 只拆解 Top 2，单条 Kimi 失败时才使用 DeepSeek V4 Pro。结果生成中文静态日报并部署到 GitHub Pages，本机无需保持开机。

## 1. 仓库与权限

目标仓库为 `Hank-Hee/News-Notification`。如果在其他仓库复用，请先 Fork 上游 `Thysrael/Horizon`，再复制本分支的改动。

进入 GitHub 仓库的 **Settings → Actions → General**：

1. 在 **Actions permissions** 中允许 GitHub Actions 运行。
2. 在 **Workflow permissions** 中选择 **Read and write permissions**。
3. 保存设置。工作流需要写入 `gh-pages` 分支，但不会把 API Key 写入该分支。

## 2. 检查三个 Repository Secrets

不要把真实 API Key 粘贴到代码、配置文件、Issue、PR 或聊天内容中。

1. 打开仓库 **Settings**。
2. 进入 **Secrets and variables → Actions**。
3. 选择 **Secrets** 标签页。
4. 点击 **New repository secret**，添加或检查 Kimi：
   - `Name`：`MOONSHOT_API_KEY`
   - `Secret`：Kimi Platform 创建的 API Key
5. 再次点击 **New repository secret**，添加 DeepSeek：
   - `Name`：`DEEPSEEK_API_KEY`
   - `Secret`：DeepSeek 开放平台创建的 API Key
6. 检查已有的 Apify Secret：
   - `Name`：`APIFY_TOKEN`
   - `Secret`：Apify Console 生成的 API Token
7. 每个 Secret 都点击 **Add secret** 保存；已存在的可直接保留。

Secret 保存后不能在 GitHub 页面再次查看明文，只能覆盖更新。代码只在 Actions 运行时读取这三个 Secret，不会把它们写入网页、JSON、CSV 或日志。

## 3. 添加模型 Variables

仍在 **Settings → Secrets and variables → Actions**，切换到 **Variables** 标签页，分别创建：

| Name | Value |
|---|---|
| `KIMI_BASE_URL` | `https://api.moonshot.cn/v1` |
| `KIMI_MODEL_ID` | `kimi-k2.6` |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com` |
| `DEEPSEEK_CANDIDATE_MODEL` | `deepseek-v4-flash` |
| `DEEPSEEK_FALLBACK_MODEL` | `deepseek-v4-pro` |

工作流对这些 Variable 都有同值默认配置，但显式创建后更容易检查。所有模型调用均固定发送 `thinking.type=disabled` 和 JSON 输出要求；Kimi 使用 `max_completion_tokens`。如果模型或 SDK 拒绝禁用 Thinking，任务会明确记录错误并停止该调用，不会静默进入思考模式。

GitHub 自动生成的 `GITHUB_TOKEN` 用于读取公开 GitHub 数据和发布 Pages，无需手动创建。

## 4. 在下次 08:30 自动运行时验收

1. 无需手动点击 **Run workflow**，等待合并后的下一个北京时间 08:30。
2. 打开仓库 **Actions**，左侧选择 **Daily Horizon AI Summary**。
3. 打开当天运行，确认 `Validate Kimi configuration`、`Validate DeepSeek configuration`、`Validate Apify configuration`、`Generate Chinese AI daily` 和 `Deploy to GitHub Pages` 均成功。
4. 如 Apify 提示 Actor 尚未授权，在 Apify Store 分别打开 `altimis/scweet` 和 `apify/website-content-crawler`，点击 **Try / Start / Allow** 完成一次授权，然后等待下一次运行或再手动重跑。

日志会按“阶段 / Provider / 模型”显示请求数、输入/输出 Token、缓存命中、重试、结构校验失败和估算费用。正常无缓存运行目标为 7 次请求：DeepSeek 评分 4 次、语义去重 1 次、Kimi 深度拆解 2 次。日志不会输出 API Key。

Apify 每日会运行两个有上限的任务：X 抓取最多 0.40 美元，邮件资讯抓取最多 0.30 美元。这是保护性上限，不是每日必然消费数。

## 5. 启用 GitHub Pages

首次工作流成功后会出现 `gh-pages` 分支。然后：

1. 打开 **Settings → Pages**。
2. 在 **Build and deployment** 的 `Source` 选择 **Deploy from a branch**。
3. `Branch` 选择 `gh-pages`，目录选择 `/(root)`。
4. 点击 **Save**，等待 GitHub 显示站点地址。

本仓库的默认地址通常为：`https://hank-hee.github.io/News-Notification/`。首页展示最新日报，文章按日期保留历史归档。

## 6. 自动运行时间

工作流 cron 为 `30 0 * * *`，即每天 UTC 00:30、北京时间 08:30 触发。GitHub 的计划任务可能有少量排队延迟。

## 7. 修改信源与筛选规则

主要配置位于 `data/config.github.json`：

- `sources.rss`：模型公司、产品媒体与构建者博客的公开 Feed；
- `sources.newsletter`：通过 Apify Website Content Crawler 每日抓取 Lenny's Newsletter、Simple.ai、AlphaSignal 的公开免费归档，不登录、不访问付费内容；
- `sources.twitter`：模型公司核心人员、真实 AI 产品构建者和少量高信噪比观察者；
- `sources.github`：重点项目 Release；
- `sources.ossinsight`：最近 24 小时开源趋势；
- `sources.google_news`：中国公司与中文 AI 新闻补充入口；
- `sources.gdelt`：海外公开新闻补充入口；
- `filtering.ai_score_threshold`：默认 `7.0`；
- `filtering.candidate_limit` / `per_source_limit`：默认 `40` / `8`；
- `filtering.final_min_items` / `final_max_items`：默认 `8` / `12`；
- `filtering.deep_analysis_limit`：默认 `2`；
- `filtering.history_dedup_days`：默认 `7`；
- `balance`：技术/产品、中国/海外软配额。

质量优先于数量。阈值以上不足 10 条时，页面会正常发布较短日报，不会用低质量条目填充。

## 8. 常见故障排查

- **Missing repository secret: MOONSHOT_API_KEY / DEEPSEEK_API_KEY**：Secret 名称拼写错误、未创建或创建在 Environment 而非 Repository。
- **Thinking disablement is incompatible**：当前 SDK 或模型不能确认关闭 Thinking；系统会安全停止该调用，不会切换到思考模式。
- **DeepSeek model unavailable**：确认使用国内官方地址 `https://api.deepseek.com`，并检查模型名为 `deepseek-v4-flash` 和 `deepseek-v4-pro`。
- **Apify Actor preflight failed**：确认 `APIFY_TOKEN` 为 Repository Secret，并在 Apify Store 对报错的 Actor 执行一次 **Try / Start / Allow**。
- **Webhook URL is empty**：说明运行的是合并前的旧版默认分支工作流；合并本 PR 后，新配置不会启用 Webhook，也不会读取 `HORIZON_WEBHOOK_URL`。
- **401 / authentication / invalid API key**：在 Kimi Platform 检查 Key 状态，然后覆盖 `MOONSHOT_API_KEY` Secret。
- **quota / billing / 额度不足**：在 Kimi Platform 检查余额与配额。此类错误会让工作流明确失败，不会发布误导性空日报。
- **429 / rate limit**：稍后手动重跑；也可降低 `analysis_concurrency` 和 `enrichment_concurrency`。
- **JSON 解析失败**：批次内合法条目会立即保留，只对缺失或无效条目补偿请求一次，不会递归拆批。
- **单一 RSS 或搜索失败**：其他来源会继续运行；所有来源均失败时工作流失败。
- **Pages 404**：确认工作流已生成 `gh-pages` 分支，且 Pages 来源为 `gh-pages` 的 `/(root)`。

## 9. 同步上游 Horizon

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

## 10. 本地运行（可选）

复制 `.env.example` 为 `.env`，只在本机 `.env` 中填写真实值，然后：

```bash
cp data/config.github.json data/config.json
uv sync
export MOONSHOT_API_KEY="你的 Kimi Key"
export DEEPSEEK_API_KEY="你的 DeepSeek Key"
export KIMI_BASE_URL="https://api.moonshot.cn/v1"
export KIMI_MODEL_ID="kimi-k2.6"
export DEEPSEEK_BASE_URL="https://api.deepseek.com"
export DEEPSEEK_CANDIDATE_MODEL="deepseek-v4-flash"
export DEEPSEEK_FALLBACK_MODEL="deepseek-v4-pro"
export APIFY_TOKEN="你的 Apify Token"
uv run horizon --hours 24
```

`.env` 已被 Git 忽略。提交前仍应运行 `git diff --cached`，确认没有真实 Secret。
