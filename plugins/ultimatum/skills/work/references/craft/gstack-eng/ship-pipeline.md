# Ship pipeline: from a finished branch to a pushed release

Read when the user asks to ship a branch and the project has its own release steps (a version file, a changelog, a docs pass), and you need the order of work and a rule for every stop.

Builds on `../../release.md`, from authorization (`../../release.md` § 0) to the readiness report (`../../release.md` § 8). This file adds the order, the resume record and the version decision. Pushing, tagging and publishing still need the user's own words (Ultimatum rule 3).

## 1. Order

1. **Bring in the base.** Merge or rebase the base branch first, then test. A simple conflict is resolved and noted; a conflict in logic stops for the user.
2. **Test and review.** Run the project's suites (`../../release.md` § 2) and a review (`pre-landing-review.md`). Only three things block: a failing test, something that would break production, or a risk of losing data or leaking a secret. Everything else goes in the notes.
3. **Prepare the release.** Version (§ 3 below), changelog, backlog file, docs (`docs-release.md`).
4. **Commit in steps.** See § 4.
5. **Verify what will ship.** Freeze the content, then rerun every check whose inputs changed since it last ran (§ 5).
6. **Push**, with the user's yes.

## 2. Keep a resume record

Write a small record in `.ultimatum/` as you go: the base commit, the reviewed tree (`git rev-parse HEAD^{tree}`), each check with its command, exit code and the tree it ran on, the version decision, docs done, and the next step. A run that is cut off resumes from the record instead of starting over. `ult handoff write` at the end.

## 3. Version decision

First read the state, comparing the version file on the branch with the base:
- **fresh**: same as base, nothing bumped yet;
- **already bumped**: differs from base by one step; do not bump again;
- **drift**: differs by more than one step, or the changelog and version disagree; stop and ask;
- **no version file**: do not invent one.

Then pick the level from the diff: a tiny fix gets the smallest step the scheme has; a normal fix gets patch; a new feature gets minor; a breaking change gets major. Minor and major need the user's yes. If other open branches have already claimed the next number, take the one after and say so. Follow the project's own rules where they exist (this repo's are in `CLAUDE.md`).

## 4. Commits a bisect can use

- Group each change with its tests and config; a migration may stand alone.
- Order so each commit builds and passes: shared code first, then models and services, then the parts that use them.
- A small change (under ~50 lines in under 4 files) can be one commit.
- Subjects say what changed for a user. Never make an empty commit. Version and changelog go in a last release commit.

## 5. Verify the frozen candidate

- A check counts only if it ran on the exact content being shipped. Compare tree hashes: same tree, the result stands; different tree, rerun.
- Only release metadata (the version line, the changelog entry) may change after a check without forcing a rerun.
- A check that reports zero tests run is a failure, not a pass.
- If the test count cannot be read, keep the exit code and say "count unavailable".
- Any content change during this step restarts it.
- List every check with command, exit code and test count. If a gate was loosened on this branch, say which and why (`pre-landing-review.md` § 2).

## 6. Hand back

Version chosen and why, commits made, checks with exit codes, docs updated, notes for the PR, and the push command waiting for the user's yes.
