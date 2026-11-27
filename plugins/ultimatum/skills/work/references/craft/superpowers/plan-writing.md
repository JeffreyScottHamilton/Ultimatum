# Writing a plan someone else can build from

Read when an approved design has to become a step-by-step plan, especially one that a helper or a later session will carry out without your memory of the talk. The spec itself, slices and tickets are in feature planning (`../../feature-planning.md` § 6) and its slices section; this file is how the plan document is built.

## Who reads it

Write for a capable engineer who has never seen this repo, does not know the domain, and will not ask you anything. They can follow exact steps; they cannot read your mind. Every file path, interface name and test command must be spelled out.

## Before the first task

1. **Scope check.** If the design covers several independent subsystems, stop and split: one plan per piece that works and can be tested on its own. Say which plan comes first.
2. **File map.** List each file to create or change and the one job it has. Files that change together sit together. Follow the repo's existing layout; split a file only when your change would make it unwieldy.
3. **Where it goes.** The project's plans folder if it has one, else `.ultimatum/plans/<date>-<slug>.md`.

## The header

Start the plan with:

| Field | Contents |
|---|---|
| Goal | one sentence |
| Shape | two or three sentences on the approach |
| Stack | languages, libraries, test runner |
| Design | path to the approved design doc |
| Rules for every task | constraints that apply everywhere (style, no new dependencies, error format), each stated once |
| Review focus | see below |

**Review focus.** Name up to five input classes no test covers yet, ranked by how likely they hide a bug: empty values, bad encodings, boundaries, odd orderings, concurrent calls. For each one, add a test to the task that owns that code. This is where you think about hostile input; when a class touches parsing, paths, auth or permissions, apply the security overlay (`../../security/secure-implementation.md`) and make its test a negative one that fails without the guard.

## Sizing a task

A task is the smallest unit that has its own test cycle and that a reviewer could reject without rejecting its neighbours. Each task ends in a commit.

- Too small: "add the import", then "add the function". Neither stands alone.
- Too big: "build the importer". Nobody can review it in one sitting.
- About right: "parse one CSV row into a `Record`, with tests for quoted commas and an empty last column".

Each step inside a task is one action of a few minutes: write the failing test, run it and see it fail, write the code, run it and see it pass, commit.

## What each task holds

```markdown
### Task 3: Parse a CSV row into a Record

Files: create src/importer/row.py; change src/importer/__init__.py; test tests/test_row.py
Consumes: Record from Task 2 (src/importer/model.py)
Produces: parse_row(line: str) -> Record, raises RowError with the column number

- [ ] Test: a row with a quoted comma gives two fields, not three
- [ ] Run `python3 -m pytest tests/test_row.py -q`; expect 1 failure naming parse_row
- [ ] Write parse_row to pass it
- [ ] Run the same command; expect all pass
- [ ] Commit: "importer: parse one CSV row"
```

The Consumes and Produces lines are the contract between tasks. A later task may only use what an earlier one produced, under the same name and signature.

## Clear, not complete

A step must leave no doubt about what to do. It does not need the whole body of the code.

- Give the signature, the behaviour and the edge cases; leave the body to the builder unless one line of code says it better than a sentence.
- Give the exact test command and what output to expect.
- When a test needs a specific case, describe the case (input, expected result), not a finished test file.

These count as plan failures, and you fix them before handing over:

- "add error handling", "validate as needed", "handle edge cases", with no cases named;
- "same as Task N" instead of the steps;
- a placeholder or a name that no task defines.

## Read it back before handing over

Go through the plan with these checks, fixing as you go:

1. **Design coverage.** Every requirement in the design points to a task. List any that do not.
2. **Step scan.** No vague steps from the list above.
3. **Name match.** Every name in Consumes exists, with the same spelling and signature, in some earlier Produces.
4. **Review focus.** Each input class has its test in an owning task.
5. **Proportion.** The longest task is not three times the length of the median; split it if so.

## Handover

Offer the user two ways to run it and recommend one:

| Way | Fits when |
|---|---|
| Here, task by task, with a check-in after each batch | few tasks, the user wants to watch |
| Delegated, one fresh helper per task with a review after each | many tasks, independent files |

Both follow `plan-execution.md`.
