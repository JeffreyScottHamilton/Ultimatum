# Store listing: text, URLs, age rating, screenshot and preview specs

Read when filling in or changing the App Store product page, or when `ult appstore check` reports AS070 to AS075.

The listing is edited in App Store Connect, or kept in the repo as `store.config.json` and pushed with `eas metadata:push` (account action, ask first). Expo's guide: https://docs.expo.dev/eas/metadata/. Apple's field reference: https://developer.apple.com/help/app-store-connect/reference/app-information and https://developer.apple.com/help/app-store-connect/reference/platform-version-information. Character limits below were current when written; check those pages.

## 1. Text fields

| Field | Limit (check live) | Changes need a new version? | Writing it |
|---|---|---|---|
| Name | 30 characters | yes | the brand plus, if room, a plain word for what it does; must be unique on the store |
| Subtitle | 30 characters | yes | the one benefit, not a repeat of the name |
| Keywords | 100 bytes, comma separated | yes | single words, no spaces after commas, no repeats of words already in the name, no competitor or trademark names |
| Promotional text | 170 characters | no | current offer or news; can change any time |
| Description | 4000 characters | yes | first two lines carry the value, since the rest is folded; then features in short lines; no prices that may change, no keyword lists |
| What's New | 4000 characters | per version | what changed in words a customer cares about |

Keywords are counted in bytes, so accented and non-Latin letters take more room. `ult appstore check` counts the limits in `store.config.json` (AS074, AS075). Claims must match the build (`review-check.md` § 1).

## 2. URLs

- **Privacy policy URL:** required for every app. HTTPS, public, no sign-in, and the same policy linked inside the app (AS072).
- **Support URL:** required; a page with a way to reach a person (AS073).
- **Marketing URL:** optional.

## 3. Category, price and availability

Pick a primary and an optional secondary category that match what the app does most. Price, storefronts and release timing (manual, automatic, scheduled, phased release for updates) are set per version.

## 4. Age rating

The owner answers Apple's questionnaire in App Store Connect (App Information, Age Rating). Answer for everything reachable, including web views and user content. Apple revised the questionnaire and its age bands in 2025; read the current form and help page rather than assuming the old 4+/9+/12+/17+ set: https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating.

## 5. Screenshots: specs only

Read the live specification before capturing: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications. What it said when this guide was written:

- 1 to 10 screenshots per device size and language, JPEG or PNG, RGB, no transparency.
- iPhone: one set at the largest required size is enough; Apple scales it down for smaller phones. The page listed 6.9-inch portrait sizes such as 1320 × 2868 and 1290 × 2796, and older 6.5-inch sizes such as 1284 × 2778 and 1242 × 2688. Check which one the page marks as required today.
- iPad: required only if the app runs on iPad (`supportsTablet`). The 13-inch size was 2064 × 2752 or 2048 × 2732 portrait.
- The page also announced new required sizes for some future SDKs; read the dated notes at the top.

Content rules: real screens from the app in use, nothing it cannot do, no other platforms' devices, readable captions. Status bar with full signal and a clean time looks best. Captures need a device or simulator at that size: a Mac, or a real phone at the largest size.

## 6. App Preview videos: specs only

This skill does not plan, script or edit videos. If the owner already has one, check it against the live spec: https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications. When written, that page said:

- 15 to 30 seconds, up to 3 previews per device size and language, up to 500 MB.
- `.mov`, `.m4v` or `.mp4` with H.264, or ProRes 422 (HQ) in `.mov`; up to 30 frames per second; stereo audio if any.
- Resolution per device size, e.g. 886 × 1920 portrait for the large iPhone sizes and 1200 × 1600 for the 13-inch iPad; confirm on the page.
- Only footage captured from the app itself.

## 7. Localisation

Each language has its own name, subtitle, keywords, description and screenshots. Add a language only when the app itself is translated, or reviewers and users see a mismatch.
