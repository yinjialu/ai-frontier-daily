---
name: ai-daily-digest
description: >-
  Generate and publish a daily AI-vendor news card digest. Fetches the latest
  Anthropic (and later OpenAI, etc.) official announcements, curates them into
  concise Chinese summaries, renders editorial 小红书 (1080×1440) and 微信公众号
  cards, updates a GitHub Pages review page, and can push a mobile notification.
  Use when the user wants to "做今天的 AI 日报 / Anthropic 动态卡片", "抓取最新
  Anthropic 新闻并生成小红书图", "更新每日 AI 速递", refresh the gh-pages review
  page, or run the daily digest pipeline.
---

# AI Daily Digest（每日 AI 大厂动态卡片）

抓取 AI 大厂（当前 **Anthropic + OpenAI**，可继续扩展）官方动态 → 中文策展 → 渲染
小红书 / 公众号卡片 → 更新 GitHub Pages 展示页 → 推送移动端通知。发布到平台的
最后一步由人工完成（符合各平台规则）。

## 多厂商（vendor）

每个厂商一条独立轨道，用 `--vendor <id>`（缺省 `anthropic`）贯穿全流程：

- 数据/产物分轨：`data/<vendor>/<date>.json`、`output/<vendor>/<date>/*.jpg`、
  `output/<vendor>/latest.json`；展示页索引 `output/index.json` 汇总所有厂商（每天一条带 `vendor`）。
- 主题厂商化：`cards.css` 用语义 token（`--bg/--fg/--accent/--feature-*`），`.v-<vendor>` 作用域换肤；
  默认（Anthropic）暖陶土色，`.v-openai` 深墨黑 + 青绿。`cards.js` 的 `VENDORS` 注册表决定品牌文案。
- 当前 id：`anthropic`、`openai`、`gemini`、`nvidia`（单品牌轨）+ `cn`（**国内大模型聚合轨**）。新增见文末「扩展到更多厂商」。

### 聚合轨（`cn` 国产大模型）

国内厂商分散、单家更新低频，故**合成一条聚合轨**：一条 `cn` 轨汇集 DeepSeek / 通义千问 / 智谱 GLM /
Kimi / 豆包 / 文心 / 混元 / MiniMax / 阶跃星辰 / 百川 / 零一万物 / 蚂蚁百灵 等多家。与单品牌轨的差别：

- **每条 update 多一个 `company` 字段**（来源公司中文名，如 `"DeepSeek"`），渲染成卡片上的公司徽标；
  单品牌轨不带 `company`，徽标自动不显示。
- **跨公司择优**：每天把各家动态放一起按重要性降序，**最多 10 条**（单品牌轨是 6 条）。
- **cn 抓取以 WebSearch 为主（重要，与国外四家不同）**：实测国内厂商官网/changelog（火山/腾讯云/
  文心/智谱/MiniMax/DeepSeek 等）对 `WebFetch` 普遍返回 **403**（反爬 + 海外 IP 限制），不可靠。
  故 cn 的发现路径**反过来**：
  1. **首选 `WebSearch`** 按 `daily-search-matrix.json` 逐家公司查近 1~3 天动态（如「智谱 GLM 发布 2026年6月」「MiniMax 新模型」），
     这是 cn 唯一稳定可达的路径（国外四家用 WebFetch RSS，cn 用 WebSearch）。
  2. **`WebFetch` 仅作补充**：搜到具体文章 URL 后可试抓细节，403 就退回用搜索摘要，**不要因抓不到就编造**。
  3. **`sources.yaml` 的 `vendors.cn.rss`（GitHub releases.atom）**可正常抓，但多为 CLI/SDK 线，
     作为「有动静」弱信号兜底，不是模型发布主信号。
- **来源质量（cn 尤其注意）**：WebSearch 命中多为中文科技媒体（二手）。严格按下文「官方 vs 媒体来源区分」：
  能找到官方原文/官方引述的写实，单一媒体源的加「据报道/据梳理」限定词，**不编造版本号与跑分**。
  某家今天没有可靠近 1~3 天动态就跳过它（聚合轨满刊靠跨公司汇总，不靠给每家硬凑）。

## 两种运行方式

