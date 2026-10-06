# -*- coding: utf-8 -*-
"""Treść poradnika (źródło). Strony HTML buduje zbuduj_poradnik.py.

Każdy artykuł: odpowiedź na górze („W skrócie”), treść w Markdown, FAQ.
Ceny i terminy muszą zgadzać się z cennikiem (cennik.html) — bez zmyślonych statystyk.
"""

DATA = '2026-10-01'          # domyślna data publikacji (pierwsze 3 artykuły)
DATA_TXT = '1 października 2026'
DZIS = '2026-10-06'          # data ostatniej dużej aktualizacji poradnika

# Artykuł może mieć własne 'data' (publikacja) i 'zmiana' (ostatnia aktualizacja) w formacie RRRR-MM-DD.
_ARTYKULY = [
    {
        'slug': 'ile-kosztuje-strona-internetowa',
        'title': 'Ile kosztuje strona internetowa w 2026? Realne ceny dla firm | Marcel Struszczak',
        'og_title': 'Ile kosztuje strona internetowa w 2026 roku?',
        'description': 'Landing od 2 000 zł, strona firmowa od 3 000 zł, sklep wyceniany indywidualnie. Od czego zależy cena strony, jakie są koszty stałe i jak nie przepłacić.',
        'h1': 'Ile kosztuje strona internetowa <em>w 2026 roku?</em>',
        'headline': 'Ile kosztuje strona internetowa w 2026 roku?',
        'lead': 'Krótko: porządna strona dla lokalnej firmy to zwykle wydatek od 2 do kilku tysięcy złotych jednorazowo plus kilkaset złotych rocznie za domenę i hosting. Poniżej rozkładam cenę na czynniki pierwsze — bez marketingowej mgły.',
        'excerpt': 'Realne widełki na rynku, od czego zależy cena, koszty stałe, o których mało kto mówi — i jak nie przepłacić.',
        'og_kicker': 'Poradnik · ceny',
        'keywords': ['ile kosztuje strona internetowa', 'cena strony internetowej', 'koszt strony www dla firmy', 'strona internetowa cennik 2026', 'landing page cena'],
        'tldr': [
            '<strong>Landing page</strong> (jedna strona): od 2 000 zł, gotowa w 4–8 dni.',
            '<strong>Strona wizytówka</strong> (rozbudowana strona firmowa): od 3 000 zł, 7–16 dni.',
            '<strong>Sklep internetowy</strong>: wycena indywidualna, po ustaleniu zakresu.',
            '<strong>Co roku</strong> płacisz tylko za domenę, hosting i SSL — u mnie 200 zł w pierwszym roku, potem 500 zł.',
            '<strong>Cenę podnoszą</strong>: liczba podstron, wersje językowe, indywidualne grafiki, rezerwacje online i ekspresowy termin.',
        ],
        'body': '''
## Ile kosztuje strona internetowa — widełki na rynku

Różnica między „stroną za 500 zł” a „stroną za 15 000 zł” bierze się z tego, kto ją robi i ile pracy w nią wkłada. Najczęściej spotkasz cztery drogi:

| Sposób | Koszt na start | Koszty stałe | Kiedy ma sens |
|---|---|---|---|
| Kreator (Wix, Squarespace, WordPress.com) | 0 zł + Twój czas | abonament, zwykle od kilkudziesięciu zł miesięcznie | masz czas i oko do projektowania |
| Gotowy szablon wdrożony przez kogoś | ok. 500–1 500 zł | domena i hosting | potrzebujesz czegokolwiek „na już” |
| Freelancer — projekt na miarę | ok. 2 000–6 000 zł | domena i hosting, drobne poprawki | mała lub średnia firma lokalna |
| Agencja | zwykle od kilku do kilkunastu tysięcy zł | często abonament za opiekę | większa firma, rozbudowany projekt |

To widełki orientacyjne — rynek jest szeroki, a ostateczna kwota zawsze zależy od zakresu.

## Od czego zależy cena strony

1. **Liczba podstron i sekcji.** Jedna strona z ofertą i kontaktem to inna praca niż serwis z cennikiem, galerią i blogiem. U mnie dodatkowa podstrona kosztuje 300–500 zł.
2. **Projekt na miarę czy szablon.** Szablon jest tańszy, ale Twoja firma wygląda wtedy jak setki innych. Projekt na miarę buduje markę — kolory, zdjęcia i klimat są Twoje.
3. **Teksty i zdjęcia.** Jeśli ich nie masz, ktoś musi je przygotować. Na start często wystarczą zdjęcia z Facebooka lub Instagrama.
4. **Funkcje.** Rezerwacje online, kalendarz wizyt, formularze, sklep i płatności to dodatkowe godziny pracy i testów.
5. **Wersje językowe.** Każdy język to tłumaczenie i dopasowanie układu — u mnie 400–600 zł za język.
6. **Termin.** Ekspresowa realizacja (nawet o połowę szybciej) to +25–50% ceny pakietu.
7. **Widoczność w Google.** Podstawowe SEO — tytuły, opisy, dane dla wyszukiwarek i podpięcie Wizytówki Google — powinno być w cenie każdej strony firmowej. Jeśli ktoś liczy za to osobno, dopytaj, co dokładnie robi.

## Koszty stałe, o których mało kto mówi

Sama strona to wydatek jednorazowy, ale żeby działała, potrzebuje trzech rzeczy opłacanych co roku:

- **Domena** (np. twojafirma.pl) — rejestratorzy kuszą promocją na pierwszy rok, a odnowienie bywa kilka razy droższe. Porównuj cenę odnowienia, nie promocję.
- **Hosting**, czyli miejsce, w którym strona „mieszka”.
- **Certyfikat SSL** — kłódka w przeglądarce. Bez niej przeglądarki ostrzegają, że strona nie jest bezpieczna.

U mnie domena, hosting i SSL to **200 zł za pierwszy rok, a potem 500 zł rocznie**. Domenę rejestruję na Twój e-mail, więc od pierwszego dnia jest w 100% Twoja, a 30 dni przed odnowieniem dostajesz ode mnie przypomnienie. Drobna zmiana poza pakietem (tekst, kolor, zdjęcie) kosztuje 80 zł.

## Ile kosztuje strona u mnie — konkretnie

| Pakiet | Cena | Czas | Co dostajesz |
|---|---|---|---|
| Landing page | od 2 000 zł | 4–8 dni | jedna strona z ofertą i kontaktem, kolory Twojej marki, formularz lub WhatsApp, 2 rundy poprawek |
| Strona wizytówka | od 3 000 zł | 7–16 dni | rozbudowana strona (oferta, o firmie, cennik, FAQ), galeria, mapa, SEO i Wizytówka Google, 5 rund poprawek |
| Strona + sklep | wycena indywidualna | po ustaleniu zakresu | katalog z cenami, koszyk, płatności online (BLIK, karta), szkolenie z obsługi |

Zanim zapłacisz złotówkę, dostajesz **darmowy projekt ze znakiem wodnym**. Zaliczkę (od 40%) wpłacasz dopiero, gdy chcesz iść dalej, a resztę po akceptacji gotowej strony. Płatność można rozłożyć na raty. Wstępną kwotę policzysz w [kalkulatorze wyceny](cennik#kalkulator). Nie wiesz, który pakiet wybrać? Zobacz porównanie [landing page czy strona wizytówka](landing-page-czy-strona-wizytowka).

## Jak nie przepłacić i nie kupić bubla

- **Zapytaj, na kogo będzie zarejestrowana domena.** Powinna być na Ciebie — inaczej przy zmianie wykonawcy możesz ją stracić.
- **Zapytaj o koszty po pierwszym roku.** Niska cena na start bywa nadrabiana drogim abonamentem.
- **Zobacz projekt przed zapłatą.** Dobry wykonawca pokaże, jak strona będzie wyglądać, zanim cokolwiek podpiszesz.
- **Sprawdź stronę na telefonie.** Większość Twoich klientów zobaczy ją właśnie tam.
- **Ustal liczbę poprawek.** Wiedz z góry, ile rund zmian jest w cenie.
- **Uważaj na umowy „na lata” za samą stronę.** Za stronę płaci się raz; co roku — tylko za domenę i hosting.
''',
        'faq': [
            ('Czy da się zrobić stronę internetową za darmo?', 'Tak, w kreatorze — ale płacisz swoim czasem, często abonamentem i efektem „jak z szablonu”. Domena z nazwą Twojej firmy i tak jest płatna.'),
            ('Czy strona internetowa to wydatek jednorazowy?', 'Projekt i wykonanie — tak. Co roku płacisz tylko za domenę, hosting i certyfikat SSL (u mnie 200 zł w pierwszym roku, potem 500 zł rocznie).'),
            ('Ile trwa zrobienie strony internetowej?', 'Landing page 4–8 dni, strona wizytówka 7–16 dni, sklep — po ustaleniu zakresu. Ekspresowa realizacja skraca czas nawet o połowę.'),
            ('Czy mogę zapłacić za stronę w ratach?', 'Tak. Zaliczka od 40% na start, reszta po akceptacji gotowej strony — i tę kwotę możesz rozłożyć na raty.'),
        ],
        'related': ['landing-page-czy-strona-wizytowka', 'strona-internetowa-czy-facebook'],
        'zmiana': DZIS,
        'curtain': ('Ceny stron', 'Ile naprawdę kosztuje strona internetowa w 2026 roku.', 'Site costs', 'What a website really costs in 2026.'),
        'bg': 'cennik',
    },
    {
        'slug': 'strona-internetowa-czy-facebook',
        'title': 'Strona internetowa czy Facebook? Co wybrać dla lokalnej firmy | Marcel Struszczak',
        'og_title': 'Strona internetowa czy Facebook — co wybrać?',
        'description': 'Social media nie zastąpią strony, a strona nie zastąpi social mediów. Za co odpowiada każde z nich, porównanie w tabeli i od czego zacząć przy małym budżecie.',
        'h1': 'Strona internetowa czy Facebook — <em>co wybrać?</em>',
        'headline': 'Strona internetowa czy Facebook — co wybrać dla lokalnej firmy?',
        'lead': 'Najkrótsza odpowiedź: nie „albo”, tylko „i”. Strona nie zastąpi social mediów, a social media nie zastąpią strony — bo każde z nich robi coś zupełnie innego.',
        'excerpt': 'Strona zdobywa nowych klientów, social media zamieniają ich w stałych. Porównanie i plan na mały budżet.',
        'og_kicker': 'Poradnik · strona i social media',
        'keywords': ['strona internetowa czy facebook', 'czy firma potrzebuje strony internetowej', 'facebook zamiast strony', 'social media dla firm', 'strona www dla małej firmy'],
        'tldr': [
            '<strong>Strona pokazuje charakter Twojej firmy nowym klientom</strong> — ktoś szuka w Google i w kilka sekund widzi, kim jesteś, co oferujesz, ile to kosztuje i jak się umówić.',
            '<strong>Social media szlifują więź z tymi, którzy już Cię znają</strong> — przypominasz się, pokazujesz nowości i zachęcasz do powrotu.',
            '<strong>Strona jest Twoja</strong>, a profil należy do platformy, która może zmienić zasady, obciąć zasięgi albo zablokować konto.',
            '<strong>Przy małym budżecie</strong> zacznij od darmowej Wizytówki Google i prostej strony, a social media prowadź regularnie — nawet skromnie.',
        ],
        'body': '''
## Za co odpowiada strona internetowa

Strona to Twoja wizytówka dla ludzi, którzy jeszcze Cię nie znają. Ktoś wpisuje w Google „fryzjer”, „mechanik” albo „kwiaciarnia” i nazwę miasta — i to jest moment, w którym wygrywasz albo przegrywasz klienta.

- **Pierwsze wrażenie.** Klient ocenia firmę w kilka sekund. Dopracowana strona mówi „to poważna firma”, zanim padnie pierwsze słowo.
- **Konkrety w jednym miejscu.** Oferta, ceny, godziny, dojazd i kontakt są zawsze pod ręką — bez przewijania starych postów.
- **Widoczność w Google i asystentach AI.** Strona może pojawiać się na wiele zapytań, a ChatGPT czy Gemini chętnie korzystają z konkretnych informacji z firmowych stron.
- **Własność.** Domena i treści należą do Ciebie. Nikt nie wyłączy Ci strony, bo zmienił regulamin.
- **Bez logowania.** Każdy może ją otworzyć — także ktoś, kto nie ma konta na Facebooku.

## Za co odpowiadają social media

Social media to codzienna rozmowa z ludźmi, którzy już Cię kojarzą: stałymi klientami, znajomymi, sąsiadami.

- **Relacja.** Regularne posty przypominają o Tobie i budują sympatię — ludzie wracają do miejsc, które „znają”.
- **Świeżość.** Nowości, promocje, kulisy pracy, ludzie z zespołu — tu to wszystko żyje.
- **Polecenia.** Udostępnienia i oznaczenia niosą Twoją firmę dalej, do znajomych Twoich klientów.

Ale: o tym, kto zobaczy Twój post, decyduje algorytm, a nie Ty. Wpisy szybko giną w strumieniu, część treści wymaga logowania, a konto może zostać ograniczone lub zablokowane — często bez jasnego powodu.

## Strona i social media — porównanie

| | Strona internetowa | Facebook / Instagram |
|---|---|---|
| Główne zadanie | zdobywa nowych klientów | utrzymuje relację ze stałymi |
| Kto tam trafia | ludzie szukający usługi w Google | ludzie, którzy Cię obserwują lub zobaczą udostępnienie |
| Kontrola | pełna — Twoja domena, Twoje zasady | platforma decyduje o zasięgu i regulaminie |
| Oferta i ceny | zawsze pod ręką | giną w starszych postach |
| Koszt | jednorazowy projekt + domena i hosting | Twój czas albo miesięczne prowadzenie |
| Widoczność w Google | na wiele zapytań | ograniczona |

## Czy firma może działać tylko na Facebooku?

Może — zwłaszcza na samym początku. Tracisz jednak dużą część klientów, którzy szukają usług w Google i nigdy nie trafią na Twój profil. Uzależniasz się też od jednej platformy: jeśli zmieni zasady albo zablokuje konto, znikasz z dnia na dzień.

Jeśli nie masz jeszcze strony, minimum to **Wizytówka Google** (Profil Firmy w Google) — jest darmowa i pokazuje Cię w Mapach oraz w lokalnych wynikach wyszukiwania ([jak ją założyć krok po kroku](jak-zalozyc-wizytowke-google)). Strona to naturalny kolejny krok: wizytówka kieruje do niej ludzi, a strona zamienia ich w klientów.

## Od czego zacząć przy małym budżecie

1. **Wizytówka Google.** Załóż ją i uzupełnij: godziny, zdjęcia, opis, numer telefonu. Zbieraj opinie od pierwszego dnia — [tu piszę, jak to robić](jak-zdobyc-opinie-google).
2. **Prosta strona.** Na start wystarczy landing page z ofertą, cenami i kontaktem. Podepnij go pod Wizytówkę Google i profile w social mediach.
3. **Regularne social media.** Lepiej dwa dobre posty tygodniowo przez cały rok niż dziesięć w jednym tygodniu, a potem cisza przez miesiąc.
4. **Spójność.** Te same dane kontaktowe, logo i kolory wszędzie — klient od razu wie, że to wciąż Ty.

Najlepiej działa duet: **strona zdobywa nowych klientów, a social media zamieniają ich w stałych.** Jeśli chcesz wiedzieć, ile kosztuje taki start, zajrzyj do artykułu [ile kosztuje strona internetowa](ile-kosztuje-strona-internetowa).
''',
        'faq': [
            ('Czy strona jest potrzebna, jeśli mam dużo obserwujących?', 'Tak. Obserwujący to w większości ludzie, którzy już Cię znają. Nowi klienci szukają w Google — a tam profil w social mediach przegrywa ze stroną i Wizytówką Google.'),
            ('Czy social media pomagają w pozycjonowaniu strony?', 'Pośrednio. Same posty nie podnoszą pozycji strony w Google, ale budują rozpoznawalność, a link do strony w profilu kieruje do niej ruch.'),
            ('Co jest ważniejsze na start — strona czy social media?', 'Jeśli zależy Ci na nowych klientach: Wizytówka Google i prosta strona. Social media dołóż, żeby utrzymać relację z tymi, którzy już przyszli.'),
            ('Czy mogę zlecić stronę i prowadzenie social mediów jednej osobie?', 'Tak — projektuję strony i prowadzę Facebooka oraz Instagrama dla firm, więc wszystko jest spójne. Prowadzenie social mediów zaczyna się od 600 zł miesięcznie.'),
        ],
        'related': ['jak-zalozyc-wizytowke-google', 'ile-kosztuje-strona-internetowa'],
        'zmiana': DZIS,
        'curtain': ('Strona czy FB', 'Co wybrać dla lokalnej firmy — i dlaczego oba.', 'Site vs FB', 'What a local business needs — and why both.'),
        'bg': 'uslugi',
    },
    {
        'slug': 'jak-zdobyc-opinie-google',
        'title': 'Jak zdobyć więcej opinii Google? 7 sposobów dla lokalnej firmy | Marcel Struszczak',
        'og_title': 'Jak zdobyć więcej opinii w Google? 7 sposobów',
        'description': 'Opinie w Google decydują, czy klient wybierze Ciebie, czy konkurencję. 7 prostych sposobów: link do opinii, kod QR, karta NFC, odpowiedzi na opinie — i czego nie robić.',
        'h1': 'Jak zdobyć więcej opinii <em>w Google?</em>',
        'headline': 'Jak zdobyć więcej opinii w Google? 7 sposobów dla lokalnej firmy',
        'lead': 'Zadowoleni klienci chętnie zostawiają opinie — pod warunkiem, że poprosisz ich we właściwym momencie, a cała sprawa zajmie im kilka sekund. Oto 7 sposobów, które to załatwiają.',
        'excerpt': 'Kiedy prosić, jak skrócić drogę do opinii (link, QR, NFC), jak odpowiadać — i czego nigdy nie robić.',
        'og_kicker': 'Poradnik · opinie Google',
        'keywords': ['jak zdobyć opinie google', 'opinie google dla firmy', 'karta nfc opinie google', 'link do opinii google', 'jak poprosić klienta o opinię'],
        'tldr': [
            '<strong>Proś zawsze i osobiście</strong> — najlepiej tuż po udanej usłudze, gdy klient jest zadowolony.',
            '<strong>Skróć drogę do zera</strong>: bezpośredni link, kod QR albo karta NFC, która od razu otwiera okno opinii.',
            '<strong>Odpowiadaj na każdą opinię</strong>, także krytyczną — czytają to przyszli klienci.',
            '<strong>Nie kupuj opinii i nie dawaj nic w zamian</strong> — to łamie zasady Google i polskie prawo.',
        ],
        'body': '''
## Dlaczego opinie w Google są tak ważne

Opinie widać przy Twojej firmie w wynikach wyszukiwania i w Mapach Google — często zanim ktokolwiek wejdzie na Twoją stronę. Dla klienta to najszybszy test: „czy inni byli zadowoleni?”.

Google sam podaje, że liczba i ocena opinii wpływają na to, jak wysoko firma pojawia się w wynikach lokalnych. Więcej dobrych opinii to więcej osób, które Cię zobaczą — i chętniej wybiorą Ciebie niż konkurencję.

## 7 sposobów na więcej opinii

### 1. Poproś osobiście — we właściwym momencie

Najlepszy moment to chwila, w której klient jest zadowolony: koniec udanej wizyty, odbiór zamówienia, podziękowanie. Wystarczy jedno zdanie: „Jeśli było dobrze, będę wdzięczny za opinię w Google — to bardzo pomaga małej firmie”.

### 2. Wyślij bezpośredni link do opinii

W Profilu Firmy w Google znajdziesz opcję „Poproś o opinie” — skopiuj link i wysyłaj go SMS-em, w wiadomości albo w mailu po wizycie. Klient klika i od razu widzi okno z gwiazdkami.

### 3. Postaw kod QR tam, gdzie klient czeka

Kod QR z linkiem do opinii na ladzie, stoliku, paragonie albo ulotce. Klient skanuje go telefonem w kilka sekund — najlepiej w chwili, gdy i tak na coś czeka.

### 4. Użyj karty lub naklejki NFC

Klient przykłada telefon do karty i od razu otwiera się okno opinii Twojej firmy — bez aplikacji, bez szukania i bez skanowania. Działa na większości współczesnych smartfonów: iPhone’y od modelu XS odczytują NFC bez aplikacji, a na Androidzie wystarczy włączone NFC. Jedna uwaga: NFC nie działa na metalu, więc kartę stawia się na ladzie lub stoliku, a naklejkę na szybie lub drzwiach. Jak to działa w praktyce i ile kosztuje, opisuję na stronie [karty NFC do opinii Google](karty-nfc-opinie-google).

### 5. Dodaj prośbę w stałych miejscach

Stopka maila, potwierdzenie rezerwacji, strona internetowa, wizytówka, paragon — wszędzie tam jedno zdanie i link „Oceń nas w Google” przypominają o opinii bez Twojego udziału.

### 6. Odpowiadaj na każdą opinię

Podziękuj za pozytywne, a na krytyczne odpowiedz spokojnie i rzeczowo: przeproś, wyjaśnij, zaproponuj rozwiązanie. Przyszli klienci czytają odpowiedzi — dobra reakcja na krytykę buduje więcej zaufania niż same piątki.

### 7. Zadbaj o samą wizytówkę

Aktualne godziny, prawdziwe zdjęcia, opis i numer telefonu. Kompletna, zadbana wizytówka wygląda wiarygodnie — a klient chętniej zostawia opinię firmie, która dba o szczegóły.

## Czego nie robić

- **Nie kupuj opinii i nie pisz ich sam.** Fałszywe opinie łamią zasady Google, a w Polsce od 2023 roku są wprost zakazane jako nieuczciwa praktyka rynkowa.
- **Nie dawaj nic w zamian za opinię.** Rabat czy prezent za recenzję jest niezgodny z zasadami Google.
- **Nie proś tylko zadowolonych.** Wybiórcze zbieranie samych pozytywnych opinii też jest zabronione przez Google.
- **Nie zbieraj opinii hurtowo.** Wiele opinii naraz z jednego miejsca może zostać odfiltrowanych jako podejrzane.

## Ile opinii potrzebujesz?

Nie ma magicznej liczby. Liczy się regularność i świeżość: lepiej kilka nowych opinii co miesiąc niż trzydzieści naraz, a potem cisza przez rok. Klienci patrzą też na daty — świeże opinie mówią, że firma działa i dba o jakość dziś.

Opinie to tylko jeden element widoczności lokalnej firmy. Jeśli zastanawiasz się, czy do tego potrzebna jest strona, przeczytaj [strona internetowa czy Facebook — co wybrać](strona-internetowa-czy-facebook).
''',
        'faq': [
            ('Jak znaleźć link do opinii mojej firmy w Google?', 'Zaloguj się na konto, na którym masz Profil Firmy w Google, wyszukaj nazwę swojej firmy i wybierz „Poproś o opinie”. Dostaniesz krótki link, który możesz wysyłać klientom albo zamienić w kod QR.'),
            ('Czy można usunąć negatywną opinię w Google?', 'Nie samodzielnie. Możesz zgłosić opinię, która łamie zasady Google (np. spam, obraźliwe treści albo opinia o innej firmie). W pozostałych przypadkach najlepsze, co możesz zrobić, to rzeczowo odpowiedzieć.'),
            ('Czy karta NFC do opinii działa na każdym telefonie?', 'Na większości współczesnych smartfonów tak: iPhone od modelu XS odczytuje ją bez aplikacji, a na Androidzie NFC musi być włączone. Dla telefonów bez NFC warto mieć obok kod QR.'),
            ('Ile kosztuje karta NFC do opinii Google?', 'U mnie karta NFC z podstawką kosztuje 60 zł, a duża naklejka NFC 80 zł — każdą programuję pod profil Twojej firmy. Wysyłam w całej Polsce.'),
        ],
        'related': ['jak-zalozyc-wizytowke-google', 'czy-twoja-firma-jest-widoczna-w-google'],
        'zmiana': DZIS,
        'curtain': ('Opinie Google', '7 sposobów na więcej opinii dla lokalnej firmy.', 'Reviews', '7 ways to get more Google reviews.'),
        'bg': 'kontakt',
    },
]

