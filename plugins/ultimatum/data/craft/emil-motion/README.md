# Emil motion craft data

Lookup tables for the website craft files in `skills/website/references/craft/emil-motion/`. Each row is a short pointer; the rules and reasons live in the file a row names. Where a table and its file disagree, the file wins. On marketing pages the house tokens in `craft/taste/motion.md` win over the times here.

Written in our own words from the ideas in the MIT-licensed emilkowalski/skills (commit 715c180). No source text or code is copied.

## Files and columns

| File | Columns |
|---|---|
| `timing.csv` | `element`, `enter_ms`, `exit_ms`, `curve`, `note`, `file` |
| `symptoms.csv` | `area` (performance, mobile, feel), `symptom`, `likely_cause`, `first_fix`, `file` |
| `vocabulary.csv` | `term`, `group`, `meaning`, `not_to_confuse_with`, `hint` |
| `worst-case.csv` | `kind`, `value`, `breaks`, `fix_hint` |
| `libraries.csv` | `task`, `library`, `url` (https), `use_when`, `skip_when` |

- `file` columns are relative to `references/craft/emil-motion/`.
- UTF-8, comma-separated, a header row, no empty cells (a missing value is written `none` or `none noted`). `tests/test_craft_emil_motion.py` checks this.
- `worst-case.csv` values use no real people, mailboxes or sites; emails use example domains.
- Times are starting points for product UI. Library and doc URLs could not be fetched from the build session (the egress proxy refused every host), so they are unchecked; open each once before relying on it.
