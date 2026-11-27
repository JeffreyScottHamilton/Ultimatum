# Page plans by site kind

Read after the copy is written and before building: classify the site, then plan it one line per section.

## Classify

Decide the site kind first and write it in the markup: `<html data-kind="software">` plus `<meta name="site-kind" content="software">`. The kind decides which tools are allowed.

| Brief looks like | Page type | Kind |
|---|---|---|
| SaaS, developer tool, AI product, fintech app | software | tech |
| A game, studio or launcher | software | gaming |
| Robots, devices, chips, vehicles, hardware | product | tech |
| Goods you buy: furniture, bikes, cosmetics, food brands | product | product |
| Agencies, studios, trades, clinics, consultants, lawyers | service | service |
| Cafés, bars, bakeries, restaurants, guesthouses, shops, florists, bike shops, local studios | place | place |

- The door decides: a maker who opens a shop, teaches classes or sells over a counter is a place.
- Tech kinds (software, gaming, tech hardware) may use effects, scenes, loops, CSS grounds and dark pages, within the budgets in `grounds-and-effects.md`.
- Every other kind gets photographs, flat colour, type, real icons, one moment and the hover layer. Nothing else moves.

## Plan

Write the plan before any markup:

```
kind: place / café
deal: nav-split · footer-visit · close-photo · rhythm space · buttons soft · mark initial
hero      | what we are and where     | shopfront photo   | place hero | 1
visit     | hours, address, call      | counter photo     | visit      | 1
menu      | coffee and food with prices | strip of four   | offer      | 2 (2 at 768)
place     | the back room for groups  | pair              | place      | 1  | moment: address
close     | book a table              | terrace photo     | close      | 1
```

Fields per line: id, idea in plain words, the picture, the section recipe, screens (plus tablet count if different), and the moment if this section holds it.

- Order the sections like a short story: name the thing, show it working, back it with proof, let the reader look around, then make the ask.
- Optional parts go in brackets, in page order.
- Each plan line names its picture so nothing is shown twice.

## Rhythm

- Neighbouring sections never share a layout. Card layouts at most twice per page.
- On software, product and service pages, a calmer section follows at most two visual ones, and the last third of the page stays calm.
- Rhythm, dealt from five: **space** (a single ground throughout; space alone parts the sections); **surface-pairs** (a run of one or two sections moved onto a second surface); **dark-band** (from the middle of the page on, one inverted section that holds the best picture); **media-band** (a full-width photograph section around the middle; not for places); **brand-band** (products only, somewhere in the later half).

## Deal lists

Deal, don't choose by taste. Run:

```
ult design deal "<trade or brief>" --kind software|game|product|hardware|service|place [--no-photos] [--footage] [--css tokens.css]
```

It deals one palette from 66 contrast-checked presets (body text at 7:1 and secondary text at 4.5:1 on both page and card, button labels at 4.5:1, the accent at 3:1 against the page; it says whether the accent may also be link text), one type pairing from the font table, a hero the kind allows, the parts below, and for tech kinds two section grounds that never clash plus a page ground. Brief words steer the palette and type toward matching trades and moods; a history in `.ultimatum/deal-history.json` keeps each pick out of the next few pages of the same kind. `--seed N` repeats a deal; `--fresh` ignores the history. `--no-photos` swaps photo-led parts as in the fallbacks below; the film hero is dealt only with `--footage`.

Write the result on plan line 2. Re-deal one part only when its use doesn't fit, and note why. The table is what the script deals from:

| Part | Software | Gaming | Product | Service | Place |
|---|---|---|---|---|---|
| nav | mega, cards, centre | mega, centre, cards | centre, cards, plain | mega, split, centre | split, plain, cards |
| footer | dark, statement, columns | dark, statement | columns, dark | visit, dark, columns | visit, columns |
| close | type, word | word, type | photo, type | type, photo | photo, word |
| rhythm | dark-band, surface-pairs, space | dark-band, media-band, space | brand-band, space, surface-pairs | surface-pairs, dark-band, space | surface-pairs, space, colour-band |
| buttons | solid, arrow, block | solid, block | solid, pill, tonal | solid, tonal | solid, pill |
| radius | sharp or soft | sharp | soft or round | soft | square |

`arrow` puts an arrow on the one button that moves the reader on, never on every button and link (house lint).

Fallbacks without photographs: nav-cards becomes nav-split or nav-centre; close-photo becomes close-word without the name; media-band becomes space (games keep a setting photo); a place hero becomes a statement hero on the brand ground.

## Software

Plan: nav · hero · (docked logo row) · app-frame · two or three feature sections · (integrations diagram) · proof · pricing or comparison · FAQ · close and footer.

