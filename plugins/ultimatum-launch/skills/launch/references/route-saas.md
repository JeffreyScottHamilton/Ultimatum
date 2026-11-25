# Route: subscription SaaS

For web apps with accounts and paid plans. Default stack: Supabase (database and auth), Stripe (billing), Vercel (hosting). Use the project's own stack if it already has one; keep the same safety rules.

## Team

Business & brand, Website (marketing pages, with "show the product working"), a data and security role, a payments role, a deploy role, Marketing. Core `/ultimatum:work` handles the app code itself, with its security overlay on auth, tenants and money.

## Supabase

- Recommend the official Supabase agent skills (`supabase/agent-skills`) for schema and Postgres work rather than repeating them.
- The Supabase MCP server, if used: **project-scoped** (pass the one project ref) and **read-only**. Never connect it to the production project. Check before relying: the exact read-only flag and its behaviour (`--read-only` in the community server docs).
- Schema changes go in as migration files in the repo, reviewed and applied by the user or CI, never typed into a live database.
- Row-level security on every table holding user data, with tests that prove a user sees their own rows **and cannot see** someone else's (`supabase test db` in CI). Check before relying: Supabase's current testing guide.
- If the user has the separate claude.ai Supabase connector enabled, suggest turning it off for this project so only the scoped one is used. Check before relying: this advice comes from a third-party write-up.

## Stripe

- **Test mode only** until launch day. Use a **restricted key** with the fewest permissions the job needs; never a full secret key in the repo, prompts or logs. Check before relying: reports that Stripe's agent connector stops accepting full secret keys from December.
- Recommend Stripe's official agent tooling (`stripe/ai`) if the user wants it.
- Build in this order: **Checkout** (hosted) → **Customer Portal** (plan changes, cancel, card update) → **webhooks**.
- Webhooks: verify the signature on every event with the endpoint secret; make handlers **idempotent** (store the event id, ignore repeats); treat webhooks, not the redirect, as the source of truth for access. Forward locally with the Stripe CLI for tests.
- Rehearse billing with **test clocks**: a renewal, a failed payment, a cancellation at period end. Check before relying: current test-clock limits in Stripe's docs.
- Going live (owner only): business verification, live keys, tax settings.

## Vercel

- Environment split: **Production** has the live Stripe key and the production database; **Preview** and **Development** have test keys and a dev database. Never share one database between preview and production.
- Recommend Vercel's official agent skills (`vercel-labs/agent-skills`) for deploy and React rules.
- Every change gets a preview deploy; production only after `ult gate approve deploy "<words>"`. Check before relying: exact `vercel env` command syntax.

## Launch checklist

- [ ] RLS tests pass in CI, including "must not see" cases
- [ ] Signup → Checkout → access granted → Portal cancel → access removed, all in test mode
- [ ] Webhook signature check and repeat-event test pass
- [ ] Test-clock rehearsal done
- [ ] Env vars split as above; no live keys outside Production
- [ ] Privacy policy and terms pages exist (owner signs off on legal text)
- [ ] Compliance review of pricing and claims on the marketing pages
- [ ] Deploy on the user's yes, then check the live signup path

## Video

Product explainers, feature launches, changelog clips and number-led demos fit **Motion Graphics** (storyboard, audio sheet, checked export). A founder or customer-outcome story for the homepage or an ad fits **Brand Film**, with the product arriving late and enabling the turn. Never film or animate a fake dashboard; show the real product.
