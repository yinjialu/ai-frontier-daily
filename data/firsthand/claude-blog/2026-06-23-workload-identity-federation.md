---
type: Article
title: Secure access to the Claude Platform with Workload Identity Federation
source: claude-blog
resource: https://claude.com/blog/workload-identity-federation
tags: [Anthropic, 身份认证, API安全, Claude Platform]
timestamp: 2026-06-23T20:53:57+08:00
---

Anthropic 宣布 Claude Platform 的 Workload Identity Federation (WIF) 正式可用,用短时、限定作用域的临时凭证取代静态 API Key。兼容任意 OIDC 提供方(AWS IAM、GCP/K8s 服务账号、Azure 托管身份、GitHub Actions、Okta 等),覆盖全部 Claude API 端点及一方 SDK 与 Claude Code。同时引入服务账号,使每个 workload 拥有独立身份、角色与审计日志,并支持通过 Admin API 以最小权限、可编程方式管理联邦规则。
