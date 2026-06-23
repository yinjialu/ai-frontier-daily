# 一手信源内参监控系统设计

**日期**: 2026-06-23
**状态**: 待实现（MVP 优先）

## 背景与目标

用户平时收藏官方网页（如 `claude.com/blog`、`anthropic.com/news`）手动巡查，痛点：遗漏内容、整理收藏麻烦。目标：小时级自动监控这些一手官方信源，发现新文章后用 AI 生成中文摘要，以 OKF 格式写入仓库并开 PR 通知用户 review。

## 分阶段交付

| 阶段 | 内容 | 满足什么 |
|------|------|---------|
| **MVP（本次实现）** | Level 1 适配器（html-links / rss）+ OKF + PR + launchd + 文件级去重 | claude.com/blog 等所有公开源——即 99% 真实痛点 |
| **阶段二（未来）** | browser-* 适配器 + Chrome MCP + 菜单栏 + 快捷键 + pending 授权链路 | 等真的遇到需要登录态的源再做 |

两个 skill 的**适配器接口**在 MVP 就定好（留扩展点），但只实现 Level 1。browser-* 相关组件本 spec 仅描述设计意图，不进 MVP plan。

## 架构概览（MVP）

```
firsthand-sources.yaml              # 监控源配置（人工维护）
skills/firsthand-source-manager/    # 信源管理 skill（接口完整，MVP 实现 add/list）
skills/firsthand-source-subscriber/ # 订阅适配器 skill（MVP 仅 Level 1 适配器）
scripts/monitor_firsthand.py        # 监控主脚本（launchd 入口）
data/firsthand-state.json           # 本轮已开 PR 短期记忆 + 信源健康统计（提交 git）
data/firsthand/<id>/*.md            # OKF 格式文章摘要（经 PR 合入 main）= 去重的唯一真相
~/Library/LaunchAgents/             # launchd plist
```

与现有日报流水线完全独立，不共享 `sources.yaml`、`data/<vendor>/` 等路径。

## 去重的唯一真相：已入库的文件（关键设计）

**"已见" = "文章已入库（OKF 文件存在于 main）"，而非"脚本看到过"。**

去重判定：扫 `data/firsthand/<id>/*.md` 每个文件 frontmatter 的 `resource` 字段，得到该源「已入库 URL 集合」。抓取页面得到的 URL 不在此集合中 = 新文章。

为什么不用一份独立的 seen 账本：若 seen 账本直推 main 标记"已见"，而 OKF 文章还在未 merge 的 PR 里，一旦 PR 被关/冲突，文章在 main 已是"已见"→ 下次不再抓 → **内容永久丢失且用户无感知**。以 git 里实际文件为唯一真相，杜绝两份账本对不齐。

`data/firsthand-state.json` 只承担两个**辅助**职责，丢失了也不会导致内容丢失：
1. **本轮防重复开 PR**：记录 `open_pr_urls`——已进入未合并 PR 的 URL，避免下一轮（PR 还没 merge 时）重复开 PR。PR merge 后这些 URL 变成 OKF 文件，可从此集合清除。
2. **健康统计**：见下文。

## 三层数据关联

信源 `id` 是贯穿三层的主键：

```
firsthand-sources.yaml          ← 源的配置（URL、类型、人工维护）
        ↕ id
data/firsthand-state.json       ← 源的健康统计 + 防重复短期记忆
        ↕ id
data/firsthand/<id>/*.md        ← 源产出的内容（OKF 文章）= 去重真相
```

## 两个 Skill

### `skills/firsthand-source-manager`

负责**"管什么"**——信源生命周期管理，由用户对话触发。

MVP 能力：
- `add <url>` → 调 subscriber 探测订阅方式 → 写入 `firsthand-sources.yaml`
- `list` → 读 `firsthand-state.json` 健康统计 → 输出每个源的状态摘要

阶段二能力：
- `health` → 标记抓取失败或异常沉默的源
- `remove <id>` → 从 yaml 移除，归档 state 记录

### `skills/firsthand-source-subscriber`

