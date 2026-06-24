# bestblogs / aihot 调研 + 借鉴落地（2026-06-24）

一手信源内参监控系统的一轮迭代记录：调研两个外部项目 → 提炼可借鉴机制 → 落地 4 点 + 早报联动 + 同事件聚合。
判断"是否值得借鉴"的标尺：**克制 / 高质量 / 稳定 / 及时**。

## 一、调研对象与结论

| | bestblogs（ginobefun/bestblogs） | aihot.virxact.com |
|--|----------------------------------|-------------------|
| 定位 | AI 驱动的**私人阅读助手**（质量优先） | AI 行业**热点聚合站**（覆盖优先） |
| 信源 | RSS/Newsletter/Twitter/YouTube/Podcast，400+ 精选源 OPML；含 wechat2rss 转 375 个公众号 | 60% 官方 + 40% 媒体（HN/TechCrunch/公众号） |
| 筛选 | AI 初评 + **编辑精审双层质量池** + 六维评分 | 多维热度排序（时间 + 信源数 + 评分） |
| 摘要 | 六维评分 + 摘要 + 关键观点 + 金句 | 事实层摘要 + 推荐理由 |
| 聚合 | 主题解读（事件/领域/人物/产品对比四类） | 同事件多源聚合标"N 个信源" |
| 气质 | **克制**（不弹窗/不骚扰/广场不个性化排序） | 大而全（单日 20+ 条，热度榜） |

**核心判断**：bestblogs 的"克制 + 质量池"气质与本系统高度一致，借鉴价值高；aihot 是"反面参照"——大而全 + 热度排序 + 媒体混入，恰是要规避的。

## 二、借鉴清单（值得 vs 规避）

### ✅ 值得借鉴
1. **wechat2rss**（暂缓，见下）：公众号 → RSS，理论上绕开 browser 适配器。
2. **跨源同事件聚合**：同一事件多源报道只讲一次 → 已落地。
3. **OKF 库反向暴露 feed/索引**：bestblogs 把精选池暴露成可过滤 RSS → 已落地（不打分）。
4. **CLI + Agent Skills（--json）**：内参做成可查询 skill/CLI → 已落地。
5. OPML 精选源挖一手源（待办）：bestblogs 公开 551 个精选源，可筛官方账号补源。

### ⚠️ 规避（aihot 反面教材）
- 媒体/社区二手源混入（违背官方一手）
- 热度排序 + 每日榜（流量逻辑，非内参逻辑）
- 单日 20+ 条全量铺（违背克制）
- 个性化画像/推荐（个人内参不需要）
- 六维评分套官方源（官方源已高信噪比，过度工程）

## 三、本轮落地（4 点 + 联动 + 聚合）

| # | 特性 | PR | 关键实现 |
|---|------|----|---------|
| A | 跨源同事件聚合（内参 PR 正文） | #52 | `pipeline.cluster_same_event`：跨源 + 共享显著二元短语(bigram) → union-find 归并；中文标题无 bigram 不误判 |
| B | OKF 库导出 index.json + feed.xml | #53 | `scripts/firsthand/index.py`：扫 OKF → 按 published 倒序；`updated` 取 max detected（稳定，不刷屏） |
| C | firsthand-digest skill + 查询 CLI | #54 | `scripts/firsthand/query.py`（`--days/--vendor/--json`）+ `skills/firsthand-digest` |
| D | 当天累积一个 PR（前置改造） | #51 | 分支固定 `firsthand/<date>`；当天后续批次追加 commit + 评论 @user；push 关键、评论尽力而为 |
| E | 早报消费内参补云端盲区 | #55 | `query.py` 加 源→vendor 映射；`ai-daily-digest` SKILL 步骤 3.5 读内参近 1~2 天条目并入候选池 |
| F | 早报策展显式同事件跨源聚合 | #56 | SKILL 步骤 5 硬规则：同事件多源合并成一条，优先官方一手 + 内参真实发布日期 |

> 第 3 点"先不做打分"——index/feed 只是清单，不引入评分（官方源已高信噪比）。
> 第 4 点查询接口默认做成 **Skill**（含 CLI 后端），契合 Claude Code 主线。

## 四、wechat2rss / 公众号：暂缓（结论存档）

用户关注的号（如**晚点LatePost**）实测：
- 免费托管 `wechat2rss.xlab.app`（本机可达，住宅 IP）**未收录晚点**；加任意号要自建或提 Issue。
- `latepost.com` 官网**纯 JS 渲染**（首页 app 壳、文章走 API、无静态链接、无 RSS、无可见 API 端点）。

**判断**：公众号/媒体号是**最不稳定的源**（反爬 + JS + 无 RSS），且媒体号违背"官方一手"。
**决定**：暂缓。真要做则自建 wechat2rss，或留到阶段二 browser 适配器。

## 五、早报 ↔ 内参 双链路分工（重要架构结论）

源起：今早 7:00 早报漏了 Claude Tag，内参 07:49 抓到。根因分析：

| | 早报（云端 Routine） | 内参（本机 launchd） |
|--|---------------------|---------------------|
| 出口 IP | 数据中心 IP → Cloudflare 拦 `anthropic.com/news`、`claude.com/blog` | **住宅/TUN 代理 IP** → 顺利过 Cloudflare |
| 信源 | GitHub releases + news(WebFetch,被拦) + 社区镜像；**无 claude.com/blog** | claude-blog/news/research/engineering 等 11 源专门直抓 |
| 节奏 | 每日 07:00 一次，策展发布 | 每小时 + 开机自启，及时 |

**结论**：早报有两个结构性盲区（**云端 IP 过不了 Cloudflare** + **信源没覆盖 blog**），内参（本机 + 住宅 IP + 专门信源）正好补上。这正是内参项目最初的立项动机（"Routines 访问 claude.com/blog 报错"）。

**分工固化**（PR #55）：内参（本机/住宅IP/小时级）抓云端够不到的 Cloudflare/JS 站 → 导出 `index.json` → 早报（云端/7点/策展）`git pull` 后消费内参 + 自身 web 抓取，统一策展成日报。两条链路互补。

## 六、两套同事件聚合机制对照

| | 内参 | 早报 |
|--|------|------|
| 实现 | Python `cluster_same_event`（共享 bigram，确定性） | Claude 策展指令（语义判断） |
| 为何不同 | 内参是管道，可代码聚类 | 早报是 Claude 驱动，靠 prompt 约束 |

两者收敛到同一原则：**同一件事只讲一次、标多来源、优先官方一手**——与"克制"一致。

## 七、待办（账上）

- **wechat2rss / 公众号**：暂缓（见第四节）。
- **阶段二 browser 适配器**：智谱 GLM、Kimi、晚点 等纯 JS 渲染源（参考 `x-fetch.sh` 的 agent-browser 范式）。
- **登录态失效根治**：摘要失败目前 ⚠️ 标记不补、不重试。
- **OPML 挖源**：从 bestblogs 551 个精选源筛官方账号补 `firsthand-sources.yaml`。
