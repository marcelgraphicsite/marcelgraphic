// Generuje obrazki podglądu linku (1200×630) dla każdej podstrony i poradnika.
// Uruchom z katalogu repozytorium:  NODE_PATH=$(npm root -g) node _zrodla/zbuduj_og.js
// Wynik: assets/img/og/<strona>.jpg oraz assets/img/og.jpg (strona główna).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.join(__dirname, '..');
const font = f => 'data:font/woff2;base64,' + fs.readFileSync(path.join(ROOT, 'assets/fonts', f)).toString('base64');

const PAGES = [
  { file: 'og.jpg', home: true },
  { file: 'og/prace.jpg', n: '01', k: 'Prace', t: 'Przewiń projekt tak, jak zrobiłby to <em>Twój klient.</em>' },
  { file: 'og/uslugi.jpg', n: '02', k: 'Usługi', t: 'Trzy sposoby, żeby klienci wybierali <em>Ciebie.</em>' },
  { file: 'og/cennik.jpg', n: '03', k: 'Cennik', t: 'Jasne ceny. <em>Zero ukrytych kosztów.</em>', s: 'Strony od 2 000 zł · Social media od 600 zł / mies. · Karty NFC od 60 zł' },
  { file: 'og/o-mnie.jpg', n: '04', k: 'O mnie', t: 'Nie sprzedaję stron. <em>Sprzedaję pierwsze wrażenie.</em>' },
  { file: 'og/kontakt.jpg', n: '05', k: 'Kontakt', t: 'Zobacz swoją nową stronę, <em>zanim wydasz złotówkę.</em>', s: 'Darmowy projekt · Odpowiedź w 24 godziny' },
  { file: 'og/poradnik.jpg', n: '06', k: 'Poradnik', t: 'Poradnik dla firm. <em>Bez lania wody.</em>', s: 'Ceny stron · Wizytówka Google · Opinie · Restauracje i salony' },
  { file: 'og/ile-kosztuje-strona-internetowa.jpg', n: '06', k: 'Poradnik', t: 'Ile kosztuje strona internetowa <em>w 2026 roku?</em>', s: 'Realne ceny, koszty stałe i jak nie przepłacić' },
  { file: 'og/strona-internetowa-czy-facebook.jpg', n: '06', k: 'Poradnik', t: 'Strona internetowa czy Facebook — <em>co wybrać?</em>', s: 'Strona zdobywa nowych klientów, social media zamieniają ich w stałych' },
  { file: 'og/jak-zdobyc-opinie-google.jpg', n: '06', k: 'Poradnik', t: 'Jak zdobyć więcej opinii <em>w Google?</em>', s: '7 sposobów dla lokalnej firmy: link, kod QR, karta NFC' },
  { file: 'og/strony-internetowe-sieradz.jpg', n: '02', k: 'Usługi · Sieradz', t: 'Strony internetowe <em>w Sieradzu.</em>', s: 'Od 2 000 zł · gotowe w 4–16 dni · spotkanie na miejscu' },
  { file: 'og/karty-nfc-opinie-google.jpg', n: '02', k: 'Usługi · Opinie Google', t: 'Karty NFC do opinii <em>Google.</em>', s: 'Karta z podstawką 60 zł · naklejka 80 zł · wysyłka w Polsce' },
  { file: 'og/prowadzenie-social-media.jpg', n: '02', k: 'Usługi · Social media', t: 'Prowadzenie social mediów <em>dla firm.</em>', s: '8 lub 12–13 postów miesięcznie · od 600 zł / mies.' },
  { file: 'og/landing-page-czy-strona-wizytowka.jpg', n: '06', k: 'Poradnik', t: 'Landing page czy strona wizytówka — <em>co wybrać?</em>', s: 'Cena, czas realizacji i widoczność w Google — porównanie' },
  { file: 'og/jak-zalozyc-wizytowke-google.jpg', n: '06', k: 'Poradnik', t: 'Jak założyć Wizytówkę Google — <em>krok po kroku</em>', s: 'Nazwa, kategoria, obszar działania i weryfikacja wideo' },
  { file: 'og/czy-twoja-firma-jest-widoczna-w-google.jpg', n: '06', k: 'Poradnik', t: 'Czy Twoja firma jest widoczna <em>w Google?</em>', s: 'Test w 10 minut: wyszukiwarka, Mapy, opinie i asystenci AI' },
  { file: 'og/strona-internetowa-dla-restauracji.jpg', n: '06', k: 'Poradnik', t: 'Strona internetowa dla restauracji — <em>co musi mieć?</em>', s: 'Menu, godziny, zamówienia, rezerwacje i zdjęcia' },
  { file: 'og/strona-internetowa-dla-salonu-urody.jpg', n: '06', k: 'Poradnik', t: 'Strona internetowa dla salonu urody — <em>co musi mieć?</em>', s: 'Cennik, rezerwacja online, galeria metamorfoz i opinie' },
  { file: 'og/polityka-prywatnosci.jpg', n: '07', k: 'Polityka prywatności', t: 'Twoje dane. <em>Krótko i po ludzku.</em>' },
];

