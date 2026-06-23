---
name: firsthand-source-subscriber
description: 一手信源订阅适配器。给定信源 URL，探测最稳的订阅方式（RSS / HTML 链接提取），返回统一的文章列表 [{url,title}]。用于 ai-frontier-daily 内参监控的新增信源探测与抓取。
---

# 一手信源订阅适配器

按 `type` 分派抓取策略，统一输出 `[{url, title}]`。

## MVP 适配器（Level 1，已实现于 scripts/firsthand/adapters.py）

- `html-links`：requests 抓页面，提取 `link_prefix` 开头的 href，拼 `base_url`。适合 SSR 站（claude.com/blog）。
- `rss`：feedparser 解析 feed。适合有 RSS/Atom 的源（OpenAI、GitHub releases.atom）。

## 探测新源订阅方式（add 时调用）

给定 URL，依次尝试：
1. 试 `<url>/rss.xml`、`/feed`、`/feed.xml`、`/sitemap.xml`，feedparser 能解析 → 用 `rss`。
2. 否则 requests 抓 HTML，统计最密集的文章链接前缀 → 用 `html-links`，推断 `link_prefix` 与 `base_url`。
3. 都不行（JS 渲染/403）→ 标记需阶段二 browser 适配器。

## 阶段二适配器（未实现）

`browser-headless` / `browser-auto`（Playwright MCP，**依赖未装组件，需先验证**）、`browser-live`（Claude in Chrome MCP，用户授权触发）、`manual`。详见 docs/superpowers/specs/2026-06-23-firsthand-monitor-design.md。
