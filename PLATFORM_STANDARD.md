# ULTIMA Platform Standard

Status: implementation specification and rollout contract (not yet a production identity/billing system).

## Product rules

- One ULTIMA identity per verified user. Central registration and profile are shared by participating applications.
- The trial is exactly 72 hours from the account's first successful email verification/activation, stored in UTC. It is one global trial, not a fresh trial for every application.
- During the trial, users may open all registered non-commerce applications marked `trial_enabled: true`.
- At trial expiry, the central entitlement service denies new sessions/access unless the user has an active Premium entitlement or an administrator has granted a Free exception.
- Free exceptions are explicit, revocable, auditable grants. Admins can set an optional expiry and a reason.
- Commerce/webshop projects are excluded from this trial/Premium gate and retain their separate checkout, identity, and operations.
- Rothshild remains outside the shared AI network and outside this access rollout unless separately approved.
- Premium payment collection is not enabled by this specification. Until a price and payment provider are chosen, Premium is an administrator-managed entitlement only; never simulate a successful payment.

## Central identity and access

- ULTIMA Central is the identity provider and application catalogue.
- Each application is registered with a unique client ID, allowed redirect URLs, audience, scopes, status, support configuration, and its own database connection.
- Use OIDC Authorization Code + PKCE for browser/mobile clients. Access tokens are short-lived, audience-restricted, and validated by each application's backend. Refresh tokens rotate and are revocable.
- Every protected application route checks the central entitlement service server-side. Hiding a tile or button in the portal is not access control.
- Require verified email, rate limits, CSRF protection for cookie sessions, secure password hashing (Argon2id or bcrypt with current parameters), recovery flows, and MFA for administrators.
- Never store plaintext passwords, bot tokens, API keys, database URLs, or payment secrets in Git.
- Admin bootstrap must use a one-time invitation or protected environment configuration for the verified address `gaussa72@gmail.com`; do not hard-code an admin password or trust an email string alone.
- Admin profile view is limited to operationally necessary fields (verified email, display name, creation date, entitlement state, trial end, last login, support status). Sensitive fields and credentials are never exposed.
- Every admin action (grant/revoke Free, Premium change, app access, profile export, account suspension) writes an immutable audit event with actor, target, timestamp, action, and reason.
- Apply GDPR principles: data minimisation, privacy notice, retention/deletion workflow, export, and access logs.

## Per-application standard

Every eligible current and future application must receive:
1. Its own dedicated production database (separate database instance/credentials; no shared customer tables across applications).
2. A migration folder and versioned schema; backups and tested restore procedure before customer data is stored.
3. An application admin website with role-protected edit controls, settings, user access state, content/configuration management, and audit history.
4. Its own Telegram support bot, with a unique BotFather token stored as `TELEGRAM_BOT_TOKEN` in that application's secret environment. Bot tokens are never committed.
5. A support handoff to central contact `@Ari_phenex` when the local bot is not configured or cannot answer.
6. OIDC client registration, entitlement middleware, health checks, error monitoring, and a deployment checklist.
7. A registry entry in `registry.json`; CI must reject an eligible app release if required security/configuration files are missing.

The local application database stores only local application data plus a minimal external identity reference (`ultima_user_id`). Central identity credentials remain central. Do not copy password hashes between applications.

## Current rollout exclusions

- All shops/webshops and checkout systems.
- Lyca, Parfum, Sneaker, Bullrun Apparel, Drop-shipping.
- Rothshild.
These remain separate and must not be silently enrolled in the shared trial, Premium gate, or shared AI network.

## Provisioning and cost guard

Dedicated persistent databases, backups, and always-on services may incur charges. Do not create paid Render resources automatically. Before provisioning, present the exact resource count, plan, region, and estimated recurring cost for approval. Free database tiers that expire or lack backups are not suitable for production customer profiles or orders.

## Rollout sequence

1. Create a dedicated GitHub repository for the ULTIMA platform core (the current GitHub integration exposes file/commit operations but no repository-creation action; until that is available, this specification is staged in the ULTIMA Central repository).
2. Implement and test central OIDC identity, email verification, MFA, profile, trial, entitlement API, and audit log.
3. Provision the central persistent database and backup/restore process.
4. Implement the Superadmin console with Free grants, expiry, revoke, and profile visibility.
5. Add per-app adapter, admin UI, dedicated DB, migrations, bot code, and health checks.
6. Integrate eligible applications in batches, test denied/allowed cases, then deploy.
7. For every future app, generate from the same adapter/template and register it before publishing.

## Acceptance tests

- A newly verified user receives one global 72-hour trial.
- Re-login and opening another eligible app do not reset the trial.
- At 72 hours, access is denied unless Premium or a valid Free grant exists.
- A Free grant can be created, extended, revoked, and audited by an authorized Superadmin.
- A non-admin cannot access profiles or admin routes.
- An app token for one audience cannot be replayed against another app.
- A commerce app is excluded from the trial/Premium middleware.
- A missing bot token produces a clear unconfigured state, not a fake successful support connection.
- Database migrations and restore are tested before production customer data is enabled.
