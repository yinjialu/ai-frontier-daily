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
    "gemini":    {"name": "Gemini", "brand": "AI 前哨 · 每日 Gemini",
                  "outroDesc": "持续追踪 Google Gemini 模型发布、API 更新与 DeepMind 研究。点个关注，明天见。"},
    "nvidia":    {"name": "NVIDIA", "brand": "AI 前哨 · 每日 NVIDIA",
                  "outroDesc": "持续追踪 NVIDIA AI 芯片/平台发布、CUDA 与推理软件、重大合作。点个关注，明天见。"},
    # 聚合轨：把多家国内大模型公司汇成一条轨，每条 update 带 company 标注来源公司。
    "cn":        {"name": "国产大模型", "brand": "AI 前哨 · 每日国产大模型",
                  "outroDesc": "持续追踪 DeepSeek、通义、智谱、Kimi、豆包、文心、混元、MiniMax 等国内大模型官方发布。点个关注，明天见。"},
}

# 每条轨道单期最多条数：单品牌厂商 6 条；聚合轨（多家公司）放宽到 10 条。
VENDOR_CAP = {"cn": 10}
def _cap(vendor): return VENDOR_CAP.get(vendor, 6)

# 聚合轨 id（每条动态需额外标注来源公司 company）。
AGG_VENDORS = {"cn"}

def _system_prompt(vendor):
    name = VENDOR_META.get(vendor, VENDOR_META["anthropic"])["name"]
    cap, agg = _cap(vendor), vendor in AGG_VENDORS
    if agg:
        # 聚合轨：输入混合多家国内公司，需逐条标注来源公司，并跨公司择优。
        company_rule = ("\n   - company（来源公司中文名，如 DeepSeek/通义千问/智谱/Kimi/豆包/文心/混元/"
                        "MiniMax/阶跃星辰/百川/零一万物/百灵，**聚合轨必填**）；")
        intro = (f"""你是「{name}」每日动态中文内容编辑。输入是今天抓到的若干条**国内多家大模型公司**官方动态原文，"""
                 f"""可能来自 DeepSeek、阿里通义、智谱、月之暗面 Kimi、字节豆包、百度文心、腾讯混元、MiniMax、"""
                 f"""阶跃星辰、百川、零一万物、蚂蚁百灵等。请跨公司统一择优。""")
    else:
        company_rule, intro = "", f"你是「{name} 动态」中文内容编辑。输入是今天抓到的若干条 {name} 官方动态原文。"
    return f"""{intro}
任务：1) 价值筛选：只保留对中文 AI 从业者有价值的条目（模型发布、能力更新、重要研究、重大合作、定价/政策变化），过滤纯招聘/行政/地区办公室开设等低价值信息。
2) 分类打标签：每条给一个标签，从【模型发布/开发者/企业/研究/生态/政策/安全】中选。
3) 中文摘要：每条 50~80 字，客观说清「变了什么+对用户意味着什么」，不夸张、不编造数据。
4) 排序：按重要性降序，最多 {cap} 条。
5) 严格输出 JSON（无多余文字、无 markdown 代码块）；今天无值得发的内容则输出 {{"skip":true,"reason":"..."}}。
   每条 update 含字段：tag（标签）、title（中文标题）、summary（中文摘要）、{company_rule}
   source（原文域名，如 {name.lower()}.com）、url（该条对应原文的完整链接，
   必须从输入原文里**原样复制 url 字段**，禁止改写或编造；找不到就留空字符串）。
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
        "brand": meta["brand"], "updates": updates[:_cap(vendor)],
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
                    "source": re.sub(r"^https?://(www\.)?", "", it["url"]).split("/")[0] or it["source"],
                    "url": it["url"]})
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
    # 原文链接防幻觉：只信任「在本次抓取的 items 里真实出现过」的 url，否则清空 → 渲染退回域名首页兜底。
    valid = {it["url"] for it in items if it.get("url")}
    for u in data.get("updates", []):
        if u.get("url") not in valid:
            u["url"] = ""
        if not u.get("source") and u.get("url"):
            u["source"] = re.sub(r"^https?://(www\.)?", "", u["url"]).split("/")[0]
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
