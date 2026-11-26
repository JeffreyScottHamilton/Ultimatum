# Checkout and store operations

Plain summaries, not legal, tax or financial advice. Anything about fees, limits, rates or vendor policy is **check before relying** on the vendor's or authority's own page. Owner-only steps (identity checks, bank details, tax registration) stay with the owner; never ask for credentials.

## Payments

- Use the platform's own payment provider first; add PayPal or a wallet if customers ask.
- Set up identity and bank checks early: they can take days (owner only).
- **Test mode first**, step by step:
  1. Turn on the provider's test mode (or the platform's test gateway).
  2. Take the test card numbers from the provider's own docs; never use a real card in test mode.
  3. Place an order for each case: a successful card, a declined card, a wallet payment if offered, an order with a discount code.
  4. Check each one: order appears, inventory drops, confirmation email arrives, analytics records it.
  5. Refund one test order and check the refund email.
  6. Switch to live (owner only, after a yes), then do one real low-value order and refund it (see `launch-checklist.md`).
- Payout schedule and any first-payout hold: check before relying on the provider's page, and tell the owner so cash flow is not a surprise.
- Each real payment, refund or payout change is its own yes.

## Tax basics (not tax advice)

- Whether you must collect sales tax, VAT or GST depends on where you and your customers are, and on thresholds. Ask an accountant or the tax authority.
- Decide: are prices shown tax-inclusive or added at checkout? Many regions expect one or the other.
- Turn on the platform's tax settings for the regions you are registered in; do not guess rates.
- Cross-border: duties and import tax may fall on the customer; say so on the shipping page.

## Shipping

| Choice | Notes |
|---|---|
| Zones | Start with regions you can serve well |
| Rates | Flat, free over a threshold, weight-based, or carrier-calculated |
| Free-shipping threshold | Rule of thumb: a bit above average order value to lift basket size; test it |
| Packaging | Weigh and measure real parcels before setting rates |
| Handling time | State it honestly on product and shipping pages |
| Tracking | Send the tracking email automatically |

Carrier prices and platform label discounts: check before relying.

How to set rates without losing money:
1. Pack three typical orders (small, medium, large) and weigh and measure each.
2. Get the real carrier price for each to your main zone and your furthest zone (carrier site or the platform's label tool).
3. Add packaging cost. That is your true shipping cost per order type.
4. Decide what the customer pays: the full cost, a flat rate that averages it out, or free (the cost goes into the product price or the threshold).
5. Write it down in the shipping policy (`policy-pages.md`) and check checkout shows the same.

Worked example with made-up numbers: if the real cost is 6 for small parcels and 9 for large, a flat 7 rate loses 2 on every large order; either price large items to cover it or add a weight-based rate.

## Policies

Four pages live before launch: refund and returns, shipping, privacy, terms. Outlines, the order to write them in and common mistakes: `policy-pages.md`. Platform generators give a starting point only; legal requirements vary by region (check before relying). The owner signs off each page.

## Abandoned cart

- Turn on the platform's abandoned-checkout email. Built-in tools may send only one email; more steps may need an email app (check before relying).
- A common sequence (rule of thumb): first about an hour after leaving, second the next day, third two or three days later.
- Plain reminder first; offer a discount only in the last one.
- Only email people who agreed to receive email where the law requires it.

## Order emails

Edit the defaults, starting from `ult shop emails` (welcome, abandoned cart, order, shipping) mapped to the platform's own variables: order confirmation, shipping confirmation, delivery, refund. Use the brand voice, show the logo, add support contact, and say what happens next. Send test orders to yourself and read them on a phone.

## Inventory

- Track stock counts; set a low-stock alert.
- Decide: allow overselling or not (usually not).
- One source of truth if you also sell on Etsy or Amazon; syncing apps: check before relying.
- Count physical stock before launch.

## Fraud basics

- Use the platform's fraud analysis; review flagged orders before shipping.
- Warning signs: mismatched billing and shipping, rush shipping on a high-value first order, many small orders from one address.
- Keep proof of shipment and delivery for chargebacks.
- Do not store card numbers yourself.

## Licences and terms

Summaries from the theme licences as read when this plugin was written; **check before relying** on Shopify's current theme licence text.

| Tool | What to know | What to do |
|---|---|---|
| Shopify Horizon theme | Use is limited to Shopify stores. Selling or distributing a theme derived from it is not allowed; delivering it to one merchant's own store is. | Client-store builds only; refuse to package a reusable or sellable theme. |
| Shopify Dawn theme | Use is limited to building themes for Shopify stores. | Same practice as Horizon: build for one merchant's store; do not package a derived theme for sale or reuse until the licence text has been read. |
| Paid third-party themes | Licence is usually per store; moving it to another store may need a new purchase (check before relying). | Buy under the owner's account, not yours. |

Video, music and stock licences are in `shared/licenses.md`. Short version: free tiers of voice and music tools are often non-commercial, free stock needs a log of source and licence, and recognisable people need releases. A company of more than 3 people needs a paid Remotion company licence (check before relying).
