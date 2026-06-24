# bianliang-skills 收敛（工程 B）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `article-harness` 收敛进公开仓 `yinjialu/bianliang-skills`（专注成稿），按 skills.sh 机制全局安装到 Claude Code + Codex；个人写作品味（writer/reviewer）留本地、运行时优先加载，不外泄。

**Architecture:** 公开仓放 harness.sh + writer/reviewer **通用模板**；个人版移到 `~/Documents/context-harness-data/article-harness/`；harness.sh 运行时本地优先、否则退模板。`npx skills add` 装进两个工具。最后改 ai-frontier-daily 的 firsthand-deepdive 调用路径。

**Tech Stack:** bash（harness.sh）、gh（建仓）、`npx skills`（skills.sh 安装）、markdown。

**关键路径：**
- 源：`/Users/jialu/Documents/Engineer/skills/article-harness/`（article-harness 现位置）
- 公开仓本地工作副本：`/Users/jialu/Documents/bianliang-skills/`（新建，结构 `skills/article-harness/`）
- 个人私有：`/Users/jialu/Documents/context-harness-data/article-harness/{writer,reviewer}.md`
- 安装落点：`~/.claude/skills/article-harness/` + `~/.codex/skills/article-harness/`

---

## File Structure

| 文件 | 职责 |
|------|------|
| `~/Documents/bianliang-skills/skills/article-harness/{SKILL.md,harness.sh,writer.md,reviewer.md}` | 公开仓 skill（writer/reviewer 为脱敏模板）|
| `~/Documents/bianliang-skills/README.md` | 仓说明 |
| `~/Documents/context-harness-data/article-harness/{writer,reviewer}.md` | 个人版（私有，运行时优先）|
| `harness.sh` | 改：本地优先加载 writer/reviewer + 调试钩子 |
| `ai-frontier-daily/skills/firsthand-deepdive/SKILL.md` | 改：harness.sh 调用路径 → 安装路径 |
| `ai-frontier-daily/CLAUDE.md` + `docs/firsthand/...` | 记录新位置/迁移 |

---

## Task 1: 建公开仓骨架 + 拷 article-harness + 脱敏模板

**Files:**
- Create: `~/Documents/bianliang-skills/skills/article-harness/*`（拷自源）
- Create: `~/Documents/bianliang-skills/README.md`
- Modify（拷贝后的副本，非源）: `skills/article-harness/writer.md`、`reviewer.md`

- [ ] **Step 1: 建目录 + 拷 article-harness**

Run:
```bash
mkdir -p ~/Documents/bianliang-skills/skills
cp -R /Users/jialu/Documents/Engineer/skills/article-harness ~/Documents/bianliang-skills/skills/article-harness
ls ~/Documents/bianliang-skills/skills/article-harness
```
Expected: 列出 `SKILL.md harness.sh writer.md reviewer.md`（及 .harness-workspace 若有则下步清掉）。

- [ ] **Step 2: 清掉拷进来的工作区残留**

Run:
```bash
rm -rf ~/Documents/bianliang-skills/skills/article-harness/.harness-workspace
```

- [ ] **Step 3: 脱敏 writer.md 模板（第 5 行作者身份）**

编辑 `~/Documents/bianliang-skills/skills/article-harness/writer.md`，把：
```
文章作者是尹家露，携程 AI 技术部，专注 Agent 基础设施。写作风格：
```
替换为：
```
文章作者是一名中文技术作者，从一线实践与第一手调研出发写作。写作风格：
```

- [ ] **Step 4: 脱敏 reviewer.md 模板（删个人自我定位项）**

编辑 `~/Documents/bianliang-skills/skills/article-harness/reviewer.md`，**删除**维度 4 里这两行（个人特定，非通用）：
```
- ✗ **作者自我定位措辞固定**：作者背景统一写"做 **Agent 基础设施**"，**不要写成"Agent / MCP 基础设施"或带 MCP**。
  （MCP 作为文章话题该提还提，但不作为作者的自我方向标签。）检查方法：搜作者自述句里的"MCP"。
```
（其余维度 + 极端强度词/制造对立/骨架标题/占位说明/AI套路腔黑名单都是**通用克制原则**，保留。）

