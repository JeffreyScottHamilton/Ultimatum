# The hero, the page as a whole, nav and footer

Read when choosing a hero posture and when assembling the section order, close, nav and footer. Section-level rules are in `layout.md`; the job that decides the anatomy is in `anatomy.md`. The posture table is also `../../../../../data/craft/hallmark/hero-postures.csv`.

## The hero

It is the first screen at 1440 x 900 and 1920 x 1080, and only the first screen (gate 44c). Pick a posture from the job, stamp it, and vary it run to run. Text beside a picture (Settled, Stage) is the most common generated hero; use it only when the picture is the strongest thing the prompt has.

| Posture | Height | Content |
|---|---|---|
| Settled | fills the screen under the nav | centred in the screen; text on six columns, visual on the other six |
| Stage | fills the screen under the nav | text on five columns, a visual on seven at 60 to 75% screen height (reverse when a poster-size head needs width); may bleed off the outer edge |
| Banner | 50 to 60% of the screen | first section shows above the fold; for references, docs, utilities |
| Ledge | fills the screen | tall field above, head resting at the base; at 1920 the head grows to its cap first |
| Corridor | fills the screen | one centred column of 44ch or less, head larger than usual |
| Poster | 92 to 100dvh | full-bleed photo or canvas; content on its calmest part with room around, low and left or centred, never squeezed into a corner |
| Counter | fills the screen under the nav | the action is the visual: subscribe field with the latest issue, booking times, buy box, download with the screen, set large under a shorter head |
| Index | fills the screen under the nav | the content is the visual: the lineup, menu or list of projects as the lead, small head above |

- **Centred in its screen:** for Settled, Stage, Banner and Corridor the space under the content is 1.0 to 1.5 times the space above (44a) and the lowest content sits within 160px of the fold (79). Spend spare height on a bigger visual or bigger type, never copy.
- **The visual is big:** six or seven columns wide and 60% of screen height or more (520px at 1440 x 900), or a portrait object at 75% tall on four or five columns; centre within 60px of the text's. A two-track hero grid (6fr 5fr or 5fr 7fr) with a 48 to 120px gap. Under 60rem the gap becomes a row gap.
- **No visual:** the head grows to display size across eight to twelve columns, or the posture is Banner and the first section starts by 640px.
- **The text:** headline seven words or fewer, one sentence at lead size, one or two actions. Under 60rem every posture collapses to its content height (Poster may stay full-bleed). A working form is a section or a close, not the default hero.
- **Local sites:** the hero must show the phone number or the booking action and the place name; Counter and Poster are the usual postures for a shop or restaurant.

## The page

- **The job decides the anatomy** (`anatomy.md`): where the action lives (hero, sticky, repeated, close) and the category's own sections. The theme dresses it, never replaces it.
- **Order follows the shape's argument** (`page-shapes.md`), never hero, three features, call to action, footer. Lead with the strongest real thing after the hero; put each fact where it works.
- **Not every page has steps, figures or a schedule.** Steps only for a real process; a figure row only for three numbers the prompt states outright. Together they sit on most generated pages; on a made page they are a choice.
- **Variety:** no same composition in neighbouring sections; mirror a split once at most, never a zigzag; at least one full-width visual on a product page; one or two bands. Statement, Steps, Figures and a closing Band are the easy reaches; if the last build used one, beat it another way.
- **Balance:** photos take a quarter to a third of the page below the hero and never lead two sections in a row; between them build from the theme's material (type, figures, rules, product, table, form).
- **Pace:** a dense section (grid, table, bento, index) is followed by a quiet one (statement, showcase); end on a real close.
- **The close is the job, not a form:** end on what the visitor came to do in the job's own form (next times, buy box, store buttons, next date and address, latest issue) or on the last strong section and the footer. An email field closes a page only when a mailing list is native to the job or was asked for (gate 85).
- **Footer:** 200 to 400px: wordmark or one closing line, the real links, the legal line. A single line under a hairline suits a letter, document or manifesto. Our local footers add name, address, phone and hours (`../../pages-and-seo.md`).
- **Nav:** one line, 56 to 80px, sized to the real destinations. Vary it against the log: edge-aligned (wordmark and one or two links or an action at opposite edges), floating pill, masthead (large centred wordmark over a rule), slab (heavy full-width bar), search-led bar with a visible command pill, a banner over a bar that retracts on scroll, a three-part bar only for four or more real destinations. A side rail only where a sticky object earns it.
- **Footer shapes:** mast (large wordmark over links), statement (one big closing sentence, links beneath), colophon block, newsletter-first (subscribe pages only), letter close (sign-off and date), index columns only for a hub with a real sitemap.

## Before shipping

Scroll at 1440 x 900 one screen at a time: is something on each screen big enough to be its reason? A screen with only a heading and a line wants a bigger visual, the line set as a statement, or two sections merged. Then squint: with the words blurred, each section has a shape and the page a rhythm of heavy and light. The render tier measures width (77), head scale (78), hero foot (79) and photo share (83); the eye judges the rest.
