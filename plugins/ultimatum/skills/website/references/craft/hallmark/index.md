# Hallmark craft: index

Read when a website build wants the Hallmark layer on top of Taste: one line per file, with the question it answers. Rebuilt in our own words from the MIT-licensed Hallmark skill (nutlope/hallmark, commit 04977e1). Where it overlaps Taste (`../taste/index.md`) or the house rules (`../../website/design-rules.md`), these files point there instead of repeating; the house rules win on any conflict.

## Reading order

1. `principles.md` then `genres.md` then `page-shapes.md` then `hero-and-page.md` then `layout.md`.
2. Then only the files the plan needs, and `gates.md` with `review-prompts.md` before hand-over.

## Files

- `principles.md`: What bar must the page clear, what is the floor, and in what order is the work done?
- `genres.md`: Which of four registers is this page, and what does each allow or refuse?
- `themes.md`: How do I pick a theme from the catalog table, and how do I write a new one?
- `direction.md`: How do I design a bespoke page when the user wants nothing templated?
- `page-shapes.md`: Which of 21 page shapes fits the subject, and how is it fingerprinted?
- `hero-and-page.md`: Which of eight hero postures, and how are the nav and footer shaped?
- `layout.md`: What are the canvas, sizes, rhythm and 17 section compositions?
- `anatomy.md`: What does a page built for one job (book, call, buy, sign up, and so on) contain?
- `craft-type-colour.md`: What are the type, OKLCH colour and surface rules?
- `craft-motion.md`: Which easings, durations and one reveal does the page get?
- `craft-copy.md`: How is copy written, how is a section opened, and what happens with missing facts?
- `craft-finish.md`: How are controls, inputs, content blocks, responsive behaviour and the document finished?
- `fonts.md`: Which faces, from where, and how are they loaded?
- `imagery.md`: What fills a page, how are slots, photos, captures and icons handled?
- `patterns.md`: How are buttons, slots, forms, switchers, stats and skip links built?
- `interaction-and-states.md`: What are the eight states, the field recipe, overlays, undo and loading?
- `microinteractions.md`: How does each stateful widget move, and in which motion character?
- `responsive.md`: Which breakpoints, units and table rules keep 320–1920 working?
- `texture.md`: When may a page carry grain, halftone, misregistration or scanlines, and within what budget?
- `scroll-choreography.md`: Which one scroll-linked pattern is allowed, and how does it degrade?
- `dark-mode.md`: How are both modes derived from one token set?
- `data-viz.md`: Which chart form, build and colour rules apply, and what must stay honest?
- `design-file.md`: How is the system locked into a portable file and exported to Tailwind, DTCG or shadcn?
- `brand-truth.md`: How are a real brand's colours and faces read without guessing from memory?
- `comp.md`: How are comps used, approved and checked against the build?
- `redesign.md`: How does a redesign, restyle, polish or audit keep content and wiring?
- `flow-branches.md`: What changes for components, app screens, other tools' pages, fast mode and frameworks?
- `gates.md`: Which tiers, gates, finish checks and reviews apply before a page is done?
- `review-prompts.md`: What does a fresh-context reviewer get asked for the hero and the finished page?
- `later.md`: Which source tools, assets and fixtures are not shipped, and what would each take?

Data: `../../../../../data/craft/hallmark/` holds `gates.csv`, `compositions.csv`, `hero-postures.csv`, `page-shapes.csv` and `themes.csv`; its `README.md` lists the columns. The checkable gates run by script: `../design-review-qa/page-lint.md`.
