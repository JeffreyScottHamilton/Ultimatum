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

## styles.csv

Built by `tools/build_styles.py` from the rows in `tools/style_rows/*.json`, written by hand in our own words. The build checks every row (palette has hex colours, tokens are valid custom properties, CSS braces balance, at least two slop habits and three checks) and rejects any row that recommends a habit the anti-generic lint bans, except inside Slop Habits. Style names match UI UX Pro Max's so the product table resolves.

| Column | Meaning |
|---|---|
| Style, Aliases | the name and other names people search with |
| Type | General, Dashboard, Mobile, Design System or Local |
| Keywords, Looks Like | search words and a short visual description |
| Use When, Avoid When | who it suits, and who it does not and why |
| Palette, Type Approach, Layout, Motion | starting colours, fonts, structure, and movement with a reduced-motion fallback |
| Slop Habits | the generic moves this style tempts people into |
| Accessibility, Performance | real risks with WCAG 2.2 criteria, and the cost (low, medium, high) |
| Mode, Effort | light-first, dark-first or both; how hard it is to build well |
| Tokens, CSS Starter, Checklist | CSS custom properties, a few lines of signature CSS, checks before shipping |

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

## products.csv
Built by `tools/build_products.py` from `tools/product_rows/*.json` (a family's shared answers plus one row per type). The build fails unless every type in `product-types.txt` and in their table has a row, every style exists in `styles.csv` and every landing pattern in `landing.csv`.

| Column | Meaning |
|---|---|
| Product Type, Keywords | the business or product and the words people search with |
| Main Action | the one thing a visitor should do (call, book, quote, sign up, buy) |
| Primary Style Recommendation | one or two style names joined by ` + `, all in `styles.csv` |
| Landing Page Pattern, Landing Pattern Match | the page pattern; the exact `landing.csv` Pattern Name that `ult design system` joins on |
| Secondary Styles | other fitting styles, comma separated |
| Trust Signals | what proves the business is real |
| Dashboard Style (if applicable) | the dashboard style, or `none needed` |
| Color Palette Focus, Booking/Quote | colour direction; how bookings or quotes arrive |
| Key Considerations | what to watch for |

## landing.csv
Built by `tools/build_landing.py` from `tools/landing_rows/*.json`.

| Column | Meaning |
|---|---|
| Pattern Name, Aliases, Keywords | name and search words |
| Kind | Local, App or Marketing |
| Section Order, Primary CTA Placement | sections joined by ` > `; where the main button goes |
| Use When, Avoid When | fit and misfit |
| Mobile, Accessibility | phone behaviour; WCAG 2.2 criteria |
| Color Strategy, Recommended Effects | colour and motion limits |
| Conversion Optimization, Slop Habits | what lifts results; generic moves to avoid |
