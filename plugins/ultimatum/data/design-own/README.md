# Ultimatum's own design tables

Written from primary sources and our own lessons, never from third-party rows. A table here replaces the one of the same name in `../design/`; `ult design domains` marks ours with "(ours)".

## colors.csv

Built by `tools/build_palettes.py` from `product-types.txt` (one business type per line). Do not edit the CSV by hand: change the families in the script and rebuild; `--check` fails if the two differ.

| Column | Meaning |
|---|---|
| Product Type | business or product type, matching `products.csv` where one exists |
| Family | the colour family the type belongs to (local trades, health, food, ...) |
| Mode | `light` or `dark` default page |
| Background and Foreground | the page and its body text |
| Card, Card Foreground | raised panels and their text |
| Border, Ring | hairlines; the focus outline |
| Muted, Muted Foreground | quiet panels and secondary text |
| Primary, Accent, Secondary, Destructive | fills, each with an `On ...` text colour for labels on it |
| Notes | why this family's colours suit the business |
| Avoid | the colour habits that make this kind of site look generic or hard to read |

Contrast (WCAG 2.2): every text pair is at least 4.5:1 (SC 1.4.3) and the ring at least 3:1 on the page (SC 1.4.11). `tests/test_design_own.py` re-checks every row. Accent is a fill colour, not a text colour on the page.

## typography.csv

Built by `tools/build_typography.py`. The pairings, moods, uses and notes are ours, written in the script. Facts about each family (designer, licence, category, weights, scripts) come from Google Fonts' own `METADATA.pb` files in github.com/google/fonts, cached in `fonts-meta.json` (`--fetch` refreshes it; the build and tests never use the network). The build fails if a pairing asks for a weight the family does not have.

| Column | Meaning |
|---|---|
| Pairing | our name for the pair |
| Mood, Best For | the tone it sets and the businesses or products it suits |
| Heading Font, Body Font | Google Fonts family names |
| Heading Weights, Body Weights | the only weights to load |
| Kind | the two families' categories, heading first |
| Licence | the families' licences (all open: OFL, Apache or Ubuntu) |
| Extra Scripts | non-Latin scripts both families cover (`-` for Latin only) |
| Heading Stack, Body Stack | CSS `font-family` with a system fallback of the same kind |
| Google Fonts URL | a CSS2 link that loads only the listed weights, with `display=swap` |
| Notes | how to use the pair well, and where it breaks |

Rules the tests hold it to: no generic face (Inter, Roboto, Arial, Open Sans) as the display face, no monospace body text, and no body face in more than four pairings. Fonts are linked, never bundled.
