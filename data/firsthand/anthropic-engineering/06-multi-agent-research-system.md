---
type: Article
title: How we built our multi-agent research system
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/multi-agent-research-system
published: 2025-06-13
tags: [多智能体系统, Agent架构, Claude, Prompt工程]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 分享其 Research 功能多智能体系统的工程经验。采用 orchestrator-worker 架构：Opus 4 主智能体规划并派生多个 Sonnet 4 子智能体并行检索，各自独立上下文窗口实现压缩。内部评测比单智能体 Opus 4 高 90.2%，尤其擅长广度优先查询。Token 用量解释 80% 的性能差异，但多智能体耗费约为对话的 15 倍，仅适合高价值、可并行、超单上下文的任务。
