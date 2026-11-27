# Taste craft data

`patterns.csv` is a lookup table for the website craft files in `skills/website/references/craft/taste/`. Each row is one named pattern: a section ground, an effect, a recipe, a moment, a big scene, a hero layout or an app-frame pane pairing. The rules for using them are in the file each row names. Where the table and the file disagree, the file wins.

Written in our own words from the ideas in the MIT-licensed Taste skill (Leonxlnx/taste-skill, commit f6b7657). No source text or code is copied.

## Columns

| Column | Required | Holds |
|---|---|---|
| `name` | yes | the pattern's id, lower case with hyphens, unique within its kind |
| `kind` | yes | `ground`, `effect-quiet`, `effect-focal`, `effect-pattern`, `effect-other`, `recipe`, `moment`, `scene`, `hero` or `pane-pairing` |
| `use_for` | yes | the job it does on a page |
| `avoid_for` | yes | where it never goes, or what it clashes with |
| `build` | yes | a short note on how it is drawn, or what it needs from the brief |
| `reduced_motion` | yes | what shows under `prefers-reduced-motion: reduce` |
| `file` | yes | the craft file, relative to `references/craft/taste/`, that holds the full rules |

- Effects, recipes and scenes are for tech pages only (software, gaming, hardware). Grounds beyond the page's three tokens are tech only too.
- UTF-8, comma-separated, a header row, no empty cells. `tests/test_craft_taste.py` checks this.

## Presets

`presets/` holds what `ult design deal` (`scripts/ultlib/deal.py`) deals from. Both are original; no upstream palette, name or hex set is reused (`tests/test_taste_deal.py` compares them when the source checkout is present).

- `palettes.json`: one object per palette with `id`, `mode` (`light` or `dark`), `kinds`, `trades`, `moods`, colours `bg`, `surface`, `ink`, `muted`, `accent`, `accentInk`, `line` (#RRGGBB), and a one-line `note` on how to use it. Every palette must pass: ink 7:1 and muted 4.5:1 on `bg` and `surface`, `accentInk` 4.5:1 on `accent`, `accent` 3:1 on `bg`.
- `type.json`: one object per type set with `pairing` (a `Pairing` in `data/design-own/typography.csv`, which holds the fonts, weights and licence), `kinds`, display `tracking`, modular `scale` and heading `case`.
