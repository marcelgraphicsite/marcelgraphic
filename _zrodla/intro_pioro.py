# -*- coding: utf-8 -*-
"""Trasa pióra dla wejścia na stronę: logo „Marcel / GraphicSite” pisze się tak, jak pisze się je ręką.

Co robi (wynik: _zrodla/intro_pioro.json — z niego zbuduj_intro.py robi SVG w index.html):
  1. Kształty liter prosto z logo (assets/img/logo.svg, #logo — wektor 1:1 z obrazka Marcela, zbuduj_logo.py):
     „Marcel” nad „GraphicSite”, dokładnie jak na obrazku; linijki rozdzielone po przerwie bez tuszu.
  2. Szkielet każdej linijki osobno (środek każdej kreski), bez krótkich odrostów.
  3. Kolejność pisania jak ręką: „Marcel” od ogonka (zawijas w pętli „M”), „GraphicSite” od ogonka „G”;
     w każdym węźle najpierw haczyki/ogonki nad nim (od wolnego końca w dół — kreska w dół, jak w kaligrafii),
     potem najmniejszy skręt; gdy brak drogi — podniesienie pióra i powrót do ostatniego niedokończonego węzła
     (dzięki temu np. poprzeczka „t” i kropki nad „i” są na końcu, jak przy pisaniu).
  4. Dociągnięcia do ostrych czubków i kropek, których szkielet nie sięga.

Potrzebne (tylko do przeliczenia; sama strona ich nie używa):
  pip install fonttools freetype-py numpy scipy scikit-image skan pillow
Uruchom z katalogu repozytorium:  python3 _zrodla/intro_pioro.py  &&  python3 _zrodla/zbuduj_intro.py
Przelicz po zmianie logo (po python3 _zrodla/zbuduj_logo.py).
"""
import json
import math
import os
import re

import numpy as np
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.svgLib.path import parse_path
from scipy import ndimage as ndi
from skan import Skeleton, summarize
from skimage.morphology import skeletonize
from PIL import Image, ImageDraw

LOGO, META = 'assets/img/logo.svg', '_zrodla/logo/logo.json'
PIORO_EM = 0.112                # grubość pióra-maski (em); musi przykryć najgrubszą kreskę z zapasem
PX_EM = 500                     # raster roboczy: 1 em = 500 px (progi niżej są w tych pikselach)
START_EM = {0: (0.443, 0.398), 1: (0.125, 1.022)}   # ogonek „M” i ogonek „G” (em od lewego górnego rogu logo)
ZACZNIJ_OD_EM = {1: [(3.2175, 1.2175)]}             # inne litery od ogonka: haczyk „S” w „Site”


# ---------- 1. kształty liter (z logo) ----------
def kontury(d):
    """kontury ścieżki (każdy od bezwzględnego M) z punktami do obrysu prostokąta"""
    out = []
    for kd in re.findall(r'M[^M]*', d):
        toks = re.findall(r'[a-zA-Z]|-?\d+(?:\.\d+)?', kd)
        x = y = 0.0; cmd = None; pts = []; i = 0
        while i < len(toks):
            t = toks[i]
            if t.isalpha():
                cmd = t; i += 1
                if cmd in 'zZ':
                    continue
            n = {'M': 2, 'l': 2, 'L': 2, 'c': 6, 'C': 6}[cmd]
            v = [float(q) for q in toks[i:i + n]]; i += n
            if cmd == 'M':
                x, y = v; pts.append((x, y)); cmd = 'l'
            elif cmd in 'lc':
                for k in range(0, n, 2):
                    pts.append((x + v[k], y + v[k + 1]))
                x, y = x + v[-2], y + v[-1]
        out.append((kd, pts))
    return out


def linie_logo():
    svg = open(LOGO, encoding='utf-8').read()
    d = re.search(r'<path id="logo" fill-rule="evenodd" d="([^"]+)"', svg).group(1)
    meta = json.load(open(META))
    ks = kontury(d)
    l1 = [k for k in ks if max(p[1] for p in k[1]) < meta['podzial']]
    l2 = [k for k in ks if max(p[1] for p in k[1]) >= meta['podzial']]
    return d, meta, [''.join(k[0] for k in l1), ''.join(k[0] for k in l2)]


