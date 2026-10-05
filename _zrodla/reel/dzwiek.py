#!/usr/bin/env python3
"""Ścieżka dźwiękowa reela: własna muzyka (100 BPM, zgodna z taktami scen) + efekty pod akcje z filmu.
Użycie: python3 dzwiek.py zdarzenia.json scenariusz.json wyjscie.wav
Wszystko syntetyzowane od zera (numpy) — bez cudzych sampli i licencji."""
import json, sys
import numpy as np

SR = 48000
rng = np.random.default_rng(7)
ev = json.load(open(sys.argv[1]))
SCN = json.load(open(sys.argv[2]))
OUT = sys.argv[3]
BPM = SCN['BPM']; BEAT = 60 / BPM; BAR = 4 * BEAT
TOTAL = SCN['total'] + 0.6
N = int(TOTAL * SR)
start = {s['id']: s['start'] for s in SCN['scenes']}

def t_(sec): return np.arange(int(sec * SR)) / SR
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)

class Bus:
    def __init__(self): self.x = np.zeros((2, N))
    def add(self, sig, at, gain=1.0, pan=0.0):
        i = int(at * SR)
        if i >= N or len(sig) == 0: return
        if i < 0: sig = sig[-i:]; i = 0
        n = min(len(sig), N - i)
        l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
        if sig.ndim == 1:
            self.x[0, i:i + n] += sig[:n] * gain * l * 1.414
            self.x[1, i:i + n] += sig[:n] * gain * r * 1.414
        else:
            self.x[0, i:i + n] += sig[0, :n] * gain
            self.x[1, i:i + n] += sig[1, :n] * gain

# ---------- filtry ----------
def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); z = 0.0
    # wektorowo przez lfilter-podobną pętlę w numpy (krótkie sygnały) — dla długich używamy biquad poniżej
    for i in range(len(x)): z = (1 - a) * x[i] + a * z; y[i] = z
    return y

def biquad(x, kind, fc, q=0.707, gain_db=0):
    """RBJ biquad; fc może być tablicą (filtr przestrajany) — wtedy liczone blokami po 64 próbki."""
    x = np.asarray(x, dtype=np.float64)
    y = np.zeros_like(x)
    fcs = np.broadcast_to(np.asarray(fc, dtype=np.float64), x.shape)
    x1 = x2 = y1 = y2 = 0.0
    B = 64
    for s in range(0, len(x), B):
        f = float(np.clip(fcs[s], 20, SR * 0.45)); w = 2 * np.pi * f / SR
        cw, sw = np.cos(w), np.sin(w); al = sw / (2 * q)
        if kind == 'lp': b0, b1, b2 = (1 - cw) / 2, 1 - cw, (1 - cw) / 2; a0, a1, a2 = 1 + al, -2 * cw, 1 - al
        elif kind == 'hp': b0, b1, b2 = (1 + cw) / 2, -(1 + cw), (1 + cw) / 2; a0, a1, a2 = 1 + al, -2 * cw, 1 - al
        else: b0, b1, b2 = al, 0, -al; a0, a1, a2 = 1 + al, -2 * cw, 1 - al  # bp
        b0 /= a0; b1 /= a0; b2 /= a0; a1 /= a0; a2 /= a0
        seg = x[s:s + B]; out = np.empty_like(seg)
        for i in range(len(seg)):
            v = b0 * seg[i] + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
            x2, x1 = x1, seg[i]; y2, y1 = y1, v; out[i] = v
        y[s:s + B] = out
    return y

