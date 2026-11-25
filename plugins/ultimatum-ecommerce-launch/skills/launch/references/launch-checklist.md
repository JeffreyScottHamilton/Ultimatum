# Launch checklist

Owner-only steps are marked (owner). Do everything you can on a development or password-protected store first; each live change needs the owner's yes. Tick a line only with evidence: a screenshot, an order number, a test result.

## Before launch

- [ ] Payments set up, identity checks done (owner)
- [ ] Domain connected, HTTPS on (owner)
- [ ] Shipping zones and rates, taxes set (check with an accountant)
- [ ] Refund, privacy, terms, shipping policies live, linked in the footer and signed off (owner); outlines in `policy-pages.md`
- [ ] Every product: title, price, images to the shot list in `product-photos.md` with alt text, inventory, weight
- [ ] Compliance review of product claims and any AI imagery
- [ ] Order emails edited and read on a phone

## Test orders

- [ ] One order in payment test mode, start to confirmation email
- [ ] One real low-value order, then refunded (owner, after a yes)
- [ ] Each shipping zone and one discount code tried
- [ ] A variant that is out of stock behaves right
- [ ] Mobile checkout on a real phone: guest checkout, wallet pay, address autofill
- [ ] Store password removed (owner, on the live store, after a yes)

## Speed and quality

- [ ] Home, collection and product pages load fast on mobile (rule of thumb: main image visible in about 2-3 seconds; test with the browser check)
- [ ] Images compressed, few apps installed, no unused scripts
- [ ] Links, forms and the 404 page work
- [ ] Taste critic pass on home and one product page

## Analytics and events

- [ ] Platform analytics on; cookie banner if your regions need it
- [ ] Events: view product, add to cart, begin checkout, purchase, email signup
- [ ] One test purchase appears in analytics with the right value
- [ ] No credentials in Git, prompts or logs

## Launch week marketing

| Move | Notes |
|---|---|
| Email list | Pre-launch signup page; send a "we are open" email; honour consent rules |
| First offer | One simple offer (launch price or free shipping for a week); check margin |
| Social | 5-7 posts from the Social team; ask before each post goes out |
| Existing channels | Etsy, Instagram bio, packaging inserts point to the store |
| Friends and first buyers | Ask for honest reviews after delivery |

## Launch week, day by day

Each post, email send and ad spend needs its own yes.

| Day | Do |
|---|---|
| Day -7 | Checklist above done; password still on; launch email and 5-7 posts drafted and through compliance review |
| Day -3 | Final real test order and refund (owner); stock counted; packaging and inserts ready |
| Day -1 | Ask the user for the go; schedule the "we are open" email; prepare replies to likely questions (shipping time, sizing, returns) |
| Day 0 | Remove the password (owner, after a yes); place one order yourself to confirm live checkout; send the email; first post; watch orders and the inbox all day |
| Day 1-2 | Ship the first orders fast; thank first buyers personally; fix anything reported, logged with `ult loop add` |
| Day 3-5 | One post showing real orders being packed (with permission if a customer is named); reply to every comment |
| Day 6-7 | First weekly review from `first-30-days.md`; record it with `ult social --results "<numbers>"` |

## First 30 days

Daily checks, the weekly review, a funnel diagnosis table and a week-by-week fix list are in `first-30-days.md`. Numbers to read there: conversion rate, average order value, cart abandonment, repeat purchase rate, traffic by source, return rate.

## Common launch-day mistakes

| Mistake | Fix |
|---|---|
| Payments still in test mode when the password comes off | Place one real order right after opening |
| Launch discount code never tested | Try every code at checkout before the email goes out |
| Shipping zone missing for a country the email reaches | Check zones against where the list and followers are |
| Launch email links to the home page | Link straight to the product or collection the email is about |
| Nobody watching the inbox on day 0 | Name who answers, and for how many hours |
