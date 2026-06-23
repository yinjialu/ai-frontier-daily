# 一手信源内参监控系统设计

**日期**: 2026-06-23  
**状态**: 待实现

## 背景与目标

用户平时收藏官方网页（如 `claude.com/blog`、`anthropic.com/news`）手动巡查，痛点：遗漏内容、整理收藏麻烦。目标：小时级自动监控这些一手官方信源，发现新文章后用 AI 生成中文摘要，以 OKF 格式写入仓库并开 PR 通知用户 review。

## 架构概览

```
firsthand-sources.yaml          # 监控源配置（人工维护）
scripts/monitor-firsthand.py    # 监控主脚本
data/firsthand-seen.json        # 已见状态 + 信源运行统计（提交 git 备份）
data/firsthand/<id>/*.md        # OKF 格式文章摘要（通过 PR 合入）
launchd plist                   # 开机自启 + 每小时轮询
```

与现有日报流水线完全独立，不共享 `sources.yaml`、`data/<vendor>/` 等路径。

## 三层数据关联

信源 `id` 是贯穿三层的主键，为后续信源健康度复盘提供完整上下文：

```
firsthand-sources.yaml          ← 源的配置（URL、类型、人工维护）
        ↕ id
data/firsthand-seen.json        ← 源的运行统计（更新频率、健康、已见数）
        ↕ id
data/firsthand/<id>/*.md        ← 源产出的内容（OKF 文章，经 PR 合入 main）
```

## 组件设计

### 1. `firsthand-sources.yaml`

监控源配置文件，由用户（或 Claude）手动添加新源。

```yaml
sources:
  - id: claude-blog
    name: Claude Blog
    url: https://claude.com/blog
    type: html-links          # 从 HTML 页面提取文章链接
    link_prefix: /blog/       # 只保留匹配此前缀的链接
    base_url: https://claude.com

  - id: anthropic-news
    name: Anthropic News
    url: https://www.anthropic.com/news
    type: html-links
    link_prefix: /news/
    base_url: https://www.anthropic.com
```

支持的 `type`：
- `html-links`：抓 HTML 页面，用正则提取 `link_prefix` 开头的 href，拼接 `base_url` 得完整 URL
- `rss`：标准 RSS/Atom feed，直接用 feedparser 解析（供未来扩展）

### 2. `scripts/monitor-firsthand.py`

单文件脚本，无需额外框架。依赖：`requests`（已在 requirements.txt）、`feedparser`（已有）、`gh` CLI、`claude` CLI。

**执行流程**：

```
读 firsthand-sources.yaml
  ↓
遍历每个源：
  抓取 URL → 提取所有文章链接
  对比 firsthand-seen.json（该源的 seen_urls）
  筛出新链接
  ↓
  有新链接？
    ├── 否 → 更新 last_checked / consecutive_empty_checks，提交 seen.json
    └── 是 → 逐篇抓全文 → 调 `claude -p` 生成中文摘要
              → 按 OKF 格式写入 data/firsthand/<id>/<date>-<slug>.md
              → 更新 seen_urls / 统计字段，提交 seen.json
              → 开 PR，Reviewer 设为 yinjialu
```

**首次运行**：把当前所有文章 URL 写入 `seen_urls`，**不创建 PR**（避免历史内容噪音）。通过 `initialized: true` 标记区分。

**错误处理**：
- 单个源抓取失败（网络/403）→ 打印日志、跳过该源、不影响其他源
- `claude -p` 失败 → 摘要字段填 `"(摘要生成失败)"`，PR 照常开
- `gh pr create` 失败 → 打印日志，`seen_urls` 不更新（下次重试）

### 3. `data/firsthand-seen.json`

提交到 git，作为运行状态备份和信源健康度原始数据。

```json
{
  "claude-blog": {
    "initialized": true,
    "seen_urls": [
      "https://claude.com/blog/artifacts-in-claude-code"
    ],
    "last_checked": "2026-06-23T15:30:00+08:00",
    "last_new_article": "2026-06-23T15:30:00+08:00",
    "total_articles_seen": 23,
    "consecutive_empty_checks": 0
  }
}
```

`consecutive_empty_checks` 连续超过阈值（如 30 次 × 1h = 30天）时，健康度复盘脚本可标记该源"可能停更或抓取失效"。

每次检查结束后脚本自动 `git commit + push`（commit message：`chore: firsthand seen update YYYY-MM-DD HH:MM`）。

### 4. OKF 文章文件格式

路径：`data/firsthand/<source-id>/<YYYY-MM-DD>-<slug>.md`

```markdown
---
type: Article
title: Artifacts in Claude Code
source: claude-blog
resource: https://claude.com/blog/artifacts-in-claude-code
tags: [claude-code, artifacts]
timestamp: 2026-06-23T15:30:00+08:00
---

Claude Code 现支持直接在对话中生成并预览 Web artifacts，
开发者可实时看到 HTML/React 组件渲染效果，无需离开终端...
```

- `source` 字段与 `firsthand-sources.yaml` 的 `id` 对应，三层关联的显式锚点
- 正文为 AI 生成的中文摘要，100 字以内

### 5. PR 通知

PR 标题：`📡 内参新动态 | Claude Blog | 2026-06-23 15:30 (2篇)`

PR 正文列出所有新文章标题 + 原文链接，便于在 PR 页面快速决定是否点进原文。Reviewer 设为 `yinjialu`，触发 GitHub 邮件通知。Label：`firsthand-intel`（不存在则自动创建）。

用户工作流：收到邮件 → PR diff 视图读摘要 → 值得深读则点 `resource` 链接 → Merge = 内容正式入库。

### 6. launchd plist

文件路径：`~/Library/LaunchAgents/com.jialu.monitor-firsthand.plist`

关键配置：
- `RunAtLoad: true` — 开机登录后立即触发一次检查
- `StartInterval: 3600` — 每小时轮询
- `StandardOutPath` / `StandardErrorPath` → `~/Library/Logs/monitor-firsthand.log`

安装脚本 `scripts/install-monitor-launchd.sh` 一键完成：复制 plist、`launchctl load`。

## 数据流

```
firsthand-sources.yaml (配置)
       ↓
monitor-firsthand.py
       ↓ 每次检查后提交
data/firsthand-seen.json (状态 + 统计，进 git)
       ↓ 有新内容时
data/firsthand/<id>/*.md (OKF 文章，进 git via PR)
       ↓
GitHub PR → 邮件通知 yinjialu review → Merge 入 main
```

## 不在范围内

- 不并入每日日报卡片流水线
- 不发送 macOS 系统通知
- 不监控需要登录的付费页面
- 不持久化文章全文（只存摘要 + 原文链接）
- 不补发"离线期间漏检"的历史通知（开机后跑当次检查即可）

## 扩展方式

**新增信源**：用户提供 URL → Claude 判断类型（html-links / rss）→ 追加到 `firsthand-sources.yaml` → 下次轮询自动覆盖，无需修改脚本。

**信源健康度复盘**：读 `firsthand-seen.json` 的 `last_new_article` / `consecutive_empty_checks` 与 `firsthand-sources.yaml` 关联，生成健康报告。三层数据的 `id` 主键保证关联零歧义。
