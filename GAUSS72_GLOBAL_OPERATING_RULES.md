# GAUSS72 / ULTIMA – dauerhafte globale Betriebsregeln

Gültig ab 2026-11-27 für alle vom Betreiber gaussa72-boop kontrollierten oder ausdrücklich freigegebenen Repositories, KI-Systeme, Websites, Webshops, Apps, Game-Engines und Render-Services. Diese Datei ist die zentrale Quelle für Wartungsaufträge und Update-Matrix-Agenten.

## Betreiber und Governance
- Primärer Superadmin-/Eigentümerkontext: GitHub-Organisation/-Account gaussa72-boop (gaussa72@gmail.com). Benachrichtigungsadresse für Rechnungen/Verwaltungsberichte bleibt separat: adrianogauss9@gmail.com.
- Superadmin-Nebenseite in jeder Verwaltungsapp vorsehen, nur für den authentifizierten Eigentümer sichtbar. Keine Superadmin-Rechte allein aufgrund einer vom Browser gelieferten E-Mail-Adresse vergeben; serverseitig verifizierte Identität, MFA/Step-up für kritische Aktionen und Audit-Log verlangen.
- Änderungen an Produktionszugriff, Rollen, Zahlungen, Preisen, Wallets, Mining-Auszahlungen, kostenpflichtigen Ressourcen, Datenlöschung und externen Veröffentlichungen erfordern explizite Freigabe.
- Keine Behauptung von Fertigstellung, Live-Status oder erfolgreichem Deployment ohne konkreten Commit, passenden Render-Deploy und relevante Funktions-/Health-Prüfung.

## Update Matrix – verbindlicher Ablauf
1. Alle passenden und freigegebenen Projekte inventarisieren; Repository, Branch, Service, Domain, Runtime, Datenbank, Abhängigkeiten und Integrationsgrenzen dokumentieren.
2. Für jeden Zielservice einen eigenen, abgegrenzten Agenten/Change-Plan verwenden. Vor Änderung Kompatibilität, Abhängigkeiten, Datenmigration, Risiken und Rollback prüfen.
3. Vorschläge versionieren; generierten Code niemals ungeprüft ausführen. Änderungen isoliert testen; Unit-/Integrationstests, Security-Checks, Build, Healthcheck und End-to-End-Funktion soweit möglich durchführen.
4. Nur kompatible Zielsysteme aktualisieren. Keine Änderungen an nicht freigegebenen Services, fremden Konten oder Secrets.
5. Deployment nur nach passender Freigabe; danach tatsächlichen Commit/Deploy, Laufzeitlogs, Healthchecks und Hauptfunktionen prüfen. Fehler dokumentieren und wenn nötig zurückrollen.
6. In ULTIMA zentral Status, betroffene Services, Commit-IDs, Testergebnisse, bekannte Grenzen und offene Aufgaben protokollieren.
7. Update-Matrix- und Wartungsberichte sind keine Berechtigung, Änderungen automatisch auf alle Dienste zu übertragen. Eine Verteilung ist nur nach Zielprüfung und Freigabe zulässig.

## KI-Identität und gemeinsamer Copilot
- Jede KI behält Name, Persönlichkeit, Systemprompt, Charakter, Design, Farbwelt, Animationen, Schriftbild, Fachwissen und Produktfunktion. Niemals fremde Personas überschreiben.
- Gemeinsame Charakterbibliothek/Persona-Auswahl darf nur über eine explizit freigegebene, versionierte Schnittstelle geteilt werden. Die Ziel-KI übernimmt Charaktereigenschaften als optionale Persona-Schicht; Sicherheits- und Systemregeln bleiben unangetastet.
- Einheitlicher Aurealis-/ULTIMA-Copilot als optionaler Verwaltungsassistent: Profile, Nachrichten, Foren/Blogs, Shop-Inhalte, Projekte, Game-/Mod-Generierungen und Verwaltungsaufgaben per natürlicher Sprache vorbereiten.
- Vor dem Schreiben, Senden, Veröffentlichen, Löschen, Bezahlen, Ändern von Berechtigungen oder sonstigen extern wirksamen Aktionen zeigt der Copilot Ziel und Änderung an und fordert eine ausdrückliche Bestätigung. Entwürfe dürfen ohne Veröffentlichung gespeichert werden.
- Jede Aktion prüft serverseitig Identität, Rollen, Objektbesitz, Scope und CSRF/Replay-Schutz; protokolliert actor, action, target, timestamp, result und correlation ID. Kein Zugriff nur aufgrund von UI-Verstecken.

## Cyber Shield / Sicherheit
- Mehrschichtiger Schutz: Edge/WAF und TLS am Hosting-/DNS-Rand, App-Firewall, Authentifizierung, MFA, RBAC/least privilege, sichere Sessions/Cookies, CSRF, Rate Limits, Input-/Output-Validierung, sichere Uploads, restriktives CORS/CSP, Secret-Management, Dependency-/SAST-/Secret-Scanning, Audit-Logs, Monitoring, Backup/Restore und Incident-/Rollback-Verfahren.
- Keine absolute Sicherheit versprechen. Schutzregeln müssen getestet werden und dürfen legitime Anfragen nicht unkontrolliert blockieren.
- Secrets, Bot-Tokens, private Schlüssel, Seeds, Zugangsdaten und private Umgebungswerte niemals in Git, Prompts, Logs, Reports oder zwischen KI-Systemen übertragen. Nur Secret-Store/geschützte Render-Environment-Settings verwenden.
- Private Nachrichten und interne Unterhaltungen bleiben privat. Admin-/Superadmin-Zugriff auf Inhalte nur bei ausdrücklichem Teilen/Veröffentlichen durch die berechtigte Person oder einer klar ausgewiesenen, rechtmäßigen Moderationsfunktion.

