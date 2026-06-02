# 新增一个厂商（vendor）Runbook

把一个 AI 大厂接进来 = 一条独立轨道。照下面 8 步走，全程改动**集中在 4 个文件 + 1 个 CI**，
其余（渲染器 render.js、展示页 index.html 主体、各发布脚本主体）厂商无关、无需动。
本文以加 OpenAI 的真实过程提炼；加 Gemini / 英伟达照搬即可（文末附两者候选配置）。

> 约定：`<id>` = 厂商小写英文 id（`openai`/`gemini`/`nvidia`…），全流程用 `--vendor <id>` 串联。
> 数据/产物落在 `data/<id>/<date>.json`、`output/<id>/<date>/*.jpg`、`output/<id>/latest.json`。

---

## Step 0 · 调研信息源（最关键，决定能不能无人值守）

目标：尽量找到**官方 RSS/Atom**（`feedparser` 能直接解析 → CI 无人值守不依赖 RSSHub）。
优先级：官方 RSS > GitHub `releases.atom` > SSR 页面（WebFetch 可抓）> RSSHub 镜像 > WebSearch 兜底。

逐项**实测**（别凭记忆写 URL）：

```bash
# RSS 是否存在（试常见路径：/rss.xml /feed /blog/rss.xml /news/rss.xml）
curl -sI "https://<官网>/news/rss.xml" | head -1
# GitHub releases.atom（SDK / CLI 仓库）
curl -sI "https://github.com/<org>/<repo>/releases.atom" | head -1
# 官网 news 页能否被 WebFetch 抓（很多是 JS 渲染或 403）—— 用 WebFetch 工具试
```

常见坑（OpenAI 实测）：
- 官网 `…/news/` 网页常 **JS 渲染或返回 403**，但同站 `…/news/rss.xml` 可用 → **优先 RSS，别直抓网页**。
- help center 类页面（release notes）多 403 → 需自建 RSSHub 或日常用 WebSearch 补。
- 产出一张表：名称 / URL / 类型(官方RSS·Atom·需WebFetch·RSSHub) / 是否官方 / 可靠性 / limit。

> 提示：可直接派一个子 agent 做这步（“调研 <厂商> 可订阅信息源，逐个 WebFetch/curl 实测”），
> 像 OpenAI 那次一样产出可粘贴的 YAML 片段。

---

## Step 1 · `sources.yaml`：加 `vendors.<id>`

```yaml
  <id>:
    rss:
      - name: <厂商> News
        url: https://<官方 rss>
        limit: 10
      - name: <厂商> SDK Releases
        url: https://github.com/<org>/<repo>/releases.atom
        limit: 10
    webfetch:                 # 无 RSS 但 SSR 可抓的页面（日常 Claude 驱动补充用）
      - name: <厂商> API Changelog
        url: https://<changelog url>
```

---

## Step 2 · `cards.js`：在 `VENDORS` 注册表加一项

```js
<id>: {id:"<id>", name:"<厂商>", daily:"<厂商> Daily", label:"<厂商大写> DAILY"},
```

- `name` → 封面标题「今天 <name> 又更新了什么」、公众号封面「<name> 今日速递」。
- `daily` → 封面 kicker；`label` → 内容卡眉头 / 公众号封面角标（建议全大写）。
- 展示页 `index.html` 的 Tab 显示名**自动**从这里派生，无需另改。

---

## Step 3 · `cards.css`：加 `.v-<id>` 主题块

卡片只引用语义 token，换肤=覆盖这些 token。复制下面整块改配色即可：

```css
/* ===== <厂商> 主题 ===== */
.v-<id>{
  --bg:#......; --bg-2:#......; --fg:#......; --muted:#......; --line:#......;
  --accent:#......; --accent-deep:#......; --accent-soft:#......;
  --feature-bg:#......; --feature-fg:#......; --feature-muted:#......;
}
/* 深底主题需要这行（浅底主题删掉）：噪点改 screen，否则糊成黑块 */
.v-<id>.card::after{mix-blend-mode:screen;opacity:.06}
```

配色指南（**第一原则：优先对齐该厂商的品牌主题色,再考虑与其它厂商区分**）：
- **先定品牌主色**：取厂商官方视觉的标志色做 `--accent`（深/中/浅三档 `--accent-deep/-/-soft`）。
  例：Anthropic 暖陶土 #C1572E + 米白；OpenAI 黑底 + ChatGPT 青绿 #10A37F；
  Gemini 蓝→紫渐变（蓝 #4F7CF7 + 紫 #A78BFA）;NVIDIA 黑底 + 标志绿 #76B900。
  底色(`--bg`)也尽量贴品牌气质：品牌偏深则深底、偏亮则浅底。
- **再保证区分**：若新厂商主色与已有某家太接近,微调明度/色相或换深浅底,确保四家一眼可分
  （已有：暖陶土浅底 / 黑底青绿 / 冷调浅底蓝紫 / 黑底绿）。版式/纸感/衬线标题始终保持一致,只换色。
- `--feature-bg` 比 `--bg` 再深/再浅一档做封面与结尾的「特写面」。
- **深底主题**（OpenAI/NVIDIA 式）：`--bg` 近黑、`--fg` 近白,并保留上面的 `.v-<id>.card::after{screen}` 那行。
- **浅底主题**（Anthropic/Gemini 式）：`--bg` 浅、`--fg` 近黑,删掉 `screen` 那行（默认 multiply 即可）。

---

## Step 4 · `curator.py`：在 `VENDOR_META` 加品牌文案

```python
"<id>": {"name": "<厂商>", "brand": "AI 前哨 · 每日 <厂商>",
         "outroDesc": "持续追踪 <厂商> 官方发布、……。点个关注，明天见。"},
```

