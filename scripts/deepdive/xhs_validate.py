#!/usr/bin/env python3
"""校验小红书卡片脚本 xhs.json 是否满足平台与版式硬约束。

用法：python -m scripts.deepdive.xhs_validate <xhs.json>
不过线打印错误并退出码 1。
"""
import json
import sys
from pathlib import Path

TITLE_MAX = 20
CAPTION_MAX = 1000
CARDS_MIN, CARDS_MAX = 4, 8
HEADING_MAX = 14
HEADING_LINES_MAX = 2
LINES_MAX = 4
LINE_MAX = 22
TAGS_MIN, TAGS_MAX = 1, 10


def _count(x) -> str:
    """安全取长度供报错展示：非字符串/列表时不抛异常，标「非文本」。"""
    return str(len(x)) if isinstance(x, (str, list)) else "非文本"


def validate_xhs(data: dict) -> list[str]:
    errors: list[str] = []
    title = data.get("title", "")
    if not isinstance(title, str) or len(title) > TITLE_MAX:
        errors.append(f"标题需 ≤{TITLE_MAX} 字（当前 {_count(title)}）")
    caption = data.get("caption", "")
    if not isinstance(caption, str) or len(caption) > CAPTION_MAX:
        errors.append(f"文案需 ≤{CAPTION_MAX} 字（当前 {_count(caption)}）")
    cards = data.get("cards")
    if not isinstance(cards, list) or not (CARDS_MIN <= len(cards) <= CARDS_MAX):
        errors.append(f"卡片数需 {CARDS_MIN}~{CARDS_MAX} 张（当前 {_count(cards)}）")
        cards = cards if isinstance(cards, list) else []
    for i, c in enumerate(cards):
        if not isinstance(c, dict):
            errors.append(f"卡片{i} 必须是对象（含 heading/lines）")
            continue
        h = c.get("heading", "")
        heading_lines = h.splitlines() if isinstance(h, str) else []
        if (
            not isinstance(h, str)
            or not heading_lines
            or len(heading_lines) > HEADING_LINES_MAX
            or any(len(line) > HEADING_MAX for line in heading_lines)
        ):
            errors.append(f"卡片{i} heading 需 ≤{HEADING_MAX} 字（当前 {_count(h)}）")
        lines = c.get("lines")
        if "kind" not in c and "quote" not in c and "image" not in c:
            if not isinstance(lines, list) or len(lines) > LINES_MAX:
                errors.append(f"卡片{i} 行数需 ≤{LINES_MAX}（当前 {_count(lines)}）")
                lines = lines if isinstance(lines, list) else []
            for j, ln in enumerate(lines):
                if not isinstance(ln, str) or len(ln) > LINE_MAX:
                    errors.append(f"卡片{i} 第{j}行 每行需 ≤{LINE_MAX} 字（当前 {_count(ln)}）")
    tags = data.get("tags")
    if not isinstance(tags, list) or not (TAGS_MIN <= len(tags) <= TAGS_MAX):
        errors.append(f"tags 需 {TAGS_MIN}~{TAGS_MAX} 个")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("用法：python -m scripts.deepdive.xhs_validate <xhs.json>", file=sys.stderr)
        return 2
    data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    errors = validate_xhs(data)
    if errors:
        print("✗ xhs.json 校验未过：", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        return 1
    print("✓ xhs.json 校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
