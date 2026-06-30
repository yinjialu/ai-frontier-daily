#!/usr/bin/env python3
"""Repair failed firsthand OKF summaries using the configured LLM service."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from scripts.firsthand.store import failed_summary_articles, write_okf
from scripts.firsthand.summarize import summarize

DEFAULT_OKF_ROOT = Path(__file__).resolve().parents[2] / "data" / "firsthand"

_FM_PUBLISHED_RE = re.compile(r"^published:\s*(\S+)\s*$", re.MULTILINE)
_FULL_TEXT_RE = re.compile(r"\n## Full Text\n\n(?P<body>.*)\Z", re.DOTALL)


def _saved_full_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = _FULL_TEXT_RE.search(text)
    return (m.group("body").strip() if m else "")


def _published(path: Path) -> str | None:
    m = _FM_PUBLISHED_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def repair_failed_summaries(root: Path = DEFAULT_OKF_ROOT, summarize_fn=summarize) -> dict:
    """Rewrite OKF files whose summary is the failure placeholder.

    The monitor stores article full text in OKF files, so this repair path does not
    refetch web pages and can run safely inside GitHub Actions.
    """
    stats = {"repaired": 0, "failed": 0, "skipped": 0}
    for article in failed_summary_articles(root):
        body = _saved_full_text(article["path"])
        if not body:
            stats["skipped"] += 1
            continue
        result = summarize_fn(article["title"] or article["url"], body)
        if result.get("error"):
            stats["failed"] += 1
        else:
            stats["repaired"] += 1
        write_okf(root, {
            "title": article["title"] or article["url"],
            "source": article["source"],
            "url": article["url"],
            "summary": result["summary"],
            "summary_error": result.get("error"),
            "tags": result.get("tags") or [],
            "published": _published(article["path"]),
            "detected": article["detected"],
            "full_text": body,
        })
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(DEFAULT_OKF_ROOT), help="OKF root directory")
    args = parser.parse_args()
    stats = repair_failed_summaries(Path(args.root))
    print(
        "firsthand summary repair: "
        f"repaired={stats['repaired']} failed={stats['failed']} skipped={stats['skipped']}"
    )
    return 1 if stats["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