- [ ] **Step 5: 写 README.md**

`~/Documents/bianliang-skills/README.md`:
```markdown
# bianliang-skills

变量生活的内容生产 skills。按 [skills.sh](https://skills.sh/) 发布，`npx skills add yinjialu/bianliang-skills` 安装（Claude Code / Codex 通用）。

## skills

- **article-harness** —— 把带骨架的草稿经 Writer-Reviewer 迭代打磨成可发布文章（专注「成稿」）。
  内置 writer/reviewer 为**通用模板**；个人写作品味放本地 `~/Documents/context-harness-data/article-harness/{writer,reviewer}.md`，
  运行时优先加载（见 `harness.sh`），不随仓公开。

## 后续

review-wechat-layout、wechat-official-draft 将陆续收敛进本仓统一管理。
```

- [ ] **Step 6: git init + 首次提交（不 push，下个 task 改完 harness.sh 再一起）**

```bash
cd ~/Documents/bianliang-skills && git init -q && git add -A && git commit -q -m "init: bianliang-skills + article-harness(脱敏模板)"
echo "ok: $(git -C ~/Documents/bianliang-skills rev-parse --short HEAD)"
```

---

## Task 2: harness.sh 本地优先加载（可测）

**Files:**
- Modify: `~/Documents/bianliang-skills/skills/article-harness/harness.sh`
- Test: `~/Documents/bianliang-skills/skills/article-harness/test_override.sh`

让 harness.sh 运行时：本地个人 writer/reviewer 存在则优先用，否则退仓内模板。加调试钩子便于测试。

- [ ] **Step 1: 写 failing test**

`~/Documents/bianliang-skills/skills/article-harness/test_override.sh`:
```bash
#!/bin/bash
set -euo pipefail
H="$(cd "$(dirname "$0")" && pwd)/harness.sh"
TMP=$(mktemp -d)
mkdir -p "$TMP/local"
echo "LOCAL-W" > "$TMP/local/writer.md"
echo "LOCAL-R" > "$TMP/local/reviewer.md"

# 1) 本地存在 → 用本地
OUT=$(ARTICLE_HARNESS_LOCAL="$TMP/local" HARNESS_DEBUG_PATHS=1 bash "$H" /dev/null 2>&1)
echo "$OUT" | grep -q "writer: $TMP/local/writer.md" || { echo "FAIL: 未优先本地 writer"; exit 1; }
echo "$OUT" | grep -q "reviewer: $TMP/local/reviewer.md" || { echo "FAIL: 未优先本地 reviewer"; exit 1; }

# 2) 本地不存在 → 退模板(仓内)
OUT2=$(ARTICLE_HARNESS_LOCAL="$TMP/none" HARNESS_DEBUG_PATHS=1 bash "$H" /dev/null 2>&1)
echo "$OUT2" | grep -q "writer: $(dirname "$H")/writer.md" || { echo "FAIL: 未退模板 writer"; exit 1; }

echo "PASS override"
rm -rf "$TMP"
```

- [ ] **Step 2: 运行确认失败**

Run: `bash ~/Documents/bianliang-skills/skills/article-harness/test_override.sh`
Expected: FAIL（当前 harness.sh 无 ARTICLE_HARNESS_LOCAL/HARNESS_DEBUG_PATHS 逻辑，不会打印 `writer:`/`reviewer:` 路径行）

- [ ] **Step 3: 改 harness.sh**

在 `harness.sh` 里，把原来的：
```bash
WRITER_SYSTEM=$(cat "$SKILL_DIR/writer.md")
REVIEWER_SYSTEM=$(cat "$SKILL_DIR/reviewer.md")
```
替换为：
```bash
# 个人写作品味优先：本地存在则用本地，否则退仓内通用模板
LOCAL_DIR="${ARTICLE_HARNESS_LOCAL:-$HOME/Documents/context-harness-data/article-harness}"
WRITER_MD="$SKILL_DIR/writer.md";     [ -f "$LOCAL_DIR/writer.md" ]   && WRITER_MD="$LOCAL_DIR/writer.md"
REVIEWER_MD="$SKILL_DIR/reviewer.md"; [ -f "$LOCAL_DIR/reviewer.md" ] && REVIEWER_MD="$LOCAL_DIR/reviewer.md"
if [ -n "${HARNESS_DEBUG_PATHS:-}" ]; then
  echo "writer: $WRITER_MD"; echo "reviewer: $REVIEWER_MD"; exit 0
fi
WRITER_SYSTEM=$(cat "$WRITER_MD")
REVIEWER_SYSTEM=$(cat "$REVIEWER_MD")
```
（`SKILL_DIR` 已在脚本上方定义，不动。）

