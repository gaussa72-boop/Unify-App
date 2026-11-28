# ULTIMA ONE – iOS release setup

## Implemented in source

- Native Expo / React Native iOS home dashboard with ULTIMA dark/gold/cyan styling
- Search and category filters across the inventory snapshot
- Catalogue of 76 Render service entries and 44 unique GitHub repositories
- Direct central shortcuts, embedded WebView service view, native back-to-hub navigation, refresh and external-open action
- On-device favourites and recently opened projects persisted with AsyncStorage
- Shop services remain separately categorized and do not share identity, checkout or AI integrations through this launcher

The catalogue is generated from `data/project_registry.json` (inventory snapshot dated 2026-11-23). It contains service entries, including multiple deployments of some projects; it is not a live health check. Reconcile the inventory against current Render and GitHub before App Store metadata is finalized.

## Cloud build and submission

1. Enrol in the Apple Developer Program: https://developer.apple.com/programs/enroll/
2. Create/sign in to an Expo account: https://expo.dev/signup
3. Install EAS CLI: `npm install -g eas-cli`
4. From this directory run `npm install`.
5. Sign in with `eas login` and configure the project with `eas build:configure`.
6. Add the generated Expo project ID under `expo.extra.eas.projectId` in `app.json`.
7. Run `eas build --platform ios --profile production`. EAS requires Apple Developer membership and valid Apple signing credentials for an App Store distribution build.
8. Test the build using TestFlight, then submit it with `eas submit --platform ios` or App Store Connect.

## App Store release gates

- No signed IPA has been generated and no EAS cloud build has been started.
- Apple Developer membership, Apple signing credentials and App Store Connect access are not configured.
- Expo account and EAS project ID are not configured.
- App icon, iPad/iPhone screenshots, support URL, publicly accessible privacy policy and App Store metadata are not finalized.
- Privacy details must accurately describe data collected by the native app and all embedded third-party websites. Do not publish a guessed privacy policy.
- Test each service URL, authentication flow, cookies, navigation and error states on physical iPhone and iPad.
- Apple Guideline 4.2 requires meaningful app-like functionality beyond a repackaged website or simple link collection. Favourites and recent history add native utility, but approval is not guaranteed; further native workflows and review are needed.
- Ensure rights/authorization for every third-party service and provide App Review with access to account-gated features or a review/demo mode.

## Official links

- Apple Developer enrollment: https://developer.apple.com/programs/enroll/
- App Store Connect: https://appstoreconnect.apple.com/
- Apple App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- Expo EAS iOS production build: https://docs.expo.dev/tutorial/eas/ios-production-build/
- Expo Submit: https://docs.expo.dev/submit/ios/
