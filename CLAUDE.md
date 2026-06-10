# ai-frontier-daily

抓取 AI 大厂官方动态 → 中文策展 → 渲染卡片 → GitHub Pages 展示 → 公众号/小红书半自动发布。
完整流水线指令(信源、策展规范、渲染、发布)见 `skills/ai-daily-digest/SKILL.md`——执行每日任务前先读它。

## 推送策略(云端 routine / 任何自动化会话必读)

- **只推当前工作分支(`claude/*`),不要尝试推 main。** 云端 GitHub 代理直推 main 必 403,
  这是预期行为,**不要把 403 当失败重试**。
- 推完分支即收工:`.github/workflows/auto-merge-daily.yml` 会在分支只含 `data/` + `output/`
  改动时自动合并入 main 并删除分支。
- **代码 / 文档 / 配置改动不要混进每日内容分支**:guard 会整支跳过,纯文档推送不触发
  workflow,改动会滞留流失。这类改动单独开分支提 PR,人工合并。
- 每日内容提交格式:`daily: YYYY-MM-DD`(auto-merge guard 依赖此标记)。

## 本机发布链路(参考)

- launchd 每天 07:15 / 07:45 / 08:30 跑 `scripts/watch-and-publish.sh`:拉 main → 各厂商建
  微信贴图草稿(`publish_wechat_newspic.py` 直调,凭据 `~/.config/wechat-official-draft/config.yaml`)。
- 贴图(newspic)链路不走 wechat-official-draft skill(其 push_draft.mjs 仅支持图文 news 形态);
  skill 留给交互排版自由文章,已项目内安装于 `.agents/skills/`。
