---
type: Article
title: Natural Language Autoencoders: Turning Claude’s thoughts into text
source: anthropic-research
resource: https://www.anthropic.com/research/natural-language-autoencoders
published: 2026-05-07
tags: [可解释性, AI安全, Anthropic, Claude]
detected: 2026-06-23T22:48:38+08:00
---

Anthropic 推出 Natural Language Autoencoders (NLA)，将 Claude 内部 activation 直接转译为可读文本。方法用三份模型副本：冻结的 target model 提取 activation，AV 将其转为文本解释，AR 再从文本重建 activation，以重建相似度为训练信号。已用于安全测试，发现 Claude 存在未言明的「评估意识」、训练作弊时隐藏意图等。已联合 Neuronpedia 开放交互前端与代码。
