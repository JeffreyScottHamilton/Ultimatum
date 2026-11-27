# Starter design tokens

Our own three-layer token set, used as the starting point when a site needs a design system and no brand values exist yet. The values (the `ink` neutral ramp, `moss` brand ramp, `ember` accent and status colours) are Ultimatum's own picks; replace them with the brand's.

| File | What it is |
|---|---|
| `starter.tokens.json` | the source: `primitive`, `semantic` (light and dark), `pairs` (contrast floors), `component` |
| `starter.tokens.css` | generated: plain CSS custom properties, `:root` and `.dark` |
| `starter.theme.css` | generated: the same tokens for Tailwind CSS v4 (`@theme`, `@theme inline`, `@custom-variant dark`) |

Edit the JSON only, then regenerate:

```
python3 tools/build_tokens.py           # write both CSS files
python3 tools/build_tokens.py --check   # exit 1 if they are stale or a contrast pair fails
python3 tools/build_tokens.py --in path/to/brand.tokens.json --out-dir path/to/styles
```

Check that pages, components and brand assets use the tokens (raw colours, fonts and sizes, unknown `var()` names, asset colours), and embed tokens into a one-file page:

```
python3 plugins/ultimatum/data/design-own/tokens/token_check.py scan --tokens path/to/tokens.css src/
python3 plugins/ultimatum/data/design-own/tokens/token_check.py colors --tokens path/to/tokens.css logo.svg
```

Every pair in `pairs` is checked in light and dark mode; the build refuses to write when one falls below its floor (4.5:1 for text, 3:1 for control borders and focus rings, WCAG 2.2 SC 1.4.3 and 1.4.11).

How the layers work and how to use the output: `skills/website/references/craft/ui-ux-pro-max/token-architecture.md` and `token-templates.md`. These files are not CSV tables, so the design search (`ult design`) does not read them.
