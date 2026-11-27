# Coding discipline: think, keep it small, touch only what was asked, prove it

Read when choosing which coding-discipline file to open: before starting a change you are unsure about, when a diff is growing, or when "done" has no test yet.

Written by us on the topics of multica-ai/andrej-karpathy-skills (commit 2c60614). That repository ships no LICENSE file, so none of its text was read into or used in these files; the ideas are common engineering practice and the wording, examples and script are ours.

- `think-first.md`: what to settle before the first edit: assumptions said out loud, the two-readings test, when to ask and when to pick, and when to push back.
- `smallest-change.md`: the size test for new code, what not to build yet, and a worked before-and-after.
- `surgical-diff.md`: every changed line traces to the request, style matching, cleaning up only your own leftovers, and `diff_scope.py`, a checker for drive-by edits.
- `checkable-goals.md`: turning a request into a check that fails now and passes when done, plans written as step and check, and when to stop looping.

Not covered, with reasons: `later.md`.
