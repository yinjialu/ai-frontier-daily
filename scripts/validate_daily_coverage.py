#!/usr/bin/env python3
"""Validate the daily digest's research coverage ledger.

The Claude-driven path uses WebFetch/WebSearch outside Python, so this ledger
is the machine-checkable handoff between research and curation. It prevents a
vendor (especially one company inside the cn aggregate track) from silently
being skipped.

Usage:
  python3 scripts/validate_daily_coverage.py --init --date 2026-07-18
  python3 scripts/validate_daily_coverage.py --check --date 2026-07-18
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "skills" / "ai-daily-digest" / "daily-search-matrix.json"


def _vendors() -> list[str]:
    proc = subprocess.run(
        [sys.executable, "skills/ai-daily-digest/run.py", "--vendors"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    return [item["id"] for item in json.loads(proc.stdout)]


def _path(date: str) -> Path:
    return ROOT / "output" / "daily-research" / f"{date}.json"


def _template(date: str) -> dict:
    vendors = _vendors()
    cn = json.loads(MATRIX.read_text("utf-8"))["cn_companies"]
    result = {
        "coverage_version": 1,
        "date": date,
        "timezone": "Asia/Shanghai",
        "vendors": {},
    }
    for vendor in vendors:
        result["vendors"][vendor] = {
            "official_search": [],
            "firsthand_query": {
                "command": f"python3 -m scripts.firsthand.query --vendor {vendor} --days 2 --json --include-open-prs",
                "status": "pending",
                "candidate_count": None,
            },
        }
    result["vendors"]["cn"]["official_search"] = {
        company: {"queries": [], "sources": []} for company in cn
    }
    return result


def _valid_url(value: object) -> bool:
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def _check_entry(vendor: str, entry: dict, errors: list[str]) -> None:
    official = entry.get("official_search")
    if vendor == "cn":
        required = json.loads(MATRIX.read_text("utf-8"))["cn_companies"]
        if not isinstance(official, dict):
            errors.append("cn.official_search 必须按公司记录逐家搜索")
        else:
            for company in required:
                item = official.get(company)
                if not isinstance(item, dict):
                    errors.append(f"cn 缺少公司搜索记录：{company}")
                    continue
                if not item.get("queries"):
                    errors.append(f"cn 未搜索：{company}")
                if not item.get("sources"):
                    errors.append(f"cn 未记录来源：{company}")
                for source in item.get("sources", []):
                    if source != "none-found" and not _valid_url(source):
                        errors.append(f"cn {company} 来源不是 URL 或 none-found：{source}")
    elif not isinstance(official, list) or not official:
        errors.append(f"{vendor} 缺少官方搜索记录")
    else:
        for i, item in enumerate(official):
            if not isinstance(item, dict) or not item.get("queries"):
                errors.append(f"{vendor}.official_search[{i}] 缺少 query")
            for source in (item.get("sources", []) if isinstance(item, dict) else []):
                if source != "none-found" and not _valid_url(source):
                    errors.append(f"{vendor} 来源不是 URL 或 none-found：{source}")

    query = entry.get("firsthand_query")
    if not isinstance(query, dict):
        errors.append(f"{vendor} 缺少 firsthand_query 记录")
        return
    command = query.get("command", "")
    for token in ("--vendor", vendor, "--days 2", "--json", "--include-open-prs"):
        if token not in command:
            errors.append(f"{vendor}.firsthand_query.command 缺少 {token}")
    if query.get("status") not in {"completed", "not-applicable"}:
        errors.append(f"{vendor}.firsthand_query.status 必须是 completed 或 not-applicable")
    if query.get("status") == "completed" and not isinstance(query.get("candidate_count"), int):
        errors.append(f"{vendor}.firsthand_query.candidate_count 必须是整数")


def check(date: str) -> int:
    path = _path(date)
    errors: list[str] = []
    if not path.exists():
        print(f"覆盖校验失败：缺少 {path}", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text("utf-8"))
    except Exception as exc:
        print(f"覆盖校验失败：无法解析 {path}: {exc}", file=sys.stderr)
        return 1
    expected = _vendors()
    if data.get("coverage_version") != 1:
        errors.append("coverage_version 必须为 1")
    if data.get("date") != date:
        errors.append(f"date 应为 {date}")
    actual = data.get("vendors")
    if not isinstance(actual, dict):
        errors.append("vendors 必须是对象")
        actual = {}
    for vendor in expected:
        entry = actual.get(vendor)
        if not isinstance(entry, dict):
            errors.append(f"缺少厂商覆盖记录：{vendor}")
        else:
            _check_entry(vendor, entry, errors)
    for vendor in actual:
        if vendor not in expected:
            errors.append(f"存在未知厂商覆盖记录：{vendor}")
    if errors:
        print("覆盖校验失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"覆盖校验通过：{date}，已完成 {len(expected)} 条厂商轨道（cn 含逐家公司记录）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.init == args.check:
        ap.error("必须且只能选择 --init 或 --check")
    path = _path(args.date)
    if args.init:
        if path.exists():
            print(f"拒绝覆盖已有覆盖记录：{path}", file=sys.stderr)
            return 1
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_template(args.date), ensure_ascii=False, indent=2) + "\n", "utf-8")
        print(f"已生成覆盖记录模板：{path}")
        return 0
    return check(args.date)


if __name__ == "__main__":
    raise SystemExit(main())
