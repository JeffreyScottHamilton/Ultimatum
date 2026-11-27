# Turn visitors into enquiries

Read when a page gets visits but few calls, bookings, sign-ups or orders, or before launching a page whose only job is one action. Work in this order: the earlier items usually matter more and cost less.

## 1. Look before changing

- Get the numbers: visits to the page, the action count, and where visitors came from (`measure.md`). Under about 100 actions a month, don't A/B test; fix the obvious and watch the trend.
- Watch five real sessions if the owner has a recording tool, or ask three people who fit the customer to try the page while thinking aloud. Note where they pause, scroll back or leave.
- Run `ult market page <file> --kind <kind>` and fix every fail first: a broken form or a missing label loses people no matter how good the words are.

## 2. Audit order

| # | Ask | Weak sign | Typical fix |
|---|---|---|---|
| 1 | Is the offer clear in five seconds on a phone? | headline about the company; no place or service named | rewrite the headline from the message sentence (`copy-and-proof.md` §1) |
| 2 | Is there one main action, easy to find? | three different button labels; action below the fold | one label everywhere, in the first screen and after each proof block |
| 3 | Does the visitor trust it? | stock photos; no reviews near the button; no address or licence | real photos, one specific review beside the button, visible contact details |
| 4 | Are the worries answered? | price, timing, area or cancellation only in small print | a short "what happens next" and the price or "from" price next to the button |
| 5 | Is the form easy? | many fields, unclear errors, no confirmation | §3 below |
| 6 | Does it load fast and work on a phone? | slow first screen, layout jumps, tiny tap targets | `search.md` §2 speed targets; tap targets at least 44 px |
| 7 | Do distractions pull away? | full navigation on an ad landing page; autoplay; chat bubble over the button | remove or delay them on single-offer pages |

Report findings as: what's wrong (with the line or screenshot), why it costs enquiries, the fix, and whether it is a quick fix (do now) or a test (needs traffic).

## 3. Forms and sign-up

- Ask only what you need to reply. A quote form needs a way to reply and what the job is; everything else can wait for the call. `ult market page` warns above 5 fields on a lead form and above 4 on a sign-up form.
- Every field has a visible label; placeholders vanish when typing. Use the right input type (`email`, `tel`) and `autocomplete` so phones fill it.
- One column. Mark the optional fields, not the required ones, when most are required.
- Errors appear next to the field as soon as the visitor leaves it, say how to fix it, and never clear what was typed.
- The button says what happens: "Get my quote", "Book Tuesday 3pm". Not "Submit".
- After sending: a confirmation on the page, what happens next, when they'll hear back, and an email copy.
- Sign-up for an account: email and password only (or a sign-in provider), a show-password toggle instead of a second password box, and no card for a free trial unless the owner chooses that trade-off knowing it cuts sign-ups and raises the share who pay.
- Long forms (insurance, quotes with many options): split into short steps with a progress line, easiest questions first, and save as they go.
- Spam: a hidden honeypot field and server-side rate limits before reaching for a puzzle that blocks real people.

## 4. Pop-ups and banners

Use one only with a clear reason and something worth having (a real discount, a guide, a booking slot). Rules:

- Not on first load. Trigger on intent: after most of the article was read, on leaving (desktop), or on a click.
- Easy to close: a visible close button, Escape works, tapping outside closes it, focus returns where it was.
- Show it once per visitor per few weeks, and never again after they sign up or close it twice.
- On phones, use a small bar or bottom sheet that doesn't cover the content. Google may rank pages lower when an interstitial hides the main content on mobile.
- No guilt-trip decline links ("No, I don't like saving money").
- Count it: shown, closed, converted. If it lifts sign-ups but raises bounces on that page, it is costing more than it brings.

## 5. After the action

The thank-you page is a second chance: confirm, set expectations, and offer one next step (add to calendar, read the prep guide, follow on one social channel). Track it as its own event so the conversion is counted on success, not on click.

## 6. When to test instead of fix

Fix straight away when a change is obviously right: a broken form, a missing price, an unlabeled field. Test when two reasonable versions compete and there is enough traffic: `ult market abtest plan` tells you how many visitors each version needs (`measure.md` §4). Never run a test the page can't finish in eight weeks.
