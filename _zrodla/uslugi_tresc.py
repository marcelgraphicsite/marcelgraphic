# -*- coding: utf-8 -*-
"""Treść stron usług (źródło). Strony HTML buduje zbuduj_poradnik.py.

Każda strona: odpowiedź na górze („W skrócie”), treść w Markdown, FAQ.
[[blok:www]], [[blok:nfc]], [[blok:social]] = karty z cenami skopiowane z cennik.html przy budowaniu,
więc ceny zmieniasz tylko w cenniku (i w tekstach poniżej, jeśli je wymieniasz).
Bez zmyślonych statystyk i obietnic, których nie ma w ofercie.
"""

DZIS = '2026-10-06'
B = 'https://marcelgraphicsite.pl/'

USLUGI = [
    {
        'slug': 'strony-internetowe-sieradz',
        'data': DZIS,
        'title': 'Strony internetowe Sieradz — tworzenie stron www dla firm | Marcel Struszczak',
        'og_title': 'Strony internetowe w Sieradzu — Marcel Struszczak',
        'description': 'Tworzę strony internetowe dla firm z Sieradza i okolic: od 2 000 zł, gotowe w 4–16 dni. Spotkam się na miejscu i pokażę darmowy projekt, zanim zapłacisz.',
        'h1': 'Strony internetowe <em>w Sieradzu.</em>',
        'crumb': 'Sieradz',
        'name': 'Strony internetowe Sieradz',
        'lead': 'Jestem z Sieradza i projektuję strony dla lokalnych firm — restauracji, salonów, warsztatów i usługodawców. Spotkamy się u Ciebie, pokażę darmowy projekt na laptopie, a Ty zdecydujesz, czy idziemy dalej.',
        'side': ['Sieradz i okolice', 'Spotkanie na miejscu', 'Darmowy projekt na start'],
        'og_kicker': 'Sieradz',
        'og_sub': 'Od 2 000 zł · gotowe w 4–16 dni · spotkanie na miejscu',
        'keywords': ['strony internetowe Sieradz', 'tworzenie stron internetowych Sieradz', 'projektowanie stron www Sieradz',
                     'strona www dla firmy Sieradz', 'strony internetowe Zduńska Wola', 'strony internetowe powiat sieradzki'],
        'tldr': [
            '<strong>Kto:</strong> Marcel Struszczak, projektant stron z Sieradza. Pracujesz bezpośrednio ze mną — bez pośredników.',
            '<strong>Ceny:</strong> landing page od 2 000 zł, strona wizytówka od 3 000 zł, sklep — wycena indywidualna. Domena, hosting i SSL: 200 zł w pierwszym roku.',
            '<strong>Czas:</strong> landing 4–8 dni, wizytówka 7–16 dni.',
            '<strong>Na start:</strong> darmowy projekt ze znakiem wodnym. Płacisz dopiero, gdy chcesz iść dalej — możliwe raty.',
            '<strong>Gdzie:</strong> Sieradz i okolice — spotkamy się u Ciebie. Zduńska Wola, Łask, Wieluń i reszta Polski — zdalnie albo po umówieniu.',
        ],
        'body': '''
## Strona, którą klienci z Sieradza znajdą w Google

Kiedy ktoś w Sieradzu szuka fryzjera, mechanika albo pizzy, wpisuje w Google usługę i nazwę miasta — najczęściej na telefonie. Google pokazuje wtedy mapkę z kilkoma firmami, a pod nią strony internetowe. Klient wybiera w kilka sekund: patrzy na opinie, zdjęcia, ceny i na to, jak firma wygląda w sieci.

Dlatego strona lokalnej firmy nie jest od tego, żeby „po prostu była”. Ma jedno zadanie: żeby klient, który Cię znalazł, zadzwonił, zarezerwował albo przyjechał — do Ciebie, a nie do konkurencji.

## Co dostajesz

- **Projekt w kolorach Twojej marki** — w pakiecie Wizytówka w pełni indywidualny, a nie kolejny szablon.
- **Stronę dopracowaną na telefonie** — tam zobaczy ją większość Twoich klientów.
- **Jeden jasny cel** — telefon, rezerwacja, zamówienie albo wiadomość na WhatsAppie jednym kliknięciem.
- **Podstawy widoczności w Google** — tytuły, opisy i dane dla wyszukiwarek, a w pakiecie Wizytówka także podpięcie Profilu Firmy w Google (Wizytówki Google).
- **Domenę na Ciebie** — rejestruję ją na Twój e-mail, więc od pierwszego dnia jest w 100% Twoja.
- **Hosting i SSL bez Twojego udziału** — ogarniam techniczne sprawy, a 30 dni przed odnowieniem przypominam o płatności.

[[blok:www]]

## Jak pracuję z firmami z Sieradza

1. **Rozmowa** — telefonicznie albo u Ciebie w firmie. Poznaję Twój biznes i to, co ma dać Ci strona.
2. **Darmowy projekt** — przygotowuję projekt ze znakiem wodnym, najczęściej na zdjęciach z Twojego Facebooka lub Instagrama. Pokazuję go na laptopie albo wysyłam link.
3. **Zaliczka od 40%** — dopiero wtedy, gdy projekt Ci się podoba. Resztę możesz rozłożyć na raty.
4. **Realizacja i poprawki** — landing w 4–8 dni, wizytówka w 7–16 dni. Płatność końcowa po akceptacji gotowej strony.
5. **Start i opieka** — domena, hosting, SSL i Wizytówka Google. Mieszkam w Sieradzu, więc nie znikam po oddaniu strony.

## Gdzie działam

Na co dzień pracuję w **Sieradzu i całym powiecie sieradzkim**: Błaszki, Brąszewice, Brzeźnio, Burzenin, Goszczanów, Klonowa, Warta, Wróblew i Złoczew. W Sieradzu i najbliższej okolicy spotkam się u Ciebie w firmie.

Robię też strony dla firm ze **Zduńskiej Woli, Szadku, Łasku, Wielunia, Poddębic, Turku, Kalisza i Łodzi** — tu spotykamy się po umówieniu albo działamy zdalnie. Z resztą Polski pracuję online: telefon, WhatsApp i e-mail wystarczą, żeby zrobić świetną stronę.

## Dlaczego lokalnie, a nie agencja z drugiego końca Polski

- **Widzimy się twarzą w twarz.** Projekt oglądasz razem ze mną, a nie w mailu od opiekuna klienta.
- **Rozmawiasz z osobą, która robi Twoją stronę.** Bez handlowca, project managera i przekazywania sprawy dalej.
- **Jestem na miejscu.** Gdy trzeba coś zmienić, nie czekasz tygodniami na odpowiedź.
- **Odpowiadam w ciągu 24 godzin.**

## Ile kosztuje strona internetowa w Sieradzu

| Pakiet | Cena | Czas | Dla kogo |
|---|---|---|---|
| Landing page | od 2 000 zł | 4–8 dni | jedna główna usługa, szybki start, mały budżet |
| Strona wizytówka | od 3 000 zł | 7–16 dni | firma z kilkoma usługami, która chce klientów z Google |
| Strona + sklep | wycena indywidualna | po ustaleniu zakresu | sprzedaż online, płatności BLIK i kartą |

Do tego domena, hosting i SSL: **200 zł za pierwszy rok, potem 500 zł rocznie**. Ceny są takie same dla firm z Sieradza i z całej Polski, a spotkanie na miejscu nic nie kosztuje. Szczegóły rozpisałem w artykule [ile kosztuje strona internetowa](ile-kosztuje-strona-internetowa), a wstępną kwotę policzysz w [kalkulatorze wyceny](cennik#kalkulator). Nie wiesz, który pakiet wybrać? Przeczytaj [landing page czy strona wizytówka](landing-page-czy-strona-wizytowka).

## Strona to połowa sukcesu. Druga połowa to Wizytówka Google

W lokalnych wynikach Google najwięcej uwagi zbiera mapka z firmami — czyli **Profile Firmy w Google** (dawniej Google Moja Firma). Strona i zadbana wizytówka działają razem: wizytówka pokazuje Cię w Mapach, a strona przekonuje klienta, że to Ty jesteś najlepszym wyborem.

- Jak założyć wizytówkę krok po kroku — [Wizytówka Google: instrukcja](jak-zalozyc-wizytowke-google).
- Jak zbierać więcej opinii — [7 sposobów na opinie w Google](jak-zdobyc-opinie-google) i [karty NFC do opinii](karty-nfc-opinie-google).
- Gdzie dziś tracisz klientów — [test widoczności w Google w 10 minut](czy-twoja-firma-jest-widoczna-w-google).
''',
        'faq': [
            ('Ile kosztuje strona internetowa w Sieradzu?', 'Landing page od 2 000 zł, strona wizytówka od 3 000 zł, a sklep wyceniam indywidualnie. Do tego domena, hosting i SSL: 200 zł w pierwszym roku, potem 500 zł rocznie. Ceny są takie same jak dla firm z reszty Polski.'),
            ('Czy możemy spotkać się osobiście?', 'Tak. W Sieradzu i okolicy przyjadę do Twojej firmy i pokażę projekt na laptopie. Jeśli wolisz, wszystko załatwimy przez telefon, WhatsApp albo e-mail.'),
            ('Czy robisz strony dla firm ze Zduńskiej Woli, Łasku albo Wielunia?', 'Tak. Pracuję z firmami z całego regionu — spotykamy się po umówieniu albo działamy zdalnie. Ceny i terminy są takie same jak w Sieradzu.'),
            ('Ile trwa zrobienie strony internetowej?', 'Landing page 4–8 dni, strona wizytówka 7–16 dni. Ekspresowa realizacja skraca czas nawet o połowę (+25–50% ceny pakietu).'),
            ('Kiedy moja nowa strona pojawi się w Google?', 'Zwykle od kilku dni do kilku tygodni od publikacji. Wysokie pozycje na popularne hasła to praca na miesiące — pomagają w niej Wizytówka Google, opinie i konkretna treść na stronie.'),
            ('Czy pomożesz z Wizytówką Google?', 'Tak. W pakiecie Wizytówka podpinam stronę do Twojego Profilu Firmy w Google i pomagam go uzupełnić. Jeśli wizytówki jeszcze nie masz, przeprowadzę Cię przez jej założenie.'),
            ('Nie mam zdjęć ani tekstów. Co teraz?', 'Na start wystarczą zdjęcia z Twojego Facebooka lub Instagrama — na nich przygotuję też darmowy projekt. Teksty ułożymy razem.'),
        ],
        'related': ['ile-kosztuje-strona-internetowa', 'landing-page-czy-strona-wizytowka', 'jak-zalozyc-wizytowke-google'],
        'curtain': ('Sieradz', 'Strony internetowe dla firm z Sieradza i okolic.', 'Sieradz', 'Websites for businesses in and around Sieradz.'),
        'bg': 'index',
        'service': {
            'name': 'Strony internetowe Sieradz — tworzenie stron www dla firm',
            'serviceType': 'Tworzenie stron internetowych',
            'description': 'Projektowanie i wykonanie stron internetowych dla firm z Sieradza i okolic: landing page, strona wizytówka i sklep internetowy. Darmowy projekt na start, spotkanie na miejscu.',
            'areaServed': [
                {'@type': 'City', 'name': 'Sieradz', 'sameAs': 'https://pl.wikipedia.org/wiki/Sieradz'},
                {'@type': 'AdministrativeArea', 'name': 'powiat sieradzki'},
                {'@type': 'City', 'name': 'Zduńska Wola'}, {'@type': 'City', 'name': 'Łask'}, {'@type': 'City', 'name': 'Wieluń'},
                {'@type': 'City', 'name': 'Złoczew'}, {'@type': 'City', 'name': 'Warta'}, {'@type': 'City', 'name': 'Błaszki'},
                {'@type': 'City', 'name': 'Szadek'}, {'@type': 'City', 'name': 'Poddębice'}, {'@type': 'City', 'name': 'Turek'},
                {'@type': 'City', 'name': 'Kalisz'}, {'@type': 'City', 'name': 'Łódź'}],
            'offers': [
                {'@type': 'Offer', 'name': 'Landing page', 'description': 'Jedna strona z ofertą i kontaktem, realizacja 4–8 dni.',
                 'priceSpecification': {'@type': 'PriceSpecification', 'minPrice': 2000, 'priceCurrency': 'PLN'}, 'url': B + 'cennik#www'},
                {'@type': 'Offer', 'name': 'Strona wizytówka', 'description': 'Rozbudowana strona firmowa z galerią, mapą, SEO i Wizytówką Google, realizacja 7–16 dni.',
                 'priceSpecification': {'@type': 'PriceSpecification', 'minPrice': 3000, 'priceCurrency': 'PLN'}, 'url': B + 'cennik#www'},
                {'@type': 'Offer', 'name': 'Strona + sklep internetowy', 'description': 'Katalog, koszyk i płatności online — wycena indywidualna.', 'url': B + 'cennik#www'},
            ],
        },
    },
    {
        'slug': 'karty-nfc-opinie-google',
        'data': DZIS,
        'title': 'Karty NFC do opinii Google — od 60 zł, wysyłka w Polsce | Marcel Struszczak',
        'og_title': 'Karty NFC do opinii Google — od 60 zł',
        'description': 'Karta NFC z podstawką 60 zł, duża naklejka 80 zł. Programuję je pod Twój profil w Google: klient przykłada telefon i od razu wystawia opinię. Wysyłka w Polsce.',
        'h1': 'Karty NFC do opinii <em>Google.</em>',
        'crumb': 'Karty NFC',
        'name': 'Karty NFC do opinii Google',
        'lead': 'Klient przykłada telefon do karty i od razu widzi okno opinii Twojej firmy. Bez szukania, bez aplikacji, bez przepisywania linków. Każdą kartę programuję osobiście pod Twój profil.',
        'side': ['Karta 60 zł · naklejka 80 zł', 'Wysyłka w całej Polsce', 'Montaż: Sieradz i okolice'],
        'og_kicker': 'Opinie Google',
        'og_sub': 'Karta z podstawką 60 zł · naklejka 80 zł · wysyłka w Polsce',
        'keywords': ['karta nfc opinie google', 'karty nfc do opinii google', 'naklejka nfc opinie google', 'karta do opinii google',
                     'jak zbierać opinie google', 'nfc opinie google cena'],
        'blok_gora': 'nfc',
        'tldr': [
            '<strong>Jak działa:</strong> w karcie jest chip NFC z linkiem do opinii Twojej firmy. Klient przykłada telefon i od razu widzi okno z gwiazdkami.',
            '<strong>Ceny:</strong> karta NFC z podstawką 60 zł, duża naklejka NFC 80 zł. Każdą programuję pod Twój Profil Firmy w Google.',
            '<strong>Telefony:</strong> iPhone od modelu XS i Android z włączonym NFC — bez żadnej aplikacji.',
            '<strong>Dostawa:</strong> wysyłka w całej Polsce albo montaż na miejscu w Sieradzu i okolicy.',
            '<strong>Uwaga:</strong> NFC nie działa na metalu — doradzę, gdzie postawić kartę, żeby działała za każdym razem.',
        ],
        'body': '''
## Jak działa karta NFC do opinii Google

W każdej karcie i naklejce jest mały chip NFC — ta sama technologia, której używasz, płacąc telefonem. Zapisuję w nim bezpośredni link do opinii Twojej firmy w Google.

1. Klient przykłada telefon do karty.
2. Telefon od razu otwiera okno opinii Twojej firmy — z gwiazdkami i polem na komentarz.
3. Klient wybiera gwiazdki, dopisuje kilka słów i gotowe.

Karta nie ma baterii i nie potrzebuje prądu ani internetu. Internet musi mieć tylko telefon klienta — żeby otworzyć stronę z opinią.

## Karta czy naklejka — co wybrać?

| | Karta NFC z podstawką | Duża naklejka NFC |
|---|---|---|
| Cena | 60 zł | 80 zł |
| Gdzie | lada, kasa, stolik, recepcja | drzwi, witryna, lada |
| Zalety | podasz ją klientowi do ręki, łatwo ją przestawić | widoczna z daleka, nie zginie |
| Programowanie | pod Twój profil w Google | pod Twój profil w Google |

Jeśli masz jedno miejsce obsługi, wystarczy karta przy kasie. Jeśli klienci czekają w kilku miejscach (stoliki, poczekalnia, stanowiska), weź kilka kart albo kartę i naklejkę — każdą programuję pod ten sam profil.

## Gdzie postawić kartę, żeby działała

- **Tam, gdzie klient i tak czeka:** przy kasie, na ladzie, na stoliku, w recepcji, przy odbiorze zamówień.
- **Nie na metalu.** Metal blokuje NFC — na metalowej ladzie postaw kartę na podstawce, a naklejkę przyklej na szybę albo drewno.
- **Na widoku.** Napis „Oceń nas w Google” mówi klientowi, co ma zrobić.
- **Z jednym zdaniem od Ciebie.** „Jeśli było dobrze, przyłóż telefon do karty — to dla nas bardzo ważne”. Prośba powiedziana na głos działa najlepiej.

## Na jakich telefonach działa

- **iPhone od modelu XS** — wystarczy przyłożyć górną część telefonu do karty, bez aplikacji.
- **Android** — większość smartfonów ma NFC; musi być włączone w ustawieniach (na wielu telefonach już jest, bo służy do płatności).
- **Telefon bez NFC** — warto mieć obok kod QR z tym samym linkiem do opinii.

## Jak zamówić

1. **Napisz albo zadzwoń** — podaj nazwę firmy z Google i liczbę kart lub naklejek.
2. **Programuję każdą sztukę** pod link do opinii Twojej firmy i sprawdzam, czy otwiera właściwe okno.
3. **Wysyłam w całej Polsce** albo przywożę i montuję na miejscu w Sieradzu i okolicy.

## Opinie zgodnie z zasadami Google

Karta tylko skraca drogę do opinii — zasady są te same co zawsze:

- **nie dawaj nic w zamian** za opinię (rabat, gratis) — to łamie zasady Google;
- **proś wszystkich klientów**, nie tylko tych zadowolonych;
- **nie pisz opinii sam** i nie kupuj ich — w Polsce fałszywe opinie są zakazaną, nieuczciwą praktyką rynkową.

Więcej sposobów znajdziesz w artykule [jak zdobyć więcej opinii w Google](jak-zdobyc-opinie-google). Nie masz jeszcze wizytówki? Zacznij od [Wizytówki Google krok po kroku](jak-zalozyc-wizytowke-google).
''',
        'faq': [
            ('Jak działa karta NFC do opinii Google?', 'W karcie jest chip NFC z zapisanym linkiem do opinii Twojej firmy. Klient przykłada telefon do karty i od razu otwiera mu się okno opinii w Google — bez szukania firmy i bez aplikacji.'),
            ('Czy karta NFC działa na iPhonie?', 'Tak — iPhone od modelu XS odczytuje kartę bez żadnej aplikacji. Na Androidzie wystarczy włączone NFC. Dla telefonów bez NFC warto mieć obok kod QR.'),
            ('Czy karta potrzebuje baterii albo internetu?', 'Nie. Karta działa bez baterii i bez prądu. Internet musi mieć tylko telefon klienta, żeby otworzyć stronę z opinią.'),
            ('Czy karta zadziała na metalowej ladzie?', 'Nie bezpośrednio na metalu — metal blokuje sygnał NFC. Postaw kartę na podstawce albo przyklej naklejkę na szybę lub drewno. Doradzę, gdzie ją umieścić.'),
            ('Ile kosztuje karta NFC do opinii Google?', 'Karta NFC z podstawką kosztuje 60 zł, a duża naklejka NFC 80 zł za sztukę. Każdą programuję pod Twój Profil Firmy w Google i wysyłam w całej Polsce.'),
            ('Czy mogę zamówić kilka kart do jednej firmy?', 'Tak. Każdą kartę i naklejkę programuję pod ten sam profil — możesz postawić je przy kasie, na stolikach i na drzwiach.'),
            ('Czy zbieranie opinii przez kartę NFC jest zgodne z zasadami Google?', 'Tak, o ile nie dajesz nic w zamian za opinię i prosisz o nią wszystkich klientów, a nie tylko zadowolonych. Karta tylko skraca drogę do okna opinii.'),
        ],
        'related': ['jak-zdobyc-opinie-google', 'jak-zalozyc-wizytowke-google', 'czy-twoja-firma-jest-widoczna-w-google'],
        'curtain': ('Karty NFC', 'Opinia w Google jednym dotknięciem telefonu.', 'NFC cards', 'A Google review with one tap of a phone.'),
        'bg': 'kontakt',
        'service': {
            'name': 'Karty NFC do opinii Google',
            'serviceType': 'Programowanie kart NFC do opinii Google',
            'description': 'Karty i naklejki NFC programowane pod Profil Firmy w Google: klient przykłada telefon i od razu wystawia opinię. Wysyłka w całej Polsce, montaż w Sieradzu i okolicy.',
            'areaServed': {'@type': 'Country', 'name': 'Polska'},
            'offers': [
                {'@type': 'Offer', 'name': 'Karta NFC do opinii Google z podstawką', 'price': 60, 'priceCurrency': 'PLN', 'availability': 'https://schema.org/InStock', 'url': B + 'karty-nfc-opinie-google'},
                {'@type': 'Offer', 'name': 'Duża naklejka NFC do opinii Google', 'price': 80, 'priceCurrency': 'PLN', 'availability': 'https://schema.org/InStock', 'url': B + 'karty-nfc-opinie-google'},
            ],
        },
        'produkty': [
            ('karta', 'Karta NFC do opinii Google z podstawką', 'Karta NFC w formacie karty płatniczej, z podstawką, zaprogramowana pod Profil Firmy w Google — klient przykłada telefon i od razu wystawia opinię.', 60),
            ('naklejka', 'Duża naklejka NFC do opinii Google', 'Duża naklejka NFC na drzwi, witrynę lub ladę, zaprogramowana pod Profil Firmy w Google.', 80),
        ],
    },
    {
        'slug': 'prowadzenie-social-media',
        'data': DZIS,
        'title': 'Prowadzenie social mediów dla firm — od 600 zł / mies. | Marcel Struszczak',
        'og_title': 'Prowadzenie social mediów dla firm',
        'description': 'Facebook i Instagram dla lokalnych firm: 8 lub 12–13 postów i karuzel miesięcznie w stylu Twojej marki. Od 600 zł / mies., bez umów na lata.',
        'h1': 'Prowadzenie social mediów <em>dla firm.</em>',
        'crumb': 'Social media',
        'name': 'Prowadzenie social mediów',
        'lead': 'Profil, który wygląda jak marka, a nie jak przypadek. Przygotowuję i publikuję posty oraz karuzele na Facebooku i Instagramie — Ty prowadzisz firmę, ja profil.',
        'side': ['Facebook · Instagram', 'Od 600 zł / mies.', 'Bez umów na lata'],
        'og_kicker': 'Social media',
        'og_sub': '8 lub 12–13 postów miesięcznie · od 600 zł / mies.',
        'keywords': ['prowadzenie social media', 'prowadzenie facebooka dla firm', 'prowadzenie instagrama dla firm',
                     'social media dla firm cennik', 'prowadzenie social media Sieradz', 'ile kosztuje prowadzenie social media'],
        'blok_gora': 'social',
        'tldr': [
            '<strong>Pakiet Start:</strong> 8 postów i karuzel miesięcznie (ok. 2 w tygodniu) — 600 zł za Facebooka, 800 zł za Facebooka i Instagram.',
            '<strong>Pakiet Pro:</strong> 12–13 postów i karuzel miesięcznie (ok. 3 w tygodniu) — 800 zł za Facebooka, 1 100 zł za Facebooka i Instagram.',
            '<strong>W cenie:</strong> grafiki w stylu Twojej marki, opisy i hashtagi pod Twoją branżę, publikacja według harmonogramu.',
            '<strong>Bez umów na lata:</strong> rozliczamy się co miesiąc.',
            '<strong>Dla kogo:</strong> lokalne firmy, które chcą regularnie przypominać się klientom, ale nie mają na to czasu.',
        ],
        'body': '''
## Co dostajesz w pakiecie

- **Posty graficzne i karuzele** — 8 albo 12–13 w miesiącu, zależnie od pakietu.
- **Spójny styl** — kolory, czcionki i układ dopasowane do Twojej marki, więc profil wygląda jak jedna całość.
- **Opisy i hashtagi** — pisane pod Twoją branżę i Twoich klientów, a nie ogólnikowe „zapraszamy”.
- **Harmonogram** — posty wychodzą regularnie, w ustalone dni. Nie musisz o niczym pamiętać.

Pakiety obejmują posty graficzne i karuzele. Rozliczamy się co miesiąc — bez umów na lata.

## Jak to wygląda w praktyce

1. **Rozmowa na start** — Twoja oferta, klienci, ton komunikacji (na „Ty” czy na „Pan/Pani”) i to, co chcesz promować w pierwszym miesiącu.
2. **Styl profilu** — ustalamy kolory, układ grafik i sposób pisania, żeby każdy post był rozpoznawalny.
3. **Posty i publikacja** — przygotowuję grafiki i opisy, a potem publikuję je według harmonogramu.
4. **Kolejny miesiąc** — dopasowujemy tematy do sezonu, nowości i promocji w Twojej firmie.

## Start czy Pro — który pakiet wybrać?

| | Start | Pro |
|---|---|---|
| Postów i karuzel w miesiącu | 8 (ok. 2 w tygodniu) | 12–13 (ok. 3 w tygodniu) |
| Facebook | 600 zł / mies. | 800 zł / mies. |
| Facebook + Instagram | 800 zł / mies. | 1 100 zł / mies. |
| Cena za post (Facebook) | ok. 75 zł | ok. 67 zł |

Jeśli w Twojej firmie co tydzień dzieje się coś nowego — nowe dania, promocje, sezonowe usługi — wybierz **Pro**. Jeśli chcesz po prostu regularnie przypominać się klientom, wystarczy **Start**.

## „Zrobię to sam w ChatGPT w 5 minut” — czy warto płacić?

Możesz. Sztuczna inteligencja świetnie pomaga pisać teksty — sam z niej korzystam. Ale post zrobiony w 5 minut zwykle wygląda jak zrobiony w 5 minut. Klient ocenia Twoją firmę po profilu w kilka sekund, a o tym, czy profil wygląda jak marka, decydują:

- **spójny wygląd** — te same kolory, układ i jakość w każdym poście,
- **regularność** — co tydzień, a nie zrywami, gdy akurat jest czas,
- **pomysł** — tematy, które pokazują Twoją firmę od najlepszej strony i prowadzą do rezerwacji.

Jeśli masz na to czas i oko do grafiki — rób sam. Jeśli wolisz zająć się firmą — od tego jestem ja.

## Social media i strona — razem działają najlepiej

Social media utrzymują relację z ludźmi, którzy już Cię znają. Nowych klientów z Google zdobywają strona internetowa i Wizytówka Google. Najlepiej działa duet: strona przyciąga, profil przypomina. Porównanie znajdziesz w artykule [strona internetowa czy Facebook](strona-internetowa-czy-facebook), a ceny stron w [cenniku](cennik#www). Jeśli działasz w Sieradzu lub okolicy, zobacz też [strony internetowe w Sieradzu](strony-internetowe-sieradz).
''',
        'faq': [
            ('Ile kosztuje prowadzenie social mediów?', 'Pakiet Start (8 postów i karuzel miesięcznie): 600 zł za Facebooka lub 800 zł za Facebooka i Instagram. Pakiet Pro (12–13 postów i karuzel): 800 zł za Facebooka lub 1 100 zł za Facebooka i Instagram.'),
            ('Czy muszę podpisać umowę na rok?', 'Nie. Rozliczamy się co miesiąc, bez umów na lata.'),
            ('Czy mogę zacząć od samego Facebooka?', 'Tak. Możesz zacząć od Facebooka, a Instagram dołożyć później — pakiet zmieniamy z miesiąca na miesiąc.'),
            ('Co, jeśli nie mam dobrych zdjęć?', 'Na start wystarczą zdjęcia, które już masz — z telefonu albo z Twojego profilu. Resztę dopracuję w grafikach.'),
            ('Czy prowadzisz social media firm spoza Sieradza?', 'Tak. Social media prowadzę zdalnie dla firm z całej Polski — wystarczą telefon, WhatsApp i e-mail.'),
            ('Dlaczego mam płacić, skoro posty zrobię w ChatGPT?', 'Możesz robić je sam — ale post zrobiony w 5 minut zwykle tak wygląda. Ja dbam o spójny wygląd, regularność i opisy, które prowadzą do rezerwacji, a Ty masz to z głowy.'),
        ],
        'related': ['strona-internetowa-czy-facebook', 'jak-zdobyc-opinie-google', 'czy-twoja-firma-jest-widoczna-w-google'],
        'curtain': ('Social media', 'Profil, który wygląda jak marka, a nie jak przypadek.', 'Social media', 'A profile that looks like a brand, not an accident.'),
        'bg': 'uslugi',
        'service': {
            'name': 'Prowadzenie social mediów dla firm (Facebook, Instagram)',
            'serviceType': 'Prowadzenie social mediów',
            'description': 'Posty graficzne i karuzele na Facebooku i Instagramie w stylu marki: opisy, hashtagi i publikacja według harmonogramu. Rozliczenie miesięczne, bez umów na lata.',
            'areaServed': {'@type': 'Country', 'name': 'Polska'},
            'offers': [
                {'@type': 'Offer', 'name': 'Pakiet Start — Facebook (8 postów miesięcznie)', 'price': 600, 'priceCurrency': 'PLN',
                 'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': 600, 'priceCurrency': 'PLN', 'unitText': 'miesiąc'}},
                {'@type': 'Offer', 'name': 'Pakiet Start — Facebook i Instagram (8 postów miesięcznie)', 'price': 800, 'priceCurrency': 'PLN',
                 'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': 800, 'priceCurrency': 'PLN', 'unitText': 'miesiąc'}},
                {'@type': 'Offer', 'name': 'Pakiet Pro — Facebook (12–13 postów miesięcznie)', 'price': 800, 'priceCurrency': 'PLN',
                 'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': 800, 'priceCurrency': 'PLN', 'unitText': 'miesiąc'}},
                {'@type': 'Offer', 'name': 'Pakiet Pro — Facebook i Instagram (12–13 postów miesięcznie)', 'price': 1100, 'priceCurrency': 'PLN',
                 'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': 1100, 'priceCurrency': 'PLN', 'unitText': 'miesiąc'}},
            ],
        },
    },
]
