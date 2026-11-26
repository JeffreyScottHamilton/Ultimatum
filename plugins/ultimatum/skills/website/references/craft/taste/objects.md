# Objects, prints and product renders

Read when a page might show a modelled object: a printed or engraved object on a tech card, or a 3D render of a physical product the brief asks to show in 3D.

## Families

| Family | What it is | Where it may appear |
|---|---|---|
| Print objects | an object modelled in code (cup, wheel, lamp, globe, cards), shown as a studio still or printed as halftone, engraving or dither | tech cards and heroes |
| Photo prints | a real photograph printed by a shader (halftone, engraving, dither), the plain photo showing under the pointer | a kit gallery only, never a page |
| Scene objects | photographs or a generic form run through a print and alive under the pointer (exploded layers, a dot object, a split reveal, a turntable, a dither sequence) | a kit gallery only; a turntable only when the form is the product's own |
| Product render | any physical product composed from a spec of simple parts and lit in real materials | a product page whose brief asks for 3D |

The source kit ships these as code (a print core, scene modules and a render builder). Their scripts are not part of this plugin (`later.md` § Source kit); the rules below apply to whatever renderer you use.

## Who gets an object

- **A page holds at most one strong object moment.** It never shares the page with another effect and never sits on a moving ground (`grounds-and-effects.md` § Budget).
- **Place, service and everyday product pages: no object, print or scene.** Photographs lead. The one exception is a product whose brief asks for 3D.
- **A physical product with no photos gets photographs first,** never a render by default. If the visitor never sees the product, the page has failed; borrow licensed photos of a similar item and name them in the report (`photos.md`).
- **Renders are for three cases:** the brief requests 3D, the page needs a configurator, or the product exists only as a model. The render then opens the hero and is shown complete in no more than two other sections, each from a different angle written on its plan line.
- A render never shows a different kind of object, a drawn SVG, loose primitives, mood stock or another maker's product, and never leaves an order form alone in one half of a split hero.
- **A game without art:** its name large over a stand-in photo of its setting; the world section is the widest photo, full bleed. No render unless the brief requests 3D.
- **Software, AI and games with art:** a print object is placed on the card whose topic it shows (say, a globe on the card about regions), or the game's own world object holds a fixed hero.

## Placement

- Print objects: on a card, large and cut by the bottom-left edge; in a tile, whole and low in the square; in a hero, in a wide frame, set to the right of centre. Never dead centre.
- Photo prints and scenes need a box with a fixed `aspect-ratio`.
- A render never has words laid over it. It stands on the section ground at full scale, never in a grey panel; its frame loses fill, border and padding.
- How much of its frame a render fills: about 0.86 on a stage, 0.88 in a hero, 0.84 in a tile, 0.9 on a card (0.3–1.2 when overridden).
- Big products: the hero and at least one other section give the product's long side 80–100% of the frame, or a close-up runs off the edges. The hero's widest view spans at least 80% of the content width at 1440. Close-ups keep their sides inside the frame where the rest runs off.

## Palette and motion

- Draw in the page tokens (ground, surface, ink, muted, accent). After a theme switch, read them again. A globe's sea is the accent.
- The accent goes on the part a maker would paint, and nowhere else.
- One mover per group. Anything that turns or loops gets a round pause button in the frame's bottom-right corner once drawn (WCAG 2.2.2).
- Nothing animates on scroll, except inside the page's one dealt big scene (`moments-and-scenes.md`).

## Client renders

How to show a product render without making the page heavy:

- **Stills by default.** Render each view to an image ahead of time, in the frame sizes used, with a half-size variant for `srcset` and a dark-ground variant where needed. The page loads images, not WebGL.
- **Modes:** auto (show the still; the default), image (still only), still (render once at frame size, copy to an image, free the context), live (turns; only when the brief wants it, one live context).
- Under **reduced motion**, and on **phones** (a coarse pointer, or a viewport below 700 px), show a single crisp still and create no WebGL context.
- **A poster shows at once** and remains in place when a shader fails to compile, WebGL2 is unavailable, or nothing gets drawn. Never leave an empty object.
- **Views:** three-quarter (default), side, front, rear, top, low, close-ups of named parts, the product in use (a scene with real props, only when a headline promises it), each colourway, and a lamp switched on or off.
- **Colourways:** each colour button names the frames it drives and swaps them to that colour's still on click, with `aria-pressed` on the chosen one. Every colour offered appears once.
- Name the render for assistive tech (`role="img"` and an `aria-label` naming the product and view); a frame a click switches is a button.
- Mark the frame's mode and state (image, still, live, poster) in attributes so a checker can count live contexts.