| 方式 | 适用 | 摘要来源 |
| --- | --- | --- |
| **A. Claude 驱动**（推荐给 routine / 交互） | Claude Code / 定时 agent | 由 Claude 直接用 web 工具抓取并策展，质量最高 |
| **B. 纯 Python**（GitHub Actions 无人值守） | CI | `run.py --live`：抓 RSS + 调 Claude API |

两种方式产出同一套 `data/<date>.json` 与 `output/<date>/*.png`，由同一渲染器
（`render.js` + `cards.js` + `cards.css`，唯一真源）渲染，风格一致。

## A. Claude 驱动（推荐；云端 routine 与交互会话通用的执行细则）

在仓库根目录执行以下步骤（`output/`、`data/` 写到当前工作目录）。
**厂商列表动态读取，不要写死数量或名字。**

1. **日期与刊号**：按 Asia/Shanghai(UTC+8) 取 `DATE=YYYY-MM-DD`（云端 runner 多为 UTC，
   直接 `date` 会差一天，用 `TZ=Asia/Shanghai date +%F`）；`edition` 用年内第几天
   VOL.NNN（`TZ=Asia/Shanghai date +%j`）。
1.5 **发布链路 doctor（前置健康检查）**：正式抓取/渲染前先跑只读 preflight，提前暴露
   Python/Node/Playwright/Pages 索引等环境问题：
   ```bash
   python3 scripts/doctor_publish.py --stage daily --stage pages
   ```
2. **取厂商清单**：运行 `python3 skills/ai-daily-digest/run.py --vendors`，得到 JSON 数组，
   每项含 `{id, name, brand, sources:[抓取URL]}`，遍历其中每一个厂商（数量与名字以输出为准）。
   若某项 `sources` 为空（环境缺 pyyaml），改读 `sources.yaml` 的 `vendors.<id>` 下
   rss/webfetch 的 url。
   **先建立本次抓取覆盖记录**（这是提交 guard 的硬前置，不是可选笔记）：
   ```bash
   python3 scripts/validate_daily_coverage.py --init --date <DATE>
   ```
   抓取完成后，把每个厂商的官方搜索 query/来源 URL、`firsthand.query` 的候选数量填入
   `output/daily-research/<DATE>.json`，并运行 `python3 scripts/validate_daily_coverage.py --check --date <DATE>`。
   `cn` 聚合轨必须逐一记录 `daily-search-matrix.json` 中的每家公司，即使搜索无结果也要写
   `sources: ["none-found"]`；缺任何一家，后续 guard 会拒绝提交。这样“没有结果”与“没有搜索”不再混淆。
3. **抓取真实最新动态**（对每个厂商 V）：依次 `WebFetch` V.sources 的 URL——RSS/Atom/网页
   都可直接 WebFetch，Google 系 RSS 也能抓；需要细节再 `WebSearch`。厂商特例：Anthropic
   主站 JS 渲染、无官方 RSS（抓 `anthropic.com/news` 顶部条目）；`openai.com/news` 网页对
   WebFetch 返回 403，用其 RSS `https://openai.com/news/rss.xml`。
3.5 **补内参（本机抓取，补云端盲区——重要）**：云端 Routine 是数据中心 IP，`anthropic.com/news`、
   `claude.com/blog` 等 Cloudflare/JS 站常被拦（早报因此会漏 news/blog 内容，只剩 GitHub releases）。
   本机内参监控用住宅 IP 已抓好这些，导出在 `data/firsthand/index.json`。对每个厂商 V，**额外读内参近 1~2 天条目作候选**：
   ```bash
   python3 -m scripts.firsthand.query --vendor <anthropic|openai|gemini|cn> --days 2 --json --include-open-prs
   ```
   把这些条目**并入候选池**，与 WebFetch/WebSearch 结果一起去重策展（同一事件只留一条，优先内参的官方一手 + 真实发布日期）。内参覆盖：anthropic（claude-blog/news/research/engineering/transformer-circuits）、openai、gemini（deepmind/google）、cn（qwen/蚂蚁百灵）；nvidia 暂无内参源，仍走 WebFetch。
   `--include-open-prs` 会只读 open / 已拉取的 `firsthand/*` PR 中 `data/firsthand/**/*.md` 的 OKF 内容，
   让「已发现但尚未合入 main」的一手官方动态也能进入当天早报候选池；它不读取 PR 里的代码改动。
   JSON 输出会给这类候选加 `candidate_origin: "open-pr"` 与 `candidate_ref: "firsthand/<date>"`，
   日报 Issue/最终回复里要保留这个来源标注，便于 review 时知道该候选尚未进入 main。

