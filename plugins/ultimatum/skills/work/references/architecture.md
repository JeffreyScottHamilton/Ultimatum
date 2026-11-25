# Architecture Guardian

Use this when a change reshapes structure. That covers new modules, moved responsibilities, refactors, cross-package work, the **large** route, and code reviews. Its job is to keep the codebase easy to extend: small focused files, explicit interfaces, one owner for each responsibility, and no parallel implementations.

## When to run it, and when not to

| Situation | What to run |
|---|---|
| Typo, constant, one-function fix (**small**) | Nothing. The router does not load this file. |
| New feature inside one module | `ult arch check --changed` once, before you report |
| New module, moved code, refactor, or large route | Graph first (below), then `--changed` before and after |
| Code review of a diff or PR | `ult arch check --changed`, and put its findings in the review |
| "Audit the architecture" or "where is the tech debt" | Full `ult arch check`, then `ult arch baseline` so later runs report only drift |

Never run a full-repository audit for a trivial change. `--changed` reads only the git diff and untracked files, and builds the import graph once to look for cycles. On this plugin's 44 Python files it took under a second.

## 1. Understand the structure before editing

Check these in order, and stop once you know where the change belongs:

1. **The import graph from `ult arch`.** Python and JS/TS imports are read locally: an edge only counts if a file's import resolves to exactly one file in the repo. Module names that two files share are skipped rather than guessed.
2. **Graphify, if `graphify-out/graph.json` exists.** `ult arch` merges its EXTRACTED import edges automatically and prints `graphify(n)` in the summary. It ignores INFERRED and AMBIGUOUS edges, so a guess never becomes a cycle finding. For blast radius before a rename or move, Graphify's `affected` command walks reverse dependents of a symbol (check `graphify --help` for the exact form in the installed version). For blast radius, run `ult arch deps <file> --reverse` (importers, capped; `--depth N` for transitive ones) instead of loading the graph file. If the graph is older than your edits, regenerate it with `graphify update .` (AST only, no model calls) or treat it as stale.
3. **`ult map summary` / `ult map query <section>`** for entry points, routes, data stores and sinks in an unfamiliar repo.
4. **Serena or an LSP MCP, if it is in your tool list,** for symbol-level work: find every reference before changing a signature, and rename with the tool rather than with text replace. Otherwise use `ult symbols <Name>` and `ult refs <Name>`.

Then answer three questions in a line each, before writing code:
- **Owner:** which existing module already owns this responsibility?
- **Seam:** which interface will the new code plug into: a registry, hook, event, plugin API, or a public function?
- **Direction:** which way do the new imports point? Low-level modules must not import high-level ones.

If an owner exists, extend it. If you create a new module, it gets one job, a name that matches its siblings, and a public surface that is smaller than its body.

## 2. Principles (a small core plus extensions)

Well-structured extensible apps keep a small, stable core and push features into modules that talk to the core through a narrow, documented API. Plugin systems such as Obsidian's (a core app plus community plugins that only use the published API) are the reference shape. Apply that at every scale:

- **Separation of responsibilities.** A file does one thing you can name in five words. Split when it has two reasons to change.
- **Explicit interfaces.** Callers use a module's public functions or types, not its internals. Export the minimum. In TypeScript, type the boundary. In Python, annotate public functions.
- **Predictable dependencies.** Imports flow one way: entry points → features → core and shared utilities. No cycles. Shared code moves down, never sideways into a sibling feature.
- **Extend, don't fork.** Before adding a helper, run `ult search` and `ult symbols` for an existing one. A second implementation of the same thing is a defect, even if it is shorter.
- **Small and focused.** The default limits are 500 lines per file and 80 per function (`--max-lines`, `--max-func`). They are prompts to look, not laws. A long table of data is fine, and a 300-line function with four jobs is not.
- **Consistent naming.** Match the directory's existing style (snake, kebab, camel or Pascal) and its vocabulary (`*_service`, `use*`, `*.test.ts`).
- **No dead weight.** That means no placeholders (`TODO`, `NotImplementedError`, `throw new Error('not implemented')`) in delivered code, no unused private functions, no speculative abstraction layers with one implementation, and no new dependency when the standard library or an existing dependency does the job.
- **Meaningful tests.** Every new module has a test that exercises its public surface. Assert behaviour, not implementation details.
- **Docs that stay true.** Document the seam: what a module promises, not how it works line by line. Where you can, make docs checkable (a test that imports each symbol a doc names).

