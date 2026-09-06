'use strict';
const $ = s => document.querySelector(s);
const DAY_MS = 864e5;
const DAILY = '__daily__';
const NAMES = Object.fromEntries(Object.entries(window.Cards.VENDORS).map(([id,v])=>[id,v.name]));
const VC = {anthropic:'#dfa684',openai:'#74d6b3',gemini:'#8daaff',nvidia:'#b5ef69',cn:'#f08f87'};
const TAG_ORDER = ['模型发布','开发者','企业','研究','生态','政策','安全'];
const esc = value => String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeURL = value => {try{const u=new URL(value);return /^https?:$/.test(u.protocol)?u.href:null;}catch{return null;}};
const iso = date => date.toISOString().slice(0,10);
const parseISO = date => new Date(`${date}T00:00:00Z`);
const storeGet = key => {try{return localStorage.getItem(key);}catch{return null;}};
const storeSet = (key,value) => {try{localStorage.setItem(key,value);}catch{}};
let ALL=[], DAYS=[], byDate={}, present=[], curVendor=DAILY, curDate=null, curTag='全部', viewMode='feed', curStyle=storeGet('card_style')==='glass'?'glass':'', car=null, loadId=0, currentData=[], failedVendors=[];
let period=7, feedPage=0, pageSize=4, pageItems=[], filteredCount=0;
const dataCache=new Map();
async function fetchJSON(url){const r=await fetch(url,{cache:'no-cache'});if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();}
async function dayData(vendor,date){const key=`${vendor}|${date}`;if(!dataCache.has(key)){const request=fetchJSON(`data/${encodeURIComponent(vendor)}/${date}.json`).then(data=>{if(!Array.isArray(data.updates))throw new Error('Invalid updates');return data;}).catch(error=>{dataCache.delete(key);throw error;});dataCache.set(key,request);}return dataCache.get(key);}
async function init(){
 try{
 const idx=await fetchJSON('output/index.json');
 ALL=(idx.days||[]).map(d=>({...d,vendor:d.vendor||'anthropic'})).filter(d=>/^\d{4}-\d{2}-\d{2}$/.test(d.date)&&/^[a-z0-9_-]+$/.test(d.vendor));
 ALL.sort((a,b)=>a.date.localeCompare(b.date));
 if(!ALL.length){$('#archiveNotice').textContent='公开归档暂无内容';$('#app').innerHTML='<div class="empty">第一道信号即将到来。公开日报发布后会出现在这里。</div>';$('#app').setAttribute('aria-busy','false');return;}
 const order=Object.keys(NAMES);present=[...new Set(ALL.map(d=>d.vendor))].sort((a,b)=>(order.indexOf(a)<0?99:order.indexOf(a))-(order.indexOf(b)<0?99:order.indexOf(b)));
 $('#channelCount').textContent=String(present.length).padStart(2,'0');
 $('#vendors').innerHTML=[DAILY,...present].map(v=>`<button class="vtab" data-v="${esc(v)}" style="--vc:${VC[v]||'#b5f76b'}" aria-pressed="false"><span class="dotv"></span>${v===DAILY?'全部信号':esc(NAMES[v]||v)}</button>`).join('');
 const latest=ALL.at(-1).date;
 $('#archiveNotice').textContent=`公开归档更新至 ${latest} · 此看板展示已发布内容，服务器巡检状态尚未接入。`;
 $('#archiveCount').textContent=new Set(ALL.map(d=>d.date)).size;
 $('#archiveRange').textContent=`${ALL[0].date.slice(5).replace('-','.')} — ${latest.slice(5).replace('-','.')}`;
 await applyVendor(DAILY);
 }catch{
 $('#archiveNotice').textContent='公开归档暂时无法读取';
 $('#app').innerHTML='<div class="empty">连接没有完成，请稍后重新读取。<button id="retryInit">重新读取</button></div>';
 $('#app').setAttribute('aria-busy','false');$('#retryInit').onclick=init;
 }
}
async function applyVendor(vendor){
 if(vendor!==DAILY&&!present.includes(vendor))return;
 curVendor=vendor;curTag='全部';viewMode='feed';feedPage=0;
 document.querySelectorAll('.vtab').forEach(el=>{const on=el.dataset.v===vendor;el.classList.toggle('on',on);el.setAttribute('aria-pressed',String(on));});
 const records=ALL.filter(d=>vendor===DAILY||d.vendor===vendor);
 DAYS=[...new Set(records.map(d=>d.date))].sort().map(date=>({date,count:records.filter(d=>d.date===date).reduce((n,d)=>n+(Number(d.count)||0),0)}));
 byDate=Object.fromEntries(DAYS.map(d=>[d.date,d]));
 $('#dateSelect').innerHTML=DAYS.slice().reverse().map(d=>`<option value="${d.date}">${d.date} ${d.date===DAYS.at(-1).date?'· 最新归档':''}</option>`).join('');
 $('#feedTitle').textContent=vendor===DAILY?'信号流':`${NAMES[vendor]||vendor} 动态`;
 $('#viewSwitch').hidden=vendor===DAILY;
 await selectDay(byDate[curDate]?curDate:DAYS.at(-1).date);
}
async function selectDay(date){
 if(!byDate[date])return;
 curDate=date;curTag='全部';car=null;feedPage=0;
 const token=++loadId;
 $('#dateSelect').value=date;
 const index=DAYS.findIndex(d=>d.date===date);$('#prevDay').disabled=index===0;$('#nextDay').disabled=index===DAYS.length-1;
 $('#app').setAttribute('aria-busy','true');$('#app').innerHTML='<div class="empty">正在读取这一天的信号…</div>';
 $('#meta').textContent='';$('#categories').innerHTML='';
 ['signalCount','modelCount','activeCount','feedCount'].forEach(id=>$('#'+id).textContent='—');
 $('#radarBlips').innerHTML='';$('#distribution').innerHTML='';
 renderHeatmap();
 const start=iso(new Date(parseISO(date).getTime()-(period-1)*DAY_MS));
 const records=ALL.filter(d=>d.date>=start&&d.date<=date).sort((a,b)=>b.date.localeCompare(a.date));
 const results=await Promise.allSettled(records.map(async r=>({vendor:r.vendor,dd:await dayData(r.vendor,r.date)})));
 if(token!==loadId)return;
 currentData=results.filter(r=>r.status==='fulfilled').map(r=>r.value);
 failedVendors=[...new Set(results.flatMap((r,i)=>r.status==='rejected'?[records[i].vendor]:[]))];
 updateDashboard();renderContent();$('#app').setAttribute('aria-busy','false');
}
function itemsForSelection(){return currentData.filter(d=>curVendor===DAILY||d.vendor===curVendor).flatMap(({vendor,dd})=>dd.updates.map(u=>({...u,vendor,archiveDate:dd.date})));}
function fitLayout(){
 const area=$('#app');const width=area.clientWidth||800,height=area.clientHeight||440;
 const cols=width>=1150?3:width>=650?2:1;
 const rows=Math.max(1,Math.min(3,Math.floor(height/205)));
 const lines=Math.max(1,Math.min(9,Math.floor((height/rows-130)/25)));
 area.style.setProperty('--feed-cols',cols);area.style.setProperty('--feed-rows',rows);area.style.setProperty('--summary-lines',lines);
 pageSize=cols*rows;
}
function renderContent(){
 car=null;
 const relevantFailures=failedVendors.filter(v=>curVendor===DAILY||v===curVendor);
 const items=itemsForSelection();
 $('#styles').hidden=viewMode!=='cards';$('#categories').hidden=viewMode==='cards';
 document.querySelectorAll('[data-view]').forEach(b=>{b.classList.toggle('on',b.dataset.view===viewMode);b.setAttribute('aria-pressed',String(b.dataset.view===viewMode));});
 document.querySelectorAll('[data-period]').forEach(b=>{b.classList.toggle('on',+b.dataset.period===period);b.setAttribute('aria-pressed',String(+b.dataset.period===period));});
 const start=iso(new Date(parseISO(curDate).getTime()-(period-1)*DAY_MS));
 $('#meta').textContent=relevantFailures.length?`${relevantFailures.map(v=>NAMES[v]||v).join('、')} 读取失败 · 当前内容不完整`:`${period===7?start+' — ':''}${curDate} · ${curVendor===DAILY?'跨厂商归档':NAMES[curVendor]||curVendor}`;
 if(!items.length){$('#app').innerHTML=`<div class="empty">${relevantFailures.length?'本期内容未能加载。<button id="retryDay">重新读取</button>':'所选范围没有已发布的动态。'}</div>`;if($('#retryDay'))$('#retryDay').onclick=()=>selectDay(curDate);$('#feedCount').textContent='0';filteredCount=0;updatePagination();return;}
 if(viewMode==='cards')return renderCards();
 const tags=['全部',...TAG_ORDER.filter(t=>items.some(u=>u.tag===t)),...[...new Set(items.map(u=>u.tag||'其他'))].filter(t=>!TAG_ORDER.includes(t))];
 $('#categories').innerHTML=tags.map(t=>`<button data-tag="${esc(t)}" class="${curTag===t?'on':''}" aria-pressed="${curTag===t}">${esc(t)}<span>${t==='全部'?items.length:items.filter(u=>(u.tag||'其他')===t).length}</span></button>`).join('');
 const filtered=items.filter(u=>curTag==='全部'||(u.tag||'其他')===curTag).sort((a,b)=>{const dateOrder=b.archiveDate.localeCompare(a.archiveDate);if(dateOrder)return dateOrder;const rank=t=>TAG_ORDER.includes(t)?TAG_ORDER.indexOf(t):99;return rank(a.tag)-rank(b.tag);});
 $('#feedCount').textContent=filtered.length;
 fitLayout();filteredCount=filtered.length;feedPage=Math.min(feedPage,Math.max(0,Math.ceil(filteredCount/pageSize)-1));pageItems=filtered.slice(feedPage*pageSize,(feedPage+1)*pageSize);
 $('#app').innerHTML='<div class="digest">'+pageItems.map((u,i)=>{
 const url=safeURL(u.url)||safeURL(u.source)||safeURL(window.Cards.srcHref(u));const domain=url?new URL(url).hostname.replace(/^www\./,''):'';
 return `<article class="ditem"><div class="dbd"><div class="item-kicker"><span class="vbadge" style="--vc:${VC[u.vendor]||'#b5f76b'}"><span class="vdot"></span>${esc(u.company||NAMES[u.vendor]||u.vendor)}</span><span class="tag-badge ${u.tag==='模型发布'?'release':''}">${esc(u.tag||'其他')}</span><time class="item-date" datetime="${esc(u.archiveDate)}">${esc(u.archiveDate.slice(5).replace('-','.'))}</time></div><h3>${esc(u.title)}</h3><p>${esc(u.summary)}</p><div class="dsrc">${url?`<a href="${esc(url)}" target="_blank" rel="noopener noreferrer" title="${esc(domain)}">原文 ↗<span class="sr-only">：${esc(u.title)}</span></a>`:'<span>暂无原文</span>'}<button class="detail-button" data-detail="${i}">展开详情 ↗<span class="sr-only">：${esc(u.title)}</span></button></div></div></article>`;
 }).join('')+'</div>';
 updatePagination();
}
function updatePagination(){const pages=Math.max(1,Math.ceil(filteredCount/pageSize));$('#pageLabel').textContent=`${String(feedPage+1).padStart(2,'0')} / ${String(pages).padStart(2,'0')}`;$('#pageRange').textContent=filteredCount?`第 ${feedPage*pageSize+1}—${Math.min((feedPage+1)*pageSize,filteredCount)} 条 / 共 ${filteredCount} 条`:'暂无信号';$('#prevPage').disabled=feedPage===0;$('#nextPage').disabled=feedPage>=pages-1;$('.pagination').hidden=viewMode==='cards';}
function updateDashboard(){
 const items=itemsForSelection();
 $('#archiveState').textContent=failedVendors.length?`${failedVendors.length} 个频道读取异常`:'当前范围已载入';
 $('#signalCount').textContent=items.length;$('#signalDate').textContent=`${curDate} · ${curVendor===DAILY?'全部频道':'所选频道'}`;
 $('#modelCount').textContent=items.filter(u=>u.tag==='模型发布').length;
 const active=new Set(items.map(u=>u.vendor)).size;$('#activeCount').textContent=String(active).padStart(2,'0');
 $('#activeCaption').textContent=failedVendors.length?`${failedVendors.length} 个频道读取失败`:`共 ${present.length} 个公开归档频道`;
 const counts=currentData.reduce((out,{vendor,dd})=>{out[vendor]=(out[vendor]||0)+dd.updates.length;return out;},{});
 const max=Math.max(1,...Object.values(counts));
 $('#distribution').innerHTML=present.map(v=>`<button class="distribution-row" data-v="${esc(v)}" style="--vc:${VC[v]||'#b5f76b'}" aria-label="查看 ${esc(NAMES[v]||v)}"><span class="distribution-name"><i></i>${esc(NAMES[v]||v)}</span><span class="distribution-track"><i style="width:${(counts[v]||0)/max*100}%"></i></span><span>${failedVendors.includes(v)?'!':counts[v]||0}</span></button>`).join('');
 $('#radarBlips').innerHTML=present.map((v,i)=>{const n=counts[v]||0;if(!n)return '';const a=(i/present.length*360-110)*Math.PI/180;const radius=25+(i%3)*8;return `<button class="radar-blip" data-v="${esc(v)}" style="left:${50+Math.cos(a)*radius}%;top:${50+Math.sin(a)*radius}%;--vc:${VC[v]||'#b5f76b'};--size:${5+n/max*4}px" title="${esc(NAMES[v]||v)} · ${n} 条" aria-label="${esc(NAMES[v]||v)}：${curDate}，${n} 条动态"><i></i></button>`;}).join('');
 const recent=DAYS.filter(d=>d.date<=curDate).slice(-16);const peak=Math.max(1,...recent.map(d=>d.count));
 $('#activityBars').innerHTML=recent.map(d=>`<i style="height:${Math.max(3,d.count/peak*28)}px"></i>`).join('');
}
function renderHeatmap(){
 // Twelve full calendar weeks ending with the selected archive week, independent of local timezone.
 const end=parseISO(curDate);end.setUTCDate(end.getUTCDate()+(6-end.getUTCDay()));
 const start=new Date(end.getTime()-83*DAY_MS);
 const days=Array.from({length:84},(_,i)=>iso(new Date(start.getTime()+i*DAY_MS)));
 const peak=Math.max(1,...days.map(d=>byDate[d]?.count||0));
 $('#cal').innerHTML=days.map(date=>{const d=byDate[date];const count=d?.count||0;const level=count?Math.max(1,Math.ceil(count/peak*4)):0;return `<button class="cell l${level}${date===curDate?' sel':''}" data-d="${date}" ${d?'':'disabled'} ${date===curDate?'aria-current="date"':''} title="${date} · ${d?count+' 条':'无归档'}" aria-label="${date}，${d?count+' 条动态，查看归档':'无归档'}"></button>`;}).join('');
 $('#heatHint').textContent=`${days[0].slice(5).replace('-','.')} — ${days.at(-1).slice(5).replace('-','.')} · ${curVendor===DAILY?'全部频道':NAMES[curVendor]||curVendor}`;
}
function renderCards(){
 const selected=currentData.find(d=>d.vendor===curVendor);if(!selected)return;
 let deck;try{deck=window.Cards.buildDeck({...selected.dd,style:curStyle}).filter(c=>/\bxhs\b/.test(c.cls));}catch{$('#app').innerHTML='<div class="empty">本期卡片暂时无法生成，请切回动态阅读。</div>';return;}
 $('#feedCount').textContent=deck.length;
 $('#app').innerHTML=`<div class="carousel" id="carousel"><div class="stage" id="stage">${deck.map((c,i)=>`<div class="card3d" data-i="${i}" role="button" tabindex="0" aria-label="查看第 ${i+1} 张卡片"><div class="card ${c.cls} deckcard">${c.inner}</div></div>`).join('')}</div><button class="nav prev" id="navPrev" aria-label="上一张卡片">‹</button><button class="nav next" id="navNext" aria-label="下一张卡片">›</button></div><div class="dots" id="dots">${deck.map((_,i)=>`<button class="dot" data-i="${i}" aria-label="第 ${i+1} 张卡片"></button>`).join('')}</div>`;
 initCarousel(deck);
 $('.pagination').hidden=true;$('#pageRange').textContent=`${curDate} · ${deck.length} 张发布卡片`;
 $('#stage').onkeydown=e=>{if(e.key==='Enter'||e.key===' '){const el=e.target.closest('.card3d');if(el){e.preventDefault();openCard(+el.dataset.i);}}};
}
function initCarousel(deck){
  const stage = $("#stage");
  car = { cards:[...stage.children], active:0, deck };
  dealIn();                       // 切换日期：洗牌发牌入场

  $("#navPrev").onclick = ()=> goCar(car.active-1);
  $("#navNext").onclick = ()=> goCar(car.active+1);
  $("#dots").onclick = e => { const t=e.target.closest(".dot"); if(t) goCar(+t.dataset.i); };
  stage.onclick = e => {
    const c = e.target.closest(".card3d"); if(!c) return;
    const i = +c.dataset.i;
    if(i===car.active) openCard(i);   // 点中间 → 放大
    else goCar(i);                    // 点两侧 → 转过去
  };

  let x0=null;
  const down = e => { x0 = (e.touches?e.touches[0]:e).clientX; };
  const up = e => {
    if(x0===null || !car) return;
    const x1 = (e.changedTouches?e.changedTouches[0]:e).clientX;
    if(Math.abs(x1-x0) > 40) goCar(car.active + (x1<x0?1:-1));
    x0=null;
  };
  stage.addEventListener("touchstart", down, {passive:true});
  stage.addEventListener("touchend", up);
  stage.addEventListener("mousedown", down);
  window.onmouseup = up;
}

