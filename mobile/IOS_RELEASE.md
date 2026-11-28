# ULTIMA ONE – iOS release setup

The Expo shell now includes a native iOS hub with a home dashboard, search and category filters, quick links to central services, an embedded service view, native navigation back to the hub, refresh, loading state and external-open action. The existing ULTIMA web portal remains the full catalogue for the inventoried websites and repositories.

## Build and submit

1. Install Node.js LTS and EAS CLI: `npm install -g eas-cli`.
2. From this directory run `npm install`.
3. Test on a physical iPhone with `npx expo start`.
4. Sign in to Expo with `eas login` and configure the project with `eas build:configure`.
5. Add the generated Expo project ID under `expo.extra.eas.projectId` in `app.json`.
6. Confirm final icon, screenshots, privacy policy URL, support URL, age rating and all service URLs.
7. Run `npm run build:ios`. EAS requires Apple signing credentials and an Apple Developer Program membership for App Store distribution.
8. Test the signed build with TestFlight, then submit it in App Store Connect.

## Release gate

This repository contains source code, not a signed IPA. Apple signing credentials, App Store Connect access, final icon/screenshots, privacy disclosures and Apple review approval are not present or completed here. Apple may reject apps that are primarily website wrappers. The native dashboard is an initial native feature set, not a guarantee of acceptance. Before submission, test every service on iPhone and complete privacy disclosures, account deletion, moderation and legal-rights checks.

Shop systems and Rothshild remain separate; this app does not merge their accounts, checkout, data or AI systems.

## Official Apple links

- Enrol: https://developer.apple.com/programs/enroll/
- App Store Connect: https://appstoreconnect.apple.com/
- App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
