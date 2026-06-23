---
type: Article
title: Measuring LLMs’ impact on N-day exploits
source: anthropic-research
resource: https://www.anthropic.com/research/n-days
published: 2026-06-08
tags: [AI安全, 漏洞利用, 红队评估, Claude]
detected: 2026-06-23T22:48:38+08:00
---

Anthropic 红队评估 LLM 对 N-day 漏洞利用的加速作用。N-day 指已公开补丁但部分设备未修复的漏洞,攻击者可通过 patch diffing 逆向定位漏洞。最强模型 Mythos Preview 在 18 个 Firefox 补丁中自主构建 8 个可执行漏洞利用,在 21 个 Windows 内核补丁中产出 8 条完整提权链(从低权限到 SYSTEM)。从 Opus 4.5 到 4.8,可生成 PoC 的补丁数从 2 增至 11。结论:patch gap 期内的威胁已大幅升级,防御方应加快补丁部署。
