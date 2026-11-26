# Building the store for real

The goal is a store you can open and click through before launch, not a plan of one. Pick the path in `route.md`, then build it here. Commands that touch a live store, payments or a domain need the owner's yes each time. Vendor commands and terms change: **check before relying** on the vendor's own docs.

## Files `ult shop` makes

| Command | Gives you |
|---|---|
| `ult shop catalog products.csv` | problems per row: missing title or price, repeated SKU, cost at or above price, compare-at not above price, no weight, no image or alt text, thin description. Exit 1 while a blocker is open |
| `ult shop catalog products.csv --to shopify` (or `woocommerce`) | `store/import-<platform>.csv` for the platform's product import, every product as a draft. Compare the header with the platform's sample CSV first |
| `ult shop numbers --price 24 --cost 6 --shipping 5` | money left per sale, margin, the most an ad can cost per sale, break-even ROAS, sales to cover monthly costs (`--fixed-monthly`). Put in the provider's real fee rates |
| `ult shop scaffold --catalog products.csv --brand "Name"` | a starter static store in `store/site/`: home grid, one page per product with Product structured data, policy page stubs, a 404, a small cart. Buy buttons use each product's Stripe Payment Link |
| `ult shop check store/site` | pre-launch check of any folder of HTML: titles, descriptions, viewport, one h1, alt text, heavy or missing images, dead links, Product data, link previews, 404 page |
| `ult shop emails --brand "Name" --color "#hex"` | welcome, abandoned cart, order confirmation and shipping emails in `store/emails/`, with a placeholder list to map to the email tool |
| `ult shop test-order --url <store url>` | `store/test-order.cjs`, a Playwright walk from home to checkout on a phone-size screen with a screenshot per step |

Product sheet columns (any order, extra columns ignored): Title, Description, Option Name, Option Value, SKU, Price, Compare at, Cost, Weight (g), Inventory, Image, Alt, Tags, Type, Vendor, Barcode, Payment link. A row with a blank title and a SKU is a variant of the product above it. An Etsy listings export works as it is for title, description, price, SKU, quantity and the first image.

## Path A: Shopify

1. The owner makes the store and a development or password-protected preview (owner).
2. Import `store/import-shopify.csv` in the admin under Products. Products arrive as drafts.
3. Theme: start from the free theme picked in `route.md`. With the Shopify CLI installed (`shopify version`), the owner logs in on their machine and the theme can be pulled, edited and previewed locally with `shopify theme dev` (check the current commands on Shopify's CLI docs). Without it, edit in the theme editor and keep a list of every change.
4. Save the preview pages (or the local dev server's pages) into a folder and run `ult shop check` on it. Read the browser check of home, a collection and a product at phone size.
5. Payments in test mode, then the test order (below).

## Path B: WooCommerce

1. Owner sets up hosting and WordPress; install WooCommerce.
2. Products, Import, upload `store/import-woocommerce.csv`, map any column the importer does not match by name.
3. A local copy (for example a local WordPress tool) is the safe place to try themes and plugins first.
4. Payment plugin in test or sandbox mode, then the test order.

## Path C: small static store with Stripe Payment Links

Good for a handful of products, a pre-order or a first drop.

1. In Stripe test mode, make a Payment Link per product (owner or with their yes); put each in the sheet's `Payment link` column.
2. `ult shop scaffold --catalog products.csv --brand "Name" --out store/site`, then replace the policy stubs with the pages from `policy-pages.md`.
3. Preview: `python3 -m http.server 8000 --directory store/site`, then the browser check at phone width.
4. `ult shop check store/site` until it shows 0 blockers.
5. Deploy only on the owner's yes (`release/SKILL.md`), then swap the test Payment Links for live ones.

Stripe Payment Links take one product per link; a basket of several products needs Stripe Checkout with a small server, or a platform. Say so when the catalogue grows.

## The test order

1. `ult shop test-order --url <preview or local url>`.
2. `node store/test-order.cjs` (Playwright is needed; the script uses a 390 px wide screen).
3. Open every screenshot in `.ultimatum/test-order/`. The step log is `steps.txt` there.
4. On a Stripe test-mode checkout (URL has `cs_test_`) the script types Stripe's public test card and stops before Pay. On any other checkout it stops before payment fields.
5. Finish the test payment by hand or with the owner, confirm the order, the stock change and the email. Tick the checklist line only with that evidence.

## When something is not possible here

Shopify admin, payment identity checks, domain and DNS are owner steps. Say what you prepared (import file, theme changes, emails) and what the owner has to click.
