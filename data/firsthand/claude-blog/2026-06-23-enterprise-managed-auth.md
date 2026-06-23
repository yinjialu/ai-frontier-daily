---
type: Article
title: Centrally manage authorization for MCP connectors
source: claude-blog
resource: https://claude.com/blog/enterprise-managed-auth
tags: [MCP, 企业授权, Anthropic, 身份管理]
timestamp: 2026-06-23T20:53:57+08:00
---

Anthropic 推出企业级集中管理 MCP connector 授权功能:管理员通过 IdP(首发支持 Okta)为全组织统一配置 connector,用户首次登录即自动按 IdP 群组/角色继承访问权限,实现零接触配置。这是 MCP 的 Enterprise-Managed Authorization 扩展首个实现,基于开放标准,可缩短 token 生命周期、随离职快速回收权限。首发支持 Asana、Atlassian、Canva、Figma、Linear、Supabase 等。
