#!/bin/bash
set -euo pipefail
PLIST="$HOME/Library/LaunchAgents/com.ultima.ai.localagent.plist"
launchctl unload "$PLIST" >/dev/null 2>&1 || true
rm -f "$PLIST"
echo "ULTIMA AI Autostart entfernt. Deine lokale Konfiguration und Token-Datei bleiben erhalten."
echo "Zum vollständigen Entfernen lösche den Ordner: $HOME/Library/Application Support/UltimaAI"
