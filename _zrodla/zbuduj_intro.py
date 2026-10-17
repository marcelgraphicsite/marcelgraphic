# -*- coding: utf-8 -*-
"""Ruch wypełniania logo na wejściu strony (#cinema): litera po literze — najpierw „Marcel”, potem „Struszczak”.

Miękka krawędź bieli to „pióro”, które biegnie po ścieżce tuszu: przez cały tusz „Marcel”, a potem bez przerwy
przez tusz „Struszczak”. Tempo: łagodny rozbieg (ROZBIEG), potem STAŁA prędkość (TEMPO — każda litera wypełnia
się po kolei, w tym samym rytmie), na końcu miękkie wyhamowanie (HAMOWANIE). Rozbieg i hamowanie mają stałe
przyspieszenie, więc prędkość zmienia się płynnie, bez skoków.

Każda linijka ma swoje okno (.cin__f), które jedzie tylko wtedy, gdy pióro przechodzi przez jej zakres.
Wycinek takiego ruchu to dokładnie krzywa cubic-bezier (paraboli albo prostej), więc @keyframes są małe
i dokładne; obie animacje mają ten sam czas i start, więc idą idealnie razem. Wszystko na transformacjach —
liczy karta graficzna, nie zamarza przy wczytywaniu strony.

Uruchom z katalogu repozytorium:  python3 _zrodla/zbuduj_intro.py
Wpisuje animacje cinW1/cinI1/cinW2/cinI2 (i ich czas) do assets/css/style.css, między znaczniki zbuduj_intro.py.
TUSZ to zmierzone (w em) szerokości i krawędzie tuszu napisów w kroju GV Script przy letter-spacing -.01em:
zmierz ponownie, jeśli zmieni się napis, krój, odstęp liter albo interlinia (LH).
"""
import math
import os
import re

TEMPO = 3.0                        # em/s — prędkość pióra w środku (mała litera ≈ 0,1 s, „M” ≈ 0,45 s)
ROZBIEG, HAMOWANIE = 0.45, 0.55    # s — łagodny start i miękkie wyhamowanie
OPOZNIENIE = 0.15                  # s — zanim pióro ruszy (przygaszony napis już widać)
TUSZ = [  # adv: szerokość tekstu; ink_l / ink_r: tusz od początku tekstu (em)
    dict(adv=2.6418, ink_l=0.0206, ink_r=2.7877),   # Marcel
    dict(adv=3.6199, ink_l=0.0508, ink_r=3.6950),   # Struszczak
]
LH = 0.82                          # interlinia napisu (.cin__name)
PL, PR = 0.25, 0.93                # padding linijki (.cin__l) z lewej i z prawej, em (jak w style.css)
KAT = math.radians(100)            # kąt maski (lekki skos jak w piśmie)
MASKA = (0.78, 0.36)               # maska: pełna do 100% - .78em, przezroczysta od 100% - .36em
EPS = 0.03

H = LH + 0.6                       # wysokość okna: linia + padding .3em u góry i u dołu
COT, SIN = abs(math.cos(KAT) / math.sin(KAT)), math.sin(KAT)
X_PELNA = H / 2 * COT - MASKA[0] / SIN       # krawędź maski na środku wysokości, od prawego brzegu okna
X_PUSTA = H / 2 * COT - MASKA[1] / SIN
SRODEK = (X_PELNA + X_PUSTA) / 2
GORA, DOL = 0.6 * COT, 0.33 * COT            # tusz sięga ~.6em nad i ~.33em pod środek okna


def liczba(v):
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    if s in ('', '-0'):
        s = '0'
    return s.replace('0.', '.', 1) if s.startswith('0.') else s.replace('-0.', '-.', 1)


