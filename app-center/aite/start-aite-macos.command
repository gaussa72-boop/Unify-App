#!/bin/bash
set -e
echo "AITE Local AI setup - macOS"
OS_VERSION="$(sw_vers -productVersion)"
MAJOR="${OS_VERSION%%.*}"
if [ "$MAJOR" -lt 14 ]; then
  echo "Dieses macOS ($OS_VERSION) liegt unter der aktuellen Ollama-Anforderung (macOS 14 Sonoma oder neuer)."
  echo "Auf einem älteren Mac kann Ollama nicht zuverlässig installiert/gestartet werden. Nutze den Windows-Laptop oder ein neueres Mac-Gerät."
  read -r -p "Enter zum Beenden."
  exit 1
fi
if ! command -v ollama >/dev/null 2>&1; then
  echo "Bitte Ollama für macOS 14+ installieren: https://ollama.com/download/mac"
  open "https://ollama.com/download/mac" || true
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then echo "Python 3 wird benötigt."; exit 1; fi
RAM_BYTES="$(sysctl -n hw.memsize)"
RAM_GB=$((RAM_BYTES / 1024 / 1024 / 1024))
if [ "$RAM_GB" -ge 32 ]; then MODEL="gpt-oss:20b"
elif [ "$RAM_GB" -ge 16 ]; then MODEL="qwen3.5:9b"
else MODEL="qwen3.5:4b"; fi
echo "Erkannter Arbeitsspeicher: $RAM_GB GB. Modell: $MODEL"
ollama pull "$MODEL"
export AITE_MODEL="$MODEL"
(ollama serve >/tmp/aite-ollama.log 2>&1 &) || true
sleep 3
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "AITE Bridge läuft auf 127.0.0.1:8765. Terminal offen lassen."
python3 "$DIR/local_bridge.py"
