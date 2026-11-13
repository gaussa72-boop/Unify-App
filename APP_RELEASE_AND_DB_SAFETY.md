# App Release and Database Safety

## Current app source package
A generated source archive contains 21 Expo / React Native starter projects corresponding to the 21 Render services currently confirmed live in the selected workspace.

Important: these are development starters with a WebView wrapper, not signed IPA/AAB binaries and not Apple/Google-approved releases. Apple may reject a simple website wrapper if it does not provide sufficient native functionality. Before submission, add meaningful native features, complete privacy disclosures, age rating, screenshots, support contact, review notes, icons, and legal rights checks.

Build steps for each app:
1. Install Node.js LTS and run `npm install`.
2. Install EAS CLI: `npm install -g eas-cli`.
3. Sign in: `eas login`.
4. Set a unique, final bundle identifier / Android package name and app assets.
5. Add native value and validate privacy/data collection declarations.
6. Run `npx expo start` and test on physical iOS and Android devices.
7. Build: `eas build --platform ios` and `eas build --platform android`.
8. Test signed builds with TestFlight / internal Play testing.
9. Submit only after store metadata and privacy information are accurate.

Official Apple resources:
- https://developer.apple.com/programs/
- https://appstoreconnect.apple.com/
- https://developer.apple.com/app-store/review/guidelines/

Official Android resources:
- https://play.google.com/console/
- https://developer.android.com/guide/app-bundle

## Database preservation — no migration performed
The selected Render workspace `tea-dbrofpkipgvc739nfeeg` was checked for Render Postgres instances and returned **no Postgres instances found**.

This is not proof that all repositories have no databases. It means no Render Postgres database was available in the selected workspace to back up or migrate. Other Render accounts/workspaces must be inspected only after their correct workspace has been explicitly selected. No workspace should be guessed.

No production database has been copied, reset, overwritten, or migrated in this pass. No data-loss-prone migration was run.

Before any migration:
1. Identify each service's actual database source (Render Postgres, external Postgres, SQLite, managed provider, or file store).
2. Verify authorized read access and capture exact source connection details in secure settings only.
3. Take a consistent database backup and separately back up uploaded files / object storage.
4. Record schema version, table names, row counts, indexes, constraints, and sample business records.
5. Restore the backup into a separate staging database and compare the restored result.
6. Run migration scripts against staging, check foreign keys, unique constraints, timestamps, money precision, and user/order relationships.
7. Switch production only after approval and a tested rollback plan.
8. Compare counts and critical records after cutover; retain the original backup according to a defined retention policy.

Never store database URLs, passwords, API keys, Telegram tokens, or payment secrets in Git. Render free filesystems are ephemeral; SQLite files on an ephemeral service filesystem must not be treated as durable production storage.

## Render deployment verification — 2026-11-13
- The 18 newly created services have their latest deployment status reported as `live`.
- Recent error-level log queries returned no entries for the 17 services queried after deployment. AI Quantumlight had earlier logged a missing `SECRET_KEY`; a random secret was configured in Render Environment, and its latest deployment is live.
- A live deployment status is not an end-to-end business acceptance test. Payment settlement, Telegram bot delivery, AI provider calls, login, order creation, and database persistence still require functional tests with the correct private credentials and test data.
- The Render API rate limit prevented creating additional services for Webshop.Parfum, IPad-App.IONOS-7, and the standalone QUANTUM-MIRROR-DARK-WONDERLAND during the last attempt. Retry after the rate limit clears.
- Render repository access still needs to be granted for private repositories IONOS-7, Bullrun.Apparel, and Quantenformel.QAI.

## Daily learning schedule
The daily practical coding lesson is scheduled for 18:00 Europe/Berlin. It covers code purpose, line-by-line behavior, data flow, APIs, Telegram bots, database operations, GitHub, Render deployments, security, exercises, and review. It continues previous fundamentals lessons and expands into OOP, web development, APIs, SQL, Linux, Docker, cybersecurity, AI/ML, RAG, agents, and app publishing.