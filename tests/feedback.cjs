const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
const {webcrypto}=require('node:crypto');
function setup(fetch){
 const nodes=new Map(); const node=id=>{if(!nodes.has(id))nodes.set(id,{textContent:'',hidden:true});return nodes.get(id);};
 const ctx={window:{},document:{querySelector:node},URL,URLSearchParams,Uint8Array,Map,crypto:webcrypto,fetch,setTimeout(){return 1;},clearTimeout(){}};
 vm.createContext(ctx);vm.runInContext(fs.readFileSync('assets/feedback.js','utf8'),ctx);
 return {api:ctx.window.RadarFeedback,ctx,node};
}
(async()=>{
 const item={url:'https://example.org/model/?utm_source=x',vendor:'openai',archiveDate:'2026-09-07'};
 let requests=[],fail=false,state='clear';
 const app=setup(async(url,options)=>{
  if(options.method){const body=JSON.parse(options.body);requests.push(body);if(fail)throw Error('connection lost');state=body.action;return {ok:true,json:async()=>({action:state,summary:{useful:state==='useful'?1:0,less:state==='less'?1:0}})};}
  return {ok:true,json:async()=>({enabled:true,entries:[],summary:{}})};
 });
 await app.api.init(()=>{});
 assert.equal(app.api.canonical(item.url),'https://example.org/model');
 await app.api.submit(item,'useful');
 assert.match(app.api.controls(item,0),/aria-pressed="true"/);
 await app.api.submit(item,'useful');assert.equal(requests.at(-1).action,'clear');
 fail=true;await app.api.submit(item,'less');
 assert.doesNotMatch(app.api.controls(item,0),/aria-pressed="true"/);
 assert.match(app.node('#feedbackNotice').textContent,/未能确认/);
 const lostId=requests.at(-1).request_id;fail=false;await app.api.submit(item,'less');
 assert.equal(requests.at(-1).request_id,lostId,'ambiguous retries preserve idempotency key');
 assert.equal(requests.at(-1).tag,undefined,'client does not submit training labels');
 const restored=setup(async()=>({ok:true,json:async()=>({enabled:true,entries:[{url:'https://example.org/model',action:'less'}]})}));
 await restored.api.init(()=>{});assert.match(restored.api.controls(item,0),/✓ 少看类似/);
 const offline=setup(async()=>{throw Error('offline');});await offline.api.init(()=>{});await offline.api.submit(item,'useful');
 assert.match(offline.node('#feedbackNotice').textContent,/不记录偏好/);
 assert.doesNotMatch(offline.api.controls(item,0),/aria-pressed="true"/);
 console.log('PASS: acknowledged feedback, undo, retry idempotency, restoration, offline honesty, URL normalization.');
})().catch(e=>{console.error(e);process.exitCode=1;});
