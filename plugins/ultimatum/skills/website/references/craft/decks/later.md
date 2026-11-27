# Decks: left out for now

Read when a deck task needs something these guides do not cover, to see whether it was left out on purpose.

| Topic | Why left out | Instead |
|---|---|---|
| A design-token validator for decks | the deck checker and the page linter cover the checkable parts | `build.md` § Check the deck |
| Background image search keywords per slide type | stock searches by keyword produce stock-looking decks | `slides.md` § Images and screenshots |
| Keynote and Google Slides native files | no open, scriptable format to test against | build a `.pptx` and import it |
| Animated chart libraries bundled with the deck | a pinned library from a CDN, loaded only when needed, is lighter | `charts.md` § Building charts for an HTML deck |

Done in 0.0.50: deck-type and layout tables, kept short and checked against the built deck (`plan-check.md`) rather than searched.

Done in 0.0.58: `deck_build.py` builds a deck from a content file into the template and runs both checkers on it (`build.md` §2). It fills layouts; the story and the words still come from `story.md`.