try:
    from scipy.signal import lfilter, fftconvolve
    def biquad(x, kind, fc, q=0.707, gain_db=0):  # noqa: F811 — szybka wersja, gdy jest scipy
        x = np.asarray(x, dtype=np.float64)
        if np.ndim(fc) == 0:
            f = float(np.clip(fc, 20, SR * 0.45)); w = 2 * np.pi * f / SR; cw, sw = np.cos(w), np.sin(w); al = sw / (2 * q)
            if kind == 'lp': b = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2]
            elif kind == 'hp': b = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]
            else: b = [al, 0, -al]
            a = [1 + al, -2 * cw, 1 - al]
            return lfilter(np.array(b) / a[0], np.array(a) / a[0], x)
        out = np.zeros_like(x); B = 256; zi = np.zeros(2)
        fcs = np.asarray(fc)
        for s in range(0, len(x), B):
            f = float(np.clip(fcs[min(s, len(fcs) - 1)], 20, SR * 0.45)); w = 2 * np.pi * f / SR; cw, sw = np.cos(w), np.sin(w); al = sw / (2 * q)
            if kind == 'lp': b = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2]
            elif kind == 'hp': b = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]
            else: b = [al, 0, -al]
            a = [1 + al, -2 * cw, 1 - al]
            out[s:s + B], zi = lfilter(np.array(b) / a[0], np.array(a) / a[0], x[s:s + B], zi=zi)
        return out
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False
    def fftconvolve(a, b):
        n = len(a) + len(b) - 1; m = 1 << (n - 1).bit_length()
        return np.fft.irfft(np.fft.rfft(a, m) * np.fft.rfft(b, m), m)[:n]

def env_ad(n, a, d, curve=1.0):
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-6), np.exp(-(t - a) / d))
    return e ** curve

# ---------- instrumenty ----------
def ep(m, dur, vel=1.0):
    """Elektryczne pianino (FM): ciepłe, z delikatnym „dzwonkiem” na ataku."""
    n = int((dur + 1.6) * SR); t = np.arange(n) / SR; f = mtof(m)
    idx = 1.5 * np.exp(-t / 0.35) + 0.25
    mod = np.sin(2 * np.pi * f * t) * idx
    car = np.sin(2 * np.pi * f * t + mod)
    bell = np.sin(2 * np.pi * f * 7.02 * t) * 0.07 * np.exp(-t / 0.08)
    amp = np.minimum(t / 0.004, 1) * np.exp(-t / (1.1 + 0.5 * (60 - min(m, 72)) / 24))
    rel = np.clip((dur + 0.25 - t) / 0.25, 0, 1)
    trem = 1 + 0.08 * np.sin(2 * np.pi * 4.5 * t)
    return (car + bell) * amp * rel * trem * vel * 0.30

def pad(ms, dur):
    n = int((dur + 1.2) * SR); t = np.arange(n) / SR; out = np.zeros((2, n))
    for m in ms:
        f = mtof(m)
        for k, det in enumerate((-0.11, 0.0, 0.12)):
            ph = rng.random() * 2 * np.pi
            saw = 2 * ((f * (1 + det / 100 * 5) * t + ph / (2 * np.pi)) % 1) - 1
            out[k % 2] += saw * (0.6 if det else 0.5)
    for c in range(2): out[c] = biquad(out[c], 'lp', 1500, 0.6)
    amp = np.minimum(t / 0.7, 1) * np.clip((dur + 1.0 - t) / 1.0, 0, 1)
    return out * amp * 0.035

def bass(m, dur, vel=1.0):
    n = int((dur + 0.08) * SR); t = np.arange(n) / SR; f = mtof(m)
    s = np.sin(2 * np.pi * f * t) + 0.32 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    s = np.tanh(s * 1.6) / 1.2
    amp = np.minimum(t / 0.006, 1) * np.clip((dur + 0.06 - t) / 0.06, 0, 1) * (0.75 + 0.25 * np.exp(-t / 0.15))
    return s * amp * vel * 0.24

def kick(vel=1.0):
    t = t_(0.5); f = 48 + 95 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / 0.28) + 0.3 * rng.standard_normal(len(t)) * np.exp(-t / 0.003)
    return np.tanh(s * 1.5) * vel * 0.46

def clap(vel=1.0):
    t = t_(0.45); nz = rng.standard_normal(len(t))
    e = np.zeros_like(t)
    for d in (0.0, 0.011, 0.022): e += (t >= d) * np.exp(-np.maximum(t - d, 0) / 0.009)
    e += (t >= 0.03) * np.exp(-np.maximum(t - 0.03, 0) / 0.11) * 0.8
    s = biquad(nz * e, 'bp', 1500, 0.9) * 2.2
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.25
    return (s + body) * vel * 0.32

