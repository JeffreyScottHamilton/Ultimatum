# Impeccable rebuild: coverage map

Source: pbakaus/impeccable at commit 3c5e75f (read only; nothing was installed or run, including its launcher, hooks and the native engine it downloads).
Our files: `plugins/ultimatum/skills/website/references/craft/impeccable/` (13 files) and `plugins/ultimatum/data/craft/impeccable/` (README and one example page with its Playwright check).

## Licences

| Part | Licence | Where it is stated |
|---|---|---|
| Everything not listed below | Apache-2.0 | root `LICENSE`, `package.json`, `Cargo.toml`, `skill/SKILL.src.md` front matter; `cursor-plugin/LICENSE` is Apache-2.0 too |
| `skill/reference/ios.md`, `skill/reference/android.md` | MIT (derived from ehmo/platform-design-skills) | `NOTICE.md` |
| fonts in `ui/component-review/fonts/` (Albert Sans, Alumni Sans, JetBrains Mono) | OFL-1.1 | the `*-OFL.txt` files next to them |
| MPL-2.0 | not found in any text file at this commit | the brief said the NOTICE adds it; `NOTICE.md` names only the MIT part. If it applies, it is to Rust crates pulled in at build time (`Cargo.lock`), which we neither use nor ship. Unverified. |

We ship none of the source's text, code or fonts. Our native-platform file is written from Apple's and Google's own guidelines, not from the MIT text.

## Inventory

All 41 files in `skill/reference/` were read (424,200 bytes), plus `skill/SKILL.src.md`, the four helper briefs in `skill/agents/` (headings and check lists), `NOTICE.md` and the command list in `skill/scripts/command-metadata.json`. Tool and plumbing folders were sized, not read:

| Folder | Size | Files |
|---|---|---|
| `skill/reference/` | 492 KB | 41 |
| `skill/agents/` | 44 KB | 4 |
| `crates/` | 17740 KB | 532 |
| `docs/` | 1148 KB | 24 |
| `tests/` | 24664 KB | 2426 |
| `ui/` | 860 KB | 30 |
| `extension/` | 228 KB | 24 |
| `demos/` | 72 KB | 6 |
| `cursor-plugin/` | 2404 KB | 67 |
| `vscode/` | 12 KB | 2 |
| `plugin/` | 2384 KB | 65 |
| `cli/` | 64 KB | 7 |
| `browser-bundle/` | 156 KB | 11 |

Not read in detail: top-level `README.md`, `DESIGN.md`, `PRODUCT.md`, `AGENTS.md`, `CLAUDE.md` (these describe the project and its own build, not design craft), and the Rust detector rules in `crates/`.

## Statuses

- **covered**: written new in our own words in the Impeccable folder.
- **expanded**: covered, and taken further with primary sources (MDN, WCAG 2.2, Apple HIG, Material 3) or a runnable example.
- **merged**: already held by another craft folder; the Impeccable file points there instead of repeating it.
- **later**: needs tooling we do not ship; see `later.md`.

Statuses were set per source file, then corrected item by item where an item belonged elsewhere.

## Merges

| Existing file | What it already held | Pointer added |
|---|---|---|
| `design-review-qa/page-modes.md` | the four page modes, hard rejections, browser-surface theming, depth and heading-space reflexes, the three looks to distrust | from `direction-process.md`, `surface-details.md`; back-pointer added to page-modes |
| `design-review-qa/slop-tells.md` | the refuse list and overused faces | from `direction-process.md`, `audit-scorecard.md` |
| `design-review-qa/craft-audit.md`, checklists, scoring | the review flow and claim ownership | from `direction-process.md`, `microcopy.md` |
| `hallmark/redesign.md` | redesign | back-pointer to `refine-moves.md` |
| `hallmark/responsive.md` | breakpoints, units, safe areas, tables | back-pointer to `adapt-contexts.md` |
| `hallmark/craft-type-colour.md`, `dark-mode.md`, `interaction-and-states.md` | base type, OKLCH colour, dark mode, eight states | from `surface-details.md` |
| `emil-motion/*` | curves, springs, reduced motion, libraries, frame budget, worst-case data | from `delight-and-onboarding.md`, `ambitious-tech.md`; back-pointer from `worst-case-data.md` to `harden.md` |
| `taste/accessibility.md`, `copy.md`, `motion.md`, `performance.md`, `photos.md`, `page-plans.md` | access basics, page copy, motion, speed, photos, page pacing | back-pointers from accessibility, copy and motion |
| `website/design-rules.md` § 5 | the revision verbs | from `refine-moves.md` (shared file left untouched) |
| `website/planner.md`, `directions.md` | the brief and three-direction flow | from `direction-process.md` |

## Map

