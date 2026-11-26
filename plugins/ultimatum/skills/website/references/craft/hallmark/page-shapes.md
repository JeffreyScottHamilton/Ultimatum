# Page shapes: 21 named fingerprints, how to pick one, the SaaS deck

Read at the shape step, after the material inventory and the job are written down. The 21 shapes are a table, `../../../../../data/craft/hallmark/page-shapes.csv` (one row each: heading, body, divider, button, image, reveal, when to reach for it, when to avoid it, the layout compositions it uses). This file holds how to choose, the six-axis fingerprint, and the two shape notes the table cannot carry.

## Shapes are a vocabulary

Design the page the brief asks for first, then name the shape that came out, so the log and gate 32 have something to compare. Picking from the list and building whatever it returns squeezes 21 shapes into the same three. If none fits, write your own fingerprint on the six axes below and give it a short name ("a season page").

The 21 shapes, in alphabetical order: bento grid, catalogue, component playground, conversational FAQ, ecosystem index, feature stack, index-first, letter, long document, manifesto, map or diagram, marquee hero, narrative workflow, photographic, portfolio grid, quote-led, specimen, split studio, stat-led, type specimen, workbench. Nav and footer belong to the shape and are settled together with the hero.

## Choosing one

1. Read the material inventory. A shape built on captures or figures requires them, either real or as slots the owner asked for. Without either, choose a shape that runs on type and facts.
2. Listen for shape cues in the brief, such as "a personal note", "tell a story", "data heavy", "many small features" or "a list of links".
3. Read the project's log and any stamp, and exclude the last three shapes used.
4. Compare with the table and the domain list below. Take the candidate furthest from the logged shapes, then run the mirror test from `principles.md`.
5. State the choice once in the Picks block and in the stamp.
6. Two briefs must yield two sites that look different, not one template in two colours. A vague tone word ("modern", "clean") is interpreted through the genre and noted as an inference; do not ask about it again.

## Domain words to three candidates (when the brief names no shape)

Pick three from separate families (product-led, poster-led, document-led, grid-led), then take whichever sits furthest from the last logged shape.

| Candidates | Domain words |
|---|---|
| photographic, quote-led, letter | podcast, audio, music |
| catalogue, photographic, bento grid | shop, product, merch, commerce |
| workbench, long document, component playground | docs, CLI, SDK, API, open source |
| bento grid, workbench, stat-led | platform, infra, B2B tool |
| portfolio grid, split studio, index-first | agency, studio, portfolio |
| long document, letter, index-first | personal one-pager, resume |
| photographic, long document, catalogue | restaurant, cafe, bar, menu |
| photographic (real photos), catalogue, marquee hero | fashion, beauty, lookbook |
| stat-led, workbench, long document | fintech, banking, payments |
| manifesto, quote-led, stat-led | manifesto, campaign, cause |
| specimen, long document, type specimen | editorial, foundry, magazine |
| bento grid, workbench, stat-led | product launch, SaaS marketing |
| marquee hero, manifesto, photographic | conference, event, speaker |
| bento grid, long document, manifesto | nothing in the brief to go on |

Developer docs and developer marketing are different briefs: a walkthrough fits workbench, while a landing page fits bento plus stat-led. A one-pager differs from a case-study portfolio too, and the page's purpose decides. For our local-business sites, the restaurant, studio, shop and trade rows map to photographic, catalogue, index-first and long document; add the call, booking or quote action from `anatomy.md`.

## The six-axis fingerprint

Choose one value per axis, written like `Centred / Single column / Double rule / Typographic / Inline / Fade-up`.

