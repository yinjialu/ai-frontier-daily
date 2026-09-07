'use strict';
// Feedback is authoritative only after the private server acknowledges it.
window.RadarFeedback = (() => {
  const states = new Map(), pending = new Map(), retries = new Map();
  let enabled = false, refresh = () => {}, summary = {}, noticeTimer;
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function canonical(value) {
    try {
      const u = new URL(value);
      if (!/^https?:$/.test(u.protocol) || u.username || u.password) return '';
      for (const k of [...u.searchParams.keys()]) if (/^utm_/i.test(k) || ['fbclid','gclid','mc_cid','mc_eid'].includes(k.toLowerCase())) u.searchParams.delete(k);
      const pairs = [...u.searchParams].sort(([ak,av],[bk,bv]) => ak < bk ? -1 : ak > bk ? 1 : av < bv ? -1 : av > bv ? 1 : 0);
      u.search = new URLSearchParams(pairs).toString();
      u.pathname = u.pathname.replace(/\/+$/, '') || '/';
      return u.href;
    } catch { return ''; }
  }
  function notify(message) {
    const el = document.querySelector('#feedbackNotice');
    el.textContent = message; el.hidden = false;
    clearTimeout(noticeTimer); noticeTimer = setTimeout(() => { el.hidden = true; }, 6500);
    el.onclick = () => { el.hidden = true; };
  }
  function renderSummary() {
    const el = document.querySelector('#feedbackSummary');
    if (el) el.textContent = enabled ? `已记录 ${summary.useful || 0} 条有价值、${summary.less || 0} 条少看类似；用于下一轮候选排序。再次点击可撤销。` : '反馈请在服务器私有工作台使用。此预览不记录偏好。';
  }
  async function init(callback) {
    refresh = callback;
    try {
      const r = await fetch('api/feedback', {cache:'no-store', credentials:'same-origin'});
      if (!r.ok) throw Error('unavailable');
      const data = await r.json();
      enabled = data.enabled === true; summary = data.summary || {};
      for (const entry of data.entries || []) states.set(canonical(entry.url), entry.action);
    } catch { enabled = false; }
    renderSummary(); refresh();
  }
  function controls(item, index) {
    const url = canonical(item.url || item.source), state = states.get(url);
    if (!url) return '';
    return `<span class="feedback-controls" aria-label="内容反馈">${[['useful','有价值'],['less','少看类似']].map(([action,label]) => `<button data-feedback="${action}" data-item="${index}" aria-pressed="${state === action}" ${pending.has(url) ? 'disabled' : ''} title="${enabled ? (state === action ? '再次点击撤销' : action === 'useful' ? '增加相近内容的优先级' : '降低相近内容的优先级') : '在服务器私有工作台记录反馈'}">${state === action ? '✓ ' : ''}${escape(label)}</button>`).join('')}</span>`;
  }
  async function submit(item, requested) {
    const url = canonical(item.url || item.source);
    if (!enabled) { notify('此预览不记录偏好，请在 Tailscale 私有工作台使用反馈。'); return; }
    if (!url || pending.has(url)) return;
    const action = states.get(url) === requested ? 'clear' : requested;
    const retry = retries.get(url);
    const requestId = retry?.action === action ? retry.requestId : Array.from(crypto.getRandomValues(new Uint8Array(16)), n => n.toString(16).padStart(2,'0')).join('');
    retries.set(url, {action, requestId}); pending.set(url, true); refresh();
    try {
      const r = await fetch('api/feedback', {method:'POST', credentials:'same-origin', headers:{'Content-Type':'application/json'}, body:JSON.stringify({request_id:requestId,url:item.url || item.source,vendor:item.vendor,archive_date:item.archiveDate,action})});
      if (!r.ok) throw Error('save failed');
      const data = await r.json();
      states.set(url, data.action); summary = data.summary || summary; retries.delete(url);
      notify(data.action === 'clear' ? '反馈已撤销。' : '已记录，将用于下一轮筛选。再次点击可撤销。');
      renderSummary();
    } catch { notify('未能确认保存，请再次点击重试。'); }
    finally { pending.delete(url); refresh(); }
  }
  return {init, controls, submit, canonical};
})();
