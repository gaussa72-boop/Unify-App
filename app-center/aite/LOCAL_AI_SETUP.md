# AITE – lokales KI-Modell ohne OpenAI-Guthaben

## Was wirklich offline funktioniert

- Die AITE-Oberfläche und ihre sechs Reflexionsmodi funktionieren ohne OpenAI.
- Ohne lokales Sprachmodell antwortet AITE mit einer kleinen eingebauten Reflexionshilfe. Das ist kein generatives Sprachmodell.
- Für freie, generative Antworten nutzt AITE standardmäßig Ollama auf dem eigenen Gerät.
- Das Modell muss einmalig heruntergeladen werden. Danach kann es lokal ohne Internet und ohne OpenAI-Guthaben laufen.
- OpenAI bleibt ein optionaler Zusatzmodus. Eine Website muss dafür einen eigenen geschützten Server-Endpunkt bereitstellen; niemals einen API-Schlüssel in die Browserseite schreiben.

## Einmalige Einrichtung

1. Ollama von der offiziellen Website installieren: https://ollama.com
2. Terminal öffnen und das Modell herunterladen:
   ```bash
   ollama pull qwen2.5:3b
   ```
3. Ollama starten:
   ```bash
   ollama serve
   ```
4. Browser auf der Website öffnen und in AITE den Modus „Lokal / Offline“ wählen.
5. Beim ersten Zugriff dem Browser erlauben, mit dem lokalen Ollama-Dienst auf diesem Gerät zu kommunizieren, falls er danach fragt.

## Browserzugriff und Sicherheit

AITE sendet lokale Anfragen an `http://localhost:11434/api/chat`. Browser können dafür eine lokale Netzwerk-/CORS-Freigabe verlangen. Falls Ollama den Ursprung blockiert, muss `OLLAMA_ORIGINS` auf die exakten Website-Ursprünge beschränkt werden, die verwendet werden (z. B. `https://astralis-app-center.onrender.com` plus die tatsächlich genutzten Projekt-Domains). Keine pauschale Freigabe für alle Ursprünge setzen, wenn es nicht zwingend nötig ist.

## Hardware und Grenzen

- Qwen 2.5 3B ist ein kompaktes Modell; Antworten und Geschwindigkeit hängen von RAM, CPU/GPU und Betriebssystem ab.
- Ältere Rechner und mobile Browser unterstützen nicht jede lokale Laufzeit. Auf solchen Geräten bleibt der Offline-Reflexionsmodus verfügbar; freie lokale Textgenerierung kann ausfallen.
- Ein bereits heruntergeladenes Modell belegt mehrere Gigabyte Speicher. Das Modell wird nicht automatisch von der Website heruntergeladen.
- Offline bedeutet: Das Modell rechnet auf deinem Gerät. Website-Updates, erstmalige Installation und Modell-Download benötigen Internet.
- Der Chatverlauf liegt standardmäßig im lokalen Browser-Speicher dieses Geräts und synchronisiert sich nicht automatisch zwischen Geräten.

## Website-spezifische Profile

Jede Einbindung kann ihr eigenes Profil wählen:
- `dharma`: Ate Rea / achtsame Reflexion
- `archetypes`: symbolische Archetypen und Spiegelwelt
- `light`: Lichtpfad und Werteorientierung
- `creator`: Kreativität und Schöpfungsarbeit
- `tech`: Projekte und Technologie
- `compass`: allgemeiner Bewusstseinskompass

Spirituelle Begriffe sind Reflexions- und Symbolsprache, keine wissenschaftlichen Tatsachenbehauptungen, Diagnosen oder Heilsversprechen.
