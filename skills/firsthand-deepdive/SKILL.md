---
name: firsthand-deepdive
description: 专题深度线——对一个值得深挖的功能点（如 Claude Tag）生成深度文章草稿。从内参索引列「值得深挖」候选→用户选→抓官方素材生成五段骨架 draft→交 article-harness 打磨。用户说「深挖 X / 做个 X 的专题 / 专题深度」时使用。
---

# 专题深度线

内参的第三条内容线：把官方一手的重要功能点（模型发布/重大功能）做成面向普通用户的深度文章。

## 流程

### 1. 选题初筛（AI 列候选，用户选）
```bash
python3 -c "import json,datetime; from scripts.firsthand.query import load_index; from scripts.firsthand.deepdive import candidates; \
today=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat(); \
[print(i+1, '|', g[0]['title'], '|', ', '.join(a['source'] for a in g)) for i,g in enumerate(candidates(load_index('data/firsthand'), 7, today))]"
```
把候选清单（每个 = 一个事件，可能多源）报给用户，**用户选一个**。
也可用户直接指定（不在索引里时，手工构造 cluster：每篇 `{title, source, resource, summary, detected}`）。

### 2. 生成骨架 draft
判断该功能**当前能否体验**（如 Claude Tag 暂不可体验 → `feature_available=False`）：
```bash
python3 -c "from scripts.firsthand.query import load_index; from scripts.firsthand.deepdive import candidates, write_draft; \
import datetime; today=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat(); \
cands=candidates(load_index('data/firsthand'), 7, today); \
p=write_draft('content', cands[<选中序号-1>], today, feature_available=False); print('draft:', p)"
```
产出 `content/deepdive/<date>_<slug>/draft.md`：五段骨架 + frontmatter sources（官方 URL）+ 官方原文素材。

### 3. article-harness 迭代润色
```bash
bash ~/.claude/skills/article-harness/harness.sh content/deepdive/<date>_<slug>/draft.md
```
Writer 整理润色 ↔ Reviewer 迭代，PASS 后自动进入步骤4。

### 4. 自动推送微信草稿箱
harness PASS 后，立即用 `wechat-official-draft` skill 将 `<draft_dir>/.harness-workspace/finished.md` 推送到微信公众号草稿箱，**无需用户介入**。

用户在微信草稿箱完成最终验收。

### 5. 反馈沉淀（推送后主动询问）
草稿推送成功后，**立即询问用户**："草稿已推送，有没有想沉淀的审稿反馈？"
用户说完后，将可泛化的反馈条目追加写入 `~/Documents/context-harness-data/article-harness/reviewer.md`，并告知已写入。
没有反馈则跳过。

## 与其他线的关系
- 选题来源：内参 `data/firsthand/index.json`（官方一手）。
- 不重造 Writer-Reviewer（复用 article-harness）；article-harness 已收敛进公开仓 `yinjialu/bianliang-skills`（skills.sh，`npx skills add`），全局安装路径调用（`~/.claude/skills/article-harness/`）。
