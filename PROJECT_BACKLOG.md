# ULTIMA / Aurealis – zentraler Projekt-Backlog
Stand: 14.11.2026

Diese Liste ist der Arbeitsstand. „Live“ bedeutet nur, dass ein Render-Deployment erfolgreich abgeschlossen wurde; es bedeutet nicht, dass jede Funktion fachlich vollständig getestet ist.

## Erledigt / deployed
- [x] ATE REA CharacterVerse – Grundwebsite, Charakterkarten, Roleplay-Oberfläche, Ate-Rea-Blog und Chronik-Link.
- [x] CharacterVerse – OpenAI SDK und OPENAI_API_KEY-Abhängigkeit aus dem Roleplay-Pfad entfernt.
- [x] CharacterVerse – Browser-lokale WebLLM/WebGPU-Inferenz, lokaler Ollama-Fallback, Service Worker, CSP, Helmet und Rate Limiting eingebaut.
- [x] Technologisierte Einheit – eigene Website mit Wissensportal und Kapitel-Leseraum erstellt.
- [x] Aurealis Cyber Shield – separate Sicherheitsübersicht erstellt und in ULTIMA Central eingetragen.
- [x] ULTIMA Central – Verzeichnis auf das aktuelle Render-Inventar mit 35 Services aktualisiert; Commit `a8a9a5fa134bd4ba741787b58363f45cef86f7df` erstellt.

## Offen – höchste Priorität
1. CharacterVerse End-to-End testen: Browsermodell auf geeignetem WebGPU-Gerät laden, Offline-Neustart testen, Ollama-Fallback testen. Der aktuelle Render-Build des letzten Dokumentations-Commits ist noch in Arbeit.
2. Gerätekompatibilität: WebGPU ist nicht überall verfügbar. Für ältere Geräte Ollama/llama.cpp lokal einrichten und dokumentieren.
3. CharacterVerse Adminbereich: sichere Anmeldung, Rollenrechte, Bücher-/Datei-Upload, Kapitel-Erkennung, Leseproben, Blog-Editor, Versionierung und Archiv.
4. Ate-Rea-Manuskripte und KI-Romane aus dem Quellenarchiv importieren, Kapitel strukturieren und mit der Vermächtnis-Chronik verknüpfen.
5. Technologisierte Einheit: vollständige Kapitel aus DOCX/PDF importieren, nicht nur den vorhandenen Kurztext-Auszug; Quellen und Versionen beibehalten.
6. Offline-KI-Architektur auf die übrigen geeigneten Websites ausrollen: gemeinsame lokale Modelladapter, Charakter-/Projektprofile, lokaler Speicher und Offline-Status.
7. Cyber Shield technisch ausbauen: echte automatisierte Health-/Header-/TLS-Prüfungen, Schwachstellenberichte, Alerts und Service-Integrationen. Das aktuelle Portal ist zunächst ein Dashboard/Checklisten-Einstieg und schützt andere Apps noch nicht automatisch.
8. Sicherheitsmiddleware in jedem einzelnen Webservice integrieren und testen: sichere Header/CSP, Authentifizierung/MFA, Rollenrechte, Rate Limits, CSRF, Input-/Upload-Prüfungen, Secrets-Handling, Backups und Wiederherstellungstests.
9. Alle 35 Render-Services im ausgewählten Primary-Workspace und 43 GitHub-Repositories beider verbundenen Konten inventarisieren: Fehler, doppelte Services, veraltete Deployments, kaputte Build-Commands, fehlende Health Checks und nicht zugeordnete Projekte prüfen.
10. Frühere Projekte vervollständigen: ULTIMA gemeinsame Identität und Rechte, Quantum-KI-Backends, KI-Game-Mod Backend, IONOS-/Note-KI-Verbindungen, Webshop-/Telegram-Bot-Workflows und App-Umsetzungen.

## Arbeitsregeln
- Vor jeder Änderung Repository, Branch, Render-Service und bestehende Version prüfen.
- Bestehende funktionierende Versionen sichern; keine Services oder Repositories ohne ausdrückliche Freigabe löschen.
- Nach jedem Commit Build-/Deploy-Status und Logs prüfen; keine Fertigmeldung ohne erfolgreichen Deploy und Funktionstest.
- Keine Geheimnisse in Quellcode, Chat oder öffentliche Repositories schreiben.
- Neue Websites in ULTIMA Central aufnehmen und Sicherheitsprüfung dokumentieren.
- Nicht abgeschlossene Aufgaben bleiben hier offen und werden bei der nächsten Projektarbeit zuerst wieder aufgegriffen.


## Aktualisierung 14.11.2026 – Service-Inventar
- Render-Inventar im ausgewählten Primary-Workspace erneut ausgelesen: 35 Services, alle als `not_suspended` gemeldet. Das ist kein Beleg für fehlerfreie HTTP-Erreichbarkeit oder vollständige Funktionen.
- ULTIMA Central `index.html` mit den 35 aktuellen Render-Service-URLs, Repository-Links und Kurzbeschreibungen aktualisiert.
- Neuer Central-Deploy `dep-dbrqa349v7es73b6h5bg` wurde gestartet; Live-Status und anschließender Browser-/Funktionscheck stehen noch aus.
- Nächster Schritt: Deploy abschließen lassen, Homepage prüfen, danach Services in Gruppen auf HTTP-/Health-Endpunkte, Logs und Kernfunktionen auditieren. Alte und doppelte Services bleiben erhalten, bis ihre Zuordnung und Abhängigkeiten geklärt sind.