负责**"怎么拿"**——订阅适配器协议，无论源是什么形态，统一输出 `[{url, title?}]`。

适配器分级（MVP 仅实现 Level 1）：

| Level | type | 实现 | 阶段 |
|-------|------|------|------|
| 1 | `html-links` | requests + 标准库 `html.parser`/正则提链接 | **MVP** |
| 1 | `rss` | feedparser | **MVP** |
| 2 | `browser-headless` | claude -p + Playwright MCP（headless） | 阶段二（**依赖未装的 Playwright MCP，需先验证可用性**） |
| 3 | `browser-auto` | claude -p + Playwright + Automation Chrome Profile | 阶段二 |
| 3b | `browser-live` | claude -p + Claude in Chrome MCP（用户授权触发） | 阶段二 |
| 4 | `manual` | 健康复盘提示人工介入 | 阶段二 |

适配器以 `type` 字段分派，新增订阅方式 = 加一个适配器函数，不改 manager 和主流程。

## 组件设计（MVP）

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
```

`rss` 类型示例：`type: rss` + `url: <feed url>`，无需 link_prefix/base_url。

### 2. `scripts/monitor_firsthand.py`

launchd 入口，每小时执行。

**执行流程：**

```
git pull --rebase（确保 data/firsthand/ 是最新真相）
读 firsthand-sources.yaml
  ↓
