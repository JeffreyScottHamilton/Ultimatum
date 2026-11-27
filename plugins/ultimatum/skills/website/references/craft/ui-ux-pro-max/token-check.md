# Token check: finding values that skip the tokens

Read when a design system exists and you need proof that pages, components, single-file HTML pieces or brand assets actually use it: after moving a flat stylesheet to tokens, before shipping a page built from tokens, or when a logo or banner should hold only brand colours.

`../../../../../data/design-own/tokens/token_check.py` is standard-library Python with no network. It reads the custom properties of one or more token stylesheets (the CSS `tools/build_tokens.py` writes, or any file of `--name: value` declarations) and compares everything else against them.

```bash
python3 token_check.py scan --tokens styles/tokens.css src/
python3 token_check.py embed --tokens styles/tokens.css card.html --out card.html --used
python3 token_check.py colors --tokens styles/tokens.css brand/logo.svg brand/banner.png
python3 token_check.py rules
```

## scan

Reads `.css`, `.scss` and `.less` files whole; `<style>` blocks, `style` attributes and colour attributes (`fill`, `stroke`, `stop-color`) in `.html`, `.svg`, `.vue`, `.svelte` and `.astro` files; and style objects in `.jsx`, `.tsx`, `.js` and `.ts` files (camelCase names are read as CSS names). Comments and `url(...)` contents are ignored. Folders are walked, skipping `node_modules`, `dist`, `build`, `vendor` and hidden folders, and the token files themselves.

| Rule | Level | What it catches |
|---|---|---|
| `raw-color` | error | a hex, `rgb()`, `hsl()`, `oklch()` or other colour written by hand where a token should be used |
| `unknown-var` | error | `var(--name)` where neither the token files nor the scanned files define `--name`, usually a typo or a removed token |
| `named-color` | warn | a colour word such as `white` or `red` in a colour property |
| `raw-font` | warn | a `font-family` that names fonts instead of using a font token |
| `off-scale` | warn | a `px`, `rem` or `em` size in a spacing, radius, type size, line height or letter spacing property that no token holds |
| `off-palette` | error | `colors` only: an asset colour too far from every token colour |

When a raw colour equals a token, the fix names it, roles first: `#2f6b4f` → `use var(--primary)`, not the primitive behind it (`token-architecture.md` § Layer 2: semantic roles). When nothing matches, the fix names the nearest token so you can decide whether the colour belongs in the system or is a mistake.

`off-scale` runs only when the token files hold sizes. A size is on the scale when a token's whole value is that size (`--text-sm: 0.875rem`), counting `1rem` as `16px`; for padding, margin and gap, any whole multiple of a `--spacing` token also counts, which is how Tailwind v4 builds its spacing (`token-templates.md`). Sizes inside longer values such as shadows are not steps. `0`, `1px` and `-1px` pass, since hairlines and resets are not scale steps. Values inside `var(...)`, including fallbacks, are not counted. Exit 0 means no errors; `--strict` fails on warnings too, which suits CI once a migration is finished. `--only raw-color,unknown-var` limits the rules; `--json` gives counts and findings for a script.

A line with `token-check: ignore` in a comment is skipped; a file holding `token-check: ignore-file` (a vendored widget, a colour picker's swatches) is skipped whole. Each ignore is a decision someone should be able to explain; review them with a search when the system changes.

## embed

Puts the token stylesheet inside an HTML page as `<style data-tokens="tokens.css">`, right after `<head>`. Use it for pieces that must stand alone: an email-safe preview, a choice board (`../../../../work/references/craft/superpowers/choice-board.md`), a downloaded report, a page sent as one file. Running it again replaces the block rather than adding a second one, so it is safe in a build step.

`--used` keeps only the properties the page reads, and the ones those point at, so `--primary` brings `--color-moss-600` with it and the other ninety tokens stay out. It needs a flat stylesheet; a token file with nested blocks such as `@media (...) { :root { ... } }` is refused under `--used` (embed it whole instead). Dark-mode blocks such as `.dark { ... }` are kept with the same pruning.

For a site with more than one page, link the generated stylesheet instead; embedding duplicates it in every page.

## colors

Lists the colours an SVG, HTML or CSS file writes, or the colours a PNG's pixels use, with the nearest token colour and the distance in OKLab (times 100). About 2 is the smallest difference most people notice side by side, so the default `--max-distance 2` flags a colour that a viewer could tell apart from the nearest brand colour. Raise it a little for photographs, where every pixel varies; lower it for flat logos.

- PNG files must be 8-bit and not interlaced (the common export); 16-bit, interlaced and files over 2 megapixels are refused with a message. Mostly transparent pixels are skipped.
- Anti-aliased edges make many small in-between colours. `--min-share 0.005` (the default) ignores colours under half a percent of the visible pixels; raise it for a busy image.
- JPEG, WebP and GIF are not read. Export a PNG of the asset, or check the source SVG.

Use it in the brand review (`brand-review.md`): a logo, icon set or banner whose colours all land near a token passes this part of the gate; one that does not either needs fixing or shows the palette is missing a colour the brand really uses.

## Where it fits

1. Build the tokens (`token-templates.md`).
2. Swap raw values for roles a component at a time (`token-architecture.md` § Moving a flat stylesheet to layers), running `scan --only raw-color,unknown-var` after each pass.
3. When the counts reach zero, add `scan --strict` to CI so new raw values fail the build.
4. Check brand assets with `colors` before they ship, and embed tokens into any page that travels alone.

It does not judge whether a token is the right one for a place (that is a review), check contrast (the generator does that for its pairs), or read class-based styling such as Tailwind utilities; class lists are not parsed, so arbitrary values like `bg-[#2f6b4f]` can slip by. For those, search for `-[#` in the templates.
