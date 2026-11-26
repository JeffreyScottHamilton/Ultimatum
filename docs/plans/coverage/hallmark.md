# Hallmark rebuild: coverage map

Source: nutlope/hallmark at commit 04977e1 (MIT, LICENSE read). Read only; none of its code was run. Ours: `plugins/ultimatum/skills/website/references/craft/hallmark/` (30 files plus `index.md`) and `plugins/ultimatum/data/craft/hallmark/` (five tables and a README).

## How this map was made

- The inventory comes from a walk of the source skill folder (187 files). Bulk folders are counted, not listed.
- Items are the source's headings and files, each assigned to the file and section that covers it. Section pointers are the nearest match found by hand; they were not generated.
- Status values: `covered` (same idea, our words), `expanded` (we add rules such as WCAG 2.2, reduced motion, local-business use, app screens, the anti-generic lint), `merged with X` (folded into an existing Ultimatum file, which stays the home of the rule; Taste files were not edited), `later` (listed in `later.md`, not shipped), `not applicable`.
- Where Hallmark overlaps Taste or the website references, our file points to them and says so in a Merged or Overlap line. Merges: `craft-type-colour.md` with `../../website/craft.md`; `craft-copy.md` with `../../copy.md`; `craft-motion.md` and `microinteractions.md` with `../taste/motion.md`; `craft-finish.md` with `../taste/cards-and-ui.md` and `../taste/accessibility.md`; `imagery.md` with `../taste/photos.md` and `../taste/icons-and-diagrams.md`; `data-viz.md` with `../taste/icons-and-diagrams.md`; `responsive.md` with `../taste/quality-gate.md`; the floor list in `principles.md` with `../../website/design-rules.md` § 2.
- Added beyond the source: the anti-generic lint ties, local-business jobs (calls, bookings, quotes, trust signals), app scope (sign-up, pricing, dashboards, checkout), and WCAG 2.2 and reduced-motion rules. Guidance never asks for eyebrows, pills, glows, gradients, fake stats or an arrow on every button.
- Item text is our own short summary and the file passes the same copy check as the craft files.

## Counts

- Items mapped: 180. Covered: 132. Expanded: 15. Merged: 13. Later: 19. Not applicable: 1.
- Shipped content: 90 gates (data), 17 compositions, 8 hero postures, 21 page shapes, 50 themes (header facts only), F1 to F26 finish checks.

## Source inventory

187 files.

| Folder | Files | Bytes |
|---|---|---|
| `./` | 2 | 19317 |
| `references` | 24 | 225970 |
| `references/macrostructures` | 21 | 32642 |
| `references/themes/` | 102 | 5722569 |
| `references/genres` | 4 | 6197 |
| `agents` | 1 | 386 |
| `scripts` | 15 | 913173 |
| `scripts/fixtures/` | 18 | 159551 |

## Item map

