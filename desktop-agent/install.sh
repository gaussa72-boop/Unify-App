#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
APP="$HOME/Library/Application Support/UltimaAI"
AGENTS="$HOME/Library/LaunchAgents"
PLIST="$AGENTS/com.ultima.ai.localagent.plist"
PYTHON="$(command -v python3 || true)"
if [ -z "$PYTHON" ]; then echo "Python 3 fehlt. Installiere eine aktuelle Python-3-Version und starte dieses Skript erneut."; exit 1; fi
"$PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,8) else 1)' || { echo "Python 3.8 oder neuer wird benötigt."; exit 1; }
mkdir -p "$APP" "$AGENTS"
chmod 700 "$APP"
cp "$ROOT/agent.py" "$APP/agent.py"
cp "$ROOT/index.html" "$APP/index.html"
chmod 700 "$APP/agent.py"
"$PYTHON" "$APP/agent.py" --init
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>com.ultima.ai.localagent</string>
<key>ProgramArguments</key><array><string>$PYTHON</string><string>$APP/agent.py</string></array>
<key>RunAtLoad</key><true/><key>KeepAlive</key><true/>
<key>StandardOutPath</key><string>$APP/agent.log</string>
<key>StandardErrorPath</key><string>$APP/agent-error.log</string>
<key>WorkingDirectory</key><string>$APP</string>
</dict></plist>
EOF
chmod 600 "$PLIST"
launchctl unload "$PLIST" >/dev/null 2>&1 || true
launchctl load -w "$PLIST"
echo ""
echo "ULTIMA AI wurde als lokaler Login-Agent eingerichtet."
echo "Öffne http://127.0.0.1:8765 auf diesem Mac."
echo "Den Schlüssel findest du lokal in: $APP/local.token"
echo "Zum Anzeigen: cat \"$APP/local.token\""
echo "Der Dienst ist ausschließlich an 127.0.0.1 gebunden."
