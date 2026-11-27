# Terse commit messages, review comments and helper reports

Read when writing a commit message, a code-review comment or a helper's hand-back report, and you want it short without losing what a later reader needs.

Commit and PR wording rules for this project are in `../../ci-and-pr.md`; review procedure is in `../../../../review/SKILL.md`. This file only covers the short forms. Text that is stored (commits, review comments) is persisted, so it uses full words and the project's own conventions even while the chat level is terse.

## Commit messages

Follow the repository's convention first; read `git log --oneline -20` before writing. If it uses Conventional Commits (<https://www.conventionalcommits.org/>):

- Subject: `type(scope): imperative summary`. Common types are `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `revert`. Scope is optional.
- Imperative verb ("add", "drop", "rename"), no trailing full stop, aim for 50 characters, never past 72.
- Write a body only when the subject cannot carry it: the reason for a change that is not obvious from the diff, a breaking change, migration steps, an issue reference. Wrap at 72.
- A breaking change gets `!` after the type and a `BREAKING CHANGE:` footer that says who must do what by when.
- Leave out narration of the diff ("this commit changes"), first person, and "now/currently". The diff already says what changed; the message says why.
- Trailers (co-author, session link, sign-off) go at the end exactly as the project or user requires. Do not add or remove attribution the user's instructions did not ask for.

Always write a body for security fixes, data migrations, reverts and breaking changes, even when the subject looks complete. Whoever bisects later needs it.

Example (ours):
```
fix(export): stream CSV rows instead of building one string

Exports over ~200k rows ran the worker out of memory. Rows are now
written as they are read, so memory stays flat.

Refs #311
```

## Review comments

One finding per line: where, what is wrong, what to do.

```
<file>:L<line>: <severity>: <problem>. <fix>.
```

| Severity | Means |
|---|---|
| `bug` | wrong behaviour that will break for someone |
| `risk` | works today but fragile: a race, an unchecked null, a swallowed error |
| `nit` | style or naming; the author may ignore it |
| `q` | a question, not a request |

Keep the exact line, the exact symbol in backticks and a concrete fix. Add the reason only when the fix does not explain itself. Drop "I noticed", "you might want to", praise repeated per comment, and restating what the line does. If you are unsure, use `q` rather than hedging a `bug`.

```
api/orders.ts:L42: bug: `user` is undefined when `findById` misses. Return 404 before reading `user.email`.
jobs/sync.py:L88: risk: retries on every exception, including `KeyboardInterrupt`. Catch `requests.RequestException` only.
ui/Table.tsx:L17: nit: `d` shadows the outer `d`. Rename to `row`.
```

Write full paragraphs instead for a security finding (impact, the input that triggers it, the reference), for a disagreement about design (it needs the argument), and for an author who is new to the code. Severity words and evidence for security follow `../../security/change-review.md`.

## Helper reports

A helper's reply lands in the manager's context word for word, so a fixed short shape saves the most. Ask for one of these in the brief (worker brief template: `../../orchestration.md` § 3. Worker brief template):

| Helper job | Reply shape | Empty reply |
|---|---|---|
| Locate code | `path:start-end  why it matters`, one per line, only ranges actually read | `no match` plus the searches run |
| Small edit (one or two files) | `path:lines  change in under ten words`, then the check command and its exit code | one word: `too-big`, `ambiguous` or `needs-confirm` |
| Review a diff | the review line format above, sorted by file then line, then a count per severity | `no issues` plus what was read |

Spot-check any empty reply before relying on it (`../../context-efficiency.md` § 6. Delegation economics). A short report is only useful if its line numbers are exact; ask helpers never to estimate a range or cite past the end of a file.
