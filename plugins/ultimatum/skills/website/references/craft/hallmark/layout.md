# Layout: canvas, sizes, rhythm, sections and compositions

Read when planning how every section sits on the page. Numbers are for a 1440 x 900 window unless stated. Heroes and whole-page rules are in `hero-and-page.md`; the 17 compositions are also a table, `../../../../../data/craft/hallmark/compositions.csv`.

## The canvas

- One container, centred and capped: 1440px wide with a 64px gutter, so content is 1312px at 1440 and stays 1312 at 1920 while the gutters grow (gate 44d).
- Twelve columns inside it with a 32px gap: one column 80px, four 416, six 640, eight 864. Every section places its parts on those columns so left edges line up from nav to footer.
- Each section: the outer element owns background and block padding; the inner container owns width and only `padding-inline` (a `padding` shorthand there silently zeroes the rhythm). A full-bleed band changes the background and keeps the container.

## Sizes

| Role | Size at 1440 | Element |
|---|---|---|
| Hero head | 84px | h1 |
| Long hero head or statement | 60px | display-small class |
| Section head | 52px | h2 |
| Item title | 25px | h3 |
| Lead (the line under a head) | 21px | lead class |
| Body | 16px | p |
| Label, caption, meta | 14px | small, figcaption, th |

- A section head under 40px at 1440 is the commonest reason a page looks unfinished (gate 78). Hero head is about 1.5 times the section head, which is about twice the item title.
- Head to its line: 16 to 24px. Head block to content: 48 to 64px (40 when tight). Grid items 32px across, 48 to 64px down; a card or well takes 32 to 40px padding.
- Our own responsive sizing and tokens are in `../taste/system.md`; use one set, not both.

## Rhythm between sections

- Gaps of 120, 144 and 176px, mixed (gate 59). A band (change of paper) takes 120px padding top and bottom.
- Space is earned by mass: 144px frames a 700px section and is a hole under a 200px one. An empty-looking page wants a bigger head, a bigger visual or a fuller section, not a smaller gap.
- Six to nine sections including hero and footer; five for a thin prompt, never fewer. Height follows content (about 5,000 to 8,000px with pictures and a full prompt, 3,000 to 4,000 on a thin one); never pad toward a height.

## A section

A section is one piece of content shown at its best: the menu, the lineup, the latest issue, the product at work, the room, the price. Decide the content, then the composition.

- **Head block:** an h2 of six words or fewer at section size, at most one line beneath at lead size, on columns 1 to 6 or 7, or split (head on 1 to 5, line on 7 to 12, baselines aligned). Centred only over a symmetric body, and never more centred head blocks than left ones. A section whose content names itself (a menu, timetable, track list, the product's screen) may go without one.
- **Never more than two neighbours with the same skeleton;** head-block, body, head-block, body reads as a template however good each body is.
- **The body fills the width:** its widest row reaches ten of twelve columns (gate 77). A narrow text block with the right half empty is the sparse page's signature: pair it with a visual, split it, or set it as a statement.
- **The body has mass:** a visual 360px tall or more; three or four items across the width; a list or table of three or more rows across ten columns; a working control on the prompt's facts; or a statement at section size or larger. A head and a paragraph are a head block, not a section.
- **A split balances:** text and visual centre on each other within 60px and neither column leaves over a fifth of the row empty.
- **Height:** usually 520 to 900px; under 360px only for a band (call to action, logo row, statement), twice a page at most.

## Compositions

Layouts, not components: build each in the theme's material and the prompt's content. Use three to six on a page and never the same one twice in a row (except in one-composition shapes, where neighbours change ratio and side).

1. **Split:** text (head, line, two to four short facts or one action) beside a visual on columns 6 to 12 or 7 to 12, 440px or taller, 4:3 to 4:5 (portrait for a product). Swap sides once a page at most; change the ratio between two splits (5/7, 4/8, 6/6).
2. **Showcase:** head block, then one visual across all twelve at 16:9 to 21:9, 560px or taller; under it at most two smaller visuals at 8/4 or 7/5, never three equal frames.
3. **Grid:** three or four items across (or two by two): plans, products, rooms, dishes, each with a photo, a large figure or a title big enough to carry the cell, then one line. Equal heights, aligned tops, 240px or taller. Never empty frames, stock faces for people or icon tiles over headings.
4. **Bento:** four to six tiles on six or twelve columns in mixed spans, rows 280 to 360px, two tiles at least with a visual, one clearly the lead.
5. **Rows:** three to five full-width rows parted by hairlines, 72 to 120px each: a title on columns 1 to 5, its line or figure on 6 to 12. Good for an FAQ, index, timeline, price list.
6. **Table:** full width, four or five rows of 56 to 72px, tabular numerals, the naming column one weight heavier.
7. **Figures:** three or four real numbers at the small display size, labels beneath, parted by vertical hairlines. Only figures the user gave, never one derived from another.
8. **Steps:** three or four stages across, each a real `<ol>` numeral, a title and a line, with a visual where the material has one; or a vertical run with a visual per stage. Only for a process the visitor really goes through.
9. **Statement:** one sentence over eight to ten columns in two or three lines at section size up to display, with attribution or one action; once a page.
10. **Band:** edge-to-edge change of paper holding what the job wants there (next free table times, the buy box, store buttons beside a screen, next date and address). Never an email field by default.
11. **Form:** fields on six or seven columns beside the head block and two to four facts, inputs 48 to 56px, one primary action.
12. **Rail:** a horizontal run past the container's edge (dates, issues, products), five or more items with the next one cut by the edge, scrollable by touch and keyboard, snap points, no arrows past two items.
13. **Pinned:** one visual held sticky on six or seven columns while three or four short panels scroll on the other side, each changing the visual's state; static under 60rem.
14. **Switcher:** one area with two to five states behind a segmented control (lunch or dinner, month or year); every state real, the first visible without script.
15. **Index:** a dense scannable list of the prompt's items with facts in columns (issues, projects with year and client, episodes with length), optionally filtered, 6 to 20 rows, lead row larger.
16. **Schedule:** time against place or day (a two-day festival, a week of classes, opening hours as a strip) with the current or next slot marked; only for times the visitor plans around.
17. **Offer:** the thing for sale with what a buyer needs at that moment: photo or screen, options, price, action, one line of delivery or terms.

Under 60rem every composition stacks in reading order: head block, then body; a split's visual after its text; a grid two across then one under 40rem; a bento's lead first; a rail stays a rail; a pinned pair unpins; a schedule becomes a column per day. Visuals keep aspect ratio and lose minimum height; nothing scrolls sideways except a rail or a labelled table.

Local-site compositions (opening hours strip, map and directions, quote form, service list with prices) are in `../taste/sections.md` and `../taste/place-pages.md`; the Offer, Schedule and Band above are the same ideas at the page-shape level.
