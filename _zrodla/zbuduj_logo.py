# -*- coding: utf-8 -*-
"""Logo „Marcel / GraphicSite” jako wektor 1:1 z obrazka Marcela (_zrodla/logo/logo-marcel-graphicsite.png).

Bez dopasowywania i przerysowywania: obrys (potrace) dokładnie tego, co jest na obrazku, w 2× rozdzielczości
(gładkie krzywe). Wynik: assets/img/logo.svg — ścieżka id="logo" (jak na obrazku: „Marcel” nad „GraphicSite”)
i id="logo-line" (te same kształty, słowa obok siebie — stopka), bez koloru: na stronie przez
<svg><use href="assets/img/logo.svg#logo"/></svg> bierze kolor tekstu (fill: currentColor).
Wymiary i linie bazowe dla intra: _zrodla/logo/logo.json.

Potrzebne (tylko do przeliczenia): pip install potracer numpy pillow
Uruchom z katalogu repozytorium:  python3 _zrodla/zbuduj_logo.py   (po podmianie obrazka logo)
"""
import json
import math
import os
import re

import numpy as np
import potrace
import potrace.potrace as _pp
from PIL import Image

ZRODLO = '_zrodla/logo/logo-marcel-graphicsite.png'
WYNIK = 'assets/img/logo.svg'
UP = 2        # obrys w 2× rozdzielczości (dokładność 0,5 px obrazka)
MARGINES = 6  # px obrazka wokół tuszu
# pomiary z obrazka (px obrazka 2160×2160) — tylko do ustawienia słów obok siebie, kształtów nie zmieniają:
EM = 400            # wielkość liter: 1 em kroju GV Script (Great Vibes) = 400 px obrazka
MARCEL_BAZA = 978   # linia bazowa „Marcel”
GRAPHIC_BAZA = 1358 # linia bazowa „GraphicSite”
ODSTEP_G = 1190.2   # w jednej linii „G” zaczyna się tyle za początkiem „M”: Marcel + spacja w kroju + .12 em (inaczej zawijas „G” dotyka „l”)


class _BezpiecznaMatematyka:
    """jak w potrace w C: pierwiastek z liczby ujemnej daje NaN (porównania wychodzą fałszywe), a nie wyjątek"""
    def __getattr__(self, k):
        return getattr(math, k)

    @staticmethod
    def sqrt(x):
        return math.sqrt(x) if x >= 0 else float('nan')


_pp.math = _BezpiecznaMatematyka()


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    im = Image.open(ZRODLO).convert('L')
    ys, xs = np.nonzero(np.array(im) < 128)
    x0, y0 = xs.min() - MARGINES, ys.min() - MARGINES
    x1, y1 = xs.max() + MARGINES + 1, ys.max() + MARGINES + 1
    big = im.crop((x0, y0, x1, y1))
    big = big.resize((big.width * UP, big.height * UP), Image.LANCZOS)
    tlo = np.array(big) >= 128            # potracer: wypełnione = False (tusz), tło = True
    krzywe = potrace.Bitmap(tlo).trace(turdsize=4, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
                                       alphamax=1.0, opticurve=True, opttolerance=0.2)
    R = lambda p: (int(round(p.x)), int(round(p.y)))
    kontury = []                          # (ścieżka konturu od bezwzględnego M, punkty do obrysu prostokąta)
    for k in krzywe:
        cur = R(k.start_point)
        d, pts, last = ['M%d %d' % cur], [cur], None
        for s in k.segments:
            if s.is_corner:
                c, e = R(s.c), R(s.end_point)
                czesci = [('l', [(c[0] - cur[0], c[1] - cur[1])]), ('l', [(e[0] - c[0], e[1] - c[1])])]
                pts += [c, e]
            else:
                c1, c2, e = R(s.c1), R(s.c2), R(s.end_point)
                czesci = [('c', [(c1[0] - cur[0], c1[1] - cur[1]), (c2[0] - cur[0], c2[1] - cur[1]), (e[0] - cur[0], e[1] - cur[1])])]
                pts += [c1, c2, e]
            cur = e
            for cmd, ps in czesci:
                nums = ' '.join('%d %d' % p for p in ps).replace(' -', '-')
                d.append((('' if nums.startswith('-') else ' ') + nums) if cmd == last else cmd + nums)
                last = cmd
        d.append('z')
        kontury.append((''.join(d), pts))

    # linijki: „Marcel” nad przerwą bez tuszu, „GraphicSite” pod nią (kształty bez zmian)
    wiersze = (np.array(big) < 128).any(1)
    srodek = len(wiersze) // 2
    puste = [y for y in range(srodek - len(wiersze) // 4, srodek + len(wiersze) // 4) if not wiersze[y]]
    podzial = (min(puste) + max(puste)) / 2 if puste else srodek
    l1 = [k for k in kontury if max(p[1] for p in k[1]) < podzial]
    l2 = [k for k in kontury if max(p[1] for p in k[1]) >= podzial]

    # wersja w jednej linii (stopka): „GraphicSite” przesunięte obok „Marcel” — na wspólną linię bazową,
    # „G” tam, gdzie stanęłoby w kroju po spacji (pomiary z obrazka, w px obrazka)
    dx = round(ODSTEP_G * UP)
    dy = round((MARCEL_BAZA - GRAPHIC_BAZA) * UP)
    def przesun(kd):  # kontur zaczyna się bezwzględnym „M x y”, dalej same komendy względne
        m = re.match(r'M(-?\d+) (-?\d+)', kd)
        return 'M%d %d' % (int(m.group(1)) + dx, int(m.group(2)) + dy) + kd[m.end():]
    linia = ''.join(k[0] for k in l1) + ''.join(przesun(k[0]) for k in l2)
    xs_ = [p[0] for k in l1 for p in k[1]] + [p[0] + dx for k in l2 for p in k[1]]
    ys_ = [p[1] for k in l1 for p in k[1]] + [p[1] + dy for k in l2 for p in k[1]]
    lb = (min(xs_) - 8, min(ys_) - 8, max(xs_) - min(xs_) + 16, max(ys_) - min(ys_) + 16)

    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><title>Marcel GraphicSite</title>'
           '<defs><path id="logo-line" fill-rule="evenodd" d="%s"/></defs>'
           '<path id="logo" fill-rule="evenodd" d="%s"/></svg>\n') % (big.width, big.height, linia, ''.join(k[0] for k in kontury))
    open(WYNIK, 'w', encoding='utf-8').write(svg)
    meta = dict(viewBox=[0, 0, big.width, big.height], em=round(EM * UP), podzial=podzial,
                baza=[round((MARCEL_BAZA - y0) * UP), round((GRAPHIC_BAZA - y0) * UP)],
                linia=dict(viewBox=list(lb), dx=dx, dy=dy), kontury=[len(l1), len(l2)])
    json.dump(meta, open('_zrodla/logo/logo.json', 'w'), indent=1)
    print('logo: %s — viewBox 0 0 %d %d, %d konturów (Marcel %d, GraphicSite %d), %d znaków' % (WYNIK, big.width, big.height, len(kontury), len(l1), len(l2), len(svg)))
    print('jedna linia (#logo-line): viewBox %s' % ' '.join(str(v) for v in lb))


if __name__ == '__main__':
    main()
