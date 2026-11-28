# ULTIMA – Cross-platform app rollout matrix

Updated: 2026-11-28

## Scope

All 44 unique repositories currently visible in the two connected GitHub accounts are assigned a per-repository `CROSS_PLATFORM_RELEASE.md` rollout specification.

Each product is planned for:
- Android APK/AAB
- iOS/iPadOS IPA, TestFlight and App Store
- macOS signed/notarized app
- Windows installer/MSIX
- Linux AppImage/deb/rpm
- PWA where a browser UI exists

## Private superadmin distribution policy

- Every project is initially prepared for the owner's private superadmin use only. Build outputs must use authenticated/private distribution; do not publish public download URLs or public release assets until the owner explicitly approves marketing/public release.
- Build each application only after inspecting its actual frontend, framework, backend/API, data model, permissions and platform capabilities. Backend-only or library-only repositories must not receive a fake app wrapper; document SDK/API distribution instead.
- Use project-specific builds and identities. Preserve each project's branding, data, accounts, AI personality and checkout boundaries.
- Installable targets where technically supported: Android APK/AAB, iOS/iPadOS IPA, macOS app, Windows installer, Linux package and PWA.
- Store signing and distribution are separate from internal owner builds and require the relevant developer accounts, signing credentials and store review.

## Repository inventory

