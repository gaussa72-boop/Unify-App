# ULTIMA Central

Central portfolio launcher for the user's websites, apps and GitHub projects.

## Live website
After the Render static-site deployment completes:
https://ultima-central-r88g.onrender.com

## Features
- Responsive dark/gold/cyan portfolio dashboard
- Search and category filters
- Direct links to GitHub repositories
- Live links only for Render services whose deployment was confirmed (NovaTube and IONOS KI)
- Installable PWA manifest, service worker and app icon
- Native Expo / React Native WebView app shell in `mobile/`

## Native iOS / Android app
1. Install a compatible Node.js and npm.
2. Enter `mobile/`.
3. Copy `.env.example` to `.env` (already contains the current Render portal URL).
4. Run `npm install` and `npx expo start`.
5. Build signed binaries using EAS Build or a supported newer macOS/Xcode environment.

The Expo project is a native app shell around the central portal. It is not yet an App Store / Play Store release. Catalina 10.15.8 cannot run current Xcode toolchains, so use a cloud build or newer Mac for current iOS binaries.

## Scope and security
This repository currently provides a portfolio launcher, not a universal identity provider or privileged control plane. The existing Flask account prototype is not deployed by the static Render blueprint. Do not use it for production authentication until verified email, MFA, secure admin bootstrap/invitations, persistent PostgreSQL, rate limits, audit logs, recovery and OIDC/client registration are implemented and reviewed.

No passwords, API keys, bot tokens, payment credentials or private environment values belong in Git. Store deployment secrets only in the relevant service's environment settings.

## Deployment
Render Blueprint: `render.yaml` (static site, free plan, Frankfurt). Auto-deploy is enabled for commits to `main`.
