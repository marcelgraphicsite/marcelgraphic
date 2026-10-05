// Scenariusz reela „19 smaczków mojej nowej strony” — wspólny dla nagrywarki, sceny i dźwięku.
// Czas liczony w taktach muzyki (100 BPM → 1 takt = 2,4 s), żeby każda zmiana sceny wypadała na raz.
(function (root) {
  const BPM = 100;
  const BAR = 240 / BPM; // 2.4 s
  const FPS = 60;

  // ** pogrubienie ** jak w nagłówkach strony
  const scenes = [
    { id: 'hook', bars: 2.5, label: 'CZĘŚĆ 2 · NOWA STRONA', title: '**19 smaczków**|mojej nowej strony.',
      caps: [{ t: 3.0, text: 'Większości nie zauważysz. Pokażę Ci każdy.' }] },
    { id: 'zmiany', bars: 4.5, label: 'PRZED → TERAZ', title: '**Co się** zmieniło?' },

    // ---- jedno ciągłe ujęcie strony na komputerze (take „main”) ----
    { id: 'f01', n: 1, bars: 3, take: 'main', title: '**Litery chudną** pod kursorem.',
      caps: [{ t: 0.5, text: 'Krój zmienny — reaguje tylko na myszkę.' }, { t: 4.4, text: 'A pod nazwiskiem hasło z mojej wizytówki.' }] },
    { id: 'f02', n: 2, bars: 3, take: 'main', title: '**Hasło**, które się nie nudzi.',
      caps: [{ t: 0.6, text: 'pracuje · sprzedaje · zarabia · przyciąga' }, { t: 4.2, text: 'Belka z hasłami przyspiesza ze scrollem — i zawraca.' }] },
    { id: 'f03', n: 3, bars: 3, take: 'main', title: '**Scrollujesz w dół** — projekty jadą w bok.',
      caps: [{ t: 0.6, text: 'Przewijasz normalnie, a karty przesuwają się w poziomie.' }, { t: 3.9, text: 'Nad projektem kursor zmienia się w „Zobacz”.' }] },
    { id: 'f04', n: 4, bars: 2.5, take: 'main', title: '**Koniec strony?** Następna czeka.',
      caps: [{ t: 0.8, text: 'Słowo wypełnia się atramentem, im bliżej końca.' }] },
    { id: 'f05', n: 5, bars: 3, take: 'main', title: '**Kurtyna** między podstronami.',
      caps: [{ t: 0.5, text: 'Mój podpis rysuje się zamiast paska ładowania.' }, { t: 4.6, text: 'Dalej w menu — kurtyna z dołu. Wstecz — z góry.' }] },
    { id: 'f06', n: 6, bars: 4, take: 'main', title: '**Projekty działają** na żywo.',
      caps: [{ t: 0.5, text: 'Przewiń stronę klienta bez wychodzenia z mojej.' }, { t: 6.4, text: 'Komputer albo telefon — jedno kliknięcie.' }] },
    { id: 'f07', n: 7, bars: 4, take: 'main', title: '**Ilustracje**, które opowiadają ofertę.',
      caps: [{ t: 0.5, text: 'Każda usługa ma swoją małą animację.' }, { t: 5.6, text: 'Linia procesu rysuje się, gdy przewijasz.' }] },
    { id: 'f08', n: 8, bars: 3, take: 'main', title: '**Cennik** bez ukrytych kosztów.',
      caps: [{ t: 0.5, text: 'Wcześniej go nie było. Teraz: 4 zakładki.' }, { t: 4.1, text: 'Ceny przeliczają się na żywo.' }] },
    { id: 'f09', n: 9, bars: 4, take: 'main', title: '**Wycena** w 30 sekund.',
      caps: [{ t: 0.5, text: 'Kalkulator czyta ceny prosto z cennika.' }, { t: 5.4, text: 'Wynik sam wpisuje się do formularza.' }] },
    { id: 'f10', n: 10, bars: 4, take: 'main', title: '**Wizytówka 1:1** jak papierowa.',
      caps: [{ t: 0.5, text: 'Pochyla się za kursorem. Z tyłu kod QR i podpis.' }, { t: 5.5, text: 'A teraz obróć ją 4 razy pod rząd…' }] },
    { id: 'f11', n: 11, bars: 3, take: 'main', title: '**Kontakt** bez szukania.',
      caps: [{ t: 0.5, text: 'E-mail kopiuje się jednym kliknięciem.' }, { t: 3.9, text: 'Zegar mówi, czy właśnie pracuję.' }] },
    { id: 'f12', n: 12, bars: 3, take: 'main', title: '**Podpis kreślony** na żywo.',
      caps: [{ t: 0.5, text: 'Wstecz w menu — kurtyna zjeżdża z góry.' }, { t: 3.6, text: 'Przy każdym wejściu na „O mnie”.' }] },
    { id: 'f13', n: 13, bars: 3, take: 'main', title: '**Kliknij moje logo** 5 razy.',
      caps: [{ t: 0.5, text: 'Logo zawsze prowadzi na start.' }, { t: 4.7, text: 'Serio. Sprawdź u siebie.' }] },
    { id: 'f14', n: 14, bars: 2.5, take: 'main', title: '**Przełączysz kartę?** Strona zawoła.',
      caps: [{ t: 1.6, text: '„Wracaj — darmowy projekt czeka 👀”' }] },
    { id: 'f15', n: 15, bars: 2.5, take: 'main', title: '**Polski** albo angielski.',
      caps: [{ t: 0.5, text: 'Jedno kliknięcie — zostajesz w tym samym miejscu.' }] },
    { id: 'f16', n: 16, bars: 3, take: 'main', title: '**Nawet błąd** wygląda dobrze.',
      caps: [{ t: 3.4, text: 'Własna strona 404 — z drogą powrotną.' }] },
    { id: 'f17', n: 17, bars: 2.5, take: 'main', title: '**Wiadomość** w konsoli.',
      caps: [{ t: 0.9, text: 'Dla tych, którzy zaglądają pod maskę.' }] },

    // ---- telefon ----
    { id: 'f18', n: 18, bars: 4, take: 'phone', title: '**Na telefonie** tak samo płynnie.',
      caps: [{ t: 0.7, text: 'Menu, kurtyna, wizytówka — wszystko pod kciukiem.' }, { t: 6.7, text: 'Słabszy telefon? Strona sama włącza tryb lekki.' }] },
    { id: 'f19', n: 19, bars: 3.5, title: '**Gotowa na Google** i AI.',
      caps: [{ t: 0.5, text: 'Każda podstrona ma własny podgląd linku.' }, { t: 4.3, text: 'ChatGPT, Perplexity i Gemini mogą ją czytać i cytować.' }] },

    { id: 'outro', bars: 5, label: 'KONIEC CZĘŚCI 2', title: '**Resztę** znajdź sam.' }
  ];

  let t = 0;
  scenes.forEach(s => { s.start = t; s.dur = s.bars * BAR; t += s.dur; s.end = t; });
  const total = t;
  // czas ujęcia „main” liczony od początku f01
  const mainStart = scenes.find(s => s.id === 'f01').start;
  const take = {};
  scenes.forEach(s => {
    if (!s.take) return;
    if (!take[s.take]) take[s.take] = { start: s.start, scenes: [] };
    s.takeT = s.start - take[s.take].start;
    take[s.take].scenes.push(s.id);
  });
  const byId = {};
  scenes.forEach(s => { byId[s.id] = s; });

  const S = { BPM, BAR, FPS, scenes, byId, total, mainStart, take };
  if (typeof module !== 'undefined') module.exports = S; else root.SCEN = S;
})(this);
