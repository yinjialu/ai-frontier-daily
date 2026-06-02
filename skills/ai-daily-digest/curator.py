"""策展+摘要：把采集到的原文整理成渲染器需要的 DATA(json)。
- live 模式：调 Claude API（需环境变量 ANTHROPIC_API_KEY），用固定 system prompt 出 JSON
- mock 模式：离线启发式整理（无需联网/密钥），用于本地跑通
"""
import os, json, datetime, re

# 厂商元信息：品牌名 + 结尾文案。新增厂商在此加一项即可。
VENDOR_META = {
    "anthropic": {"name": "Anthropic", "brand": "AI 前哨 · 每日 Anthropic",
                  "outroDesc": "持续追踪 Anthropic 官方发布、工程博客、研究与更新日志。点个关注，明天见。"},
    "openai":    {"name": "OpenAI", "brand": "AI 前哨 · 每日 OpenAI",
                  "outroDesc": "持续追踪 OpenAI 官方发布、Codex、API 更新与研究。点个关注，明天见。"},
}

def _system_prompt(vendor):
    name = VENDOR_META.get(vendor, VENDOR_META["anthropic"])["name"]
    return f"""你是「{name} 动态」中文内容编辑。输入是今天抓到的若干条 {name} 官方动态原文。
任务：1) 价值筛选：只保留对中文 AI 从业者有价值的条目（模型发布、能力更新、重要研究、重大合作、定价/政策变化），过滤纯招聘/行政/地区办公室开设等低价值信息。
2) 分类打标签：每条给一个标签，从【模型发布/开发者/企业/研究/生态/政策/安全】中选。
3) 中文摘要：每条 50~80 字，客观说清「变了什么+对用户意味着什么」，不夸张、不编造数据。
4) 排序：按重要性降序，最多 6 条。
5) 严格输出 JSON（无多余文字、无 markdown 代码块），字段见下；今天无值得发的内容则输出 {{"skip":true,"reason":"..."}}。
严禁逐字复制英文长句；摘要必须是你自己的中文转写。"""

def _today():
    d = datetime.date.today()
    wd = "一二三四五六日"[d.weekday()]
    return d.strftime("%Y.%m.%d"), f"{d.month}月{d.day}日 周{wd}"

def _wrap(updates, vendor="anthropic"):
    date, cn = _today()
    meta = VENDOR_META.get(vendor, VENDOR_META["anthropic"])
    return {
        "vendor": vendor,
        "date": date, "cnDate": cn, "edition": "VOL." + datetime.date.today().strftime("%j"),
        "brand": meta["brand"], "updates": updates[:6],
        "outroTitle": "每天一条\n看懂 AI 大厂动向",
        "outroDesc": meta["outroDesc"],
        "outroCta": "关注 · 不错过任何更新",
    }

# ---- 离线启发式（mock） ----
_TAGS = [("模型发布", ["opus","sonnet","haiku","model","发布","upgrade"]),
         ("开发者", ["code","sdk","api","developer","workflow"]),
         ("企业", ["enterprise","agent","managed","sandbox","企业"]),
         ("研究", ["research","paper","interpretab","safety research"]),
         ("生态", ["acqui","partner","integrat","收购","合作"]),
         ("政策", ["policy","regulat","政策"])]

def _tag(text):
    t = text.lower()
    for tag, kws in _TAGS:
        if any(k in t for k in kws):
            return tag
    return "生态"

def _mock(items, vendor="anthropic"):
    ups = []
    for it in items:
        raw = re.sub(r"\s+", " ", it["raw"]).strip()
        summary = (raw[:78] + "…") if len(raw) > 80 else raw
        ups.append({"tag": _tag(it["title"] + " " + raw), "title": it["title"],
                    "summary": summary or "（待补充摘要）",
                    "source": re.sub(r"^https?://(www\.)?", "", it["url"]).split("/")[0] or it["source"]})
    return _wrap(ups, vendor)

# ---- Claude API（live） ----
def _live(items, vendor="anthropic"):
    import urllib.request
    payload = {
        "model": "claude-opus-4-8", "max_tokens": 2000,
        "system": _system_prompt(vendor),
        "messages": [{"role": "user", "content":
            "今天抓到的原文：\n" + json.dumps(items, ensure_ascii=False, indent=2) +
            "\n\n请按要求输出 DATA JSON（含 date/cnDate/edition/brand/updates/outro* 字段）。"}],
    }
    req = urllib.request.Request("https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                 "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read())
    text = "".join(b.get("text", "") for b in resp["content"])
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(text)
    if data.get("skip"):
        return data
    # 补齐缺失的固定字段
    base = _wrap(data.get("updates", []), vendor)
    base.update({k: v for k, v in data.items() if v})
    base["vendor"] = vendor                       # vendor 以参数为准，不被模型输出覆盖
    return base

def curate(items, mock=True, vendor="anthropic"):
    if not items:
        return {"skip": True, "reason": "今日无新动态"}
    return _mock(items, vendor) if mock else _live(items, vendor)

if __name__ == "__main__":
    import sys, collector
    v = sys.argv[1] if len(sys.argv) > 1 else "anthropic"
    print(json.dumps(curate(collector.collect(mock=True, vendor=v), mock=True, vendor=v), ensure_ascii=False, indent=2))