_NOWE = [
    {
        'slug': 'landing-page-czy-strona-wizytowka',
        'data': DZIS,
        'title': 'Landing page czy strona wizytówka — co wybrać? | Marcel Struszczak',
        'og_title': 'Landing page czy strona wizytówka — co wybrać?',
        'description': 'Landing page to jedna strona z jednym celem, strona wizytówka to pełna strona firmowa. Porównanie: cena, czas, SEO i dla kogo — oraz kiedy zacząć od landingu.',
        'h1': 'Landing page czy strona wizytówka — <em>co wybrać?</em>',
        'headline': 'Landing page czy strona wizytówka — co wybrać dla firmy?',
        'lead': 'Najkrótsza odpowiedź: landing, jeśli masz jedną główną usługę i chcesz szybko wystartować. Wizytówka, jeśli masz kilka usług i chcesz być widoczny w Google na więcej zapytań. Poniżej różnice w liczbach.',
        'excerpt': 'Jedna strona z jednym celem czy pełna strona firmowa? Porównanie ceny, czasu realizacji i widoczności w Google.',
        'og_kicker': 'Poradnik · rodzaje stron',
        'keywords': ['landing page czy strona wizytówka', 'co to jest landing page', 'strona wizytówka co to', 'landing page cena',
                     'strona one page czy wielostronicowa', 'jaka strona dla małej firmy'],
        'tldr': [
            '<strong>Landing page</strong> = jedna strona z jednym celem (telefon, zapis, zamówienie). U mnie od 2 000 zł, 4–8 dni.',
            '<strong>Strona wizytówka</strong> = pełna strona firmowa: oferta, o firmie, cennik, FAQ, galeria, mapa. Od 3 000 zł, 7–16 dni.',
            '<strong>W Google lepiej radzi sobie wizytówka</strong> — więcej treści to więcej zapytań, na które możesz się pokazać.',
            '<strong>Landing sprawdza się</strong> przy reklamach, jednej usłudze i starcie z małym budżetem.',
            '<strong>Landing możesz później rozbudować</strong> — dodatkowa podstrona kosztuje u mnie 300–500 zł.',
        ],
        'body': '''
## Czym jest landing page

Landing page (strona docelowa) to **jedna strona z jednym zadaniem**. Klient trafia na nią z reklamy, z Instagrama albo z Google i ma zrobić jedną rzecz: zadzwonić, zapisać się albo zamówić. Wszystko inne — menu z pięcioma zakładkami, blog, długa historia firmy — tylko by rozpraszało.

Typowy landing to kilka sekcji jedna pod drugą: mocny nagłówek, oferta, korzyści, opinie, kontakt. W moim pakiecie Landing dostajesz stronę z ofertą i kontaktem na gotowym szablonie dopasowanym do kolorów Twojej marki, formularz albo link do WhatsAppa i 2 rundy poprawek.

## Czym jest strona wizytówka

Strona wizytówka to **pełna strona firmowa**. Pokazuje całą ofertę, opowiada o firmie i odpowiada na pytania, zanim klient je zada. Ma więcej sekcji — ofertę, o firmie, cennik, FAQ, galerię, mapę — i nawigację, która od razu prowadzi tam, gdzie klient chce.

W moim pakiecie Wizytówka dostajesz indywidualny projekt graficzny, animacje przy przewijaniu, galerię, mapę Google, podstawowe SEO z podpięciem Wizytówki Google i 5 rund poprawek. Stronę można rozbudować o kolejne podstrony.

## Landing page czy wizytówka — porównanie

| | Landing page | Strona wizytówka |
|---|---|---|
| Cel | jedna akcja: telefon, zapis, zamówienie | przedstawia całą firmę i ofertę |
| Zawartość | nagłówek, oferta, kontakt | oferta, o firmie, cennik, FAQ, galeria, mapa |
| Projekt graficzny | szablon w kolorach Twojej marki | indywidualny |
| Cena u mnie | od 2 000 zł | od 3 000 zł |
| Czas realizacji | 4–8 dni | 7–16 dni |
| Poprawki w cenie | 2 rundy | 5 rund |
| Widoczność w Google | podstawowa | szersza: SEO i Wizytówka Google |

## Kiedy wybrać landing page

- **Masz jedną główną usługę** — np. food truck, korepetycje, montaż klimatyzacji.
- **Puszczasz reklamy** na Facebooku albo w Google i potrzebujesz strony, która zamienia kliknięcia w zapytania.
- **Startujesz z małym budżetem** i chcesz być w sieci w kilka dni.
- **Testujesz nowy pomysł** i nie wiesz jeszcze, czy wypali.

## Kiedy wybrać stronę wizytówkę

- **Masz kilka usług** i każda zasługuje na własne miejsce.
- **Chcesz, żeby klienci znajdowali Cię w Google** — więcej treści to więcej zapytań, na które możesz się pokazać.
- **Klienci porównują Cię z konkurencją** — potrzebujesz galerii, cennika i odpowiedzi na pytania.
- **Budujesz markę na lata**, a nie jedną kampanię.

## Wizytówka Google to nie strona wizytówka

To częsta pomyłka. **Wizytówka Google** (Profil Firmy w Google) to darmowy wpis w Mapach i w wynikach Google. **Strona wizytówka** to Twoja własna strona internetowa. Potrzebujesz obu: wizytówka sprowadza klienta, a strona przekonuje go do wyboru. Jak założyć tę pierwszą, opisuję w poradniku [Wizytówka Google krok po kroku](jak-zalozyc-wizytowke-google).

## A może od razu sklep?

Jeśli chcesz sprzedawać online — produkty, bony podarunkowe, zamówienia z płatnością BLIK lub kartą — potrzebujesz strony ze sklepem. Wyceniam ją indywidualnie, po rozmowie o zakresie.

## Jak zdecydować w 3 pytaniach

1. **Ile masz usług?** Jedna — landing. Kilka — wizytówka.
2. **Skąd mają przychodzić klienci?** Z reklam — landing. Z Google — wizytówka.
3. **Ile masz czasu i budżetu?** Mało — landing teraz, rozbudowa później. Więcej — od razu wizytówka.

Nadal nie wiesz? Napisz — doradzę po krótkiej rozmowie, a darmowy projekt pokaże Ci, jak to będzie wyglądać. Ceny i dodatki sprawdzisz w [cenniku](cennik#www), a pełny obraz kosztów w artykule [ile kosztuje strona internetowa](ile-kosztuje-strona-internetowa).
''',
        'faq': [
            ('Czy landing page jest dobry do SEO?', 'Pod jedno konkretne hasło — tak. Ale strona z jednym tematem pokaże się na mniej zapytań niż rozbudowana strona firmowa. Jeśli zależy Ci na klientach z Google, lepsza będzie strona wizytówka.'),
            ('Czy z landing page można później zrobić stronę wizytówkę?', 'Tak. Landing możesz rozbudować o kolejne sekcje i podstrony — u mnie dodatkowa podstrona kosztuje 300–500 zł.'),
            ('Czym różni się strona wizytówka od Wizytówki Google?', 'Strona wizytówka to Twoja własna strona internetowa. Wizytówka Google (Profil Firmy w Google) to darmowy wpis w Mapach i wynikach Google. Najlepiej mieć jedno i drugie.'),
            ('Ile kosztuje landing page, a ile strona wizytówka?', 'U mnie landing page kosztuje od 2 000 zł (4–8 dni), a strona wizytówka od 3 000 zł (7–16 dni). Do tego domena, hosting i SSL: 200 zł w pierwszym roku, potem 500 zł rocznie.'),
        ],
        'related': ['ile-kosztuje-strona-internetowa', 'jak-zalozyc-wizytowke-google'],
        'curtain': ('Landing czy wizytówka', 'Którą stronę wybrać dla swojej firmy.', 'Landing or showcase', 'Which website fits your business.'),
        'bg': 'cennik',
    },
    {
        'slug': 'jak-zalozyc-wizytowke-google',
        'data': DZIS,
        'title': 'Jak założyć Wizytówkę Google? Krok po kroku (2026) | Marcel Struszczak',
        'og_title': 'Jak założyć Wizytówkę Google — krok po kroku',
        'description': 'Załóż darmowy Profil Firmy w Google: nazwa, kategoria, adres lub obszar działania i weryfikacja wideo. Krok po kroku — i błędy, przez które wizytówka znika.',
        'h1': 'Jak założyć Wizytówkę Google — <em>krok po kroku</em>',
        'headline': 'Jak założyć Wizytówkę Google (Profil Firmy w Google) — krok po kroku',
        'lead': 'Wizytówka Google — dziś oficjalnie Profil Firmy w Google, dawniej Google Moja Firma — to darmowy wpis, dzięki któremu Twoja firma pojawia się w Mapach i w lokalnych wynikach wyszukiwania. Założysz ją w kwadrans, weryfikacja trwa dłużej. Oto cała droga.',
        'excerpt': 'Nazwa, kategoria, obszar działania i weryfikacja wideo — jak założyć Profil Firmy w Google i nie dać się zawiesić.',
        'og_kicker': 'Poradnik · Wizytówka Google',
        'keywords': ['jak założyć wizytówkę google', 'wizytówka google', 'profil firmy w google', 'google moja firma',
                     'weryfikacja wizytówki google', 'wizytówka google bez adresu'],
        'tldr': [
            '<strong>Wizytówka jest darmowa</strong> — zakładasz ją na stronie google.com/business, na swoim koncie Google.',
            '<strong>Nazwa musi być prawdziwa</strong> — bez dopisków w stylu „najlepszy fryzjer Sieradz”.',
            '<strong>Dojeżdżasz do klientów?</strong> Ukryj adres i ustaw obszar działania (do 20 miejscowości).',
            '<strong>Weryfikacja:</strong> Google sam wybiera metodę — często to krótkie nagranie wideo, sprawdzane do 5 dni roboczych.',
            '<strong>Po weryfikacji</strong> uzupełnij godziny, zdjęcia, opis i usługi — i zbieraj opinie od pierwszego dnia.',
        ],
        'body': '''
## Co daje Wizytówka Google

Kiedy ktoś wpisuje „mechanik Sieradz” albo „fryzjer w pobliżu”, Google pokazuje mapkę z kilkoma firmami. To właśnie wizytówki. Klient widzi w nich od razu:

- nazwę, kategorię i opinie,
- godziny otwarcia i numer telefonu z przyciskiem „Zadzwoń”,
- trasę dojazdu albo obszar, w którym działasz,
- zdjęcia, usługi i link do Twojej strony.

Wizytówka jest **darmowa**, a dla wielu lokalnych firm to najważniejsze miejsce w całym internecie. Uważaj na telefony „z Google” z ofertą płatnej weryfikacji albo „pozycjonowania wizytówki” — Google nie pobiera opłat za Profil Firmy.

## Zanim zaczniesz — przygotuj

- **Konto Google** — najlepiej osobne, firmowe, do którego zawsze będziesz mieć dostęp.
- **Nazwę firmy** — dokładnie taką, jakiej używasz na szyldzie, wizytówkach i dokumentach.
- **Kategorię główną** — jak najbardziej konkretną, np. „Pizzeria”, a nie „Restauracja”.
- **Adres albo obszar działania** — w zależności od tego, czy klienci przychodzą do Ciebie.
- **Telefon i adres strony internetowej.**
- **Kilka zdjęć** — logo, wnętrze, efekty pracy, zespół.

## Jak założyć Wizytówkę Google — krok po kroku

1. **Wejdź na google.com/business** i zaloguj się na konto Google.
2. **Wpisz nazwę firmy.** Jeśli Google podpowie, że taka firma już jest w Mapach, nie zakładaj drugiej wizytówki — poproś o dostęp do istniejącej.
3. **Wybierz kategorię główną.** Kolejne kategorie dodasz później.
4. **Zdecyduj o lokalizacji.** Jeśli klienci przychodzą do Ciebie (sklep, salon, lokal), wpisz adres i sprawdź pinezkę na mapie. Jeśli to Ty jeździsz do klientów, nie pokazuj adresu i ustaw **obszar działania**: miasta albo kody pocztowe, maksymalnie 20 pozycji, najdalej mniej więcej 2 godziny jazdy od siedziby.
5. **Podaj telefon i adres strony.**
6. **Zweryfikuj firmę.** Google sam wybiera metodę — często jest to nagranie wideo, czasem telefon, SMS albo e-mail.
7. **Uzupełnij profil** — o tym niżej.

## Weryfikacja wideo — jak ją przejść

Jeśli Google poprosi o wideo, nagrywasz je telefonem jednym ujęciem — bez cięć i montażu, co najmniej 30 sekund. Na nagraniu pokaż:

- **gdzie jesteś** — ulicę, numer budynku, pobliskie znaki albo punkty orientacyjne;
- **że firma istnieje** — szyld, wnętrze, sprzęt albo narzędzia pracy;
- **że to Ty nią zarządzasz** — np. zaplecze, kasę, otwieranie lokalu albo dokumenty firmy (bez numerów kont i danych osobowych).

Nie nagrywaj twarzy innych osób. Google sprawdza nagranie do 5 dni roboczych.

## Co uzupełnić po weryfikacji

- **Godziny otwarcia** — także godziny specjalne w święta.
- **Opis firmy** (do 750 znaków) — konkretnie: co robisz, dla kogo i gdzie. Bez wykrzykników i pisania wielkimi literami.
- **Usługi albo produkty** — z krótkim opisem, a jeśli możesz, z ceną.
- **Zdjęcia** — logo, zdjęcie w tle, wnętrze, zespół, efekty pracy. Dodawaj nowe regularnie.
- **Link do strony, menu albo rezerwacji.**
- **Dodatkowe kategorie** — tylko te, które naprawdę pasują.

## Błędy, przez które wizytówka może zostać zawieszona

- **Dopiski w nazwie** — np. „Salon Ania — fryzjer Sieradz tanio”. Nazwa ma być taka jak w rzeczywistości.
- **Adres wirtualny, skrytka pocztowa albo cudzy lokal.**
- **Firma działająca wyłącznie online** — Profil Firmy jest dla firm, które spotykają się z klientami.
- **Duże zmiany zaraz po weryfikacji** — nowa nazwa, adres czy kategoria mogą wymusić ponowną weryfikację.
- **Dwie wizytówki tej samej firmy.**
- **Kupowanie opinii albo nagradzanie za opinie.**

## Co dalej: jak wypaść lepiej niż konkurencja

1. **Zbieraj opinie od pierwszego dnia** i odpowiadaj na każdą — [7 sposobów na więcej opinii](jak-zdobyc-opinie-google), w tym [karty NFC do opinii](karty-nfc-opinie-google).
2. **Dodawaj zdjęcia i aktualności** — pokazują, że firma działa.
3. **Podepnij stronę internetową** z tymi samymi danymi co w wizytówce: nazwa, adres, telefon. Wizytówka sprowadza klienta, a strona przekonuje go do wyboru.
4. **Sprawdź efekt** — [test widoczności w Google w 10 minut](czy-twoja-firma-jest-widoczna-w-google).
''',
        'faq': [
            ('Ile kosztuje Wizytówka Google?', 'Nic — Profil Firmy w Google jest darmowy. Jeśli ktoś dzwoni „z Google” i chce pieniędzy za założenie albo weryfikację wizytówki, to nie jest Google.'),
            ('Ile trwa weryfikacja wizytówki?', 'To zależy od metody. Nagranie wideo Google sprawdza do 5 dni roboczych; weryfikacja telefonem, SMS-em albo e-mailem bywa szybsza.'),
            ('Czy mogę założyć wizytówkę bez adresu?', 'Tak, jeśli dojeżdżasz do klientów — wtedy ukrywasz adres i ustawiasz obszar działania. Firmy działające wyłącznie online nie mogą mieć Profilu Firmy w Google.'),
            ('Czym różni się Wizytówka Google od strony wizytówki?', 'Wizytówka Google to darmowy profil firmy w Mapach i wynikach Google. Strona wizytówka to Twoja własna strona internetowa. Najlepiej działają razem.'),
            ('Czy pomożesz mi z wizytówką?', 'Tak. W pakiecie Wizytówka podpinam stronę do Twojego Profilu Firmy w Google i pomagam go uzupełnić. Jeśli wizytówki jeszcze nie masz, przeprowadzę Cię przez jej założenie.'),
        ],
        'related': ['jak-zdobyc-opinie-google', 'czy-twoja-firma-jest-widoczna-w-google'],
        'curtain': ('Wizytówka Google', 'Profil Firmy w Google krok po kroku.', 'Google profile', 'Google Business Profile, step by step.'),
        'bg': 'kontakt',
    },
    {
        'slug': 'czy-twoja-firma-jest-widoczna-w-google',
        'data': DZIS,
        'title': 'Czy Twoja firma jest widoczna w Google? Test w 10 minut | Marcel Struszczak',
        'og_title': 'Czy Twoja firma jest widoczna w Google? Test w 10 minut',
        'description': 'Sprawdź, czy klienci znajdą Twoją firmę: wyszukiwarka, Mapy, opinie, strona na telefonie i asystenci AI. 8 kroków, które zrobisz na telefonie w 10 minut.',
        'h1': 'Czy Twoja firma jest widoczna <em>w Google?</em>',
        'headline': 'Czy Twoja firma jest widoczna w Google? Test w 10 minut',
        'lead': 'Zrób ten test na telefonie — tak, jak robią to Twoi klienci. Zajmie 10 minut i pokaże, gdzie tracisz klientów: w wyszukiwarce, w Mapach czy w odpowiedziach asystentów AI.',
        'excerpt': '8 kroków na telefonie: wyszukiwarka, Mapy, opinie, strona i asystenci AI. Zobacz, gdzie tracisz klientów.',
        'og_kicker': 'Poradnik · widoczność',
        'keywords': ['jak sprawdzić widoczność firmy w google', 'czy moja firma jest w google', 'pozycja firmy w google',
                     'jak sprawdzić czy strona jest zaindeksowana', 'firma w mapach google', 'firma w chatgpt'],
        'tldr': [
            '<strong>Szukaj jak klient:</strong> na telefonie, w karcie incognito — „usługa + miasto”.',
            '<strong>Sprawdź mapkę z firmami</strong> nad wynikami — to najcenniejsze miejsce w lokalnym Google.',
            '<strong>Wpisz nazwę swojej firmy:</strong> czy widać wizytówkę, godziny, telefon, stronę i opinie?',
            '<strong>Zapytaj ChatGPT, Gemini albo Perplexity</strong>, kogo polecają w Twojej branży i Twoim mieście.',
            '<strong>Każdy krok, którego nie przejdziesz,</strong> to klienci, którzy dziś wybierają konkurencję.',
        ],
        'body': '''
## Zanim zaczniesz

- **Użyj telefonu** — większość Twoich klientów szuka właśnie na nim.
- **Otwórz kartę incognito** (prywatną). Google dopasowuje wyniki do Twojej historii, więc na zwykłej karcie możesz widzieć swoją firmę wyżej niż klienci.
- **Bądź w swoim mieście** albo dopisuj jego nazwę do zapytań. Wyniki lokalne zależą od tego, gdzie jesteś.

## Test w 8 krokach

### 1. Wpisz usługę i miasto

Na przykład „fryzjer Sieradz”, „pizza Zduńska Wola” albo „mechanik Łask”. Czy jesteś na pierwszej stronie wyników? Zapisz trzy firmy, które widać najwyżej — to Twoja realna konkurencja.

### 2. Sprawdź mapkę z firmami

Nad zwykłymi wynikami Google często pokazuje mapkę z kilkoma firmami. To najcenniejsze miejsce w lokalnych wynikach. Jeśli Cię tam nie ma, kliknij „Więcej firm” i sprawdź, na którym miejscu jesteś.

### 3. Wpisz „[usługa] w pobliżu”

Tak szuka wielu klientów, zwłaszcza gdy są już w drodze. Ten wynik zależy głównie od Wizytówki Google: kategorii, opinii i odległości.

### 4. Wpisz nazwę swojej firmy

Powinna pojawić się Twoja wizytówka: nazwa, kategoria, godziny, telefon, strona i zdjęcia. Sprawdź, czy wszystko jest aktualne. Jeśli wizytówki nie ma — [załóż ją krok po kroku](jak-zalozyc-wizytowke-google).

### 5. Sprawdź opinie

Ile ich masz, jaka jest średnia, kiedy pojawiła się ostatnia i czy na nie odpowiadasz. Porównaj to z trzema firmami z kroku 1. Jeśli wypadasz słabiej — [7 sposobów na więcej opinii](jak-zdobyc-opinie-google).

### 6. Otwórz swoją stronę na telefonie

Czy ładuje się szybko? Czy w kilka sekund widać, co robisz, ile to kosztuje i jak się skontaktować? Czy numer telefonu da się kliknąć? Szybkość sprawdzisz za darmo w narzędziu PageSpeed Insights (pagespeed.web.dev).

### 7. Sprawdź, czy Google zna Twoją stronę

Wpisz w Google `site:twojafirma.pl` (z adresem swojej strony). Jeśli nie ma żadnych wyników, Google nie zaindeksował strony i nikt jej nie znajdzie. Rozwiązanie: dodaj stronę do Google Search Console i zgłoś mapę witryny.

### 8. Zapytaj asystenta AI

Coraz więcej osób pyta ChatGPT, Gemini albo Perplexity, zamiast przeglądać wyniki. Zapytaj: „Polecisz [usługę] w [mieście]?”. Asystenci budują odpowiedź z tego, co znajdą w sieci: stron firm, map, opinii i katalogów. Jeśli Cię nie wymieniają, zwykle brakuje im konkretów — strony z ofertą i miastem, kompletnej wizytówki albo opinii.

## Wynik: co poprawić najpierw

| Problem | Co zrobić |
|---|---|
| Nie ma Cię w mapce z firmami | załóż albo uzupełnij Wizytówkę Google |
| Masz mniej opinii niż konkurencja | proś o opinię po każdej usłudze: link, kod QR albo karta NFC |
| Wpis `site:` nie pokazuje Twojej strony | dodaj stronę do Google Search Console i zgłoś mapę witryny |
| Strona jest wolna albo nieczytelna na telefonie | nowa, lekka strona projektowana najpierw na telefon |
| W różnych miejscach są różne dane | ujednolić nazwę, adres i telefon wszędzie |
| Asystenci AI Cię nie znają | strona z konkretami (oferta, ceny, miasto), wizytówki w Google i Bing, wpisy w katalogach firm |

## Najważniejsze na koniec

Widoczność w Google to nie jeden trik, tylko trzy rzeczy, które działają razem: **Wizytówka Google, opinie i dobra strona**. Jeśli test wypadł słabo, zacznij od wizytówki (jest darmowa), a potem zadbaj o stronę. Chcesz zobaczyć, jak mogłaby wyglądać Twoja nowa strona? [Napisz do mnie](kontakt) — przygotuję darmowy projekt.
''',
        'faq': [
            ('Dlaczego widzę swoją firmę wysoko w Google, a klienci nie?', 'Google dopasowuje wyniki do historii wyszukiwania i lokalizacji. Ty często odwiedzasz swoją stronę, więc widzisz ją wyżej. Sprawdzaj w karcie incognito i na innym telefonie.'),
            ('Ile czasu potrzeba, żeby nowa strona pojawiła się w Google?', 'Zwykle od kilku dni do kilku tygodni. Przyspieszysz to, dodając stronę do Google Search Console i zgłaszając mapę witryny.'),
            ('Czy płatne reklamy Google poprawiają pozycję w bezpłatnych wynikach?', 'Nie. Reklamy i wyniki bezpłatne działają osobno — reklama znika razem z budżetem, a pozycję w bezpłatnych wynikach budują strona, Wizytówka Google i opinie.'),
            ('Jak za darmo sprawdzić pozycję mojej strony w Google?', 'W Google Search Console, w raporcie „Skuteczność”. Zobaczysz tam zapytania, na które pokazuje się Twoja strona, liczbę kliknięć i średnią pozycję.'),
            ('Jak sprawdzić, czy ChatGPT zna moją firmę?', 'Zapytaj go o polecenie firmy z Twojej branży w Twoim mieście, a potem wprost o Twoją firmę. Jeśli odpowiedzi są puste albo błędne, zadbaj o stronę z konkretami, wizytówki w Google i Bing oraz wpisy w katalogach firm.'),
        ],
        'related': ['jak-zalozyc-wizytowke-google', 'jak-zdobyc-opinie-google'],
        'curtain': ('Widoczność', 'Test widoczności firmy w Google w 10 minut.', 'Visibility', 'A 10-minute Google visibility test.'),
        'bg': 'index',
    },
    {
        'slug': 'strona-internetowa-dla-restauracji',
        'data': DZIS,
        'title': 'Strona internetowa dla restauracji — co musi mieć? | Marcel Struszczak',
        'og_title': 'Strona internetowa dla restauracji — co musi mieć?',
        'description': 'Menu jako tekst, godziny, mapa, zamówienia i rezerwacje, prawdziwe zdjęcia. 10 rzeczy, które musi mieć strona restauracji, żeby goście wybierali Ciebie.',
        'h1': 'Strona internetowa dla restauracji — <em>co musi mieć?</em>',
        'headline': 'Strona internetowa dla restauracji — co musi mieć?',
        'lead': 'Gość decyduje w kilka sekund: menu, ceny, godziny i dojazd. Jeśli tego nie znajdzie, wybierze lokal obok. Oto 10 rzeczy, które musi mieć strona restauracji — i kilka, które tylko przeszkadzają.',
        'excerpt': 'Menu, godziny, zamówienia, rezerwacje i zdjęcia — 10 rzeczy, dzięki którym gość wybiera Twój lokal.',
        'og_kicker': 'Poradnik · gastronomia',
        'keywords': ['strona internetowa dla restauracji', 'strona www restauracji', 'co powinna zawierać strona restauracji',
                     'menu na stronie restauracji', 'strona internetowa pizzeria', 'strona dla food trucka'],
        'tldr': [
            '<strong>Menu z cenami jako tekst</strong> na stronie — nie PDF i nie zdjęcie karty.',
            '<strong>Godziny, adres z mapą i telefon</strong> widoczne od razu na telefonie.',
            '<strong>Jeden wyraźny przycisk:</strong> zamów, zarezerwuj albo zadzwoń.',
            '<strong>Prawdziwe zdjęcia</strong> potraw i wnętrza zamiast zdjęć ze stocka.',
            '<strong>Te same dane</strong> na stronie, w Wizytówce Google i na Facebooku.',
        ],
        'body': '''
## Po co restauracji strona, skoro ma Facebooka

Kiedy ktoś jest głodny, wpisuje w Google „pizza”, „burger” albo „obiad” i nazwę miasta. Google pokazuje mapkę z lokalami i strony internetowe, a profil na Facebooku przegrywa tu ze stroną i Wizytówką Google. Do tego menu na Facebooku to często zdjęcie karty sprzed roku, a godziny giną w starych postach.

Strona to miejsce, w którym gość w kilka sekund znajduje wszystko, czego potrzebuje, żeby przyjść albo zamówić. Facebook i Instagram nadal są potrzebne — do pokazywania nowości i budowania relacji. Więcej o tym duecie piszę w artykule [strona internetowa czy Facebook](strona-internetowa-czy-facebook).

## 10 rzeczy, które musi mieć strona restauracji

### 1. Menu z cenami — jako tekst

Menu to najczęściej otwierana część strony restauracji. Pokaż je jako zwykły tekst: nazwy dań, krótki opis i cena. Taki tekst wygodnie czyta się na telefonie, łatwo go zaktualizować, a Google i asystenci AI rozumieją, co serwujesz — i mogą pokazać Cię komuś, kto szuka „burgera z jalapeño” albo „pizzy na cienkim cieście”.

Menu w PDF albo jako zdjęcie karty to kłopot: trzeba je powiększać palcami, długo się ładuje, a wyszukiwarka nie zawsze odczyta, co jest w środku.

### 2. Godziny otwarcia — aktualne

Godziny powinny być widoczne od razu, także w święta i dni wolne. Te same godziny wpisz w Wizytówce Google. Rozbieżności to najprostszy sposób, żeby stracić gościa, który przyjechał pod zamknięte drzwi.

### 3. Adres, mapa i dojazd

Adres z mapą, informacja o parkingu i wejściu. Na telefonie — przycisk, który od razu otwiera nawigację.

### 4. Jeden główny przycisk

Zdecyduj, czego najbardziej chcesz od gościa: zamówienia, rezerwacji czy telefonu. Ten przycisk powinien być widoczny cały czas, także podczas przewijania na telefonie. Numer telefonu musi być klikalny, żeby dzwonić jednym dotknięciem.

### 5. Zamówienia online

Masz dwie drogi:

- **Link do platformy** (np. Pyszne.pl, Glovo czy Wolt) — szybko i bez dodatkowej pracy, ale platforma pobiera prowizję od zamówień.
- **Własne zamówienia na stronie** — bez prowizji dla pośrednika, za to z większą pracą na start: koszyk, płatności, obsługa.

Wiele lokali łączy obie drogi. Jeśli przyjmujesz zamówienia online, gość powinien znać skład i alergeny, zanim zamówi — tego wymagają przepisy o informowaniu konsumentów o żywności.

### 6. Rezerwacje stolików

W małym lokalu wystarczy telefon albo krótki formularz. Jeśli rezerwacji jest dużo, system z wyborem godziny i liczby osób oszczędza czas Tobie i obsłudze.

### 7. Prawdziwe zdjęcia

Twoje dania, Twoje wnętrze, Twój zespół. Zdjęcia ze stocka gość rozpozna od razu — i przestanie wierzyć reszcie strony. Na start wystarczą dobre zdjęcia z telefonu, zrobione przy dziennym świetle.

### 8. Szybkość na telefonie

Większość gości zobaczy stronę na telefonie, często na mobilnym internecie. Lekkie zdjęcia, żadnych filmów odtwarzanych w tle i żadnych wyskakujących okien zasłaniających menu.

### 9. Opinie i Wizytówka Google

Opinie widać obok Twojego lokalu w Mapach Google — często zanim ktoś wejdzie na stronę. Podlinkuj wizytówkę na stronie i aktywnie zbieraj opinie: [7 sposobów na więcej opinii](jak-zdobyc-opinie-google). Najprościej robi się to [kartą NFC przy kasie](karty-nfc-opinie-google).

### 10. Podstawy SEO lokalnego

Tytuł strony z rodzajem kuchni i miastem (np. „Burgery Sieradz — ŻAR”), te same dane kontaktowe wszędzie i dane strukturalne dla restauracji (menu, godziny, rodzaj kuchni). Dzięki temu Google i asystenci AI wiedzą dokładnie, czym jesteś i gdzie Cię znaleźć.

## Czego unikać na stronie restauracji

- **Muzyki i filmów, które włączają się same.**
- **Menu w PDF albo jako zdjęcia karty.**
- **Nieaktualnych cen i godzin** — gość, który zapłaci więcej niż na stronie, nie wróci.
- **Wyskakujących okien**, które zasłaniają menu na telefonie.
- **Strony, którą trzeba powiększać palcami**, żeby cokolwiek przeczytać.

## Ile kosztuje strona internetowa dla restauracji

| Potrzeba | Pakiet | Cena u mnie | Czas |
|---|---|---|---|
| Menu, godziny, mapa i kontakt (food truck, mały lokal) | Landing page | od 2 000 zł | 4–8 dni |
| Pełna strona: menu, galeria, rezerwacje, o lokalu, SEO | Strona wizytówka | od 3 000 zł | 7–16 dni |
| Zamówienia i płatności online na stronie | Strona + sklep | wycena indywidualna | po ustaleniu zakresu |

Zanim zapłacisz złotówkę, dostajesz darmowy projekt ze znakiem wodnym — najczęściej na zdjęciach z Twojego Facebooka lub Instagrama. Więcej o cenach: [ile kosztuje strona internetowa](ile-kosztuje-strona-internetowa).

## Przykład: koncept ŻAR Burger

Jak to wygląda w praktyce, pokazuję w koncepcie [ŻAR Burger](zar-burger) — stronie burgerowni, którą możesz przewinąć na żywo. Menu w kartach ze zdjęciami dań, status „otwarte teraz” liczony na bieżąco, pasek z daniami i rysowana mapa dojazdu. To projekt koncepcyjny, a nie realizacja dla klienta — ale dokładnie tak może wyglądać Twój lokal. Wszystkie projekty zobaczysz w [portfolio](prace).
''',
        'faq': [
            ('Czy menu w PDF wystarczy na stronie restauracji?', 'Lepiej nie. PDF trzeba powiększać na telefonie, długo się ładuje, a Google i asystenci AI nie zawsze odczytają jego treść. Menu jako zwykły tekst na stronie jest wygodniejsze dla gości i lepsze dla widoczności.'),
            ('Czy restauracja może przyjmować zamówienia online bez Pyszne.pl?', 'Tak — przez własny system zamówień na stronie, bez prowizji dla pośrednika. To większa praca na start (koszyk, płatności), dlatego wyceniam ją indywidualnie. Wiele lokali łączy własne zamówienia z platformami.'),
            ('Ile kosztuje strona internetowa dla restauracji?', 'U mnie landing page z menu, godzinami i mapą kosztuje od 2 000 zł, a pełna strona wizytówka z galerią i rezerwacjami od 3 000 zł. Zamówienia z płatnościami online wyceniam indywidualnie.'),
            ('Ile trwa zrobienie strony dla restauracji?', 'Landing page 4–8 dni, strona wizytówka 7–16 dni. Jeśli zależy Ci na czasie, ekspresowa realizacja skraca termin nawet o połowę.'),
            ('Czy potrzebuję profesjonalnej sesji zdjęciowej?', 'Na start nie. Dobre zdjęcia z telefonu przy dziennym świetle wystarczą — na nich przygotuję też darmowy projekt strony. Sesję zawsze można dołożyć później.'),
        ],
        'related': ['jak-zalozyc-wizytowke-google', 'jak-zdobyc-opinie-google'],
        'curtain': ('Restauracje', 'Co musi mieć strona restauracji.', 'Restaurants', 'What a restaurant website needs.'),
        'bg': 'prace',
    },
    {
        'slug': 'strona-internetowa-dla-salonu-urody',
        'data': DZIS,
        'title': 'Strona internetowa dla salonu urody — co musi mieć? | Marcel Struszczak',
        'og_title': 'Strona internetowa dla salonu urody — co musi mieć?',
        'description': 'Cennik, rezerwacja online, galeria metamorfoz, zespół i opinie. Co musi mieć strona salonu urody, fryzjera lub barbera, żeby klienci rezerwowali u Ciebie.',
        'h1': 'Strona internetowa dla salonu urody — <em>co musi mieć?</em>',
        'headline': 'Strona internetowa dla salonu urody — co musi mieć?',
        'lead': 'Klientka wybiera salon oczami: zdjęcia, ceny, wolne terminy. Instagram pokazuje klimat, ale to strona zamienia oglądanie w rezerwację. Oto, co musi się na niej znaleźć — to samo dotyczy fryzjera, barbera i stylistki paznokci.',
        'excerpt': 'Cennik, rezerwacja online, galeria metamorfoz i opinie — co sprawia, że klientka rezerwuje właśnie u Ciebie.',
        'og_kicker': 'Poradnik · beauty',
        'keywords': ['strona internetowa dla salonu urody', 'strona dla salonu kosmetycznego', 'strona internetowa dla fryzjera',
                     'strona dla barbera', 'rezerwacja online salon', 'strona www salon beauty'],
        'tldr': [
            '<strong>Cennik usług z czasem trwania</strong> — klientka chce wiedzieć, ile zapłaci, zanim zadzwoni.',
            '<strong>Rezerwacja w 2–3 kliknięciach:</strong> własny kalendarz, przycisk do Booksy albo chociaż WhatsApp.',
            '<strong>Galeria prac i metamorfoz</strong> — tylko prawdziwe zdjęcia, za zgodą klientek.',
            '<strong>Zespół, dojazd, godziny i opinie z Google</strong> budują zaufanie przed pierwszą wizytą.',
            '<strong>Ten sam styl co na Instagramie</strong> — strona ma wyglądać jak Twój salon.',
        ],
        'body': '''
## Instagram czy strona? Jedno i drugie

Instagram to wizytówka klimatu salonu — i dobrze, że go masz. Ale klientka, która szuka „kosmetyczki”, „manicure” albo „fryzjera” w swoim mieście, często zaczyna w Google. Tam liczą się strona i Wizytówka Google, a profil na Instagramie może się w ogóle nie pojawić. Strona zbiera w jednym miejscu to, czego na Instagramie trzeba szukać: ceny, terminy, dojazd i rezerwację.

## Co musi mieć strona salonu urody

### 1. Cennik usług

Podziel usługi na kategorie (twarz, ciało, dłonie i stopy, brwi i rzęsy, włosy) i przy każdej podaj cenę oraz czas trwania. Jeśli cena zależy od długości włosów albo zakresu zabiegu — napisz „od”. „Ceny ustalane indywidualnie” przy każdej usłudze zniechęca: klientka woli salon, w którym od razu wie, na co się przygotować.

### 2. Rezerwacja online

To najważniejszy przycisk na stronie. Masz trzy drogi:

- **Własny kalendarz rezerwacji na stronie** — w Twoim stylu i bez pośrednika, za to trzeba go pilnować.
- **Przycisk „Umów wizytę” prowadzący do Booksy** — wiele klientek zna tę aplikację, ale to abonament i miejsce, w którym klientka widzi też inne salony.
- **WhatsApp albo telefon** — najprostsze na start, gdy rezerwacji nie jest dużo.

Niezależnie od wyboru: rezerwacja powinna zająć 2–3 kliknięcia i nie wymagać zakładania konta.

### 3. Galeria prac i metamorfoz

To ona sprzedaje najbardziej. Pokaż efekty „przed i po”, w dobrym świetle, przy różnych usługach. Zdjęcia klientek publikuj tylko za ich zgodą — najlepiej pisemną — bo wizerunek to dane osobowe.

### 4. Zespół

Imię, specjalizacja i zdjęcie każdej osoby. Klientka chętniej rezerwuje wizytę u „Ani od rzęs” niż u anonimowego „specjalisty”.

### 5. Opinie

Pokaż prawdziwe opinie z Google i podlinkuj swoją wizytówkę. Karta NFC w recepcji pozwala zostawić opinię jednym dotknięciem telefonu — [jak działają karty NFC do opinii](karty-nfc-opinie-google).

### 6. Dojazd, parking i godziny

Adres z mapą, informacja o parkingu, wejściu i piętrze. Godziny takie same jak w Wizytówce Google.

### 7. Bony podarunkowe

Jeśli je sprzedajesz — pokaż je na stronie. To gotowy prezent, którego ktoś szuka przed świętami albo urodzinami. Sprzedaż bonów online z płatnością to już funkcja sklepu.

### 8. Styl jak w salonie

Kolory, zdjęcia i klimat strony powinny zgadzać się z tym, co klientka zobaczy na miejscu i na Instagramie. Spójność buduje zaufanie, zanim ktoś przekroczy próg.

## Fryzjer, barber, paznokcie — na co zwrócić uwagę

- **Fryzjer:** cennik zależny od długości włosów i jasna informacja, co jest w cenie (mycie, modelowanie).
- **Barber:** rezerwacja do konkretnego barbera, usługi łączone (strzyżenie i broda) i męski, mocny klimat — tak jak w moim koncepcie [Vesper Barber](vesper-barber) z kalendarzem wizyt i mapą dojazdu.
- **Paznokcie i rzęsy:** duża galeria wzorów i stylizacji — to główny powód, dla którego ktoś wybiera właśnie Ciebie.

## Czego unikać

- **Zdjęć ze stocka** — klientka chce zobaczyć Twoje prace, a nie cudze.
- **Rezerwacji, która wymaga zakładania konta.**
- **Cennika w PDF** albo braku cennika.
- **Nieaktualnych godzin i promocji sprzed roku.**

## Ile kosztuje strona salonu urody

| Potrzeba | Pakiet | Cena u mnie | Czas |
|---|---|---|---|
| Cennik, przycisk rezerwacji, kontakt i mapa | Landing page | od 2 000 zł | 4–8 dni |
| Pełna strona: galeria, zespół, cennik, rezerwacja, SEO | Strona wizytówka | od 3 000 zł | 7–16 dni |
| Sprzedaż bonów i produktów online | Strona + sklep | wycena indywidualna | po ustaleniu zakresu |

Jak może wyglądać strona Twojego salonu, pokazuję w koncepcie [Luxe Salon](luxe-salon): spokojny klimat japandi, cennik usług, rezerwacja jednym kliknięciem, galeria metamorfoz i tryb ciemny. Zanim cokolwiek zapłacisz, przygotuję darmowy projekt na zdjęciach z Twojego Instagrama.
''',
        'faq': [
            ('Czy salon potrzebuje strony, skoro ma Booksy i Instagrama?', 'Tak. Instagram pokazuje klimat, Booksy przyjmuje rezerwacje, a strona zbiera wszystko w jednym miejscu i pokazuje Cię w Google — tam, gdzie szuka wiele nowych klientek. Booksy podepniesz do strony przyciskiem „Umów wizytę”.'),
            ('Jak połączyć stronę z Booksy?', 'Najprościej przyciskiem „Umów wizytę”, który prowadzi do Twojego profilu w Booksy. Klientka klika i od razu wybiera termin.'),
            ('Czy mogę pokazywać na stronie zdjęcia klientek?', 'Tylko za ich zgodą — najlepiej pisemną, bo wizerunek to dane osobowe. Bezpieczna alternatywa to zdjęcia samych efektów, bez twarzy.'),
            ('Ile kosztuje strona internetowa dla salonu urody?', 'U mnie landing page z cennikiem i przyciskiem rezerwacji kosztuje od 2 000 zł, a pełna strona z galerią i zespołem od 3 000 zł. Sprzedaż bonów online wyceniam indywidualnie.'),
            ('Ile trwa zrobienie strony dla salonu?', 'Landing page 4–8 dni, strona wizytówka 7–16 dni. Na start dostajesz darmowy projekt ze znakiem wodnym.'),
        ],
        'related': ['jak-zdobyc-opinie-google', 'landing-page-czy-strona-wizytowka'],
        'curtain': ('Salony urody', 'Co musi mieć strona salonu urody.', 'Beauty salons', 'What a beauty salon website needs.'),
        'bg': 'o-mnie',
    },
]

