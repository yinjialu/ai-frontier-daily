---
type: Article
title: Desktop Extensions: One-click MCP server installation for Claude Desktop
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/desktop-extensions
published: 2025-06-26
tags: [MCP, Claude Desktop, 开发者工具, Anthropic]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 推出 Desktop Extensions（.mcpb 文件），将 MCP server 及全部依赖打包成单个安装包，用户双击即可安装，无需 Node.js/Python 运行时、手动改 JSON 配置或处理依赖冲突。核心是 manifest.json 描述元数据与配置，Claude Desktop 内置 Node.js 运行时、自动更新、密钥存入系统钥匙串。支持 Node/Python/二进制三类。2025-09 起扩展名由 .dxt 改为 .mcpb。
