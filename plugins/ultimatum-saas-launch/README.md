# Ultimatum SaaS Launch

A launch manager for software products: web apps, mobile apps, B2B tools, APIs and subscriptions. It runs the shared Ultimatum Launch teams with SaaS-specific guidance. Every post, spend, publish and deploy waits for your yes.

It needs two other plugins: `ultimatum` (core) and `ultimatum-launch` (the shared teams: business, website, social media, brand film, motion graphics, and the taste and compliance reviewers).

## Install

```
/plugin marketplace add JeffreyScottHamilton/Ultimatum
/plugin install ultimatum@ultimatum
/plugin install ultimatum-launch@ultimatum
/plugin install ultimatum-saas-launch@ultimatum
```

## Start

Say "help me launch my SaaS" or run `/ultimatum-saas-launch:launch`. The manager prints the steps and the next one with `ult launch --kind saas --root .`.

## What it adds over the base manager

- **SaaS intake** in batches of 5 to 8 questions with recommended answers: customer, job, stage, buying path, pricing, platforms, integrations, data handled, channels, date, budget.
- **Routing** for landing page, marketing site and docs, and for waitlist, beta and public launch paths, plus Supabase, Stripe and Vercel notes and which video style fits.
- **Pricing and billing** guidance: models, pricing page layout, test-mode billing, tax and refund basics.
- **Activation** guidance: sign-up, first run, onboarding emails, docs and the feedback loop.
- **Launch checklist**: trust pages, security review through `ultimatum:work`, analytics events, a launch-week plan and first-30-day metrics.
- Hands the SaaS notes to the shared teams, which cannot read this plugin's files.

Prices, fees and vendor policies in the guides are marked "check before relying"; confirm them on the vendor's page. Nothing here is legal or tax advice.

MIT licence; see `LICENSE`.
