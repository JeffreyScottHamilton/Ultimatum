# Launch checklist

Tick each line with evidence (a link, a command, a test result). Legal text is the owner's to sign off; this is not legal advice. Rules of thumb are marked.

## Trust basics

- [ ] **Privacy policy** that matches what the product really collects, with a contact address. Owner signs off.
- [ ] **Terms of service**, including refund and cancellation rules.
- [ ] **Security page**: how data is stored and protected, who to tell about a problem. Claim only what is true; the compliance reviewer checks it.
- [ ] **Status page** or a plain place where outages are posted.
- [ ] **Data handling**: what you store, where, how a user exports or deletes it, which vendors see it. Cookie notice where analytics needs one (check before relying: local rules).
- [ ] **Auth hardening**: run a security review with `ultimatum:work` on sign-in, password reset, sessions, roles and tenant separation. Row-level security tests include "must not see" cases.
- [ ] **Billing** rehearsed in test mode: sign up, pay, access, change plan, cancel, failed payment, repeat webhook (see `pricing-and-billing.md`).
- [ ] Backups exist and a restore was tried once. Secrets only in environment variables.
- [ ] Error tracking on, and a named person watching it launch week.

## Analytics events

Track the smallest set that answers questions. Name them clearly and keep personal data out of event properties.

- visited_pricing, signed_up, verified_email, reached_activation (the aha), started_trial, paid, upgraded, cancelled, invited_teammate.
- Add the traffic source to sign-up. Check the sequence works end to end before launch day.
- Respect consent rules for analytics tools; choose one tool, not four.

## Launch-week plan

| Day | Do |
|---|---|
| Before | Email the waitlist a date and what is coming; line up a few beta users to say what they got; demo video checked; assets and copy through compliance review |
| Launch day | Waitlist email first; founder posts on the user's own accounts; launch post on Product Hunt and/or Hacker News if they fit; relevant communities where posting is allowed |
| Days 2 to 4 | Reply to every comment and email quickly; fix what breaks; share one honest lesson or a number |
| End of week | Thank-you email, results review (`ult social --results`), pick the next test |

- Product Hunt and Hacker News have their own rules (no vote begging, Hacker News expects a plain title and a "Show HN" fit). Check before relying: each site's current guidelines.
- Communities ban promotion often; read the rules, lead with usefulness, and ask the user before each post.
- Demo video: Motion Graphics for a product walk-through; show real screens.
- Every post, send and ad spend waits for the user's yes.

## First 30 days

| Measure | What it tells you | If it is weak |
|---|---|---|
| Visit to sign-up | Is the promise and page clear? | Rewrite the headline and the proof; test one thing at a time |
| Sign-up to activation | Does onboarding work? | Cut steps, add a template, fix the first task, email nudges |
| Trial to paid | Is value felt before the trial ends? | Move the paywall, shorten the path to aha, reconsider card-up-front |
| Churn (share leaving each month) | Do people keep the value? | Read cancel answers, talk to five churned users, fix the top cause |
| MRR (monthly recurring revenue) and growth | Is it a business yet? | Revisit price and plans; add annual; focus on the channel that converted |

- Benchmarks vary widely by product; compare to your own previous week first.
- Review weekly with the user: one number that moved, one cause guess, one change to try. Change one thing at a time.
