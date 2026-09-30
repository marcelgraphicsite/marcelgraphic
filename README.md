# Marcel Struszczak — portfolio i oferta (wersja wielostronicowa)

Strona: https://marcelgraphicsite.github.io/marcelgraphic/

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

## Formularz — aktywacja (jednorazowo, 30 sekund)

Formularz wysyła zgłoszenia na `marcel.graphicsite@gmail.com` przez darmowy FormSubmit.

1. Po wdrożeniu wyślij sobie testowe zgłoszenie z `kontakt.html` (z adresu github.io, nie z pliku na dysku).
2. Przyjdzie mail „Activate Form” — kliknij przycisk.
3. Od teraz każde zgłoszenie trafia prosto na skrzynkę.

Zanim formularz jest aktywny, strona otwiera klientowi program pocztowy z gotową wiadomością — nic nie przepada.
Wyłączenie FormSubmit: w `assets/js/app.js` ustaw `FORM_ENDPOINT = ''`.

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
