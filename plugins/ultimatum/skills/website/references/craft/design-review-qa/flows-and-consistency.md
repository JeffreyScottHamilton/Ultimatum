# Flows, goodwill and cross-page consistency

Read after the page-by-page audit, to judge how the site feels in use. Static screenshots miss delay, feedback and tone, so walk two or three real flows and then compare pages with each other.

## Flow review (2 to 3 flows)

Pick flows that matter to the owner: for a local business, find the phone number or book a visit; for an app, sign up, first action, pay. Per flow:

1. Open the start page, capture a first screenshot, note the interactive controls.
2. Perform each step with Playwright (`getByRole` locators first, stable ids second; never styling classes), wait on a visible condition rather than a fixed sleep, and capture a result shot.
3. Compare the page text and URL before and after each step to see what changed.
4. Keep a console listener running the whole time; a new error after a click is a finding.

Forms may be filled but are not submitted on a site that is not yours or not local. Local scratch data only.

Judge the feel, not only the function:

- **Response.** Does a click answer at once? Is there a loading state if it takes more than a moment?
- **Transition.** Intentional, or absent, or the same stock fade?
- **Feedback.** Is it obvious the action worked or failed, immediately?
- **Form polish.** Visible focus, validation at a sensible time, errors beside the field, input preserved after an error.

Narrate the flow in the first person while doing it ("I press Sign up... still spinning after three seconds..."), naming each element, its place and its weight. A recipe for the Playwright side is in `qa-playwright-recipes.md`.

## Goodwill meter (a heuristic, not a measurement)

Start at 70 out of 100 and track what each step costs or buys. The drains and fills matter more than the number.

| Drains | Cost |
|---|---|
| Hiding what people want (price, contact details, delivery cost) | 15 |
| Interstitials, splash screens, forced tours | 15 |
| Punishing format (rejecting dashes in a phone number) | 10 |
| Asking for information you do not need | 10 |
| Careless-looking screens | 10 |
| Each choice that is unclear | 5 |

| Fills | Gain |
|---|---|
| The top tasks are obvious | 10 |
| Errors recover gracefully with a specific fix | 10 |
| Costs and limits stated up front | 5 |
| A step removed through direct links, smart defaults or autofill (per step) | 5 |
| A plain apology when something breaks | 5 |

Report one line per step ("Step 2, checkout: 70 to 55, minus 15 for the forced account"), then the final value: below 30 is serious experience debt, 30 to 60 needs work, above 60 is healthy. The largest drains and fills become findings.

## Cross-page consistency

Compare screenshots across pages:

- Same navigation and footer everywhere, with the current page marked.
- The same component styled the same way (a button that changes shape from page to page is a finding).
- One tone: not playful on one page and corporate on the next.
- The spacing rhythm and type scale carry over.
- Real content, not leftover lorem or a different company name.

Quote the two screenshots that disagree. One-off components that could be the shared one go in the quick wins list.

## Merge note

`../taste/quality-gate.md` has the widths and tap-size walk; do not repeat them here. This file adds the judging layer on top.