def okno(meta):
    em = meta['em']; SC = PX_EM / em
    vb = meta['viewBox']
    VBX, VBY = vb[0] - 0.25 * em, vb[1] - 0.25 * em
    VBW, VBH = vb[2] + 0.5 * em, vb[3] + 0.5 * em
    return SC, VBX, VBY, VBW, VBH


def raster(d_linii, SC, VBX, VBY, VBW, VBH):
    """biało-czarny raster linijki logo (FreeType, wypełnienie even-odd jak w SVG)"""
    W, H = round(VBW * SC), round(VBH * SC)
    pen = FreeTypePen(None)
    parse_path(d_linii, pen)                    # współrzędne SVG (y w dół)
    a = pen.array(width=W, height=H, transform=(SC, 0, 0, -SC, -VBX * SC, H + VBY * SC), evenOdd=True)
    return a > 0.5


# ---------- 2. szkielet ----------
def galezie(im):
    dist = ndi.distance_transform_edt(im)
    S = Skeleton(skeletonize(im))
    df = summarize(S, separator='_')
    br = []
    for i in range(S.n_paths):
        co = S.path_coordinates(i)[:, ::-1].astype(float)
        br.append(dict(id=i, pts=co, a=int(df['node_id_src'][i]), b=int(df['node_id_dst'][i]), L=float(df['branch_distance'][i]),
                       r=dist[co[:, 1].astype(int), co[:, 0].astype(int)]))
    return prune(sklej(br))


def stopnie(br):
    deg = {}
    for b in br:
        deg[b['a']] = deg.get(b['a'], 0) + 1
        deg[b['b']] = deg.get(b['b'], 0) + 1
    return deg


def sklej(br):
    """gałęzie przez węzły stopnia 2 → jedna gałąź"""
    while True:
        deg = stopnie(br)
        for n, d in deg.items():
            inc = [b for b in br if b['a'] == n or b['b'] == n]
            if d != 2 or len(inc) != 2:
                continue
            p, q = inc
            pp, pa, pr = (p['pts'], p['a'], p['r']) if p['b'] == n else (p['pts'][::-1], p['b'], p['r'][::-1])
            qq, qb, qr = (q['pts'], q['b'], q['r']) if q['a'] == n else (q['pts'][::-1], q['a'], q['r'][::-1])
            nb = dict(id=min(p['id'], q['id']), pts=np.vstack([pp, qq[1:]]), a=pa, b=qb, L=p['L'] + q['L'], r=np.concatenate([pr, qr[1:]]))
            br = [b for b in br if b is not p and b is not q] + [nb]
            break
        else:
            return br


def prune(br):
    """bez krótkich odrostów: gałąź z jednym wolnym końcem, krótsza niż ~grubość kreski"""
    while True:
        deg = stopnie(br)
        out = []
        for b in br:
            ea, eb = deg[b['a']] == 1, deg[b['b']] == 1
            if ea != eb and b['L'] < 1.25 * (b['r'][-1] if ea else b['r'][0]) + 6:
                continue
            out.append(b)
        if len(out) == len(br):
            return br
        br = sklej(out)


# ---------- 3. kolejność pisania ----------
def kierunek(pts, k=14):
    k = min(k, len(pts) - 1)
    v = pts[k] - pts[0] if k >= 1 else np.zeros(2)
    n = np.linalg.norm(v)
    return v / n if n else v


