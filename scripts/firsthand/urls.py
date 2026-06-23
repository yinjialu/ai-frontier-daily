from urllib.parse import urljoin, urlsplit, urlunsplit


def canonical_url(url: str) -> str:
    """去 query/fragment，去末尾斜杠，作为去重主键。"""
    parts = urlsplit(url)
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def make_absolute(href: str, base_url: str) -> str:
    """相对路径补全为绝对 URL；已是绝对则原样返回。"""
    return urljoin(base_url.rstrip("/") + "/", href)
