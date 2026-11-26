# gstack engineering craft: idea, plan, review, ship, look back

Read when work needs more than the base files give on testing an idea, reviewing a plan for scope or engineering, a two-pass pre-merge review, an ordered ship with a version decision, docs after a change, a retro from git history, or caution and edit-boundary modes.

Rebuilt from the ideas in garrytan/gstack at commit 7dace1f (MIT). All wording and code here are ours. The base rules live in `../../feature-planning.md`, `../../release.md`, `../../debugging.md` and `../../../../review/SKILL.md`; these files only add what those leave out.

- `office-hours.md`: testing an idea before any plan, picking two or three questions by stage, checking premises, and a half-page brief.
- `scope-review.md`: whether a plan aims at the right thing: a stance (grow, pick, hold, cut), three horizons, alternatives, additions one at a time, and review sections for large plans.
- `plan-eng-review.md`: whether a plan is built well: scope questions, design twice and weak-boundary signs, one failure per new path, a test map, and what to hand back.
- `error-rescue-map.md`: one row per failure with its handler and what the user sees, shadow paths of each input, and both orders of async work.
- `pre-landing-review.md`: intent versus diff, a production pass and a rot pass, a sideways sweep, a quoted line behind each finding, then fix first and ask once.
- `ship-pipeline.md`: the order from base merge to push, a resume record, the version decision by state, bisectable commits, and checks that must have run on the frozen content.
- `docs-release.md`: a coverage map of what shipped against four kinds of doc, what to edit freely and what to ask about, and changelog care.
- `retro.md`: numbers from git history, what each one means, comparing with the last retro, and how to write it up.
- `safety-modes.md`: deny, ask and allow tiers for shell commands, and a one-folder edit boundary.

Scripts: `../../../../../data/craft/gstack-eng/` (`command_guard.py`, `retro_stats.py`).

Not rebuilt, with reasons: `later.md`.
