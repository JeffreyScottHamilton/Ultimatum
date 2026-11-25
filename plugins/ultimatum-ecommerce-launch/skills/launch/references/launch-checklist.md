# Launch checklist

Owner-only steps are marked (owner). Do them on a development store first; each live change needs the owner's yes.

## Before launch

- [ ] Payments set up, identity checks done (owner)
- [ ] Domain connected, HTTPS on (owner)
- [ ] Shipping zones and rates, taxes set (check with an accountant)
- [ ] Refund, privacy, terms, shipping policies live and signed off (owner)
- [ ] Every product: title, price, images with alt text, inventory, weight
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

## First 30 days

Read numbers from platform exports; rules of thumb below are labelled guesses, not benchmarks (check industry data before relying).

| Metric | What it tells you | If it is low |
|---|---|---|
| Conversion rate (orders / sessions) | Is the page persuading? | Fix photos, shipping info, price clarity, reviews |
| Average order value | Basket size | Bundles, free-shipping threshold, add-ons |
| Cart abandonment | Checkout friction | Show shipping cost early, add wallets, send reminders |
| Repeat purchase rate | Product and brand fit | Post-purchase email, refills, loyalty offer |
| Traffic by source | Where buyers come from | Double down on one channel; cut the rest |
| Return and refund rate | Description accuracy | Improve sizing and photos |

Change one thing at a time, note it in `brand/brand.md`, and compare after at least a week. Bring results to the user (`ult social --results` for social) and agree the next test.
