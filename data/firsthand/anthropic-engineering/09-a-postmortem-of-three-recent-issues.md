---
type: Article
title: A postmortem of three recent issues
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
published: 2025-09-17
tags: [Anthropic, 推理基础设施, 故障复盘, TPU/编译器]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 复盘 8-9 月三个基础设施 bug 导致 Claude 响应质量间歇性下降：上下文窗口路由错误将短请求误发到 1M token 服务器；TPU 运行时优化误配导致输出乱码（英文中夹杂中泰文字符）；XLA:TPU 编译器 top-k 选词隐藏 bug。强调质量下降仅因 bug，绝非按负载降智，并改进检测测试。
