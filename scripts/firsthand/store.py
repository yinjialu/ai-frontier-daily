import json
import re
from pathlib import Path

_FM_RESOURCE_RE = re.compile(r"^resource:\s*(\S+)\s*$", re.MULTILINE)
_FM_PUBLISHED_RE = re.compile(r"^published:\s*(\S+)\s*$", re.MULTILINE)
_SEQ_PREFIX_RE = re.compile(r"^(\d+)-")


def slugify(url: str) -> str:
    """取 URL 最后一段作为 slug。末段是 index.html/index 等无意义时，退用父段
    （如 .../2026/may-update/index.html → may-update）。"""
    parts = url.rstrip("/").rsplit("/", 2)
    last = parts[-1]
    if last.lower() in ("index.html", "index.htm", "index") and len(parts) >= 2:
        return parts[-2]
    return last


def _source_dir(root: Path, source_id: str) -> Path:
    return Path(root) / source_id


def _existing_okf_for(d: Path, url: str) -> Path | None:
    """返回目录中 resource==url 的现有 OKF 文件（用于幂等复用原文件名/序号）。"""
    if not d.exists():
        return None
    for md in d.glob("*.md"):
        m = _FM_RESOURCE_RE.search(md.read_text(encoding="utf-8"))
        if m and m.group(1) == url:
            return md
    return None


def _next_sequence(d: Path) -> int:
    """目录中现有最大序号 + 1（无则 1）。新文章总是最新 → 接在序号末尾。"""
    mx = 0
    if d.exists():
        for md in d.glob("*.md"):
            m = _SEQ_PREFIX_RE.match(md.name)
            if m:
                mx = max(mx, int(m.group(1)))
    return mx + 1


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


def _render_okf(article: dict) -> str:
    tags = ", ".join(article.get("tags") or [])
    body = article.get("summary") or ""
    # 摘要失败：把原因写进 body，commit/PR diff 里直接可见为啥失败（不再静默吞掉）。
    err = article.get("summary_error")
    if err:
        body = f"{body}\n\n> 失败原因：{err}"
    published = article.get("published")
    fm = [
        "---",
        "type: Article",
        f"title: {article['title']}",
        f"source: {article['source']}",
        f"resource: {article['url']}",
    ]
    if published:
        fm.append(f"published: {published}")
    fm.append(f"tags: [{tags}]")
    fm.append(f"detected: {article['detected']}")
    fm.append("---")
    full_text = article.get("full_text") or ""
    full_text_section = f"\n\n## Full Text\n\n{full_text}" if full_text.strip() else ""
    return "\n".join(fm) + "\n\n" + body + full_text_section + "\n"


def write_okf(root: Path, article: dict) -> Path:
    """写一篇 OKF markdown，返回路径。文件名 <NN>-<slug>.md。

    <NN> 是 2 位序号，按写入顺序递增（backfill 时按 published 升序写 → 序号=发布序）。
    新文章总是最新 → 取「现有最大序号+1」接在末尾，无需重编号。
    同一 URL 重写 → 复用原文件名（含原序号），幂等。

    frontmatter:
      published —— 文章真实发布日期（取不到则不写该字段，不杜撰）
      detected  —— 内参监控发现该文的时间（诚实标注，非发布时间）
    """
    d = _source_dir(root, article["source"])
    d.mkdir(parents=True, exist_ok=True)
    url = article["url"]
    existing = _existing_okf_for(d, url)
    if existing is not None:
        path = existing  # 幂等：同一 URL 复用原文件名/序号
    else:
        seq = _next_sequence(d)
        path = d / f"{seq:02d}-{slugify(url)}.md"
    path.write_text(_render_okf(article), encoding="utf-8")
    return path


def renumber_source(d: Path) -> None:
    """按 published 升序（undated 排最后，再按原序号稳定）重排目录内所有 OKF 的序号前缀。
    一次性整理/迁移用；去重靠文件内 resource，重命名不影响。"""
    d = Path(d)
    if not d.exists():
        return
    files = list(d.glob("*.md"))

    def key(md):
        t = md.read_text(encoding="utf-8")
        pm = _FM_PUBLISHED_RE.search(t)
        published = pm.group(1) if pm else "9999-99-99"  # undated 最后
        sm = _SEQ_PREFIX_RE.match(md.name)
        old_seq = int(sm.group(1)) if sm else 0
        return (published, old_seq, md.name)

    files.sort(key=key)
    # 先全部改临时名避免改名冲突，再定序号
    tmp = []
    for i, md in enumerate(files):
        t = md.rename(d / f".__renum_{i}.md")
        tmp.append(t)
    for i, md in enumerate(tmp, start=1):
        slug = _SEQ_PREFIX_RE.sub("", md.name.replace(".__renum_", "").rsplit(".md", 1)[0])
        # 从内容恢复 slug：用 resource 末段更稳
        rm = _FM_RESOURCE_RE.search(md.read_text(encoding="utf-8"))
        slug = slugify(rm.group(1)) if rm else f"item{i}"
        md.rename(d / f"{i:02d}-{slug}.md")


def load_state(state_file: Path) -> dict:
    p = Path(state_file)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save_state(state_file: Path, state: dict) -> None:
    Path(state_file).write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )
