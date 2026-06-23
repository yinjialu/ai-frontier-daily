# 一手信源内参监控系统设计

**日期**: 2026-06-23  
**状态**: 待实现

## 背景与目标

用户平时收藏官方网页（如 `claude.com/blog`、`anthropic.com/news`）手动巡查，痛点：遗漏内容、整理收藏麻烦。目标：小时级自动监控这些一手官方信源，发现新文章后用 AI 生成中文摘要，以 OKF 格式写入仓库并开 PR 通知用户 review。

## 架构概览

```
firsthand-sources.yaml              # 监控源配置（人工维护）
skills/firsthand-source-manager/    # 信源管理 skill
skills/firsthand-source-subscriber/ # 订阅适配器 skill
scripts/monitor-firsthand.py        # 监控主脚本（launchd 入口）
scripts/run-pending-live.sh         # 用户主动触发 browser-live 源
data/firsthand-seen.json            # 已见状态 + 信源运行统计（提交 git）
data/firsthand-pending-live.json    # 待用户授权的 browser-live 源（运行时）
data/firsthand/<id>/*.md            # OKF 格式文章摘要（经 PR 合入 main）
~/Library/LaunchAgents/             # launchd plist
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

## 两个 Skill

### `skills/firsthand-source-manager`

负责**"管什么"**——信源生命周期管理，由用户对话触发。

能力：
- `add <url>` → 调 subscriber skill 探测订阅方式 → 写入 `firsthand-sources.yaml`
- `list` → 读 `seen.json` 健康统计 → 输出每个源的状态摘要
- `health` → 标记 `consecutive_empty_checks` 超阈值的源，建议修复或移除
- `remove <id>` → 从 yaml 移除，归档 seen.json 记录

### `skills/firsthand-source-subscriber`

负责**"怎么拿"**——订阅适配器协议，无论源是什么形态，统一输出 `[{url, title?, published?}]`。

适配器分级，按调用方式分两条路：

**launchd 自动化路（后台无人值守，零视觉干扰）：**

| Level | type | 实现 | 适用场景 |
|-------|------|------|---------|
| 1 | `html-links` / `rss` | requests / feedparser | SSR 站、有 RSS 的源 |
| 2 | `browser-headless` | claude -p + Playwright MCP（headless） | JS 渲染，无需登录 |
| 3 | `browser-auto` | claude -p + Playwright + Automation Chrome Profile（headless） | 需要登录，专属 Profile |

**用户主动触发路（browser-live，有人值守）：**

| Level | type | 实现 | 适用场景 |
|-------|------|------|---------|
| 3b | `browser-live` | claude -p + Claude in Chrome MCP | 真实 Chrome，实时登录态 |
| 4 | `manual` | 健康复盘时提示人工介入 | 二步验证、企业 SSO |

新增订阅方式 = 加一个适配器，不改 manager 和 monitor 脚本。

## 组件设计

### 1. `firsthand-sources.yaml`

```yaml
sources:
  - id: claude-blog
    name: Claude Blog
    url: https://claude.com/blog
    type: html-links
    link_prefix: /blog/
    base_url: https://claude.com

  - id: anthropic-news
    name: Anthropic News
    url: https://www.anthropic.com/news
    type: html-links
    link_prefix: /news/
    base_url: https://www.anthropic.com

  - id: some-paid-site
    name: 某付费内容站
    url: https://example.com/members/updates
    type: browser-live          # 需要登录，用户授权后触发
    link_prefix: /members/updates/
    base_url: https://example.com
```

### 2. `scripts/monitor-firsthand.py`

launchd 入口，每小时自动执行。

**执行流程：**

```
读 firsthand-sources.yaml
  ↓
按 type 分流：
  Level 1/2/3（自动化）→ 直接抓取 → 对比 seen.json → 有新文章则写 OKF + 开 PR
  browser-live          → 写入 pending-live.json → 发 macOS 通知 + 更新菜单栏
  ↓
更新 seen.json → git commit + push
```

**首次运行**：把当前所有文章 URL 写入 `seen_urls`，不创建 PR（避免历史噪音），通过 `initialized: true` 标记区分。

**错误处理**：
- 单个源抓取失败 → 打印日志、跳过，不影响其他源
- `claude -p` 失败 → 摘要填 `"(摘要生成失败)"`，PR 照常开
- `gh pr create` 失败 → 打印日志，`seen_urls` 不更新（下次重试）

### 3. `data/firsthand-seen.json`

提交到 git，作为运行状态备份和健康度原始数据。每次检查后自动 `git commit + push`。

```json
{
  "claude-blog": {
    "initialized": true,
    "seen_urls": ["https://claude.com/blog/artifacts-in-claude-code"],
    "last_checked": "2026-06-23T15:30:00+08:00",
    "last_new_article": "2026-06-23T15:30:00+08:00",
    "total_articles_seen": 23,
    "consecutive_empty_checks": 0
  }
}
```

### 4. browser-live 源的用户授权链路

**通知发送（launchd 检测到 pending 时）：**

```bash
osascript -e 'display notification "claude-blog 等 2 个源需要浏览器访问" \
  with title "📡 内参待处理" subtitle "按 ⌥⌘I 立即触发"'
