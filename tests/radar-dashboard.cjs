const vm=require('node:vm');
const fs=require('node:fs');
const assert=require('node:assert/strict');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
process.chdir(root);
const elements=new Map();
function element(selector){if(!elements.has(selector))elements.set(selector,{innerHTML:'',textContent:'',dataset:{},style:{setProperty(){}},classList:{toggle(){}},setAttribute(){},addEventListener(){},querySelectorAll(){return[];}});return elements.get(selector);}
// Freeze the historical fixture window so future daily publications do not alter expectations.
const index=JSON.parse(fs.readFileSync('output/index.json'));
index.days=index.days.filter(d=>d.date<='2026-08-11');
const ctx={console,URL,Intl,Date,Map,Set,Promise,localStorage:{getItem(){throw Error('blocked');},setItem(){throw Error('blocked');}},setInterval(){},setTimeout(){},requestAnimationFrame(){},document:{querySelector:element,querySelectorAll(){return[];},body:element('body'),addEventListener(){}},window:{Cards:require(path.join(root,'skills/ai-daily-digest/cards.js')),matchMedia(){return {matches:false};},addEventListener(){}},fetch:async url=>({ok:true,json:async()=>url==='output/index.json'?index:JSON.parse(fs.readFileSync(path.join(root,url),'utf8'))})};
vm.createContext(ctx);vm.runInContext(fs.readFileSync('assets/radar.js','utf8'),ctx);
async function settle(){for(let i=0;i<12;i++)await new Promise(r=>setImmediate(r));}
(async()=>{
await settle();
assert.equal(vm.runInContext('curDate',ctx),'2026-08-11');
assert.ok(element('#signalCount').textContent>1);
assert.match(element('#app').innerHTML,/https:\/\/openai.com\/index\/hsp-gruppe/);
assert.match(element('#archiveNotice').textContent,/尚未接入/);
await vm.runInContext("period=1; applyVendor('anthropic')",ctx);
assert.equal(vm.runInContext('curDate',ctx),'2026-08-09');
assert.match(element('#app').innerHTML,/claude.com/);
await vm.runInContext("applyVendor('__daily__'); selectDay('2026-08-06')",ctx);
await settle();
const expected=index.days.filter(d=>d.date==='2026-08-06').reduce((n,d)=>n+JSON.parse(fs.readFileSync(`data/${d.vendor}/${d.date}.json`)).updates.length,0);
assert.equal(element('#signalCount').textContent,expected);
vm.runInContext("curTag='模型发布'; renderContent()",ctx);
assert.equal(element('#feedCount').textContent,vm.runInContext("itemsForSelection().filter(u=>u.tag==='模型发布').length",ctx));
assert.equal(vm.runInContext("safeURL('javascript:alert(1)')",ctx),null);
assert.equal(vm.runInContext("esc('<img src=x onerror=alert(1)>')",ctx),'&lt;img src=x onerror=alert(1)&gt;');
// Pagination must adapt to the actual content area, including an open side panel.
vm.runInContext("period=7",ctx);
await vm.runInContext("selectDay('2026-08-11')",ctx);
element('#app').clientWidth=1400;element('#app').clientHeight=480;
vm.runInContext('renderContent()',ctx);
assert.equal(vm.runInContext('pageSize',ctx),6);
const firstPage=element('#app').innerHTML;
vm.runInContext('feedPage=1;renderContent()',ctx);
assert.notEqual(element('#app').innerHTML,firstPage);
assert.match(element('#pageRange').textContent,/第 7/);
element('#app').clientWidth=390;element('#app').clientHeight=440;
vm.runInContext('renderContent()',ctx);
assert.equal(vm.runInContext('pageSize',ctx),2);
vm.runInContext('period=1',ctx);
// Legacy content uses dotted dates; the public manifest owns archive dates.
await vm.runInContext("selectDay('2026-06-03')",ctx);
assert.equal(vm.runInContext("itemsForSelection().every(u=>u.archiveDate==='2026-06-03')",ctx),true);
// A delayed response from the previous date must not overwrite the new selection.
ctx.fetch=async url=>{if(url.includes('2026-08-07'))await new Promise(r=>setTimeout(r,25));return{ok:true,json:async()=>url==='output/index.json'?index:JSON.parse(fs.readFileSync(path.join(root,url),'utf8'))};};
vm.runInContext('dataCache.clear()',ctx);
await vm.runInContext("Promise.all([selectDay('2026-08-07'),selectDay('2026-08-11')])",ctx);
assert.equal(element('#signalCount').textContent,1);
assert.match(element('#app').innerHTML,/HSP/);
// Partial outage stays visible, and failed fetches are retryable.
ctx.fetch=async url=>({ok:!url.includes('anthropic'),status:503,json:async()=>url==='output/index.json'?index:JSON.parse(fs.readFileSync(path.join(root,url),'utf8'))});
vm.runInContext('dataCache.clear()',ctx);
await vm.runInContext("selectDay('2026-08-06')",ctx);
assert.match(element('#meta').textContent,/读取失败/);
assert.equal(vm.runInContext("dataCache.has('anthropic|2026-08-06')",ctx),false);
assert.match(element('#activeCaption').textContent,/读取失败/);
console.log('PASS: real archive load, original source links, vendor/date/category selection, stale-response protection, partial outages, retry cache, storage denied, escaping, adaptive pagination (desktop/mobile).');
})().catch(e=>{console.error(e);process.exitCode=1;});
