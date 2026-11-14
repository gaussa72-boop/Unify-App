#!/bin/bash
set -e
echo "AITE Local AI setup - macOS"
if ! command -v ollama >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    brew install ollama
  else
    echo "Bitte Ollama für deine macOS-Version von https://ollama.com/download installieren."
    echo "Auf älteren Macs kann die aktuelle Ollama-Version nicht mehr unterstützt werden."
    read -r -p "Drücke Enter zum Beenden."
    exit 1
  fi
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 wird benötigt. Bitte Python 3 installieren und erneut starten."
  exit 1
fi
ollama pull qwen2.5:3b
(ollama serve >/tmp/aite-ollama.log 2>&1 &) || true
sleep 3
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "AITE Bridge läuft. Terminalfenster offen lassen."
python3 "$DIR/local_bridge.py"
