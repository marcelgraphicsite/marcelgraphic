// Lokalny serwer strony do nagrywania reela: czyste adresy (/prace → prace.html) i własna 404 — jak na GitHub Pages.
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(process.env.ROOT || path.join(__dirname, '../..'));
const PORT = +process.env.PORT || 8123;
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2', '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml', '.vcf': 'text/vcard', '.webmanifest': 'application/manifest+json', '.mp3': 'audio/mpeg', '.wav': 'audio/wav' };
const send = (res, file, code) => {
  res.writeHead(code || 200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store', 'Access-Control-Allow-Origin': '*' });
  fs.createReadStream(file).pipe(res);
};
http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROOT, path.normalize(p));
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  for (const c of [f, f + '.html']) if (fs.existsSync(c) && fs.statSync(c).isFile()) return send(res, c);
  send(res, path.join(ROOT, '404.html'), 404);
}).listen(PORT, () => console.log('serwer: http://localhost:' + PORT));
