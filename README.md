# 每日 Anthropic 动态 · 自动素材仓库

存储抓取到的 Anthropic 官方动态（`data/`），渲染成小红书/公众号卡片（`output/`），
用 GitHub Pages 当移动端审核页展示，GitHub Actions 每天自动更新。

## 一次性上线（在你本机，需已装 gh 并登录）

```bash
cd anthropic-daily-repo                    # 进入本仓库目录

# 仓库已初始化好；如未初始化则先：git init -b main && git add -A && git commit -m init

# 1) 创建 GitHub 仓库并推送（Pages 免费版需 public）
gh repo create anthropic-daily --public --source=. --remote=origin --push

# 2) 开启 Pages：从 main 分支根目录部署
#    （命令式，OWNER 换成你的用户名；失败就用下面的网页方式）
gh api -X POST repos/$(gh api user -q .login)/anthropic-daily/pages \
  -f "source[branch]=main" -f "source[path]=/" || \
  echo "→ 改用网页：Settings → Pages → Source 选 Deploy from a branch → main / (root)"

# 3) 配置 Actions 密钥（真实模式调 Claude 用；切勿写进代码）
gh secret set ANTHROPIC_API_KEY --body "sk-ant-你的key"

# 4) 立即跑一次真实抓取（也可等每天 09:00 自动跑）
gh workflow run daily-anthropic-watch.yml
```

上线后审核页地址：`https://<你的用户名>.github.io/anthropic-daily/`
手机打开即可审核当天卡片；通过后下载图片手动发小红书 / 手动建公众号草稿。

## 它如何运转

- `.github/workflows/daily.yml`：每天北京时间 09:00（或手动触发）跑 `run.py --live`，
  抓 `sources.yaml` 的 RSS → 去重 → 调 Claude 摘要 → Playwright 渲染卡片 →
  把 `data/` 与 `output/` 提交回仓库。
- GitHub Pages「从分支部署」：仓库一有新提交就自动重新发布，`index.html` 读取
  `output/latest.json` 展示当天卡片。无需额外部署步骤。
- 去重状态 `seen.db` 不提交（.gitignore），每个 runner 是干净环境，
  因此用 `data/` 里已存在的日期做幂等：同一天重复触发不会重复产出。

## 安全

- `ANTHROPIC_API_KEY` 只放 Actions Secrets，**绝不进仓库**。
- 仓库为 public，里面只放反正要公开发布的卡片与摘要；不要放任何密钥或私密内容。
- 发布永远人工完成最后一步（见下）。

## 发布（人工，符合平台规则）

- 小红书：无合规发布 API，下载竖图手动发笔记。
- 公众号（个人订阅号）：2025 年 7 月起个人主体账号发布/草稿接口权限被回收，
  直连 `draft/add` 返回 48001。改为手动建草稿贴图，或用 135/壹伴等已授权编辑器导入草稿箱。

## 本地预览 / 调试

```bash
pip install -r requirements.txt
python run.py                 # mock，无需联网/密钥
python -m http.server 8000    # 打开 http://localhost:8000/index.html
```
