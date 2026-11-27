# Later: what these guides leave out

Read when a task needs something the UI UX Pro Max guides in this folder do not cover, to see whether it was left out on purpose and where to go instead.

## Out of scope for this rebuild

| Left out | Why | Go to instead |
|---|---|---|
| slide decks (the slides skill, the design system's slide tokens, layouts, copy formulas and slide search) | done in 0.0.39 as its own folder | `../decks/index.md` |
| banner design (sizes and styles by platform) | done in 0.0.40, with dated sizes | `../identity/banners.md` |
| logo creation (prompting, styles, colour psychology) | another session owns the logo and identity guide | that guide, once merged |
| corporate identity packs (stationery, deliverables, style guides) | same as above | that guide, once merged |
| icon design | done in 0.0.40 | `../identity/icons.md` |
| social photo design and design routing from the design skill | outside the three guides asked for | `../hallmark/imagery.md`, `../taste/photos.md` |
| the bundled canvas fonts | fonts are linked or self-hosted with their licence, never shipped in this plugin | `../hallmark/fonts.md` |
| AI image-generation prompts in the brand template | prompts for image services belong with the image tools that run them | a later imagery guide |
| the brand update presets | the source's presets are its own picks; ours are the starter tokens | `../../../../../data/design-own/tokens/starter.tokens.json` |
| platform size tables for logos and social avatars | change often; need a dated source | `../identity/banners.md` § 3. Social covers and headers, dated; then each platform's help pages |

## Source scripts not rebuilt

None of the source's scripts were run or ported. Where a job matters, it is covered by our own tool or another way:

| Source script's job | Our answer |
|---|---|
| generate CSS from a token file | `tools/build_tokens.py` (our own, stdlib only) |
| validate tokens and find raw values in CSS | the generator's reference and contrast checks; `token_check.py scan` for raw values in CSS, HTML, SVG and components (`token-check.md`) |
| embed tokens into HTML, validate HTML against tokens | `token_check.py embed` and `scan` (`token-check.md` § embed) |
| sync brand values into tokens, inject brand context into prompts | by hand, following `brand-flow.md` § 3. Turn the guide into tokens |
| extract colours from images, validate assets | `token_check.py colors` for PNG, SVG, HTML and CSS against the palette (`token-check.md` § colors); JPEG and WebP not read |
| add shadcn components, generate a Tailwind config | use the official CLIs: `npx shadcn@latest add`, and CSS-first Tailwind v4 config (`tailwind-customisation.md`) |
| slide search, slide token validation, background image fetch | deck checking is done (`../decks/build.md`); slide search and image fetch stay out |

## Could come next

- A DTCG import for `tools/build_tokens.py`, so a design tool's export can be the source directly.
- More filled component sheets (tabs, menu, toast, pagination) in `component-specs.md`.
