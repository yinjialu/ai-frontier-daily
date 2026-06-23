# 换台 Mac 安装「AI 前哨」本机发布链路

> 面向 AI agent / 人类操作者的可执行安装说明。目标：在一台**裸机 mac** 上把
> 每日 07:15 / 07:45 / 08:30 自动跑的微信公众号发布定时任务（launchd）装起来。
>
> 背景：云端 GitHub 代理只能推 `daily-*` 分支、推不了 main，所以「合并入 main + 微信发布」
> 这步必须在一台有完整 push 权与公众号凭据的本机上跑。本文件说明如何复刻这台本机。

## TL;DR（已满足前置时）

```bash
git clone git@github.com:yinjialu/ai-frontier-daily.git ~/ai-frontier-daily
cd ~/ai-frontier-daily
python3 -m pip install -r requirements.txt          # 或 uv pip install -r requirements.txt
# 建凭据（见下方第 3 步），然后：
scripts/install-launchd.sh
```

装完 `launchctl kickstart -k gui/$(id -u)/com.yinjialu.ai-frontier-daily.publish` 立即试跑一次。

---

## 配置资产清单：什么在仓库、什么在本机

| 资产 | 位置 | 进 git？ | 换机如何获得 |
|---|---|---|---|
| launchd plist | `scripts/launchd-publish.plist` | ✅ 已跟踪 | 随仓库克隆，`install-launchd.sh` symlink 进 `~/Library/LaunchAgents/` |
| 发布主脚本 | `scripts/watch-and-publish.sh` | ✅ | 随仓库 |
| 通知脚本 | `scripts/notify.sh` | ✅ | 随仓库 |
| Python 依赖 | `requirements.txt` | ✅ | `pip install -r` |
| 安装脚本 | `scripts/install-launchd.sh` | ✅ | 随仓库 |
| 微信凭据 | `~/.config/wechat-official-draft/config.yaml` | ❌ 私密 | 从 `scripts/config-templates/` 复制填写 |
| 推送渠道 key | `~/.config/ai-frontier-daily/notify.env` | ❌ 私密 | 从 `scripts/config-templates/` 复制填写（可选） |
| 小红书登录态 | `~/.config/xiaohongshu-mcp/` | ❌ 私密 | 仅当启用 XHS（默认暂停）才需要 |
| 发布去重标记 | `.last_published.*` | ❌（gitignore） | 自动生成，无需迁移 |

---

## 前置条件

1. **仓库必须克隆到 `~/ai-frontier-daily`** —— plist 里 `exec` 路径硬编码 `$HOME/ai-frontier-daily`。
   装到别处需手改 `scripts/launchd-publish.plist`（见末尾「已知 TODO」）。
2. **Python 3 + 依赖**：`pip install -r requirements.txt`（feedparser / requests / pyyaml）。
3. **git push 权限**：本机能直推 main（SSH key 已加 GitHub）。若网络掐 22 端口，
   `~/.ssh/config` 把 github.com 走 `ssh.github.com:443`。
4. **微信凭据 + IP 白名单**（见第 3 步）。

---

## 分步安装

### 1. 克隆 + 依赖

```bash
git clone git@github.com:yinjialu/ai-frontier-daily.git ~/ai-frontier-daily
cd ~/ai-frontier-daily
python3 -m pip install -r requirements.txt
```

### 2. 校验发布脚本能跑（dry-run，不碰任何发布 API）

```bash
scripts/watch-and-publish.sh --dry-run
```

### 3. 建本机私密凭据

**微信公众号**（不配则公众号发布失败）：

```bash
mkdir -p ~/.config/wechat-official-draft
cp scripts/config-templates/wechat-official-draft.config.yaml.example \
   ~/.config/wechat-official-draft/config.yaml
chmod 600 ~/.config/wechat-official-draft/config.yaml
# 编辑填入 appid / secret
```

> ⚠ 两个硬性前置，否则报错 40164 / IP 不在白名单：
> 1. 必须是**已认证服务号**（订阅号无草稿/素材 API）。
> 2. 本机**公网出口 IP** 必须加入公众号后台「IP 白名单」。
>    查出口：`curl -s https://api.ipify.org`。本机走 TUN 全局代理时出口会轮换，
>    需把代理出口段都加白名单或固定出口。

**手机推送**（可选，不配则退回 macOS 桌面通知）：

```bash
mkdir -p ~/.config/ai-frontier-daily
cp scripts/config-templates/notify.env.example ~/.config/ai-frontier-daily/notify.env
# 取消注释填入 BARK_KEY / SERVERCHAN_SENDKEY / NOTIFY_WEBHOOK 任一
```

### 4. 安装 launchd 任务

```bash
scripts/install-launchd.sh
```

脚本会：校验仓库路径与 Python 依赖 → 检查凭据（缺失只告警）→ 把 plist symlink 进
`~/Library/LaunchAgents/` → `launchctl bootstrap` 加载 → 校验已注册。幂等，可重复运行。

### 5. 验证

```bash
# 确认已注册（LastExitStatus 应为 0）
launchctl list com.yinjialu.ai-frontier-daily.publish

# 立即手动触发一次，不必等到早上
launchctl kickstart -k gui/$(id -u)/com.yinjialu.ai-frontier-daily.publish

# 看日志
tail -f ~/Library/Logs/ai-frontier-daily-publish.log
```

日志结尾出现 `✓ watch-and-publish 完成（YYYY-MM-DD）` 即成功。

---

## 卸载

```bash
scripts/install-launchd.sh --uninstall
```

---

## 故障排查

| 症状 | 原因 / 处理 |
|---|---|
| 公众号发布失败、日志含 40164 | 本机出口 IP 不在公众号 IP 白名单。`curl -s https://api.ipify.org` 查出口并加白名单 |
| `import feedparser` 报错 | 没装依赖：`pip install -r requirements.txt` |
| `install-launchd.sh` 报「仓库不在 ~/ai-frontier-daily」 | 把仓库移到该路径，或手改 plist 的 exec 路径 |
| git push 403 / 连接被断 | 22 端口被掐，改 `ssh.github.com:443`；代理出口轮换见仓库 memory |
| launchd 未触发 | `launchctl list` 看是否注册；macOS「登录项 / 后台」里确认未被禁用 |

---

## 已知 TODO（可移植性遗留，本次未改）

- **`scripts/watch-and-publish.sh:22` 硬编码本机路径**：
  `export PATH="/Users/jialu/anaconda3/bin:$PATH:/opt/homebrew/bin:$HOME/.nvm/versions/node/v24.13.0/bin"`
  —— anaconda3 绝对路径、node 版本号 `v24.13.0` 都是本机专属，换机若路径不同会失效。
  应改为自动探测（如 `command -v python3`、`brew --prefix`、`$NVM_DIR` 下取当前版本）。
- **plist 硬编码 `$HOME/ai-frontier-daily`**：仓库只能克隆在此路径，否则需手改 plist。
  可改为安装时由 `install-launchd.sh` 用实际 `$REPO` 渲染 plist 模板。
