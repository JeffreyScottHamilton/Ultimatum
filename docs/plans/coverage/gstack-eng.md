# gstack engineering skills rebuild: coverage map

Source: garrytan/gstack at commit 7dace1f (MIT, "Copyright (c) 2026 Garry Tan", LICENSE read at that commit). Ours: `plugins/ultimatum/skills/work/references/craft/gstack-eng/` and `plugins/ultimatum/data/craft/gstack-eng/`.

## How this map was made

- Items are the main sections of the in-scope skills: review (with its checklist), office-hours, ship, plan-eng-review, plan-ceo-review, document-release, retro, careful, freeze, guard and unfreeze. Design review, QA, the browser daemon and the binaries are out of scope (design review and QA were rebuilt earlier under `skills/website/references/craft/design-review-qa/`).
- Status: `covered` (same idea, our words, in a new file), `expanded` (we add to it: a runnable stdlib script, the untrusted-input rule, the security overlay, the user's yes before scope changes, pushes or version bumps), `merged` (already in an existing reference, so not repeated), `later` (in `later.md`, not shipped).
- The brief names an investigate skill; there is none at 7dace1f, so it is a `later` row. Debugging is already in `debugging.md`.
- The eight design red flags in plan-eng-review are credited by the source to pstack's architect skill (Lauren Tan, MIT, per the source's NOTICE.md); ours restates the ideas only.
- Not verified: the source's external links were not followed; none of its binaries, hooks or scripts were run. Our `command_guard.py` and `retro_stats.py` are new code, checked by their self-checks and the tests below.

## Items

