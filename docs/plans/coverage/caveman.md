# Caveman rebuild: coverage map

Source: JuliusBrussee/caveman at commit 47c61be (read only; no installer, hook, script, binary or package from it was run).
Our files: `plugins/ultimatum/skills/work/references/craft/caveman/` (6 files) and `plugins/ultimatum/data/craft/caveman/` (README, `check_compressed.py`, three example files). Test: `plugins/ultimatum/tests/test_craft_caveman.py`.

## Licence

Root `LICENSE` is Apache-2.0; `LICENSING.md` says the project moved to Apache-2.0 at 3.0.0 and keeps `LICENSE-MIT` for earlier contributions; a `NOTICE` file is present. We ship none of the source's text or code; no NOTICE text needs carrying because nothing was redistributed.

## Inventory

Read in full: `skills/caveman`, `caveman-review`, `ultracave`, `caveman-commit`, `megacave`, `caveman-compress` (SKILL.md; SECURITY.md skimmed), `cavecrew`, `caveman-explore`, `native/native-core.md`, `investigate-first`, `surgical-patch`, `lean-build`, `safe-refactor`, `migration`, `verify-and-stop`. Read by description only: `caveman-evidence-review`, `-discover`, `-optimize`, `-learn`, `-manage`, `-setup`, `-stats`, `-help`. Sized, not read: the runtime folders (`packages/` 7.3 MB, `proxy/` 6.5 MB, `engine/` 5.2 MB, `docs/` 1.6 MB, `tests/` 1.5 MB, `shared/` 1.2 MB, `extension/`, `mcp/`, `src/`, `evals/`, `installer/`, `plugins/`, `browse/`, `mem/`, `agents/`, `supabase/`, `shrink/`), and 39 files under `skills/generated/`, `agents/`, `commands/` and `hooks/`.

## Overlap with existing references

- `context-efficiency.md` § 1–2 already held "compress prose, never evidence" and the full-sentence exceptions. Those rows are **merged**; `terse-voice.md` is the deeper version, and a pointer line is proposed.
- `debugging.md`, `tdd.md`, `feature-planning.md` and `data-and-infra.md` hold the long forms of the task stances; `task-stances.md` keeps only the stop rules and the simplicity ladder.
- `orchestration.md` holds the worker brief; `terse-artifacts.md` adds only the reply shapes.

## Items

