---
type: Article
title: Code execution with MCP: Building more efficient agents
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/code-execution-with-mcp
published: 2025-11-04
tags: [MCP, AI Agent, Token优化, Anthropic]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 提出用代码执行替代直接工具调用来提升 MCP Agent 效率。传统做法把所有工具定义预加载进上下文、中间结果反复穿过模型，导致 token 暴涨。新方案将 MCP 服务器暴露为代码 API（每个工具一个文件），Agent 按需加载工具并在执行环境内处理数据，再回传结果，从而支持更多工具、消耗更少 token。
