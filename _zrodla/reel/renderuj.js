// Renderer reela: scena.html → klatki 1080×1920 → ffmpeg (H.264, 60 kl./s).
// Użycie:
//   node renderuj.js --stills=1.5,20,33.2 [--prev]          → PNG do $REEL_OUT/stills
//   node renderuj.js --from=0 --to=10 --out=seg.mp4 [--prev] → kawałek filmu
//   node renderuj.js --sfx=zdarzenia.json                     → lista zdarzeń dla dźwięku
//   node renderuj.js --all --workers=3                        → cały film (równolegle) bez dźwięku
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const S = require('./scenariusz.js');

const OUT = process.env.REEL_OUT || path.join(__dirname, 'out');
const args = process.argv.slice(2);
const arg = (k, d) => { const a = args.find(x => x.startsWith('--' + k + '=')); return a ? a.split('=')[1] : (args.includes('--' + k) ? true : d); };
const PREV = !!arg('prev', false);
const TAKES = arg('takes', path.join(OUT, PREV ? '../prev' : 'takes'));
const FPS = S.FPS;

function loadMeta() {
  const M = {};
  for (const k of ['main', 'hook', 'old', 'phone']) {
    const p = path.join(TAKES, k, 'meta.json');
    if (!fs.existsSync(p)) { if (!arg('stills') && !PREV) throw new Error('brak ujęcia: ' + p); M[k] = { frames: [{ x: 0, y: 0 }], clicks: [], taps: [], marks: {} }; continue; }
    const m = JSON.parse(fs.readFileSync(p, 'utf8'));
    m.frames = m.frames.map(f => ({ x: f.x, y: f.y, cur: f.cur, down: f.down, title: f.title, path: f.path }));
    M[k] = m;
  }
  return M;
}
function assets() {
  const root = path.resolve(__dirname, '../..');
  const html = fs.readFileSync(path.join(root, 'o-mnie.html'), 'utf8');
  const sig = (html.match(/<svg class="sig"[\s\S]*?<\/svg>/) || [''])[0];
  return {
    dir: 'file://' + path.resolve(TAKES),
    step: PREV ? 6 : 1,
    fav: 'file://' + path.join(root, 'assets/img/favicon.svg'),
    og: 'file://' + path.join(root, 'assets/img/og/cennik.jpg'),
    sig
  };
}

async function openScene() {
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files', '--force-color-profile=srgb', '--disable-lcd-text', '--font-render-hinting=none', '--hide-scrollbars'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('[błąd sceny]', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('[konsola]', m.text().slice(0, 200)); });
  const M = loadMeta(), A = assets();
  await page.addInitScript(([m, a]) => { window.META = m; window.ASSETS = a; }, [M, A]);
  await page.goto('file://' + path.join(__dirname, 'scena.html'));
  await page.evaluate(() => window.ready);
  const cdp = await page.context().newCDPSession(page);
  return { browser, page, cdp };
}
const shot = async (cdp, fmt) => Buffer.from((await cdp.send('Page.captureScreenshot', { format: fmt, quality: fmt === 'jpeg' ? 95 : undefined, optimizeForSpeed: fmt === 'jpeg' })).data, 'base64');

async function stills(list) {
  const { browser, page, cdp } = await openScene();
  const dir = path.join(OUT, 'stills');
  fs.mkdirSync(dir, { recursive: true });
  for (const t of list) {
    await page.evaluate(T => window.render(T), t);
    const f = path.join(dir, `t${t.toFixed(2).padStart(7, '0')}.png`);
    fs.writeFileSync(f, await shot(cdp, 'png'));
    console.log(f);
  }
  await browser.close();
}

function ffmpegSink(out) {
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '4.2',
    '-x264-params', 'keyint=120:min-keyint=60:aq-mode=3:deblock=-1,-1', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', String(FPS), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  return ff;
}

async function segment(from, to, out) {
  const { browser, page, cdp } = await openScene();
  const ff = ffmpegSink(out);
  const f0 = Math.round(from * FPS), f1 = Math.round(to * FPS);
  const t0 = Date.now();
  for (let f = f0; f < f1; f++) {
    await page.evaluate(T => window.render(T), f / FPS);
    const buf = await shot(cdp, 'jpeg');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - f0) % 300 === 0) console.log(`  [${path.basename(out)}] ${(f / FPS).toFixed(1)} s (${((Date.now() - t0) / Math.max(1, f - f0)).toFixed(0)} ms/kl.)`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
}

async function all(workers) {
  const total = S.total, dir = path.join(OUT, 'seg');
  fs.mkdirSync(dir, { recursive: true });
  const n = workers, parts = [];
  for (let i = 0; i < n; i++) parts.push([+(total * i / n).toFixed(4), +(total * (i + 1) / n).toFixed(4)]);
  // granice na pełnych klatkach
  parts.forEach(p => { p[0] = Math.round(p[0] * FPS) / FPS; p[1] = Math.round(p[1] * FPS) / FPS; });
  await Promise.all(parts.map((p, i) => new Promise((res, rej) => {
    const c = spawn(process.execPath, [__filename, `--from=${p[0]}`, `--to=${p[1]}`, `--out=${path.join(dir, `s${i}.mp4`)}`, `--takes=${TAKES}`].concat(PREV ? ['--prev'] : []), { stdio: 'inherit', env: process.env });
    c.on('close', code => (code ? rej(new Error('segment ' + i)) : res()));
  })));
  fs.writeFileSync(path.join(dir, 'list.txt'), parts.map((p, i) => `file 's${i}.mp4'`).join('\n'));
  console.log('segmenty gotowe');
}

(async () => {
  if (arg('stills')) await stills(String(arg('stills')).split(',').map(Number));
  else if (arg('sfx')) {
    const { browser, page } = await openScene();
    fs.writeFileSync(arg('sfx'), JSON.stringify(await page.evaluate(() => window.sfx()), null, 1));
    await browser.close();
  } else if (arg('all')) await all(+arg('workers', 3));
  else await segment(+arg('from', 0), +arg('to', 2), arg('out', path.join(OUT, 'seg.mp4')));
})();
