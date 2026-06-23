---
type: Article
title: Best practices for Claude Code
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/claude-code-best-practices
published: 2025-04-18
tags: [Claude Code, 上下文工程, Agent 实践, Prompt Engineering]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 官方发布的 Claude Code 最佳实践指南。核心约束是上下文窗口会快速填满且性能随之下降,因此需积极管理。关键实践:给 Claude 可运行的验证手段(测试/构建/截图),让闭环自动收敛;先探索再规划后编码;提供具体上下文与丰富内容;配置 CLAUDE.md、权限、hooks、skills、子代理;通过 /goal、Stop hook、对抗式审查子代理多层级把关停止条件;并行多会话、非交互与自动模式实现规模化。
