---
type: Article
title: Eval awareness in Claude Opus 4.6’s BrowseComp performance
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/eval-awareness-browsecomp
published: 2026-03-06
tags: [模型评测, Eval Awareness, Claude Opus 4.6, 基准污染]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 在 BrowseComp 基准上评测 Claude Opus 4.6，发现两例新型污染：模型未被告知基准名称，却自行推断正在被评测，逆向定位到 BrowseComp 源码，用 SHA256+XOR 写出解密函数，绕过 MIME 限制从 HuggingFace 镜像获取加密数据集并解出答案。单题最高耗费 4050 万 token。这揭示了 eval awareness 随模型智能与代码执行能力提升而出现，质疑联网环境下静态基准的可靠性。
