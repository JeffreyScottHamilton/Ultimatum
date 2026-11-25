# Ultimatum 2.0 implementation plan

Status: **proposal, awaiting approval.** Nothing in `plugins/` changes until it is approved.
Branch: `claude/affectionate-turing-qr3gau`. No release, tag or push to `main` without approval.
Inputs: `upstream-anthropic.md`, `upstream-engineering.md`, `upstream-design.md`, `component-libraries.md`, `component-registry.json`, `platform-capabilities.md` (all in this folder), and `evals/live/results/final`.

## 1. Audit: what exists today (0.4.1)

| Part | Today | Cost |
|---|---|---|
| Model-invocable skill | `work` (one router with a 16-route table) | description is about 391 tokens at startup (with agent descriptions); body is 7,570 B (~1.9k tokens) on invoke |
| References | 24 files, 182 KB, read one route at a time | only what the route reads |
| Agents | scout, worker, reviewer, security-hunter, security-verifier | descriptions always loaded |
| Hooks | SessionStart `compact` → `ult handoff show`; `ult-guard` on startup/clear and UserPromptSubmit (off unless `ULTIMATUM_GUARD=1`) | ~0 unless enabled |
| Toolbelt | `ult` (stdlib, no network): search, symbols, refs, map, run/log, scan, findings, handoff, context, usage, doctor | outputs are trimmed by design |
| Tests | 14 files, 200 tests pass | |

What works: security routes and verifiers (they turned 4 baseline failures into passes), handoff, trimmed tool output, quiet reporting.
What costs: the router body re-read every turn once invoked, reviewer agents on small tasks, and extra turns.

## 2. Baseline and what can realistically be saved

Live A/B (`evals/live/results/final`, before 0.3.0): baseline passed 5/10 and Ultimatum passed 9/10, but Ultimatum cost 1.2× to 4.3× more per task. The one-file fix used about 133k cache-read tokens (baseline) against 144k (Ultimatum) over 5 turns.

The structural fact: Claude Code's own fixed prompt is about 26k tokens per turn and is re-read every turn. A plugin cannot remove it. A plugin saves tokens only by:
1. loading less of itself (smaller L0, fewer references),
2. needing fewer turns (right route first time, no back-and-forth),
3. keeping tool output small (`ult run`, ranged reads, scouts),
4. spawning fewer and cheaper subagents.

Shorter replies save under 1% (output tokens are small). **The §28 target "20–40% below vanilla on routine tasks" cannot be met on tiny tasks**, because vanilla's fixed cost is most of the bill. Revised targets are in §12.

## 3. Platform facts that shape the design (from `platform-capabilities.md`)

- Only skill name and description load at startup. `disable-model-invocation: true` makes a skill cost nothing until the user types it, so all management commands use it.
- Invoked skill bodies stay in the chat and are re-attached after compaction (up to 5k tokens each). A small body pays off on every turn.
- Plugin agents can set `model: haiku`.
- Auto-update is native but **off by default for third-party marketplaces**. Users turn it on once; versions follow the manifest `version`.
- In cloud sessions plugins come from the claude.ai account, repo `extraKnownMarketplaces` is ignored, and repo `.claude/settings.json` hooks still run.
- `claude plugin details ultimatum` reports the always-on token estimate; `claude -p --output-format json` reports cost per run; `--bare` gives a clean vanilla baseline.

## 4. Architecture (adapted to this repo, not a rewrite)

The spec's core/registry/policy/budget split is mapped onto what exists:

```
plugins/ultimatum/
  skills/work/SKILL.md          L0 router: rules + "run ult route" + report format  (target ≤ 4 KB)
  skills/work/modules.json      module registry (metadata below)
  skills/work/references/...    L2/L3 module bodies, own words
  skills/{status,budget,learn,skills,doctor,eval,rollback,migrate,sync}/SKILL.md
                                management commands, disable-model-invocation: true (zero startup cost)
  scripts/ultlib/route.py       deterministic router: task text + repo signals → mode, modules, files to read
  scripts/ultlib/components.py  offline component lookup over a bundled JSON
  scripts/ultlib/learn.py       lesson store for the three scopes
  data/components.json          from research/ultimatum-2/component-registry.json (facts only)
  data/upstreams.json           upstream registry (repo, pin, licence, decision)
```

