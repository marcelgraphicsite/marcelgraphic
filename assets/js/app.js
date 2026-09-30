/* =====================================================================
   Marcel Struszczak — interakcje (wszystkie podstrony).
   Bez zależności (Lenis opcjonalnie, tylko myszka). Każdy moduł działa
   osobno — błąd w jednym nie wyłącza reszty strony.
   ===================================================================== */
(() => {
  'use strict';

  /* ---------- ustawienia ---------- */
  // Formularz wysyła przez FormSubmit. Pierwsze zgłoszenie przyśle maila z linkiem
  // aktywacyjnym — kliknij go raz. Ustaw '' aby używać tylko programu pocztowego.
  const FORM_ENDPOINT = 'https://formsubmit.co/ajax/marcel.graphicsite@gmail.com';
  const EMAIL = 'marcel.graphicsite@gmail.com';

  /* ---------- helpers ---------- */
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const root = document.documentElement;
  const PAGE = root.dataset.page || 'index';
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const FINE = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, k) => a + (b - a) * k;
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* tryb prywatny */ } }
  };
  const sess = {
    get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) { /* ok */ } },
    del(k) { try { sessionStorage.removeItem(k); } catch (e) { /* ok */ } }
  };
  const mod = (name, fn) => { try { fn(); } catch (e) { if (window.console) console.warn('[' + name + ']', e); } };
  const scrollFns = [], resizeFns = [], langHooks = [], hashHandlers = [], liteHooks = [];
  const VER = ((document.currentScript && document.currentScript.src.match(/[?&]v=(\w+)/)) || [])[1] || '';
  // tryb lekki: słabszy sprzęt dostaje tańsze efekty — animacje zostają, znika to, co obciąża GPU
  const isLite = () => root.classList.contains('lite');
  const setLite = () => {
    if (isLite()) return;
    root.classList.add('lite');
    try { sessionStorage.setItem('ms-lite', '1'); } catch (e) { /* ok */ }
    liteHooks.forEach(f => { try { f(); } catch (e) { /* ok */ } });
  };
  let ticking = false;
  const runScroll = () => { ticking = false; scrollFns.forEach(f => { try { f(); } catch (e) { /* ok */ } }); };
  const requestScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(runScroll); } };
  const ARRIVING = root.classList.contains('is-arriving');
  let lenis = null;
  let gateOpen = false, openGate;
  const gate = new Promise(r => { openGate = () => { gateOpen = true; r(); }; }); // start animacji wejścia (po kurtynie)
  const menuCtl = { open: false, set() {} };

  /* ---------- mapa podstron (kolejność = kierunek przejścia) ---------- */
  const ORDER = { index: 0, prace: 1, uslugi: 2, cennik: 3, 'o-mnie': 4, kontakt: 5, 'luxe-salon': 6, 'vesper-barber': 6, 'zar-burger': 6 };
  const NUMS = { index: '00', prace: '01', uslugi: '02', cennik: '03', 'o-mnie': '04', kontakt: '05', 'luxe-salon': '↗', 'vesper-barber': '↗', 'zar-burger': '↗' };
  const CONCEPTS = { luxe: 'Luxe Salon', vesper: 'Vesper Barber', zar: 'ŻAR Burger' };
  const keyOf = url => {
    const f = url.pathname.split('/').pop();
    if (!f) return 'index';
    const m = f.match(/^([\w-]+)\.html?$/i);
    return m ? m[1].toLowerCase() : null;
  };

  /* ---------- i18n ---------- */
  const EN = window.__EN || {};
  const T = window.__T || { pl: {}, en: {} };
  const initLang = (() => {
    let q = null;
    try { q = new URLSearchParams(location.search).get('lang'); } catch (e) { /* ok */ }
    return (q === 'en' || q === 'pl') ? q : (store.get('ms-lang') === 'en' ? 'en' : 'pl');
  })();
  let LANG = initLang;
  const t = () => T[LANG] || T.pl;
  const PL = {};
  $$('[data-i18n]').forEach(el => { const k = el.dataset.i18n; if (!(k in PL)) PL[k] = el.innerHTML; });
  const PL_ATTR = new Map();
  $$('[data-i18n-attr]').forEach(el => {
    const m = {};
    el.dataset.i18nAttr.split(';').forEach(p => { const a = p.split(':')[0]; m[a] = el.getAttribute(a); });
    PL_ATTR.set(el, m);
  });
  const group = n => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, LANG === 'en' ? ',' : ' ');
  const cur = () => (LANG === 'en' ? 'PLN' : 'zł');
  const money = n => `${group(n)} ${cur()}`;
  const range = (a, b) => (a === b ? money(a) : `${group(a)}–${group(b)} ${cur()}`);

  /* ---------- nagłówki: podział na słowa (wjeżdżają po kolei) ---------- */
  function splitWords(el) {
    let i = 0;
    const walk = node => {
      Array.from(node.childNodes).forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(p => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(' ')); return; }
            const w = document.createElement('span'); w.className = 'w';
            const wi = document.createElement('span'); wi.className = 'wi';
            wi.style.setProperty('--i', i++); wi.textContent = p;
            w.appendChild(wi); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    };
    walk(el);
  }
  $$('[data-split]').forEach(el => { splitWords(el); el.dataset.lang = 'pl'; });

  function applyLang(l) {
    LANG = l === 'en' ? 'en' : 'pl';
    root.lang = LANG;
    $$('[data-i18n]').forEach(el => {
      const v = LANG === 'en' ? EN[el.dataset.i18n] : PL[el.dataset.i18n];
      if (v == null) return;
      if (el.hasAttribute('data-split')) {
        if (el.dataset.lang !== LANG) { el.innerHTML = v; splitWords(el); el.dataset.lang = LANG; }
      } else if (el.innerHTML !== v) el.innerHTML = v;
    });
    PL_ATTR.forEach((m, el) => {
      el.dataset.i18nAttr.split(';').forEach(p => {
        const [a, k] = p.split(':');
        const v = LANG === 'en' ? EN[k] : m[a];
        if (v != null) el.setAttribute(a, v);
      });
    });
    $$('[data-num]').forEach(el => { el.textContent = group(+el.dataset.num); });
    const L = t();
    if (L.titles && L.titles[PAGE]) document.title = L.titles[PAGE];
    const md = $('meta[name="description"]');
    if (md && L.descs && L.descs[PAGE]) md.setAttribute('content', L.descs[PAGE]);
    $$('[data-lang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === LANG)));
    root.classList.toggle('lang-en', LANG === 'en');
    langHooks.forEach(f => { try { f(); } catch (e) { /* ok */ } });
  }

  /* ---------- toast ---------- */
  const toastEl = $('#toast');
  let toastTimer;
  const toast = msg => {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add('in');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => toastEl.classList.remove('in'), 2600);
  };

  /* ---------- przewijanie ---------- */
  function scrollToY(y, instant) {
    if (lenis) { lenis.scrollTo(y, instant ? { immediate: true } : { duration: 1.2 }); return; }
    if (instant || RM) {
      const prev = root.style.scrollBehavior;
      root.style.scrollBehavior = 'auto';
      window.scrollTo(0, y);
      root.style.scrollBehavior = prev;
    } else window.scrollTo({ top: y, behavior: 'smooth' });
  }
  function scrollToEl(el, instant) {
    if (!el) return;
    scrollToY(Math.max(0, el.getBoundingClientRect().top + scrollY - 76), instant);
  }
  function handleHash(hash) {
    const id = decodeURIComponent((hash || '').slice(1));
    if (!id) return;
    for (const h of hashHandlers) if (h(id)) return;
    scrollToEl(document.getElementById(id));
  }

  /* ---------- reveal ---------- */
  mod('reveal', () => {
    const els = $$('.reveal, [data-split], .foot__word');
    if (!('IntersectionObserver' in window)) { els.forEach(e => e.classList.add('in')); return; }
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: 0, rootMargin: '0px 0px -8% 0px' });
    gate.then(() => els.forEach(el => io.observe(el)));
  });
  window.__msReady = true;

  /* =====================================================================
     PRZEJŚCIA MIĘDZY PODSTRONAMI
     Kurtyna wjeżdża z etykietą strony docelowej (numer, nazwa, hasło),
     a nowa strona startuje zasłonięta tą samą etykietą i ją odsłania.
     Kierunek zależy od kolejności podstron: dalej = z dołu, wstecz = z góry.
     ===================================================================== */
  // Kurtyna jedzie na transform (GPU) — płynnie także na słabych telefonach.
  // Napis stoi w miejscu i ma stały rozmiar; podpis rysuje się jak pasek ładowania
  // (postęp liczony od chwili kliknięcia, więc na nowej stronie rysuje się dalej bez skoku).
  let leaving = false;
  const LEAVE_MS = 680;
  function goTo(href, key) {
    if (leaving) return;
    const curtain = $('#curtain');
    if (!curtain || RM) { location.href = href; return; }
    leaving = true;
    const L = (t().pages || {})[key] || { t: key, s: '' };
    const cT = $('.curtain__t', curtain);
    $('.curtain__n', curtain).textContent = `(${NUMS[key] || '—'})`;
    cT.textContent = L.t;
    cT.classList.toggle('is-long', String(L.t).length > 9);
    $('.curtain__s', curtain).textContent = L.s;
    const oTo = key in ORDER ? ORDER[key] : 9, oFrom = PAGE in ORDER ? ORDER[PAGE] : 0;
    const dir = oTo < oFrom ? 'back' : 'fwd';
    root.classList.remove('is-arriving', 'is-revealing');
    root.setAttribute('data-dir', dir);
    // kontekst: podkreślenie w menu od razu przeskakuje na cel
    $$('[data-nav]').forEach(l => l.classList.toggle('is-active', l.dataset.nav === key));
    if (menuCtl.open) menuCtl.set(false);
    if (lenis) lenis.stop();
    const cur = $('#cursor');
    if (cur) { cur.classList.remove('view', 'big'); cur.classList.add('dark', 'lock'); }
    const t0 = Date.now();
    void curtain.offsetWidth;
    root.classList.add('is-leaving');
    if (window.__msSig) window.__msSig.start(t0);
    sess.set('ms-nav', JSON.stringify({ to: key, from: PAGE, dir, t: t0 }));
    setTimeout(() => { location.href = href; }, LEAVE_MS);
  }

  mod('links', () => {
    document.addEventListener('click', e => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = e.target.closest && e.target.closest('a[href]');
      if (!a) return;
      const raw = a.getAttribute('href') || '';
      if (/^(mailto:|tel:|javascript:)/i.test(raw) || a.hasAttribute('download') || (a.target && a.target !== '_self')) return;
      let url;
      try { url = new URL(a.href, location.href); } catch (err) { return; }
      if (url.origin !== location.origin) return;
      const key = keyOf(url);
      if (url.pathname === location.pathname || (key && key === PAGE)) {
        e.preventDefault();
        if (menuCtl.open) menuCtl.set(false);
        if (url.hash && url.hash.length > 1) {
          if (location.hash !== url.hash) { try { history.pushState(null, '', url.hash); } catch (err) { /* ok */ } }
          handleHash(url.hash);
        } else scrollToY(0);
        return;
      }
      if (!key || !(key in ORDER)) return;
      e.preventDefault();
      goTo(url.href, key);
    });
    addEventListener('popstate', () => handleHash(location.hash));
  });

  /* ---------- wejście na stronę zza kurtyny ---------- */
  // podpis dorysowuje się do końca, dopiero potem kurtyna odsłania stronę
  let revealed = false;
  const reveal = () => {
    if (revealed) return;
    revealed = true;
    root.classList.add('is-revealing');
    setTimeout(openGate, 200);
    setTimeout(() => { root.classList.remove('is-arriving', 'is-revealing'); root.removeAttribute('data-dir'); }, 880);
  };
  const finishThenReveal = () => {
    const sig = window.__msSig;
    if (sig) sig.finish(reveal); else reveal();
    setTimeout(reveal, 1500); // bezpiecznik
  };
  mod('arrive', () => {
    if (!ARRIVING) { openGate(); return; }
    const fonts = document.fonts && document.fonts.ready ? Promise.race([document.fonts.ready, wait(600)]) : wait(0);
    fonts.then(finishThenReveal, finishThenReveal);
  });

  /* ---------- powrót przyciskiem „wstecz” (bfcache) ---------- */
  addEventListener('pageshow', e => {
    if (!e.persisted) return;
    leaving = false;
    sess.del('ms-nav');
    const c = $('#curtain');
    if (menuCtl.open) menuCtl.set(false);
    $$('[data-nav]').forEach(l => l.classList.toggle('is-active', l.dataset.nav === PAGE));
    if (c && root.classList.contains('is-leaving')) {
      root.classList.remove('is-leaving');
      root.classList.add('is-arriving');
      root.setAttribute('data-dir', 'back');
      revealed = false;
      finishThenReveal();
    }
    const cu = $('#cursor');
    if (cu) cu.classList.remove('lock', 'dark');
    if (lenis) lenis.start();
  });

  /* ---------- wstępne pobieranie podstron (przejście startuje od razu) ---------- */
  mod('prefetch', () => {
    const done = new Set([location.pathname]);
    const pf = a => {
      let url;
      try { url = new URL(a.href, location.href); } catch (e) { return; }
      if (url.origin !== location.origin) return;
      const key = keyOf(url);
      if (!key || !(key in ORDER) || done.has(url.pathname)) return;
      done.add(url.pathname);
      const l = document.createElement('link');
      l.rel = 'prefetch'; l.href = url.pathname;
      document.head.appendChild(l);
    };
    const on = e => { const a = e.target.closest && e.target.closest('a[href]'); if (a) pf(a); };
    document.addEventListener('pointerover', on, { passive: true });
    document.addEventListener('touchstart', on, { passive: true });
    document.addEventListener('focusin', on);
    const idle = window.requestIdleCallback || (f => setTimeout(f, 1800));
    idle(() => { const n = $('a.next'); if (n) pf(n); });
  });

  /* ---------- kurtyna intro (pierwsza wizyta na starcie) ---------- */
  mod('cinema', () => {
    const c = $('#cinema');
    if (!c) return;
    if (root.classList.contains('no-cinema')) { c.remove(); return; }
    setTimeout(() => c.remove(), RM ? 0 : 1700);
  });

  /* ---------- żywe tło: miękkie światło na papierze (canvas w małej rozdzielczości) ---------- */
  mod('bg', () => {
    const cv = $('.bg__cv');
    if (!cv || !cv.getContext) return;
    const ctx = cv.getContext('2d', { alpha: false });
    const SC = 0.12;
    const P = {
      index: [[0.14, 0.10], [0.84, 0.34], [0.38, 0.92]],
      prace: [[0.78, 0.14], [0.18, 0.62], [0.70, 0.96]],
      uslugi: [[0.30, 0.88], [0.72, 0.12], [0.06, 0.30]],
      cennik: [[0.88, 0.78], [0.26, 0.20], [0.60, 0.44]],
      'o-mnie': [[0.08, 0.60], [0.62, 0.84], [0.90, 0.08]],
      kontakt: [[0.62, 0.06], [0.10, 0.24], [0.84, 0.86]]
    };
    const B = [
      { r: 0.80, c: '222,217,203', a: 0.85, f: [0.000071, 0.000053], ph: [0.0, 1.7], amp: [0.08, 0.07] },
      { r: 0.64, c: '255,255,252', a: 0.95, f: [0.000047, 0.000061], ph: [2.1, 0.4], amp: [0.09, 0.08] },
      { r: 0.58, c: '210,207,196', a: 0.58, f: [0.000059, 0.000043], ph: [4.2, 2.9], amp: [0.10, 0.06] }
    ];
    const from = P[root.dataset.bg] || P[PAGE] || P.index;
    const to = P[PAGE] || P.index;
    root.dataset.bg = PAGE;
    let blendStart = 0, W = 0, H = 0, vt = Date.now(), lastReal = 0;
    const size = () => {
      const w = Math.max(48, Math.round(innerWidth * SC)), h = Math.max(48, Math.round(innerHeight * SC));
      if (w === W && h === H) return;
      W = w; H = h; cv.width = W; cv.height = H;
    };
    size();
    let lx = -1, ly = -1, tlx = -1, tly = -1, la = 0;
    if (FINE && !RM) {
      addEventListener('pointermove', e => {
        if (e.pointerType !== 'mouse') return;
        tlx = e.clientX; tly = e.clientY;
        if (lx < 0) { lx = tlx; ly = tly; }
      }, { passive: true });
    }
    const ease = x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
    const draw = now => {
      // „czas tła” płynie tylko, gdy rysujemy — po pauzie nie ma przeskoku
      vt += lastReal ? Math.min(66, now - lastReal) : 0;
      lastReal = now;
      const time = vt;
      if (!blendStart && gateOpen) blendStart = now;
      const k = from === to ? 1 : (blendStart ? ease(clamp((now - blendStart) / 2400, 0, 1)) : 0);
      ctx.fillStyle = '#f4f3ef';
      ctx.fillRect(0, 0, W, H);
      const M = Math.max(W, H);
      const doc = document.documentElement;
      const prog = clamp(scrollY / Math.max(1, doc.scrollHeight - innerHeight), 0, 1);
      B.forEach((b, i) => {
        const bx = lerp(from[i][0], to[i][0], k), by = lerp(from[i][1], to[i][1], k);
        const dx = RM ? 0 : Math.sin(time * b.f[0] + b.ph[0]) * b.amp[0];
        const dy = RM ? 0 : Math.cos(time * b.f[1] + b.ph[1]) * b.amp[1];
        const x = (bx + dx) * W, y = (by + dy - prog * 0.22 * (i === 1 ? -1 : 1)) * H;
        const r = b.r * M * (1 + (RM ? 0 : Math.sin(time * b.f[0] * 1.3 + i) * 0.06));
        const g = ctx.createRadialGradient(x, y, 0, x, y, r);
        g.addColorStop(0, `rgba(${b.c},${b.a})`);
        g.addColorStop(1, `rgba(${b.c},0)`);
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, W, H);
      });
      if (tlx >= 0) {
        lx = lerp(lx, tlx, 0.09); ly = lerp(ly, tly, 0.09); la = Math.min(0.5, la + 0.02);
        const x = lx * SC, y = ly * SC, r = M * 0.34;
        const g = ctx.createRadialGradient(x, y, 0, x, y, r);
        g.addColorStop(0, `rgba(255,255,255,${la.toFixed(3)})`);
        g.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, W, H);
      }
    };
    resizeFns.push(() => { size(); draw(performance.now()); });
    if (RM) { draw(performance.now()); return; }
    // Komputer: stały, powolny ruch (30 kl./s). Telefon i słabszy sprzęt: rysuje tylko, gdy coś
    // się dzieje (wejście na stronę, przewijanie) — tło dalej żyje, a procesor i bateria odpoczywają.
    let last = 0, raf = 0, until = 0;
    const continuous = () => FINE && !isLite();
    const loop = now => {
      raf = 0;
      if (document.hidden || leaving) return;
      if (now - last >= (continuous() ? 33 : 50)) { last = now; draw(now); }
      if (continuous() || now < until) raf = requestAnimationFrame(loop);
    };
    const kick = ms => {
      until = Math.max(until, performance.now() + (ms || 0));
      if (!raf) raf = requestAnimationFrame(loop);
    };
    draw(performance.now());
    kick(0);
    scrollFns.push(() => kick(260));
    gate.then(() => kick(2700));
    document.addEventListener('visibilitychange', () => { if (!document.hidden) kick(0); });
    addEventListener('pageshow', e => { if (e.persisted) kick(2700); });
    liteHooks.push(() => kick(0));
  });

  /* ---------- nawigacja ---------- */
  mod('nav', () => {
    const nav = $('#nav');
    if (!nav) return;
    let prevY = scrollY, down = 0, up = 0;
    scrollFns.push(() => {
      const y = scrollY, dy = y - prevY;
      prevY = y;
      nav.classList.toggle('is-scrolled', y > 20);
      if (dy > 0) { down += dy; up = 0; } else if (dy < 0) { up -= dy; down = 0; }
      if (menuCtl.open) { nav.classList.remove('is-hidden'); return; }
      if (y > 560 && down > 70) nav.classList.add('is-hidden');
      if (up > 26 || y < 560) nav.classList.remove('is-hidden');
    });
    nav.addEventListener('focusin', () => nav.classList.remove('is-hidden'));
  });

  /* ---------- menu mobilne ---------- */
  mod('menu', () => {
    const btn = $('#menuBtn'), m = $('#mmenu');
    if (!btn || !m) return;
    const label = () => { btn.textContent = menuCtl.open ? t().menuClose : t().menu; };
    menuCtl.set = v => {
      menuCtl.open = v;
      m.classList.toggle('is-open', v);
      if (v) m.removeAttribute('inert'); else m.setAttribute('inert', '');
      btn.setAttribute('aria-expanded', String(v));
      root.classList.toggle('no-scroll', v);
      if (lenis) { if (v) lenis.stop(); else if (!leaving) lenis.start(); }
      label();
    };
    btn.addEventListener('click', () => menuCtl.set(!menuCtl.open));
    addEventListener('keydown', e => { if (e.key === 'Escape' && menuCtl.open) { menuCtl.set(false); btn.focus(); } });
    const wide = matchMedia('(min-width: 1024px)');
    const onWide = e => { if (e.matches && menuCtl.open) menuCtl.set(false); };
    if (wide.addEventListener) wide.addEventListener('change', onWide); else if (wide.addListener) wide.addListener(onWide);
    langHooks.push(label);
  });

  /* ---------- pasek postępu ---------- */
  mod('progress', () => {
    const bar = $('#progress');
    if (!bar) return;
    let docH = 0;
    const measure = () => { docH = root.scrollHeight; };
    if ('ResizeObserver' in window) new ResizeObserver(measure).observe(document.body);
    scrollFns.push(() => {
      if (!docH || !('ResizeObserver' in window)) measure();
      const h = docH - innerHeight;
      bar.style.transform = `scaleX(${h > 0 ? clamp(scrollY / h, 0, 1).toFixed(4) : 0})`;
    });
  });

  /* ---------- start: przypięte intro (nazwisko stoi, napisy w tle jadą) ---------- */
  mod('pin', () => {
    const pin = $('#pin');
    if (!pin) return;
    const ghosts = $$('.ghost-row', pin), blobs = $$('.blob', pin), hint = $('#scrollHint');
    let VH = innerHeight, W = innerWidth, last = -1;
    addEventListener('resize', () => {
      if (innerWidth !== W || Math.abs(innerHeight - VH) > 160) { W = innerWidth; VH = innerHeight; }
    }, { passive: true });
    scrollFns.push(() => {
      const total = Math.max(1, pin.offsetHeight - VH);
      const p = clamp((scrollY - pin.offsetTop) / total, 0, 1);
      if (Math.abs(p - last) < 0.0005) return;
      last = p;
      if (hint) hint.style.opacity = p > 0.06 ? '0' : '1';
      if (RM) return;
      ghosts.forEach((g, i) => {
        const x = i % 2 === 0 ? -p * 34 : (p - 1) * 34;
        g.style.transform = `translate3d(${x.toFixed(3)}%,0,0)`;
      });
      blobs.forEach((b, i) => {
        const d = i % 2 === 0 ? 1 : -1;
        b.style.transform = `translate3d(${(d * p * 60).toFixed(1)}px,${(d * p * -42).toFixed(1)}px,0) scale(${(1 + p * 0.35).toFixed(3)})`;
      });
    });
  });

  /* ---------- start: rotujące słowo w nagłówku ---------- */
  mod('rotator', () => {
    const el = $('[data-rotator]');
    if (!el) return;
    let nodes = [], idx = 0, timer = null, visible = true, started = false;
    const build = words => {
      el.innerHTML = '';
      nodes = (words || ['pracuje,']).map((w, i) => {
        const s = document.createElement('span');
        s.className = 'rot__w' + (i === 0 ? ' is-on' : '');
        s.textContent = w;
        el.appendChild(s);
        return s;
      });
      idx = 0;
    };
    const next = () => {
      const c = nodes[idx];
      idx = (idx + 1) % nodes.length;
      const n = nodes[idx];
      c.classList.remove('is-on'); c.classList.add('is-out');
      n.classList.add('no-t'); n.classList.remove('is-out'); void n.offsetWidth;
      n.classList.remove('no-t'); n.classList.add('is-on');
      setTimeout(() => { c.classList.add('no-t'); c.classList.remove('is-out'); void c.offsetWidth; c.classList.remove('no-t'); }, 1050);
    };
    const start = () => { if (!started || RM || timer || !visible || document.hidden || nodes.length < 2) return; timer = setInterval(next, 2600); };
    const stop = () => { clearInterval(timer); timer = null; };
    build(t().rot);
    if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) start(); else stop(); }).observe(el);
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    gate.then(() => setTimeout(() => { started = true; start(); }, 1600));
    langHooks.push(() => { stop(); build(t().rot); start(); });
  });

  /* ---------- belka z hasłami (reaguje na prędkość scrolla) ---------- */
  mod('marquee', () => {
    const band = $('.band'), track = $('[data-marquee]');
    if (!band || !track) return;
    const item = track.firstElementChild;
    let x = 0, w = 0, dir = 1, boost = 0, run = false, last = 0, prevY = scrollY;
    const fill = () => {
      $$('.band__item', track).forEach((n, i) => { if (i) n.remove(); });
      w = item.getBoundingClientRect().width;
      let g = 0;
      while (track.scrollWidth < innerWidth * 2 + w && g++ < 8) track.appendChild(item.cloneNode(true));
    };
    const loop = now => {
      if (!run) return;
      const dt = Math.min(64, now - (last || now));
      last = now;
      boost *= 0.92;
      x -= (0.045 + boost) * dt * dir;
      if (w) { if (x <= -w) x += w; if (x > 0) x -= w; }
      track.style.transform = `translate3d(${x.toFixed(2)}px,0,0)`;
      requestAnimationFrame(loop);
    };
    fill();
    scrollFns.push(() => {
      const dy = scrollY - prevY;
      prevY = scrollY;
      if (Math.abs(dy) > 0.5) { dir = dy > 0 ? 1 : -1; boost = clamp(boost + Math.abs(dy) * 0.0022, 0, 0.9); }
    });
    resizeFns.push(fill);
    langHooks.push(fill);
    if (document.fonts) document.fonts.ready.then(fill);
    if (!RM && 'IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => {
        if (e.isIntersecting && !run) { run = true; last = 0; requestAnimationFrame(loop); } else if (!e.isIntersecting) run = false;
      }).observe(band);
    }
  });

  /* ---------- wybrane projekty: poziomy scroll ---------- */
  mod('hs', () => {
    const hs = $('#hs'), track = $('#hsTrack');
    if (!hs || !track) return;
    const count = $('#hsCount'), bar = $('#hsBar'), cards = $$('.pc', track);
    let pin = false, dist = 0;
    const setUI = p => {
      const i = clamp(Math.round(p * (cards.length - 1)), 0, cards.length - 1);
      if (count) count.textContent = `0${i + 1} / 0${cards.length}`;
      if (bar) bar.style.setProperty('--p', (0.25 + p * 0.75).toFixed(3));
    };
    const update = () => {
      if (!pin) return;
      const r = hs.getBoundingClientRect();
      const total = hs.offsetHeight - innerHeight;
      const p = total > 0 ? clamp(-r.top / total, 0, 1) : 0;
      track.style.transform = `translate3d(${(-p * dist).toFixed(1)}px,0,0)`;
      setUI(p);
    };
    const setup = () => {
      pin = innerWidth >= 1024 && !RM;
      hs.classList.toggle('hs--pin', pin);
      track.style.transform = '';
      if (pin) {
        const lastCard = cards[cards.length - 1];
        const gut = parseFloat(getComputedStyle(track).paddingRight) || 24;
        dist = Math.max(0, lastCard.offsetLeft + lastCard.offsetWidth + gut - root.clientWidth);
        hs.style.height = (dist + innerHeight) + 'px';
      } else hs.style.height = '';
      update();
    };
    track.addEventListener('scroll', () => {
      if (pin) return;
      const max = track.scrollWidth - track.clientWidth;
      setUI(max > 0 ? track.scrollLeft / max : 0);
    }, { passive: true });
    scrollFns.push(update);
    resizeFns.push(setup);
    setup();
    if (document.fonts) document.fonts.ready.then(setup);
    addEventListener('load', setup);
    // obracające się światło na karcie CTA pracuje tylko, gdy karta jest na ekranie
    const cta = $('.pc--cta', track);
    if (cta && 'IntersectionObserver' in window) new IntersectionObserver(([e]) => cta.classList.toggle('is-vis', e.isIntersecting)).observe(cta);
  });

  /* ---------- karta CTA (prace): obracające się światło tylko, gdy karta jest na ekranie ---------- */
  mod('ctaSpin', () => {
    const cards = $$('.cta-card');
    if (!cards.length || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('is-vis', e.isIntersecting)));
    cards.forEach(c => io.observe(c));
  });

  /* ---------- ilustracje usług: animują się tylko, gdy są widoczne ---------- */
  mod('play', () => {
    const els = $$('[data-play]');
    if (!els.length || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('play', e.isIntersecting && !RM)), { threshold: 0.2 });
    gate.then(() => els.forEach(el => io.observe(el)));
  });

  /* ---------- proces: linia rysuje się przy scrollu ---------- */
  mod('steps', () => {
    const wrap = $('#steps');
    if (!wrap) return;
    const line = $('.steps__line', wrap), steps = $$('.step', wrap);
    const dots = steps.map(s => $('.step__dot', s));
    scrollFns.push(() => {
      const r = line.getBoundingClientRect();
      if (r.bottom < -200 || r.top > innerHeight + 200) return;
      const horiz = r.width > r.height;
      const len = Math.max(1, horiz ? r.width : r.height);
      const p = horiz ? clamp((innerHeight * 0.85 - r.top) / (innerHeight * 0.45), 0, 1) : clamp((innerHeight * 0.72 - r.top) / len, 0, 1);
      // najpierw wszystkie odczyty, potem zapisy (bez wymuszania przeliczeń w każdej klatce)
      const pos = dots.map(d => { const b = d.getBoundingClientRect(); return horiz ? b.left + b.width / 2 - r.left : b.top + b.height / 2 - r.top; });
      wrap.style.setProperty('--p', p.toFixed(4));
      steps.forEach((s, i) => s.classList.toggle('is-on', p * len >= pos[i] - 1));
    });
  });

  /* ---------- liczniki ---------- */
  mod('counters', () => {
    const els = $$('[data-count]');
    if (!els.length || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      const el = e.target, to = +el.dataset.count;
      if (RM || to === 0) { el.textContent = to; return; }
      const t0 = performance.now(), dur = 1500;
      const tick = now => {
        const k = clamp((now - t0) / dur, 0, 1);
        el.textContent = Math.round(to * (1 - Math.pow(1 - k, 4)));
        if (k < 1) requestAnimationFrame(tick);
      };
      el.textContent = '0';
      requestAnimationFrame(tick);
    }), { threshold: 0.6 });
    gate.then(() => els.forEach(el => io.observe(el)));
  });

  /* ---------- o mnie: przesuwający się napis w tle ---------- */
  mod('ghost', () => {
    const g = $('[data-ghost]');
    if (!g || RM) return;
    const sec = g.parentElement;
    scrollFns.push(() => {
      const r = sec.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      const p = (innerHeight - r.top) / (innerHeight + r.height);
      g.style.transform = `translate3d(${(-p * 18).toFixed(2)}%,0,0)`;
    });
  });

  /* ---------- podpis rysuje się jak długopisem ---------- */
  mod('sig', () => {
    $$('svg.sig').forEach(svg => {
      const paths = $$('path', svg);
      if (!paths.length) return;
      const lens = paths.map(p => { try { return p.getTotalLength(); } catch (e) { return 0; } });
      const total = lens.reduce((a, b) => a + b, 0) || 1;
      const onCard = !!svg.closest('.bcard');
      const DUR = onCard ? 1.9 : 2.6;
      let acc = 0;
      paths.forEach((p, i) => {
        const d = Math.max(0.035, lens[i] / total * DUR);
        p.style.setProperty('--len', (lens[i] + 1).toFixed(1));
        p.style.setProperty('--dur', d.toFixed(3) + 's');
        p.style.setProperty('--dl', acc.toFixed(3) + 's');
        acc += d * 0.9;
      });
      svg.classList.add('is-ready');
      if (onCard) return;
      if (RM || !('IntersectionObserver' in window)) { svg.classList.add('is-drawn'); return; }
      const io = new IntersectionObserver(([e]) => {
        if (e.isIntersecting) { io.disconnect(); setTimeout(() => svg.classList.add('is-drawn'), 380); }
      }, { threshold: 0.35 });
      gate.then(() => io.observe(svg));
    });
  });

  /* ---------- cennik: zakładki z przesuwaną kreską ---------- */
  let selectTab = () => {};
  mod('tabs', () => {
    const list = $('.tabs[role="tablist"]');
    if (!list) return;
    const tabs = $$('[role="tab"]', list), ind = $('.tabs__ind', list);
    if (ind) list.classList.add('has-ind');
    const place = () => {
      const c = tabs.find(x => x.getAttribute('aria-selected') === 'true');
      if (!c || !ind) return;
      ind.style.width = c.offsetWidth + 'px';
      ind.style.transform = `translateX(${c.offsetLeft}px)`;
    };
    selectTab = (key, focus) => {
      if (!tabs.some(x => x.dataset.tab === key)) return;
      tabs.forEach(tb => {
        const on = tb.dataset.tab === key;
        tb.setAttribute('aria-selected', String(on));
        tb.tabIndex = on ? 0 : -1;
        const panel = document.getElementById(tb.getAttribute('aria-controls'));
        if (panel) panel.hidden = !on;
        if (on && focus) tb.focus();
        if (on && list.scrollWidth > list.clientWidth) {
          const left = Math.max(0, tb.offsetLeft - 24);
          try { list.scrollTo({ left, behavior: RM ? 'auto' : 'smooth' }); } catch (e) { list.scrollLeft = left; }
        }
      });
      place();
    };
    tabs.forEach((tb, i) => {
      tb.addEventListener('click', () => {
        selectTab(tb.dataset.tab);
        try { history.replaceState(null, '', '#' + tb.dataset.tab); } catch (e) { /* ok */ }
      });
      tb.addEventListener('keydown', e => {
        let j = null;
        if (e.key === 'ArrowRight') j = (i + 1) % tabs.length;
        else if (e.key === 'ArrowLeft') j = (i - 1 + tabs.length) % tabs.length;
        else if (e.key === 'Home') j = 0;
        else if (e.key === 'End') j = tabs.length - 1;
        if (j !== null) { e.preventDefault(); selectTab(tabs[j].dataset.tab, true); }
      });
    });
    hashHandlers.push(id => {
      if (!tabs.some(x => x.dataset.tab === id)) return false;
      selectTab(id);
      scrollToEl($('#pakiety'));
      return true;
    });
    const h = decodeURIComponent(location.hash.slice(1));
    if (h && tabs.some(x => x.dataset.tab === h)) {
      selectTab(h);
      requestAnimationFrame(() => scrollToEl($('#pakiety'), true));
    }
    place();
    resizeFns.push(place);
    langHooks.push(() => requestAnimationFrame(place));
    if (document.fonts) document.fonts.ready.then(place);
  });

  /* ---------- animowane liczby ---------- */
  function tweenNum(el, from, to) {
    if (RM || from === to) { el.textContent = group(to); return; }
    const t0 = performance.now(), dur = 600;
    const tick = now => {
      const k = clamp((now - t0) / dur, 0, 1), e = 1 - Math.pow(1 - k, 4);
      el.textContent = group(from + (to - from) * e);
      if (k < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  /* ---------- social: przełącznik platformy ---------- */
  let plat = 'fb';
  mod('social', () => {
    const btns = $$('[data-plat]');
    if (!btns.length) return;
    const update = animate => {
      btns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.plat === plat)));
      $$('[data-social]').forEach(card => {
        const price = +card.dataset[plat === 'fb' ? 'fb' : 'fbig'];
        const el = $('[data-social-price]', card), prev = +(el.dataset.v || price);
        el.dataset.v = price;
        if (animate) tweenNum(el, prev, price); else el.textContent = group(price);
        $('[data-social-pp]', card).textContent = t().perPost(Math.round(price / +card.dataset.posts));
      });
    };
    btns.forEach(b => b.addEventListener('click', () => { plat = b.dataset.plat; update(true); }));
    langHooks.push(() => update(false));
  });

  /* ---------- kalkulator (ceny czytane z kart cennika) ---------- */
  let lastSummary = '', lastHead = '', calcRender = () => {}, S = { on: {} };
  mod('calc', () => {
    const calcEl = $('#calc');
    if (!calcEl) return;
    const card = sel => $(sel);
    const addon = k => { const li = $(`[data-addon="${k}"]`); return { min: +li.dataset.min, max: +li.dataset.max }; };
    const P = {
      pkg: {
        landing: { price: +card('[data-pkg="landing"]').dataset.price, days: card('[data-pkg="landing"]').dataset.days },
        wizytowka: { price: +card('[data-pkg="wizytowka"]').dataset.price, days: card('[data-pkg="wizytowka"]').dataset.days },
        sklep: { price: 0, days: '' }
      },
      sub: addon('subpage'), gfx: addon('graphics'), lng: addon('lang'), exp: addon('express'),
      host: +card('[data-host="first"]').dataset.price,
      social: {
        start: { fb: +card('[data-social="start"]').dataset.fb, fbig: +card('[data-social="start"]').dataset.fbig },
        pro: { fb: +card('[data-social="pro"]').dataset.fb, fbig: +card('[data-social="pro"]').dataset.fbig }
      },
      card: +card('[data-nfc="card"]').dataset.price, sticker: +card('[data-nfc="sticker"]').dataset.price
    };
    S = { on: { www: true, social: false, nfc: false }, subpages: 0, cards: 1, stickers: 0 };
    const val = name => { const i = $(`input[name="${name}"]:checked`, calcEl); return i ? i.value : null; };
    const chk = name => $(`input[name="${name}"]`, calcEl).checked;
    $$('.cg', calcEl).forEach(g => {
      const key = g.dataset.group, sw = $('.sw', g);
      $('[data-toggle]', g).addEventListener('click', () => {
        S.on[key] = !S.on[key];
        g.classList.toggle('is-on', S.on[key]);
        sw.setAttribute('aria-checked', String(S.on[key]));
        calcRender();
      });
    });
    $$('[data-stepper]', calcEl).forEach(st => {
      const key = st.dataset.stepper, out = $('output', st);
      const [minus, plus] = $$('button', st);
      const sync = () => { out.textContent = S[key]; minus.disabled = S[key] <= 0; plus.disabled = S[key] >= 20; };
      st.addEventListener('click', e => {
        const b = e.target.closest('[data-step]');
        if (!b) return;
        S[key] = clamp(S[key] + +b.dataset.step, 0, 20); sync(); calcRender();
      });
      sync();
    });
    calcEl.addEventListener('change', () => calcRender());
    const once = $('#sumOnce');
    calcRender = () => {
      const L = t().calc, lines = [];
      let min = 0, approx = false, custom = false, monthly = 0, time = '—';
      if (S.on.www) {
        const pk = val('pkg');
        if (pk === 'sklep') { custom = true; lines.push([L.names.sklep, L.custom]); time = L.tbd; }
        else {
          const p = P.pkg[pk]; min += p.price; approx = true;
          lines.push([L.names[pk], `${L.from} ${money(p.price)}`]);
          const [a, b] = p.days.split('-').map(Number);
          time = chk('express') ? `${Math.ceil(a / 2)}–${Math.ceil(b / 2)} ${L.days}` : `${a}–${b} ${L.days}`;
        }
        if (S.subpages) { min += S.subpages * P.sub.min; approx = true; lines.push([`${L.subpages} × ${S.subpages}`, range(S.subpages * P.sub.min, S.subpages * P.sub.max)]); }
        if (chk('lang')) { min += P.lng.min; approx = true; lines.push([L.lang, range(P.lng.min, P.lng.max)]); }
        if (chk('graphics')) { min += P.gfx.min; approx = true; lines.push([L.graphics, range(P.gfx.min, P.gfx.max)]); }
        if (chk('express')) {
          if (pk === 'sklep') lines.push([L.express, L.custom]);
          else {
            const base = P.pkg[pk].price, a = Math.round(base * P.exp.min / 100), b = Math.round(base * P.exp.max / 100);
            min += a; approx = true; lines.push([L.express, range(a, b)]);
          }
        }
        if (chk('hosting')) { min += P.host; lines.push([L.host, money(P.host)]); }
      }
      if (S.on.social) {
        const sp = val('spkg'), pl = val('plat');
        monthly = P.social[sp][pl];
        lines.push([`${L.social} ${sp === 'pro' ? 'Pro' : 'Start'} · ${pl === 'fb' ? 'FB' : 'FB + IG'}`, `${money(monthly)} ${L.perMonth}`]);
      }
      if (S.on.nfc) {
        if (S.cards) { min += S.cards * P.card; lines.push([`${L.card} × ${S.cards}`, money(S.cards * P.card)]); }
        if (S.stickers) { min += S.stickers * P.sticker; lines.push([`${L.sticker} × ${S.stickers}`, money(S.stickers * P.sticker)]); }
      }
      const prev = +(once.dataset.v || 0);
      if (!min && custom) {
        once.classList.add('txt'); once.innerHTML = `<b>${L.custom}</b>`; once.dataset.v = 0;
      } else {
        once.classList.remove('txt');
        once.innerHTML = `${approx ? `<small>${L.from}</small>` : ''}<b>${group(prev)}</b><span>${cur()}</span>${custom ? `<i>+ ${L.shopShort}</i>` : ''}`;
        tweenNum($('b', once), prev, min); once.dataset.v = min;
      }
      $('#sumMonthly').textContent = monthly ? `${money(monthly)} ${L.perMonth}` : '—';
      $('#sumTime').textContent = time;
      $('#sumLines').innerHTML = lines.length
        ? lines.map(([a, b]) => `<li><span>${a}</span><b>${b}</b></li>`).join('')
        : `<li><span>${L.empty}</span></li>`;
      const txt = lines.map(([a, b]) => `• ${a}: ${b}`).join('\n');
      lastHead = min ? `${approx ? L.from + ' ' : ''}${money(min)}${custom ? ' + ' + L.shopShort : ''}` : (custom ? L.custom : '');
      lastSummary = lines.length ? `${L.mailIntro}\n${txt}${lastHead ? `\n${L.onceLbl}: ${lastHead}` : ''}${monthly ? `\n${L.monthlyLbl}: ${money(monthly)}` : ''}` : '';
    };
    langHooks.push(() => calcRender());
  });

  /* ---------- wybór pakietu → gotowa wiadomość w formularzu (między podstronami) ---------- */
  mod('prefill', () => {
    const save = (text, needs, label) => sess.set('ms-prefill', JSON.stringify({ text, needs, label }));
    document.addEventListener('click', e => {
      const b = e.target.closest && e.target.closest('[data-pick]');
      if (!b) return;
      const k = b.dataset.pick, P2 = t().pick, PL2 = t().pickLabel;
      if (k === 'social-start' || k === 'social-pro') {
        const pk = k === 'social-pro' ? 'Pro' : 'Start';
        const c = $(`[data-social="${k === 'social-pro' ? 'pro' : 'start'}"]`);
        const price = c ? +c.dataset[plat === 'fb' ? 'fb' : 'fbig'] : 0;
        const pl = plat === 'fb' ? 'Facebook' : 'Facebook + Instagram';
        save(P2.social(pk, pl, money(price)), ['social'], PL2.social(pk, pl));
      } else if (k.indexOf('nfc') === 0) save(P2[k], ['nfc'], PL2[k]);
      else if (k.indexOf('concept-') === 0) { const n = CONCEPTS[k.slice(8)] || ''; save(P2.concept(n), ['www'], PL2.concept(n)); }
      else if (P2[k]) save(P2[k], ['www'], PL2[k]);
    }, true);
    const send = $('#sumSend');
    if (send) send.addEventListener('click', () => {
      calcRender();
      if (lastSummary) save(lastSummary, Object.keys(S.on).filter(k => S.on[k]), `${t().pickLabel.calc}${lastHead ? ': ' + lastHead : ''}`);
    }, true);

    const form = $('#leadForm'), msg = $('#f-msg');
    if (!form || !msg) return;
    let d = null;
    try { d = JSON.parse(sess.get('ms-prefill') || 'null'); } catch (e) { d = null; }
    if (!d) {
      let q = null;
      try { q = new URLSearchParams(location.search).get('projekt'); } catch (e) { /* ok */ }
      if (q && CONCEPTS[q]) d = { text: t().pick.concept(CONCEPTS[q]), needs: ['www'], label: t().pickLabel.concept(CONCEPTS[q]) };
    }
    if (!d || !d.text) return;
    sess.del('ms-prefill');
    msg.value = d.text;
    $$('input[name="need"]', form).forEach(c => { if ((d.needs || []).indexOf(c.value) > -1) c.checked = true; });
    const note = $('#prefill');
    if (note) {
      $('#prefillTxt').textContent = d.label ? ` — ${d.label}` : '';
      note.classList.add('is-on');
      $('#prefillX').addEventListener('click', () => {
        msg.value = '';
        $$('input[name="need"]', form).forEach(c => { c.checked = false; });
        note.classList.remove('is-on');
        msg.focus();
      });
    }
    // kontekst: po wejściu przewijamy prosto do formularza
    gate.then(() => setTimeout(() => {
      scrollToEl($('#formularz'));
      if (FINE) setTimeout(() => { const n = $('#f-name'); if (n && !n.value) n.focus({ preventScroll: true }); }, 900);
    }, ARRIVING ? 350 : 150));
  });

  /* ---------- FAQ ---------- */
  mod('faq', () => $$('.qa').forEach(qa => {
    const btn = $('button', qa);
    btn.addEventListener('click', () => {
      const open = !qa.classList.contains('is-open');
      qa.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
  }));

  /* ---------- kopiuj e-mail ---------- */
  mod('copy', () => {
    const copyText = async txt => {
      try { await navigator.clipboard.writeText(txt); return true; } catch (e) {
        const ta = document.createElement('textarea');
        ta.value = txt; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        let ok = false;
        try { ok = document.execCommand('copy'); } catch (e2) { ok = false; }
        ta.remove(); return ok;
      }
    };
    $$('[data-copy]').forEach(b => b.addEventListener('click', async () => {
      const ok = await copyText(b.dataset.copy), lbl = $('span', b) || b;
      if (!ok) { location.href = 'mailto:' + b.dataset.copy; return; }
      lbl.textContent = t().copiedShort; toast(t().copied);
      setTimeout(() => { lbl.textContent = t().copy; }, 2200);
    }));
  });

  /* ---------- zegar: Sieradz ---------- */
  mod('clock', () => {
    const time = $('#clockTime'), status = $('#clockStatus');
    if (!time || !status) return;
    const update = () => {
      let h = 12, m = 0;
      try {
        const parts = new Intl.DateTimeFormat('pl-PL', { timeZone: 'Europe/Warsaw', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
        h = +parts.find(p => p.type === 'hour').value % 24; m = +parts.find(p => p.type === 'minute').value;
      } catch (e) { const d = new Date(); h = d.getHours(); m = d.getMinutes(); }
      time.innerHTML = `${String(h).padStart(2, '0')}<i>:</i>${String(m).padStart(2, '0')}`;
      const C = t().clock;
      status.textContent = (h >= 7 && h < 21) ? C.work : (h >= 21 && h < 23) ? C.evening : C.night;
    };
    update(); setInterval(update, 20000);
    langHooks.push(update);
  });

  /* ---------- formularz: walidacja + wysyłka ---------- */
  mod('form', () => {
    const form = $('#leadForm');
    if (!form) return;
    const fName = $('#f-name'), fContact = $('#f-contact'), msg = $('#f-msg');
    const fieldErr = (input, text) => {
      const f = input.closest('.field');
      f.classList.toggle('err', !!text);
      $('.ferr', f).textContent = text || '';
      input.setAttribute('aria-invalid', text ? 'true' : 'false');
    };
    const validContact = v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) || v.replace(/\D/g, '').length >= 9;
    const validate = (focus = true) => {
      const F = t().form;
      let ok = true;
      if (fName.value.trim().length < 2) { fieldErr(fName, F.errName); ok = false; } else fieldErr(fName, '');
      const c = fContact.value.trim();
      if (!c) { fieldErr(fContact, F.errContact); ok = false; }
      else if (!validContact(c)) { fieldErr(fContact, F.errContactBad); ok = false; }
      else fieldErr(fContact, '');
      if (!ok && focus) { const bad = $('.err input', form); if (bad) bad.focus(); }
      return ok;
    };
    langHooks.push(() => { if ($('.field.err', form)) validate(false); });
    [fName, fContact].forEach(i => i.addEventListener('input', () => { if (i.closest('.field').classList.contains('err')) validate(false); }));
    const collect = () => ({
      name: fName.value.trim(), biz: $('#f-biz').value.trim(), contact: fContact.value.trim(),
      needs: $$('input[name="need"]:checked', form).map(c => c.nextElementSibling.textContent.trim()).join(', '),
      link: $('#f-link').value.trim(), msg: msg.value.trim()
    });
    const mailtoHref = d => {
      const F = t().form;
      const subject = `${F.mailSubject}${d.biz ? ' — ' + d.biz : ''}`;
      const body = [`${F.lblName}: ${d.name}`, d.biz ? `${F.lblBiz}: ${d.biz}` : '', `${F.lblContact}: ${d.contact}`,
        d.needs ? `${F.lblNeeds}: ${d.needs}` : '', d.link ? `${F.lblLink}: ${d.link}` : '']
        .filter(Boolean).concat(d.msg ? ['', d.msg] : []).join('\n');
      return `mailto:${EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    };
    const showSent = (mode, d) => {
      const F = t().form;
      $('#okTitle').textContent = mode === 'ajax' ? F.okAjaxT(d.name) : F.okMailT;
      $('#okText').innerHTML = mode === 'ajax' ? F.okAjaxD : F.okMailD(EMAIL);
      form.classList.add('is-sent');
    };
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!validate()) return;
      const d = collect();
      if ($('input[name="_honey"]', form).value) { showSent('ajax', d); return; }
      const btn = $('button[type="submit"]', form), lbl = $('span', btn), old = lbl.textContent;
      btn.disabled = true; lbl.textContent = t().form.sending;
      let ok = false;
      if (FORM_ENDPOINT && window.fetch && location.protocol !== 'file:') {
        try {
          const ctrl = new AbortController(), to = setTimeout(() => ctrl.abort(), 9000);
          const F = t().form;
          const r = await fetch(FORM_ENDPOINT, {
            method: 'POST', signal: ctrl.signal,
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify({
              _subject: `${F.mailSubject}: ${d.name}${d.biz ? ' (' + d.biz + ')' : ''}`, _template: 'table', _captcha: 'false',
              [F.lblName]: d.name, [F.lblBiz]: d.biz || '—', [F.lblContact]: d.contact, [F.lblNeeds]: d.needs || '—',
              [F.lblLink]: d.link || '—', [F.lblMsg]: d.msg || '—', _replyto: /@/.test(d.contact) ? d.contact : undefined
            })
          });
          clearTimeout(to);
          const j = await r.json().catch(() => ({}));
          ok = r.ok && String(j.success) === 'true';
        } catch (err) { ok = false; }
      }
      btn.disabled = false; lbl.textContent = old;
      if (ok) showSent('ajax', d);
      else { location.href = mailtoHref(d); showSent('mailto', d); }
    });
    $('#okAgain').addEventListener('click', () => {
      form.reset(); form.classList.remove('is-sent');
      const note = $('#prefill'); if (note) note.classList.remove('is-on');
      fName.focus();
    });
  });

  /* ---------- wizytówka: obracanie, przechył, podpis ---------- */
  mod('bcard', () => {
    const card = $('#bcard');
    if (!card) return;
    const sig = $('.bc-sig', card);
    // starsze przeglądarki (iOS < 16) nie znają jednostek cqw: litery liczone z szerokości karty
    if (!(window.CSS && CSS.supports && CSS.supports('width', '1cqw'))) {
      const fit = () => card.style.setProperty('--cq', (card.offsetWidth / 100).toFixed(3) + 'px');
      fit(); resizeFns.push(fit);
    }
    let flipped = false, flips = 0, flipT = 0;
    const flip = () => {
      flipped = !flipped;
      card.classList.toggle('is-flipped', flipped);
      card.setAttribute('aria-pressed', String(flipped));
      if (flipped && sig && !sig.classList.contains('is-drawn')) setTimeout(() => sig.classList.add('is-drawn'), 380);
      flips++;
      clearTimeout(flipT);
      flipT = setTimeout(() => { flips = 0; }, 1800);
      if (flips >= 4) { flips = 0; toast(t().bcEgg); }
    };
    card.addEventListener('click', flip);
    card.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); flip(); } });
    if (FINE && !RM) {
      card.addEventListener('pointermove', e => {
        const r = card.getBoundingClientRect();
        const x = clamp((e.clientX - r.left) / r.width, 0, 1), y = clamp((e.clientY - r.top) / r.height, 0, 1);
        card.classList.add('is-tilting');
        card.style.setProperty('--ry', ((x - 0.5) * 18).toFixed(2) + 'deg');
        card.style.setProperty('--rx', ((0.5 - y) * 14).toFixed(2) + 'deg');
        card.style.setProperty('--gx', ((flipped ? 1 - x : x) * 100).toFixed(1) + '%');
        card.style.setProperty('--gy', (y * 100).toFixed(1) + '%');
      });
      card.addEventListener('pointerleave', () => {
        card.classList.remove('is-tilting');
        card.style.setProperty('--rx', '0deg');
        card.style.setProperty('--ry', '0deg');
      });
    }
    // delikatna podpowiedź przy pierwszym pokazaniu: karta lekko się uchyla
    if (!RM && 'IntersectionObserver' in window) {
      const io = new IntersectionObserver(([e]) => {
        if (!e.isIntersecting) return;
        io.disconnect();
        setTimeout(() => {
          card.style.setProperty('--ry', '-24deg');
          setTimeout(() => card.style.setProperty('--ry', '0deg'), 700);
        }, 900);
      }, { threshold: 0.6 });
      gate.then(() => io.observe(card));
    }
  });

  /* ---------- prace: podgląd na żywo (komputer / telefon) ---------- */
  mod('studio', () => {
    const stage = $('#stage');
    if (!stage) return;
    const dev = $('#device'), frame = $('#devFrame'), poster = $('#devPoster'), play = $('#devPlay'), url = $('#devUrl');
    const tabs = $$('.ptab'), ind = $('.ptabs .tabs__ind'), devBtns = $$('[data-dev]');
    const PR = {
      luxe: { file: 'luxe-salon.html', dom: 'luxe-salon.pl', img: 'luxe', n: '01' },
      vesper: { file: 'vesper-barber.html', dom: 'vesper-barber.pl', img: 'vesper', n: '02' },
      zar: { file: 'zar-burger.html', dom: 'zar-burger.pl', img: 'zar', n: '03' }
    };
    let proj = 'luxe', mode = innerWidth < 760 ? 'phone' : 'desk', live = false, loaded = '';
    const place = () => {
      const c = tabs.find(x => x.dataset.proj === proj);
      if (!c || !ind) return;
      ind.style.width = c.offsetWidth + 'px';
      ind.style.transform = `translateX(${c.offsetLeft}px)`;
    };
    const layout = () => {
      const sw = stage.clientWidth, pad = sw < 640 ? 14 : 36;
      let w, h, s, sh;
      if (mode === 'desk') { w = sw - pad * 2; h = Math.round(w * 800 / 1280) + 32; s = w / 1280; sh = h + pad * 2; }
      else {
        // telefon zawsze mieści się w scenie razem z ramką (także na najwęższych ekranach)
        h = Math.round(clamp(innerHeight * 0.74, 440, 660));
        const maxW = sw - pad * 2 - 24;
        if (h * 390 / 844 > maxW) h = Math.round(maxW * 844 / 390);
        w = Math.round(h * 390 / 844); s = w / 390; sh = h + pad * 2 + 20;
      }
      stage.style.setProperty('--stage-h', sh + 'px');
      dev.style.setProperty('--dw', w + 'px');
      dev.style.setProperty('--dh', h + 'px');
      dev.style.setProperty('--s', s.toFixed(4));
    };
    const renderInfo = animate => {
      const P = PR[proj], D = (t().projects || {})[proj] || {};
      const set = () => {
        $('#stNum').textContent = `${P.n} / 03`;
        $('#stTitle').textContent = CONCEPTS[proj];
        $('#stCat').innerHTML = D.cat || '';
        $('#stDesc').innerHTML = D.desc || '';
        ['m1', 'm2', 'm3', 'm4'].forEach((m, i) => { $('#stM' + (i + 1)).innerHTML = D[m] || ''; });
        $('#stOpen').href = P.file;
        $('#stWant').dataset.pick = 'concept-' + proj;
        frame.title = t().frame(CONCEPTS[proj]);
      };
      if (!animate || RM) { set(); return; }
      const box = $('#studioInfo');
      box.classList.remove('swap-in'); box.classList.add('swap-out');
      setTimeout(() => { set(); box.classList.remove('swap-out'); void box.offsetWidth; box.classList.add('swap-in'); }, 260);
    };
    const load = () => {
      live = true;
      dev.classList.add('is-live');
      const src = PR[proj].file;
      if (loaded === src) return;
      loaded = src;
      dev.classList.remove('is-ready');
      dev.classList.add('is-loading');
      frame.tabIndex = 0;
      frame.src = src;
    };
    frame.addEventListener('load', () => {
      if (!loaded) return;
      dev.classList.remove('is-loading');
      dev.classList.add('is-ready');
    });
    play.addEventListener('click', load);
    const setProj = (k, focus) => {
      if (!PR[k] || k === proj) return;
      proj = k;
      tabs.forEach(b => {
        const on = b.dataset.proj === k;
        b.setAttribute('aria-selected', String(on));
        b.tabIndex = on ? 0 : -1;
        if (on && focus) b.focus();
      });
      place();
      url.textContent = PR[k].dom;
      poster.src = `assets/img/${PR[k].img}-1200.webp`;
      if (poster.animate && !RM) poster.animate([{ opacity: 0.2, transform: 'scale(1.03)' }, { opacity: 1, transform: 'none' }], { duration: 600, easing: 'cubic-bezier(.16,1,.3,1)' });
      renderInfo(true);
      if (live) load(); else dev.classList.remove('is-ready');
    };
    tabs.forEach((b, i) => {
      b.addEventListener('click', () => setProj(b.dataset.proj));
      b.addEventListener('keydown', e => {
        let j = null;
        if (e.key === 'ArrowRight') j = (i + 1) % tabs.length;
        else if (e.key === 'ArrowLeft') j = (i - 1 + tabs.length) % tabs.length;
        if (j !== null) { e.preventDefault(); setProj(tabs[j].dataset.proj, true); }
      });
    });
    const setMode = m => {
      mode = m;
      dev.classList.toggle('is-phone', m === 'phone');
      devBtns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.dev === m)));
      layout();
    };
    devBtns.forEach(b => b.addEventListener('click', () => setMode(b.dataset.dev)));
    setMode(mode);
    let q = null;
    try { q = new URLSearchParams(location.search).get('projekt'); } catch (e) { /* ok */ }
    if (q && PR[q]) setProj(q);
    if ('ResizeObserver' in window) new ResizeObserver(() => { layout(); place(); }).observe(stage);
    else resizeFns.push(() => { layout(); place(); });
    langHooks.push(() => { renderInfo(false); requestAnimationFrame(place); });
    if (document.fonts) document.fonts.ready.then(place);
    place();
  });

  /* ---------- kursor (kropka; „Zobacz” nad projektami) ---------- */
  mod('cursor', () => {
    const c = $('#cursor');
    if (!c || !FINE || RM) return;
    let x = -100, y = -100, cx = x, cy = y, raf = 0, shown = false;
    const loop = () => {
      cx += (x - cx) * 0.35; cy += (y - cy) * 0.35;
      c.style.transform = `translate3d(${cx.toFixed(1)}px,${cy.toFixed(1)}px,0) translate(-50%,-50%)`;
      raf = (Math.abs(x - cx) > 0.1 || Math.abs(y - cy) > 0.1) ? requestAnimationFrame(loop) : 0;
    };
    addEventListener('mousemove', e => {
      x = e.clientX; y = e.clientY;
      if (!shown) { shown = true; cx = x; cy = y; c.classList.add('on'); }
      if (!raf) raf = requestAnimationFrame(loop);
    }, { passive: true });
    document.addEventListener('mouseleave', () => c.classList.remove('on'));
    document.addEventListener('mouseenter', () => { if (shown) c.classList.add('on'); });
    document.addEventListener('mouseover', e => {
      if (c.classList.contains('lock')) return;
      const tg = e.target;
      const el = tg.closest && tg.closest('[data-cursor],a,button,label,[role="tab"],[role="button"]');
      const view = !!(el && el.dataset.cursor === 'view');
      c.classList.toggle('view', view);
      c.classList.toggle('big', !!el && !view);
      c.classList.toggle('dark', !!(tg.closest && tg.closest('[data-dark]')));
    });
    frameOut(c);
  });
  function frameOut(c) {
    // nad ramką z podglądem kursor systemowy przejmuje stery
    const f = $('#devFrame');
    if (!f) return;
    f.addEventListener('mouseenter', () => c.classList.remove('on'));
  }

  /* ---------- magnetyczne przyciski ---------- */
  mod('magnetic', () => {
    if (!FINE || RM) return;
    $$('.mag').forEach(el => {
      el.addEventListener('mousemove', e => {
        const r = el.getBoundingClientRect();
        const mx = clamp((e.clientX - r.left - r.width / 2) * 0.25, -12, 12);
        const my = clamp((e.clientY - r.top - r.height / 2) * 0.3, -8, 8);
        el.style.transform = `translate(${mx.toFixed(1)}px,${my.toFixed(1)}px)`;
      });
      el.addEventListener('mouseleave', () => { el.style.transform = ''; });
    });
  });

  /* ---------- drobiazgi ---------- */
  mod('misc', () => {
    $$('.year').forEach(y => { y.textContent = new Date().getFullYear(); });
    $$('[data-totop]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); e.stopPropagation(); scrollToY(0); }, true));
    // 5 szybkich kliknięć w logo na stronie startowej = gwiazdki
    const logo = $('.logo-mark');
    let clicks = 0, ct = 0;
    if (logo) logo.addEventListener('click', () => {
      if (PAGE !== 'index') return;
      clicks++; clearTimeout(ct); ct = setTimeout(() => { clicks = 0; }, 1400);
      if (clicks < 5) return;
      clicks = 0; toast(t().egg);
      if (RM || !document.body.animate) return;
      const r = logo.getBoundingClientRect();
      for (let i = 0; i < 22; i++) {
        const s = document.createElement('span');
        s.className = 'spark';
        s.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 0l2.6 9.4L24 12l-9.4 2.6L12 24l-2.6-9.4L0 12l9.4-2.6z"/></svg>';
        document.body.appendChild(s);
        const x0 = r.left + r.width * Math.random(), y0 = r.top + r.height / 2;
        const ang = Math.random() * Math.PI * 2, dist = 80 + Math.random() * 160, sc = 0.5 + Math.random() * 0.9;
        const an = s.animate([
          { transform: `translate(${x0}px,${y0}px) scale(0) rotate(0deg)`, opacity: 1 },
          { transform: `translate(${x0 + Math.cos(ang) * dist}px,${y0 + Math.sin(ang) * dist + 60}px) scale(${sc}) rotate(${Math.random() * 360}deg)`, opacity: 0 }
        ], { duration: 1100 + Math.random() * 700, easing: 'cubic-bezier(.16,1,.3,1)', fill: 'forwards' });
        an.onfinish = () => s.remove();
      }
    });
    document.addEventListener('visibilitychange', () => {
      const L = t();
      document.title = document.hidden ? L.away : ((L.titles && L.titles[PAGE]) || document.title);
    });
    try {
      console.log('%cMarcel Struszczak', 'font:28px Georgia,serif;font-style:italic;color:#17171a');
      console.log('%cZaglądasz pod maskę? Lubię to. Jeśli Twoja firma potrzebuje strony, która robi robotę: ' + EMAIL, 'color:#6f6d66;font:12px monospace');
    } catch (e) { /* ok */ }
  });

  /* ---------- płynny scroll (tylko myszka) ---------- */
  // Lenis pobiera się tylko na komputerach z myszką (telefony i słaby sprzęt przewijają natywnie)
  mod('lenis', () => {
    if (!FINE || RM || isLite()) return;
    const init = () => {
      if (!window.Lenis || lenis || leaving || isLite()) return;
      lenis = new window.Lenis({ lerp: 0.105, smoothWheel: true, wheelMultiplier: 1 });
      root.classList.add('lenis');
      lenis.on('scroll', requestScroll);
      const inst = lenis;
      const raf = time => { if (lenis !== inst) return; inst.raf(time); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
      if (!gateOpen || menuCtl.open) { lenis.stop(); gate.then(() => { if (lenis && !leaving && !menuCtl.open) lenis.start(); }); }
    };
    if (window.Lenis) { init(); return; }
    const s = document.createElement('script');
    s.src = 'assets/js/lenis.min.js' + (VER ? '?v=' + VER : '');
    s.async = true;
    s.onload = init;
    document.head.appendChild(s);
    liteHooks.push(() => {
      if (!lenis) return;
      try { lenis.destroy(); } catch (e) { /* ok */ }
      lenis = null;
      root.classList.remove('lenis', 'lenis-stopped', 'lenis-smooth', 'lenis-scrolling');
    });
  });

  /* ---------- sprawdzenie płynności: jeśli sprzęt nie wyrabia, włącza się tryb lekki ---------- */
  mod('perf', () => {
    if (isLite() || RM || !window.requestAnimationFrame) return;
    let tries = 0;
    const sample = () => {
      if (isLite() || tries > 2) return;
      if (document.hidden || leaving || !gateOpen || menuCtl.open) { tries++; setTimeout(sample, 2500); return; }
      const ds = [];
      let prev = 0;
      const f = now => {
        if (prev) ds.push(now - prev);
        prev = now;
        if (ds.length < 48) { requestAnimationFrame(f); return; }
        ds.sort((a, b) => a - b);
        if (ds[24] > 24 || ds[38] > 42) setLite();
      };
      requestAnimationFrame(f);
    };
    const go = () => setTimeout(sample, 1800);
    if (document.readyState === 'complete') go(); else addEventListener('load', go);
  });

  /* ---------- język ---------- */
  mod('lang', () => {
    $$('[data-lang]').forEach(b => b.addEventListener('click', () => {
      const l = b.dataset.lang;
      if (l === LANG && root.lang === l) return;
      store.set('ms-lang', l);
      applyLang(l);
      requestScroll();
    }));
    if (initLang === 'en') applyLang('en');
    else langHooks.forEach(f => { try { f(); } catch (e) { /* ok */ } });
    root.classList.add('i18n-done');
  });

  /* ---------- pętla scrolla ---------- */
  let rT = 0;
  addEventListener('scroll', requestScroll, { passive: true });
  addEventListener('resize', () => {
    clearTimeout(rT);
    rT = setTimeout(() => { resizeFns.forEach(f => { try { f(); } catch (e) { /* ok */ } }); requestScroll(); }, 140);
  }, { passive: true });
  addEventListener('load', requestScroll);
  runScroll();
})();
