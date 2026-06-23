---
type: Article
title: An update on recent Claude Code quality reports
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/april-23-postmortem
published: 2026-04-23
tags: [Claude Code, 模型质量, 推理强度, Prompt工程]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 复盘近期 Claude Code 质量下降投诉，定位为三处独立改动叠加所致：3月4日将默认推理强度从 high 降为 medium（已于4月7日回滚，现 Opus 4.7 默认 xhigh）；3月26日清理闲置会话旧思维链的优化存在 bug，导致每轮都清空、显得健忘重复（4月10日修复）；4月16日新增降低冗长度的系统提示损害编码质量（4月20日回滚）。API 未受影响，全部已修复并重置订阅额度。
