---
name: firsthand-source-manager
description: 维护 ai-frontier-daily 的一手信源清单 firsthand-sources.yaml。新增信源（探测订阅方式并写入）、列出信源健康状态。用户说"帮我监控这个网页 / 加个信源 / 看看信源健康度"时使用。
---

# 一手信源管理

## add <url>

1. 调 firsthand-source-subscriber 探测订阅方式（rss / html-links）。
2. 生成 source 条目（id 用域名+路径推导的 kebab-case），追加到 `firsthand-sources.yaml`。
3. 提示用户：下一轮 launchd（每小时）或手动 `launchctl kickstart -k gui/$(id -u)/com.yinjialu.ai-frontier-daily.firsthand` 生效；该源首刊静默（只记录不开 PR）。

## list

读 `data/firsthand-state.json`，每个源输出：id、last_fetch_ok（失败显示 last_fetch_error）、last_new_article、已入库篇数（扫 `data/firsthand/<id>/` 的 .md 文件数）。
`last_checked`（上次运行时间，每小时变）在本地 `data/.firsthand-heartbeat.json`（gitignore，不提交），需要看「是否还在跑」时读它。

## 阶段二

- `health`：标记 last_fetch_ok=false 或异常沉默的源。
- `remove <id>`：从 yaml 移除并归档 state。