遍历每个源：
  按 type 调对应适配器抓取 → 得到当前文章 URL 列表
  扫 data/firsthand/<id>/*.md 得已入库 URL 集合
  扣除已入库 + state.open_pr_urls → 得「真·新文章」
  更新健康统计（last_fetch_ok / last_fetch_error / last_new_article）
  ↓
所有源汇总「真·新文章」：
  为空 → 仅 commit+push state.json（健康统计）到 main，结束
  非空 → 逐篇抓全文 → claude -p 生成 {summary, tags}
         → 写 OKF 文件到 data/firsthand/<id>/<date>-<slug>.md
         → 把这些 URL 加入 state.open_pr_urls
         → 在 firsthand/<date> 分支提交 OKF 文件 + state.json
         → gh pr create（reviewer=yinjialu）
```

**首刊判定**：源在 `data/firsthand/<id>/` 无任何文件**且** state 中无该源记录 → 视为首刊，把当前所有文章 URL 直接写入 `state.open_pr_urls` 并标记已处理，**不开 PR**（避免新增源时喷一屏历史）。该源下次起正常运转。

**错误处理：**
- 单个源抓取失败 → 记 `last_fetch_ok=false` + `last_fetch_error`，跳过该源，不影响其他源
- `claude -p` 摘要失败 → summary 填 `"(摘要生成失败)"`、tags 留空，OKF 文件照常写、PR 照常开
- `gh pr create` 失败 → 打印日志，**不**把 URL 加入 open_pr_urls（下轮重试）

**launchd 环境**：脚本顶部复用 `watch-and-publish.sh` 的 PATH 处理（`export PATH=...` 含 anaconda/homebrew/nvm node），确保 `claude`、`gh`、`git` 可寻址、OAuth token 可读。

### 3. `data/firsthand-state.json`

提交到 git。丢失不致命（去重真相在 OKF 文件），仅影响防重复与健康统计。

```json
{
  "claude-blog": {
    "open_pr_urls": [],
    "last_checked": "2026-06-23T15:30:00+08:00",
    "last_fetch_ok": true,
    "last_fetch_error": null,
    "last_new_article": "2026-06-23T15:30:00+08:00",
    "initialized": true,
    "known_urls_count": 23
  }
}
```

健康统计字段（替代被废弃的 `consecutive_empty_checks`）：
- `last_fetch_ok` / `last_fetch_error`：**抓取是否成功**——页面改版、403、选择器失效在此暴露，这才是真正的健康问题（低频源长期无新内容是正常的，不算异常）。
- `last_new_article`：距上次有新内容多久，结合源历史频率人工判断异常（如月更博客沉默 60 天才可疑）。

每轮结束 `git commit + push`（**本机推 main 无 403**；commit message：`chore: firsthand state YYYY-MM-DD HH:MM`，**绝不用 `daily:` 前缀**）。

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

- `resource` 字段是去重判定读取的锚点，必须是干净的完整 URL（去 query/trailing slash）。
- `source` 字段 = `firsthand-sources.yaml` 的 `id`。
- `summary`（正文）与 `tags` 由同一次 `claude -p` 结构化输出（prompt 要求返回 JSON `{summary, tags}`），summary 100 字以内。

### 5. PR 通知

- **每轮所有源的新文章合并到一个 PR**（减少噪音），分支 `firsthand/<YYYY-MM-DD>`（**不用 `claude/*`、`daily-*` 前缀**——避免触发 auto-merge-daily workflow 白跑）。
- 标题：`📡 内参新动态 | 2026-06-23 15:30 (claude-blog 2篇, anthropic-news 1篇)`
- 正文列出每源新文章标题 + `resource` 链接。
- Reviewer 设 `yinjialu`，触发 GitHub 邮件通知。Label：`firsthand-intel`（不存在则建）。
- merge 后分支自动删除（`gh pr merge --delete-branch` 由用户手动 merge 时带）。
- **commit message 不用 `daily:` 前缀**——否则会被 auto-merge-daily 误自动合并、来不及 review。

用户工作流：邮件 → PR diff 读摘要 → 值得深读点 `resource` → Merge = 入库。Merge 后下一轮 `git pull` 使 OKF 文件成为去重真相，`open_pr_urls` 中对应 URL 被清除。

### 6. launchd plist

`~/Library/LaunchAgents/com.jialu.monitor-firsthand.plist`

- `RunAtLoad: true` — 开机登录后立即触发一次检查
- `StartInterval: 3600` — 每小时轮询
- `StandardOutPath` / `StandardErrorPath` → `~/Library/Logs/monitor-firsthand.log`

安装脚本 `scripts/install-monitor-launchd.sh`：复制 plist、`launchctl load`。

## 数据流（MVP）

```
firsthand-sources.yaml（配置）
       ↓
monitor_firsthand.py（每小时，git pull 先行）
       ↓ 抓取 → 扣除已入库文件 → 真·新文章
       ├── 有 → claude -p 摘要 → OKF 文件 → firsthand/<date> 分支 → PR → 邮件
       └── 无 → 仅更新健康统计
       ↓（每轮）
data/firsthand-state.json → commit + push main（健康统计 + 防重复，非去重真相）
       ↓
data/firsthand/<id>/*.md（PR merge 后）→ 成为下一轮去重真相
```

## 阶段二设计（不进 MVP plan，仅记录意图）

需要登录态/JS 渲染的源，分两条路：

- **launchd 自动化路**：`browser-headless`（Playwright headless，无登录）、`browser-auto`（Playwright + 专属 Automation Chrome Profile，有登录，headless 不干扰用户）。**前置：先验证 Playwright MCP 可装可用 + `claude -p --allowedTools mcp__...` 能调起 MCP 拿结构化输出。**
- **用户授权路**：`browser-live` 用 Claude in Chrome MCP 操控真实浏览器。launchd 检测到此类源有待检内容 → 写 `pending-live.json` → macOS 通知 + 菜单栏（xbar/SwiftBar）亮起 → 用户按 ⌥⌘I（macOS Shortcuts 绑 `run-pending-live.sh`）授权触发。**绝不在后台自动操控可见浏览器**（避免开会投屏时冲突）。

## 不在范围内

- 不并入每日日报卡片流水线
- 不持久化文章全文（只存摘要 + 原文链接）
- 不补发"离线期间漏检"的历史通知（开机后跑当次检查即可）
- MVP 不实现 browser-* 任何适配器

## 扩展方式

- **新增信源**：对话触发 source-manager，提供 URL，探测类型写入 yaml，无需改脚本。
- **新增订阅方式**：在 subscriber 加适配器函数，按 `type` 分派。
- **信源健康复盘**：读 `firsthand-state.json` 的 `last_fetch_ok` / `last_new_article` 与 yaml 关联。
