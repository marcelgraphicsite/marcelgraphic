// Scena reela: wszystko jest czystą funkcją czasu → render(T) daje zawsze tę samą klatkę.
// Ruch obiektów i kamery liczą sprężyny (policzone z góry dla całego filmu), więc nic nie startuje ani nie staje „na sztywno”.
(() => {
  'use strict';
  const S = window.SCEN, M = window.META, A = window.ASSETS;
  const FPS = 60, N = Math.ceil(S.total * FPS) + 2;
  const SC = S.byId;
  const $ = id => document.getElementById(id);

  // ---------- matematyka ----------
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, k) => a + (b - a) * k;
  const inv = (a, b, v) => clamp((v - a) / (b - a), 0, 1);
  const E = {
    lin: k => k,
    outExpo: k => (k >= 1 ? 1 : 1 - Math.pow(2, -10 * k)),
    outCubic: k => 1 - Math.pow(1 - k, 3),
    outQuart: k => 1 - Math.pow(1 - k, 4),
    outQuint: k => 1 - Math.pow(1 - k, 5),
    inCubic: k => k * k * k,
    inQuart: k => k * k * k * k,
    io: k => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2),
    io5: k => (k < 0.5 ? 16 * Math.pow(k, 5) : 1 - Math.pow(-2 * k + 2, 5) / 2),
    sine: k => -(Math.cos(Math.PI * k) - 1) / 2,
    outBack: k => { const c1 = 1.5, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); }
  };
  const seg = (t, t0, d, e) => (e || E.io)(clamp((t - t0) / d, 0, 1));
  // odpowiedź sprężyny (0→1) — do jednorazowych wejść z lekkim odbiciem
  const spring = (t, w, z) => {
    if (t <= 0) return 0;
    if (z >= 1) return 1 - (1 + w * t) * Math.exp(-w * t);
    const wd = w * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t));
  };
  // deterministyczny „los”
  const rnd = (i, s = 1) => { const x = Math.sin(i * 127.1 + s * 311.7) * 43758.5453; return x - Math.floor(x); };

  // ---------- zapis do DOM tylko gdy wartość się zmienia ----------
  const C = new Map();
  const st = (el, k, v) => { let o = C.get(el); if (!o) C.set(el, o = {}); if (o[k] !== v) { o[k] = v; el.style[k] = v; } };
  const tx = (el, v) => { if (el._t !== v) { el._t = v; el.textContent = v; } };
  const hx = (el, v) => { if (el._h !== v) { el._h = v; el.innerHTML = v; } };
  let pend = [];
  const im = (el, url) => { if (el._u !== url) { el._u = url; el.src = url; pend.push(el.decode().catch(() => {})); } };
  const px = v => v.toFixed(2) + 'px';
  const show = (el, on) => st(el, 'display', on ? '' : 'none');

  // ---------- ujęcia ----------
  const nF = k => (M[k] ? M[k].frames.length : 1);
  const STEP = A.step || 1; // podgląd roboczy: zapisana co n-ta klatka
  const fr = (k, i) => `${A.dir}/${k}/${String(Math.round(clamp(Math.round(i), 0, nF(k) - 1) / STEP) * STEP).padStart(5, '0')}.jpg`;
  const meta = (k, i) => M[k].frames[clamp(Math.round(i), 0, nF(k) - 1)];
  const mainI = T => (T - S.mainStart) * FPS;
  const tk = (id, dt) => SC[id].takeT + dt; // czas w ujęciu main
  const mk = (name, i = 0) => {
    const a = M.main.marks[name];
    if (!a || !a[i] || !a[i].r) return null;
    const [x, y, w, h] = a[i].r;
    return { x, y: y + 72, w, h, cx: x + w / 2, cy: y + 72 + h / 2 };
  };
  const mkc = (name, fx, fy) => { const m = mk(name); return m ? [m.cx, m.cy] : [fx, fy]; };

  // ekran Maca: wirtualne px (1280×800) → świat
  const K = 0.75, SX = 60, SY = 630;
  const Wd = (x, y) => [SX + x * K, SY + y * K];

  // =====================================================================
  // KANAŁY ANIMACJI (sprężyny liczone z góry)
  // =====================================================================
  const KEYS = {};
  const key = (name, T, v, o = {}) => { (KEYS[name] = KEYS[name] || []).push(Object.assign({ T, v }, o)); };
  const CH = {};
  function buildChannels() {
    for (const [name, keys] of Object.entries(KEYS)) {
      keys.sort((a, b) => a.T - b.T);
      const out = new Float32Array(N + 1);
      const val = (k, T) => (typeof k.v === 'function' ? k.v(T) : k.v);
      let cur = keys[0], x = val(cur, 0), v = 0, ki = 0, w = 6, z = 1;
      const SUB = 8, dt = 1 / FPS / SUB;
      for (let f = 0; f <= N; f++) {
        const T = f / FPS;
        while (ki < keys.length && keys[ki].T <= T + 1e-9) {
          cur = keys[ki++];
          w = cur.w || 6; z = cur.z == null ? 1 : cur.z;
          if (cur.snap) { x = val(cur, T); v = 0; }
        }
        out[f] = x;
        for (let s = 0; s < SUB; s++) {
          const tg = val(cur, T + s * dt);
          const a = w * w * (tg - x) - 2 * z * w * v;
          v += a * dt; x += v * dt;
        }
      }
      CH[name] = out;
    }
  }
  const ch = (name, T) => {
    const a = CH[name];
    if (!a) return 0;
    const f = clamp(T * FPS, 0, N), i = Math.floor(f), k = f - i;
    return lerp(a[i], a[Math.min(N, i + 1)], k);
  };

  // ---------- kamera ----------
  // s = zoom, f = punkt ekranu Maca (wirtualne px) albo w = punkt świata, a = gdzie ten punkt ma stanąć na kadrze
  function cam(T, o) {
    const w = o.w || 3.6, z = o.z == null ? 1 : o.z;
    const s = o.s == null ? 1 : o.s;
    let wx, wy;
    if (o.wpt) [wx, wy] = o.wpt;
    else if (o.f) {
      [wx, wy] = Wd(o.f[0], o.f[1]);
      if (o.clamp !== false && s > 1.08) {
        const half = 540 / s;
        wx = clamp(wx, SX + half - 6, SX + 960 - half + 6);
      }
    } else [wx, wy] = [540, 945];
    const a = o.a || [540, 950];
    key('cz', T, Math.log(s), { w, z });
    key('cx', T, wx, { w, z }); key('cy', T, wy, { w, z });
    key('cax', T, a[0], { w, z }); key('cay', T, a[1], { w, z });
    key('crx', T, o.rx || 0, { w: w * 0.8, z: 1 }); key('cry', T, o.ry || 0, { w: w * 0.8, z: 1 });
  }
  const at = (id, L) => SC[id].start + L;

  function choreo() {
    // ---------------- wartości startowe ----------------
    ['mx', 'mry', 'mrx', 'mblur', 'nx', 'nry', 'pblur'].forEach(n => key(n, 0, 0, { snap: true }));
    key('my', 0, 0, { snap: true }); key('ms', 0, 1, { snap: true }); key('mop', 0, 1, { snap: true });
    key('px', 0, 650, { snap: true }); key('py', 0, 3000, { snap: true }); key('ps', 0, 0.93, { snap: true });
    key('prz', 0, 0, { snap: true }); key('pry', 0, 0, { snap: true });
    key('nop', 0, 0, { snap: true }); key('ny', 0, 0, { snap: true });

    // ---------------- HOOK ----------------
    key('my', 0, 300, { snap: true }); key('mrx', 0, 18, { snap: true }); key('ms', 0, 0.86, { snap: true }); key('mop', 0, 0, { snap: true });
    key('my', 0.05, 0, { w: 4.4, z: 0.82 }); key('mrx', 0.05, 0, { w: 3.6 }); key('ms', 0.05, 1, { w: 4.2, z: 0.9 }); key('mop', 0.05, 1, { w: 7 });
    cam(0, { s: 1, wpt: [540, 950], w: 3 });
    cam(0.9, { s: 1.06, wpt: [540, 942], w: 1.2 });
    cam(at('hook', 4.6), { s: 1.1, wpt: [540, 935], w: 1.4 });

    // ---------------- PRZED → TERAZ ----------------
    const Z0 = SC.zmiany.start;
    cam(Z0, { s: 1, wpt: [540, 980], a: [540, 960], w: 3.2 });
    key('mx', Z0, 1180, { w: 4.2 }); key('mry', Z0, -34, { w: 4.2 });
    key('nop', Z0, 1, { snap: true }); key('nx', Z0, -1180, { snap: true }); key('nry', Z0, 32, { snap: true });
    key('nx', Z0 + 0.05, 0, { w: 4.3, z: 0.86 }); key('nry', Z0 + 0.05, 0, { w: 3.8 });
    // Mac spada z góry po rozbiciu netbooka
    key('mx', Z0 + 4.3, 0, { snap: true }); key('mry', Z0 + 4.3, 0, { snap: true });
    key('my', Z0 + 4.3, -1500, { snap: true }); key('my', Z0 + 4.32, 140, { w: 7.6, z: 0.72 });
    key('nop', Z0 + 5.4, 0, { snap: true });
    cam(Z0 + 4.4, { s: 1.0, wpt: [540, 1000], w: 3 });
    key('my', Z0 + 9.55, 0, { w: 3.6 });
    cam(Z0 + 9.6, { s: 1.32, f: mkc('name', 640, 409), w: 2.6 });

    // ---------------- 19 smaczków (ujęcie main) ----------------
    const nm = mkc('name', 640, 409);
    cam(at('f01', 0.3), { s: 1.55, f: nm, w: 1.6 });
    cam(at('f01', 4.6), { s: 2.15, f: mkc('cap', 640, 595), w: 2.6 });
    cam(at('f01', 6.7), { s: 1.3, f: [640, 400], w: 3 });

    cam(at('f02', 0.15), { s: 1.22, f: [640, 430], w: 3 });
    cam(at('f02', 2.0), { s: 1.7, f: mkc('rotw', 680, 382), w: 2.8 });
    cam(at('f02', 4.0), { s: 1.45, f: (() => { const b = mk('band'); return [640, b ? b.cy - 40 : 650]; })(), w: 3 });
    cam(at('f02', 6.6), { s: 1.25, f: [640, 430], w: 3 });

    cam(at('f03', 1.5), { s: 1.4, f: mkc('hs', 640, 420), w: 2.4 });
    cam(at('f03', 3.9), { s: 1.75, f: [700, 470], w: 2.4 });
    cam(at('f03', 6.5), { s: 1.3, f: [640, 430], w: 3 });

    cam(at('f04', 0.1), { s: 1.12, f: [640, 430], w: 3 });
    cam(at('f04', 2.4), { s: 1.85, f: (() => { const m = mk('next'); return m ? [m.x + m.w * 0.62, m.cy] : [400, 560]; })(), w: 2 });

    cam(at('f05', 1.55), { s: 1.12, f: [640, 430], w: 4.2 });
    cam(at('f05', 2.15), { s: 1.85, f: [330, 535], w: 3.6 });
    cam(at('f05', 3.5), { s: 1.3, f: [640, 400], w: 3 });
    cam(at('f05', 4.8), { s: 1.5, f: [520, 300], w: 2.4 });

    cam(at('f06', 0.2), { s: 1.2, f: [640, 420], w: 3 });
    cam(at('f06', 1.1), { s: 1.55, f: [520, 300], w: 3 });
    cam(at('f06', 2.7), { s: 1.4, f: mkc('device', 640, 500), w: 2.6 });
    cam(at('f06', 6.3), { s: 1.6, f: [980, 260], w: 3 });
    cam(at('f06', 7.9), { s: 1.45, f: (() => { const m = mk('device2'); return m ? [m.cx, m.cy - 30] : [640, 480]; })(), w: 2.6 });

    cam(at('f07', 0.1), { s: 1.6, f: [560, 200], w: 3 });
    cam(at('f07', 1.6), { s: 1.12, f: [640, 430], w: 4 });
    cam(at('f07', 3.3), { s: 1.38, f: (() => { const m = mk('ills'); return m ? [m.cx, m.cy] : [640, 500]; })(), w: 2.6 });
    cam(at('f07', 5.7), { s: 1.4, f: [640, 470], w: 2.2 });
    cam(at('f07', 8.4), { s: 1.55, f: mkc('steps', 640, 560), w: 2.4 });

    cam(at('f08', 0.1), { s: 1.55, f: [480, 560], w: 3 });
    cam(at('f08', 1.5), { s: 1.12, f: [640, 430], w: 4 });
    cam(at('f08', 3.0), { s: 1.45, f: [520, 330], w: 2.8 });
    cam(at('f08', 4.4), { s: 1.55, f: (() => { const m = mk('social'); return m ? [m.cx, m.y + 220] : [640, 450]; })(), w: 2.6 });
    cam(at('f08', 6.5), { s: 1.35, f: [640, 430], w: 3 });

    cam(at('f09', 0.2), { s: 1.2, f: [640, 430], w: 3 });
    cam(at('f09', 1.5), { s: 1.5, f: (() => { const m = mk('calc'); return m ? [m.cx, m.y + 260] : [640, 400]; })(), w: 2.6 });
    cam(at('f09', 5.3), { s: 1.6, f: (() => { const m = mk('sum'); return m ? [m.cx, m.cy + 120] : [940, 300]; })(), w: 2.6 });
    cam(at('f09', 6.4), { s: 1.12, f: [640, 430], w: 4 });
    cam(at('f09', 8.3), { s: 1.6, f: (() => { const m = mk('form'); return m ? [m.cx, m.y + 150] : [870, 480]; })(), w: 3.2 });

    cam(at('f10', 0.4), { s: 1.75, f: (() => { const m = mk('card'); return m ? [m.cx, m.cy] : [330, 455]; })(), w: 2.4 });
    cam(at('f10', 7.2), { s: 1.4, f: [560, 520], w: 2.6 });

    cam(at('f11', 0.2), { s: 1.55, f: (() => { const m = mk('copy'); return m ? [m.cx, m.cy + 40] : [600, 380]; })(), w: 2.8 });
    cam(at('f11', 3.5), { s: 1.55, f: (() => { const m = mk('clock'); return m ? [m.cx + 120, m.cy - 60] : [400, 600]; })(), w: 2.4 });

    cam(at('f12', 0.05), { s: 1.55, f: [700, 200], w: 3 });
    cam(at('f12', 1.5), { s: 1.12, f: [640, 430], w: 4 });
    cam(at('f12', 3.2), { s: 1.75, f: (() => { const m = mk('sig'); return m ? [m.cx + 60, m.cy - 40] : [400, 600]; })(), w: 2.4 });

    cam(at('f13', 0.1), { s: 1.5, f: [200, 200], w: 3 });
    cam(at('f13', 1.5), { s: 1.12, f: [640, 430], w: 4 });
    cam(at('f13', 3.1), { s: 1.6, f: [300, 300], w: 2.8 });
    cam(at('f13', 5.0), { s: 1.45, f: (() => { const m = mk('toast3'); return m ? [m.cx, m.cy - 120] : [640, 600]; })(), w: 2.6 });

    cam(at('f14', 0.2), { s: 1.2, f: [640, 300], w: 3 });
    cam(at('f14', 0.7), { s: 2.1, f: [372, 30], clamp: false, a: [540, 900], w: 2.8 });
    cam(at('f14', 4.9), { s: 1.25, f: [640, 400], w: 3 });

    cam(at('f15', 0.1), { s: 1.2, f: [640, 420], w: 3 });
    cam(at('f15', 1.3), { s: 1.85, f: [1090, 110], clamp: false, a: [600, 860], w: 3 });
    cam(at('f15', 2.5), { s: 1.5, f: (() => { const m = mk('hero'); return m ? [m.x + 380, m.y + 130] : [500, 300]; })(), w: 2.6 });
    cam(at('f15', 4.2), { s: 1.7, f: [1060, 120], clamp: false, a: [600, 860], w: 3 });
    cam(at('f15', 5.0), { s: 1.45, f: [520, 330], w: 2.6 });

    cam(at('f16', 0.0), { s: 1.3, f: [640, 300], w: 3 });
    cam(at('f16', 0.55), { s: 2.05, f: [470, 56], clamp: false, a: [540, 900], w: 3 });
    cam(at('f16', 2.95), { s: 1.2, f: [640, 420], w: 3.4 });
    cam(at('f16', 3.9), { s: 1.55, f: [420, 400], w: 2.6 });
    cam(at('f16', 6.2), { s: 1.2, f: [640, 420], w: 3 });

    cam(at('f17', 0.2), { s: 1.15, f: [640, 430], w: 3 });
    cam(at('f17', 0.8), { s: 1.95, f: [370, 560], w: 2.6 });
    cam(at('f17', 5.0), { s: 1.0, wpt: [540, 945], w: 3 });

    // ---------------- TELEFON ----------------
    const F18 = SC.f18.start;
    key('my', F18, -190, { w: 4.6 }); key('ms', F18, 0.8, { w: 4.6 }); key('mblur', F18, 7, { w: 4 }); key('mop', F18, 0.92, { w: 4 });
    key('py', F18 - 0.01, 2600, { snap: true }); key('prz', F18 - 0.01, -14, { snap: true }); key('pry', F18 - 0.01, 22, { snap: true });
    key('px', F18 - 0.01, 640, { snap: true }); key('ps', F18 - 0.01, 0.95, { snap: true });
    key('py', F18, 1035, { w: 5.4, z: 0.72 }); key('prz', F18, 0, { w: 4.2, z: 0.8 }); key('pry', F18, -5, { w: 3.4 });
    cam(F18, { s: 1, wpt: [560, 990], w: 3 });
    cam(F18 + 1.6, { s: 1.06, wpt: [620, 1020], w: 1.8 });

    // ---------------- GOOGLE I AI ----------------
    const F19 = SC.f19.start;
    cam(F19 + 0.1, { s: 1.12, wpt: [645, 1035], a: [540, 1010], w: 2.6 });
    key('my', F19 + 3.75, 0, { w: 4.2 }); key('ms', F19 + 3.75, 1, { w: 4.2 }); key('mblur', F19 + 3.75, 0, { w: 4.4 }); key('mop', F19 + 3.75, 1, { w: 5 });
    key('px', F19 + 3.75, 1460, { w: 3.6 }); key('py', F19 + 3.75, 1180, { w: 3.6 }); key('ps', F19 + 3.75, 0.62, { w: 3.6 }); key('pblur', F19 + 3.75, 4, { w: 4 });
    key('prz', F19 + 3.75, 6, { w: 3.5 }); key('pry', F19 + 3.75, -12, { w: 3.5 });
    cam(F19 + 3.75, { s: 1.0, wpt: [540, 945], w: 3.2 });
    cam(F19 + 4.4, { s: 1.38, f: [640, 430], w: 2.6 });

    // ---------------- OUTRO ----------------
    const O = SC.outro.start;
    key('px', O, 870, { w: 3.2 }); key('py', O, 1235, { w: 3.2 }); key('ps', O, 0.6, { w: 3.2 }); key('pblur', O, 0, { w: 4 });
    key('prz', O, 3, { w: 3 }); key('pry', O, -14, { w: 3 });
    cam(O, { s: 0.93, wpt: [600, 1010], w: 2.2 });
    cam(O + 5.3, { s: 3.6, f: [640, 436], clamp: false, w: 2.4 });
  }

  // =====================================================================
  // STAŁE ELEMENTY
  // =====================================================================
  function initStatic() {
    // tło: ziarno papieru
    const g = $('grain'), gc = g.getContext('2d'), id = gc.createImageData(540, 960);
    for (let i = 0; i < id.data.length; i += 4) { const v = 128 + (rnd(i, 7) - 0.5) * 255; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; }
    gc.putImageData(id, 0, 0);
    [['b1', 1100, '222,217,203', 0.8], ['b2', 900, '255,255,252', 0.95], ['b3', 820, '210,207,196', 0.55]].forEach(([n, r, c, a]) => {
      const e = $(n); e.style.width = e.style.height = r + 'px';
      e.style.background = `radial-gradient(closest-side,rgba(${c},${a}),rgba(${c},0))`;
    });
    $('favImg').src = A.fav;
    $('ogImg').src = A.og;
    // tytuły
    const tt = $('titles');
    S.scenes.forEach(s => {
      const d = document.createElement('div');
      d.className = 'ttl';
      d.style.display = 'none';
      let bold = false, i = 0;
      s.title.split(/(\*\*|\|)/).forEach(part => {
        if (part === '**') { bold = !bold; return; }
        if (part === '|') { d.appendChild(document.createElement('br')); return; }
        part.split(/(\s+)/).forEach(w => {
          if (!w) return;
          if (/^\s+$/.test(w)) { d.appendChild(document.createTextNode(' ')); return; }
          const o = document.createElement('span'); o.className = 'w';
          const n = document.createElement('span'); n.className = 'wi ' + (bold ? 'bd' : 'lt'); n.textContent = w; n.dataset.i = i++;
          o.appendChild(n); d.appendChild(o);
        });
      });
      s._ttl = d; s._words = [...d.querySelectorAll('.wi')];
      tt.appendChild(d);
      s._caps = (s.caps || []).map(c => {
        const e = document.createElement('div'); e.className = 'cap'; e.textContent = c.text; e.style.display = 'none';
        $('caps').appendChild(e); return e;
      });
    });
    // pasek postępu
    for (let i = 0; i < 19; i++) { const s = document.createElement('i'); s.appendChild(document.createElement('b')); $('prog').appendChild(s); }
    // lista przed → teraz
    const L = [['Jedna strona', '11 podstron'], ['Portfolio projektanta', 'Oferta dla lokalnych firm'], ['Bez cennika', 'Cennik + kalkulator'], ['Sam e-mail', 'Formularz + wizytówka 3D']];
    L.forEach(([a, b]) => {
      const r = document.createElement('div'); r.className = 'row';
      r.innerHTML = `<span class="old">${a}<s></s></span><span class="arr">→</span><span class="nw">${b}</span><i class="ln"></i>`;
      $('list').appendChild(r);
    });
    // checklista telefonu
    ['Menu', 'Kurtyna', 'Wizytówka'].forEach(t => {
      const r = document.createElement('div'); r.className = 'it';
      r.innerHTML = `<span class="ck"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="17" fill="none" stroke="rgba(23,23,26,.22)" stroke-width="2.5"/><circle class="cf" cx="20" cy="20" r="18.5" fill="#17171a"/><path class="tk" d="M12.5 20.5l5 5 10-11" fill="none" stroke="#f4f3ef" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="26" stroke-dashoffset="26"/></svg></span><span class="lb">${t}</span>`;
      $('check').appendChild(r);
    });
    // robots.txt
    const R = [['Googlebot', 'Google'], ['Bingbot', 'Bing · Copilot'], ['GPTBot', 'ChatGPT'], ['PerplexityBot', 'Perplexity'], ['ClaudeBot', 'Claude'], ['Google-Extended', 'Gemini'], ['Applebot', 'Apple']];
    R.forEach(([a, b], i) => {
      const r = document.createElement('div'); r.className = 'row'; r.style.top = (74 + i * 56) + 'px';
      r.innerHTML = `<span class="k">User-agent:</span><span class="v">${a}</span><span class="who"><i></i>${b}</span>`;
      $('rRows').appendChild(r);
    });
    const al = document.createElement('div'); al.className = 'row'; al.style.top = (74 + 7 * 56 + 8) + 'px';
    al.innerHTML = '<span class="k">Allow:</span><span class="v">/ <span style="color:#7d7a72">— całą stronę wolno czytać i cytować</span></span>';
    $('rRows').appendChild(al);
    // klawisze netbooka (cząsteczki)
    const keysTxt = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890';
    for (let i = 0; i < 44; i++) {
      const k = document.createElement('div'); k.className = 'key'; k.textContent = keysTxt[i % keysTxt.length]; $('nbKeys').appendChild(k);
      const [x, y] = deckKey(i), d = document.createElement('i'); d.className = 'dk';
      d.style.left = (x - 84 - 28) + 'px'; d.style.top = (y - 1296 - 4) + 'px';
      document.querySelector('#nb .base').appendChild(d);
    }
    // kursor
    $('cursor').innerHTML = `<svg id="cArrow" width="30" height="44" viewBox="0 0 30 44"><path d="M3 2.5v33.6l8.2-7.7 5.3 12.3 5.6-2.4-5.2-12h11.3z" fill="#111" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/></svg><svg id="cHand" width="34" height="40" viewBox="0 0 34 40" style="display:none;left:-8px;top:-2px"><path d="M12.2 3.6c1.7 0 3 1.3 3 3v10.2c.6-.5 1.4-.8 2.2-.8 1.4 0 2.6.9 3 2.1.6-.6 1.4-1 2.3-1 1.5 0 2.7 1 3 2.3.5-.4 1.2-.6 1.9-.6 1.7 0 3.1 1.4 3.1 3.1v8.5c0 5.6-4.3 9.8-10 9.8h-2.5c-3.3 0-5.6-1.3-7.6-3.9L4 26.7c-.9-1.3-.7-3.1.6-4 1.2-.9 2.9-.7 3.9.4l.7.8V6.6c0-1.7 1.3-3 3-3z" fill="#fff" stroke="#111" stroke-width="2" stroke-linejoin="round"/><path d="M15.2 17v7.5M20.4 18.6v6M25.6 20.5v4.6" stroke="#111" stroke-width="1.7" stroke-linecap="round"/></svg>`;
  }

  // =====================================================================
  // KURSOR I KLIKNIĘCIA (ekran Maca)
  // =====================================================================
  // dodatkowe ruchy kursora rysowane tylko w scenie (pasek kart, pasek adresu)
  const OVR = [];
  function cursorOverrides() {
    const F14 = SC.f14.start;
    // z pozycji nad stroną → „+” → (karta wraca) → z powrotem na pierwszą kartę
    OVR.push({ t0: F14 + 0.35, t1: F14 + 5.6, pts: [[0.35, null], [1.15, [404, 22]], [3.55, [398, 25]], [4.35, [220, 22]], [5.0, [226, 24]], [5.6, null]] });
  }
  const COMPCLICKS = [];
  function compClicks() {
    COMPCLICKS.push({ T: at('f14', 1.25), x: 404, y: 22 });
    COMPCLICKS.push({ T: at('f14', 4.5), x: 222, y: 22 });
    COMPCLICKS.push({ T: at('f16', 0.82), x: 470, y: 42 + 0 });
  }
  const hand = k => k * k * k * (10 + k * (-15 + 6 * k));
  function cursorAt(T) {
    // pozycja z nagrania (wirtualne px ekranu)
    const sc = sceneAt(T);
    if (!sc.take || sc.take !== 'main') {
      if (T >= SC.f01.start - 0.6 && T < SC.f18.start + 0.6) { /* przejścia */ } else return null;
    }
    const i = mainI(T);
    if (i < 0) return null;
    const m = meta('main', i);
    let x = m.x, y = m.y + 72, cur = m.cur;
    for (const o of OVR) {
      if (T < o.t0 || T > o.t1) continue;
      const L = T - (o.t0 - o.pts[0][0]);
      for (let j = 0; j < o.pts.length - 1; j++) {
        const [ta, pa] = o.pts[j], [tb, pb] = o.pts[j + 1];
        if (L < ta || L > tb) continue;
        const k = hand(inv(ta, tb, L));
        const P = p => p || [m.x, m.y + 72];
        const a = P(pa), b = P(pb);
        x = lerp(a[0], b[0], k); y = lerp(a[1], b[1], k);
        cur = (pb && !pa) || (pa && pb) ? 'pointer' : cur;
      }
    }
    return { x, y, cur, down: m.down };
  }
  let CLICKS = [];
  function buildClicks() {
    CLICKS = M.main.clicks.map(c => ({ T: S.mainStart + c.t, x: c.x, y: c.y + 72 })).concat(COMPCLICKS);
  }

  // =====================================================================
  // RENDER
  // =====================================================================
  const sceneAt = T => S.scenes.find(s => T >= s.start && T < s.end) || S.scenes[S.scenes.length - 1];
  let lastScene = null;

  function render(T) {
    pend = [];
    const sc = sceneAt(T), L = T - sc.start;
    renderBg(T);
    renderCam(T);
    renderMac(T, sc, L);
    renderNetbook(T);
    renderPhone(T, sc, L);
    renderHud(T, sc, L);
    renderLoupes(T);
    renderEnd(T);
    return Promise.all(pend);
  }

  function renderBg(T) {
    const P = [[0.16, 0.12], [0.84, 0.38], [0.36, 0.9]];
    ['b1', 'b2', 'b3'].forEach((n, i) => {
      const e = $(n), r = parseFloat(e.style.width);
      const x = (P[i][0] + Math.sin(T * (0.11 + i * 0.03) + i * 2) * 0.07) * 1080 - r / 2;
      const y = (P[i][1] + Math.cos(T * (0.09 + i * 0.025) + i) * 0.05) * 1920 - r / 2;
      st(e, 'transform', `translate3d(${px(x)},${px(y)},0)`);
    });
  }

  function renderCam(T) {
    const s = Math.exp(ch('cz', T));
    // żywa kamera: delikatny, ciągły dryf (nic nigdy nie stoi martwo)
    const dx = Math.sin(T * 0.37) * 5 + Math.sin(T * 0.83 + 1) * 2;
    const dy = Math.cos(T * 0.29) * 4 + Math.sin(T * 0.71 + 2) * 1.6;
    let ry = ch('cry', T) + Math.sin(T * 0.23) * 0.9;
    let rx = ch('crx', T) + Math.cos(T * 0.31) * 0.6;
    if (T >= SC.outro.start) ry += lerp(-7, 7, E.sine(inv(SC.outro.start, SC.outro.start + 5.6, T))) * (1 - inv(SC.outro.start + 5.0, SC.outro.start + 6.2, T));
    const ax = ch('cax', T), ay = ch('cay', T), fx = ch('cx', T) + dx / s, fy = ch('cy', T) + dy / s;
    st($('cam'), 'transform', `translate3d(${px(ax)},${px(ay)},0) scale(${s.toFixed(5)}) rotateX(${rx.toFixed(3)}deg) rotateY(${ry.toFixed(3)}deg) translate3d(${px(-fx)},${px(-fy)},0)`);
    st($('world'), 'perspectiveOrigin', `${px(ax)} ${px(ay)}`);
    // dolna mgła tylko przy zbliżeniu (żeby podpis nie leżał na stopce Maca)
    st($('fogB'), 'opacity', clamp((s - 1.04) / 0.18, 0, 1).toFixed(3));
  }

  // ---------------- Mac ----------------
  const STILLS = () => ({
    start: 0,
    prace: Math.round(tk('f05', 4.4) * FPS),
    uslugi: Math.round(tk('f07', 4.7) * FPS),
    cennik: Math.round(tk('f09', 2.2) * FPS),
    kontakt: Math.round(tk('f10', 0.6) * FPS)
  });
  let ST = null;
  const WIPES = [[5.0, 'prace', '(01)', 'Prace'], [5.9, 'uslugi', '(02)', 'Usługi'], [6.8, 'cennik', '(03)', 'Cennik'], [7.7, 'kontakt', '(05)', 'Kontakt'], [8.9, 'start', '(00)', 'Start']];

  function renderMac(T, sc, L) {
    const mac = $('mac');
    const x = ch('mx', T), y = ch('my', T), s = ch('ms', T), ry = ch('mry', T), rx = ch('mrx', T), op = ch('mop', T), bl = ch('mblur', T);
    const vis = op > 0.01 && Math.abs(x) < 1500 && y > -1450;
    show(mac, vis);
    if (!vis) return;
    st(mac, 'transform', `translate3d(${px(x)},${px(y)},0) rotateY(${ry.toFixed(3)}deg) rotateX(${rx.toFixed(3)}deg) scale(${s.toFixed(4)})`);
    st(mac, 'opacity', op.toFixed(3));
    st(mac, 'filter', bl > 0.15 ? `blur(${bl.toFixed(2)}px)` : 'none');
    // cień przy lądowaniu: im wyżej Mac, tym mniejszy i jaśniejszy
    const hgt = clamp(-y / 600, 0, 1);
    st(mac.querySelector('.cshadow'), 'transform', `translateY(${px(-y)}) scale(${(1 - hgt * 0.5).toFixed(3)},${(1 - hgt * 0.3).toFixed(3)})`);
    st(mac.querySelector('.cshadow'), 'opacity', (1 - hgt * 0.85).toFixed(3));
    st(mac.querySelector('.glass'), 'backgroundPosition', `${px(ry * 6)} 0`);

    // ---- zawartość ekranu ----
    const A1 = $('vpA'), B1 = $('vpB');
    let take = 'main', idx = mainI(T), power = 0, tTitle = null, tPath = null;
    let wipeP = -1, wipeLbl = null, nextStill = null;
    if (T < SC.zmiany.start) {
      take = 'hook'; idx = (T - 0.78) * FPS;
      power = 1 - seg(T, 0.62, 0.28, E.outCubic);
    } else if (T < SC.f01.start) {
      const Lz = T - SC.zmiany.start;
      ST = ST || STILLS();
      if (Lz < 1.4) { take = 'hook'; idx = nF('hook') - 1; }
      else {
        let cur = 'start';
        for (const w of WIPES) {
          const p = (Lz - w[0]) / 0.86;
          if (p >= 0.46) cur = w[1];
          if (p > 0 && p < 1) { wipeP = p; wipeLbl = w; }
        }
        take = 'main'; idx = ST[cur];
      }
    } else if (T >= SC.outro.start) {
      take = 'main'; idx = tk('f02', 2.2) * FPS + (T - SC.outro.start) * FPS;
    }
    im(A1, fr(take, idx));
    const m = meta(take, idx);
    tTitle = m.title || ''; tPath = m.path || '/';
    st($('power'), 'opacity', power.toFixed(3));
    show($('power'), power > 0.001);

    // kurtyna montażu
    const wp = $('wipe');
    if (wipeP >= 0) {
      const p = wipeP;
      const yy = p < 0.42 ? 100 * (1 - E.outQuart(p / 0.42)) : p < 0.5 ? 0 : -100 * E.inCubic((p - 0.5) / 0.5);
      show(wp, true);
      st(wp, 'transform', `translateY(${yy.toFixed(3)}%)`);
      tx(wp.querySelector('.n'), wipeLbl[2]); tx(wp.querySelector('.t'), wipeLbl[3]);
      st(wp.querySelector('.t'), 'transform', `translateY(${((1 - E.outCubic(clamp(p / 0.45, 0, 1))) * 40).toFixed(2)}px)`);
    } else show(wp, false);

    // nowa karta (f14)
    const F14 = SC.f14.start;
    const ntOn = T >= F14 + 1.3 && T < F14 + 4.75;
    const ntA = ntOn ? Math.min(seg(T, F14 + 1.3, 0.22, E.outCubic), 1 - seg(T, F14 + 4.4, 0.3)) : 0;
    st($('newtab'), 'opacity', ntA.toFixed(3)); show($('newtab'), ntA > 0.001);
    // tab 2 („Nowa karta”) wjeżdża i znika
    const t2 = $('tab2');
    const t2k = T < F14 + 1.25 ? 0 : T < F14 + 4.55 ? E.outCubic(inv(F14 + 1.25, F14 + 1.6, T)) : 1 - E.io(inv(F14 + 4.55, F14 + 4.9, T));
    show(t2, t2k > 0.001);
    st(t2, 'left', px(388)); st(t2, 'width', px(300 * t2k)); st(t2, 'opacity', t2k.toFixed(3));
    const t2on = T >= F14 + 1.25 && T < F14 + 4.5;
    t2.classList.toggle('on', t2on); $('tab1').classList.toggle('on', !t2on);
    st($('plus'), 'left', px(392 + 300 * t2k));

    // tytuł karty: w tle strona woła
    let title = tTitle;
    if (T >= F14 + 1.35 && T < F14 + 4.5) {
      const away = 'Wracaj — darmowy projekt czeka 👀';
      const k = clamp((T - (F14 + 1.55)) / 0.9, 0, 1);
      const chars = [...away];
      title = k <= 0 ? tTitle : chars.slice(0, Math.max(1, Math.round(chars.length * k))).join('');
    }
    // robots.txt (f19)
    const F19 = SC.f19.start;
    const rbA = T >= F19 + 3.6 && T < SC.outro.start + 0.7 ? seg(T, F19 + 3.6, 0.35, E.outCubic) * (1 - seg(T, SC.outro.start, 0.7, E.io)) : 0;
    st($('robots'), 'opacity', rbA.toFixed(3)); show($('robots'), rbA > 0.001);
    if (rbA > 0) {
      [...$('rRows').children].forEach((r, i) => {
        const k = seg(T, F19 + 4.25 + i * 0.2, 0.5, E.outQuart);
        st(r, 'opacity', k.toFixed(3)); st(r, 'transform', `translateX(${px((1 - k) * 30)})`);
      });
      title = 'robots.txt'; tPath = '/robots.txt';
    }
    hx($('tab1t'), escapeHtml(title));
    // pasek adresu
    let urlHtml = 'marcelgraphicsite.pl' + (tPath && tPath !== '/' ? `<span class="p">${escapeHtml(decodeURIComponent(tPath))}</span>` : '');
    const F16 = SC.f16.start;
    if (T >= F16 + 0.82 && T < F16 + 2.78) {
      const full = 'marcelgraphicsite.pl/strona-ktorej-nie-ma';
      if (T < F16 + 1.05) urlHtml = `<span class="sel">marcelgraphicsite.pl${tPath !== '/' ? escapeHtml(tPath) : ''}</span>`;
      else {
        const n = Math.round(clamp((T - (F16 + 1.05)) / 1.45, 0, 1) * full.length);
        const blink = Math.floor((T - F16) * 2.2) % 2 === 0 || n < full.length;
        urlHtml = escapeHtml(full.slice(0, n)) + (blink ? '<span class="caret"></span>' : '');
      }
    }
    hx($('urlT'), urlHtml);

    // konsola (f17)
    const F17 = SC.f17.start;
    const dvK = T < F17 ? 0 : T < SC.f18.start ? E.outQuart(inv(F17 + 0.35, F17 + 1.1, T)) : 1;
    const dvOut = T >= SC.f17.end - 0.7 ? E.io(inv(SC.f17.end - 0.7, SC.f17.end + 0.2, T)) : 0;
    const dvH = 360 * dvK * (1 - dvOut);
    show($('devtools'), dvH > 0.5);
    st($('devtools'), 'transform', `translateY(${px(-dvH)})`);
    [$('dl1'), $('dl2')].forEach((e, i) => { const k = seg(T, F17 + 1.25 + i * 0.35, 0.45, E.outCubic); st(e, 'opacity', k.toFixed(3)); st(e, 'transform', `translateY(${px((1 - k) * 10)})`); });
    st($('dcar'), 'opacity', Math.floor(T * 2.4) % 2 ? '0' : '1');

    // kursor
    const c = cursorAt(T), cu = $('cursor');
    const onMac = T >= SC.f01.start - 0.3 && T < SC.f18.start + 0.4;
    if (c && onMac && c.x > -30 && c.x < 1300 && c.y > -30 && c.y < 830) {
      show(cu, true);
      const handOn = c.cur === 'pointer';
      show($('cArrow'), !handOn); show($('cHand'), handOn);
      let sc2 = 1;
      for (const k of CLICKS) { const d = T - k.T; if (d > -0.02 && d < 0.2) sc2 = Math.min(sc2, 1 - 0.14 * Math.sin(clamp((d + 0.02) / 0.22, 0, 1) * Math.PI)); }
      const fade = Math.min(inv(SC.f01.start - 0.3, SC.f01.start + 0.1, T), 1 - inv(SC.f18.start, SC.f18.start + 0.4, T));
      st(cu, 'transform', `translate3d(${px(c.x - 3)},${px(c.y - 3)},0) scale(${sc2.toFixed(3)})`);
      st(cu, 'opacity', fade.toFixed(3));
    } else show(cu, false);
    // fala po kliknięciu
    const rp = $('ripples');
    let html = '';
    for (const k of CLICKS) {
      const d = T - k.T;
      if (d < 0 || d > 0.55) continue;
      const e = E.outCubic(d / 0.55), r = 8 + 34 * e;
      html += `<div class="ripple" style="left:${(k.x - r).toFixed(1)}px;top:${(k.y - r).toFixed(1)}px;width:${(2 * r).toFixed(1)}px;height:${(2 * r).toFixed(1)}px;opacity:${(0.85 * (1 - e)).toFixed(3)}"></div>`;
    }
    hx(rp, html);
  }
  const escapeHtml = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  // ---------------- netbook ----------------
  // klawisz i: środek na klawiaturze (współrzędne świata, netbook w spoczynku)
  const deckKey = i => { const col = i % 11, row = Math.floor(i / 11); return [180 + col * 66 + row * 7 + 28, 1306 + row * 11]; };
  function renderNetbook(T) {
    const Z0 = SC.zmiany.start, L = T - Z0;
    const nb = $('nb'), note = $('note'), keys = $('nbKeys');
    const on = T >= Z0 && T < Z0 + 5.6;
    show(nb, on); show(note, on && L < 4.6); show(keys, on && L > 3.6);
    if (!on) return;
    const x = ch('nx', T), ry = ch('nry', T);
    // spadanie po rozbiciu
    const tf = Math.max(0, L - 4.0);
    const fy = 0.5 * 5200 * tf * tf, frz = tf * tf * 26;
    st(nb, 'transform', `translate3d(${px(x)},${px(fy)},0) rotateY(${ry.toFixed(3)}deg) rotateZ(${frz.toFixed(3)}deg)`);
    im($('nbImg'), fr('old', 36 + Math.max(0, L - 0.2) * FPS));
    // usterka i zgaśnięcie ekranu
    const gl = L > 3.75 && L < 4.15;
    st($('nbImg'), 'transform', gl ? `translateX(${px((rnd(Math.floor(L * 40), 3) - 0.5) * 60)})` : 'none');
    st($('nbImg'), 'filter', gl ? `contrast(1.6) hue-rotate(${Math.floor(rnd(Math.floor(L * 40), 5) * 180)}deg)` : 'none');
    const ko = clamp((L - 3.98) / 0.12, 0, 1), kl = clamp((L - 4.1) / 0.14, 0, 1);
    st($('nbImg'), 'transformOrigin', '50% 50%');
    if (ko > 0) {
      st($('nbImg'), 'transform', `scale(${(1 - kl * 0.98).toFixed(4)},${Math.max(0.006, 1 - E.inCubic(ko)).toFixed(4)})`);
      st($('nbImg'), 'filter', `brightness(${(1 + ko * 1.6).toFixed(3)})`);
    }
    st($('nbImg'), 'opacity', (1 - clamp((L - 4.18) / 0.08, 0, 1)).toFixed(3));
    st($('nbOff'), 'opacity', (ko > 0 ? 1 : 0).toFixed(2));
    st($('nbOff'), 'zIndex', '-1');
    st(document.querySelector('#nbScr .och'), 'opacity', (1 - ko).toFixed(3));
    // karteczka TODO: lekko faluje, odkleja się i spada
    const nx0 = 748 + x, ny0 = 726;
    const tn = Math.max(0, L - 3.15);
    const wob = Math.sin(L * 3.1) * 1.5 + (L > 2.7 ? Math.sin((L - 2.7) * 22) * 6 * Math.exp(-(L - 2.7) * 2) : 0);
    const nfy = 0.5 * 3600 * tn * tn, nfx = tn * 220, nrot = -7 + wob + tn * tn * 140;
    st(note, 'transform', `translate3d(${px(nx0 + nfx)},${px(ny0 + nfy)},0) rotate(${nrot.toFixed(3)}deg)`);
    // klawisze wyskakują z klawiatury
    const tk0 = 3.62;
    const dks = document.querySelectorAll('#nb .dk');
    [...keys.children].forEach((k, i) => {
      const t = L - tk0 - rnd(i, 2) * 0.12;
      st(dks[i], 'opacity', t < 0 ? '1' : '0');
      if (t < 0) { st(k, 'opacity', '0'); return; }
      const col = i % 11;
      const [kx, ky] = deckKey(i), x0 = kx + x, y0 = ky;
      const vx = (rnd(i, 4) - 0.5) * 900 + (col - 5) * 40, vy = -900 - rnd(i, 6) * 900, g = 3600;
      const px2 = x0 + vx * t, py2 = y0 + vy * t + 0.5 * g * t * t;
      const rot = (rnd(i, 8) - 0.5) * 900 * t;
      st(k, 'opacity', '1');
      st(k, 'transform', `translate3d(${px(px2)},${px(py2)},0) rotate(${rot.toFixed(2)}deg)`);
    });
  }

  // ---------------- iPhone ----------------
  const PH_OFF = 0.35;
  function renderPhone(T, sc, L) {
    const ph = $('phone');
    const py = ch('py', T);
    const on = py < 2400 && T >= SC.f18.start - 0.05;
    show(ph, on);
    if (!on) return;
    const x = ch('px', T), s = ch('ps', T), rz = ch('prz', T), ry = ch('pry', T), bl = ch('pblur', T);
    // wibracja przy obróceniu wizytówki (Android)
    const vibT = SC.f18.start + PH_OFF + 6.1;
    const vib = T > vibT && T < vibT + 0.42 ? Math.sin((T - vibT) * 52) * 0.9 * Math.pow(1 - (T - vibT) / 0.42, 2) : 0;
    st($('ph'), 'transform', `translate3d(${px(x - 210.5)},${px(py - 440)},0) rotateY(${ry.toFixed(3)}deg) rotateZ(${(rz + vib).toFixed(3)}deg) scale(${s.toFixed(4)})`);
    st($('ph'), 'filter', bl > 0.15 ? `blur(${bl.toFixed(2)}px)` : 'none');
    // zawartość
    let idx = (T - SC.f18.start - PH_OFF) * FPS;
    if (T >= SC.outro.start) idx = 0.95 * FPS;
    im($('phImg'), fr('phone', idx));
    // czat (f19)
    const F19 = SC.f19.start;
    const chatA = T >= F19 && T < SC.outro.start + 0.4 ? Math.min(seg(T, F19 + 0.05, 0.4, E.outCubic), 1 - seg(T, SC.outro.start, 0.4)) : 0;
    st($('phChat'), 'opacity', chatA.toFixed(3)); show($('phChat'), chatA > 0.001);
    if (chatA > 0) {
      const pop = (el, t0) => { const k = seg(T, t0, 0.5, E.outBack); const a = seg(T, t0, 0.2, E.lin); st(el, 'opacity', a.toFixed(3)); st(el, 'transform', `translateY(${px((1 - k) * 18)}) scale(${(0.9 + 0.1 * k).toFixed(4)})`); };
      pop($('cb1'), F19 + 0.5);
      const tpA = T > F19 + 1.05 && T < F19 + 1.75 ? 1 : 0;
      st($('ctp'), 'opacity', String(tpA));
      [...$('ctp').children].forEach((d, i) => st(d, 'transform', `translateY(${px(Math.sin(T * 12 - i * 0.9) * 2.5)})`));
      pop($('cb2'), F19 + 1.75);
      pop($('cpv'), F19 + 2.05);
      pop($('cb3'), F19 + 3.15);
    }
    // dotknięcia
    let html = '';
    for (const tp of M.phone.taps) {
      const d = T - (SC.f18.start + PH_OFF + tp.t);
      if (d < -0.12 || d > 0.6) continue;
      const k = d < 0 ? 1 + d / 0.12 : 1;
      const e = d < 0 ? 0 : E.outCubic(d / 0.6);
      const r = (d < 0 ? 16 * k : 16 + 18 * e);
      const a = d < 0 ? k * 0.9 : 0.9 * (1 - e);
      html += `<div class="tap" style="left:${(tp.x - r).toFixed(1)}px;top:${(tp.y + 54 - r).toFixed(1)}px;width:${(2 * r).toFixed(1)}px;height:${(2 * r).toFixed(1)}px;opacity:${a.toFixed(3)}"></div>`;
    }
    hx($('phTaps'), html);
  }

  // ---------------- HUD ----------------
  function wordsAnim(s, T) {
    const d = s._ttl;
    const tIn = s.start + (s.id === 'hook' ? 0.25 : 0.06), tOut = s.id === 'outro' ? SC.outro.start + 5.25 : s.end - 0.34;
    const visible = T >= tIn - 0.01 && T < tOut + 0.75;
    show(d, visible);
    if (!visible) return;
    s._words.forEach((w, i) => {
      const ki = clamp((T - tIn - i * 0.055) / 0.85, 0, 1), ei = E.outExpo(ki);
      const ko = clamp((T - tOut - i * 0.028) / 0.46, 0, 1), eo = E.inCubic(ko);
      const y = (1 - ei) * 112 - eo * 112;
      st(w, 'transform', `translate3d(0,${y.toFixed(3)}%,0)`);
      st(w, 'opacity', (Math.min(1, ki * 2.5) * (1 - ko * 0.6)).toFixed(3));
    });
  }
  function capsAnim(s, T) {
    (s.caps || []).forEach((c, i) => {
      const e = s._caps[i];
      const t0 = s.start + c.t, t1 = i + 1 < s.caps.length ? s.start + s.caps[i + 1].t - 0.05 : s.end - 0.28;
      const vis = T >= t0 && T < t1 + 0.45;
      show(e, vis);
      if (!vis) return;
      const ki = E.outCubic(clamp((T - t0) / 0.7, 0, 1)), ko = E.inCubic(clamp((T - t1) / 0.4, 0, 1));
      st(e, 'opacity', (ki * (1 - ko)).toFixed(3));
      st(e, 'transform', `translate3d(0,${px((1 - ki) * 26 - ko * 18)},0)`);
      st(e, 'filter', ki < 0.999 || ko > 0 ? `blur(${((1 - ki) * 9 + ko * 6).toFixed(2)}px)` : 'none');
      e.style.setProperty('--d', E.outExpo(clamp((T - t0 + 0.1) / 0.6, 0, 1)).toFixed(3));
    });
  }
  function renderHud(T, sc, L) {
    S.scenes.forEach(s => { wordsAnim(s, T); capsAnim(s, T); });
    // nagłówek
    const lbl = s => (s.n ? null : s.label);
    const idx = S.scenes.indexOf(sc), prev = S.scenes[idx - 1];
    const lA = $('lblA'), lB = $('lblB'), cnt = $('cnt');
    const kc = clamp(L / 0.5, 0, 1), ec = E.outCubic(kc);
    const curL = lbl(sc), prvL = prev ? lbl(prev) : null;
    tx(lA, curL || ''); tx(lB, (kc < 1 && prvL && prvL !== curL) ? prvL : '');
    st(lA, 'transform', `translateY(${px((prvL !== curL ? (1 - ec) * 30 : 0))})`); st(lA, 'opacity', (curL ? (prvL !== curL ? ec : 1) : 0).toFixed(3));
    st(lB, 'transform', `translateY(${px(-ec * 30)})`); st(lB, 'opacity', (1 - ec).toFixed(3));
    // licznik 01 / 19 (cyfry się toczą)
    const n = sc.n || 0, pn = prev && prev.n ? prev.n : 0;
    if (n) {
      const a = String(n).padStart(2, '0'), b = String(pn || 0).padStart(2, '0');
      let h = '';
      for (let i = 0; i < 2; i++) {
        const chg = pn && a[i] !== b[i];
        const k = chg ? E.outExpo(clamp(L / 0.6, 0, 1)) : 1;
        h += `<span class="dg"><span style="transform:translateY(${((1 - k) * 100).toFixed(2)}%)">${a[i]}</span>${chg && k < 1 ? `<span style="transform:translateY(${(-k * 100).toFixed(2)}%)">${b[i]}</span>` : ''}</span>`;
      }
      hx(cnt, h + '<span class="of"> / 19</span>');
      const ka = pn ? 1 : E.outCubic(clamp(L / 0.5, 0, 1));
      st(cnt, 'opacity', ka.toFixed(3)); st(cnt, 'transform', `translateY(${px((1 - ka) * 30)})`);
      show(cnt, true);
    } else {
      const ko = prev && prev.n ? 1 - E.outCubic(clamp(L / 0.4, 0, 1)) : 0;
      show(cnt, ko > 0.001);
      st(cnt, 'opacity', ko.toFixed(3)); st(cnt, 'transform', `translateY(${px(-(1 - ko) * 30)})`);
    }
    // pasek postępu / linia
    const progA = T < SC.f01.start ? seg(T, SC.f01.start - 0.4, 0.4) : T > SC.outro.start + 5.2 ? 1 - seg(T, SC.outro.start + 5.2, 0.4) : 1;
    st($('prog'), 'opacity', progA.toFixed(3));
    const lineA = T < SC.f01.start ? seg(T, 0.15, 0.9, E.outCubic) : 0;
    st($('line'), 'transform', `scaleX(${lineA.toFixed(4)})`); st($('line'), 'opacity', (T < SC.f01.start ? 1 - seg(T, SC.f01.start - 0.4, 0.4) : 0).toFixed(3));
    [...$('prog').children].forEach((e, i) => {
      const s = S.scenes.find(x => x.n === i + 1);
      const k = T >= SC.outro.start ? 1 : clamp((T - s.start) / s.dur, 0, 1);
      st(e.firstChild, 'transform', `scaleX(${k.toFixed(4)})`);
    });
    const hdrA = T > SC.outro.start + 5.2 ? 1 - seg(T, SC.outro.start + 5.2, 0.4) : seg(T, 0.1, 0.6, E.outCubic);
    st($('hdr'), 'opacity', hdrA.toFixed(3));
    // duża cyfra w tle (jak na stronie)
    renderGhost(T, sc, L);
    // lista przed → teraz
    renderList(T);
    renderCheck(T);
  }
  function ghostTxt(s) { return s.id === 'hook' ? '19' : s.n ? String(s.n).padStart(2, '0') : ''; }
  function renderGhost(T, sc, L) {
    const g = $('ghost');
    const idx = S.scenes.indexOf(sc), prev = S.scenes[idx - 1];
    const a = ghostTxt(sc), b = prev ? ghostTxt(prev) : '';
    const k = E.outExpo(clamp((L - 0.05) / 1.1, 0, 1)), ko = E.inCubic(clamp(L / 0.5, 0, 1));
    let h = '';
    if (a) h += `<span style="transform:translate3d(0,${((1 - k) * 60).toFixed(2)}%,0);opacity:${k.toFixed(3)}">${a}</span>`;
    if (b && b !== a && ko < 1) h += `<span style="transform:translate3d(0,${(-ko * 40).toFixed(2)}%,0);opacity:${(1 - ko).toFixed(3)}">${b}</span>`;
    if (a === b && a) h = `<span>${a}</span>`;
    hx(g, h);
  }
  function renderList(T) {
    const Z0 = SC.zmiany.start, L = T - Z0;
    const on = L > 0 && L < 10.8;
    show($('list'), on);
    if (!on) return;
    [...$('list').children].forEach((r, i) => {
      const ki = E.outExpo(clamp((L - 0.75 - i * 0.16) / 0.9, 0, 1));
      const ko = E.inCubic(clamp((L - 9.05 - i * 0.06) / 0.45, 0, 1));
      st(r, 'opacity', (ki * (1 - ko)).toFixed(3));
      st(r, 'transform', `translate3d(${px((1 - ki) * -40)},${px(-ko * 26)},0)`);
      st(r.querySelector('.ln'), 'transform', `scaleX(${E.outCubic(clamp((L - 0.9 - i * 0.16) / 0.9, 0, 1)).toFixed(4)})`);
      const t0 = 5.0 + i * 0.9;
      const ks = E.io(clamp((L - t0) / 0.32, 0, 1));
      st(r.querySelector('s'), 'transform', `scaleX(${ks.toFixed(4)})`);
      const old = r.querySelector('.old'), arr = r.querySelector('.arr'), nw = r.querySelector('.nw');
      const ow = old.offsetWidth;
      st(old, 'color', ks > 0.5 ? 'rgba(23,23,26,.38)' : '#17171a');
      const ka = E.outExpo(clamp((L - t0 - 0.18) / 0.8, 0, 1));
      st(arr, 'left', px(ow + 22)); st(arr, 'opacity', ka.toFixed(3)); st(arr, 'transform', `translateX(${px((1 - ka) * -16)})`);
      const kn = E.outExpo(clamp((L - t0 - 0.28) / 0.85, 0, 1));
      st(nw, 'left', px(ow + 74)); st(nw, 'opacity', kn.toFixed(3)); st(nw, 'transform', `translateX(${px((1 - kn) * 30)})`);
    });
  }
  function renderCheck(T) {
    const F18 = SC.f18.start, L = T - F18;
    const on = L > 0 && T < SC.f19.start + 0.6;
    show($('check'), on);
    if (!on) return;
    const out = E.inCubic(clamp((T - SC.f19.start + 0.1) / 0.5, 0, 1));
    const tick = [PH_OFF + 1.45, PH_OFF + 3.6, PH_OFF + 6.75];
    [...$('check').children].forEach((r, i) => {
      const ki = E.outExpo(clamp((L - 0.7 - i * 0.14) / 0.8, 0, 1));
      st(r, 'opacity', (ki * (1 - out)).toFixed(3));
      st(r, 'transform', `translate3d(${px((1 - ki) * -30 - out * 30)},0,0)`);
      const kc = clamp((L - tick[i]) / 0.45, 0, 1);
      const cf = r.querySelector('.cf'), tk2 = r.querySelector('.tk');
      cf.setAttribute('r', (18.5 * E.outBack(kc)).toFixed(2));
      tk2.setAttribute('stroke-dashoffset', (26 * (1 - E.outCubic(clamp((L - tick[i] - 0.12) / 0.4, 0, 1)))).toFixed(2));
      st(r.querySelector('.lb'), 'color', kc > 0 ? '#17171a' : 'rgba(23,23,26,.45)');
    });
  }

  // ---------------- lupy ----------------
  const LOUPES = [];
  function loupes() {
    const ex = (m, p) => (m ? [m.x - p, m.y - p, m.w + 2 * p, m.h + 2 * p] : null);
    const sum = mk('sum');
    if (sum) LOUPES.push({ T0: at('f09', 1.9), T1: at('f09', 5.2), src: ex(sum, 14), pos: [540, 1250], w: 760 });
    let toast = mk('toast');
    // pomiar wypadł w trakcie wjazdu toastu — toast jest zawsze wyśrodkowany na dole (szerokość z tekstu)
    if (!toast || toast.w < 100) toast = { x: 640 - 224, y: 670 + 72, w: 448, h: 38 };
    if (toast) LOUPES.push({ T0: at('f10', 7.25), T1: at('f10', 9.4), src: ex(toast, 18), pos: [540, 1270], w: 900 });
    const cp = mk('copy');
    if (cp) LOUPES.push({ T0: at('f11', 1.85), T1: at('f11', 3.3), src: [cp.x - 330, cp.y - 16, cp.w + 380, cp.h + 32], pos: [540, 1260], w: 860 });
    const ck = mk('clock');
    if (ck) LOUPES.push({ T0: at('f11', 4.5), T1: at('f11', 7.0), src: ex(ck, 16), pos: [540, 1250], w: 820 });
    LOUPES.push({ T0: at('f13', 3.35), T1: at('f13', 5.1), src: [0, 72, 330, 230], pos: [540, 1180], w: 640, cursor: true });
  }
  function renderLoupes(T) {
    const box = $('loupes'), wires = $('wires');
    let i = 0, wh = '';
    const active = LOUPES.filter(l => T > l.T0 - 0.05 && T < l.T1 + 0.5);
    while (box.children.length < active.length) { const d = document.createElement('div'); d.className = 'lp'; d.innerHTML = '<img><svg class="lcur" viewBox="0 0 30 44"><path d="M3 2.5v33.6l8.2-7.7 5.3 12.3 5.6-2.4-5.2-12h11.3z" fill="#111" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/></svg>'; box.appendChild(d); }
    [...box.children].forEach((d, j) => show(d, j < active.length));
    const ol = $('outlines');
    let oh = '';
    for (const l of active) {
      const d = box.children[i++];
      const kin = spring(T - l.T0, 9, 0.62), kout = E.inCubic(clamp((T - l.T1) / 0.4, 0, 1));
      const a = clamp((T - l.T0) / 0.18, 0, 1) * (1 - kout);
      const z = l.w / l.src[2], h = l.src[3] * z;
      const sc = (0.72 + 0.28 * kin) * (1 - 0.15 * kout);
      st(d, 'left', px(l.pos[0] - l.w / 2)); st(d, 'top', px(l.pos[1] - h / 2));
      st(d, 'width', px(l.w)); st(d, 'height', px(h));
      st(d, 'opacity', a.toFixed(3));
      st(d, 'transform', `translate3d(0,${px((1 - kin) * 40 + kout * 30)},0) scale(${sc.toFixed(4)})`);
      const img = d.firstChild;
      im(img, $('vpA')._u);
      st(img, 'width', '1280px'); st(img, 'height', '728px');
      st(img, 'transform', `scale(${z.toFixed(4)}) translate(${px(-l.src[0])},${px(-(l.src[1] - 72))})`);
      const lc = d.lastChild, c = cursorAt(T);
      if (l.cursor && c) { show(lc, true); st(lc, 'transform', `translate(${px((c.x - 3 - l.src[0]) * z)},${px((c.y - 3 - l.src[1]) * z)}) scale(${(z * 0.62).toFixed(3)})`); } else show(lc, false);
      // obrys źródła na ekranie + linia do lupy
      oh += `<div style="left:${l.src[0]}px;top:${l.src[1] - 72}px;width:${l.src[2]}px;height:${l.src[3]}px;opacity:${(a * 0.9).toFixed(3)}"></div>`;
    }
    hx(ol, oh);
    // linie łączące (po przeliczeniu transformacji przez przeglądarkę)
    if (active.length) {
      const outs = [...ol.children];
      active.forEach((l, j) => {
        const r1 = outs[j].getBoundingClientRect(), r2 = box.children[j].getBoundingClientRect();
        const a = parseFloat(outs[j].style.opacity) || 0;
        if (a < 0.02) return;
        const x1 = r1.left + r1.width / 2, y1 = r1.bottom, x2 = r2.left + r2.width / 2, y2 = r2.top;
        wh += `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="rgba(23,23,26,${(0.35 * a).toFixed(3)})" stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"/><circle cx="${x1.toFixed(1)}" cy="${y1.toFixed(1)}" r="5" fill="rgba(23,23,26,${(0.8 * a).toFixed(3)})"/>`;
      });
    }
    hx(wires, wh);
  }

  // ---------------- plansza końcowa ----------------
  function renderEnd(T) {
    const O = SC.outro.start, L = T - O;
    const a = seg(T, O + 5.75, 0.6, E.outCubic);
    st($('end'), 'opacity', a.toFixed(3)); show($('end'), a > 0.001);
    if (a <= 0) return;
    const e = $('end');
    const f = (sel, t0, dy = 20) => { const el = e.querySelector(sel); const k = E.outExpo(clamp((L - t0) / 0.9, 0, 1)); st(el, 'opacity', k.toFixed(3)); st(el, 'transform', `translate3d(0,${px((1 - k) * dy)},0)`); };
    f('.pf', 6.2); f('.tag', 7.75); f('.dom', 8.1, 30); f('.q', 8.85); f('.q2', 9.05);
    st(e.querySelector('.ul'), 'transform', `scaleX(${E.io(clamp((L - 8.35) / 0.7, 0, 1)).toFixed(4)})`);
    // imię pismem odręcznym — odsłaniane jak pisane piórem (miękka krawędź jedzie od lewej)
    const p = E.sine(clamp((L - 6.25) / 1.9, 0, 1)) * 112 - 6;
    const nm = $('endName');
    st(nm, 'webkitMaskImage', `linear-gradient(90deg,#000 ${p.toFixed(2)}%,rgba(0,0,0,0) ${(p + 6).toFixed(2)}%)`);
    st(nm, 'maskImage', `linear-gradient(90deg,#000 ${p.toFixed(2)}%,rgba(0,0,0,0) ${(p + 6).toFixed(2)}%)`);
  }

  // =====================================================================
  // DŹWIĘK — lista zdarzeń dla syntezatora
  // =====================================================================
  function sfx() {
    const ev = [];
    const add = (t, type, o = {}) => ev.push(Object.assign({ t: +t.toFixed(4), type }, o));
    S.scenes.forEach((s, i) => { if (i) add(s.start - 0.12, 'whoosh', { amt: s.n ? 0.55 : 0.9 }); });
    CLICKS.forEach(c => add(c.T, 'click'));
    M.phone.taps.forEach(tp => add(SC.f18.start + PH_OFF + tp.t, 'tap'));
    // zmiany podstron w ujęciu main (kurtyna)
    let lp = null;
    M.main.frames.forEach((f, i) => { if (lp !== null && f.path !== lp) add(S.mainStart + i / FPS - 0.5, 'curtain'); lp = f.path; });
    const Z0 = SC.zmiany.start;
    add(Z0 + 3.2, 'peel'); add(Z0 + 3.62, 'crash'); add(Z0 + 3.75, 'glitch'); add(Z0 + 4.62, 'thud');
    WIPES.forEach(w => add(Z0 + w[0], 'swish'));
    for (let i = 0; i < 4; i++) { add(Z0 + 0.75 + i * 0.16, 'tick', { v: 0.5 }); add(Z0 + 5.0 + i * 0.9, 'strike'); add(Z0 + 5.3 + i * 0.9, 'pop', { v: 0.6 }); }
    LOUPES.forEach(l => { add(l.T0, 'pop', { v: 0.8 }); add(l.T1, 'unpop', { v: 0.4 }); });
    const F16 = SC.f16.start;
    for (let i = 0; i < 41; i++) add(F16 + 1.05 + i * (1.45 / 41) + (rnd(i, 9) - 0.5) * 0.02, 'key', { v: 0.6 + rnd(i, 3) * 0.4 });
    add(F16 + 2.75, 'enter');
    add(at('f13', 4.45), 'shimmer');
    add(at('f10', 7.05), 'ding'); add(at('f11', 1.75), 'ding'); add(at('f13', 4.45), 'ding');
    [1.45, 3.6, 6.75].forEach(t => add(SC.f18.start + PH_OFF + t, 'pop', { v: 0.7 }));
    add(SC.f18.start + PH_OFF + 6.1, 'buzz');
    [0.5, 1.75, 2.05, 3.15].forEach(t => add(SC.f19.start + t, 'bubble'));
    for (let i = 0; i < 8; i++) add(SC.f19.start + 4.25 + i * 0.2, 'tick', { v: 0.45 });
    add(0.62, 'power');
    add(SC.outro.start + 5.3, 'riser');
    add(SC.outro.start + 6.2, 'final');
    S.scenes.forEach(s => { if (s.n) add(s.start + 0.05, 'count', { v: 0.5 }); });
    return ev.sort((a, b) => a.t - b.t);
  }

  // =====================================================================
  choreo();
  buildChannels();
  initStatic();
  cursorOverrides();
  compClicks();
  buildClicks();
  loupes();
  window.render = render;
  window.dbg = T => ({ s: Math.exp(ch('cz', T)), cx: ch('cx', T), cy: ch('cy', T), msg: mk('msg'), form: mk('form') });
  window.sfx = sfx;
  window.TOTAL = S.total;
  // wszystkie kroje wczytane z góry (inaczej pierwsza klatka z nowym znakiem pokazałaby krój zastępczy)
  window.ready = Promise.all(['300 40px "Inter V"', '680 40px "Inter V"', '20px Mono', '40px Script', '40px "Serif I"', '40px Garamond', '40px Caveat', '40px Emoji']
    .map(f => document.fonts.load(f, f.includes('Emoji') ? '👀👇😍' : 'Aąę'))).then(() => document.fonts.ready);
})();
