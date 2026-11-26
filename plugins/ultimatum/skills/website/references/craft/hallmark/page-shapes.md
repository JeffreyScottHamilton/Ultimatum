# Page shapes: 21 named fingerprints, how to pick one, the SaaS deck

Read at the shape step, after the material inventory and the job are written down. The 21 shapes are a table, `../../../../../data/craft/hallmark/page-shapes.csv` (one row each: heading, body, divider, button, image, reveal, when to reach for it, when to avoid it, the layout compositions it uses). This file holds how to choose, the six-axis fingerprint, and the two shape notes the table cannot carry.

## A vocabulary, not a menu

Design the page the prompt asks for first, then name the shape you made so the log and gate 32 have something to compare. Reaching into the list and building what comes back collapses 21 shapes into the same three. If nothing fits, describe your own fingerprint on the six axes below and give it a short name ("a season page").

The 21: bento grid, long document, marquee hero, stat-led, workbench, conversational FAQ, manifesto, photographic, quote-led, specimen, catalogue, letter, index-first, narrative workflow, split studio, feature stack, type specimen, portfolio grid, map or diagram, ecosystem index, component playground. Nav and footer belong to the shape and are settled with the hero.

## How to pick

1. Read the material inventory. A shape that runs on captures or figures needs them (real, or slots the user asked for). With neither, take a shape that carries type and facts.
2. Note words in the prompt that signal a shape ("data heavy", "tell a story", "a list of links", "many small features", "personal note").
3. Read the log and any stamp in the project; exclude the last three shapes.
4. Match against the table and the domain list below; choose the one most distant from the logged shapes, then run the mirror test from `principles.md`.
5. State the pick once in the Picks block and the stamp.
6. Two pages for two prompts must look like different sites, not colour swaps of one template. A vague tone word ("modern", "clean") is read through the genre and stated as an inference, never asked again.

## Domain to three candidates (when the prompt names no shape)

Take three from different families (grid-led, document-led, poster-led, product-led); pick the one most distant from the last logged shape.

| Domain words | Candidates |
|---|---|
| podcast, audio, music | photographic, quote-led, letter |
| shop, product, merch, commerce | catalogue, photographic, bento grid |
| docs, CLI, SDK, API, open source | workbench, long document, component playground |
| platform, infra, B2B tool | bento grid, workbench, stat-led |
| agency, studio, portfolio | portfolio grid, split studio, index-first |
| personal one-pager, resume | long document, letter, index-first |
| restaurant, cafe, bar, menu | photographic, long document, catalogue |
| fashion, beauty, lookbook | photographic (real photos), catalogue, marquee hero |
| fintech, banking, payments | stat-led, workbench, long document |
| manifesto, campaign, cause | manifesto, quote-led, stat-led |
| editorial, foundry, magazine | specimen, long document, type specimen |
| product launch, SaaS marketing | bento grid, workbench, stat-led |
| conference, event, speaker | marquee hero, manifesto, photographic |
| no signal | bento grid, long document, manifesto |

Developer docs and developer marketing are different prompts: a walkthrough wants workbench, the landing wants bento plus stat-led. A one-pager and a case-study portfolio differ too; the "use" answer decides. For our local-business sites, restaurant, studio, shop and trade rows map to photographic, catalogue, index-first and long document; add the call, booking or quote action from `anatomy.md`.

## The six-axis fingerprint

Write one choice per axis, such as `Hanging|Asymmetric spans|Hairline|Outlined|Margin-aligned|None`.

1. **Heading placement:** left-margin (a label beside a heading is an eyebrow), hanging above in air, centred display, bottom-aligned, overlapping a photo or block, sticky, numbered by structure (a real `<ol>` with counters or one graphic numeral), inline with the body. Any is fair; a narrow auto-centred head over full-width left-flush content reads as a mistake.
2. **Body composition:** single column; two-column asymmetric (wide body, narrow caption margin); multi-column justified with hyphenation; marginalia; three equal columns for reference density; full-bleed with margin reset (65ch body, pull quotes and images bleed); asymmetric spans (2-1-3).
3. **Divider language:** hairline (0.5–1px, inset or bleed), ornament, negative space, bleed-colour block, double rule. One language per page, varied in weight and placement per seam.
4. **Button voice:** solid, outlined, unstyled underlined word, oversized solid, typographic only, form as the call.
5. **Image treatment:** full-bleed, cropped to grid, inline with text, margin-aligned, none.
6. **Reveal:** fade-up stagger (once), horizontal sweep, type unmask (a clip-path opening over text), number tick (real figures only), typewriter (terminal only), none.

Two rules: choices come from the same world (a justified newspaper body wants a typographic call, not an oversized solid), and no more than three of six axes are shared with any of the last three logged entries (a None forced by theme or material is not a shared choice).

## SaaS section deck (deal it, do not sequence it)

For a B2B SaaS page on the bento, stat-led, workbench or marquee shapes. Cards have roles, not positions.

| Base card | Role | Composition |
|---|---|---|
| Spec sheet | what it is in figures it ships with: limits, formats, versions, regions | table or rows |
| Worked example | the product doing one real job on the user's material | showcase or split |
| Changelog | last 3–4 entries with real dates | rows |
| Comparison | the product beside today's way, row by row, no scores | table |
| Pricing | the real price, 2–3 tiers; "Contact sales" on every tier says the brand distrusts the buyer | pricing rules in `craft-finish.md` |
| FAQ | real objections answered like a person | conversational FAQ shape |
| Call strip | the ask once, one button | band |
| Footer | the close in the theme's voice | `hero-and-page.md` |

Material cards exist only when the user supplied the material (and the Picks block says so): hero visual (a real capture, else the product built in a slot or a type hero), logo row (own customers, with permission; otherwise absent, no "trusted by" line), three features (three named capabilities each with a capture or figure; otherwise fold into the example or spec), testimonials (verbatim with name, role, company; otherwise absent).

Every deal deviates twice: drop at least one base card and name it (the call strip is the usual cut; the footer never drops), and either promote a second base card into the hero's place (a spec sheet as hero says "the numbers are the pitch") or reorder one adjacent pair (pricing before the example). Record it as `deck: -cta +changelog`. Fewer than five cards is a landing strip: add cards or change shape. Gaps mix the three section-gap steps. Non-SaaS shapes (editorial, manifesto, letter, long document, quote-led) skip the deck; a bakery does not need a tier comparison.

## Shape notes

**Long document** keeps its section heads inline with the text, which needs a little CSS:

```html
<article class="prose">
  <p>Opening paragraph.</p>
  <h2 class="run-in">A short head.</h2>
  <p>Text that continues on the same line. <a href="#prices">See the prices</a></p>
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