- [ ] **Step 4: 运行确认通过**

Run: `bash ~/Documents/bianliang-skills/skills/article-harness/test_override.sh`
Expected: 打印 `PASS override`

- [ ] **Step 5: Commit**

```bash
cd ~/Documents/bianliang-skills
git add -A && git commit -q -m "feat(article-harness): writer/reviewer 本地优先加载 + 测试"
```

---

## Task 3: 个人 writer/reviewer 移到本地私有路径

**Files:**
- Create: `~/Documents/context-harness-data/article-harness/{writer,reviewer}.md`（个人版，私有）

把**个人原版**（含尹家露/携程 + MCP 自我定位等）放到本地私有路径——这是 harness 运行时优先加载的版本。

- [ ] **Step 1: 拷个人原版到私有路径**

Run（从源 Engineer/skills 拷**未脱敏**的原版）:
```bash
mkdir -p ~/Documents/context-harness-data/article-harness
cp /Users/jialu/Documents/Engineer/skills/article-harness/writer.md   ~/Documents/context-harness-data/article-harness/writer.md
cp /Users/jialu/Documents/Engineer/skills/article-harness/reviewer.md ~/Documents/context-harness-data/article-harness/reviewer.md
```

- [ ] **Step 2: 验证个人版含个人信息、模板版不含**

Run:
```bash
echo "个人版应含尹家露: $(grep -c 尹家露 ~/Documents/context-harness-data/article-harness/writer.md)"
echo "个人版应含MCP规则: $(grep -c '自我定位' ~/Documents/context-harness-data/article-harness/reviewer.md)"
echo "模板版应不含尹家露: $(grep -c 尹家露 ~/Documents/bianliang-skills/skills/article-harness/writer.md)"
echo "模板版应不含MCP规则: $(grep -c '自我定位' ~/Documents/bianliang-skills/skills/article-harness/reviewer.md)"
```
Expected: 个人版 1/1，模板版 0/0。

- [ ] **Step 3: 验证 harness（用安装前的仓副本）真用本地个人版**

Run:
```bash
HARNESS_DEBUG_PATHS=1 bash ~/Documents/bianliang-skills/skills/article-harness/harness.sh /dev/null
```
Expected: 打印 `writer: /Users/jialu/Documents/context-harness-data/article-harness/writer.md`（本地优先生效）。

> 注：context-harness-data 是否纳入 git 由其自身管理；本 task 只放文件，不在此提交。

---

## Task 4: 发布公开仓 + 全局安装 + 验证两工具

**Files:** 无（发布/安装操作）

> ⚠️ 这一步会**创建公开 GitHub 仓**（外发布动作）。spec 已授权"建公开仓 + skills.sh 发布"。执行前向用户确认一次再 push。

- [ ] **Step 1: 建公开仓并 push**

```bash
cd ~/Documents/bianliang-skills
gh repo create yinjialu/bianliang-skills --public --source=. --remote=origin --push
```
Expected: 仓创建、main 推送成功。

- [ ] **Step 2: 全局安装（skills.sh / npx skills）**

```bash
npx -y skills add yinjialu/bianliang-skills
```
Expected: 安装成功提示。

- [ ] **Step 3: 验证两个工具都装上**

Run:
```bash
ls -la ~/.claude/skills/article-harness/SKILL.md 2>/dev/null && echo "Claude Code ✓" || echo "Claude Code ✗"
ls -la ~/.codex/skills/article-harness/SKILL.md   2>/dev/null && echo "Codex ✓" || echo "Codex ✗"
```
Expected: 两个都 ✓。（若某工具的安装目录不同，按 `npx skills` 实际落点核对；Codex 安装落点以其文档为准。）