- [ ] [ariandomimate-blip/Aktiv-Lyca](https://github.com/ariandomimate-blip/Aktiv-Lyca) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [ariandomimate-blip/Webshop.Parfum](https://github.com/ariandomimate-blip/Webshop.Parfum) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [ariandomimate-blip/sneaker](https://github.com/ariandomimate-blip/sneaker) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [ariandomimate-blip/rothshild-order](https://github.com/ariandomimate-blip/rothshild-order) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [ariandomimate-blip/Drop-shipping](https://github.com/ariandomimate-blip/Drop-shipping) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [ariandomimate-blip/Autokrypt-B-rse](https://github.com/ariandomimate-blip/Autokrypt-B-rse) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [ariandomimate-blip/Ate-Rea-Verm-chtnis-chronik](https://github.com/ariandomimate-blip/Ate-Rea-Verm-chtnis-chronik) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Quantum.K](https://github.com/gaussa72-boop/Quantum.K) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Quantum.AI.](https://github.com/gaussa72-boop/Quantum.AI.) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Quantum.KI.Ultra.Pro.V2](https://github.com/gaussa72-boop/Quantum.KI.Ultra.Pro.V2) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/ultra-ki-v2](https://github.com/gaussa72-boop/ultra-ki-v2) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/UltraKI.AI](https://github.com/gaussa72-boop/UltraKI.AI) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/IONOS-7](https://github.com/gaussa72-boop/IONOS-7) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/IONOS-KI](https://github.com/gaussa72-boop/IONOS-KI) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/IPad-App.IONOS-7](https://github.com/gaussa72-boop/IPad-App.IONOS-7) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Quantum.MIrror.Wonderland](https://github.com/gaussa72-boop/Quantum.MIrror.Wonderland) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/AI-Quantumlight](https://github.com/gaussa72-boop/AI-Quantumlight) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Quantum-KI-CAT.CHAT.](https://github.com/gaussa72-boop/Quantum-KI-CAT.CHAT.) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/IONOS-8](https://github.com/gaussa72-boop/IONOS-8) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Quantum_Singularity](https://github.com/gaussa72-boop/Quantum_Singularity) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/galactic-ai-v3](https://github.com/gaussa72-boop/galactic-ai-v3) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/codex-relay](https://github.com/gaussa72-boop/codex-relay) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Bullrun.Apparel](https://github.com/gaussa72-boop/Bullrun.Apparel) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/KI-Game-Mod](https://github.com/gaussa72-boop/KI-Game-Mod) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Quantenformel.QAI](https://github.com/gaussa72-boop/Quantenformel.QAI) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Note-KI](https://github.com/gaussa72-boop/Note-KI) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Quantenformel](https://github.com/gaussa72-boop/Quantenformel) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/QUANTUM-MIRROR-DARK-WONDERLAND](https://github.com/gaussa72-boop/QUANTUM-MIRROR-DARK-WONDERLAND) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Rea.Signature](https://github.com/gaussa72-boop/Rea.Signature) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Ultra_KI_Merge](https://github.com/gaussa72-boop/Ultra_KI_Merge) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Quantum-Shield](https://github.com/gaussa72-boop/Quantum-Shield) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Ate-Rea-](https://github.com/gaussa72-boop/Ate-Rea-) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Ate-Rea-Verm-chtnis](https://github.com/gaussa72-boop/Ate-Rea-Verm-chtnis) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Novatube](https://github.com/gaussa72-boop/Novatube) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Omega.Aurealis](https://github.com/gaussa72-boop/Omega.Aurealis) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Lichtkrieger](https://github.com/gaussa72-boop/Lichtkrieger) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/The-Lord](https://github.com/gaussa72-boop/The-Lord) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Unify-App](https://github.com/gaussa72-boop/Unify-App) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Aurealis-Trading](https://github.com/gaussa72-boop/Aurealis-Trading) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Kryptoaurora](https://github.com/gaussa72-boop/Kryptoaurora) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Aurealis-Creative-AI](https://github.com/gaussa72-boop/Aurealis-Creative-AI) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Aurelis-Creative-AI-Studio](https://github.com/gaussa72-boop/Aurelis-Creative-AI-Studio) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/ate-rea-characterverse](https://github.com/gaussa72-boop/ate-rea-characterverse) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Neuroforge](https://github.com/gaussa72-boop/Neuroforge) – release spec committed; app implementation, signing, builds and tests still pending
- [ ] [gaussa72-boop/Aurealis-Shopping-AI](https://github.com/gaussa72-boop/Aurealis-Shopping-AI) – release spec committed; app implementation, signing, builds and tests still pending

## Required implementation order

1. Inspect each repository and determine if it is a frontend, full-stack application, backend/API, game, or infrastructure repository.
2. Frontend/full-stack products receive project-specific mobile, desktop and PWA clients. Backend-only repositories receive platform-specific client packages only where an actual user-facing product exists; otherwise document API/SDK integrations rather than wrapping an API as an app.
3. Preserve separate brand identity, accounts, databases, payment flows, AI personalities, data and permissions.
4. Use Capacitor for suitable web-based mobile clients, Tauri for desktop clients and PWA for web installation. Use native modules when product functionality requires them.
5. Build, test, sign and record actual APK/AAB, IPA, macOS, Windows and Linux artifacts. Store submission is separate and requires the appropriate developer accounts and review.
6. Keep ULTIMA project inventory synchronized for new repositories and new websites. Apply this matrix to every newly added user-owned website/repository by default.

## Deployment / current service status

Live Render API recheck on 2026-11-28: 85 services across the three connected workspaces; all 85 reported `not_suspended` (55 Workspace One, 6 Phenex, 24 Workspace 30). 84 report Auto Deploy enabled and one reports Auto Deploy disabled. `not_suspended` does not mean latest deployment is healthy. See `DEPLOYMENT_ENVIRONMENT_MATRIX.md` for service-to-repository mapping and environment-variable requirements.

A read of the three connected Render workspaces on 2026-11-28 returned 85 services: Workspace One 55, Phenex 6, Workspace 30 24. The Render API marked all 85 listed services as suspended in this inventory response. No restart, paid plan change, or deployment was triggered as part of this app-preparation pass. Re-check actual service state before resuming; resuming services may incur charges.

## Important boundaries

Rothshild, Lyca, BullRun and Sneaker remain separate from the shared ULTIMA/Aurealis integrations where previously requested. Their own app packaging is still included; this does not authorize merging their accounts, databases, checkout, or AI systems.

## Evidence discipline

A repository specification is not a native app, installer, signed build, successful deployment or store approval. Mark each platform complete only after the actual build artifact and test evidence exist.
