# Imagery: what fills a page, slots, capturing the product, treating photos

Read on every page build before placing a single picture. A page looks made when it shows the real thing (the place, the food, the hands at work, the product running) and generated when it shows a gradient box, a drawing of a loaf or a heading with nothing under it. Our photo sourcing and credit rules are in `../taste/photos.md` and icon and diagram rules in `../taste/icons-and-diagrams.md`; this file adds the ordering, slots, capture and balance rules.

## What fills a page

Take the first that fits:

1. The user's own images and recordings, asked for up front. They win every slot.
2. Screenshots of the real product, taken by the build when the product can be reached: a URL, a running dev server, a project that starts with one command, an app on this machine (see Product).
3. The product built, only when there is nothing to capture yet.
4. Photographs from a licensed source, treated in the theme's way (see Placing photographs and `../taste/photos.md`).
5. Generated stills, only when the user asked and a generator is configured (`comp.md`).
6. Type at full scale, when the prompt is about words.

Which prompts want which:

- **A place, material, food, object, craft, event or people at work** (bakery, ski school, weaving studio, tailor, farm): photographs lead. The hero photograph is the largest thing on the first screen (full-bleed behind the head, or beside it at 60 to 75% screen height). Then two to four more, one large, each on its subject (an off-subject picture is cut, never kept to fill a count), with sections of material alone between them (a menu as rows, hours as a table, a statement, a form). Photos take a quarter to a third of the page.
- **Software:** the product leads and the hero visual is its interface. One or two photographs may set the scene when each passes the deletion test: remove it and the page loses a fact. A city at night, a laptop on a desk or an office building fails.
- **Words** (docs, API, CLI, type specimen, a manifesto): type and code carry it; one full-bleed photo band at most. A manifesto about something physical shows it.
- A photograph never stands in for a fact: numbers, names and claims stay in type, and a picture of a person never stands in for a customer, teammate or testimonial (F9).

## Library

Source's own approach: a vetted photo library queried by script. We do not ship that library (see `later.md`); use the user's photos first and our rules in `../taste/photos.md` for borrowed ones. What carries over:

