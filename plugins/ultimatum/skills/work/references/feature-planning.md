# Feature planning

Goal: turn a request into a small, agreed spec and independently verifiable slices, spending only as much ceremony as the size of the change deserves. The general loop is in SKILL.md §3; this file covers what happens before step 3 (Change).

## 1. Size it first

| Size | Signal | Do |
|---|---|---|
| Trivial | clear, local, one obvious approach | State assumptions in one line and go. No spec. |
| Normal | one feature, a few files, 1-3 open points | Short spec (§5), then slices (§6). One session. |
| Multi-session | several subsystems, days of work, or more than ~10 files | Spec plus decision list, then tickets (§6), then `orchestration.md`. |

If you are unsure, start as Normal and promote when §8 triggers.

## 2. Read before asking

1. Read what the project already says: `README`, `CONTRIBUTING`, `docs/`, ADRs, `GLOSSARY*`, `CLAUDE.md`/`AGENTS.md`, open tickets the user linked. `ult map query` for structure.
2. Find the nearest existing feature that resembles the request (`ult search`, `ult refs`). Note the pattern it uses for routes, storage, errors, tests. New work follows that pattern unless the spec says otherwise.
3. Answer every factual question yourself from code, config, or docs. Never ask the user something the repo can answer.
4. Restate in 3-5 lines: the request, what exists, anything that conflicts with the request, any cheaper path you found. If a cheaper path exists, say so before designing the expensive one.

## 3. Questions

Ask only when the answer changes what gets built and neither the repo nor the request settles it.
- Batch at most 3 questions in one message. Each carries your recommended default, so a bare "yes" accepts it.
- Order by blast radius: data shape and permissions first, naming and copy last.
- Probe failure modes while specifying; ask only the ones the code cannot answer: empty input, very large input, duplicates, wrong role, called twice, partial failure, concurrent edits.
- If the user is unavailable or says "your call", take the defaults, record each in the rulings log (§7), and continue.
- Do not ask for permission to proceed on a Normal or Trivial feature once defaults are stated. Stop for approval only on: irreversible data changes, security-sensitive behavior, anything that spends money or contacts an external service.

## 4. Vocabulary and model

Trigger: the request or code uses a term two ways, or two terms for one thing (for example "account" vs "workspace").
1. List the terms with one-line definitions taken from code or docs. Mark conflicts.
2. Pick one meaning per term, state it, and use it in the spec, tests, and names.
3. Where the project keeps a glossary or ADRs, add the entry there. Otherwise keep it in the spec's Terms section. Do not create a glossary file in a repo that has none without asking.
4. If the change adds or alters stored data, write the entity list with fields, ownership, and lifecycle (created, updated, deleted by whom) before any code. Route it to `data-and-infra.md` for migrations.

## 5. Prototype only to settle a real uncertainty

Allowed when a specific question blocks the design and reading cannot answer it: does this library support X, is this query fast enough, does this layout fit.
1. Write the question as one sentence and the observation that would answer it.
2. Build the smallest throwaway under a clearly named path (`.ultimatum/proto/<name>/` or a scratch dir). First line of every file: `THROWAWAY PROTOTYPE - delete before merge`.
3. Run it, record the answer in the spec or rulings log, delete the prototype, then build the real thing from the slice plan. Never grow a prototype into the implementation.
4. Stop after the question is answered. A prototype that answers nothing in one sitting means the question was wrong; restate it.

## 6. Spec

Where it lives: follow the project (`docs/specs/`, `docs/adr/`, an issue, a PR description). If the project has no convention, write `.ultimatum/specs/<slug>.md` (untracked). Ask before adding any tracked doc file.

Contents (short; a spec longer than the code it describes is a transcript):
1. **Problem** - who needs what, in two sentences.
2. **Requirements** - numbered, each testable, written as behavior ("returns 404 for a deleted project"), not file paths or line numbers (these age badly).
3. **Success checks** - the exact commands or interactions that prove each requirement. These become acceptance checks for slices.
4. **Non-goals** - what is explicitly out, including tempting adjacent work.
5. **Terms** - from §4, only if needed.
6. **Interfaces** - public signatures, endpoints, events, schema, with exact names; slices and workers copy these verbatim.
7. **Open points** - unresolved items with the default in force.

Self-check before moving on: every requirement has a success check; no requirement says "handle edge cases" without naming them; names are consistent; nothing contradicts a repo convention.

## 7. Slices and tickets

1. Prefactor first when it makes the change easy: a separate no-behavior-change step that keeps tests green.
2. Slice vertically: each slice is a thin working path through every layer it needs, demonstrable on its own. Not "all models, then all routes".
3. Size each slice to what one worker or one focused session can finish and verify.
4. Per slice write: goal (one line), requirements covered (numbers), files likely touched, interface it consumes and produces, **acceptance command** and expected result, blockers (other slices).
5. Order by blockers. The ready set is the slices whose blockers are done; the first slice is the thinnest end-to-end path (walking skeleton).
6. Wide mechanical refactors: expand (add new alongside old), migrate in batches, contract (remove old). Each batch keeps the suite green.
7. Tracker: if `gh`/GitHub MCP is present and the user wants tickets, one issue per slice with the same fields. Otherwise keep the list in the spec. Creating remote issues needs the user's say-so.

## 8. Rulings log

When the spec is silent or wrong, decide instead of stalling: authority is the spec, then the repo's conventions, then the least surprising behavior.
- Record in the spec's end section or `ult note --kind decision --title "<topic>" --body "Ruling: <what> - because <why> - cost if wrong: <x>"`.
- Surface all rulings in the final report.
- Stop and ask instead of ruling when the choice is irreversible, security-relevant, touches an external system, or every option is a guess.

## 9. Escalate to `orchestration.md`

Switch when any holds: three or more slices have no shared files and can run at once; the work exceeds what fits comfortably in one context; the user asks for parallel agents. Before switching, the spec's Interfaces section must be complete, because workers see only their slice. Otherwise do the slices yourself in blocker order, one test-first slice at a time (`tdd.md`).

## 10. Done planning when

- Spec exists (or assumptions line for Trivial), user-visible defaults stated.
- Each slice has an acceptance command that can fail.
- No open point blocks slice 1.
Then start slice 1. Do not wait for sign-off beyond the stop conditions in §3.
