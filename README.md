# Marcel Struszczak — portfolio i oferta (wersja wielostronicowa)

Strona: https://marcelgraphicsite.pl/

## Co jest w środku

| Plik / folder | Co to jest |
|---|---|
| `index.html` | Start: intro z nazwiskiem, hero, belka z hasłami, wybrane projekty (poziomy scroll), usługi w skrócie, liczby, CTA |
| `prace.html` | Podgląd projektów na żywo (komputer / telefon) + opis każdego konceptu |
| `uslugi.html` | „Trzy sposoby…” z animowanymi ilustracjami + współpraca krok po kroku |
| `cennik.html` | Wycena: zakładki z pakietami (każda z własną animacją), formularz zapytania o wycenę, FAQ |
| `o-mnie.html` | Cytat, podpis rysujący się na żywo, tekst, zasady pracy |
| `kontakt.html` | Formularz + wizytówka 3D (obraca się, QR do Facebooka, podpis, „Zapisz kontakt”) |
| `luxe-salon.html`, `vesper-barber.html`, `zar-burger.html` | Projekty koncepcyjne |
| `404.html` | Własna strona błędu (GitHub Pages używa jej automatycznie) |
| `assets/css/style.css` | Wygląd wszystkich podstron (jeden plik) |
| `assets/js/app.js` | Przejścia między stronami, tło, animacje, zapytanie o wycenę, formularz, wizytówka |
| `assets/js/i18n.js` | Wersja angielska (przełącznik PL/EN) |
| `assets/js/lenis.min.js` | Płynne przewijanie myszką (biblioteka Lenis, licencja MIT) |
| `assets/fonts/` | Czcionki (lokalnie — bez Google Fonts) |
| `assets/img/` | Miniatury projektów, ikony, `og.jpg` (podgląd linku na FB/Messengerze) |
| `assets/zar/` | Zdjęcia do strony ŻAR |
| `assets/marcel-struszczak.vcf` | Kontakt do zapisania w telefonie (przycisk „Zapisz kontakt”) |
| `sitemap.xml` | Mapa strony do Google Search Console (generowana przez `_zrodla/zbuduj_poradnik.py`) |
| `strony-internetowe-sieradz.html`, `karty-nfc-opinie-google.html`, `prowadzenie-social-media.html` | Strony usług (generowane z `_zrodla/uslugi_tresc.py`) |
| `poradnik.html` + artykuły | Poradnik (generowany z `_zrodla/poradnik_tresc.py`) |
| `feed.xml` | Kanał RSS poradnika |

## Wdrożenie na GitHub Pages

1. Cała strona (razem z folderem `assets`) leży już w głównym katalogu repozytorium, stara wersja jednostronicowa jest zastąpiona.
2. Scal gałąź z poprawkami do gałęzi, z której publikuje GitHub Pages (zwykle `main` — widać to w Settings → Pages).
3. Po 1–2 minutach nowa wersja działa pod tym samym adresem.

`gmina-warta.html` (stary projekt) zostaje na serwerze, żeby wcześniej wysłane linki dalej działały — nowe portfolio go nie linkuje.

Stare linki z wersji jednostronicowej (np. `…/marcelgraphic/#kontakt`, `#cennik`, `#kalkulator`) same przekierowują na właściwą podstronę — nic, co już udostępniłeś, się nie zepsuje.

## Jak działają przejścia

- Pierwsze wejście na stronę główną (raz na kartę przeglądarki): kurtyna stoi zamknięta, a na środku przygaszone logo wypełnia się bielą — najpierw „Marcel”, potem „Struszczak”, jednym płynnym ruchem (ok. 2 s). To animacja CSS liczona przez kartę graficzną, więc nie przycina się nawet wtedy, gdy telefon w tym czasie wczytuje stronę. Logo cały czas stoi w jednym miejscu: gdy jest całe białe i strona się wczytała (najdłużej ok. 5 s; jeśli trzeba poczekać, napis spokojnie „oddycha”), gaśnie w miejscu i kurtyna się rozsuwa. Na czas intra pasek przeglądarki w telefonie jest czarny. Klik albo dowolny klawisz przyspiesza. Żeby zobaczyć intro jeszcze raz, otwórz stronę w nowej karcie (odświeżenie tej samej karty go nie pokazuje). Kod: `#cinema` w `index.html` i `style.css`, moduł `cinema` w `assets/js/app.js`; ruch wypełniania liczy `python3 _zrodla/zbuduj_intro.py` (po zmianie napisu albo kroju logo).
- Klik w link do innej podstrony: kurtyna wjeżdża z numerem i nazwą strony docelowej, nowa strona odsłania się spod niej. Dalej w menu = kurtyna z dołu, wstecz = z góry.
- Pasek ładowania to Twój podpis z wizytówki (wygładzona, schludna wersja). Rysuje się od kliknięcia, na nowej stronie dorysowuje się do końca i dopiero wtedy kurtyna się odsuwa.
- Napis na kurtynie stoi w miejscu i ma stały rozmiar przed i po zmianie strony (osobny, osadzony mini-krój — nic się nie doczytuje w trakcie).
- Kurtyna jedzie na karcie graficznej (transform), więc jest płynna także na starszych telefonach.
- Wybór pakietu w zakładce Wycena, zapytanie o wycenę albo „Chcę taką stronę” przy projekcie przenosi się do formularza w Kontakcie (z krótką notką, co zostało wybrane).
- Osoby z wyłączonymi animacjami w systemie przechodzą między stronami od razu, bez kurtyny.

