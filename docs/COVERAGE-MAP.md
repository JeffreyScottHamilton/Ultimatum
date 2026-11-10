# Upstream coverage map

Maintainer-facing map from every capability in the upstream research inventories to what Ultimatum does about it today. It is not a user guide and not a marketing claim. Written 2026-11-10 against the plugin tree in this repository. Upstream revisions and licenses come from `research/REVISIONS.md`; capability ids come from `research/context-efficiency.md`, `research/engineering-delivery.md`, `research/ui-browser.md` and `research/security.md`.

Policy reminder: Ultimatum ships original text and code only. Nothing here quotes upstream wording. ASVS and WSTG are cited by id and title only (CC BY-SA); context-mode (ELv2) and Serena's application (GPL) are design references only.

## How to read the tables

- One section per upstream project, in the order of the research files. Each section gives the repo, the inspected revision and the license, then one row per capability id. No inventory id is omitted (the generator that produced this file checked the list against the four research files).
- Columns: `id | capability (user-facing) | status | where in Ultimatum | verification | notes`.
- Path shorthand. A bare name such as `tdd.md` is `plugins/ultimatum/skills/work/references/tdd.md`; `security/findings.md` is under `references/security/`; `agents/x.md`, `scripts/...`, `tests/...` and `schemas/...` are under `plugins/ultimatum/`. `§N` is the numbered heading in that file; `react.md` uses letters (`§A` to `§I`). `ult <cmd>` is `python3 plugins/ultimatum/scripts/ult <cmd>`.
- "Partial" after native or shared means the capability is covered only in part. The note says which part. Partial rows are counted separately in the summary.
- Every path and section number in the `where` column was checked by script against the files on disk. A `native` row whose file is missing would be shown as `native (pending: <file>)`; there are none at the time of writing.

## Status legend

| Status | Meaning |
|---|---|
| **native** | An Ultimatum file implements it. The row names the file and section, or the `ult` subcommand. |
| **shared** | Covered by a general behavior rather than a dedicated mechanism, for example SKILL.md §1 rule 2 (exact evidence). The row names the behavior. |
| **optional** | Needs an external tool or MCP server. The row names it, how it is detected, and the local fallback. Nothing is installed or contacted without the user asking (SKILL.md §4). |
| **gap** | Not covered. The note gives the reason and what would close it. |
| **rejected** | Deliberately not adopted (always-on hooks, telemetry, network or hosted dependence, license, out of scope), with the reason. |

## Verification legend

Inventory text or a reference file is not verification. The column says what, if anything, runs against the capability:

- `unit: test_x.py`: a stdlib unit test under `plugins/ultimatum/tests/` exercises the script behavior. Run: `python3 -m unittest discover -s plugins/ultimatum/tests`. At time of writing that command ran 165 tests, all passing, on a machine with Playwright available (the browser tests need node and Playwright).
- `eval N-name (defined, not run)`: `evals/live/run_live.py` has a case with deterministic graders on the fixture, but no recorded result exists. `(run)`: a result is recorded under `evals/live/results/smoke-1`. Only `1-one-file` has been run, in both arms, and both arms passed, so it does not yet show any difference from plain Claude Code.
- Eval graders check outcomes (tests pass, files touched, a probe result), not whether a reference was followed. A note says which outcome is graded.
- `none (guidance text only)`: the behavior is an instruction in a reference file, not exercised by any test or eval. `none (not implemented)`: nothing exists.

## Summary counts

Counts are rows (capability ids). The partial column is a subset of native plus shared, not an extra status.

| Project | native | native (pending) | shared | optional | gap | rejected | total | of which partial |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| caveman | 13 | 0 | 2 | 0 | 0 | 10 | 25 | 8 |
| rtk | 5 | 0 | 0 | 0 | 1 | 7 | 13 | 3 |
| context-mode | 5 | 0 | 2 | 0 | 1 | 5 | 13 | 6 |
| graphify | 1 | 0 | 1 | 3 | 0 | 5 | 10 | 1 |
| serena | 2 | 0 | 3 | 7 | 0 | 3 | 15 | 2 |
| context7 | 0 | 0 | 0 | 4 | 0 | 4 | 8 | 0 |
| ponytail | 5 | 0 | 4 | 0 | 3 | 2 | 14 | 5 |
| andrej-karpathy-skills | 0 | 0 | 4 | 0 | 0 | 0 | 4 | 0 |
| skills (Matt Pocock) | 10 | 0 | 6 | 0 | 6 | 3 | 25 | 6 |
| superpowers | 13 | 0 | 2 | 0 | 2 | 1 | 18 | 3 |
| plugin-claude (Sentry) | 2 | 0 | 0 | 0 | 2 | 2 | 6 | 0 |
| skills (Sentry) | 6 | 0 | 4 | 1 | 0 | 1 | 12 | 4 |
| gstack | 4 | 0 | 7 | 0 | 2 | 3 | 16 | 6 |
| agent-skills (Supabase) | 4 | 0 | 2 | 1 | 0 | 0 | 7 | 2 |
| agent-skills (HashiCorp) | 3 | 0 | 0 | 0 | 0 | 5 | 8 | 2 |
| autoresearch | 4 | 0 | 4 | 0 | 0 | 1 | 9 | 5 |
| skills (Anthropic): skill-creator | 4 | 0 | 0 | 0 | 4 | 0 | 8 | 1 |
| taste-skill | 7 | 0 | 2 | 0 | 0 | 6 | 15 | 7 |
| impeccable | 10 | 0 | 6 | 0 | 1 | 7 | 24 | 7 |
| skills (Emil Kowalski) | 6 | 0 | 4 | 0 | 4 | 2 | 16 | 5 |
| ui (shadcn skill) | 1 | 0 | 1 | 1 | 0 | 8 | 11 | 2 |
| agent-skills (Vercel) | 4 | 0 | 1 | 0 | 0 | 4 | 9 | 1 |
| playwright-cli | 5 | 0 | 3 | 0 | 5 | 4 | 17 | 4 |
| axe-core | 1 | 0 | 2 | 2 | 2 | 1 | 8 | 1 |
| chrome-devtools-mcp | 0 | 0 | 2 | 7 | 0 | 2 | 11 | 1 |
| security-audit-skill (Cloudflare) | 20 | 0 | 0 | 0 | 2 | 0 | 22 | 8 |
| skills (Trail of Bits) | 11 | 0 | 5 | 2 | 8 | 5 | 31 | 7 |
| ASVS 5.0 | 19 | 0 | 0 | 0 | 1 | 1 | 21 | 17 |
| Web Security Testing Guide | 1 | 0 | 1 | 0 | 0 | 0 | 2 | 2 |
| semgrep | 0 | 0 | 0 | 5 | 2 | 1 | 8 | 0 |
| osv-scanner | 0 | 0 | 0 | 4 | 1 | 1 | 6 | 0 |
| gitleaks | 0 | 0 | 1 | 6 | 0 | 0 | 7 | 1 |
| **All projects** | **166** | **0** | **69** | **43** | **47** | **94** | **419** | **117** |

By research area:

| Area | native | pending | shared | optional | gap | rejected | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Context and token efficiency | 26 | 0 | 8 | 14 | 2 | 34 | 84 |
| Engineering, planning and delivery | 55 | 0 | 33 | 2 | 19 | 18 | 127 |
| UI, design engineering and browser verification | 34 | 0 | 21 | 10 | 12 | 34 | 111 |
| Security and test depth | 51 | 0 | 7 | 17 | 14 | 8 | 97 |

Verification of the rows that claim some coverage (native, shared, optional):

- 278 rows in total. 83 touch a unit test, 23 name an eval case (8 both), and 180 have neither.
- None of the eval cases other than `1-one-file` has a recorded result, so eval mentions mean "a grader exists", not "verified by a run".
- Rows that rely on a reference file alone (the large majority of engineering, UI and planning rows) are guidance: they describe what the agent is told to do, not proof that it does it.

## Genuine gaps

47 rows are gaps. Reason and closure are taken from each row's note. Rows marked partial in the tables below are also incomplete, but they have some coverage, so they are not listed here.

| id | project | capability | reason and what would close it |
|---|---|---|---|
| RTK-03 | rtk | Declarative, user-extensible TOML filters with inline tests | Reason: families are hard-coded in run.py and not loadable from a project file. Closure: add an opt-in filter file with a trust gate, only if the generic fallback proves too noisy in practice. |
| CTX-02 | context-mode | Batch several commands and queries in one call | Reason: separate `ult run` and `ult find` calls cost extra turns. Closure: low value; document a two-call pattern only if measured turns matter. |
| PNT-05 | ponytail | Deferral marker comments for known-limit shortcuts | Reason: no marker convention; Ultimatum avoids adding comment conventions to user code. Closure: a one-line rule in SKILL.md §3 if users ask for it. |
| PNT-09 | ponytail | Whole-repo lean audit lens | Reason: no over-engineering audit route; `discover` and `sec-audit` are different questions. Closure: a short reference that points `ultimatum:reviewer` at a repo scope. |
| PNT-10 | ponytail | Debt ledger from deferral markers | Reason: depends on PNT-05 markers. Closure: only if PNT-05 is adopted; release.md §2 step 5 already greps TODO/FIXME the change introduced. |
| MPC-11 | skills (Matt Pocock) | PR body with visual summary, evidence, merge danger | Reason: no PR-writing guide (one-way doors are covered for releases in release.md §4). Closure: a short PR-description section in ci-and-pr.md or release.md. |
| MPC-12 | skills (Matt Pocock) | Issue triage label state machine | Reason: only PR feedback triage exists (ci-and-pr.md §4). Closure: a triage reference if issue management is wanted. |
| MPC-14 | skills (Matt Pocock) | Retro of the agent environment (navigation, checks, standards) | Reason: no environment retro. Closure: reuse skill-evaluation.md §8 style findings in a short retro route. |
| MPC-17 | skills (Matt Pocock) | Deep-module vocabulary and architecture improvement | Reason: no architecture-improvement route (tdd.md §2 only mentions adding a seam). Closure: a reference on module depth and seams. |
| MPC-19 | skills (Matt Pocock) | Generate an interactive bash script for human-only steps | Reason: not covered. Closure: low priority; add only on demand. |
| MPC-21 | skills (Matt Pocock) | Re-pitch in simple terms; questionnaire builder | Reason: communication helpers, not covered. Closure: none planned. |
| SUP-16 | superpowers | Finishing a branch: tests green, then a fixed set of options | Reason: release.md covers readiness but not a merge/PR/discard menu; orchestration.md §7 says not to push without authorization. Closure: a short finish-branch section. |
| SUP-18 | superpowers | Forensic review of a past session from transcripts | Reason: no transcript-forensics route. Closure: out of scope unless requested; eval stream output exists in evals/live/results. |
| SPC-03 | plugin-claude (Sentry) | Issue-category awareness (cron/metric monitors have no stack trace) | Reason: production.md does not mention monitor-type issues. Closure: one paragraph in production.md §1. |
| SPC-04 | plugin-claude (Sentry) | Make stack traces readable (source maps, dSYM, ProGuard ...) | Reason: production.md §2 only says to ask for source maps or the right revision. Closure: a symbolication subsection. |
| GST-10 | gstack | /modernize: revalidate an old PR as a claim | Reason: not covered. Closure: a short stale-PR revalidation section in ci-and-pr.md. |
| GST-13 | gstack | /health weighted code-quality score | Reason: no composite score. Closure: not planned; the optimization loop can track any metric the user names. |
| SKC-04 | skills (Anthropic): skill-creator | Benchmark aggregation: mean, stddev, delta | Reason: run_live.py writes per-run summaries; skill-evaluation.md §4 describes mean ± stdev, but no script aggregates. Closure: an aggregation script over summary.json. |
| SKC-05 | skills (Anthropic): skill-creator | Blind A/B comparison and unblinding analysis | Reason: not built. Closure: add only if rubric-style outputs need comparison. |
| SKC-06 | skills (Anthropic): skill-creator | Trigger evals and description optimization | Reason: skill-evaluation.md §1 step 6 and §3 near-miss negatives are guidance; no trigger runner exists. Closure: a small `claude -p` trigger harness. |
| SKC-08 | skills (Anthropic): skill-creator | Human review viewer with per-case feedback | Reason: not built. Closure: low priority. |
| IMP-06 | impeccable | document: generate DESIGN.md from code | Reason: ui.md reads an existing DESIGN.md but has no procedure to derive one. Closure: a token/component extraction procedure that asks before adding a tracked file. |
| EML-05 | skills (Emil Kowalski) | Find places that should animate | Reason: not covered. Closure: low value; ui.md §5 steps 1-2 can be applied on request. |
| EML-08 | skills (Emil Kowalski) | Choreography recipes: staggers, entrances, morphs | Reason: ui.md allows one authored moment and view transitions only. Closure: a short recipes reference if heavy motion work is common. |
| EML-09 | skills (Emil Kowalski) | Gestures: finger tracking, interruptible drag and sheets | Reason: only a pointer-tracking note exists (ui.md §5 step 6). Closure: gesture reference. |
| EML-10 | skills (Emil Kowalski) | Apple-style spring motion and materials | Reason: not covered. Closure: low priority. |
| PWC-01 | playwright-cli | Snapshot and ref model (YAML accessibility snapshot, element refs) | Reason: ult-browser uses CSS selectors and does not emit an accessibility snapshot. Closure: optionally add a snapshot dump or detect and use the upstream CLI when installed. |
| PWC-03 | playwright-cli | Snapshot options and find | Reason: depends on PWC-01. Closure: same. |
| PWC-06 | playwright-cli | Tabs, named sessions, persistent profile | Reason: each viewport uses a fresh context. Closure: not needed for verification; add only if login-flow checks require it. |
| PWC-11 | playwright-cli | Tracing and video recording | Reason: not provided. Closure: optional flag to write a Playwright trace. |
| PWC-13 | playwright-cli | highlight and generate-locator | Reason: not provided. Closure: low priority. |
| AXE-02 | axe-core | Rule and tag selection (wcag2a, wcag22aa, best-practice ...) | Reason: the script runs axe with its defaults. Closure: pass a `runOnly` tag option through a flag. |
| AXE-04 | axe-core | Incomplete (needs review) results | Reason: only violations are reported; incomplete results are dropped. Closure: report incomplete counts as WARN. |
| CF-08 | security-audit-skill (Cloudflare) | Prior-run reuse with carried and revalidated findings | Reason: findings.md §2 keeps rejected items so they are not rediscovered, and fingerprints must be unique, but no re-run procedure exists. Closure: a re-run section in full-audit.md (carry confirmed items, revalidate changed files). |
| CF-11 | security-audit-skill (Cloudflare) | Coverage-critic waves looking for unmapped surface | Reason: no critic agent or step; full-audit.md §4 (deep) only adds a second pass on high-risk checked items. Closure: add a fresh-context critic step that reads the trust-boundary map and ledger. |
| TOB-06 | skills (Trail of Bits) | Semgrep rule creation and porting | Reason: specialist task. Closure: point to an installed upstream rule-authoring plugin; nothing built in. |
| TOB-18 | skills (Trail of Bits) | Fuzzing and sanitizer handbook skills | Reason: native-code fuzzing is specialist work. Closure: mention as an escalation only; no built-in route. |
| TOB-21 | skills (Trail of Bits) | Constant-time analysis (compiler-induced timing channels) | Reason: specialist crypto tooling. Closure: out of scope for the base plugin. |
| TOB-22 | skills (Trail of Bits) | Zeroization audit | Reason: specialist (asm/CFG). Closure: out of scope. |
| TOB-23 | skills (Trail of Bits) | C and Rust language-specific reviews | Reason: no language-specific multi-worker review. Closure: out of scope. |
| TOB-24 | skills (Trail of Bits) | Trailmark code graph and slicing | Reason: `ult map` is a lighter, regex-based map. Closure: optional Graphify (GRA rows) for graph needs. |
| TOB-25 | skills (Trail of Bits) | Smart-contract security scanners and advisors | Reason: blockchain is out of scope. Closure: none planned. |
| TOB-29 | skills (Trail of Bits) | Open-sourcing hygiene incl. secrets in history | Reason: `ult scan` runs gitleaks on a directory, not git history, and release.md §5 checks the diff only. Closure: run `gitleaks git` when installed and add a pre-release history check. |
| ASVS-03 | ASVS 5.0 | Level selection guidance (L1 / L2 / L3) | Reason: no level policy; profiles quick/standard/deep (full-audit.md §4) change breadth instead. Closure: add a level-to-profile note if users ask for ASVS-level claims. |
| SG-05 | semgrep | Targeting: include/exclude, severity filters, ignore files | Reason: only `--path` narrows the scan target; semgrep's own filters are not passed through. Closure: pass-through flags. |
| SG-07 | semgrep | Rule authoring helpers (--validate, --test) | Reason: same as TOB-06. Closure: none planned. |
| OSV-02 | osv-scanner | Lockfile selection, ignore handling, config file | Reason: not exposed. Closure: pass-through flags if a repo needs them. |

