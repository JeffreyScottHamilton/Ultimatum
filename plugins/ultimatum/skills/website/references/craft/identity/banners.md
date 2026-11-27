# Banners, ads and covers: sizes and how to lay them out

Read when the owner needs a web ad, a social cover, an email header or a printed banner. Platforms change their sizes and crops: check each one's own help page on the day and write the date next to the size you used. For the avatar, link preview and post templates, `identity-kit.md` § Social images.

## 1. Rules for any banner

- **One message.** A banner is seen for about a second. Name, one short line, and at most one call to action.
- **Hierarchy:** the line or the product is biggest, the logo is clearly there but smaller, the button looks like a button.
- **Safe area:** keep text and the logo inside the central area; each platform crops covers differently on phone and desktop, and profile photos and buttons sit on top of covers.
- **Contrast and size:** text must read at the size the banner is actually shown, often smaller than the file. Check at 100% on a phone.
- **Brand:** the same colours, faces and photo style as the site; the banner is the first thing many people see.
- **Files:** PNG for flat graphics and text, JPEG or WebP for photos; keep under each platform's file limit. Export at 2× where the platform allows it, so text stays sharp on dense screens.
- **Truth:** prices, offers and dates on a banner are claims; check them with the owner (`../hallmark/brand-truth.md`).

## 2. Web display ads

The most used sizes (CSS pixels; supply 2× files where the ad network accepts them):

| Size | Name | Notes |
|---|---|---|
| 300×250 | medium rectangle | the most widely available slot; design this one first |
| 336×280 | large rectangle | same layout as 300×250 with a little more room |
| 728×90 | leaderboard | very short: logo, one line, button in a row |
| 970×90 / 970×250 | large leaderboard / billboard | top of page on desktop |
| 300×600 | half page | room for an image above the line |
| 160×600 | wide skyscraper | stack: logo, line, button |
| 320×50 / 320×100 | mobile banner / large mobile banner | text must still read at this size; keep to a few words |

Ad networks also set file size limits, animation length limits and rules about borders and clickable areas: read the network's current spec sheet before exporting. Animated ads end on a frame that works alone, with the message and the button visible.

## 3. Social covers and headers

Approximate upload sizes in late 2026; check the platform's help page before use.

| Place | Upload size | What crops it |
|---|---|---|
| X (Twitter) header | 1500×500 | profile photo overlaps the lower left; top and bottom crop on some screens |
| LinkedIn personal cover | 1584×396 | profile photo covers the lower left |
| LinkedIn company cover | 1128×191 | logo sits over the left side |
| Facebook page cover | about 1640×624 upload; shown wider and shorter on desktop than phone | keep text in the middle band |
| YouTube channel banner | 2560×1440 | only the central 1546×423 shows on every device |
| Twitch profile banner | 1200×480 | |
| Instagram post | 1080×1350 (4:5) or 1080×1080 | the grid shows a crop of the middle |
| Stories and short vertical video | 1080×1920 | top and bottom 250 px or so are covered by the interface |
| Pinterest pin | 1000×1500 (2:3) | |

Make one master design with a generous safe area, then adapt it for each place, rather than designing each from scratch.

## 4. Email headers and in-app banners

- Email: 600–640 px wide is still the safe width for the body; export at 2× (1200 px wide) and set the display width in the HTML. Many email clients block images by default, so the alt text carries the message and nothing essential lives only in the image.
- In-app and on-site banners: built in HTML and CSS, not as images, so text is real, resizes and can be translated. Give each a close button and remember that it was closed.

## 5. Printed banners

Ask the printer for their template; their specs win.

| Piece | Common size | Notes |
|---|---|---|
| Roll-up (pull-up) stand | 850×2000 mm | keep text above about 800 mm from the floor; the bottom is hidden by tables and feet |
| Vinyl banner | to order, e.g. 3×1 m | eyelets every 50 cm; keep text clear of the edges and eyelets |
| Poster | A2, A1, or 18×24 in, 24×36 in | read distance decides the type size (`identity-kit.md` § Print pieces) |

Files: PDF at final size (or the printer's scale), images at 100–150 ppi at final size for large banners viewed from a distance, bleed as the printer asks, vector logo, colours as the printer asks.
