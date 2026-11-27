# Decks: left out for now

Read when a deck task needs something these guides do not cover, to see whether it was left out on purpose.

| Topic | Why left out | Instead |
|---|---|---|
| Searchable tables of layouts, strategies, colour moods and typography per slide type | a lookup table adds load cost without adding judgment; the guides hold the choices that matter | `slides.md` and `story.md` |
| A slide generator script | generated decks look alike; the template plus the slide list is faster to make good | `../../../../../data/craft/decks/template.html` |
| A design-token validator for decks | the deck checker and the page linter cover the checkable parts | `build.md` § Check the deck |
| Background image search keywords per slide type | stock searches by keyword produce stock-looking decks | `slides.md` § Images and screenshots |
| Keynote and Google Slides native files | no open, scriptable format to test against | build a `.pptx` and import it |
| Animated chart libraries bundled with the deck | a pinned library from a CDN, loaded only when needed, is lighter | `charts.md` § Building charts for an HTML deck |
