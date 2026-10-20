# -*- coding: utf-8 -*-
"""Logo „Marcel / GraphicSite” jako wektor 1:1 z obrazka Marcela (_zrodla/logo/logo-marcel-graphicsite.png).

Bez dopasowywania i przerysowywania: obrys (potrace) dokładnie tego, co jest na obrazku, w 2× rozdzielczości
(gładkie krzywe). Wynik: assets/img/logo.svg — jedna ścieżka id="logo", bez koloru (na stronie przez
<svg><use href="assets/img/logo.svg#logo"/></svg> bierze kolor tekstu, fill: currentColor).

Potrzebne (tylko do przeliczenia): pip install potracer numpy pillow
Uruchom z katalogu repozytorium:  python3 _zrodla/zbuduj_logo.py   (po podmianie obrazka logo)
"""
import math
import os

import numpy as np
import potrace
import potrace.potrace as _pp
from PIL import Image

ZRODLO = '_zrodla/logo/logo-marcel-graphicsite.png'
WYNIK = 'assets/img/logo.svg'
UP = 2        # obrys w 2× rozdzielczości (dokładność 0,5 px obrazka)
MARGINES = 6  # px obrazka wokół tuszu


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
    d = []
    for k in krzywe:
        cur = R(k.start_point)
        d.append('M%d %d' % cur)
        last = None
        for s in k.segments:
            if s.is_corner:
                c, e = R(s.c), R(s.end_point)
                czesci = [('l', [(c[0] - cur[0], c[1] - cur[1])]), ('l', [(e[0] - c[0], e[1] - c[1])])]
            else:
                c1, c2, e = R(s.c1), R(s.c2), R(s.end_point)
                czesci = [('c', [(c1[0] - cur[0], c1[1] - cur[1]), (c2[0] - cur[0], c2[1] - cur[1]), (e[0] - cur[0], e[1] - cur[1])])]
            cur = e
            for cmd, pts in czesci:
                nums = ' '.join('%d %d' % p for p in pts).replace(' -', '-')
                d.append((('' if nums.startswith('-') else ' ') + nums) if cmd == last else cmd + nums)
                last = cmd
        d.append('z')
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><title>Marcel GraphicSite</title>'
           '<path id="logo" fill-rule="evenodd" d="%s"/></svg>\n') % (big.width, big.height, ''.join(d))
    open(WYNIK, 'w', encoding='utf-8').write(svg)
    print('logo: %s — viewBox 0 0 %d %d (proporcje %.4f), %d konturów, %d znaków' % (WYNIK, big.width, big.height, big.width / big.height, len(krzywe), len(svg)))


if __name__ == '__main__':
    main()
