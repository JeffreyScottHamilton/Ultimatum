# Route: software product

Pick from the approved brief, tell the user in one line, let them override. Default stack suggestion: Supabase (database, auth), Stripe (billing), Vercel (hosting). Use the project's own stack if it has one; the safety rules stay the same.

## What to build

| Need | Build |
|---|---|
| Idea or stage unclear, no product yet | **Landing page**: one promise, one demo or mockup, one action (join waitlist). |
| Product works, several audiences, pricing and proof to show | **Marketing site**: home, product or features, pricing, about, a few use-case pages, blog if marketing will write. |
| Developers or complex setup | Add **docs**: quick start in under 10 minutes, API reference, examples. Docs live on their own path or subdomain. |
| Both audiences | Marketing site first; docs when the first customer asks a how-to question twice (rule of thumb). |

## Launch path by stage

- **Waitlist.** Landing page, email capture, a thank-you message that asks one question (what do you need it for?). Send a short update every two to three weeks. Goal: a list to invite from.
- **Private beta.** Invite in small waves, 10–50 people at first (rule of thumb). Free or discounted, a feedback channel, one call or form per user. Fix activation before inviting more (see `activation.md`).
- **Public launch.** Pricing page live (`pricing-page-examples.md`), billing tested in test mode, trust pages up (`launch-checklist.md`), onboarding emails on (`onboarding-emails.md`), demo video, the day-by-day plan in `launch-week.md`, a person on call the first days.
- **Live and quiet.** Skip the "launch" framing; run a relaunch around a real change (new feature, price, integration) and measure activation first.

## Team

Business & brand, Website ("show the product working"), a data and security role, a payments role, a deploy role, Marketing. App code is coding work done in a coding session, with a security review on auth, tenants and money.

## Supabase

- Official Supabase agent skills (`supabase/agent-skills`) help with schema and Postgres work.
- MCP server, if used: project-scoped and read-only; never connected to production. Check before relying: the exact read-only flag (`--read-only` in community server docs).
- Schema changes are migration files in the repo, reviewed and applied by the user or CI, never typed into a live database.
- Row-level security on every table holding user data, with tests that a user sees their own rows and cannot see another's. Check before relying: Supabase's current testing guide.
- If the claude.ai Supabase connector is on, suggest turning it off for this project so only the scoped, read-only server is used (this is a precaution, not a vendor rule).

## Stripe

- Test mode until launch day. Restricted key with the fewest permissions; never a full secret key in the repo, prompts or logs. Check before relying: whether Stripe's agent tools still accept full secret keys (reports say they no longer do).
- Build in order: hosted Checkout, Customer Portal (plan change, cancel, card update), webhooks.
- Webhooks: verify the signature on every event, make handlers idempotent (store event id, ignore repeats), and treat webhooks, not the redirect, as the source of truth for access.
- Rehearse with test clocks: renewal, failed payment, cancel at period end. Check before relying: current test-clock limits.
- Going live is the owner's job: business verification, live keys, tax settings. More in `pricing-and-billing.md`.

## Vercel

- Production holds live keys and the production database; Preview and Development hold test keys and a dev database. Never share one database between preview and production.
- Every change gets a preview deploy; production only after `ult gate approve deploy "<words>"`. Check before relying: exact `vercel env` syntax.

## Mobile apps and APIs

- Mobile: app store review takes time and has its own rules on in-app purchases and privacy labels. Check before relying: each store's current guidelines and fee rules. Plan for review delay in the date.
- APIs: a docs site, API keys per user, rate limits stated on the pricing page, a status page, and a changelog.

## Video

- **Motion Graphics**: product explainers, feature launches, changelog clips, number-led demos. Storyboard, audio sheet, checked export.
- **Brand Film**: a founder story or a customer-outcome story for the homepage or an ad; the product arrives late and enables the turn.
- Show the real product. Never animate a fake dashboard or invent usage numbers.
