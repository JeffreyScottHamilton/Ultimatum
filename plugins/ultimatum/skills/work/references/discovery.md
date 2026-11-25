# Discovery: understanding a codebase quickly and correctly

Purpose: answer "how does X work?", or get oriented before changing an unfamiliar repo, using as little reading as possible and claiming only what the source confirms.

## 1. Orientation pass (once per repo, about 5 minutes of tool calls)

1. Read the project's own guidance before anything else: `CLAUDE.md`/`AGENTS.md`, `README`, `CONTRIBUTING`, `docs/architecture*`, ADRs. Their conventions override Ultimatum defaults.
2. Run `ult map summary` to get languages, manifests, entry points, routes, data stores, auth hotspots, CI, infra, and docs. It builds on first use, and you can rebuild it with `ult map build` after big changes.
3. Learn how the project builds and tests: package.json scripts, Makefile, `pyproject` tool sections, CI workflow steps. CI is the source of truth for "how tests are run here".
4. Run `git log --oneline -15` and `git log --format='%h %s' -- <dir>` for the area you'll touch. Recent commits show the conventions in practice and who is changing what.

## 2. Answering a specific question

1. Turn the question into symbols and strings: route paths, function names, error text, config keys, table names.
2. Find the anchors: `ult symbols <Name>`, `ult refs <Name>`, `ult search '<string>'`, `ult map query <keyword>`.
3. **Trace the path in the source.** Go from entry point (route, CLI, job, event) through middleware and guards to the handler, then the service, the data access, and the response. Read each hop at its line range.
4. State the answer with an anchor for each hop (`path:line`). Mark anything inferred rather than read as *inferred*.
5. If the trace crosses a library boundary and the behavior depends on the library, check the installed version's source or types. If Context7 is available, check its docs for that version. Don't rely on memory.

## 3. Reuse-first inventory (before writing new code)

Before you add a helper, component, query, hook, endpoint, or config option, search for an existing one:
- the name family (`format*`, `*Money*`, `use*`, `*Dialog*`), plus the domain noun
- where similar features were built recently (`git log -S '<similar call>'`)
- the shared directories: `utils/`, `lib/`, `common/`, `shared/`, `components/`, `hooks/`, `services/`, the design-system package

Choose the most-used, non-deprecated option. Check for deprecation markers (comments, `@deprecated`, `legacy/` dirs, lint rules) and choose the one current code calls. If two options compete, say which one you picked and why.

Extend an existing function only if the change is backward compatible for its callers (check `ult refs`). Otherwise compose the existing pieces.

## 4. Output for a "how does it work" question

- Give the short answer first, in two to five sentences.
- Then list the path as numbered hops, each with `path:line` and one clause.
- Then add gotchas: config flags, environment differences, surprising defaults, dead code.
- End with what you didn't verify.

Don't produce architecture essays the user didn't ask for. Ask before saving a written map to the repo, and keep personal notes in `ult note`.
