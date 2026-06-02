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

## A. Claude 驱动（推荐）

在仓库根目录执行以下步骤（`output/`、`data/` 写到当前工作目录）：

1. **抓取真实最新动态**（先确定 `<vendor>`）。
   - **Anthropic**：用 `WebFetch` 拉 `https://www.anthropic.com/news` 取顶部最新条目
     （标题 + 日期 + 分类），必要时 `WebSearch` 补充细节。主站 JS 渲染、无官方 RSS。
   - **OpenAI**：有官方 RSS，直接 `WebFetch` 拉 `https://openai.com/news/rss.xml`
     （`openai.com/news` 网页本身对 WebFetch 返回 403，用 RSS 代替）；API/Codex 细节可补抓
     `https://developers.openai.com/api/docs/changelog`。
   - 各厂商的源都登记在 `sources.yaml` 的 `vendors.<vendor>` 下。
2. **价值筛选 + 中文策展**。只保留对中文 AI 从业者有价值的条目（模型发布、能力
   更新、重要研究、重大合作、定价/政策），过滤纯招聘/办公室开设/人事任命等。
   每条：选一个标签【模型发布/开发者/企业/研究/生态/政策/安全】，写 50–80 字
   客观中文摘要（说清「变了什么 + 对用户意味着什么」，不夸张不编造），按重要性
   降序，最多 6 条。
3. **写当天数据**到 `data/<vendor>/<YYYY-MM-DD>.json`（必含 `"vendor"` 字段），字段见下面 schema。
   渲染默认输出 **JPEG**（移动端优先：1080×1440、`deviceScaleFactor:1`、质量 86，
   单张约 100–300KB，低于公众号在文图片 1MB 上限，省去后压缩）。可用环境变量
   `CARD_FORMAT=png|jpeg`、`CARD_QUALITY`、`CARD_SCALE` 覆盖。
4. **渲染卡片**：
   ```bash
   node "$SKILL_DIR/render.js" data/<vendor>/<date>.json output/<vendor>/<date> --engine playwright
   ```
   （`$SKILL_DIR` = 本 skill 目录；首次需 `npm i playwright && npx playwright install chromium`）
5. **更新展示页指针与索引**：直接调 `python "$SKILL_DIR/run.py" --reindex`，
   它扫描 `data/*/*.json` 重建各厂商 `output/<vendor>/latest.json` + 汇总 `output/index.json`（jpg 感知）。
6. **提交并推送**（触发 GitHub Pages 重新发布）：
   ```bash
   git add -A data output && git commit -m "daily: <vendor> <date>" && git push
   ```
7. **推送移动端**：用 `PushNotification` 发一条「今日卡片已生成 · 查看：
   https://<user>.github.io/<repo>/」，用户手机上打开展示页查看卡片。

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
`vendor` 取 `anthropic`|`openai`（缺省按 anthropic）。`edition` 用年内第几天（`date +%j`）。
今天无值得发的内容则不发卡片。

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
```

- 去重 `seen.db`（SQLite，指纹按 `vendor|归一化标题`）写到 `DIGEST_OUT`，各厂商互不干扰，每天只推增量。
- live 摘要在 `curator.py` 调 Claude API（system prompt 随 vendor 切换）；mock 用离线启发式。
- CI（`.github/workflows/daily.yml`）每天先后跑 anthropic、openai 两轨，再一次性提交。

## 文件结构

```
skills/ai-daily-digest/
  SKILL.md          # 本文件
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

