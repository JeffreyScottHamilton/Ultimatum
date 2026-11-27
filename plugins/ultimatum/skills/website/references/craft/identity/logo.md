# Logo: choosing, drawing and testing a mark

Read when the owner has no logo, or asks for a new one. Read `logo-colour.md` next, and `ai-logo.md` before using an image model.

A small business needs a mark that is readable on a phone screen, a van door and a receipt. Most need less design than they think: a well-set name beats a clever symbol nobody recognises.

## 1. Pick the kind of mark

| Kind | What it is | Fits | Watch out |
|---|---|---|---|
| Wordmark | the name set in type, often adjusted by hand | new businesses, short or distinctive names, local trades, studios | long names get small; needs careful spacing |
| Monogram | one to three initials | long names, firms known by initials, luxury and fashion | initials mean nothing until people know the brand |
| Symbol | a picture of a thing (a leaf, a key, a cup) | when the thing is the business and the shape is simple | clichés (the tooth, the house roof, the globe) |
| Abstract mark | a shape with no literal meaning | larger brands that will spend on making it known | means nothing on day one; pair it with the name |
| Character | a person or animal drawn as the brand | food, kids, games, friendly local shops | hard to draw small; dates quickly |
| Badge | name inside a shape (crest, seal, stamp) | breweries, barbers, schools, clubs, heritage | fine detail fills in at small sizes |
| Combination | symbol and name together, also usable apart | most businesses that want an app icon or avatar | needs a symbol strong enough to stand alone |

Default for a new local business: a wordmark, plus a monogram or simple symbol cut from it for the favicon and social avatar.

## 2. Start from the brief, not from shapes

Write down before drawing:
- the name exactly as written (capitals, spaces, accents) and any tagline that must lock up with it;
- three words for how it should feel, taken from the owner (not "modern, clean, professional", which every brief says);
- where it will live most: phone screen, shop sign, uniform, packaging, a van;
- what nearby competitors look like, so the mark can differ from them;
- anything ruled out (colours tied to a rival, a symbol with a local meaning).

## 3. Draw it

- **Type first.** Start from a typeface whose licence allows logo use (most OFL and Apache fonts do; check `ult design search "<feel>" --in font` and the licence column). Then adjust: tighten or loosen letter spacing by eye, fix awkward pairs, and consider one custom detail (a joined pair of letters, a cut stroke) rather than many.
- **Outline the text** in the final file so it does not depend on the font being installed, but keep the editable version with live text.
- **Simple geometry.** Few points, consistent stroke widths, shapes snapped to a grid where it helps. Optical fixes beat mathematical ones: round shapes sit slightly above and below the flat ones, so they look the same size.
- **One idea.** If the mark needs a sentence to explain, simplify it.

## 4. Lockups and rules

Prepare these versions:
- primary (usually horizontal: symbol left of the name), stacked (symbol above), symbol alone, name alone;
- full colour, one colour (black), and reversed (white on dark).

Set two rules and write them down:
- **clear space:** keep a margin equal to a named part of the mark (for example the height of the capital letter) free of other things;
- **minimum size:** the smallest width at which it still reads (test it, see below), for screen in pixels and for print in millimetres.

## 5. Test before calling it done

1. **Small:** view it at 16 px and 32 px (favicon), and 24 mm wide in print. Use the symbol or monogram where the full mark breaks.
2. **One colour:** black on white and white on black. If it only works in colour, it is not done.
3. **On real backgrounds:** a photo, the brand's darkest and lightest colours, a busy social feed screenshot.
4. **Blur and squint:** at a glance, is the silhouette distinctive?
5. **Next to competitors:** put it in a row with three local rivals; it must not be confused with any of them.
6. **Name check:** before the owner commits, run the trademark search in `../../app/legal-risk.md` step 7.

## 6. Files to hand over

```
logo/
  source/      editable file (SVG or design-tool file) with live text
  svg/         primary, stacked, symbol, wordmark: colour, black, white
  png/         same set at 512, 1024 and 2048 px wide, transparent background
  print/       PDF of the vector versions (colours noted as hex and, if printing, the printer's CMYK)
  logo-rules.pdf   one page: versions, clear space, minimum size, colours, what not to do
```

A clean web SVG has a `viewBox`, no fixed width and height, no embedded raster images, text converted to paths, and a title for screen readers when used inline:

```html
<svg viewBox="0 0 120 32" role="img" aria-labelledby="logo-title">
  <title id="logo-title">Harbour Bakery</title>
  <circle cx="16" cy="16" r="14" fill="currentColor"/>
  <rect x="40" y="10" width="76" height="12" rx="2" fill="currentColor"/>
</svg>
```

Used as an image, give it alt text with the business name (`<img src="/logo.svg" alt="Harbour Bakery">`) and link it to the home page. `fill="currentColor"` lets one file follow the text colour in light and dark themes.

## What not to do

- Don't put the tagline, a web address or a phone number inside the mark.
- Don't use gradients, shadows or glows the mark depends on; they fail in one colour and in print.
- Don't stretch, rotate, outline or recolour it outside the written versions.
- Don't base it on another brand's mark, a stock icon, or a font whose licence forbids logo use.