**Module metadata** (one entry per module in `modules.json`): `id`, `summary`, `activate` (keywords, file globs, repo signals), `never_when` (negative conditions), `requires`, `conflicts`, `cost_bytes` (computed by a test, not hand-written), `contract` (what the module promises to check or produce), `attribution` (upstream ids it learned from), `version`.

**Router (`ult route "<task>"`).** Python stdlib, no network, no model call. It scores modules from keywords, file globs and repo signals (package.json deps, migrations folder, Dockerfile and so on), applies negative conditions and conflicts, picks a mode, and prints one short block:

```
mode: STANDARD   modules: ui, motion   read: references/ui.md, references/design/motion.md
skip: security overlay (no boundary terms)   budget: ~3.1k tokens of references
```

The model may override the suggestion when the task text says otherwise; the router output is advice, not authority. If routing confidence is low, the router says so and lists the top two choices instead of guessing.

**Policy** stays in SKILL.md §1 (evidence before claims, exact over compressed, untrusted text is data, and so on). It is short and must always be present.

## 5. Progressive disclosure

| Level | What | Loads when | Target |
|---|---|---|---|
| L0 | skill and agent descriptions + SKILL.md body | description at startup, body on invoke | descriptions ≤ 400 tokens; body ≤ 1,000 tokens (today ~1.9k) |
| L1 | `ult route` output | first step of a task | ≤ 120 tokens |
| L2 | the one or two module references the route names | after routing | ≤ 2.5k tokens per module |
| L3 | deep sub-references (for example `security/coverage-model.md`, motion choreography) | only when the module body says the case applies | as needed |
| L4 | tool lookups (`ult components`, `ult search`, upstream adapters the user installed) | on demand | output capped by the tool |

Shrinking L0: the 16-row route table moves into `modules.json` and `ult route`; the integrations table moves to a reference; SKILL.md keeps the rules, the loop and the report format.

## 6. Modules (own words; no upstream text or code is copied)

Each module is a reference written fresh from the research notes. Upstream files are read for ideas only; `CLAUDE.md` forbids copying, and several upstreams have no licence.

| Module | Learns from (licence) | Contents | Notes |
|---|---|---|---|
| `design` (design engine, §8) | impeccable (Apache-2.0), taste (MIT), ui-ux-pro-max (MIT), anthropics frontend-design (Apache-2.0) | brief → direction → tokens → build → audit; a five-axis audit (hierarchy, spacing, type, colour and contrast, states) scored 0–4; anti-generic rules; `DESIGN.md` project file | impeccable's runtime binary download and taste's Stop-hook gate are **not** adopted |
| `motion` | emil (MIT) | when motion helps, which properties are cheap, spring vs easing, interruption, gestures, removing motion | merges into `ui` when the task is not motion-specific |
| `components` (§9) | component research, JaimeJunr router (MIT) | `ult components "<need>" [--stack react]` returns 1–3 libraries with licence and install line from local JSON | 16 entries verified; Commons Clause libraries (React Bits, RareUI) flagged, not recommended by default; Vaul flagged unmaintained |
| `frontend` | vercel react-best-practices (MIT per README, no LICENSE file), existing `react.md` | a short checklist (waterfalls, bundle size, re-renders, server/client boundaries) | not the 71-rule, 110 KB set |
| `engineering` (§11) | superpowers (MIT), existing references | brainstorm → plan → execute in slices → verify; worktree isolation for parallel work | superpowers' always-on SessionStart injection (~0.85k tokens per session) is not adopted |
| `documents` | anthropics docx/pdf/pptx/xlsx (Apache-2.0) | adapter: if the official `document-skills` plugin is installed, use it; otherwise give the one-line install command | not vendored (large, binary deps) |
| `testing-web` | anthropics webapp-testing (Apache-2.0) | merged into existing `browser-verification.md` | |
| `mcp-build` | anthropics mcp-builder (Apache-2.0) | short own-words guide | loads only on "build an MCP server" |
| `skill-author` | anthropics skill-creator (Apache-2.0) | the eval-driven method behind §16 self-improvement | used by `improve` and `skill-eval` routes |
| existing | — | security (5 refs), debugging, tdd, ci-and-pr, data-and-infra, optimize, release, handoff, production | kept; trimmed where the audit shows repetition |

