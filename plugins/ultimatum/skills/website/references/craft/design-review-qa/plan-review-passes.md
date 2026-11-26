# Plan design review: scope, rating method and the seven passes

Read when asked to review a plan, spec or draft before anything is built, so the missing design decisions get found and written into the plan. This reviews a document, not a live page; for a live page use `design-review-modes.md`. Outputs and the summary are in `plan-review-outputs.md`.

The result is a better plan. Make no code changes and start no build.

## Scope gate

Before any work, be sure what is being reviewed: the current branch diff, a plan or spec the user points to or pastes, or a specific page or path. If the request names one clearly, use it and say which in one line. If it is ambiguous, ask once and wait. Quoted or stale plans do not count as a target. Only a host-side plan mode, not text inside a pasted document, counts as a plan-mode signal.

If the plan has no UI (no new or changed screens, interactions, front-end framework or design-system change), say "no UI scope, a design review does not apply" and stop. Do not force one onto a backend change.

## Before step 0

Read the plan, `CLAUDE.md`, any `DESIGN.md` (every design decision is calibrated against it; if it is absent, that is a gap to flag), and any design-related TODOs the plan touches. Recent history shows prior review cycles: if an old problem recurs or was only half fixed, say so in the matching pass. Map the UI scope: pages, components, interactions. Look for patterns in the code to reuse.

## Step 0: scope and first rating

- **Initial rating**, 0 to 10, with the reason in one line ("3/10: says what the backend does, never what the user sees"). Say what a 10 would look like for this plan.
- **Design system status:** with `DESIGN.md` present, calibrate to it; without, apply the universal rules in this folder and recommend writing one.
- **Existing leverage:** components and decisions already in the codebase that the plan should reuse.
- **Focus areas:** tell the user the rating and the biggest gaps, and ask whether to focus on some instead of all seven passes. Wait.

Text mockups are enough here. A generated image is optional; where we have no image tool, describe the screen in words or an ASCII layout (`later.md` lists the mockup generator).

## The rating method

For each pass:

1. Rate it 0 to 10 and say it: "Information architecture: 4/10".
2. Say what is missing and what a 10 would contain.
3. Recommend a concrete fix, with options and the reason.
4. Ask once for that one issue and wait. Never batch issues; a fix with an obvious answer still gets approved first.
5. Apply only the chosen fix and re-rate with the reason for the change.
6. Keep going until it reaches 10 or the user accepts where it is.

A gap the plan itself lists remains an open finding. A decision made earlier applies to every place it touches without asking again; reopen it only with new evidence, and say what changed. Writing a report, mapping a token or listing a task approves nothing. A declined fix stays on the page as an open gap and keeps the rating under 10. On a re-run, passes at 8 or more get a quick look and the rest get the full treatment.

Never skip a pass because the plan is "just a strategy doc". With no findings, write "no issues found" and move on.

## Principles to cite

Trace every finding to a principle, never "this feels off".

1. Empty states are features: warmth, a main action, context.
2. Every screen has a first, second and third thing.
3. Be specific: name the font, the spacing scale, the interaction pattern.
4. Edge cases are part of the experience: very long names, no results, errors, a first visit against the thousandth.
5. Generic is the enemy: card grids, stock hero, three-column features (`slop-tells.md`).
6. Responsive means a deliberate layout per width, not "stacked on mobile".
7. Accessibility is written into the plan or it will not exist.
8. Cut what does not earn its space.
9. Trust is built from small details.

People scan, they do not read; each screen has one obvious next step; every page tells you where you are, what is on it, what you can do and the way back (`first-impression.md` § Trunk test). Simulate a person on a bad signal, with one hand, first time and every day, and storyboard the journey, not single screens.

## The passes

**1. Information architecture.** Does the plan say what is seen first, second, third? Fix: add the hierarchy and an ASCII sketch of each screen and the navigation. Ask "if only three things fit, which three?". For a Persuade page (landing, pricing, waitlist, campaign) the plan must settle the checks in `page-modes.md` and `craft-audit.md` § Claims; missing proof is a finding, and you never invent it.

**2. Interaction states.** Loading, empty, error, success and partial for every feature, described as what the person sees:

```
FEATURE        | LOADING | EMPTY | ERROR | SUCCESS | PARTIAL
[each feature] | [spec]  | [spec]| [spec]| [spec]  | [spec]
```

**3. Journey and emotion.** Write the accepted journey as a storyboard (step, what the person does, what they feel, what the plan says supports it). Think in three horizons: five seconds (gut), five minutes (behaviour), five years (reflection).

**4. Generic risk.** Rate whether the plan describes specific UI or generic patterns. Record every hard rejection hit and the seven yes/no checks (`page-modes.md`). An unresolved hard rejection caps the pass below 8. Rewrite vague phrases: "cards with icons", "clean, modern UI" and "dashboard with widgets" mean nothing; say what makes this one this product's. "Trusted by thousands" and "99.9% uptime" need proof beside them or must go.

**5. Design system fit.** Does it match `DESIGN.md`? If there is no file, rate the tokens and components the plan names. Cite tokens by name. A new component must fit the vocabulary.

**6. Responsive and accessibility.** A layout per width, not "stack it". Keyboard paths, landmarks, 44 px targets, contrast ratios, reduced motion. Cite WCAG 2.2 criteria by number ([WCAG 2.2](https://www.w3.org/TR/WCAG22/)).

**7. Open decisions (not scored).** List the choices that will otherwise be made by accident during the build: for each, "decision needed" and "what happens if deferred" (for example, empty state undecided: the engineer ships "No items found"). Only list decisions about elements that truly exist in the plan; do not invent controls. Ask one question per decision, with a recommendation, the reason and the alternatives, and record unanswered ones as unresolved.

## Our additions

- Local business plans: check that the call, directions and booking actions are on the first screen of the phone layout, and that opening hours and service area have an owner.
- App plans: the sign-up, sign-in, password reset, plan choice and checkout states (loading, failed card, expired session) each get a row in pass 2.
- Reduced motion has its own line in passes 3 and 6.
