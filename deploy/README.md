# Hermes 服务器部署

此流水线把运行依赖移到现有 Hermes 容器的持久卷中。Hermes 提供调度、现有 Vertex ADC/模型和网页搜索；Python 负责采集、校验、SQLite 队列、投递回执，Playwright 复用项目原卡片渲染器。

## 用户已确定的运行方式

| 北京时间 | 行为 |
|---|---|
| 每 30 分钟 | 抓官方 RSS、公告列表及 RSSHub；仅重大且有原文/日期的新动态即时通知 |
| 07:30 | 用 Hermes 搜索逐家补充官方渠道，含国内 12 家及海外 7 家；二手结果只记线索 |
| 08:00 | 按过去 36 小时发现、官方发布在过去 72 小时内的有效候选，生成中文早报和卡片 ZIP，发飞书群 |
| 08:15 | 若早报尚无成功投递回执则重试；已成功则静默 |

日报是滚动窗口汇总，可能再次包含已发过的重大快讯；同一期内跨来源同事件合并。首次成功采集或订阅配置变更时建立静默基线，不补发历史。正文/日期不足的条目不能当作正式模型发布。图片与模型调用失败会保留队列与本期草稿以便重试。单源连续失败 3 次后群内告警；源状态不变时每天最多一次相同告警。

## 路径

- 容器项目：`/opt/data/workspace/ai-frontier-daily`
- 持久数据：项目下 `.server-state/`，含 SQLite、健康记录、搜索覆盖、各期图片/文案/ZIP
- Python 附加依赖：项目下 `.server-packages/`，不改 Hermes 的核心依赖
- Chromium：`/opt/data/cache/frontier-playwright`
- Cron 入口：`/opt/data/scripts/frontier_*.py`
- 私有群配置：`/opt/data/frontier-server.json`（0600）；不放进 Git

当前主 Hermes 使用 host 网络，所以可访问宿主的 `127.0.0.1:1200`。RSSHub 只绑定环回地址，512 MB 内存、0.5 CPU 限额；默认镜像固定到已验收 digest。无需 Redis/浏览器服务，当前 Qwen 路由不要求登录。RSSHub 仍可能因上游反爬或页面改版而失败；空 feed 视为异常，不视为无新闻。

## 安装

先把此版本代码复制/检出到上述持久目录，不复制本机密钥、`.env` 或私人草稿。RSSHub 在宿主使用 `docker compose -f deploy/rsshub-compose.yaml up -d`；已有同名实例时先检查，不重复启动。

在 Hermes 容器的项目目录执行：

```sh
uv pip install --target .server-packages -r deploy/server-requirements.txt
npm ci
PLAYWRIGHT_BROWSERS_PATH=/opt/data/cache/frontier-playwright npx playwright install --with-deps chromium
export PYTHONPATH="$PWD/.server-packages:/opt/hermes"
export PLAYWRIGHT_BROWSERS_PATH=/opt/data/cache/frontier-playwright
python -m scripts.server.worker baseline
python -m scripts.server.worker scout
python -m scripts.server.worker health
# 使用已经核对的目标群 ID，切勿靠同名猜测租户。
export FRONTIER_FEISHU_CHAT_ID=oc_REPLACE_WITH_VERIFIED_GROUP
python -m scripts.server.worker smoke --send
python deploy/install-hermes.py
hermes cron list
hermes cron status
```

安装器不改全局时区。当前 UTC 容器的 `0 0 * * *` 对应北京时间 08:00；Asia/Shanghai 容器使用 `0 8 * * *`。其他时区直接拒绝安装。后续修改 Hermes 时区必须重新检查 cron 表达式。安装器保留已存在同名任务，避免重复；改时间须显式 `hermes cron edit`。

Python/Node 包和浏览器均在持久卷内，普通重启不需要重新安装；替换 Hermes 镜像时重新运行依赖与渲染 smoke test，系统浏览器库属于容器镜像。不要为部署本项目重启或替换现有飞书机器人配置。

## 验证与发布边界

- `python -m pytest tests/test_server.py -q` 验证基线、增量去重、来源更换、HTML/空 RSS、防伪来源、日期语义、模型输出和失败投递重试。
- 必须实际验证 Vertex 请求、Feishu API 回执、Playwright 产图与 ZIP 上传。仅存在 cron 条目不代表未来运行已成功。
- `.server-state/research/<date>.json` 逐家记录真实搜索 query、官方候选及媒体线索；失败不能填 `none-found`。
- `.server-state/editions/<date>/coverage.json` 保存该期自动源与搜索状态；正文里明确未覆盖和失效源。
- 群内 ZIP 包含各轨道小红书 JPEG、公众号封面/长图和 Markdown 文案。正式社交平台发布由用户审核后手动操作。
- 服务器当前不更新旧 GitHub Pages 发布页，避免把待审核材料变成公开内容。原页面保留历史内容；不要把它的旧日期当作新产出。
- Feishu API UUID 与 SQLite 回执降低重复投递。API 幂等窗口并非永久；极端情况下远端已接收而本地回执未落盘、且跨越远端窗口重试，仍可能重复。不能声称端到端 exactly-once。

## 排查 / 回滚

`hermes cron runs` 查看运行与失败投递；用 `python -m scripts.server.worker health` 查看具体源。`worker` 的正常日志写 stderr；脚本成功且无消息时 stdout 为空，Hermes 保持静默。

暂停本项目四个任务：`hermes cron pause <id>`（先 `list` 核对名称）。仅停止 RSSHub 用 `docker stop ai-frontier-rsshub`，其他 Hermes/投资机器人保持运行。恢复用 `hermes cron resume <id>` 与 `docker start ai-frontier-rsshub`。

备份 SQLite 时使用 SQLite backup API 或停本项目任务后复制，不单独拷贝正在写入的 DB 文件而遗漏 WAL。迁移备份整个 `.server-state`、私有群配置与项目代码；不要提交到公共仓库。已废弃的 Mac launchd/Codex 日报任务若仍存在，应核对后停用，防止两套同时出刊。