4. **去重（Claude 链路）**：看 `data/<V.id>/` 里最近的 *.json，只挑近 1~3 天的「新」条目，
   避免与已发布重复；若今天 `data/<V.id>/<DATE>.json` 已存在且已覆盖当日要点，则该厂商
   跳过、不覆写。（B 链路的 `seen.db` 去重不适用于本链路。）
5. **价值筛选 + 中文策展**。只保留对中文 AI 从业者有价值的条目（模型发布、能力
   更新、重要研究、重大合作、定价/政策），过滤纯招聘/办公室开设/人事任命等。
   每条：选一个标签【模型发布/开发者/企业/研究/生态/政策/安全】，写 50–80 字
   客观中文摘要（说清「变了什么 + 对用户意味着什么」，不夸张不编造），按重要性
   降序，最多 6 条。
   - **聚合轨 `cn`**：跨多家公司统一择优，**最多 10 条**，且每条必须带 `company`
     字段（来源公司中文名，如「DeepSeek」「通义千问」「智谱」「Kimi」「豆包」「文心」「混元」
     「MiniMax」「阶跃星辰」「百川」「零一万物」「百灵」），用于渲染公司徽标。
   - **同事件跨源聚合（去重，重要）**：同一件事被多个信息源报道（如 Anthropic 同一发布同时出现在
     `anthropic.com/news` 与 `claude.com/blog`，或内参 + web 抓到同一条）时，**合并成一条**，
     不要重复占用名额。择优规则：优先**官方一手**来源作主链接、取**真实发布日期**（内参的 `published`）；
     正文可点明"多家/多源报道"。判据：标题/主体指向同一事件（同一产品名、同一公告）。聚合轨 `cn`
     同理——同一新闻被多家媒体转载只算一条，`company` 取最权威来源。
     摘要必须保留对应中文限定词（「可能」「据报道」「疑似」），不得改写为断言。
   - **官方 vs 媒体来源区分**：涉及根因分析、「史上最大/最严重」等定性描述，
     须区分是官方 postmortem/Status Dashboard 确认，还是媒体推测或用户反馈；
     若官方仅承认故障存在但未给出根因，摘要只写「官方确认」，不写未经证实的技术原因。
6. **写当天数据**到 `data/<vendor>/<YYYY-MM-DD>.json`（必含 `"vendor"` 字段），字段见下面 schema。
   该厂商今天无值得发的内容则跳过它、不写文件。
   渲染默认输出 **JPEG**（移动端优先：1080×1440、`deviceScaleFactor:1`、质量 86，
   单张约 100–300KB，低于公众号在文图片 1MB 上限，省去后压缩）。可用环境变量
   `CARD_FORMAT=png|jpeg`、`CARD_QUALITY`、`CARD_SCALE` 覆盖。
   - **卡片质感（风格层，正交于 vendor 主题）**：默认「经典」（与历史像素一致）。
     `CARD_STYLE=glass`（或数据里加 `"style":"glass"`）切到「液态玻璃 / Apple Liquid Glass」——
     彩色渐变底 + 磨砂玻璃面板 + 镜面高光，仅换材质不改主题色，新增厂商自动可用。
     backdrop-filter 仅 Chromium（Playwright）/浏览器生效，wkhtml 退化为半透明无模糊。
     本地预览对比：浏览器打开 `skills/ai-daily-digest/glass-preview.html`；
     展示页 `index.html` 顶部「质感」可一键切换（存 `localStorage`）。
7. **渲染卡片**：
   渲染前先跑一次环境自检（幂等；用 `uv` 管 Python 依赖、安装 npm 依赖与 Playwright Chromium，
   并做 Python + Chromium smoke test）：
   ```bash
   scripts/ensure-daily-render-env.sh
   ```
   ```bash
   node "$SKILL_DIR/render.js" data/<vendor>/<date>.json output/<vendor>/<date> --engine playwright
   ```
   （`$SKILL_DIR` = 本 skill 目录；Playwright 渲染器已使用整页 clip 截图，避免元素稳定性等待导致的
   `elementHandle.screenshot` 超时。）
