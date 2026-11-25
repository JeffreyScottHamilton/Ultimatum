# Activation: from sign-up to "aha"

Activation is the moment a new user first gets the value they came for. A launch that fills sign-ups but not activation only wastes the traffic. Numbers here are rules of thumb unless marked.

## Define it first

- Write the **aha moment** in one sentence in the user's words: "created a first report", "sent a first invoice", "made a first API call that returned data".
- Pick one **activation metric** that counts it: share of new sign-ups who reach it within a set time (a day or a week, pick one). Track it from day one.

Examples (made-up products, to show the shape):

| Product | Aha moment | Activation metric |
|---|---|---|
| Invoicing tool | First invoice sent to a real client | Share of sign-ups who send an invoice within 7 days |
| Team chat | A teammate replies | Share of new workspaces with 2+ people posting within 3 days |
| Data API | A call returns real data | Share of new keys with a successful call within 1 day |

How to choose: list 3 candidate actions, check which one the users who stayed (in beta data, if any) did early and the ones who left did not. If there is no data yet, choose the action closest to the promise on the landing page and revisit after a month.

## Sign-up flow

- Ask for the least: email and password, or one social sign-in. Collect the rest after value.
- Verify email without blocking the first look when you can.
- Say what happens next on the sign-up page. Do not hide the price.
- Test it on a phone and on a slow connection. Log every drop-off step.
- Auth is high risk: run a security review in a coding session (rate limits, password reset, session handling).

## First-run experience

- Land the user in the product, not a tour. One clear first task, a sample project or template so the screen is never empty.
- Show a short checklist of 3 to 5 steps; the last one is the aha.
- Cut every step that does not lead to it. Test with 5 real people watching silently (rule of thumb: most big problems show by the fifth).
- Offer help in context: a tooltip, a help link, a human reply address. No wall of modals.

## Onboarding emails

The full sequence (welcome, nudges to the aha step, trial ending), example copy and what to measure: `onboarding-emails.md`. Two rules here: stop nudges the moment the person activates, and sending needs the user's yes.

## Docs and help

- A quick start (under 10 minutes to first result), a short FAQ drawn from real questions, and a contact path.
- Searchable help; link it from empty states and error messages.
- Keep a changelog page; it is free marketing and shows the product is alive.

## Feedback loop

- Ask at two points: after the aha ("what almost stopped you?") and at cancel ("what was missing?"). One question each.
- Read every answer in the first weeks; tag them; share the top three themes with the user weekly.
- Turn themes into the next fixes: onboarding copy first, then features. Re-measure activation after each change.

## Beginner mistakes

| Mistake | Fix |
|---|---|
| Counting sign-ups as success | Count activation; sign-ups without it are wasted traffic |
| A product tour of every feature before any value | One first task, then the next |
| Empty screen on first log-in | Sample data or a template |
| Long sign-up form (company size, role, phone) | Ask later, after value, and only what you use |
| Changing onboarding and pricing in the same week | One change at a time, measured for a week |