## 3. Deterministic checks (`ult arch`)

```
ult arch check [--changed] [--drift] [--path DIR] [--exclude GLOB] [--strict] [--record] [--json]
ult arch baseline
```

| Finding | Meaning | Blocking with `--strict` |
|---|---|---|
| `cycle` | Import cycle (Tarjan SCC over local and Graphify EXTRACTED edges) | yes |
| `stub` | Placeholder left in code (abstract methods and overloads are exempt) | yes |
| `dup` | The same normalised 8-line block in two places (imports and comments ignored) | no |
| `size` / `func-size` | File or function over the limit | no |
| `naming` | Style outlier in its directory, or a Python module name that cannot be imported | no |
| `dead?` | Private top-level Python function or class that is never referenced (a lead, so verify it) | no |
| `untested?` | Changed source file whose name no test mentions (a lead) | no |

The summary line also reports the typed share: the percentage of Python functions that are fully annotated, plus the count of TypeScript `any`. Use it as a trend, not a gate.

Fixture, vendor, snapshot and migration directories are skipped. Generated code goes in `--exclude`. Findings marked `?` are leads: open the file before acting on them.

**Drift.** `ult arch baseline` records the current findings in `.ultimatum/arch-baseline.json`, which stays local and is never committed. `ult arch check --drift` then prints only findings that are new since the baseline, which is how a legacy repo can adopt the checks without first fixing everything.

## 4. Optional helpers, and when each pays off

| Tool | Use it for | Skip it when |
|---|---|---|
| Graphify | Repo-wide relationships, blast radius, cycles across languages that `ult arch` cannot parse | No `graphify-out/` exists and the task is local. Building a graph runs a model pass over docs and costs tokens. |
| Serena / LSP MCP | Exact references and safe renames in large typed codebases | Small repo, or a dynamic language where `ult refs` is just as good |
| RTK | Optional output filtering if the user already uses it | Always prefer `ult run`, which keeps raw output and exit codes. Some RTK filters drop the per-finding lines a review needs. |
| Repomix | Packing a bounded, explicit file list into one file for a reviewer or subagent that cannot read the repo | You can point the agent at paths instead. Never pack a whole repo into the chat. Check the packed file's size before handing it over. |

These are user-installed tools. Ultimatum does not vendor or install them. `ult doctor` shows which ones are on PATH.

## 5. Review checklist

When you review a diff, run `ult arch check --changed`, then go through:

1. Did it extend the owning module, or start a parallel one? Search for the old helper by name.
2. Do new imports point downward? Any new `cycle`?
3. Is the public surface minimal, and is the boundary typed?
4. Any `stub`, commented-out code, debug output, or unused private helper?
5. Is every new file small, single-purpose, and named like its siblings?
6. Does each new module have a test of its public behaviour?
7. Any new dependency? Name why the standard library or an existing dependency was not enough.
8. Any abstraction with one implementation and no second caller planned in this task?

Report findings with `file:line` and the fix. Mark unverified leads as leads.

## 6. Feeding the learning loop

`ult arch check --record` adds one local observation per day, holding only finding **counts** (no paths and no code), to `.ultimatum/observations.jsonl`. `ult learn propose` turns repeated counts into fixed-wording lessons, such as "break import cycles by moving shared code down". Those lessons go through the normal sanitized-proposal and PR-approval flow described in `self-improvement.md`.

## 7. Quality is never traded for tokens

A cheaper run that leaves a new cycle, placeholder or failing test is a failed run. In evaluations, a task passes only if its tests pass **and** `ult arch check --changed` shows no new blocking finding. Report cost per passing task with that definition. Never accept a change, a proposal or a routing tweak that saves tokens by lowering either.