def hat(vel=1.0, open_=False):
    t = t_(0.35 if open_ else 0.08); nz = rng.standard_normal(len(t))
    s = biquad(nz, 'hp', 7500, 0.8) * np.exp(-t / (0.13 if open_ else 0.022))
    return s * vel * 0.09

def shaker(vel=1.0):
    t = t_(0.09); nz = rng.standard_normal(len(t))
    e = np.minimum(t / 0.012, 1) * np.exp(-t / 0.03)
    return biquad(biquad(nz, 'bp', 7500, 1.2), 'lp', 9000) * e * vel * 0.07

def pluck(m, vel=1.0):
    f = mtof(m); n = int(1.3 * SR); P = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, P); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % P]
        buf[i % P] = 0.5 * (buf[i % P] + buf[(i + 1) % P]) * 0.996
    out = biquad(out, 'lp', 3500)
    return out * vel * 0.24

# ---------- muzyka ----------
mus, drm, bas, rvs = Bus(), Bus(), Bus(), Bus()
CH = [  # (bas, akord)
    (41, [57, 60, 64, 67]),   # Fmaj9
    (43, [59, 62, 64, 69]),   # G6/9
    (40, [55, 59, 62, 66]),   # Em9
    (45, [55, 60, 64, 71]),   # Am9
]
F01 = start['f01']; Z0 = start['zmiany']; O = start['outro']
BREAK0, BREAK1 = start['f14'], start['f16']
END_STOP = O + 5.25
nbars = int(np.ceil(TOTAL / BAR)) + 1

def sec_intensity(t):
    if t < Z0: return 0
    if t < F01: return 1
    if BREAK0 <= t < BREAK1: return 2
    if t >= END_STOP: return -1
    return 3

swing = 0.035
for b in range(nbars):
    t0 = b * BAR
    if t0 >= TOTAL: break
    root, chord = CH[b % 4]
    I = sec_intensity(t0 + 0.01)
    # ---- akordy (pad zawsze, EP od hooka) ----
    if t0 < END_STOP:
        mus.add(pad(chord, BAR), t0, 1.0 if I != 2 else 1.3)
        # EP: synkopowane akordy
        pat = [(0, 1.1, 1.0), (1.5, 0.45, 0.75), (2.5, 0.9, 0.85), (3.5, 0.4, 0.6)] if I >= 1 else [(0, 2.2, 0.9), (2.5, 1.2, 0.6)]
        for (bt, du, v) in pat:
            st = t0 + bt * BEAT + (swing if (bt % 1) else 0)
            if st >= END_STOP: continue
            for k, m in enumerate(chord):
                mus.add(ep(m, du * BEAT, v), st + k * 0.006, 1.0, pan=(k - 1.5) * 0.25)
    # ---- bas ----
    if I in (1, 3) and t0 >= Z0 + BAR * 0.5:
        bp = [(0, 1.4, 1.0), (1.5, 0.4, 0.8), (2.0, 0.9, 0.9), (3.25, 0.25, 0.7), (3.5, 0.45, 0.85)]
        for (bt, du, v) in bp:
            st = t0 + bt * BEAT + (swing if (bt % 1) else 0)
            m = root + (12 if bt == 3.25 else 0) + (7 if bt == 3.5 and b % 2 else 0)
            if st < END_STOP: bas.add(bass(m, du * BEAT, v if I == 3 else v * 0.7), st)
    # ---- perkusja ----
    for s16 in range(16):
        st = t0 + s16 * BEAT / 4 + (swing if s16 % 2 else 0)
        if st >= END_STOP: break
        Ii = sec_intensity(st)
        if Ii == 3:
            if s16 in (0, 8) or (s16 == 7 and b % 2 == 1) or (s16 == 10 and b % 4 == 3): drm.add(kick(1.0 if s16 in (0, 8) else 0.7), st)
            if s16 in (4, 12): drm.add(clap(1.0), st)
            if s16 % 4 == 2: drm.add(hat(0.85, open_=True), st, pan=0.2)
            elif s16 % 2 == 0: drm.add(hat(0.5), st, pan=0.25)
            drm.add(shaker(0.55 + 0.45 * (s16 % 2)), st, pan=-0.3)
        elif Ii == 1:
            if st > Z0 + 0.6:
                if s16 % 2 == 1: drm.add(shaker(0.6), st, pan=-0.3)
                if s16 % 4 == 2: drm.add(hat(0.45, open_=True), st, pan=0.2)
                if s16 == 0 and st > Z0 + 4.4: drm.add(kick(0.7), st)
        elif Ii == 2:
            if s16 % 2 == 1: drm.add(shaker(0.5), st, pan=-0.3)
            if s16 in (4, 12): drm.add(clap(0.45), st)
    # ---- melodia (pluck) od f04 do przerwy i po powrocie ----
    mot = [(0, 76), (0.75, 74), (1.5, 72), (2.5, 69), (3.0, 71)] if b % 2 == 0 else [(0, 72), (0.75, 71), (1.5, 69), (2.0, 67), (3.0, 64)]
    if (start['f04'] <= t0 < BREAK0) or (BREAK1 <= t0 < O):
        for (bt, m) in mot:
            st = t0 + bt * BEAT + (swing if (bt % 1) else 0)
            mus.add(pluck(m, 0.9), st, 1.0, pan=0.35 * np.sin(b + bt))

