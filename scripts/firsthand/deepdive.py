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


def build_skeleton(cluster: list[dict], fetch_text_fn=fetch_article_text,
                   feature_available: bool = False) -> str:
    """一组同事件文章 → article-harness 草稿 markdown。
    frontmatter sources 给官方 URL（type: reference），正文为五段骨架 + TODO，
    末尾附官方原文素材（供 Writer 整理/翻译，不直接入正文）。"""
    primary = cluster[0]
    title = primary.get("title") or primary.get("resource")

    src_lines = ["sources:"]
    for a in cluster:
        src_lines.append(f"  - type: reference")
        src_lines.append(f"    url: {a['resource']}")
        src_lines.append(f"    note: {a['source']} 官方原文，引用时按此注明出处")

    seen_summaries = "；".join(a.get("summary") or "" for a in cluster if a.get("summary"))

    screenshot_todo = (
        "TODO（Writer 指令）: 补操作截图/录屏入正文。"
        if feature_available else
        "TODO（Writer 指令）: 该功能暂不可体验 → **本节整节不进成稿正文**（删掉本节，"
        "不要写成「暂不可体验，待补」之类占位段落）；不可体验这点若重要，用一句自然的"
        "读者向陈述并入相邻段落即可，'待开放后补截图'以审核说明带外告知作者。")

    body = [
        "---",
        f"title: {title}",
        *src_lines,
        "---",
        "",
        f"# {title}",
        "",
        f"> 内参摘要（起点，非成稿）：{seen_summaries}",
        "",
        "## ① 这是什么（向普通用户）",
        "TODO: 用一句话向普通用户说清这是什么、能干嘛。素材见文末官方原文。",
        "",
        "## ② 功能详解",
        "TODO: 解决什么痛点 / 怎么用 / 关键限制。基于官方原文整理，不堆术语。",
        "",
        "## ③ 官方案例整理 + 翻译",
        "TODO: 整理官网/博客的 use case 并译为中文，保留官方限定词（may/reportedly→可能/据称），不夸大。",
        "",
        "## ④ 实操截图/录屏",
        screenshot_todo,
        "",
        "## ⑤ 作者点评（变量生活视角）",
        "TODO: 尹家露视角的判断（可选）。",
        "",
        "---",
        "## 官方原文素材（供 Writer 整理/翻译，不直接入正文）",
    ]
    for a in cluster:
        text = ""
        try:
            text = fetch_text_fn(a["resource"])
        except Exception as e:
            text = f"(抓取失败: {e})"
        body.append(f"### [{a['source']}] {a.get('title') or ''}")
        body.append(f"原文: {a['resource']}")
        body.append(text[:6000])
        body.append("")
    return "\n".join(body)


def write_draft(content_root, cluster: list[dict], today: str,
                fetch_text_fn=fetch_article_text, feature_available: bool = False) -> Path:
    """写 <content_root>/deepdive/<date>_<slug>/draft.md，返回路径。"""
    slug = slugify(cluster[0]["resource"])
    d = Path(content_root) / "deepdive" / f"{today}_{slug}"
    d.mkdir(parents=True, exist_ok=True)
    path = d / "draft.md"
    path.write_text(build_skeleton(cluster, fetch_text_fn, feature_available), encoding="utf-8")
    return path