def trasa(br, start_xy, nad=10.0, drobne=12, preferowane=()):
    nodes = {}
    for b in br:
        nodes.setdefault(b['a'], b['pts'][0]); nodes.setdefault(b['b'], b['pts'][-1])
    deg = stopnie(br)
    used, kreski, odwiedzone = set(), [], []

    def orient(b, n):
        return (b['pts'], b['b']) if b['a'] == n else (b['pts'][::-1], b['a'])

    def drugi(b, n):
        return b['b'] if b['a'] == n else b['a']

    def wolne(n):
        return [b for b in br if id(b) not in used and (b['a'] == n or b['b'] == n)]

    def gorny(n):  # wolny koniec leżący wyżej niż większość swojej kreski
        if deg[n] != 1:
            return False
        pts, _ = orient(next(b for b in br if b['a'] == n or b['b'] == n), n)
        return pts[0][1] < np.median(pts[:, 1]) - 4

    def kawalek(n):  # węzły osiągalne po niedokończonych gałęziach
        seen, stos = {n}, [n]
        while stos:
            m = stos.pop()
            for b in wolne(m):
                o = drugi(b, m)
                if o not in seen:
                    seen.add(o); stos.append(o)
        return seen

    def caly(n):  # całe słowo (kawałek liter połączonych kreskami), niezależnie od tego, co już napisane
        seen, stos = {n}, [n]
        while stos:
            m = stos.pop()
            for b in br:
                if b['a'] == m or b['b'] == m:
                    o = drugi(b, m)
                    if o not in seen:
                        seen.add(o); stos.append(o)
        return seen

    def wyjscie(b, n):  # ogonek wyjściowy słowa: najbardziej wysunięty w prawo wolny koniec słowa — pióro kończy na nim
        t = drugi(b, n)
        konce = [m for m in caly(n) if deg[m] == 1]
        return t == max(konce, key=lambda m: nodes[m][0])

    def pisz(cur):
        out, kreska, kier = [], [nodes[cur][None, :]], None
        while True:
            for b in sorted([b for b in wolne(cur) if deg[drugi(b, cur)] == 1 and nodes[drugi(b, cur)][1] < nodes[cur][1] - nad
                             and len(wolne(cur)) > 1 and not wyjscie(b, cur)], key=lambda b: nodes[drugi(b, cur)][0]):
                pts, _ = orient(b, drugi(b, cur))       # haczyk: od wolnego końca w dół do węzła
                used.add(id(b))
                s = np.vstack(kreska)
                if len(s) > 1:
                    out.append(s)
                out.append(pts)
                kreska = [nodes[cur][None, :]]
                kier = -kierunek(pts[::-1])
            cand = wolne(cur)
            if not cand:
                break
            if kier is None or len(cand) == 1:
                pick = cand[0] if len(cand) == 1 else max(cand, key=lambda b: len(b['pts']))
            else:
                pick = max(cand, key=lambda b: float(np.dot(kier, kierunek(orient(b, cur)[0]))))
            pts, nxt = orient(pick, cur)
            used.add(id(pick)); odwiedzone.append(cur)
            kreska.append(pts[1:])
            kier = -kierunek(pts[::-1])
            cur = nxt
        s = np.vstack(kreska)
        if len(s) > 1:
            out.append(s)
        return out

    kreski += pisz(min([n for n in nodes if deg[n] == 1], key=lambda n: np.linalg.norm(nodes[n] - np.array(start_xy))))
    while any(id(b) not in used for b in br):
        wroc = next((n for n in reversed(odwiedzone) if wolne(n)), None)
        if wroc is None:   # nowy, rozłączny kawałek: najbardziej lewy „górny” wolny koniec
            konce = [n for n in nodes if deg[n] == 1 and wolne(n)]
            gora = [n for n in konce if gorny(n)]
            wroc = min(gora or konce or list({b['a'] for b in br if id(b) not in used}), key=lambda n: nodes[n][0])
            # ogonek, od którego ta litera się zaczyna (np. haczyk „S”), jeśli należy do tego samego kawałka
            k = kawalek(wroc)
            pref = [n for n in konce if n in k and any(np.linalg.norm(nodes[n] - np.array(p)) < 40 for p in preferowane)]
            if pref:
                wroc = pref[0]
        kreski += pisz(wroc)
    return [s for s in kreski if np.sum(np.linalg.norm(np.diff(s, axis=0), axis=1)) >= drobne]


