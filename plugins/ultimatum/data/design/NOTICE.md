# Design tables: third-party data

The CSV files in this folder are design data from
[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
(commit in `SOURCE.txt`), used under its MIT licence (`LICENSE`, Copyright (c) 2024
Next Level Builder). They are the one place in Ultimatum that ships upstream content
instead of original wording; the licence must stay with them.

Changes made on import (`tools/import_design_data.py`, which repeats them):

- Kept 12 tables and 12 stacks. Left out the full Google Fonts and Phosphor icon
  catalogues and the provenance ledger.
- Removed deprecated styles and the row-number, status and replacement columns.
- Added `Landing Pattern Match` to `products.csv`: the landing pattern in
  `landing.csv` that each product's suggested pattern refers to, or blank.
- Collapsed whitespace in every cell; renamed `Light Mode ✓` / `Dark Mode ✓`.

The search code that reads them (`scripts/ultlib/design.py`) is Ultimatum's own.
