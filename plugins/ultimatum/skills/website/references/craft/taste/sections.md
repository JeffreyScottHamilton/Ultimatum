# Section recipes

Read when building any section after the hero: navigation, proof, features, app screens, offers, local-business blocks, forms, pricing, FAQ, close and footer. Which sections a page gets, and in what order, is in `page-plans.md`; place-specific recipes are in `place-pages.md`.

## Rules for every section

- One idea, one `h2`, and at most one action besides the main one. Pairs of buttons only in the hero or a product's compare-and-buy row.
- Every section shows real material: a photograph, a portrait, a diagram card, the client's own UI, the product's real icons, or, on tech pages only, the page's single effect. Sections without a picture are allowed only for a price list, FAQ, spec table, booking form or a dealt statement moment, each once, and two of them never sit next to each other.
- A picture takes at least half a tile: 50/50 in a split, or a whole screen as a layer.
- A quote needs the speaker's face beside it, or it folds into the section above.
- Short blocks (a quote, a logo row, a fact row, a short FAQ) under about 495 px tall join the previous section, placed last in it with 64–96 px of space above. An FAQ taller than that becomes its own section.
- Card layouts (2×2, bento, three cards, split card, open tiles) appear at most twice per page, and neighbours never share a layout.
- One split pair per page: text left, visual right, top-aligned; text first on phone.
- Repeat the same scaffold (heading position, padding, ground logic) so the reader learns it once.
- The main action uses the same words everywhere (nav, hero, close or booking, phone bar) and is a filled button nowhere else.
- Every nav word, button and footer link points at an `#id` on the page; the logo points at `#top`. Never `href="#"`, `/contact` or a made-up path. Privacy, terms and imprint get small real pages or are left out.
- At 390 keep the desktop grounds, photographs and order; each photograph follows its text.
- At 768 and 820, re-plan screens for stacked content and write it on the plan line ("2 at 768").
- Use only the system's classes; page-specific CSS lives inside a visual, never on layout.

## Navigation

- Fixed, opaque header with a 1 px hairline. No blur, no shrinking on scroll, no hiding, no shadow.
- Logo: the client's SVG; otherwise a dealt mark, an initial, or a plain wordmark. A mark sits beside the name in nav and footer.
- Four to six one-word links at 15 px / 500. Place pages use place words (Menu, Visit, Rooms, Order).
- The primary action as a button at the right; a second action only as a plain word.
- `aria-current="true"` on the word for the section in view, shown by a 2 px bar under it; only one at a time.
- Variants, dealt per page:
  - plain: logo left, links, button right.
  - centre: logo left, four or five centred words that never wrap at 1024.
  - split: logo centred, words either side (shops, places); its menu word may open photo cards.
  - mega: hover panel of grouped feature columns with short muted lines and one picture card (software).
  - cards: a panel of two to four picture cards; on a place, three photo cards with a price.
  - tone: a dark nav on a dark hero (tech only).
- Panels open on hover after 150 ms (fade plus a 6 px drop), on click, and on Enter. The trigger is a `<button aria-expanded>`; Escape closes and returns focus. The click on the word itself goes to its section.
- 640–1023: the primary button stays visible beside a 44 px menu button.
- Under 640: the menu button opens a full-screen sheet with 56 px rows; on a place it also shows the street and today's hours.
- Disclosure pattern: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/

## Hero copy

Layout and hero types are in `layout-and-heroes.md`; the words:

- `h1` of two to eight words that names the category and who it is for. No slogan.
- One lead of 15–30 words carrying one hard fact (a price, a time, a place, a number from the brief).
- Primary button is verb plus object ("Book a table", "Start a free trial") and repeats word for word in nav, close and phone bar.
- A place shows today's hours in the hero or the screen right after it.
- App store links are text links, not badge images, unless the client supplies the official badges.

## Proof

Proof comes as small, precise items taken from the brief: a press mention, a rating line, a figure with a footnote, a quote with a name and a photo, logos the owners allow. Never big stat-number rows, filler stat strips, check-icon lists or logo walls. Nothing invented (see `copy.md`).

- logo-row: up to six real logos in one still row, one height, in their own colours or one neutral tone.
- quote-stat: a named quote of 40 words or fewer with a portrait, beside one sourced figure.
- customer-proof-row: three customer cards, each with name, role, one line and one figure.
- people-row: four portrait tiles of the real team; never stock faces.
- timeline-rail: four dated moments with the newest in the accent colour (software and service history only; never on a place).

