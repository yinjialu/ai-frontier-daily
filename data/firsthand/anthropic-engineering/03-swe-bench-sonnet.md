---
type: Article
title: Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/swe-bench-sonnet
published: 2025-01-06
tags: [Claude 3.5 Sonnet, SWE-bench, Coding Agent, Agent Scaffold]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 升级版 Claude 3.5 Sonnet 在 SWE-bench Verified 软件工程基准上达到 49%，超越此前 SOTA 的 45%。关键在于极简 agent scaffold：仅配 Bash 工具与文件编辑工具，给模型最大自主权，让其自行判断探索、复现、修改、测试的流程，而非硬编码工作流，并持续采样直到模型自认完成或触及 200k 上下文上限。
