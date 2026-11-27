# Hardening: real data, languages, errors and broken input

Read when a screen works with tidy sample data and now has to survive long names, other languages, failures, permissions, many items and interrupted gestures.

The stress-test method (worst-case fixtures, failure signatures, truncate or wrap per field) is in `../../craft/emil-motion/worst-case-data.md`. This file adds language handling, error and permission states, concurrency and gesture recovery. A runnable page that shows each move is `../../../../../data/craft/impeccable/examples/harden-demo.html`, checked by `check-harden.js` in the same folder.

## Inputs to try

- Text: empty, one character, 100+ characters with no spaces, emoji, accents, Arabic or Hebrew, Chinese, Japanese or Korean.
- Numbers: zero, negative, millions, billions, many decimals.
- Lists: none, one, a thousand rows, fifty options in a select.
- Network: offline, slow, timed out, a request that fails halfway.

## Layout that survives long content

- A flex or grid child will not shrink below its content unless you set `min-inline-size: 0` (or `min-width: 0`). Without it, one long name pushes siblings out of the row.
- Pick per field: truncate with an ellipsis (names in a dense list, with the full value in a tooltip or detail view), clamp to N lines (descriptions), or wrap with `overflow-wrap: anywhere` (addresses, URLs).
- Size buttons by padding, never a fixed width, so a longer translation still fits.
- Leave room for text to grow: translations from English often run 30 to 40% longer, and German or Finnish words can be very long.

## Languages and scripts

- Use logical properties (`margin-inline-start`, `padding-inline`, `border-inline-end`, `inset-inline-start`) so layout follows reading direction. Mirror only icons whose meaning is directional.
- Format numbers, money and dates with `Intl` and the user's locale; never build them by hand. `Intl.NumberFormat('fa-IR')` gives Eastern Arabic-Indic digits; `de-DE` swaps the decimal and grouping marks. See MDN: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl>.
- Plurals vary by language: Arabic has six categories (zero, one, two, few, many, other). Use `Intl.PluralRules` or an i18n library with full sentences per category, never `count + "s"`.
- Write whole messages with named slots, so a translator can reorder words. Never join sentence fragments.
- Calendars: Persian users usually expect the Solar Hijri calendar and many Arabic readers the Hijri one; pass the calendar in the locale tag (`fa-IR`, or `ar-SA-u-ca-islamic`).
- Persian and Kurdish use the zero-width non-joiner (U+200C) inside words. Text filters that strip invisible characters break those words; keep it.
- Persian and Arabic use different code points for yeh and kaf. Store what the user typed. When matching search terms, normalise both sides to one form.
- Serve and store UTF-8 everywhere. Count characters with `Intl.Segmenter` when a limit must match what the user sees, since one emoji can be several code units.

## Errors

Every failure message answers three things: what failed, why (when known and useful), and what the user can do now. Keep the user's input after a failed submit.

| Response | What the screen does |
|---|---|
| Validation (400, 422) | show the message next to the field, keep the input |
| Not signed in (401) | send to sign-in, then back to the same place |
| Forbidden (403) | say the user lacks access and who can grant it |
| Not found (404) | a not-found state with a way back, not a blank panel |
| Rate limited (429) | say when to retry; disable the action until then |
| Server error (5xx) | a short apology, a retry, and a way to reach support |
| Offline or timeout | say so, keep what was typed, retry when back online |

One failed panel must not blank the whole screen. Contain the error where it happened.

## Validation and the security overlay

Client-side checks (`required`, `maxlength`, `pattern`, input `type`) help the user; they protect nothing. The server must validate and encode every input again. Anything touching sign-in, sessions, roles, uploads or text built into queries or HTML goes through Ultimatum's security overlay: `../../../../work/references/security/secure-implementation.md`. Tie each hint to its field with `aria-describedby` so the rule is read aloud.

## Empty, loading and permission states

- Empty: say why it is empty and give the one next action. "No results" also says what was searched.
- Loading: say what is loading; use a skeleton for known shapes; give a time or progress for long jobs. Never fake progress.
- Permissions: no access to view, view but not edit, read-only mode. Each says why and how to get access.

## Doing two things at once

- Disable a submit button while its request is in flight, or make the request idempotent, so a double click does not send twice.
- Optimistic updates need a rollback path and a visible note when the server says no.
- When two people edit the same record, detect the conflict (a version number or timestamp) and show both values.
- Cancel pending requests, timers and listeners when a view closes.

## Interrupted gestures

Custom sliders, drag handles and swipe strips must recover from the cases below, and the next drag must work without a reload:
- a second finger lands mid-drag: keep following the first pointer, ignore the second;
- the browser takes the gesture to scroll: handle `pointercancel`;
- capture is dropped: listen for `lostpointercapture`;
- the finger or mouse lets go beyond the control, or the tab is blurred during the drag.

Set `touch-action` to the axis the control does not use (for a horizontal slider, `pan-y`), so a vertical swipe across it still scrolls the page. Pointer events: <https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events>.

When you report a gesture check, say what produced the evidence (emulated viewport, synthetic touch in which engine, or a real device) and what stayed untested.

## Verify

Paste a 120-character name, emoji and an Arabic string into every text field. Switch a container to `dir="rtl"`. Throttle the network and go offline. Force each error code. Load a thousand rows. Click submit ten times fast. Run each interrupted-gesture case, then drag again. Zoom to 200%.
