// Nagrywarka ujęć strony do reela — klatka po klatce w wirtualnym czasie (60 kl./s, zero szarpnięć).
// Użycie: NODE_PATH=$(npm root -g) node nagraj.js <main|hook|old|phone> [--preview] [--from=s] [--to=s]
// Klatki i dane (kursor, kliknięcia, tytuł karty, pozycje elementów) lądują w $REEL_OUT/<ujęcie>/.
const { chromium, devices } = require('playwright');
const fs = require('fs');
const path = require('path');
const S = require('./scenariusz.js');

const OUT = process.env.REEL_OUT || path.join(__dirname, 'out');
const BASE = 'http://localhost:' + (process.env.PORT || 8123);
const OLD_BASE = 'http://localhost:' + (process.env.OLD_PORT || 8124);
const FPS = S.FPS, DT = 1000 / FPS;
const args = process.argv.slice(2);
const TAKE = args[0] || 'main';
const PREVIEW = args.includes('--preview');
const argNum = (k, d) => { const a = args.find(x => x.startsWith('--' + k + '=')); return a ? +a.split('=')[1] : d; };

// ---------- krzywe ruchu ----------
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const E = {
  lin: k => k,
  // minimalne szarpnięcie — tak rusza ręka człowieka
  hand: k => k * k * k * (10 + k * (-15 + 6 * k)),
  io3: k => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2),
  io5: k => (k < 0.5 ? 16 * Math.pow(k, 5) : 1 - Math.pow(-2 * k + 2, 5) / 2),
  sine: k => -(Math.cos(Math.PI * k) - 1) / 2,
  out4: k => 1 - Math.pow(1 - k, 4)
};

