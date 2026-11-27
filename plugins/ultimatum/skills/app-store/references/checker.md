# `ult appstore check`: what each finding means

Read when `ult appstore check` printed a code you need to act on, or to know what the check does and does not cover.

```bash
ult appstore check --root <app folder> [--config resolved.json] [--since <git ref>] [--json]
```

It reads `app.json` (or `app.config.json`, or the file given with `--config`), `eas.json`, `package.json`, the store config named by `eas.json` `submit.production.ios.metadataPath` (default `store.config.json`), the icon PNG, and file names in the project. It uses the Python standard library only, makes no network calls and changes nothing.

- Exit **0**: no fail or warn findings (notes may remain).
- Exit **1**: at least one fail or warn.
- Exit **2**: bad input: missing folder, broken JSON, or only `app.config.js`/`.ts` (resolve it first with `npx expo config --json > app.config.resolved.json`, then pass `--config app.config.resolved.json`).

Levels: **fail** blocks an upload or review, or leaks a secret; **warn** is a likely rejection or a risky setting; **note** is something a person should look at. Clean output proves only that these checks passed, not that Apple will approve.

## Input

| Code | Level | Meaning |
|---|---|---|
| AS002 | note | A dynamic config sits beside `app.json` and may change it; the check read the static file only. |
| AS003 | note | `package.json` has neither `expo` nor `react-native`. |

## Identity (`setup.md` § 1)

| Code | Level | Meaning |
|---|---|---|
| AS010 | fail | No `ios.bundleIdentifier`. |
| AS011 | fail | Bundle ID has characters or a shape Apple does not accept. |
| AS012 | warn | Bundle ID is a placeholder such as `com.example.*`. |
| AS013 | warn | No `name`. |

## Versions (`setup.md` § 2)

| Code | Level | Meaning |
|---|---|---|
| AS020 | warn | No `version`. |
| AS021 | fail | `version` is not one to three whole numbers, e.g. `1.2.0-beta`. |
| AS022 | note | Build numbers come from EAS (remote), so `ios.buildNumber` in the config is ignored. |
| AS023 | warn | Local versioning with no `ios.buildNumber` and no `autoIncrement`. |
| AS024 | fail | `ios.buildNumber` is not made of whole numbers. |
| AS025 | fail | With `--since`: same version as the ref and the build number did not go up. |
| AS026 | fail | With `--since`: `version` went down. |
| AS027 | note | With `--since`: the config could not be read at that ref, so nothing was compared. |

## Permission text (`setup.md` § 5)

| Code | Level | Meaning |
|---|---|---|
| AS030 | fail | A package that asks for a permission is installed and its usage string is missing. |
| AS031 | warn | A usage string is vague or under 25 characters. |
| AS032 | warn | The package's config plugin is listed without its text option, so Expo's generic text ships. |
| AS033 | note | A package may ask for an extra permission (e.g. microphone with the camera); add the text if the feature is used. |

## Privacy manifest (`review-check.md` § 3)

| Code | Level | Meaning |
|---|---|---|
| AS040 | warn | No `ios.privacyManifests`; React Native's own use of UserDefaults needs declaring. |
| AS041 | fail | The manifest block has the wrong shape. |
| AS042 | fail | An `NSPrivacyAccessedAPIType` is not one of the known categories (often a typo). |
| AS043 | fail | An entry has no reasons, or a reason that does not look like Apple's codes. |
| AS044 | warn | A tracking or ads library is installed but `NSPrivacyTracking` is not true. |

## Icon, splash, encryption, iPad (`setup.md` § 3, 4, 6, 8)

| Code | Level | Meaning |
|---|---|---|
| AS050 | fail | No icon set. |
| AS051 | fail | The icon file does not exist. |
| AS052 | warn | The icon is not a PNG, so its size could not be read. |
| AS053 | warn | The icon is not 1024 × 1024. |
| AS054 | warn | The icon has an alpha channel. |
| AS055 | warn | No splash screen configured. |
| AS056 | warn | `ios.config.usesNonExemptEncryption` not set, so every upload asks the export question. |
| AS057 | note | `supportsTablet` is on: test on iPad and supply iPad screenshots. |

## eas.json (`builds.md`, `updates.md`, `submit-and-rejections.md`)

| Code | Level | Meaning |
|---|---|---|
| AS060 | warn | No `eas.json`. |
| AS061 | warn / note | A profile is missing: warn for production, note for development and preview. |
| AS062 | fail | The production profile is internal distribution or a development client. |
| AS063 | fail | The production profile builds for the simulator. |
| AS064 | note | The development profile is not a development client. |
| AS065 | note | No `submit.production.ios.ascAppId`; `eas submit` will ask. |
| AS066 | warn | `expo-updates` is installed but there is no `runtimeVersion`. |
| AS067 | note | `runtimeVersion` is a fixed string; change it by hand on every native change, or use a policy. |
| AS068 | warn | A store or preview profile has no `channel`, so updates cannot reach it. |

## Store listing (`listing.md`)

| Code | Level | Meaning |
|---|---|---|
| AS070 | warn | No store config file, so the listing could not be checked here. |
| AS071 | warn | The store config has no `apple.info` block. |
| AS072 | fail / warn | No privacy policy URL (fail), or it is not HTTPS (warn). |
| AS073 | warn | No support URL, or it is not HTTPS. |
| AS074 | fail | A text field is over its character limit. |
| AS075 | fail | Keywords are over 100 bytes. |

## Policy risks (`review-check.md` § 5 and 7)

| Code | Level | Meaning |
|---|---|---|
| AS080 | warn | A Google or Facebook sign-in library is installed with no Apple sign-in package. |
| AS081 | note | A card-payments SDK with no in-app purchase library: decide which payment rule applies. |

## Secrets (`builds.md` § 2)

| Code | Level | Meaning |
|---|---|---|
| AS090 | fail | A signing or key file (`.p8`, `.p12`, `.mobileprovision`, `.keystore`, `.jks`) is inside the project. |
| AS091 | fail | Secret-looking text (a private key block, live payment key, cloud key, access token) in a config file. |
| AS092 | fail / warn | A secret-named value written into `eas.json` env (fail), or an `EXPO_PUBLIC_` one, which ships inside the app (warn). |
| AS093 | fail | `ascApiKeyPath` points inside the project. |

## Not covered

The check cannot see: native code that asks for permissions without a known package, whether privacy reasons are true, App Store Connect answers, the policy page's content, whether the backend is live, the build that Apple actually received, or anything in Apple's current guidelines. Those are in `review-check.md`.
