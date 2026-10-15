# -*- coding: utf-8 -*-
"""Nagłówek bezpieczeństwa CSP (Content-Security-Policy) na podstronach strony.

GitHub Pages nie pozwala ustawić nagłówków HTTP, więc polityka idzie w <meta http-equiv>.
Pozwala tylko na pliki z naszej domeny + wysyłkę formularza do Web3Forms; obce skrypty,
wtyczki i wstrzyknięty kod nie zadziałają. Skrypty inline (start strony, podpis w kurtynie)
są dozwolone po skrócie SHA-256, liczonym tutaj z plików.

Uruchom z katalogu repozytorium:  python3 _zrodla/zbuduj_csp.py
Uruchamia się też na końcu zbuduj_poradnik.py. Po każdej ręcznej zmianie skryptu inline
w którymkolwiek pliku HTML trzeba go puścić ponownie — inaczej przeglądarka zablokuje ten skrypt.
Projekty koncepcyjne (osobne strony z własnymi skryptami) zostają bez CSP.
"""
import base64
import glob
import hashlib
import os
import re

POMIN = {'luxe-salon.html', 'vesper-barber.html', 'zar-burger.html', 'gmina-warta.html', 'google1a4fd6f90fdf66e4.html'}
SKRYPT = re.compile(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', re.S)
META_CSP = re.compile(r'\s*<meta http-equiv="Content-Security-Policy" content="[^"]*">')
META_REF = re.compile(r'\s*<meta name="referrer" content="[^"]*">')
VIEWPORT = re.compile(r'(<meta name="viewport" content="[^"]*">)')


def polityka(skroty):
    return '; '.join([
        "default-src 'self'",
        "script-src 'self'" + ''.join(" 'sha256-%s'" % h for h in skroty),
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data:",
        "font-src 'self' data:",
        "connect-src 'self' https://api.web3forms.com",
        "frame-src 'self'",
        "media-src 'self'",
        "manifest-src 'self'",
        "worker-src 'none'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "upgrade-insecure-requests",
    ])


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    zmienione = 0
    for f in sorted(glob.glob('*.html')):
        if f in POMIN:
            continue
        s = open(f, encoding='utf-8').read()
        skroty = []
        for m in SKRYPT.finditer(s):
            if 'ld+json' in m.group(1):
                continue  # dane strukturalne nie są wykonywane
            h = base64.b64encode(hashlib.sha256(m.group(2).encode('utf-8')).digest()).decode()
            if h not in skroty:
                skroty.append(h)
        nowy = META_REF.sub('', META_CSP.sub('', s))
        meta = ('\n<meta http-equiv="Content-Security-Policy" content="%s">'
                '\n<meta name="referrer" content="strict-origin-when-cross-origin">' % polityka(skroty))
        nowy, n = VIEWPORT.subn(lambda m: m.group(1) + meta, nowy, count=1)
        if not n:
            raise SystemExit('brak <meta name="viewport"> w ' + f)
        if nowy != s:
            open(f, 'w', encoding='utf-8').write(nowy)
            zmienione += 1
    print('CSP: zaktualizowano %d plików' % zmienione)


if __name__ == '__main__':
    main()
