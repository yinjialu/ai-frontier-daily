---
type: Article
title: Beyond permission prompts: making Claude Code more secure and autonomous
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/claude-code-sandboxing
published: 2025-10-20
tags: [Claude Code, Agent 安全, 沙箱隔离, Prompt Injection]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 为 Claude Code 推出基于沙箱的两项新功能：文件系统隔离与网络隔离，在 OS 层(Linux bubblewrap / macOS seatbelt)设定边界，让 Claude 无需频繁权限确认即可自主执行命令。内部使用中安全减少 84% 权限弹窗，并能防御 prompt injection 导致的密钥泄露或恶意外联。同时开源沙箱运行时，并发布可在云端隔离沙箱运行的 Claude Code on the web。