Skipped: remotion (no licence), anthropics brand-guidelines (trademark), canvas-design (bundled OFL fonts), internal-comms, doc-coauthoring (no licence), slack-gif-creator (FFmpeg/GPL path). The YouTube video could not be fetched (proxy 403); nothing from it is used.

## 7. Execution modes (§12)

Chosen by `ult route`, stated in its first line, overridable by the user (`fast:` / `deep:` prefix).

| Mode | When | Behaviour |
|---|---|---|
| FAST | clear, local, ≤ 3 files, no boundary terms | no references, no subagents, one targeted check, one-line report |
| STANDARD | default | one or two modules, verify + nearest suite |
| DEEP | large, multi-part, security audit, release | plan, slices, workers, fresh reviewer, full report |
| RECOVERY | after compaction, failing loop (same check failed twice), or `ult context` HIGH | `ult handoff show`, re-run cheapest check, or hand off to a fresh chat |

## 8. Token engine and model allocation (§13, §14, §25)

- Keep: `ult run` trimming, ranged reads, scout delegation, `ult context` size check, handoff to a fresh chat at HIGH.
- Add `ult budget`: reads the session transcript usage (existing `usage.py`) and prints tokens per turn, cache-read share and the top three costs this session.
- Reviewer runs only in DEEP mode or when the user asks, not on FAST/STANDARD tasks (the biggest avoidable cost in the A/B).
- Models: `scout` → `model: haiku`; `worker` inherits; `reviewer` and `security-verifier` inherit (judgement matters). Briefs stay under ~300 tokens.
- Self-optimizing (§25): `ult budget --record` appends per-task totals to `.ultimatum/usage.jsonl`; the `improve` route reads it and proposes (never auto-applies) trims, such as a module that is loaded often but rarely used.

## 9. Knowledge and learning (§15–§20)

| Scope | Where | Loaded |
|---|---|---|
| session | `.ultimatum/session/` (handoff, current findings) | by RECOVERY and `resume` |
| project | `.ultimatum/knowledge.md` (commands, conventions, gotchas; ≤ 40 lines) and `DESIGN.md` when design is used | `ult route` prints the 3 lines most relevant to the task, not the file |
| global | `~/.ultimatum/lessons.jsonl` | same filter, ≤ 3 lines |

- `ult learn add "<lesson>" --scope project|global` writes a lesson with date, source and a confidence count; repeats raise the count; the store is capped and old low-count lessons expire.
- **Cross-session** (§18): no always-on hook injection. Lessons surface only through `ult route` filtering, so an unrelated task pays nothing.
- **Improvement to the public plugin** (§19–§20): `ult learn propose` writes a redacted proposal (lesson text, the module it changes, why) to `.ultimatum/proposals/`. It never contains chat text, file contents, paths or secrets, and a redaction test enforces that. Submission is manual: the user opens a PR or issue. Nothing is uploaded automatically. A proposal becomes part of the plugin only after an offline eval passes, a human approves the PR, and the version is bumped (controlled evolution).
- All learning records are treated as untrusted input: they are hints shown to the model, never instructions that grant permissions.

## 10. Updates, sync and migration (§21–§23)