Suggested priority (maintainer judgement, in rough order of effect on correctness):

1. **CF-11, CF-08 (audit rigor).** No coverage-critic step and no re-run procedure, so an audit can close its ledger without anyone checking what the ledger omitted, and repeat audits start from zero.
2. **TOB-29 / GL-01 (secrets in history).** Nothing scans git history for committed secrets.
3. **PWC-01 / PWC-03 (browser snapshots) and AXE-04 (axe incomplete results).** The browser check cannot report an accessibility tree and drops axe's "needs review" results.
4. **SKC-04 to SKC-06 (eval tooling).** There is no aggregation, blind comparison or trigger-eval runner, and only one of nine eval cases has been run.
5. **MPC-11 / SUP-16 / GST-10 (delivery edges).** No PR-description guide, finish-branch options, or stale-PR revalidation.

## Known verification limits

- `ult scan` has `tests/test_scan.py`, but the semgrep, gitleaks and osv-scanner paths are tested only against stub executables. No test runs the real tools.
- `ult run` zero-tests-ran detection (the `ZERO_RUN` patterns) has no dedicated test. The cargo, go, tsc, lint, install and git output families have no dedicated test either; unittest, pytest-like and jest-like selection are tested.
- `scripts/ult-browser.mjs`: tests cover the fixture app, a deliberately broken page, external-origin blocking, stress overflow and the missing-Playwright exit 3. They do not assert the console-error finding, `--reduced-motion`, or the path where axe-core is installed.
- Eval cases 2 to 9 are defined with deterministic graders against `fixtures/` answer keys, but none has been run. The answer keys under `fixtures/_answer-keys/` were not read for this map.
- Reference-file behavior is exercised only by the evals, and apart from `1-one-file` none has run. Whether an agent follows a given paragraph is unmeasured.

## Context and token efficiency (research/context-efficiency.md)

### caveman

Repo `JuliusBrussee/caveman` · revision `3dc497a7f858` · license: Apache-2.0