def ruch():
    """Geometria okien + profil ruchu pióra. Zwraca (linie, czas D w s, funkcje s(t), s'(t), granice odcinków)."""
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
    S = hi - lo                                                    # cała droga pióra (em)
    D = ROZBIEG + HAMOWANIE + (S - TEMPO * (ROZBIEG + HAMOWANIE) / 2) / TEMPO
    ta, tc = ROZBIEG / D, HAMOWANIE / D
    vm = 1 / (1 - ta / 2 - tc / 2)                                 # prędkość w środku (droga 0..1 na czas 0..1)

    def s_(t):
        if t <= ta:
            return vm * t * t / (2 * ta)
        if t <= 1 - tc:
            return vm * ta / 2 + vm * (t - ta)
        return 1 - vm * (1 - t) ** 2 / (2 * tc)

    def v_(t):
        return vm * t / ta if t <= ta else vm if t <= 1 - tc else vm * (1 - t) / tc

    def t_(s):
        lo_, hi_ = 0.0, 1.0
        for _ in range(90):
            m = (lo_ + hi_) / 2
            if s_(m) < s:
                lo_ = m
            else:
                hi_ = m
        return (lo_ + hi_) / 2

    for L in linie:
        L['sa'], L['sb'] = (L['a'] - lo) / S, (L['b'] - lo) / S
        L['ta'], L['tb'] = t_(L['sa']), t_(L['sb'])
    return linie, D, s_, v_, (ta, 1 - tc), S, lo


def keyframes():
    linie, D, s_, v_, granice, _, _ = ruch()
    out = []
    for i, L in enumerate(linie, 1):
        pkt = [L['ta']] + [g for g in granice if L['ta'] + 1e-6 < g < L['tb'] - 1e-6] + [L['tb']]
        f = lambda t: (s_(t) - L['sa']) / (L['sb'] - L['sa'])
        for nazwa, znak in (('cinW%d' % i, ''), ('cinI%d' % i, '-')):
            start = 'calc(%s100%% %s %sem)' % ('-' if not znak else '', '+' if not znak else '-', liczba(L['K']))

            def poz(fr):
                if fr <= 1e-6:
                    return 'translate3d(%s,0,0)' % start
                if fr >= 1 - 1e-6:
                    return 'translate3d(0,0,0)'
                return 'translate3d(calc((%s) * %s),0,0)' % (start[5:-1], liczba(1 - fr))
            klatki = []
            for j in range(len(pkt) - 1):
                t1, t2 = pkt[j], pkt[j + 1]
                ds = s_(t2) - s_(t1)
                a = v_(t1) * (t2 - t1) / ds if ds > 0 else 1                # nachylenie na starcie wycinka
                tf = 'linear' if abs(a - 1) < 1e-4 else 'cubic-bezier(.3333,%s,.6667,%s)' % (liczba(a / 3), liczba((a + 1) / 3))
                sel = ('0%%,%s%%' % liczba(t1 * 100)) if (j == 0 and t1 > 1e-6) else ('0%' if j == 0 else '%s%%' % liczba(t1 * 100))
                klatki.append('%s{transform:%s;animation-timing-function:%s}' % (sel, poz(f(t1)), tf))
            koniec = 'to' if L['tb'] > 1 - 1e-6 else '%s%%,to' % liczba(L['tb'] * 100)
            klatki.append('%s{transform:translate3d(0,0,0)}' % koniec)
            out.append('@keyframes %s{%s}' % (nazwa, ''.join(klatki)))
    czas = '%ss' % liczba(round(D, 2))
    opoz = '%ss' % liczba(OPOZNIENIE)
    css = ['.js #cinema .cin__f{animation:cinW1 %s linear %s both}' % (czas, opoz),
           '.js #cinema .cin__f>span{animation:cinI1 %s linear %s both}' % (czas, opoz),
           '.js #cinema .cin__l+.cin__l .cin__f{animation-name:cinW2}',
           '.js #cinema .cin__l+.cin__l .cin__f>span{animation-name:cinI2}']
    return '\n'.join(css + out), D


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    f = 'assets/css/style.css'
    s = open(f, encoding='utf-8').read()
    kf, D = keyframes()
    blok = '/* >>> zbuduj_intro.py */\n' + kf + '\n/* <<< zbuduj_intro.py */'
    nowy, n = re.subn(r'/\* >>> zbuduj_intro\.py \*/.*?/\* <<< zbuduj_intro\.py \*/', lambda m: blok, s, flags=re.S)
    if n != 1:
        raise SystemExit('brak znaczników zbuduj_intro.py w ' + f)
    if nowy != s:
        open(f, 'w', encoding='utf-8').write(nowy)
    print('intro: wypełnianie %.2f s (+%.2f s opóźnienia) — keyframes %s' % (D, OPOZNIENIE, 'zaktualizowane' if nowy != s else 'bez zmian'))


if __name__ == '__main__':
    main()
