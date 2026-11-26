# Imagery: what fills a page, slots, capturing the product, treating photos

Read before placing any picture on a page build. Pages feel real when visitors see the actual place, dish, hands or running product, and feel generated when they see a gradient box, a clip-art loaf or a heading floating over nothing. Photo sourcing and credits live in `../taste/photos.md`; icons and diagrams in `../taste/icons-and-diagrams.md`. This file adds the order of preference, slots, product capture and balance. Merged with Taste's photo rules; where both speak, the stricter wins.

## Order of preference

Work down the list and stop at the first source you can use.

1. Pictures and recordings the owner supplied (ask early). They beat everything.
2. Screenshots of the real product, captured by the build whenever it can run or be reached: a live URL, a dev server, a project with a one-command start, a local app (see Product below).
3. A built version of the product, only if nothing exists to capture yet.
4. Licensed photographs, treated to match the theme (see Placing photographs).
5. Generated stills, only when the owner asked and a generator is set up (`comp.md`).
6. Large type, when the subject is language itself.

Match the brief to the source:

- **Place, craft, food, material, event, people working** (bakery, ski school, weaving studio, tailor, farm, plumber's van): photographs lead. The first-screen photo is the biggest element, either full-bleed under the headline or alongside it at 60–75% of screen height. Add 2–4 more, one of them large, each about its own subject. Cut any off-subject picture rather than pad the count. Put material-only sections between them: a menu as rows, hours as a table, a statement, an enquiry form. Together, photographs occupy about 25–33% of page area.
- **Software:** the interface leads the first screen. A photograph or two can set a scene if it survives the deletion test, meaning removing it loses a fact. Skylines, laptops on desks and office buildings fail.
- **Language-led** (docs, API, CLI, specimen, manifesto): type and code do the work, with at most one full-bleed photo band. A manifesto about a physical thing shows that thing.
- Never let a photo carry a fact. Figures, names and claims stay as text, and a portrait never poses as a customer, teammate or testimonial (F9).

## Sourcing rules that carry over

We do not ship the source's photo library (see `later.md`). Use the owner's photos first, then the borrowing rules in `../taste/photos.md`.

- Do not type an image URL from memory or lift one from a stock site. Use supplied files or ones you can name and credit (gate 76).
- Credit borrowed photos in a single footer line tagged `data-credits`, kept out of the word budget. Some licences demand it.
- Ship a responsive `srcset`; set `sizes` from the layout (`50vw` for a half-width picture, `100vw` for full-bleed); crop through the frame with `aspect-ratio`, `object-fit: cover` and an `object-position` that holds the subject (MDN: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#srcset).
- The top photo is the largest paint, so give it `fetchpriority="high"` and no lazy loading; lazy-load the rest. Full-bleed needs 2400px on the long edge, or it softens at 1920 wide.
- A stand-in must be easy to swap and carry alt text naming the real subject; list it in the handoff.

## Slots

A slot is any picture the owner will replace. Give it a `data-slot` name, a `data-alt` describing the right image, and a fixed size (`aspect-ratio` or height).

- A slot always shows something real: the owner's image, a borrowed photo or the full-fidelity built product. The wash colour is for load time only; a slot that shows only the wash counts as an empty picture (gate 81).
- No visible placeholder text such as "screenshot goes here", ratio hints or "sample" badges. Data attributes and the handoff carry that information.
- Mark any child that should outlive the swap (credit, plate number) with `data-keep`. Text over a slotted photo lives in a sibling layer above (`z-index` 2 or higher), not inside the slot.
- At most four slots per row, and no frame set for things you have no pictures of (a team, venues). Use type for those (gate 68).

Our swap helper:

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

**Capture before you mock.** If the product is real, show it. During pre-flight look for a URL in the brief, a running server, a `package.json` whose scripts include `dev` or `start`, a local app, or a path the owner names. Start it on a free port (install only what the lockfile says), bring it to a state that tells the story (sample data, a project open), then shoot 1440×900 and 390×844 at 2x. Playwright reference: https://playwright.dev/python/docs/screenshots


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

For one element use `locator.screenshot()`. Electron apps expose a DevTools port; other desktop apps need the OS screenshot tool; mobile apps need a simulator; a command-line tool is run for real and its output pasted into a code block. Inspect every capture before it ships: no personal data (names, emails, tokens, paths), no error screens unless they are the story, no debug overlays. Use a few: main screen in the hero, a close crop, a second screen, the phone layout. Stamp `imagery: screenshots n`. They belong to the owner, so no credit line.

**Dress the capture in the theme.** Place it in a slot with the theme's radius and an inset outline. Never draw a browser bar, device bezel, traffic-light dots or notch (gates 47a, 47b). Crop to the selling part, keep text readable at displayed size (do not upscale), do not retouch. Tag the slot `data-kind="product"` so it stays out of the photo-share count.

**Build only when capture is impossible** (an idea, a product not yet made). The hero visual is the main screen in HTML and CSS: working-looking controls, eight or more elements, nouns from the brief, the theme's surfaces and type, sized as the hero visual. Placeholder data reads as obviously sample (`example.com`, "Example Kitchen", round sums) and never as a claim (46a). Put it in a slot so a real screenshot can replace it, and have the handoff list the screens to capture later. Never mock something you could have captured (84).

An interactive control (a calculator on the owner's price list, a booking form) makes a good section, or a decent close, once per page; it is not the default hero. For apps behind sign-in use a seeded demo account, never customer data.

## Placing photographs

- **Large or absent.** Six of twelve columns and 440px tall at minimum, or full-bleed. Sets of four or more can shrink if each carries its fact. Imagine deleting it: if the screen reads the same, it is too small or too weak.
- **One subject per frame**, cropped tightly and leaning toward the text. Vary ratios (portrait 4:5 beside text, wide 16:9 or 21:9 spanning, square in pairs) and widths (8 and 4 columns). Equal frames are right only for a real set such as three dishes or three rooms.
- **Balance.** After the hero, photos take up to a third of the page at 1440 wide (45% for photographic or portfolio shapes; product pictures excluded). Never two photo-led sections back to back; follow a picture with something carried by type, rules, colour or the product. Software alternates product and type sections; language-led pages get one photo at most. When unsure, cut the weakest and set its fact large.
- **Text on a photograph** goes on the quietest region, over a scrim drawn in the theme's ink (a 35–65% gradient from the text edge, covering only the text side), with 4.5:1 contrast against the image underneath. No centred white lettering on a busy frame. A theme that bans gradients gets a solid ink plate.
- **Captions state facts** from the brief, in the label style, beside or beneath the picture (dish and price, room and hours). Credits never go there, and a caption never passes a stand-in off as the owner's own person, place or product.
- **Every photo gets the theme treatment**, the owner's too: natural, warm, muted, mono, duotone from two theme tokens, or a one-token tint, plus small contrast, saturation or exposure nudges. Duotone and tint flatten pale subjects (snow, white walls) into blank fields, so pick frames with tonal range and judge through the treatment. They occupy the slot's `::before`, so draw hairlines with `::after`.
- **The frame follows the theme:** its radius and a hairline inset outline in ink at 6–10% opacity (`outline-offset: -1px` with a 1px solid outline). Never pair a border with a wide shadow (F24).

## Generated stills

Only on request, or for a subject no source reaches; see `comp.md`. Never trigger generation unprompted.

## Forbidden

- Drawn illustration (80): any SVG or CSS picture of a thing, creature, person, building or scene above icon size. Keep SVG for single-set icons, the owner's logo, charts of real data, system diagrams and plain geometric texture.
- Also out: an empty picture (81); a counting device (82); mascots, illustration packs, 3D blobs, isometric scenes; portraits of strangers as proof (F9); logo walls lacking the owner's logos (46a); blobs or aurora behind text (29); hover zoom or rotation (11); text baked into pictures; photos of a screen showing another company's interface.

## Icons, logos, video, 3D

- **Icons:** a single library per page (Lucide by default, https://lucide.dev), one stroke weight and style, drawn on the set's grid at 16, 20, 24 or 32px (a 24 viewBox shows at 24px, not shrunk to 19), coloured by `currentColor`, aligned with the first line of multi-line text, not inside a coloured tile (gate 3, F5), never an emoji. On an icon button, pad the icon's side to equal the vertical padding.
- **Logos:** the owner's, in monochrome, one treatment per row, 32–48px tall (20–28 in the footer). Use Simple Icons (https://simpleicons.org) only for a platform the page mentions. No invented wall.
- **Video:** the owner's footage, with a `poster`, set to `playsinline muted loop autoplay` (28a, 28b). Serve WebM (AV1 or VP9) first, H.264 MP4 second, under 2 MB per ten seconds. Loops over five seconds need a visible pause control; spoken video needs captions.
- **3D and WebGL** only for a 3D product, when visitors can steer it, with a still fallback (`../taste/objects.md`).
- **Motion libraries:** CSS and `@property` first; a React animation library for orchestrated entrances only; a timeline library only when the timeline is the product (`../../website/libraries.md`).

## Stamp, log, handoff

Write `imagery: photographs 5 muted · product sample, hero plus demo-2` (or `imagery: none`) into the stamp and log so the next build can vary. The handoff names each stand-in and built sample with slot, size and what the owner's real picture should show.
