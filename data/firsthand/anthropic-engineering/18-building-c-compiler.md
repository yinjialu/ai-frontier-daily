---
type: Article
title: Building a C compiler with a team of parallel Claudes
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/building-c-compiler
published: 2026-02-05
tags: [Agent 编排, 并行 Agent, Claude Code, 自主软件开发]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 研究员 Carlini 用 Opus 4.6 的「agent teams」方法，让 16 个 Claude 实例在共享代码库上无人值守并行协作，经约 2000 次会话、2 万美元成本，从零写出 10 万行 Rust 实现的 C 编译器，可编译 Linux 6.9（x86/ARM/RISC-V）。核心经验：无限 Ralph-loop 自驱、git 文件锁防止任务冲突、靠高质量测试与 CI 让 agent 在无人监督下保持正确方向。
