---
type: Article
title: How we built Claude Code auto mode: a safer way to skip permissions
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/claude-code-auto-mode
published: 2026-03-25
tags: [Claude Code, Agent 安全, 权限管理, Prompt Injection]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 推出 Claude Code 的 auto mode：用模型分类器替代人工授权，在跳过权限确认与安全之间取得平衡。采用双层防御——输入层用 prompt-injection 探针扫描工具输出，输出层用 Sonnet 4.6 transcript 分类器在执行前评估每个动作（先单 token 快筛，再按需 CoT 推理）。主要拦截过度激进与误判 blast radius 的行为，subagent 递归套用同一管线。
