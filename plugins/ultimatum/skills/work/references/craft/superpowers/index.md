# Superpowers craft: deeper notes on the build loop

Read when the build loop in the router needs more than the base files give: shaping a request through conversation, writing or running a plan, deeper debugging moves, judging a test, a review round, or closing a branch.

Rebuilt from the ideas in obra/superpowers at commit 22f0b46 (MIT). All wording and code here are ours. The base rules live in `../../feature-planning.md`, `../../tdd.md`, `../../debugging.md` and `../../orchestration.md`; these files only add what those leave out.

- `shaping-conversation.md`: turning a vague request into a design the user approved: first message shapes, open questions before options, playback, the approaches message, the builder check and the build gate.
- `plan-writing.md`: a plan someone with no context can run: header, interfaces per task, what a step must hold, and the five self-review checks.
- `plan-execution.md`: running a plan yourself or through helpers: the progress ledger, the completion contract, rulings, the four stops, and grading the final review.
- `debugging-moves.md`: tracing a bad value back to where it was made, guards at several layers, waiting on a condition instead of a sleep, and finding the test that leaves junk behind.
- `test-judgement.md`: whether a test earns its place: name the break, derive the expected value by hand, mock rules and the mutation pass.
- `review-rounds.md`: asking for a review with a clean brief, and taking review feedback without agreeing on reflex.
- `done-claims.md`: which evidence each kind of "done" needs, and the wording that gives away a claim nobody checked.
- `branch-close.md`: checking for an existing worktree, setting one up safely, and the end-of-branch choices with their cleanup rules.

Scripts: `../../../../../data/craft/superpowers/` (`wait_until.py`, `find_polluter.py`).

Not rebuilt, with reasons: `later.md`.
