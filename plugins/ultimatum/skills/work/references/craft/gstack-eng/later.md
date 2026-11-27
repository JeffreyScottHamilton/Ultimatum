# gstack engineering skills: parts not rebuilt

Read when you wonder whether some gstack engineering skill exists here; most of what is left out runs the source's own binaries or is outside this brief.

Routing for the rebuilt parts is in `index.md`; the main router is `../../../SKILL.md`.

| Source part | Why it is not here |
|---|---|
| Preambles, telemetry, update checks, question tuning and learnings capture in every skill | the source's own runtime; Ultimatum has `ult learn` and `ult handoff` |
| The browser daemon, its binaries, design review and QA skills | outside the brief (named as skipped) |
| Helper binaries the skills call (`gstack-ship-release`, `gstack-evidence`, `gstack-review-read`, `gstack-retro-metrics`, scorecards, freeze state scripts) | binaries, not run; the ideas they serve are written as steps, and `retro_stats.py` and `command_guard.py` are our own |
| Hook install for the careful, guard and freeze modes | changes the user's settings; how to do it, only on request: (`safety-modes.md` § 3) |
| Investigate skill | not present at commit 7dace1f; the review checklist only refers to it. Our version is `../../debugging.md` |
| Multi-model second opinions, specialist reader fan-out, review-bot comment triage and the review log format | tied to the source's agent runtime; parallel review is in `../../orchestration.md` § 8 |
| Gate-disposition logging with actor stamps, and the "honesty inventory" lines | the idea is kept (each loosened gate listed with its reason) (`pre-landing-review.md` § 6) and (`ship-pipeline.md` § 5); the log format is not |
| Queue-aware version claims across worktrees via the source's workspace tool | the rule (take the next free number) is kept, not the tool: (`ship-pipeline.md` § 3) |
| Global retro across every repo and AI tool on the machine, eureka and skill-usage rows, shortcut-marker ledger | reads files outside the project; outside a single-repo retro |
| Factory scorecard and merged-PR counts via `gh` | needs network and a login; `retro.md` sticks to local git |
| The office-hours pushback that overrides a user's "just build it" | conflicts with Ultimatum rule 4; replaced by listing assumptions and moving on |
| Founder and startup coaching beyond the question list (pitch advice, YC framing) | outside an engineering brief |
| Doc generation skill suggested for coverage gaps | outside the brief; `docs-release.md` flags gaps only |
