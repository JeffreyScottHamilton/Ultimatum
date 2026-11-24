# Ultimatum 2.0 build spec (interfaces shared by all workers)

Read with `PLAN.md`. Repo root: `/home/user/Ultimatum`. Plugin: `plugins/ultimatum/` (below, `P/`).

## Hard rules (every worker)
- Toolbelt (`P/scripts/ult`, `P/scripts/ultlib/*.py`) is **Python 3.9+ standard library only, no network access**. Use `from __future__ import annotations`. Reuse `ultlib/common.py` (`project_root`, `state_dir`, `write_private`, `dump_json`, `redact`, `eprint`).
- Each new module exposes `register(sub)` that adds its argparse subparser(s) and sets `func`. `P/scripts/ult` already imports these optional modules by name: `route, components, learn, budget, sync, upstreams, update`.
- **Original wording and code only.** Never copy text or code from upstream repos. Do not open the upstream clones in the scratchpad; work from the notes in `research/ultimatum-2/`.
- Never commit, push, or edit files you do not own. Never run upstream scripts or download/execute remote programs.
- Tests: `unittest`, in `P/tests/test_<name>.py`, using `P/tests/_harness.py` (`UltCase`, `self.ult(...)` returns `R` with `.code .out .err .all`; `self.root` is a temp project; `ULTIMATUM_ROOT` env points there). Run: `python3 -m unittest discover -s plugins/ultimatum/tests` from the repo root. All 200 existing tests must still pass.
- Output of every command is short (it lands in a chat that is re-read each turn). Cap lists. No ANSI colour.

## Module registry: `P/skills/work/modules.json`
```json
{"version": 1, "modules": [
  {"id": "ui", "kind": "route|addon|overlay", "summary": "...",
   "activate": {"keywords": ["..."], "phrases": ["..."], "files": ["*.tsx"], "deps": ["react"]},
   "never_when": ["..."], "requires": [], "conflicts": [], "read": ["ui.md", "browser-verification.md"],
   "mode_hint": "STANDARD", "contract": "one sentence", "attribution": ["upstream ids"], "version": "2.0.0"}
]}
```
- `read` paths are relative to `P/skills/work/references/`. `cost_bytes` is **not** stored; it is computed from the files.
- Routes (exactly one chosen): small, discover, feature, large, bug, ci-pr, ui, data-infra, optimize, release, sec-review, sec-audit, sec-fix, handoff, improve, skill-eval, documents, mcp-build, skill-author.
- Add-ons (zero or more, max 2): react (`react.md`), design (`design/design.md`), motion (`design/motion.md`), components (`design/components.md`), production (`production.md`), context (`context-efficiency.md`), integrations (`integrations.md`).
- Overlay: security (`security/secure-implementation.md`).

## `ult route "<task>" [--root DIR] [--json] [--eval FILE]`
Deterministic scoring, no model call. Prints at most 6 lines:
```
mode: STANDARD  route: ui  +: react, motion
read: ui.md, browser-verification.md, react.md, design/motion.md (~3.4k tokens)
overlay: security (touches: auth)         # or: overlay: none
alt: feature (low confidence)             # only when the top two routes are close
lessons: <up to 3 one-line lessons from learn.relevant()>   # only when any
```
- Modes: FAST (route small, no overlay), STANDARD (default), DEEP (large, sec-audit, release, or the word "audit"/"thorough"/"deep"), RECOVERY (task says resume/continue/pick up/after compaction, or a handoff file exists and the task is empty). User prefixes `fast:` / `deep:` force the mode.
- `--root` lets repo signals add add-ons (package.json deps react/next → react).
- `--eval FILE` reads JSONL cases `{"task": str, "route": str, "addons": [..], "overlay": bool, "mode": str?}` and prints accuracy for route, overlay, addons; exit 1 if route accuracy < 0.95 or overlay accuracy < 1.0.
- Lessons: `try: from ultlib.learn import relevant` → `relevant(task, root, limit=3) -> list[str]`; skip silently if unavailable.

## `ult components "<need>" [--stack react|vue|svelte|any] [--all] [--json]`
Offline lookup over `P/data/components.json` (built from `research/ultimatum-2/component-registry.json`). Prints ≤3 matches: name, licence, maintained?, install line, one-line fit. Restricted licences (Commons Clause, non-SPDX, none) are excluded unless `--all`, and then flagged.

## `ult upstreams [--json]`
Lists `P/data/upstreams.json`: id, repo, pinned commit, licence, decision (adapt|adapter|skip), modules, reviewed date.

## `ult learn ...` (state in `state_dir()`; global store `~/.ultimatum/` or `ULTIMATUM_HOME`)
- `observe [--transcript PATH] [--hook]`: reads the transcript (in hook mode, JSON on stdin with `transcript_path`), records **counts and categories only** (repeated failing command kinds, re-reads, oversized outputs, user corrections, routes used) to `observations.jsonl`. Hook mode prints nothing, always exits 0, finishes in < 2 s, and is disabled by `ULTIMATUM_OBSERVE=0`.
- `add "<lesson>" [--scope project|global] [--module ID]`, `list [--scope]`, `prune`.
- `relevant(task, root, limit)` function: keyword overlap, ≤ 3 lines, each ≤ 120 chars.
- `propose`: aggregates observations into `proposals/<id>.json` + `.md`. **Allow-list fields only:** plugin version, module id, category, counts, a generic lesson sentence chosen from a fixed template set. No paths, code, user text, repo names, URLs or secrets. A test feeds a transcript full of secrets/paths and asserts none reach the proposal.
- Project knowledge file: `state_dir()/knowledge.md` (git-ignored with the rest of `.ultimatum/`).

## `ult budget [--record] [--transcript PATH]`
Turns, tokens per turn (latest), cache-read share, top 3 costs this chat. `--record` appends a totals line to `state_dir()/usage.jsonl`. Reuse `usage.py`/`context.py` parsing.

## `ult sync export --to DIR | import --from DIR`
Copies global lessons + project `knowledge.md` to/from a folder the user chooses (for example a clone of their own private repo). Merge on import, dedupe, never overwrite newer entries. No git or network in the toolbelt; the `/ultimatum:sync` skill runs git with the user's approval.

## `ult update status | setup [--apply] | migrate`
- `status`: running plugin version (from `P/.claude-plugin/plugin.json`), marketplace copy version if found under `~/.claude/plugins/`, whether auto-update is on for the `ultimatum` marketplace, and the one next step.
- `setup`: prints the one-time steps for local CLI, cloud (claude.ai/customize/plugins) and running sessions (`/reload-plugins`); `--apply` sets `extraKnownMarketplaces.ultimatum.autoUpdate = true` in `~/.claude/settings.json` (backup first, preserve all other keys, idempotent). Tests use a temp `HOME`.
- `migrate`: idempotent upgrade of 0.4.x state in `.ultimatum/` (no-op if nothing to do); prints what changed.

## Management skills (`P/skills/<name>/SKILL.md`, all `disable-model-invocation: true`)
status, setup, sync, learn, skills, budget, eval, doctor, rollback, migrate. Each is short (≤ 1.5 KB) and calls the toolbelt with `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" ...`.