## Features

- product-statement: a paragraph whose second half is in muted ink, a cut-out photo, three facts.
- features-2x2: four cards, each with a panel showing the feature.
- bento: one wide card and one narrow, then three small, all panels one height.
- split-text-left: text with three facts beside one or two overlapping frames.
- tabs-tour: three to six tabs that switch one fixed-height frame on click only (never on a timer). Software only. Follow the tabs pattern: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
- chapter: one feature area with a wide frame and four named parts.
- steps: three numbered cards, no arrows between them, never chained to another steps block.
- integrations-grid: real tool icons; use 72 px tiles only when the brief lists nine or more tools, otherwise a diagram card (`icons-and-diagrams.md`).
- screenshot-strip (games): three to five uncaptioned 16:9 captures.

## App screens

The app-frame shows the product big, in one window across the wrap: a list pane beside the open item. Only the open pane may loop.

```html
<section id="product" class="sec">
  <div class="wrap">
    <h2>Review every change in one place</h2>
    <figure class="app" role="img" aria-label="Review queue with an open pull request and its comments">
      <div class="app__bar"><span></span><span></span><span></span></div>
      <ul class="app__list" role="list">
        <li aria-current="true">Fix rounding in invoice totals</li>
        <li>Add retry to webhook sender</li>
        <li>Move fonts to self-hosting</li>
      </ul>
      <div class="app__open"><!-- open item: diff, thread, status --></div>
    </figure>
  </div>
</section>
<style>
  .app { margin: var(--head-gap) 0 0; display: grid; grid-template: auto 1fr / 2fr 5fr;
         height: min(620px, 70svh); border: 1px solid var(--line); border-radius: 16px;
         background: var(--surface); overflow: hidden; }
  .app__bar { display: flex; gap: 6px; grid-column: 1 / -1; border-bottom: 1px solid var(--line); padding: 12px 16px; }
  .app__bar span { inline-size: 10px; aspect-ratio: 1; background: var(--line); border-radius: 50%; }
  .app__list { border-right: 1px solid var(--line); padding: 8px; overflow: auto; font-size: 14px; }
  .app__list li { padding: 10px 12px; border-radius: 8px; }
  .app__list [aria-current] { background: var(--bg-alt); }
  @media (max-width: 1023px) { .app { grid-template-columns: 1fr 2fr; } }
  @media (max-width: 639px)  { .app { grid-template-columns: 1fr; } .app__list { display: none; } }
</style>
```

- Fill it with the client's own screens or rewritten fragments (`cards-and-ui.md`). Never a generic dashboard, never stock people at screens.
- Pane pairings by product type (code review, support desk, docs, CI, booking) are rows in `../../../../../data/craft/taste/patterns.csv`.
- For dashboards and admin views inside the real app, the craft is in `../../website/craft.md`; this frame is only the marketing picture of it.

## Products and services

- line-up: model tiles with photo, name and "from" price; one ratio.
- rooms-list: room tiles with photo, seasonal "from" price and a book action.
- services-list: rows of name, one line and "from" price, beside one photograph. No icon cards.
- peek-list: rows that swap one photograph on hover, focus or tap (each row is a link or button, so keyboard users get the same).
- Prices come only from the brief: "from" prices on cards or a table. Otherwise "Price on request" or nothing.

## Local business

Calls, bookings, quotes and directions are the actions that matter. Make them one tap.

