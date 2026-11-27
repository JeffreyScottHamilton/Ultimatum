# Building, exporting and checking a deck

Read when the slide list is agreed and it is time to make the file. The default here is one HTML file: it is plain text, diffs well, needs no paid app, and prints to a PDF that opens anywhere.

## 1. Choose the format

| The owner needs | Build |
|---|---|
| To present from a laptop, or send a PDF | one HTML file from `../../../../../data/craft/decks/template.html`, exported to PDF |
| To edit it themselves in PowerPoint or Keynote | a `.pptx` file (the `pptx` skill, if installed, or `python-pptx`), using the same story and layouts |
| Their company template | fill that template; use only the story, copy and chart guides here |
| Google Slides | build the `.pptx` and import it, then check fonts and spacing in Slides |

Ask which one before building if it is not clear; converting later loses layout.

## 2. The HTML template

`../../../../../data/craft/decks/template.html` is a working four-slide deck:

- each `<section class="slide">` is one 1920×1080 slide, scaled to fit the window;
- arrow keys, space and page keys move between slides;
- `<aside class="notes">` holds speaker notes, hidden on screen;
- colours and faces are CSS variables at the top; change them to the brand's and nothing else needs to change;
- print styles put one slide on each 1920×1080 page, so the browser's print to PDF gives a clean file.

Copy it into the project, rename it, then replace the sample slides with the agreed list from `story.md`.

Or build it from content: `deck_build.py starter seed > deck.json` (any type in `deck-types.csv`) writes one entry per planned slide (beat, layout, empty fields; `deck_build.py fields` lists what each layout reads). Fill in the words, add a `theme` (`bg`, `ink`, `muted`, `accent`, `line` as `#rrggbb`, `display`, `body` as font lists; low-contrast colours are refused), then `deck_build.py build deck.json -o deck.html`. It escapes all text, refuses images without alt text, and runs both checkers on the result: exit 1 means it built but has findings to fix in the content. The layouts stay plain on purpose; give the brand's look through the theme and a few added classes, not by hand-editing each slide. Keep one stylesheet in the file; add layout classes (from `slides.md`) as you need them rather than styling each slide by hand.

Fonts: link web fonts with a pinned URL, or use faces installed everywhere if the file must work offline. Embed images as files next to the deck, or as data URIs for a single-file hand-off; keep the file under about 20 MB so it emails.

## 3. Export to PDF

In a browser: open the deck, print, choose "Save as PDF", set margins to none and background graphics on.

From the command line with Chromium (headless, no network needed for local files):

```bash
chromium --headless --no-sandbox --print-to-pdf=deck.pdf --no-pdf-header-footer deck.html
```

Or with Playwright, which honours the page size set in the print styles:

```js
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + require('path').resolve('deck.html'));
  await p.pdf({ path: 'deck.pdf', preferCSSPageSize: true, printBackground: true });
  await b.close();
})();
```

Then open the PDF and look at every page: nothing cut off at the edges, one slide per page, fonts right, charts drawn in their final state.

For a notes version, add a print stylesheet that shows `.notes` under each slide on a taller page, or export the notes as a separate document.

## 4. Speaker notes

Write notes as what you will say, in short lines, not as a script to read. Each slide's note answers: what is the one thing to say here, and what is the bridge to the next slide. Put numbers' sources and the likely questions in the notes too.

## 5. Check the deck

Run the checker on the HTML file:

```bash
python3 ../../../../../data/craft/decks/deck_check.py deck.html
```

(Use the path to `data/craft/decks/deck_check.py` in the installed plugin.) It reads only the local file. Each line is `file:line rule [severity]: what to fix`; exit code 1 means findings, 0 none, 2 a bad argument or unreadable file. `--rules` lists the rules, `--only rule,rule` narrows them, `--json` gives machine-readable output, and `--max-slides N` sets the length limit (default 20; a seed pitch is about 14, a launch about 10).

| Rule | What it catches |
|---|---|
| `no-headline` | a slide with no h1 or h2 |
| `two-headlines` | two headlines competing on one slide |
| `topic-headline` | a one- or two-word label such as "Market" on a middle slide |
| `long-headline` | a headline over 15 words |
| `too-many-words` | over 45 body words on a slide, notes excluded |
| `too-many-bullets` | more than five top-level bullets |
| `nested-bullets` | a list inside a list |
| `big-table` | a table over 7 rows (header included) or 5 columns |
| `img-no-alt` | an image without alt text |
| `small-text` | a font size under 24 px outside the notes and print styles |
| `no-notes` | no speaker notes on any slide |
| `too-many-slides` | more slides than `--max-slides` |

For structure (beats, their order, word budgets per layout) run `deck_plan.py check` (`plan-check.md`). What neither can see: whether the story holds, whether headlines read as a sequence, contrast on images, whether a chart matches its headline, or whether numbers are true. Those need a person, or the page linter (`../design-review-qa/page-lint.md`) for the visual tells, and a read through the headlines in order.

## 6. Before hand-off

- Read only the headlines, in order: the story still holds.
- Every number has a source in the notes, and every placeholder is listed for the owner.
- Run `deck_check.py` and fix or explain each finding.
- Open the exported PDF on a laptop and, if possible, on a projector or a shared screen.
- Hand over the HTML, the PDF, the fonts or font links, and the image files.