8. **更新展示页指针与索引**（所有厂商处理完后执行一次）：调 `python "$SKILL_DIR/run.py" --reindex`，
   它按实际生成的 *.jpg 重建各厂商 `output/<vendor>/latest.json` + 汇总 `output/index.json`，
   不要手拼这两个文件。
9. **提交并推送**（触发 GitHub Pages 重新发布）：若本次有任意厂商产出新内容：
   ```bash
   git add -A data output
   python3 scripts/validate_daily_coverage.py --check --date <DATE>
   scripts/guard-daily-content-commit.sh <DATE>
   git commit -m "daily: <DATE>"
   ```
   **一次提交涵盖所有厂商；commit 格式必须是 `daily: YYYY-MM-DD`**（auto-merge guard 的
   正则依赖此标记，写成 `daily: <vendor> <date>` 会被整支跳过）。推送遵循仓库根目录
   AGENTS.md / CLAUDE.md 与下文「推送策略（routine 必读）」：云端只推当前工作分支
   （Codex 用 `Codex/daily-YYYY-MM-DD`，Claude 用 `claude/*`），本机会话可直推 main。
   `guard-daily-content-commit.sh` 是 hard guard：当前分支必须是 `Codex/daily-<DATE>`，
   staged diff 必须只含 `data/` + `output/` 且不能含 `data/firsthand/`，否则直接停止。
   所有厂商今天都无新内容则不提交、直接结束。
10. **开当天 GitHub Issue**（每日讨论贴，仅当本次有新内容时执行）：在本仓库创建 Issue，
    标题 `📰 VOL.NNN · YYYY-MM-DD 每日 AI 动态`，label `daily-digest`。正文按厂商分节，
    每节列出今日各条目（标题加粗 + 一句话摘要 + 源链接），末尾附展示页链接并邀请讨论。
    优先用 GitHub MCP 的 issue 创建工具（如 `mcp__github__issue_write`，method=create），
    没有就用 `gh issue create`；若 label 不存在或打 label 失败，就不带 label 创建，
    确保 Issue 本身建成功。创建前先查当天是否已有同标题 Issue，已有则跳过，每天最多一个。
11. **推送移动端**：用 `PushNotification` 发一条通知：一句话概括今天各厂商各发了几条 +
    Issue 链接（若本次创建了）+ 展示页 `https://yinjialu.github.io/ai-frontier-daily/`
    （工具不可用则写进最终回复）。微信草稿由本机定时任务处理，云端无需管。

### data JSON schema

```json
{
  "vendor": "anthropic",
  "date": "2026.05.31", "cnDate": "5月31日 周日",
  "edition": "VOL.151", "brand": "AI 前哨 · 每日 Anthropic",
  "updates": [
    {"tag": "模型发布", "title": "标题", "summary": "50-80字中文摘要", "source": "anthropic.com"}
    // 聚合轨 cn 每条还需带 "company": "DeepSeek"（来源公司中文名 → 渲染公司徽标）
  ],
  "outroTitle": "每天一条\n看懂 AI 大厂动向",
  "outroDesc": "…", "outroCta": "关注 · 不错过任何更新"
}
```
`vendor` 取 `run.py --vendors` 输出的任一 id（不要写死取值范围）。`brand` 用该 vendor 的 brand 字段。
`edition` 用年内第几天（`TZ=Asia/Shanghai date +%j`）。今天无值得发的内容则不发卡片。

## B. 纯 Python（无人值守 / CI）

```bash
pip install -r requirements.txt          # pyyaml feedparser
export DIGEST_OUT="$PWD"                  # data/ output/ 写到这里（默认即当前目录）
python run.py                       # mock：用 fixtures，离线跑通，不需要 key（anthropic）
python run.py --vendor openai       # 指定厂商
python run.py --live                # 真实：抓 sources.yaml 的 RSS + 调 Claude API（需 ANTHROPIC_API_KEY）
python run.py --force               # 忽略去重强制处理
python run.py --engine playwright   # 字体保真渲染（生产推荐）
python run.py --reindex             # 仅重建 latest.json + index.json（扫描所有厂商）
python run.py --vendors             # 打印厂商清单 JSON [{id,name,brand,sources}]（routine/CI 自适应遍历用）
```

