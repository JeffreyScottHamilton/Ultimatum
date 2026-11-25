# Style: product demo

Use this for a screen recording of software, a website or an app, or a hands-on demo of a physical product. The viewer should see one task done from start to finish and want to try it. Platform specifications here are **check before relying**.

## Script first

Write the script before recording. One task per video.

| Part | What it does | Example (fictional app "Tally") |
|---|---|---|
| Outcome | Show the end result first, in two seconds | The finished invoice sliding into the client's inbox |
| Problem | One line on what was slow or annoying before | "Invoices used to take me twenty minutes." |
| Steps | Three to five clicks or actions, each one visible | Pick client, add hours, press send |
| Proof | A real detail the viewer can check | The time on screen, the email arriving |
| Next step | One action | "Try it free, link in profile." |

Read the script aloud with a timer. If it runs long, cut a step, not the outcome.

## Prepare the screen

- Use a clean account with fictional data: names like "Northwind Studio", amounts that are plainly sample figures. Never record real customer data.
- Close notifications, other tabs, bookmarks with personal names, and chat apps.
- Set the browser or app zoom so text is readable on a phone after cropping.
- Use a plain desktop background.
- Rehearse the clicks once so the recording is smooth.

## Recording settings

- Record at the screen's native resolution or higher than the export, so zooms stay sharp.
- Use a steady frame rate. Check that the editor or the export settings match it.
- Record voice separately or with a decent microphone in a quiet room. Voice quality matters more than picture quality.
- Record a few seconds of silence in the room for noise reduction later.
- For a physical product, use a tripod, even light, and a plain surface; follow the photo house rules in `brand/brand.md` if they exist.

## Zooms and cursor highlights

- A wide screen recording is unreadable on a phone. Zoom in on the area that matters for each step, then zoom out only when the viewer needs to see where they are.
- Ease zooms in and out; a sudden jump is disorienting.
- Highlight the cursor or each click with a soft ring. Hide the cursor when it is idle.
- Use a short callout (an arrow or a label) for the one thing the viewer must notice in a step. Motion-graphics titles and callouts follow `motion-graphics/guide.md`.

## Pacing

- Cut waiting: loading spinners, typing long text, scrolling. Show the start and the result, or speed it up and say so on screen.
- Keep each step on screen long enough to read the label you are pointing at.
- Match voice to picture: say the step as it happens.

## Captions

- Captions on, burned in for short vertical video, plus an `.srt` where the platform accepts one.
- Spell product terms, button labels and numbers exactly as they appear on screen.
- Keep captions clear of the zoomed area and of each platform's overlay (check before relying on any safe-zone margin).

## What to blur or replace

Blur, or better, replace before recording:

- Email addresses, phone numbers, names and avatars of real people.
- API keys, tokens, passwords, internal URLs and account IDs.
- Real invoices, orders, balances and customer records.
- Browser tabs, bookmarks and notifications.
- Anything on a second monitor that slides into view.

Blurring after the fact is a fallback; a single missed frame leaks the data. Step through the final export frame by frame around every blurred area.

## Claims

- Show what the product does today, at the plan the viewer can buy. If a feature is on a higher plan or in beta, say so on screen.
- Do not speed up a process without saying so if speed is part of the claim.
- Run the compliance reviewer on claims, comparisons and any numbers.

## Hand-off or finish here

- Editor named: follow `editors/guide.md`.
- No editor: zooms and callouts can be built as motion graphics (HyperFrames, see `motion-graphics/guide.md`) layered over the recording, or cut with `ffmpeg`.

## Beginner mistakes

| Mistake | Fix |
|---|---|
| Recording the whole screen and never zooming | Zoom on every step |
| Real customer data on screen | Fictional demo account from the start |
| Explaining the menu before showing the result | Outcome first |
| Five features in one video | One task per video |
| Cursor wandering while talking | Plan the clicks; hide the idle cursor |
| Showing a paid feature as if it were free | Label the plan on screen |
