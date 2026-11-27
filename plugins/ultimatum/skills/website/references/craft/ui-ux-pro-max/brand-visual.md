# Brand visual identity: colour, type, logo use, imagery

Read at step 2 of `brand-flow.md` once the voice is set, or when an existing palette, type spec or logo rule needs writing down. For a real company's actual values, first read them by `../hallmark/brand-truth.md`. For choosing a palette or type pair from scratch, start from `../../../../../data/design-own/colors.csv` and `../../../../../data/design-own/typography.csv`, and the house lint in `../../website/design-rules.md` § 2. Anti-generic lint.

## Colour: roles before values

A brand palette is a short list of jobs, each filled by one colour family. Name the job first; the hex comes second.

| Role | Count | Job |
|---|---|---|
| brand | 1, at most 2 | the colour people remember; logo, main action, key highlights |
| support | 0-2 | variety for illustration, charts, section grounds; never competes with the main action |
| neutral | 1 family, 9-11 steps | text, surfaces, borders, dividers; most of every screen |
| status | 4 (danger, warning, success, info) | meaning only; never decoration |

### Build each family as a ramp

From each chosen colour, build a ramp of steps (50 lightest to 950 darkest is the common naming). Keep the hue roughly steady and move lightness in even perceived steps; OKLCH makes this easier than HSL because its lightness tracks what the eye sees. Mark which step is the **anchor** (the exact brand value from the logo) so nobody "corrects" it.

Rules of thumb that hold up in practice:

- text on white needs roughly step 600 or darker of a mid-saturation hue; check, do not assume;
- yellow and light green fail as text on white at almost every step that still looks yellow; use them as grounds with dark text instead;
- a brand colour that fails as a button background with white text gets dark text, or a darker step for buttons only, recorded in the guide.

### How much of each

Neutrals carry most of the area; the brand colour is a spice. A useful starting split is about 70 / 20 / 10 (neutral grounds and text / support and tinted surfaces / brand accents and actions). It is a starting point to break with intent, not a rule; a festival site may run the brand colour as the ground.

### Write it down three ways

For each colour the guide gives: the role, the name, hex, an OKLCH or RGB value for screens, CMYK and a spot colour reference only if print exists, and the approved text colour on it with its contrast ratio. Then the same values appear as primitive tokens (`token-architecture.md`), and nowhere else.

### Contrast floors (WCAG 2.2)

| Use | Floor | Criterion |
|---|---|---|
| body text and small labels | 4.5:1 | 1.4.3 Contrast (Minimum), AA |
| large text (24 px regular, or about 18.7 px bold, and up) | 3:1 | 1.4.3 |
| icons, borders that show a control, focus rings, chart marks | 3:1 against what is next to them | 1.4.11 Non-text Contrast, AA |

Source: https://www.w3.org/TR/WCAG22/. The token generator (`tools/build_tokens.py`) computes the ratio for every listed pair; `../../../../../data/design-own/colors.csv` already carries checked pairs for 160+ product types. Colour is never the only signal: errors and statuses also get a word or an icon (1.4.1 Use of Color).

### Do and avoid

- Do keep one brand colour for the main action across the whole site.
- Do derive hover, pressed and focus colours from the ramp, not by eye.
- Avoid tints and opacities of one colour as a palette; pick steps from the ramp.
- Avoid using a status colour for branding (a red brand needs a separate danger red that reads differently, or an icon on every error).

## Type: a short, loadable spec

### Families

At most two families, three if one is a monospace for code or data. For each: the role (display, text, mono), the weights actually used, the fallback stack, and the licence and source. Link to the font host or self-host from the licensed files; never paste a font file into the repo without its licence beside it. Picking and loading are covered in `../hallmark/fonts.md`; avoid the reflex choices it lists unless the brand asks.