## Słabsze urządzenia

- Strona sama rozpoznaje słabszy sprzęt (albo mierzy płynność przez sekundę po wczytaniu) i włącza „tryb lekki”: animacje zostają, znika tylko to, co najbardziej obciąża procesor i kartę graficzną (ziarno papieru, rozmycie pod menu, ciągłe odświeżanie tła).
- Na telefonach tło rusza się przy przewijaniu i przy zmianie strony, zamiast liczyć się bez przerwy — oszczędza baterię.
- Płynne przewijanie myszką (Lenis) pobiera się tylko na komputerach.
- Na telefonach nie ma rozmycia pod menu ani ziarna papieru — to najcięższe efekty dla słabszej karty graficznej, a na jasnym tle wyglądają tak samo.
- Efekty w pętli (obracające się światło na czarnych kartach, ilustracje usług) pracują tylko wtedy, gdy są na ekranie — przewinięte poza ekran nie obciążają telefonu.
- Start przejścia między stronami przelicza tylko kurtynę, nie całą stronę — brak przycięcia w chwili kliknięcia, także na starych telefonach.
- iPhone z wycięciem (notch) trzymany poziomo: logo, menu, marginesy i nazwisko na starcie nie wchodzą pod wycięcie ani zaokrąglone rogi.
- Starsze iPhone'y (iOS 14–15, np. 6s, 7, SE 1. gen.): wizytówka i nakładki mają zapasowe style, więc wyglądają tak samo jak na nowych.
- Strona nie da się „przesunąć w bok” palcem na żadnym iOS (nic nie wystaje poza ekran, także na 320 px).

## Smaczki

- Pod nazwiskiem na starcie hasło z wizytówki „Cyfrowy rozwój lokalnych firm” (tym samym krojem co na karcie; znika przy przewijaniu).
- Na komputerze litery nazwiska chudną pod kursorem (krój zmienny) — tylko myszka, telefony nie liczą nic (w trybie lekkim wyłączone).
- Wielkie słowo „następna strona” na dole każdej podstrony wypełnia się atramentem, im bliżej końca.
- Na Androidzie wizytówka lekko wibruje przy obracaniu.

## Animacje na każdym komputerze

- „Ogranicz ruch” w systemie (np. Windows → Ułatwienia dostępu → „Pokaż animacje” wyłączone, częste na słabszych PC) NIE wyłącza już animacji: zostają przenikania, liczniki, podpis, ilustracje, a kurtyna przy zmianie strony przenika zamiast jechać. Znika tylko duży ruch (paralaksa, przewijanie w bok, jadący pasek).
- Komputer bez sprzętowej akceleracji grafiki (wyłączona w przeglądarce, stary sterownik) jest wykrywany od razu i dostaje tryb lekki — bez rozmyć, ziarna i przeliczania tła przy scrollu.
- Płynność mierzona jest też podczas przewijania (nie tylko w spoczynku) — jeśli sprzęt się tnie, tryb lekki włącza się sam.

## SEO, AEO i GEO (Google, odpowiedzi AI, lokalnie)

