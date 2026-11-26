# Place pages: cafés, shops, guesthouses, studios

Read when the site kind is place (anywhere people walk in). It refines `sections.md` and `page-plans.md` for these pages.

## What a place page is

- Markup: mark the root `<html data-kind="place">`, add `<meta name="site-kind" content="place">`, and scope every place rule under `html[data-kind="place"]`.
- The page rests on three things: photographs, flat colour and type. Study well-run independent bookshops, bakeries and coffee roasters for feel; never copy their sites.
- Never on a place: effects, WebGL, canvas, CSS gradients, grain, glass, scenes, loops, counters, UI fragments, diagrams; cards for features or plans, accordions, tabs, toggles, rows of logos, fact strips, timelines, calendar cards, a map the brief did not ask for; unbriefed ratings, reviews, figures or quotes; words on photographs; rounded or filtered photos; a nav bar you can see through or that blurs; display type that is outlined, faded, blurred or tilted; carousels; any dark section other than the one brand band.
- Counting length: the nav is not a screen; the close-and-footer is one; a two-screen section counts as two.

## Photographs

- Photo counts per section, each picture different: one in the hero; one for the visit (none if there is a map); one for the menu; 2–6 for rooms; 4 for goods; 3, 1 or a wall for the place; 2–3 for orders or 1 for booking; one for the close.
- The hero is a photograph whenever any frame fits. A remote guesthouse may lead with its landscape.
- Never two sections built around one picture. Text beside a single photo happens once per page besides the visit block.
- Under eight usable frames (client's plus stand-ins) is the short page; eight to twelve compact; twelve or more full. These three names mean only these lengths.
- With no photographs at all: no mood stock, code-drawn ground, illustration, empty box or apology. Try a stand-in search first (`photos.md`); list the shots to take in the report.

## Compositions

Deal one for the offer and one for the place section; re-deal the place one while it equals the offer's.

| Id | At 1440 (1200 wrap) | At 390 |
|---|---|---|
| bleed | head row, then one 1440×560 photo across the viewport; once per page, never right after the hero | 4:5 crop, 390×488 |
| pair | two photos on span 6, one ratio (4:3 at 588×441 or 4:5 at 588×735), tops level | stacked, 342 wide, 24 apart |
| trio | span 5 at 4:5 (486×607), span 4 at 1:1 (384), span 3 at 4:3 (282×212), tops on one line | one 342, then two 165 |
| strip | square details, edge to edge: 4 on span 3 (282) or 6 on span 2 (180) | at most four, in pairs at 165 |
| tall-small | 4:5 tall photo on span 6 at the left line; text and a 1:1 span-3 photo on the right | text, tall at 342, small at 165 |

- In the offer, a strip runs under the menu groups; a pair or tall-small takes the photo slot beside groups narrowed to span 6.
- wall: head row, then photos edge to edge with 0–2 px gaps; two-up at 390; no names under them.
- story: 6/6, text left (a one- or two-line `h2`, then 3–6 lines at 20/30 on the people who run it), a 4:3 people-at-work photo right. Once per page.

## Type moment

One per page, ink on the page ground or the brand band only; never outline, pale, rotated or on a photo.

- address: street and district set large under the visit heading, `font-size: clamp(3rem, 2rem + 4vw, 6.5rem)`. Never an invented street.
- name: the close becomes close-word; the photograph moves to the place composition. Footer name capped at `12vw`.

## Hero

Fixed, never dealt (`layout-and-heroes.md` § Place hero). Copy: `h1` of 40 characters or fewer saying what and where; a sub-line of 80 characters or fewer with one fact; one main button.

A notice line (14 px, one number) may sit above the `h1` for a cut-off or holiday hours, repeated where that fact belongs. It never rotates.

## Visit

Always screen two, `id="visit"`.

- A panel on the alternate ground on span 6, beside a 1:1 or 4:3 shopfront or room photo.
- Panel: `h2` "Visit" top left; an open-now line at its right only with real hours; address at 20/30 linked to the map; `tel:` link only when a number is given; the week's hours as a list with today marked (`sections.md` § Local business has the script).
- Second button: if a street address is known and the primary action is not directions, "Get directions"; "See the area" for a district only; "Call" only with a real number.
- Up to two extra 44 px rows: step-free access, delivery area, check-in and check-out, repair turnaround, or "By appointment".
- With the address moment, the heading and street run across the wrap above the split, and the photo becomes 4:3.
- At 390: the panel first (24 px padding, address 18/28), then the photo at 342, 4:5 at most. Hours never live only in the footer.
- Map: only with a known street. A still map image in the photo frame with a pin; never a live embed, contour art or dot pattern. Map data must carry its attribution (OpenStreetMap: https://www.openstreetmap.org/copyright).
- Accessibility facts help real visitors: step-free entrance, accessible toilet, quiet hours. Ask the client.

## Offer: menus, rooms, goods, orders

- Head row: an `h2` of 40 characters or fewer (32/40; 24/30 at 390) on the left line, a 16 px line and a link at the right, 56 px above the content.
- Menu group: a 13 px weight-500 label with 12 px of air and no rule; rows with 1 px closing rules; name 16/24/500 left, price right in tabular figures (`font-variant-numeric: tabular-nums`), optional muted description.
- Menu rows 44 px (64 with a description); six rows with descriptions or eight without, the rest behind the head-row link; paired groups hold equal row counts. Text with visible prices; never an image, PDF, tabs or accordion. At 390, one column with the photos after the first group.
- List text is 16/24 at least (rows, descriptions, room facts, hours); 13 px only for group labels.
- Rooms ("Rooms and prices", with breakfast and check-in/out times on the side line): each room a 4:3 photo, name, facts, "from" price and "Book this room". Row layout: three on span 4 (384×288) or four on span 3 (282×212); at 390 one column 342×256, 48 apart. Side layout: the heading as the first cell; two rooms on span 4 (always side), three on span 3, four as a 2×2 on span 4 over two screens.
- Goods: 4 square cards (282, span 3; bouquets are 282×352, 4:5), each a link with a flat fill or hairline, showing just the name and price, plus an outline "Add" if it sells online. On a phone (390): pairs at 165, 4 or 6 in all, and below them one full-width button to the whole range. Never a swipe row.
- Orders (cakes, catering, events): below the head row, 3 order types on span 4. Each: a 4:3 photo, a hairline, a 13 px label, a title at 20/28, and body at 16/26 giving notice needed and whether it is collected or delivered. For florists' events, list what the enquiry should include (the date, the venue, how many guests, the budget).

## Booking

- A head row (e.g. "Book a room" / "Answers come within 24 hours."); below it the form on the second ground with 48 px padding, matched in height by a span-6 photo at 4:3 beside it.
- No photo, texture or glass under the form. A named booking system replaces it.
- Form rules are in `sections.md` § Forms.

## Close and footer

- close-photo: an `h2` of eight words or fewer, one line such as the hours, the main action, and a 1:1 photo not used above, with no words on it.
- On a colour band: the close sits on the brand ground with every word at 7:1 and the button inverted.
- footer-visit: the address large (32/40, span 7) and linking to the map, a single line of directions, no button; hours with today marked; nav row; legal row; name set wide (capped at `12vw`).
- footer-columns: Visit, Contact as given, nav words, delivery or check-in or newsletter, legal row.
- Credits: one footer line linking to the list, never one link per photo.

## Actions and motion

- One main action per screen. Transactions sit in nav, hero, booking or close, and phone bar. "Get directions" appears only in the hero, phone bar and visit.
- Nav word "Visit" points to `#visit`. The footer gives the address as a link, never a button.
- Phone bar: a single full-width button when the action is ordering or booking; if not, two buttons, "Call" and "Get directions". Hidden until the hero button scrolls away (`system.md`).
- Motion: hover only (underlines draw, photos zoom 1.03, cards lift 2 px, buttons press, arrows move 3 px). The hero enters once; on scroll only the dealt moment's section moves.
- Splits are 6/6, text left, top-aligned; text first on phone.

## Colour and type by trade

- One accent on the primary button, focus ring and colour-band close. Darken a client's accent as far as needed for 3:1 on the shape and 4.5:1 on its label, against both grounds.
- One surface band at most plus one brand band; flat colour only. The nav may use dark ink.
- Pairings: a serif display with a plain sans for bakeries, restaurants and guesthouses; one sans in two weights for shops; a softer sans for florists and studios. Display 400; text 400 and 500.

## Order by trade

- Café: the menu written out as text, with its own layout; the room as a story row or a composition; goods or beans only when they are for sale.
- Bakery: goods with prices; one order card per kind; process as a strip or trio on one screen; several shops as a ruled list with streets.
- Guesthouse: hero may show the region; visit (address moment fits); rooms; an unlabelled full-bleed of the house; booking; arrival and departure times.
- Shop or bookshop: latest arrivals as goods cards with Add; plain-text category links; a single story row; footer with each shop's address, hours and newsletter.
- Bike shop: visit; the workshop and how long repairs take; a ruled price list for servicing ending in "Book a service"; latest bikes cut out on white; brands as text; story.
- Florist: a notice line (where it delivers, order-by time, cost); screen two holds delivery and the visit; 4 bouquet tiles at 4:5 each priced "from"; 3 photos of events.
- Trades (plumber, electrician, builder) are services with a van, not places: see `page-plans.md` § Service.

## Short page

For under eight usable photographs. Three screens, 2,700 px at most at 1440, `data-page-mode="short"`.

- Hero, one one-screen section holding visit and offer, then close and footer.
- Set that section as plain type straight on the page ground, with no card or box around it: the offer as ruled text groups; visit as three span-4 columns (address, hours with today, contact).
- With one photo: groups and the photo in one top-aligned row, photo last. Three groups on span 3 with a 1:1 photo (282); two groups on span 6 with a 3:2 photo (588×392).
- Menu names fit one line beside their price on span 3 (about 24 characters); shorten longer ones. Equal row counts.
- Under 640: two screens, photo after the groups at 16:9.
- 640–1023: stays one screen (600–830 px content) with three groups and three visit columns across. With a photo: two screens (heading and full-width photo, then groups and visit).
- Nav: three or four words pointing at group ids (`#tableware`, `#classes`, `#visit`).
- Moment with a photo: picture-develops on the figure (needs half the wrap or more). Without a photo: one statement section of 12–40 words with word-highlight, making the page four screens (3,600 px).
- Drops: no place section, second offer, place composition, type moment or rooms layout. Write "not used" beside each on plan line 2. Without pictures: nav-split with no panel and close-word without the name; choose the brand band or the wide footer name, not both.
