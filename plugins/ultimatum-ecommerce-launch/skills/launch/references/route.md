# Route: online store

For shops selling from a catalogue. Team: Business & brand, a store builder, Website (anything outside the theme), a copywriter, a creative producer, Marketing, the compliance reviewer. Marketing runs the usual loop.

## Platform choice

All claims about fees, plans and limits: **check before relying** on the vendor's own page.

| Situation | Usually fits | Why |
|---|---|---|
| First store, no tech help, wants fast launch | Shopify | Hosted, checkout and payments built in, themes and apps |
| Already has a WordPress site or blog that earns | WooCommerce | Keeps one site and full code control; you run hosting, updates, security |
| Needs custom checkout logic or deep code control | WooCommerce, or Shopify with a developer | Depends on the logic |
| Handmade, few items, testing demand | Stay on Etsy, add a simple own store later | Marketplace brings traffic; own store brings brand and email list |
| Print-on-demand | Shopify or WooCommerce with a POD app | Check the partner's shipping times and margins |
| Digital downloads only | Shopify with a download app, or a digital-sales tool | Check fees and tax handling |
| Selling mostly on social | A platform with that channel built in | Check per-channel terms |

Rule of thumb (not a fact): the platform the owner can keep running alone beats the one with the longest feature list.

Quick test before you recommend: can the owner add a product, change a price and refund an order without help? Show them on the platform's free trial or demo if one exists (check before relying).

Moving from Etsy: keep the Etsy listings live, link to the new store from packaging and the shop About page, and read Etsy's rules on links and off-site sales first (check before relying).

## Shopify working rules

- Recommend Shopify's official **AI Toolkit** plugin and its Dev MCP rather than repeating what they do (check before relying: current name, install steps and what it can change). Avoid community Shopify skill packs that run code through hooks.
- Work on a **development store** first. On the live store the **owner confirms every change**: changes through the toolkit may not be undoable.
- The toolkit's telemetry is on by default. When the store belongs to a client or holds customer data, offer to turn it off before starting. Check before relying: the current opt-out method.
- Themes: build on **Dawn** or **Horizon** with Shopify CLI and theme check. Licences allow building for a merchant's own store; **never package or sell a reusable theme** derived from them. See `checkout-and-ops.md`.

## Theme choice

| Need | Pick |
|---|---|
| Small catalogue, bold imagery | Horizon-style theme, a few strong sections |
| Large catalogue, filters, speed | Dawn, lightly changed |
| Strong custom look | Start from a free theme, customise sections; paid themes: check licence and price before relying |

Prefer the theme's built-in sections to custom code; every extra app slows the store. Run the Website team for three look directions, then apply the chosen one to the theme.

## Store structure

- **Navigation:** Shop (collections), About, Contact/FAQ. Four to six items at most.
- **Collections:** by what the customer wants (gifts, for the kitchen), not your internal categories. Add "Best sellers" and "New".
- **Pages:** home, collection, product, cart, about, contact, shipping, returns, privacy, terms.
- **Footer:** policies, email signup, social links, payment icons.

## Higgsfield (product photos, ad packs, UGC-style video)

- **Default for product and social video**, through the Higgsfield MCP when the user has connected it. Follow `video/higgsfield.md`: credit check, plan per shot with costs, the user's yes, one generation, review, then the next. The whole video follows `video/guide.md`; voice, music and effects follow `video/audio.md` (ElevenLabs by default).
- Not connected: say so, offer Motion Graphics instead, and do not install anything.
- Only after a **credit check**: say what will be generated, how many, and the estimated credits; wait for the user's yes. Agent use spends credits even on "unlimited" plans. Check before relying: plan prices, which plans allow the MCP, commercial rights on the free tier.
- One generation per yes; never retry silently. No real people without consent; label AI content where platforms require it.
- AI product images must still show the real product accurately; a misleading image is a compliance blocker.

## Ad creative

- Each ad angle states a hypothesis: the metric it should move and in which direction. Keep a learnings list in `brand/brand.md`.
- Read ad results from CSV exports the user provides; never ask for ad-account API keys.

## Video style

| Content | Style | Why |
|---|---|---|
| Product ad or social clip from product photos (most stores) | Higgsfield first, after a credit check; Motion Graphics second | Real product, fast variants; label AI content |
| Many products, one format | Motion Graphics, one template and many variants | Cheap to repeat per product |
| Product demo or a number (free shipping, 4.8 stars) | Motion Graphics | Clear, quick to update |
| Maker, craft or gifting story | Brand Film with real footage of the maker | Feeling carries; no AI people |
| UGC-style product clips | Higgsfield, after a credit check | Fast variants; label AI content |

Paid ads: check stock and music licences in `checkout-and-ops.md` and `shared/licenses.md`.

## Beginner mistakes at this stage

| Mistake | Fix |
|---|---|
| Choosing a platform for one feature they may never use | Choose for daily running; add an app later if the need is real |
| Buying a theme before the catalogue and photos exist | Pick the theme after `product-photos.md` shots are done; good photos decide most of the look |
| Installing apps "just in case" | Each app slows pages and adds data sharing to the privacy page; add one per real need |
| Mega-menu with every category | Four to six top items; collections by what the buyer wants |
