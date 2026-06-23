def diff_new_articles(fetched: list[dict], ingested: set, open_pr: set) -> list[dict]:
    """抓取结果中扣除已入库 + 已在未合并 PR 的 URL，得真·新文章。"""
    known = ingested | open_pr
    return [a for a in fetched if a["url"] not in known]
