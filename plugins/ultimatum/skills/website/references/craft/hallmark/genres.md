# Genres: four registers that set the defaults

Read at the start of a build, after the ask, to name the register in the stamp. The genre leans the theme choice and sets what is allowed or refused. If nothing signals another, use editorial. For local business sites, pick by feel (a family bakery is editorial or playful; a clinic or law firm is modern-minimal), never by trade alone.

| | Editorial (default) | Modern-minimal | Atmospheric | Playful |
|---|---|---|---|---|
| For | portfolios, manifestos, studios, magazine pieces, podcasts, brand stories | SaaS, API, platform, B2B, dashboards, billing | AI creative tools, music, video, nocturnal or cinematic prompts | fun, friendly, kids, games, community |
| Accent | one hue, limited to what the posture allows | ink, or one hue on focus and one control | one hue in the canvas, focus, small tags; not display text | soft low chroma; full-palette lifts chroma to 0.24 across named roles |
| Layout | asymmetric, hairlines, type large | two-column hero with a big slot, thin visible borders | canvas first, type on it; centred hero allowed when type is the visual | rounded surfaces (12px cards, 8px inputs), soft offset shadows, tinted bands |
| Motion | quiet, one entrance | minimal, reveals off | fade only | pointer-responsive, one entrance, spring only on declared moments |
| Copy | specific, hand-set, verbs over adjectives | declarative and technical; say "built for" only when the audience is concrete | direct, slightly poetic | warm, direct, no quirk for its own sake |

## Allowed

- **Editorial:** hairlines, fleurons, drop caps, double rules, italic in body copy, 2:5 or 3:7 columns, captioned photos, edge-aligned headlines, one `<mark>` band.
- **Modern-minimal:** pill controls (ink-filled primary beside outlined secondary), pure white paper and zero-chroma neutrals, a subtle-border surface at 8px radius, large tight display.
- **Atmospheric:** up to two fixed radial blooms, each covering a fifth to a third of the canvas and still, a blurred nav pill (the one glass licence), a centred hero, accent-filled pills, cards raised by lightness steps, display to 6rem.
- **Playful:** soft offset shadows, hover lifts, a hard offset shadow if the theme states it, one character moment, emoji inside a sentence only.

## Refused

- **Editorial:** gradient pills, a centred-everything hero (unless the theme is built around a centred handbill), glass, pure black or white.
- **Modern-minimal:** italic serif body, hairlines everywhere, asymmetric prose columns, ornament, overshoot easing, gradient text, glass, a terminal look as decoration for a non-developer product, a monospace label voice.
- **Atmospheric:** coloured glow shadows, a spotlight behind the hero, mesh gradients, light sections in a dark build, a third hue, glass cards, gradient text.
- **Playful:** saturated pinks and violets with no stated posture, comic faces, bounce outside declared moments, glass, gradient text, status dots and sticker pills on every element.

## Chrome that fits (affinities, not rules)

Editorial: masthead, quiet edge bar, colophon. Modern-minimal: dense balanced bar, floating pill, mega-menu, search pill. Atmospheric: floating blur pill, command palette, statement footer. Playful: heavy slab bar, banner, marquee footer. The stamp names the choice rather than arriving by reflex.

Stamp: `genre: <name>`. These sit inside Ultimatum's own rules: no glow, gradient text or fake stats by default (`../../website/design-rules.md` section 2); an atmospheric carve-out is the theme's declared material, not a default.
