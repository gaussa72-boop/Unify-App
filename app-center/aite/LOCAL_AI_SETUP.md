# AITE – lokales KI-Modell ohne OpenAI-Guthaben

## Was offline wirklich funktioniert

AITE hat drei klar getrennte Modi:

- **Lokal / Offline mit Ollama:** generative Antworten werden auf dem eigenen Gerät berechnet. Das Modell muss einmalig heruntergeladen sein; danach benötigt die Inferenz weder Internet noch OpenAI-Guthaben.
- **Offline-Fallback:** ohne laufenden lokalen Modellserver gibt AITE eine kurze, regelbasierte Reflexionshilfe. Das ist ausdrücklich kein generatives Sprachmodell.
- **Online / OpenAI:** nur über einen geschützten Server-Endpunkt der jeweiligen Website. API-Schlüssel gehören niemals in Browser-JavaScript.

## Einrichtung unter Windows

1. Ollama installieren: https://ollama.com/download
2. PowerShell im Ordner `app-center/aite` öffnen.
3. Starten:
   ```powershell
   .\start-aite-windows.ps1
   ```
4. Das Skript wählt anhand des Arbeitsspeichers ein passendes Qwen-3.5-Modell, lädt es einmalig und startet Ollama sowie die lokale AITE-Bridge.
5. Dieses PowerShell-Fenster geöffnet lassen, solange AITE den lokalen Modellserver verwenden soll.

## Einrichtung unter macOS

Das mitgelieferte macOS-Skript setzt **macOS 14 Sonoma oder neuer** und Ollama voraus. Es bricht auf älteren macOS-Versionen absichtlich ab. Starte im Ordner `app-center/aite`:
```bash
./start-aite-macos.command
```
Auf älteren Macs ist dieser Ollama-Aufbau nicht unterstützt; dort bleibt nur der einfache Offline-Fallback oder ein separates, unterstütztes Gerät.

## Technischer Aufbau und Ports

- AITE-Bridge: `http://127.0.0.1:8766`
- Ollama: `http://127.0.0.1:11434`
- Die Bridge lauscht nur auf `127.0.0.1`, nicht im LAN oder öffentlichen Internet.
- Der ULTIMA Desktop-Agent verwendet separat Port `8765`; dadurch können beide lokalen Dienste gleichzeitig laufen.
- Die Bridge erlaubt nur explizit eingetragene Website-Ursprünge. Die Installationsskripte setzen eine Allowlist für die verbundenen Render-Websites. Eigene Domains müssen explizit ergänzt werden.

Manuelle Einrichtung:
```bash
ollama pull qwen3.5:4b
ollama serve
AITE_MODEL=qwen3.5:4b AITE_ALLOWED_ORIGINS=https://deine-domain.example python3 local_bridge.py
```

Die AITE-Weboberfläche fragt `/health` ab und sendet Chats an `/api/chat`. Bei fehlendem lokalen Dienst bleibt die kurze Reflexionshilfe verfügbar; freie lokale Textgenerierung steht dann nicht zur Verfügung.

## Hardware und Grenzen

- Das Modell wird nicht automatisch durch das Öffnen einer Website installiert.
- Modellgröße, RAM-Bedarf und Geschwindigkeit hängen von der gewählten Qwen-Variante, Quantisierung und Hardware ab.
- Ältere Geräte können bei großen Modellen sehr langsam sein oder sie nicht laden. Wähle ein Modell, das genug RAM für Betriebssystem und andere Apps übrig lässt.
- Das Modell muss mindestens einmal heruntergeladen werden. Erst danach kann die lokale Inferenz offline laufen.
- Browser- und Gesprächsverlauf werden lokal gespeichert und nicht automatisch zwischen Geräten synchronisiert.

## Website-Profile

Jede Einbindung kann ihr eigenes AITE-Profil wählen:

- `dharma`: Ate Rea / achtsame Reflexion
- `archetypes`: symbolische Archetypen und Spiegelwelt
- `light`: Lichtpfad und Werteorientierung
- `creator`: Kreativität und Schöpfungsarbeit
- `tech`: Projekte und Technologie
- `compass`: allgemeiner Bewusstseinskompass

Spirituelle Begriffe sind Reflexions- und Symbolsprache, keine wissenschaftlichen Tatsachenbehauptungen, Diagnosen oder Heilsversprechen.
