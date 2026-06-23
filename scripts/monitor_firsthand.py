#!/usr/bin/env python3
"""一手信源内参监控 —— launchd 每小时入口。"""
import os
os.environ["PATH"] = (
    "/Users/jialu/anaconda3/bin:" + os.environ.get("PATH", "")
    + ":/opt/homebrew/bin:" + os.path.expanduser("~/.nvm/versions/node/v24.13.0/bin")
    + ":" + os.path.expanduser("~/.local/bin")
)

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.firsthand.config import load_sources
from scripts.firsthand.adapters import fetch_source, fetch_article_text
from scripts.firsthand.summarize import summarize
from scripts.firsthand.store import ingested_urls, write_okf, load_state, save_state
from scripts.firsthand.pipeline import diff_new_articles

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = REPO / "firsthand-sources.yaml"
DEFAULT_OKF_ROOT = REPO / "data" / "firsthand"
DEFAULT_STATE = REPO / "data" / "firsthand-state.json"


def run_once(sources_path, okf_root, state_file, now,
             fetch_fn=fetch_source,
             article_text_fn=fetch_article_text,
             summarize_fn=summarize,
             open_pr_fn=None,
             commit_state_fn=None):
    """单轮检查。副作用函数（PR/commit）可注入便于测试。返回统计 dict。"""
    okf_root = Path(okf_root)
    sources = load_sources(sources_path)
    state = load_state(state_file)
    all_new = []
    for source in sources:
        sid = source["id"]
        st = state.setdefault(sid, {})
        try:
            fetched = fetch_fn(source)
            st["last_fetch_ok"] = True
            st["last_fetch_error"] = None
        except Exception as e:
            st["last_fetch_ok"] = False
            st["last_fetch_error"] = str(e)
            st["last_checked"] = now
            continue
        st["last_checked"] = now
        ingested = ingested_urls(okf_root, sid)
        open_pr = set(st.get("open_pr_urls", []))
        first_run = not ingested and not open_pr and "total_articles_seen" not in st
        new_articles = diff_new_articles(fetched, ingested, open_pr)
        if first_run:
            st["open_pr_urls"] = [a["url"] for a in fetched]
            st["total_articles_seen"] = len(fetched)
            continue
        st["total_articles_seen"] = len(ingested) + len(open_pr)
        for art in new_articles:
            all_new.append((source, art))

    new_count = 0
    if all_new:
        pr_articles = []
        for source, art in all_new:
            text = article_text_fn(art["url"])
            s = summarize_fn(art.get("title") or art["url"], text)
            article = {
                "title": art.get("title") or art["url"],
                "source": source["id"],
                "url": art["url"],
                "summary": s["summary"],
                "tags": s["tags"],
                "timestamp": now,
            }
            write_okf(okf_root, article)
            state[source["id"]].setdefault("open_pr_urls", [])
            state[source["id"]]["open_pr_urls"].append(art["url"])
            state[source["id"]]["last_new_article"] = now
            pr_articles.append(article)
        new_count = len(pr_articles)
        branch = f"firsthand/{now[:10]}"
        if open_pr_fn:
            open_pr_fn(branch, pr_articles)

    save_state(state_file, state)
    if commit_state_fn:
        commit_state_fn()
    return {"new_count": new_count}


def _real_open_pr(branch, articles):
    """建分支、提交 OKF 文件、开 PR。"""
    subprocess.run(["git", "checkout", "-B", branch], cwd=REPO, check=True)
    # 只提 OKF 文件——state.json 走 main 单独提交，避免两头写同一文件 merge 时回退
    subprocess.run(["git", "add", "data/firsthand/"], cwd=REPO, check=True)
    subprocess.run(["git", "commit", "-m", f"firsthand: 内参新动态 {branch}"],
                   cwd=REPO, check=True)
    subprocess.run(["git", "push", "-u", "origin", branch], cwd=REPO, check=True)
    by_source = {}
    for a in articles:
        by_source.setdefault(a["source"], []).append(a)
    counts = ", ".join(f"{k} {len(v)}篇" for k, v in by_source.items())
    title = f"📡 内参新动态 | {branch[-10:]} ({counts})"
    body_lines = []
    for sid, arts in by_source.items():
        body_lines.append(f"## {sid}")
        for a in arts:
            body_lines.append(f"- [{a['title']}]({a['url']})")
            body_lines.append(f"  > {a['summary']}")
    subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body", "\n".join(body_lines),
         "--reviewer", "yinjialu", "--label", "firsthand-intel", "--base", "main"],
        cwd=REPO, check=True,
    )
    subprocess.run(["git", "checkout", "main"], cwd=REPO, check=True)


def _real_commit_state():
    """state.json 直接提交 main（本机无 403）。"""
    subprocess.run(["git", "add", "data/firsthand-state.json"], cwd=REPO, check=False)
    r = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO)
    if r.returncode != 0:
        subprocess.run(["git", "commit", "-m", "chore: firsthand state"], cwd=REPO, check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO, check=False)


def main():
    import datetime
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec="seconds")
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=REPO, check=False)
    result = run_once(
        DEFAULT_SOURCES, DEFAULT_OKF_ROOT, DEFAULT_STATE, now,
        open_pr_fn=_real_open_pr, commit_state_fn=_real_commit_state,
    )
    print(f"[firsthand] {now} new={result['new_count']}")


if __name__ == "__main__":
    main()
