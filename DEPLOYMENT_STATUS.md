# ULTIMA Central — Deployment Status

Last reviewed: 2026-11-13

## Confirmed live Render services (21)

### Existing services
- ULTIMA Central — https://ultima-central-bt56.onrender.com
- NovaTube — https://novatube-studio-vli0.onrender.com
- IONOS KI — https://ionos-ki-v2-1oki.onrender.com

### Newly created services in Render workspace gaussadriano30
- Quantum.K — https://quantum-k-app.onrender.com
- Quantum.AI. — https://quantum-ai-app.onrender.com
- Quantum.KI.Ultra.Pro.V2 — https://quantum-ki-ultra-pro-v2-9pvf.onrender.com
- ultra-ki-v2 — https://ultra-ki-v2-app.onrender.com
- UltraKI.AI — https://ultraki-ai-app.onrender.com
- IONOS-8 — https://ionos-8-platform.onrender.com
- AI-Quantumlight — https://ai-quantumlight-k84q.onrender.com
- Quantum-KI-CAT.CHAT. — https://quantum-ki-cat-chat-2t79.onrender.com
- Quantum_Singularity — https://quantum-singularity-8liw.onrender.com
- galactic-ai-v3 — https://galactic-ai-v3-app.onrender.com
- Quantum.MIrror.Wonderland — https://quantum-mirror-wonderland-vibh.onrender.com
- Omega.Aurealis — https://omega-aurealis.onrender.com
- Lichtkrieger — https://lichtkrieger-hub.onrender.com
- Ate-Rea-Verm-chtnis — https://ate-rea-library.onrender.com
- Autokrypt-B-rse — https://autokrypt-boerse.onrender.com
- Drop-shipping — https://drop-shipping-store.onrender.com
- Aktiv-Lyca — https://aktiv-lyca-standalone.onrender.com
- sneaker — https://sneaker-store-27cn.onrender.com

All newly created services use the Frankfurt region, free plan, and automatic deploys from the main branch. "Live" here means Render reports a successful deployment; it does not certify every third-party integration, payment flow, bot, or AI API call.

## Remaining work and blockers

### Render API rate limit — retry required
These public repositories were inspected, but service creation was rejected by a Render API rate limit:
- ariandomimate-blip/Webshop.Parfum
- gaussa72-boop/IPad-App.IONOS-7
- gaussa72-boop/QUANTUM-MIRROR-DARK-WONDERLAND

### Private GitHub repositories not fetchable by this Render connection
Render rejected repository fetches for:
- gaussa72-boop/IONOS-7
- gaussa72-boop/Bullrun.Apparel
- gaussa72-boop/Quantenformel.QAI

Keep these repositories private. Grant the Render GitHub integration access to the relevant repositories, then create their services.

### Persistent storage, database, or secret prerequisites
Do not deploy these as production services on ephemeral free storage:
- Note-KI — SQLite database, uploaded files, and generated project files need persistent storage.
- Rea.Signature — SQLite order data and Telegram integration need persistent storage and bot secrets.
- The-Lord — configured blueprint requests a paid persistent disk and secret configuration.
- Quantenformel — Docker deployment requests a paid plan, persistent SQLite data, and an OpenAI API key.
- rothshild-order — its Render blueprint requests a paid PostgreSQL database and paid web plan. Keep it separate from the shared AI network.
- Ultra_KI_Merge — its configured blueprint requires an OpenAI API key; do not invent or commit one.

### Not a standalone production web app yet
- Ate-Rea- — repository is empty.
- Ate-Rea-Verm-chtnis-chronik — README only; no app source found.
- KI-Game-Mod — its README identifies Quantum.MIrror.Wonderland as the canonical integrated application; avoid deploying a duplicate.
- codex-relay — developer workspace / CLI monorepo, not a conventional public web app.
- IPad-App.IONOS-7 — currently a web shell/placeholder; no native Swift app source is present.

## Integration notes
- Aktiv-Lyca, Webshop.Parfum, sneaker, Bullrun, and Rothshild remain separate shop/service projects and are not added to the shared AI network.
- Drop-shipping currently returns HTTP 501 for checkout until a payment provider and supplier-order API are configured.
- Aktiv-Lyca's current server entry point serves the storefront and health route; Telegram checkout requires its bot tokens and webhook settings.
- AI services can boot without a configured OpenAI API key, but their AI features may remain unavailable until the key is added in each service's Render Environment settings.
- Never commit passwords, bot tokens, payment secrets, or OpenAI API keys to GitHub.