const css = `
@font-face{font-family:Inter;font-weight:300 700;src:url(${font('inter-var.woff2')}) format("woff2")}
@font-face{font-family:Mono;src:url(${font('jetbrains-mono-400.woff2')}) format("woff2")}
@font-face{font-family:Script;src:url(${font('gv-script.woff2')}) format("woff2")}
@font-face{font-family:Card;font-weight:500;src:url(${font('eb-garamond-500.woff2')}) format("woff2")}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1200px;height:630px}
body{position:relative;overflow:hidden;background:#f4f3ef;color:#17171a;font-family:Inter;-webkit-font-smoothing:antialiased;letter-spacing:-.011em}
.light{position:absolute;inset:0;background:radial-gradient(60% 70% at 18% 12%,rgba(255,255,252,.95),rgba(255,255,252,0) 70%),radial-gradient(55% 60% at 88% 92%,rgba(222,217,203,.75),rgba(222,217,203,0) 70%)}
.ghost{position:absolute;left:-40px;white-space:nowrap;font-weight:600;letter-spacing:-.04em;color:rgba(23,23,26,.035);font-size:190px;line-height:1}
.logo{position:absolute;top:44px;left:56px;font-family:Script;font-size:30px;line-height:.92}
.num{position:absolute;top:-40px;right:-22px;font-weight:600;font-size:400px;letter-spacing:-.06em;line-height:.8;color:rgba(23,23,26,.04)}
.k{position:absolute;top:58px;right:56px;font-family:Mono;font-size:15px;letter-spacing:.08em;text-transform:uppercase;color:#6f6d66}
.t{position:absolute;left:56px;right:110px;bottom:150px;font-weight:600;font-size:76px;letter-spacing:-.045em;line-height:1.0}
.t em{font-style:normal;font-weight:300}
.s{position:absolute;left:58px;bottom:104px;font-family:Mono;font-size:17px;color:#6f6d66;letter-spacing:.01em}
.foot{position:absolute;left:56px;right:56px;bottom:44px;display:flex;justify-content:space-between;font-family:Mono;font-size:15px;color:#6f6d66;letter-spacing:.02em;padding-top:18px;border-top:1px solid rgba(23,23,26,.12)}
.home .name{position:absolute;left:0;right:0;top:150px;text-align:center;font-weight:600;font-size:150px;letter-spacing:-.05em;line-height:.86}
.home .cap{position:absolute;left:0;right:0;top:442px;text-align:center;font-family:Card;font-weight:500;font-size:27px;letter-spacing:.2em;text-transform:uppercase;color:#424245}
`;

const html = p => `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body class="${p.home ? 'home' : ''}">
<div class="light"></div>
${[0, 1, 2, 3].map(i => `<div class="ghost" style="top:${-30 + i * 170}px;left:${i % 2 ? -260 : -40}px">Marcel Struszczak · Marcel Struszczak ·</div>`).join('')}
${p.home ? '' : `<div class="num">${p.n}</div>`}
<div class="logo">Marcel<br>Struszczak</div>
${p.home
    ? `<div class="name">Marcel<br>Struszczak</div><div class="cap">Cyfrowy rozwój lokalnych firm</div>
       <div class="foot"><span>Strony internetowe · Social media · Opinie Google</span><span>marcelgraphicsite.pl</span></div>`
    : `<div class="k">(${p.n}) ${p.k}</div><div class="t">${p.t}</div>${p.s ? `<div class="s">${p.s}</div>` : ''}
       <div class="foot"><span>Marcel Struszczak · Cyfrowy rozwój lokalnych firm</span><span>marcelgraphicsite.pl</span></div>`}
</body></html>`;

(async () => {
  fs.mkdirSync(path.join(ROOT, 'assets/img/og'), { recursive: true });
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  for (const p of PAGES) {
    await page.setContent(html(p), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    // tytuł nie może wyjść poza obrazek: w razie potrzeby zmniejsz czcionkę
    await page.evaluate(() => {
      const t = document.querySelector('.t'); if (!t) return;
      let fs = 76; while ((t.getBoundingClientRect().top < 150 || t.scrollWidth > t.clientWidth + 2) && fs > 48) { fs -= 2; t.style.fontSize = fs + 'px'; }
    });
    const out = path.join(ROOT, 'assets/img', p.file);
    await page.screenshot({ path: out, type: 'jpeg', quality: 86 });
    console.log('zapisano', p.file, Math.round(fs.statSync(out).size / 1024) + ' KB');
  }
  await b.close();
})();
