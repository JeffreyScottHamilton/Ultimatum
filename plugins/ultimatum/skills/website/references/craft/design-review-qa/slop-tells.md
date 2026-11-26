# Slop tells: the generic-looking patterns and how to grade them

Read when scoring category 9 of the audit (generic or machine-made look), or before a build to avoid the patterns. The question: would a human designer at a respected studio ship this? The house version of this list is `../../website/design-rules.md` § 2; this file adds the audit-side detail and does not replace it. Where they overlap the house list wins and the audit just names the hit.

## The eleven classic patterns

1. Purple, violet or indigo gradient backgrounds, or blue-to-purple schemes.
2. The three-column feature grid: icon in a coloured circle, bold title, two-line blurb, repeated three times symmetrically.
3. Icons in coloured circles as section decoration.
4. Everything centred: every heading, description and card.
5. One big bubbly radius on every element.
6. Blobs, floating circles and wavy SVG dividers. If a section feels empty, it needs better content, not decoration.
7. Emoji as design: rockets in headings, emoji bullets.
8. A coloured left border on cards.
9. Hero copy of the "Welcome to X", "Unlock the power of..." or "Your all-in-one solution" kind.
10. Cookie-cutter rhythm: hero, three features, testimonials, pricing, call-to-action, every band the same height.
11. A system font stack as the main display or body face: the "gave up on type" signal.

## Rule ids (rendered-page tells with a name)

Use the id in findings so a repeat audit can compare. Each is one finding per element even when both a scan and a judgement hit it.

| Id | Tell |
|---|---|
| border-accent-on-rounded | accent border on a rounded card |
| overused-font | overused display font |
| flat-type-hierarchy | sizes too close to read as levels |
| gradient-text | gradient-filled text |
| cream-palette | cream default palette |
| nested-cards | cards inside cards |
| shape-assembled-illustration | art built from basic shapes |
| dark-glow | glow on a dark surface |
| radial-halo | radial halo behind content |
| radial-spotlight-glow | spotlight glow |
| marquee | scrolling logo strip |
| icon-tile-stack | icon tile above every heading |
| italic-serif-display | italic serif for display |
| hero-eyebrow-chip | chip or pill above the hero heading |
| kicker-above-heading | small label above every heading |
| marketing-buzzword | buzzword copy |
| aphoristic-cadence | short punchy fragments for rhythm |
| oversized-h1 | headline too big for its job |
| theater-slop-phrase | stage-whisper phrases |

Polish only (note, do not grade): monotonous spacing, bounce easing, pulsing dot, blinking cursor, numbered section labels, em-dash overuse, extreme negative tracking, thin border with a wide shadow, repeating stripes, grid-paper background, image hover transforms, monospace as costume, unthemed browser surfaces.

## Judgement tells (no tool finds these; you are the detector)

- Gradient buttons for the main action. One flat colour from the palette.
- A stock-photo hero, or a grey box standing in for one. Show the real product or nothing.
- Rounded shadowed cards as the container for everything. A stack of cards is not a layout.
- A testimonial row with avatars, five stars and quotes nobody said. Real names and real claims, or cut it.
- The default hero: headline left, screenshot right, two buttons.
- "Get started" and "Learn more" as the only actions. Name what the click buys.
- Three big numbers with tiny labels under the hero. Made-up statistics are never allowed (`craft-audit.md` § Claims).
- A grid of same-shaped cards for content of unequal weight.
- Frosted glass as the default surface. One translucent layer where it explains depth.
- Generated doodles and mascots instead of art direction.
- Every secondary action in a modal.
- Sparklines, progress rings and fake avatars filling space where content belongs.
- Dark because "it is a developer tool", light because "it is health". Use the use-scene test in `page-modes.md`.
- Only the happy path is designed. Empty, loading, error and long-content states are part of every component.

## Fonts

- Overused as the display voice: Inter, Roboto, Arial, Helvetica, Open Sans, Lato and similar. Allowed as body or UI on an Operate or Read surface when the design doc assigns that role.
- Novelty or dated faces to flag: Papyrus, Comic Sans, Lobster, Impact, Jokerman, Brush Script, Hobo, Trajan, Courier New as body, handwriting fonts.
- Faces the source also flags, as one opinion to weigh: Raleway, Clash Display.
- A named, deliberate pairing beats a default every time (`../../website/craft.md` § 2).

## How to grade

Each hit is one finding at medium impact; a first-impression hit (hard rejection in `page-modes.md`) is high. The AI-slop score is graded on its own and also counts 5 per cent of the design score (`scoring-and-baseline.md`).
