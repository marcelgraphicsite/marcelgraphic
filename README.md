# Marcel Struszczak — portfolio i oferta (wersja wielostronicowa)

Strona: https://marcelgraphicsite.pl/

## Co jest w środku

| Plik / folder | Co to jest |
|---|---|
| `index.html` | Start: intro z nazwiskiem, hero, belka z hasłami, wybrane projekty (poziomy scroll), usługi w skrócie, liczby, CTA |
| `prace.html` | Podgląd projektów na żywo (komputer / telefon) + opis każdego konceptu |
| `uslugi.html` | „Trzy sposoby…” z animowanymi ilustracjami + współpraca krok po kroku |
| `cennik.html` | Zakładki cennika (każda z własną animacją), kalkulator, FAQ |
| `o-mnie.html` | Cytat, podpis rysujący się na żywo, tekst, zasady pracy |
| `kontakt.html` | Formularz + wizytówka 3D (obraca się, QR do Facebooka, podpis, „Zapisz kontakt”) |
| `luxe-salon.html`, `vesper-barber.html`, `zar-burger.html` | Projekty koncepcyjne |
| `404.html` | Własna strona błędu (GitHub Pages używa jej automatycznie) |
| `assets/css/style.css` | Wygląd wszystkich podstron (jeden plik) |
| `assets/js/app.js` | Przejścia między stronami, tło, animacje, kalkulator, formularz, wizytówka |
| `assets/js/i18n.js` | Wersja angielska (przełącznik PL/EN) |
| `assets/js/lenis.min.js` | Płynne przewijanie myszką (biblioteka Lenis, licencja MIT) |
| `assets/fonts/` | Czcionki (lokalnie — bez Google Fonts) |
| `assets/img/` | Miniatury projektów, ikony, `og.jpg` (podgląd linku na FB/Messengerze) |
| `assets/zar/` | Zdjęcia do strony ŻAR |
| `assets/marcel-struszczak.vcf` | Kontakt do zapisania w telefonie (przycisk „Zapisz kontakt”) |
| `sitemap.xml` | Mapa strony do Google Search Console |

## Wdrożenie na GitHub Pages

1. Cała strona (razem z folderem `assets`) leży już w głównym katalogu repozytorium, stara wersja jednostronicowa jest zastąpiona.
2. Scal gałąź z poprawkami do gałęzi, z której publikuje GitHub Pages (zwykle `main` — widać to w Settings → Pages).
3. Po 1–2 minutach nowa wersja działa pod tym samym adresem.

`gmina-warta.html` (stary projekt) zostaje na serwerze, żeby wcześniej wysłane linki dalej działały — nowe portfolio go nie linkuje.

Stare linki z wersji jednostronicowej (np. `…/marcelgraphic/#kontakt`, `#cennik`, `#kalkulator`) same przekierowują na właściwą podstronę — nic, co już udostępniłeś, się nie zepsuje.

## Jak działają przejścia

- Klik w link do innej podstrony: kurtyna wjeżdża z numerem i nazwą strony docelowej, nowa strona odsłania się spod niej. Dalej w menu = kurtyna z dołu, wstecz = z góry.
- Pasek ładowania to Twój podpis z wizytówki (wygładzona, schludna wersja). Rysuje się od kliknięcia, na nowej stronie dorysowuje się do końca i dopiero wtedy kurtyna się odsuwa.
- Napis na kurtynie stoi w miejscu i ma stały rozmiar przed i po zmianie strony (osobny, osadzony mini-krój — nic się nie doczytuje w trakcie).
- Kurtyna jedzie na karcie graficznej (transform), więc jest płynna także na starszych telefonach.
- Wybór pakietu w cenniku, wynik kalkulatora albo „Chcę taką stronę” przy projekcie przenosi się do formularza w Kontakcie (z krótką notką, co zostało wybrane).
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
- Tytuły pod frazy, które ludzie wpisują: „strony internetowe dla firm”, „tworzenie stron www”, „cennik stron internetowych”, „ile kosztuje strona internetowa”.
- Dane strukturalne (JSON-LD) jako jeden graf: WebSite + firma (ProfessionalService: cennik, obszar działania — Sieradz i 100 km wokół, okoliczne miasta, cała Polska) + Marcel (Person), usługi (Service), proces współpracy (HowTo), FAQ (FAQPage), O mnie, Kontakt, Prace, poradnik (BlogPosting + FAQ), okruszki i daty aktualizacji na każdej stronie.
- **Poradnik** (`poradnik` + 3 artykuły): odpowiedź na górze („W skrócie”), spis treści, tabele, FAQ — format, który Google pokazuje w odpowiedziach, a ChatGPT/Perplexity/Gemini chętnie cytują.
- Osobny obrazek podglądu linku (Facebook, Messenger, WhatsApp) dla każdej podstrony i artykułu: `assets/img/og/`.
- `robots.txt` jawnie wpuszcza roboty wyszukiwarek AI (ChatGPT, Perplexity, Claude, Gemini, Apple, Bing/Copilot).
- `llms.txt` i `llms-full.txt` — wizytówka i pełna treść strony dla asystentów AI (ceny, proces, FAQ, artykuły).
- `sitemap.xml` z obrazami, manifest, meta robots z dużymi podglądami, klucz IndexNow (`963cc2e7ad1b2927af49a2cfbcc214f7.txt`).

