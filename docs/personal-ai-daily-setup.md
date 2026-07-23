# Horizon AI Daily 部署与密钥配置 SOP

这套配置每天在 GitHub Actions 中运行，使用 Kimi Platform 的 OpenAI-compatible API，生成中文静态日报并部署到 GitHub Pages。本机无需保持开机。

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

## 3. 添加 Kimi Variables

仍在 **Settings → Secrets and variables → Actions**，切换到 **Variables** 标签页，分别创建：

| Name | Value |
|---|---|
| `KIMI_BASE_URL` | `https://api.moonshot.cn/v1` |
| `KIMI_MODEL_ID` | Kimi Platform 控制台显示的真实模型 ID |

模型 ID 不应猜测。请从 Kimi Platform 控制台复制当前账号可用的准确 ID。`KIMI_BASE_URL` 和 `KIMI_MODEL_ID` 不是密钥，使用 Repository Variables 即可。

GitHub 自动生成的 `GITHUB_TOKEN` 用于读取公开 GitHub 数据和发布 Pages，无需手动创建。

## 4. 手动验证工作流

1. 打开仓库 **Actions**。
2. 左侧选择 **Daily Horizon AI Summary**。
3. 点击 **Run workflow**，选择默认分支后再次点击 **Run workflow**。
4. 打开本次运行，确认 `Validate Kimi configuration`、`Generate Chinese AI daily` 和 `Deploy to GitHub Pages` 均成功。

日志会显示输入 Token、输出 Token、总 Token、AI 请求次数、分析阶段请求次数和深度分析阶段请求次数。若 Provider 没有返回 usage，会明确显示“Provider 未返回 Token 用量”。日志不会输出 API Key。

## 5. 启用 GitHub Pages

首次工作流成功后会出现 `gh-pages` 分支。然后：

1. 打开 **Settings → Pages**。
2. 在 **Build and deployment** 的 `Source` 选择 **Deploy from a branch**。
3. `Branch` 选择 `gh-pages`，目录选择 `/(root)`。
4. 点击 **Save**，等待 GitHub 显示站点地址。

本仓库的默认地址通常为：`https://hank-hee.github.io/News-Notification/`。首页展示最新日报，文章按日期保留历史归档。

## 6. 自动运行时间

工作流 cron 为 `30 23 * * *`，即每天 UTC 23:30、北京时间次日 07:30 触发，为抓取、Kimi 分析和 Pages 部署预留约 30 分钟。GitHub 的计划任务可能有少量排队延迟。

## 7. 修改信源与筛选规则

主要配置位于 `data/config.github.json`：

- `sources.rss`：官方 RSS、ArXiv、Product Hunt 和高质量技术分析来源；
- `sources.github`：重点项目 Release；
- `sources.ossinsight`：最近 24 小时开源趋势；
- `sources.google_news`：中国公司与中文 AI 新闻补充入口；
- `sources.gdelt`：海外公开新闻补充入口；
- `filtering.ai_score_threshold`：默认 `7.5`；
- `filtering.final_min_items` / `final_max_items`：默认 `10` / `12`；
- `filtering.deep_analysis_limit`：默认 `5`；
- `filtering.history_dedup_days`：默认 `7`；
- `balance`：技术/产品、中国/海外软配额。

质量优先于数量。阈值以上不足 10 条时，页面会正常发布较短日报，不会用低质量条目填充。

## 8. 常见故障排查

- **Missing repository secret: MOONSHOT_API_KEY**：Secret 名称拼写错误、未创建或创建在 Environment 而非 Repository。
- **Missing repository variable: KIMI_MODEL_ID**：未创建同名 Repository Variable，或值为空。
- **401 / authentication / invalid API key**：在 Kimi Platform 检查 Key 状态，然后覆盖 `MOONSHOT_API_KEY` Secret。
- **quota / billing / 额度不足**：在 Kimi Platform 检查余额与配额。此类错误会让工作流明确失败，不会发布误导性空日报。
- **429 / rate limit**：稍后手动重跑；也可降低 `analysis_concurrency` 和 `enrichment_concurrency`。
- **JSON 解析失败**：系统会自动缩小批次，最终降级为单条分析；持续失败时检查所选模型是否稳定支持 JSON 输出。
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
uv run horizon --hours 24
```

`.env` 已被 Git 忽略。提交前仍应运行 `git diff --cached`，确认没有真实 Secret。
