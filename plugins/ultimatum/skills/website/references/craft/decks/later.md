# Decks: left out for now

Read when a deck task needs something these guides do not cover, to see whether it was left out on purpose.

| Topic | Why left out | Instead |
|---|---|---|
| A slide generator script | generated decks look alike; the template plus the slide list is faster to make good | `../../../../../data/craft/decks/template.html` |
| A design-token validator for decks | the deck checker and the page linter cover the checkable parts | `build.md` § Check the deck |
| Background image search keywords per slide type | stock searches by keyword produce stock-looking decks | `slides.md` § Images and screenshots |
| Keynote and Google Slides native files | no open, scriptable format to test against | build a `.pptx` and import it |
| Animated chart libraries bundled with the deck | a pinned library from a CDN, loaded only when needed, is lighter | `charts.md` § Building charts for an HTML deck |

Done in 0.0.50: deck-type and layout tables, kept short and checked against the built deck (`plan-check.md`) rather than searched.
