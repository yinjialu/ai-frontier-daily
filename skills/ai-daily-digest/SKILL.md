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

抓取 AI 大厂（当前 Anthropic，后续可扩展 OpenAI 等）官方动态 → 中文策展 → 渲染
小红书 / 公众号卡片 → 更新 GitHub Pages 审核页 → 推送移动端通知。发布到平台的
最后一步由人工完成（符合各平台规则）。

## 两种运行方式

| 方式 | 适用 | 摘要来源 |
| --- | --- | --- |
| **A. Claude 驱动**（推荐给 routine / 交互） | Claude Code / 定时 agent | 由 Claude 直接用 web 工具抓取并策展，质量最高 |
| **B. 纯 Python**（GitHub Actions 无人值守） | CI | `run.py --live`：抓 RSS + 调 Claude API |

两种方式产出同一套 `data/<date>.json` 与 `output/<date>/*.png`，由同一渲染器
（`render.js` + `cards.js` + `cards.css`，唯一真源）渲染，风格一致。

## A. Claude 驱动（推荐）

在仓库根目录执行以下步骤（`output/`、`data/` 写到当前工作目录）：

1. **抓取真实最新动态**。用 `WebFetch` 拉 `https://www.anthropic.com/news`
   取顶部最新条目（标题 + 日期 + 分类），必要时 `WebSearch` 补充细节。也可读
   `sources.yaml` 里的 RSS。
2. **价值筛选 + 中文策展**。只保留对中文 AI 从业者有价值的条目（模型发布、能力
   更新、重要研究、重大合作、定价/政策），过滤纯招聘/办公室开设/人事任命等。
   每条：选一个标签【模型发布/开发者/企业/研究/生态/政策/安全】，写 50–80 字
   客观中文摘要（说清「变了什么 + 对用户意味着什么」，不夸张不编造），按重要性
   降序，最多 6 条。
3. **写当天数据**到 `data/<YYYY-MM-DD>.json`，字段见下面 schema。
   渲染默认输出 **JPEG**（移动端优先：1080×1440、`deviceScaleFactor:1`、质量 86，
   单张约 100–300KB，低于公众号在文图片 1MB 上限，省去后压缩）。可用环境变量
   `CARD_FORMAT=png|jpeg`、`CARD_QUALITY`、`CARD_SCALE` 覆盖。
4. **渲染卡片**：
   ```bash
   node "$SKILL_DIR/render.js" data/<date>.json output/<date> --engine playwright
   ```
   （`$SKILL_DIR` = 本 skill 目录；首次需 `npm i playwright && npx playwright install chromium`）
5. **更新审核页指针** `output/latest.json`：`{date, cnDate, dir, files:[*.png 排序]}`。
6. **提交并推送**（触发 GitHub Pages 重新发布）：
   ```bash
   git add -A data output && git commit -m "daily: <date>" && git push
   ```
7. **推送移动端**：用 `PushNotification` 发一条「今日卡片已生成 · 审核：
   https://<user>.github.io/<repo>/」，用户手机上打开审核页查看卡片。

### data JSON schema

```json
{
  "date": "2026.05.31", "cnDate": "5月31日 周日",
  "edition": "VOL.151", "brand": "AI 前哨 · 每日 Anthropic",
  "updates": [
    {"tag": "模型发布", "title": "标题", "summary": "50-80字中文摘要", "source": "anthropic.com"}
  ],
  "outroTitle": "每天一条\n看懂 AI 大厂动向",
  "outroDesc": "…", "outroCta": "关注 · 不错过任何更新"
}
```
`edition` 用年内第几天（`date +%j`）。今天无值得发的内容则不发卡片。

## B. 纯 Python（无人值守 / CI）

```bash
pip install -r requirements.txt          # pyyaml feedparser
export DIGEST_OUT="$PWD"                  # data/ output/ 写到这里（默认即当前目录）
python run.py            # mock：用 fixtures，离线跑通，不需要 key
python run.py --live     # 真实：抓 sources.yaml 的 RSS + 调 Claude API（需 ANTHROPIC_API_KEY）
python run.py --force    # 忽略去重强制处理
python run.py --engine playwright   # 字体保真渲染（生产推荐）
```

- 去重 `seen.db`（SQLite，按归一化标题指纹）写到 `DIGEST_OUT`，保证每天只推增量。
- live 摘要在 `curator.py` 调 Claude API；mock 用离线启发式。

## 文件结构

