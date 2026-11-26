# Grounds and effects

Read when choosing section backgrounds, a brand band, or (on tech pages only) the page's one shader, canvas or WebGL effect.

## Who gets effects

"Effect" covers anything shader, canvas, WebGL, print-style or scroll-driven: lit grounds, creative WebGL parts, objects and prints, big scenes, tech moments, film or 3D heroes, timed loops. Card details live in `cards-and-ui.md` and timings in `motion.md`.

- **Effects are for tech pages only:** software (AI and developer tools count), gaming, and products with a technical subject (hardware, devices, networks). Hardware is dealt as tech.
- **Every other kind is flat** (place, service, everyday product). The house lint already bans decorative gradients and glass (`../../website/design-rules.md` §2). On these pages also never use canvas, WebGL, autoplay video, CSS gradients, SVG patterns or texture grounds, `backdrop-filter`, `filter`, `mix-blend-mode`, `mask-image`, grain, halftone, dither, duotone, print looks, SVG animation, GIFs, Lottie, a custom cursor, or a scroll or animation library.
- **What calm kinds do get:** the hero entrance; one or two moments built from photographs or type (`moments-and-scenes.md`); a map baked to a still; photographs in true colour; real icons; diagrams that hold still (places get none); and a 3D render of the product if, and only if, the brief requests 3D (`objects.md`).
- **Subject before effect.** An effect never stands where the product, device or game world belongs. A robot arm drawn as a silk shader loses to a plain photo of the arm. Hardware lacking photographs borrows licensed shots of a similar machine in use; a game lacking art sets its title big over borrowed photographs of the kind of place it is set in.
- With a 3D brief, the render is the picture. The single effect may serve as the stage behind it, drawing on the same WebGL budget, but may not stand next to it as a rival focal picture.
- Every non-effect visual is a real interface capture or a real photograph. Never filter, print, dither or grade a photograph.

| | Tech | Product and service | Place |
|---|---|---|---|
| Lead picture | real UI, the device, the game world | photographs | photographs |
| The one effect | allowed | none | none |
| Card panel grounds | still, from the effect's family | photo or diagram on a flat panel | none |
| Moments | up to two (any tech pool) | one or two, photo or type | one or two, photo or type |
| Big scene | at most one | none | none |
| Diagram cards | up to two, may pulse | one, still | none |
| Timed loops | one | none | none |
| CSS grounds | 0–2 | flat tokens only | flat tokens only |

## Ground tokens

Every page, any kind, uses three ground tokens and nothing else:

- **Main:** white, or a light tint of the client's colour (OKLCH lightness 0.80–0.97, low chroma). It covers at least 55% of the page height (60% on software and product). Choose it by trade; the house default for warm trades is cream (`design-rules.md`).
- **Alt:** the same hue, 0.06–0.15 darker in lightness and never below 0.70. Used for panels and at most one band.
- **Dark:** lightness 0.05 or lower: near-black, never charcoal grey and never violet. One dark body section per page. A fully dark page is tech only.

- One to three ground colours run down the page, the same order at 390 as at 1440.
- Grounds change only at section edges, with no rule lines between sections. Never fake a ground with a coloured box inset in a white section.
- Light and evening grades may switch on load or on a click, never on scroll.
- Tech pages may add the lit ground and CSS grounds below.

```css
:root {
  --g-main: oklch(0.97 0.012 85);
  --g-alt:  oklch(from var(--g-main) calc(l - 0.08) c h);   /* same hue, one step down */
  --g-dark: oklch(0.04 0.01 85);
  --ink:    oklch(0.20 0.01 85);
}
```

Relative colour syntax: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_colors/Relative_colors

## Brand band

Product and place pages may set one band in the client's colour, once, in the second half of the page.

- On a place, keep the band's colour muted enough to sit with photographs. Text on it reaches 7:1, and its button inverts (ground-coloured fill, band-coloured text).
- A band is a section with real content (an offer, opening times, a booking prompt), never a strip of colour alone.

## Rhythm

- Tech pages run in bands: dark, lit, surface.
- Beyond the three tokens, at most two dealt grounds per page, and only one of them loud. Never put two strong grounds next to each other.
- A ground never changes a section's height. Where two grounds meet softly, fade over 120 px at most.