Write fallback stacks that resemble the brand face in width, so a slow load does not reflow the page: a humanist sans falls back to `system-ui, "Segoe UI", Roboto, sans-serif`; a transitional serif to `Georgia, "Times New Roman", serif`.

### Scale

Pick a base (16 px for body on screens, never smaller for running text) and a ratio. Small ratios (1.125-1.2) suit dense apps; larger ones (1.25-1.333) suit marketing pages with few levels. Write the scale as a table with the token name, size, line height, weight and use:

| Token | Size | Line height | Weight | Use |
|---|---|---|---|---|
| `--text-sm` | 14 px | 1.45 | 400 | captions, table cells |
| `--text-base` | 16 px | 1.55 | 400 | body |
| `--text-lg` | 20 px | 1.4 | 500 | lead paragraph |
| `--text-2xl` | 31 px | 1.2 | 600 | section heading |
| `--text-4xl` | 49 px | 1.05 | 650 | page title |

(Here a 1.25 ratio, rounded.) Big type wants tighter line height and, for display sizes only, slightly tighter tracking; body text keeps the default. For fluid headings use `clamp()` between a phone size and a desktop size so they never jump.

### Settings that matter

- line length 45-75 characters for body (`max-width: 65ch` is a good default);
- paragraph spacing about one line height; headings sit closer to the text they introduce than to the text before;
- text survives the WCAG 1.4.12 Text Spacing overrides (line height 1.5, paragraph spacing 2x, letter 0.12em, word 0.16em) without clipping;
- body text resizes to 200% without loss (1.4.4).

## Logo use

The guide sets rules around the existing mark. Designing a new logo is out of scope here (see `later.md`).

### Versions

List each version that exists and when it is used: full lockup (symbol plus wordmark), horizontal and stacked if both exist, symbol alone for small spaces (favicon, app icon, social avatar), wordmark alone. For each colour treatment: full colour, one colour, and reversed (light on dark). Show which version goes on which ground.

### Clear space

Pick a unit taken from the mark itself (for example the height of the wordmark's x-height or of the symbol) and require that much empty space on every side. A unit from the mark scales with it; a fixed pixel value does not.

### Minimum size

State the smallest width at which each version stays legible, for screen in CSS px and for print in mm. Below it, switch to the symbol. Typical floors are around 80-120 px wide for a full lockup and 16-32 px for a symbol, but test the mark file itself: thin strokes fail sooner.

### Grounds

Show the logo on the approved grounds: white, the darkest neutral, the brand colour, and a photo with a scrim. For photos, the logo sits on an even, plain area or on a solid panel; never on a busy patch.

### Misuse

Write the bans as a short list with a picture of each where possible: no stretching or squashing, no rotation, no recolouring outside the approved treatments, no outlines, shadows or glows added, no rearranging the parts, no placing on a ground that fails contrast, no re-typesetting the wordmark in another font.

### Files

Keep vector masters (SVG for screen, PDF or EPS for print) plus PNG exports at fixed sizes for tools that cannot take vectors. The folder layout and naming are in `brand-assets.md`. Give the SVG a `<title>` and use `role="img"` with an accessible name where it is a link home.

### Partners

When a partner's mark sits beside ours: match optical size, not pixel size; separate them with a thin rule or clear space equal to the larger clear-space unit; agree who leads. Get the partner's written approval for their logo's use.

## Imagery

Describe the photo and illustration style in a few lines a photographer could act on: subject (real staff and premises over stock), light (natural or studio), colour grade, framing (close or wide), people (candid or posed), and what to avoid. Rules for sourcing, alt text and credits are in `../hallmark/imagery.md` and `../taste/photos.md`. For icons, name one set and one stroke weight; mixing sets is the most common visual slip.

## Quick checks before a page ships

- logo version, size and ground are all on the approved list;
- every colour on the page is a token, and every token is in the guide;
- text pairs pass their contrast floor in each mode;
- only the guide's families and weights load;
- photos match the written style; one icon set.