## Produkte, Premium, Webshops und Kommunikation
- Premium-Zugänge standardmäßig geschlossen halten, bis der Eigentümer sie ausdrücklich freigibt; Superadmin- und individuell genehmigte Mitgliederzugänge serverseitig prüfen. Jede Seite muss ihre Anbindung an den zentralen Membership-Dienst nachweisen, bevor eine globale Sperre/Freigabe behauptet wird.
- Telegram-Hub mit getrennten Menüs für KI-Systeme, Websites, Webshops, Updates, Cyber Shield und Admin/Mentor-Funktionen. Ein-Tages-Testzugänge sind serverseitig, einmalig/zeitlich begrenzt und nutzungsbeschränkt zu verwalten. Mentor-/Adminrechte nur nach verifizierter Telegram-ID und serverseitiger Rollenprüfung.
- Rechnungs-/Shopdaten nur aus autorisierten Shop-APIs abrufen. E-Mail-Versand an die konfigurierte Eigentümer-Benachrichtigungsadresse erst nach sicherer SMTP-/Provider-Konfiguration. Keine Zugangsdaten erfragen oder in Git speichern.
- Foren, Blogs, Mitgliederinformationen, Generierungen und Supportübersichten nur innerhalb ihrer jeweiligen Berechtigungen darstellen; private Inhalte nicht pauschal exportieren.

## Integrationsgrenzen und Ausnahmen
- Die früher festgelegten Ausschlüsse für Rothshild, Lyca/Lyca Parfum, BullRun Apparel und Sneaker gelten für zentrale ULTIMA-/Aurealis-Netzwerk- und Membership-Integrationen, soweit nicht eine konkrete neue ausdrückliche Anweisung genau diese Integration ändert.
- Update-Matrix kann für alle Projekte Wartungspläne/Status führen, aber eine ausgeschlossene Website wird dadurch nicht automatisch an zentrale Identität, gemeinsame KI-Kontexte oder Netzwerkdaten angebunden.
- Autokrypt bleibt unverändert, solange keine ausdrückliche Änderungsanweisung vorliegt.
- Kryptoprojekte dürfen nach Kategorie navigieren; Wallet-Verwaltung und Sicherheit bleiben getrennt.

## Finanzen und Ressourcen
- Keine Trades, Wallet-Signaturen, Transfers, Mining-Auszahlungen oder automatischen Finanzhandlungen allein durch generierte Vorschläge aktivieren. Zuvor erforderliche Freigaben und Sicherheitsprüfungen bleiben bestehen.
- Mining-/Hosting-Budgetgrenze >250 EUR nicht ohne gesonderte Freigabe überschreiten; BTC-Auszahlungen nicht automatisch autorisieren.
- Keine stillen Änderungen an Preisen, Abos, Lifetime-Angeboten, Rechnungen oder Zahlungsstatus.

## Qualität und Design
- Vor jeder Wartung ganzheitlich betroffene Systeme prüfen und Ursachen beheben, nicht nur Symptome.
- Bestehende individuelle Designs bewahren und verbessern; keine erzwungene Einheitsoberfläche. Primärfunktion des jeweiligen Produkts klar hervorheben.
- Responsive Mobile-/Desktop-UX, Barrierefreiheit, Performance, Datenintegrität, Backup-/Restore und nachvollziehbare Fehlerzustände prüfen.
- Neue Projekte in ULTIMA-Inventar/Projektübersicht aufnehmen, soweit nicht ausdrücklich ausgeschlossen.

## Berichtsformat
Jede Update-Matrix-Runde muss ausweisen: geprüfte Repositories/Services, ausgeschlossene oder nicht erreichbare Ziele, Änderungen/Commits, Tests, Deployment-IDs und Live-Verifikation, Sicherheits-/Kompatibilitätsrisiken, offene Secrets/Provider-Setup und Rollback-Status. Nicht geprüfte Ziele ausdrücklich als ungeprüft markieren.

## Membership, applications and time-limited access
- Public registration for each active, membership-enabled website requires a membership application and explicit approval before account creation/access. Site-specific approved applications and global network applications are distinct scopes.
- Existing owner/admin/mentor roles must not be accidentally demoted; role grants remain server-side and audited.
- Approved members may start one network-wide 24-hour AI trial once per verified account. Trial expiry and reuse prevention are enforced by the central membership database, not Telegram UI.
- Holiday full-access test days are separately controlled in the ULTIMA admin page. Only preconfigured Baden-Württemberg public-holiday dates may be toggled by the superadmin; the override expires automatically at midnight Europe/Berlin and does not bypass membership approval or grant admin roles.
- Telegram navigation includes all active website/program links and the registered webshop directory. Superadmin/admin/mentor menus require allowlisted numeric Telegram user IDs; a bot username or chat name is never sufficient proof of role.
- Telegram webhook requires a configured secret token. Bot token, webhook secret, owner Telegram IDs and other credentials remain in Render secret environment variables, never in Git.