class Take {
  constructor(name, opt) {
    this.name = name;
    this.opt = opt;
    this.events = [];
    this.mseg = null;     // aktywny ruch myszki
    this.sseg = null;     // aktywne przewijanie
    this.mouse = opt.mouse0 ? opt.mouse0.slice() : [-50, -50];
    this.down = false;
    this.meta = { name, fps: FPS, viewport: opt.viewport, dpr: opt.dpr, frames: [], clicks: [], taps: [], marks: {}, keys: [] };
    this.f = 0;
    this.drift = opt.drift !== false;
    this.dir = path.join(OUT, name);
  }
  at(t, fn) { this.events.push({ t, fn, i: this.events.length }); return this; }
  // ruch kursora do celu (punkt, selektor albo funkcja) po łuku
  move(t, dur, target, o = {}) {
    return this.at(t, async () => {
      const from = this.mouse.slice();
      const to = await this.resolve(target);
      const dx = to[0] - from[0], dy = to[1] - from[1], L = Math.hypot(dx, dy) || 1;
      const arc = o.arc == null ? 0.14 : o.arc;
      const c = [(from[0] + to[0]) / 2 - dy / L * L * arc, (from[1] + to[1]) / 2 + dx / L * L * arc];
      // cel ze selektora śledzony na żywo (strona może się jeszcze przewijać, menu wjeżdżać)
      this.mseg = { t0: t, t1: t + dur, from, to, c, arc, live: (target && target.sel) ? target : null, ease: E[o.ease || 'hand'] };
    });
  }
  path(t, dur, fn, o = {}) {
    return this.at(t, async () => { const from = this.mouse.slice(); this.mseg = { t0: t, t1: t + dur, fn, from, ease: E[o.ease || 'lin'] }; });
  }
  click(t, o = {}) {
    this.at(t, async () => {
      this.down = true;
      this.meta.clicks.push({ t, x: this.mouse[0], y: this.mouse[1], f: this.f, ui: o.ui || null });
      await this.page.mouse.down();
    });
    return this.at(t + 0.075, async () => { this.down = false; await this.page.mouse.up(); });
  }
  tap(t, target) {
    return this.at(t, async () => {
      const p = await this.resolve(target);
      this.meta.taps.push({ t, x: p[0], y: p[1], f: this.f });
      await this.page.touchscreen.tap(p[0], p[1]);
    });
  }
  // przewijanie strony do pozycji (liczba, selektor albo {by})
  scroll(t, dur, target, o = {}) {
    return this.at(t, async () => {
      const y0 = o.from != null ? o.from : await this.page.evaluate(() => scrollY);
      let y1;
      if (typeof target === 'number') y1 = target;
      else if (target.by != null) y1 = y0 + target.by;
      else y1 = await this.page.evaluate(([s, off]) => { const e = document.querySelector(s); return e.getBoundingClientRect().top + scrollY - (off || 0); }, [target.sel, target.off]);
      const max = await this.page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
      y1 = clamp(y1, 0, max);
      this.sseg = { t0: t, t1: t + dur, y0, y1, ease: E[o.ease || 'io3'] };
    });
  }
  // przewijanie wewnątrz ramki (podgląd projektu)
  frameScroll(t, dur, y1, o = {}) {
    return this.at(t, async () => {
      const fr = this.page.frames().find(f => f !== this.page.mainFrame() && /zar-burger|luxe|vesper/.test(f.url()));
      if (!fr) return;
      const y0 = await fr.evaluate(() => scrollY).catch(() => 0);
      this.fseg = { t0: t, t1: t + dur, y0, y1, fr, ease: E[o.ease || 'io3'] };
    });
  }
  key(t, k) { return this.at(t, async () => { this.meta.keys.push({ t, k }); await this.page.keyboard.press(k); }); }
  go(t, url) { return this.at(t, async () => { await this.page.evaluate(u => { location.href = u; }, url); }); }
  mark(t, name, sel, o = {}) {
    return this.at(t, async () => {
      const r = await this.page.evaluate(([s, all]) => {
        const els = all ? [...document.querySelectorAll(s)] : [document.querySelector(s)];
        const rs = els.filter(Boolean).map(e => e.getBoundingClientRect());
        if (!rs.length) return null;
        const x0 = Math.min(...rs.map(r => r.left)), y0 = Math.min(...rs.map(r => r.top));
        const x1 = Math.max(...rs.map(r => r.right)), y1 = Math.max(...rs.map(r => r.bottom));
        return [x0, y0, x1 - x0, y1 - y0];
      }, [sel, !!o.all]);
      (this.meta.marks[name] = this.meta.marks[name] || []).push({ t, f: this.f, r });
    });
  }
  async resolve(target) {
    if (Array.isArray(target)) return target;
    if (typeof target === 'function') return target(this);
    const r = await this.page.evaluate(s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }, target.sel);
    if (!r) { console.warn('brak elementu', target.sel); return this.mouse.slice(); }
    return [r[0] + r[2] * (target.rx == null ? 0.5 : target.rx) + (target.dx || 0), r[1] + r[3] * (target.ry == null ? 0.5 : target.ry) + (target.dy || 0)];
  }

  // ---------- przeglądarka ----------
  async open() {
    fs.mkdirSync(this.dir, { recursive: true });
    this.browser = await chromium.launch({ args: ['--hide-scrollbars', '--force-color-profile=srgb', '--disable-lcd-text', '--font-render-hinting=none'] });
    const o = this.opt;
    this.ctx = await this.browser.newContext({
      viewport: o.viewport, deviceScaleFactor: PREVIEW ? 1 : o.dpr, isMobile: !!o.mobile, hasTouch: !!o.mobile,
      userAgent: o.ua, locale: 'pl-PL', timezoneId: 'Europe/Warsaw', permissions: ['clipboard-read', 'clipboard-write']
    });
    await this.ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: BASE });
    await this.ctx.addInitScript({ path: path.join(__dirname, 'czas.js') });
    await this.ctx.addInitScript(([intro]) => {
      try { sessionStorage.setItem('ms-gpu', '1'); if (!intro && !sessionStorage.getItem('__reel_once')) { sessionStorage.setItem('ms-intro', '1'); } sessionStorage.setItem('__reel_once', '1'); } catch (e) { /* ok */ }
      // linki na stronie 404 prowadzą na domenę — w nagraniu zostajemy lokalnie
      document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('a[href^="https://marcelgraphicsite.pl"]').forEach(a => { const u = new URL(a.href); a.setAttribute('href', u.pathname + u.search); });
      });
    }, [!!o.intro]);
    await this.ctx.route('**/lenis.min.js*', r => r.abort());
    // stara strona brała fonty z Google — w nagraniu te same kroje z dysku
    await this.ctx.route(/fonts\.googleapis\.com/, r => r.fulfill({ contentType: 'text/css', body:
      `@font-face{font-family:"Inter";src:url(${BASE}/assets/fonts/inter-var.woff2) format("woff2");font-weight:100 900}` +
      `@font-face{font-family:"JetBrains Mono";src:url(${BASE}/assets/fonts/jetbrains-mono-400.woff2) format("woff2");font-weight:400 500}` }));
    await this.ctx.route(/fonts\.gstatic\.com/, r => r.abort());
    if (o.noCinema) await this.ctx.addInitScript(() => { document.addEventListener('DOMContentLoaded', () => { const c = document.getElementById('cinema'); if (c) c.remove(); }); });
    this.page = await this.ctx.newPage();
    this.page.on('pageerror', e => console.log('  [błąd strony]', e.message));
    this.page.on('console', m => { if (m.type() === 'warning' && !/\[/.test(m.text())) console.log('  [konsola]', m.text().slice(0, 140)); });
    await this.page.goto(o.url, { waitUntil: 'load' });
    await this.settle();
    if (o.mouse0 && !o.mobile) await this.page.mouse.move(o.mouse0[0], o.mouse0[1]);
    // rozgrzewka: strona kończy animację wejścia, zanim ruszy pierwsza klatka nagrania
    if (o.warm) await this.page.evaluate(n => { for (let i = 0; i < n; i++) window.__vt.step(1000 / 60); }, Math.round(o.warm * FPS));
  }
  async settle() {
    await this.page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].filter(i => !i.complete).map(i => new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 4000); })));
    }).catch(() => {});
    this.cdp = await this.ctx.newCDPSession(this.page);
  }
  async waitNewPage() {
    for (let i = 0; i < 400; i++) {
      const ok = await this.page.evaluate(() => !window.__leaving && document.readyState === 'complete' && !!window.__vt).catch(() => false);
      if (ok) break;
      await new Promise(r => setTimeout(r, 40));
    }
    await this.settle();
    if (!this.opt.mobile) await this.page.mouse.move(this.mouse[0], this.mouse[1]);
  }

  // ---------- jedna klatka ----------
  async frame(capture) {
    const t = this.f / FPS;
    this.events.sort((a, b) => a.t - b.t || a.i - b.i);
    while (this.events.length && this.events[0].t <= t + 1e-6) {
      const e = this.events.shift();
      await e.fn();
      if (await this.leaving()) await this.waitNewPage();
    }
    // kursor
    if (this.mseg) {
      const s = this.mseg, k = clamp((t - s.t0) / (s.t1 - s.t0), 0, 1), e = s.ease(k);
      if (s.fn) this.mouse = s.fn(e, s.from);
      else {
        if (s.live) {
          const to = await this.resolve(s.live);
          const dx = to[0] - s.from[0], dy = to[1] - s.from[1];
          s.to = to; s.c = [(s.from[0] + to[0]) / 2 - dy * s.arc, (s.from[1] + to[1]) / 2 + dx * s.arc];
        }
        const u = 1 - e;
        this.mouse = [u * u * s.from[0] + 2 * u * e * s.c[0] + e * e * s.to[0], u * u * s.from[1] + 2 * u * e * s.c[1] + e * e * s.to[1]];
      }
      if (k >= 1) this.mseg = null;
    }
    // drobne drżenie ręki (dzięki temu strona widzi ruch i odświeża hover pod kursorem)
    let mx = this.mouse[0], my = this.mouse[1];
    if (this.drift && !this.opt.mobile) { mx += Math.sin(t * 1.7) * 1.2 + Math.sin(t * 3.1 + 1) * 0.6; my += Math.cos(t * 1.3) * 1.0 + Math.sin(t * 2.3 + 2) * 0.5; }
    if (!this.opt.mobile) await this.page.mouse.move(mx, my);
    // przewijanie
    if (this.sseg) {
      const s = this.sseg, k = clamp((t - s.t0) / (s.t1 - s.t0), 0, 1);
      await this.page.evaluate(y => window.__reelScroll(y), s.y0 + (s.y1 - s.y0) * s.ease(k));
      if (k >= 1) this.sseg = null;
    }
    if (this.fseg) {
      const s = this.fseg, k = clamp((t - s.t0) / (s.t1 - s.t0), 0, 1);
      await s.fr.evaluate(y => window.__reelScroll && window.__reelScroll(y), s.y0 + (s.y1 - s.y0) * s.ease(k)).catch(() => {});
      if (k >= 1) this.fseg = null;
    }
    // krok czasu: najpierw ramki (podgląd projektu), potem strona
    for (const fr of this.page.frames()) {
      if (fr === this.page.mainFrame()) continue;
      await fr.evaluate(dt => window.__vt && window.__vt.step(dt), DT).catch(() => {});
    }
    const info = await this.page.evaluate(async ([dt, x, y]) => {
      await window.__vt.realFrame();
      window.__vt.step(dt);
      let cur = 'default';
      const el = document.elementFromPoint(x, y);
      if (el) {
        let c = getComputedStyle(el).cursor;
        if (c === 'auto') c = el.closest('a[href],button,label,[role="button"],[role="tab"]') ? 'pointer' : (el.closest('input:not([type=checkbox]):not([type=radio]),textarea') ? 'text' : 'default');
        cur = c;
      }
      const dot = document.getElementById('cursor');
      return { title: document.title, path: location.pathname + location.search, sy: Math.round(scrollY), vx: visualViewport ? visualViewport.pageLeft : scrollX, vy: visualViewport ? visualViewport.pageTop : scrollY, cur, lang: document.documentElement.lang, dot: dot ? dot.className : '' };
    }, [DT, mx, my]).catch(() => null);
    if (await this.leaving()) { /* nawigacja zaczęła się w tej klatce — dokończ ją przed zrzutem */ }
    const vxy = info ? [info.vx, info.vy] : [0, 0];
    if (info) { delete info.vx; delete info.vy; }
    this.meta.frames.push(Object.assign({ f: this.f, x: +mx.toFixed(2), y: +my.toFixed(2), down: this.down }, info || {}));
    if (capture) {
      // zrzut w pełnej rozdzielczości urządzenia (clip liczony od góry dokumentu)
      const vp = this.opt.viewport, scale = PREVIEW ? 1 : this.opt.dpr;
      const { data } = await this.cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: PREVIEW ? 70 : 93, optimizeForSpeed: true, clip: { x: vxy[0], y: vxy[1], width: vp.width, height: vp.height, scale } });
      await fs.promises.writeFile(path.join(this.dir, String(this.f).padStart(5, '0') + '.jpg'), Buffer.from(data, 'base64'));
    }
    this.f++;
  }
  async leaving() { return this.page.evaluate(() => !!window.__leaving).catch(() => true); }

  async run(T) {
    const n = Math.round(T * FPS), from = Math.round(argNum('from', 0) * FPS), to = Math.round(argNum('to', T) * FPS), every = PREVIEW ? 6 : 1;
    const t0 = Date.now();
    // kilka procesów naraz: każdy przechodzi trasę od początku (szybko, bez zrzutów), a zrzuca tylko swój zakres
    const stop = args.some(a => a.startsWith('--to=')) ? Math.min(n, to + 1) : n;
    while (this.f < stop) {
      const cap = this.f >= from && this.f <= to && this.f % every === 0;
      await this.frame(cap);
      if (this.f % 300 === 0) console.log(`  ${this.name}: ${(this.f / FPS).toFixed(1)} s / ${T.toFixed(1)} s (${((Date.now() - t0) / this.f).toFixed(0)} ms/kl.)`);
    }
    if (stop === n) fs.writeFileSync(path.join(this.dir, 'meta.json'), JSON.stringify(this.meta));
    await this.browser.close();
    console.log(`  ${this.name}: gotowe — ${n} klatek`);
  }
}