# akord końcowy z długim wybrzmieniem
fin = start['outro'] + 6.2
for k, m in enumerate([45, 57, 60, 64, 67, 71, 76]):
    mus.add(ep(m, 4.0, 0.9), fin + k * 0.03, 1.0, pan=(k - 3) * 0.15)
mus.add(pad([57, 60, 64, 71], 4.5), fin, 1.6)
bas.add(bass(33, 3.2, 1.0) * np.exp(-t_(3.28) / 1.5)[:len(bass(33, 3.2, 1.0))], fin)

# ---------- efekty ----------
sfx = Bus()
def noise(sec): return rng.standard_normal(int(sec * SR))
def whoosh(sec, f0, f1, q=1.0):
    n = int(sec * SR); t = np.arange(n) / SR; k = t / sec
    fc = f0 * (f1 / f0) ** np.sin(np.pi * k / 2)
    e = np.sin(np.pi * k) ** 1.6
    return biquad(noise(sec), 'bp', fc, q) * e
def click_s():
    a = biquad(noise(0.012), 'bp', 3200, 2.0) * np.exp(-t_(0.012) / 0.0025)
    b = biquad(noise(0.012), 'bp', 2400, 2.0) * np.exp(-t_(0.012) / 0.002)
    out = np.zeros(int(0.09 * SR)); out[:len(a)] += a * 1.0; i = int(0.07 * SR); out[i:i + len(b)] += b * 0.6
    return out * 0.55
def key_s(v):
    f = 1800 + rng.random() * 1400
    s = biquad(noise(0.03), 'bp', f, 3.0) * np.exp(-t_(0.03) / 0.006)
    s += np.sin(2 * np.pi * 180 * t_(0.03)) * np.exp(-t_(0.03) / 0.01) * 0.3
    return s * v * 0.5
def pop_s(v, up=False):
    t = t_(0.16); f = (500 + 900 * (t / 0.16)) if up else (1100 * np.exp(-t / 0.05) + 380)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.045) * v * 0.35
def tick_s(v):
    t = t_(0.05); return (np.sin(2 * np.pi * 2100 * t) * 0.6 + biquad(noise(0.05), 'bp', 4000, 4) * 0.4) * np.exp(-t / 0.008) * v * 0.4
def ding_s():
    t = t_(1.6); s = np.zeros(len(t))
    for (f, a, d0) in ((1318.5, 0.5, 0.0), (1975.5, 0.35, 0.09)):
        tt = np.maximum(t - d0, 0); s += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.45) * a * (t >= d0)
    return s * 0.22
