---
type: Article
title: Harness design for long-running application development
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/harness-design-long-running-apps
published: 2026-03-24
tags: [Agent Harness 设计, 多智能体架构, 上下文工程, 长时自主编码]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic Labs 探讨 harness 设计如何突破长时自主编码与前端设计的性能上限。借鉴 GAN 思路构建 generator+evaluator 双智能体,再扩展为 planner-generator-evaluator 三智能体架构。关键洞察:用 context reset(清空重启+结构化交接)而非 compaction 解决上下文焦虑;分离生成与评估智能体,并将主观审美转化为可评分的设计准则,形成迭代反馈闭环。
