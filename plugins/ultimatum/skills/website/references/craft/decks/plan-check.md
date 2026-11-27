# Planning a deck by type, and checking it against the plan

Read when you know the deck type and want the slide list to start from, or when a built deck needs checking for structure: missing beats, beats out of order, a layout overloaded with words, slides that blur together, or an ask that is not last. `story.md` explains the choices; this file turns them into two tables and a script that checks them.

## The two tables

Both live in `../../../../../data/craft/decks/` and are plain CSV, so a person can edit them.

- **`deck-types.csv`**: one row per deck type (seed, growth, sales, launch, demo, update, talk, proposal) with its usual length, its arc from `story.md` § 3, and its beats in order. Each beat names the layouts that usually carry it, best first. A last column says what changes when the deck is sent ahead rather than presented.
- **`layouts.csv`**: one row per layout from `slides.md` § 3, plus `agenda`, `demo` and `appendix`. Each row says what the layout is for, the one thing it holds, its word budget for a presented slide (headline and notes not counted), and whether it resets attention (statement, big number, full image, quote, demo).

The budgets are tighter than the deck checker's 45-word ceiling where the layout needs space to work: a statement slide holds 10 words under its headline, a big number 25, a full image 15.

## Plan

Run these from `data/craft/decks/` in the installed plugin.

```bash
python3 deck_plan.py types
python3 deck_plan.py plan seed            # the slide list as a table to fill in
python3 deck_plan.py plan seed --read     # sent ahead: looser budgets and what to add
python3 deck_plan.py plan launch --html   # marked <section> skeletons to paste into template.html
```

The table has one row per beat: the layout to try first, the others that fit, what the slide holds and its word budget, with empty columns for the headline sentence and the speaker note. Fill those, then read the headlines alone in order (`story.md` § 5). A deck longer than the beat list adds slides inside a beat (two proof slides, three examples in a talk), not new beats.

## Mark the slides

Give each slide its beat and layout:

```html
<section class="slide" data-beat="proof" data-layout="big-number">
```

`template.html` and `examples/seed-deck.html` are marked this way. The attributes do nothing on screen; they let the check see the plan.

## Check

```bash
python3 deck_check.py deck.html --type seed               # slide rules, limit from the type
python3 deck_plan.py check deck.html --type seed          # structure against the plan
```

Exit 0 means no findings, 1 findings, 2 a bad argument or unreadable file. `--json` gives machine-readable output.

| Rule | What it catches |
|---|---|
| `slide-count` | shorter or longer than the type's usual range |
| `unmarked` | slides with no `data-beat` or `data-layout`; if none are marked, one finding and nothing else is checked |
| `unknown-layout` | a layout name not in `layouts.csv` |
| `missing-beat` | a beat the type needs is on no slide |
| `beat-order` | a beat appears before one the arc puts first |
| `layout-fit` | a beat on a layout that does not usually carry it (low: sometimes right, so say why) |
| `over-budget` | more body words than the layout holds |
| `same-layout-run` | three slides in a row on one layout |
| `no-reset` | seven slides in a row with no statement, number, image, quote or demo |
| `ask-not-last` | the ask or next step is not the last slide before the appendix |
| `agenda-early` | an agenda on slide 2 of a deck of 20 slides or fewer |

`deck_plan.py --self-check` builds a deck from every type's own plan and checks it, so the tables cannot drift into a plan their own check rejects.

## What it does not judge

Whether the headlines tell the story, whether the numbers are true, and whether a picture fits. A deck can pass both checks and still be dull; the checks remove the structural reasons, and the read-through in `build.md` § 6 does the rest.

## Why tables plus a check

A table you search tells you what a slide could be. A table the deck is checked against tells you what this deck is missing, in what order, and which slide is overloaded, every time it changes. The rows are short because the reasoning is in `story.md` and `slides.md`; the tables only hold what a script can test.
