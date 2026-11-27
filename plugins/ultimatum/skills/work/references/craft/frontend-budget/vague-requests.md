# Vague requests: base paths and worked examples

Read when a UI request names an area but no fault ("improve the UX", "it looks cheap", "people get lost", "work on the brand") and you need to know what to ask, what to measure, and which guide to open once the user answers. This file makes the rule concrete (`phase-routing.md` § 4).

Paths written as **pack/file.md** are in the website skill's craft folder (`skills/website/references/craft/`).

## The path in four steps

1. **Pick the area.** Run the table instead of guessing:

```bash
python3 data/craft/frontend-budget/vague_path.py match "the menu is confusing on my phone"
```

It prints the best area (and up to two close seconds; on a tie a specific area beats the catch-all `ux`), up to four questions, which guide each answer leads to, the first measurement, and what to do on "you decide". Exit 4 means no area matched: ask which area, with the listed areas as options. The table is `../../../../../data/craft/frontend-budget/vague-paths.csv`; `vague_path.py check` confirms every route still points at a real file.

2. **Measure before asking, when you can.** If the page runs, take the area's first check (usually `page_lint.py` and `render_check.py` in `data/craft/design-review-qa/` of the plugin). Don't show the findings yet. They decide which options you offer and which questions you can skip; a question the page already answers is a wasted turn.
3. **Ask once.** One message, at most four questions, each with options and a default. Skip any question the context answers: "which page" is settled by a screenshot they pasted, a URL that is open, or the last page edited.
4. **Route on the answer.** Load only the guides the answers point to, at most one lead and two supports per phase (`load-budget.md` § 1). An answer that belongs to another area switches path. Several answers become phases (`phase-routing.md` § 3).

"You decide", or no answer: take the area's fallback. Most are a scoped critique or a built "show me the 10" page beside the current one, then ask which finding to fix first.

## Areas at a glance

| Area | Sounds like | First measurement |
|---|---|---|
| ux | hard to use, confusing, clunky | lint, then render |
| navigation | can't find, get lost, menu | render at 390 and 1280 |
| hierarchy | nothing stands out, wall of text | render: first-screen fit |
| flows | signup, checkout, onboarding, form | walk the flow in a browser |
| identity-new | no brand yet, new product | deal a palette and type set |
| identity-existing | generic, AI-made, dated, inconsistent | lint: count the generic tells |
| looks | ugly, cheap, make it better | lint, then render |
| settings | preferences, admin area | render at 390 and 1280 |
| copy | wording, labels, tone | lint: copy rules |
| mobile | phone, small screen, touch | render at 320, 390, 768 |
| feel | janky, stiff, animation | DevTools Performance recording |
| speed | slow, loading, heavy | Lighthouse on a phone profile |
| access | keyboard, contrast, screen reader | render: contrast as painted |

## Worked example 1: "the landing page looks cheap"

- **Area:** `looks` (one strong word, no second area).
- **Measure:** `page_lint.py index.html` finds three cards in a row with the same icon-title-text shape, a purple-to-blue gradient heading and two stock phrases. `render_check.py index.html` finds body text at 3.9:1 on the hero image at 390 px.
- **Ask** (two questions skipped: the page is known, and the lint shows it is more than one colour problem):
  1. Polish what is there, or a new direction? *(default: new direction, because four of the findings are generic tells, not mistakes)*
  2. A site you find good, and what about it? *(default: none; I'll deal three directions)*
- **Answer:** "new direction; I like a calm developer-tool site I use." The answer moves the path to `identity-existing`: the lead is **hallmark/direction.md**, with **design-review-qa/mockup-step.md** as support so the user picks between built directions. Name the quality ("calm: one accent, lots of space, quiet type"), never copy the reference site.
- **Done when:** the picked direction is built and the lint and render findings from the first step are gone.

## Worked example 2: "users say they get lost in the app"

- **Area:** `navigation` ("get lost").
- **Measure:** render at 390 and 1280. At 390 the side menu is hidden behind an unlabelled icon; at 1280 it shows eleven items at the same weight.
- **Ask:**
  1. Which screen do people get lost from? *(options: the three most-used screens from the routes file)*
  2. Are the destinations right and only the menu is wrong, or is the structure wrong? *(default: structure, because eleven equal items usually means nothing was grouped)*
- **Answer:** "structure; we added pages over time." Lead: **design-review-qa/flows-and-consistency.md** to list every destination with its label and group them; support: **impeccable/adapt-contexts.md** for the phone version. First deliverable is a table of destinations, old label, new label and group, which the user approves before any code changes.
- **Done when:** the menu has at most seven top-level items, the current place is marked, and the phone menu has a visible label.

## Worked example 3: "the signup is bad"

- **Area:** `flows`.
- **Measure:** walk the flow with the Playwright recipe in **design-review-qa/qa-playwright-recipes.md**. Four steps; the password rule only shows after a failed submit; the first useful screen is a blank dashboard.
- **Ask:**
  1. Where do people stop? *(options: step 2, the password, the empty dashboard, don't know)*
  2. Is shortening the flow on the table, or must every step stay? *(default: shorten)*
- **Answer:** "don't know where, and yes shorten it." With no drop-off data, say so and suggest reading support messages or analytics before a redesign; meanwhile fix what is wrong whatever the data says. Lead: **impeccable/harden.md** (rules shown before the error, inline validation); support: **impeccable/delight-and-onboarding.md** (the first screen shows a sample, not an empty grid).
- **Done when:** the walk shows the rule before typing, no step lost data on back, and the first screen after signup has something to do.

## Worked example 4: "make it better", nothing else

- **Area:** none. `vague_path.py match "make it better"` exits 4: no area matched. Ask which area first, in one question, offering `looks`, `ux`, `flows` and `copy` with `looks` as the default (the most common meaning).
- If the user says "you decide", run the `looks` fallback on the page changed last, and say which page you chose.

## What goes wrong

- Asking eight questions. Four at most; the measurement should have answered the rest.
- Critiquing before asking. Listing faults answers a question nobody asked when they wanted a fresh look (`phase-routing.md` § 2).
- Loading every guide an area lists. Load the ones the answers point to.
- Treating a named reference site as a template. Take the quality, not the layout, copy or logo.
- Dropping the user's words. Put the original complaint at the top of the plan and check the result against it.
