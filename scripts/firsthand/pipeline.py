from .summarize import SUMMARY_FAILED


def diff_new_articles(fetched: list[dict], ingested: set, open_pr: set) -> list[dict]:
    """抓取结果中扣除已入库 + 已在未合并 PR 的 URL，得真·新文章。"""
    known = ingested | open_pr
    return [a for a in fetched if a["url"] not in known]


def render_pr_body(articles: list[dict]) -> str:
    """把文章列表渲染成 PR 正文（按 source 分组）。
    摘要失败的文章打 ⚠️ 标记并单独提示，方便人工 review 时一眼识别。"""
    by_source = {}
    for a in articles:
        by_source.setdefault(a["source"], []).append(a)
    failed = sum(1 for a in articles if a["summary"] == SUMMARY_FAILED)
    lines = []
    if failed:
        lines.append(f"> ⚠️ {failed} 篇摘要生成失败（见下方 ⚠️ 标记），点原文链接手动查看。")
        lines.append("")
    for sid, arts in by_source.items():
        lines.append(f"## {sid}")
        for a in arts:
            mark = " ⚠️" if a["summary"] == SUMMARY_FAILED else ""
            lines.append(f"- [{a['title']}]({a['url']}){mark}")
            lines.append(f"  > {a['summary']}")
    return "\n".join(lines)
