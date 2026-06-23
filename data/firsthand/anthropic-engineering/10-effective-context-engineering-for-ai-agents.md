---
type: Article
title: Effective context engineering for AI agents
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
published: 2025-09-29
tags: [Context Engineering, AI Agent, Prompt Engineering, Anthropic]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 提出 context engineering 是 prompt engineering 的自然延伸：从写好提示词，转向在推理全程策划与维护最优的 token 集合（系统提示、工具、MCP、外部数据、消息历史等）。因 attention budget 有限、长上下文存在 context rot，核心原则是用最小高信号 token 集最大化目标行为，系统提示应保持恰当'altitude'，避免过度硬编码脆弱逻辑。
