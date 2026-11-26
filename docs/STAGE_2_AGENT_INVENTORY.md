# AUREALIS INFINITY / ULTIMA — Stage 2 Inventarisierung

Stand: 2026-11-26

## Ziel von Stage 2
Vollständige Inventarisierung der aktiven Agenten, Original-Prompts, Speicher, Schnittstellen und Testfälle; anschließend ein gemeinsamer Agentenvertrag und ein Pilot mit genau einem Dienst.

## Verifizierte Bestandsaufnahme aus dem ULTIMA-Code
Quelle: `mcp_gateway.py` in `gaussa72-boop/Unify-App`.
- Der read-only MCP-Katalog enthält 36 Agentenprofile.
- Jedes Profil enthält ID, Anzeigename, Fachgebiet und eine Persona-Kurzbeschreibung.
- Diese Beschreibungen sind **keine Original-System-Prompts**. Die Original-Prompts pro Agent wurden in dieser Phase nicht vollständig abgerufen und bleiben als offene Inventarisierungsarbeit markiert.
- Der MCP-Gateway-Header beschreibt einen authentifizierten, zustandslosen, read-only Zugang. Keine Deploy-, Shell-, Zahlungs-, Veröffentlichungs-, Lösch- oder Account-Schreibwerkzeuge.
- Der Gateway-Katalog enthält 36 Agenten-IDs: aurealis, aite, ionos, quantum, dark_wonderland, neuroforge, cosmican, guardian, studio, ionos8, galactic, singularity, quantumlight, quantum_ai, ultra_ki, ultra_ki_pro, cat_chat, quantum_mirror, aurealis_omega, quantum_super, quantenformel_qai, note_ki, rea_signature, aurealis_creative, aurealis_studio, ionos7, ionos_mobile, aurealis_shopping, ultra_ki_merge, ate_rea, ate_rea_characterverse, novatube, lichtkrieger, the_lord, ki_game_mod, quantenformel.

## Persona- und Speicherinventar
- Persona: Für die 36 Einträge liegen Kurzbeschreibungen im Gateway vor. Original-Prompts, Versionierung und Herkunft je Produktivdienst: **offen**.
- Speicher: Das Gateway ist zustandslos. Persistente Memory-Namespaces pro Agent, Datenbankzuordnung, Retention und Löschpfad: **nicht durch diesen Katalog belegt**.
- Schutzregel: Keine Persona, kein Prompt und kein Agentengedächtnis eines Dienstes wird durch einen anderen überschrieben. Jede Änderung benötigt Diff, Eigentümerfreigabe und Regressionstest.

## Schnittstelleninventar
- ULTIMA Central: Flask-Portal, Projektkatalog, Admin-/AI-Studio-Routen.
- MCP: authentifizierter read-only Agenten-/Capability-Katalog.
- Update Matrix: proposal-first API; Status-/Agenten-/Proposal-Routen; Vorschläge werden nicht automatisch ausgeführt oder deployed.
- Projektregister: `data/project_registry.json` ist ausdrücklich ein Inventar-Snapshot, keine Live-Synchronisation.
- AUREALIS INFINITY: statisches Render-Dashboard; keine aktive Agenten-Orchestrierung oder DGX-Verbindung durch die Website allein nachgewiesen.
- Produktive Agenten-Provider-Endpunkte, Authentifizierungsverfahren und Webhooks pro Projekt: **noch zu erheben**.

## Gemeinsamer Agentenvertrag — Entwurf
1. Identität: stabile agent_id, Anzeigename, Eigentümerdienst, Version.
2. Persona: Original-System-Prompt unverändert als versioniertes Artefakt; Persona-Hash und Freigabe vor Änderung.
3. Memory: eigener Namespace pro Agent; Zugriff nur explizit freigegeben; keine Cross-Agent-Übernahme.
4. Fähigkeiten: allowlist aus benannten Tools und Scopes; default deny.
5. Aufgabenformat: task_id, Ziel, Kontextquellen, Eingabe, gewünschtes Ergebnis, Frist und Risikoklasse.
6. Ergebnisformat: Status, Zusammenfassung, Artefakte, Quellen, Tests, offene Punkte und verwendete Tools.
7. Sicherheit: Geheimnisse nie in Prompts/Logs; Least Privilege; personenbezogene Daten minimieren.
8. Freigaben: Deployment, Zahlungen, Wallets, Veröffentlichungen, Kontenänderungen und Löschungen erfordern menschliche Freigabe.
9. Beobachtbarkeit: korrelierte Audit-Events, Zeitstempel, Agent-Version, Kosten und Fehler.
10. Tests: Vertragstests, Persona-Regression, Memory-Isolation, Berechtigungsprüfung und Fehler-/Timeout-Verhalten.

## Pilotdienst
Vorgeschlagener Pilot: **AUREALIS INFINITY als read-only Status-/Katalogadapter**. Grund: klar abgegrenzter Umfang; zunächst keine Schreibrechte, keine Wallets, keine Deployments. Pilot ist noch nicht als ausgeführt markiert.

## Testfälle für den Pilot
- T01 Agentenliste ist nur mit gültigem Token erreichbar.
- T02 Ohne Token wird 401 zurückgegeben.
- T03 Read-only-Routen verändern keine Daten.
- T04 Agenten-IDs bleiben stabil und eindeutig.
- T05 Persona-Kurzbeschreibung wird unverändert ausgeliefert.
- T06 Memory-Namespaces sind getrennt; bis technische Implementierung vorhanden ist, muss der Test als BLOCKED markiert werden.
- T07 Nicht erlaubte Schreibaktionen werden nicht angeboten.
- T08 Fehlerhafte/unbekannte Agenten-ID wird kontrolliert abgewiesen.
- T09 Timeout/Provider-Ausfall erzeugt keine Teiländerung.
- T10 Deployment-/Zahlungs-/Wallet-/Publishing-Aktionen verlangen menschliche Freigabe.

## Offene Stage-2-Arbeiten
- Original-System-Prompts aus jedem produktiven Repository/Service sichern und mit Hash/Version erfassen.
- Tatsächliche Speicher- und Datenbankpfade je Agent prüfen.
- Live-Endpunkte, Auth und Event-/Webhook-Verträge je Dienst erfassen.
- Test-Suites je Dienst identifizieren und ausführen.
- Pilotadapter implementieren und die Tests gegen echte Staging-Endpunkte ausführen.
- 76 im aktuellen Render-Snapshot gelistete Services sind Inventarhinweise; der Snapshot enthält mehrere Duplikate und veraltete/ungeprüfte Statuswerte. Vor Live-Aussagen ist ein frischer Workspace-Abgleich nötig.

## Katalog
Die Website unter `/ideas/` ist ein konsolidierter Ideen- und Projektkatalog. Sie ist ein Arbeitsinventar aus verfügbaren Gesprächsnotizen und Repository-/Service-Namen, keine Behauptung vollständiger Historie.