function goCar(i){
  if(!car) return;
  car.active = Math.max(0, Math.min(car.cards.length-1, i));
  layoutCarousel();               // 左右翻看：平滑 coverflow 过渡
}

// 把单张卡片摆到 coverflow 目标位
function placeCard(el, i){
  const stageW = ($("#carousel")||{}).clientWidth || 600;
  const spread = Math.min(180, stageW*0.28);
  const dd = i - car.active, ad = Math.abs(dd);
  el.classList.toggle("active", dd===0);
  if(ad>3){
    el.style.opacity = 0; el.style.pointerEvents = "none";
    el.style.transform = `translate(-50%,-50%) translateX(${dd*60}px) translateZ(-700px)`;
    return;
  }
  el.style.opacity = 1 - ad*0.16;
  el.style.pointerEvents = "auto";
  el.style.zIndex = 20 - ad;
  el.style.filter = ad ? `brightness(${1-ad*0.08})` : "none";
  el.style.transform = `translate(-50%,-50%) translateX(${dd*spread}px) `+
    `translateZ(${-ad*140}px) rotateY(${-dd*44}deg) scale(${1-ad*0.05})`;
}

function updateDots(){
  document.querySelectorAll("#dots .dot").forEach((el,i)=>
    {el.classList.toggle("on", i===car.active);el.setAttribute('aria-pressed',String(i===car.active));});
  $("#navPrev").disabled=car.active===0;
  $("#navNext").disabled=car.active===car.cards.length-1;
}

