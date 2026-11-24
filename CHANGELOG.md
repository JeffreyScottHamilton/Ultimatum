# Changelog

All notable changes to Ultimatum are listed here. Versions follow [Semantic Versioning](https://semver.org/); the version in `plugins/ultimatum/.claude-plugin/plugin.json` is the source of truth and must be bumped for installs to update.

## [2.0.0] - 2026-11-24

### Added
- `ult route "<task>"`: a local, deterministic router (no model call). It picks a mode (FAST, STANDARD, DEEP, RECOVERY), one route, up to two add-ons and the security overlay, and lists only the reference files to read with their token cost. Routes and add-ons live in `skills/work/modules.json`. `--eval FILE` scores it against labelled tasks.
- New guidance modules: UI design (`design/design.md`), motion (`design/motion.md`), component selection (`design/components.md`), MCP server building and skill authoring.
- `ult components "<need>"`: offline lookup of permissively licensed component and animation libraries. Restricted or unlicensed ones are hidden unless `--all`, and then flagged, with MIT alternatives listed.
- `ult upstreams`: the reviewed upstream projects with pinned revisions, licences and decisions.
- `ult learn`: local lessons (`add`, `list`, `prune`), automatic observation at the end of each turn (counts and categories only; `ULTIMATUM_OBSERVE=0` turns it off), and `propose`, which writes redacted improvement proposals from a fixed allow-list. Nothing leaves the machine unless you approve `/ultimatum:learn submit`.
- `ult budget`, `ult sync export|import` (copy lessons to a folder such as a clone of your own private repo), and `ult update status|setup|migrate`.
- Management skills that cost nothing at startup (`disable-model-invocation`): `/ultimatum:status`, `setup`, `sync`, `learn`, `skills`, `budget`, `eval`, `doctor`, `rollback`, `migrate`.
- `/ultimatum:setup` turns on marketplace auto-update once (with a backup of `~/.claude/settings.json`), and explains the cloud and running-session steps.
- CI fails a pull request that changes the plugin without bumping the version and adding a changelog entry.
- Static size tests for the always-loaded skill body, descriptions, management skills and references.
- Live A/B runner arms for plain Claude Code, 0.4.1 and 2.0, with a total spend cap (`--max-total-usd`).
- Architecture Guardian. `ult arch check` finds import cycles (Python and JS/TS, plus Graphify's EXTRACTED import edges when `graphify-out/graph.json` exists), duplicated blocks, oversized files and functions, placeholder code, naming outliers, unused private functions and untested changed modules. `--changed` limits it to the git diff. `ult arch baseline` plus `--drift` report only new findings. `--strict` exits 1 on cycles or placeholders. `--record` adds finding counts (no paths or code) to local observations.
- `architecture` add-on (`references/architecture.md`). It loads for the large route, refactors, structural words and code reviews, and never for small, handoff, improve or security routes. Add-ons gained a `with_routes` field for this.
- The live A/B gates its pass on code quality: a task passes only if its graders pass and `ult arch` finds no new cycle or placeholder. New architecture findings are reported next to tokens and cost.
- `ult audit start` and `ult audit finish`. Start creates the audit ledger, runs the offline scan and writes a findings skeleton that records which scanners did not run. Finish checks the ledger, validates the findings and renders the report. Together they produce the audit deliverables without the model reading the long audit procedure.
- `ult route` prints a one-line `do:` contract for routes that have a deterministic deliverable: sec-audit, bug and ci-pr.
- `ult arch deps <path> [--reverse] [--depth N]`: lists one file's neighbours in the import graph, so the full graph never enters the chat.
- `evals/live/analyze.py` reports token waste from live A/B transcripts: first-call context, cache writes, large tool results, rereads, polling, and tests run without `ult run`.
- The router sends defect reports that never say "bug" (symptoms such as "drops", "returns None", `KeyError` or HTTP 500s) to the bug route. A lone symptom verb in a feature request still routes to feature. Route accuracy did not drop on any held-out set; holdout3 went from 46/60 to 47/60.
- Three local learning signals, saved as counts only: `poll-sleep`, `raw-test-output` and `reread`. Each one maps to a fixed lesson.
- `ult route --cat` prints the listed references (and the security guide when the overlay is on) after the routing lines, so routing and reading take one tool call instead of two.

- **Motion Graphics workflow.** `/ultimatum:motion-graphics` (or a plain request such as "Make a 15 second logo reveal video") plans a clip as brief → story and sound → storyboard, then **stops for storyboard approval** before production animation. Small changes to an existing clip skip the storyboard. The Animator prefers HyperFrames when installed, then HTML captured with Playwright, then plain ffmpeg; timing and easing follow `coding/guides/motion.md`. `ult motion "<task>"` prints the plan; `ult motion --approve "…"` records the approved storyboard in the shared brief.
- `ult beats FILE`: beat times from librosa when installed (labelled **suggested beats**), otherwise loud onsets found with ffmpeg (labelled **possible cues**). Both are suggestions to check against the audio before timing cuts. `ult media FILE`: duration, size, fps, codecs and loudness (LUFS) of an export, with warnings for common export problems.
- **Review loop.** The Reviewer reports to the Manager, who marks blockers and sends them back to the Builder or Animator; the Reviewer rechecks each fix. Open blockers stop delivery; minor findings go in the report. `ult loop add|triage|fixed|recheck|status` tracks this when there are several findings.
- **Chat mode.** Plain questions are answered directly with no workflow; the prompt hook now routes questions to chat, coding to Work, websites (including animations inside a site) to Website, and standalone clips to Motion Graphics. Typed commands still win.
- Search escalation: after two focused searches, or when a change spans 3+ areas, run `ult map`, then Graphify for one question, then confirm in the code.
- Credits and upstream pins for HyperFrames, gstack, Matt Pocock's skills, shadcn/ui, Graphify, Caveman and the Karpathy guidelines.

- **Two workflows.** `/ultimatum:work` stays the default for chat and coding. The new `/ultimatum:website` handles website work: the Manager writes one brief (goal, design direction, 3 to 6 browser checks), an optional Designer runs only when a new look is needed, the Builder works mobile, desktop and keyboard, the Reviewer checks the real page, and the Manager fixes, rechecks and reports. Small website jobs stay solo. `ult website "<task>" [--json|--cat]` prints the plan and only the files it needs, and never loads the Work skill.
- **Website starts from plain chat.** A new `UserPromptSubmit` hook (`scripts/ult-pick`, local, stdlib only) adds one line pointing Claude to `/ultimatum:website` when a prompt is clearly website work: a website named outright ("Build me a website for my coffee shop"), or interface words such as "mobile menu" inside a project that is a website (an `index.html` or a web framework in `package.json`). Other prompts get nothing. Prompts starting with `/` are left alone, so explicit commands still win. `ULTIMATUM_AUTO=0` turns it off.
- **Work starts from plain chat too.** The same hook now sends other coding requests ("Fix the CSV export") to `/ultimatum:work`, so it no longer depends on a line in the user's `CLAUDE.md`. `ultlib/pick.py` decides website, work or chat offline. Plain questions, questions about how code works, writing help and small talk get nothing. Measured offline: 362/386 labelled coding tasks start a workflow (the 23 code questions plus one task that starts with `/` stay in chat on purpose); 40/40 plain-chat messages stay in chat; on two unseen sets written afterwards, 30/30 + 20/20 coding and 30/30 + 19/20 chat (first set scored 23/30 and 26/30 before fixes).
- **Small website fixes stay on the bug.** The browser check runs before the edit; findings that were already there are reported as "seen, not changed", and tap targets are resized only in new or redesigned parts. `ult website` prints the scope line.
- **Visual planning for new sites and redesigns.** The Manager acts as Planner and writes one brief (audience, first action, pages and sections, mobile layout, assumptions, `[[PLACEHOLDER: …]]` for missing business facts, build phases each with a check). The Designer adds one visual direction to the same brief. The Planner turns it into a ready-to-paste ChatGPT mockup prompt (a grayscale wireframe first when the layout needs review), shows a mockup when an image tool is available, explains it in plain words and stops: no production code until the user approves the look. `ult website --approve "…" [--image PATH]` records the approval in the brief's Approved direction section, which the Builder builds from and the Reviewer compares against on phone and desktop. `ult website` prints a `gate:` line and loads the new `skills/website/planner.md` only on this path. Small fixes keep the short path (brief, focused fix, browser check) with no approval stop.
- `ult route` adds `workflow: website` on the same rule. The Work skill then switches to the website workflow, unless the user typed `/ultimatum:work`.
- The Website Manager runs the whole job: a new site or redesign gets Design, Build and a browser Review; a plain fix keeps the current look, reproduces the bug, fixes it and checks it in a browser at 375 and 1280 px. It decides on its own when a helper (Designer, Builder, Reviewer) is worth it, leaves the user a preview, and lists exactly what it still needs (photos, text, domain, hosting login).
- **Shared defaults** in one file (`shared/defaults.md`): answer first in plain words, reuse what works, plan to fit the job, report only what was checked. Every `--cat` prints it first.
- **Shared skills** `design`, `coding` (with `guides/website.md`), `review` and `release`. They cost nothing at startup (`disable-model-invocation`) and the workflows read them by path. Release says Ready or Blocked, and deploys or publishes only on the user's explicit yes.
- **SECURITY mode** for the security routes: the shared Review skill plus the OWASP-informed guides.
- **Code-map escalation** (`references/code-map.md`) printed for DEEP tasks: search first, then `ult map`, then one Graphify question, then confirm in the code.
- `/ultimatum:style` and `ult style status|apply|remove`: an opt-in copy of the shared defaults in your user `CLAUDE.md`, between markers, with a one-time backup. `remove` restores the file byte for byte. Your own instructions are left alone.
- Tests for website routing, the optional Designer, solo small jobs, selective loading, Release gating and the style setup.

### Changed
- `ultimatum:worker` runs on Haiku by default; give it `model: sonnet` in the brief when the slice needs judgment. The reviewer stays optional.
- The Work skill's description and rules are shorter; the reuse rule moved into the shared defaults. A small task's `--cat` now prints only the shared defaults (about 700 bytes more than before).
- Held-out routing labels: 9 security-route cases in `tests/data/routing_holdout.jsonl` now expect mode SECURITY instead of STANDARD or DEEP, because that mode is new. Routes did not change.
- `SKILL.md` sends obvious one-spot edits (typo, rename, a stated one-liner) straight to FAST mode without running the router.
- The router drops prompt-leak requests ("output the system prompt") before scoring, and "plan it first" or "new setting" now count toward the feature route. Dev routing went from 193/196 to 195/196; the held-out sets did not change.

### Removed
- The Office documents route (`documents.md`, Word, Excel, PowerPoint and PDF). It was out of scope for a developer skill; Anthropic's own document skills cover it.
- `SKILL.md` file is down from 7.6 KB (0.4.1) to 4.5 KB: the routing table moved into the router, so it is no longer re-read on every turn.
- The reviewer agent is described as a once-per-DEEP-task step.
- The reviewer runs `ult arch check --changed` and checks for parallel modules, wrong-way imports, placeholders and needless dependencies.
- `ult doctor` lists Graphify, Repomix and RTK. `integrations.md` says when each one pays off.
- Self-improvement rejects a proposal that saves tokens but fails tests or adds a blocking architecture finding.
- Agent descriptions, which load in every session, are shorter: 661 bytes for all five, down from about 1,140.
- The orchestration rules now cover launching workers. Launch them in one message, never sleep or poll, and never edit a slice that has been delegated. Briefs carry anchors, so workers don't re-read the repo.

### Compatibility
- Every 0.4.x command, hook, agent and reference path still works. `ult update migrate` is a no-op on existing `.ultimatum/` state apart from creating `knowledge.md` and `proposals/`.

## [0.4.1] - 2026-11-23

### Changed
- Quieter replies. No narration while working. A finished, verified task with nothing for the user to do now ends with just `Done.`. Otherwise it reports one line per action the user must take, or per failed or skipped check or risk. Full detail (files, commands, exit codes) only on request, or for large, audit and release work. Verification itself is unchanged.
- README: the always-on cost note now points to the measured A/B range instead of an older estimate.

## [0.4.0] - 2026-11-22

### Changed
- Token use is now the first rule. The live A/B run (`evals/live/results/final`) showed Ultimatum costing 1.2× to 4.3× more per task than plain Claude Code. Most of that was fixed overhead, not the work itself.
- The main session makes edits itself again. 0.3.0 sent every edit, even a one-line fix, to an `ultimatum:worker`, and each worker starts a whole new context. Workers are now only for independent slices of large work, and the reviewer only for large work.
- `SKILL.md`, which loads on every task and is re-read on every turn, is down from 12.4 KB to 7.0 KB. The optional-integrations table moved to `references/integrations.md`, read only before using one of those tools. The skill description is shorter too.
- Terse replies by default: short sentences, no preamble or restated plan. A small task's report is one to three lines. Code, paths, errors and evidence stay exact.
- `ult retro` runs only after long tasks (roughly 15+ turns) or a user correction, not after every task.
- README: the "unmeasured" line now gives the measured A/B numbers. 0.4.0 itself has not been re-measured.

## [0.3.1] - 2026-11-21

### Fixed
- The chat-size guard no longer blocks small chats for being idle. The idle rule now applies only when the chat also re-reads more than 150k tokens (`ULTIMATUM_GUARD_IDLE_TOKENS`). A small chat paused for 14 hours was blocked before, although re-reading it once costs little.
- The guard could lock a chat: a blocked prompt is not added to the transcript, so the chat stayed "idle" and every retry was blocked again. It now blocks a chat once: sending a message again in that chat goes through, and the block message says so.

### Changed
- UI route: more distinctive interfaces. Before choosing a direction, Ultimatum sketches three directions from different sources and drops any that fail a swap test (still fits with a competitor's name). The direction card gains a concept line that every choice must follow.
- New `ui.md` §3a, "Sources of distinctiveness": domain artifacts, real content as the graphic, typography as voice, a named color source built in OKLCH, composition with tension, a structural constraint, edge details and copy with a point of view.
- Cards are appended to `.ultimatum/ui-directions.md`. A new card must change the concept, display face and accent from the last two, unless the brief or existing identity pins them.
- The UI critique gate adds a distinctiveness check on screenshots (swap, memory, squint and card-drift tests) within the same 3-round limit.
- README: how to turn on marketplace auto-update (`"autoUpdate": true` in user settings).

## [0.3.0] - 2026-11-17

### Changed
- **The main session only orchestrates.** New rule 7: it never edits project files; every edit, including a one-line fix, goes to `ultimatum:worker`, searches across many files go to `ultimatum:scout`, and anything beyond a small change gets `ultimatum:reviewer`. A small change uses one worker with a brief of a few lines. `orchestration.md`, `feature-planning.md`, `context-efficiency.md`, and the worker agent follow.
- **Never asks for a new chat or a manual `/compact`.** `ult context` HIGH now means "write the handoff, compaction is close", not "open a fresh chat". The README documents setting the auto-compact window to 200k with `CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000`.
- The coach no longer treats compactions or a high subagent share as waste in themselves.

### Added
- `hooks/hooks.json`: one `SessionStart` hook (source `compact`) that prints `ult handoff show` after each compaction, so work resumes in the same chat. It is local and read-only, and sits beside the opt-in guard hooks from 0.2.7.
- Learn step in the default loop, run without being asked: `ult retro` checks the current chat and its subagents for repeated failures, re-reads, oversized outputs, search churn, and corrections. Project lessons become one-line rules in the project's `CLAUDE.md` under `## Learned`; lessons about Ultimatum are flagged as `Skill lesson:` in the report.
- Daily self-improvement run (`self-improvement.md` §2): a scheduled cloud session reads recent sessions, makes at most one tested change to the plugin, and opens a pull request. It never merges.
- Repository `CLAUDE.md` and `.claude/settings.json` (200k window) for sessions that work on Ultimatum itself.

Not measured: the cost and quality effect of always delegating. The last live A/B (`docs/TEST-REPORT.md`) predates this change.

## [0.2.9] - 2026-11-16

### Changed
- Auto-compact is the main control for long chats; the guard is now a safety net. Guard defaults rise to 400k tokens per turn and 240 idle minutes, because a new chat starts at ~78k tokens per turn and must re-learn the work, so switching at 150k saved little.
- Rule 7: when `ult context` reports HIGH, write a handoff and ask the user to type `/compact` (same chat, same machine and files) instead of opening a fresh chat.

## [0.2.8] - 2026-11-16

### Added
- Auto-resume after a guard block: a `SessionStart` hook (new chat or `/clear`, only with `ULTIMATUM_GUARD=1`) loads the guard's handoff into the next chat once, so the first message can be anything. Blocks older than 7 days are dropped.

## [0.2.7] - 2026-11-16

### Added
- Opt-in chat-size guard (`hooks/hooks.json`, `scripts/ult-guard`): a `UserPromptSubmit` hook, off unless `ULTIMATUM_GUARD=1`. When a chat's last turn re-read over 150k tokens or it was idle over 60 minutes, it blocks the prompt with exit code 2 (zero model tokens), writes a handoff, and prints "Chat too large. Start a new chat and type: /ultimatum:work resume". Thresholds: `ULTIMATUM_GUARD_TOKENS`, `ULTIMATUM_GUARD_IDLE_MIN`.
- `ult handoff write --keep`: fills unset fields from the existing handoff, so an automatic write never erases the recorded goal, decisions, or next step.

## [0.2.6] - 2026-11-15

### Added
- `ult context`: one line showing how many tokens each turn of the current chat re-reads (exit 3 when over 150k). In a 636-turn chat it reported ~566k tokens per turn, which is why usage drained in minutes.
- Rule 7: before substantial work in a long chat, check `ult context`; if HIGH, save a handoff and continue in a fresh chat (`/ultimatum:work resume`) instead of paying the huge re-read on every step.

## [0.2.5] - 2026-11-12

### Changed
- Routing is explicitly zero-overhead: Ultimatum decides the route from the task itself, never runs tools or opens references just to decide, and loads an extra reference only when the task proves to need it.

## [0.2.4] - 2026-11-12

### Added
- Rule 7, "Keep the conversation small": every turn re-reads the whole chat, so Ultimatum keeps bulk out of it (`ult run`, ranged reads, capped searches), batches tool calls, sends broad exploration to the scout subagent, keeps replies short, and suggests `/compact` or a fresh session from the handoff when the chat grows long.

## [0.2.3] - 2026-11-12

### Added
- `ult scan --history`: gitleaks scans every commit, finding secrets that were committed and later deleted. Without gitleaks the report says "git history secrets: NOT checked" instead of implying a clean result. Full audits now use it.

### Fixed
- `ult scan` no longer reports the same secret twice when gitleaks and the built-in patterns both catch it. The external lead is kept and notes the agreeing built-in rule.

## [0.2.2] - 2026-11-12

### Added
- Compaction guidance: on longer tasks Ultimatum refreshes the handoff at milestones, and re-checks the handoff and evidence after a compaction (SKILL.md §3, `handoff.md`).
- README: how to cap context at about 200k tokens (`claude --autocompact 200000`, or `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=20` in cloud settings).

## [0.2.1] - 2026-11-12

### Fixed
- `ult note` could give two notes the same reference when they were saved within the same millisecond, so the second overwrote the first in lookups. References now carry a random suffix. Found as an intermittent CI failure; this was also the undiagnosed one-off unit-test failure noted in the 0.1.0 test report.

## [0.2.0] - 2026-11-11

### Added
- **Efficiency coach** (`improve` route): ask "efficiency review" or "daily coach". It reads this machine's Claude Code transcripts (including subagents), reports where tokens went by task category, and flags avoidable work: oversized tool output, repeated reads, repeated failing commands, search churn, user corrections, context compactions, heavy delegation. It then proposes one change, applied only with your approval.
- `ult usage report`: the local analyzer. It stores counts, categories, tool names and redacted paths/commands only, never prompt text or tool output. No network.
- `ult improve`: an experiment ledger (propose → apply with a baseline snapshot → measure after ≥3 sessions → keep or roll back). Verdicts weigh tokens per session against quality signals (corrections, tool errors).
- Reference `self-improvement.md`: the review procedure, allowed changes, privacy rules, and how to schedule it on your own machine.

## [0.1.1] - 2026-11-11

### Fixed
- `ult search` crashed with a traceback on an invalid regex and on a `--path` outside the project when ripgrep was not installed. Found by the first CI run (CI runners have no ripgrep). Both now exit with a clear error, on both the ripgrep and pure-Python paths.

### Added
- CI on every push: unit tests on Python 3.9, 3.11 and 3.13 (without ripgrep, so the fallback search path is covered) and `claude plugin validate --strict`.

## [0.1.0] - 2026-11-11 (preview)

First public preview. Tested on small fixture projects only; see `docs/TEST-REPORT.md` for exactly what was and was not tested.

### Added
- One entry command, `/ultimatum:work <task>`, routing to workflows for small changes, discovery, features, large features with parallel workers, debugging, CI/PR feedback, UI with browser verification, data and infrastructure, bounded optimization, releases, handoff and resume.
- Three security workflows: a secure-implementation pass that runs automatically on sensitive changes, security review of a change, and full audit with a coverage ledger, a fresh verifier, and confirmed / needs-validation / rejected findings.
- Five subagents: `scout`, `worker`, `reviewer`, `security-hunter`, `security-verifier`.
- `ult` toolbelt (Python 3.9+ standard library, no network): `run`/`log` with raw-log recovery, `search`/`symbols`/`refs`, `map`, `note`/`find`/`get`, `handoff`, `scan` (wraps Semgrep, Gitleaks and OSV-Scanner when installed), `findings`, `doctor`.
- `ult-browser.mjs`: Playwright-based viewport, interaction, and accessibility checks, with axe-core when installed.
- `ULTIMATUM_STATE_DIR` to keep all state outside the repository for strict read-only work.

### Known limitations
- Not yet tested on large real-world repositories or with models other than `sonnet`.
- Costs about 1.5–1.8x plain Claude Code per task in the recorded evals; no token-savings claim is made.
- CI/PR, production, data/infra, optimization and release workflows were tested for routing only.
