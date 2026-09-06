# 模型官方发布渠道校准（2026-09-06）

模型公告、API 可用性和开源权重是三种不同信号。官方公告通常用于确认新能力；API 更新日志用于确认上线、定价、限额、弃用；官方 GitHub/Hugging Face 用于确认权重/许可。SDK、CLI releases 不能等同于模型发布。社交账号/科技媒体只作发现线索，卡片主链接回到官方原文。抓取时间、sitemap lastmod、Atom updated 均不是原始发布日期。

| 厂商 | 官方主渠道 | 校准与接入 |
|---|---|---|
| OpenAI | [News RSS](https://openai.com/news/rss.xml)、[API Changelog](https://developers.openai.com/api/docs/changelog) | 原生 RSS；更新日志使用官方 `.md` 版本按月份与日解析，不能仅抓 SDK |
| Anthropic / Claude | [Newsroom](https://www.anthropic.com/news)、[Claude Blog](https://claude.com/blog)、[Engineering](https://www.anthropic.com/engineering)、[Research](https://www.anthropic.com/research)、[Claude API release notes](https://platform.claude.com/docs/en/release-notes/overview) | 官网列表为主；RSSHub `/anthropic/news`、`/anthropic/engineering`、`/anthropic/research` 可作转换兜底。社区 RSS 镜像不是官方 feed |
| Google / Gemini | [DeepMind RSS](https://deepmind.google/blog/rss.xml)、[Models & Research RSS](https://blog.google/innovation-and-ai/models-and-research/rss/)、[Gemini API Changelog](https://ai.google.dev/gemini-api/docs/changelog)、[Vertex release notes](https://cloud.google.com/vertex-ai/generative-ai/docs/release-notes) | 模型公告、Gemini API、Vertex 上线分别监控，三者时间可能不同 |
| DeepSeek | [API Change Log](https://api-docs.deepseek.com/updates/)、[官方 GitHub](https://github.com/deepseek-ai)、[官方模型页](https://huggingface.co/deepseek-ai) | API 公告为主；RSSHub `/deepseek/news` 已核对上游实现。新仓库只作线索 |
| Qwen | [当前博客](https://qwen.ai/blog)、[旧博客](https://qwenlm.github.io/blog/)、[官方模型页](https://huggingface.co/Qwen) | **不能只订阅旧 GitHub Pages 博客**；自建 RSSHub `/qwen/blog/zh-CN` 从当前站点数据接口生成 RSS，VM 已返回有效条目 |
| 智谱 / GLM | [国内产品发布](https://docs.bigmodel.cn/cn/update/new-releases)、[Z.ai 文档](https://docs.z.ai/release-notes/new-released)、[官方模型页](https://huggingface.co/zai-org) | 实测旧 `z.ai/blog` 为 404，不能继续标为健康；改接 Z.ai 文档的日期时间线，另用每天官方域名搜索补充 |
| Kimi | [Kimi Blog](https://www.kimi.com/blog)、[Moonshot Changelog](https://platform.moonshot.ai/docs/changelog)、[官方模型页](https://huggingface.co/moonshotai) | Kimi 博客已抓到文章；已补新域名 kimi.ai；CLI release 只作辅助 |
| 豆包 / Seed | [Seed Blog](https://seed.bytedance.com/zh/blog)、[模型目录](https://seed.bytedance.com/zh/models)、[方舟公告](https://www.volcengine.com/docs/82379/1159177) | 官网博客动态加载，当前固定列表适配失败；每日官方站点搜索补充，不能声称 feed 已接通 |
| MiniMax | [News](https://www.minimax.io/news)、[Blog](https://www.minimax.io/blog)、[官方模型页](https://huggingface.co/MiniMaxAI) | 新模型文章已有 `/blog` 路径，仅 `/news/` 会漏；改用官方 sitemap 发现，发布日期回文章核对 |
| 文心 / ERNIE | [百度千帆](https://cloud.baidu.com/doc/qianfan-docs/index.html)、[ERNIE](https://ernie.baidu.com/) | 每日官方站点搜索；固定订阅适配待补 |
| 混元 | [混元官网](https://hunyuan.tencent.com/)、[腾讯云产品动态](https://cloud.tencent.com/document/product/1729/97765) | 每日官方站点搜索；不要把平台更新直接视为新模型 |
| 阶跃星辰 | [官网](https://www.stepfun.com/)、[官方模型页](https://huggingface.co/stepfun-ai) | 每日官方站点搜索，模型卡/许可补充核实 |
| 百川 | [官网](https://www.baichuan-ai.com/)、[官方模型页](https://huggingface.co/baichuan-inc) | 每日官方站点搜索，量化版本不冒充独立新基座模型 |
| 零一万物 | [官网](https://www.01.ai/cn)、[官方模型页](https://huggingface.co/01-ai) | 每日官方站点搜索，无可靠新增就不凑日报 |
| 百灵 / inclusionAI | [当前博客](https://www.inclusion-ai.org/blog)、[现有订阅入口](https://inclusionai.github.io/blog/atom.xml) | feed 文章已指向新域名 `inclusion-ai.org`，白名单需要同步迁移 |
| xAI / Grok | [News](https://x.ai/news)、[API 文档](https://docs.x.ai/) | 官网 News 已抓到条目；人员个人账号不替代发布公告 |
| Mistral | [News](https://mistral.ai/news/)、[模型文档](https://docs.mistral.ai/) | 官网文章为主，权重与 API 可用性分别记录 |
| Meta / Llama | [Meta AI Blog](https://ai.meta.com/blog/)、[Llama](https://www.llama.com/) | 官网文章为主，另核对模型许可与获取范围 |
| NVIDIA | [Newsroom feed](https://nvidianews.nvidia.com/releases.xml)、[Blog feed](https://blogs.nvidia.com/feed/)、[Developer Blog](https://developer.nvidia.com/blog/) | Newsroom feed 同时链接 NVIDIA Blog，两个官方域名均需接受；模型与基础设施新闻分开分类 |

## RSSHub 的定位

公共 `rsshub.app` 本次访问返回 403，所以服务器自建环回实例。上游 [官方 Docker Compose](https://github.com/DIYgod/RSSHub/blob/master/docker-compose.yml) 和路由源码已核对：[Anthropic](https://github.com/DIYgod/RSSHub/tree/master/lib/routes/anthropic)、[DeepSeek](https://github.com/DIYgod/RSSHub/tree/master/lib/routes/deepseek)、[Qwen](https://github.com/DIYgod/RSSHub/tree/master/lib/routes/qwen)。优先原生 RSS，次选官方 HTML/更新日志，缺少订阅的站点再用 RSSHub 或真实搜索补充。

RSSHub 不会自动把“全网”变成可靠可订阅数据，也不能保证绕过反爬。微信公众号、X 等路由可能需要登录或额外配置，当前没有自动搬运个人浏览器登录态。官方渠道清单是校准结果；实际自动订阅和真实搜索覆盖分别以部署配置及健康/研究台账为准。Hugging Face 链接目前为人工核验入口，不代表已启用模型仓库轮询。
