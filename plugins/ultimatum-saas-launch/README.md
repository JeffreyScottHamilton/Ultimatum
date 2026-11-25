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
- **Pricing and billing**: models, how to pick a value metric, test-mode billing with a step-by-step test script, tax and refund basics.
- **Pricing page examples**: worked layouts for self-serve, usage-based and sales-led products, a FAQ list and the monthly/annual toggle.
- **Activation**: defining the aha moment with examples, sign-up, first run, docs and the feedback loop.
- **Onboarding emails**: a welcome-to-trial-end sequence that branches on activation, example copy and what to measure.
- **Launch checklist**: trust pages, security review through `ultimatum:work`, analytics events and first-30-day metrics.
- **Launch week**: a day-by-day plan from two weeks out to the first weekly review, and what to do if launch day is quiet or something breaks.
- Each guide ends with the mistakes beginners usually make.
- Hands the SaaS notes to the shared teams, which cannot read this plugin's files.

Prices, fees and vendor policies in the guides are marked "check before relying"; confirm them on the vendor's page. Nothing here is legal or tax advice.

MIT licence; see `LICENSE`.