- Never write an image URL from memory or take one from a stock site. Use only files the user supplied or ones you can name and credit (gate 76).
- Credit every borrowed photo in one footer line marked with a `data-credits` attribute (excluded from the word budget); some licences require it.
- Keep a responsive `srcset`, set `sizes` to the layout (`50vw` for a half, `100vw` full-bleed), crop with the frame: `aspect-ratio` on the slot, `object-fit: cover`, an `object-position` that keeps the subject in frame (MDN: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#srcset).
- The hero photograph is the LCP element: `fetchpriority="high"`, never `loading="lazy"`; every other image is lazy. A full-bleed frame needs a photo 2400px or more on its long side; smaller goes soft at 1920.
- A stand-in stays swappable in its slot with an alt-text hint naming what the real picture should show, listed in the handoff.

## Slots

A slot is any picture the user will replace: a `data-slot` name, a `data-alt` saying what belongs there, and a real size (an `aspect-ratio` or fixed height).

- A slot always shows something: the user's image, a borrowed photo, or the product built at full fidelity. Its wash colour exists only while a photo loads; a slot showing only its wash is an empty picture (gate 81).
- No visible placeholder labels ("your screenshot here", ratio notes, "sample" chips). The data attributes and the handoff carry that.
- A child that must survive the swap (a credit, a plate number) carries `data-keep`. Text over a slotted photograph sits in a sibling layer above it (`z-index` 2 or more), never inside the slot.
- Never more than four slots in a row, and never a set of frames for things the page has no pictures of (a team, venues): set those in type (gate 68).

A small slot-swap script, ours:

```html
<figure><div class="slot" data-slot="hero" data-alt="the shopfront at opening time"></div></figure>
<script>
  function fillSlots(map) {
    for (const [name, src] of Object.entries(map)) {
      const slot = document.querySelector(`[data-slot="${name}"]`);
      if (!slot) continue;
      const img = new Image();
      img.alt = slot.dataset.alt || '';
      img.onload = () => { slot.replaceChildren(img, ...slot.querySelectorAll('[data-keep]')); };
      img.src = src;  // a failed load leaves the stand-in in place
    }
  }
</script>
```

## Product

**Capture it.** If the product exists, the page shows it, not a mock. Find it in pre-flight: a URL in the prompt, a running dev server, a `package.json` with a `dev` or `start` script, an app on the machine, a path the user names. Start it (install only what its lockfile asks for, free port), put it in the state that tells the story (sample data, a real project open), then capture at 1440 x 900 and 390 x 844 at 2x. With Playwright (https://playwright.dev/python/docs/screenshots):

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h in [("desktop", 1440, 900), ("phone", 390, 844)]:
        page = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        page.goto("http://localhost:3000/")
        page.screenshot(path=f"shot-{name}.png")
    b.close()
```

Use `locator.screenshot()` for one element. Desktop apps on Electron expose a DevTools port to capture through; other apps use the OS screenshot tool; a phone app its simulator; a terminal tool is run and its real output set in a code block. Look at every capture before shipping: no personal data (names, emails, tokens, file paths), no error states unless they are the point, no debug overlays. Use several: the main screen in the hero, a detail cropped large, a second screen, the phone view. Stamp `imagery: screenshots n`; they are the user's own, so no credit.

**Frame it in the theme:** inside a slot with the theme's radius and an inset outline, never a drawn browser bar, device frame, traffic lights or notch (gates 47a, 47b). Crop to the part that sells, keep text legible at its displayed size (never upscale), never retouch. Mark the slot as a product picture (`data-kind="product"`) so it does not count toward the photo share.

**Build it only when it cannot be captured** (an idea, an unbuilt product): the hero visual is the main screen in HTML and CSS with real controls, at least eight elements, the prompt's nouns, the theme's surfaces and type, at the hero visual size. Sample values read as samples (`example.com`, "Example Kitchen", round amounts), never a claim (46a). It sits in a slot so the real screenshot replaces it, and the handoff names the screens to capture once it runs. Never build a mock of a product that could have been captured (84).

A working control (a calculator on the owner's prices, a booking form) is a fine section or close, once a page; not the default hero. For apps with sign-in, capture with a seeded demo account and never real customer data.

## Placing photographs

- **Big or not at all:** six of twelve columns and 440px tall or more, or full-bleed. A set of four or more may run smaller, each with its fact. Delete the picture in your head: if the screen says the same thing, it is too weak or small.
- **One subject per frame,** cropped tight, its weight leaning toward the text. Vary ratio (4:5 beside text, 16:9 or 21:9 across, 1:1 in a pair) and size (8 and 4 columns); equal frames only for a true set (three dishes, three rooms).
- **Balance:** below the hero photographs take at most a third of the page at 1440 (45% on photographic or portfolio shapes; product pictures do not count). Never two photograph-led sections in a row; follow a picture with a section the theme's type, rules, colour or the product carry alone. Software alternates product with type-led sections; word-led pages take one photo at most. If in doubt cut the weakest picture and set its fact large.
- **Text over a photograph** sits on its calmest part over a scrim from the theme's ink (35 to 65% gradient from the text's edge, behind the text side only), at 4.5:1 or better against the image beneath. No centred white type over a busy frame. A theme that refuses gradients uses a solid ink plate.
- **Captions are facts** from the prompt in the label style, beside or under the picture (the dish and its price, the room and its hours). Never a credit there, and never a caption claiming a stand-in as the user's own person, place or product.
- **Theme treatment on every photo,** including the user's: natural, warm, muted, mono, duotone in two theme tokens or tint in one, with small contrast, saturation or exposure tweaks. Duotone and tint flatten pale subjects (snow, a white wall) into empty fields; choose frames with tonal range and look through the treatment. Duotone and tint use the slot's `::before`, so draw keylines with `::after`.
- **The frame is the theme's:** its radius, an inset outline of ink at 6 to 10% (`outline: 1px solid ...; outline-offset: -1px`). Never a border plus a wide shadow (F24).

## Generated stills

Only when the user asked for generated images or a subject no source can reach; see `comp.md`. Never fire it automatically.

## Never

- A drawn illustration (80): an SVG or CSS figure of an object, plant, animal, person, product, building, landscape or scene past icon size. SVG is for icons from one set, the user's logo, real-data charts and diagrams of a real system, and plain geometry used as texture.
- An empty picture (81), a counting device (82), illustration packs and mascots (unDraw-style sets, 3D blobs, isometric scenes), stock faces as proof (F9), a logo wall without the user's logos (46a), blobs or aurora behind text (29), an image that zooms or rotates on hover (11), text baked into a picture, a photograph of a screen showing someone else's interface.

## Icons, logos, video, 3D

- **Icons:** one library a page (Lucide by default, https://lucide.dev), one stroke width and style, at 16, 20, 24 or 32px on the set's grid (a 24 viewBox at 24px, never scaled to 19), `currentColor`, aligned to the first line of multi-line text, never in a coloured tile (gate 3, F5), never an emoji. A button with an icon pads the icon side by the vertical padding.
- **Logos:** the user's own, monochrome, one treatment per row, 32 to 48px tall (20 to 28 in a footer). Simple Icons (https://simpleicons.org) only for a platform the page names. Never an invented wall.
- **Video:** the user's footage with `autoplay muted loop playsinline` and a `poster` (28a, 28b); WebM (AV1 or VP9) then H.264 MP4; under 2 MB per ten seconds; a visible pause control on any loop past five seconds; captions if it speaks.
- **3D and WebGL** only when the product is 3D and the visitor handles it, with a still fallback (`../taste/objects.md`).
- **Motion libraries:** CSS and `@property` first; a React animation library only for orchestrated entrances; a timeline library only when a timeline is the product (`../../website/libraries.md`).

## Stamp, log and handoff

Record `imagery: photographs 5 muted · product sample in hero and demo-2` (or `imagery: none`) in the stamp and log so the next build rotates. The handoff lists every stand-in and built sample with its slot, size and what the user's own picture should show.