```

**菜单栏视觉反馈（xbar/SwiftBar）：**

`~/.xbar/plugins/firsthand-pending.1h.sh` — 每小时刷新，检测 `pending-live.json` 是否存在：
- 无 pending → 菜单栏不显示（或显示 `📡` 暗色）
- 有 pending → 显示 `📡●`（亮色），点击触发 `run-pending-live.sh`

菜单栏状态持续可见，不依赖通知弹窗是否被划走。

**macOS Shortcuts 快捷键（⌥⌘I）：**

在「快捷指令」App 建一个 Shortcut，步骤：运行 Shell 脚本 → `~/ai-frontier-daily/scripts/run-pending-live.sh`。系统设置里绑全局快捷键，任何 App 里均可触发。

**`scripts/run-pending-live.sh`：**

```bash
#!/bin/bash
PENDING=~/ai-frontier-daily/data/firsthand-pending-live.json
[ -f "$PENDING" ] || exit 0   # 无 pending，静默退出

claude -p "$(cat skills/firsthand-source-subscriber/browser-live-prompt.md)" \
  --allowedTools "mcp__Claude_in_Chrome__*,Bash" < "$PENDING"

rm "$PENDING"
```

### 5. OKF 文章文件格式

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

`source` 字段与 `firsthand-sources.yaml` 的 `id` 对应，三层关联的显式锚点。

### 6. PR 通知

PR 标题：`📡 内参新动态 | Claude Blog | 2026-06-23 15:30 (2篇)`

Reviewer 设为 `yinjialu`，触发 GitHub 邮件通知。Label：`firsthand-intel`（不存在则自动创建）。

用户工作流：收到邮件 → PR diff 视图读摘要 → 值得深读则点 `resource` 链接 → Merge = 内容正式入库。

### 7. launchd plist

文件路径：`~/Library/LaunchAgents/com.jialu.monitor-firsthand.plist`

- `RunAtLoad: true` — 开机登录后立即触发一次检查
- `StartInterval: 3600` — 每小时轮询
- `StandardOutPath` / `StandardErrorPath` → `~/Library/Logs/monitor-firsthand.log`

安装脚本 `scripts/install-monitor-launchd.sh` 一键完成：复制 plist、`launchctl load`。

## 完整触发矩阵

| 场景 | 触发方式 | 浏览器 | 用户感知 |
|------|---------|--------|---------|
| Level 1/2/3 有新内容 | launchd 自动 | headless/无 | PR 邮件通知 |
| browser-live 有待检内容 | launchd 通知 → 菜单栏亮起 → ⌥⌘I | 你的 Chrome | 主动授权 |
| 手动新增信源 | 对话触发 source-manager skill | 你的 Chrome（可选） | 全程可见 |
| 信源健康复盘 | 对话触发 source-manager health | 无 | 报告输出 |

## 数据流

```
firsthand-sources.yaml（配置）
       ↓
monitor-firsthand.py（每小时）
       ├── 自动化源 → 抓取 → OKF 文件 → PR → 邮件通知
       └── browser-live 源 → pending-live.json
                                  ↓
                           菜单栏亮起 + macOS 通知
                                  ↓（用户按 ⌥⌘I）
                           run-pending-live.sh
                           → claude + Chrome MCP → OKF 文件 → PR
       ↓（每次检查后）
data/firsthand-seen.json → git commit + push（备份 + 健康统计）
```

## 不在范围内

- 不并入每日日报卡片流水线
- 不持久化文章全文（只存摘要 + 原文链接）
- 不补发"离线期间漏检"的历史通知（开机后跑当次检查即可）
- 不监控需要二步验证的源（标 `manual`，健康复盘时提示）

## 扩展方式

**新增信源**：对话触发 source-manager skill，提供 URL，自动探测类型写入 yaml，无需修改脚本。

**新增订阅方式**：在 subscriber skill 里加适配器描述，Python 脚本对应实现，两者共享策略定义。

**信源健康度复盘**：读 `firsthand-seen.json` 的统计字段与 `firsthand-sources.yaml` 关联，`consecutive_empty_checks` 超阈值自动标记。
