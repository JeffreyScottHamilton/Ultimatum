# Pricing and billing

Plain guidance, not tax or legal advice. Every price, fee, limit and vendor policy here is "check before relying" on the vendor's own page. Items labelled "rule of thumb" are habits, not facts.

## Pricing models

| Model | Fits | Watch out for |
|---|---|---|
| Flat | One simple product, one kind of customer | Heavy users cost you more than they pay |
| Tiered (good, better, best) | Mixed customers with different needs | Too many tiers confuse; 3 is the usual (rule of thumb) |
| Per seat | Team tools where value grows with people | Customers share logins or cap seats |
| Usage-based | API, AI or storage where cost follows use | Bills are hard to predict; show a calculator and a cap |
| Freemium | Product spreads by use and has a clear paid limit | Free users cost money; the paywall must sit where value is felt |
| Free trial, card required | Sales-ready buyers, high intent | Fewer sign-ups, but a higher share of them pay (rule of thumb) |
| Free trial, no card | Wide top of funnel, need to learn fast | Lower trial-to-paid; needs good onboarding emails |

## How to pick

1. Name the **value metric**: what grows when the customer gets more value (seats, projects, calls, records)? Charge on that.
2. Check your own cost per customer at light and heavy use. Price above it.
3. Look at 3 competitors' pricing pages (fact-finder, sourced). Do not copy; place yourself on purpose.
4. Start with two or three plans and an annual option. Prices are easier to raise for new users than to cut. Test with real buyers, not guesses.
5. Writing it down: a plan name, a price, who it is for, what is included, the limit.

## Pricing page anatomy

- One-line promise, then plans side by side with the recommended one marked.
- Price, billing period toggle (monthly / yearly), and what the buyer gets in plain words.
- A clear action per plan (start trial, contact sales).
- Limits and overage rules stated openly; no hidden fees.
- FAQ: cancel, refund, switch plans, data export, tax, security.
- Proof near the buttons: a short customer quote or logo only if the user has permission.
- Compliance review before it ships: claims such as "save 10 hours" need evidence.

## Billing provider basics

- A hosted billing provider (Stripe is the default in `route.md`; Paddle and Lemon Squeezy act as a merchant of record that handle sales tax for you, check before relying on what each covers and charges) keeps card data off your servers.
- Always build in **test mode** first: test cards, test webhooks, test clocks. Use live mode only after the user's yes and for one action at a time.
- Webhook signature checks, idempotent handlers, and webhooks as source of truth for access.
- Keep keys in environment variables, restricted scope, never in Git, prompts or logs.
- Plan for failure: failed card retries, a grace period, and a clear email asking to update the card.
- Test the full path: sign up, pay, access on, change plan, cancel, access off at period end.

## Taxes on digital services

- Selling software across states and countries can mean collecting sales tax, VAT or GST. Rules differ by place and change. Check before relying: the thresholds and registration rules for each place you sell.
- Options: a merchant of record handles it for a fee; or you register and use your billing provider's tax tool. Show prices with or without tax the way each market expects.
- Ask an accountant before launch. This is not tax advice.

## Refunds and cancellation

- State the policy on the pricing page and in the terms: refund window, prorating, what happens to data after cancelling.
- Let people cancel in the product in a few clicks (Customer Portal). Hard-to-cancel flows draw complaints and, in some places, legal trouble (check before relying: local rules on automatic renewal).
- Send a renewal reminder for annual plans where the law or good practice asks for it.
- Refunds are money movement: ask the user before issuing each one.