def thud_s():
    t = t_(0.9); f = 38 + 60 * np.exp(-t / 0.06)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.32)
    s += biquad(noise(0.9), 'lp', 400) * np.exp(-t / 0.05) * 0.6
    return np.tanh(s * 1.8) * 0.7
def crash_s():
    n = int(0.9 * SR); out = np.zeros(n)
    for i in range(70):
        d = (rng.random() ** 1.8) * 0.75; L = int(0.02 * SR); j = int(d * SR)
        if j + L >= n: continue
        f = 1500 + rng.random() * 4500
        out[j:j + L] += biquad(noise(0.02), 'bp', f, 5) * np.exp(-t_(0.02) / 0.004) * (0.4 + rng.random() * 0.6)
    out += biquad(noise(0.9), 'lp', 300) * np.exp(-t_(0.9) / 0.08) * 0.8
    return out * 0.6
def glitch_s():
    t = t_(0.4); sq = np.sign(np.sin(2 * np.pi * 110 * t * (1 + 3 * (np.floor(t * 25) % 3))))
    gate = (np.floor(t * 40) % 2)
    return biquad(sq * gate, 'lp', 2500) * np.exp(-t / 0.2) * 0.18
def peel_s():
    t = t_(0.5); return biquad(noise(0.5), 'hp', 2500) * (rng.random(len(t)) > 0.97) * np.exp(-t / 0.2) * 0.6 + whoosh(0.5, 1500, 5000, 2) * 0.15
def shimmer_s():
    n = int(1.4 * SR); out = np.zeros(n)
    for i in range(18):
        d = rng.random() * 0.9; f = mtof(84 + rng.choice([0, 3, 5, 7, 10, 12, 15]))
        tt = t_(0.5); j = int(d * SR)
        out[j:j + len(tt)] += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.12) * 0.12
    return out
def buzz_s():
    t = t_(0.28); return np.sign(np.sin(2 * np.pi * 160 * t)) * (0.5 + 0.5 * np.sin(2 * np.pi * 30 * t)) * np.minimum(1, (0.28 - t) / 0.05) * 0.06
def bubble_s():
    t = t_(0.12); f = 600 + 1400 * (t / 0.12) ** 0.6
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03) * 0.28
def power_s():
    t = t_(1.2); s = np.sin(2 * np.pi * 55 * t) * np.minimum(t / 0.3, 1) * np.exp(-t / 0.5) * 0.3
    s += np.sin(2 * np.pi * mtof(81) * t) * np.exp(-t / 0.4) * 0.08 * (t > 0.15)
    return s
def riser_s():
    n = int(1.0 * SR); t = np.arange(n) / SR
    s = biquad(noise(1.0), 'bp', 400 * (12 ** (t / 1.0)), 1.5) * (t / 1.0) ** 2
    return s * 0.5
def final_s():
    t = t_(3.0); s = np.sin(2 * np.pi * np.cumsum(30 + 50 * np.exp(-t / 0.1)) / SR) * np.exp(-t / 0.9) * 0.6
    return np.tanh(s * 1.4)
def strike_s():
    return whoosh(0.22, 2500, 7000, 2.5) * 0.35
def tap_s():
    t = t_(0.08); return (np.sin(2 * np.pi * 140 * t) * np.exp(-t / 0.02) * 0.6 + biquad(noise(0.08), 'bp', 2000, 2) * np.exp(-t / 0.005) * 0.4) * 0.5

