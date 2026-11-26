# Phase routing for UI work

Read when a UI request arrives and you need to decide what it is, which phases it needs, and whether to ask first.

## 1. Read the project before choosing

Look for what is already decided: a design file at the root, token files, a theme config, a component folder, a component library in the package manifest, a brand guide the user linked. If any exist, they are rung 2 of the ladder (`precedence.md` § 1). If two disagree, ask which wins before writing code (`precedence.md` § 3).

## 2. Classify in three answers

1. **Job:** build new; change what exists (redesign, restyle, move to a library); review only; one craft (motion, copy, colour, type, layout); assets.
2. **Surface:** marketing page; product screen (dashboard, form, settings, table); one component; mobile web; native.
3. **Stack signals:** the library, styling system and framework from § 1.

A complaint about looks ("ugly", "generic", "cluttered") is a *change* job: the user wants a new direction, not a list of faults. An explicit "just review it" stays a review.

## 3. Phases

Run only the phases the task needs, in this order, each with its own lead (`load-budget.md` § 1):

| Phase | Runs when | Decides | Hand-off |
|---|---|---|---|
| Diagnose | the job is change | what is wrong, with evidence | a short findings list |
| Direction | new work, or a looks complaint | the concept, palette, type, motion budget | written into the design file or plan |
| Build | always | the code, following the project's system | a running page |
| Motion | something moves | timings, easing, reduced-motion versions | motion notes |
| Review | anything a user sees | pass or the fixes left | screenshots and the review report |

A request that mixes jobs ("restyle it and add animation") is several phases, in the order above. For a looks complaint, Diagnose and Direction run together: a critique alone does not give the new direction that was asked for.

## 4. Vague complaints: ask first

Call a complaint vague if it points at no specific fault ("still bad", "improve the UX", "work on the identity"). Naming the page only answers where, not what.

1. Load only the base. Read the project and the chat history. If the user says "still", a previous attempt fell short: find what that attempt changed.
2. If the app runs and a browser is at hand, look at the page the user most likely means, so the questions are grounded. Do not list faults yet.
3. Ask at most four questions in one message, each with options and a default, skipping what the context already answers. Typical axes: which area (flow, reading order, forms, identity, copy, mobile), what feels wrong about it, what to keep, a site they like.
4. Before the answers: no critique, no direction, no prototype. One neutral line about what exists is fine.
5. If the user says "you decide", run Diagnose with Direction on the main page, as for any complaint about looks.

## 5. Finish the same way

For anything a user sees: desktop and mobile screenshots read back (`../../browser-verification.md` § 5), the review pack's checks, a motion review if the change moves, fix and recapture. Without a browser, say that the visual check did not run; do not report it as passed. Run one finish reviewer per page, not every pack's reviewer in turn.
