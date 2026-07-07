#!/usr/bin/env python3
"""Preflight checks for the AI Frontier publishing chain.

The doctor is intentionally read-only. It validates local prerequisites before
daily digest generation, WeChat draft creation, Xiaohongshu card rendering, and
Pages deployment checks.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""
    required: bool = True


def _run(cmd: list[str], timeout: int = 20) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=timeout)


def _command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def _file_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def _tcp_dns(host: str) -> tuple[bool, str]:
    try:
        socket.getaddrinfo(host, 443)
        return True, "dns ok"
    except OSError as exc:
        return False, str(exc)


def _compact_output(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Error:") or stripped.startswith("ModuleNotFoundError"):
            return stripped
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("at "):
            return stripped
    return text.strip()


def check_daily() -> list[Check]:
    checks: list[Check] = []
    py = REPO / ".venv" / "bin" / "python"
    python_cmd = str(py) if py.exists() else sys.executable
    checks.append(Check("python", True, python_cmd))

    try:
        proc = _run([python_cmd, "skills/ai-daily-digest/run.py", "--vendors"], timeout=20)
        vendors = json.loads(proc.stdout) if proc.returncode == 0 else []
        checks.append(Check("daily vendors", bool(vendors), f"{len(vendors)} vendors"))
    except Exception as exc:  # noqa: BLE001 - diagnostic script
        checks.append(Check("daily vendors", False, str(exc)))

    checks.append(Check("render env script", _file_exists(REPO / "scripts/ensure-daily-render-env.sh")))
    checks.append(Check("node", _command_exists("node"), shutil.which("node") or "missing"))

    try:
        proc = _run(["node", "-e", "require('playwright'); console.log('playwright ok')"], timeout=20)
        checks.append(Check(
            "playwright module",
            proc.returncode == 0,
            _compact_output(proc.stdout or proc.stderr) or "run scripts/ensure-daily-render-env.sh",
            required=False,
        ))
    except Exception as exc:  # noqa: BLE001
        checks.append(Check("playwright module", False, str(exc), required=False))

    checks.append(Check("daily guard", os.access(REPO / "scripts/guard-daily-content-commit.sh", os.X_OK)))
    return checks


def check_wechat() -> list[Check]:
    cfg = Path.home() / ".config/wechat-official-draft/config.yaml"
    dns_ok, dns_detail = _tcp_dns("api.weixin.qq.com")
    return [
        Check("wechat config", _file_exists(cfg), str(cfg)),
        Check("wechat api dns", dns_ok, dns_detail),
        Check(
            "wechat newspic script",
            _file_exists(REPO / "skills/ai-daily-digest/publish_wechat_newspic.py"),
        ),
    ]


def check_xhs() -> list[Check]:
    return [
        Check("xhs validator", _file_exists(REPO / "scripts/deepdive/xhs_validate.py")),
        Check("xhs renderer", _file_exists(REPO / "scripts/deepdive/render_xhs.py")),
        Check("node", _command_exists("node"), shutil.which("node") or "missing"),
    ]


def check_pages() -> list[Check]:
    checks: list[Check] = []
    idx = REPO / "output/index.json"
    if not idx.exists():
        checks.append(Check("pages index", False, "output/index.json missing"))
    else:
        try:
            data = json.loads(idx.read_text(encoding="utf-8"))
            updated = data.get("updated")
            days = [d for d in data.get("days", []) if d.get("date") == updated]
            checks.append(Check("pages index", bool(updated and days), f"updated={updated} entries={len(days)}"))
        except Exception as exc:  # noqa: BLE001
            checks.append(Check("pages index", False, str(exc)))
    checks.append(Check("pages workflow", _file_exists(REPO / ".github/workflows/pages-deploy.yml")))
    checks.append(Check("publish page", _file_exists(REPO / "publish.html")))
    return checks


CHECKS = {
    "daily": check_daily,
    "wechat": check_wechat,
    "xhs": check_xhs,
    "pages": check_pages,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stage",
        action="append",
        choices=sorted(CHECKS),
        help="stage to check; repeatable. default: all stages",
    )
    args = parser.parse_args(argv)
    stages = args.stage or ["daily", "wechat", "xhs", "pages"]

    failed = False
    for stage in stages:
        print(f"[{stage}]")
        for check in CHECKS[stage]():
            marker = "✓" if check.ok else ("✗" if check.required else "!")
            print(f"  {marker} {check.name}{(': ' + check.detail) if check.detail else ''}")
            failed = failed or (check.required and not check.ok)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
