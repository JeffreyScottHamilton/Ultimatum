# UI UX Pro Max guides rebuild: coverage map

Source: nextlevelbuilder/ui-ux-pro-max-skill at commit a4fc248, read from `/tmp/src/uiux` (MIT for the repository; Apache-2.0 for `ui-styling`, per its LICENSE.txt). Read only; none of its scripts were run. Ours: `plugins/ultimatum/skills/website/references/craft/ui-ux-pro-max/` (16 guides, `index.md`, `later.md`), `plugins/ultimatum/data/design-own/tokens/` and `tools/build_tokens.py`.

## How this map was made

- The inventory is a walk of the six skill folders under `.claude/skills/` (brand, design-system, ui-styling, design, slides, banner-design); `cli/assets/skills/` holds the same skills and is not mapped twice. Test folders and `__pycache__` are left out. The 81 files in `ui-styling/canvas-fonts/` are one row.
- One row per source file. `Where` names our file and section; pointers were assigned by hand.
- Status: `covered` (same topic, our words), `expanded` (we add rules or move it to current versions: Tailwind v4, WCAG 2.2, APG keyboard patterns, our own generator and tested templates), `merged with X` (folded into another of our files), `later` (listed in `later.md`, not shipped).
- The brand guides point to `../hallmark/brand-truth.md` for checking an owner's facts rather than repeating it.
- Source v3 and HSL-triplet Tailwind material is marked `expanded`: it is rebuilt for v4 (`@theme`, `@theme inline`, full colour values).
- Item text is our own and this file passes the same copy check as the guides.

## Items

