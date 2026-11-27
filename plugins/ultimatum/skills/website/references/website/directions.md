# Three directions

Three HTML pages that a person could tell apart from across the room. Same content and the same first action, different answers to "what should this feel like".

## Make them really different

First classify the page kind and note its effect cap (`design-rules.md`: a law firm gets fewer effects than a launch page). Deal each direction a palette, type pair and layout before any code.

Pick each direction's palette, type pair and hero layout on purpose so no two share more than one of the three. No brand → run `ult design system "<brief>"` once and use it for one direction and as the checklist for all three; the other two go elsewhere on purpose. Start from `brand/brand.md` when it exists (all three keep its colours and fonts but differ in layout, scale and motion). Check the user's reference sites: each direction should be close to at least one of them in spirit, never a copy of its layout, words or images.

Each direction gets one motion personality and keeps it on every element:

| Personality | Timing | Easing | Typical moves |
|---|---|---|---|
| **Snappy / precise** | 150–250 ms | sharp ease-out | crisp hover states, small slides, counters, tight stagger |
| **Soft / floaty** | 500–900 ms | long gentle ease-in-out | drifting layers, slow fades, light parallax, rounded shapes |
| **Cinematic / bold** | 800–1400 ms | strong ease-in-out, pinned sections | big type reveals, scroll-pinned scenes, full-bleed media, masked wipes |

Name the personality at the top of each file in a comment, with its durations and easing, so the builder can carry it into the real site.

## Files

`.ultimatum/directions/a.html`, `b.html`, `c.html`, each standalone (inline CSS, a little JS, GSAP and Lenis from a pinned CDN version if used). Serve the folder and screenshot each:

`node "${CLAUDE_PLUGIN_ROOT}/scripts/ult-browser.mjs" <url> --viewports 375x812,768x1024,1440x900`

Keep the screenshots next to the files. Show 1440 and 375 to the user; the critic gets all three widths.

## Anti-generic list

Before the critic sees anything, run the plan, de-generic pass, remove-one habit and lint in `design-rules.md`. The lint is the short list of habits that make a page look machine-made; honour a hit only when the brand or a reference truly calls for it, and say why. Decoration should carry information (a real photo, a real number, the real product).

## Show the product working

For a product, app or SaaS page, the hero or the next section shows the product doing its job: a short looping screen recording, a live mini demo, or an animated real interface with real-looking data. A stock photo of people at laptops, a blurred dashboard or a feature list is not enough. No product to show yet → a clearly labelled placeholder and a note in the report.

## Revision moves

After the user picks, they steer with the verbs in `design-rules.md` (bolder, quieter, tighter, looser, simpler, warmer, cooler, sharper). Re-run the critic after any big move.
