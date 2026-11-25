# Design engine

Goal: a UI with one clear direction, tokens that carry it, and a verdict from a five-axis audit run on a real browser render. Add-on to the `ui` route (`ui.md`). An existing product language wins (`ui.md` §1); this file governs new or redesigned surfaces and the audit.

Order: **brief → direction → tokens → build → audit.** Do not skip to build.

## 1. Brief

- Write four lines: who uses it, the job, the one thing the screen must make obvious, and the constraints (brand, platform, accessibility target, content length range).
- Infer what you can from the repo and the request. Ask only for what changes the result; state the other defaults.

## 2. Direction

- Propose two or three directions. Each gets one line of rationale and one structural constraint (`ui.md` §3).
- Name the signature move and where it lives (one place, not everywhere).
- Drop any direction that looks like the default of the component kit in use, unless the brief asks for that look.
- Record the chosen direction in one paragraph; it is the reference for every later decision.

## 3. Tokens

- Define tokens before components. Minimum set:
  - colour roles: surface, raised surface, text, muted text, accent, danger, focus ring;
  - type scale: four to six steps;
  - spacing scale: one base unit, six to eight steps;
  - radius: two values at most; elevation: three levels at most;
  - motion: up to three durations and two easings (`motion.md` §3).
- Name roles, not hues: `--text-muted`, not `--gray-500`.
- Dark mode is a second value set for the same roles. Do not invert colours with a filter.
- Use the project's token location and format. Do not introduce a token system when one exists.

## 4. Build

- Build one real content sample first, then the states (§6). Do not build a grid of placeholders.
- Use real content lengths and real data shapes, not lorem ipsum.
- Every spacing value comes from the scale; every colour comes from a role.

## 5. Audit: five axes, scored 0 to 4

| Axis | Check on the rendered screen |
|---|---|
| Hierarchy | One primary action per view. Reading order matches importance at 375 px and 1280 px. Heading levels match visual weight. |
| Spacing and rhythm | Values from the scale. Related items closer than separate groups. Consistent vertical rhythm. No one-off margins. |
| Typography | Two families at most. Prose 45 to 75 characters per line. Body line height 1.4 to 1.6. Aligned numbers tabular. No body text under 14 px. |
| Colour and contrast | Text at least 4.5:1 (3:1 for large text). Focus indicator and control boundaries at least 3:1. Colour is never the only signal. Dark mode checked as its own pass. |
| States | Empty, loading, error, long text, zero/one/many items, disabled, focus, permission denied. Each designed, none left at browser default. |

Scores:

- **4**: meets the direction; no defect a user would notice; confirmed in screenshots.
- **3**: good; only nits that do not block a task.
- **2**: usable but inconsistent; one visible drag (for example, four type sizes where two were intended).
- **1**: users will stumble (wrong emphasis, failing contrast, a broken state).
- **0**: broken or missing on this axis.

Gate: ship needs 3 or more on every axis. Any 0 or 1 blocks. Report a table with one line of evidence per axis (the screenshot or the check that showed it).

## 6. States checklist

- **Empty:** say what is missing and give the next action.
- **Loading:** a skeleton that matches the final layout size; progress shown past about one second; no page-wide spinner alone.
- **Error:** say what happened and what the user can do; keep their input; no raw error codes.
- **Long text:** a 100-character unbroken string, a name that wraps to three lines, a translation 40% longer. Run `ult-browser --stress`.
- **Partial data:** a missing field does not blank the card.

## 7. Anti-generic rules

- No default gradient on backgrounds, buttons or heroes unless the brand has one.
- Do not centre everything. Align text to one edge; centre only short single blocks (an empty state, a confirmation).
- An icon needs a label or a common affordance (close, search, menu). Drop decorative icons on every card heading.
- No grid of identical icon + title + text cards as the whole page structure.
- No hero that is a big number, a small label and three stats unless the number is the story.
- One shadow or elevation scale; no glows.
- One radius pair; not every element pill-shaped.
- No stock illustration, emoji or fake testimonial, metric or logo as decoration.
- `ui.md` §6 lists more tells; a brief can earn any of them back.

## 8. Verify in a browser

- Run `ult-browser` at 375x812 and 1280x800, with `--stress` and, when there is motion, `--reduced-motion` (`browser-verification.md` §1).
- Read the screenshots back, and score the five axes from them, not from the code.
- If the browser step is skipped, say so and mark every score as provisional.

## 9. DESIGN.md (optional project file)

- Write it only when the user wants direction kept across sessions. Ask once.
- Location: `.ultimatum/DESIGN.md` (local, git-ignored with `.ultimatum/`). If the project already has a design doc, extend that file instead.
- Keep it under 40 lines: the direction paragraph, the signature move, the token roles and values, project thresholds for the audit, and up to five "never" rules taken from the user's corrections.
- Update it only when the user states a rule. Never store user copy, personal data or screenshots of real users.