- Pictures: the client's live screens, otherwise UI fragments rewritten to the product's own subject (`cards-and-ui.md`); diagram cards; real tool icons.
- Integrations: a fan-in or hub diagram card; an icon grid only for nine or more tools named in the brief.
- Proof only when the brief supplies a quote or figure; otherwise the calm section is pricing or FAQ.
- Never: a render of some object standing in for the real product, the product chopped into small bits strewn over coloured panels, or stock shots of people looking at screens.
- App scope for the real product (sign-up, onboarding, dashboard, billing, checkout) is built with `../../website/craft.md` and `accessibility.md`; the marketing page links into it with the same action words.

## Product

Plan: nav · hero · the range, no later than section three · 2–3 sections on features · a spec table or comparison · proof · visit-map if relevant · up to 5 FAQs · the order section as the final section · close · footer.

1. **Big.** At least twice (the hero plus one other section) the product takes 80–100% of the frame's width, runs off an edge, or covers 8+ columns. Cut-outs and renders stand directly on the page ground without a box. A medium-sized product inside a rounded grey panel set on grey is out.
2. **Whole product three times at most,** a different picture each time. Other sections show use, parts, people or a diagram. A smaller copy, recolour or mirror counts as the same view.
3. **Show every promise.** "Takes four crates" needs a picture of four crates, or the line goes.
4. **Compositions** per picture section, neighbours differ: bleed (the product across the viewport), pair (two views, one ratio), trio (whole, part, detail), strip (4 close-ups, one per part named in the specs), tall-small (use shot tall, detail small), split (text and one big picture, once, never right after a bleed).
5. **Swatches swap the picture.** Every colour offered appears at least once; a colour the photos can't show stays a named swatch and goes on the shot list.
6. **No fact twice.** A three-figure row takes the selling numbers (for example load, range, price); spec rows take the rest.
7. **Hover:** linked cards lift 2 px and their picture zooms 1.03 (`motion.md`).

- All sections share a single flat ground except one, which takes a contrasting ground and the best view of the product.
- Prices only "from" on cards or in a table, only from the brief. No monthly plan switch.
- Only a technical product may use the single effect. Renders appear only if the brief requests 3D (`objects.md`).
- No photographs from the client? Borrow licensed shots of a similar item (`photos.md` § Stand-ins); the hero is a photo hero, the order card comes last.
- Never: photographs of something else, app screens the product lacks, logo rows, tabs, or copy apologising for missing material.

Checkout scope: the order section links to the real cart or payment page. Show total price with tax and delivery before the final button, allow review and correction (WCAG 3.3.4), and keep the same action words from product card to confirmation.

## Hardware

- Its own photos; else stand-ins of the same machine at work, plus CAD, exploded-view or film slots for the client's files.
- A split hero whose only content is an order form is not allowed.

## Game

Plan: nav · named hero · trailer frame · full-bleed world sections · screenshot strip (three to five) · systems diagram · platforms · press · FAQ · close and footer.

- The `h1` names the game (40 characters at most), or the client's wordmark sits over a genre `h1`. A page that never names its game reads as abstract art; in the source's own tests such a page scored clearly lower than one with a date, a world and feature cards.
- The lead or a line under the hero gives the launch date or status from the brief ("Coming to PC"); never an invented date.
- With key art: key art and in-engine shots run full bleed under one grade. The world and crew carry the page; the hero object is shown complete in the hero and in no more than two other sections.
- Without art: a type-led hero over a photograph of the game's kind of setting, three to five frames in one light with nothing readable, the widest as a full-bleed world section. Every stand-in is listed with the art that should replace it.
- One shader effect may sit behind words in its own section, never on the photographs.
- Platforms: use official store marks only under each brand's guidelines (Steam, PlayStation, Epic); otherwise name the platform in text.
- Never: UI fragments or dashboards, stock players at screens, drawn SVG or empty panels in place of the world, an effect or statement hero where key art belongs.

## Service

Plan: nav · hero · services list (prices from, when given) · work grid of three to six photos or a photo pair · steps · people row · proof quote · (pricing) · FAQ · close and footer.

- Pictures: the work, the team and the rooms, one or two per screen. Real icons only for tools the firm really uses.
- Quotes and call-backs are the main actions for trades: a quote form and a `tel:` link in the header.
- Never: product UI the firm doesn't run, stock handshakes, logos of invented clients, or tabs.

## Place

Full rules in `place-pages.md`. Length follows the number of usable photographs:

| Photographs | Page | Screens | Sections |
|---|---|---|---|
| 12–20 | full | up to 6 | hero, visit, offer, place, orders or booking, close and footer |
| 8–12 | compact | 4–5 | hero, visit, offer, (place), close and footer |
| under 8 | short | 3 (2,700 px at 1440) | hero, one visit-and-offer section, close and footer |

## Local business facts

- Demo addresses: street and district only, no house number, so no real door is implied.
- Demo contacts use `.example` domains (RFC 2606) and never a real-format phone number. List every stand-in in the report.
- Real facts that earn trust: licence number, area served, years trading, owner's name and photo, a link to independent reviews. Only from the brief.