- Phone as a link: `<a href="tel:+15551234567">(555) 123-4567</a>`. Show it in the header on every page (same place each time, WCAG 3.2.6) and in the visit block.
- Directions link only when a street is known: `https://www.openstreetmap.org/search?query=<street>+<district>` (or the client's maps link). District only: "See the area".
- Quotes: a short form (job, postcode, photos optional, preferred contact) whose button says what happens ("Get a quote by Friday").
- A named booking system (the client's own) replaces the form; link or embed it, never rebuild it.
- Menus and price lists are text with visible prices, set beside a photo; never an image or PDF.
- Hours as a description list with the time zone, today marked, and an open-now line filled by script:

```html
<dl class="hours" data-tz="Europe/London">
  <div data-day="1"><dt>Monday</dt><dd data-open="08:00" data-close="17:00">8:00–17:00</dd></div>
  <div data-day="2"><dt>Tuesday</dt><dd data-open="08:00" data-close="17:00">8:00–17:00</dd></div>
  <div data-day="0"><dt>Sunday</dt><dd>Closed</dd></div>
</dl>
<p class="open-now" role="status"></p>
<script>
  // Mark today and say whether it is open now, in the shop's own time zone.
  const dl = document.querySelector('.hours');
  const fmt = { hourCycle: 'h23', weekday: 'short', minute: '2-digit', hour: '2-digit', timeZone: dl.dataset.tz };
  const parts = new Intl.DateTimeFormat('en-GB', fmt).formatToParts(new Date());
  const get = t => parts.find(p => p.type === t).value;
  const day = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(get('weekday'));
  const now = get('hour') + ':' + get('minute');
  const row = dl.querySelector(`[data-day="${day}"]`);
  if (row) {
    row.setAttribute('aria-current', 'date');
    const dd = row.querySelector('dd');
    const open = dd.dataset.open && now >= dd.dataset.open && now < dd.dataset.close;
    document.querySelector('.open-now').textContent =
      open ? `Open now until ${dd.dataset.close}` : 'Closed now';
  }
</script>
```

- Hours marked as assumed (`data-assumed`, see `copy.md`) get no open-now line. The list reads correctly with scripts off.
- visit-map: address, hours with time zone, and either a still map image with a pin or a shopfront photo. Never a live map embed by default (it is heavy and tracks visitors).
- Trust for a local firm: the licence or registration number, years trading, the area served, real reviews with a link to their source, a named owner photo. All from the brief.
- `Intl.DateTimeFormat`: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat

## Forms

One form recipe for the whole page (booking, contact, quote, sign-up).

- Posts to the client's real endpoint. Without one, use a `mailto:` on an `.example` address as a stand-in and list it in the report. Never `action="#"`.
- Fields 48 px tall, 14 px labels, 16 px input text (stops iOS zoom), one column, six fields at most. Never in a modal.
- Visible `<label for>`, right input types and `autocomplete`, paste allowed (`accessibility.md`).
- Errors only on submit: `aria-invalid`, a message tied with `aria-describedby`, focus the first bad field.
- One status line (`role="status"`). Show "Sending…" only if the reply takes over 300 ms. If sending fails, nothing the visitor typed is lost.
- Success only after a real answer from the server, saying when the reply will come ("We'll call you back today before 6 pm").
- Text fields instead of `type="date"` on pages not in English, where the native picker's language may not match.
- Sign-up and checkout forms add: password managers and passkeys work, no re-typing of known data, and money actions can be reviewed before they are final (`accessibility.md` § Forms, sign-in and checkout).

## Pricing

- pricing-three: three plans, the middle one featured by a border or ground (not a "most popular" badge unless the client has that data), a monthly/yearly switch that is a real toggle button with `aria-pressed`. Use CSS subgrid so feature rows line up across cards.
- pricing-two: free and paid.
- comparison-table: a real `<table>` with header cells and 48 px rows; on phone it becomes one stacked list per plan, never sideways scroll.
- Plan tables are for software. Products show "from" prices; places show menus and rooms.
- Prices, limits and trial terms only from the brief.
- Subgrid: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid

## FAQ

- Five to eight questions, answers open by default (no accordion on a page this short). Short questions, answers of one to three sentences.
- Mark up as headings and paragraphs, or a `<dl>`. If the list is long enough to need folding, use `<details>`/`<summary>`, never a custom accordion.

## Close

The closing section is one screen and is part of `footer.closing`:

- close-type: a large `h2` of eight words or fewer, one line, and a full-width extra-large button.
- close-photo: the action row above a client photo not used earlier, with no words on it.
- close-word: an `h2` with its button, and below them the client's name running the width of the wrap (capped at `12vw`).
- With no photographs, close-photo becomes close-word without the name.

## Footer

- One screen: row one is the dealt close, row two the link directory and legal row.
- footer-columns: quiet link columns that mirror the nav, contact as given, newsletter only if the client runs one, then the legal row.
- footer-dark: the one dark band, at the end.
- footer-visit (places and services with a door): the address large and linked to the map, one line on the way, hours with today marked, no button.
- footer-statement (tech only): an inset slab on a lit ground joining close and footer.
- Legal row: © year and legal name, privacy, terms, and an imprint only when company details are given. Photo credits as one line linking to the credits list.
- Social links only when the client supplies them.
