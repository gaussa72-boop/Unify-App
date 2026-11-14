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
if [ "$RAM_GB" -ge 128 ]; then MODEL="qwen3.5:122b"
elif [ "$RAM_GB" -ge 64 ]; then MODEL="qwen3.5:35b"
elif [ "$RAM_GB" -ge 32 ]; then MODEL="qwen3.5:27b"
elif [ "$RAM_GB" -ge 16 ]; then MODEL="qwen3.5:9b"
elif [ "$RAM_GB" -ge 8 ]; then MODEL="qwen3.5:4b"
else MODEL="qwen3.5:2b"; fi
echo "Erkannter Arbeitsspeicher: $RAM_GB GB. Modell: $MODEL"
ollama pull "$MODEL"
export AITE_MODEL="$MODEL"
export AITE_ALLOWED_ORIGINS="https://aurealis-cyber-shield.onrender.com,https://technologisierte-einheit.onrender.com,https://ate-rea-characterverse.onrender.com,https://aurelis-creative-ai-studio.onrender.com,https://ultima-central-45ne.onrender.com,https://ultima-unify-45ne.onrender.com,https://lichtkrieger-dark-mirror-realms.onrender.com,https://lichtkrieger-cloud-gaming.onrender.com,https://ultima-membership-api.onrender.com,https://astralis-omega.onrender.com,https://novatube-a10l.onrender.com,https://ate-rea-vermachtnis.onrender.com,https://dropshift-store.onrender.com,https://quantum-ai-zeah.onrender.com,https://ki-game-mod.onrender.com,https://note-ki.onrender.com,https://ipad-app-ionos-7.onrender.com,https://galactic-ai-v3.onrender.com,https://quantum-super-intelligence.onrender.com,https://ionos-8.onrender.com,https://quantum-ki-cat-chat.onrender.com,https://ai-quantumlight.onrender.com,https://quantenformel.onrender.com,https://quantum-singularity.onrender.com,https://ionos-ai.onrender.com,https://rea-signature.onrender.com,https://quantum-ai-renewed.onrender.com,https://quantum-ki-ultra-pro-v2-renewed.onrender.com,https://bullrun-apparel.onrender.com,https://quantum-mirror-wonderland.onrender.com,https://ionos-ki.onrender.com,https://ionos-7.onrender.com,https://ultraki-ai.onrender.com,https://ultra-ki-v2.onrender.com,https://quantum-ki-ultra-pro-v2.onrender.com,https://quantumai-chat.onrender.com,https://trinity-trading-k03l.onrender.com,https://aktiv-lyca-rgds.onrender.com,https://royal-palace-4r57.onrender.com,https://business-real-estate-membership-wswk.onrender.com,https://sneaker-store-bow5.onrender.com,https://webshop-parfum-90dl.onrender.com,https://aktiv-lyca-rnmc.onrender.com,https://astralis-app-center.onrender.com,https://sneaker-store-27cn.onrender.com,https://aktiv-lyca-standalone.onrender.com,https://drop-shipping-store.onrender.com,https://autokrypt-boerse.onrender.com,https://ate-rea-library.onrender.com,https://lichtkrieger-hub.onrender.com,https://omega-aurealis.onrender.com,https://quantum-mirror-wonderland-vibh.onrender.com,https://galactic-ai-v3-app.onrender.com,https://quantum-singularity-8liw.onrender.com,https://quantum-ki-cat-chat-2t79.onrender.com,https://ai-quantumlight-k84q.onrender.com,https://ionos-8-platform.onrender.com,https://ultraki-ai-app.onrender.com,https://ultra-ki-v2-app.onrender.com,https://quantum-ki-ultra-pro-v2-9pvf.onrender.com,https://quantum-ai-app.onrender.com,https://quantum-k-app.onrender.com,https://ultima-central-bt56.onrender.com,https://ultima-central-5zeh.onrender.com,https://ultima-central-r88g.onrender.com,https://novatube-studio-vli0.onrender.com,https://ionos-ki-v2-1oki.onrender.com"
(ollama serve >/tmp/aite-ollama.log 2>&1 &) || true
sleep 3
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "AITE Bridge läuft auf 127.0.0.1:8765. Terminal offen lassen."
python3 "$DIR/local_bridge.py"
