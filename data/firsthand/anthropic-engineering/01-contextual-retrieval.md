---
type: Article
title: Introducing Contextual Retrieval
source: anthropic-engineering
resource: https://www.anthropic.com/engineering/contextual-retrieval
published: 2024-09-19
tags: [RAG, 检索增强, Anthropic, Prompt Caching]
detected: 2026-06-23T21:56:58+08:00
---

Anthropic 提出 Contextual Retrieval，针对传统 RAG 切块丢失上下文导致检索失败的问题，通过 Contextual Embeddings 与 Contextual BM25 为每个 chunk 补充上下文，使检索失败率降低 49%，结合重排序后降低 67%。并指出知识库小于 20 万 token 时可直接配合 prompt caching 全量放入上下文。