**Po Twojej stronie (raz, ok. 30 minut — to daje najwięcej):**
1. **Google Search Console** → dodaj usługę „Domena” `marcelgraphicsite.pl` (weryfikacja rekordem TXT w DNS u rejestratora) → Mapy witryn → zgłoś `sitemap.xml`.
2. **Bing Webmaster Tools** → „Importuj z Google Search Console” (jedno kliknięcie). Z indeksu Binga korzystają ChatGPT (wyszukiwanie), Copilot i DuckDuckGo.
3. **IndexNow** — po każdej większej zmianie otwórz w przeglądarce:
   `https://api.indexnow.org/indexnow?url=https://marcelgraphicsite.pl/&key=963cc2e7ad1b2927af49a2cfbcc214f7`
4. **Wizytówka Google (Profil Firmy w Google)** — załóż jako firma usługowa bez adresu (obszar: Sieradz + okolice + Polska), wpisz stronę `https://marcelgraphicsite.pl`, telefon `+48 511 808 498`, kategorie „Projektant stron WWW” i „Agencja marketingu internetowego”, dodaj zdjęcia. To najważniejszy czynnik w lokalnych wynikach.
5. **Opinie** — poproś pierwszych klientów o opinię w Google (link „Poproś o opinie” z wizytówki).
6. **Te same dane wszędzie** (NAP): nazwa, telefon, strona — w wizytówce Google, na Facebooku, Instagramie, LinkedInie i w katalogach firm (np. Panorama Firm, pkt.pl).
7. **Linki zwrotne**: na każdej stronie zrobionej dla klienta zostaw w stopce „Projekt: Marcel Struszczak” z linkiem do `marcelgraphicsite.pl` (za zgodą klienta).
8. W ustawieniach GitHub Pages zaznacz **Enforce HTTPS**.

**Nowy artykuł w poradniku:** dopisz go w `_zrodla/poradnik_tresc.py` (tytuł, „W skrócie”, treść w Markdown, FAQ), potem uruchom:
`python3 _zrodla/zbuduj_poradnik.py && python3 _zrodla/zbuduj_llms.py && NODE_PATH=$(npm root -g) node _zrodla/zbuduj_og.js`
i dodaj adres do `sitemap.xml` oraz numer/napis kurtyny w `assets/js/app.js` (ORDER/NUMS) i `assets/js/i18n.js` (pages). Folder `_zrodla` nie jest publikowany.

## Formularz

Zgłoszenia z `kontakt.html` idą na `marcel.graphicsite@gmail.com` przez darmowy Web3Forms — bez aktywacji, działa od razu.

- Klucz (`FORM_KEY` w `assets/js/app.js`) jest publiczny z założenia — tak działa Web3Forms. Zmiana adresu odbiorcy: nowy klucz z web3forms.com.
- Temat maila: „… : Imię (Firma)”; „Odpowiedz” trafia prosto do klienta, jeśli podał e-mail.
- Gdyby wysyłka się nie udała (brak sieci itp.), klientowi otwiera się program pocztowy z gotową wiadomością — nic nie przepada.
- Wyłączenie: `FORM_ENDPOINT = ''`.

## Zmiana cen

- `cennik.html` — karty pakietów: atrybuty `data-price`, `data-fb`, `data-fbig`, `data-min`, `data-max` oraz liczba w tekście obok. Kalkulator czyta ceny z tych atrybutów.
- Te same kwoty są też w: odpowiedziach FAQ (`cennik.html` + `assets/js/i18n.js`), cenach „od …” na `index.html` i `uslugi.html` oraz w gotowych wiadomościach „Interesuje mnie pakiet…” (`assets/js/i18n.js`, sekcje `pick` i `pickLabel`).

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