// 翻看（同一天内）：直接过渡，无错位延迟
function layoutCarousel(){
  if(!car) return;
  const width=Math.min(268,Math.max(120,(($('#carousel')?.clientHeight||400)-24)*.75),($('#carousel')?.clientWidth||600)*.68);
  car.cards.forEach(el=>el.style.setProperty('--cw',Math.floor(width)));
  car.cards.forEach((el,i)=>{ el.style.transitionDelay = "0ms"; placeCard(el,i); });
  updateDots();
}

// 切换日期入场：先叠成一摞「洗牌」，再依次发牌散开
function dealIn(){
  if(!car) return;
  const n = car.cards.length, mid = (n-1)/2;
  car.cards.forEach((el,i)=>{
    el.style.transition = "none";
    el.style.transitionDelay = "0ms";
    el.style.zIndex = 50 - Math.abs(i-car.active);
    el.style.opacity = Math.abs(i-car.active) > 3 ? 0 : 1;
    el.style.filter = "none";
    el.style.transform = `translate(-50%,-50%) translateY(48px) `+
      `rotate(${(i-mid)*4}deg) scale(.8)`;            // 叠成一摞微扇形
  });
  void $("#stage").offsetWidth;                        // 强制 reflow 固化初始态
  requestAnimationFrame(()=>{
    if(!car) return;                                   // 入场动画排队期间已切到日报/别处（car 置空），跳过
    car.cards.forEach((el,i)=>{
      el.style.transition = "";                        // 恢复 CSS 过渡
      el.style.transitionDelay = (Math.min(Math.abs(i-car.active),4)*60)+"ms";  // 由中心向外错位发牌
      placeCard(el,i);
    });
    updateDots();
    setTimeout(()=>{ if(car) car.cards.forEach(el=>el.style.transitionDelay="0ms"); }, 900);
  });
}