| Source item | Status | Where |
|---|---|---|
| `banner-design/SKILL.md` | covered | `../identity/banners.md` § 1 Rules for any banner |
| `banner-design/references/banner-sizes-and-styles.md` | expanded | `../identity/banners.md` § 2–5 (dated sizes, print, email; check each platform's page) |
| `brand/SKILL.md` | expanded | `brand-flow.md`, with `../hallmark/brand-truth.md` as the facts check |
| `brand/references/approval-checklist.md` | covered | `brand-review.md` |
| `brand/references/asset-organization.md` | covered | `brand-assets.md` |
| `brand/references/brand-guideline-template.md` | merged with brand-guidelines-template.md | `brand-guidelines-template.md` |
| `brand/references/color-palette-management.md` | covered | `brand-visual.md` § Colour: roles before values |
| `brand/references/consistency-checklist.md` | merged with brand-review.md | `brand-review.md` |
| `brand/references/logo-usage-rules.md` | covered | `brand-visual.md` § Logo use |
| `brand/references/messaging-framework.md` | merged with brand-voice.md | `brand-voice.md` |
| `brand/references/typography-specifications.md` | covered | `brand-visual.md` § Type: a short, loadable spec |
| `brand/references/update.md` | merged with brand-flow.md | `brand-flow.md` § 5. Updating an existing brand; its presets are in `later.md` |
| `brand/references/visual-identity.md` | merged with ../hallmark/brand-truth.md | `brand-visual.md` and `../hallmark/brand-truth.md` |
| `brand/references/voice-framework.md` | covered | `brand-voice.md` |
| `brand/scripts/extract-colors.cjs` | later | `later.md` § Source scripts not rebuilt |
| `brand/scripts/inject-brand-context.cjs` | later | `later.md` § Source scripts not rebuilt |
| `brand/scripts/sync-brand-to-tokens.cjs` | later | `later.md`; by hand in `brand-flow.md` § 3. Turn the guide into tokens |
| `brand/scripts/validate-asset.cjs` | later | `later.md` § Source scripts not rebuilt |
| `brand/templates/brand-guidelines-starter.md` | merged with brand-guidelines-template.md | `brand-guidelines-template.md` |
| `design-system/SKILL.md` | expanded | `token-architecture.md`, `token-templates.md` |
| `design-system/data/slide-backgrounds.csv` | later | `../decks/later.md` (background keywords) |
| `design-system/data/slide-charts.csv` | covered | `../decks/charts.md` § Which chart |
| `design-system/data/slide-color-logic.csv` | covered | `../decks/slides.md` § Colour and backgrounds |
| `design-system/data/slide-copy.csv` | merged with slides/references/copywriting-formulas.md | `../decks/story.md` |
| `design-system/data/slide-layout-logic.csv` | covered | `../decks/plan-check.md` (`deck-types.csv`, `layouts.csv`) |
| `design-system/data/slide-layouts.csv` | merged with slides/references/layout-patterns.md | `../decks/slides.md` |
| `design-system/data/slide-strategies.csv` | merged with slides/references/slide-strategies.md | `../decks/story.md` |
| `design-system/data/slide-typography.csv` | covered | `../decks/slides.md` § Type that reads across a room |
| `design-system/references/component-specs.md` | expanded | `component-specs.md` |
| `design-system/references/component-tokens.md` | merged with token-architecture.md | `token-architecture.md` § Layer 3: component tokens |
| `design-system/references/primitive-tokens.md` | merged with token-architecture.md | `token-architecture.md` § Layer 1: primitives |
| `design-system/references/semantic-tokens.md` | merged with token-architecture.md | `token-architecture.md` § Layer 2: semantic roles |
| `design-system/references/states-and-variants.md` | expanded | `states-and-variants.md` |
| `design-system/references/tailwind-integration.md` | expanded | `token-templates.md` § Template 2: Tailwind CSS v4 theme (v3 config rebuilt as v4 `@theme`) |
| `design-system/references/token-architecture.md` | expanded | `token-architecture.md` |
| `design-system/scripts/embed-tokens.cjs` | later | `later.md` § Source scripts not rebuilt |
| `design-system/scripts/fetch-background.py` | later | `later.md` § Out of scope for this rebuild |
| `design-system/scripts/generate-slide.py` | later | `../decks/later.md` (generator) |
| `design-system/scripts/generate-tokens.cjs` | expanded | `tools/build_tokens.py` (our own stdlib generator; source not run) |
| `design-system/scripts/html-token-validator.py` | later | `later.md` § Source scripts not rebuilt |
| `design-system/scripts/search-slides.py` | covered | `../decks/plan-check.md` (`deck_plan.py plan` and `check`) |
| `design-system/scripts/slide-token-validator.py` | expanded | `data/craft/decks/deck_check.py`, 12 rules |
| `design-system/scripts/slide_search_core.py` | later | `../decks/later.md` (lookup tables) |
| `design-system/scripts/validate-tokens.cjs` | merged with tools/build_tokens.py | reference and contrast checks in `tools/build_tokens.py` |
| `design-system/templates/design-tokens-starter.json` | expanded | `data/design-own/tokens/starter.tokens.json` (our own values, contrast pairs checked) |
| `design/SKILL.md` | later | `later.md` § Out of scope for this rebuild |
| `design/data/cip/deliverables.csv` | later | `later.md` § Out of scope for this rebuild |
| `design/data/cip/industries.csv` | later | `later.md` § Out of scope for this rebuild |
| `design/data/cip/mockup-contexts.csv` | later | `later.md` § Out of scope for this rebuild |
| `design/data/cip/styles.csv` | later | `later.md` § Out of scope for this rebuild |
| `design/data/icon/styles.csv` | merged with icon-design.md | `../identity/icons.md` § 1–2 (libraries by style, fill or line) |
| `design/data/logo/colors.csv` | later | `later.md` § Out of scope for this rebuild |
| `design/data/logo/industries.csv` | later | `later.md` § Out of scope for this rebuild |
| `design/data/logo/styles.csv` | later | `later.md` § Out of scope for this rebuild |
| `design/references/banner-sizes-and-styles.md` | merged with banner-sizes-and-styles.md | `../identity/banners.md` |
| `design/references/cip-deliverable-guide.md` | later | `later.md` § Out of scope for this rebuild |
| `design/references/cip-design.md` | later | `later.md` § Out of scope for this rebuild |
| `design/references/cip-prompt-engineering.md` | later | `later.md` § Out of scope for this rebuild |
| `design/references/cip-style-guide.md` | later | `later.md` § Out of scope for this rebuild |
| `design/references/design-routing.md` | later | `later.md` § Out of scope for this rebuild |
| `design/references/icon-design.md` | expanded | `../identity/icons.md`, with `icon_check.py` (12 rules) |
| `design/references/logo-color-psychology.md` | later | `later.md` § Out of scope for this rebuild |
| `design/references/logo-design.md` | later | `later.md` § Out of scope for this rebuild |
| `design/references/logo-prompt-engineering.md` | later | `later.md` § Out of scope for this rebuild |
| `design/references/logo-style-guide.md` | later | `later.md` § Out of scope for this rebuild |
| `design/references/slides-copywriting-formulas.md` | merged with slides/references/copywriting-formulas.md | `../decks/story.md` |
| `design/references/slides-create.md` | merged with slides/references/create.md | `../decks/story.md` |
| `design/references/slides-html-template.md` | merged with slides/references/html-template.md | `../decks/build.md` |
| `design/references/slides-layout-patterns.md` | merged with slides/references/layout-patterns.md | `../decks/slides.md` |
| `design/references/slides-strategies.md` | merged with slides/references/slide-strategies.md | `../decks/story.md` |
| `design/references/slides.md` | merged with slides/SKILL.md | `../decks/index.md` |
| `design/references/social-photos-design.md` | later | `later.md` § Out of scope for this rebuild |
| `design/scripts/cip/core.py` | later | `later.md` § Out of scope for this rebuild |
| `design/scripts/cip/generate.py` | later | `later.md` § Out of scope for this rebuild |
| `design/scripts/cip/render-html.py` | later | `later.md` § Out of scope for this rebuild |
| `design/scripts/cip/search.py` | later | `later.md` § Out of scope for this rebuild |
| `design/scripts/icon/generate.py` | later | `../identity/later.md` (generators that call paid image APIs) |
| `design/scripts/logo/core.py` | later | `later.md` § Out of scope for this rebuild |
| `design/scripts/logo/generate.py` | later | `later.md` § Out of scope for this rebuild |
| `design/scripts/logo/search.py` | later | `later.md` § Out of scope for this rebuild |
| `slides/SKILL.md` | covered | `../decks/index.md` |
| `slides/references/copywriting-formulas.md` | expanded | `../decks/story.md` § Headlines are sentences, § Copy patterns |
| `slides/references/create.md` | expanded | `../decks/story.md` § Write three lines, § The slide list |
| `slides/references/html-template.md` | expanded | `data/craft/decks/template.html`, `../decks/build.md` (PDF export, notes) |
| `slides/references/layout-patterns.md` | covered | `../decks/slides.md` § Layouts most decks need |
| `slides/references/slide-strategies.md` | covered | `../decks/story.md` § Pick the deck type, § Arcs that work |
| `ui-styling/LICENSE.txt` | covered | Apache-2.0 noted in `index.md` and the proposed CREDITS line |
| `ui-styling/SKILL.md` | covered | `index.md` § UI styling |
| `ui-styling/canvas-fonts/ (81 font and OFL files)` | later | `later.md`; fonts are linked, never bundled |
| `ui-styling/references/canvas-design-system.md` | expanded | `canvas-design.md` |
| `ui-styling/references/shadcn-accessibility.md` | expanded | `shadcn-accessibility.md` (WCAG 2.2, APG links) |
| `ui-styling/references/shadcn-components.md` | covered | `shadcn-components.md` |
| `ui-styling/references/shadcn-theming.md` | covered | `shadcn-theming.md` |
| `ui-styling/references/tailwind-customization.md` | expanded | `tailwind-customisation.md` (v3 config rebuilt for v4 CSS-first) |
| `ui-styling/references/tailwind-responsive.md` | merged with tailwind-utilities.md | `tailwind-utilities.md` § Responsive: mobile first |
| `ui-styling/references/tailwind-utilities.md` | expanded | `tailwind-utilities.md` (v4 names, container queries) |
| `ui-styling/scripts/.coverage` | later | a test artefact; not adopted |
| `ui-styling/scripts/requirements.txt` | later | `later.md` § Source scripts not rebuilt |
| `ui-styling/scripts/shadcn_add.py` | later | official `npx shadcn@latest add` in `shadcn-components.md` |
| `ui-styling/scripts/tailwind_config_gen.py` | later | CSS-first config in `tailwind-customisation.md` |

Counts: covered 17 / expanded 18 / merged 22 / later 43 (100 rows). Slides rows updated in 0.0.39; icon and banner rows in 0.0.40.
