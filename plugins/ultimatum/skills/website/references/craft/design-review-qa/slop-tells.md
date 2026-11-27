# Slop tells: the generic-looking patterns and how to grade them

Read when scoring category 9 of the audit (generic or machine-made look), or before a build to avoid the patterns. The test: would a good studio's designer put their name on it? The house version of this list is `../../website/design-rules.md` § 2; this file adds the audit-side detail and does not replace it. Where they overlap the house list wins and the audit just names the hit. Eighteen of these can be found by script first: `page-lint.md`.

## The eleven classic patterns

1. Purple, violet or indigo gradient backgrounds, or blue-to-purple schemes.
2. The three-column feature grid: icon in a coloured circle, bold title, two-line blurb, repeated three times symmetrically.
3. Icons in coloured circles as section decoration.
4. Everything centred: every heading, description and card.
5. One big bubbly radius on every element.
6. Blobs, floating circles and wavy SVG dividers. A section that feels empty needs better content; ornament does not fix it.
7. Emoji as design: rockets in headings, emoji bullets.
8. A coloured left border on cards.
9. Hero copy of the "Welcome to X", "Unlock the power of..." or "Your all-in-one solution" kind.
10. Cookie-cutter rhythm: hero, three features, testimonials, pricing, call-to-action, every band the same height.
11. A system font stack as the main display or body face: the "gave up on type" signal.

## Rule ids (rendered-page tells with a name)

Use the id in findings so a repeat audit can compare. Each is one finding per element even when both a scan and a judgement hit it.

| Id | Tell |
|---|---|
| border-accent-on-rounded | coloured edge line on a card with rounded corners |
| overused-font | a display face everyone uses |
| flat-type-hierarchy | text sizes so close they read as one level |
| gradient-text | text filled with a gradient |
| cream-palette | cream default palette |
| nested-cards | cards inside cards |
| shape-assembled-illustration | art built from basic shapes |
| dark-glow | glow on a dark surface |
| radial-halo | radial halo behind content |
| radial-spotlight-glow | spotlight glow |
| marquee | scrolling logo strip |
| icon-tile-stack | a small icon tile stacked over each heading |
| italic-serif-display | italic serif for display |
| hero-eyebrow-chip | chip or pill above the hero heading |
| kicker-above-heading | small label above every heading |
| marketing-buzzword | buzzword copy |
| aphoristic-cadence | short punchy fragments for rhythm |
| oversized-h1 | headline too big for its job |
| theater-slop-phrase | stage-whisper phrases |

Polish only, noted but ungraded: identical spacing everywhere, bouncy easing, a pulsing dot, a blinking cursor, numbered section labels, too many em dashes, very tight tracking, thin border with a wide shadow, repeating stripes, grid-paper background, image hover transforms, monospace as costume, unthemed browser surfaces.

## Judgement tells (no tool finds these; you are the detector)

- Gradient buttons for the main action. One flat colour from the palette.
- A stock-photo hero, or a grey box standing in for one. Show the real product or nothing.
- Rounded, shadowed cards holding everything. Stacked cards do not make a layout.
- Testimonials with avatars, star ratings and quotes no customer gave. Use named, real statements or drop the row.
- The default hero: headline left, screenshot right, two buttons.
- Buttons that say only "Get started" or "Learn more". State what the click gets the visitor.
- A band of three huge figures with small captions below the hero. Invented statistics are never allowed (`craft-audit.md` § Claims).
- A grid of same-shaped cards for content of unequal weight.
- Frosted glass everywhere. Keep one translucent layer, where it explains depth.
- Generated doodles and mascots instead of art direction.
- Every secondary action in a modal.
- Sparklines, progress rings and fake avatars stuffed in where real content should sit.
- Dark because "it is a developer tool", light because "it is health". Use the use-scene test in `page-modes.md`.
- Only the success case is drawn. Every component also needs its empty, loading, error and overflowing-content versions.

## Fonts

- Overused as the display voice: Inter, Roboto, Arial, Helvetica, Open Sans, Lato and similar. Fine for body or interface text on an Operate or Read page if the design doc gives them that role.
- Novelty or dated faces to flag: Papyrus, Comic Sans, Lobster, Impact, Jokerman, Brush Script, Hobo, Trajan, Courier New as body, handwriting fonts.
- Faces the source also flags, as one opinion to weigh: Raleway, Clash Display.
- A named, deliberate pairing beats a default every time (`../../website/craft.md` § 2).

## How to grade

Each hit is one finding at medium impact; a first-impression hit (hard rejection in `page-modes.md`) is high. The AI-slop score is graded on its own and also counts 5 per cent of the design score (`scoring-and-baseline.md`).
