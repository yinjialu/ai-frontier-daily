---
type: Article
title: Building effective agents
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/building-effective-agents
published: 2024-12-19
tags: [AI Agent, LLM 工程实践, Anthropic, Workflow 设计模式]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 工程团队总结构建有效 LLM agent 的经验：最成功的实现往往用简单可组合的模式而非复杂框架。区分 workflow（预定义代码路径编排）与 agent（模型自主决策），建议优先用最简方案，必要时再加复杂度。核心构建块是增强型 LLM（检索、工具、记忆），并介绍 prompt chaining、routing 等常见模式。