| Source | Item | Ours | Status |
|---|---|---|---|
| `SKILL.md` | The Floor (16 never-waived rules) | principles.md § The floor (never waived) | expanded |
| `SKILL.md` | Flow 0 pre-flight | principles.md § Order of work; flow-branches.md § Pre-flight edge cases | covered |
| `SKILL.md` | Flow 1 ask once | principles.md § Ask once | expanded |
| `SKILL.md` | Flow 2 shape | principles.md § Shape, signature and the mirror test | covered |
| `SKILL.md` | Flow 3 direction | principles.md § Order of work; themes.md; direction.md | covered |
| `SKILL.md` | Flow 4 load | principles.md § Order of work | covered |
| `SKILL.md` | Flow 5 picks block | principles.md § Picks block (said once) | covered |
| `SKILL.md` | Flow 6 build | principles.md § Order of work | covered |
| `SKILL.md` | Flow 7 sweep | principles.md § Order of work; gates.md § The two reviews, in fresh context | covered |
| `SKILL.md` | Branches (component, app, redesign, custom, fast, harnesses) | flow-branches.md | covered |
| `LICENSE` | MIT licence, copyright line | CREDITS line proposed (see report); licence not copied into the plugin | later |
| `agents/openai.yaml` | listing for another agent platform | later.md § Tooling | not applicable |
| `references/anatomy.md` | ten visitor jobs, one section each | anatomy.md § Jobs | covered |
| `references/anatomy.md` | How pages end | anatomy.md § How pages end | covered |
| `references/anatomy.md` | local trades and app jobs (not in the source) | anatomy.md § Local trades and apps | expanded |
| `references/brand-truth.md` | The protocol | brand-truth.md § Protocol | covered |
| `references/brand-truth.md` | Caching and staleness | brand-truth.md § Caching | covered |
| `references/brand-truth.md` | When fetching is impossible | brand-truth.md § When fetching is impossible | covered |
| `references/brand-truth.md` | What the protocol never does | brand-truth.md § Never | covered |
| `references/comp.md` | What the comp is | comp.md § What a comp is | covered |
| `references/comp.md` | The call | comp.md § The call | covered |
| `references/comp.md` | The approval point | comp.md § Approval | covered |
| `references/comp.md` | Reproduction discipline | comp.md § Reproduction check | covered |
| `references/comp.md` | The medium inventory | comp.md § Medium inventory | covered |
| `references/comp.md` | Generated stills | comp.md § Generated stills; imagery.md § Generated stills | merged with imagery.md |
| `references/craft.md` | 1 Type | craft-type-colour.md § Type | merged with website/craft.md |
| `references/craft.md` | 2 Colour | craft-type-colour.md § Colour | merged with website/craft.md |
| `references/craft.md` | 3 Surfaces | craft-type-colour.md § Surfaces | merged with website/craft.md |
| `references/craft.md` | 4 The hero's motion | craft-motion.md § Hero entrance | covered |
| `references/craft.md` | 5 Motion | craft-motion.md § Rules for every page | merged with taste/motion.md |
| `references/craft.md` | 6 Copy | craft-copy.md § Voice and budgets | merged with website/copy.md |
| `references/craft.md` | 7 Opening a section | craft-copy.md § Opening a section | covered |
| `references/craft.md` | 8 Missing facts | craft-copy.md § Missing facts | covered |
| `references/craft.md` | 9 Finish | craft-finish.md | merged with taste/cards-and-ui.md and taste/accessibility.md |
| `references/dark-mode.md` | The stance | dark-mode.md § Stance | covered |
| `references/dark-mode.md` | Token re-derivation | dark-mode.md § Token re-derivation | covered |
| `references/dark-mode.md` | Emission | dark-mode.md § Emission | covered |
| `references/dark-mode.md` | Dark discipline | dark-mode.md § Rules that change | covered |
| `references/dark-mode.md` | Verification | dark-mode.md § Verify | covered |
| `references/data-viz.md` | Form first | data-viz.md § Pick the form first | merged with taste/icons-and-diagrams.md |
| `references/data-viz.md` | Construction | data-viz.md § Build | covered |
| `references/data-viz.md` | Colour | data-viz.md § Colour | covered |
| `references/data-viz.md` | Honesty | data-viz.md § Honesty | covered |
| `references/data-viz.md` | Dark | data-viz.md § Dark | covered |
| `references/data-viz.md` | The dashboard bar | data-viz.md § The dashboard bar | expanded |
| `references/design-md.md` | Triggers | design-file.md § Rules | covered |
| `references/design-md.md` | Format and template | design-file.md § Template | covered |
| `references/design-md.md` | Exports | design-file.md § Exports | covered |
| `references/design-md.md` | After the file exists | design-file.md § Rules | covered |
| `references/direction.md` | Yours, all of it | direction.md § What stays yours | covered |
| `references/direction.md` | Before the first line of code | direction.md § Before any code | covered |
| `references/direction.md` | Spent | direction.md § Spent defaults, refused on sight | merged with website/design-rules.md § 2 |
| `references/direction.md` | Pictures | direction.md § Pictures and words | covered |
| `references/direction.md` | Words | direction.md § Pictures and words | covered |
| `references/direction.md` | What still binds | direction.md § What still binds | covered |
| `references/direction.md` | Mechanics | direction.md § Mechanics | covered |
| `references/direction.md` | local business and app notes (not in the source) | direction.md § Local business and app notes | expanded |
| `references/export-formats.md` | The token set | design-file.md § Token families | covered |
| `references/export-formats.md` | tokens.css in a project | design-file.md § Placing tokens in a project | covered |
| `references/export-formats.md` | Tailwind v4 | design-file.md § Tailwind v4 | covered |
| `references/export-formats.md` | DTCG tokens.json | design-file.md § DTCG tokens.json | covered |
| `references/export-formats.md` | shadcn/ui | design-file.md § shadcn/ui | covered |
| `references/flow.md` | Pre-flight edge cases | flow-branches.md § Pre-flight edge cases | covered |
| `references/flow.md` | Component scope | flow-branches.md § Component scope | covered |
| `references/flow.md` | App screens | flow-branches.md § App screens | expanded |
| `references/flow.md` | Sweep for a page not built here | flow-branches.md § Sweeping a page this process did not build | covered |
| `references/flow.md` | Archive builds, Hallmark sweeps | flow-branches.md § Another tool is driving | covered |
| `references/flow.md` | Fast mode | flow-branches.md § Fast mode | covered |
| `references/flow.md` | Edit-time linting | flow-branches.md § Edit-time checks | later |
| `references/flow.md` | Comp before build | flow-branches.md § What the work must produce; comp.md | covered |
| `references/flow.md` | Harnesses | flow-branches.md § Harness notes | covered |
| `references/flow.md` | Framework projects | flow-branches.md § Framework projects | covered |
| `references/flow.md` | Output contract | flow-branches.md § What the work must produce | covered |
| `references/fonts.md` | The rule | fonts.md § Rule | covered |
| `references/fonts.md` | Banned as a default | fonts.md § Reflex choices to avoid by default | covered |
| `references/fonts.md` | Sources | fonts.md § Sources | covered |
| `references/fonts.md` | Display faces the catalog does not use | fonts.md § Alternatives by class | covered |
| `references/fonts.md` | Body faces | fonts.md § Alternatives by class | covered |
| `references/fonts.md` | The wordmark | fonts.md § Wordmark | covered |
| `references/fonts.md` | Loading | fonts.md § Loading | covered |
| `references/gates.md` | 1 How a gate binds | gates.md § Tiers | covered |
| `references/gates.md` | 2 Waivers and answers | gates.md § Stamp, waivers and answers | covered |
| `references/gates.md` | 3 Pre-emit critique | gates.md § Pre-emit critique | covered |
| `references/gates.md` | 4 The gates (about 90, six groups) | data/craft/hallmark/gates.csv (90 rows); gates.md | covered |
| `references/gates.md` | 5 Finish checks F1 to F26 | gates.md § Finish checks (F1 to F26) | covered |
| `references/gates.md` | 5 Judged clauses | gates.md § Judged clauses | covered |
| `references/gates.md` | 6 The two reviews | gates.md § The two reviews, in fresh context; review-prompts.md | covered |
| `references/gates.md` | WCAG 2.2, reduced motion, local business and app rules (not in the source) | gates.md § Judged clauses; craft-finish.md; interaction-and-states.md | expanded |
| `references/imagery.md` | 1 What fills a page | imagery.md § Order of preference | covered |
| `references/imagery.md` | 2 The library | imagery.md § Sourcing rules that carry over | merged with taste/photos.md |
| `references/imagery.md` | 3 Slots | imagery.md § Slots | covered |
| `references/imagery.md` | 4 The product, captured first | imagery.md § Product | covered |
| `references/imagery.md` | 5 Placing and treating photographs | imagery.md § Placing photographs | covered |
| `references/imagery.md` | 6 Generated stills | imagery.md § Generated stills | covered |
| `references/imagery.md` | 7 Never | imagery.md § Forbidden | covered |
| `references/imagery.md` | 8 Icons, logos, video, 3D | imagery.md § Icons, logos, video, 3D | merged with taste/icons-and-diagrams.md |
| `references/imagery.md` | 9 Stamp, log and handoff | imagery.md § Stamp, log, handoff | covered |
| `references/interaction-and-states.md` | The eight states | interaction-and-states.md § The eight states | covered |
| `references/interaction-and-states.md` | Focus rings | interaction-and-states.md § Focus rings and hit targets | expanded |
| `references/interaction-and-states.md` | Hit targets | interaction-and-states.md § Focus rings and hit targets | expanded |
| `references/interaction-and-states.md` | Forms and the field | interaction-and-states.md § Forms | expanded |
| `references/interaction-and-states.md` | Modals and overlays | interaction-and-states.md § Dialogs and overlays | covered |
| `references/interaction-and-states.md` | Popovers, menus, tooltips | interaction-and-states.md § Popovers | covered |
| `references/interaction-and-states.md` | Undo over confirm | interaction-and-states.md § Undo | covered |
| `references/interaction-and-states.md` | Loading and empty | interaction-and-states.md § Loading and empty | covered |
| `references/layout.md` | 1 The canvas | layout.md § The canvas | covered |
| `references/layout.md` | 2 Sizes | layout.md § Sizes | covered |
| `references/layout.md` | 3 Rhythm between sections | layout.md § Rhythm between sections | covered |
| `references/layout.md` | 4 A section | layout.md § What a section is | covered |
| `references/layout.md` | 5 Compositions (17) | layout.md § Compositions; data/craft/hallmark/compositions.csv | covered |
| `references/layout.md` | 6 The hero (8 postures) | hero-and-page.md § The hero; data/craft/hallmark/hero-postures.csv | covered |
| `references/layout.md` | 7 The page | hero-and-page.md § The page | covered |
| `references/layout.md` | 8 Before shipping | hero-and-page.md § Before shipping | covered |
| `references/macrostructures.md` | Index of 21 shapes | page-shapes.md § Shapes are a vocabulary; data/craft/hallmark/page-shapes.csv | covered |
| `references/macrostructures.md` | SaaS section deck | page-shapes.md § SaaS section deck (dealt, not sequenced) | covered |
| `references/macrostructures.md` | How to pick | page-shapes.md § Choosing one | covered |
| `references/macrostructures.md` | The fingerprint: six axes | page-shapes.md § The six-axis fingerprint | covered |
| `references/macrostructures.md` | Domain to trio | page-shapes.md § Domain words to three candidates | expanded |
| `references/microinteractions.md` | Principles | microinteractions.md § Principles | merged with taste/motion.md |
| `references/microinteractions.md` | Recipes | microinteractions.md § Recipes | covered |
| `references/microinteractions.md` | Motion character | microinteractions.md § Character of the system | covered |
| `references/patterns.md` | Controls, all eight states | patterns.md § Controls, all eight states | covered |
| `references/patterns.md` | A photograph in a slot | patterns.md § A photograph in a slot | covered |
| `references/patterns.md` | A choice between a few | patterns.md § A choice between a few | covered |
| `references/patterns.md` | A rail and a switcher | patterns.md § A rail and a switcher | covered |
| `references/patterns.md` | fact-slot pattern | patterns.md, the section on a fact the prompt did not give | covered |
| `references/patterns.md` | unwired form pattern | patterns.md, the section on a form that posts nowhere yet | covered |
| `references/patterns.md` | One reveal that survives no script | patterns.md § One reveal that survives no script | covered |
| `references/patterns.md` | Figures that compare | patterns.md § Figures that compare | covered |
| `references/patterns.md` | A loop that can pause | patterns.md § A loop that can pause | expanded |
| `references/patterns.md` | A way past the nav | patterns.md § A way past the nav | expanded |
| `references/redesign.md` | What a redesign keeps | redesign.md § What a redesign keeps | covered |
| `references/redesign.md` | Depth | redesign.md § Depth | covered |
| `references/redesign.md` | Before | redesign.md § Before | covered |
| `references/redesign.md` | The ask | redesign.md § The ask | covered |
| `references/redesign.md` | The plan | redesign.md § The plan | covered |
| `references/redesign.md` | Build | redesign.md § Build | covered |
| `references/redesign.md` | After | redesign.md § After | covered |
| `references/responsive.md` | What the script checks and cannot | responsive.md § Check by eye at each width | merged with taste/quality-gate.md |
| `references/responsive.md` | Breakpoints | responsive.md § Breakpoints | covered |
| `references/responsive.md` | Fluid and discrete | responsive.md § Fluid and discrete | covered |
| `references/responsive.md` | Clickable text never wraps | responsive.md § Clickable text never wraps | covered |
| `references/responsive.md` | Units and safe areas | responsive.md § Units and safe areas | covered |
| `references/responsive.md` | Tables, images, languages | responsive.md § Tables, images, languages | covered |
| `references/review-finish.md` | Finish review prompt | review-prompts.md § Finish review (the built page) | covered |
| `references/review-hero.md` | Hero review prompt | review-prompts.md § Hero review (the first screen, mid-build) | covered |
| `references/scroll-choreography.md` | Budget | scroll-choreography.md § Rules | covered |
| `references/scroll-choreography.md` | 1 Pinned chapter | scroll-choreography.md § Pinned chapter | covered |
| `references/scroll-choreography.md` | 2 Scrub-linked headline | scroll-choreography.md § Scrubbed headline | covered |
| `references/scroll-choreography.md` | 3 Progress spine | scroll-choreography.md § Progress spine | covered |
| `references/scroll-choreography.md` | 4 Sticky diptych | scroll-choreography.md § Sticky diptych | covered |
| `references/scroll-choreography.md` | JS fallback | scroll-choreography.md § Fallback | expanded |
| `references/texture.md` | The budget | texture.md § Budget | covered |
| `references/texture.md` | Grain | texture.md § Recipes | covered |
| `references/texture.md` | Halftone | texture.md § Recipes | covered |
| `references/texture.md` | Misregistration | texture.md § Recipes | covered |
| `references/texture.md` | Scanline | texture.md § Recipes | covered |
| `references/texture.md` | Deckle | texture.md § Recipes | covered |
| `references/texture.md` | Affinity: who earns texture | texture.md § Who earns it | covered |
| `references/texture.md` | Reduced motion and accessibility | texture.md § Recipes; craft-motion.md | expanded |
| `scripts/capture.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/capture.test.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/imagegen.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/install-hook.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/install.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/lint-hook.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/photos.json` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/picture.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/refcheck.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/reroll-exhaustion.test.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/sloplint-render.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/sloplint-render.test.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/sloplint.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/theme.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `scripts/theme.test.mjs` | Node tool, data or test | later.md § Tooling / § Assets and fixtures | later |
| `references/macrostructures/ (21 files)` | one file per page shape | data/craft/hallmark/page-shapes.csv; page-shapes.md § Shape notes | covered |
| `references/genres/ (4 files)` | atmospheric, editorial, modern-minimal, playful: allowed, refused, chrome | genres.md | covered |
| `references/themes/*.md (51 files)` | 50 theme files plus an index | data/craft/hallmark/themes.csv (50 rows); themes.md | covered |
| `references/themes/*.jpg (50 files)` | one reference picture per theme | later.md § Assets and fixtures | later |
| `scripts/fixtures/ (18 files)` | sample pages for the lint gates | later.md § Assets and fixtures | later |

