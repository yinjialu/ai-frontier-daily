---
type: Article
title: Agent identity in Claude Tag: a new access model for autonomous, team-wide AI
source: claude-blog
resource: https://claude.com/blog/agent-identity-access-model
published: 2026-06-24
tags: [Agent 身份与权限, Claude Tag, 多人协作 AI, 企业访问控制]
detected: 2026-06-24T07:49:26+08:00
---

Anthropic 为 Claude Tag(多人协作场景)推出 agent identity 访问模型:Claude 不再借用某个用户的权限,而是以自身独立账号行事——在 Slack 以 Claude app 发言、以 Claude GitHub App 提 PR、用服务账号查数仓。管理员在 workspace 层定义身份(连接、仓库、connector、skills、standing instructions),各 channel 默认继承并可覆盖,权限从 per-user 转为 per-channel,撤销身份即全局断权,也杜绝共享频道成为私人文档的侧门。
