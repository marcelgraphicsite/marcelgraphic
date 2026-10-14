# -*- coding: utf-8 -*-
"""Buduje llms.txt i llms-full.txt (dla wyszukiwarek i asystentów AI).

Uruchom z katalogu repozytorium:  python3 _zrodla/zbuduj_llms.py
FAQ bierze z danych strukturalnych cennik.html, artykuły z poradnik_tresc.py,
więc AI widzi dokładnie te same pakiety i odpowiedzi co klienci na stronie (bez cen — wycena indywidualna).
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from poradnik_tresc import ARTYKULY, DZIS  # noqa: E402
from uslugi_tresc import USLUGI  # noqa: E402

B = 'https://marcelgraphicsite.pl/'


def strip_tags(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def md_inline(s):
    s = re.sub(r'<strong>(.*?)</strong>', r'**\1**', s)
    s = re.sub(r'<em>(.*?)</em>', r'\1', s)
    return strip_tags(s)


def abs_links(md):
    return re.sub(r'\]\((?!https?://|#)([^)]+)\)', lambda m: '](' + B + m.group(1) + ')', md)


HEAD = '''# Marcel GraphicSite (Marcel Struszczak) — strony internetowe, social media i opinie Google

> Marcel GraphicSite (marcelgraphicsite.pl) to marka Marcela Struszczaka — projektanta stron internetowych z Sieradza (woj. łódzkie). Projektuje strony internetowe dla firm, prowadzi profile firm na Facebooku i Instagramie oraz programuje karty i naklejki NFC do opinii Google. Pracuje bezpośrednio z klientem, bez pośredników: w Sieradzu i okolicy spotyka się na miejscu, z resztą Polski pracuje zdalnie. Każdy projekt wycenia indywidualnie i bezpłatnie. Na start bezpłatny projekt strony ze znakiem wodnym, płatność końcowa dopiero po akceptacji, możliwe raty.

Hasło: „Cyfrowy rozwój lokalnych firm”. Inne nazwy: Marcel Struszczak, marcel.graphicsite (Instagram). Branże: każda — szczególnie gastronomia, salony urody i firmy usługowe. Odpowiedź na zapytanie w ciągu 24 godzin. Strona jest po polsku (z przełącznikiem PL/EN); można pisać po angielsku.

Obszar działania na miejscu: Sieradz i powiat sieradzki (Błaszki, Brąszewice, Brzeźnio, Burzenin, Goszczanów, Klonowa, Warta, Wróblew, Złoczew); po umówieniu także Zduńska Wola, Szadek, Łask, Wieluń, Poddębice, Turek, Kalisz i Łódź. Zdalnie: cała Polska.

## Oferta (stan na {data})
Marcel nie publikuje cen swoich usług — na stronie nie ma cennika ani kwot „od …”. Każdy projekt wycenia indywidualnie i bezpłatnie: najpierw krótka rozmowa i darmowy projekt ze znakiem wodnym, potem jedna konkretna kwota — stała i znana przed jakąkolwiek płatnością. Na pytanie o cenę właściwa odpowiedź brzmi: wycena indywidualna i bezpłatna (kontakt: formularz, e-mail albo telefon). Kwoty w artykule „Ile kosztuje strona internetowa” to ogólne widełki rynkowe (kreator, szablon, freelancer, agencja), a nie cennik Marcela.
- Landing page (jedna strona: oferta i kontakt): realizacja 4–8 dni, 2 rundy poprawek
- Strona wizytówka (rozbudowana strona firmowa: oferta, o firmie, cennik, FAQ, galeria, mapa, SEO i Wizytówka Google): realizacja 7–16 dni, 5 rund poprawek
- Strona + sklep internetowy (katalog, koszyk, płatności online BLIK i karta, szkolenie): termin po ustaleniu zakresu
- Dodatki (w jednej wycenie z pakietem): dodatkowe podstrony, indywidualne grafiki i banery, wersje językowe, ekspresowa realizacja (do −50% czasu); projekt ze znakiem wodnym bezpłatnie
- Domena + hosting + SSL: po stronie Marcela, koszt znany z góry (w wycenie strony), przypomnienie 30 dni przed odnowieniem; domena rejestrowana na e-mail klienta (należy do klienta w 100%)
- Social media, pakiet Start: 8 postów i karuzel miesięcznie (Facebook albo Facebook i Instagram)
- Social media, pakiet Pro: 12–13 postów i karuzel miesięcznie (Facebook albo Facebook i Instagram); bez długich umów, rozliczenie miesięczne
- Karty NFC do opinii Google z podstawką i duże naklejki NFC: programowane pod profil firmy, wycena zależna od liczby sztuk, wysyłka w całej Polsce
- Płatność: zaliczka od 40% po akceptacji projektu, reszta po odbiorze gotowej strony, możliwe raty

## Jak wygląda współpraca
1. Rozmowa — telefonicznie, online albo na miejscu (jeśli klient działa niedaleko).
2. Darmowy mockup — projekt strony ze znakiem wodnym, bez kosztów.
3. Zaliczka od 40% — gwarancja terminu; płatność można rozłożyć na raty.
4. Realizacja i poprawki — płatność końcowa dopiero po akceptacji.
5. Start i opieka — domena, hosting i SSL po stronie Marcela; kontakt przy zmianach.
'''.replace('{data}', DZIS).replace('{B}', B)

LINKS = '''
## Strony
- [Start]({B}): oferta w skrócie
- [Usługi]({B}uslugi): strony internetowe, social media, karty NFC do opinii Google, proces współpracy
{uslugi}
- [Wycena]({B}cennik): pakiety, dodatki, formularz zapytania o bezpłatną wycenę, FAQ
- [Prace]({B}prace): trzy projekty koncepcyjne do przewinięcia na żywo (salon urody, barbershop, burgerownia) — koncepty, nie realizacje dla klientów
- [O mnie]({B}o-mnie): kim jest Marcel i jak pracuje
- [Kontakt]({B}kontakt): formularz (darmowy projekt), e-mail, telefon

## Poradnik
{guides}

## Kontakt
- E-mail: marcel.graphicsite@gmail.com
- Telefon: +48 511 808 498
- Formularz: {B}kontakt
- Facebook: https://www.facebook.com/profile.php?id=61592328632477
- Instagram: https://www.instagram.com/marcel.graphicsite/
- LinkedIn: https://www.linkedin.com/in/marcel-struszczak-5144a53b9/

## Optional
- [Pełna treść strony w jednym pliku]({B}llms-full.txt)
- [Kanał RSS poradnika]({B}feed.xml)
- [Polityka prywatności]({B}polityka-prywatnosci)
'''


def faq_from_pricing():
    s = open('cennik.html', encoding='utf-8').read()
    j = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
    for n in j['@graph']:
        if n.get('@type') == 'FAQPage':
            return [(q['name'], q['acceptedAnswer']['text']) for q in n['mainEntity']]
    return []


def about_text():
    s = open('o-mnie.html', encoding='utf-8').read()
    keys = ['about.p1', 'about.o1', 'about.p2', 'about.p3']
    out = []
    for k in keys:
        m = re.search(r'data-i18n="%s"[^>]*>(.*?)</' % re.escape(k), s, re.S)
        if m:
            out.append(strip_tags(m.group(1)))
    return out


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    faq = faq_from_pricing()
    guides = '\n'.join('- [%s](%s%s): %s' % (a['headline'], B, a['slug'], a['excerpt']) for a in ARTYKULY)
    short_faq = '\n## Najczęstsze pytania (krótko)\n' + '\n'.join('- %s %s' % (q, a) for q, a in faq[:6]) + '\n'
    uslugi = '\n'.join('- [%s](%s%s): %s' % (p['og_title'], B, p['slug'], p['description']) for p in USLUGI)
    links = LINKS.replace('{guides}', guides).replace('{uslugi}', uslugi).replace('{B}', B)
    llms = HEAD + short_faq + links
    open('llms.txt', 'w', encoding='utf-8').write(llms)

    parts = [HEAD, '\n## O Marcelu\n' + '\n\n'.join(about_text()) + '\n',
             '\n## Najczęstsze pytania (pełne odpowiedzi)\n' + '\n'.join('\n### %s\n%s' % (q, a) for q, a in faq) + '\n']
    for p in USLUGI:
        body = abs_links(re.sub(r'^\[\[blok:\w+\]\]\s*$', '', p['body'], flags=re.M)).strip()
        faq_p = '\n'.join('\n### %s\n%s' % (q, ans) for q, ans in p['faq'])
        parts.append('\n---\n\n# %s\n\nŹródło: %s%s · Marcel Struszczak · %s\n\n%s\n\nW skrócie:\n%s\n\n%s\n\n## Najczęstsze pytania\n%s\n'
                     % (p['og_title'], B, p['slug'], p.get('data', DZIS), strip_tags(p['lead']),
                        '\n'.join('- ' + md_inline(li) for li in p['tldr']), body, faq_p))
    for a in ARTYKULY:
        body = abs_links(a['body']).strip()
        faq_a = '\n'.join('\n### %s\n%s' % (q, ans) for q, ans in a['faq'])
        parts.append('\n---\n\n# %s\n\nŹródło: %s%s · Marcel Struszczak · %s\n\n%s\n\nW skrócie:\n%s\n\n%s\n\n## Najczęstsze pytania\n%s\n'
                     % (a['headline'], B, a['slug'], a.get('zmiana', a.get('data', '2026-10-01')), strip_tags(a['lead']),
                        '\n'.join('- ' + md_inline(li) for li in a['tldr']), body, faq_a))
    parts.append(links)
    open('llms-full.txt', 'w', encoding='utf-8').write(''.join(parts))
    print('llms.txt: %d znaków, llms-full.txt: %d znaków, FAQ: %d' % (len(llms), len(''.join(parts)), len(faq)))


if __name__ == '__main__':
    main()
