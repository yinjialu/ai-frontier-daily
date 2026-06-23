---
type: Article
title: Effective harnesses for long-running agents
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
published: 2025-11-26
tags: [AI Agent, Claude Agent SDK, Context Engineering, Harness 设计]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 探讨长时运行 Agent 的 harness 设计：跨多个 context window 工作时每次会话都无记忆。方案分两部分——initializer agent 首次运行搭建环境（init.sh、claude-progress.txt 进度日志、初始 git commit、200+ 条 feature 需求清单），coding agent 每次只做增量推进并留下清晰产物。借鉴人类工程师交接班实践，解决一次性硬塞和过早判定完成两大失败模式。
