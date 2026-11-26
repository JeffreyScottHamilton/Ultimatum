# Effect parts

Read on a tech page when an effect should live inside one element (a headline, button, ring, chart or feature-card panel) rather than behind a section. The page budget and catalogue are in `grounds-and-effects.md`.

## Parts

An effect can also live inside one element on a tech page: a feature card's panel, an icon tile, the area under a chart, a chip, a ring border, the fill of a button, or the letters of a headline. Each part starts only near the screen.

- **Ways to show an effect inside an element:** fill the glyphs (an overlay beside the text, never inside it, so the text stays real), windows (one canvas seen through many shapes), a ring (a 1.5 px border), or a soft glow behind one object.
- **Every WebGL part is the page's one effect.** Its place is the hero, the data-visual frame, or the section of a dealt moment; it never shares the screen with a live hero ground. Painted 2 × 2 panels are still card grounds.
- **Everywhere else stays quiet:** grain on chips holds still; the recommended plan alone gets a ring; a search box glows just while it has focus; a page has a single lit border.
- A glow is allowed a single time: still, on a dark ground, behind the main object of the hero, and kept off text and away from buttons. Transitions that play once (crack, melt, tile flip) live in the data-visual frame and fire a single time, either when clicked or as the hero is revealed.
- Ray marching belongs only to a dark hero, rendered at 50% resolution. Dither and halftone appear only as still grounds and never over a photograph.
- Scrolling moves nothing; cards never move by themselves.

| Part | Use for | Not for |
|---|---|---|
| headline fill | hero or closing line, 2–3 filled words | body text; two filled lines on one page |
| stat fill | stat-sized proof figures taken from the brief, two to four of them | made-up figures, count-up animation, small type |
| button fill | the one primary call to action, low-contrast grain moving only while pointed at | every button |
| prompt box | hero prompt for an AI or developer product | ordinary forms |
| search glow | docs or command search, only while focused | site search on a shop |
| tab indicator | a product tour or dashboard preview | navigation |
| icon tiles | glyph-drawn tiles in a grid of features | logos of brands |
| spotlight cards | a row of plain feature cards | a page with another pointer effect |
| globe | real global reach | local businesses |
| street map | a visit section for a street the brief gives, baked still | anything without a place |
| area chart | a single measure tracked across time | ornament with no figures behind it |
| bars | monthly figures on a labelled scale, 16 bars at most | trends without a scale |
| photo with copy | the client's own photo in colour | mood stock, filters |
| avatar ring | calls, presence or a team list | static team grids |
| pricing border | the recommended plan | every plan |
| progress fill | an import or setup step inside a product window | page loaders |

- In type (letters, digits): on dark or colour pages a still aurora-curtains or silk-folds; on light pages stat digits take a simple ink fade only. Type never carries line-engraving, halftone-screen, caustics or fluted-glass.
- Inside small shapes: still low-contrast grain. No silk, glass or metal sheen.
- In charts: still ruled-grounds, or an accent fade beneath the line; still grain for bars. Never grid-pulse (it blinks at random) or halftone-screen in a chart.
- Pass each effect only its own parameters. Values tuned for one look blank on another.
- Fixed hues only where nature sets them: a blue sky over grass, a gold horizon at dusk, blue water and green parks on a map.
- Numbers and names come from the brief; a missing figure is left out, never invented or tagged "sample".

## Feature-card panels

Four cards in two rows. Each has a panel inset by 8 px (`cards-and-ui.md` § Depth); the panel shows a still, bright ground with a single product window that runs off its lower edge.

- Ground: grain-gradient, or (by default) painterly-landscape, drawn once as a picture; ruled-grounds only for a technical panel with no UI.
- Give each panel its own light and composition (horizon, side, slope) so no two look alike. A grid of four mixes lights, e.g. day, grain, dusk, meadow:
  - **day:** layered hills under a pale sky, the hills graphite when the accent is warm and blue-grey when it is cool.
  - **dusk:** a deep-blue sky, gold along the horizon line only, and dark hills whose ridge catches the light.
  - **meadow:** a field in sun, a distant blue ridge, and a clear sky that lightens toward the horizon; at most once in a grid.
  - **grain:** for a cool accent, a deep ground; for a warm accent, a pale warm one.
- The window demonstrates the feature using its true labels (say, an invite, a payout list, a checkout, an invoice) and runs out of the panel with no empty space below its last row. At most two panels run a short pointer demo, one per row.
- Rejected: a small dialog on empty ground; an orb ground; a landscape in the accent hue only (it reads as a filter); a warm accent on a dark ground; a complementary accent on a colour page.

