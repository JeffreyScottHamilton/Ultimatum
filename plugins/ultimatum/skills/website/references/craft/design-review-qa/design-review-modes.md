# Design review: scope, modes and ground rules

Read first when asked to audit, polish or "check if it looks good" on a page that already exists, or to review a design plan before it is built. It says which review to run, how deep, and what the reviewer may and may not do.

## Which review

| Situation | Run | File |
|---|---|---|
| A page or app exists and runs locally | Live design audit | this file, then `first-impression.md` onward |
| A plan, spec or mockup exists, nothing is built | Plan design review | `plan-review-passes.md` |
| UI is being built right now and each state needs a quick look | Build loop | `build-loop.md` |
| The question is "does it work", not "does it look right" | QA | `qa-modes-and-loop.md` |
| A landing or campaign page must convert | Live audit plus the craft audit | `craft-audit.md` |

If the target has no UI (a pure backend change), say a design review does not apply and stop.

## Inputs to settle before looking

- **Target URL.** A local dev URL or a static build served on `127.0.0.1`. Nothing remote unless the owner names it and accepts that the review touches a live site. No URL on a feature branch: scope to the pages the diff touches (see Diff-aware below).
- **Scope.** Whole site, one page, or one flow.
- **Depth.** Quick, Full or Deep (below).
- **Design system.** Look in the repo root for a design doc (`DESIGN.md`, `brand/brand.md`, a style guide), then for tokens the code ships: `:root` custom properties, Tailwind config, a theme file. Judge against that system; a deviation from the project's own system outranks a generic taste call. With neither, use the house rules (`../../website/design-rules.md`) and offer to write the inferred system down.
- **Auth.** Never type or ask for credentials. If the page bounces to a sign-in wall (URL contains `login`, `signin`, `auth` or `sso`), say so, ask the owner to supply a signed-in state, and review only what is reachable.

## Depth modes

| Mode | Pages | What runs |
|---|---|---|
| Quick | home plus 2 key pages | first impression, system extraction, short checklist; fastest route to a score |
| Full (default) | 5 to 8 reachable pages | all phases, responsive captures, 2 to 3 flows, full checklist |
| Deep | 10 to 15 pages | every flow, every checklist item; for pre-launch or a redesign |
| Diff-aware | pages the branch touched | map changed files to routes; compare quality before and after |
| Regression | as Full | then compare with the saved baseline (`scoring-and-baseline.md`) |

Diff-aware steps: list changed files against the branch's base (`git diff <base>...HEAD --name-only`, base from the repo's default branch, never assumed), map files to routes, find the running app on a local port, audit only those pages.

## Posture

- Think as a designer who can also read CSS: does it feel intentional, not only does it work.
- Every finding needs a screenshot, a measured value, or both. "The spacing feels off" is not a finding; "card gap is 13 px beside a 16 px section gap" is.
- Name generic patterns by their name (`slop-tells.md`); most owners cannot see them.
- 5 to 10 well-evidenced findings beat 20 vague ones. Depth over breadth.
- Write each finding down as you meet it, not at the end.
- Quick wins always get their own short list: the 3 to 5 fixes that each take under half an hour and move the page most.
- Fix noise by removal. When a page is busy, cut before adding; clarity beats consistency when the two clash.
- During discovery, judge the rendered page, not its source. Source is read only in the fix loop (`fix-loop.md`).

## How people behave (the lens for every judgement)

- They scan; nobody reads a page. Each screen is a signboard with one obvious next step.
- They pick the first plausible option and improvise, so the path of least effort has to be the correct one.
- They need orientation on every page (`first-impression.md` § Trunk test).
- Things that can be clicked must look clickable. Convention beats novelty. Welcome text and instructions get cut.
- Every confusion spends a little goodwill (`flows-and-consistency.md` § Goodwill).
- Phones raise every stake: thumb reach, 44 px targets, no hover.

## Tools we have

Playwright with headless Chromium, `ult-browser.mjs` for the standard checks (`../../../../work/references/browser-verification.md`), the scripts in `design-audit-recipes.md`, and the `taste-critic` agent for an independent score (`second-opinion.md`). No external design-generation service, no remote browser; steps that depended on one are listed in `later.md`.

Link: [WCAG 2.2](https://www.w3.org/TR/WCAG22/) is the accessibility baseline for every check in this folder.
