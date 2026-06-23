---
type: Article
title: Equipping agents for the real world with Agent Skills
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
published: 2025-10-16
tags: [Agent Skills, 渐进式披露, Claude, Agent 工程]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 推出 Agent Skills：用文件夹组织指令、脚本和资源，让通用 Agent 动态发现并加载领域专长。核心是渐进式披露——启动仅加载 name/description 元数据，需要时读 SKILL.md，再按需加载附加文件，使可打包上下文近乎无限。Skill 还可内置代码供 Claude 按需执行，兼顾确定性与效率。已开放为跨平台标准。