**Na stronie (zrobione):**
- **Strony usług pod konkretne hasła:** `strony-internetowe-sieradz` (lokalnie: Sieradz, powiat sieradzki, okoliczne miasta), `karty-nfc-opinie-google` (cała Polska), `prowadzenie-social-media`. Każda: odpowiedź na górze („W skrócie”), karty z cenami (kopiowane z `cennik.html` przy budowaniu), FAQ, dane strukturalne Service (+ Product dla kart NFC).
- **Poradnik** (`poradnik` + 8 artykułów): ceny stron, landing czy wizytówka, Wizytówka Google krok po kroku, test widoczności w Google, strona czy Facebook, opinie Google, strona dla restauracji, strona dla salonu urody. Format „W skrócie” + spis treści + tabele + FAQ — tak, żeby Google i asystenci AI (ChatGPT, Gemini, Perplexity) mogli cytować konkretne odpowiedzi.
- Linkowanie wewnętrzne: stopka „Oferta” na każdej stronie, karty „Z poradnika” na stronie głównej i w Usługach, linki z cennika i z O mnie do stron usług.
- Dane strukturalne (JSON-LD) jako jeden graf: WebSite + firma (ProfessionalService z obszarem działania: Sieradz, powiat sieradzki, okoliczne miasta, województwo, Polska) + Marcel (Person) + usługi (Service, Offer) + artykuły (BlogPosting + FAQPage) + okruszki i daty na każdej stronie.
- Nazwy marki dla wyszukiwarek i AI: „Marcel Struszczak”, „Marcel GraphicSite”, „marcelgraphicsite.pl”, „marcel.graphicsite”.
- Osobny obrazek podglądu linku dla każdej podstrony i artykułu: `assets/img/og/`.
- `robots.txt` jawnie wpuszcza roboty wyszukiwarek AI (ChatGPT, Perplexity, Claude, Gemini, Apple, Bing/Copilot).
- `llms.txt` i `llms-full.txt` — wizytówka i pełna treść strony dla asystentów AI (pakiety, zasady wyceny, obszar działania, usługi, FAQ, artykuły).
- `sitemap.xml` (generowana: wszystkie strony bez „noindex”, data = ostatni commit pliku), `feed.xml` (kanał RSS poradnika), IndexNow (automat w `.github/workflows/indexnow.yml` po każdym pushu na gałąź strony).
- Google Search Console: plik weryfikacyjny `google1a4fd6f90fdf66e4.html` — **nie usuwaj go**, bo Search Console straci weryfikację.

**Po Twojej stronie — to daje najwięcej (plan z gotowymi tekstami dostałeś osobno):**
1. Google Search Console + Bing Webmaster Tools (zrobione 6.10.2026) → „Sprawdzanie adresu URL” → „Poproś o zindeksowanie” dla nowych stron.
2. Profil Firmy w Google (firma usługowa, ukryty adres, obszar: Sieradz i okolice), potem Bing Places i Apple Business.
3. Fixly, Oferteo i Useme — ich strony już są wysoko na „projektowanie stron internetowych Sieradz”.
4. Opinie od klientów, te same dane (nazwa, telefon, strona) wszędzie, link „Projekt: Marcel Struszczak” na stronach klientów.

**Nowy artykuł albo nowa strona usługi:** dopisz w `_zrodla/poradnik_tresc.py` (artykuł) albo `_zrodla/uslugi_tresc.py` (usługa), dodaj obrazek w `_zrodla/zbuduj_og.js`, numer/napis kurtyny w `assets/js/app.js` (ORDER/NUMS) i `assets/js/i18n.js` (pages), potem uruchom:
`python3 _zrodla/zbuduj_poradnik.py && python3 _zrodla/zbuduj_llms.py && NODE_PATH=$(npm root -g) node _zrodla/zbuduj_og.js`
(`zbuduj_poradnik.py` przy okazji odświeża sitemap.xml, feed.xml i karty „Z poradnika”). Folder `_zrodla` nie jest publikowany.

## Formularz

Zgłoszenia z `kontakt.html` idą na `marcel.graphicsite@gmail.com` przez darmowy Web3Forms — bez aktywacji, działa od razu.

- Klucz (`FORM_KEY` w `assets/js/app.js`) jest publiczny z założenia — tak działa Web3Forms. Zmiana adresu odbiorcy: nowy klucz z web3forms.com.
- Temat maila: „… : Imię (Firma)”; „Odpowiedz” trafia prosto do klienta, jeśli podał e-mail.
- Gdyby wysyłka się nie udała (brak sieci itp.), klientowi otwiera się program pocztowy z gotową wiadomością — nic nie przepada.
- Wyłączenie: `FORM_ENDPOINT = ''`.

## Bezpieczeństwo