1. **Heading placement:** in the left margin (a label beside a heading counts as an eyebrow), hanging above in open space, centred display, bottom-aligned, overlapping a photo or block, sticky, numbered by structure (a real `<ol>` with counters, or one graphic numeral), or inline with the body. Any of these works; a narrow, auto-centred heading above full-width, left-flush content looks like a mistake.
2. **Body composition:** single column; two asymmetric columns (wide body, narrow caption margin); multi-column justified with hyphenation; marginalia; three equal columns for reference density; full-bleed with the margins reset, body held at 65ch while pull quotes and images break out; asymmetric spans (2-1-3).
3. **Divider language:** hairline (0.5–1px, inset or bleeding), ornament, empty space, a block of bleed colour, or a double rule. Keep one language per page, varying weight and placement from seam to seam.
4. **Button voice:** solid, outlined, an unstyled underlined word, oversized solid, type only, or the form itself as the call.
5. **Image treatment:** full-bleed, cropped to the grid, inline with text, aligned to the margin, or none.
6. **Reveal:** staggered fade-up (once), horizontal sweep, number tick (real figures only), type unmasking (text revealed by an opening clip-path), typewriter (terminal pages only), or none.

Two rules apply. Choices must come from one world: a justified newspaper body calls for a typographic action, not an oversized solid button. And no more than three of the six axes may repeat from any of the last three logged entries, and a None imposed by the theme or material is not counted as shared.

## SaaS section deck (dealt, not sequenced)

For a B2B SaaS page in the bento, stat-led, workbench or marquee shapes. Cards carry roles, not positions.

| Base card | Role | Composition |
|---|---|---|
| Spec sheet | the product in figures: limits, formats, versions, regions | table or rows |
| Worked example | one real job done in the product on the owner's own material | showcase or split |
| Changelog | last 3–4 entries, real dates | rows |
| Comparison | the product beside the current way of doing it, row by row, no scores | table |
| Pricing | the real price in 2–3 tiers; a "Contact sales" label on every tier signals distrust of the buyer | pricing rules in `craft-finish.md` |
| FAQ | actual objections, answered like a person would | conversational FAQ shape |
| Call strip | the one ask, one button | band |
| Footer | the closing voice of the theme | `hero-and-page.md` |

Material cards appear only when the owner supplied the material, and the Picks block says so. Hero visual: a real capture, else the product built in a slot, else a type hero. Logo row: the owner's own customers, with permission; otherwise omit it, with no "trusted by" line. Features: three capabilities by name, each backed by a capture or a figure, otherwise fold them into the example or spec. Testimonials: verbatim, with name, role and company, otherwise omit.

Every deal must deviate in two ways. First, name and remove at least one base card (the call strip is the usual cut and the footer always stays). Second, either promote another base card into the hero's slot (a spec sheet as hero says "the numbers are the pitch") or swap one adjacent pair (pricing ahead of the example). Record it like `deck: -cta +changelog`. With fewer than five cards you have a landing strip, so add cards or switch shape. Mix the three section-gap steps for spacing. Shapes outside SaaS (editorial, manifesto, letter, long document, quote-led) skip the deck; a bakery needs no tier comparison.

## Shape notes

**Long document** keeps its section heads inline with the text, which needs a little CSS:

```html
<article class="prose">
  <p>Opening paragraph.</p>
  <h2 class="run-in">A short head.</h2>
  <p>The text carries on along the same line. <a href="#prices">Prices are below</a></p>
</article>
<style>
  .prose { max-width: 65ch; line-height: 1.7; }
  .prose h2.run-in { display: inline; font: inherit; font-weight: 700; margin: 0; }
  .prose h2.run-in + p { display: inline; }
</style>
```

**Conversational FAQ** answers sit in native `<details>` (https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details); to animate the open state use a grid wrapper whose row goes from `0fr` to `1fr` over the long duration with the out easing, and let reduced motion open it at once.

**Opening-line style per shape** (write your own lines, from the prompt's facts): bento names the category and promise in a few words; long document and letter open in the first person, dated if useful; stat-led finishes the user's figure with a verb phrase; catalogue and ecosystem headers carry a date and a count; manifesto commits and never hedges; workbench and component playground open on a real example instead of a claim; quote-led uses only the user's quote.

For a local site the same shapes apply with the action added: a phone link, a booking step or a quote form must sit in the first screen whatever the shape (see `hero-and-page.md` and `anatomy.md`).
