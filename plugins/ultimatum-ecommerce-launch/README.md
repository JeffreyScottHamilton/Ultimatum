# Ultimatum E-commerce Launch

A launch manager for online stores: Shopify, WooCommerce, Etsy-to-own-store, print-on-demand and small DTC brands. It runs the shared Ultimatum Launch teams with store-specific intake, platform and theme advice, catalogue rules, checkout and operations notes, and a launch checklist. Every spend, post, publish and deploy waits for your yes.

It needs the core `ultimatum` plugin and the `ultimatum-launch` plugin, which holds the Business, Website, Social Media, Brand Film and Motion Graphics teams and the reviewer agents.

## Install

```
/plugin marketplace add JeffreyScottHamilton/Ultimatum
/plugin install ultimatum@ultimatum
/plugin install ultimatum-launch@ultimatum
/plugin install ultimatum-ecommerce-launch@ultimatum
```

## Start

Say "Help me launch my online store", or type `/ultimatum-ecommerce-launch:launch <what you sell>`. Progress is kept in `.ultimatum/`; run it again to resume.

## What it adds over the base manager

| Area | What you get |
|---|---|
| Intake | Store questions in rounds with recommended answers: catalogue, fulfilment, platform, payments, tax, returns, channels |
| Route | Shopify vs WooCommerce and other choices, theme choice, store structure, which video style fits |
| Catalogue | Product data sheet with an example, titles and descriptions, product-page anatomy, reviews, cross-sell |
| Product photos | A shot list per product and per category, a cheap home setup, an editing pass, rules for AI images |
| Checkout and ops | Payments tested step by step, tax basics (not tax advice), how to set shipping rates, abandoned cart, emails, inventory, fraud |
| Policy pages | Outlines for refund, shipping, privacy and terms pages and how to get them signed off (not legal advice) |
| Checklist | Test orders, mobile checkout, speed, analytics events, a day-by-day launch week |
| First 30 days | Daily checks, a weekly review, a funnel diagnosis table and a week-by-week fix list |

Each guide ends with the mistakes beginners usually make.

The manager runs the shared teams from `ultimatum-launch` and hands them the store notes they need. Prices, fees and vendor policies are marked "check before relying"; confirm them on the vendor's page. Shopify theme licence rows are in `skills/launch/references/checkout-and-ops.md`.

MIT licence; see `LICENSE`.
