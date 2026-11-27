# Submit with EAS Submit, then handle rejections

Read when uploading a build to App Store Connect, sending a version to App Review, or answering a rejection in Resolution Center.

Expo's guide: https://docs.expo.dev/submit/ios/. Apple's: https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-for-review and https://developer.apple.com/distribute/app-review/.

## 1. One-time setup

- The app record exists in App Store Connect with the bundle ID from `setup.md` § 1.
- `submit.production.ios.ascAppId` in `eas.json` holds the app's numeric Apple ID (App Store Connect, App Information, General). Without it EAS asks interactively (AS065).
- Pick how EAS signs in to App Store Connect:
  - **App Store Connect API key (preferred, and the only option in CI):** the owner creates a key with the App Manager role in Users and Access, Integrations, then lets EAS store it with `eas credentials` or the first `eas submit`. EAS keeps it on its servers.
  - **Apple ID with an app-specific password:** the owner types it when asked, or sets `EXPO_APPLE_APP_SPECIFIC_PASSWORD` in their own shell or CI secrets.
- The key file (`AuthKey_*.p8`), key IDs and passwords never go in the repo, `eas.json`, `.env` files that are committed, or chat. If `ascApiKeyPath` is used at all, it must point outside the project (AS093).

## 2. Uploading

Ask before each of these; they use the owner's accounts:

```bash
eas submit -p ios --latest            # the newest production build
eas submit -p ios --id <build id>     # a specific build
eas build -p ios --profile production --auto-submit   # build, then upload
```

The upload lands in TestFlight first. Apple processes it, then it can be tested (`testflight.md`) and attached to a version.

## 3. Sending for review (in App Store Connect)

1. Create or open the version (the same number as `version`).
2. Fill the listing (`listing.md`), App Privacy (`review-check.md` § 4) and App Review Information: demo account, notes, contact (`review-check.md` § 6).
3. Select the build.
4. Choose the release: manual, automatic after approval, or scheduled. For updates, phased release spreads it over several days.
5. Submit. Status moves through Waiting for Review, In Review, then Ready for Distribution, Rejected or Metadata Rejected.

Times vary; Apple posts no fixed review time. Expedited review exists for urgent fixes and should be kept for real emergencies.

## 4. When a version is rejected

The message in Resolution Center (App Review, on the submission) names one or more guideline sections and often has screenshots.

1. **Read it all, then fetch the named sections** from the current guidelines (`review-check.md` § 0). Match each point to the exact screen or field.
2. **Sort each point:**
   - Binary problem (a crash, missing feature, missing account deletion): fix the code, make a new build with a higher build number, submit again.
   - Metadata problem (screenshots, description, age rating, privacy answers): fix in App Store Connect; usually no new build.
   - Information request (how does X work, demo account failed): answer in Resolution Center; no build.
   - Disagreement: if the app does follow the guideline, reply with facts. If that fails, the owner can appeal to the App Review Board.
3. **Run the whole review check again.** Reviewers often find the next issue only after the first is fixed.

## 5. Writing the Resolution Center reply

The reply is from the owner, in their name. Draft it for them; they post it. Keep it short and specific:

- Thank the reviewer once, then answer each point in the order raised, numbered the same way.
- For each: what was changed, where to see it (screen path or a timestamped screen recording link), and the build number that has it.
- For a disagreement: quote the behaviour, not feelings. Explain how the app meets the guideline's purpose, with steps to see it.
- If a demo account failed, give a fresh one in App Review Information and say you did.
- No threats, no comparisons with other apps, no guessing what the reviewer meant.

Skeleton (fill from the actual rejection; do not send as is):

```
Hello, and thank you for the review.

1. Guideline <number> – <topic>: In build <n> we <change>. To see it: <steps>.
2. Guideline <number> – <topic>: <answer or change>.

A new build (<version> (<build>)) is attached to this submission. Please let us know if anything else is needed.
```

## 6. After approval

If the release is manual, the owner presses Release. Check the live listing, install from the store on a clean device, and tag the commit with the version and build number so `ult appstore check --since <tag>` works for the next release.
