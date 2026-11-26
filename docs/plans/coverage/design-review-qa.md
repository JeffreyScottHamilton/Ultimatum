# Coverage: design-review-qa

Source: garrytan/gstack at 7dace1f (MIT, Garry Tan). In scope: design-review, plan-design-review, qa, qa-only. Read as text only; nothing from it was run. Our files: `plugins/ultimatum/skills/website/references/craft/design-review-qa/` (23 files plus index) and `plugins/ultimatum/data/craft/design-review-qa/`.

Impeccable note: the source's slop rule ids and some polish tells come from the Impeccable project (Apache-2.0; also derived from Elaya's work). We took only the ideas and the ids as names, wrote our own wording, and did not use its engine. The CREDITS line proposed in the report should name it.

## Inventory (size in bytes)

| size | file |
|---|---|
| 85181 | `design-review/SKILL.md` |
| 14171 | `design-review/SKILL.md.tmpl` |
| 5709 | `design-review/sections/build-loop.md` |
| 5496 | `design-review/sections/build-loop.md.tmpl` |
| 7067 | `design-review/sections/craft-audit.md` |
| 2878 | `design-review/sections/craft-audit.md.tmpl` |
| 1273 | `design-review/sections/manifest.json` |
| 10032 | `design-review/sections/outside-voices.md` |
| 26 | `design-review/sections/outside-voices.md.tmpl` |
| 22396 | `design-review/sections/preamble.md` |
| 13234 | `design-review/sections/test-bootstrap.md` |
| 19 | `design-review/sections/test-bootstrap.md.tmpl` |
| 16661 | `design-review/templates/preview-fixtures.mjs` |
| 56205 | `plan-design-review/SKILL.md` |
| 16979 | `plan-design-review/SKILL.md.tmpl` |
| 1325 | `plan-design-review/sections/checklist.md` |
| 1209 | `plan-design-review/sections/checklist.md.tmpl` |
| 1353 | `plan-design-review/sections/manifest.json` |
| 22396 | `plan-design-review/sections/preamble.md` |
| 49314 | `plan-design-review/sections/review-sections.md` |
| 20373 | `plan-design-review/sections/review-sections.md.tmpl` |
| 21913 | `qa-only/SKILL.md` |
| 10874 | `qa-only/SKILL.md.tmpl` |
| 8615 | `qa-only/sections/exploratory.md` |
| 19 | `qa-only/sections/exploratory.md.tmpl` |
| 522 | `qa-only/sections/manifest.json` |
| 22396 | `qa-only/sections/preamble.md` |
| 4881 | `qa-only/sections/reporting.md` |
| 4765 | `qa-only/sections/reporting.md.tmpl` |
| 29283 | `qa/SKILL.md` |
| 11947 | `qa/SKILL.md.tmpl` |
| 3839 | `qa/references/issue-taxonomy.md` |
| 10901 | `qa/sections/browser-setup.md` |
| 1364 | `qa/sections/browser-setup.md.tmpl` |
| 1154 | `qa/sections/browser-verify.md` |
| 1033 | `qa/sections/browser-verify.md.tmpl` |
| 8032 | `qa/sections/exploratory.md` |
| 19 | `qa/sections/exploratory.md.tmpl` |
| 2393 | `qa/sections/manifest.json` |
| 22396 | `qa/sections/preamble.md` |
| 11411 | `qa/sections/qa-patterns.md` |
| 19 | `qa/sections/qa-patterns.md.tmpl` |
| 1590 | `qa/sections/scope.md` |
| 13 | `qa/sections/scope.md.tmpl` |
| 3933 | `qa/sections/system-functional.md` |
| 18 | `qa/sections/system-functional.md.tmpl` |
| 7276 | `qa/sections/test-bootstrap.md` |
| 5657 | `qa/sections/test-bootstrap.md.tmpl` |
| 3209 | `qa/templates/functional-report-template.md` |
| 3134 | `qa/templates/qa-report-template.md` |

The `.tmpl` files duplicate the built `SKILL.md` and `sections/*.md`; noted only. The three `preamble.md` copies (22396 bytes each) are the same harness boilerplate.

## Coverage map

Status: covered, expanded (ours adds local-business, app, WCAG 2.2 or reduced-motion rules), merged with X, later.

