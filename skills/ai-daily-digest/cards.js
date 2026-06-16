/* 卡片构建逻辑：唯一真源。浏览器（预览页）与 Node（渲染器）共用。
   buildDeck(DATA) -> [{name, cls, w, h, inner}]   h 为 null 表示高度自适应。
   多厂商：DATA.vendor（anthropic|openai，缺省 anthropic）决定品牌文案与主题 class，
   主题色由 cards.css 的 .v-<vendor> 作用域覆盖语义 token 实现，版式厂商无关。*/
(function (root) {
  function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;");}
  function escAttr(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/"/g,"&quot;");}
  function pad(n){return String(n).padStart(2,"0");}

  // 来源链接：优先用原文 url；缺 url 时退回 https://<域名> 兜底到官网首页；都没有则纯文本。
  // 渲染成 <a> 时样式继承父级、无下划线（见 cards.css .srclink），导出的图片视觉零变化；
  // 仅展示页可点，hover 才显下划线。
  function srcHref(u){
    var url = (u && u.url || "").trim();
    if(/^https?:\/\//i.test(url)) return url;
    var s = (u && u.source || "").trim();
    if(/^[\w.-]+\.[a-z]{2,}/i.test(s)) return "https://" + s.split("/")[0];
    return "";
  }
  function srcHTML(u){
    var label = esc(u && u.source), href = srcHref(u);
    return href
      ? `<a class="srclink" href="${escAttr(href)}" target="_blank" rel="noopener noreferrer">${label}</a>`
      : label;
  }

  // 厂商注册表：新增厂商在此加一项 + 在 cards.css 加 .v-<id> 主题即可。
  // 聚合轨（如 cn 国产大模型）把多家公司汇成一条轨，每条 update 带 company 字段标注来源公司，
  // 渲染成公司徽标（org chip）；单品牌厂商不带 company，徽标自动不渲染。
  var VENDORS = {
    anthropic: {id:"anthropic", name:"Anthropic", daily:"Anthropic Daily", label:"ANTHROPIC DAILY"},
    openai:    {id:"openai",    name:"OpenAI",    daily:"OpenAI Daily",    label:"OPENAI DAILY"},
    gemini:    {id:"gemini",    name:"Gemini",    daily:"Gemini Daily",    label:"GEMINI DAILY"},
    nvidia:    {id:"nvidia",    name:"NVIDIA",    daily:"NVIDIA Daily",    label:"NVIDIA DAILY"},
    cn:        {id:"cn",        name:"国产大模型", daily:"China LLM Daily", label:"国产大模型 · 每日"},
  };
  function vendorOf(DATA){ return VENDORS[(DATA && DATA.vendor) || "anthropic"] || VENDORS.anthropic; }

  // 风格层（正交于 vendor 主题）：DATA.style==="glass"/"liquid-glass" → 追加 style-glass class。
  // 经典版不带 style 字段 → 返回空串，产出与历史像素一致。渲染器可用 CARD_STYLE 覆盖 DATA.style。
  function styleClass(DATA){
    var s = (DATA && DATA.style || "").toLowerCase();
    return (s === "glass" || s === "liquid-glass" || s === "liquidglass") ? " style-glass" : "";
  }

  // 公司徽标：聚合轨里标注该条来自哪家公司（DeepSeek / 通义 …）。无 company 字段则返回空串。
  function orgChip(u){ var c = u && u.company; return c ? `<span class="org">${esc(c)}</span>` : ""; }

  // 小红书内容卡是固定 1080×1440 + overflow:hidden，长文案会被裁切。
  // 按标题/摘要字数分档，给卡片附加 t1..t4 / s1..s4 class（见 cards.css），
  // 自适应缩小字号让文字容得下；短文案不附 class，保持原始大字号美观。
  // 纯字数判定 → 确定性、跨环境（预览页/playwright/wkhtml）一致，无需运行时测量。
  function fitClass(title, summary){
    var t = String(title==null?"":title).length, s = String(summary==null?"":summary).length;
    var tc = t<=22?"" : t<=34?"t1" : t<=48?"t2" : t<=64?"t3" : "t4";
    var sc = s<=110?"" : s<=165?"s1" : s<=220?"s2" : s<=275?"s3" : "s4";
    return (tc + " " + sc).trim();
  }

  function buildDeck(DATA){
    var out=[], U=DATA.updates||[], V=vendorOf(DATA), vc="v-"+V.id, sc=styleClass(DATA);

    // 小红书封面
    out.push({name:"小红书_00_封面", cls:vc+" xhs xhs-cover", w:1080, h:1440, inner:`
      <div class="blob" style="width:440px;height:440px;background:var(--accent-soft);top:-120px;right:-100px"></div>
      <div class="blob" style="width:220px;height:220px;background:var(--accent);bottom:520px;left:-80px;opacity:.45"></div>
      <div class="inner">
        <div class="topbar"><span class="edition">${esc(DATA.edition)}</span><span class="date">${esc(DATA.date)}</span></div>
        <div class="kicker">${esc(V.daily)}</div>
        <h1>今天 ${esc(V.name)}<br>又<em>更新</em>了什么</h1>
        <div class="teasers">
          ${U.slice(0,3).map((u,i)=>`<div class="teaser"><span class="n">${i+1}</span><span>${u.company?`<b class="tco">${esc(u.company)}</b> `:""}${esc(u.title)}</span></div>`).join("")}
        </div>
        <div class="footer"><span>${esc(DATA.brand)}</span><span>${esc(DATA.cnDate)}</span></div>
      </div>`});

    // 小红书内容卡
    U.forEach(function(u,i){
      out.push({name:"小红书_"+pad(i+1)+"_"+esc(u.tag), cls:(vc+" xhs xhs-item "+fitClass(u.title,u.summary)).trim(), w:1080, h:1440, inner:`
        <div class="blob" style="width:300px;height:300px;background:var(--accent-soft);top:-90px;right:-90px;opacity:.5"></div>
        <div class="bgnum">${pad(i+1)}</div>
        <div class="inner">
          <div class="head">
            <span class="edition">${esc(V.label)} · ${esc(DATA.edition)}</span>
            <span class="pager"><b>${pad(i+1)}</b> / ${pad(U.length)}</span>
          </div>
          <div class="body">
            <div class="tags"><span class="tag">${esc(u.tag)}</span>${orgChip(u)}</div>
            <h2>${esc(u.title)}</h2>
            <div class="rule"></div>
            <div class="sum">${esc(u.summary)}</div>
          </div>
          <div class="src"><span>来源 ${srcHTML(u)}</span><span>${esc(DATA.brand)}</span></div>
        </div>`});
    });

    // 小红书结尾卡
    out.push({name:"小红书_99_结尾", cls:vc+" xhs xhs-outro", w:1080, h:1440, inner:`
      <div class="blob" style="width:400px;height:400px;background:var(--accent);bottom:-120px;right:-100px;opacity:.4"></div>
      <div class="inner">
        <div class="mark">— that's a wrap</div>
        <h2>${esc(DATA.outroTitle).replace(/\n/g,"<br>")}</h2>
        <p>${esc(DATA.outroDesc)}</p>
        <span class="cta">${esc(DATA.outroCta)}</span>
      </div>`});

    // 公众号封面
    out.push({name:"公众号_封面_900x383", cls:vc+" gzh-cover", w:900, h:383, inner:`
      <div class="blob" style="width:340px;height:340px;background:var(--accent);top:-130px;right:140px;opacity:.45"></div>
      <div class="inner">
        <div class="row"><span>${esc(DATA.edition)} · ${esc(V.label)}</span><span>${esc(DATA.date)}</span></div>
        <h1>${esc(V.name)} 今日<em> 速递</em></h1>
        <div class="sub">${esc(DATA.cnDate)} · 共 ${U.length} 条更新 · ${esc(DATA.brand)}</div>
      </div>`});

    // 公众号正文长图（高度自适应）
    out.push({name:"公众号_正文长图", cls:vc+" gzh-body", w:900, h:null, inner:`
      <div class="inner">
        <div class="head">Today's Briefing · ${esc(DATA.date)}</div>
        <h2>今日要点</h2>
        <div class="gline"></div>
        ${U.map((u,i)=>`
          <div class="e">
            <div class="num">${pad(i+1)}</div>
            <div class="bd"><span class="tag">${esc(u.tag)}</span>${orgChip(u)}<h3>${esc(u.title)}</h3>
              <p>${esc(u.summary)}</p><div class="s">↗ ${srcHTML(u)}</div></div>
          </div>`).join("")}
        <div class="foot"><span>${esc(DATA.brand)}</span><span>${esc(DATA.cnDate)}</span></div>
      </div>`});

    // 正交风格层：统一给每张卡片 cls 追加 style class（经典版 sc 为空，无影响）
    if (sc) out.forEach(function(c){ c.cls += sc; });

    return out;
  }

  root.Cards = { buildDeck: buildDeck, VENDORS: VENDORS, srcHTML: srcHTML, srcHref: srcHref };
  if (typeof module !== "undefined" && module.exports) module.exports = root.Cards;
})(typeof window !== "undefined" ? window : globalThis);
