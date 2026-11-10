# Evaluating Ultimatum itself

Goal: show with evidence whether a change to Ultimatum's skill, references, agents, or scripts makes behavior better, and never claim improvement (including token or speed savings) without a measured baseline. Use this when asked to test, tune, or measure the plugin. Facts about the CLI come from `research/platform.md`.

## 1. Static gates (free, run first, every change)

1. `claude plugin validate ./plugins/ultimatum --strict` exits 0 with no errors or warnings. Marketplace root: `claude plugin validate . --strict`. Use `--json` in CI.
2. `claude plugin details ultimatum`: read the projected token cost. Always-on cost (skill name + description, agent descriptions) must stay near its recorded budget; the router's on-invoke cost must not grow without cause. Record the numbers before and after your change.
3. Size guard: `SKILL.md` stays small (under ~500 lines and well under 20 KB, because compaction truncates re-attached skills). Occasional material belongs in `references/`.
4. Reference hygiene: every reference named in the route table exists; each starts with a purpose line; every `ult` command shown exists (`python3 plugins/ultimatum/scripts/ult <cmd> --help`).
5. Script tests: run the stdlib unit tests for `scripts/` via `ult run`; quote counts (ZERO_RUN is a failure).
6. Frontmatter: description leads with the trigger condition, one branch per genuine use, within the length limit; allowed keys only.

## 2. Behavioral evals (paid; run cheap first)

Command shape: `claude plugin eval plugins/ultimatum ...`
- Free scaffolding: `claude plugin eval init --bare <name>` creates `evals/<name>/prompt.md` and `graders/criteria.md`. Avoid the interactive `init` unless the user accepts the token cost.
- Cheap iteration: `claude plugin eval plugins/ultimatum --trust-plugin --ablation none --runs 1 --max-cost-usd 1 --model haiku --no-publish --json out.json`. Put the target before `--json`.
- Real comparison: default `--ablation with-without` (with-plugin arm vs baseline arm without it), `--runs 3` or more, `--threshold` set before running, `--max-cost-usd` set, `-j` modest.
- Exit codes: 0 pass, 1 below threshold or load or API error, 2 cost ceiling hit with partial results (treat as incomplete, not as pass).
- Results land in `evals/results/<timestamp>/` (gitignore it). Keep `aggregate-result.json` as evidence.
- Evals run in an isolated workspace with only the plugin under test, so they also prove the core works with no other packs installed.
- Baseline arm cannot dispatch plugin agents (`Agent type 'x:y' not found` is expected there); it measures what plain Claude does.
- Allow tools explicitly for cases that need them (`--allow-tools "Bash(python3 *)"`); default is read-only. File fixtures use `case.yaml` `context.scaffold_script` with `--scaffold`.

## 3. Case design

One directory per case: `prompt.md` (frontmatter + realistic prompt) and `graders/*.md`.
1. **Realistic prompts**: casual wording, file paths, partial context, the way a user types, not "please use the work skill". A prompt Claude would handle identically without the plugin proves nothing.
2. **Cover the routes**: at least one case per route in the SKILL.md table, plus overlay triggers (auth change, RLS, deploy settings).
3. **Near-miss negatives**: prompts that look related but should not use the heavy path (a one-line typo fix should not spawn a plan; a general question should not trigger `release.md`). Grade that the skill's extras did **not** happen (`tool_used` with `max: 0`, `regex` with `match: not_contains`).
4. **Discriminating assertions**: each assertion must fail for a plausible wrong-but-confident answer. Prefer free graders (`regex`, `tool_used`, `tool_order`, `file_exists`) for mechanical facts: test was run before the claim, the RED run precedes the edit (`tool_order`), the file exists with the right content (`file_exists` + `llm` on `files`/`{source: file}`). Use `llm` graders for judgment (root cause stated, assumptions disclosed) with a rubric that names pass and fail evidence.
5. **Skill-fired indicator**: `tool_used` on `Skill` with `input_match` for the work skill. Under with-without ablation it is an indicator only, not scored.
6. **Pressure scenarios** for discipline: prompts that tempt skipping evidence ("just say it's fixed", "skip the test, I'm in a hurry", a failing CI where the quick fix is deleting a test). Pass = the discipline holds.
7. **Held-out set**: write cases before tuning; keep roughly 40% unseen by whoever edits the references. Choose changes by held-out results, not by the cases you tuned on.
8. **At least 3 runs per arm** per case (more when variance is high). Single runs are anecdotes.
9. Grader sanity: feed a known-good and a known-bad output through each grader (where deterministic) and confirm verdicts differ. Flag assertions that always pass, always fail, or have high variance.

## 4. Measuring

Record in this order, and do not skip ahead:
1. **Correctness first:** case pass rate per arm (mean and sample stdev across runs), which assertions moved.
2. **Quality failures:** reasons from failed runs (quote the transcript or grader line).
3. **Then cost:** tokens, wall time, tool calls, cache read/creation tokens, and **subagent usage** (workers, reviewers, scouts, each model and their tokens). A change that shrinks main-context tokens by delegating is not a saving until total usage is counted.
4. Capture duration and tokens when each run finishes; they cannot be recovered later.
5. Report the delta between arms with variance (mean ± stdev, n runs). If the difference is within the spread, say "no measurable difference".

## 5. Regression gates

- Classify against the previous recorded baseline: green to red counts as a regression; red to red is unchanged; new failing cases are new; flakes within the baseline's own noise are classified, not blamed.
- List dimensions that could not be run (no network, no cost budget). Never silently drop them.
- A change may merge when: static gates pass, no case regressed beyond noise, no near-miss negative started failing, and always-on token cost did not grow without justification.
- Fix attempts for a regression: at most 3, each must shrink the failing set.

## 6. Claims policy

- No statements like "saves X% tokens", "faster", or "more accurate" without a run pair (before/after or with/without), the run count, the variance, and the command that produced it. Put the aggregate path in the report.
- Do not report estimates as measurements. Do not generalize from one repo or model.
- A bar written in the same change as its result is suspect: set the threshold and arms before spending, and say so in the report.
- Cheap dry run first, tiny priced pilot second, full run only after both.

## 7. Report

```
Change evaluated: <commit/diff summary>
Static: validate <exit>, details <always-on tokens before -> after>, script tests <n ran>
Evals: <command>, cases <n>, runs/arm <n>, ablation <mode>, cost <usd>
Correctness: <arm: pass rate mean ± sd> ; regressions: <list or none>
Cost (secondary): tokens, time, subagent usage per arm
Not measured: <list>
Verdict: <ship | hold | inconclusive> with reason
```

## 8. Changing references: the minimum loop

1. Run the case set on the current plugin (baseline, saved result).
2. Identify the failing behavior and quote the transcript lines that show the shortcut or mistake.
3. Edit the single reference that governs it, adding the smallest rule that closes that gap.
4. Rerun the same cases with fresh runs; compare per §4 and §5.
5. If a rule is not changing any graded behavior across runs, remove it: unused instructions only cost context.
6. Verification runs happen in a fresh session, not the one that wrote the change.

## 9. Common eval mistakes

- Judging by one lucky run.
- Prompts that name the skill, which tests invocation but not usefulness.
- Graders that check a surface string and pass confident wrong answers.
- Comparing arms with different tools allowed.
- Reading ablation results from a case where the baseline arm cannot use plugin agents without noting it.
- Reporting token savings from the main context while ignoring subagent tokens.
