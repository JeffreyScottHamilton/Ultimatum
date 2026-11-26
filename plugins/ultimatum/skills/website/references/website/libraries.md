# Libraries for design directions

When you show three design directions, base each one on a different motion or component library. That way the user picks between real feels, not three versions of the same one. Licences change: each entry below records what was observed and when, and is **check before relying** on the library's own repository before anything is installed.

## The three libraries

### React Bits

- **What it is:** animated text, backgrounds, interactive effects and 3D pieces for React, copied into the project by its CLI or by hand. Source: https://github.com/DavidHDev/react-bits
- **Licence:** MIT plus the Commons Clause, per our component catalogue and the repository's LICENSE.md (observed 2026-11-25). Use the components inside the site being built, including for a paying client. Never sell, sublicense or redistribute the components themselves, for example as a template or component pack. The Pro tier is a separate paid product; do not use it without the user's licence and yes.
- **Check:** read the current LICENSE.md before use; tell the user about the Commons Clause in one line.

### Watermelon UI

- **What it is:** React components, blocks and templates shown at https://ui.watermelon.sh, with platform source at https://github.com/WatermelonCorp/watermelon-platform
- **Licence:** the repository's LICENSE file is MIT (observed 2026-11-25). The site's terms (https://ui.watermelon.sh/terms) say components may be used "in line with the relevant repository licenses and terms" and leave the user responsible for compliance. No page found says plainly that the MIT grant covers every component, block and template shown on the site.
- **Rule:** treat the licence as unclear. Use Watermelon UI only after telling the user this and getting their confirmation. Record the confirmation and the link to the terms in the project notes.

### Anime.js

- **What it is:** a JavaScript animation engine, framework-neutral: timelines, staggered tweens, SVG path and morph motion, scroll-linked animation. Source: https://github.com/juliangarnier/anime ; package `animejs`.
- **Licence:** MIT, per the repository's LICENSE.md (observed 2026-11-25).
- **Check:** confirm the major version's API in its own docs; examples from older versions may not run.

## Pairing directions with libraries

| Direction | Library | Two or three effects | Feels like |
|---|---|---|---|
| Calm and editorial | Anime.js | Staggered fade-up of headings and paragraphs on scroll; a slow SVG line drawing under the hero; gentle number count-up in a proof strip | A well-set magazine; motion only confirms reading order |
| Bold and kinetic | React Bits | Split-letter animated headline; an animated gradient or particle background behind the hero only; a scroll-velocity text band | A launch page with energy; one loud area, quiet elsewhere |
| Playful and interactive | Watermelon UI (after the user confirms its licence), otherwise a permissive alternative from `ult components` | Hover-reactive cards; an animated tab or toggle for plans; a small interactive demo block | A product you want to poke at |

These are examples. Swap a pairing when the brand or the stack calls for it; keep three different libraries across the three directions.

## Fallback

When a library does not fit the stack, its licence is unclear and the user has not confirmed, or a direction needs something none of the three offers:

```
ult components "<need>"
```

For example `ult components "animated number counter" --stack react`. Prefer entries marked permissive (MIT, Apache-2.0, ISC, BSD) and maintained. A restricted entry needs the same one-line explanation and the user's yes as React Bits.

## Installing

- Install into the user's project with the project's own package manager (`npm`, `pnpm`, `yarn` or `bun`; use the one whose lockfile is present). For copy-in libraries, follow their CLI or copy the single component's source into the project's components folder, with the licence header kept.
- Never copy library code into the plugin or into shared Ultimatum files.
- Record each library, version, licence and source link in the project notes so the compliance reviewer can check it.
- Do not run remote install scripts piped into a shell; use the package manager.

## Limits on every effect

- **Reduced motion:** honour `prefers-reduced-motion`. With it set, show the end state with no movement, or a simple fade. Test it.
- **No layout shift:** reserve space for animated elements; animate `transform` and `opacity`, not width, height or top. Check the page's layout-shift score in the browser check.
- **Content never hidden:** text and buttons must be readable and usable if the script fails, loads late or is blocked. Do not start content at zero opacity without a fallback.
- **Performance:** one heavy effect (canvas, WebGL, particles) per page at most, paused when off screen. Test on a mid-range phone.
- **Purpose:** each effect points the eye to something that matters or confirms an action. Remove decoration that competes with the main call to action.
- **Accessibility:** keyboard focus stays visible during animations; nothing flashes rapidly.
