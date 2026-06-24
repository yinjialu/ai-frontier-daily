---
name: firsthand-digest
description: 查询一手信源内参库「最近有什么新动态」。读 ai-frontier-daily 的 OKF 内参库(data/firsthand/)，按时间窗汇总 AI 大厂官方最新动态。用户问「最近有什么新动态 / 内参最近有啥 / Anthropic/OpenAI 最近发了什么 / 这周 AI 大厂动态」时使用。
---

# 一手信源内参速览

内参库位于 `data/firsthand/`（OKF markdown），导出索引在 `data/firsthand/index.json`。
本 skill 回答「最近有什么新动态」——只覆盖**官方一手**信源（11 个：Anthropic/OpenAI/Google/千问/蚂蚁百灵等）。

## 用法

默认查近 7 天。运行查询脚本（在仓库根）：

```bash
python3 -m scripts.firsthand.query --days 7          # 文本，按源分组 + 摘要
python3 -m scripts.firsthand.query --days 7 --json   # JSON，给 agent 进一步处理
```

- 用户说「这周 / 最近三天 / 这个月」→ 对应 `--days 7 / 3 / 30`。
- 想看某个厂商 → 跑完用源 id 过滤（claude-blog / anthropic-news / openai-news / deepmind-blog / qwen-blog / inclusionai-ling 等）。

## 呈现原则（克制）

- **少而精**：直接给标题 + 一句话摘要 + 原文链接，不堆砌。
- **按重要性而非数量**：模型发布/重大能力更新优先；例行公告靠后或省略。
- **跨源同事件合并**：同一件事被多个源报道时只讲一次、标注「N 个源」。
- 数据为空就如实说「近 N 天无新动态」，不编造。

## 数据说明

- `published` = 文章真实发布日期；`detected` = 内参监控发现时间。
- 索引由 launchd 每小时从 OKF 库重建（`scripts/firsthand/index.py`）。
- 若 `index.json` 不存在或过旧，可直接扫 `data/firsthand/<source>/*.md`。
