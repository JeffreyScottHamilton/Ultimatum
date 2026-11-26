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
