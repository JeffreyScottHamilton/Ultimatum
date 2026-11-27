# Photographs

Read when a page needs pictures: choosing them, finding stand-ins, placing, serving and crediting them.

## Where photos lead

- A place is its photographs: two or three per screen, the client's own wherever possible.
- Software leads with its real interface; a game with its own art. Neither leads with library frames.
- A physical product always shows photographs: the client's if they exist, otherwise licensed shots of a similar item (§ Stand-ins).
- A photograph never stands where an effect or an empty box would be, and no drawn box, grid or effect stands where a photograph belongs.
- With nothing usable, show real UI or type. Render the product only if the brief requests 3D (`objects.md`).

## Sources, in order

1. The client's own (shot by them, commissioned, supplier images for their own range).
2. A vetted library of free-licence frames, for detail slots only.
3. A live search of a free-licence archive, each result treated as a stand-in.
4. Nothing: type or real UI.

Tag every image so the gate and the report can count them:

```html
<img src="img/counter.webp" alt="Oat flat white on the walnut counter"
     data-source="client" data-subject="counter" width="1200" height="900"
     loading="lazy" decoding="async" sizes="(min-width: 1440px) 588px, 90vw">
```

`data-source` values: `client`, `commissioned`, `phone`, `supplier`, `illustration` (owned only), `library`, `stand-in`.

- Library frames fill detail slots only: hands, tools, materials, process. They never stand in for a person, the product, a shopfront, a room or the hero. At most one picture in three.
- Some trades have no fitting detail frames at all (bars, wine, weaving, letterpress); for them the library supplies nothing.
- All other pictures are type, real UI, the product or photographs the client took.

## Stand-ins

- With no client photographs, say so in the report and recommend, in order: a half-day local shoot, a phone shoot, or products on one plain backdrop.
- Shot list for a place: shopfront, the room seen from the door, counter or bench, three products, hands at work, one detail, each guest room. A normal (1×) lens, window light, no flash.
- Shot list for a product: plain backdrop, three angles, the parts the spec names, the product in use.
- Each stand-in shows a similar item complete and being used. Keep one colour grade across all of them; no visible brand of another maker; no face that could pass for a real customer.
- Live search candidates: only public-domain or Creative Commons (CC0, CC BY, CC BY-SA) licences, JPEG at 1600 px wide or more for wide slots (1200 for small ones); no paintings, drawings, maps, logos or posters. Search a product by its own words, a game by its setting, a trade by two or three plain words ("pottery wheel hands", "bike workshop stand").
- Open every candidate at full size. Keep it only if it is sharp, shows no readable business name, no staff face, no landmark, and matches the set's grade.
- Write fresh alt text for each stand-in; the report lists each one as a picture the client should replace, but the page itself does not mention it.
- A place whose trade leads with its land (a remote guesthouse) may use a landscape of that named region as a draft stand-in; name this exception in the report.
- Under eight usable frames after searching means the short page (`place-pages.md` § Short page).
- Don't reuse the same library frames build after build; keep a history of frames used.
- Wikimedia Commons reuse guide: https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia

## Layouts

- Ratios: 4:5, 4:3 and 1:1 on a place; other kinds may add 3:2. One ratio per row.
- Edges at 1440: 80 to 1360, or 120 to 1320 for places. At 390 a photo is 342 px wide.
- One visual world: one light, one grade. Monochrome is allowed for a single, chosen frame. A page never repeats a picture.
- A product appears whole in three sections at most.
- Hero: a plain full-colour photograph. The place hero is a full-bleed photograph with nothing on it (`layout-and-heroes.md` § Place hero).
- Rooms: each room's facts sit next to a single detail shot. Menus are written text alongside their layout, not a photograph for every dish.
- Photo bands: one or two on a product page; one on a place, never next to the hero. A place page may end on a square photo of its shopfront, without text.
- Compositions for places (bleed, pair, trio, strip, tall-small) are in `place-pages.md` § Compositions.
- Cut-outs (transparent WebP) only for the client's own product. Supplier images only in a product grid. Illustration only if the client owns it.