- 去重 `seen.db`（SQLite，指纹按 `vendor|归一化标题`）写到 `DIGEST_OUT`，各厂商互不干扰，每天只推增量。
- live 摘要在 `curator.py` 调 Claude API（system prompt 随 vendor 切换）；mock 用离线启发式。
- CI（`.github/workflows/daily.yml`）每天循环跑所有厂商（`for v in $(run.py --vendors …)`），再一次性提交；
  新增厂商自动覆盖。CCR 每日 routine 同样自适应。

## 文件结构

```
skills/ai-daily-digest/
  SKILL.md          # 本文件
  ADD_VENDOR.md     # 新增厂商 runbook（加 Gemini/英伟达等照此走）
  run.py            # 编排：采集→去重→摘要→渲染→更新指针（--vendor / --reindex）
  collector.py      # 采集（mock 读 fixtures / live 抓 vendors.<vendor>.rss）
  curator.py        # 策展+摘要（mock 启发式 / live 调 Claude；VENDOR_META 品牌文案）
  dedup.py          # SQLite 去重（指纹按 vendor 命名空间）
  render.js         # 渲染器（playwright / wkhtmltoimage）
  cards.js          # 卡片构建逻辑 + VENDORS 注册表（浏览器与 Node 共用，唯一真源）
  cards.css         # 卡片样式（语义 token + .v-<vendor> 主题）
  sources.yaml      # 信息源（按 vendors.<vendor> 分组的 RSS / webfetch）
  fixtures/         # mock 样例数据

# 数据/产物（写到 DIGEST_OUT，默认仓库根）：
data/<vendor>/<date>.json          # 当天结构化数据
output/<vendor>/<date>/*.jpg       # 渲染卡片
output/<vendor>/latest.json        # 该厂商最新一天指针（发布脚本消费）
output/index.json                  # 汇总所有厂商，供展示页（每天一条带 vendor）
```
仓库根目录的 `index.html`（展示页）读 `output/index.json`，顶部 Anthropic/OpenAI
切换 Tab，按厂商主题展示当天卡片轮播 + 采集热力图，由 GitHub Pages 部署。

## 输出卡片

- 小红书 1080×1440：封面 + 每条一张内容卡（含 `01/06` 页码与水印序号）+ 结尾卡。
- 微信公众号：900×383 封面 + 正文长图（高度自适应）。

## 发布（人工，符合平台规则）

