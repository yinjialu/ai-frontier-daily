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
- 当前 id：`anthropic`、`openai`。新增厂商见文末「扩展到更多厂商」。

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
2. **取厂商清单**：运行 `python3 skills/ai-daily-digest/run.py --vendors`，得到 JSON 数组，
   每项含 `{id, name, brand, sources:[抓取URL]}`，遍历其中每一个厂商（数量与名字以输出为准）。
   若某项 `sources` 为空（环境缺 pyyaml），改读 `sources.yaml` 的 `vendors.<id>` 下
   rss/webfetch 的 url。
3. **抓取真实最新动态**（对每个厂商 V）：依次 `WebFetch` V.sources 的 URL——RSS/Atom/网页
   都可直接 WebFetch，Google 系 RSS 也能抓；需要细节再 `WebSearch`。厂商特例：Anthropic
   主站 JS 渲染、无官方 RSS（抓 `anthropic.com/news` 顶部条目）；`openai.com/news` 网页对
   WebFetch 返回 403，用其 RSS `https://openai.com/news/rss.xml`。
4. **去重（Claude 链路）**：看 `data/<V.id>/` 里最近的 *.json，只挑近 1~3 天的「新」条目，
   避免与已发布重复；若今天 `data/<V.id>/<DATE>.json` 已存在且已覆盖当日要点，则该厂商
   跳过、不覆写。（B 链路的 `seen.db` 去重不适用于本链路。）
5. **价值筛选 + 中文策展**。只保留对中文 AI 从业者有价值的条目（模型发布、能力
   更新、重要研究、重大合作、定价/政策），过滤纯招聘/办公室开设/人事任命等。
   每条：选一个标签【模型发布/开发者/企业/研究/生态/政策/安全】，写 50–80 字
   客观中文摘要（说清「变了什么 + 对用户意味着什么」，不夸张不编造），按重要性
   降序，最多 6 条。
6. **写当天数据**到 `data/<vendor>/<YYYY-MM-DD>.json`（必含 `"vendor"` 字段），字段见下面 schema。
   该厂商今天无值得发的内容则跳过它、不写文件。
   渲染默认输出 **JPEG**（移动端优先：1080×1440、`deviceScaleFactor:1`、质量 86，
   单张约 100–300KB，低于公众号在文图片 1MB 上限，省去后压缩）。可用环境变量
   `CARD_FORMAT=png|jpeg`、`CARD_QUALITY`、`CARD_SCALE` 覆盖。
7. **渲染卡片**：
   ```bash
   node "$SKILL_DIR/render.js" data/<vendor>/<date>.json output/<vendor>/<date> --engine playwright
   ```
   （`$SKILL_DIR` = 本 skill 目录；首次缺依赖先 `npm i playwright && npx playwright install --with-deps chromium`）
8. **更新展示页指针与索引**（所有厂商处理完后执行一次）：调 `python "$SKILL_DIR/run.py" --reindex`，
   它按实际生成的 *.jpg 重建各厂商 `output/<vendor>/latest.json` + 汇总 `output/index.json`，
   不要手拼这两个文件。
9. **提交并推送**（触发 GitHub Pages 重新发布）：若本次有任意厂商产出新内容：
   ```bash
   git add -A data output && git commit -m "daily: <DATE>"
   ```
   **一次提交涵盖所有厂商；commit 格式必须是 `daily: YYYY-MM-DD`**（auto-merge guard 的
   正则依赖此标记，写成 `daily: <vendor> <date>` 会被整支跳过）。推送遵循仓库根目录
   CLAUDE.md 与下文「推送策略（routine 必读）」：云端只推当前工作分支（`claude/*`），
   本机会话可直推 main。所有厂商今天都无新内容则不提交、直接结束。
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

  **推送策略（routine 必读）**：Claude Code on the web 的 GitHub 代理只允许推当前工作分支，
  直推 main 会得到 403——这是预期行为，**不要把 403 当失败重试，也不要尝试推 main**。
  routine 只需把 `daily: YYYY-MM-DD` 提交推到自己的工作分支（`claude/*`），
  `.github/workflows/auto-merge-daily.yml` 会在分支只含 `data/`+`output/` 改动时自动合并入 main
  并删除分支。**代码 / 文档 / 配置改动不要混进每日内容分支**——guard 会整支跳过；
  这类改动请单独开分支提 PR 人工合并（纯文档推送不会触发 workflow，混推会滞留在分支上流失）。

  一条命令搞定「合并分支 + 各厂商建草稿」：

  ```bash
  scripts/watch-and-publish.sh --dry-run   # 演练：照常合并 daily 分支，但微信只打印结构不碰 API
  scripts/watch-and-publish.sh             # 合并 daily-* → main → 为当天每个厂商建微信贴图草稿
  VENDORS_PUBLISH="anthropic openai" scripts/watch-and-publish.sh   # 只给指定厂商发微信
  ```

  它做三件事：① `git fetch`，把未合并的 `origin/daily-<DATE>` 用 `-X theirs` 合并进 main、
  `run.py --reindex` 重建指针、push main、删远端分支；② 对每个有当天 `data/<vendor>/<DATE>.json`
  的厂商跑 `publish_wechat_newspic.py --vendor <id>` 建**贴图(newspic)**草稿；③ `.last_published.<vendor>`
  去重（每家每天只成功一次）。凭据 `~/.config/wechat-official-draft/config.yaml`，本机公网 IP 须在
  公众号 IP 白名单，且需已认证服务号。

  - 单厂商手动发：`scripts/publish-local.sh [--vendor <id>]`（只发不合并）。
  - 图文文章形态（可选）：`to_wechat_md.py [--vendor <id>]` → `push_draft.mjs`。

  每日自动：`scripts/launchd-publish.plist`（LaunchAgent，每天 07:15/07:45/08:30 跑 `watch-and-publish.sh`，
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
6. **云端定时无需改**：CCR 每日 routine 与 `daily.yml` 都自适应——跑 `run.py --vendors` 读出厂商清单
   再遍历；只要新厂商在 `curator.py` `VENDOR_META` + `sources.yaml` 登记好即可被自动带上。

展示页 Tab 的**显示名与顺序**也自动派生（名字取 `cards.js` 的 `VENDORS.name`、顺序按其定义序）；
只有上面第 4 步的**颜色**需手加。`run.py --vendors` 可本地自测厂商清单与各家源 URL。