const box=$('#box'),boxStage=$('#boxStage');
function openCard(index){if(!car?.deck[index])return;const c=car.deck[index];const scale=Math.min(window.innerHeight*.90/1440,window.innerWidth*.92/1080);boxStage.style.width=1080*scale+'px';boxStage.style.height=1440*scale+'px';boxStage.innerHTML=`<div class="card ${c.cls} deckcard" style="transform:scale(${scale})">${c.inner}</div>`;if(!box.open)box.showModal();}
function closeBox(){box.close();boxStage.innerHTML='';}
$('#closeBox').onclick=closeBox;box.onclick=e=>{if(e.target===box)closeBox();};
window.addEventListener('resize',()=>{layoutCarousel();if(box.open&&car)openCard(car.active);});
document.addEventListener('keydown',e=>{if(box.open||/^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName))return;if(car&&e.key==='ArrowLeft')goCar(car.active-1);if(car&&e.key==='ArrowRight')goCar(car.active+1);});
$('#vendors').onclick=e=>{const el=e.target.closest('[data-v]');if(el)applyVendor(el.dataset.v);};
$('#distribution').onclick=$('#radarBlips').onclick=e=>{const el=e.target.closest('[data-v]');if(el){const date=curDate;applyVendor(el.dataset.v).then(()=>{if(curDate!==date)$('#meta').textContent+=' · 所选日无该频道归档，已显示最近一期';});}};
$('#dateSelect').onchange=e=>selectDay(e.target.value);
$('#prevDay').onclick=()=>{const i=DAYS.findIndex(d=>d.date===curDate);if(i>0)selectDay(DAYS[i-1].date);};
$('#nextDay').onclick=()=>{const i=DAYS.findIndex(d=>d.date===curDate);if(i<DAYS.length-1)selectDay(DAYS[i+1].date);};
$('#categories').onclick=e=>{const el=e.target.closest('[data-tag]');if(el){curTag=el.dataset.tag;feedPage=0;renderContent();}};
$('#viewSwitch').onclick=e=>{const el=e.target.closest('[data-view]');if(el){viewMode=el.dataset.view;if(viewMode==='cards'&&period!==1){period=1;selectDay(curDate);}else renderContent();}};
$('#periodSwitch').onclick=e=>{const el=e.target.closest('[data-period]');if(el){period=+el.dataset.period;if(period===7)viewMode='feed';selectDay(curDate);}};
$('#prevPage').onclick=()=>{if(feedPage>0){feedPage--;renderContent();}};
$('#nextPage').onclick=()=>{if((feedPage+1)*pageSize<filteredCount){feedPage++;renderContent();}};
$('#statusToggle').onclick=()=>{const open=$('#statusPanel').hidden;$('#statusPanel').hidden=!open;document.body.classList.toggle('status-open',open);$('#statusToggle').setAttribute('aria-expanded',String(open));$('#statusToggle').innerHTML=`◎ 信源与雷达 <span>${open?'收起 ↙':'展开 ↗'}</span>`;requestAnimationFrame(()=>{if(viewMode==='feed')renderContent();else layoutCarousel();});};
$('#app').onclick=e=>{const button=e.target.closest('[data-detail]');if(!button)return;const u=pageItems[+button.dataset.detail];if(!u)return;$('#detailMeta').textContent=`${u.company||NAMES[u.vendor]||u.vendor} / ${u.tag||'其他'} / 归档 ${u.archiveDate}`;$('#detailTitle').textContent=u.title;$('#detailSummary').textContent=u.summary;const url=safeURL(u.url)||safeURL(u.source)||safeURL(window.Cards.srcHref(u));$('#detailSource').hidden=!url;if(url)$('#detailSource').href=url;$('#detailDialog').showModal();};
$('#closeDetail').onclick=()=>$('#detailDialog').close();
$('#detailDialog').onclick=e=>{if(e.target===$('#detailDialog'))$('#detailDialog').close();};
if(typeof ResizeObserver!=='undefined'){new ResizeObserver(()=>{if(currentData.length&&viewMode==='feed')renderContent();}).observe($('#app'));}
$('#cal').onclick=e=>{const el=e.target.closest('[data-d]');if(el&&!el.disabled)selectDay(el.dataset.d);};
$('#styles').onclick=e=>{const el=e.target.closest('[data-s]');if(el){curStyle=el.dataset.s;storeSet('card_style',curStyle);syncStyle();renderContent();}};
function syncStyle(){document.querySelectorAll('.stab').forEach(el=>{el.classList.toggle('on',el.dataset.s===curStyle);el.setAttribute('aria-pressed',String(el.dataset.s===curStyle));});}syncStyle();
let motionPaused=storeGet('radar_motion')==='paused'||window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function syncMotion(){document.body.classList.toggle('motion-paused',motionPaused);$('#motionToggle').setAttribute('aria-pressed',String(motionPaused));$('#motionToggle').setAttribute('aria-label',motionPaused?'播放雷达动画':'暂停雷达动画');$('#motionToggle').textContent=motionPaused?'▷':'Ⅱ';}syncMotion();
$('#motionToggle').onclick=()=>{motionPaused=!motionPaused;storeSet('radar_motion',motionPaused?'paused':'playing');syncMotion();};
function updateClock(){$('#clock').textContent='UTC+8 '+new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Shanghai',hour:'2-digit',minute:'2-digit'}).format(new Date());}updateClock();setInterval(updateClock,30000);
init();
