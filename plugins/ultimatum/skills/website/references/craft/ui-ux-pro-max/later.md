# Later: what these guides leave out

Read when a task needs something the UI UX Pro Max guides in this folder do not cover, to see whether it was left out on purpose and where to go instead.

## Out of scope for this rebuild

| Left out | Why | Go to instead |
|---|---|---|
| slide decks (the slides skill, the design system's slide tokens, layouts, copy formulas and slide search) | a separate skill and job | the Slides artifact type, or `../../website/design-rules.md` for the look |
| banner design (sizes and styles by platform) | a separate skill; platform sizes change often and need a dated source | each platform's own help pages, checked on the day |
| logo creation (prompting, styles, colour psychology) | another session owns the logo and identity guide | that guide, once merged |
| corporate identity packs (stationery, deliverables, style guides) | same as above | that guide, once merged |
| icon design | same as above | `brand-visual.md` § Imagery for choosing one set |
| social photo design and design routing from the design skill | outside the three guides asked for | `../hallmark/imagery.md`, `../taste/photos.md` |
| the bundled canvas fonts | fonts are linked or self-hosted with their licence, never shipped in this plugin | `../hallmark/fonts.md` |
| AI image-generation prompts in the brand template | prompts for image services belong with the image tools that run them | a later imagery guide |
| the brand update presets | the source's presets are its own picks; ours are the starter tokens | `../../../../../data/design-own/tokens/starter.tokens.json` |
| platform size tables for logos and social avatars | change often; need a dated source | each platform's help pages |

## Source scripts not rebuilt

None of the source's scripts were run or ported. Where a job matters, it is covered another way:

| Source script's job | Our answer |
|---|---|
| generate CSS from a token file | `tools/build_tokens.py` (our own, stdlib only) |
| validate tokens and find raw values in CSS | the generator's reference and contrast checks; a search for raw colours in CI (`token-architecture.md` § Moving a flat stylesheet to layers) |
| embed tokens into HTML, validate HTML against tokens | not rebuilt; link the generated stylesheet instead |
| sync brand values into tokens, inject brand context into prompts | by hand, following `brand-flow.md` § 3. Turn the guide into tokens |
| extract colours from images, validate assets | not rebuilt; read values from the brand's own files (`../hallmark/brand-truth.md`) |
| add shadcn components, generate a Tailwind config | use the official CLIs: `npx shadcn@latest add`, and CSS-first Tailwind v4 config (`tailwind-customisation.md`) |
| slide search, slide token validation, background image fetch | out of scope with slides |

## Could come next

- A DTCG import for `tools/build_tokens.py`, so a design tool's export can be the source directly.
- A raw-value scanner in the toolbelt that flags colours outside the token file.
- More filled component sheets (tabs, menu, toast, pagination) in `component-specs.md`.
