# Update Matrix – globale Betriebsregeln

Datum: 2026-11-27
Eigentümerkontext: gaussa72-boop

## Änderung
- Neue kanonische Richtlinie: `GAUSS72_GLOBAL_OPERATING_RULES.md`.
- Update-Matrix-Agenten erhalten die globale Richtlinie im Prompt; ihre projektspezifischen Personas bleiben erhalten.
- Geltungsbereich: kompatible, kontrollierte oder ausdrücklich freigegebene Projekte über beide verbundenen GitHub-Konten und Render Primary, jeweils nach Einzelprüfung.
- Rollout: Inventarisierung, Kompatibilitäts- und Sicherheitsprüfung, versionierter Vorschlag, isolierte Tests, Freigabe bei risikoreichen Aktionen, Deployment, Health-/Funktionsprüfung, Status- und Rollback-Dokumentation.
- Integrationsausschlüsse, Autokrypt-Sonderstatus, private Nachrichten, Finanzfreigaben und Secret-Handling bleiben verbindlich geregelt.

## Verifikation
- GitHub-Commits: siehe die zugehörigen Commits im Verlauf dieses Repositories.
- Noch nicht erfolgt: flächendeckende Verteilung in alle übrigen Repositories, End-to-End-Tests aller Dienste und Verifikation aller Render-Deployments. Kein globaler Rollout wird behauptet.
- Der Matrix-Code bleibt proposal-first; er führt generierten Code nicht selbst aus und startet keine Deployments autonom.

## Nächste Schritte
1. Alle Repositories und Render-Services beider Konten inventarisieren und Integrationsgrenzen klassifizieren.
2. Projektweise Update-Agenten/Manifeste anlegen, ohne bestehende KI-Personas zu überschreiben.
3. Tests und Sicherheitschecks je Zielsystem ausführen.
4. Freigegebene Änderungen schrittweise ausrollen und verifizieren.
