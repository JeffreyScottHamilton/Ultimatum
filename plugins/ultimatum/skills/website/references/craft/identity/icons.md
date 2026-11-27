# Interface icons: choosing a set, drawing your own, and checking them

Read when a product needs icons beyond what one library gives, or when an icon set is being drawn for a brand. For using a library icon on a page (sizes, colour, alignment), `../hallmark/imagery.md` § Icons, logos, video, 3D is the rule; this file is about the set itself.

## 1. Use a library first

Drawing icons is slow and easy to get wrong. Start from one open library that matches the brand's line and corner style, and draw only the few icons it lacks, in its style.

| Library | Style | Licence |
|---|---|---|
| Lucide | 24 grid, 2 px stroke, round caps and joins | ISC |
| Phosphor | 256 grid, six weights from thin to fill, plus duotone | MIT |
| Heroicons | 24 outline and solid, 20 and 16 solid | MIT |
| Tabler | 24 grid, 2 px stroke, adjustable | MIT |
| Material Symbols | variable font: weight, fill, grade, optical size | Apache-2.0 |
| Remix Icon | 24 grid, line and fill pairs | Apache-2.0 (check the current licence page) |

Check the licence file in the release you use and keep it with the icons (`../../shared/licenses.md`). One library per product; mixing two sets is the most visible slip.

## 2. When drawing icons, set the rules first

Write these down before drawing the first icon, and give them to anyone who adds one later:

- **Grid:** a square canvas, usually 24×24, with 2 px of padding on each side, so the live area is 20×20.
- **Keyline shapes:** a circle about 20 across, a square about 18, a portrait and a landscape rectangle. Icons fill these shapes so that a round icon and a square icon look the same size; a circle drawn to the full square looks too big.
- **Stroke:** one width for the set (1.5 or 2 at 24 px), centred on the path, never scaled when the icon is resized.
- **Caps and joins:** round or square, the same throughout.
- **Corners:** one outer corner radius (often 2) and inner corners that follow it.
- **Angles:** prefer 0, 45 and 90 degrees; other angles only where the object needs them.
- **Fill or line:** decide whether the set is outline, filled, or both as pairs. Filled versions mark a selected or active state.
- **Detail:** the fewest strokes that still name the object. If it needs a label to be understood, it needs a label in the interface too.

## 3. Drawing well

- Draw on whole or half pixels so strokes land on the pixel grid at 1× and stay sharp.
- Leave at least one stroke width of space between separate parts, or they merge at small sizes.
- Balance by eye, not by the numbers: shapes with points (triangles, arrows) need to be a little bigger to look the same size as circles and squares.
- Draw a metaphor people already know (a magnifier for search, a gear for settings). A clever new metaphor needs a label.
- Arrows and objects that point face the same way across the set, and mirror correctly for right-to-left languages where direction carries meaning (back, forward, reply), but not where it does not (a clock, a checkmark, a media play button).
- Test at the real sizes (16, 20, 24) and at 1× and 2× before calling one done, on light and dark backgrounds.

## 4. Export as clean SVG

- `viewBox="0 0 24 24"` and no fixed `width` and `height`, or `width` and `height` equal to the viewBox so they can be overridden in CSS.
- `stroke="currentColor"` (or `fill="currentColor"` for filled icons) so the icon takes the text colour; no hard-coded colours except in deliberate multicolour icons.
- `fill="none"` on outline icons, `stroke-width`, `stroke-linecap` and `stroke-linejoin` set once on the root `<svg>`.
- Outline the text, flatten the transforms, remove hidden layers, editor metadata, IDs and embedded raster images. An SVG optimiser does most of this; check that it did not round coordinates so far that shapes move.
- One icon per file, named for what it shows (`calendar.svg`), not where it is used (`header-icon.svg`).
- Decorative icons get `aria-hidden="true"` where they are used; icons that stand alone as a button need an accessible name on the button.

## 5. Check the set

Run the icon checker over the folder:

```bash
python3 ../../../../../data/craft/identity/icon_check.py icons/
```

It reads local SVG files only. Each line is `file rule [severity]: what to fix`; exit 1 means findings, 0 none, 2 a bad argument or no SVG files. `--rules` lists the rules, `--only` narrows them, `--json` gives machine-readable output, and `--size N` sets the expected canvas (default 24).

| Rule | What it catches |
|---|---|
| `no-viewbox` | an SVG without a viewBox |
| `not-square` | a viewBox that is not square |
| `wrong-size` | a viewBox of another size than the set's |
| `fixed-colour` | a hard-coded fill or stroke colour instead of `currentColor` or `none` |
| `mixed-stroke` | a stroke width that differs from the rest of the set |
| `mixed-caps` | a line cap or join that differs from the rest of the set |
| `has-text` | live text inside the icon |
| `has-raster` | an embedded image |
| `has-transform` | a transform left on a shape |
| `editor-junk` | editor metadata, comments or namespaces left in the file |
| `out-of-bounds` | path coordinates outside the canvas |
| `too-complex` | very long path data for an interface icon |

What it cannot see: whether the icons look the same size, whether the metaphor is clear, or whether parts merge at 16 px. Look at the whole set side by side at 16 and 24 px for that.
