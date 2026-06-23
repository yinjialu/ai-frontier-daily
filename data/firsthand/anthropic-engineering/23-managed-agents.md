---
type: Article
title: Scaling Managed Agents: Decoupling the brain from the hands
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/managed-agents
published: 2026-04-08
tags: [AI Agent 架构, Anthropic, Harness 设计, Agent 安全]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 工程团队介绍 Managed Agents（长时程 Agent 托管服务）的架构演进。核心是将「大脑」（Claude 及其 harness）与「双手」（sandbox/工具）和「session」（事件日志）解耦，借鉴操作系统虚拟化思路定义稳定接口，让各组件可独立替换、失败与重启。harness 移出容器、容器和 harness 都变为可弃用的 cattle，并通过隔离凭据修复 prompt 注入安全边界。
