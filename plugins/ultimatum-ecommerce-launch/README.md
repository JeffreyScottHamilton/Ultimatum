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
| Catalogue | Product data sheet, consistent photos, titles and descriptions, product-page anatomy, reviews, cross-sell |
| Checkout and ops | Payments with test mode, tax basics (not tax advice), shipping, policies, abandoned cart, emails, inventory, fraud |
| Checklist | Test orders, mobile checkout, speed, analytics events, launch week, first-30-days metrics |

The manager runs the shared teams from `ultimatum-launch` and hands them the store notes they need. Prices, fees and vendor policies are marked "check before relying"; confirm them on the vendor's page. Shopify theme licence rows are in `skills/launch/references/checkout-and-ops.md`.

MIT licence; see `LICENSE`.
