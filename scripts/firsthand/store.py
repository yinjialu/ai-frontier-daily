import hashlib
import json
import re
from pathlib import Path

_FM_RESOURCE_RE = re.compile(r"^resource:\s*(\S+)\s*$", re.MULTILINE)


def slugify(url: str) -> str:
    """取 URL 最后一段作为 slug。"""
    return url.rstrip("/").rsplit("/", 1)[-1]


def _source_dir(root: Path, source_id: str) -> Path:
    return Path(root) / source_id


def ingested_urls(root: Path, source_id: str) -> set[str]:
    """扫 data/firsthand/<id>/*.md 的 frontmatter resource，= 已入库 URL 集合（去重真相）。"""
    d = _source_dir(root, source_id)
    if not d.exists():
        return set()
    urls = set()
    for md in d.glob("*.md"):
        m = _FM_RESOURCE_RE.search(md.read_text(encoding="utf-8"))
        if m:
            urls.add(m.group(1))
    return urls


def write_okf(root: Path, article: dict) -> Path:
    """写一篇 OKF markdown，返回路径。文件名 <date>-<slug>.md。"""
    d = _source_dir(root, article["source"])
    d.mkdir(parents=True, exist_ok=True)
    date = article["timestamp"][:10]
    url = article["url"]
    slug = slugify(url)
    path = d / f"{date}-{slug}.md"
    # 防覆盖：若目标已存在且其 resource 与当前 url 不同（真冲突），改用带短哈希文件名。
    # 重复写同一篇 URL（resource 相同）时仍用原名，幂等覆盖自身。
    if path.exists():
        m = _FM_RESOURCE_RE.search(path.read_text(encoding="utf-8"))
        if m and m.group(1) != url:
            h6 = hashlib.sha1(url.encode()).hexdigest()[:6]
            path = d / f"{date}-{slug}-{h6}.md"
    tags = ", ".join(article.get("tags") or [])
    body = article.get("summary") or ""
    content = (
        "---\n"
        "type: Article\n"
        f"title: {article['title']}\n"
        f"source: {article['source']}\n"
        f"resource: {article['url']}\n"
        f"tags: [{tags}]\n"
        f"timestamp: {article['timestamp']}\n"
        "---\n\n"
        f"{body}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def load_state(state_file: Path) -> dict:
    p = Path(state_file)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save_state(state_file: Path, state: dict) -> None:
    Path(state_file).write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )
