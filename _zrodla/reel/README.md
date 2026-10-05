# Reel „19 smaczków mojej nowej strony” (część 2)

Pionowy film 1080×1920, 60 kl./s, ok. 2:54. Wszystko na ekranie to **prawdziwa strona** nagrana klatka po klatce,
pokazana na atrapie Maca (Studio Display), iPhone'a i starego netbooka.

## Jak to działa

| Plik | Co robi |
|---|---|
| `scenariusz.js` | Kolejność scen, tytuły, podpisy i długości w taktach muzyki (100 BPM, 1 takt = 2,4 s) — wspólne dla wszystkiego niżej |
| `czas.js` | Wirtualny zegar wstrzykiwany do strony: timery, `requestAnimationFrame`, `Date`, animacje CSS — każda klatka to dokładnie 1/60 s, więc nagranie jest idealnie płynne niezależnie od szybkości komputera |
| `nagraj.js` | Nagrywa ujęcia: `hook` (pierwsze wejście), `main` (cała wycieczka po stronie bez cięć), `old` (strona z czerwca), `phone` (telefon). Kursor jedzie po łukach jak ręka, przewijanie ma płynne krzywe |
| `serwer.js` | Lokalny serwer z czystymi adresami (`/prace` → `prace.html`) i stroną 404 — jak GitHub Pages |
| `scena.html` + `scena.js` | Montaż: Mac, telefon, netbook, napisy, licznik 01/19, lupy, kamera na sprężynach (zero sztywnych startów i stopów) |
| `renderuj.js` | Renderuje scenę do MP4 (kilka procesów naraz), robi podglądowe kadry i listę zdarzeń dźwiękowych |
| `dzwiek.py` | Muzyka i efekty syntetyzowane od zera (bez cudzych sampli): kliknięcia, kurtyny, pisanie, rozbicie netbooka, lądowanie Maca… zsynchronizowane z obrazem |
| `fonty/` | Caveat (karteczka „TODO”) i 3 emoji z Noto Color Emoji — obie licencja SIL OFL |

## Zbudowanie od zera

```bash
bash _zrodla/reel/zbuduj.sh /tmp/reel     # ok. 1 h na 4 rdzeniach
```

Podgląd pojedynczych kadrów (bez renderu całości):

```bash
NODE_PATH=$(npm root -g) REEL_OUT=/tmp/reel node _zrodla/reel/renderuj.js --takes=/tmp/reel/takes --stills=20,45.5,120
```

Zmiana tekstu, kolejności albo długości sceny: `scenariusz.js` (czasy ruchów kursora w `nagraj.js` są liczone od początku sceny, więc po zmianie długości trzeba nagrać ujęcia ponownie).