def wygladz(p, sigma=3.0):
    if len(p) < 5:
        return p
    q = np.stack([ndi.gaussian_filter1d(p[:, 0], sigma, mode='nearest'), ndi.gaussian_filter1d(p[:, 1], sigma, mode='nearest')], 1)
    q[0], q[-1] = p[0], p[-1]
    return q


def rdp(p, eps):
    if len(p) < 3:
        return p
    a, b = p[0], p[-1]; ab = b - a; n = np.linalg.norm(ab)
    d = np.linalg.norm(p - a, axis=1) if n == 0 else np.abs(ab[0] * (p[:, 1] - a[1]) - ab[1] * (p[:, 0] - a[0])) / n
    i = int(np.argmax(d))
    return np.vstack([rdp(p[:i + 1], eps)[:-1], rdp(p[i:], eps)]) if d[i] > eps else np.vstack([a, b])


def jednostki(p):
    return np.stack([p[:, 0] / SC + VBX, p[:, 1] / SC + VBY], 1)


# ---------- 4. czubki poza zasięgiem pióra ----------
def czubki(im, kreski_u):
    px = lambda p: ((p[0] - VBX) * SC, (p[1] - VBY) * SC)
    m = Image.new('L', (im.shape[1], im.shape[0]), 0); d = ImageDraw.Draw(m); r = PIORO / 2 * SC
    for st in kreski_u:
        pts = [px(p) for p in st]
        d.line(pts, fill=255, width=int(round(2 * r)), joint='curve')
        for q in (pts[0], pts[-1]):
            d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=255)
    zle = im & ~ndi.binary_dilation(np.array(m) > 127, iterations=1)
    lab, n = ndi.label(zle)
    wszystkie = [(si, vi, np.array(px(p))) for si, st in enumerate(kreski_u) for vi, p in enumerate(st)]
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 3:
            continue
        plama = np.stack([xs, ys], 1).astype(float)
        si, vi, q = min(wszystkie, key=lambda t: np.linalg.norm(t[2] - plama.mean(0)))
        far = plama[np.argmax(np.linalg.norm(plama - q, axis=1))]
        v = far - q; v = v / (np.linalg.norm(v) or 1)
        to_u = lambda p: [round(p[0] / SC + VBX, 1), round(p[1] / SC + VBY, 1)]
        out.append(dict(kreska=si, punkt=vi, pts=[to_u(q), to_u(far + v * 3)]))
    return out


def main():
    global SC, VBX, VBY, VBW, VBH, PIORO
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    d, meta, linie = linie_logo()
    SC, VBX, VBY, VBW, VBH = okno(meta)
    em = meta['em']
    PIORO = round(PIORO_EM * em)
    wynik = dict(box=dict(w=meta['viewBox'][2], h=meta['viewBox'][3]), em=em, d=d, pioro=PIORO, kreski=[], czubki=[], linie=[])
    for li, dl in enumerate(linie):
        im = raster(dl, SC, VBX, VBY, VBW, VBH)
        sx, sy = START_EM[li]
        pref = [((x * em - VBX) * SC, (y * em - VBY) * SC) for x, y in ZACZNIJ_OD_EM.get(li, [])]
        kreski = trasa(galezie(im), ((sx * em - VBX) * SC, (sy * em - VBY) * SC), preferowane=pref)
        ku = [jednostki(rdp(wygladz(s), 0.5)).round(1).tolist() for s in kreski]
        off = len(wynik['kreski'])
        wynik['czubki'] += [dict(c, kreska=c['kreska'] + off) for c in czubki(im, ku)]
        wynik['kreski'] += ku
        wynik['linie'].append(off)
        print('linijka %d: %d pociągnięć, %d dociągnięć do czubków' % (li + 1, len(ku), sum(1 for c in wynik['czubki'] if c['kreska'] >= off)))
    json.dump(wynik, open('_zrodla/intro_pioro.json', 'w'), separators=(',', ':'))
    print('zapisano _zrodla/intro_pioro.json')


if __name__ == '__main__':
    main()
