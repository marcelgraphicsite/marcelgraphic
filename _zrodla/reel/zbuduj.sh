#!/usr/bin/env bash
# Cały reel od zera: nagranie strony → scena → dźwięk → MP4 (1080×1920, 60 kl./s).
# Użycie: bash _zrodla/reel/zbuduj.sh [katalog_roboczy]
# Wymaga: node + playwright (globalnie), ffmpeg, python3 z numpy i scipy, git.
set -euo pipefail
cd "$(dirname "$0")"
WORK="${1:-$(pwd)/out}"
mkdir -p "$WORK/takes"
export NODE_PATH="$(npm root -g)"
export REEL_OUT="$WORK"

# 1) serwery: aktualna strona (8123) i stara wersja z czerwca (8124)
if [ ! -d "$WORK/stara" ]; then mkdir -p "$WORK/stara"; git -C ../.. archive 7aa7e19 | tar -x -C "$WORK/stara"; fi
node serwer.js > "$WORK/serwer.log" 2>&1 & S1=$!
ROOT="$WORK/stara" PORT=8124 node serwer.js > "$WORK/serwer-old.log" 2>&1 & S2=$!
trap 'kill $S1 $S2 2>/dev/null || true' EXIT
sleep 1

# 2) ujęcia strony (wirtualny czas, klatka po klatce)
for take in hook main old phone; do
  REEL_OUT="$WORK/takes" node nagraj.js "$take"
done

# 3) lista zdarzeń dźwiękowych + ścieżka dźwiękowa
node renderuj.js --takes="$WORK/takes" --sfx="$WORK/zdarzenia.json"
node -e "console.log(JSON.stringify(require('./scenariusz.js')))" > "$WORK/scen.json"
python3 dzwiek.py "$WORK/zdarzenia.json" "$WORK/scen.json" "$WORK/audio.wav"

# 4) obraz (3 procesy równolegle) i złożenie
node renderuj.js --takes="$WORK/takes" --all --workers="${WORKERS:-3}"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$WORK/seg/list.txt" -i "$WORK/audio.wav" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 -movflags +faststart -shortest "$WORK/reel_19_smaczkow.mp4"
echo "gotowe: $WORK/reel_19_smaczkow.mp4"
