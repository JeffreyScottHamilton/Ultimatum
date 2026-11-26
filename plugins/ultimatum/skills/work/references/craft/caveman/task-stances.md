# Task stances: investigate, patch, build lean, refactor, migrate, verify

Read when a coding task clearly fits one narrow stance (find the cause only, fix one bug, build the smallest complete feature, restructure without changing behaviour, migrate data or an API, or prove a change and stop) and you want the short rule set for it.

These are compact versions of rules covered in depth elsewhere: debugging in `../../debugging.md`, test-first in `../../tdd.md`, planning and slicing in `../../feature-planning.md`, schema and data changes in `../../data-and-infra.md`. Each stance below adds only what those files leave implicit: what to do, and when to stop.

## The simplicity ladder

Before writing new code, take the first rung that works without bending the design:

1. The code already does it: call what is there, or leave the code as it is.
2. A layer, type or helper already owns this kind of thing: extend it there.
3. The standard library, platform, database or an installed dependency does it: use that.
4. A small new piece fits the current structure: put it where the rule it enforces belongs.
5. The structure blocks a clean change: do the refactor the task needs, as its own step.

Judge by total complexity and clear ownership, not by lines changed. A wider coherent change beats a cramped patch that duplicates a guard in the wrong place.

Leave out what nobody asked for: extra modes, plug-in points, interfaces with one implementation, config for fixed values, new services. Simplicity never removes input validation at a trust boundary, authorization, error handling, data-loss protection, accessibility, rollback safety or compatibility. When the change touches any of those, follow `../../security/secure-implementation.md`.

## Investigate only

- Keep what you saw apart from what you think caused it.
- Trace the inputs, the state changes and who owns each step.
- Rank guesses by evidence and by how cheaply each can be ruled out.
- Do not edit product code until one mechanism explains everything you saw.
- **Stop** when you can name the cause, or the exact thing blocking you. Report the cause and the proof; make no fix unless the task asked for one.

## Fix one bug

- Reproduce first when that is cheap; otherwise capture the strongest evidence you can.
- Change the narrowest layer that owns the wrong behaviour.
- Leave unrelated code and the user's own changes alone: no drive-by renames or cleanups.
- Add only the regression test this bug needs (`../../tdd.md` § 5. Regression tests (bug fixes)).
- **Stop** when the failure is gone and the regression test passes along with the nearest wider suite.

## Build the smallest complete feature

- Write the acceptance checks and the non-goals first, from the request and the repo.
- Trace from the entry point through each layer that owns a rule.
- Deliver a working path end to end across those layers; do not force it into one file.
- Add a dependency, config, service or migration only when acceptance needs it, and say what it costs.
- **Stop** when the acceptance checks pass. Report only omissions that matter.

## Refactor without changing behaviour

- Fix the boundary first: which behaviour must not change, and which check proves it. Run that check before editing.
- Keep feature work out of the refactor.
- Shift a single owner boundary per step; each intermediate state must build and pass.
- Keep public interfaces, error behaviour, ordering and compatibility unless the task says otherwise.
- **Stop** when the same check passes and the structure asked for is in place.

## Migrate data, a schema or an API

- Map the current readers, writers, data shape and compatibility window before editing.
- Write the forward path and the rollback path.
- Sequence expand, migrate, verify, contract. Old and new must both work while a rollout overlaps.
- Make retries safe to repeat and partial failure visible.
- Destructive steps (dropping a column, deleting old data) are separate and need the user's yes.
- **Stop** after the stage that was asked for; never run the contract step on your own.

## Verify and stop

- Turn the acceptance conditions into the smallest set of checks that proves them.
- Reuse a result only if the repository has not changed since it ran.
- Run focused checks before wide ones.
- Report each check as exactly one of: **passed**, **failed**, **unavailable** (the tool or service is not here), or **blocked** (something else must happen first). Quote the command and exit code.
- Do not edit product code unless the request includes fixes. Do not add polish or extra tests once the criteria pass.
- **Stop** as soon as the proof is complete.