```html
<figure class="product" data-mode="image">
  <img src="/renders/bike-34.avif" srcset="/renders/bike-34-half.avif 800w, /renders/bike-34.avif 1600w"
       sizes="(min-width: 1024px) 60vw, 100vw" width="1600" height="1000"
       alt="City bike in sage green, three-quarter view" decoding="async">
</figure>
<div class="swatches" role="group" aria-label="Frame colour">
  <button type="button" aria-pressed="true"  data-src="/renders/bike-34.avif">Sage</button>
  <button type="button" aria-pressed="false" data-src="/renders/bike-34-ink.avif">Ink</button>
</div>
<script type="module">
  const img = document.querySelector('.product img');
  for (const b of document.querySelectorAll('.swatches button')) {
    b.addEventListener('click', () => {
      for (const other of b.parentElement.children) other.setAttribute('aria-pressed', other === b ? 'true' : 'false');
      img.removeAttribute('srcset');          // one still per colour in this small example
      img.src = b.dataset.src;
      img.alt = `City bike in ${b.textContent.toLowerCase()}, three-quarter view`;
    });
  }
</script>
```

## Building a product spec

When a render is truly needed, describe the product as parts:

- **Axes:** x to the front, y up, z across. Scale so the largest side is one unit and the lowest point stands on the floor. Use real measurements.
- **Part types:** tubes and beams (frames, bars), boxes and panels (housings, plates), cylinders and discs (bases, hubs, lenses), spheres and ellipsoids (bulbs, knobs), tori (rings, chainrings, status lights), joints (hinges), wheels (bikes, casters), shades (lampshades), seats (saddles, cushions), baskets, arcs (mudguards, hoops), springs, and paths (handles, cables, bent tubes).
- Each part has a material, an optional fillet into its neighbours, a name, an optional motion group, and seams cut as panel lines.
- **Materials:** leather, fabric, wood, plastic, rubber, steel, chrome, metal, light, and paint (the single material allowed the accent colour); each with a gloss, satin or matte finish and an optional glow.
- **Motion:** up to four groups, each turning about its parent's pivot (a lamp's arm, then its head). Joints move only while the product turns.
- **Craft:** model the details that make the object recognisable: spokes, chain and mudguards on a bike; springs, knobs and cord on a lamp; caps, seams and grip pads on a device. Check at 1440 and 390.
- **Cannot render well:** text or logos on the product, clear glass, draping cloth, free-form organic surfaces such as faces, animals, shoes or car bodies and anything thinner than a texel. A game composes machines, buildings and props, never a character.
- **Spec faults to catch before rendering:** an unknown part type or material, a view naming a missing part, a part in a group that doesn't exist, more than 90 parts.

## Budget

Cost grows with parts, since every part is tested at every ray step: about 20 parts cost like a print object; 60–70 run on a laptop GPU but crawl on CPU. Keep a spec under 90 parts. Rendering stills on CPU can take minutes per view; render them ahead, never on the visitor's machine.

| Family | Cost per frame | Live contexts |
|---|---|---|
| Print objects | high | share two |
| Photo prints | low | one each, three at most |
| Scene objects | low | two at most |
| Product render | none as a still | one when live |

- At most four live WebGL contexts on the page, counting the page's effects (`performance.md` § WebGL).
- Free contexts off screen and in a hidden tab. Reduced motion shows one still frame.

## Never

- A caption or apology on a render or print ("made in code", "stand-in", "illustration", "3D model").
- An object laid on top of the hero photo, or used instead of the client's photographs.
- A render on a place page, or a render of a different kind of product.
- Credits for renders (none needed); any photos used are credited in the footer's single credit line (`photos.md` § Captions and credits).