- 小红书：无合规发布 API。本机有 `xhs-publisher` skill（浏览器 UI 自动化驱动
  creator.xiaohongshu.com，需已登录 Chrome + Claude 驱动，且按平台规范【人工点发布】，
  无法像公众号那样无人值守 cron）。`to_xhs_post.py` 把 data 整理成发布素材包：
  `python to_xhs_post.py [--vendor openai]` → 写 `output/<vendor>/<date>/小红书文案.txt`
  （标题≤20/正文/标签/配图清单）并打印 JSON（date/vendor/title/content/tags/images），
  标签随厂商切换（Anthropic `#AI #Anthropic #Claude`／OpenAI `#AI #OpenAI #ChatGPT`），
  供 xhs-publisher 上传当天 6–8 张竖图时直接套用。

  **小红书半自动发布（Claude + Chrome，用户说「发今天的小红书」时走这套）：**
  1. `git pull` 取云端最新，`python to_xhs_post.py [--vendor <id>]` 生成素材包（读其 stdout 的
     JSON：title/content/tags/images）。
  2. 用 Claude-in-Chrome 打开 `https://creator.xiaohongshu.com/publish/publish?target=image`，
     点「上传图片」（红色按钮），按 images 顺序（小红书_00 封面 → 99 结尾）上传当天竖图。
     页面 DOM 选择器与逐步操作参考 `xhs-publisher` skill（已软链到 ~/.claude/skills/）。
  3. 填标题（title，≤20 字）、正文（content）；正文末尾空两行后接 tags（随厂商，见 stdout 的 `tags`）。
  4. **停在「发布」按钮前**，截图给用户确认，由用户手动点发布（平台反自动化规范，切勿自动发）。
- 公众号个人订阅号：草稿接口权限已回收，手动建草稿贴图，或用 135/壹伴等已授权
  编辑器导入草稿箱。
- 公众号【已认证服务号】——「云端抓取 → 本机推送」半自动链路（仍由人工群发）：

  云端（北京 07:00 routine）只负责抓取+渲染+提交；推送草稿在本机完成。

  ```bash
  scripts/publish-local.sh --dry-run                 # 打印将提交的结构，不碰 API（anthropic）
  scripts/publish-local.sh                           # 拉取云端最新 → 创建贴图草稿（anthropic）
  scripts/publish-local.sh --vendor openai           # 指定厂商
  ```

  **默认形态＝贴图（newspic / 图片消息）**：`git pull` → `publish_wechat_newspic.py [--vendor <id>]`
  把当天小红书整套卡片传为永久素材 → `draft/add(article_type=newspic, image_info)` 建贴图
  草稿（公众号原生图片帖，更贴合卡片）→ `.last_published.<vendor>` 去重 → 系统通知。配文由结构化
  数据自动生成（标题 + 每条摘要，随 vendor 切换品牌）。凭据 `~/.config/wechat-official-draft/config.yaml`，
  本机公网 IP 须在公众号 IP 白名单，且需已认证服务号。

  另一形态（可选，手动）＝图文文章（news，内嵌同一套图）：
  `to_wechat_md.py [--vendor <id>]` → `wechat-official-draft/scripts/push_draft.mjs --file .. --cover ..`。

  每日自动：`scripts/launchd-publish.plist`（LaunchAgent，每天 07:30 + 08:30 跑上面的脚本）。
  安装：`cp scripts/launchd-publish.plist ~/Library/LaunchAgents/ && launchctl load -w
  ~/Library/LaunchAgents/com.yinjialu.ai-frontier-daily.publish.plist`。
  （如需同时自动推 OpenAI 公众号，在 plist 里加一条 `--vendor openai` 的调用即可。）

## 扩展到更多厂商

加一个厂商通常只需四处改动（均无需动渲染器）：
1. `sources.yaml`：在 `vendors.<新id>` 下加 `rss`/`webfetch` 源。
2. `cards.js`：在 `VENDORS` 注册表加一项（name/daily/label）。
3. `cards.css`：加一个 `.v-<新id>` 主题块覆盖语义 token（配色）。
4. `curator.py`：在 `VENDOR_META` 加品牌名/brand/结尾文案；发布脚本的 `VENDOR_NAME`/标签按需补。
然后展示页 `index.html` 会自动从 `output/index.json` 读出新厂商并加 Tab（`VENDOR_NAMES`
里补个显示名即可）。