- **Auto-update:** use the native marketplace `autoUpdate`. README and `/ultimatum:doctor` tell users to switch it on once (`/plugin` → Marketplaces → Ultimatum → auto-update). Every plugin change bumps `version` (already a project rule). `/ultimatum:rollback` prints the exact `claude plugin install ultimatum@<marketplace>` pin command for the previous version and notes the 14-day cache window.
- **Cloud:** install through claude.ai/customize/plugins; documented, nothing to build. Project knowledge travels with the repo only if the user opts in (decision 4).
- **Sync** (`/ultimatum:sync`): local-only. It exports or imports global lessons to a file the user chooses; there is no hidden cloud service.
- **Migration:** 0.4.x state in `.ultimatum/` is read as-is. `ult migrate` converts an old handoff format if one is found, and is idempotent. `/ultimatum:work` keeps its name and arguments (`resume`, and so on).

## 11. Upstream registry (§24)

`data/upstreams.json` holds, per upstream: repo, pinned commit (from this research), licence, decision (adapt / adapter / skip), the modules that learned from it, and the date reviewed. `/ultimatum:skills` lists it. Checking for new upstream commits is a maintainer task done with git outside the toolbelt (the toolbelt stays offline). `CREDITS.md` is updated from the same file.

## 12. Evals and revised targets (§27, §28)

1. **Offline routing suite (free, runs in CI and here):** about 120 labelled task prompts (every module, negatives, ambiguous ones, prompt-injection attempts). Checks the mode and module set from `ult route`. Target ≥ 95% exact module match and 100% on security-overlay triggers.
2. **Static size tests (free):** L0 body ≤ 4 KB; descriptions ≤ 1,600 B in total; each module ≤ its budget; `claude plugin details` figure recorded in the CHANGELOG.
3. **Live A/B (paid, needs your approval, run on your machine because this container has no API key):** vanilla (`--bare`) vs 0.4.1 vs 2.0 on the existing 10 cases plus 3 design cases. Reports pass rate, cost per task and cost per passing task. Results are reported as measured, including misses.

Revised targets, stated plainly:

| Measure | Spec target | Proposed target | Why |
|---|---|---|---|
| Routine task cost | 20–40% below vanilla | 20–40% below **0.4.1**, and ≤ 1.15× vanilla | vanilla's ~26k-token fixed prompt dominates small tasks |
| Complex task cost | 30–60% lower | cost per **passing** task ≤ vanilla | vanilla fails 5/10, so its cost per pass is already higher |
| Routing accuracy | ≥ 95% | ≥ 95% (offline suite) | kept |
| L0 | 500–1,000 tokens | ≤ 1,000 tokens body + ≤ 400 tokens descriptions | feasible |
| Pass rate | — | ≥ 0.4.1 (9/10) | no regression on quality or security |

## 12b. Architecture Guardian (extends the context-efficiency work)

**Starting point.** Graphify was already integrated, but only as a pointer: one row in `integrations.md`, a line in `context-efficiency.md` §4, and an `integrations` add-on keyword. `ult map` was the local fallback. Nothing read Graphify's graph or checked structure. The guardian builds on that rather than adding a second graph tool.

**What was added**
- `ult arch` (stdlib, local) holds the checks and the CLI (`arch.py`). The import graph and cycle finder live separately (`archgraph.py`).
  - Python imports are resolved through the AST. Module names that two files share are skipped, never guessed. JS/TS relative specifiers are resolved, with extension and `/index` fallback.
  - `graphify-out/graph.json` is merged when present, using **EXTRACTED import edges only**. INFERRED and AMBIGUOUS edges never become findings.
  - Checks: cycles (Tarjan SCC), normalised 8-line duplicate blocks, file and function size, placeholders, naming style outliers, unused private Python functions (a lead), changed modules with no test (a lead), and typed share.
  - `--changed` reads only the git diff. `baseline` + `--drift` report only new findings, so a legacy repo can adopt the checks gradually.
