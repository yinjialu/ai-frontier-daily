---
name: deepdive-xiaohongshu
description: 把专题深度成稿转换为小红书图文卡（封面+知识卡 1080×1440）+ 笔记文案，复用本仓渲染/发布栈。触发词「发小红书 / 转小红书图文 / 深度内容小红书」。
---

# deepdive-xiaohongshu

把 `content/deepdive/<slug>/draft.md` 成稿稳定转换为小红书图文笔记。

## 步骤

### 1. 生成卡片脚本 xhs.json
读成稿 `content/deepdive/<slug>/draft.md`（及 `assets/`/`xhs/assets/` 下配图），**改写**（不照搬）成 `content/deepdive/<slug>/xhs.json`。默认使用沉淀自 `content/deepdive/2026-06-24_introducing-claude-tag/xhs/` 的 editorial magazine 版式：

- `slug`：文章目录名去日期前缀。
- `title`：小红书标题，**≤20 字**，点出核心钩子。
- `style`：固定 `"editorial"`。
- `edition` / `brand` / `period`：如 `"AI FRONTIER"` / `"变量生活"` / `"2026.06"`。
- `cover`：文章已有封面图相对路径（如 `assets/cover-*.png`）；没有则 `null`。
- `coverTitle`：封面显示标题，可用 `\n` 手动断成两行。
- `topics`：封面 pill，2~3 个短标签。
- `coverCaption`：封面底部 1~2 行短句。
- `cards`：**4~8 张**，每张 `heading` 最多两行、每行 ≤14 字；优先用下面三种卡：
  - `{"kind":"quote","heading","quote","notes","footer"}`：观点/转折卡，`notes` 为 `[label,text]` 数组。
  - `{"kind":"image","heading","image","caption","footer"}`：配图解释卡，`image` 是相对路径。
  - `{"kind":"closing","heading","quote","notes","footer"}`：收束/导流卡。
- `caption`：笔记正文，**≤1000 字**，开头一句抓人 + 分点讲清 + 结尾引导，自然口吻。
- `tags`：1~10 个，如 `["AI","Claude","Agent"]`。

**改写原则**：长文 → 杂志卡。封面给总隐喻；quote 卡承载判断；image 卡承载关键结构图/小黑插画；closing 卡收束到公众号长文。不要把长段落塞进 bullet，宁可减少卡数、放大单个判断。

### 2. 校验 + 渲染
```bash
python -m scripts.deepdive.xhs_validate content/deepdive/<slug>/xhs.json   # 不过线先改
python -m scripts.deepdive.render_xhs content/deepdive/<slug>             # 出图到 output/deepdive/<slug>/
```
校验不过会列出超限项（标题/文案/卡数/行数/每行字数）——按提示缩短重生成，**不要硬发**。

### 3. 发布
- 移动端：打开发布页 `publish.html`「深度内容」入口 → 选当前 slug → 「📲 发送到快捷指令」把图存相册 → 小红书 App 手动发；文案从「🔗 复制文案」取（`output/deepdive/<slug>/caption.txt`）。
- 自动发（可选）：复用 `skills/ai-daily-digest/publish_xhs_newspic.py` 的 xiaohongshu-mcp 链路。

## 稳定性
- 生成期硬约束 + `xhs_validate.py` 拦截（标题≤20/文案≤1000/卡 4~8/heading 每行≤14）。
- 版式 `.card.deepdive.xhs-card` 走 `overflow:hidden` 兜底；卡片尺寸固定 1080×1440。
- 封面图/正文配图自动生成不在本 skill（交 Codex 小黑出图）；本 skill 只用已有图片路径。

## 与其他线的关系
- 输入来自专题深度成稿（`firsthand-deepdive` 产出 + article-harness 打磨）。
- 渲染复用 `skills/ai-daily-digest/render.js`（深度卡为 `cards.js`/`cards.css` 分支 `kind:"deepdive", style:"editorial"`）。
- 发布复用早报小红书链路（`publish.html` / `publish_xhs_newspic.py` / xiaohongshu-mcp）。
- 设计/计划见 `docs/superpowers/{specs,plans}/2026-06-24-专题深度小红书发布*`。
