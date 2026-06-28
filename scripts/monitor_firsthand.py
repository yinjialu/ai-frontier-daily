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
from scripts.firsthand.adapters import (
    fetch_source, fetch_article_text, fetch_article_title, fetch_article_published,
)
from scripts.firsthand.summarize import summarize
from scripts.firsthand.store import ingested_urls, write_okf, load_state, save_state
from scripts.firsthand.pipeline import diff_new_articles, render_pr_body

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = REPO / "firsthand-sources.yaml"
DEFAULT_OKF_ROOT = REPO / "data" / "firsthand"
DEFAULT_STATE = REPO / "data" / "firsthand-state.json"


def run_once(sources_path, okf_root, state_file, now,
             fetch_fn=fetch_source,
             article_text_fn=fetch_article_text,
             article_title_fn=fetch_article_title,
             article_published_fn=fetch_article_published,
             summarize_fn=summarize,
             open_pr_fn=None,
             commit_state_fn=None):
    """单轮检查。副作用函数（PR/commit）可注入便于测试。返回统计 dict。"""
    okf_root = Path(okf_root)
    sources = load_sources(sources_path)
    state = load_state(state_file)
    # last_checked 是每轮都变的心跳，单独写本地 heartbeat 文件（gitignore），
    # 不进提交的 state.json —— 否则每小时一次 commit 刷屏 main。
    heartbeat_file = Path(state_file).parent / ".firsthand-heartbeat.json"
    heartbeat = load_state(heartbeat_file)
    all_new = []
    for source in sources:
        sid = source["id"]
        st = state.setdefault(sid, {})
        st.pop("last_checked", None)  # 迁移：旧版把 last_checked 存这里，现移到 heartbeat
        heartbeat[sid] = now
        try:
            fetched = fetch_fn(source)
            st["last_fetch_ok"] = True
            st["last_fetch_error"] = None
        except Exception as e:
            st["last_fetch_ok"] = False
            st["last_fetch_error"] = str(e)
            continue
        ingested = ingested_urls(okf_root, sid)
        open_pr = set(st.get("open_pr_urls", []))
        # 去重唯一真相 = OKF 文件。有 OKF 文件永远不是首刊；
        # 否则看显式 initialized flag（与 open_pr / known_urls_count 解耦，
        # 避免 state 部分损坏时误开历史全量 PR）。
        first_run = not ingested and not st.get("initialized")
        new_articles = diff_new_articles(fetched, ingested, open_pr)
        if first_run:
            st["open_pr_urls"] = [a["url"] for a in fetched]
            st["initialized"] = True
            continue
        st["known_urls_count"] = len(ingested) + len(open_pr)
        for art in new_articles:
            all_new.append((source, art))

    new_count = 0
    if all_new:
        # 先为每篇定真实发布日期，再按 published 升序写 → OKF 序号前缀 = 发布序。
        # 真实发布日期：优先列表页带的（engineering），否则去文章页取（claude-blog JSON-LD）。
        for source, art in all_new:
            published = art.get("published")
            if not published:
                try:
                    published = article_published_fn(art["url"])
                except Exception:
                    published = None
            art["published"] = published
        all_new.sort(key=lambda sa: sa[1].get("published") or "9999-99-99")

        pr_articles = []
        for source, art in all_new:
            text = article_text_fn(art["url"])
            # html-links 适配器不带标题 → 去文章页取 <h1>/<title>；失败回退 URL
            title = art.get("title")
            if not title:
                try:
                    title = article_title_fn(art["url"])
                except Exception:
                    title = None
            title = title or art["url"]
            published = art.get("published")
            s = summarize_fn(title, text)
            article = {
                "title": title,
                "source": source["id"],
                "url": art["url"],
                "summary": s["summary"],
                "summary_error": s.get("error"),  # 摘要失败原因（成功为 None）→ 进 OKF/PR
                "tags": s["tags"],
                "published": published,     # 真实发布日期（取不到则 None，不写入文件）
                "detected": now,            # 探测时间（诚实标注）
                "full_text": text,          # 原文备份，避免链接失效/访问受限时云端无内容可用
            }
            write_okf(okf_root, article)
            pr_articles.append((source["id"], article))
        # 当天一个 PR：分支固定 firsthand/<date>；当天后续批次追加 commit + 评论 @user（见 _real_open_pr）
        branch = f"firsthand/{now[:10]}"
        pr_ok = True
        if open_pr_fn:
            try:
                open_pr_fn(branch, [a for _, a in pr_articles])
            except Exception as e:
                # 开 PR 失败不崩整轮：不标记已见 → 下一轮自动重试（OKF 已在分支，不丢内容）
                pr_ok = False
                print(f"[firsthand] open_pr 失败，本批留待下轮重试: {e}")
        if pr_ok:
            for sid, article in pr_articles:
                state[sid].setdefault("open_pr_urls", []).append(article["url"])
                state[sid]["last_new_article"] = now
            new_count = len(pr_articles)

    save_state(state_file, state)
    save_state(heartbeat_file, heartbeat)  # 本地心跳，不提交
    if commit_state_fn:
        commit_state_fn()
    return {"new_count": new_count}


