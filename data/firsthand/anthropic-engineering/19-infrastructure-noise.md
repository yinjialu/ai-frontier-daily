---
type: Article
title: Quantifying infrastructure noise in agentic coding evals
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/infrastructure-noise
published: 2026-02-05
tags: [AI评测, Agentic Coding, 基础设施, 模型评估]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 发现 agentic coding 评测(如 SWE-bench、Terminal-Bench)中,基础设施资源配置就能让分数波动数个百分点,甚至超过模型间排名差距。在 Terminal-Bench 2.0 上,严格资源限制(floor=ceiling)会因瞬时内存峰值 OOM 杀死容器,基建错误率达 5.8%。3x 余量内主要修复稳定性不改变难度;超过 3x 后额外资源直接帮 agent 解出原本解不了的题,最高较 1x 提升 6 个百分点。资源配置实质改变了评测衡量的内容。