- **CSP (Content-Security-Policy)** w `<meta>` na każdej podstronie (GitHub Pages nie pozwala ustawić nagłówków HTTP): tylko pliki z tej domeny + wysyłka formularza do Web3Forms; obce i wstrzyknięte skrypty są blokowane. Skrypty inline są dozwolone po skrócie SHA-256 — **po każdej zmianie skryptu inline uruchom `python3 _zrodla/zbuduj_csp.py`** (robi to też `zbuduj_poradnik.py`), inaczej przeglądarka go zablokuje. Projekty koncepcyjne nie mają CSP.
- **Formularz:** walidacja, limity długości pól (HTML i JS), pułapka na boty (`_honey`), limit wysyłek z jednej przeglądarki (1 na minutę, 5 na dobę). Dane z formularza nigdy nie trafiają do HTML (tylko `textContent`).
- **Klucze:** jedyny klucz to publiczny klucz Web3Forms (z założenia jawny — pozwala tylko wysłać wiadomość na Twój e-mail). Plik klucza IndexNow i plik weryfikacji Google muszą być publiczne. Żadnych `.env`, haseł ani tokenów w repo i w historii.
- **Biblioteki:** wszystko z tej domeny; Vesper używa lokalnych kopii Alpine.js i GSAP z `assets/vendor/` (zamiast CDN).
- **Konta:** prawdziwe „wejście administratora” to konta GitHub, Google, rejestratora domeny i Web3Forms — wszędzie weryfikacja dwuetapowa.

## Ceny i wycena

- Na stronie nie ma cennika: wszędzie jest **wycena indywidualna i bezpłatna** (zakładka Wycena, adres `/cennik` bez zmian). Jedyne kwoty to **widełki dla orientacji** w bloku „Dla orientacji” na stronie Wycena (`#widelki`), pokazywane **dopiero po kliknięciu** „Pokaż widełki” — wartości są w `assets/js/i18n.js` (`window.__T.pl.ori` i `en.ori`), a nie w HTML, więc Google i asystenci AI ich nie cytują (blok ma też `data-nosnippet`). FAQ, dane strukturalne i `llms.txt` nie zawierają kwot; inne strony tylko odsyłają do bloku. Kwoty zostały tylko w projektach koncepcyjnych (ŻAR, Luxe, Vesper, Gmina Warta — to ceny wymyślonych lokali) i jako ogólne widełki rynkowe w artykule „Ile kosztuje strona internetowa”.
- `cennik.html` — karty pakietów (zakres, czas realizacji, poprawki) i formularz zapytania o wycenę. Formularz nie liczy kwot: zbiera, czego klient potrzebuje, liczy czas realizacji (atrybut `data-days` na kartach) i przenosi listę do formularza w Kontakcie.
- Teksty FAQ są w `cennik.html` (PL) i `assets/js/i18n.js` (EN); gotowe wiadomości „Interesuje mnie pakiet…” w `assets/js/i18n.js` (sekcje `pick` i `pickLabel`).
- Strony usług i poradnik budujesz z `_zrodla` (`python3 _zrodla/zbuduj_poradnik.py`, potem `python3 _zrodla/zbuduj_llms.py`); karty pakietów kopiują się tam z `cennik.html`.

## Wizytówka

- Wektorowa kopia Twojej wizytówki 85 × 55 mm: front z nazwiskiem, tyłem z kodem QR (prowadzi na Twój profil na Facebooku — ten sam adres co na papierowej) i podpisem, który rysuje się przy pierwszym obróceniu.
- „Zapisz kontakt” pobiera plik `assets/marcel-struszczak.vcf` (telefon, e-mail, strona, Facebook). Numer zmienisz w tym pliku i w stopkach stron (szukaj `511 808 498`).
- Mały żart: obróć kartę 4 razy pod rząd.

## Do sprawdzenia przed publikacją

- **Telefon 511 808 498** jest teraz na stronie (wizytówka, Kontakt, stopka, menu). Jeśli nie chcesz go publicznie — daj znać albo usuń linki `tel:`.
- **Facebook** — link w stopce i Kontakcie to adres z kodu QR na wizytówce.
- **Instagram** — `instagram.com/marcel.graphicsite`. Jeśli login jest inny, podmień go we wszystkich plikach (szukaj `instagram.com`).

## Projekty koncepcyjne

- Mają `noindex`, więc Google nie pokaże ich jako prawdziwych firm.
- Pasek „Projekt koncepcyjny”: „← Portfolio” wraca do podglądu tego samego projektu na `prace.html`, a „Chcę taką stronę” otwiera formularz z gotową wiadomością.
- W podglądzie na żywo (ramka na `prace.html`) pasek jest ukryty, żeby nie zasłaniał strony.

## Google

Dodaj stronę w Google Search Console, zgłoś `sitemap.xml` i wklej link do strony w swojej wizytówce Google.
