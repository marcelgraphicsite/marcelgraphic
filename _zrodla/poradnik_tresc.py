# -*- coding: utf-8 -*-
"""Treść poradnika (źródło). Strony HTML buduje zbuduj_poradnik.py.

Każdy artykuł: odpowiedź na górze („W skrócie”), treść w Markdown, FAQ.
Ceny i terminy muszą zgadzać się z cennikiem (cennik.html) — bez zmyślonych statystyk.
"""

DATA = '2026-10-01'
DATA_TXT = '1 października 2026'

ARTYKULY = [
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

Zanim zapłacisz złotówkę, dostajesz **darmowy projekt ze znakiem wodnym**. Zaliczkę (od 40%) wpłacasz dopiero, gdy chcesz iść dalej, a resztę po akceptacji gotowej strony. Płatność można rozłożyć na raty. Wstępną kwotę policzysz w [kalkulatorze wyceny](cennik#kalkulator).

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
        'related': ['strona-internetowa-czy-facebook', 'jak-zdobyc-opinie-google'],
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

Jeśli nie masz jeszcze strony, minimum to **Wizytówka Google** (Profil Firmy w Google) — jest darmowa i pokazuje Cię w Mapach oraz w lokalnych wynikach wyszukiwania. Strona to naturalny kolejny krok: wizytówka kieruje do niej ludzi, a strona zamienia ich w klientów.

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
        'related': ['ile-kosztuje-strona-internetowa', 'jak-zdobyc-opinie-google'],
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

Klient przykłada telefon do karty i od razu otwiera się okno opinii Twojej firmy — bez aplikacji, bez szukania i bez skanowania. Działa na większości współczesnych smartfonów: iPhone’y od modelu XS odczytują NFC bez aplikacji, a na Androidzie wystarczy włączone NFC. Jedna uwaga: NFC nie działa na metalu, więc kartę stawia się na ladzie lub stoliku, a naklejkę na szybie lub drzwiach.

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
        'related': ['ile-kosztuje-strona-internetowa', 'strona-internetowa-czy-facebook'],
        'curtain': ('Opinie Google', '7 sposobów na więcej opinii dla lokalnej firmy.', 'Reviews', '7 ways to get more Google reviews.'),
        'bg': 'kontakt',
    },
]

PORADNIK = {
    'slug': 'poradnik',
    'title': 'Poradnik dla firm — strony, social media, opinie Google | Marcel Struszczak',
    'og_title': 'Poradnik dla firm. Bez lania wody.',
    'description': 'Konkretne odpowiedzi dla właścicieli firm: ile kosztuje strona internetowa, strona czy Facebook, jak zdobyć więcej opinii w Google.',
    'h1': 'Poradnik. <em>Bez lania wody.</em>',
    'lead': 'Krótkie, konkretne odpowiedzi na pytania, które najczęściej słyszę od właścicieli firm: ile to kosztuje, co wybrać i jak przyciągnąć klientów.',
    'og_kicker': 'Poradnik dla firm',
    'curtain': ('Poradnik', 'Konkretne odpowiedzi na pytania, które słyszę najczęściej.', 'Guides', 'Straight answers to the questions I hear most.'),
    'bg': 'o-mnie',
}
