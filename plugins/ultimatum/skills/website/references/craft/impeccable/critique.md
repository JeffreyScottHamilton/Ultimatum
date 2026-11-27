# Design critique: heuristics, load and personas

Read when you are asked to critique a page or screen as a user would meet it, and want a scored review with clear priorities rather than a list of opinions.

The first-impression and page-mode passes are already in `../design-review-qa/first-impression.md` and `../design-review-qa/page-modes.md`. This file adds three lenses those do not cover: a heuristic score, a cognitive-load check and persona walks.

## Order of work

1. Find the source of the target (a file path beats a URL), and look at it rendered at the sizes it ships.
2. Form your own view before reading any automated detector output, so the tool does not anchor you.
3. Answer one question first: **could another product use this unchanged?** If yes, that is the headline finding.
4. Then run the three lenses below.
5. Report in full. Questions to the user go last, and only ones whose answer changes a fix (Ultimatum rule: ask only questions that change the outcome).
6. If you started a dev server, stop it.

## Lens 1: ten usability heuristics, 0 to 4 each

Use Jakob Nielsen's ten heuristics (<https://www.nngroup.com/articles/ten-usability-heuristics/>): visibility of system status; match with the real world; user control and freedom; consistency and standards; error prevention; recognition rather than recall; flexibility and efficiency; aesthetic and minimalist design; help users recover from errors; help and documentation.

Score each 0 (absent or harmful) to 4 (no issues found). On a marketing or story page, "flexibility and efficiency" and "help and documentation" may be marked n/a; the maximum is then 4 times the number scored.

Rough calibration from the source: most real interfaces land between 20 and 32 out of 40. Bands: 36 to 40 excellent; 28 to 35 good; 20 to 27 fair; 12 to 19 poor; below 12 failing. With n/a items, use the same cut points as percentages (90, 70, 50, 30).

## Lens 2: cognitive load

Working memory holds about four chunks (Cowan, 2001, <https://doi.org/10.1017/S0140525X01003922>). Five to seven competing items strain it; eight or more overload it. Of the three kinds of load (intrinsic to the task, extraneous from the design, germane to learning), the design can only cut the extraneous kind.

Eight checks, pass or fail:
1. One clear focus per view.
2. Content chunked into groups of four or fewer.
3. Related things grouped by space or rule, not just colour.
4. A visible hierarchy: you can tell what to read first.
5. One decision asked at a time.
6. Four or fewer options at any choice point.
7. Nothing the user must remember from a previous screen.
8. Detail is disclosed when needed, not all at once.

0 to 1 failures: low load. 2 to 3: moderate. 4 or more: high, and a priority finding.

Common culprits: a wall of equal options; asking the user to carry a value between screens; a key action hidden behind an unlabelled icon; internal jargon; every element at the same weight; the same action styled three ways; one screen doing three jobs; forcing a switch of context mid-task.

Useful limits: one primary button plus one or two secondary, the rest in a menu; five or fewer top-level nav items; four or fewer siblings per docs sidebar group.

## Lens 3: emotional path

Mark the peaks and lows along the main task. People judge an experience mostly by its strongest moment and its end. Look for a dip with no recovery, and for high-stakes steps (payment, deletion, sending) that lack reassurance about what happens next.

## Lens 4: persona walks

Walk the main task as two or three of these, chosen for the interface:

| Persona | Watches for |
|---|---|
| Power user | shortcuts, bulk actions, density, no forced tours |
| First-timer | what this is, what to do first, jargon |
| Assistive-tech user | keyboard path, names read aloud, focus order, contrast |
| Stress tester | empty, long, broken and slow states (see `harden.md`) |
| Distracted phone user | one thumb, interruptions, resuming where they left off |

Pick by type: a dashboard gets power user and assistive-tech user; a sign-up flow gets first-timer and distracted phone user; a data form gets stress tester. Add one or two personas drawn from the project's own audience when the brief names them.

## Severity

- **P0** blocks the task.
- **P1** major: many users fail or struggle.
- **P2** minor, with a workaround.
- **P3** polish.

Tie-break: if a user would contact support over it, it is P1 or worse.

## The report

1. Overall impression in two or three sentences, starting with the specificity verdict.
2. Two or three strengths worth keeping.
3. Three to five priority issues. Each: what is wrong (name the element), why it matters, the fix, and which refine move from `refine-moves.md` it calls for.
4. Persona red flags, one line each.
5. Minor notes.
6. Scores: heuristic total and band, cognitive-load rating.
7. Two to four questions tied to findings, each with concrete options. Skip them if there are fewer than three priority issues.

Write findings as plain statements ("the Save button sits below the fold at 390 px"), never "consider exploring". Respect any scope or off-limits areas the user set.