system prompt（中文策展指令）会自动按 `name` 套用，无需另写。

---

## Step 5 · 发布脚本：补显示名 / 标签（3 处，半自动发布才需要）

- `to_xhs_post.py` → `VENDOR_META`：加 `{"name": "...", "tags": "#AI #<厂商> #<产品>"}`（小红书标签≤3）。
- `to_wechat_md.py` → `VENDOR_NAME`：加 `"<id>": "<厂商>"`。
- `publish_wechat_newspic.py` → `VENDOR_NAME`：加 `"<id>": "<厂商>"`。

> 这三处是发布配文/标签的厂商名，纯文字。不发对应平台可暂时不加。

---

## Step 6 · 产出第一期（Claude 驱动路径，无需 API key）

日常/首发推荐这条：由 Claude 亲自抓+策展（`run.py --live` 那条要 `ANTHROPIC_API_KEY`，CI 才有）。

1. **抓**：用 `WebFetch` 拉 Step 0 选定的源（RSS 优先），必要时 `WebSearch` 补细节。
2. **策展**：筛对中文从业者有价值的（模型发布/能力/研究/合作/定价政策），每条选标签
   【模型发布/开发者/企业/研究/生态/政策/安全】+ 写 50–80 字客观中文摘要，按重要性降序，≤6 条。
3. **写数据** `data/<id>/<date>.json`（**必须含 `"vendor":"<id>"`**），schema 见 SKILL.md。
4. **渲染**：
   ```bash
   node "$SKILL_DIR/render.js" data/<id>/<date>.json output/<id>/<date> --engine playwright
   ```
5. **重建索引**：`python "$SKILL_DIR/run.py" --reindex`（生成 `output/<id>/latest.json` + 汇总 `output/index.json`）。

---

## Step 7 · 验证（照搬本次用过的命令）

```bash
# a) 看几张渲染图：封面 / 一张内容卡 / 结尾，确认主题色与文案对
#    （Read output/<id>/<date>/小红书_00_封面.jpg 等）

# b) 确认 Anthropic 没被改坏：把某天用新 CSS 重渲到临时目录再肉眼比对
node skills/ai-daily-digest/render.js data/anthropic/<某天>.json /tmp/chk --engine playwright --only 0

# c) 隔离烟测整条 Python 管线（不碰真实数据）
DIGEST_OUT=/tmp/smoke python3 skills/ai-daily-digest/run.py --vendor <id> --force
python3 -c "import json;d=json.load(open('/tmp/smoke/output/index.json'));print(d['vendors'])"

# d) 展示页：本地起服务器，浏览器或 playwright 验证 Tab 切换
python3 -m http.server 8000   # 打开 http://localhost:8000/index.html
```

页面检查点：顶部出现新 Tab；切过去页面 accent / 热力图换色、卡片轮播是新主题；切回 Anthropic 恢复原样；无 console 报错。

---

## Step 8 · CI（`.github/workflows/daily.yml`）加一条轨道

在已有 anthropic / openai 后面加：

```yaml
      - name: Run pipeline (live · <id>)
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          DIGEST_OUT: ${{ github.workspace }}
        run: python skills/ai-daily-digest/run.py --live --vendor <id> --engine playwright
```

（commit & push 那步不用改，`git add -A data output` 已覆盖所有厂商。）

---

## 改动清单（一眼核对，别漏）

| 文件 | 改什么 |
|---|---|
| `sources.yaml` | `vendors.<id>` 的 rss/webfetch |
| `cards.js` | `VENDORS` 加一项（驱动文案 + 展示页 Tab 名） |
| `cards.css` | `.v-<id>` 主题块（+ 深底加 screen 行） |
| `curator.py` | `VENDOR_META` 品牌/结尾文案 |
| `to_xhs_post.py` / `to_wechat_md.py` / `publish_wechat_newspic.py` | 显示名/标签（仅发布才需） |
| `.github/workflows/daily.yml` | 加一条 `--vendor <id>` 步骤 |
| `index.html` | **无需改**（Tab 名从 cards.js 派生） |
| `render.js` | **无需改** |

---

## 附录 · Gemini / 英伟达候选配置（URL 与配色均**需先实测**再落地）

> 下面是起点，不是结论。务必先按 Step 0 用 `curl -sI` / WebFetch 验证每个 URL，再写进 `sources.yaml`。

### Gemini（Google）`id: gemini`
- 候选源（待核实）：Google Keyword 博客 / DeepMind 博客 RSS；`ai.google.dev` 的 API changelog（多为 SSR/无 RSS，WebFetch 抓）；
  GitHub `googleapis/python-genai`、`google-gemini/generative-ai-*` 的 `releases.atom`。
- 主题方向：Gemini 蓝紫渐变 → 浅底 + 蓝紫 accent（`--accent` 取 `#4F7CF7` 一档蓝，`--accent-soft` 偏紫 `#A78BFA`）；
  浅底主题，删掉 `screen` 那行。标签 `#AI #Gemini #Google`。

### 英伟达（NVIDIA）`id: nvidia`
- 候选源（待核实）：NVIDIA 博客 `blogs.nvidia.com/feed/`；NVIDIA Developer 博客 RSS；
  Newsroom `nvidianews.nvidia.com` 的 RSS；相关 GitHub 仓库 `releases.atom`。
- 主题方向：NVIDIA 经典「黑底 + 荧光绿 #76B900」→ 深底主题（`--bg` 近黑、`--accent` `#76B900`、`--accent-soft` `#A4D65E`），
  保留 `screen` 那行。标签 `#AI #NVIDIA #GPU`。
