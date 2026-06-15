#!/usr/bin/env python3
"""把当天 data/<vendor>/<date>.json 整理成「小红书发布素材包」。

用法：
  python to_xhs_post.py                          # 默认 anthropic
  python to_xhs_post.py --vendor openai          # 指定厂商
  python to_xhs_post.py data/openai/2026-06-02.json  # 指定文件

产出：
  - output/<vendor>/<date>/小红书文案.txt  供人工核对
  - stdout 打印 JSON：{date, vendor, title, content, tags, images}
"""
import sys, os, json, re
from pathlib import Path

OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())

VENDOR_META = {
    "anthropic": {"name": "Anthropic", "base_tags": ["#AI", "#Anthropic", "#Claude"]},
    "openai":    {"name": "OpenAI",    "base_tags": ["#AI", "#OpenAI", "#ChatGPT"]},
    "gemini":    {"name": "Gemini",    "base_tags": ["#AI", "#Google", "#Gemini"]},
    "nvidia":    {"name": "NVIDIA",    "base_tags": ["#AI", "#NVIDIA", "#GPU"]},
    "cn":        {"name": "国产大模型", "base_tags": ["#AI", "#国产大模型", "#大模型"]},
}

# 更新 tag 字段 → 话题标签
_TAG_FIELD_MAP = {
    "模型发布": "#大模型",
    "开发者":   "#AI开发者",
    "研究":     "#AI研究",
    "政策":     "#AI政策",
    "安全":     "#AI安全",
    "生态":     "#AI生态",
    "企业":     "#AI应用",
}

# 标题/摘要关键词 → 额外话题标签
_KEYWORD_TAGS = [
    (r"Codex",         "#Codex"),
    (r"Sora",          "#Sora"),
    (r"TensorRT",      "#TensorRT"),
    (r"Dynamo",        "#Dynamo"),
    (r"Gemini CLI",    "#GeminiCLI"),
    (r"Claude Code",   "#ClaudeCode"),
    (r"NeMo",          "#NeMo"),
    (r"Agent SDK",     "#ClaudeCode"),
    (r"Antigravity",   "#Antigravity"),
]


def build_tags(vendor, updates):
    """内容自适应标签：厂商基础标签 + 文章话题标签，共最多 5 个。"""
    meta = VENDOR_META.get(vendor, VENDOR_META["anthropic"])
    base = list(meta["base_tags"])
    extra = []

    seen = set(base)
    for u in updates:
        # 按 tag 字段映射
        t = _TAG_FIELD_MAP.get(u.get("tag", ""))
        if t and t not in seen:
            extra.append(t); seen.add(t)
        # 按关键词扫描
        text = (u.get("title", "") + " " + u.get("summary", ""))
        for pattern, tag in _KEYWORD_TAGS:
            if re.search(pattern, text) and tag not in seen:
                extra.append(tag); seen.add(tag)

    # 基础标签全保留 + 额外最多 2 个（总数不超 5）
    combined = base + extra[: max(0, 5 - len(base))]
    return " ".join(combined)


def build(data):
    vendor = data.get("vendor", "anthropic")
    updates = data.get("updates", [])
    meta = VENDOR_META.get(vendor, VENDOR_META["anthropic"])
    name = meta["name"]
    brand = data.get("brand", f"AI 前哨 · 每日 {name}")
    cn_date = data.get("cnDate", "")  # e.g. "6月14日 周日"

    # 标题：cnDate｜厂商 今日 N 条动态（手动发布不受 20 字硬限制）
    title = f"{cn_date}｜{name} 今日 {len(updates)} 条动态"

    # 正文：编号 + 标签 + 标题 + 摘要，每条空行分隔
    lines = []
    for i, u in enumerate(updates, 1):
        lines.append(f"{i}.【{u.get('tag', '')}】{u.get('title', '')}")
        lines.append(u.get("summary", ""))
        lines.append("")

    tags = build_tags(vendor, updates)
    lines.append(f"—— {brand}，点关注不错过 🔔 {tags}")
    content = "\n".join(lines).strip()

    return title, content, tags


def _arg_value(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def _positional():
    out, skip = [], False
    for a in sys.argv[1:]:
        if skip: skip = False; continue
        if a == "--vendor": skip = True; continue
        if a.startswith("--"): continue
        out.append(a)
    return out


def main():
    args = _positional()
    vendor = _arg_value("--vendor", "anthropic")
    if args:
        data_file = Path(args[0]); date = data_file.stem
        vendor = data_file.parent.name if data_file.parent.name in VENDOR_META else vendor
    else:
        latest = json.loads((OUT / "output" / vendor / "latest.json").read_text("utf-8"))
        date = latest["dir"]; data_file = OUT / "data" / vendor / f"{date}.json"

    data = json.loads(data_file.read_text("utf-8"))
    vendor = data.get("vendor", vendor)
    out_dir = OUT / "output" / vendor / date

    title, content, tags = build(data)
    images = [str(p) for p in sorted(out_dir.glob("小红书_*"))
              if p.suffix.lower() in (".png", ".jpg", ".jpeg")]

    txt = (f"【标题】\n{title}\n\n"
           f"【正文（含标签）】\n{content}\n\n"
           f"【配图】（按此顺序上传，共 {len(images)} 张）\n" +
           "\n".join(f"  {i+1}. {os.path.basename(p)}" for i, p in enumerate(images)) + "\n")
    (out_dir / "小红书文案.txt").write_text(txt, "utf-8")

    print(json.dumps({"date": date, "vendor": vendor, "title": title,
                      "content": content, "tags": tags, "images": images},
                     ensure_ascii=False))
    print(f"✓ {out_dir/'小红书文案.txt'}（{len(images)} 张配图）", file=sys.stderr)


if __name__ == "__main__":
    main()
