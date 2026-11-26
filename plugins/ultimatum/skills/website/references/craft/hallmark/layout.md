# Layout: canvas, sizes, rhythm, sections and compositions

Read when deciding where every section sits. Figures assume a 1440×900 window unless noted. First-screen and whole-page rules are in `hero-and-page.md`; the 17 compositions also exist as a table in `../../../../../data/craft/hallmark/compositions.csv`.

## The canvas

- A single centred container capped at 1440px with 64px side gutters. Content measures 1312px at 1440 and stays 1312 at 1920 as the gutters widen (gate 44d).
- Inside it, a twelve-column grid with 32px gaps (one column 80px, four 416, six 640, eight 864). Every section hangs its parts on those columns so left edges align from nav to footer.
- Split the work in each section: the outer element carries background and vertical padding; the inner container carries width and `padding-inline` alone. Writing the `padding` shorthand on the inner one quietly cancels the vertical rhythm. A full-bleed band swaps the background and keeps the same container.

## Sizes

| Role | At 1440 | Element |
|---|---|---|
| Hero headline | 84px | h1 |
| Long hero headline or statement | 60px | display-small class |
| Section heading | 52px | h2 |
| Item title | 25px | h3 |
| Lead (line under a heading) | 21px | lead class |
| Body | 16px | p |
| Label, caption, meta | 14px | small, figcaption, th |

- Section headings below 40px at 1440 are the usual reason a page reads as unfinished (gate 78). The hero headline is roughly 1.5 times the section heading, which is roughly double the item title.
- Spacing: heading to its line 16–24px; heading block to content 48–64px (40 if compact); grid gutter 32px sideways and 48–64px vertically; cards and wells pad 32–40px.
- Fluid sizing and tokens for the sibling system are in `../taste/system.md`. Adopt one scale, never both.

## Rhythm between sections

- Mix the gaps: 120, 144 and 176px (gate 59). A band, meaning a change of paper, pads 120px above and below.
- Mass earns space. 144px frames a 700px section but leaves a hole beneath a 200px one. If a page feels empty, enlarge the heading, the visual or the section's content; do not shrink the gap.
- Use 6–9 sections counting hero and footer, or five for a short brief and never fewer. Page height is a result of content: about 5,000–8,000px with pictures and a full brief, 3,000–4,000px for a short one. Do not pad toward a number.

## What a section is

One section presents one thing well: the menu, the lineup, the newest issue, the product in use, the room, the price. Choose the content first, then the composition.

- **Heading block.** Keep the h2 to six words at most, set at section size, with no more than a single lead-size line below it. Place it on columns 1–6 or 7, or split it (heading on 1–5, line on 7–12, baselines matched). Centre it only above a symmetric body, and never have more centred heading blocks than left-aligned ones. A section whose content announces itself (menu, timetable, track list, the product's own screen) can skip it.
- **No more than two neighbours share a skeleton.** Heading, body, heading, body repeated reads as a template however good each body is.
- **The body spans the width.** Make the widest row span ten columns of the twelve (gate 77). A narrow text column beside an empty right half is the signature of a sparse page; fix it by adding a visual, splitting the row or turning it into a statement.
- **The body has weight**, from any one of these: a visual 360px or taller; 3–4 items across; a list or table with at least three rows over ten columns; a working control built on the brief's facts; a statement at section size or bigger. A heading plus a paragraph is only a heading block.
- **Splits stay balanced.** Align the text and visual centres within 60px, and keep at least four fifths of each row occupied.
- **Height.** Typically 520–900px. Below 360px is for bands only (call to action, logo row, statement), at most two per page.

## Compositions

These are layouts, not components. Build each from the theme's material and the brief's content. Use 3–6 per page and never the same one twice in sequence (single-composition shapes instead vary ratio and side between neighbours).

1. **Split.** A visual at least 440px tall on columns 6–12 or 7–12 (portrait for products, 4:3–4:5), with text beside it: heading, line, and 2–4 short facts or a single action. Flip sides at most once; between two splits change the proportion (5/7, 4/8, 6/6).
2. **Showcase.** After the heading block, one full-width visual (16:9–21:9, 560px minimum). At most two smaller visuals under it, 8/4 or 7/5. Three equal frames are out.
3. **Grid.** Three or four items in a row (or a two-by-two): plans, products, rooms, dishes. Each has a photo, a big figure or a title large enough to carry the cell, then a line. Same heights, tops aligned, 240px or taller. No empty frames, stock portraits or icon tiles above headings.
4. **Bento.** Four to six tiles on a six- or twelve-column base with varied spans, rows of 280–360px, at least two tiles holding a visual, one clearly leading.
5. **Rows.** Between 3 and 5 full-width rows divided by hairlines, 72–120px each, title in columns 1–5 and its line or figure in 6–12. Fits FAQs, indexes, timelines and price lists.
6. **Table.** Full width, 4–5 rows of 56–72px, tabular numerals, the naming column a weight heavier.
7. **Figures.** Three or four genuine numbers at small-display size with labels underneath, divided by vertical hairlines. Use only figures the owner gave; never compute one from another.
8. **Steps.** 3–4 stages side by side, each with a real `<ol>` numeral, a title and a line (plus a visual when you have one), or a vertical sequence with a visual for every stage. Only for a process the visitor really follows.
9. **Statement.** A single sentence across 8–10 columns in 2–3 lines, section size up to display, with a credit or one action. Once per page.
10. **Band.** A full-width stripe in a different paper holding whatever the visitor needs at that point, such as free table times, the buy box, app-store buttons next to a screen, or the next date and the address. Not an email field by default.
11. **Form.** Heading block and 2–4 facts on one side, fields across 6–7 columns on the other; each input 48–56px tall; a single primary action.
12. **Rail.** A horizontal strip running past the container edge (dates, issues, products) with five or more items, the next one clipped, touch and keyboard scrolling, snap points, and no arrows beyond two items.
13. **Pinned.** A visual held sticky on 6–7 columns while 3–4 short panels scroll opposite, each changing the visual's state. Static below 60rem.
14. **Switcher.** A single area toggling between 2–5 states through a segmented control (lunch against dinner, monthly against yearly). All states hold real content, and the first renders without script.
15. **Index.** A tight list for scanning, 6–20 rows, one column per fact (issue number; project, year and client; episode and runtime), filterable if useful, with the first row enlarged.
16. **Schedule.** Times plotted against place or day (two festival days, a timetable of classes for a week, opening hours drawn as a strip), with the slot happening now or next highlighted. Reserve for times visitors plan around.
17. **Offer.** What is for sale, with what a buyer needs right then: photo or screen, options, price, action, one line on delivery or terms.

Under 60rem, compositions fall into reading order, heading block ahead of body. Splits show text before the visual; grids use two columns and then one under 40rem; a bento starts with its lead tile; rails stay rails; pinned pairs release; a schedule gets a column for each day. Visuals keep ratio but lose minimum height. Only a rail or a labelled table may scroll sideways.

Local-business compositions (opening-hours strip, map and directions, quote form, priced service list) are covered in `../taste/sections.md` and `../taste/place-pages.md`. Offer, Schedule and Band above are the same ideas at page-shape level.
