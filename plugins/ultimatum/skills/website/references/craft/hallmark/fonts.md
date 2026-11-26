# Fonts: choosing and loading type on a custom build

Read on a custom run only. A catalog theme already names its faces. See also `craft-type-colour.md` and `../taste/` for the type scale.

## Rule

Choose a display face and a body face, or let one family do both; an extra outlier face is allowed if it has exactly one job (wordmark, headline figure or code). Decide the style class first, shortlist 2–3 faces, and test each with the real headline. Fame, name or topical association never settles it. Free faces only unless the user confirmed a licence; prefer variable fonts. Ultimatum's own `fonts` guidance and the design data set can supply pairings; use whichever the project already loads.

## Reflex choices to avoid by default

Inter and Roboto lead the list, followed by Poppins, Montserrat, Lato, Open Sans, Raleway, Nunito, Work Sans, Source Sans, DM Sans and Plus Jakarta Sans. Add the system font stack, Arial and Helvetica when used for display or body text, Georgia, Lora and Merriweather as the body serif, and the default monospace. They stay available if the user requests one or the project already loads it; note that in the stamp.

Overused but good (justify each in the Picks block): Playfair Display, Cormorant, Fraunces, Instrument Serif, Space Grotesk, Bebas Neue, Unbounded as display; Geist, Instrument Sans, Mona Sans as body.

## Sources

- Google Fonts: free CDN, the default.
- Fontshare: free for commercial use, loaded with a stylesheet link such as `<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=general-sans@500&display=swap">`.
- A foundry (Klim, Pangram Pangram, Production Type, Lineto, Colophon) only with a confirmed licence.

## Alternatives by class

| Class | Faces |
|---|---|
| roman serif | Gambetta, Marcellus, Alegreya, Piazzolla, Castoro, Cardo, EB Garamond |
| high-contrast serif | Erode, Besley, Rozha One, Abril Fatface, Libre Bodoni, Gloock |
| slab | Arvo, Hepta Slab, Domine, Alfa Slab One (Bespoke Slab has old-style figures, so put numbers in the body face) |
| grotesk | Rethink Sans, Reddit Sans, Albert Sans, Clash Grotesk, Supreme |
| geometric | Lexend, League Spartan, Afacad, Satoshi, Excon |
| rounded | Inclusive Sans, Varela Round, Chubbo, Comico |
| condensed or heavy | Teko, Tektur, Antonio, Michroma, Clash Display, Khand |
| mono display | Sometype Mono, Red Hat Mono, Fragment Mono, Space Mono |
| pixel | Tiny5, Pixelify Sans, VT323, Press Start 2P |
| handwritten | Shantell Sans, Caveat, Gochi Hand |

Body sans options: General Sans, Switzer, Manrope, Archivo, Public Sans, Karla, Golos Text, Onest, Figtree, IBM Plex Sans, Hanken Grotesk. Body serifs: Crimson Pro, Spectral, Literata, Source Serif 4, Newsreader. Monospace: Fira Code, DM Mono, IBM Plex Mono, JetBrains Mono, Geist Mono.

## Wordmark

On pages with a strong tone, set the wordmark in its own face; merging it into the body family flattens the hierarchy.

```css
:root {
  --font-body: "Switzer", system-ui, sans-serif;
  --font-mark: "Gambetta", Georgia, serif;
}
.wordmark { font-family: var(--font-mark); letter-spacing: -0.015em; font-weight: 600; }
```

Stay with one family only when the reading voice is the brand, as in letters and manifestos, and then take its display cut or heaviest weight. A local shop can carry its sign lettering as the wordmark, supplied as a logo file.

## Loading

- Load only used weights, one `<link>` per source with `display=swap`, preceded by `rel="preconnect"`.
- For self-hosted `@font-face`, use `font-display: swap` with a fallback tuned via `size-adjust` and the ascent, descent and line-gap overrides, so swapping does not shift the fold. Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face
- Set `font-synthesis: none` and load a real italic wherever a heading needs one.
- A variable font loads once and gives every weight.
- Body text 16px or more, honouring user font size (WCAG 1.4.4).