| Source item | Status | Where |
|---|---|---|
| office-hours: startup vs builder mode | covered | office-hours.md § 1 |
| office-hours: intrapreneur sponsor and reorg test | covered | office-hours.md § 1, § 3 |
| office-hours: specificity, interest is not demand, user words, watch don't demo | covered | office-hours.md § 2 |
| office-hours: status quo is the competitor, narrow beats wide | covered | office-hours.md § 2 |
| office-hours: anti-sycophancy, take a position | covered | office-hours.md § 2 |
| office-hours: six forcing questions | covered | office-hours.md § 3 |
| office-hours: questions chosen by product stage | covered | office-hours.md § 3 |
| office-hours: pushback patterns | covered | office-hours.md § 2 |
| office-hours: escape hatch that overrides the user | later | later.md (conflicts with rule 4) |
| office-hours: builder-mode generative questions | covered | office-hours.md § 1 |
| office-hours: premise check | covered | office-hours.md § 4 |
| office-hours: alternatives (minimal, ideal, lateral) and wait for choice | merged | feature-planning.md § 0; office-hours.md § 5 |
| office-hours: design doc output | expanded | office-hours.md § 6 (feeds feature-planning § 6) |
| office-hours: YC and pitch coaching | later | later.md |
| plan-ceo-review: four modes | covered | scope-review.md § 1 |
| plan-ceo-review: mode chosen by rule, scope changes need approval | expanded | scope-review.md § 1 (user's call) |
| plan-ceo-review: premise (problem, do nothing, proxy) | covered | scope-review.md § 2 |
| plan-ceo-review: existing code | merged | feature-planning.md § 2 |
| plan-ceo-review: dream state current/plan/12-month | covered | scope-review.md § 3 |
| plan-ceo-review: alternatives | covered | scope-review.md § 4 |
| plan-ceo-review: 10x check, delight scan, add/defer/skip | covered | scope-review.md § 5 |
| plan-ceo-review: deferrals to TODOS | covered | scope-review.md § 5 |
| plan-ceo-review: temporal interrogation | covered | scope-review.md § 6 |
| plan-ceo-review: zero silent failures, prime directives | covered | error-rescue-map.md § 1 |
| plan-ceo-review: error and rescue map | covered | error-rescue-map.md § 1 |
| plan-ceo-review: no catch-alls, log context, retry/degrade/re-raise | covered | error-rescue-map.md § 1 |
| plan-ceo-review: LLM malformed/empty/refusal | covered | error-rescue-map.md § 1 |
| plan-ceo-review: security with likelihood and impact | expanded | scope-review.md § 7 (security overlay) |
| plan-ceo-review: data-flow shadow paths | covered | error-rescue-map.md § 2 |
| plan-ceo-review: async ordering, both orders, pause/release | covered | error-rescue-map.md § 3 |
| plan-ceo-review: interaction edge cases | covered | scope-review.md § 7 |
| plan-ceo-review: code quality section | merged | plan-eng-review.md § 1 |
| plan-ceo-review: test section, hostile QA, pyramid, flakiness | merged | tdd.md; debugging.md § 6; plan-eng-review.md § 5 |
| plan-ceo-review: performance | merged | plan-eng-review.md § 6 |
| plan-ceo-review: observability, three-weeks-later test, runbooks | covered | scope-review.md § 7; error-rescue-map.md § 4 |
| plan-ceo-review: deployment, old+new together, first 5 min / hour | merged | release.md § 4, § 7; scope-review.md § 7 |
| plan-ceo-review: trajectory and reversibility 1-5 | covered | scope-review.md § 7 |
| plan-ceo-review: failure modes registry | merged | error-rescue-map.md § 1 |
| plan-eng-review: engineering preferences | covered | plan-eng-review.md § 1 |
| plan-eng-review: cognitive patterns (14) | covered | plan-eng-review.md § 1 (the ones that change a review) |
| plan-eng-review: what exists, minimum change, complexity gate | covered | plan-eng-review.md § 2 |
| plan-eng-review: search for built-ins, check --help | covered | plan-eng-review.md § 2 |
| plan-eng-review: reality rows (premise, already done, numbers with basis, contracts, falsification) | covered | plan-eng-review.md § 2 |
| plan-eng-review: tier-2 reality rows (perf table, units, dependency fallback, obligation tiers) | merged | plan-eng-review.md § 2, § 6 |
| plan-eng-review: design twice | covered | plan-eng-review.md § 3 |
| plan-eng-review: eight red flags (pstack-derived, MIT) | covered | plan-eng-review.md § 3 |
| plan-eng-review: shared-code rubric | covered | plan-eng-review.md § 1 |
| plan-eng-review: one production failure per new path | covered | plan-eng-review.md § 4 |
| plan-eng-review: test level matrix (unit/integ/E2E/eval) | covered | plan-eng-review.md § 5 |
| plan-eng-review: regression iron rule | merged | tdd.md § 1 |
| plan-eng-review: coverage diagram with gap markers | covered | plan-eng-review.md § 5 |
| plan-eng-review: test plan artifact | merged | feature-planning.md § 6 |
| plan-eng-review: performance scale or unknown | covered | plan-eng-review.md § 6 |
| plan-eng-review: NOT in scope, what exists, failure modes, tasks | covered | plan-eng-review.md § 7 |
| plan-eng-review: worktree parallelization table | merged | orchestration.md § 1; plan-eng-review.md § 7 |
| plan-eng-review: confidence calibration | covered | pre-landing-review.md § 5 |
| review: scope drift (creep and missing) | covered | pre-landing-review.md § 1 |
| review: PR text untrusted | expanded | pre-landing-review.md § 1 (rule 3) |
| review: PR type decides categories | covered | pre-landing-review.md § 1 |
| review: SQL and data safety | covered | pre-landing-review.md § 2 |
| review: races, find-or-create, atomic status | covered | pre-landing-review.md § 2 |
| review: trust in LLM output, SSRF, stored prompt injection | expanded | pre-landing-review.md § 2 (security overlay) |
| review: shell injection | expanded | pre-landing-review.md § 2 (security overlay) |
| review: enum and value completeness | covered | pre-landing-review.md § 2 |
| review: gate integrity | merged | release.md § 2; pre-landing-review.md § 2 |
| review: data repairs explicit, preview, unreachable from upgrades | covered | pre-landing-review.md § 2 |
| review: informational pass categories | covered | pre-landing-review.md § 3 |
| review: distribution CI checks | covered | pre-landing-review.md § 3 |
| review: sideways sweep and sibling call sites | covered | pre-landing-review.md § 4 |
| review: forced-critical classes | covered | pre-landing-review.md § 4 |
| review: cache in front of guarded call, static to dynamic import, parity twins, pool in transaction | covered | pre-landing-review.md § 4 |
| review: test-only flake fix needs before/after failure rate | covered | pre-landing-review.md § 4 |
| review: quote the motivating line, confidence cap | covered | pre-landing-review.md § 5 |
| review: fix-first, auto-fix vs ask, one batch | covered | pre-landing-review.md § 6 |
| review: test-stub findings are ask | covered | pre-landing-review.md § 6 |
| review: gate disposition question (restore/keep/open) | covered | pre-landing-review.md § 6 |
| review: re-run checks after fixes | expanded | pre-landing-review.md § 6 (rule 2) |
| review: report with checked/not checked | merged | review/SKILL.md |
| review: specialist fan-out, bot comments, cross-model, review log | later | later.md |
| review: exploratory QA step | later | later.md (QA skipped by brief) |
| ship: route integrate/test/prepare/verify/push | covered | ship-pipeline.md § 1 |
| ship: merge base first, stop on logic conflicts | covered | ship-pipeline.md § 1 |
| ship: blocking policy (test fail, prod break, data/secret loss) | covered | ship-pipeline.md § 1 |
| ship: invocation record for resume | expanded | ship-pipeline.md § 2 (.ultimatum, ult handoff) |
| ship: receipts bound to content | covered | ship-pipeline.md § 5 |
| ship: version state (fresh/bumped/drift/none) | covered | ship-pipeline.md § 3 |
| ship: version level and asks | covered | ship-pipeline.md § 3 |
| ship: queue-aware version claims | covered | ship-pipeline.md § 3 |
| ship: TODOS update | merged | docs-release.md § 3 |
| ship: docs audit every ship | covered | ship-pipeline.md § 1; docs-release.md |
| ship: bisectable commits | covered | ship-pipeline.md § 4 |
| ship: frozen candidate verification, reuse by inputs | covered | ship-pipeline.md § 5 |
| ship: zero-run is failure, count unavailable | covered | ship-pipeline.md § 5 |
| ship: honesty inventory of gate edits | covered | ship-pipeline.md § 5 |
| ship: push and PR | merged | release.md § 0 (user's yes) |
| ship: helper binaries and receipts ledger | later | later.md |
| document-release: diff analysis and change classes | covered | docs-release.md § 1 |
| document-release: coverage map, four doc kinds | covered | docs-release.md § 2 |
| document-release: diagram drift advisory | covered | docs-release.md § 2 |
| document-release: stop / never-stop lists | covered | docs-release.md § 3, § 4 |
| document-release: never clobber changelog, edit not write | covered | docs-release.md § 5 |
| document-release: version only with ask | merged | release.md § 3; ship-pipeline.md § 3 |
| document-release: discoverability | covered | docs-release.md § 6 |
| document-release: ship-owned mode and spawned marking | later | later.md (runtime) |
| document-release: banned-terms binary | later | later.md |
| retro: metrics from git log on origin default | expanded | retro.md § 1 (retro_stats.py) |
| retro: features first, LOC as context | covered | retro.md § 2 |
| retro: hour histogram | later | later.md (not shipped; low value for a single repo) |
| retro: sessions with 45-min gap | expanded | retro.md § 2 (retro_stats.py) |
| retro: commit types, fix ratio over 50% | expanded | retro.md § 2 (retro_stats.py) |
| retro: hotspots, 5+ churn | expanded | retro.md § 2 (retro_stats.py) |
| retro: size buckets | expanded | retro.md § 2 (retro_stats.py) |
| retro: focus score | expanded | retro.md § 2 (retro_stats.py) |
| retro: streak anchored at newest commit | expanded | retro.md § 2 (retro_stats.py) |
| retro: team analysis, praise and growth | covered | retro.md § 4 |
| retro: week-over-week trends | merged | retro.md § 3 |
| retro: history snapshots, same window, recommendation follow-through | covered | retro.md § 3 |
| retro: tone rules | covered | retro.md § 4 |
| retro: zero commits | covered | retro.md § 4 |
| retro: shortcut ledger, eureka, skill usage, global mode, scorecard | later | later.md |
| careful: destructive patterns | covered | safety-modes.md § 1 |
| careful: PowerShell equivalents | covered | safety-modes.md § 1 |
| careful: safe build-dir exceptions | expanded | safety-modes.md § 1 (command_guard.py) |
| careful: deny vs ask tiers, lease never deny | expanded | safety-modes.md § 1 (command_guard.py) |
| careful: project patterns only tighten | expanded | safety-modes.md § 1 (--extra) |
| careful: hook decision JSON | expanded | safety-modes.md § 3 (command_guard.py hook, fail closed) |
| freeze: boundary under folder, resolve paths and symlinks, trailing slash | expanded | safety-modes.md § 2 (command_guard.py path) |
| freeze: fail closed, not a security boundary | covered | safety-modes.md § 2 |
| guard: careful plus freeze | covered | safety-modes.md |
| unfreeze: lifting needs the user's words | covered | safety-modes.md § 2 |
| hook install for the modes | later | later.md |
| investigate skill | later | later.md (not present at 7dace1f) |

Counts: covered 84 / expanded 20 / merged 17 / later 11 (132 rows).
