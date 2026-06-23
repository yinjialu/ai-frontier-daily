---
type: Article
title: Writing effective tools for agents — with agents
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/writing-tools-for-agents
published: 2025-09-11
tags: [AI Agent, MCP, 工具设计, Claude Code]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 工程团队分享如何为 AI agent 编写高效工具。核心方法：先快速搭建原型并本地测试（用 MCP server 或 DXT 接入 Claude Code/Desktop），再基于真实场景生成大量评估任务来系统衡量工具表现，最后让 Claude Code 针对评估结果自动优化工具。关键原则包括：选对该实现的工具、用命名空间划清功能边界、返回有意义的上下文、优化 token 效率、对工具描述做 prompt 工程。强调工具是确定性系统与非确定性 agent 之间的新型契约，需为 agent 而非开发者设计。