```
skills/ai-daily-digest/
  SKILL.md          # 本文件
  run.py            # 编排：采集→去重→摘要→渲染→更新指针
  collector.py      # 采集（mock 读 fixtures / live 抓 RSS）
  curator.py        # 策展+摘要（mock 启发式 / live 调 Claude）
  dedup.py          # SQLite 去重
  render.js         # 渲染器（playwright / wkhtmltoimage）
  cards.js          # 卡片构建逻辑（浏览器与 Node 共用，唯一真源）
  cards.css         # 卡片样式
  sources.yaml      # 信息源（RSS）
  fixtures/         # mock 样例数据
```
仓库根目录的 `index.html`（审核页）读 `output/latest.json` 展示当天卡片，由
GitHub Pages 部署。

## 输出卡片

- 小红书 1080×1440：封面 + 每条一张内容卡（含 `01/06` 页码与水印序号）+ 结尾卡。
- 微信公众号：900×383 封面 + 正文长图（高度自适应）。

## 发布（人工，符合平台规则）

- 小红书：无合规发布 API。本机有 `xhs-publisher` skill（浏览器 UI 自动化驱动
  creator.xiaohongshu.com，需已登录 Chrome + Claude 驱动，且按平台规范【人工点发布】，
  无法像公众号那样无人值守 cron）。`to_xhs_post.py` 把 data 整理成发布素材包：
  `python to_xhs_post.py` → 写 `output/<date>/小红书文案.txt`（标题≤20/正文/标签/配图清单）
  并打印 JSON（title/content/tags/images），供 xhs-publisher 上传当天 6–8 张竖图时直接套用。

  **小红书半自动发布（Claude + Chrome，用户说「发今天的小红书」时走这套）：**
  1. `git pull` 取云端最新，`python to_xhs_post.py` 生成素材包（读其 stdout 的 JSON：
     title/content/tags/images）。
  2. 用 Claude-in-Chrome 打开 `https://creator.xiaohongshu.com/publish/publish?target=image`，
     点「上传图片」（红色按钮），按 images 顺序（小红书_00 封面 → 99 结尾）上传当天竖图。
     页面 DOM 选择器与逐步操作参考 `xhs-publisher` skill（已软链到 ~/.claude/skills/）。
  3. 填标题（title，≤20 字）、正文（content）；正文末尾空两行后接 tags（`#AI #Anthropic #Claude`）。
  4. **停在「发布」按钮前**，截图给用户确认，由用户手动点发布（平台反自动化规范，切勿自动发）。
- 公众号个人订阅号：草稿接口权限已回收，手动建草稿贴图，或用 135/壹伴等已授权
  编辑器导入草稿箱。
- 公众号【已认证服务号】——「云端抓取 → 本机推送」半自动链路（仍由人工群发）：

  云端（北京 07:00 routine）只负责抓取+渲染+提交；推送草稿在本机完成。

  ```bash
  scripts/publish-local.sh --dry-run   # 打印将提交的结构，不碰 API
  scripts/publish-local.sh             # 拉取云端最新 → 创建贴图草稿
  ```

  **默认形态＝贴图（newspic / 图片消息）**：`git pull` → `publish_wechat_newspic.py`
  把当天小红书整套卡片传为永久素材 → `draft/add(article_type=newspic, image_info)` 建贴图
  草稿（公众号原生图片帖，更贴合卡片）→ `.last_published` 去重 → 系统通知。配文由结构化
  数据自动生成（标题 + 每条摘要）。凭据 `~/.config/wechat-official-draft/config.yaml`，
  本机公网 IP 须在公众号 IP 白名单，且需已认证服务号。

  另一形态（可选，手动）＝图文文章（news，内嵌同一套图）：
  `to_wechat_md.py` → `wechat-official-draft/scripts/push_draft.mjs --file .. --cover ..`。

  每日自动：`scripts/launchd-publish.plist`（LaunchAgent，每天 07:30 + 08:30 跑上面的脚本）。
  安装：`cp scripts/launchd-publish.plist ~/Library/LaunchAgents/ && launchctl load -w
  ~/Library/LaunchAgents/com.yinjialu.ai-frontier-daily.publish.plist`。

## 扩展到更多厂商

在 `sources.yaml` 增加新厂商的 RSS，或在「Claude 驱动」第 1 步增加抓取的官网；
`brand`/封面文案可随厂商调整。卡片模板厂商无关，无需改渲染器。
