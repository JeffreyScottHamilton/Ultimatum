# Identity kit: icons, social images and print

Read when the logo is approved and the site needs favicons and app icons, or the owner asks for cards, signs or social images. Sizes for social platforms change: check each platform's own help page on the day and note the date.

## Favicons and app icons for a website

Use the symbol or monogram, not the full wordmark. Three files cover modern browsers and phones:

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
```

- `favicon.ico`: 32×32 for old browsers and tools that only look for that file.
- `icon.svg`: scales to any size; it can switch colours for dark browser themes:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
    <style>path{fill:#1F5C4A}@media (prefers-color-scheme:dark){path{fill:#9AD9C2}}</style>
    <path d="M4 22c0-8 5-14 12-14s12 6 12 14z"/>
  </svg>
  ```
- `apple-touch-icon.png`: 180×180, solid background (iOS fills transparency with black), no rounded corners (iOS adds them).
- In `manifest.webmanifest`, 192×192 and 512×512 PNGs, plus a 512×512 `"purpose": "maskable"` version whose important part sits inside the central circle of 80% of the width; Android crops the rest into its own shape.

Test: load the site in a desktop browser (tab icon in light and dark), add it to a phone's home screen, and check the icon is centred and not clipped.

## Native app icons

- iOS: one 1024×1024 master without transparency; the system masks the corners. Follow Apple's app icon guidance: https://developer.apple.com/design/human-interface-guidelines/app-icons
- Android adaptive icons: a 108×108 dp foreground and background, with the important part inside the central 66 dp, because launchers crop to different shapes: https://developer.android.com/develop/ui/views/launch/icon_design_adaptive
- Simple silhouette, one strong shape, no small text. Check it at the smallest size the system uses.

## Social images

- Avatar: the symbol on a solid brand colour, centred to survive a circle crop.
- Cover or banner: keep text and the mark in the middle area, because each platform crops differently on phones and desktops.
- Link preview (Open Graph): 1200×630 is the common size; see `../../pages-and-seo.md` for the meta tags.
- Post templates: two or three layouts with the brand fonts and colours, room for a photo and a short line.

## Print pieces

Ask the printer for their template first; their specs win over these defaults.

| Piece | Common size | Notes |
|---|---|---|
| Business card | 85×55 mm (EU), 3.5×2 in (US) | 3 mm (or 1/8 in) bleed; keep text 4 mm inside the edge; name, role, phone, email, site |
| Letterhead | A4 or US Letter | logo, address and legal details (company number where the law asks) |
| Envelope | DL (110×220 mm) or US #10 | logo and return address only |
| Signs and windows | measure on site | read from the distance people stand: a rough rule is 25 mm of letter height per 10 m |
| Vehicles | from the vehicle's template | name, what you do and a phone number readable at a glance; nothing small |
| Uniforms | embroidery or print area from the supplier | one-colour mark; fine detail and thin lines fill in when stitched |

Print files: PDF (PDF/X if the printer asks), vector logo, fonts embedded or outlined, colours in the printer's CMYK or spot, images at 300 ppi at final size.

## Organising the files

```
brand/
  brand.md          colours (hex, CMYK), fonts with licence and links, voice notes, logo rules
  logo/             as in logo.md §6
  icons/            favicon.ico, icon.svg, apple-touch-icon.png, icon-192.png, icon-512.png, icon-maskable.png
  social/           avatar, covers, post templates
  print/            card, letterhead, envelope: print-ready PDFs and editable sources
```

Name files by what and where: `logo-stacked-white.svg`, `card-front-print.pdf`. Keep the editable sources; the owner will need them for every reprint.
