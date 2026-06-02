/* 卡片构建逻辑：唯一真源。浏览器（预览页）与 Node（渲染器）共用。
   buildDeck(DATA) -> [{name, cls, w, h, inner}]   h 为 null 表示高度自适应。
   多厂商：DATA.vendor（anthropic|openai，缺省 anthropic）决定品牌文案与主题 class，
   主题色由 cards.css 的 .v-<vendor> 作用域覆盖语义 token 实现，版式厂商无关。*/
(function (root) {
  function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;");}
  function pad(n){return String(n).padStart(2,"0");}

  // 厂商注册表：新增厂商在此加一项 + 在 cards.css 加 .v-<id> 主题即可。
  var VENDORS = {
    anthropic: {id:"anthropic", name:"Anthropic", daily:"Anthropic Daily", label:"ANTHROPIC DAILY"},
    openai:    {id:"openai",    name:"OpenAI",    daily:"OpenAI Daily",    label:"OPENAI DAILY"},
  };
  function vendorOf(DATA){ return VENDORS[(DATA && DATA.vendor) || "anthropic"] || VENDORS.anthropic; }

  function buildDeck(DATA){
    var out=[], U=DATA.updates||[], V=vendorOf(DATA), vc="v-"+V.id;

    // 小红书封面
    out.push({name:"小红书_00_封面", cls:vc+" xhs xhs-cover", w:1080, h:1440, inner:`
      <div class="blob" style="width:440px;height:440px;background:var(--accent-soft);top:-120px;right:-100px"></div>
      <div class="blob" style="width:220px;height:220px;background:var(--accent);bottom:520px;left:-80px;opacity:.45"></div>
      <div class="inner">
        <div class="topbar"><span class="edition">${esc(DATA.edition)}</span><span class="date">${esc(DATA.date)}</span></div>
        <div class="kicker">${esc(V.daily)}</div>
        <h1>今天 ${esc(V.name)}<br>又<em>更新</em>了什么</h1>
        <div class="teasers">
          ${U.slice(0,3).map((u,i)=>`<div class="teaser"><span class="n">${i+1}</span><span>${esc(u.title)}</span></div>`).join("")}
        </div>
        <div class="footer"><span>${esc(DATA.brand)}</span><span>${esc(DATA.cnDate)}</span></div>
      </div>`});

    // 小红书内容卡
    U.forEach(function(u,i){
      out.push({name:"小红书_"+pad(i+1)+"_"+esc(u.tag), cls:vc+" xhs xhs-item", w:1080, h:1440, inner:`
        <div class="blob" style="width:300px;height:300px;background:var(--accent-soft);top:-90px;right:-90px;opacity:.5"></div>
        <div class="bgnum">${pad(i+1)}</div>
        <div class="inner">
          <div class="head">
            <span class="edition">${esc(V.label)} · ${esc(DATA.edition)}</span>
            <span class="pager"><b>${pad(i+1)}</b> / ${pad(U.length)}</span>
          </div>
          <div class="body">
            <span class="tag">${esc(u.tag)}</span>
            <h2>${esc(u.title)}</h2>
            <div class="rule"></div>
            <div class="sum">${esc(u.summary)}</div>
          </div>
          <div class="src"><span>来源 ${esc(u.source)}</span><span>${esc(DATA.brand)}</span></div>
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
            <div class="bd"><span class="tag">${esc(u.tag)}</span><h3>${esc(u.title)}</h3>
              <p>${esc(u.summary)}</p><div class="s">↗ ${esc(u.source)}</div></div>
          </div>`).join("")}
        <div class="foot"><span>${esc(DATA.brand)}</span><span>${esc(DATA.cnDate)}</span></div>
      </div>`});

    return out;
  }

  root.Cards = { buildDeck: buildDeck, VENDORS: VENDORS };
  if (typeof module !== "undefined" && module.exports) module.exports = root.Cards;
})(typeof window !== "undefined" ? window : globalThis);
