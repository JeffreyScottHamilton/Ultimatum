# Project setup: identity, versions, icon, splash, permission text

Read when an Expo app is about to get its first store build, or `ult appstore check` reports AS010 to AS057.

Everything here lives in the app config: `app.json` (keys under `expo`) or a dynamic `app.config.js`/`.ts`. Expo turns it into the native `Info.plist` and project at build time, so with Continuous Native Generation (no committed `ios/` folder) the config is the only place to change. If the repo does commit an `ios/` folder, Expo does not rewrite it: make the same change in Xcode's files too, and say which side wins.

Reference pages: Expo's app config reference at https://docs.expo.dev/versions/latest/config/app/ and Apple's Info.plist keys at https://developer.apple.com/documentation/bundleresources/information-property-list.

## 1. Identity

| Setting | Where | Rule of thumb |
|---|---|---|
| Bundle ID | `ios.bundleIdentifier` | Reverse domain you control, e.g. `com.yourcompany.appname`. Letters, digits, hyphens and dots. It is permanent once the app record exists in App Store Connect, so settle it before the first upload. Never ship `com.example.*` or a template's ID. |
| Display name | `name` | What shows under the icon. The store name is set separately in App Store Connect (see `listing.md`). |
| Slug and owner | `slug`, `owner` | Identify the project on Expo's side; changing them later breaks update and build history links. |

The app record in App Store Connect (My Apps, then New App) needs the same bundle ID, registered under Certificates, Identifiers & Profiles. EAS can register it for you during the first `eas build` if the owner signs in; that is an account action, so ask first.

## 2. Version and build number

Apple tracks two numbers:

- **Version** (`version`, Apple's CFBundleShortVersionString): what customers see, three numbers such as `1.4.0`. Raise it for each release that goes to review.
- **Build number** (`ios.buildNumber`, Apple's CFBundleVersion): must go up for every upload under the same version. App Store Connect rejects a second upload with a number it has already seen.

Pick one owner for the build number and write it down:

- **Remote (recommended):** set `"cli": { "appVersionSource": "remote" }` in `eas.json` and `"autoIncrement": true` on the production profile. EAS keeps the counter and raises it on each build; `ios.buildNumber` in the config is then ignored, so delete it to avoid confusion (AS022). Seed or fix the counter with `eas build:version:set`; copy it back into a local config with `eas build:version:sync`. Check Expo's notes on runtime version policies before mixing this with `runtimeVersion: { "policy": "nativeVersion" }`.
- **Local:** you raise `ios.buildNumber` by hand before every production build. Run `ult appstore check --since <last release tag>` to catch a forgotten bump (AS025).

Expo's guide: https://docs.expo.dev/build-reference/app-versions/.

## 3. Icon

- One square PNG, 1024 by 1024 pixels, no transparency (Apple rejects an alpha channel in the store icon), no rounded corners (iOS adds the mask). Set it with `icon`, or `ios.icon` to give iOS its own.
- `ios.icon` can also take light, dark and tinted variants for the iOS 18 and later home screen styles; check the current Expo app config page for the shape it accepts.
- Keep important shapes away from the corners and make sure it still reads at 60 pixels.
- Apple's guidance: https://developer.apple.com/design/human-interface-guidelines/app-icons.

## 4. Splash screen

Use the `expo-splash-screen` config plugin in `plugins` with an image, a background colour and, if the app has a dark mode, a dark variant. Keep it simple: a centred logo on a plain colour. Hide it from code once the first screen has its data, so users do not see a blank frame. Expo's guide: https://docs.expo.dev/develop/user-interface/splash-screen-and-app-icon/.

## 5. Permission text (usage strings)

iOS shows a system prompt the first time an app asks for the camera, photos, location, contacts and so on. The prompt's text comes from a usage description key. If the key is missing the app crashes at that moment, and App Review rejects text that does not say why the app needs access.

How to set them:

1. Prefer the library's config plugin option, e.g. `["expo-camera", { "cameraPermission": "..." }]`. Listing the plugin without the option ships Expo's generic default text (AS032).
2. Otherwise set the key directly in `ios.infoPlist`, e.g. `"NSCameraUsageDescription": "..."`.
3. Only ask for what the app uses. Remove a library you no longer call, or its plugin may still add a key and a prompt.

Write each one as: what the app does with it, in the user's terms, and what they get. One sentence is enough.

- Weak: "This app needs camera access." / "Needed."
- Better: "Tide Notes uses the camera to scan paper notes into your notebook."

Common keys: NSCameraUsageDescription, NSMicrophoneUsageDescription, NSPhotoLibraryUsageDescription, NSPhotoLibraryAddUsageDescription, NSLocationWhenInUseUsageDescription, NSLocationAlwaysAndWhenInUseUsageDescription, NSContactsUsageDescription, NSCalendarsFullAccessUsageDescription, NSRemindersFullAccessUsageDescription, NSFaceIDUsageDescription, NSMotionUsageDescription, NSSpeechRecognitionUsageDescription, and NSUserTrackingUsageDescription for the App Tracking Transparency prompt. Apple's list: https://developer.apple.com/documentation/bundleresources/protected-resources.

`ult appstore check` maps installed Expo packages to the keys they need (AS030) and flags vague or very short text (AS031). It cannot see a native module that asks for a permission without a known package; search the code for `request*Permission` calls too.

## 6. Export compliance

Each upload asks whether the app uses non-exempt encryption. Most apps only use HTTPS and standard OS crypto, which is exempt; set `ios.config.usesNonExemptEncryption: false` so the question is answered in the build (AS056). If the app ships its own encryption, the owner must answer the export questions in App Store Connect and may need documents. Apple's overview: https://developer.apple.com/documentation/security/complying-with-encryption-export-regulations.

## 7. Privacy manifest

Covered with the review check in `review-check.md` § 3, because it must match the privacy answers given in App Store Connect.

## 8. iPad

`ios.supportsTablet: true` makes the app run full screen on iPad, which means App Review will test it there and the listing needs iPad screenshots (AS057). Leave it off unless the layout has been checked on an iPad size.