## Named grounds

Sixteen CSS grounds for tech pages, applied as section classes. Section grounds keep ink at 7:1 and muted text at 4.5:1, measured from the real pixels. Tints lean toward the accent, never violet. Each takes a few tuning properties (strength, angle, position).

| Family | Grounds | Use |
|---|---|---|
| Soft | mist (two-hue wash), halo (one light behind a centred line), ruled (fine grid as the page's own frame), dots (dot field in margins and corners, clear behind headings), arcs (rings rising from below, for a closing call), liquid (two slow blobs in neighbouring hues; the only moving CSS ground) | behind content |
| Hard | grain (tinted field with fine grain), dusk (one tone melting into the next), band (second tone lit from one corner), field (grainy one-family gradient), photo (calm photograph; text on its calm part, `photos.md`), horizon (a dark band whose lower edge glows along a curve, as a planet's limb does), deep (almost black, a cool pool of light at the top, a bright edge) | one strong band |
| Page and panel | paper (page ground with fine grain, never flat), topglow (light under the nav), stage (vivid grainy mesh one card sits on) | scoped to the page top or one panel |

- The **lit ground** (a page-wide light treatment) is tech only, behind UI and closing bands.
- Each ground's mood, roles, pairings and clashes are in `../../../../../data/craft/taste/patterns.csv`.

## Building gradients

On tech pages only, where a ground is drawn in code:

- Mix page tokens in OKLCH with chroma under 0.12, so the result stays in the palette.
- Build light first: 4–6 stops in one hue, with 4–10% grain to stop banding.
- Dither dark gradients. A plain two-stop linear gradient is never decoration. A seam between two tones is a hard stop, not a blur.
- Grain lives only inside the one effect: still, never animated, never over text.

```css
.g-sweep {
  background:
    radial-gradient(120% 80% at 50% 110%, oklch(from var(--accent) 0.62 0.10 h) 0%, transparent 60%),
    linear-gradient(in oklch to bottom,
      oklch(from var(--g-dark) 0.05 0.010 h) 0%, oklch(from var(--g-dark) 0.07 0.020 h) 35%,
      oklch(from var(--g-dark) 0.10 0.030 h) 65%, oklch(from var(--g-dark) 0.14 0.040 h) 100%);
}
```

## Recipes

Tech only; each counts as the page's one effect or one dealt ground.

- **Studio sweep:** a floor that curves up into the wall behind a product, lit from above.
- **Corner glow:** one soft light from a single corner of a dark band.
- **Painterly field:** a blurred landscape in broad soft dabs, sky over hills.
- **Spotlight floor:** a slanted beam ending in a pool, with the object standing in it.
- **Product-colour wash:** the ground cross-fades to a chosen colourway on click, never on scroll.
- **Woven tile or ordered dither:** once per page, never behind body text.
- **Grid marks:** registration crosses on one dark technical band.
- **Ledger rules:** hairline rows inside a section, never between sections.

## Budget

- **A tech page gets a single effect,** chosen from: a big scene; a single object; one WebGL part; or a live ground, placed in the hero or in the data-visual frame. A CSS ground with grain, dither or texture uses up that single slot. One card group may also carry quiet still grounds from the same family, held as pictures.
- **Beats:** the effect, a scene and moments make at most three beats. Two beats never share a section or sit in adjoining ones; a quiet section separates them, and the final third leading into the close stays quiet.
- **Moments beside it:** up to two section moments, plus at most one load, hover or click moment in the hero or data-visual frame, never in or beside a scene's section.
- **One pointer effect per page:** a hover or liquid moment, a pointer-lit button, spotlight cards or a turning object. Never a replaced cursor or magnetic button.
- **WebGL:** at most four live contexts on the page (`performance.md` § WebGL).
- A moving ground runs on a clock, not on scroll. If it moves for more than 5 s it has a pause button (WCAG 2.2.2), and it holds still under reduced motion.

## Effects catalogue

Each effect draws in page tokens: no fixed hue, never violet, and text over it reads 4.5:1. Each one is dealt once per slot per page, and pairs that clash never share a page.

| Group | Effects | Slot |
|---|---|---|
| Quiet (even field behind UI) | grain-gradient (soft drifting shapes under grain), painterly-landscape (out-of-focus hills and sky), gradient-mesh (colour islands over a folding surface), silk-folds (satin in one colour), fluted-glass (ribbed glass bending what is behind) | cards, hero |
| Focal (a subject in itself) | orb-sphere (one lit sphere with a rim), spotlight-cone (stage light landing as a pool), god-rays (shafts through haze), aurora-curtains (light curtains on a night sky; dark and colour pages), caustics (water light on a pool floor) | hero, alone |
| Pattern (never behind UI) | ruled-grounds, grid-pulse (signals along a hairline grid), contour-lines, dot-terrain (land as a point cloud), dotted-globe, ridgeline (stacked lines into peaks), halftone-screen, bayer-dither, ascii-shade (a sphere drawn in monospace characters), line-engraving, duotone-grade | hero, data-visual |
| Other | film-light-leak (a warm leak of light entering from a single side), prism-dispersion (a beam split into a spectrum; dark only), soft-light-bars (upright light bars beside an empty area), edge-glow (light running round a border) | hero, one border |

- **Named only, never dealt at random:** dotted-globe (only for real global reach), duotone-grade (never on a client photo), edge-glow, ridgeline.
- At most two effect ids per page outside moments. Each panel gets its own seed. No pattern or focal tile in cards.
- On the dark inverse ground, use an effect made for dark. If nothing fits a slot, drop the slot.
- Old names: gradient-mesh was called mesh-gradient and fluted-glass was iridescent-foil. Removed: riso-print, paper-texture, liquid-chrome, marble-warp, truchet-arcs, pixel-mosaic.

## Placement

- Only three places: the hero frame or hero layer; the page's single data-visual frame, placed below an `h2` (up to 1280 × 540 at 1440, 342 × 256 at 390); or a scene's own section. One data-visual frame per page.
- An effect in a hero frame needs the visual on the right of a 6/6 or 5/7 split; otherwise it goes to a section of its own. Used as a layer behind the hero, it keeps text to its quiet area, at 4.5:1 contrast.
- In a split frame, a product window sits at the corner, cut by the right and bottom edges; an optional second piece overlaps only the window's lower-right edge and is hidden from 1024 to 1279 px and on phones. Text and UI never share a half.
- Text sits only on an effect's quiet part; noise and fog never hold content.
- On tech pages, every ground that holds UI is marked so page, card, panel and UI never become four near-black layers.

## Effect parts

Effects inside one element (headline fill, button fill, rings, charts, feature-card panels) are in `effect-parts.md`.

## Motion and cost

- Effects react to the pointer or to time and hold once assembled. Ambient cycles last 4 s or longer; drifts move a few pixels a second; 2–10% of the pixels change in any 0.9 s.
- An effect either settles at rest or offers a pause button. A poster shows before it runs, and the poster stays when motion is reduced, on phones, and if WebGL fails. No sound on entry; pointer play is off on touch.
- Oversize the canvas by 20–25 px and clip the overflow. Render at a sample per CSS pixel (0.75 for big canvases); keep the whole page near 1.5 megapixels and cap device pixel ratio at 1.5. Run noise, particle and ray-marched work at 50% resolution and no more than 30 frames per second.
- Bake noise into a single texture once, then drift that texture.
- Use blend modes for a glint within an effect, never on type. Frosted or glassy panels are out; a menu overlay dims the page by a flat 40%.
- Freeze still effects: draw once near the screen, copy the result to an image, release the context (`cards-and-ui.md` § Grounds). Draw stills one after another, never leave a still's loop running, and never give a still a pause button. Screenshots must wait for pending stills.
- Off screen, or with the tab hidden, all of it pauses.
- Video is tech only, in the hero or data-visual frame (`later.md` § Video).

## Never

- On a page that is not tech: WebGL, gradients, grain, print looks or any effect.
- An effect where a photo or the product belongs. A print, dither or grade over a photograph.
- Cards holding a moving canvas or live effect, or cards that animate as you scroll.
- Captions that explain a picture. Blinking or random change. Violet or lavender.
- Copying another site's code, assets or signature device.
