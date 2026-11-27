# Builds: EAS Build profiles and credentials

Read when setting up or changing `eas.json`, choosing which build to make, or when `ult appstore check` reports AS060 to AS068 or AS090 to AS093.

Expo's references: https://docs.expo.dev/build/eas-json/ and https://docs.expo.dev/app-signing/managed-credentials/.

## 1. The three profiles

| Profile | For | Key settings | Installs on |
|---|---|---|---|
| `development` | the team, day to day | `"developmentClient": true`, `"distribution": "internal"`; `"ios": { "simulator": true }` in a copy if someone has a Mac | registered devices (ad hoc), or a simulator |
| `preview` | testers before the store | `"distribution": "internal"`, the release JS bundle, a `preview` channel | registered devices, from a link |
| `production` | TestFlight and the App Store | `"distribution": "store"` (the default), `"autoIncrement": true`, a `production` channel | through App Store Connect only |

A minimal shape, with shared values in a base profile:

```json
{
  "cli": { "version": ">= 12.0.0", "appVersionSource": "remote" },
  "build": {
    "base": { "node": "20.18.0" },
    "development": { "extends": "base", "developmentClient": true, "distribution": "internal", "channel": "development" },
    "preview": { "extends": "base", "distribution": "internal", "channel": "preview" },
    "production": { "extends": "base", "autoIncrement": true, "channel": "production" }
  },
  "submit": { "production": { "ios": { "ascAppId": "<numeric Apple ID>" } } }
}
```

Check the current Expo page for the CLI version and image names before copying a value. Things `ult appstore check` fails on: a production profile set to internal distribution or a development client (AS062), or one that builds for the simulator (AS063); none of those can be uploaded.

## 2. Credentials stay with EAS

The safe default: let EAS create and store the distribution certificate and provisioning profile on the owner's first `eas build -p ios --profile production`. EAS asks the owner to sign in to Apple once, then reuses them. Nothing secret enters the repo.

- See or reset them with `eas credentials` (account action, ask first).
- If the team must hold its own files, use `credentials.json` with `"credentialsSource": "local"` only on a machine that keeps those files out of git, and add them to `.gitignore` before they exist. Prefer EAS.
- Values the build needs at run time (a public API base URL) go in `env` in the profile or in EAS environment variables. Secrets (a payments secret key, a server token) never go in the app at all: the app is a public download and anything inside it can be read. Keep them on the server.
- `EXPO_PUBLIC_` variables are compiled into the JS bundle by design; never give one a secret (AS092 warns).
- `ult appstore check` fails on signing files anywhere in the project (AS090), secret-looking text in the config files (AS091), a secret-named literal in `eas.json` env (AS092) and an `ascApiKeyPath` that points inside the project (AS093).

If a key was ever committed, removing the file is not enough: the owner must revoke it (App Store Connect, Users and Access, Integrations) and make a new one. Say so.

## 3. Which build to make

| Need | Build |
|---|---|
| Native code changed (new library with native parts, config plugin, permission, Expo SDK upgrade, icon, splash, bundle ID) | new `development` build for the team; new `production` build for the store |
| Testers need to try a branch on their phones | `preview` |
| Anything bound for TestFlight or review | `production` |
| JS or asset change only, store build already out | maybe an EAS Update instead: see `updates.md` |

## 4. Running a build

Builds use the owner's Expo account and build minutes, and the first iOS build signs in to Apple. Always ask before starting one, and show the command:

```bash
eas build --platform ios --profile production
```

While it runs, the log is on expo.dev. When it fails: read the first error in the "Install dependencies", "Prebuild" or "Run fastlane" step, reproduce prebuild locally with `npx expo prebuild --clean` (works on Linux) and `npx expo-doctor` for dependency mismatches. Pods and Xcode compile errors can only be reproduced on a Mac.

## 5. Local builds

`eas build --local` and `npx expo run:ios` need macOS with Xcode. This container is Linux: it can edit, check and run `npx expo prebuild` to inspect the generated `Info.plist`, but not compile iOS.
