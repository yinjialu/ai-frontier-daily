# ai-frontier-daily

抓取 AI 大厂官方动态 → 中文策展 → 渲染卡片 → GitHub Pages 展示 → 公众号/小红书半自动发布。
完整流水线指令(信源、策展规范、渲染、发布)见 `skills/ai-daily-digest/SKILL.md`——执行每日任务前先读它。

## 服务器主流程（2026-09 迁移）

- 常驻主流程由服务器 Hermes Cron 执行 `scripts/server/worker.py`：每 30 分钟巡检，07:30 逐家官方站点补充搜索，08:00 生成中文早报与发布卡片，08:15 幂等补偿。业务时间统一 Asia/Shanghai，安装器显式换算服务器时区。
- 自动订阅清单是 `deploy/server-sources.yaml`；搜索矩阵是 `deploy/discovery-sources.yaml`（包含全部 12 家国内公司）。官方原文才进入卡片；搜索摘要只作线索。RSSHub 仅为转换层，不能提高来源权威性。
- 服务器所有状态、私有草稿、投递回执在 `.server-state/`（持久卷、gitignore），SQLite 原子写入。新增/修改来源首轮静默基线，历史文章不会作为突发新闻推送。
- 服务器覆盖台账是 `.server-state/health.json`、`research/<date>.json` 和 `editions/<date>/coverage.json`；必须区分成功、失败、未搜索和无可靠新内容。下面 `validate_daily_coverage.py` 是旧 GitHub 日报工作流的覆盖契约，继续适用于该流程，不能伪造 WebSearch 或 firsthand.query 执行记录来满足校验。
- 通过当前 Hermes 飞书机器人发送通知卡片及 ZIP 发布包（小红书竖图、公众号封面/长图、中文文案/原文链接）。公众号/小红书正式发布仍由用户审核后手动执行。服务器不向公开仓库提交私人运行状态，也不自动更新 Pages。
- 迁移部署与回滚见 `deploy/README.md`。原本机 launchd / Codex Automation 为旧链路参考，不再作为服务器的运行依赖。代码变更仍单独开 `Codex/*` 分支提 PR。

## 推送策略(云端 routine / 任何自动化会话必读)

- **每日早报内容生成已迁移到 Codex Automation**:每天北京时间 22:00 预制次日刊,按
  `skills/ai-daily-digest/SKILL.md` 生成 `data/` + `output/`,提交 `daily: YYYY-MM-DD`,
  推 `Codex/daily-YYYY-MM-DD` 分支;auto-merge workflow 负责合入 main。
- **只推当前工作分支(`claude/*`),不要尝试推 main。** 云端 GitHub 代理直推 main 必 403,
  这是预期行为,**不要把 403 当失败重试**。
- 推完分支即收工:`.github/workflows/auto-merge-daily.yml` 会在分支只含 `data/` + `output/`
  改动时自动合并入 main 并删除分支。
- **代码 / 文档 / 配置改动不要混进每日内容分支**:guard 会整支跳过,纯文档推送不触发
  workflow,改动会滞留流失。这类改动单独开分支提 PR,人工合并。
- 每日内容提交格式:`daily: YYYY-MM-DD`(auto-merge guard 依赖此标记)。

## 一手信源内参监控(独立于每日日报)

- launchd `com.yinjialu.ai-frontier-daily.firsthand` 每小时 + 开机自启，通过固定独立 worktree 跑 `scripts/monitor_firsthand.py`:
  抓 `firsthand-sources.yaml` 信源 → 新文章经 DeepSeek Anthropic-compatible API 出中文摘要
  (`~/.config/ai-frontier-daily/firsthand.env`) → 写 `data/firsthand/<id>/*.md`(OKF)
  → **当天累积一个 `firsthand/<date>` PR**(reviewer=yinjialu):当天首批建 PR,后续批次往同分支追加
  commit + 评论 @yinjialu 通知(克制:一天一条线程,不刷屏)。装/触发见 `scripts/install-firsthand-launchd.sh`;
  与主工作区及每日发布任务(`com.yinjialu.ai-frontier-daily.publish`)隔离。新机迁移见 `scripts/SETUP-NEW-MACHINE.md`。
  若 PR 里有失败摘要,评论 `@DeepSeek` 可触发 `.github/workflows/deepseek.yml` 用 DeepSeek 补修并提交回 PR 分支。
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
- **小红书发布**:`deepdive-xiaohongshu` skill 把成稿 → `xhs.json`(卡片脚本,硬约束校验 `scripts/deepdive/xhs_validate.py`)
  → `scripts/deepdive/render_xhs.py` 复用 `render.js` 渲染 1080×1440 知识卡到 `output/deepdive/<slug>/`(封面内联 base64
  规避 setContent 拦 file://;深度卡为 `cards.js`/`cards.css` 纯追加 `kind:"deepdive"`)→ `publish.html`「深度内容」入口
  移动端发布(快捷指令)或 `publish_xhs_newspic.py`(xiaohongshu-mcp)。设计/计划见
  `docs/superpowers/{specs,plans}/2026-06-24-专题深度小红书发布*`。

## 本机发布链路(参考)

- launchd 每天 23:15 / 23:45 / 次日 00:30 跑独立 publisher worktree：读取次日刊 → 各厂商建
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