// =====================================================================
// UJĘCIA
// =====================================================================
const sc = id => S.byId[id];
const DESK = { viewport: { width: 1280, height: 728 }, dpr: 2 };

// --- hook: pierwsze wejście na stronę (kurtyna „kino”) ---
async function hook() {
  const T = new Take('hook', Object.assign({ url: BASE + '/', intro: true, drift: false }, DESK));
  await T.open();
  await T.run(6.6);
}

// --- stara strona (jedna, z czerwca) na netbooku ---
async function old() {
  const T = new Take('old', { url: OLD_BASE + '/', viewport: { width: 1024, height: 552 }, dpr: 1.5, drift: false, noCinema: true });
  await T.open();
  const y0 = await T.page.evaluate(() => { const h = [...document.querySelectorAll('h1,h2')].find(e => /Design/.test(e.textContent)); return h ? h.getBoundingClientRect().top + scrollY - 140 : 1200; });
  T.scroll(0, 0.6, y0, { from: y0 });
  T.scroll(0.6, 8.6, y0 + 820, { ease: 'sine', from: y0 });
  await T.run(10);
}

// --- główne ujęcie: cała wycieczka po stronie bez cięć ---
async function main() {
  const T = new Take('main', Object.assign({ url: BASE + '/', mouse0: [1240, 700], warm: 1.6 }, DESK));
  await T.open();
  const A = (id, dt) => sc(id).takeT + dt;

  // 01 litery chudną pod kursorem
  T.mark(A('f01', 0), 'name', '.pin-word');
  T.mark(A('f01', 0), 'cap', '#pinCap');
  T.move(A('f01', 0.25), 1.3, [960, 268], { arc: 0.18 });
  T.move(A('f01', 1.6), 1.7, [300, 275], { arc: -0.04, ease: 'sine' });
  T.move(A('f01', 3.35), 0.6, [215, 414], { arc: 0.2 });
  T.move(A('f01', 3.95), 1.75, [1075, 406], { arc: 0.03, ease: 'sine' });
  T.move(A('f01', 5.75), 0.9, [905, 585], { arc: -0.2 });

  // 02 hasło w nagłówku + belka
  T.scroll(A('f02', 0.0), 1.9, 1640, { ease: 'io3' });
  T.move(A('f02', 0.2), 1.6, [1010, 470], { arc: 0.1 });
  T.mark(A('f02', 2.0), 'rot', '.hero h1, .hero .h1, .hero__top');
  T.mark(A('f02', 2.0), 'rotw', '[data-rotator]');
  T.mark(A('f02', 2.0), 'band', '.band');
  T.scroll(A('f02', 4.15), 0.85, 1960, { ease: 'io3' });
  T.mark(A('f02', 5.0), 'band2', '.band');
  T.scroll(A('f02', 5.25), 0.8, 1640, { ease: 'io3' });
  T.move(A('f02', 4.3), 1.6, [930, 560], { arc: 0.1 });

  // 03 projekty jadą w bok
  T.scroll(A('f03', 0.0), 1.5, 2560, { ease: 'io3' });
  T.move(A('f03', 0.3), 1.2, [700, 400], { arc: 0.12 });
  T.scroll(A('f03', 1.55), 5.2, 4330, { ease: 'sine' });
  T.mark(A('f03', 3.0), 'hs', '#hsTrack');

  // 04 „następna strona” wypełnia się atramentem
  T.scroll(A('f04', 0.0), 2.3, 6560, { ease: 'io5' });
  T.move(A('f04', 0.2), 1.6, [930, 600], { arc: 0.1 });
  T.scroll(A('f04', 2.35), 3.5, 6990, { ease: 'sine' });
  T.mark(A('f04', 5.6), 'next', '.next__word');

  // 05 kurtyna (klik w „Prace →”), podpis zamiast paska ładowania
  T.move(A('f05', 0.15), 1.05, { sel: '.next__word', rx: 0.55, ry: 0.55 }, { arc: -0.12 });
  T.click(A('f05', 1.4));
  T.move(A('f05', 3.6), 1.4, [1010, 560], { arc: 0.15 });

  // 06 projekty na żywo (ŻAR, potem telefon)
  T.scroll(A('f06', 0.0), 1.4, 600, { ease: 'io3' });
  T.move(A('f06', 0.5), 1.0, { sel: '[data-proj="zar"]' }, { arc: 0.1 });
  T.click(A('f06', 1.65));
  T.move(A('f06', 2.1), 0.9, { sel: '#devPlay' }, { arc: -0.12 });
  T.click(A('f06', 3.15));
  T.mark(A('f06', 3.2), 'device', '#device');
  T.move(A('f06', 3.6), 0.9, [700, 420], { arc: 0.1 });
  T.frameScroll(A('f06', 4.3), 2.2, 980, { ease: 'io3' });
  T.move(A('f06', 6.4), 0.9, { sel: '[data-dev="phone"]' }, { arc: 0.12 });
  T.click(A('f06', 7.4));
  T.move(A('f06', 7.8), 0.9, [700, 430], { arc: -0.1 });
  T.frameScroll(A('f06', 8.0), 1.5, 1800, { ease: 'io3' });
  T.mark(A('f06', 8.4), 'device2', '#device');

  // 07 usługi: ilustracje i linia procesu
  T.scroll(A('f07', 0.0), 0.7, 500, { ease: 'io3' });
  T.move(A('f07', 0.2), 1.0, { sel: '[data-nav="uslugi"]' }, { arc: 0.1 });
  T.click(A('f07', 1.35));
  T.move(A('f07', 3.0), 1.0, [640, 520], { arc: 0.12 });
  T.scroll(A('f07', 3.2), 1.2, 300, { ease: 'io3' });
  T.mark(A('f07', 4.5), 'ills', '[data-play]', { all: true });
  T.move(A('f07', 4.2), 1.2, [870, 470], { arc: -0.1 });
  T.scroll(A('f07', 5.5), 3.4, 1560, { ease: 'io3' });
  T.mark(A('f07', 9.0), 'steps', '#steps');

  // 08 cennik: zakładki, ceny na żywo
  T.move(A('f08', 0.1), 1.0, { sel: 'a.btn[href="cennik"]' }, { arc: 0.12 });
  T.click(A('f08', 1.25));
  T.scroll(A('f08', 2.9), 0.9, 470, { ease: 'io3' });
  T.move(A('f08', 3.0), 0.8, { sel: '[data-tab="social"]' }, { arc: -0.1 });
  T.click(A('f08', 3.95));
  T.mark(A('f08', 4.0), 'tabs', '.tabs[role="tablist"]');
  T.move(A('f08', 4.3), 0.8, { sel: '[data-plat="fbig"]' }, { arc: 0.12 });
  T.click(A('f08', 5.25));
  T.mark(A('f08', 5.3), 'social', '[role="tabpanel"]:not([hidden])');
  T.move(A('f08', 5.8), 0.75, { sel: '[data-tab="nfc"]' }, { arc: -0.1 });
  T.click(A('f08', 6.65));

  // 09 kalkulator → wynik w formularzu
  T.scroll(A('f09', 0.0), 1.4, { sel: '#calc', off: 56 }, { ease: 'io3' });
  T.mark(A('f09', 1.5), 'calc', '#calc');
  T.mark(A('f09', 1.5), 'sum', '#sumOnce');
  T.move(A('f09', 0.6), 1.0, { sel: 'input[name="pkg"][value="wizytowka"]', dx: 40 }, { arc: 0.1 });
  T.click(A('f09', 1.75));
  T.move(A('f09', 2.0), 0.6, { sel: '[data-stepper="subpages"] [data-step="1"], [data-stepper] button:last-child' }, { arc: -0.1 });
  T.click(A('f09', 2.7));
  T.click(A('f09', 3.05));
  T.move(A('f09', 3.25), 0.55, { sel: 'input[name="lang"]' }, { arc: 0.1 });
  T.click(A('f09', 3.9));
  T.move(A('f09', 4.1), 0.6, { sel: '.cg[data-group="social"] [data-toggle]' }, { arc: -0.12 });
  T.click(A('f09', 4.8));
  T.move(A('f09', 5.2), 0.8, { sel: '#sumSend' }, { arc: 0.12 });
  T.click(A('f09', 6.2));
  T.move(A('f09', 8.3), 1.0, [1000, 560], { arc: 0.1 });
  T.mark(A('f09', 9.5), 'form', '#leadForm');
  T.mark(A('f09', 9.5), 'msg', '#f-msg');

  // 10 wizytówka: przechył, obrót, 4 obroty = niespodzianka
  T.mark(A('f10', 0.1), 'card', '#bcard');
  T.move(A('f10', 0.1), 0.9, { sel: '#bcard', rx: 0.62, ry: 0.4 }, { arc: 0.15 });
  T.path(A('f10', 1.0), 2.4, (e, from) => {
    const a = e * Math.PI * 2.2;
    return [from[0] - 30 + Math.cos(a) * 150 - 120 * Math.sin(a * 0.5), from[1] + 30 + Math.sin(a) * 85];
  }, { ease: 'sine' });
  T.move(A('f10', 3.4), 0.35, { sel: '#bcard', rx: 0.55, ry: 0.55 }, { arc: 0.1 });
  T.click(A('f10', 3.8));
  T.path(A('f10', 4.0), 1.8, (e, from) => [from[0] + Math.sin(e * Math.PI * 2) * 60, from[1] + Math.sin(e * Math.PI) * -35], { ease: 'sine' });
  T.click(A('f10', 6.0)); T.click(A('f10', 6.33)); T.click(A('f10', 6.66)); T.click(A('f10', 6.99));
  T.mark(A('f10', 7.4), 'toast', '#toast');

  // 11 kopiuj e-mail + zegar
  T.scroll(A('f11', 0.0), 1.0, 480, { ease: 'io3' });
  T.move(A('f11', 0.5), 1.0, { sel: '[data-copy]' }, { arc: -0.12 });
  T.click(A('f11', 1.7));
  T.mark(A('f11', 1.8), 'copy', '[data-copy]');
  T.mark(A('f11', 2.0), 'toast2', '#toast');
  T.scroll(A('f11', 3.3), 1.2, 760, { ease: 'io3' });
  T.move(A('f11', 3.5), 1.2, [600, 600], { arc: 0.1 });
  T.mark(A('f11', 4.6), 'clock', '#clockTime, #clockStatus', { all: true });

  // 12 „O mnie” — wstecz, kurtyna z góry, podpis
  T.scroll(A('f12', 0.0), 0.7, 690, { ease: 'io3' });
  T.move(A('f12', 0.2), 1.0, { sel: '[data-nav="o-mnie"]' }, { arc: 0.1 });
  T.click(A('f12', 1.35));
  T.move(A('f12', 3.0), 1.2, [980, 560], { arc: 0.12 });
  T.mark(A('f12', 4.0), 'sig', 'svg.sig');

  // 13 logo: najpierw na start, potem 5 kliknięć
  T.move(A('f13', 0.15), 1.0, { sel: '.logo-mark' }, { arc: -0.1 });
  T.click(A('f13', 1.3));
  [3.55, 3.77, 3.99, 4.21, 4.43].forEach((d, i) => T.click(A('f13', d), { ui: 'logo' + (i + 1) }));
  T.mark(A('f13', 3.4), 'logo', '.logo-mark');
  T.mark(A('f13', 5.0), 'toast3', '#toast');

  // 14 karta przeglądarki (pasek kart rysuje scena) — kursor wychodzi z okna strony
  T.move(A('f14', 0.1), 0.8, [1040, -40], { arc: 0.1 });

  // 15 PL / EN
  T.scroll(A('f15', 0.0), 1.2, 1700, { ease: 'io3' });
  T.scroll(A('f15', 1.3), 0.5, 1640, { ease: 'io3' });
  T.move(A('f15', 1.0), 1.0, { sel: '[data-lang="en"]' }, { arc: 0.1 });
  T.click(A('f15', 2.1));
  T.mark(A('f15', 2.6), 'hero', '.hero__top');
  T.mark(A('f15', 2.6), 'langs', '.lang');
  T.move(A('f15', 3.9), 0.7, { sel: '[data-lang="pl"]' }, { arc: -0.15 });
  T.click(A('f15', 4.75));

  // 16 404 — adres wpisany w pasku (scena), strona błędu, powrót na start
  T.move(A('f16', 0.0), 0.7, [520, -30], { arc: 0.1 });
  T.go(A('f16', 2.75), BASE + '/strona-ktorej-nie-ma');
  T.move(A('f16', 3.1), 1.0, [430, 330], { arc: 0.12 });
  T.mark(A('f16', 3.2), 'e404', 'main, body > *:not(script)');
  T.move(A('f16', 4.3), 1.3, { sel: 'a[href="/"]' }, { arc: -0.15 });
  T.click(A('f16', 6.2));

  // 17 konsola (panel rysuje scena) — strona startowa w tle
  T.move(A('f17', 0.3), 1.2, [1100, 640], { arc: 0.1 });

  await T.run(sc('f17').takeT + sc('f17').dur + 2.4);
}

// --- telefon ---
async function phone() {
  const iphone = devices['iPhone 15 Pro'] || devices['iPhone 14 Pro'];
  const T = new Take('phone', { url: BASE + '/', viewport: { width: 393, height: 728 }, dpr: 3, mobile: true, ua: iphone.userAgent, drift: false });
  await T.open();
  T.tap(0.9, { sel: '#menuBtn' });
  T.tap(2.3, { sel: '#mmenu a[href="kontakt"]' });
  T.scroll(4.3, 1.4, { sel: '#bcard', off: 150 }, { ease: 'io3' });
  T.mark(5.8, 'card', '#bcard');
  T.tap(6.1, { sel: '#bcard' });
  T.scroll(8.2, 1.4, { by: 160 }, { ease: 'io3' });
  await T.run(S.byId.f18.dur + 1.2);
}

(async () => {
  const fn = { main, hook, old, phone }[TAKE];
  if (!fn) { console.error('nieznane ujęcie', TAKE); process.exit(1); }
  await fn();
})();
