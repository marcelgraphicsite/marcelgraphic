# -*- coding: utf-8 -*-
"""Ruch wypełniania logo na wejściu strony (#cinema): najpierw „Marcel”, potem „Struszczak” — jednym ruchem.

Miękka krawędź bieli biegnie po „ścieżce tuszu”: przez cały tusz „Marcel”, a potem bez przerwy przez tusz
„Struszczak”, po jednej łagodnej krzywej (KRZYWA). Każda linijka ma swoje okno (.cin__f), które jedzie tylko
wtedy, gdy ścieżka przechodzi przez jego zakres. Fragment krzywej Béziera to znowu krzywa Béziera, więc ruch
każdej linijki jest zapisany dokładnie jako cubic-bezier w @keyframes; obie animacje mają ten sam czas i start
(style.css: 1.9s, opóźnienie .15s), więc idą idealnie razem. Wszystko na transformacjach — liczy karta graficzna.

Uruchom z katalogu repozytorium:  python3 _zrodla/zbuduj_intro.py
Wpisuje @keyframes cinW1/cinI1/cinW2/cinI2 do assets/css/style.css (między znacznikami zbuduj_intro.py).
TUSZ to zmierzone (w em) szerokości i krawędzie tuszu napisów w kroju GV Script: zmierz ponownie,
jeśli zmieni się napis, krój albo odstęp liter (ink = skrajne białe piksele zrzutu w stosunku do początku tekstu).
"""
import math
import os
import re

KRZYWA = (0.37, 0.0, 0.63, 1.0)    # łagodny start i koniec, prawie stałe tempo w środku
TUSZ = [  # adv: szerokość tekstu; ink_l / ink_r: tusz od początku tekstu (em, krój GV Script, letter-spacing .01em)
    dict(adv=2.7616, ink_l=0.0197, ink_r=2.8877),   # Marcel
    dict(adv=3.8198, ink_l=0.0500, ink_r=3.8756),   # Struszczak
]
PL, PR = 0.25, 1.15                # padding linijki (.cin__l) z lewej i z prawej, em
KAT = math.radians(100)            # kąt maski (lekki skos jak w piśmie)
H = 0.9 + 0.6                      # wysokość okna: linia .9em + padding .3em u góry i u dołu
MASKA = (0.95, 0.40)               # maska: pełna do 100% - .95em, przezroczysta od 100% - .4em
EPS = 0.03

COT, SIN = abs(math.cos(KAT) / math.sin(KAT)), math.sin(KAT)
X_PELNA = H / 2 * COT - MASKA[0] / SIN       # krawędź maski na środku wysokości, od prawego brzegu okna
X_PUSTA = H / 2 * COT - MASKA[1] / SIN
SRODEK = (X_PELNA + X_PUSTA) / 2
GORA, DOL = 0.6 * COT, 0.33 * COT            # tusz sięga ~.6em nad i ~.33em pod środek okna


def bez(p0, p1, p2, p3, u):
    return (1 - u) ** 3 * p0 + 3 * (1 - u) ** 2 * u * p1 + 3 * (1 - u) * u ** 2 * p2 + u ** 3 * p3


def odwrotnie(f, v):
    lo, hi = 0.0, 1.0
    for _ in range(90):
        m = (lo + hi) / 2
        if f(m) < v:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def podziel(P, u):
    lerp = lambda a, b: (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
    a, b, c = lerp(P[0], P[1]), lerp(P[1], P[2]), lerp(P[2], P[3])
    d, e = lerp(a, b), lerp(b, c)
    f = lerp(d, e)
    return [P[0], a, d, f], [f, e, c, P[3]]


def liczba(v):
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    if s in ('', '-0'):
        s = '0'
    return s.replace('0.', '.', 1) if s.startswith('0.') else s.replace('-0.', '-.', 1)


def keyframes():
    linie = []
    for t in TUSZ:
        s, e, W = PL + t['ink_l'], PL + t['ink_r'], PL + t['adv'] + PR
        K = math.floor((s - EPS - X_PUSTA - GORA) * 100) / 100     # start: ani odrobiny bieli na tuszu
        assert (W + X_PELNA - DOL) - e > EPS, 'za mały prawy padding'  # koniec (translate 0): cały biały
        linie.append(dict(s=s, e=e, K=K, c0=K + SRODEK, c1=W + SRODEK))
    przes = [0.0, linie[0]['e'] - linie[0]['s']]                  # „Struszczak” zaczyna się tam, gdzie kończy „Marcel”
    for L, o in zip(linie, przes):
        L['a'], L['b'] = L['c0'] - L['s'] + o, L['c1'] - L['s'] + o
    lo, hi = linie[0]['a'], linie[1]['b']
    P = [(0, 0), KRZYWA[:2], KRZYWA[2:], (1, 1)]
    by = lambda u: bez(0, KRZYWA[1], KRZYWA[3], 1, u)
    out = []
    for i, L in enumerate(linie, 1):
        ua, ub = odwrotnie(by, (L['a'] - lo) / (hi - lo)), odwrotnie(by, (L['b'] - lo) / (hi - lo))
        _, R = podziel(P, ua)
        Q, _ = podziel(R, (ub - ua) / (1 - ua) if ua < 1 else 1)
        (x0, y0), (x3, y3) = Q[0], Q[3]
        cb = [(Q[1][0] - x0) / (x3 - x0), (Q[1][1] - y0) / (y3 - y0), (Q[2][0] - x0) / (x3 - x0), (Q[2][1] - y0) / (y3 - y0)]
        cb[0], cb[2] = min(max(cb[0], 0), 1), min(max(cb[2], 0), 1)
        tf = 'cubic-bezier(%s)' % ','.join(liczba(v) for v in cb)
        for nazwa, start in (('cinW%d' % i, 'calc(-100%% + %sem)' % liczba(L['K'])), ('cinI%d' % i, 'calc(100%% - %sem)' % liczba(L['K']))):
            t0 = 'transform:translate3d(%s,0,0)' % start
            if x0 < 1e-6:
                body = '0%%{%s;animation-timing-function:%s}%s%%,to{transform:translate3d(0,0,0)}' % (t0, tf, liczba(x3 * 100))
            else:
                body = '0%%,%s%%{%s;animation-timing-function:%s}to{transform:translate3d(0,0,0)}' % (liczba(x0 * 100), t0, tf)
            out.append('@keyframes %s{%s}' % (nazwa, body))
    return '\n'.join(out)


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    f = 'assets/css/style.css'
    s = open(f, encoding='utf-8').read()
    blok = '/* >>> zbuduj_intro.py */\n' + keyframes() + '\n/* <<< zbuduj_intro.py */'
    nowy, n = re.subn(r'/\* >>> zbuduj_intro\.py \*/.*?/\* <<< zbuduj_intro\.py \*/', lambda m: blok, s, flags=re.S)
    if n != 1:
        raise SystemExit('brak znaczników zbuduj_intro.py w ' + f)
    if nowy != s:
        open(f, 'w', encoding='utf-8').write(nowy)
    print('intro: keyframes ' + ('zaktualizowane' if nowy != s else 'bez zmian'))


if __name__ == '__main__':
    main()
