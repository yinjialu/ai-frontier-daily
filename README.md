# AI 前哨 · 每日 AI 大厂动态

抓取 AI 大厂官方动态（当前 **Anthropic**，后续可扩展 OpenAI 等）→ 中文策展 →
渲染小红书 / 公众号卡片 → GitHub Pages 当移动端审核页展示 → GitHub Actions 每天自动更新。

整条流程封装为可安装的 **Agent Skill**：[`skills/ai-daily-digest`](skills/ai-daily-digest/SKILL.md)。

## 在线审核页（GitHub Pages）

`https://<你的用户名>.github.io/ai-frontier-daily/`

手机打开即可审核当天卡片：小红书 6 张竖图直接发笔记；公众号封面 + 正文长图手动建草稿。

## 安装这个 Skill

```bash
# 装到当前项目
npx skills add yinjialu/ai-frontier-daily

# 或装到全局（所有项目可用）
npx skills add yinjialu/ai-frontier-daily --skill ai-daily-digest -g -a claude-code -y
```

安装后在 Claude Code 里说「做今天的 Anthropic 动态卡片」「更新每日 AI 速递」即可触发。
Skill 用法详见 [`skills/ai-daily-digest/SKILL.md`](skills/ai-daily-digest/SKILL.md)。

## 它如何运转

- **Claude 驱动**（交互 / 定时 routine）：Claude 用 web 工具抓真实动态 → 中文策展 →
  `node render.js` 渲染 → 提交触发 Pages → `PushNotification` 推手机。
- **无人值守**（`.github/workflows/daily.yml`，每天北京时间 09:00 或手动触发）：
  跑 `skills/ai-daily-digest/run.py --live`，抓 RSS → 去重 → 调 Claude 摘要 →
  Playwright 渲染 → 提交 `data/` 与 `output/` 回仓库。
- GitHub Pages「从分支部署」：仓库一有新提交就自动重新发布，`index.html` 读
  `output/latest.json` 展示当天卡片。

## 一次性上线（本机，需已装 gh 并登录）

```bash
gh repo create ai-frontier-daily --public --source=. --remote=origin --push

# 开启 Pages：从 main 分支根目录部署
gh api -X POST repos/$(gh api user -q .login)/ai-frontier-daily/pages \
  -f "source[branch]=main" -f "source[path]=/" || \
  echo "→ 改用网页：Settings → Pages → Deploy from a branch → main / (root)"

# 配置 Actions 密钥（live 模式调 Claude 用；切勿写进代码）
gh secret set ANTHROPIC_API_KEY --body "sk-ant-你的key"

# 立即跑一次真实抓取（也可等每天 09:00 自动跑）
gh workflow run daily-anthropic-watch
```

## 本地预览 / 调试

```bash
pip install -r skills/ai-daily-digest/requirements.txt
npm i playwright && npx playwright install chromium
python skills/ai-daily-digest/run.py                 # mock，无需联网/密钥
python -m http.server 8000                            # 打开 http://localhost:8000/index.html
```
`data/` 与 `output/` 默认写到当前目录（可用环境变量 `DIGEST_OUT` 指定）。

## 安全

- `ANTHROPIC_API_KEY` 只放 Actions Secrets，**绝不进仓库**。
- 仓库 public，只放反正要公开发布的卡片与摘要；不要放任何密钥或私密内容。
- 发布到小红书 / 公众号的最后一步永远人工完成（符合平台规则）。
