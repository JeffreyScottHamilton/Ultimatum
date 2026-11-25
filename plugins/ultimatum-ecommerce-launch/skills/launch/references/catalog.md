# Catalogue and product pages

Hand the relevant parts of this file to the Website and Social teams in the skill args. Numbers below are rules of thumb, not facts.

## Product data

Keep one sheet (CSV) as the source of truth:

| Field | Notes |
|---|---|
| Title | Plain words a buyer would search |
| Price, compare-at price | Currency, tax-inclusive or not by region |
| SKU, barcode | Unique SKU per variant |
| Weight, dimensions | Needed for shipping rates |
| Variants | Size, colour; one image per colour |
| Cost | For margin checks; never shown |
| Inventory | Count, or "made to order" |
| Country of origin, materials, care | Often required for labels and customs: check regional rules |

Import by the platform's CSV tool into a development or hidden store first. The platform's template sets the exact column names: download its sample CSV and fill that (check before relying: column names change between platforms and versions).

Example rows (a made-up product, to show the shape):

| Handle | Title | Option: Scent | SKU | Price | Weight (g) | Inventory |
|---|---|---|---|---|---|---|
| cedar-candle | Hand-poured soy candle | Cedar and smoke | CND-CEDAR-200 | 24.00 | 410 | 30 |
| cedar-candle | Hand-poured soy candle | Fig and black tea | CND-FIG-200 | 24.00 | 410 | 18 |

Steps:
1. Fill five products first, import, check them in the store, then do the rest.
2. Weigh each item packed, not bare.
3. Keep the sheet as the master; edit there and re-import, or edit in the platform and re-export, but not both.

## Photos

Full shot list, setup and editing pass: `product-photos.md`. The short version: one background, the same angles and crop ratio for every product, one image per colour variant, alt text on every image.

## Titles and descriptions

- Title: what it is + the key trait. "Hand-poured soy candle, cedar and smoke".
- First two lines: the benefit and who it is for. Then bullets: size, materials, care, shipping note.
- Write like a person; no stuffed keywords; no claims you cannot back up (health, "best", "eco") - the compliance reviewer checks them.
- Answer the doubts: fit, sizing, how long it lasts, what is in the box.

## Product-page anatomy (top to bottom)

1. Images, with the first one clear on a phone.
2. Title, price, star rating if real.
3. Variant picker and a clear Add to cart button.
4. Shipping and returns line near the button.
5. Short description, bullets, details accordion (materials, care, size chart).
6. Reviews and customer photos.
7. "You may also like".

## Variants and collections

- Use variants for options of the same item; separate products when photos, prices or descriptions differ much.
- Show out-of-stock variants as unavailable rather than hiding them, and offer a back-in-stock email.
- Collections by need, occasion, price band; automated by tag so new items appear.

## Reviews and UGC

- Collect after delivery: an email about a week or two after the order arrives (rule of thumb; later for products that take time to judge, like skincare).
- Only real reviews; never fake or incentivise only good ones. Rules on review incentives vary: check before relying.
- Ask permission before reposting a customer photo; log it.
- Before launch there are no reviews: use a founder note, a guarantee, press or test-buyer quotes with permission.

## Cross-sell

- "Goes well with" on the product page (hand-picked for best sellers).
- A bundle or set at a small saving; check margin first.
- In cart: one low-price add-on, not five.
- After purchase: the order email suggests refills or companions.

## Beginner mistakes

| Mistake | Fix |
|---|---|
| Launching with the whole back catalogue | Launch with the best sellers; add the rest once pages convert |
| Supplier description pasted in | Rewrite in the store's voice; duplicate text helps nobody and may break the supplier's terms |
| Variants as separate products (or the reverse) | Same item in options = variants; different photos and prices = products |
| No weights entered | Shipping rates come out wrong at checkout |
| Compare-at prices that were never charged | Only show a "was" price the item really sold at; reference-price rules vary by place (check before relying) |
| Claims like "organic", "non-toxic", "eco" without proof | Remove, or keep the certificate on file; the compliance reviewer checks |
