# ULTIMA – Dauerhafte Wartungs- und Qualitätsrichtlinie

Diese Richtlinie ist ein dauerhafter Projektstandard für alle Websites, Apps, Backends, KI-Systeme und Softwareprojekte im ULTIMA-Netzwerk.

## Grundsatz

Bei jeder neuen Änderung und bei jeder ausdrücklich angeforderten Wartungsrunde wird der vorhandene Stand auf eine aktuelle, stabile und zur Laufzeit passende Version gebracht. Das Ziel ist die bestmögliche sinnvolle Qualität – nicht das ungeprüfte Einspielen jeder Vorab- oder Major-Version.

## Pflicht-Checkliste je Projekt

1. **Bestandsaufnahme:** Repository, Hauptbranch, Laufzeit, Framework, Build-/Startbefehl, Render-Service, Domain, Datenbank und Umgebungsvariablen-Key-Namen erfassen. Niemals Secret-Werte in Logs, Commits oder Reports ausgeben.
2. **Abhängigkeiten:** Veraltete, unsichere oder inkompatible Pakete erkennen. Updates bevorzugt auf aktuelle stabile Versionen; Major-Updates zuerst auf Kompatibilität prüfen und nicht blind in Produktion übernehmen.
3. **Sicherheit:** Authentifizierung, Rollen, Sitzungen, Zugriffskontrolle, CORS, CSRF, Eingabevalidierung, Secret-Verwaltung, Uploads, Rate-Limits und Datenbankzugriffe prüfen.
4. **Funktion:** Navigationswege, Formulare, Buttons, APIs, Webhooks, Chat-/KI-Aufrufe, Zahlungen, Uploads und Fehlerzustände prüfen. Keine Funktionen als erfolgreich melden, die nicht ausgeführt und überprüft wurden.
5. **KI-Qualität:** Jede KI behält ihren eigenen Namen, Charakter, Systemprompt, Wissenskontext und ihre Funktionen. Gemeinsame Laufzeit-/Fallback-Komponenten dürfen die Persona nicht überschreiben. Online-Modell, lokales Modell und Offline-Fallback sichtbar unterscheiden.
6. **Leistung und UX:** Responsives Layout, Accessibility, Ladezeiten, Caching, Bild-/Videooptimierung, mobile Bedienbarkeit und klare Statusmeldungen verbessern.
7. **Tests:** Syntax-/Build-Checks, Unit-/Integrationstests und – wo möglich – HTTP-Healthchecks und reale Funktionsprüfungen vor der Live-Bestätigung durchführen.
8. **Deployment:** Änderungen nachvollziehbar committen, auf Render veröffentlichen, den genauen Commit gegen den neuesten Deploy prüfen und Logs auf Build- bzw. Laufzeitfehler kontrollieren. Nach Deployment die relevanten Seiten und Endpunkte erneut prüfen.
9. **Daten und Rückfall:** Vor schema- oder datenverändernden Änderungen Migrationen und Rückfallmöglichkeit berücksichtigen. Keine Passwörter, Konten, Preise oder Zahlungszustände ohne Autorisierung ändern.
10. **Dokumentation:** Datum, Commit, betroffene Services, Prüfergebnis, offene Voraussetzungen und bekannte Grenzen dokumentieren.

## Freigabeprinzip

- Kleine, rückwärtskompatible Verbesserungen können direkt veröffentlicht werden.
- Datenbankmigrationen, neue Kosten, Preis-/Zahlungsänderungen, Berechtigungsänderungen und externe Provider-Integrationen benötigen besondere Prüfung.
- Für eine vollständige KI-Online-Funktion müssen die benötigten Anbieter-Secrets vorhanden sein. Für lokale/offlinefähige KI müssen Modell, Runtime und lokaler Bridge-Prozess auf dem Zielgerät installiert und gestartet sein.
- Ein grüner Render-Deployment-Status beweist nur, dass der Code veröffentlicht wurde. Er beweist nicht automatisch alle End-to-End-Funktionen.

## Standardbericht

Jede Wartungsrunde nennt:
- welche Projekte und Services tatsächlich geprüft wurden;
- welche Commits und Deployments veröffentlicht wurden;
- welche Tests und Healthchecks erfolgreich waren;
- welche Funktionen noch Secrets, Geräte-Setup oder externe Provider benötigen;
- welche Services nicht geprüft oder nicht erreichbar waren.

**Leitlinie:** Immer verbessern, wo ein konkreter Qualitätsgewinn belegbar ist. Stabilität, Sicherheit und die eigenständige Identität jedes Projekts haben Vorrang vor ungeprüften Updates.
