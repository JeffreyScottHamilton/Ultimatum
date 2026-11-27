# Updates: EAS Update or a new store build

Read when a change is ready for users of an app already on the store, to decide whether an over-the-air update is allowed and safe, or a new build and review are needed.

Expo's guides: https://docs.expo.dev/eas-update/introduction/ and https://docs.expo.dev/eas-update/runtime-versions/. Apple's rule on downloaded code sits in the App Review Guidelines around 2.5.2 and in the Apple Developer Program License Agreement; fetch the current text (`review-check.md` § 0).

## 1. How EAS Update works

A store build contains the native code plus a JS bundle and assets. With `expo-updates`, the build checks its channel for a newer JS bundle and assets and loads them on the next launch. An update reaches a build only if both share a **runtime version** and the build's **channel** points at the branch the update was published to.

Set these up before the first store build, or updates cannot reach it:

- `runtimeVersion` in the app config. Use a policy: `{ "policy": "fingerprint" }` (changes whenever native code changes; safest) or `{ "policy": "appVersion" }` (changes with `version`; you must raise `version` for every native change). A fixed string works only if you change it by hand every time (AS067). Missing entirely with `expo-updates` installed is AS066.
- A `channel` on the preview and production build profiles (AS068).
- `updates.url` set by `eas update:configure`.

## 2. The decision

| Change | Ship as |
|---|---|
| JS logic, copy, styles, screens built from existing components | EAS Update |
| Images, fonts and other assets loaded by JS | EAS Update |
| A bug fix in JS | EAS Update, then fold into the next build |
| New or upgraded library with native code, or an Expo SDK upgrade | new build and review |
| Any app config change that ends up native: permissions and usage strings, icon, splash, bundle ID, entitlements, plugins, `infoPlist` | new build and review |
| `version` change for the store | new build and review |
| A new feature or a change to what the app is for | new build and review, even if it is all JS |

The last row is Apple's rule, not a technical one: downloaded code may fix and improve the app, but must not change its main purpose, add features that would need review, or get around review. When in doubt, submit a build.

## 3. Publishing an update safely

Updates reach real users within minutes, so treat them like a release. Ask the owner before publishing to a live channel.

1. Publish to the preview channel first: `eas update --channel preview --message "<what changed>"` and test it on a preview build on a device.
2. Check the runtime version printed by the command matches the store build's (Expo's dashboard shows both).
3. Publish to production, ideally with a rollout percentage if the project uses it: `eas update --channel production --message "<what changed>"`.
4. Watch crash reports. To undo, republish the last good update (`eas update:republish`) or follow Expo's rollback guide: https://docs.expo.dev/eas-update/rollbacks/.

## 4. Store builds still need

- A higher build number for every upload, and a higher `version` for every release to review (`setup.md` § 2).
- Updated listing text (What's New), and privacy answers if a new SDK collects data.
- A fresh pass of `ult appstore check --since <last release tag>` and the review check.
