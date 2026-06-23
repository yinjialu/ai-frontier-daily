---
type: Article
title: New in Claude Managed Agents: run agents on a schedule and store environment variables in vaults
source: claude-blog
resource: https://claude.com/blog/whats-new-in-claude-managed-agents
published: 2026-06-09
tags: [Claude Managed Agents, 定时任务调度, 密钥管理, Agent 基础设施]
detected: 2026-06-23T20:53:57+08:00
---

Anthropic 为 Claude Managed Agents 推出两项公测能力:一是定时部署(scheduled deployment),为 agent 配置 cron 计划,每次触发自动开新 session 完成任务,无需自建调度器,适用于夜间数据同步、每周合规扫描等周期任务;二是 vault 扩展支持环境变量,密钥仅在网络边界注入且限定可达域名,模型永远看不到真实 key,让 CLI(Browserbase、KERNEL、Notion 等)安全发起鉴权请求。
