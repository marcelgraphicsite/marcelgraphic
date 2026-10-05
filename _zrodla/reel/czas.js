// Wirtualny czas wstrzykiwany do strony przed jej skryptami.
// Strona „myśli”, że płynie czas, ale każda klatka nagrania to dokładnie 1/60 s:
// timery, requestAnimationFrame, Date, performance.now i animacje CSS/WAAPI idą krok po kroku.
// Czas przechodzi przez nawigację (sessionStorage), więc kurtyna między podstronami jest ciągła.
(() => {
  if (window.__vt) return;
  const KEY = '__reel_vt';
  const RealDate = Date;
  const realRAF = window.requestAnimationFrame.bind(window);
  let now = 0, epoch = Date.UTC(2026, 9, 6, 8, 40); // stała data: wtorek 10:40 w Polsce (zegar w Kontakcie: „Teraz pracuję”)
  try {
    const s = JSON.parse(sessionStorage.getItem(KEY) || 'null');
    if (s) { now = s.now; epoch = s.epoch; }
  } catch (e) { /* ok */ }

  let seq = 0;
  const timers = new Map();
  let rafs = new Map();
  const add = (fn, ms, args, rep) => {
    const id = ++seq;
    const d = Math.max(0, +ms || 0);
    timers.set(id, { id, fn, at: now + d, d, args, rep, seq: id });
    return id;
  };
  window.setTimeout = (fn, ms, ...a) => add(fn, ms, a, false);
  window.setInterval = (fn, ms, ...a) => add(fn, Math.max(1, +ms || 0), a, true);
  window.clearTimeout = window.clearInterval = id => { timers.delete(id); };
  window.requestAnimationFrame = fn => { const id = ++seq; rafs.set(id, fn); return id; };
  window.cancelAnimationFrame = id => { rafs.delete(id); };
  window.requestIdleCallback = fn => add(() => fn({ didTimeout: false, timeRemaining: () => 12 }), 1, [], false);
  window.cancelIdleCallback = id => timers.delete(id);
  performance.now = () => now;

  function FakeDate(...a) {
    if (!(this instanceof FakeDate)) return new RealDate(epoch + now).toString();
    return a.length ? new RealDate(...a) : new RealDate(epoch + now);
  }
  FakeDate.prototype = RealDate.prototype;
  FakeDate.now = () => Math.floor(epoch + now);
  FakeDate.parse = RealDate.parse;
  FakeDate.UTC = RealDate.UTC;
  window.Date = FakeDate;

  // animacje CSS i WAAPI: zatrzymane, a czas ustawiany ręcznie co klatkę
  const seen = new WeakMap();
  const cssPaused = a => {
    if (!(window.CSSAnimation && a instanceof CSSAnimation)) return false;
    const ef = a.effect;
    if (!ef || !ef.target) return false;
    const cs = getComputedStyle(ef.target, ef.pseudoElement || null);
    const names = cs.animationName.split(',').map(s => s.trim());
    const st = cs.animationPlayState.split(',').map(s => s.trim());
    const i = Math.max(0, names.indexOf(a.animationName));
    return st[i % st.length] === 'paused';
  };
  const syncAnims = dt => {
    for (const a of document.getAnimations()) {
      if (a.playState === 'finished' || a.playState === 'idle') continue;
      let r = seen.get(a);
      if (!r) { r = { el: 0 }; seen.set(a, r); }
      else if (!cssPaused(a)) r.el += dt * (a.playbackRate || 1);
      const end = a.effect ? a.effect.getComputedTiming().endTime : Infinity;
      if (r.el >= end && isFinite(end)) { try { a.finish(); } catch (e) { /* ok */ } continue; }
      if (a.playState !== 'paused') a.pause();
      a.currentTime = r.el;
    }
  };

  // płynne przewijanie strony (scrollTo/scrollIntoView z behavior:'smooth') liczone w wirtualnym czasie
  const anims = [];
  const ease = x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
  const rawScrollTo = window.scrollTo.bind(window);
  const smoothTo = (y) => {
    const from = window.scrollY, max = document.documentElement.scrollHeight - innerHeight;
    const to = Math.max(0, Math.min(max, y));
    anims.length = 0;
    anims.push({ from, to, t0: now, d: Math.min(1100, 500 + Math.abs(to - from) * 0.35) });
  };
  window.scrollTo = function (a, b) {
    if (a && typeof a === 'object') {
      if (a.behavior === 'smooth') { smoothTo(a.top != null ? a.top : window.scrollY); return; }
      return rawScrollTo({ left: a.left || 0, top: a.top != null ? a.top : window.scrollY, behavior: 'instant' });
    }
    return rawScrollTo({ left: a || 0, top: b || 0, behavior: 'instant' });
  };
  window.scroll = window.scrollTo;
  const rawSIV = Element.prototype.scrollIntoView;
  Element.prototype.scrollIntoView = function (o) {
    if (o && typeof o === 'object' && o.behavior === 'smooth') { smoothTo(this.getBoundingClientRect().top + window.scrollY - (o.block === 'center' ? innerHeight / 2 : 0)); return; }
    return rawSIV.call(this, o);
  };
  window.__reelScroll = y => { anims.length = 0; rawScrollTo({ left: 0, top: y, behavior: 'instant' }); };
  const runScrollAnims = () => {
    if (!anims.length) return;
    const a = anims[0], k = Math.min(1, (now - a.t0) / a.d);
    rawScrollTo({ left: 0, top: a.from + (a.to - a.from) * ease(k), behavior: 'instant' });
    if (k >= 1) anims.length = 0;
  };
  const st = document.createElement('style');
  st.textContent = 'html{scroll-behavior:auto!important}';
  const putStyle = () => { const p = document.head || document.documentElement; if (p && !st.isConnected) p.appendChild(st); };
  putStyle();
  if (!st.isConnected) new MutationObserver((m, o) => { putStyle(); if (st.isConnected) o.disconnect(); }).observe(document, { childList: true, subtree: true });
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
    putStyle();
  });
  // wyjście ze strony (nawigacja) — nagrywarka czeka na nową stronę
  window.__leaving = false;
  try { navigation.addEventListener('navigate', e => { if (!e.destination.sameDocument) window.__leaving = true; }); } catch (e) { /* ok */ }
  addEventListener('pagehide', () => { window.__leaving = true; });

  const save = () => { try { sessionStorage.setItem(KEY, JSON.stringify({ now, epoch })); } catch (e) { /* ok */ } };

  // jeden krok = jedna klatka filmu
  window.__vt = {
    get now() { return now; },
    realFrame: () => new Promise(r => realRAF(() => r())),
    step(dt) {
      const end = now + dt;
      // timery w kolejności czasu (także te dodane w trakcie)
      for (let guard = 0; guard < 5000; guard++) {
        let next = null;
        for (const t of timers.values()) if (t.at <= end && (!next || t.at < next.at || (t.at === next.at && t.seq < next.seq))) next = t;
        if (!next) break;
        now = Math.max(now, next.at);
        if (next.rep) { next.at += next.d; next.seq = ++seq; } else timers.delete(next.id);
        try { typeof next.fn === 'function' ? next.fn(...next.args) : (0, eval)(next.fn); } catch (e) { console.warn(e); }
      }
      now = end;
      runScrollAnims();
      const cbs = rafs; rafs = new Map();
      cbs.forEach(fn => { try { fn(now); } catch (e) { console.warn(e); } });
      syncAnims(dt);
      save();
    },
    sync: () => syncAnims(0),
    save
  };
  save();
})();
