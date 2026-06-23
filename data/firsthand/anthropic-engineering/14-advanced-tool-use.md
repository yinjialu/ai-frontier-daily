---
type: Article
title: Introducing advanced tool use on the Claude Developer Platform
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/advanced-tool-use
published: 2025-11-24
tags: [Claude API, 工具调用, Agent 开发, 上下文工程]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 为 Claude 开发者平台推出三项工具使用 beta 功能：Tool Search Tool 让 Claude 按需检索工具，避免上千工具定义占满上下文（实测节省 85% token，MCP 评测准确率 Opus 4.5 从 79.5% 升至 88.1%）；Programmatic Tool Calling 让模型在代码执行环境中调用工具、减少上下文负担；Tool Use Examples 用示例而非纯 schema 教模型正确用法。
