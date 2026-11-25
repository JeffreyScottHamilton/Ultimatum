# First 30 days: watch, diagnose, fix

After the store opens, the job is to find the biggest leak and fix one thing at a time. Read numbers from the platform's own reports and exports. Rule-of-thumb thresholds are not benchmarks; average rates vary a lot by product, price and traffic source, so compare the store against its own previous week first.

## Numbers to watch

| Metric | What it tells you | If it is low |
|---|---|---|
| Conversion rate (orders / sessions) | Is the page persuading? | Fix photos, shipping info, price clarity, reviews |
| Average order value | Basket size | Bundles, free-shipping threshold, add-ons |
| Cart abandonment | Checkout friction | Show shipping cost early, add wallets, send reminders |
| Repeat purchase rate | Product and brand fit | Post-purchase email, refills, loyalty offer |
| Traffic by source | Where buyers come from | Double down on one channel; cut the rest |
| Return and refund rate | Description accuracy | Improve sizing and photos |

## Daily for the first week (about 15 minutes)

- [ ] Every order shipped within the stated handling time; tracking emails sent.
- [ ] Inbox and social messages answered within a day.
- [ ] Flagged orders from fraud analysis reviewed before shipping.
- [ ] Payment provider dashboard: no failed payouts or account holds (owner).
- [ ] Error check: open home, one product, cart and checkout on a phone; anything broken goes into `ult loop add "<finding>" --where "<page>" --blocker`.
- [ ] Note sessions, orders and revenue in a simple sheet, plus anything that happened (post went out, email sent).

## Weekly review (with the user)

1. Pull: sessions, orders, conversion rate, average order value, top traffic sources, top viewed products, cart and checkout drop-off, refunds and returns.
2. Find the biggest leak with the funnel table below.
3. Pick one change, write down what it should move and by how much you would call it a win, and when you will read it (at least a week later, rule of thumb, or longer if traffic is low).
4. Record the week with `ult social --results "<numbers and notes>"` and in `brand/brand.md` learnings.

## Funnel diagnosis

Look at the step where people drop off most compared with the previous step.

| Where people stop | Likely causes | Fix to try first |
|---|---|---|
| Few sessions at all | No traffic channel working yet | Email the list again, post on the one channel with the most followers, ask early buyers to share; do not redesign the store yet |
| Visit home, leave | Unclear what is sold or for whom; slow load | Hero image of the best seller, a plain headline, faster images |
| View products, no add to cart | Price surprise, weak photos, doubts unanswered | More photos (see `product-photos.md`), shipping cost and returns near the button, size guide, a review or guarantee |
| Add to cart, no checkout | Shipping cost revealed late, forced account, coupon field hunting | Show shipping early, allow guest checkout, add a free-shipping progress note |
| Begin checkout, no purchase | Payment options, trust, form length, errors | Add a wallet payment, test checkout on a phone again, check error messages |
| Buy once, never again | Product or follow-up | Post-purchase email with care tips and a refill or companion product |
| Many returns | Description mismatch | Fix sizing info, photos and colour accuracy on the returned products |

## Fix list for the first 30 days

Work top to bottom; skip what is already fine.

**Week 1: make sure nothing is broken**
- [ ] Place one more real order on a phone, on mobile data, and refund it (owner, after a yes).
- [ ] Check every order email reads well on a phone.
- [ ] Check analytics shows the same order count as the platform.
- [ ] Fix any product with a missing image, price, weight or alt text.

**Week 2: remove doubt on product pages**
- [ ] Top five viewed products: add missing shots, a size or dimension line, care and materials.
- [ ] Shipping and returns line near Add to cart on every product page.
- [ ] Answer the three questions customers asked most, on the page or FAQ.

**Week 3: lift order value and recover carts**
- [ ] Abandoned-checkout emails on and reading well (see `checkout-and-ops.md`).
- [ ] One bundle or "goes well with" on the best seller; check margin first.
- [ ] Try a free-shipping threshold if most orders sit just below it (rule of thumb); measure for at least a week.

**Week 4: start the repeat loop**
- [ ] Review request email to every buyer after delivery (see `catalog.md`).
- [ ] Post-purchase email: care tips, then a related product later.
- [ ] Keep one traffic channel, drop or pause the one that brought no buyers.
- [ ] Write a one-page 30-day summary for the user: numbers, what changed, what to try next.

## What not to do in the first month

| Tempting | Why to wait |
|---|---|
| Redesigning the theme | Too little data; fix product pages and checkout first |
| Installing many apps | Each one slows pages and adds a privacy-page entry |
| Running a big discount | Trains buyers to wait; check margin, keep one simple launch offer |
| Spending on ads before the page converts organic visitors | Ads multiply a leak; any ad spend needs the user's yes and a stated budget |
| Changing three things at once | You will not know which one worked |
