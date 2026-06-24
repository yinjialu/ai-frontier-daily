"""专题深度线：选题初筛 + 骨架生成器。
复用内参 index（query.recent）+ 同事件聚合（pipeline.cluster_same_event），
产出带官方素材的 draft.md，喂给 article-harness 打磨。
"""
from pathlib import Path

from .query import recent
from .pipeline import cluster_same_event
from .adapters import fetch_article_text
from .store import slugify


def candidates(items: list[dict], days: int, today: str) -> list[list[dict]]:
    """内参近 days 天条目 → 同事件聚成候选（每候选 = 一个事件的一组文章），按时间倒序。
    cluster_same_event 用 title 字段，index 条目已带 title/source。"""
    recents = recent(items, days, today)
    groups = cluster_same_event(recents)
    for g in groups:
        g.sort(key=lambda a: a.get("detected") or "", reverse=True)
    groups.sort(key=lambda g: g[0].get("detected") or "", reverse=True)
    return groups
