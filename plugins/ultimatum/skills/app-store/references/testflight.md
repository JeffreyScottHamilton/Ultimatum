# TestFlight: internal testers, external groups, device checks

Read when a production build has been uploaded and needs testing before review, or when planning a beta.

Apple's pages: https://developer.apple.com/testflight/ and the TestFlight section of App Store Connect Help at https://developer.apple.com/help/app-store-connect/test-a-beta-version/overview-of-testflight. Check them for the current tester limits and how long a build stays available; those numbers change.

## 1. Getting a build into TestFlight

A production build reaches TestFlight once it is uploaded to App Store Connect: `eas submit -p ios` (see `submit-and-rejections.md`), or `eas build --auto-submit`. Both use the owner's account; ask first. Apple then processes the build, which can take from minutes to over an hour. Answer the export compliance question if the build did not (AS056).

## 2. Internal testers

- People on the owner's App Store Connect team with a role that allows it. No Apple review needed; a build is available as soon as processing finishes.
- Best for the first pass by the people who know the app.
- Testers install the TestFlight app on their iPhone or iPad and accept the invite.

## 3. External groups

- Anyone with an email invite or a public link, outside the team.
- The first build of each version for external testers goes through **Beta App Review**. It checks broadly the same things as App Review, so a beta that fails here would fail later too. Fill in Test Information: what to test, a contact, and a demo account if the app needs a sign-in (same rules as `review-check.md` § 6).
- Later builds of the same version usually go to testers without a full review, but Apple may still review them.
- Keep groups by purpose ("friends and family", "power users"), and write "What to Test" notes for each build in plain words.

## 4. What to check on a real device

Use at least two screen sizes: a small current iPhone and the largest one you can get (the largest is also the required screenshot size). If the app runs on iPad, add one iPad. A simulator is not enough: it misses the camera, push, real performance, sign-in with Apple, purchases with a sandbox account and the permission prompts as users see them.

For each size, go through:

- [ ] Fresh install: the splash screen, then the first screen, without a blank frame or a crash.
- [ ] Every permission prompt appears at the moment the feature is used, with the text from `setup.md` § 5; deny it and the app still works and explains how to turn it on.
- [ ] Sign up, sign in, sign out, password reset, and account deletion from inside the app if the app has accounts.
- [ ] Sign in with Apple, if offered, including "Hide My Email".
- [ ] Purchases and restore with a sandbox Apple account, if the app sells anything.
- [ ] Layout: notch and Dynamic Island, the home indicator, the keyboard over forms, landscape if supported, the largest text size in Settings, dark mode.
- [ ] Offline and slow network: a clear message, no endless spinner, no crash.
- [ ] Links: privacy policy and support open, deep links land on the right screen.
- [ ] Push notifications, if used: the prompt, delivery, tapping one.
- [ ] Backgrounding and returning; killing the app and reopening it.
- [ ] No test data, placeholder text, debug menus or "beta" labels in what a reviewer would see.

Crash reports and screenshots testers send appear under the app's TestFlight tab in App Store Connect. Write the results down with the build number, device and iOS version.

## 5. What this needs

All of this needs the owner's App Store Connect account and real devices. From this container you can prepare the "What to Test" notes, the tester checklist and the fixes the testers find.