# Kolejność na stronie Poradnik (i w kanale RSS według dat).
_PO_SLUGU = {a['slug']: a for a in _ARTYKULY + _NOWE}
ARTYKULY = [_PO_SLUGU[s] for s in [
    'ile-kosztuje-strona-internetowa', 'landing-page-czy-strona-wizytowka', 'jak-zalozyc-wizytowke-google',
    'czy-twoja-firma-jest-widoczna-w-google', 'strona-internetowa-czy-facebook', 'jak-zdobyc-opinie-google',
    'strona-internetowa-dla-restauracji', 'strona-internetowa-dla-salonu-urody']]
assert len(ARTYKULY) == len(_PO_SLUGU)

# Karty „Z poradnika” na stronie głównej i na stronie Usługi.
NA_STARCIE = ['ile-kosztuje-strona-internetowa', 'jak-zalozyc-wizytowke-google', 'czy-twoja-firma-jest-widoczna-w-google']
NA_USLUGACH = ['ile-kosztuje-strona-internetowa', 'landing-page-czy-strona-wizytowka', 'strona-internetowa-czy-facebook']

PORADNIK = {
    'slug': 'poradnik',
    'title': 'Poradnik dla firm — strony, social media, opinie Google | Marcel Struszczak',
    'og_title': 'Poradnik dla firm. Bez lania wody.',
    'description': 'Konkretne odpowiedzi dla właścicieli firm: ceny stron, landing czy wizytówka, Wizytówka Google, opinie i co musi mieć strona restauracji albo salonu.',
    'h1': 'Poradnik. <em>Bez lania wody.</em>',
    'lead': 'Krótkie, konkretne odpowiedzi na pytania, które najczęściej słyszę od właścicieli firm: ile to kosztuje, co wybrać i jak przyciągnąć klientów.',
    'og_kicker': 'Poradnik dla firm',
    'curtain': ('Poradnik', 'Konkretne odpowiedzi na pytania, które słyszę najczęściej.', 'Guides', 'Straight answers to the questions I hear most.'),
    'bg': 'o-mnie',
}
