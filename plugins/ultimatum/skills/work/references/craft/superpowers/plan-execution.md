# Carrying out a written plan

Read when you have an approved plan from `plan-writing.md` and are about to build it, here or through helpers, or when you resume one after a break. Dispatch rules, briefs, fix-round caps and the final two-axis review are in `../../orchestration.md`; this file adds what that one leaves out.

## Here or delegated

| | Inline (you build each task) | Delegated (fresh helper per task) |
|---|---|---|
| Context | grows with every task | stays small; each helper starts clean |
| Speed | no hand-off cost | pays for a brief and a review per task |
| Good for | under five tasks, tightly coupled files | many tasks, separate files |

Either way, the check after each task is yours: re-run its test command and read its diff.

## Before task 1: pre-flight

Read the whole plan once and list every place where two instructions pull against each other: the header says "no new dependencies" but Task 4 adds one; Task 2 produces `load()` and Task 5 consumes `read()`. Put them in one table, with your proposed resolution, and settle them with the user in one message before you start. Anything you can resolve yourself without changing the result goes into the ledger as a ruling (below).

## The ledger

Keep a plain file at `.ultimatum/plans/<slug>.ledger.md`. Its first line names the plan file and its commit, so a later session can tell whether the ledger still belongs to that plan. Then one line per finished task:

```text
plan: .ultimatum/plans/2026-11-26-importer.md @ 4f2c1a9
Task 1: complete (commits 4f2c1a9..b81e03d, tests: python3 -m pytest tests/test_model.py -q -> 6 passed)
Task 2: complete (commits b81e03d..c0d77e2, tests: python3 -m pytest tests/test_row.py -q -> 9 passed)
Ruling: Task 3 file name - plan says utils.py, repo uses helpers.py; used helpers.py - cost if wrong: one rename
Deferred: Task 2 minor - error message wording, reviewer note 3
```

**Resuming.** Read the ledger and `git log --oneline` since the first commit it names. A task counts as done only when both agree and its test command still passes now. Re-run that command before you build on it.

## Rulings

When the plan is silent or a little wrong and you can decide without changing what the user gets, decide, keep going, and log one line: `Ruling: what - why - cost if wrong`. Do not stop to ask for these.

Stop and ask only for:

1. something that cannot be undone (data deletion, a migration on shared data, a force push);
2. anything touching auth, secrets, permissions or other security boundaries;
3. a side effect outside the repo (a network call to a real service, a message sent, money spent);
4. a plan so broken that every way forward is a guess.

## What "task done" means

A task is done when all of these hold, and you checked each one yourself:

- its test command ran this session, with the expected result and exit code quoted in the ledger;
- the diff touches only the files the task names, or each extra file has a ruling;
- the names in its Produces line exist with the stated signatures;
- the commit is made and its hash is in the ledger.

A helper's "done" is a claim, not a result. Re-run the command and read the diff (`done-claims.md`).

## The final review

After the last task, review the whole range in one go.

- **Range.** Use the commit before Task 1 as the base, recorded in the ledger, not `HEAD~1`: that only shows the last task.
- **Reviewer.** A fresh read-only helper on the strongest model available, with the design, the plan and `git diff BASE..HEAD`. Brief as in `review-rounds.md`.
- **Grade by effect on the user.** Treat the design as a statement of intent, not a contract to match word for word. Re-grade each finding by what a user of the change would hit: a wrong result is Critical, a confusing error message is Minor, whatever the reviewer called it.
- **Fixes.** Critical and Important findings get one fix pass. Each fix starts with a test that fails on the current code and passes after. Minor findings go into the ledger as `Deferred:` lines.
- **Limits.** Things the reviewer could not judge (performance under load, a platform they could not run) go into a "not judged" list in the report, not into silence.

## The closing message

Report in this order: what was built; the checks you ran with exit codes; the rulings you made (copied from the ledger); the deferred minors; what was not judged; what needs the user.

## Small tricks that save rounds

- **Batch same-shape edits.** Ten one-line renames across ten files are one task for one helper, not ten.
- **Pick the model by turns, not price.** A cheap model that needs four fix rounds costs more than a stronger one that needs one. For tasks with judgement in them, start a tier up.
- **Fix loops** follow the caps in orchestration (`../../orchestration.md` § 6); when a helper keeps failing the same check, change the brief or the model, not just the wording of your complaint.
