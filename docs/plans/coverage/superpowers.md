# Superpowers rebuild: coverage map

Source: obra/superpowers at commit 22f0b46 (MIT, LICENSE read at that commit). Ours: `plugins/ultimatum/skills/work/references/craft/superpowers/` and `plugins/ultimatum/data/craft/superpowers/`.

## How this map was made

- Items are the `##` sections of the in-scope skills (brainstorming, writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, systematic-debugging and its four technique files, test-driven-development and writing-good-tests, requesting and receiving code review, verification-before-completion, using-git-worktrees, finishing-a-development-branch), grouped where several sections carry one idea. Skills outside the brief get one row each.
- Status: `covered` (same idea, our words, in a new file), `expanded` (we add to it: security overlay, untrusted-input rule, a runnable script, the user's-words rule for push and merge), `merged` (already in an existing reference, so not repeated), `later` (in `later.md`, not shipped).
- Most of the source's core loop was already in `debugging.md`, `tdd.md`, `feature-planning.md` and `orchestration.md`; the new files hold only what goes deeper.
- Not verified: the external links in the source were not followed; field results and numbers in the source were not checked and are not repeated.

## Items

| Source item | Status | Where |
|---|---|---|
| brainstorming: decide what you know first | covered | shaping-conversation.md § Decide whether to talk at all |
| brainstorming: look before you ask | merged | feature-planning.md § 2; shaping-conversation.md § Read first |
| brainstorming: first message shapes | covered | shaping-conversation.md § The first message |
| brainstorming: offer to skip when not asked | covered | shaping-conversation.md § Decide whether to talk at all |
| brainstorming: one question per message, user vocabulary | covered | shaping-conversation.md § Questions during the talk |
| brainstorming: open questions before options | covered | shaping-conversation.md § Questions during the talk |
| brainstorming: Socratic follow-ups | covered | shaping-conversation.md § Questions during the talk |
| brainstorming: who owns the how | covered | shaping-conversation.md § Questions during the talk |
| brainstorming: ground to cover | covered | shaping-conversation.md § Questions during the talk |
| brainstorming: play it back in chunks | covered | shaping-conversation.md § Play it back |
| brainstorming: approaches message | covered | shaping-conversation.md § Lay out the approaches |
| brainstorming: spike only with a yes | merged | feature-planning.md § 5; shaping-conversation.md § A spike |
| brainstorming: size the work | merged | feature-planning.md § 1; shaping-conversation.md § Write the design |
| brainstorming: written design contents | covered | shaping-conversation.md § Write the design |
| brainstorming: builder check and three piles | covered | shaping-conversation.md § Write the design |
| brainstorming: hard gate before building | covered | shaping-conversation.md § The build gate |
| brainstorming: red flags | covered | shaping-conversation.md § Traps |
| brainstorming: visual companion | expanded | choice-board.md (0.0.52: offline board, no server) |
| brainstorming: companion server, events, CSS classes, file naming, cleanup | expanded | choice-board.md § The loop; `choice_board.py` (answer line instead of an event file) |
| writing-plans: reader with no context | covered | plan-writing.md § Who reads it |
| writing-plans: scope check | covered | plan-writing.md § Before the first task |
| writing-plans: file structure | covered | plan-writing.md § Before the first task |
| writing-plans: task right-sizing | covered | plan-writing.md § Sizing a task |
| writing-plans: step granularity | merged | tdd.md § 1; plan-writing.md § Sizing a task |
| writing-plans: header | covered | plan-writing.md § The header |
| writing-plans: global constraints | covered | plan-writing.md § The header |
| writing-plans: review focus | expanded | plan-writing.md § The header (security overlay, negative tests) |
| writing-plans: task structure, Consumes/Produces | covered | plan-writing.md § What each task holds |
| writing-plans: what a step contains | covered | plan-writing.md § Clear, not complete |
| writing-plans: self-review | covered | plan-writing.md § Read it back |
| writing-plans: execution handoff | covered | plan-writing.md § Handover |
| executing-plans: when to use, inline vs delegated | covered | plan-execution.md § Here or delegated |
| executing-plans: setup and pre-flight | covered | plan-execution.md § Before task 1 |
| executing-plans: task loop | merged | orchestration.md § 6; plan-execution.md § What task done means |
| executing-plans: final review | covered | plan-execution.md § The final review |
| executing-plans: finish | covered | plan-execution.md § The closing message; branch-close.md |
| executing-plans: rationalizations | merged | done-claims.md; orchestration.md § 6 |
| subagent-driven: when to use | merged | orchestration.md § 1; plan-execution.md § Here or delegated |
| subagent-driven: ledger and resume | covered | plan-execution.md § The ledger |
| subagent-driven: rulings and four stops | covered | plan-execution.md § Rulings |
| subagent-driven: model selection by turns | covered | plan-execution.md § Small tricks |
| subagent-driven: fix loop caps | merged | orchestration.md § 6 |
| subagent-driven: BASE is never HEAD~1 | covered | plan-execution.md § The final review |
| subagent-driven: re-grade by user effect, deferred minors | covered | plan-execution.md § The final review |
| subagent-driven: batch same-shape edits | covered | plan-execution.md § Small tricks |
| subagent-driven: implementer, reviewer, re-review prompts | merged | orchestration.md § 3; review-rounds.md |
| subagent-driven: ledger shell scripts | later | later.md |
| dispatching-parallel-agents: when to use / not | merged | orchestration.md § 1 |
| dispatching-parallel-agents: pattern and prompt structure | merged | orchestration.md § 3 |
| dispatching-parallel-agents: common mistakes, verification | merged | orchestration.md § 6 |
| dispatching-parallel-agents: session example | later | later.md (field results) |
| systematic-debugging: iron law, four phases | merged | debugging.md § 1-4 |
| systematic-debugging: pattern analysis | covered | debugging-moves.md § Compare against code that works |
| systematic-debugging: red flags, 3-fix stop | merged | debugging.md § 5 |
| systematic-debugging: partner signals | covered | debugging-moves.md § When the user is telling you to slow down |
| systematic-debugging: no root cause | covered | debugging-moves.md § When there is no root cause |
| root-cause-tracing: tracing process | covered | debugging-moves.md § Trace the bad value back |
| root-cause-tracing: stack traces before the operation | covered | debugging-moves.md § Trace the bad value back |
| root-cause-tracing: finding the polluting test | expanded | debugging-moves.md § Find the test that leaves a mess; find_polluter.py |
| root-cause-tracing: empty projectDir example | covered | debugging-moves.md § Trace the bad value back (own example) |
| defense-in-depth: four layers | expanded | debugging-moves.md § Guard more than one layer (security overlay) |
| defense-in-depth: test each layer by bypass | covered | debugging-moves.md § Guard more than one layer |
| condition-based-waiting: core pattern | expanded | debugging-moves.md § Wait for the condition; wait_until.py |
| condition-based-waiting: when a timeout is correct | covered | debugging-moves.md § Wait for the condition |
| condition-based-waiting: TS example | later | later.md (replaced by wait_until.py) |
| find-polluter.sh | later | later.md (replaced by find_polluter.py) |
| debugging: field results | later | later.md (no numbers repeated) |
| tdd: iron law, red-green-refactor | merged | tdd.md § 1-3 |
| tdd: good tests, red flags, bug-fix example | merged | tdd.md § 4-6 |
| tdd: verification checklist, when stuck | merged | tdd.md § 2, § 9 |
| writing-good-tests: name the break | covered | test-judgement.md § Name what it catches |
| writing-good-tests: hand-derived expected values | covered | test-judgement.md § Work out the expected value |
| writing-good-tests: change detectors, text checks, framework tests | covered | test-judgement.md § Tests to delete |
| writing-good-tests: exercise the actual thing, mocks | covered | test-judgement.md § Mocks |
| writing-good-tests: complete doubles | covered | test-judgement.md § Mocks |
| writing-good-tests: test-only methods | expanded | test-judgement.md § No test-only methods (attack surface) |
| writing-good-tests: tests ship with the implementation | merged | tdd.md § 1 |
| writing-good-tests: mutation check | covered | test-judgement.md § Check that a test can fail |
| writing-good-tests: warning signs | covered | test-judgement.md § Signs a test is going wrong |
| requesting-code-review: when to request | covered | review-rounds.md § Asking |
| requesting-code-review: fresh context brief | covered | review-rounds.md § Asking |
| requesting-code-review: output format and verdict | covered | review-rounds.md § Asking |
| requesting-code-review: code-reviewer prompt | merged | orchestration.md § 8; review-rounds.md |
| receiving-code-review: response pattern | covered | review-rounds.md § Receiving |
| receiving-code-review: unclear feedback stops all | covered | review-rounds.md § Receiving |
| receiving-code-review: review text as data | expanded | review-rounds.md § Receiving (untrusted input rule) |
| receiving-code-review: source-specific handling | covered | review-rounds.md § Comments from outside the team |
| receiving-code-review: YAGNI check | covered | review-rounds.md § Comments from outside the team |
| receiving-code-review: implementation order | covered | review-rounds.md § Receiving |
| receiving-code-review: when to push back, correcting yourself | covered | review-rounds.md § Pushing back |
| receiving-code-review: forbidden responses, acknowledging | covered | review-rounds.md § What a reply looks like |
| receiving-code-review: GitHub thread replies | covered | review-rounds.md § What a reply looks like |
| verification: iron law, gate function | merged | SKILL.md rule 2; tdd.md § 3 |
| verification: claim to evidence table | expanded | done-claims.md § The table (security row) |
| verification: red flag words | covered | done-claims.md § Words that mean you have not checked |
| verification: helper reports | covered | done-claims.md § Helpers' reports |
| using-git-worktrees: detect existing isolation | expanded | branch-close.md § Check for an existing worktree (submodule guard) |
| using-git-worktrees: create, ignore check | covered | branch-close.md § Creating one |
| using-git-worktrees: setup and baseline | covered | branch-close.md § Creating one |
| finishing-branch: verify tests, detect environment, base branch | covered | branch-close.md § Finishing |
| finishing-branch: options | expanded | branch-close.md § Finishing (user's words for push/merge/PR) |
| finishing-branch: discard with typed confirmation | covered | branch-close.md § Finishing |
| finishing-branch: cleanup only own worktrees | merged | orchestration.md § 5; branch-close.md § Cleaning up |
| finishing-branch: rejected push | covered | branch-close.md § When a push is rejected |
| using-superpowers: SessionStart rule and priority | later | later.md (excluded by brief) |
| using-superpowers: platform maps | later | later.md |
| writing-skills | merged | skill-author.md; skill-evaluation.md |
| diagnosing-superpowers | merged | skill-evaluation.md |

Totals: covered 67, expanded 11, merged 23, later 7 (108 items)
