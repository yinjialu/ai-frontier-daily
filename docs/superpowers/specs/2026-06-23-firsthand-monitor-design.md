# 一手信源内参监控系统设计

**日期**: 2026-06-23  
**状态**: 待实现

## 背景与目标

用户平时收藏官方网页（如 `claude.com/blog`、`anthropic.com/news`）手动巡查，痛点：遗漏内容、整理收藏麻烦。目标：小时级自动监控这些一手官方信源，发现新文章后用 AI 生成中文摘要，通过 GitHub Issue 通知用户。

## 架构概览

```
firsthand-sources.yaml       # 监控源配置（人工维护）
scripts/monitor-firsthand.py # 监控主脚本
data/firsthand-seen.json     # 已见文章状态（运行时生成）
launchd plist                # 开机自启 + 每小时轮询
```

与现有日报流水线完全独立，不共享 `sources.yaml`、`data/<vendor>/` 等路径。

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
    ├── 否 → 更新 last_checked，继续下一个源
    └── 是 → 逐篇抓全文（requests.get + BeautifulSoup 提取正文）
              → 调 `claude -p` 生成中文摘要（100字以内）
              → 汇总后调 `gh issue create` 创建 GitHub Issue
              → 更新 seen_urls + last_checked
```

**首次运行**：把当前所有文章 URL 写入 `seen_urls`，**不创建 Issue**（避免历史内容噪音）。通过 `firsthand-seen.json` 里 `initialized: true` 标记区分。

**错误处理**：
- 单个源抓取失败（网络/403）→ 打印日志、跳过该源、不影响其他源
- `claude -p` 失败 → 摘要字段填 `"(摘要生成失败)"`，Issue 照常创建
- `gh issue create` 失败 → 打印日志，`seen_urls` 不更新（下次重试）

### 3. `data/firsthand-seen.json`

```json
{
  "claude-blog": {
    "initialized": true,
    "seen_urls": [
      "https://claude.com/blog/artifacts-in-claude-code",
      "https://claude.com/blog/claude-managed-agents"
    ],
    "last_checked": "2026-06-23T09:30:00+08:00"
  }
}
```

文件存 `data/` 目录但不提交 git（加入 `.gitignore`），属于本机运行时状态。

### 4. GitHub Issue 格式

```
标题: 📡 内参新动态 | Claude Blog | 2026-06-23 15:30

正文:
## 新文章 (2篇)

### Claude Managed Agents Memory
> Claude 现已支持跨会话记忆能力，开发者可通过 API 持久化 agent 上下文...
🔗 https://claude.com/blog/claude-managed-agents-memory

---

### Artifacts in Claude Code  
> Claude Code 现支持直接在对话中生成并预览 Web artifacts...
🔗 https://claude.com/blog/artifacts-in-claude-code
```

Assignee 设为 `yinjialu`，触发 GitHub 邮件通知。Label：`firsthand-intel`（若不存在则自动创建）。

### 5. launchd plist

文件路径：`~/Library/LaunchAgents/com.jialu.monitor-firsthand.plist`

关键配置：
- `RunAtLoad: true` — 开机自启，登录后立即触发一次检查
- `StartInterval: 3600` — 每小时轮询
- `StandardOutPath` / `StandardErrorPath` → `~/Library/Logs/monitor-firsthand.log`

安装脚本 `scripts/install-monitor-launchd.sh` 一键完成：复制 plist、`launchctl load`。

## 数据流

```
firsthand-sources.yaml (配置)
       ↓
monitor-firsthand.py
       ↓ 读写
data/firsthand-seen.json (状态)
       ↓ 新内容时
GitHub Issue (通知 + 存档)
```

## 不在范围内

- 不并入每日日报卡片流水线
- 不发送 macOS 系统通知（GitHub Issue 已覆盖通知需求）
- 不监控需要登录的付费页面
- 不持久化文章全文（只存 URL）
- 不补发"离线期间漏检"的历史通知（开机后跑当次检查即可）

## 扩展方式

用户提供新 URL → Claude 判断类型（html-links / rss）→ 追加到 `firsthand-sources.yaml` → 下次轮询自动覆盖。无需修改脚本。
