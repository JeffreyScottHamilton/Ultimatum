# Fonts: choosing and loading type on a custom build

Read on a custom run only. A catalog theme already names its faces. See also `craft-type-colour.md` and `../taste/` for the type scale.

## Rule

One display face and one body face (or one family for both), plus at most one outlier with a single role (wordmark, headline figure, code). Choose the class the idea needs, shortlist two or three faces, then decide by setting the real headline in each. A name, reputation or subject link is not a reason. Free faces only unless the user confirmed a licence; prefer variable fonts. Ultimatum's own `fonts` guidance and the design data set can supply pairings; use whichever the project already loads.

## Reflex choices to avoid by default

Inter, Roboto, Open Sans, Lato, Poppins, Source Sans, Nunito, Montserrat, Raleway, Work Sans, DM Sans, Plus Jakarta Sans, the system stack, Arial or Helvetica as display or body; Merriweather, Lora or Georgia as the body serif; system mono. Allowed when the user asks or the project already uses it; then say so in the stamp.

Overused but good (justify each in the Picks block): Playfair Display, Cormorant, Fraunces, Instrument Serif, Space Grotesk, Bebas Neue, Unbounded as display; Geist, Instrument Sans, Mona Sans as body.

## Sources

- Google Fonts: free CDN, the default.
- Fontshare: free for commercial use. `<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,700&display=swap" rel="stylesheet">`
- A foundry (Klim, Pangram Pangram, Production Type, Lineto, Colophon) only with a confirmed licence.

## Alternatives by class

| Class | Faces |
|---|---|
| roman serif | EB Garamond, Cardo, Castoro, Piazzolla, Alegreya, Marcellus, Gambetta |
| high-contrast serif | Gloock, Libre Bodoni, Abril Fatface, Rozha One, Besley, Erode |
| slab | Arvo, Hepta Slab, Domine, Alfa Slab One (Bespoke Slab has old-style figures, so put numbers in the body face) |
| grotesk | Rethink Sans, Reddit Sans, Albert Sans, Clash Grotesk, Supreme |
| geometric | Lexend, League Spartan, Afacad, Satoshi, Excon |
| rounded | Inclusive Sans, Varela Round, Chubbo, Comico |
| condensed or heavy | Teko, Tektur, Antonio, Michroma, Clash Display, Khand |
| mono display | Space Mono, Fragment Mono, Red Hat Mono, Sometype Mono |
| pixel | Press Start 2P, VT323, Pixelify Sans, Tiny5 |
| handwritten | Shantell Sans, Caveat, Gochi Hand |

Body sans: Hanken Grotesk, IBM Plex Sans, Figtree, Onest, Golos Text, Karla, Public Sans, Archivo, Manrope, Switzer, General Sans. Body serif: Newsreader, Source Serif 4, Literata, Spectral, Crimson Pro. Mono: Geist Mono, JetBrains Mono, IBM Plex Mono, DM Mono, Fira Code.

## Wordmark

Give the wordmark its own face on tone-rich pages; folding it into the body family flattens the hierarchy.

```css
:root { --font-body: "Switzer", ui-sans-serif, system-ui, sans-serif; --font-outlier: "Gambetta", ui-serif, serif; }
.wordmark { font-family: var(--font-outlier); font-weight: 600; letter-spacing: -0.015em; }
```

Use one family only when the body voice is the brand (letters, manifestos); then use its display cut or heaviest weight. A local shop can carry its sign lettering as the wordmark, supplied as a logo file.

## Loading

- Load only used weights, one `<link>` per source with `display=swap`, preceded by `rel="preconnect"`.
- Self-hosted `@font-face`: `font-display: swap` plus a metric-matched fallback (`size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`) so the swap does not move the fold. Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face
- `font-synthesis: none`; load the italic if a heading uses it.
- A variable font loads once and gives every weight.
- Body text 16px or more, honouring user font size (WCAG 1.4.4).
