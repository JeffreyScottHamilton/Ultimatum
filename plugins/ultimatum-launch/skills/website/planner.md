# Planner: brief, three directions, approval

For a new site or a major redesign. The Manager does this itself; a separate Planner or Designer helper only on a large job that splits cleanly.

## 1. Brief (`.ultimatum/brief.md`)

About one screen, with these sections:

- **For whom:** the visitors and what they came for.
- **First action:** the one thing a visitor should do first (call, book, order, sign up), and where it sits.
- **Pages and sections:** each page with its sections in order.
- **Mobile:** what a 375 px visitor sees first, how the menu works, what stacks or hides.
- **References:** the 3–5 sites the user likes (from intake or `brand/brand.md`) and what they like about each.
- **Assumptions:** what you decided without asking.
- **Placeholders:** each missing business fact as `[[PLACEHOLDER: what goes here]]`, e.g. `[[PLACEHOLDER: opening hours]]`.
- **Phases:** 2–4 build phases, each with the check that proves it done ("Hero and menu: at 375 px the book button shows without scrolling").
- **Browser checks:** 3–6 checks for the reviewer: main actions, 375/768/1440 px, a keyboard path, no console errors.

Ask the user only about gaps that would change the plan (online ordering or not, one page or several). Everything else gets a placeholder.

## 2. Layout first when it is the open question

If the structure itself is unclear (unusual page, many sections, the user is unsure), first build a **grayscale wireframe** in HTML: boxes, labels and real headings, no colour or photos. Get a yes on the layout, then build the styled directions.

## 3. Three directions

Follow `references/directions.md` and `references/design-rules.md`: name the page kind and its effect cap, deal each direction a palette, type pair and layout, run the lint, and remove one element. Real HTML and CSS, real headings, the user's exact words where they gave them and short realistic placeholder copy otherwise (say it is placeholder). No AI image mockups from ChatGPT or similar tools: the user judges something that already moves and scrolls.

## 4. Critic, then show and stop

Run the taste critic (`ultimatum-launch:taste-critic`) on the screenshots. Findings come as blocker, major, minor or nit; fix blockers and majors and re-run it, at most three rounds, until a direction scores 8/10 or better.

Then show the three: the 1440 and 375 screenshots, the local file to open, and 2–3 plain sentences each (who it suits, what the visitor sees first, how it moves). List open questions and **end your turn**. No production code until the user approves. Asking for changes means revise and show again; the user can say bolder, quieter, tighter, warmer and so on.

## 5. Record the approval

When the user approves, record it in their terms:

`ult website --approve "<direction picked, colours, type, motion, changes asked for>" --image <path to its 1440 screenshot>`

This writes an **Approved direction** section in the brief. The builder builds from it and the reviewer compares the real page with it.

## Existing site: finding your way

On a redesign of a larger site, if two focused searches have not shown how pages, styles and components connect, or the change touches three or more areas, run `ult map`, then Graphify (if installed) for one specific question. Confirm in the code before you plan around it.