- 小红书【全自动，2026-06-11 起】：走本机 [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
  服务（二进制 `~/.local/bin/xiaohongshu-mcp`，cookie/工作目录 `~/.config/xiaohongshu-mcp/`，
  HTTP MCP 端口 18060，账号 ai-report）。一条命令发一厂商：
  `python skills/ai-daily-digest/publish_xhs_newspic.py --vendor <id> [--private|--dry-run]`
  —— 内部先调 `to_xhs_post.py` 组装素材（标题≤20 字/正文≤1000 字/标签数组/竖图清单，
  标签随厂商切换），再把卡片复制为 ASCII 临时名（服务不接受中文路径）调 `publish_content`。
  服务未启动会自动拉起；登录态失效时在 `~/.config/xiaohongshu-mcp/` 下重跑
  `~/.local/bin/xiaohongshu-login` 扫码。`watch-and-publish.sh` 的 [4/4] 步已挂入每日链路
  （去重标记 `.last_published_xhs.<vendor>`，厂商间隔 45s 防风控连发）。
  注意：xiaohongshu-mcp 是独立登录态，与浏览器里 creator 后台网页登录可能互踢；
  `--private` 发「仅自己可见」笔记，用于测试链路。
- 公众号个人订阅号：草稿接口权限已回收，手动建草稿贴图，或用 135/壹伴等已授权
  编辑器导入草稿箱。
- 公众号【已认证服务号】——「云端抓取 → 本机合并+推送」半自动链路（仍由人工群发）：

  **推送策略（routine 必读）**：云端 GitHub 代理只允许推当前工作分支，
  直推 main 会得到 403——这是预期行为，**不要把 403 当失败重试，也不要尝试推 main**。
  routine 只需把 `daily: YYYY-MM-DD` 提交推到自己的工作分支（Codex 用 `Codex/daily-YYYY-MM-DD`，
  Claude 用 `claude/*`），
  `.github/workflows/auto-merge-daily.yml` 会在分支只含 `data/`+`output/` 改动时自动合并入 main
  并删除分支。**代码 / 文档 / 配置改动不要混进每日内容分支**——guard 会整支跳过；
  这类改动请单独开分支提 PR 人工合并（纯文档推送不会触发 workflow，混推会滞留在分支上流失）。

  一条命令搞定「合并分支 + 各厂商建草稿」：

  ```bash
  scripts/watch-and-publish.sh --dry-run   # 演练：照常合并每日内容分支，但微信只打印结构不碰 API
  scripts/watch-and-publish.sh             # 合并 daily-* / Codex/daily-* → main → 为当天每个厂商建微信贴图草稿
  VENDORS_PUBLISH="anthropic openai" scripts/watch-and-publish.sh   # 只给指定厂商发微信
  ```

  它做三件事：① `git fetch`，把未合并的 `origin/daily-<DATE>` / `origin/Codex/daily-<DATE>` 用 `-X theirs` 合并进 main、
  `run.py --reindex` 重建指针、push main、删远端分支；② 对每个有当天 `data/<vendor>/<DATE>.json`
  的厂商跑 `publish_wechat_newspic.py --vendor <id>` 建**贴图(newspic)**草稿；③ `.last_published.<vendor>`
  去重（每家每天只成功一次）。凭据 `~/.config/wechat-official-draft/config.yaml`，本机公网 IP 须在
  公众号 IP 白名单，且需已认证服务号。

  - 单厂商手动发：`scripts/publish-local.sh [--vendor <id>]`（只发不合并）。
  - 图文文章形态（可选）：`to_wechat_md.py [--vendor <id>]` → `push_draft.mjs`。

  每日自动：`scripts/launchd-publish.plist`（LaunchAgent，每天 23:15/23:45/次日 00:30 通过独立 publisher worktree 跑 `watch-and-publish.sh`，
  多次兜底吸收云端 cron 抖动）。安装/更新：
  ```bash
  cp scripts/launchd-publish.plist ~/Library/LaunchAgents/com.yinjialu.ai-frontier-daily.publish.plist
  launchctl unload ~/Library/LaunchAgents/com.yinjialu.ai-frontier-daily.publish.plist 2>/dev/null
  launchctl load -w ~/Library/LaunchAgents/com.yinjialu.ai-frontier-daily.publish.plist
  ```

## 扩展到更多厂商

**完整步骤见 [`ADD_VENDOR.md`](ADD_VENDOR.md)**（含调研信息源、配色、产出首期、验证的逐步 runbook，
附 Gemini / 英伟达候选配置）。速览——改动集中在 5 个文件；**云端定时与渲染器无需改**：

1. `sources.yaml`：在 `vendors.<新id>` 下加 `rss`/`webfetch` 源（先 `curl -sI` / WebFetch 实测）。
2. `cards.js`：在 `VENDORS` 注册表加一项（name/daily/label）。
3. `cards.css`：加一个 `.v-<新id>` 主题块覆盖语义 token（深底主题记得加 `.v-<id>.card::after{screen}`）。
4. `index.html`：加**两处颜色**——`.vtab[data-v="<id>"]{--vc}`（Tab 选中色）+ `body.v-<id>{...--clay/--h0..h4}`
   （页面强调色 + 热力图梯度）。**易漏**：缺了 Tab 选中态没色、页面 chrome 不换色。
5. `curator.py`：在 `VENDOR_META` 加品牌名/brand/结尾文案；发布脚本（to_xhs_post/to_wechat_md/
   publish_wechat_newspic）的 `VENDOR_NAME`/标签按需补。
6. **云端定时无需改**：Codex Automation / CCR routine 与 `daily.yml` 都自适应——跑 `run.py --vendors` 读出厂商清单
   再遍历；只要新厂商在 `curator.py` `VENDOR_META` + `sources.yaml` 登记好即可被自动带上。

展示页 Tab 的**显示名与顺序**也自动派生（名字取 `cards.js` 的 `VENDORS.name`、顺序按其定义序）；
只有上面第 4 步的**颜色**需手加。`run.py --vendors` 可本地自测厂商清单与各家源 URL。