| Id | Source item (our words) | Our file | Status |
|---|---|---|---|
| SK1 | finish the deliverable fully | design-review-qa/page-modes.md | merged |
| SK2 | ambition scales with mode (persuade/experience bold; operate/read precise) | design-review-qa/page-modes.md | merged |
| SK3 | look at render at shipped sizes, batch fixes per look | design-review-qa/page-modes.md | merged |
| SK4 | launcher context step | later.md | later |
| SK5 | load craft-floor right before any UI edit | design-review-qa/page-modes.md | merged |
| SK6 | brief beats taste warnings | design-review-qa/page-modes.md | merged |
| SK7 | refine keeps identity, redesign replaces look but keeps truth | refine-moves.md | covered |
| SK8 | no hate/militarist emblems as decoration | design-review-qa/page-modes.md | merged |
| SK9 | missing design doc != greenfield | direction-process.md § Starting state | covered |
| SK10 | four modes by surface not product (persuade, operate, read, experience) | design-review-qa/page-modes.md | merged |
| SK11 | 24-command table | later.md § command menu | later |
| SK12 | routing/pin/hooks/doctor | later.md | later |
| SK13 | never fix drift as side quest | design-review-qa/page-modes.md | merged |
| CF1 | contrast 4.5/3, tint secondary text on coloured grounds | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF2 | shadows need offset+blur, zero-offset halo = decoration | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF3 | more space above heading than below | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF4 | measure 65-75ch, display <=6rem, tracking floor -0.04em, balanced headings | hallmark/craft-type-colour.md | merged |
| CF5 | one authored motion moment, expo ease-out from visible default, blur/clip-path/mask allowed | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF6 | states hover/disabled/loading/error/empty + focus | hallmark/interaction-and-states.md | merged |
| CF7 | theme browser surfaces: ::selection, caret, scrollbar, focus ring, underline offset, tabular numerals | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF8 | controls name action, errors name problem+fix | microcopy.md | covered |
| CF9 | every brief item findable | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF10 | equal icon cards / nested cards | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF11 | hero-metric template | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF12 | eyebrow kicker ban | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF13 | section numbers 01/02 | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF14 | needless modal | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF15 | gradient text | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF16 | decorative glass | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF17 | coloured side border >1px | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF18 | hard offset shadow outside neobrutal | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF19 | sparkline/ring filler | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF20 | mono as costume | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF21 | system display face | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF22 | emoji/unicode as icons | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF23 | geometric mask faking organic edge -> real alpha matte | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF24 | light/dark from use scene | direction-process.md § Finding a world | covered |
| CF25 | tracking -0.02..-0.03 best | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF26 | one elevation (border OR shadow), card radius 12-16, pills only small controls | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF27 | no sketch SVG/feTurbulence grain, geometry SVG fine | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF28 | stripes/grids only with real subject | design-review-qa/page-modes.md, slop-tells.md | merged |
| CF29 | claims from supplied truth, label illustrative values | design-review-qa/craft-audit.md § 2 | merged |
| RT1 | context-aware menu from signals JSON | later.md | later |
| RT2 | never auto-run a command | later.md § command menu | later |
| RT3 | 2-3 picks with reasons | later.md § command menu | later |
| RT4 | link https://impeccable.style/docs/ | later.md § command menu | later |
| MP1 | opening: offer clear, action in working form (search box, slots, add to cart), proof only this product has | design-review-qa/page-modes.md | merged |
| MP2 | world carries page, never a painted poster of it | design-review-qa/page-modes.md | merged |
| MP3 | parts keep working wherever world puts them | design-review-qa/page-modes.md | merged |
| MP4 | object world = one object, one scale, real form (book = two pages) | design-review-qa/page-modes.md | merged |
| MP5 | comps 2-3 bolder not cleaner | design-review-qa/page-modes.md | merged |
| MO1 | world lends only type, palette, density, one signature move | surface-details.md § Product UI | covered |
| MO2 | grey+one accent = default not restraint | surface-details.md § Product UI | covered |
| MO3 | tool/instrument worlds become costume | surface-details.md § Product UI | covered |
| MO4 | first viewport = shell, work areas, first data, then signature move (e.g. service health as transit map) | surface-details.md § Product UI | covered |
| MO5 | standard controls | surface-details.md § Product UI | covered |
| MO6 | real content, plausible data, one interesting state | surface-details.md § Product UI | covered |
| MO7 | state colours only where meaningful; moving headline number shows history | surface-details.md § Product UI | covered |
| MO8 | variants vary organisation (rail/top bar/command-first, density), distinct at thumbnail | design-review-qa/page-modes.md | merged |
| MO9 | self-check: name covered, reads as category product? | surface-details.md § Product UI | covered |
| MR1 | world owns frame (masthead, rail, openers, code/table setting), column stays calm | design-review-qa/page-modes.md | merged |
| MR2 | publishing traditions transfer best (reference books, specimens, timetables, field guides) | design-review-qa/page-modes.md | merged |
| MR3 | first viewport: nav+position, title, opening answer, column, way forward | design-review-qa/page-modes.md | merged |
| MR4 | measure 60-75ch, ~16px body, mono only for code/labels | design-review-qa/page-modes.md | merged |
| MR5 | real hardest content in comps | design-review-qa/page-modes.md | merged |
| MR6 | variants vary nav model/margins, never the column | design-review-qa/page-modes.md | merged |
| MR7 | self-check: where am I, could this be any product's docs | design-review-qa/page-modes.md | merged |
| OP1 | slop test = category-fluent user trusts it at once | surface-details.md § Product UI | covered |
| OP2 | one family fine | surface-details.md § Product UI | covered |
| OP3 | fixed rem scale not fluid | surface-details.md § Product UI | covered |
| OP4 | ratio 1.125-1.2 | surface-details.md § Product UI | covered |
| OP5 | prose 65-75ch, tables 120ch+ ok | surface-details.md § Product UI | covered |
| OP6 | restrained colour floor | surface-details.md § Product UI | covered |
| OP7 | full state vocabulary standardized | surface-details.md § Product UI | covered |
| OP8 | accent only actions/selection/state | surface-details.md § Product UI | covered |
| OP9 | second neutral layer for chrome | surface-details.md § Product UI | covered |
| OP10 | structural responsive | surface-details.md § Product UI | covered |
| OP11 | every control 7 states | surface-details.md § Product UI | covered |
| OP12 | skeletons not spinners | surface-details.md § Product UI | covered |
| OP13 | empty states teach | surface-details.md § Product UI | covered |
| OP14 | consistent affordances | surface-details.md § Product UI | covered |
| OP15 | overlays escape overflow: dialog, popover API, fixed, portal | surface-details.md § Product UI | covered |
| OP16 | 150-250ms | surface-details.md § Product UI | covered |
| OP17 | motion = state only | surface-details.md § Product UI | covered |
| OP18 | no page-load choreography | surface-details.md § Product UI | covered |
| OP19 | avoid display fonts in labels, reinvented controls, saturated inactive states, modal-first | surface-details.md § Product UI | covered |
| OP20 | permissions: system fonts, standard nav, density, sameness | surface-details.md § Product UI | covered |
| SH1 | discovery before code | direction-process.md § Questions | covered |
| SH2 | 2-3 questions per round, usually one round | direction-process.md § Questions | covered |
| SH3 | assert likely reading, invite correction | direction-process.md § Questions | covered |
| SH4 | round 1 purpose/people/outcome/unique truth | direction-process.md § Questions | covered |
| SH5 | round 2 content ranges, states, fidelity, untouchables, constraints | direction-process.md § Questions | covered |
| SH6 | never ask for CSS values | direction-process.md § Questions | covered |
| SH7 | brief 7 parts (job, outcome, direction, scope, states, interaction, constraints) | direction-process.md § Questions | covered |
| SH8 | 3-5 bullets when settled | direction-process.md § Questions | covered |
| SH9 | confirm then stop, no code | direction-process.md § Questions | covered |
| RM1 | split regions by what varies independently (content, moving parts, structure) | later.md § region-map | later |
| RM2 | comp crops are reference not production assets | later.md § region-map | later |
| NW1 | three docs own truth: product facts / durable visual system / per-surface brief | direction-process.md | covered |
| NW2 | four starting states: redesign, established world, incomplete brand, none | direction-process.md | covered |
| NW3 | local addition inherits surface, never a new identity | direction-process.md | covered |
| NW4 | ask 2-3 questions by mode (persuade: who acts, belief, proof; operate: task, info, states, frequency; read: qu | direction-process.md | covered |
| NW5 | always ask success, untouchables, what would feel wrong | direction-process.md | covered |
| NW6 | extend surface = no concept round | direction-process.md | covered |
| NW7 | whole surface in world = 5-7 structures, deal three | direction-process.md | covered |
| NW8 | new world: name mechanism, scene, cultural home, the category rut and its opposite | direction-process.md | covered |
| NW9 | seven candidate systems from audience's culture, each with why + look | direction-process.md | covered |
| NW10 | concept-seed dice roll assignment | later.md | later |
| NW11 | present one committed direction with named raises: world, first viewport, path, signature interaction, reach,  | direction-process.md | covered |
| NW12 | challenger verdict wins/competitive/declined on two axes (audience identification, product clarity) | direction-process.md | covered |
| NW13 | donation = discipline, never clothes (button shadow, face) | direction-process.md | covered |
| NW14 | always offer the plain category standard as user's door, never recommend it | direction-process.md | covered |
| NW15 | operate/read code-led | direction-process.md | covered |
| NW16 | colour strategy first: restrained / committed 30-60% / full palette 3-4 roles / drenched | direction-process.md | covered |
| NW17 | colour at page scale | direction-process.md | covered |
| NW18 | light/dark from one-sentence physical scene | direction-process.md | covered |
| NW19 | overused faces list (Fraunces, Playfair, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk/Mono, IBM P | design-review-qa/slop-tells.md § Fonts | merged |
| NW20 | four AI clusters: cream+serif+terracotta; near-black+neon glow; editorial hairline+italic serif+tracked mono;  | design-review-qa/page-modes.md § Calibration | merged |
| NW21 | category-guess self-check | direction-process.md | covered |
| NW22 | negative constraints ban devices not energy | direction-process.md | covered |
| NW23 | bookish subject != cream | direction-process.md | covered |
| NW24 | model prior: warm subjects drift to cream/lamplight, treat as spent | direction-process.md | covered |
| NW25 | direction contract in brief, never shipped in source/DOM/comments/data attrs | direction-process.md | covered |
| NW26 | design doc written after build from the build | direction-process.md | covered |
| NW27 | surface-brief/build-phase/comp-spec gates | later.md | later |
| NW28 | comp is spatial contract, models over-believe recreations | direction-process.md | covered |
| NW29 | plates for raster regions, transparent PNG | later.md § visualize | later |
| NW30 | sections inherit comp system | direction-process.md | covered |
| NW31 | responsive incl 1280-1600 desktop, no fixed px grids | direction-process.md | covered |
| NW32 | first viewport is a thesis; memory test | direction-process.md | covered |
| NW33 | prove not claim; synthetic demo data labelled | direction-process.md | covered |
| NW34 | author content assets | taste/photos.md | merged |
| NW35 | build the named technique (canvas, WebGL, view transitions) not an imitation | direction-process.md | covered |
| NW36 | pace scroll: dense then quiet, real close | taste/page-plans.md | merged |
| NW37 | real verified photos of the subject's object; verify URLs | direction-process.md | covered |
| NW38 | motion once, content visible by default | emil-motion/choreography.md | merged |
| NW39 | one batched screenshot round desktop+mobile (+user's actual width); drive every state, check overlap/clipping; | direction-process.md | covered |
| NW40 | capture validity: settle motion, full-page from top, open each file and confirm | design-review-qa (capture rules) | merged |
| NW41 | finish reviewer dispositions recapture/rebuild/ship/fix; two fix rounds unattended | later.md | later |
| NW42 | report verdict at actual scope only | direction-process.md | covered |
| NW43 | documenter writes design doc after | later.md | later |
| CQ1 | two isolated assessments (design review vs detector) via subagents, degraded banner if inline | later.md | later |
| CQ2 | review before detector output to avoid anchoring | critique.md | covered |
| CQ3 | resolve target to source path over URL | critique.md | covered |
| CQ4 | stop any server you started | critique.md | covered |
| CQ5 | report fully, then questions last | critique.md | covered |
| CQ6 | design-specificity verdict first: could another product use it unchanged | critique.md | covered |
| CQ7 | holistic: hierarchy, IA, fit, discoverability, type, colour, a11y, states, copy, edge cases | critique.md | covered |
| CQ8 | cognitive load: >4 visible options flagged | critique.md | covered |
| CQ9 | emotional arc: peak-end, valleys, reassurance at high stakes | critique.md | covered |
| CQ10 | Nielsen 10 heuristics 0-4 each, n/a allowed for 7 and 10 on persuade/experience, max = 4 x scored | critique.md | covered |
| CQ11 | most real UIs 20-32/40 | critique.md | covered |
| CQ12 | bands 36-40 / 28-35 / 20-27 / 12-19 / 0-11, or by % 90/70/50/30 | critique.md | covered |
| CQ13 | report: impression, 2-3 strengths, 3-5 priority issues (what, why, fix, command), persona red flags, minor not | critique.md | covered |
| CQ14 | P0 blocking, P1 major, P2 minor with workaround, P3 polish; tie-break: would user contact support -> P1+ | critique.md | covered |
| CQ15 | be specific, name the element, no "consider exploring" | critique.md | covered |
| CQ16 | 2-4 follow-up questions tied to findings with concrete options; skip only if <3 priority issues | critique.md | covered |
| CQ17 | action list mapped to commands, respect scope/off-limits | critique.md | covered |
| CQ18 | snapshot persistence and 5-run trend line | later.md | later |
| CQ19 | cognitive load types intrinsic/extraneous/germane | critique.md | covered |
| CQ20 | 8-item checklist (single focus, chunks <=4, grouping, hierarchy, one decision at a time, <=4 options, no memor | critique.md | covered |
| CQ21 | working memory ~4 (Cowan 2001); 5-7 strain, 8+ overload | critique.md | covered |
| CQ22 | 1 primary + 1-2 secondary buttons, rest in menu; nav <=5 top items; docs sidebar <=4 siblings | critique.md | covered |
| CQ23 | eight violations: option wall, memory bridge, hidden location, jargon, flat weight, inconsistent pattern, mult | critique.md | covered |
| CQ24 | personas: power user, first-timer, a11y-dependent, stress tester, distracted mobile; pick 2-3 per interface ty | critique.md | covered |
| CQ25 | desktop apps via remote-debugging port on 127.0.0.1 | later.md | later |
| AU1 | code-level, document not fix | audit-scorecard.md | covered |
| AU2 | five dimensions scored 0-4: a11y, performance, theming, responsive, implementation integrity; total /20 bands  | audit-scorecard.md | covered |
| AU3 | a11y: contrast 4.5/3 (7 AAA), reduced motion keeps state change (flag global 0.01ms kill), ARIA, focus/tab ord | audit-scorecard.md | covered |
| AU4 | perf: layout thrash, layout-property animation, unbounded blur/filter, lazy images, will-change only targeted, | audit-scorecard.md | covered |
| AU5 | theming: hard-coded colours, dark mode contrast, token mixing, theme switch staleness | audit-scorecard.md | covered |
| AU6 | responsive: fixed widths, 44px comfort / WCAG 2.5.8 24px min w/ exceptions, touch gestures fighting scroll, ho | audit-scorecard.md | covered |
| AU7 | RTL only when dir=rtl declared: physical props vs logical (margin-inline-start, inset-inline-start), centering | audit-scorecard.md | covered |
| AU8 | integrity: drift, decorative content, interchangeable structure | audit-scorecard.md | covered |
| AU9 | issue record: severity, location, category, impact, WCAG ref, fix | audit-scorecard.md | covered |
| AU10 | systemic patterns section; positives section; keep P3 few; verify before reporting | audit-scorecard.md | covered |
| PO1 | refinement never hidden redesign; say if concept wrong | refine-moves.md § Polish | covered |
| PO2 | detector result = defect evidence, not quality proof | refine-moves.md § Polish | covered |
| PO3 | classify drift: missing token / one-off / conceptual mismatch / local defect, fix at narrowest level | refine-moves.md § Polish | covered |
| PO4 | gather: completeness, bar, time, known unfinished, real states/lengths/roles/inputs | refine-moves.md § Polish | covered |
| PO5 | triage order: broken/data loss/misleading/inaccessible -> missing states -> flow/hierarchy/drift -> visual/mot | refine-moves.md § Polish | covered |
| PO6 | don't perfect one corner | refine-moves.md § Polish | covered |
| PO7 | match neighbour mental models, save behaviour, optimistic vs pessimistic | refine-moves.md § Polish | covered |
| PO8 | optical alignment; localization expansion, zoom, font loading | hallmark/craft-type-colour.md | merged |
| PO9 | image aspect ratio to stop CLS | taste/performance.md | merged |
| PO10 | states incl success; motion interruptible | refine-moves.md § Polish | covered |
| PO11 | long/missing/localized/offline/slow/permission content | refine-moves.md § Polish | covered |
| PO12 | remove debug, dead code; promote tokens only when reused | refine-moves.md § Polish | covered |
| PO13 | walk again with mouse, keyboard, touch; console errors, CLS, latency | refine-moves.md § Polish | covered |
| PO14 | finish with clean diff | refine-moves.md § Polish | covered |
| DI1 | complexity sources: too many elements, variation, overload, noise, hierarchy, feature creep | refine-moves.md § Simplify | covered |
| DI2 | one primary goal; 80/20 | refine-moves.md § Simplify | covered |
| DI3 | IA: cut scope, progressive disclosure, merge actions, one primary action | refine-moves.md § Simplify | covered |
| DI4 | palette 1-2 brand + neutrals, semantic colours with non-colour cue; one family, 3-4 sizes, 2-3 weights; no nes | design-review-qa/slop-tells.md | merged |
| DI5 | layout: linear flow, inline secondary content, one alignment | refine-moves.md § Simplify | covered |
| DI6 | interaction: smart defaults, inline edit over modal, drop steps, one next action | refine-moves.md § Simplify | covered |
| DI7 | copy: active voice, no restating headers | refine-moves.md § Simplify | covered |
| DI8 | code: dead CSS, fewer variants (3 cover 90%) | refine-moves.md § Simplify | covered |
| DI9 | avoid removing needed function/a11y/decision info, mystery != minimal | refine-moves.md § Simplify | covered |
| DI10 | verify faster task, still complete | refine-moves.md § Simplify | covered |
| DI11 | record what was removed and alternative access | refine-moves.md § Simplify | covered |
| HA1 | extreme inputs | emil-motion/worst-case-data.md | merged |
| HA2 | error scenarios | harden.md (+ MDN links, example page) | expanded |
| HA3 | 30-40% text expansion | emil-motion/worst-case-data.md | merged |
| HA4 | text overflow: min-width 0, clamp, overflow-wrap | harden.md (+ MDN links, example page) | expanded |
| HA5 | logical properties | harden.md (+ MDN links, example page) | expanded |
| HA6 | Arabic-script ZWNJ, yeh and kaf variants | harden.md (+ MDN links, example page) | expanded |
| HA7 | locale digits and calendars | harden.md (+ MDN links, example page) | expanded |
| HA8 | UTF-8 throughout | harden.md (+ MDN links, example page) | expanded |
| HA9 | Intl dates and numbers | harden.md (+ MDN links, example page) | expanded |
| HA10 | plural rules | harden.md (+ MDN links, example page) | expanded |
| HA11 | network, form and API errors by status | harden.md (+ MDN links, example page) | expanded |
| HA12 | graceful degradation | harden.md (+ MDN links, example page) | expanded |
| HA13 | empty, loading, large and concurrent states | harden.md (+ MDN links, example page) | expanded |
| HA14 | interrupted gestures: pointercancel, lostpointercapture | harden.md (+ MDN links, example page) | expanded |
| HA15 | permission states | harden.md (+ MDN links, example page) | expanded |
| HA16 | client and server validation | harden.md (+ MDN links, example page) | expanded |
| HA17 | keyboard, screen reader, high contrast | harden.md (+ MDN links, example page) | expanded |
| HA18 | slow connections | harden.md (+ MDN links, example page) | expanded |
| HA19 | memory leaks | harden.md (+ MDN links, example page) | expanded |
| HA20 | debounce and throttle | harden.md (+ MDN links, example page) | expanded |
| HA21 | testing list | harden.md (+ MDN links, example page) | expanded |
| HA22 | evidence statement | harden.md (+ MDN links, example page) | expanded |
| OZ1 | measure first | taste/performance.md, emil-motion/performance.md | merged |
| OZ2 | Core Web Vitals targets | taste/performance.md, emil-motion/performance.md | merged |
| OZ3 | images | taste/performance.md, emil-motion/performance.md | merged |
| OZ4 | bundle size | taste/performance.md, emil-motion/performance.md | merged |
| OZ5 | CSS | taste/performance.md, emil-motion/performance.md | merged |
| OZ6 | fonts | taste/performance.md, emil-motion/performance.md | merged |
| OZ7 | loading order | taste/performance.md, emil-motion/performance.md | merged |
| OZ8 | contain and content-visibility | taste/performance.md, emil-motion/performance.md | merged |
| OZ9 | paint cost | taste/performance.md, emil-motion/performance.md | merged |
| OZ10 | 60fps | taste/performance.md, emil-motion/performance.md | merged |
| OZ11 | React memo | taste/performance.md, emil-motion/performance.md | merged |
| OZ12 | network | taste/performance.md, emil-motion/performance.md | merged |
| OZ13 | monitoring | taste/performance.md, emil-motion/performance.md | merged |
| OZ14 | avoid list | taste/performance.md, emil-motion/performance.md | merged |
| CL1 | audit the language | microcopy.md | covered |
| CL2 | message hierarchy | microcopy.md | covered |
| CL3 | actions | microcopy.md | covered |
| CL4 | forms | microcopy.md | covered |
| CL5 | errors: what, why, recover | microcopy.md | covered |
| CL6 | loading, empty, success | microcopy.md | covered |
| CL7 | help text | microcopy.md | covered |
| CL8 | translatable messages | microcopy.md | covered |
| CL9 | alt text | microcopy.md | covered |
| CL10 | label alignment | microcopy.md | covered |
| CL11 | verify | microcopy.md | covered |
| AD1 | input detection | adapt-contexts.md | covered |
| AD2 | phone strategy | adapt-contexts.md | covered |
| AD3 | tablet strategy | adapt-contexts.md | covered |
| AD4 | desktop strategy | adapt-contexts.md | covered |
| AD5 | print | adapt-contexts.md | covered |
| AD6 | email | adapt-contexts.md | covered |
| AD7 | breakpoints from content | hallmark/responsive.md | merged |
| AD8 | container queries | adapt-contexts.md | covered |
| AD9 | touch targets | hallmark/responsive.md | merged |
| AD10 | safe areas, viewport-fit | hallmark/responsive.md | merged |
| AD11 | srcset and picture | adapt-contexts.md | covered |
| AD12 | custom-control gesture checks | adapt-contexts.md | covered |
| AD13 | real-device testing | adapt-contexts.md | covered |
| AN1 | motion by mode | delight-and-onboarding.md § Motion thesis | covered |
| AN2 | each motion has a job | delight-and-onboarding.md § Motion thesis | covered |
| AN3 | motion thesis: focal, continuity, feedback, budget | delight-and-onboarding.md § Motion thesis | covered |
| AN4 | material by meaning | delight-and-onboarding.md § Motion thesis | covered |
| AN5 | runtime choice | emil-motion/libraries-and-toasts.md | merged |
| AN6 | reduced motion keeps feedback | emil-motion/reduced-motion.md | merged |
| BO1 | scope is the user's | refine-moves.md § Turn up | covered |
| BO2 | amplify the owned system | refine-moves.md § Turn up | covered |
| BO3 | keep claims | refine-moves.md § Turn up | covered |
| BO4 | commit to the move | refine-moves.md § Turn up | covered |
| BO5 | own rhythm | refine-moves.md § Turn up | covered |
| BO6 | skeleton test | refine-moves.md § Turn up | covered |
| QU1 | intensity sources | refine-moves.md § Tone down | covered |
| QU2 | desaturate 70-85% | refine-moves.md § Tone down | covered |
| QU3 | 10% accent | refine-moves.md § Tone down | covered |
| QU4 | tinted greys | refine-moves.md § Tone down | covered |
| QU5 | never grey on colour | refine-moves.md § Tone down | covered |
| QU6 | reduce weight | refine-moves.md § Tone down | covered |
| QU7 | remove decoration | refine-moves.md § Tone down | covered |
| QU8 | motion 10-20px, no bounce | refine-moves.md § Tone down | covered |
| QU9 | avoid list | refine-moves.md § Tone down | covered |
| CO1 | use by mode | surface-details.md § Colour roles | covered |
| CO2 | audit colour | surface-details.md § Colour roles | covered |
| CO3 | role list | surface-details.md § Colour roles | covered |
| CO4 | system scale | hallmark/craft-type-colour.md | merged |
| CO5 | dark mode not inverted | hallmark/dark-mode.md | merged |
| CO6 | data needs non-colour cues | surface-details.md § Colour roles | covered |
| DE1 | use by mode | delight-and-onboarding.md § Delight | covered |
| DE2 | find opportunities | delight-and-onboarding.md § Delight | covered |
| DE3 | one delight thesis | delight-and-onboarding.md § Delight | covered |
| DE4 | emotional moments | delight-and-onboarding.md § Delight | covered |
| DE5 | protect list | delight-and-onboarding.md § Delight | covered |
| LA1 | use by mode | surface-details.md § Layout | covered |
| LA2 | squint test | surface-details.md § Layout | covered |
| LA3 | grouping | surface-details.md § Layout | covered |
| LA4 | rhythm | surface-details.md § Layout | covered |
| LA5 | structure | surface-details.md § Layout | covered |
| LA6 | density | surface-details.md § Layout | covered |
| LA7 | adaptation | surface-details.md § Layout | covered |
| LA8 | extremes | surface-details.md § Layout | covered |
| LA9 | spatial thesis | surface-details.md § Layout | covered |
| LA10 | 4-unit base | surface-details.md § Layout | covered |
| LA11 | gap | surface-details.md § Layout | covered |
| LA12 | optical corrections after render | surface-details.md § Layout | covered |
| TY1 | use by mode | surface-details.md § Type | covered |
| TY2 | authority | surface-details.md § Type | covered |
| TY3 | hierarchy | surface-details.md § Type | covered |
| TY4 | scale | hallmark/craft-type-colour.md | merged |
| TY5 | reading measure 45-75ch | surface-details.md § Type | covered |
| TY6 | stress | hallmark/craft-type-colour.md | merged |
| TY7 | delivery | surface-details.md § Type | covered |
| TY8 | 16px floor | surface-details.md § Type | covered |
| TY9 | light-on-dark compensation | surface-details.md § Type | covered |
| TY10 | text-wrap balance and pretty | surface-details.md § Type | covered |
| TY11 | paragraph rhythm | surface-details.md § Type | covered |
| OV1 | propose 2-3 directions first | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV2 | view transitions | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV3 | @starting-style | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV4 | springs | emil-motion/springs.md | merged |
| OV5 | scroll-driven animation | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV6 | WebGL, WebGPU, Canvas, SVG filters | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV7 | virtual scroll | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV8 | @property | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV9 | Web Animations API | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV10 | workers, OffscreenCanvas, WASM | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV11 | Web Audio opt-in | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV12 | progressive enhancement | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV13 | 60fps, lazy init, pause offscreen | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV14 | never list | ambitious-tech.md (+ MDN links, support notes) | expanded |
| OV15 | wow, removal, device, context tests | ambitious-tech.md (+ MDN links, support notes) | expanded |
| ON1 | assess goal and value moment | delight-and-onboarding.md § Onboarding | covered |
| ON2 | show do not tell | delight-and-onboarding.md § Onboarding | covered |
| ON3 | optional | delight-and-onboarding.md § Onboarding | covered |
| ON4 | time to value | delight-and-onboarding.md § Onboarding | covered |
| ON5 | context over ceremony | delight-and-onboarding.md § Onboarding | covered |
| ON6 | respect the user | delight-and-onboarding.md § Onboarding | covered |
| ON7 | welcome | delight-and-onboarding.md § Onboarding | covered |
| ON8 | account setup | delight-and-onboarding.md § Onboarding | covered |
| ON9 | checklist | delight-and-onboarding.md § Onboarding | covered |
| ON10 | tooltips at point of use | delight-and-onboarding.md § Onboarding | covered |
| ON11 | sample content | delight-and-onboarding.md § Onboarding | covered |
| ON12 | measure completion | delight-and-onboarding.md § Onboarding | covered |
| VI1 | three comps | later.md § visualize | later |
| VI2 | one approval | later.md § visualize | later |
| VI3 | comp becomes spec | later.md § visualize | later |
| VI4 | plates and provenance | later.md § visualize | later |
| AUN1 | VoiceOver and TalkBack | audit-scorecard.md § native | covered |
| AUN2 | native performance | audit-scorecard.md § native | covered |
| AUN3 | appearance | audit-scorecard.md § native | covered |
| AUN4 | platform conformance (critical) | audit-scorecard.md § native | covered |
| AUN5 | adaptivity | audit-scorecard.md § native | covered |
| ADN1 | restructure, do not stretch | native-platforms.md § Bigger screens | covered |
| ADN2 | navigation reshapes | native-platforms.md § Bigger screens | covered |
| ADN3 | split view | native-platforms.md § Bigger screens | covered |
| ADN4 | orientation and foldables | native-platforms.md § Bigger screens | covered |
| ADN5 | size classes | native-platforms.md § Bigger screens | covered |
| ADN6 | insets | native-platforms.md § Bigger screens | covered |
| ADN7 | web to native | native-platforms.md § Bigger screens | covered |
| IOS1 | safe area | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS2 | tab bar 2-5 | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS3 | edge-swipe back | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS4 | large titles | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS5 | 44pt targets | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS6 | Dynamic Type | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS7 | San Francisco | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS8 | 11pt floor, 17 body | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS9 | semantic colours | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS10 | dark mode | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS11 | one tint | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS12 | system materials | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS13 | platform controls | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS14 | SF Symbols | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS15 | modality | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS16 | grouped lists | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS17 | system transitions | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS18 | Reduce Motion | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| IOS19 | simulator evidence | native-platforms.md § iOS (checked against Apple HIG) | expanded |
| AND1 | Material navigation by size | native-platforms.md § Android (checked against Material 3) | expanded |
| AND2 | Back and predictive back | native-platforms.md § Android (checked against Material 3) | expanded |
| AND3 | edge-to-edge insets | native-platforms.md § Android (checked against Material 3) | expanded |
| AND4 | top app bar and FAB | native-platforms.md § Android (checked against Material 3) | expanded |
| AND5 | 48dp and 8dp | native-platforms.md § Android (checked against Material 3) | expanded |
| AND6 | type scale | native-platforms.md § Android (checked against Material 3) | expanded |
| AND7 | Roboto | native-platforms.md § Android (checked against Material 3) | expanded |
| AND8 | sp units | native-platforms.md § Android (checked against Material 3) | expanded |
| AND9 | colour roles | native-platforms.md § Android (checked against Material 3) | expanded |
| AND10 | dynamic colour | native-platforms.md § Android (checked against Material 3) | expanded |
| AND11 | dark theme | native-platforms.md § Android (checked against Material 3) | expanded |
| AND12 | tonal elevation | native-platforms.md § Android (checked against Material 3) | expanded |
| AND13 | components | native-platforms.md § Android (checked against Material 3) | expanded |
| AND14 | one FAB | native-platforms.md § Android (checked against Material 3) | expanded |
| AND15 | snackbars | native-platforms.md § Android (checked against Material 3) | expanded |
| AND16 | motion patterns | native-platforms.md § Android (checked against Material 3) | expanded |
| AND17 | emulator evidence | native-platforms.md § Android (checked against Material 3) | expanded |
| FR1 | finish reviewer: evidence first | design-review-qa (capture rules) | merged |
| FR2 | persistence | direction-process.md § Final review | covered |
| FR3 | fidelity matrix | direction-process.md § Final review | covered |
| FR4 | ceiling | direction-process.md § Final review | covered |
| FR5 | contract by promise | direction-process.md § Final review | covered |
| FR6 | truth | direction-process.md § Final review | covered |
| FR7 | floor | direction-process.md § Final review | covered |
| FR8 | one-word disposition | direction-process.md § Final review | covered |
| FR9 | verdict pass scores, does not hunt | direction-process.md § Final review | covered |

## Totals

404 items: covered 229, expanded 70, merged 84, later 21.