for e in ev:
    t, ty = e['t'], e['type']; v = e.get('v', 1.0)
    p = (rng.random() - 0.5) * 0.5
    if ty == 'click': sfx.add(click_s(), t - 0.004, 0.9, p)
    elif ty == 'tap': sfx.add(tap_s(), t, 0.9, p)
    elif ty == 'whoosh': sfx.add(whoosh(0.55, 300, 2400, 0.9), t - 0.25, 0.22 * e.get('amt', 0.6), p)
    elif ty == 'curtain': sfx.add(whoosh(0.75, 180, 1300, 0.7), t, 0.3, 0)
    elif ty == 'swish': sfx.add(whoosh(0.4, 400, 3000, 1.2), t, 0.16, p)
    elif ty == 'key': sfx.add(key_s(v), t, 0.9, p * 0.4)
    elif ty == 'enter': sfx.add(key_s(1.0) * 1.6, t, 1.0, 0)
    elif ty == 'pop': sfx.add(pop_s(v), t, 1.0, p)
    elif ty == 'unpop': sfx.add(pop_s(v, up=True)[::-1] * 0.5, t, 1.0, p)
    elif ty == 'tick': sfx.add(tick_s(v), t, 1.0, p)
    elif ty == 'count': sfx.add(tick_s(v) * 0.6, t, 1.0, 0)
    elif ty == 'ding': sfx.add(ding_s(), t + 0.08, 1.0, 0.1)
    elif ty == 'thud': sfx.add(thud_s(), t, 1.0, 0)
    elif ty == 'crash': sfx.add(crash_s(), t, 1.0, 0)
    elif ty == 'glitch': sfx.add(glitch_s(), t, 1.0, 0)
    elif ty == 'peel': sfx.add(peel_s(), t, 1.0, 0.3)
    elif ty == 'shimmer': sfx.add(shimmer_s(), t, 1.0, -0.3)
    elif ty == 'buzz': sfx.add(buzz_s(), t, 1.0, 0)
    elif ty == 'bubble': sfx.add(bubble_s(), t, 1.0, 0.2)
    elif ty == 'power': sfx.add(power_s(), t, 1.0, 0)
    elif ty == 'riser': sfx.add(riser_s(), t - 0.1, 1.0, 0)
    elif ty == 'final': sfx.add(final_s(), t, 0.9, 0)
    elif ty == 'strike': sfx.add(strike_s(), t, 1.0, p)

# ---------- miks ----------
# sidechain: muzyka „oddycha” razem ze stopą
sc = np.zeros(N)
for b in range(nbars):
    for s16 in (0, 8):
        st = b * BAR + s16 * BEAT / 4
        if sec_intensity(st) == 3:
            i = int(st * SR); tt = t_(0.32); n = min(len(tt), N - i)
            if n > 0: sc[i:i + n] = np.maximum(sc[i:i + n], np.exp(-tt[:n] / 0.11))
duck = 1 - 0.45 * sc
mus.x *= duck; bas.x *= (1 - 0.6 * sc)

# pogłos (splot ze sztuczną odpowiedzią pomieszczenia)
irn = int(2.4 * SR); tir = np.arange(irn) / SR
ir = np.stack([rng.standard_normal(irn), rng.standard_normal(irn)]) * np.exp(-tir / 0.55)
ir[:, :int(0.012 * SR)] = 0
ir = np.stack([biquad(ir[0], 'lp', 6000), biquad(ir[1], 'lp', 6000)]) * 0.012
send = mus.x * 0.35 + drm.x * np.array([[0.12], [0.12]]) + sfx.x * 0.25
wet = np.stack([fftconvolve(send[c], ir[c])[:N] for c in range(2)])

mix = mus.x * 0.9 + drm.x * 0.85 + bas.x * 0.95 + sfx.x * 1.0 + wet
# wejście i wyjście
fade = np.ones(N); fi = int(0.05 * SR); fade[:fi] = np.linspace(0, 1, fi)
fo = int(1.2 * SR); fade[-fo:] = np.linspace(1, 0, fo) ** 2
mix *= fade
# ciepło + limiter
for c in range(2): mix[c] = biquad(mix[c], 'hp', 30)
rms = np.sqrt(np.mean(mix ** 2)) + 1e-9
mix *= 10 ** (-15.5 / 20) / rms
mix = np.tanh(mix * 1.15) / np.tanh(1.15)
peak = np.max(np.abs(mix)); mix *= min(1.0, 10 ** (-1.0 / 20) / peak)
pcm = (np.clip(mix.T, -1, 1) * 32767).astype('<i2')
import wave
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('zapisano', OUT, f'{TOTAL:.1f} s, rms {20*np.log10(np.sqrt(np.mean(mix**2))):.1f} dBFS, scipy={HAVE_SCIPY}')
