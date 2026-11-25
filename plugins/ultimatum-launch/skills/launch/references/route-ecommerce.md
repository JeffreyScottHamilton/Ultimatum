# Route: e-commerce

For shops selling from a catalogue. Default stack: Shopify. Product images and ad creative may use Higgsfield; marketing runs the usual loop.

## Team

Business & brand, a store builder, Website (for anything outside the theme), a copywriter, a creative producer, Marketing, the compliance reviewer.

## Shopify

- Recommend the official **Shopify AI Toolkit** plugin (and its Dev MCP) rather than repeating it; avoid community Shopify skill packs that run code through hooks.
- Work on a **development store** first. On the live store, the **owner confirms every change** before it is made: changes through the toolkit may not be undoable.
- The toolkit's telemetry is on by default. When the store belongs to a client or holds customer data, offer to turn it off (the opt-out described in its README) before starting. Check before relying: the current opt-out method.
- Themes: build on **Dawn** or **Horizon** with Shopify CLI and theme check. Their licences allow building for a merchant's own Shopify store; **never package or sell a reusable theme** derived from them (Horizon is the stricter of the two). See `licenses.md`.

## Higgsfield (product photos, ad packs, UGC-style video)

- Only after a **credit check**: say what will be generated, how many, and the estimated credits; wait for the user's yes. Agent use spends credits even on "unlimited" plans. Check before relying: plan prices, which plans allow the MCP, and commercial rights on the free tier.
- One generation per yes; never retry silently. Extra care with AI faces and avatars: no real people without their consent, and label AI content where platforms require it.

## Ad creative

- Each ad angle states a hypothesis: the metric it should move and in which direction. Keep a learnings list in `brand/brand.md` so tested angles are not repeated.
- Read ad results from exports the user provides (CSV); never ask for ad-account API keys.

## Launch checklist (owner-only steps marked)

- [ ] Payments set up and identity checks done (owner only)
- [ ] Domain connected (owner only)
- [ ] Shipping zones and rates, taxes
- [ ] Refund, privacy, terms and shipping policies (owner signs off)
- [ ] Every product: title, price, images with alt text, inventory
- [ ] A real test order placed and refunded
- [ ] Store password removed (owner only, on the live store, after a yes)
- [ ] Compliance review of product claims and any AI imagery
