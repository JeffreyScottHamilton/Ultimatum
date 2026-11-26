# Impeccable data

Our own example files for `skills/website/references/craft/impeccable/`. Nothing here is copied from the source, and none of the source's code was run.

- `examples/harden-demo.html`: a page that shows long names truncating inside a flex row, logical borders in left-to-right and right-to-left text, a mirrored arrow, `Intl` number and plural formatting, a popover escaping an `overflow: hidden` card, and a slider that ends cleanly on `pointercancel`.
- `examples/check-harden.js`: a Playwright script that loads the page at 390 by 844 and makes 15 checks. Run it with `NODE_PATH=$(npm root -g) node check-harden.js` from this folder; it prints the count and exits 0 when all pass.
