---
type: Article
title: How we contain Claude across products
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/how-we-contain-claude
tags: [Agent 安全, Containment 沙箱, Claude Code, Prompt Injection]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 工程团队分享如何为 claude.ai、Claude Code、Cowork 三款 Agent 产品设计安全容纳(containment)机制以限制 Agent 的破坏半径。核心思路从 human-in-the-loop 逐审批转向控制 Agent 能访问的边界:沙箱、VM、文件系统隔离、egress 控制。指出审批疲劳(用户批准约93%提示)使监督失效,Claude Code auto mode 可拦截约83%过激行为,模型层防御(Opus 4.7 注入攻击成功率约0.1%)永远无法100%可靠,故需环境层硬边界兜底。