## Text on photos

- Never on a place.
- Otherwise text may overlay a photo just twice, in the hero and one closing band, set on a calm area of the frame or in a solid box. No scrim, gradient, fade or blur to rescue it.
- The text must pass 4.5:1 against the pixels behind it at every width (`accessibility.md`).
- At 768 the lead photo (3:2) is cropped to its centre; if the words then land on the subject, move them under the photo.
- A full-bleed photo carrying words needs its own 390 crop with the subject inside the middle 342 px.
- All text is real HTML text; none is part of the image file.

## Serving

```html
<picture>
  <source media="(max-width: 639px)" srcset="img/hero-780x975.webp" width="780" height="975">
  <img src="img/hero-2400.webp" srcset="img/hero-1600.webp 1600w, img/hero-2400.webp 2400w"
       sizes="100vw" alt="The shop window on a wet morning" width="2400" height="1350"
       fetchpriority="high" loading="eager" data-source="client" data-subject="shopfront">
</picture>
```

- The hero: `sizes="100vw"`, `fetchpriority="high"`, eager, plus a phone crop (4:5) through `<picture>`. A client hero gets a phone crop only if its source covers 4:5 at 390 without upscaling; otherwise use 4:3.
- Every other image: `loading="lazy"`, `decoding="async"`, `width` and `height` set, and `sizes` matching the shown width.
- Images in menus and tabs drop lazy loading so they are ready when opened. `object-position` follows the subject.
- WebP, about 400 KB for the hero and 250 KB for others; budgets in `performance.md` § Images.
- Never serve a soft, upscaled hero at 1440; ask for the client's original.
- A photograph is visible from first paint: never inside an opacity-0 reveal or a developing mask that might not run. Check for blank frames at four widths.
- MDN responsive images: https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images

## Treatment

- No print effect, dither, duotone, grain, filter or blend mode on any photograph.
- Hover: a linked photo zooms 1.02–1.03 over 600 ms inside its frame. No tilt, rotation or slow pan-and-zoom. Place photos never fade.
- Place photos have square corners, no border and no shadow. A product page uses one radius throughout; software windows 12–20 px.

## Captions and credits

- No caption under pictures. A place name goes in the alt text.
- Licence credits: one line in the footer's legal row linking to a credits page that names photographer, licence, source and whether the frame was cropped or adapted (CC BY requires this: https://creativecommons.org/licenses/by/4.0/).
- Public-domain frames still name the photographer and link the Public Domain Mark: https://creativecommons.org/publicdomain/mark/1.0/
- Alt text says what the photograph shows in this context; decorative repeats take `alt=""` (WCAG 1.1.1).

## Truth

Never show as the client's:

- anything that identifies another business: its signage, interior, counter, branded cups, bags, machines or products;
- a face as staff, guest or customer;
- another place's coast or landmark, or a lone house on a hotel page;
- trade clichés: overhead latte art, a frame packed with coffee beans, a still life of pastry and coffee, flour dusted on black, a neatly made bed, a full-length posed model;
- mood stock, animals, vehicles, famous viewpoints, AI images, composites, street-level map imagery, or gradients and shaders standing in for photos.

Never use a search result without viewing it full size, and never leave one out of the report.

```js
// Gate helper: count images by source and flag untagged or over-quota library use.
function photoAudit(doc = document) {
  const imgs = [...doc.querySelectorAll('img')];
  const by = imgs.reduce((m, i) => (m[i.dataset.source || 'untagged'] = (m[i.dataset.source || 'untagged'] || 0) + 1, m), {});
  const lib = by.library || 0; // stand-ins are counted in the report, not this quota
  return { by, untagged: by.untagged || 0, libraryOverQuota: lib * 3 > imgs.length,
           noAlt: imgs.filter(i => !i.hasAttribute('alt')).length };
}
```