def _existing_open_pr(branch: str) -> str:
    """当天分支若已有 open PR，返回其编号，否则空串。"""
    r = subprocess.run(
        ["gh", "pr", "list", "--head", branch, "--state", "open",
         "--json", "number", "--jq", ".[0].number // empty"],
        cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip()


def _real_open_pr(branch, articles):
    """当天累积一个 PR：
    - 当天已有 open PR → checkout 该分支、追加 OKF commit、push（PR 自动更新）、评论 @user 通知；
    - 当天还没有 → 新建分支 + PR（reviewer=yinjialu）。
    无论中途是否抛异常都切回 main，避免无人值守循环卡在 firsthand 分支。
    push 是关键步骤（check=True）；label/评论是尽力而为（check=False），失败不影响去重标记。"""
    by_source = {}
    for a in articles:
        by_source.setdefault(a["source"], []).append(a)
    counts = ", ".join(f"{k} {len(v)}篇" for k, v in by_source.items())
    body = render_pr_body(articles)
    try:
        pr_num = _existing_open_pr(branch)
        if pr_num:
            # 更新模式：切到已有分支，追加本批 OKF
            subprocess.run(["git", "fetch", "origin", branch], cwd=REPO, check=True)
            subprocess.run(["git", "checkout", "-B", branch, f"origin/{branch}"],
                           cwd=REPO, check=True)
            subprocess.run(["git", "add", "data/firsthand/"], cwd=REPO, check=True)
            subprocess.run(["git", "commit", "-m", f"firsthand: 新增 ({counts})"],
                           cwd=REPO, check=True)
            subprocess.run(["git", "push", "origin", branch], cwd=REPO, check=True)
            # 评论里 @user → 触发提醒通知（尽力而为，失败不影响）
            subprocess.run(["gh", "pr", "comment", pr_num,
                            "--body", f"@yinjialu 🆕 本日内参新增（{counts}）：\n\n{body}"],
                           cwd=REPO, check=False)
        else:
            # 新建模式
            subprocess.run(["git", "checkout", "-B", branch], cwd=REPO, check=True)
            subprocess.run(["git", "add", "data/firsthand/"], cwd=REPO, check=True)
            subprocess.run(["git", "commit", "-m", f"firsthand: 内参新动态 {branch}"],
                           cwd=REPO, check=True)
            subprocess.run(["git", "push", "-u", "origin", branch], cwd=REPO, check=True)
            title = f"📡 内参新动态 | {branch.split('/')[-1]} ({counts})"
            # 确保 label 存在（缺则建，幂等，失败不影响）
            subprocess.run(["gh", "label", "create", "firsthand-intel",
                            "--color", "1f6feb", "--description", "一手信源内参监控"],
                           cwd=REPO, check=False)
            subprocess.run(
                ["gh", "pr", "create", "--title", title, "--body", body,
                 "--reviewer", "yinjialu", "--label", "firsthand-intel", "--base", "main"],
                cwd=REPO, check=True,
            )
    finally:
        subprocess.run(["git", "checkout", "main"], cwd=REPO, check=False)


def _real_commit_state():
    """state.json + 索引产物(index.json/feed.xml)直接提交 main（本机无 403）。
    索引从 main 的 OKF 重建,内容不变则字节一致 → 不产生提交,不刷屏。"""
    try:
        from scripts.firsthand.index import write_outputs
        write_outputs(DEFAULT_OKF_ROOT)
    except Exception as e:
        print(f"[firsthand] 索引生成失败(忽略): {e}")
    subprocess.run(["git", "add", "data/firsthand-state.json",
                    "data/firsthand/index.json", "data/firsthand/feed.xml"],
                   cwd=REPO, check=False)
    r = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO)
    if r.returncode != 0:
        subprocess.run(["git", "commit", "-m", "chore: firsthand state + index"], cwd=REPO, check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO, check=False)


