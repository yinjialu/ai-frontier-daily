"""查询内参 OKF 索引："最近有什么新动态"。

可被 firsthand-digest skill 调用，也可当 CLI：
    python3 -m scripts.firsthand.query --days 7 [--json]
"""
import argparse
import datetime
import json
import subprocess
from pathlib import Path

from scripts.firsthand.index import parse_okf


# 内参 source id → 每日早报 vendor 轨。供早报(云端,IP 抓不到 news/blog)消费内参(本机抓)补盲区。
SOURCE_VENDOR = {
    "claude-blog": "anthropic", "anthropic-news": "anthropic",
    "anthropic-research": "anthropic", "anthropic-engineering": "anthropic",
    "transformer-circuits": "anthropic",
    "openai-news": "openai",
    "deepmind-blog": "gemini", "google-models-research": "gemini",
    "google-gemini": "gemini",
    "qwen-blog": "cn", "inclusionai-ling": "cn",
}


def vendor_of(source: str) -> str | None:
    return SOURCE_VENDOR.get(source)


def filter_vendor(items: list[dict], vendor: str) -> list[dict]:
    return [a for a in items if vendor_of(a.get("source")) == vendor]


def load_index(okf_root) -> list[dict]:
    p = Path(okf_root) / "index.json"
    if not p.exists():
        return []
    items = json.loads(p.read_text(encoding="utf-8")).get("items", [])
    for item in items:
        item.setdefault("candidate_origin", "main")
    return items


def _is_firsthand_okf(path: str) -> bool:
    parts = path.split("/")
    return (
        len(parts) == 4
        and parts[0] == "data"
        and parts[1] == "firsthand"
        and path.endswith(".md")
    )


def okf_items_from_tree(tree: dict[str, str]) -> list[dict]:
    """Parse OKF markdown blobs from a path->text tree, ignoring non-OKF files."""
    return [parse_okf(text) for path, text in tree.items() if _is_firsthand_okf(path)]


def merge_by_resource(main_items: list[dict], overlay_items: list[dict]) -> list[dict]:
    """Merge items by resource URL; overlay items win, then sort by detected desc."""
    by_resource = {}
    fallback = []
    for item in main_items:
        resource = item.get("resource")
        if resource:
            by_resource[resource] = item
        else:
            fallback.append(item)
    for item in overlay_items:
        resource = item.get("resource")
        if resource:
            by_resource[resource] = item
        else:
            fallback.append(item)
    merged = list(by_resource.values()) + fallback
    merged.sort(key=lambda a: a.get("detected") or "", reverse=True)
    return merged


def _open_firsthand_pr_branches() -> list[str]:
    """Return open PR head branches under firsthand/*; failure means no overlay."""
    proc = subprocess.run(
        ["gh", "pr", "list", "--state", "open", "--json", "headRefName", "--limit", "100"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return _local_firsthand_remote_branches()
    try:
        prs = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    return sorted({
        pr.get("headRefName")
        for pr in prs
        if str(pr.get("headRefName") or "").startswith("firsthand/")
    })


def _local_firsthand_remote_branches() -> list[str]:
    """Best-effort fallback when GitHub API is unavailable.

    It may include already-merged remote branches, but merge_by_resource plus the
    recent window keeps this safe for early-morning digest candidate discovery.
    """
    proc = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/firsthand"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return []
    branches = []
    for ref in proc.stdout.splitlines():
        if ref.startswith("origin/firsthand/"):
            branches.append(ref.removeprefix("origin/"))
    return sorted(set(branches))


def _git_tree_for_branch(branch: str) -> dict[str, str]:
    """Fetch and read data/firsthand/*.md from origin/<branch> without checkout."""
    ref = f"origin/{branch}"
    exists = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", ref],
        capture_output=True, text=True,
    )
    if exists.returncode != 0:
        fetched = subprocess.run(
            ["git", "fetch", "origin", branch, "--quiet"],
            capture_output=True, text=True,
        )
        if fetched.returncode != 0:
            return {}
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, "--", "data/firsthand"],
        capture_output=True, text=True,
    )
    if listing.returncode != 0:
        return {}
    tree = {}
    for path in listing.stdout.splitlines():
        if not _is_firsthand_okf(path):
            continue
        blob = subprocess.run(
            ["git", "show", f"{ref}:{path}"],
            capture_output=True, text=True,
        )
        if blob.returncode == 0:
            tree[path] = blob.stdout
    return tree


def load_open_pr_items(branches: list[str] | None = None) -> list[dict]:
    branches = branches if branches is not None else _open_firsthand_pr_branches()
    items = []
    for branch in branches:
        for item in okf_items_from_tree(_git_tree_for_branch(branch)):
            item["candidate_origin"] = "open-pr"
            item["candidate_ref"] = branch
            items.append(item)
    return items


def recent(items: list[dict], days: int, today: str) -> list[dict]:
    """返回 detected 在近 days 天内的条目，按 detected 倒序。today 形如 'YYYY-MM-DD'。"""
    cutoff = (datetime.date.fromisoformat(today)
              - datetime.timedelta(days=days)).isoformat()
    out = [a for a in items if (a.get("detected") or "")[:10] >= cutoff]
    out.sort(key=lambda a: a.get("detected") or "", reverse=True)
    return out


def _render_text(items: list[dict]) -> str:
    if not items:
        return "近期无新动态。"
    by_source: dict[str, list] = {}
    for a in items:
        by_source.setdefault(a.get("source") or "?", []).append(a)
    lines = [f"近期新动态（{len(items)} 篇）：", ""]
    for sid, arts in by_source.items():
        lines.append(f"## {sid}（{len(arts)}）")
        for a in arts:
            pub = a.get("published") or "?"
            ref = ""
            if a.get("candidate_origin") == "open-pr":
                ref = f"（open PR: {a.get('candidate_ref') or '?'}）"
            lines.append(f"- [{pub}] {a.get('title')} {ref}— {a.get('resource')}")
            if a.get("summary"):
                lines.append(f"  > {a['summary']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--vendor", default=None,
                    help="按早报 vendor 轨过滤（anthropic/openai/gemini/nvidia/cn）")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent.parent
                                          / "data" / "firsthand"))
    ap.add_argument("--json", action="store_true", help="输出 JSON（给 agent 消费）")
    ap.add_argument("--include-open-prs", action="store_true",
                    help="叠加 open firsthand/* PR 中尚未合入 main 的 OKF 条目")
    args = ap.parse_args()
    today = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()
    items = load_index(args.root)
    if args.include_open_prs:
        items = merge_by_resource(items, load_open_pr_items())
    items = recent(items, args.days, today)
    if args.vendor:
        items = filter_vendor(items, args.vendor)
    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        print(_render_text(items))


if __name__ == "__main__":
    main()
