# UI UX Pro Max guides: brand, design system and UI styling

Read when a website task needs a written brand guide, a token-based design system, or shadcn/ui and Tailwind CSS v4 styling. These guides are rebuilt in our own words from the topics of the MIT and Apache-2.0 licensed UI UX Pro Max skills; nothing is copied. Start with the one line that fits the job, and read others only when it points to them.

## Brand

- `brand-flow.md`: the order to build or update a brand guide, from the owner's facts to tokens and back.
- `brand-voice.md`: voice sliders, traits with their limits, tone by moment, word lists and the messaging block.
- `brand-visual.md`: palette roles and ramps, contrast floors, the type spec, logo use rules and imagery notes.
- `brand-assets.md`: folder layout, file names, the per-asset record, tags and quarterly clean-up.
- `brand-review.md`: the approval gate for one piece and the consistency audit for the whole brand.
- `brand-guidelines-template.md`: a fill-in brand guidelines file with a summary card and change log.

## Design system

- `token-architecture.md`: primitive, semantic and component layers, naming, dark mode by override, migration from flat CSS.
- `token-templates.md`: the plain CSS and Tailwind v4 templates our generator writes, and how they were tested.
- `states-and-variants.md`: which state wins, the attribute for each state, loading and errors, variants from local tokens.
- `component-specs.md`: the spec sheet format, filled in for button, field, card, badge, alert, dialog and table.

## UI styling

- `shadcn-components.md`: setting up shadcn/ui, choosing the right component, forms, variants and keeping copies healthy.
- `shadcn-theming.md`: colour roles, putting a brand in, adding a role, radius, dark mode with next-themes.
- `shadcn-accessibility.md`: what the primitives handle, keyboard by component, names, forms, announcements, tests.
- `tailwind-utilities.md`: utilities, complete class names, mobile-first breakpoints and container queries in v4.
- `tailwind-customisation.md`: `@theme`, `@utility`, `@custom-variant`, layers, arbitrary values and moving from v3.
- `canvas-design.md`: posters and single-image pieces: idea first, fixed constraints, finish and export.

## Not here yet

- `later.md`: what was left out and why (slides, banners, logo and identity design, icons, the source's scripts).

Tools and data: `tools/build_tokens.py` builds CSS from `../../../../../data/design-own/tokens/starter.tokens.json` and checks every contrast pair.
