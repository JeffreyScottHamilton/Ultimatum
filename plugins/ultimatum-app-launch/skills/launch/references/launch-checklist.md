# Launch checklist

Tick each line with evidence (a link, a command, a test result). Legal text is the owner's to sign off; this is not legal advice. Rules of thumb are marked.

## Trust basics

- [ ] **Privacy policy** that matches what the product really collects, with a contact address. Owner signs off.
- [ ] **Terms of service**, including refund and cancellation rules.
- [ ] **Security page**: how data is stored and protected, who to tell about a problem. Claim only what is true; the compliance reviewer checks it.
- [ ] **Status page** or a plain place where outages are posted.
- [ ] **Data handling**: what you store, where, how a user exports or deletes it, which vendors see it. Cookie notice where analytics needs one (check before relying: local rules).
- [ ] **Auth hardening**: run a security review in a coding session on sign-in, password reset, sessions, roles and tenant separation. Row-level security tests include "must not see" cases.
- [ ] **Billing** rehearsed in test mode: sign up, pay, access, change plan, cancel, failed payment, repeat webhook (see `pricing-and-billing.md`).
- [ ] **Pricing page** matches the billing set-up and the terms: same prices, trial length, refund rule (`pricing-page-examples.md`).
- [ ] **Onboarding emails** set up, tested in a few mail apps, and approved by the user (`onboarding-emails.md`).
- [ ] Backups exist and a restore was tried once. Secrets only in environment variables.
- [ ] Error tracking on, and a named person watching it launch week.

## Analytics events

Track the smallest set that answers questions. Name them clearly and keep personal data out of event properties.

- visited_pricing, signed_up, verified_email, reached_activation (the aha), started_trial, paid, upgraded, cancelled, invited_teammate.
- Add the traffic source to sign-up. Check the sequence works end to end before launch day.
- Respect consent rules for analytics tools; choose one tool, not four.

## Launch week

Day-by-day plan, what to do if launch day is quiet or something breaks, and common mistakes: `launch-week.md`. Every post, send and ad spend waits for the user's yes.

## First 30 days

| Measure | What it tells you | If it is weak |
|---|---|---|
| Visit to sign-up | Is the promise and page clear? | Rewrite the headline and the proof; test one thing at a time |
| Sign-up to activation | Does onboarding work? | Cut steps, add a template, fix the first task, email nudges |
| Trial to paid | Is value felt before the trial ends? | Move the paywall, shorten the path to aha, reconsider card-up-front |
| Churn (share leaving each month) | Do people keep the value? | Read cancel answers, talk to five churned users, fix the top cause |
| MRR (monthly recurring revenue) and growth | Is it a business yet? | Revisit price and plans; add annual; focus on the channel that converted |

- Benchmarks vary widely by product; compare to your own previous week first. Any outside benchmark is check before relying, with its source named.
- Review weekly with the user: one number that moved, one cause guess, one change to try. Change one thing at a time.

## Beginner mistakes

| Mistake | Fix |
|---|---|
| Ticking lines without evidence | Each tick has a link, a command or a test result |
| Privacy policy from a template that lists tools you do not use (or misses ones you do) | List the real vendors: hosting, database, email, analytics, billing, error tracking |
| Restore never tried | A backup that was never restored is a guess; try one restore into a scratch database |
| Five analytics tools | One tool, the events above, consent handled |
| Security page claiming certifications you do not have | Claim only what is true; the compliance reviewer checks |
