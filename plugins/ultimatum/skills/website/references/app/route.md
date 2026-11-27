# App sites: route

Read this when the brief needs accounts, saved data, members-only pages or payments. Small and content sites follow `../route.md` alone.

## When a site becomes an app

| Need | Simplest fit | Build an app when |
|---|---|---|
| Take a deposit or sell a few services | Stripe Payment Link or the booking tool's payment step, linked from the site | the price depends on what the visitor picks, or paying must unlock something on the site |
| Sell products | a hosted shop (Shopify, Square, the builder's shop) | the catalogue is small and the checkout is custom, or the shop is part of a members product |
| Members-only content | the newsletter or course tool's members area | members need their own saved data, roles or a dashboard |
| Subscriptions | Stripe Checkout in subscription mode plus the customer portal | access on the site depends on the subscription |
| Client portal, dashboard, saved work | — | always an app |

Offer the simplest fit first and say what it costs in fees and lock-in (check before relying). Build the app only when the owner picks it.

## Default stack

When nothing exists yet:
- Next.js (App Router) on Vercel or Netlify.
- Supabase for the database, sign-in and file storage.
- Stripe for payments.

When the project already has a framework, keep it and use the same three services through their SDKs. Other good choices are fine when the owner already pays for them (Clerk or Auth.js for sign-in, Neon or Firebase for data, Paddle or Lemon Squeezy as merchant of record when the owner wants someone else to handle sales tax). Read each vendor's current docs before using them.

## What the brief adds

Under `## Build brief`, add these lines for an app:
- **Accounts:** who signs up, how (email and password, magic link, Google, Apple), and the roles (member, staff, admin).
- **Data:** the things the app stores, who owns each, who may see it, and how long it is kept.
- **Payments:** one-off or subscription, the prices, trial, refunds policy, and the currency and countries.
- **Emails:** what the app sends (confirm, reset, receipt, failed payment) and from which address.

## Order and approvals

1. Brief → `ult gate approve brief`.
2. Three directions → mockup approval, as for any site.
3. **Data model.** Write the tables, owners and access rules as a migration (`supabase.md`). Show it in plain words: "members can see only their own bookings; staff can see all bookings for their location". On the owner's yes: `ult gate approve data-model "<their words>" --file supabase/migrations/<file>.sql`. Any later edit to that file reopens the gate.
4. Build the sign-in flows (`auth.md`), then the pages, then payments in **test mode only** (`stripe.md`).
5. Security pass on every change to sign-in, data access or payments. Follow `${CLAUDE_PLUGIN_ROOT}/skills/work/references/security/secure-implementation.md` and add a test that fails without each guard. Run the second-user test from `supabase.md`.
6. `checklist.md` (app go-live), then the usual publish and deploy approvals.
7. **Real payments.** Live keys and real charges only after `ult gate approve live-payments "<their words>"`. Close it with `ult gate done live-payments` once the switch is made.

## Hard rules

- The secret keys (Supabase secret or service-role key, Stripe secret key, webhook signing secret) live only in the host's environment variables and in local `.env` files ignored by Git. They are never in browser code, prompts, logs or commits.
- The owner creates the Supabase, Stripe and hosting accounts and pastes keys into the host's settings themselves.
- Row-level security is on for every table the browser can reach, before any real data goes in.
- Nothing is fulfilled from a redirect alone: payment state comes from verified webhooks.
- Personal data: collect only what the brief names, add a privacy page saying what is kept and why, and give users a way to delete their account.