HEARTBEAT_ISSUE_TITLE = "📡 firsthand 监控心跳"
HEARTBEAT_ISSUE_LABEL = "firsthand-heartbeat"


def _ensure_heartbeat_issue() -> str:
    """找到或创建心跳 issue，返回 issue number（字符串）。"""
    r = subprocess.run(
        ["gh", "issue", "list", "--label", HEARTBEAT_ISSUE_LABEL,
         "--state", "open", "--json", "number", "--jq", ".[0].number // empty"],
        cwd=REPO, capture_output=True, text=True)
    num = r.stdout.strip()
    if num:
        return num
    # 确保 label 存在
    subprocess.run(
        ["gh", "label", "create", HEARTBEAT_ISSUE_LABEL,
         "--color", "0075ca", "--description", "firsthand 监控心跳"],
        cwd=REPO, check=False, capture_output=True)
    r2 = subprocess.run(
        ["gh", "issue", "create",
         "--title", HEARTBEAT_ISSUE_TITLE,
         "--label", HEARTBEAT_ISSUE_LABEL,
         "--body", "此 Issue 由监控脚本自动维护，记录每次 firsthand 监控的执行结果。"],
        cwd=REPO, capture_output=True, text=True, check=True)
    # 输出形如 https://github.com/owner/repo/issues/123
    import re
    m = re.search(r"/issues/(\d+)", r2.stdout)
    return m.group(1) if m else ""


def _post_heartbeat(now: str, new_count: int, error: str | None = None):
    """更新心跳 issue 的唯一评论为最新状态。失败静默，不影响主流程。"""
    import datetime, json
    try:
        issue_num = _ensure_heartbeat_issue()
        if not issue_num:
            return
        dt = datetime.datetime.fromisoformat(now)
        next_str = (dt + datetime.timedelta(hours=1)).strftime("%H:%M")
        if error:
            body = (
                f"### ❌ 执行失败 `{now}`\n\n"
                f"```\n{error[:1000]}\n```\n\n"
                f"下次检测：约 {next_str}"
            )
        elif new_count > 0:
            body = (
                f"### ✅ `{now}` — 发现 {new_count} 条新内容\n\n"
                f"已开 PR，下次检测：约 {next_str}"
            )
        else:
            body = (
                f"### ✅ `{now}` — 无新内容\n\n"
                f"各信源均无更新，下次检测：约 {next_str}"
            )
        # 找现有评论 → 编辑；没有则新建
        r = subprocess.run(
            ["gh", "api", f"repos/{{owner}}/{{repo}}/issues/{issue_num}/comments",
             "--jq", ".[0].id // empty"],
            cwd=REPO, capture_output=True, text=True)
        comment_id = r.stdout.strip()
        if comment_id:
            subprocess.run(
                ["gh", "api", "--method", "PATCH",
                 f"repos/{{owner}}/{{repo}}/issues/comments/{comment_id}",
                 "-f", f"body={body}"],
                cwd=REPO, check=False, capture_output=True)
        else:
            subprocess.run(
                ["gh", "issue", "comment", issue_num, "--body", body],
                cwd=REPO, check=False, capture_output=True)
    except Exception as e:
        print(f"[firsthand] 心跳评论失败(忽略): {e}")


def main():
    import datetime, time
    tz8 = datetime.timezone(datetime.timedelta(hours=8))
    start_dt = datetime.datetime.now(tz8)
    now = start_dt.isoformat(timespec="seconds")
    t0 = time.monotonic()

    print(f"[firsthand] START {now}")

    # --autostash：监控与交互会话共用本仓工作目录，pull 前自动 stash 未提交改动、
    # pull 完再恢复，避免脏工作树时 `pull --rebase` 硬失败（state 提交滞留）。
    subprocess.run(["git", "pull", "--rebase", "--autostash", "origin", "main"], cwd=REPO, check=False)

    error_msg = None
    new_count = 0
    try:
        result = run_once(
            DEFAULT_SOURCES, DEFAULT_OKF_ROOT, DEFAULT_STATE, now,
            open_pr_fn=_real_open_pr, commit_state_fn=_real_commit_state,
        )
        new_count = result["new_count"]
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"[firsthand] ERROR {now}: {e}")

    elapsed = round(time.monotonic() - t0)
    status = "ERROR" if error_msg else "OK"
    print(f"[firsthand] END {now} status={status} new={new_count} elapsed={elapsed}s")

    _post_heartbeat(now, new_count, error=error_msg)


if __name__ == "__main__":
    main()