Counts: native 13, pending 0, shared 2, optional 0, gap 0, rejected 10 (25 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| CAV-01 | Terse chat voice, answer first, facts intact | native | context-efficiency.md §2 | none (guidance text only) | On request only ("be brief"); no mode flag, levels, or persistence. Repo-persisted text is not terse. |
| CAV-02 | Maximum-compression voice with a never-cut floor | shared | context-efficiency.md §1 (the table is the floor) and §2 | none (guidance text only) | No separate mode. Asking for terser output tightens prose only; the never-compress column still applies. |
| CAV-03 | Classical-Chinese compression mode | rejected | - | none (guidance text only) | Upstream calls the savings small and noisy; no fit for this plugin. |
| CAV-04 | Mode persistence across sessions, compaction, subagents; status badge | rejected | - | none (guidance text only) | Needs SessionStart/UserPromptSubmit/SubagentStart hooks and a statusline. Ultimatum ships no hooks (research/ARCHITECTURE-DECISIONS.md #12). |
| CAV-05 | /caveman-stats: per-session token savings report | rejected | - | none (guidance text only) | Reads transcripts through a hook. Ultimatum makes no savings claims without a measured baseline (skill-evaluation.md §6). |
| CAV-06 | Terse Conventional-Commits writer | rejected | - | none (guidance text only) | Commit text follows the project's own style (context-efficiency.md §2, not-terse list). No terse commit mode. |
| CAV-07 | One-line-per-finding terse code review | native (partial) | agents/reviewer.md (`[P0-P3] path:line — problem — evidence — fix`) | none (guidance text only) | Partial: findings are ranked one-liners with evidence, but not a fixed 4-severity terse grammar. Security findings use full fields (security/findings.md §1). |
| CAV-08 | /caveman-compress: rewrite memory files tersely with backup | rejected | - | none (guidance text only) | Sends file contents to a model provider and has no local equivalent. Not adopted. |
| CAV-09 | Delegation decision guide (who gets what) | native | orchestration.md §1, §3; context-efficiency.md §6; SKILL.md §3 Delegation | none (guidance text only) | Includes the spot-check rule for a worker's "no match" / "no issues" claims (context-efficiency.md §6). |
| CAV-10 | Read-only locator returning path:line anchors | native | agents/scout.md | none (guidance text only) | Cheap model (haiku), read-only Bash, answer + anchors + an Unverified list. Re-verification of negative claims is the manager's duty. |
| CAV-11 | Surgical 1-2 file builder with a receipt | native (partial) | agents/worker.md | none (guidance text only) | Partial: owns a file list and reports Status/Files/Acceptance, and can run tests (upstream builder cannot). No `too-big`/`ambiguous` refusal grammar; BLOCKED/NEEDS_CONTEXT instead. |
| CAV-12 | Severity-tagged diff reviewer | native | agents/reviewer.md | none (guidance text only) | Sonnet, read-only apart from running tests through `ult run`. |
| CAV-13 | Cold-start localizer returning only path:range reasons | native (partial) | agents/scout.md; discovery.md §2 | none (guidance text only) | Partial: anchors are `path:line`, not ranges, and there is no first-turn parallel fan-out rule. |
| CAV-14 | Per-role model pinning | native | `model:` in each agents/*.md (scout haiku; worker, reviewer, security-hunter sonnet; security-verifier inherit) | none (guidance text only) | Static choice only. No env-var override and no dynamic routing. Rationale: context-efficiency.md §6 (model by role). |
| CAV-15 | Small workflow skills: investigate-first, lean-build, surgical-patch, safe-refactor, migration, verify-and-stop | shared | SKILL.md §1 rules 1-3, §3; discovery.md; feature-planning.md §7.6; data-and-infra.md §1; tdd.md §3 | none (guidance text only) | Spread across the single router skill and references instead of six skills. |
| CAV-16 | Help card | native (partial) | `ult --help` | unit: test_doctor.py | Partial: lists the toolbelt only (test_help_and_bad_cmd). No card for the skill's routes. |
| CAV-17 | Slash-command stubs per mode | rejected | - | none (guidance text only) | One entry point `/ultimatum:work <task>`; no commands/ directory (ARCHITECTURE-DECISIONS.md #1). |
| CAV-18 | /caveman-init: always-on rule files for other editors (curl \| node) | rejected | - | none (guidance text only) | Claude Code plugin only; piping a download into an interpreter is not acceptable. |
| CAV-19 | MCP proxy that shrinks tool descriptions | rejected | - | none (guidance text only) | Ultimatum ships no MCP servers or proxies. |
| CAV-20 | Engine: detect content shape, compress, store exact original, retrieve by handle | native (partial) | `ult run`, `ult log`, `ult find`, `ult get` (scripts/ultlib/run.py, store.py); context-efficiency.md §3, §5 | unit: test_run.py, test_store.py; eval 3-noisy (defined, not run) | Partial: command-output families only (unittest, pytest, jest, go, cargo, tsc, lint, install, git, generic). No JSON/HTML/diff/table compressors. Raw log is kept byte for byte (test_raw_log_byte_identical). |
| CAV-21 | Durable project facts with recall budget, supersede, forget | native (partial) | `ult note` / `ult find` / `ult get` (store.py); handoff.md | unit: test_store.py | Partial: FTS5 search with kinds. No supersede, history or forget commands. |
| CAV-22 | Bounded repo map and evidence bundle | native (partial) | `ult map build\|summary\|query` (repomap.py); discovery.md §1 | unit: test_map.py; eval 2-unfamiliar (defined, not run) | Partial: regex-built, capped, section-queried. No match-strength classification; hits are labelled leads (repomap docstring). |
| CAV-23 | Hosted-account skills (discover, setup, optimize, manage, learn) | rejected | - | none (guidance text only) | Need a hosted account; not applicable. |
| CAV-24 | Local LLM proxy, agent wrapping, browser bridge, image pipeline, SDKs | rejected | - | none (guidance text only) | Out of scope; no proxy, daemon or telemetry. |
| CAV-25 | Honest measurement harness (baseline, control prompt, skill arm) | native (partial) | evals/live/run_live.py; skill-evaluation.md §2, §4, §6 | harness only: ran for 1 case (evals/live/results/smoke-1); no unit test | Partial: two arms (plugin vs plain), no "answer concisely" control arm. Only 1-one-file has a recorded result and both arms passed, so it does not discriminate yet. |

### rtk

Repo `rtk-ai/rtk` · revision `08a261a0d081` · license: Apache-2.0 (CLI and filters); the `proxy/` daemon is BUSL-1.1

Counts: native 5, pending 0, shared 0, optional 0, gap 1, rejected 7 (13 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| RTK-01 | Transparent rewrite of Bash commands to filtered forms | rejected | - | none (guidance text only) | A PreToolUse rewrite hook is an always-on hook that changes what runs. Replaced by explicit `ult run -- <cmd>` where the agent chooses. |
| RTK-02 | Per-tool output filters (~100 commands) | native (partial) | `ult run` families in scripts/ultlib/run.py; context-efficiency.md §3 | unit: test_run.py | Partial: nine families plus a generic fallback. Does not inject machine-readable flags into the command. Dedicated tests exist for unittest, pytest-like and jest-like selection and the buried-failure case; cargo, go, tsc, lint, install and git families have no dedicated test. |
| RTK-03 | Declarative, user-extensible TOML filters with inline tests | gap | - | none (not implemented) | Reason: families are hard-coded in run.py and not loadable from a project file. Closure: add an opt-in filter file with a trust gate, only if the generic fallback proves too noisy in practice. |
| RTK-04 | Raw output recovery by hash | native | `ult run` writes `.ultimatum/logs/<id>.log` (mode 0600); `ult log <id> --lines A:B \| --grep RE`; context-efficiency.md §3 | unit: test_run.py; eval 3-noisy (defined, not run) | Always stored, not only on failure. Printed output is redacted, the raw log is not. No retention cap is documented. |
| RTK-05 | "Never worse" guard and three-tier parsing | native (partial) | `ult run` selection tiers (passthrough / structured / pattern) in run.py | unit: test_run.py | Partial: small output passes through unchanged (test_small_output_full). No token-estimate comparison. A non-zero exit with no recognised pattern prints a warning instead of claiming success. |
| RTK-06 | Exit code propagation and a bypass hatch | native | `ult run` returns the child's exit code; plain Bash for quiet commands (context-efficiency.md §3) | unit: test_run.py | Tested: exit codes, 127 missing command, 124 timeout, signal death. |
| RTK-07 | Read/grep/find/ls/json/log helpers with caps | native (partial) | `ult search`, `ult symbols`, `ult refs` (search.py); context-efficiency.md §4 | unit: test_search.py | Partial: grouped, capped search with ripgrep or a Python fallback. No read-with-comment-stripping, tree, wc or json-schema helpers. |
| RTK-08 | Savings analytics, discover, learn | rejected | - | none (guidance text only) | No telemetry and no savings claims without a baseline (skill-evaluation.md §6). `ult logs` lists runs and exit codes only. |
| RTK-09 | Pipeline presets (terse, verbatim-diffs, delegate-reads, posthook) | rejected | - | none (guidance text only) | Engine/hook features. The equivalents that exist are rules: code and diffs are never compressed (context-efficiency.md §1) and broad reads go to `ultimatum:scout` (§6). |
| RTK-10 | LLM API proxy daemon | rejected | - | none (guidance text only) | Out of scope and a different license (BUSL-1.1). |
| RTK-11 | Hook integrity, trust gate, permission precedence | rejected | - | none (guidance text only) | No hooks are shipped, so there is nothing to integrity-check. `ult scan` flags risky hooks in a scanned repo (rules `agent-hook-fetch-exec`, `agent-bypass-permissions`). |
| RTK-12 | Installers for ~15 agents | rejected | - | none (guidance text only) | Claude Code plugin only. |
| RTK-13 | Maintainer-only skills and agents for developing rtk | rejected | - | none (guidance text only) | Not a user-facing capability. |

### context-mode

Repo `mksglu/context-mode` · revision `3a3ef7d53c9a` · license: Elastic License 2.0 (source-available). Ideas only; no code or prose reused

Counts: native 5, pending 0, shared 2, optional 0, gap 1, rejected 5 (13 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| CTX-01 | Run code, return only what it prints, index the rest | native (partial) | `ult run` (`--timeout`, `--shell` opt-in); context-efficiency.md §3 | unit: test_run.py | Partial: runs a command, prints bounded evidence, keeps the full log. No interpreter runner, no `intent` query over output, no output cap pointer to a search tool. |
| CTX-02 | Batch several commands and queries in one call | gap | - | none (not implemented) | Reason: separate `ult run` and `ult find` calls cost extra turns. Closure: low value; document a two-call pattern only if measured turns matter. |
| CTX-03 | Index a file, URL or text into the store | native (partial) | `ult note --body -` (stdin) and automatic log indexing (store.py) | unit: test_store.py | Partial: notes and run logs only. Arbitrary files and URLs are not indexed (URL fetch is network egress). |
| CTX-04 | BM25 search over indexed content with scopes | native (partial) | `ult find` / `ult get` (SQLite FTS5 in `.ultimatum/index.db`); context-efficiency.md §5 | unit: test_store.py | Partial: one project DB, kind filter, no session/worktree scopes, no recency fusion. Hits point back to log ranges that must be re-read. |
| CTX-05 | Resume block after compaction | native (partial) | `ult handoff write\|show` (handoff.py); handoff.md | unit: test_handoff.py; eval 9-handoff (defined, not run) | Partial: written on request and checked on resume (HEAD moved, missing files/log ids). Not generated automatically after compaction. |
| CTX-06 | stats / doctor / upgrade / purge tools | native (partial) | `ult doctor` | unit: test_doctor.py | Partial: only doctor exists, and it lists CLI tools without changing anything. Stats, upgrade and purge are not provided (self-modifying or telemetry). |
| CTX-07 | Automatic replacement of oversized tool output | rejected | - | none (guidance text only) | A PostToolUse hook that rewrites what the model sees. Explicit `ult run` instead. |
| CTX-08 | Deny whole-file Read over a size limit | rejected | - | none (guidance text only) | Enforcement hook not adopted. Advice only: read the relevant range (context-efficiency.md §4 step 2). |
| CTX-09 | Deny WebFetch and unbounded curl in favour of index-and-search | rejected | - | none (guidance text only) | Hook-based denial. Ultimatum's rule is network use only on the user's say-so (SKILL.md §4). |
| CTX-10 | Subagents inherit the output budget | shared (partial) | Reply caps in agents/scout.md (about 40 lines) and agents/worker.md (15 lines); orchestration.md §3 REPLY | none (guidance text only) | Partial: requested in prompts, not enforced. |
| CTX-11 | Journal of tool calls and memory-file indexing | rejected | - | none (guidance text only) | Needs a capture hook and stores tool outputs outside the repo. Ultimatum keeps explicit notes, logs and handoffs instead. |
| CTX-12 | Prompt-cache safety rules | shared | By construction: no hooks, no MCP server, static SKILL.md and references (ARCHITECTURE-DECISIONS.md #12) | none (guidance text only) | Nothing mutates the tool list or injected text mid-session. Not independently measured. |
| CTX-13 | Adapters for ten hosts | rejected | - | none (guidance text only) | Claude Code only. |

### graphify

Repo `Graphify-Labs/graphify` · revision `5eedffa87476` · license: Apache-2.0

Counts: native 1, pending 0, shared 1, optional 3, gap 0, rejected 5 (10 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| GRA-01 | Persistent code/docs graph with report and HTML | optional | Graphify if a built graph (`graphify-out/`) or its tool exists; `ult doctor` does not detect it (SKILL.md §4). Fallback: `ult map build` | unit: test_map.py | Never load a whole graph; query it narrowly (context-efficiency.md §4 step 4). Fallback is a regex map at `.ultimatum/map.json`, not an AST graph. |
| GRA-02 | Graph query, path and explain commands | optional | Graphify CLI if present. Fallback: `ult map query <term>`, `ult symbols`, `ult refs` | unit: test_map.py, test_search.py | Fallback has no path or explain commands. |
| GRA-03 | Graph MCP server tools | optional | Check the agent's own tool list (SKILL.md §4). Fallback as above | none (guidance text only) | Name the tool before use; no hosted service without the user asking. |
| GRA-04 | Freshness: incremental update, watch, post-commit hook | rejected | - | none (guidance text only) | Hook/watcher not adopted. Rebuild manually with `ult map build` after big changes (discovery.md §1). |
| GRA-05 | Always-on "query the graph before grep" instruction and read guard | rejected | - | none (guidance text only) | Always-on instruction plus PreToolUse guard. |
| GRA-06 | EXTRACTED / INFERRED / AMBIGUOUS edge confidence | shared | SKILL.md §3 step 1 (confirm relationships in source); context-efficiency.md §4 step 3 (map hits are guesses until opened) | none (guidance text only) | Partial in spirit: no per-edge label, only a blanket "lead, not proof" rule. |
| GRA-07 | Blast radius of a symbol, import cycles, graph diff | native (partial) | `ult refs <name>` (search.py) | unit: test_search.py | Partial: direct word-boundary references only. No transitive walk, cycle detection or graph diff. |
| GRA-08 | Wiki, Obsidian, GraphML, Cypher, call-flow exports | rejected | - | none (guidance text only) | Extras. |
| GRA-09 | Cross-repo graphs, URL/video/audio ingestion, PR impact | rejected | - | none (guidance text only) | Network and out of scope for the core. |
| GRA-10 | Skill installers for ~14 platforms | rejected | - | none (guidance text only) | Claude Code only. |

### serena

Repo `oraios/serena` · revision `6e5c3776d4e6` · license: Mixed: SolidLSP MIT; Serena application GPL-3.0-or-later. Design ideas only; no code or prose reused

Counts: native 2, pending 0, shared 3, optional 7, gap 0, rejected 3 (15 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| SER-01 | Symbol overview of a file | optional | Serena or LSP MCP if in the agent's tool list. Fallback: `ult symbols <name> --path <file>` | unit: test_search.py | Fallback finds definitions by name; there is no per-file overview. |
| SER-02 | find_symbol with name paths, bodies, kinds | optional | Serena/LSP MCP. Fallback: `ult symbols <name>` / `--regex` | unit: test_search.py | Fallback: per-language definition regexes, capped. No name-path syntax. |
| SER-03 | Referencing symbols with snippets | optional | Serena/LSP MCP. Fallback: `ult refs <name>` | unit: test_search.py | Textual, not semantic; dynamic dispatch is invisible. Open each hit. |
| SER-04 | Implementations and declarations | optional | LSP MCP. Fallback: `ult search` + reading source | none (guidance text only) | No dedicated local command. |
| SER-05 | Diagnostics for a file or symbol | optional | LSP MCP. Fallback: run the type checker or linter through `ult run` (tsc and lint families) | unit: test_run.py | Test coverage is for `ult run` generally, not for diagnostics. |
| SER-06 | Symbol-level edits (replace body, insert before/after) | optional | Serena MCP. Fallback: the host's Edit tool (SKILL.md §4) | none (guidance text only) | No local symbol-edit command. |
| SER-07 | Reference-aware rename, safe delete, IDE refactors | optional | Serena/LSP/JetBrains MCP. Fallback: `ult refs` then manual edits with tests | none (guidance text only) | Ultimatum does not adopt Serena's "trust the refactor and skip re-reading" trade; run the checks (SKILL.md §1 rule 1). |
| SER-08 | File tools: read, list, find, regex search, replace, dry-run multi-file replace | shared | Host tools (Read, Grep, Glob, Edit) plus `ult search` | unit: test_search.py | No dry-run multi-file replace. |
| SER-09 | Execute shell command | shared | Host Bash; `ult run` for noisy output | unit: test_run.py | Same as upstream's Claude Code context, which drops it. |
| SER-10 | Project memories with topics and a stale-reference check | native (partial) | `ult note` / `find` / `get`; handoff.md (Cross-session memory) | unit: test_store.py | Partial: no memory graph, rename, or staleness check. Store hits must be re-read against source. |
| SER-11 | Onboarding pass that derives structure and commands | native | discovery.md §1 (orientation pass) and `ult map summary` | unit: test_map.py | Does not write memories automatically; asks before saving a written map (discovery.md §4). |
| SER-12 | Modes: editing, planning (read-only), one-shot, no-memories ... | shared (partial) | Read-only agents (agents/scout.md, agents/reviewer.md, agents/security-hunter.md, agents/security-verifier.md); read-only posture in security/change-review.md | none (guidance text only) | Partial: read-only is a per-agent property, not a switchable mode. |
| SER-13 | Per-host contexts with forceful "Read is forbidden" wording | rejected | - | none (guidance text only) | Overrides host defaults; one host only. |
| SER-14 | Reminder hook that counts non-symbolic reads and denies | rejected | - | none (guidance text only) | Hook-based enforcement; guidance only (context-efficiency.md §4). |
| SER-15 | Project switching, cross-project queries, dashboard, REPL | rejected | - | none (guidance text only) | One project root per run (`ULTIMATUM_ROOT` override exists for tests and worktrees). |

### context7

Repo `upstash/context7` · revision `6e68ffcbad0e` · license: MIT (repository); the documentation index is a hosted service

Counts: native 0, pending 0, shared 0, optional 4, gap 0, rejected 4 (8 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| C7-01 | Resolve a library name to a documentation id | optional | Context7 MCP if in the agent's tool list (`ult doctor` only reminds to check). Fallback: lockfile version, installed package source/types (SKILL.md §4; context-efficiency.md §4 step 5) | none (guidance text only) | Query text goes to a third party, so the tool is named before use. |
| C7-02 | Query current docs and snippets for one concept | optional | Context7 MCP. Fallback: read installed source/types for the locked version; `--help` | none (guidance text only) | Budget: one concept per query, about three calls (context-efficiency.md §4). Answers from memory are labelled unverified when version matters. |
| C7-03 | query-code: grep/read the library source at the docs version | optional | Context7 MCP preview tool, if present. Fallback: `node_modules` / site-packages source | none (guidance text only) | Results are third-party text: data, not instructions. |
| C7-04 | Upgrade guide and docs-feedback tools | optional | Upgrade guide: Context7 MCP if present. Fallback: package changelog and lockfile diff | none (guidance text only) | The feedback-submission tool is not used (writes to a third party). |
| C7-05 | Skills teaching the MCP/CLI flows | rejected | - | none (guidance text only) | Ultimatum's own rule (SKILL.md §4) replaces them; the upstream `find-docs` trigger is intentionally greedy. |
| C7-06 | ctx7 CLI (`npx ctx7@latest ...`) | rejected | - | none (guidance text only) | Runs unpinned remote code on every call. |
| C7-07 | docs-researcher subagent and /context7:docs command | rejected | - | none (guidance text only) | No dedicated docs agent; the main loop queries inline under the call budget. |
| C7-08 | Always-on rule: use Context7 for any library question | rejected | - | none (guidance text only) | Over-triggers. Used only when the version-specific answer matters. |

## Engineering, planning and delivery (research/engineering-delivery.md)

### ponytail

Repo `DietrichGebert/ponytail` · revision `96608e078b2d` · license: MIT

Counts: native 5, pending 0, shared 4, optional 0, gap 3, rejected 2 (14 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| PNT-01 | Always-on "lazy senior dev" mode with lite/full/ultra levels | shared (partial) | SKILL.md §1 rule 3 (reuse first, smallest complete change) | eval 1-one-file (run; baseline arm also passed, so it does not discriminate) | Partial: the principle always applies; there are no levels, no persisted flag and no injection hook. |
| PNT-02 | Reuse-first ladder before writing code | native | discovery.md §3 (reuse-first inventory); SKILL.md §1 rule 3 | eval 2-unfamiliar (defined, not run) grades reuse of existing helpers | The eval grader checks that the diff reuses `format_money` and `outstanding_for` and avoids a legacy decoy. |
| PNT-03 | List every caller, test and config a change must reach | shared (partial) | SKILL.md §3 step 1; discovery.md §3; debugging.md §3 step 4 (`ult refs`) | none (guidance text only) | Partial: no explicit "scope list" artifact. |
| PNT-04 | Bug-fix rule: fix the shared root cause, check all callers | native | debugging.md §3 step 4, §4 | none (guidance text only) |  |
| PNT-05 | Deferral marker comments for known-limit shortcuts | gap | - | none (not implemented) | Reason: no marker convention; Ultimatum avoids adding comment conventions to user code. Closure: a one-line rule in SKILL.md §3 if users ask for it. |
| PNT-06 | Never-cut list (validation, data-loss handling, security, accessibility) | shared (partial) | SKILL.md §2 security overlay trigger list; ui.md §4; production.md §5 | none (guidance text only) | Partial: distributed across references, no single list. |
| PNT-07 | A small test only where branches, parsers, money or security exist | native | tdd.md §1, §4; SKILL.md §3 step 3 | none (guidance text only) | Trivial changes carry no test requirement. |
| PNT-08 | Diff review with a concrete triggering case per finding | native (partial) | agents/reviewer.md; orchestration.md §8 ("a finding needs file:line and a concrete input") | none (guidance text only) | Partial: no fixed ordering lens (correct, safe, scale, tested, fast, lean). |
| PNT-09 | Whole-repo lean audit lens | gap | - | none (not implemented) | Reason: no over-engineering audit route; `discover` and `sec-audit` are different questions. Closure: a short reference that points `ultimatum:reviewer` at a repo scope. |
| PNT-10 | Debt ledger from deferral markers | gap | - | none (not implemented) | Reason: depends on PNT-05 markers. Closure: only if PNT-05 is adopted; release.md §2 step 5 already greps TODO/FIXME the change introduced. |
| PNT-11 | Benchmark scoreboard with an honesty boundary | rejected | - | none (guidance text only) | Ultimatum prints no savings scoreboard; claims need a measured baseline (skill-evaluation.md §6). |
| PNT-12 | Reference card | native (partial) | `ult --help` | unit: test_doctor.py | Partial: toolbelt only. |
| PNT-13 | Re-inject rules into spawned subagents via hook | shared | Rules are restated in each agents/*.md and in the brief template (orchestration.md §3 RULES) | none (guidance text only) | No hook. Agents cannot resolve plugin variables, so SKILL.md tells the manager to pass the substituted `ult` path. |
| PNT-14 | Cross-host packaging with drift checks | rejected | - | none (guidance text only) | Claude Code only. |

### andrej-karpathy-skills

Repo `multica-ai/andrej-karpathy-skills` · revision `2c606141936f` · license: MIT (stated in the README; no LICENSE file at this revision)

Counts: native 0, pending 0, shared 4, optional 0, gap 0, rejected 0 (4 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| KRP-01 | Think before coding: assumptions, interpretations, push back | shared | SKILL.md §1 rule 5; feature-planning.md §2 step 4, §3 | none (guidance text only) | Assumptions are stated in one line; questions only when they change the outcome. |
| KRP-02 | Simplicity first: no speculative features or abstractions | shared | SKILL.md §1 rule 3 | eval 1-one-file (run; baseline arm also passed, so it does not discriminate) |  |
| KRP-03 | Surgical changes: touch only what is needed, report unrelated dead code | shared | SKILL.md §1 rules 3 and 6, §3 step 5; agents/worker.md (ownership, no scope creep) | eval 1-one-file (run; baseline arm also passed, so it does not discriminate) | The grader checks that only the target file changed and no plan document was written. |
| KRP-04 | Goal-driven execution with verifiable steps | shared | SKILL.md §3 step 2 (state the acceptance check); feature-planning.md §6 (success checks) | none (guidance text only) |  |

### skills (Matt Pocock)

Repo `mattpocock/skills` · revision `4ae2317ddb22` · license: MIT

Counts: native 10, pending 0, shared 6, optional 0, gap 6, rejected 3 (25 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| MPC-01 | Requirements interview as a decision tree in rounds | shared (partial) | feature-planning.md §3 (questions batched, defaults attached, ordered by blast radius) | none (guidance text only) | Partial: at most 3 questions per message, no frontier-by-round tree. |
| MPC-02 | grill-me / grill-with-docs variants | shared (partial) | feature-planning.md §3, §4 | none (guidance text only) | Partial: same. |
| MPC-03 | Domain modeling against a glossary | native | feature-planning.md §4 (vocabulary and model) | none (guidance text only) | Does not create a glossary in a repo that has none without asking. |
| MPC-04 | Synthesize a spec without interviewing | native | feature-planning.md §6 | none (guidance text only) | Spec location follows the project; else `.ultimatum/specs/<slug>.md`. |
| MPC-05 | Vertical tracer-bullet tickets with blocking edges | native | feature-planning.md §7 | none (guidance text only) | Remote issues need the user's say-so. |
| MPC-06 | Implement a ticket test-first, then review, then commit | native | tdd.md §1; SKILL.md §3 | none (guidance text only) | Commits only when asked. |
| MPC-07 | Implement a whole spec as a task graph with subagents and worktrees | native | orchestration.md §2-§8 | eval 8-large (defined, not run) grades parallel workers, an integrated review and tests | The grader counts subagent calls and a review-type agent; it does not judge brief quality. |
| MPC-08 | TDD at agreed seams; reject tautological tests | native | tdd.md §1, §4, §6 | none (guidance text only) |  |
| MPC-09 | Diagnose bugs by building a tight feedback loop first | native | debugging.md §1-§3 | eval 3-noisy (defined, not run) grades the fix and quoting of the key failure |  |
| MPC-10 | Two-axis code review in fresh sub-agents (standards, spec) | native | orchestration.md §8; agents/reviewer.md | none (guidance text only) | Run as two separate passes. |
| MPC-11 | PR body with visual summary, evidence, merge danger | gap | - | none (not implemented) | Reason: no PR-writing guide (one-way doors are covered for releases in release.md §4). Closure: a short PR-description section in ci-and-pr.md or release.md. |
| MPC-12 | Issue triage label state machine | gap | - | none (not implemented) | Reason: only PR feedback triage exists (ci-and-pr.md §4). Closure: a triage reference if issue management is wanted. |
| MPC-13 | Agent brief contract on ready-for-agent issues | shared (partial) | orchestration.md §3 (worker brief template) | none (guidance text only) | Partial: covers worker briefs, not issue-comment contracts. |
| MPC-14 | Retro of the agent environment (navigation, checks, standards) | gap | - | none (not implemented) | Reason: no environment retro. Closure: reuse skill-evaluation.md §8 style findings in a short retro route. |
| MPC-15 | Background research against primary sources into a cited note | shared (partial) | discovery.md §2 step 5; `ult note`; `ultimatum:scout` | none (guidance text only) | Partial: no cited-note file contract. |
| MPC-16 | Throwaway prototype answering one question | native | feature-planning.md §5 | none (guidance text only) | Throwaway marker and delete-before-merge rule. |
| MPC-17 | Deep-module vocabulary and architecture improvement | gap | - | none (not implemented) | Reason: no architecture-improvement route (tdd.md §2 only mentions adding a seam). Closure: a reference on module depth and seams. |
| MPC-18 | Wayfinder: map issue plus decision tickets sized to a session | shared (partial) | feature-planning.md §1 (multi-session row), §7; handoff.md | none (guidance text only) | Partial: no map-issue structure. |
| MPC-19 | Generate an interactive bash script for human-only steps | gap | - | none (not implemented) | Reason: not covered. Closure: low priority; add only on demand. |
| MPC-20 | Handoff file for a fresh agent | native | handoff.md; `ult handoff write\|show` | unit: test_handoff.py; eval 9-handoff (defined, not run) | Stored under `.ultimatum/` rather than the OS temp dir; `show` checks HEAD, files and log ids against the repo. |
| MPC-21 | Re-pitch in simple terms; questionnaire builder | gap | - | none (not implemented) | Reason: communication helpers, not covered. Closure: none planned. |
| MPC-22 | Writing-for-agents guidance (pointers, load budgets) | shared (partial) | SKILL.md structure (router plus on-demand references); skill-evaluation.md §1 step 3 | none (guidance text only) | Partial: followed in the plugin's own layout; no standalone guide. |
| MPC-23 | Git guardrail hook blocking push, hard reset, clean, branch -D | rejected | - | none (guidance text only) | Hook not adopted. Rules instead: SKILL.md §1 rule 4, ci-and-pr.md §0 and §6, release.md §0, orchestration.md §7. |
| MPC-24 | Pre-commit setup, tracker config, router, learning skills | rejected | - | none (guidance text only) | Changes project configuration (SKILL.md §1 rule 6). |
| MPC-25 | Misc and learning skills (teach, writing-beats, scaffold-exercises ...) | rejected | - | none (guidance text only) | Out of scope. |

### superpowers

Repo `obra/superpowers` · revision `22f0b463e7a5` · license: MIT

Counts: native 13, pending 0, shared 2, optional 0, gap 2, rejected 1 (18 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| SUP-01 | Skill-gate bootstrap injected at session start ("invoke if 1% applies") | rejected | - | none (guidance text only) | Always-on hook and over-triggering. One router skill with a trigger description. |
| SUP-02 | Brainstorming with a hard gate before building | shared (partial) | feature-planning.md §2, §3, §10 | none (guidance text only) | Partial and deliberate: design happens before code, but there is no hard stop. §10 says not to wait for sign-off beyond the listed stop conditions. |
| SUP-03 | Plans written for an engineer with no context | native (partial) | feature-planning.md §6, §7 | none (guidance text only) | Partial: no verbatim Global Constraints block. |
| SUP-04 | Subagent-driven development controller loop | native | orchestration.md §2, §5-§8 | eval 8-large (defined, not run) | BASE sha, conflict scan, fix rounds, integrated review. |
| SUP-05 | Implementer contract with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT | native | agents/worker.md; orchestration.md §3 | none (guidance text only) | Same four statuses. |
| SUP-06 | Task reviewer that does not trust the implementer's report | native | orchestration.md §6 step 1; agents/reviewer.md | none (guidance text only) |  |
| SUP-07 | Inline plan execution with a single final review | shared | feature-planning.md §7; SKILL.md §3; orchestration.md §8 | none (guidance text only) |  |
| SUP-08 | "Rulings, not stalls" for ambiguity in a running plan | native | feature-planning.md §8; orchestration.md §10 | none (guidance text only) | Rulings carry a cost-if-wrong note and are surfaced in the report. |
| SUP-09 | Parallel agents per independent failure domain | native | orchestration.md §1 | none (guidance text only) |  |
| SUP-10 | Git worktrees with existing-isolation detection | native (partial) | orchestration.md §5 | none (guidance text only) | Partial: no detection of an existing worktree or submodule guard. |
| SUP-11 | Test-driven development with the red failure checked | native | tdd.md §1-§3, §5 | eval 1-one-file (run) (outcome only) | Process is not graded; the grader checks the final tests. |
| SUP-12 | Systematic debugging in four phases | native | debugging.md §1-§5 | none (guidance text only) |  |
| SUP-13 | Verification before completion claims | native | SKILL.md §1 rule 1, §5; tdd.md §3; release.md §2 | none (guidance text only) | The zero-tests-ran warning in `ult run` has no dedicated unit test. |
| SUP-14 | Request code review with BASE/HEAD shas | native | orchestration.md §2 step 4, §8; agents/reviewer.md | none (guidance text only) |  |
| SUP-15 | Receiving review: verify, then implement one item at a time | native | ci-and-pr.md §4, §5 | none (guidance text only) |  |
| SUP-16 | Finishing a branch: tests green, then a fixed set of options | gap | - | none (not implemented) | Reason: release.md covers readiness but not a merge/PR/discard menu; orchestration.md §7 says not to push without authorization. Closure: a short finish-branch section. |
| SUP-17 | TDD for skills: baseline pressure scenarios first | native | skill-evaluation.md §3, §8 | none (guidance text only) | Applies to editing Ultimatum itself. |
| SUP-18 | Forensic review of a past session from transcripts | gap | - | none (not implemented) | Reason: no transcript-forensics route. Closure: out of scope unless requested; eval stream output exists in evals/live/results. |

### plugin-claude (Sentry)

Repo `getsentry/plugin-claude` · revision `1b082a07d1a8` · license: MIT

Counts: native 2, pending 0, shared 0, optional 0, gap 2, rejected 2 (6 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| SPC-01 | Debug a production issue end to end from an error event | native | production.md §1-§7. Sentry MCP or `sentry-cli` if present (`ult doctor` lists sentry-cli); otherwise user-pasted traces | none (guidance text only) | Optional integration with a local path: pasted evidence plus `ult search` on the error string (production.md §9). |
| SPC-02 | Event fields are untrusted input; never paste raw values | native | production.md §0; SKILL.md §1 rule 4 | none (guidance text only) |  |
| SPC-03 | Issue-category awareness (cron/metric monitors have no stack trace) | gap | - | none (not implemented) | Reason: production.md does not mention monitor-type issues. Closure: one paragraph in production.md §1. |
| SPC-04 | Make stack traces readable (source maps, dSYM, ProGuard ...) | gap | - | none (not implemented) | Reason: production.md §2 only says to ask for source maps or the right revision. Closure: a symbolication subsection. |
| SPC-05 | SDK setup and instrumentation across products | rejected | - | none (guidance text only) | Vendor-specific; generic observability fixes are in production.md §5 step 3. |
| SPC-06 | Release tracking, alert creation, OTel collector setup | rejected | - | none (guidance text only) | Vendor-specific; generic release checks are in release.md §7. |

### skills (Sentry)

Repo `getsentry/skills` · revision `e94f22214528` · license: Apache-2.0

Counts: native 6, pending 0, shared 4, optional 1, gap 0, rejected 1 (12 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| SSK-01 | iterate-pr: loop until actionable CI is green and feedback handled | native | ci-and-pr.md §1-§6. `gh` or GitHub MCP if present (`ult doctor` lists gh); else local test run plus workflow file read | none (guidance text only) | Stops on draft, human gates, rebase needs; pushing is user-authorized (§0). |
| SSK-02 | Review-feedback triage by LOGAF markers and heuristics | native | ci-and-pr.md §4 | none (guidance text only) | Low-priority items are listed for the user to choose. |
| SSK-03 | CI failure handling: read the full log, state the cause, fix root cause | native | ci-and-pr.md §3; debugging.md §7 | none (guidance text only) |  |
| SSK-04 | Check-state machine (fix / wait / blocked on human gate) | native | ci-and-pr.md §2 | none (guidance text only) |  |
| SSK-05 | Exit rules (same failure twice, unclear feedback, infra issue) | native | ci-and-pr.md §6 | none (guidance text only) | Max 5 fix-push rounds. |
| SSK-06 | Reply inside review threads (script) | optional | `gh api` or GitHub MCP reply tool if present. Fallback: show the drafted reply text (ci-and-pr.md §5) | none (guidance text only) | Posting needs authorization. |
| SSK-07 | Code-review practices, find-bugs, security-review skills | shared (partial) | agents/reviewer.md; security/change-review.md | none (guidance text only) | Partial: no Sentry-specific practice checklist. |
| SSK-08 | Commit message conventions | shared (partial) | SKILL.md §1 rule 3 (match local style); ci-and-pr.md §3 step 5 (state the cause); debugging.md §9 | none (guidance text only) | Partial: no format spec. |
| SSK-09 | Worker brief with ownership boundary and validation commands | native | orchestration.md §3 | none (guidance text only) |  |
| SSK-10 | Specialist reviews, e.g. Django performance with validated findings only | shared (partial) | data-and-infra.md §2 (N+1, indexes, pagination); orchestration.md §8 (zero findings is valid) | none (guidance text only) | Partial: framework-neutral. |
| SSK-11 | Skill meta: skill-writer, agents-md, settings audit | shared (partial) | skill-evaluation.md §1 (static gates) | none (guidance text only) | Partial: no AGENTS.md size guide or settings audit. |
| SSK-12 | Archive-only frontend issue queue cleanup | rejected | - | none (guidance text only) | Acts on an external system's queue. |

### gstack

Repo `garrytan/gstack` · revision `7dace1fdeabc` · license: MIT

Counts: native 4, pending 0, shared 7, optional 0, gap 2, rejected 3 (16 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| GST-01 | /ship: merge base, tests, reviews, version bump, changelog, PR | native (partial) | release.md §1-§8 | none (guidance text only) | Partial: prepares and checks; publishing is the user's decision (§0). |
| GST-02 | Verification gate with evidence receipts | shared | SKILL.md §1 rule 1 and §5 (Verified line); release.md §8 | none (guidance text only) | No receipt-reuse scheme. |
| GST-03 | /verify with PASS / FAIL / UNMAPPED / ZERO_RUN verdicts | native | tdd.md §3; release.md §2 step 2; `ult run` prints a zero-tests warning | unit: test_run.py | ZERO_RUN detection is in run.py but not asserted by a dedicated test. |
| GST-04 | Pre-landing review with critical and informational passes | shared | agents/reviewer.md; orchestration.md §8; security/change-review.md §2-§3 | none (guidance text only) |  |
| GST-05 | Gate-integrity review: loosened tests, thresholds, CI | native | ci-and-pr.md §3 (never weaken a gate); release.md §2 step 3; agents/reviewer.md | none (guidance text only) |  |
| GST-06 | /qa test-fix-verify with tiered scope | shared (partial) | browser-verification.md; ui.md §9 (critique gate, 3 rounds) | eval 4-ui (defined, not run) grades real-browser use at two widths | Partial: no clean-tree gate or severity tiers. |
| GST-07 | /canary post-deploy monitor | native (partial) | release.md §7; production.md §6 | none (guidance text only) | Partial: checklist, no screenshot baseline monitor. |
| GST-08 | Safety hooks (/careful, /freeze) | rejected | - | none (guidance text only) | Hooks not adopted; authorization rules in text. |
| GST-09 | /spec interrogation gate before an issue | shared | feature-planning.md §2, §3, §6 | none (guidance text only) |  |
| GST-10 | /modernize: revalidate an old PR as a claim | gap | - | none (not implemented) | Reason: not covered. Closure: a short stale-PR revalidation section in ci-and-pr.md. |
| GST-11 | /captain: controller over parallel PR lanes with READY blocks | shared (partial) | orchestration.md §6-§8 | none (guidance text only) | Partial: single integration branch only. |
| GST-12 | Planning reviews (office-hours, CEO/eng review personas) | shared (partial) | feature-planning.md §2 step 4 (cheaper path), §6 (self-check) | none (guidance text only) | Partial: no persona reviews. |
| GST-13 | /health weighted code-quality score | gap | - | none (not implemented) | Reason: no composite score. Closure: not planned; the optimization loop can track any metric the user names. |
| GST-14 | Docs and memory: release docs, context save/restore, learnings, retro | shared (partial) | release.md §3; handoff.md; `ult note` | unit: test_handoff.py, test_store.py | Partial: no weekly git-metrics retro. |
| GST-15 | Browser and design commands, cookie import, pairing | rejected | - | none (guidance text only) | Persistent browser daemon and cookie import not adopted. See `ult-browser.mjs` (PWC rows). |
| GST-16 | Second-opinion wrappers, remote runs, telemetry opt-in | rejected | - | none (guidance text only) | Sends code to third parties and adds telemetry. |

### agent-skills (Supabase)

Repo `supabase/agent-skills` · revision `c9be0e931b79` · license: MIT

Counts: native 4, pending 0, shared 2, optional 1, gap 0, rejected 0 (7 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| SBA-01 | Verify against live product docs; verify after fixing with a query | optional | Supabase MCP or `supabase` CLI if present (`ult doctor` lists supabase). Fallback: files and a local database (data-and-infra.md §0 step 4, §6) | none (guidance text only) | Read-only operations by default; stop retrying after 2-3 attempts. |
| SBA-02 | Security checklist of silent traps | native | data-and-infra.md §3 (11 RLS checks) | none (guidance text only) | No RLS fixture exists, so no eval case exercises it. |
| SBA-03 | RLS and grants are separate; enable RLS on exposed tables | native | data-and-infra.md §3 check 1 | none (guidance text only) |  |
| SBA-04 | Schema change workflow: migrations, advisors, lint before commit | native | data-and-infra.md §1, §6 | none (guidance text only) | Never applies migrations to shared environments without authorization (§0). |
| SBA-05 | Fetch the debugging doc before diagnosing | shared | data-and-infra.md §6 (last bullet: read the error and the docs for the installed version) | none (guidance text only) |  |
| SBA-06 | Postgres best-practice rule set (8 categories) | native (partial) | data-and-infra.md §1 step 4, §2, §3 | none (guidance text only) | Partial: queries, locks, indexes, RLS. Connection pooling and monitoring are brief. |
| SBA-07 | Scoped tokens for CLI, MCP and CI | shared (partial) | security/secure-implementation.md §6 (Secrets; LLM / agent tools: least privilege) | none (guidance text only) | Partial: no Supabase-token-specific guidance. |

### agent-skills (HashiCorp)

Repo `hashicorp/agent-skills` · revision `5e30fa5c867b` · license: MPL-2.0 (ideas only; no text reused)

Counts: native 3, pending 0, shared 0, optional 0, gap 0, rejected 5 (8 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| HCP-01 | terraform-test: plan-mode vs apply-mode tests, mocks, timeouts | native | data-and-infra.md §4 step 2 | none (guidance text only) | Optional `terraform` CLI (listed by `ult doctor`). Apply-mode tests need an authorized test account. |
| HCP-02 | Module refactoring: coupling analysis, typed interfaces, moved blocks | native (partial) | data-and-infra.md §4 step 6 | none (guidance text only) | Partial. |
| HCP-03 | Style guide: file layout, version constraints, naming | native (partial) | data-and-infra.md §4 step 1 | none (guidance text only) | Partial. |
| HCP-04 | Provider acceptance tests (TestAcc, TF_ACC, timeouts) | rejected | - | none (guidance text only) | Provider authoring is a specialist domain; ideas only and no tooling. |
| HCP-05 | Provider test patterns (lifecycle, sweepers, import) | rejected | - | none (guidance text only) | Same. |
| HCP-06 | Provider configuration patterns | rejected | - | none (guidance text only) | Same. |
| HCP-07 | Provider/resource/action authoring, policy tests, stacks | rejected | - | none (guidance text only) | Same. |
| HCP-08 | Repo hygiene scripts (structure validation, link check) | rejected | - | none (guidance text only) | Maintainer tooling; Ultimatum's own gates are in skill-evaluation.md §1. |

### autoresearch

Repo `uditgoenka/autoresearch` · revision `7bddd056dfd0` · license: MIT

Counts: native 4, pending 0, shared 4, optional 0, gap 0, rejected 1 (9 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| ARS-01 | Goal / scope / metric / verify / guard loop with baseline | native | optimization-loop.md §1-§2 | none (guidance text only) | Ledger at `.ultimatum/opt/<name>.tsv`. |
| ARS-02 | Behavior-preserving optimization: acceptance separate from search metric | native | optimization-loop.md §4 | none (guidance text only) | Held-out and adversarial inputs. |
| ARS-03 | Fork-and-flush cadence | native (partial) | optimization-loop.md §3 (plateau reset from ledger and best commit) | none (guidance text only) | Partial: no scheduled flush. |
| ARS-04 | Free-text goal to pinned success predicate, one confirmation | native (partial) | optimization-loop.md §1 steps 1-3 | none (guidance text only) | Partial: no archetype classifier. |
| ARS-05 | Screen derived shell strings for destructive patterns | shared (partial) | optimization-loop.md §1 step 7 | none (guidance text only) | Partial and honest: an instruction to screen, not a screening tool. |
| ARS-06 | Regression gate: green-to-red only, classified before diff | shared (partial) | optimization-loop.md §2 step 5; skill-evaluation.md §5 | none (guidance text only) | Partial: classification table applies to evals of Ultimatum. |
| ARS-07 | fix / debug / security / ship loop variants | shared | debugging.md; security/full-audit.md; release.md; optimization-loop.md (metric = error count) | none (guidance text only) |  |
| ARS-08 | Hooks: scout-block, privacy-block, dangerous-command block | rejected | - | none (guidance text only) | Hooks not adopted. |
| ARS-09 | Handoff JSON between chained subcommands | shared (partial) | `.ultimatum/security/` findings and ledger JSON; handoff.md | none (guidance text only) | Partial: JSON exists for security artifacts only. |

### skills (Anthropic): skill-creator

Repo `anthropics/skills` · revision `2c5958ecac7c` · license: Per-skill license; skill-creator's `LICENSE.txt` is Apache-2.0 (no repo-level LICENSE file)

Counts: native 4, pending 0, shared 0, optional 0, gap 4, rejected 0 (8 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| SKC-01 | Skill authoring loop with realistic test prompts | native | skill-evaluation.md §3, §8 | none (guidance text only) |  |
| SKC-02 | With-skill vs baseline runs launched together | native | evals/live/run_live.py; skill-evaluation.md §2 | harness only: ran for 1 case (evals/live/results/smoke-1) | Both arms share settings and an isolated config dir. Only 1-one-file has a recorded result. |
| SKC-03 | Grader reads transcript and outputs, with evidence | native (partial) | evals/live/run_live.py graders; skill-evaluation.md §3 | none (guidance text only) | Partial: graders are deterministic Python checks against fixture answer keys, not transcript-reading LLM graders. |
| SKC-04 | Benchmark aggregation: mean, stddev, delta | gap | - | none (not implemented) | Reason: run_live.py writes per-run summaries; skill-evaluation.md §4 describes mean ± stdev, but no script aggregates. Closure: an aggregation script over summary.json. |
| SKC-05 | Blind A/B comparison and unblinding analysis | gap | - | none (not implemented) | Reason: not built. Closure: add only if rubric-style outputs need comparison. |
| SKC-06 | Trigger evals and description optimization | gap | - | none (not implemented) | Reason: skill-evaluation.md §1 step 6 and §3 near-miss negatives are guidance; no trigger runner exists. Closure: a small `claude -p` trigger harness. |
| SKC-07 | Static validation of frontmatter keys | native | skill-evaluation.md §1 (`claude plugin validate`) | none (guidance text only) | Delegates to the host CLI. |
| SKC-08 | Human review viewer with per-case feedback | gap | - | none (not implemented) | Reason: not built. Closure: low priority. |

## UI, design engineering and browser verification (research/ui-browser.md)

### taste-skill

Repo `Leonxlnx/taste-skill` · revision `f6b76575f949` · license: MIT

Counts: native 7, pending 0, shared 2, optional 0, gap 0, rejected 6 (15 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| TST-01 | Business-kind classification that drives the whole page plan | rejected | - | none (guidance text only) | Replaced by surface-mode classification (ui.md §2), which classifies the requested surface instead of the product category. |
| TST-02 | Nine house rules (4 widths, one section per screen, equal edges, hover ...) | shared (partial) | ui.md §4 (craft floor); browser-verification.md §2 | none (guidance text only) | Partial: no image-caption, real-photo or hover micro-animation rules. |
| TST-03 | Deterministic dealing of hero, palette, type, nav, with history files | rejected | - | none (guidance text only) | Randomized dealing not adopted. A direction card with a reason per choice and a "do not repeat the last palette" rule instead (ui.md §3). |
| TST-04 | Copy layer: fact sheet, voice card, banned words | native (partial) | ui.md §4 (copy), §6 (filler words and stock lines) | none (guidance text only) | Partial: no fact-sheet or voice-card artifacts. |
| TST-05 | Page plan by screens | shared (partial) | ui.md §2 (Persuade surfaces: one idea per screen) | none (guidance text only) | Partial. |
| TST-06 | Photography sourcing with credits | rejected | - | none (guidance text only) | Needs external image services. ui.md §1 rule 6 requires real content and marking assumed values. |
| TST-07 | Real product/tool icons as local files | rejected | - | none (guidance text only) | Not adopted; ui.md §6 only warns against emoji standing in for icons. |
| TST-08 | Shader effects, scenes, print renders (tech-only) | rejected | - | none (guidance text only) | Decorative effects out of scope. |
| TST-09 | Motion layer: one entrance, dealt moments, reduced motion, no scroll reveals | native | ui.md §5 | none (guidance text only) | "One authored moment per surface"; reduced-motion handling (step 9). |
| TST-10 | Performance budget table with WARN/FAIL numbers | native (partial) | browser-verification.md §10 (LCP, CLS budgets); react.md §D | none (guidance text only) | Partial: two budget numbers, no table. |
| TST-11 | Multi-width layout and consistency checker | native (partial) | scripts/ult-browser.mjs (`h-overflow`, `element-overflow`, `tap-target-*`, `--stress`, per viewport) | unit: test_browser.py (needs node + Playwright); eval 4-ui (defined, not run) | Partial: no hero-fit or section-height rules. Tested ids: h-overflow, tap-target-small, stress-overflow. |
| TST-12 | Screenshot at a chosen size, "still loading" detection | native (partial) | scripts/ult-browser.mjs (load screenshot per viewport); browser-verification.md §5 | unit: test_browser.py (needs node + Playwright) | Partial: screenshots are taken; reading them back is a manual duty. No still-loading detection. |
| TST-13 | Finish gate with bounded rounds and a waivers file | native | ui.md §9 (3 rounds, WAIVE line format) | none (guidance text only) | No Stop hook; the bound is a rule. |
| TST-14 | Report format with a GATE line first | native (partial) | ui.md §9 last paragraph; browser-verification.md §12 (`ULT-BROWSER:` line verbatim) | unit: test_browser.py (needs node + Playwright) | Partial. |
| TST-15 | Reusable UI fragments for software pages | rejected | - | none (guidance text only) | Ultimatum reuses the project's own components (ui.md §1). |

### impeccable

Repo `pbakaus/impeccable` · revision `3c5e75fa07be` · license: Apache-2.0

Counts: native 10, pending 0, shared 6, optional 0, gap 1, rejected 7 (24 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| IMP-01 | Load PRODUCT.md, DESIGN.md and surface brief once per session | native (partial) | ui.md §1 (design context docs, tokens, existing screens) | eval 4-ui (defined, not run) grades reuse of the project's dialog, toast and button | Partial: read on demand, not injected by a hook. |
| IMP-02 | Mode model: Persuade / Operate / Read / Experience | native | ui.md §2 | none (guidance text only) |  |
| IMP-03 | Craft floor applied before editing | native | ui.md §4, §6 | none (guidance text only) |  |
| IMP-04 | Shape: plan UX before code | shared | ui.md §3 (direction card); feature-planning.md | none (guidance text only) |  |
| IMP-05 | init writes PRODUCT.md | rejected | - | none (guidance text only) | Does not create tracked doc files unprompted (feature-planning.md §6, SKILL.md §1 rule 6). |
| IMP-06 | document: generate DESIGN.md from code | gap | - | none (not implemented) | Reason: ui.md reads an existing DESIGN.md but has no procedure to derive one. Closure: a token/component extraction procedure that asks before adding a tracked file. |
| IMP-07 | extract: consolidate repeated parts (3+ uses) | native | ui.md §1 rule 3 | none (guidance text only) |  |
| IMP-08 | critique: heuristic review with isolated judgement and detector passes | native (partial) | ui.md §7 (last paragraph), §9 | none (guidance text only) | Partial: the split is advised when a subagent is available; no UI-specific agent. |
| IMP-09 | audit: five dimensions scored 0-4 with P0-P3 | native | ui.md §7 | none (guidance text only) | Own wording, same five dimensions. |
| IMP-10 | polish: classify drift and fix at the narrowest level | shared (partial) | ui.md §1 rules 1-2 | none (guidance text only) | Partial. |
| IMP-11 | bolder / quieter / distill | rejected | - | none (guidance text only) | Not adopted as commands. |
| IMP-12 | harden: extreme inputs, errors, i18n, long text | native | ui.md §4 (long and odd content); browser-verification.md §8 | unit: test_browser.py (needs node + Playwright) (stress-overflow) |  |
| IMP-13 | onboard: first-run and empty states | shared (partial) | ui.md §4 (states: empty, error) | none (guidance text only) | Partial: no onboarding flow guidance. |
| IMP-14 | animate: motion thesis and property choice | native | ui.md §5 | none (guidance text only) |  |
| IMP-15 | colorize / typeset / layout with judgement then detector scan | shared | ui.md §4, §7; `ult-browser` as the mechanical pass | none (guidance text only) |  |
| IMP-16 | delight / overdrive | rejected | - | none (guidance text only) | Not adopted. |
| IMP-17 | clarify copy; adapt responsive; optimize UI performance | shared | ui.md §4 (copy); browser-verification.md §2, §10 | none (guidance text only) |  |
| IMP-18 | live: select an element and hot-swap generated variants through HMR | rejected | - | none (guidance text only) | Dev-server integration not adopted. |
| IMP-19 | Design detector CLI with JSON and scope options | native (partial) | scripts/ult-browser.mjs (`--viewports`, `--stress`, `--reduced-motion`, `report.json`) | unit: test_browser.py (needs node + Playwright) | Partial: a fixed check set, not a design-rule detector. |
| IMP-20 | Detector rule catalog (~60 named rules) | native (partial) | scripts/ult-browser.mjs audit ids: contrast, tiny-text, img-alt, accessible-name, lang, title, duplicate-id, heading-order, h1-*, tap-target-* | unit: test_browser.py (needs node + Playwright) (img-alt, accessible-name, h-overflow, lang, title, duplicate-id, tap-target-small asserted) | Partial: about 15 mechanical checks. Anti-generic tells (ui.md §6) are prose, not detected. |
| IMP-21 | Post-edit design hook running the detector | rejected | - | none (guidance text only) | Hook not adopted; the check is run at the critique gate (ui.md §9). |
| IMP-22 | doctor: repair PRODUCT/DESIGN/config drift | rejected | - | none (guidance text only) | `ult doctor` only lists CLI tools and changes nothing. |
| IMP-23 | Plugin sub-agents: finish-reviewer, documenter, asset-producer ... | shared (partial) | agents/reviewer.md | none (guidance text only) | Partial: only the reviewer exists. |
| IMP-24 | Browser overlay and editor extension | rejected | - | none (guidance text only) | Out of scope. |

### skills (Emil Kowalski)

Repo `emilkowalski/skills` · revision `715c1807e08c` · license: MIT

Counts: native 6, pending 0, shared 4, optional 0, gap 4, rejected 2 (16 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| EML-01 | Design-engineering philosophy and animation decision framework | native | ui.md §5 | none (guidance text only) | Frequency, purpose, easing, duration, physicality, interruptibility, performance. |
| EML-02 | Animate in decision order | native | ui.md §5 | none (guidance text only) |  |
| EML-03 | Review animations with exact values | native | ui.md §5 last paragraph (Before \| After \| Why table) | none (guidance text only) |  |
| EML-04 | Read-only audit producing plans for other agents | shared (partial) | ui.md §7 (audit is findings only) | none (guidance text only) | Partial: no plan template. |
| EML-05 | Find places that should animate | gap | - | none (not implemented) | Reason: not covered. Closure: low value; ui.md §5 steps 1-2 can be applied on request. |
| EML-06 | Remove animations (subtract-only) | shared (partial) | ui.md §5 steps 1-2 (no animation for high-frequency use) | none (guidance text only) | Partial: no subtract-only mode. |
| EML-07 | Animation performance: composite-only properties, per-frame state | native | ui.md §5 step 7; react.md §E step 10, §F step 4 | none (guidance text only) |  |
| EML-08 | Choreography recipes: staggers, entrances, morphs | gap | - | none (not implemented) | Reason: ui.md allows one authored moment and view transitions only. Closure: a short recipes reference if heavy motion work is common. |
| EML-09 | Gestures: finger tracking, interruptible drag and sheets | gap | - | none (not implemented) | Reason: only a pointer-tracking note exists (ui.md §5 step 6). Closure: gesture reference. |
| EML-10 | Apple-style spring motion and materials | gap | - | none (not implemented) | Reason: not covered. Closure: low priority. |
| EML-11 | Animation vocabulary glossary | rejected | - | none (guidance text only) | Not adopted. |
| EML-12 | break-ui: worst-case data behind a toggle | native (partial) | scripts/ult-browser.mjs `--stress`; browser-verification.md §8; ui.md §4 | unit: test_browser.py (needs node + Playwright) (stress-overflow) | Partial: no in-app demo-data toggle is built. |
| EML-13 | Mobile-native feel fixes (100vh, input zoom, safe area, hover) | native (partial) | ui.md §4 (100dvh, 16px inputs, hover media, touch targets); react.md §I | none (guidance text only) | Partial: no sticky-hover or tap-highlight rules. |
| EML-14 | Prototype N versions behind a picker; library picks; toast library | shared (partial) | feature-planning.md §5 (prototype); ui.md §1 rule 5 | none (guidance text only) | Partial: no live picker or curated library list. |
| EML-15 | Native/mobile animation skills (Expo, Swift) | rejected | - | none (guidance text only) | Out of scope; react.md §I has short React Native notes only. |
| EML-16 | UI and performance cheatsheets | shared | ui.md §4-§5; react.md | none (guidance text only) |  |

### ui (shadcn skill)

Repo `shadcn-ui/ui` · revision `8ab27715521c` · license: MIT

Counts: native 1, pending 0, shared 1, optional 1, gap 0, rejected 8 (11 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| SHD-01 | Project-aware context from `shadcn info --json` | optional | `components.json` presence signals a shadcn project; read it and list the ui directory. `npx shadcn ...` only after the user agrees (ui.md §1 rule 5). Fallback: read files | none (guidance text only) | `ult doctor` does not list shadcn. |
| SHD-02 | Reuse-first workflow: installed, search registry, docs, view, add | native (partial) | ui.md §1 rule 5 | none (guidance text only) | Partial: compose from installed components; adding downloads code and needs approval. |
| SHD-03 | Critical styling and composition rules with incorrect/correct pairs | shared (partial) | ui.md §1 (tokens before literals, reuse); react.md §A | none (guidance text only) | Partial: no shadcn-specific rule pairs. |
| SHD-04 | Preset switching protocol | rejected | - | none (guidance text only) | shadcn-specific tooling. |
| SHD-05 | Design system from DESIGN.md | rejected | - | none (guidance text only) | Same. |
| SHD-06 | Showcase coverage script | rejected | - | none (guidance text only) | Same. |
| SHD-07 | Registry authoring | rejected | - | none (guidance text only) | Same. |
| SHD-08 | shadcn MCP server | rejected | - | none (guidance text only) | Not referenced by Ultimatum; files plus a user-approved CLI are used. |
| SHD-09 | Radix-to-base migration skill | rejected | - | none (guidance text only) | Library-specific. |
| SHD-10 | Evals: eight UI prompts | rejected | - | none (guidance text only) | Ultimatum's own UI check is eval 4-ui against fixtures/ui-app. |
| SHD-11 | Docs page for installing the skill | rejected | - | none (guidance text only) | Not applicable. |

### agent-skills (Vercel)

Repo `vercel-labs/agent-skills` · revision `1a2c79d4e6c4` · license: MIT (README and skill frontmatter; no LICENSE file at this revision)

Counts: native 4, pending 0, shared 1, optional 0, gap 0, rejected 4 (9 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| VCL-01 | React best practices (70 rules, 8 priority categories) | native | react.md §A-§F | none (guidance text only) | Condensed, original rules ordered by usual payoff. Not a rule-by-rule port. |
| VCL-02 | Composition patterns: compound components, avoid boolean props | native | react.md §A | none (guidance text only) |  |
| VCL-03 | Review files against a remotely fetched web-interface guideline | rejected | - | none (guidance text only) | Fetching a guideline at runtime is network use. ui.md §4 holds the local floor. |
| VCL-04 | View transitions | native | react.md §G | none (guidance text only) | Check the installed React/Next version first. |
| VCL-05 | React Native rules | native (partial) | react.md §I | none (guidance text only) | Partial: short notes. |
| VCL-06 | Deploy to Vercel | rejected | - | none (guidance text only) | Vendor deploy. Deploys need explicit authorization (release.md §0). |
| VCL-07 | Vercel CLI with tokens | rejected | - | none (guidance text only) | Generic token handling: SKILL.md §1 rule 4, data-and-infra.md §0 step 2. |
| VCL-08 | Metrics-first cost/performance audit with gates | shared | optimization-loop.md §1, §7; react.md §D step 5 | none (guidance text only) |  |
| VCL-09 | Review prose against a fetched writing handbook | rejected | - | none (guidance text only) | Runtime fetch; out of scope. |

### playwright-cli

Repo `microsoft/playwright-cli` · revision `9166133dd68a` · license: Apache-2.0

Counts: native 5, pending 0, shared 3, optional 0, gap 5, rejected 4 (17 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| PWC-01 | Snapshot and ref model (YAML accessibility snapshot, element refs) | gap | - | none (not implemented) | Reason: ult-browser uses CSS selectors and does not emit an accessibility snapshot. Closure: optionally add a snapshot dump or detect and use the upstream CLI when installed. |
| PWC-02 | Interaction commands (click, fill, type, hover, select, drag ...) | native (partial) | scripts/ult-browser.mjs `--steps` file: click, press, fill, wait, screenshot, expect (browser-verification.md §1) | unit: test_browser.py (needs node + Playwright) (steps and a failed expect tested) | Partial: no hover, select, check, drag, upload or double-click steps. Anything else: a custom Playwright snippet. |
| PWC-03 | Snapshot options and find | gap | - | none (not implemented) | Reason: depends on PWC-01. Closure: same. |
| PWC-04 | eval / run-code for arbitrary page code | shared | browser-verification.md §9, §10 (Playwright library snippets run with `node`) | none (guidance text only) |  |
| PWC-05 | Screenshots and PDF | native (partial) | scripts/ult-browser.mjs (full-page PNG per viewport and per `screenshot` step) | unit: test_browser.py (needs node + Playwright) | Partial: no PDF, no element screenshots. |
| PWC-06 | Tabs, named sessions, persistent profile | gap | - | none (not implemented) | Reason: each viewport uses a fresh context. Closure: not needed for verification; add only if login-flow checks require it. |
| PWC-07 | Storage state and cookie/localStorage commands | shared | browser-verification.md §9 (snippet; never print values) | none (guidance text only) |  |
| PWC-08 | Emulation: color scheme, reduced motion, forced colors, contrast, print | native (partial) | scripts/ult-browser.mjs `--viewports`, `--reduced-motion` | unit: test_browser.py (needs node + Playwright) (viewports tested; `--reduced-motion` not asserted) | Partial: no color-scheme, forced-colors or print emulation. |
| PWC-09 | Network mocking and request inspection | shared (partial) | browser-verification.md §8 (Playwright `route` snippet); ult-browser lists failed requests and blocks off-origin requests | unit: test_browser.py (needs node + Playwright) (external blocking asserted) | Partial: no mocking command. |
| PWC-10 | Console output | native | scripts/ult-browser.mjs (`console-error`, `page-error`, `request-failed`, `http-error` are FAIL; browser-verification.md §6) | none specific (test_browser.py does not assert console-error) | Capturing is in the script; no test asserts the console-error id. |
| PWC-11 | Tracing and video recording | gap | - | none (not implemented) | Reason: not provided. Closure: optional flag to write a Playwright trace. |
| PWC-12 | show --annotate dashboard for human feedback | rejected | - | none (guidance text only) | Interactive human-in-the-loop UI; out of scope. |
| PWC-13 | highlight and generate-locator | gap | - | none (not implemented) | Reason: not provided. Closure: low priority. |
| PWC-14 | WebMCP page tools | rejected | - | none (guidance text only) | Page-registered tools are untrusted input; not used. |
| PWC-15 | --raw and --json output modes | native | scripts/ult-browser.mjs writes `<out>/report.json` and a final `ULT-BROWSER:` line | unit: test_browser.py (needs node + Playwright) | The tests parse report.json. |
| PWC-16 | Attach screenshots/video to PRs via `gh` | rejected | - | none (guidance text only) | Posting to a PR needs authorization (ci-and-pr.md §0). Artifacts stay in `.ultimatum/browser/`. |
| PWC-17 | Skill install/update check against npm | rejected | - | none (guidance text only) | Network check not adopted. |

### axe-core

Repo `dequelabs/axe-core` · revision `c50bf8e8933e` · license: MPL-2.0 (invoked, never vendored)

Counts: native 1, pending 0, shared 2, optional 2, gap 2, rejected 1 (8 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| AXE-01 | axe.run returning violations / passes / incomplete | optional | scripts/ult-browser.mjs `--axe auto\|path\|off`: looks at `ULT_AXE_PATH`, `require.resolve('axe-core')`, the project, then global npm root; never downloads. `ult doctor` lists axe-core. Fallback: built-in DOM checks | unit: test_browser.py (needs node + Playwright) (asserts the report names engine axe-core or fallback; the axe-present path runs only if axe is installed) | Report states the engine. Say "axe not available; fallback coverage only" when it is not used (browser-verification.md §1). |
| AXE-02 | Rule and tag selection (wcag2a, wcag22aa, best-practice ...) | gap | - | none (not implemented) | Reason: the script runs axe with its defaults. Closure: pass a `runOnly` tag option through a flag. |
| AXE-03 | Result item shape (id, impact, nodes, help) | optional | scripts/ult-browser.mjs maps each violation to `axe:<rule id>` with up to 5 nodes | none (guidance text only) | Uses a subset of fields. |
| AXE-04 | Incomplete (needs review) results | gap | - | none (not implemented) | Reason: only violations are reported; incomplete results are dropped. Closure: report incomplete counts as WARN. |
| AXE-05 | Impact semantics (minor ... critical) | native | scripts/ult-browser.mjs (critical/serious = FAIL, others WARN); browser-verification.md §7 | none (guidance text only) |  |
| AXE-06 | Rule count and coverage claims | shared | browser-verification.md §7 (automated tools find a limited share; manual criteria added) | none (guidance text only) | No coverage percentage is claimed. |
| AXE-07 | Accessibility-supported policy (AT/browser combinations) | shared (partial) | browser-verification.md §7, §12 (screen reader listed under not verified) | none (guidance text only) | Partial: no AT matrix. |
| AXE-08 | Custom rules, plugins, locales | rejected | - | none (guidance text only) | Not needed. |

### chrome-devtools-mcp

Repo `ChromeDevTools/chrome-devtools-mcp` · revision `6b056c848a98` · license: Apache-2.0

Counts: native 0, pending 0, shared 2, optional 7, gap 0, rejected 2 (11 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| CDM-01 | Input automation tools (click, fill, drag, upload ...) | optional | Chrome DevTools MCP if in the agent's tool list. Fallback: `ult-browser.mjs --steps` or a Playwright snippet | unit: test_browser.py (needs node + Playwright) (fallback) | Name the tool before using it (SKILL.md §4). |
| CDM-02 | Navigation and page management | optional | Chrome DevTools MCP. Fallback: `ult-browser.mjs <url>` | unit: test_browser.py (needs node + Playwright) (fallback) |  |
| CDM-03 | Emulation: viewport, network, CPU throttling, color scheme | optional | Chrome DevTools MCP. Fallback: `--viewports`, `--reduced-motion` | unit: test_browser.py (needs node + Playwright) (fallback) | No throttling in the fallback. |
| CDM-04 | Performance traces and insight analysis | optional | `performance_start_trace` / `performance_stop_trace` / `performance_analyze_insight` named in browser-verification.md §10. Fallback: PerformanceObserver snippet (LCP, CLS) | none (guidance text only) |  |
| CDM-05 | List and inspect network requests | optional | Chrome DevTools MCP. Fallback: ult-browser failed-request and HTTP 4xx/5xx findings | unit: test_browser.py (needs node + Playwright) (fallback partly) |  |
| CDM-06 | Debugging: evaluate script, console messages, screenshots, Lighthouse | optional | Chrome DevTools MCP (`lighthouse_audit` named in §10). Fallback: ult-browser console capture | unit: test_browser.py (needs node + Playwright) (fallback partly) |  |
| CDM-07 | Heap snapshots and memory analysis | optional | `take_memory_snapshot` named in browser-verification.md §10. Fallback: repeat-and-compare DOM-node/heap snippet | none (guidance text only) |  |
| CDM-08 | Extensions, third-party tools, WebMCP, PWA, WebAuthn tools | rejected | - | none (guidance text only) | Not used. |
| CDM-09 | Cookies and storage through script evaluation | shared | browser-verification.md §9 | none (guidance text only) |  |
| CDM-10 | Bundled skills (a11y debugging, LCP, memory leaks, ...) | shared (partial) | browser-verification.md §4, §7, §10 | none (guidance text only) | Partial: manual criteria lists, not the upstream skills. |
| CDM-11 | CLI mode and slim mode | rejected | - | none (guidance text only) | Not used. |

## Security and test depth (research/security.md)

### security-audit-skill (Cloudflare)

Repo `cloudflare/security-audit-skill` · revision `c1c8a8c14710` · license: MIT

Counts: native 20, pending 0, shared 0, optional 0, gap 2, rejected 0 (22 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| CF-01 | Guidance mode vs full-audit mode chosen from the request | native | SKILL.md §2 (routes sec-review, sec-audit, sec-fix plus the secure-implementation overlay); security/full-audit.md opening line | none (guidance text only) | Full audit only when the user asks for an audit. |
| CF-02 | Execution safety: source read-only, target code only in a sandbox | native (partial) | security/full-audit.md §0 (active testing not authorized by default), §9; agents/security-hunter.md and agents/security-verifier.md (read-only) | none (guidance text only) | Partial and honest: no OS sandbox. Rule is not to run target code at all unless the user agrees to the project's own tests or a local fixture. |
| CF-03 | Run directory and write isolation | native (partial) | security/full-audit.md (outputs in `.ultimatum/security/`); hunters have no Write/Edit tools; manager records via `ult findings add` | none (guidance text only) | Partial: no descriptor promotion or per-agent scratch dirs. |
| CF-04 | Reconnaissance by four parallel read-only agents | native (partial) | security/full-audit.md §1-§2 (manager runs `ult map`, `ult scan`, builds a trust-boundary map) | unit: test_map.py, test_scan.py | Partial: done by the manager, no recon agents. |
| CF-05 | Deterministic coverage ledger | native (partial) | `ult findings ledger init\|mark\|check` (findings.py `PRESETS`); security/full-audit.md §3; schemas/coverage-ledger.schema.json | unit: test_findings.py; eval 6-audit (defined, not run) grades that coverage is recorded | Partial: one item per audit area (18 audit, 5 review), not a surface × boundary × subsystem × attack-class matrix. `check` fails on open or evidence-less items. |
| CF-06 | Run profiles quick / standard / deep and scoped runs | native | security/full-audit.md §4; `ult findings ledger init --profile --scope`; review preset for diffs | unit: test_findings.py |  |
| CF-07 | Cost budget in agent invocations | native | security/full-audit.md §4 (reserve verifiers before hunters) | none (guidance text only) |  |
| CF-08 | Prior-run reuse with carried and revalidated findings | gap | - | none (not implemented) | Reason: findings.md §2 keeps rejected items so they are not rediscovered, and fingerprints must be unique, but no re-run procedure exists. Closure: a re-run section in full-audit.md (carry confirmed items, revalidate changed files). |
| CF-09 | Coverage-led hunting waves by isolated hunters | native (partial) | security/full-audit.md §5; agents/security-hunter.md | eval 6-audit (defined, not run) | Partial: one pass of hunters, no wave loop. |
| CF-10 | Core hunting method: principal, input, control, trace to minimum effect | native | agents/security-hunter.md (trace every lead to source and sink); security/findings.md §1 | none (guidance text only) |  |
| CF-11 | Coverage-critic waves looking for unmapped surface | gap | - | none (not implemented) | Reason: no critic agent or step; full-audit.md §4 (deep) only adds a second pass on high-risk checked items. Closure: add a fresh-context critic step that reads the trust-boundary map and ledger. |
| CF-12 | Attack-class prompts (injection, access control, files, crypto, logic ...) | native | security/coverage-model.md §1-§3; security/secure-implementation.md §6; ledger audit areas | none (guidance text only) | Questions and checklists, not verbatim hunter prompt blocks. |
| CF-13 | Nine domain companions (AI, protocol, client, supply chain, cloud ...) | native (partial) | security/coverage-model.md §4 (AI-agent); ledger areas ci-cd, deploy-iac, dependencies, ai-agent | none (guidance text only) | Partial: no protocol/RPC, mobile or blockchain companions. |
| CF-14 | Independent validation by a fresh verifier that tries to refute | native | agents/security-verifier.md; security/full-audit.md §6; security/findings.md §4 | eval 6-audit (defined, not run) grades confirmed IDOR and rejected leads | The grader checks outputs, not that a fresh verifier was used. |
| CF-15 | Three-verdict model (confirmed / needs-validation / rejected) | native | security/findings.md §2; `ult findings validate` | unit: test_findings.py | Hyphenated `needs-validation`. |
| CF-16 | Strict findings.json schema, sorted, fingerprints | native (partial) | security/findings.md §1; schemas/findings.schema.json; `ult findings validate\|add` | unit: test_findings.py | Partial: unknown fields only warn; no sorted-by-fingerprint rule is documented. Duplicate id/fingerprint and unredacted secrets are errors. |
| CF-17 | Independent verification of final records | native (partial) | agents/security-verifier.md; security/full-audit.md §6 | none (guidance text only) | Partial: one verification stage on candidates, no second pass over final records. |
| CF-18 | Reports derived only from final records | native | `ult findings render`; security/findings.md §7 ("the JSON is the source") | unit: test_findings.py |  |
| CF-19 | Severity anchors with a high-vs-medium discriminator | native | security/findings.md §3 | none (guidance text only) | Impact-first with caps; CVSS not used. |
| CF-20 | Anti-pattern list (checklist deviation is not a vuln, no guessing deployment ...) | native | security/findings.md §5 (FP-01..FP-20), §2; SKILL.md §1 rule 1 | none (guidance text only) |  |
| CF-21 | AI/LLM companion: indirect injection, tool authority, exfiltration | native | security/coverage-model.md §4; `ult scan` ai-agent rules (agent-instruction-text, hidden-unicode, agent-bypass-permissions, agent-broad-allow, agent-hook-fetch-exec, mcp-unpinned-launcher, mcp-inline-secret) | unit: test_scan.py (prompt-injection text, agent configs) |  |
| CF-22 | Validators for findings and ledger (zero-dependency) | native | `ult findings validate`, `ult findings ledger check` (Python stdlib, no Node) | unit: test_findings.py | Tests cover valid/invalid files, redaction rules, id/fingerprint checks, ledger lifecycle. |

### skills (Trail of Bits)

Repo `trailofbits/skills` · revision `e4dd0bb5b155` · license: CC BY-SA 4.0 (share-alike). No prose reused; Ultimatum writes its own text

Counts: native 11, pending 0, shared 5, optional 2, gap 8, rejected 5 (31 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| TOB-01 | fp-check: gates and verdict for a suspected bug | native | agents/security-verifier.md; security/findings.md §4, §5 | none (guidance text only) |  |
| TOB-02 | Differential review of a PR, commit or diff | native | security/change-review.md; `ult scan --diff <base>` (changed lines, `diff-removed-guard`) | unit: test_scan.py (test_diff_limits_to_changed_lines_and_flags_removed_guard) | The eval 5-secure-feature covers the implementation overlay, not change review. |
| TOB-03 | Context building before analysis | shared | discovery.md §2; security/full-audit.md §2 (trust-boundary map) | none (guidance text only) |  |
| TOB-04 | Variant analysis from a known root cause | native | security/remediation.md §5; security/change-review.md §3 step 4 (siblings) | eval 7-remediation (defined, not run) grades the PUT variant of the GET IDOR |  |
| TOB-05 | Static analysis: Semgrep, CodeQL, SARIF handling | optional | semgrep: `ult scan --semgrep-config <local rules or p/...>` (never by default; detect with PATH lookup, listed by `ult doctor`; registry packs need consent). Fallback: built-in sink leads | unit: test_scan.py (fake semgrep stub only) | Runs with `--metrics=off --disable-version-check`. CodeQL and SARIF parsing are not implemented. |
| TOB-06 | Semgrep rule creation and porting | gap | - | none (not implemented) | Reason: specialist task. Closure: point to an installed upstream rule-authoring plugin; nothing built in. |
| TOB-07 | Insecure defaults: fallback secrets, default creds, fail-open config | native | `ult scan` rules fallback-secret, debug-enabled, cors-wildcard, cookie-flags, tls-verify-off; security/secure-implementation.md §6 (Secrets, Deploy settings) | unit: test_scan.py | Leads, not findings. |
| TOB-08 | Sharp edges: footgun APIs and dangerous defaults | native (partial) | security/secure-implementation.md §6 | none (guidance text only) | Partial: short per-surface checklists, not a six-category review. |
| TOB-09 | Supply-chain risk: advisories, abandoned upstreams, publisher changes | optional | osv-scanner via `ult scan` (offline with `OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY`, online only with `--osv-online`); fallback: manifest/lockfile inventory and `dep-*` leads, advisory status `unknown` | unit: test_scan.py (fake osv stub; exit 128 is not clean) | Abandoned-upstream and publisher checks are not done. |
| TOB-10 | Agentic-actions auditor for CI workflows invoking AI agents | native (partial) | `ult scan` ci-* rules (ci-expression-injection, ci-prt-checkout-head, ci-permissions-write-all, ci-action-unpinned); security/coverage-model.md §4 (Agent CI actions) | unit: test_scan.py (test_ci_risks) | Partial: nine attack vectors are not enumerated one by one. |
| TOB-11 | CVSS v4 scoring | rejected | - | none (guidance text only) | Severity is impact-first (findings.md §3); CVSS would be an unused label. |
| TOB-12 | Triage brocards for inbound reports | native | agents/security-verifier.md; security/findings.md §4, §5 | none (guidance text only) | Folded into verifier questions and FP patterns. |
| TOB-13 | Patching bugs: reproduce, validate, patch, prove | native | security/remediation.md §1-§4, §6 | eval 7-remediation (defined, not run) grades exploit blocked, same-tenant access intact, regression tests for GET and PUT |  |
| TOB-14 | Post-patch validation on base and patched checkouts | native (partial) | security/remediation.md §4 step 4 (stash or revert one guard line, run the same test twice) | none (guidance text only) | Partial: manual procedure; no runner script. |
| TOB-15 | Regression hunt campaigns | shared (partial) | security/change-review.md §2 (`git log -S`, blame); debugging.md §2 (bisect) | none (guidance text only) | Partial: no dedicated campaign. |
| TOB-16 | Property-based testing guidance | native | tdd.md §7 | none (guidance text only) |  |
| TOB-17 | Mutation testing | shared (partial) | tdd.md §6 (flip check); security/secure-implementation.md §5 (revert the guard) | none (guidance text only) | Partial: manual mutation only. Mutation tools are not detected or wired. |
| TOB-18 | Fuzzing and sanitizer handbook skills | gap | - | none (not implemented) | Reason: native-code fuzzing is specialist work. Closure: mention as an escalation only; no built-in route. |
| TOB-19 | Spec-to-code compliance, one check per requirement | shared (partial) | security/coverage-model.md §1 (ASVS chapter pass); feature-planning.md §6 (success checks) | none (guidance text only) | Partial. |
| TOB-20 | Entry-point analyzer | native (partial) | `ult map query routes\|entry_points`; security/full-audit.md §1 | unit: test_map.py | Partial: lists leads with file:line; no "who can call this" column. |
| TOB-21 | Constant-time analysis (compiler-induced timing channels) | gap | - | none (not implemented) | Reason: specialist crypto tooling. Closure: out of scope for the base plugin. |
| TOB-22 | Zeroization audit | gap | - | none (not implemented) | Reason: specialist (asm/CFG). Closure: out of scope. |
| TOB-23 | C and Rust language-specific reviews | gap | - | none (not implemented) | Reason: no language-specific multi-worker review. Closure: out of scope. |
| TOB-24 | Trailmark code graph and slicing | gap | - | none (not implemented) | Reason: `ult map` is a lighter, regex-based map. Closure: optional Graphify (GRA rows) for graph needs. |
| TOB-25 | Smart-contract security scanners and advisors | gap | - | none (not implemented) | Reason: blockchain is out of scope. Closure: none planned. |
| TOB-26 | Second opinion from another vendor's CLI | rejected | - | none (guidance text only) | Sends code to third parties. |
| TOB-27 | Review-and-fix loop with a findings ledger | shared | SKILL.md §3; orchestration.md §6 (fix rounds); security/full-audit.md §6 | none (guidance text only) |  |
| TOB-28 | Interactive HTML walkthrough of a change | rejected | - | none (guidance text only) | Not adopted. |
| TOB-29 | Open-sourcing hygiene incl. secrets in history | gap | - | none (not implemented) | Reason: `ult scan` runs gitleaks on a directory, not git history, and release.md §5 checks the diff only. Closure: run `gitleaks git` when installed and add a pre-release history check. |
| TOB-30 | Niche tools: APK scanner, Burp parser, YARA, DWARF ... | rejected | - | none (guidance text only) | Specialist. |
| TOB-31 | Convenience skills: gh-cli, modern-python, devcontainer ... | rejected | - | none (guidance text only) | Out of scope. |

### ASVS 5.0

Repo `OWASP/ASVS` · revision `62981c68fd06` · license: CC BY-SA 4.0 (IDs and titles cited only; no requirement text reused)

Counts: native 19, pending 0, shared 0, optional 0, gap 1, rejected 1 (21 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| V1 | Encoding and Sanitization | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit items injection, parsing; `ult scan` sink rules | unit: test_scan.py (sink rules); eval 6-audit (defined, not run) grades the SQL-injection lead is rejected | Partial: vocabulary and applicability, no per-requirement checklist. |
| V2 | Validation and Business Logic | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit item business-logic; security/secure-implementation.md §6 (money) | none (guidance text only) | Partial. |
| V3 | Web Frontend Security | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit items output-xss, config; `ult scan` html-sink, cors-wildcard, cookie-flags; ui.md §8 | unit: test_scan.py | Partial. |
| V4 | API and Web Service | native (partial) | security/coverage-model.md §1 (question only); WSTG-APIT tags on authz-object | none (guidance text only) | Partial: no dedicated ledger item or scanner rule for GraphQL/WebSocket. |
| V5 | File Handling | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit item files; `ult scan` path-from-request, archive-extract; security/secure-implementation.md §6 | unit: test_scan.py | Partial. |
| V6 | Authentication | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit item authn; security/secure-implementation.md §6 | none (guidance text only) | Partial. |
| V7 | Session Management | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit item session | none (guidance text only) | Partial. |
| V8 | Authorization | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit items authz-function, authz-object, review item removed-checks | eval 6-audit (defined, not run) grades the confirmed IDOR; eval 5-secure-feature (defined, not run) and eval 7-remediation (defined, not run) test cross-account access | Partial: strongest-tested chapter, but only against small fixtures. |
| V9 | Self-contained Tokens | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS` (tag on session item); `ult scan` jwt-unverified, jwt-decode-only | unit: test_scan.py | Partial. |
| V10 | OAuth and OIDC | native (partial) | security/coverage-model.md §1 (question and N/A reason format only) | none (guidance text only) | Partial: no ledger item, tag or scanner rule. |
| V11 | Cryptography | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit item crypto; `ult scan` weak-hash, weak-hash-password, insecure-random, tls-verify-off | unit: test_scan.py | Partial. |
| V12 | Secure Communication | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; `ult scan` tls-verify-off; ssrf item | unit: test_scan.py | Partial. |
| V13 | Configuration | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit items secrets, config, deploy-iac; `ult scan` iac-* rules | unit: test_scan.py | Partial. |
| V14 | Data Protection | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit item data-exposure; security/secure-implementation.md §6 | none (guidance text only) | Partial. |
| V15 | Secure Coding and Architecture | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit items dependencies, business-logic | unit: test_scan.py (dependency inventory leads) | Partial. |
| V16 | Security Logging and Error Handling | native (partial) | security/coverage-model.md §1 (applicability + source-level question); ledger tags in findings.py `PRESETS`; audit item data-exposure | none (guidance text only) | Partial: logging coverage is not a separate item. |
| V17 | WebRTC | native (partial) | security/coverage-model.md §1 ("usually not applicable: say so") | none (guidance text only) | Partial: applicability note only. |
| ASVS-01 | Stable requirement IDs as a coverage vocabulary | native | security/coverage-model.md §1; ledger tags such as `ASVS:V8`; findings `refs.asvs` | none (guidance text only) | IDs and titles only. |
| ASVS-02 | Documentation-type requirements need written evidence | native | security/coverage-model.md §1 (needs-owner unless a doc exists in the repo) | none (guidance text only) |  |
| ASVS-03 | Level selection guidance (L1 / L2 / L3) | gap | - | none (not implemented) | Reason: no level policy; profiles quick/standard/deep (full-audit.md §4) change breadth instead. Closure: add a level-to-profile note if users ask for ASVS-level claims. |
| ASVS-04 | Mapping to ASVS 4.0.3, CWE and NIST | rejected | - | none (guidance text only) | Not needed; scan leads carry CWE ids (scan.py) and findings accept `cwe`. |

### Web Security Testing Guide

Repo `OWASP/wstg` · revision `e493506b9cde` · license: CC BY-SA 4.0 (IDs and titles cited only)

Counts: native 1, pending 0, shared 1, optional 0, gap 0, rejected 0 (2 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| WSTG-01 | Test catalogue with stable IDs as a "did we consider this class" checklist | native (partial) | security/coverage-model.md §2 (12 categories INFO, CONF, IDNT, ATHN, ATHZ, SESS, INJT, ERRH, CRYP, BUSL, CLNT, APIT turned into source-level questions); ledger tags `WSTG-*` | none (guidance text only) | Partial: WASM category is not listed. Live-probe steps are excluded; items that need a live probe become needs-validation or blocked. Uses the current `INJT` name, not the outdated `INPV`. |
| WSTG-02 | Reporting guidance and tool appendix | shared (partial) | security/findings.md §7 (report template) | unit: test_findings.py | Partial: no tool appendix. |

### semgrep

Repo `semgrep/semgrep` · revision `692bfae4ca1b` · license: LGPL-2.1 (engine; invoked only as an optional external tool)

Counts: native 0, pending 0, shared 0, optional 5, gap 2, rejected 1 (8 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| SG-01 | Scan with a rule file, directory or registry id | optional | `ult scan --semgrep-config` <local file/dir or p/...>. Detect: PATH lookup (`ult doctor`). Registry ids download rules and need consent. Fallback: built-in sink leads (`ult scan`) | unit: test_scan.py (fake stub) | Without a config, `ult scan` prints "semgrep: not run: no rules given". |
| SG-02 | Machine-readable output formats | optional | `ult scan` runs semgrep with `--json` and normalises results to leads; `--json OUT` writes the combined report | unit: test_scan.py | Other formats are not used. |
| SG-03 | Diff-aware scan from a baseline commit | optional | `ult scan --diff BASE` adds `--baseline-commit` for semgrep | none (guidance text only) | Not asserted by a test. |
| SG-04 | Telemetry control | optional | `ult scan` always passes `--metrics=off --disable-version-check` | unit: test_scan.py (flags asserted) |  |
| SG-05 | Targeting: include/exclude, severity filters, ignore files | gap | - | none (not implemented) | Reason: only `--path` narrows the scan target; semgrep's own filters are not passed through. Closure: pass-through flags. |
| SG-06 | Exit-code control | optional | `ult scan` prints each external command with its exit code and a completed/failed status | unit: test_scan.py |  |
| SG-07 | Rule authoring helpers (--validate, --test) | gap | - | none (not implemented) | Reason: same as TOB-06. Closure: none planned. |
| SG-08 | Pro features (interfile taint, secret validation, supply chain) | rejected | - | none (guidance text only) | Paid and networked. |

### osv-scanner

Repo `google/osv-scanner` · revision `02f96a40691c` · license: Apache-2.0

Counts: native 0, pending 0, shared 0, optional 4, gap 1, rejected 1 (6 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| OSV-01 | Scan a source tree for vulnerable packages | optional | `ult scan` runs `osv-scanner scan source -r --format json` when installed and allowed. Fallback: manifest/lockfile inventory, advisory status `unknown` | unit: test_scan.py (fake stub) | Advisories are never reported clean unless osv-scanner completed. |
| OSV-02 | Lockfile selection, ignore handling, config file | gap | - | none (not implemented) | Reason: not exposed. Closure: pass-through flags if a repo needs them. |
| OSV-03 | Output formats (table, json, sarif, SBOM ...) | optional | JSON only, parsed into leads | unit: test_scan.py |  |
| OSV-04 | Offline mode with a local database | optional | Runs with `--offline` only when `OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY` is a directory; `--osv-online` needs the user's consent | unit: test_scan.py (test_osv_not_run_offline_without_db) |  |
| OSV-05 | Supported lockfile list | optional | osv-scanner's own; Ultimatum's `LOCKFILES` and `MANIFESTS` sets drive the inventory and `dep-no-lockfile` / `dep-unpinned` leads | unit: test_scan.py |  |
| OSV-06 | Container image scans and guided fix | rejected | - | none (guidance text only) | Fix can run package managers; never run. |

### gitleaks

Repo `gitleaks/gitleaks` · revision `5f6ec56cfa6f` · license: MIT

Counts: native 0, pending 0, shared 1, optional 6, gap 0, rejected 0 (7 total).

| id | capability | status | where in Ultimatum | verification | notes |
|---|---|---|---|---|---|
| GL-01 | Scan a directory or git history for secrets | optional | `ult scan` runs `gitleaks dir <target> --redact --exit-code 3 --report-format json` when installed. Fallback: built-in secret patterns (`scan_secrets`) | unit: test_scan.py (fake stub; built-in fallback and redaction tests) | Only `dir`; `gitleaks git` (history) is not run. See TOB-29. |
| GL-02 | Report formats and path | optional | JSON report written privately, parsed into leads | unit: test_scan.py |  |
| GL-03 | Redaction of secret values | optional | `--redact` is always passed; Ultimatum redacts again before printing or storing (`redact()`) | unit: test_scan.py, test_common.py (test_redacted_everywhere; redact patterns) |  |
| GL-04 | Config and custom rules | optional | No `--config` is passed; gitleaks applies its own lookup | none (guidance text only) |  |
| GL-05 | Suppression: inline allow, ignore file, baseline | shared (partial) | `ult scan` rule `suppressed-signal` lists `gitleaks:allow` / `nosemgrep` / `nosec` comments as leads | unit: test_scan.py | Partial: gitleaks applies its own suppression; Ultimatum only flags the comments. |
| GL-06 | Decoding and archive depth options | optional | Left at gitleaks defaults | none (guidance text only) |  |
| GL-07 | Exit codes | optional | `--exit-code 3` separates "leaks found" from errors; the code and status are printed | unit: test_scan.py |  |

