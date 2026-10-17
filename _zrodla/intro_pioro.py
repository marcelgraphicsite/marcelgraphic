# -*- coding: utf-8 -*-
"""Trasa pióra dla wejścia na stronę: logo „Marcel / Struszczak” pisze się tak, jak pisze się je ręką.

Co robi (wynik: _zrodla/intro_pioro.json — z niego zbuduj_intro.py robi SVG w index.html):
  1. Kształty liter prosto z kroju GV Script (assets/fonts/gv-script.woff2), ułożone jak w CSS
     (HarfBuzz z kerningiem, letter-spacing -.01em, interlinia .82) — ścieżki SVG w jednostkach fontu (1 em = 1000).
  2. Szkielet każdej linijki osobno (środek każdej kreski), bez krótkich odrostów.
  3. Kolejność pisania jak ręką: „Marcel” od ogonka (zawijas w pętli „M”), „Struszczak” od haczyka „S”;
     w każdym węźle najpierw haczyki/ogonki nad nim (od wolnego końca w dół — kreska w dół, jak w kaligrafii),
     potem najmniejszy skręt; gdy brak drogi — podniesienie pióra i powrót do ostatniego niedokończonego węzła
     (dzięki temu np. poprzeczka „t” jest na końcu, jak przy pisaniu).
  4. Dociągnięcia do ostrych czubków, których szkielet nie sięga (np. koniec haczyka „c”, stopka „k”).

Potrzebne (tylko do przeliczenia; sama strona ich nie używa):
  pip install fonttools brotli uharfbuzz freetype-py numpy scipy scikit-image skan pillow
Uruchom z katalogu repozytorium:  python3 _zrodla/intro_pioro.py  &&  python3 _zrodla/zbuduj_intro.py
Przelicz tylko po zmianie napisu, kroju, odstępu liter albo interlinii logo w intro.
"""
import io
import json
import math
import os

import numpy as np
import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from scipy import ndimage as ndi
from skan import Skeleton, summarize
from skimage.morphology import skeletonize
from PIL import Image, ImageDraw

KROJ = 'assets/fonts/gv-script.woff2'
LINIE = ('Marcel', 'Struszczak')
LS, LH = -0.01, 0.82            # letter-spacing i interlinia (em) — jak .cin__svg w style.css
PIORO = 112                     # grubość pióra-maski (jednostki fontu); musi przykryć najgrubszą kreskę z zapasem
SC, VBX, VBY, VBW, VBH = 0.5, -300, -400, 4300, 2500   # raster roboczy: 0,5 px na jednostkę
START = {0: (318, 296), 1: (588, 626)}                 # ogonek „M” i haczyk „S” (piksele rastra roboczego)


# ---------- 1. kształty liter ----------
def font():
    tt = TTFont(KROJ)
    tt.flavor = None
    buf = io.BytesIO(); tt.save(buf)
    face = hb.Face(hb.Blob(buf.getvalue()))
    return tt, hb.Font(face)


class RelPen(BasePen):
    """Zwarta ścieżka SVG: komendy względne, współrzędne całkowite (bez kumulacji zaokrągleń), y w dół."""
    def __init__(self, gs, dx, dy):
        super().__init__(gs); self.dx, self.dy = dx, dy; self.out = []; self.cur = self.start = (0, 0)

    def P(self, p):
        return (round(p[0] + self.dx), round(self.dy - p[1]))

    def rel(self, a):
        return (a[0] - self.cur[0], a[1] - self.cur[1])

    def _moveTo(self, p):
        a = self.P(p); self.out.append(('M', [a])); self.cur = self.start = a

    def _lineTo(self, p):
        a = self.P(p); self.out.append(('l', [self.rel(a)])); self.cur = a

    def _qCurveToOne(self, p1, p2):
        a, b = self.P(p1), self.P(p2); self.out.append(('q', [self.rel(a), self.rel(b)])); self.cur = b

    def _curveToOne(self, p1, p2, p3):
        a, b, c = self.P(p1), self.P(p2), self.P(p3); self.out.append(('c', [self.rel(a), self.rel(b), self.rel(c)])); self.cur = c

    def _closePath(self):
        self.out.append(('z', [])); self.cur = self.start


def svg_d(cmds):
    s, last = [], None
    for c, pts in cmds:
        nums = ' '.join('%d %d' % p for p in pts).replace(' -', '-')
        s.append(((' ' if nums and not nums.startswith('-') else '') + nums) if c == last and c != 'M' else c + nums)
        last = c
    return ''.join(s)


def uloz(tt, hbf):
    gs, order, upm = tt.getGlyphSet(), tt.getGlyphOrder(), tt['head'].unitsPerEm
    asc, desc = tt['hhea'].ascent, -tt['hhea'].descent
    base = [round(LH * upm / 2 - (asc + desc) / 2 + asc)]
    base.append(base[0] + round(LH * upm))
    linie = []
    for li, text in enumerate(LINIE):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(hbf, buf, {})
        x, cmds, glify = 0.0, [], []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = order[info.codepoint]
            pen = RelPen(gs, x + pos.x_offset, base[li] - pos.y_offset); gs[name].draw(pen)
            cmds += pen.out; glify.append((name, x + pos.x_offset, pos.y_offset)); x += pos.x_advance + LS * upm
        linie.append(dict(d=svg_d(cmds), glify=glify, w=x - LS * upm, base=base[li]))
    return linie, gs


def raster(gs, linia):
    """biało-czarny raster linijki (0,5 px na jednostkę, okno VB) — FreeType, wypełnienie nonzero"""
    W, H = round(VBW * SC), round(VBH * SC)
    pen = FreeTypePen(gs)
    for name, x, yo in linia['glify']:
        gs[name].draw(TransformPen(pen, (1, 0, 0, 1, x, yo)))
    a = pen.array(width=W, height=H, transform=(SC, 0, 0, SC, -VBX * SC, H - (linia['base'] - VBY) * SC))
    return a > 0.5                                 # pokrycie piksela tuszem 0..1


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


def trasa(br, start_xy, nad=10.0, drobne=12):
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

    def pisz(cur):
        out, kreska, kier = [], [nodes[cur][None, :]], None
        while True:
            for b in sorted([b for b in wolne(cur) if deg[drugi(b, cur)] == 1 and nodes[drugi(b, cur)][1] < nodes[cur][1] - nad
                             and len(wolne(cur)) > 1], key=lambda b: nodes[drugi(b, cur)][0]):
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
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    tt, hbf = font()
    linie, gs = uloz(tt, hbf)
    wynik = dict(box=dict(w=round(max(l['w'] for l in linie)), h=round(2 * LH * 1000)), d=''.join(l['d'] for l in linie),
                 pioro=PIORO, kreski=[], czubki=[], linie=[])
    for li, l in enumerate(linie):
        im = raster(gs, l)
        kreski = trasa(galezie(im), START[li])
        ku = [jednostki(rdp(wygladz(s), 0.5)).round(1).tolist() for s in kreski]
        off = len(wynik['kreski'])
        wynik['czubki'] += [dict(c, kreska=c['kreska'] + off) for c in czubki(im, ku)]
        wynik['kreski'] += ku
        wynik['linie'].append(off)
        print('linijka %d (%s): %d pociągnięć, %d dociągnięć do czubków' % (li + 1, LINIE[li], len(ku), sum(1 for c in wynik['czubki'] if c['kreska'] >= off)))
    json.dump(wynik, open('_zrodla/intro_pioro.json', 'w'), separators=(',', ':'))
    print('zapisano _zrodla/intro_pioro.json')


if __name__ == '__main__':
    main()