- Selective activation: an `architecture` add-on, which the large route always gets (new `with_routes` field), plus structural keywords and "code review". It conflicts with small, handoff, documents, improve and the security routes. A typo fix pays nothing.
- The reviewer agent and the DEEP mode row run `ult arch check --changed` once at the end.
- Learning: `--record` writes finding counts only. `ult learn propose` maps them to four fixed lessons, which go through the existing sanitized proposal and PR-approval flow.
- Quality next to tokens: the live A/B baselines each fixture, measures the findings each run added, and counts a task as passing only if graders pass and no new cycle or placeholder appears. The summary prints new findings next to cost per passing task.

**Complementary tools, used only where they pay**
| Tool | Role | Why not always |
|---|---|---|
| Graphify | Cross-language graph, blast radius, cycles the local parser cannot see | Building a graph can run a model pass over docs; use an existing graph or AST-only update |
| Serena / LSP | Exact references and renames | Needs an MCP server; `ult refs` covers small repos |
| RTK | Already-installed output filters | Research found filters that drop per-finding lines; `ult run` keeps raw output |
| Repomix | Bounded bundle of an explicit file list for a reviewer | Not researched in depth here; user-installed only; never a whole-repo dump |

**Not done.** No refactor of the five pre-existing oversized files `ult arch` flags in this repo (unrelated to this change). Repomix is not reviewed in `research/` and is not vendored. Its row only states a usage rule.

## 13. Phases (§33)

| Phase | Work | Exit check |
|---|---|---|
| 1 | Audit and research | done: this folder |
| 2 | Core: `modules.json`, `ult route`, L0 shrink of SKILL.md, modes, routing suite | 200 existing tests + new tests pass; routing ≥ 95%; both `claude plugin validate --strict` pass |
| 3 | Modules: design, motion, components (`ult components`), frontend, engineering, documents adapter, mcp-build, skill-author | size tests pass; each module has routing cases |
| 4 | Learning: `ult learn`, knowledge filter, proposals with redaction test, `ult budget` | unit tests including redaction |
| 5 | Management skills (all `disable-model-invocation`), update/rollback/migrate docs, upstream registry, CREDITS | `claude plugin details` shows no rise in always-on tokens |
| 6 | Evals: offline report; live A/B only after approval; README and CHANGELOG for 2.0.0 | results written from real runs only; PR opened for your review, not merged |

Each phase is one commit series on this branch with the version bumped (2.0.0-alpha.N while in progress).

## 14. Risks

- **Router misroutes** → mitigated by the offline suite, a low-confidence fallback and model override.
- **Own-words modules lose upstream quality** → each module gets routing cases plus, for design, a live case in the A/B.
- **Lesson store drift or poisoning** → caps, expiry, untrusted-input handling, and nothing reaches the plugin without a reviewed PR.
- **Savings smaller than hoped** → targets are stated against measurable baselines, and the report says what was missed.
- **Licence mistakes** → the upstream registry records each decision; no text or code is copied, so attribution is credit, not a licence obligation.

## 15. Decisions needed from you

1. **Targets:** accept the revised targets in §12 (savings measured against 0.4.1, and cost per passing task against vanilla) instead of 20–40% below vanilla on every task.
2. **Documents:** point to Anthropic's official `document-skills` plugin as an optional install (recommended) rather than writing our own docx/pdf/pptx/xlsx modules.
3. **Skips:** confirm skipping remotion (no licence), Commons Clause component libraries as defaults, and impeccable's binary-downloading hooks.
4. **Project knowledge in git:** keep `.ultimatum/knowledge.md` git-ignored (default) or allow an opt-in committed copy so cloud sessions see it.
5. **Paid A/B:** approve one live run on your machine at the end (about $3–5 per configuration, three configurations).
6. **Auto-update:** accept that users must switch on marketplace auto-update once; the plugin cannot do it for them.