| Source item | Our file and section | Status |
|---|---|---|
| design-review: scope, inputs, depth modes, posture | design-review-modes.md | covered |
| design-review: design-system lookup (design doc, tokens) | design-review-modes.md | merged with design-rules.md |
| design-review: Krug behaviour lens, tools | design-review-modes.md, first-impression.md | covered |
| Phase 1 first impression, 5-second test, trunk test, critique voice, quick wins | first-impression.md | expanded |
| Phase 2 design system extraction | design-audit-recipes.md (script), scoring-and-baseline.md | expanded |
| Phase 3 page audit, per-page checks | checklist-visual.md, checklist-behaviour.md | covered |
| Classifier Persuade/Operate/Read/Experience/Hybrid, mode rules | page-modes.md | expanded |
| Hard rejections (7), litmus checks (7), reflexes, three looks | page-modes.md | covered |
| Checklist categories 1-4, 6 (hierarchy, type, colour, space, responsive) | checklist-visual.md, design-checks.csv | expanded |
| Checklist categories 5, 7, 8, 10 (states, motion, copy, speed) | checklist-behaviour.md, design-checks.csv | expanded |
| Category 9 slop: 11 patterns, rule ids, polish, judgement tells, fonts | slop-tells.md, slop-tells.csv | merged with design-rules.md section 2 |
| Phase 4 flows, goodwill meter | flows-and-consistency.md | covered |
| Phase 5 consistency | flows-and-consistency.md | covered |
| Scoring weights, grade arithmetic, baseline JSON, regression, report layout | scoring-and-baseline.md | covered (our own JSON schema) |
| Phases 7-11: triage, fix loop, 30-fix cap, risk, final audit, report | fix-loop.md | covered |
| Design-doc rule, commits | fix-loop.md | covered (commits only on request) |
| TODOS update | fix-loop.md | covered |
| craft-audit: claims, sample content, ship floor, motion, Persuade checks | craft-audit.md | expanded |
| build-loop: 7 items, rounds, receipts, outcomes | build-loop.md | covered |
| outside-voices: Codex voice | later.md | later |
| outside-voices: independent subagent, brief, litmus | second-opinion.md | covered |
| design-review test-bootstrap | qa-fix-and-tests.md | merged with qa test-bootstrap |
| templates/preview-fixtures.mjs (loopback fixture server, scenario shim) | later.md | later |
| design-review preamble, 3 copies | later.md | later (harness boilerplate) |
| plan-design-review: scope gate | plan-review-passes.md | covered |
| plan: pre-review audit, UI scope detection, retrospective check | plan-review-passes.md | covered |
| plan: design philosophy and 9 principles, Krug behaviour | plan-review-passes.md | covered |
| plan: Step 0 (rating, design file status, leverage, focus) | plan-review-passes.md | covered |
| plan: Step 0.5 mockups, design binary, comparison board, "show me a 10" | later.md | later |
| plan: 0-10 rating method, one question per issue, carry decisions | plan-review-passes.md | covered |
| plan: passes 1-7 | plan-review-passes.md | expanded |
| plan: required outputs, completion summary, score rule, unresolved decisions | plan-review-outputs.md | covered |
| plan: review log, dashboard, chaining | plan-review-outputs.md, later.md | covered (log line), later (dashboard) |
| plan: checklist (autoplan profile) | later.md | later |
| qa: issue taxonomy (4 severities, 7 categories) | qa-taxonomy.md, qa-issues.csv | covered |
| qa: per-page exploration checklist | qa-taxonomy.md | covered |
| qa: scope (surface, isolation, boundaries) | qa-modes-and-loop.md | covered |
| qa: modes (Full, Quick, Regression, Diff-aware), tiers, parameters | qa-modes-and-loop.md | covered |
| qa: charters, probe loop, budgets | qa-modes-and-loop.md | covered |
| qa: health score, baseline, framework guidance | qa-health-score.md | covered |
| qa: qa-patterns (browser scripts) | qa-playwright-recipes.md | expanded (own Playwright script, run) |
| qa: browser-setup (Aside, browse daemon, cookie import) | later.md | later |
| qa: browser-verify | qa-fix-and-tests.md | covered |
| qa: system-functional (10 contracts) | qa-functional.md | expanded |
| qa: report templates (browser, functional) | qa-reports.md | covered |
| qa: fix loop, regression tests, 50-fix cap, test bootstrap marker table | qa-fix-and-tests.md | covered |
| qa-only: reporting, evidence-first, timing fields | qa-reports.md | covered |
| qa-only: exploratory | qa-modes-and-loop.md, qa-taxonomy.md | merged with qa exploratory |
| gstack-* tools, learnings, gbrain, review dashboard | later.md | later |
| Local-business and app additions, WCAG 2.2, reduced motion | checklist-behaviour.md, qa-taxonomy.md, plan-review-passes.md | added (not in source) |
