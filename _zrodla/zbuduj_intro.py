# -*- coding: utf-8 -*-
"""Wejście na stronę (#cinema): logo „Marcel / Struszczak” pisze się piórem — litera po literze, w kolejności pisania.

Z _zrodla/intro_pioro.json (kształty liter + trasa pióra, liczone przez intro_pioro.py) robi SVG w index.html
(między znacznikami zbuduj_intro.py): przygaszone logo + białe logo pod maską, w której pióro rysuje kolejne
pociągnięcia (stroke-dashoffset). Czas każdego pociągnięcia liczy tutaj:
  - stałe tempo pióra (TEMPO), łagodny rozbieg na pierwszym pociągnięciu (ogonek „M”) i miękkie wyhamowanie
    na ostatnim (poprzeczka „t”),
  - przerwa między pociągnięciami jak ręka w powietrzu (odległość / szybsze tempo, najwyżej POWIETRZE_MAX),
  - dociągnięcia do ostrych czubków ruszają, gdy pióro mija najbliższy punkt kreski.
Uruchom z katalogu repozytorium:  python3 _zrodla/zbuduj_intro.py   (sama biblioteka standardowa)
"""
import json
import math
import os
import re

TEMPO = 19.0          # em/s — prędkość pióra wzdłuż kreski (1 em = 1000 jednostek)
START = 0.12          # s — od startu pióra (klasa .pen, gdy procesor wolny), przygaszone logo już widać
POWIETRZE = 2.5       # ręka w powietrzu jest tyle razy szybsza od pióra
POWIETRZE_MAX = 0.07  # s — najdłuższa przerwa między pociągnięciami
WYDLUZ = 24           # jednostki — końce pociągnięć odrobinę dłuższe (szkielet jest krótszy niż litera)
WYHAMOWANIE_MIN = 0.16  # s — ostatnie pociągnięcie (poprzeczka „t”) nie krócej niż tyle


def dl(p):
    return sum(math.hypot(p[i + 1][0] - p[i][0], p[i + 1][1] - p[i][1]) for i in range(len(p) - 1))


def wydluz(p, e):
    def za(a, b):
        dx, dy = a[0] - b[0], a[1] - b[1]
        n = math.hypot(dx, dy) or 1
        return [a[0] + dx / n * e, a[1] + dy / n * e]
    k = min(len(p) - 1, 3)
    return [za(p[0], p[k])] + p + [za(p[-1], p[-1 - k])]


def liczba(v, n=3):
    s = ('%.*f' % (n, v)).rstrip('0').rstrip('.')
    return s[1:] if s.startswith('0.') else (s or '0')


def svg(dane):
    v = TEMPO * 1000
    kreski = [wydluz(p, WYDLUZ) for p in dane['kreski']]
    el, t, prev = [], START, None
    for i, p in enumerate(kreski):
        if prev is not None:
            t += min(POWIETRZE_MAX, math.hypot(p[0][0] - prev[0], p[0][1] - prev[1]) / (POWIETRZE * v))
        l = dl(p)
        if i == 0:                                  # rozbieg: stałe przyspieszenie, kończy z prędkością pióra
            d, e = 2 * l / v, 'cubic-bezier(.3333,0,.6667,.3333)'
        elif i == len(kreski) - 1:                  # wyhamowanie na ostatnim pociągnięciu
            d, e = max(WYHAMOWANIE_MIN, 2 * l / v), 'cubic-bezier(.3333,.6667,.6667,1)'
        else:
            d, e = l / v, ''
        el.append(dict(p=p, l=l, d=d, t=t, e=e))
        t += d
        prev = p[-1]
    koniec = t
    for c in dane['czubki']:                         # dociągnięcia do czubków
        k = el[c['kreska']]
        frac = min(1, dl(k['p'][:c['punkt'] + 2]) / max(1, k['l']))
        if k['e'].startswith('cubic-bezier(.3333,0'):
            frac = math.sqrt(frac)
        elif k['e']:
            frac = 1 - math.sqrt(1 - frac)
        q = c['pts']
        el.append(dict(p=q, l=dl(q), d=max(0.04, dl(q) / v), t=k['t'] + frac * k['d'], e=''))
    sciezki = ''.join(
        '<path d="M%s" style="--l:%d;--d:%ss;--t:%ss%s"/>' % (
            ' '.join('%d %d' % (round(x), round(y)) for x, y in k['p']), math.ceil(k['l']) + 2,
            liczba(k['d']), liczba(k['t']), (';--e:' + k['e']) if k['e'] else '')
        for k in el)
    box = dane['box']
    return ('<svg class="cin__svg" viewBox="0 0 %d %d" aria-hidden="true" focusable="false" data-koniec="%s">'
            '<defs><path id="cinT" d="%s"/><mask id="cinM" maskUnits="userSpaceOnUse" x="-400" y="-500" width="4500" height="2700">'
            '<g class="cin__pen" stroke-width="%d">%s</g></mask></defs>'
            '<use href="#cinT" class="cin__ghost"/><use href="#cinT" class="cin__ink" mask="url(#cinM)"/></svg>') % (
        box['w'], box['h'], liczba(koniec, 2), dane['d'], dane['pioro'], sciezki), koniec, len(el)


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    dane = json.load(open('_zrodla/intro_pioro.json'))
    kod, koniec, n = svg(dane)
    f = 'index.html'
    s = open(f, encoding='utf-8').read()
    nowy, ile = re.subn(r'<!-- >>> zbuduj_intro\.py -->.*?<!-- <<< zbuduj_intro\.py -->',
                        lambda m: '<!-- >>> zbuduj_intro.py -->' + kod + '<!-- <<< zbuduj_intro.py -->', s, flags=re.S)
    if ile != 1:
        raise SystemExit('brak znaczników zbuduj_intro.py w ' + f)
    if nowy != s:
        open(f, 'w', encoding='utf-8').write(nowy)
    print('intro: %d pociągnięć pióra, pisanie od %.2f do %.2f s, SVG %d znaków' % (n, START, koniec, len(kod)))


if __name__ == '__main__':
    main()
