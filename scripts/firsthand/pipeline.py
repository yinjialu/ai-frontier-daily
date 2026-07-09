import re

from .summarize import SUMMARY_FAILED
from .urls import canonical_url


def diff_new_articles(fetched: list[dict], ingested: set, open_pr: set) -> list[dict]:
    """抓取结果中扣除已入库 + 已在未合并 PR 的 URL，得真·新文章。"""
    known = {canonical_url(u) for u in (ingested | open_pr)}
    return [a for a in fetched if canonical_url(a["url"]) not in known]


# 标题里太常见、不具区分度的词，不参与 bigram（避免"the/a/in"等噪音）
_STOPWORDS = {
    "the", "a", "an", "in", "of", "to", "for", "and", "or", "on", "with",
    "now", "new", "how", "why", "our", "your", "is", "are", "at", "by",
}


def _title_bigrams(title: str) -> set:
    """提取标题里相邻显著词构成的二元短语集合（小写）。
    共享一个二元短语（如 'claude tag'）比共享单个词更能说明"同一事件"。
    中文标题无空格分词 → 几乎无 bigram，自然不会误判归并。"""
    tokens = [t for t in re.split(r"[^A-Za-z0-9]+", title.lower())
              if len(t) >= 2 and t not in _STOPWORDS]
    return {f"{tokens[i]} {tokens[i + 1]}" for i in range(len(tokens) - 1)}


def cluster_same_event(articles: list[dict]) -> list[list[dict]]:
    """把"疑似同一事件"的跨源文章归并成组（union-find）。
    判据：来自不同源 且 标题共享 ≥1 个显著二元短语。返回组列表（含单元素组）。"""
    n = len(articles)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    bigrams = [_title_bigrams(a["title"]) for a in articles]
    for i in range(n):
        for j in range(i + 1, n):
            if articles[i]["source"] != articles[j]["source"] and (bigrams[i] & bigrams[j]):
                union(i, j)

    groups: dict[int, list] = {}
    for idx, art in enumerate(articles):
        groups.setdefault(find(idx), []).append(art)
    return list(groups.values())


def _render_article(a: dict) -> list[str]:
    mark = " ⚠️" if a["summary"] == SUMMARY_FAILED else ""
    return [f"- [{a['title']}]({a['url']}){mark}", f"  > {a['summary']}"]


def render_pr_body(articles: list[dict]) -> str:
    """渲染 PR 正文。
    - 跨源同事件先归并到「🔗 疑似同一事件（N 源）」一节（克制：同一件事不重复轰炸）；
    - 其余按 source 分组；
    - 摘要失败的文章打 ⚠️ 标记并顶部提示。"""
    groups = cluster_same_event(articles)
    multi = [g for g in groups if len(g) > 1]
    singles = [g[0] for g in groups if len(g) == 1]

    failed = sum(1 for a in articles if a["summary"] == SUMMARY_FAILED)
    lines = []
    if failed:
        lines.append(f"> ⚠️ {failed} 篇摘要生成失败（见下方 ⚠️ 标记），点原文链接手动查看。")
        lines.append("")

    for g in multi:
        sources = ", ".join(sorted({a["source"] for a in g}))
        lines.append(f"## 🔗 疑似同一事件（{len(g)} 源：{sources}）")
        for a in g:
            lines.append(f"- **[{a['source']}]** [{a['title']}]({a['url']})"
                         + (" ⚠️" if a["summary"] == SUMMARY_FAILED else ""))
            lines.append(f"  > {a['summary']}")

    by_source: dict[str, list] = {}
    for a in singles:
        by_source.setdefault(a["source"], []).append(a)
    for sid, arts in by_source.items():
        lines.append(f"## {sid}")
        for a in arts:
            lines.extend(_render_article(a))
    return "\n".join(lines)
