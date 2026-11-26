# Icons, logos and diagrams

Read when a page names tools, file types or integrations, needs interface glyphs, or wants a node-and-line diagram of how something connects.

## Real logos

- A tool the product really works with shows its **real logo in its own colours**: where a real mark exists, never substitute a look-alike, a stock glyph, or an initial inside a circle.
- A fictional client's own mark is designed for it, never borrowed from a real brand.
- Logo rows of customers appear only when the brief names them and gives permission (`copy.md` § Truth).

## Icon sets

Use only sets whose licence allows reuse, pinned to a version, in this order:

| Set | Holds | Licence | Use |
|---|---|---|---|
| gilbarbara/logos (https://github.com/gilbarbara/logos) | about 1,500 brand marks in full colour | CC0 | first choice for any brand |
| Simple Icons (https://simpleicons.org/) | one-colour brand marks with the official hex | CC0 | only where no colour mark exists |
| vscode-icons (https://github.com/vscode-icons/vscode-icons) | coloured document icons (Excel, Word, PowerPoint, PDF, Markdown, zip) | MIT | a document type, never a brand |
| Lucide (https://lucide.dev/) | interface glyphs, one line set | ISC | search, arrow, check, a feature point |

- The source kit's resolver covered 458 tools, 38 file types and 435 glyphs tagged by kind (dev, AI, gaming, engine, hardware, chips, cloud, database, monitoring, payments, social). Its scripts are not part of this plugin (`later.md` § Source tooling).
- Check each set's licence file at the pinned version before shipping, and record the version.

## Trademarks

- Every mark stays its owner's trademark. Show it only to identify a tool the product truly integrates with (nominative use), and never suggest the owner endorses the client.
- Add to the footer credit line: "All product names and logos belong to their respective owners." Keep a small credits file listing each icon's file, set, source version, licence and whether it is a trademark.
- Consoles whose marks are in no permitted set (Xbox, Nintendo) are named in type, never drawn. A game's store row uses marks that are available (Steam, PlayStation, Epic Games).
- Office documents show as file-type icons, not the suite's brand.
- A set whose package licence covers only the compilation, not each mark, is not used.

## Serving icons

- Write every icon to a local SVG at build time from the pinned package. No runtime CDN call, no icon font, no tinting a colour mark by CSS filter.
- Crop each mark to its drawn bounds with a 2% margin, and classify its shape by the cropped width-to-height ratio: wide (over 1.8 : 1), landscape (over 1.25 : 1), tall (under 0.8 : 1). File icons are not cropped.
- Scan the finished page for every named tool and check each has its file before shipping.

## Interface glyphs

- One line set only (Lucide). A glyph is inline SVG with `stroke="currentColor"` so it takes the text colour, and `aria-hidden="true"` beside a text label.
- One-colour brand marks fit a row of customer logos and footer social links.
- Arrows after button labels follow the house lint (`../../website/design-rules.md` §2): not on every button.

## On dark grounds

- Logos sit on a soft light tile on dark grounds, so every colour reads.
- Black marks (GitHub, Apple, X) turn white on a dark ground. Wordmark-only logos (Stripe, NVIDIA, Go) take a wide tile.
- A multi-tone mark shown in one colour keeps its detail: knock out (make transparent) the parts that were drawn in the background colour instead of filling them in.
- Drop a pale mark from any light layout where it would disappear against the tile.
- **Violet:** the page's own palette never uses violet, but a third-party logo is not recoloured. Measure the share of a mark's coloured fill that is violet (deep navy is not violet). At half or more (for example Stripe, Twitch, Terraform, Datadog, Kotlin, .NET), a tool the product truly uses keeps its colours; a customer-logo row may print it in one colour. Under half (Figma, Google Drive) prints as drawn. Swapping a well-known logo for a grey placeholder counts as an error.

## Layouts

| Layout | Use |
|---|---|
| tile | a soft square behind one logo |
| row | a list row: icon, name, short fact |
| chip | a name with a small icon inline |
| stack | overlapping round tiles ("works with") |
| mosaic | an integration grid of tiles |
| file card | a file-type icon with name and size |

- Icon sizes 16, 20, 24, 32, 40, 48, 56 px. Integration grids, file cards and lists of sources a product reads use the real icons at 20–40 px, not grey squares.
- In a tile, a landscape mark fills 70% of the tile's width and a portrait mark 68% of its height.
- Icons never animate.

## Diagrams

A diagram shows how things connect (the product among its tools, data gathering into one store, a pair of systems kept in step, an ordered sequence, geographic regions). An interface fragment shows what a user sees (`cards-and-ui.md`). Choose by which question the section answers.

- **Tech pages:** one per section, two per page at most; they may pulse.
- **Product and service pages:** one, still, with no ground pattern or glow.
- **Place pages:** none.
- A game's diagram shows a system (matchmaking, saves, a season), never stands in for pictures of the game.
- A malformed diagram draws what it can and logs an error; it never leaves an empty card.
- Draw diagrams as inline SVG with real text, at a card size (about 560 × 340) or a section size (about 1200 × 560).

### Diagram layouts

| Layout | Shows | Default ground (tech) |
|---|---|---|
| hub | one core with tools around it; a mind map when tools have sub-items; a radial web | concentric rings |
| ring | logos or regions on an orbit | none |
| tree | one thing branching out | dots |
| lanes | one input, a core, parallel lanes | dots |
| fan-in, bow-tie | many into one; and out again to many | dots |
| sync | two systems with records crossing | none |
| timeline | steps done in turn | none |
| grid | files into a pipeline | dots |
| free | your own nodes and edges | dots |

- The source kit holds 27 preset specs across these layouts, tagged by page kind (software, tech, gaming, product, service); start from the shape, never its sample words.
- The diagram that leads a section may add a soft glow behind its core (tech only).
- Sizes: card or band; a flat drawing takes the larger size when it fits.
- Lines: every line is a hairline. Spokes leave the core's edge as straight rays by default, or as curves, elbows or swirls. Flows turn corners with rounded elbows. The core is a tile filled with ink.

### Labels

- Every label, number and icon must be swapped for the client's real ones. Labels are plain, 1–3 words; the core carries the product's own name.
- Numbers only from the brief (`../../website/design-rules.md` §2 bans fake stats); no jargon.
- Up to 8 spokes and 12 nodes in a card. More than that is a list.
- A diagram gets no caption; its card's title names what it shows, and the SVG has a `<title>` and `role="img"` for screen readers.
- Tools show their real marks in their own colours. A core with no icon is its name on a rounded label.

### Diagram motion

Tech only. A pulse is a short bright dash with a glow running along each line, in the accent; only the light and what it reaches take the accent.

- Laid out as a ripple: each spoke or route starts 0.24–0.5 s after the last, inside one 2.5–4 s cycle (3.2 s default).
- Hovering the card, or tabbing focus into it, starts the run again from the beginning.
- Runs only on screen. Phones and reduced motion hold it still. A diagram still moving after 5 s gets a pause control (WCAG 2.2.2).
- The card itself stays put, and scrolling triggers nothing.

```html
<figure class="dg">
  <svg viewBox="0 0 560 340" role="img" aria-labelledby="dg-t">
    <title id="dg-t">Ledgerline sends each paid invoice to Xero, Stripe and Slack</title>
    <g class="dg-lines" fill="none" stroke="currentColor" stroke-opacity=".25" stroke-width="1">
      <path id="s1" d="M280 170 L120 70"/><path id="s2" d="M280 170 L440 70"/><path id="s3" d="M280 170 L280 300"/>
    </g>
    <g class="dg-pulse" stroke-linecap="round" stroke-width="2" stroke="var(--accent)" fill="none">
      <use href="#s1" style="--d:0s"/><use href="#s2" style="--d:.32s"/><use href="#s3" style="--d:.64s"/>
    </g>
    <rect x="220" y="150" width="120" height="40" rx="8" fill="var(--ink)"/>
    <text x="280" y="175" text-anchor="middle" fill="var(--g-main)" font-size="14">Ledgerline</text>
    <text x="120" y="60" text-anchor="middle" font-size="13">Xero</text>
    <text x="440" y="60" text-anchor="middle" font-size="13">Stripe</text>
    <text x="280" y="322" text-anchor="middle" font-size="13">Slack</text>
  </svg>
</figure>
<style>
  .dg-pulse use { stroke-dasharray: 18 400; stroke-dashoffset: 18;
                  animation: dg-run 3.2s linear infinite; animation-delay: var(--d); }
  @keyframes dg-run { 0% { stroke-dashoffset: 18; } 40%, 100% { stroke-dashoffset: -210; } }
  @media (prefers-reduced-motion: reduce), (hover: none) { .dg-pulse { display: none; } }
</style>
```

## Dimension drawing

On a product page whose photographs already show the product, a side-view drawing may sit beside its specs.

- Draw it as a single inline SVG to scale, with 1 user unit = 1 mm; the `viewBox` is the product plus 6%; the box's `aspect-ratio` is its width over its height.
- Two or three dimension lines, each with its figure as live text.
- Not allowed: as the hero; as the sole image of the product; on hardware, which gets photographs or the client's own render instead; on any page that has no photographs.