## Examples run

Run with Python Playwright against a scratch page, headless Chromium (the preinstalled headless shell; the bundled build named by this Playwright version was missing). All of these passed after one fix.

- `craft-motion.md` reveal: hidden at rest with the `js` class, shown after `.in`, visible with no script, visible and unshifted under reduced motion. The run found that the reduced-motion rule reset `transform` while the reveal moves with `translate`; fixed to `translate: none`.
- `patterns.md`: no page errors; button min-height, disabled opacity, busy cursor, quiet background, keyboard focus ring and hover colour; segmented radios checked by label click; loop toggle (Pause and Play, hidden under reduced motion); skip link hidden until keyboard focus.
- `imagery.md`: `fillSlots` swaps in an image with the slot's alt text and keeps the earlier content when a load fails; the capture snippet wrote two PNGs against a local server.
- `texture.md`: all CSS blocks parse and the grain data URI decodes as a 180 by 180 image.
- `scroll-choreography.md`: CSS blocks parse; `animation-timeline` is supported in the Chromium used. The scrolling behaviour itself was not exercised.
- `microinteractions.md` copy button: state set and cleared after 2.5 seconds, with `clipboard.writeText` stubbed because the page is not a secure context.
- `page-shapes.md` run-in head: heading and next paragraph share a line.
- `redesign.md` `before.py` (three PNGs and the inventory JSON) and the `comp.md` screenshot snippet, both against a local server.
- Every CSS block in the craft files: each declaration passed `CSS.supports`.

Loaded without errors but not otherwise asserted: the `data-viz.md` and `dark-mode.md` HTML, the other `patterns.md` blocks (rail, figures, unwired form). Not run: the optimistic-toggle snippet in `microinteractions.md`, the IntersectionObserver fallback in `scroll-choreography.md`, the Tailwind and DTCG blocks in `design-file.md`.

## Not verified

- The external links in the craft files (MDN, Playwright, Tailwind, Lucide, Simple Icons and similar) were not fetched here; the proxy refused the connection or none was tried. The test checks only that they are https.
- Gate counts and thresholds were rewritten from the source's table by hand; they have not been re-run against a linter (the source's Node linter is not adopted).
- The 50 theme bodies and 50 pictures are not shipped; only header facts (`themes.csv`).
