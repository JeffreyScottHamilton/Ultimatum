# Writing a skill

Goal: a skill that triggers on the right requests, loads only what it needs, and beats no skill on realistic tasks. Used by the `skill-author` and `skill-eval` routes. How to measure Ultimatum itself is in `skill-evaluation.md`.

## 1. Capture intent

- One sentence: what the skill enables and for whom.
- Trigger cases: the requests that should load it, and the close ones that should not.
- Output: what a good result looks like, and whether a grader can check it (a file, a command's exit code, a fact that must appear) or only judge it.

## 2. Test prompts first

- Write 8 to 12 realistic prompts before drafting the body. Vary the wording: casual, partial paths, typos, pasted context.
- Half should trigger the skill. Half should not. Near misses matter most.
- Give each prompt a check: a command that must pass, a file that must exist, a fact that must appear, or a rubric line a grader can apply.
- Keep prompts beside the skill source, not in the shipped plugin, when they are large.

## 3. The description is the trigger

- The description is always in context; the body loads only on use. Put every "when to use" fact in the description.
- Lead with the user's situation, then the action. Use the nouns and verbs users actually type.
- Add an exclusion only when a near miss would otherwise trigger wrongly.
- Check the description against the near-miss prompts before touching the body.

Held-out trigger tuning with a split and repeated runs: `craft/anthropic-method/trigger-tuning.md`.

## 4. Progressive disclosure

- Body: the workflow as numbered steps, plus the rules that always apply. Short enough to read in one pass.
- References: detail, long tables, per-variant notes. Each one states when to read it.
- Scripts: take over repeated or fragile work so the model does not rewrite it each time. Keep their output short.
- One level deep: the body links to references; references do not link onward.

## 5. Size budgets

- The entry file stays well under 20 KB and 500 lines in this plugin. Move the rest into references.
- Frontmatter uses only allowed keys. The description is short, since it costs tokens on every session.
- Measure with `wc -c` on each file. Report the on-invoke cost: body plus the files a typical run reads.

Field limits, variant layout and a frontmatter lint: `craft/anthropic-method/skill-frontmatter.md`.

## 6. Compare with and without

- Run each test prompt twice in the same setup: once with the skill, once without (the baseline). Same model, same tools, same starting state.
- Grade blind where you can: the grader sees the outputs, not which arm made them.
- Record pass rate, failed checks, time and tokens per arm. Repeat noisy cases at least three times.
- Ship only if the skill wins on the checks that matter and loses none of the must-pass checks.

Iteration folders, baselines and grading records: `craft/anthropic-method/eval-workspace.md`.

## 7. Iterate

- Read failing transcripts, not only the scores. Find the cause in the instructions, fix it, and re-run the same prompts.
- Generalise from failures: write one rule that covers a class of mistakes, not one line per prompt.
- Delete text that did not change any result. Lean instructions beat long ones.
- Stop when the next change moves the score by less than run-to-run noise.
- Keep a few prompts unseen during tuning, and run them last as a check against overfitting.

## 8. Originality

- Write the skill's text yourself. Do not copy example or upstream skill text, even from a permissive licence. Credit ideas, not wording.
