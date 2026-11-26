# Hallmark craft data

Lookup tables for the website craft files in `skills/website/references/craft/hallmark/`. Each CSV is UTF-8, comma-separated, has a header row and no empty cells. The rules are in the file each table points to; where table and file disagree, the file wins.

Written in our own words from the ideas in the MIT-licensed Hallmark skill (nutlope/hallmark, commit 04977e1). No source text or code is copied.

## Files and columns

| File | Rows | Columns |
|---|---|---|
| `gates.csv` | one per numbered gate | `gate` (id), `tier` (Floor, Reflex, Finish or Ledger), `check` (class: M static, R render, J judged, or a mix such as M/R or R/J), `group` (topic), `the_tell` (what to look for), `the_fix` (what to do) |
| `compositions.csv` | one per section composition | `name`, `columns`, `size`, `use_for`, `rule` |
| `hero-postures.csv` | one per hero posture | `name`, `height`, `content`, `use_for`, `rule` |
| `page-shapes.csv` | one per page shape | `id`, `name`, `idea`, `heading`, `body`, `divider`, `button`, `image`, `reveal`, `reach_for`, `avoid_for`, `built_from` |
| `themes.csv` | one per catalog theme | `slug`, `name`, `genre`, `posture`, `paper_band`, `paper_lightness`, `paper_hue`, `display_class`, `display_face`, `accent_band`, `accent_hue`, `photo_treatment`, `routes_from` (five routing words joined by ` | `) |

Palette numbers in `themes.csv` are OKLCH anchors: paper lightness in percent and hue in degrees. Search by genre, posture or routing word, then write the theme body by `themes.md`.