| Source item | Status | Where |
|---|---|---|
| caveman: persistent mode until switched off | expanded | terse-voice.md § Levels |
| caveman: answer first, cut openers and recaps | merged | context-efficiency.md § 2; terse-voice.md § Cuts that are safe |
| caveman: drop filler, hedges, pleasantries | covered | terse-voice.md § Cuts that are safe |
| caveman: short words, no invented abbreviations | expanded | terse-voice.md § The floor |
| caveman: articles optional, fragments allowed | covered | terse-voice.md § Levels (Fragments) |
| caveman: never drop negations | expanded | terse-voice.md § The floor; check_compressed.py |
| caveman: numbers and units exact | covered | terse-voice.md § The floor |
| caveman: one idea per sentence (ASD-STE100 style) | covered | terse-voice.md § Levels (Brief) |
| caveman: payload verbatim (code, commands, paths, errors) | merged | context-efficiency.md § 1; terse-voice.md § The floor |
| caveman: changed lines plus context, not whole file | covered | terse-voice.md § The floor |
| caveman: never delete existing comments | covered | terse-voice.md § The floor |
| caveman: bounded status lines during tool runs | covered | terse-voice.md § Cuts that are safe |
| caveman: keep the user's language | covered | terse-voice.md § The floor |
| caveman: one term per thing | covered | terse-voice.md § The floor |
| caveman: never perform the voice | covered | terse-voice.md § Always switch back |
| caveman: break rules for security warnings | merged | context-efficiency.md § 2; terse-voice.md § Always switch back |
| caveman: break rules for irreversible actions | merged | context-efficiency.md § 2; terse-voice.md § Always switch back |
| caveman: break rules for step order | covered | terse-voice.md § Always switch back |
| caveman: break rules for a confused user | covered | terse-voice.md § Always switch back |
| caveman: break rules for persisted text | merged | context-efficiency.md § 2; terse-voice.md § Always switch back |
| caveman: break rules for questions to the user | covered | terse-voice.md § Always switch back |
| caveman: break rules for ambiguous fragments | covered | terse-voice.md § Always switch back |
| caveman: pre-send check | expanded | terse-voice.md § Check before sending |
| caveman: status query reports mode, changes nothing | covered | terse-voice.md § Levels |
| caveman: hook-tracked mode value | later | later.md (hooks) |
| ultracave: grammar stripped, payload only | covered | terse-voice.md § Levels (Payload) |
| ultracave: each fact once, no summary after list | covered | terse-voice.md § Cuts that are safe |
| ultracave: cut conjunctions only when order survives | covered | terse-voice.md § Always switch back (ordered steps) |
| ultracave: worked examples | expanded | terse-voice.md § Example (our own, three levels) |
| megacave: Classical Chinese register | covered | terse-voice.md § Levels |
| megacave: savings small and noisy, never claim | covered | terse-voice.md § Levels |
| megacave: identifiers stay in original script | merged | terse-voice.md § The floor |
| megacave: ambiguous clause falls back to vernacular | merged | terse-voice.md § Always switch back |
| caveman-commit: Conventional Commits subject | covered | terse-artifacts.md § Commit messages |
| caveman-commit: imperative, length limits, no period | covered | terse-artifacts.md § Commit messages |
| caveman-commit: body only when needed | covered | terse-artifacts.md § Commit messages |
| caveman-commit: breaking change marker and footer | covered | terse-artifacts.md § Commit messages |
| caveman-commit: never-in list (narration, first person) | covered | terse-artifacts.md § Commit messages |
| caveman-commit: attribution trailers per user rule | expanded | terse-artifacts.md § Commit messages |
| caveman-commit: always body for security, migration, revert | covered | terse-artifacts.md § Commit messages |
| caveman-commit: does not run git commit | merged | terse-artifacts.md; ci-and-pr.md |
| caveman-commit: follow project convention first | expanded | terse-artifacts.md § Commit messages (read git log) |
| caveman-review: one line per finding format | covered | terse-artifacts.md § Review comments |
| caveman-review: severity prefixes | covered | terse-artifacts.md § Review comments |
| caveman-review: drop list (hedges, praise, restating) | covered | terse-artifacts.md § Review comments |
| caveman-review: keep list (line, symbol, fix, why) | covered | terse-artifacts.md § Review comments |
| caveman-review: full prose for security, design, newcomers | merged | terse-artifacts.md; security/change-review.md |
| caveman-review: review only, no approve | merged | review/SKILL.md |
| caveman-compress: requires a file path | covered | compress-memory.md § Before you start |
| caveman-compress: data leaves the machine | expanded | compress-memory.md § Before you start |
| caveman-compress: backup outside loaded folders | covered | compress-memory.md § Before you start |
| caveman-compress: remove list | covered | compress-memory.md § What to cut |
| caveman-compress: preserve-exactly list | covered | compress-memory.md § What must come through |
| caveman-compress: preserve structure | covered | compress-memory.md § What must come through |
| caveman-compress: code blocks read-only | covered | compress-memory.md § What must come through |
| caveman-compress: validate, targeted fix, no recompress | expanded | compress-memory.md § Check the result; check_compressed.py |
| caveman-compress: provider script and CLI | later | later.md |
| caveman-compress: SECURITY.md (provider data handling) | merged | compress-memory.md § Before you start |
| cavecrew: when to use which helper | merged | orchestration.md; terse-artifacts.md § Helper reports |
| cavecrew: helper output contracts | covered | terse-artifacts.md § Helper reports |
| cavecrew: subagent presets | later | later.md |
| caveman-explore: parallel first turn, cite only read ranges | merged | context-efficiency.md § 4; terse-artifacts.md § Helper reports |
| native-core: simplicity ladder | covered | task-stances.md § The simplicity ladder |
| native-core: avoid speculative extension | covered | task-stances.md § The simplicity ladder |
| native-core: simplicity never removes safety | expanded | task-stances.md § The simplicity ladder (+ security overlay) |
| investigate-first | covered | task-stances.md § Investigate only |
| surgical-patch | merged | debugging.md § 4; task-stances.md § Fix one bug |
| lean-build | covered | task-stances.md § Build the smallest complete feature |
| safe-refactor | covered | task-stances.md § Refactor without changing behaviour |
| migration | merged | feature-planning.md § 7; data-and-infra.md; task-stances.md § Migrate |
| verify-and-stop | expanded | task-stances.md § Verify and stop |
| caveman-evidence-review | later | later.md (cloud) |
| caveman-discover | later | later.md (cloud) |
| caveman-optimize | later | later.md (cloud) |
| caveman-learn | later | later.md (cloud) |
| caveman-manage | later | later.md (cloud) |
| caveman-setup | later | later.md (cloud) |
| caveman-stats | later | later.md (cloud) |
| caveman-help | later | later.md (command set) |
| skills/generated per-host copies | later | later.md |
| activation-rule.mjs, verbs-gate.mjs, compile.mjs, registry.json | later | later.md (runtime) |
| hooks/, commands/, agents/ | later | later.md |
| engine/, proxy/, browse/, mcp/, mem/, shrink/, extension/, packages/ | later | later.md (runtime) |
| benchmarks/, evals/, README benchmark figures | later | later.md (no numbers repeated) |

Totals: covered 42, expanded 11, merged 15, later 16 (84 items)

## Not verified

- Token savings: none measured; the source's benchmark numbers are not repeated.
- Cloud and runtime skills were judged from their descriptions only.
- `check_compressed.py` was run on our three example files only, not on a real CLAUDE.md.
