# Eval workspace, grading and benchmark reading

Read when you run a with-and-without comparison of a skill and need a place to keep runs, a grading record, a blind comparison or a way to read the summary. The method is in `../../skill-author.md` (§ 6 and § 7) and `../../skill-evaluation.md` (§ 3 and § 4); this file adds the bookkeeping.

## 1. One folder per iteration

Keep runs beside the skill, not inside it, so they never ship:

```
<skill>-workspace/
  iteration-1/
    <case-name>/
      with_skill/run-1/  outputs/  grading.json  timing.json
      without_skill/run-1/ ...
  iteration-2/ ...
```

- Give each case a descriptive folder name (`csv-quoted-commas`, not `case-3`).
- A new iteration is a new folder. Never overwrite the previous one; the comparison needs it.
- Write timing (seconds, tokens) as soon as a run ends. Most runners report it once, in the completion message, and it is gone after that.

## 2. Which baseline

| Situation | Baseline arm |
|---|---|
| New skill | the same prompt with no skill loaded |
| Changing an existing skill | a saved copy of the skill before the change (`old_skill`) |
| Two candidate rewrites | each other, plus the old version |

Start every arm in the same turn so they share model, tools and starting state.

## 3. The grading record

One `grading.json` per run. Each expectation keeps three fields: its text, whether it passed, and the evidence (a quoted line, a file path and line, a command and exit code). `bench_summary.py` reads this shape.

```json
{
 "expectations": [
  {"text": "report quotes the test command and its exit code",
   "passed": true, "evidence": "out.md:12 `pytest -q` exit 0"}],
 "timing": {"seconds": 41.2, "tokens": 18300}
}
```

A pass with no evidence counts as a fail. The summary script lists any pass with an empty evidence field.

## 4. Three reviewer roles

Each role is a separate reader with no stake in the result. Where the host has no subagents, skip the blind comparison and say so.

1. **Grader**: checks each expectation against the outputs. The burden is on the output: an expectation passes only when the evidence is on the page, not when it is plausible. It also pulls out claims the output makes on its own ("all tests pass") and checks them, and it notes expectations so loose that a wrong answer would pass them.
2. **Blind comparator**: gets two outputs labelled A and B, never which arm made them. Scores each on content (correct, complete) and on form (organised, usable), 1 to 5, and names a winner or a tie with a one-line reason.
3. **Post-hoc analyst**: after the labels are revealed, reads both transcripts to say why the winner won. Did the losing run ignore an instruction, misread one, or hit a gap the skill never covers? Each suggestion gets a priority (high, medium, low) and names the line in the skill to change.

## 5. Reading the summary

```
python3 plugins/ultimatum/data/craft/anthropic-method/bench_summary.py <skill>-workspace/iteration-2
```

It prints pass rate as mean ± sample standard deviation per arm, mean time and tokens, then flags:
- an assertion that passes in every arm: it does not discriminate, so it proves nothing about the skill; drop or sharpen it;
- an assertion that fails in every arm: usually a broken assertion or an impossible task;
- an assertion that passes in some runs of one arm: flaky; add runs before reading the delta.

When writing up, separate what the numbers show from what you think explains them, and put cost beside quality: a skill that adds 2 points of pass rate for twice the tokens is a trade, not a win. If the arms overlap within their spread, say "no measurable difference" (`../../skill-evaluation.md` § 6).