- [ ] **Step 4: 验证装好的 harness 仍本地优先**

```bash
HARNESS_DEBUG_PATHS=1 bash ~/.claude/skills/article-harness/harness.sh /dev/null
```
Expected: 打印 `writer: .../context-harness-data/article-harness/writer.md`（安装版也走本地个人品味）。

---

## Task 5: 收尾——旧副本单一真相 + 改 firsthand-deepdive 路径

**Files:**
- Delete/symlink: `/Users/jialu/Documents/Engineer/skills/article-harness`
- Modify: `/Users/jialu/ai-frontier-daily/skills/firsthand-deepdive/SKILL.md`

- [ ] **Step 1: 旧 Engineer/skills/article-harness → 软链到安装版（单一真相）**

```bash
rm -rf /Users/jialu/Documents/Engineer/skills/article-harness
ln -s ~/.claude/skills/article-harness /Users/jialu/Documents/Engineer/skills/article-harness
ls -la /Users/jialu/Documents/Engineer/skills/article-harness
```
Expected: 显示软链 → `~/.claude/skills/article-harness`。

- [ ] **Step 2: 改 firsthand-deepdive 里 harness.sh 调用路径**

编辑 `/Users/jialu/ai-frontier-daily/skills/firsthand-deepdive/SKILL.md`，把第 3 步的：
```
bash /Users/jialu/Documents/Engineer/skills/article-harness/harness.sh content/deepdive/<date>_<slug>/draft.md
```
改为：
```
bash ~/.claude/skills/article-harness/harness.sh content/deepdive/<date>_<slug>/draft.md
```
并把文末"与其他线的关系"里"复用 article-harness；工程 B 收敛后仅改第 3 步路径"更新为"已收敛进 bianliang-skills，全局安装路径调用"。

- [ ] **Step 3: 冒烟验证 firsthand-deepdive 路径可达**

Run:
```bash
test -e ~/.claude/skills/article-harness/harness.sh && echo "harness 路径可达 ✓"
```
Expected: `harness 路径可达 ✓`

- [ ] **Step 4: Commit（ai-frontier-daily 分支）**

```bash
cd /Users/jialu/ai-frontier-daily
git add skills/firsthand-deepdive/SKILL.md
git commit -m "chore(deepdive): article-harness 调用改为 bianliang-skills 全局安装路径"
```

---

## Task 6: 文档串联

**Files:**
- Modify: `/Users/jialu/ai-frontier-daily/CLAUDE.md`

- [ ] **Step 1: CLAUDE.md 记录 article-harness 新位置**

在 `CLAUDE.md` 的「第三条内容线」段落末尾追加：
```markdown
- article-harness 已收敛进公开仓 `yinjialu/bianliang-skills`（skills.sh，`npx skills add yinjialu/bianliang-skills`），
  Claude Code/Codex 全局安装于 `~/.claude/skills/article-harness`、`~/.codex/skills/article-harness`。
  个人写作品味（writer/reviewer）留本地 `~/Documents/context-harness-data/article-harness/`，运行时优先加载，不随仓公开。
  设计/计划见 `docs/superpowers/{specs,plans}/2026-06-24-bianliang-skills-收敛*`。
```

- [ ] **Step 2: Commit**

```bash
cd /Users/jialu/ai-frontier-daily
git add CLAUDE.md
git commit -m "docs(skills): 记录 article-harness 收敛进 bianliang-skills"
```

---

## 完成标准

- [ ] 公开仓 `yinjialu/bianliang-skills` 已建、含 `skills/article-harness/`（writer/reviewer 为脱敏模板）
- [ ] `bash test_override.sh` PASS（本地优先逻辑）
- [ ] 个人 writer/reviewer 在 `~/Documents/context-harness-data/article-harness/`，harness 运行时优先加载
- [ ] `npx skills add` 后 `~/.claude/skills/` 与 `~/.codex/skills/` 都有 article-harness
- [ ] 旧 Engineer/skills/article-harness 软链到安装版，无重复真相
- [ ] firsthand-deepdive 调用路径已改、可达；CLAUDE.md 记录新位置
