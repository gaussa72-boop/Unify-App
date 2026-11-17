# ULTIMA Central

Central portfolio launcher for websites, apps and GitHub projects.

## Live portal
https://ultima-central-bt56.onrender.com

## Features
- Responsive ULTIMA dark/gold/cyan portfolio dashboard
- Search and category filters for the connected project portfolio
- GitHub source links and confirmed Render live-service links
- Installable PWA manifest, service worker and icon
- Native Expo / React Native WebView app shell in `mobile/`

## Native iOS / Android app
1. Install a compatible Node.js and npm.
2. Enter `mobile/`.
3. Copy `.env.example` to `.env` (it contains the current portal URL).
4. Run `npm install` and `npx expo start`.
5. Use EAS Build or a supported newer Mac/Xcode environment for signed iOS and Android release builds.

This is a native app shell that opens the central portal. It is not yet an App Store / Play Store release. macOS Catalina 10.15.8 is too old for current Xcode toolchains; use cloud build or newer macOS for current iOS binaries.

## Scope and security
This project currently provides a portfolio launcher, not a universal identity provider or privileged control plane. The older Flask account prototype in `app.py` is not used by the deployed service. Do not connect production authentication to that prototype until verified email, MFA, secure admin bootstrap/invitations, persistent PostgreSQL, rate limits, audit logs, recovery and OIDC/client registration have been implemented and reviewed.

No passwords, API keys, bot tokens, payment credentials or private environment values belong in Git. Store deployment secrets only in each service's environment settings.

## ULTIMA AI Personal Command Center

The authenticated `/assistant/` page is the first dashboard prototype for the planned ULTIMA AI assistant. It includes browser-only optional voice input and a status endpoint. It does **not** install a desktop background agent or control the user's computer, phone, or email. The desktop agent, mobile companion, OAuth email integrations, and permissioned action runner remain separate implementation milestones.

Security model: least-privilege OAuth, per-device pairing, scoped permissions, approval for external communications, payments, deletion, account/security changes and publishing, immutable audit events, visible microphone status, and an emergency stop. Never store email passwords, API keys, or device credentials in Git.

Project inventory: `data/project_registry.json` records the currently inventoried Render workspaces and GitHub repositories. It is an inventory snapshot only; it does not move or rename live projects.

## Deployment
Render Blueprint uses `portal_server.py`, Python 3.11 and the free Frankfurt web-service plan. Auto-deploy is enabled for pushes to `main`.
