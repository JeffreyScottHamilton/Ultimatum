# Anatomy craft data

`figures.csv` is a lookup table for the website craft files in `skills/website/references/craft/anatomy/`. Each row is one named technique: a part type, a texture, an effect, a motion or a check. The rules are in the file each row names. Where the table and the file disagree, the file wins.

`iso-slabs.html` is a small own example: isometric projection, three blocks, four tones, depth sort, and an operable slider. It was opened in Chromium with Playwright and checked for polygon counts, value text and page errors.

`figure_audit.py` counts the static audit table on a JSON scene (`audit.md`). `figure_draw.py` draws that scene to an accessible SVG at any camera and pose, and sweeps its turn, slide and hinge groups for collisions, crowding, depth-order cycles and torn pipes (`draw.md`). Both are standard-library Python with a `--self-check`. `examples/` holds a clean scene, a faulty one for the static audit, and `turning-scene.json`, whose lid and lead fail the motion audit on purpose.

Written in our own words from the ideas in the MIT-licensed Anatomy skill (commit 1482e84). No source text or code is copied.

## Columns

| Column | Required | Holds |
|---|---|---|
| `name` | yes | the technique id, lower case with hyphens, unique within its kind |
| `kind` | yes | `part`, `texture`, `effect`, `motion`, `check` or `format` |
| `use_for` | yes | the job it does in a figure |
| `avoid_for` | yes | where it does not belong |
| `build` | yes | a short note on how it is drawn or run |
| `reduced_motion` | yes | what shows under `prefers-reduced-motion: reduce` |
| `file` | yes | the craft file, relative to `references/craft/anatomy/`, with the full rules |

UTF-8, comma-separated, a header row, no empty cells. `tests/test_craft_anatomy.py` checks this.
