---
type: Article
title: The "think" tool: Enabling Claude to stop and think in complex tool use situations
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/claude-think-tool
published: 2025-03-20
tags: [Agent工具调用, Claude, 推理优化, τ-Bench]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 推出「think」工具,让 Claude 在复杂工具调用链中暂停、整理思路。区别于 extended thinking(响应前规划),它在生成过程中评估已获信息是否充足,适合策略密集、序列决策场景。τ-Bench 测试中航空域 pass^1 相对提升 54%。注:2025年12月官方更新建议多数场景改用 extended thinking。
