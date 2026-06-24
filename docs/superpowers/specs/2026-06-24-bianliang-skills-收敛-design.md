# bianliang-skills 收敛（工程 B）设计

**日期**: 2026-06-24
**状态**: 待实现

## 背景与目标

通用内容生产 skills 现在散落（`Documents/Engineer/skills/` + installed + ai-frontier-daily/skills），无单一真相，跨工具（Claude Code / Codex）维护费劲。

工程 B：建一个**公开仓 `yinjialu/bianliang-skills`**，把内容生产 skills 收敛进去，按 **skills.sh** 机制（`npx skills add yinjialu/bianliang-skills`）全局安装——Claude Code 与 Codex 都能装、都能用，单一真相。

## 范围（分期）

`bianliang-skills` 是**伞仓**，分期收敛：

| 期 | 收进来的 skill | 本工程 B |
|----|---------------|---------|
| **B（本期）** | `article-harness`（专注**成稿**：Writer-Reviewer 把带骨架草稿打磨成可发布文章）| ✅ 做 |
| 后续 | `review-wechat-layout` + `wechat-official-draft`（排版/发布侧，搭配发布）| ⏳ 推迟 |

**不做 / 丢弃：**
- `publish-wechat`（Engineer/skills）—— 与已发布的 `wechat-official-draft` **功能重复**（都是 Markdown→公众号草稿）。发布统一用 `wechat-official-draft`，publish-wechat 弃用。

## 架构

```
公开仓 yinjialu/bianliang-skills
  skills/
    article-harness/
      SKILL.md
      harness.sh
      writer.md      ← 通用模板(脱敏,无尹家露/无个人黑名单)
      reviewer.md    ← 通用模板(通用维度,无个人禁用词)
  README.md
       │
       │ npx skills add yinjialu/bianliang-skills
       ▼
  ~/.claude/skills/article-harness  +  ~/.codex/skills/article-harness
```

## 核心：公开工具 / 私有品味 拆分

`article-harness` 的 `writer.md`（作者风格，含"尹家露/携程"）与 `reviewer.md`（沉淀的个人写作品味、禁用词黑名单、"自我定位不带 MCP"等）是**个人隐私**，不能进公开仓。

| 层 | 内容 | 落点 |
|----|------|------|
| **公开（仓里）** | harness.sh + writer.md/reviewer.md **通用模板**：机制完整、维度通用，去掉一切个人特定信息 | bianliang-skills 公开仓 |
| **私有（本地）** | 你的个人 writer.md（作者风格）+ reviewer.md（沉淀品味/黑名单）| `~/Documents/context-harness-data/article-harness/{writer,reviewer}.md` |
| **加载逻辑** | `harness.sh` 运行时：本地个人版**存在则优先用**，否则退仓内模板 | 改 harness.sh |

**harness.sh 加载规则**（伪代码）：
```bash
LOCAL_DIR="${ARTICLE_HARNESS_LOCAL:-$HOME/Documents/context-harness-data/article-harness}"
WRITER_MD="$SKILL_DIR/writer.md";   [ -f "$LOCAL_DIR/writer.md" ]   && WRITER_MD="$LOCAL_DIR/writer.md"
REVIEWER_MD="$SKILL_DIR/reviewer.md"; [ -f "$LOCAL_DIR/reviewer.md" ] && REVIEWER_MD="$LOCAL_DIR/reviewer.md"
```
→ 工具人人可装可用；你的写作品味只在本地生效、不外泄。沉淀仍写本地 reviewer.md（机制不变）。

## 迁移 + 收尾步骤

1. 建公开仓 `yinjialu/bianliang-skills`，结构 `skills/article-harness/`。
2. 拷 `Engineer/skills/article-harness` 进去；`writer.md`/`reviewer.md` **脱敏成通用模板**（删个人信息/黑名单，留机制与通用维度）。
3. 把**个人 writer.md/reviewer.md** 移到 `~/Documents/context-harness-data/article-harness/`。
4. 改 `harness.sh`：本地个人版优先加载（见上）。
5. push 公开仓 → `npx skills add yinjialu/bianliang-skills` → 验证 `~/.claude/skills/` 与 `~/.codex/skills/` 都装上、能跑。
6. 收尾单一真相：旧 `Engineer/skills/article-harness` 删除或软链到安装版。
7. **改 ai-frontier-daily 的 `skills/firsthand-deepdive/SKILL.md`**：harness.sh 调用路径从 `Engineer/skills/article-harness/harness.sh` 改为安装路径（`~/.claude/skills/article-harness/harness.sh`）——工程 A 留的那一处。

## 不在范围内

- 不收 review-wechat-layout / wechat-official-draft（后续期）。
- 不迁 publish-wechat（弃用，发布用 wechat-official-draft）。
- 不改 article-harness 的 Writer-Reviewer 机制本身（只做拆分 + 收敛 + 路径）。
- 不在 Claude Code 接图像生成（出图交 Codex，已定）。

## 待定（实现时定）

- **本地私有路径**：默认 `~/Documents/context-harness-data/article-harness/`，可用环境变量 `ARTICLE_HARNESS_LOCAL` 覆盖。
- **脱敏粒度**：模板 writer.md 用什么占位作者（如"（作者）"或泛化"中文技术作者"）；reviewer.md 模板保留通用 7 维度 + 通用反套路黑名单（极端强度词等普适项），去掉纯个人项（自我定位 MCP 等）。
