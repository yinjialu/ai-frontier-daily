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

### 3. 交 article-harness 打磨（复用，不重造）
```bash
bash ~/.claude/skills/article-harness/harness.sh content/deepdive/<date>_<slug>/draft.md
```
Writer 整理润色 ↔ Reviewer 按 reviewer.md 评分迭代，输出成稿。**用户只审核**。

### 4. 审核反馈沉淀（已有机制）
用户对成稿的每条可泛化反馈 → 沉淀进 `article-harness/reviewer.md`（含专题深度专属维度：官方案例翻译准确 / 对普通用户友好不堆术语 / 截图占位标注清楚）。说一次，后续自动检查。

### 5. 发布
终审后 → `wechat-official-draft` skill 排版发布。

## 与其他线的关系
- 选题来源：内参 `data/firsthand/index.json`（官方一手）。
- 不重造 Writer-Reviewer（复用 article-harness）；article-harness 已收敛进公开仓 `yinjialu/bianliang-skills`（skills.sh，`npx skills add`），全局安装路径调用（`~/.claude/skills/article-harness/`）。
