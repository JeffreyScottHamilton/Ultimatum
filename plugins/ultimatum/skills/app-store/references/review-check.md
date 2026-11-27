# Pre-submission review check

Read before submitting a version for App Review or an external TestFlight group, or after a rejection to see what else may be caught next time.

## 0. Fetch the current guidelines first

Apple revises the App Review Guidelines several times a year. Before using this check, fetch the live page and note its "last updated" date in your report:

- App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- What changed recently: https://developer.apple.com/news/ (filter for App Store)

The section numbers below are pointers to where a topic lived when this guide was written (page read 2026-11-27). Look the section up in the fetched page and work from its current text; never quote a guideline from memory or from this file. If a number has moved, say so.

## 1. The app is complete (around 2.1 and 2.3)

- [ ] No crashes, placeholder text, "lorem ipsum", test data, "coming soon" screens or broken links on any path a reviewer can reach.
- [ ] The backend, sign-in and any web content are live and reachable from Apple's network during review.
- [ ] Every feature the listing or screenshots mention is in this build; nothing in the listing promises more.
- [ ] Hidden or remotely switched-on features are disclosed in the review notes.
- [ ] It does something an app is needed for: not a thin wrapper around a website, not a copy of the owner's other apps (around 4.2 and 4.3).

## 2. Privacy policy and data (around 5.1.1 and 5.1.2)

- [ ] A privacy policy URL is in App Store Connect and the policy is reachable from inside the app (settings or the sign-up screen). `ult appstore check` looks for `privacyPolicyUrl` in the store config (AS072).
- [ ] The policy says what data is collected, how, what for, who it is shared with, how long it is kept, and how users can delete it.
- [ ] Each permission is asked for when the feature is used, with text that says why (`setup.md` § 5), and the app keeps working if the user says no.
- [ ] Users are not forced to grant access or share data the feature does not need.
- [ ] Tracking across other companies' apps or sites only after the App Tracking Transparency prompt says yes.

## 3. Privacy manifest and required-reason APIs

Apple requires apps, and the third-party SDKs inside them, to declare in a privacy manifest (`PrivacyInfo.xcprivacy`) why they use certain APIs that can fingerprint a device. In Expo the app's manifest is written from `ios.privacyManifests` in the app config.

- `NSPrivacyAccessedAPITypes`: one entry per category the app's own code or its JS libraries' native parts use, each with an approved reason code. The categories at the time of writing were UserDefaults (React Native itself uses it, so nearly every Expo app needs this one), plus active keyboards, disk space, boot time and file timestamps.
- `NSPrivacyTracking` and `NSPrivacyTrackingDomains`: true and the domains, if the app tracks.
- `NSPrivacyCollectedDataTypes`: what data the app collects and why. Keep it in line with the nutrition label below.

Get the current category names and reason codes from Apple's page, not from here: https://developer.apple.com/documentation/bundleresources/privacy-manifest-files and https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api. Expo's guide: https://docs.expo.dev/guides/apple-privacy/. Many Expo and community libraries ship their own manifests; after `npx expo prebuild` you can read the merged result in the generated `ios/` folder.

`ult appstore check` flags a missing manifest (AS040), a wrong shape (AS041), an unknown category (AS042), an entry with no or malformed reasons (AS043) and a tracking library without `NSPrivacyTracking` (AS044). It cannot tell whether the chosen reason is true; a person must.

## 4. Privacy nutrition labels

In App Store Connect, App Privacy, the owner answers what data types the app and every SDK in it collect, whether each is linked to the user, and whether it is used for tracking. Apple shows the answers on the store page.

- [ ] Walk through every SDK in `package.json`: analytics, crash reporting, ads, payments, sign-in, push. Each vendor publishes what it collects; use their current docs.
- [ ] The answers match the privacy policy and the manifest's `NSPrivacyCollectedDataTypes`.
- [ ] Update the answers when an SDK is added.

Apple's guide: https://developer.apple.com/app-store/app-privacy-details/.

## 5. Accounts and sign-in

- [ ] **Account deletion (around 5.1.1(v)):** if users can create an account, they can start deleting it from inside the app, not only by email or a website form. Deleting removes the account and its data, apart from what the law requires keeping, and says what happens to active subscriptions. Apple's page: https://developer.apple.com/support/offering-account-deletion-in-your-app/.
- [ ] **Sign-in rules (around 4.8):** if the app offers a third-party or social sign-in (Google, Facebook and so on) for the main account, check the current text for the equivalent privacy-friendly option it requires. Sign in with Apple meets it. `ult appstore check` notes a Google or Facebook sign-in library without an Apple sign-in package (AS080); whether an exception applies is a judgement from the current text.
- [ ] Do not require sign-in before the user can see what the app does, unless the core feature needs an account.

## 6. Demo account and review notes (around 2.1)

- [ ] If any feature is behind a sign-in, give App Review a working demo account in App Store Connect, App Review Information: user name, password, and any code or second factor they would need, or a demo mode they can switch on.
- [ ] The account is full enough to show every feature: sample content, an active subscription or a way to reach paid features in the sandbox.
- [ ] Notes explain anything not obvious: hardware the app needs, a location it works in, where a hidden feature is, why a permission is asked.
- [ ] A reachable contact name, phone and email.

Never put the demo password in the repo or in chat logs; the owner types it into App Store Connect.

## 7. Payments (around 3.1)

- [ ] Digital goods and features used in the app (unlocks, subscriptions, coins, premium content) are sold with Apple's in-app purchase, unless the fetched text gives an exception that fits: reader apps, the US storefront rules on external links, or an entitlement the owner holds for a storefront. Check the current 3.1.1 and 3.1.3 text and the storefront.
- [ ] Physical goods and services used outside the app (deliveries, rides, tickets) use a normal payment provider, not in-app purchase.
- [ ] Subscriptions: the price, period and what is included are shown before purchase; a way to restore purchases; the current minimum period and free-trial rules in 3.1.2.
- [ ] `ult appstore check` notes a card-payments SDK with no in-app purchase library (AS081) so someone decides which rule applies.

Apple's overview: https://developer.apple.com/in-app-purchase/.

## 8. Content and audience

- [ ] User-generated content (around 1.2): a way to filter, report and block, and a published contact.
- [ ] Kids Category or apps aimed at children (around 1.3 and 5.1.4): stricter data, ads and link rules.
- [ ] The age rating questionnaire answered honestly (`listing.md` § 4).
- [ ] Health, finance, gambling, VPN and other regulated areas: read the matching sections; they often need documents or a company account.

## 9. Record the result

Write a short table for the owner: each item, yes / no / not applicable, and the evidence (screen, file, URL). Add the date and "last updated" stamp of the guidelines you checked against. Items you could not see from the repo (backend live, policy text, App Store Connect answers) are marked "owner to confirm", not passed.
