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

## 一手信源内参监控(独立于每日日报)

- launchd `com.yinjialu.ai-frontier-daily.firsthand` 每小时 + 开机自启跑 `scripts/monitor_firsthand.py`:
  抓 `firsthand-sources.yaml` 信源 → 新文章 `claude -p` 出中文摘要 → 写 `data/firsthand/<id>/*.md`(OKF)
  → **当天累积一个 `firsthand/<date>` PR**(reviewer=yinjialu):当天首批建 PR,后续批次往同分支追加
  commit + 评论 @yinjialu 通知(克制:一天一条线程,不刷屏)。装/触发见 `scripts/install-firsthand-launchd.sh`;
  与每日发布任务(`com.yinjialu.ai-frontier-daily.publish`)独立。新机迁移见 `scripts/SETUP-NEW-MACHINE.md`。
- **去重唯一真相 = `data/firsthand/<id>/` 实际文件**(扫 frontmatter `resource`),不是独立账本;
  `data/firsthand-state.json`(健康统计 + 防重复 open_pr_urls)直接提交 main,本机无 403。
- **内参 PR 分支必须 `firsthand/` 前缀、commit 不带 `daily:`**——否则触发/误触发 auto-merge-daily。
- 新增信源走 `firsthand-source-manager` skill;新源**首刊静默**(只记录 `initialized`,不开 PR)。
- plist 用 anaconda python(`/Users/jialu/anaconda3/bin/python3`,依赖在此),非系统 python。
- 阶段二(browser-* 登录态源 + 菜单栏/快捷键授权)见
  `docs/superpowers/specs/2026-06-23-firsthand-monitor-design.md`。

## 第三条内容线:专题深度(firsthand-deepdive)

- 对官方一手的重要功能点做面向普通用户的深度文章。流程:选题初筛(扫 `data/firsthand/index.json` 同事件聚合候选)
  → 用户选 → `scripts/firsthand/deepdive.py` 生成五段骨架 draft 到 `content/deepdive/<date>_<slug>/`
  → 交 `article-harness`(复用,不重造)Writer-Reviewer 打磨 → 用户审核 → 反馈沉淀 → `wechat-official-draft` 发布。
- 触发:`firsthand-deepdive` skill(「深挖 X / 专题深度」)。
- **article-harness 已收敛进公开仓 `yinjialu/bianliang-skills`**(skills.sh,`npx skills add yinjialu/bianliang-skills`),
  全局安装于 `~/.agents/skills/article-harness`(Claude Code/Codex 等 universal 工具共享,Claude Code 软链 `~/.claude/skills/`)。
  **个人写作品味(writer/reviewer)留本地 `~/Documents/context-harness-data/article-harness/`,运行时优先加载,不随仓公开。**
  设计/计划见 `docs/superpowers/{specs,plans}/2026-06-24-{专题深度线,bianliang-skills-收敛}*`。

## 本机发布链路(参考)

- launchd 每天 07:15 / 07:45 / 08:30 跑 `scripts/watch-and-publish.sh`:拉 main → 各厂商建
  微信贴图草稿(`publish_wechat_newspic.py` 直调,凭据 `~/.config/wechat-official-draft/config.yaml`)。
- 贴图(newspic)链路不走 wechat-official-draft skill(其 push_draft.mjs 仅支持图文 news 形态);
  skill 留给交互排版自由文章,已项目内安装于 `.agents/skills/`。

## 小红书发布页 / iPhone 快捷指令(迁移初始化参考)

- 发布页 `publish.html`(GitHub Pages: `/ai-frontier-daily/publish.html`)由 `output/index.json`
  的 `updated`+`days` 驱动:仅展示 `date===updated` 当日内容,某厂商今日无更新显示「今日暂无内容」,
  不回退历史日期(避免发错)。每个 Tab 提供「📲 发送到快捷指令 / 🔗 复制链接 / ⬇️ 打包 zip」。
- 「📲 发送到快捷指令」用 `shortcuts://run-shortcut?name=<指令名>&input=text&text=<链接>` 直接把
  图片链接作为输入喂给快捷指令(绕开剪贴板,规避 iOS 把 URL 列表识别成单对象 / execCommand 失效)。
  首次在页面填一次指令名,存 `localStorage.xhs_shortcut_name`,长按按钮可重设。
- **现成快捷指令(换设备直接装)**:https://www.icloud.com/shortcuts/265f03551e974bac82c2ca8c87031dd4
  名称「社媒内容下载」(页面默认值)。逻辑:拆分文本(快捷指令输入,按新行)→ 重复 → 获取URL内容 →
  存储到相簿。
