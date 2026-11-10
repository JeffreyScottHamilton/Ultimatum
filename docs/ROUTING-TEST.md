# Routing test (claude plugin eval)

Independent dry-run of `/ultimatum:work` routing. Cases live in `plugins/ultimatum/evals/<case>/` (prompt.md + graders/*.md). All graders are free and deterministic (`tool_used`, `regex`). Each prompt ends with: "This is a routing dry-run: do not implement; state the route you chose and read the references you would use, then stop." Tools: Read, Glob, Grep, Skill. Empty workspace.

## Command

```
claude plugin eval plugins/ultimatum --trust-plugin --ablation none --runs 1 --model sonnet --max-cost-usd 4 --no-publish --json <scratchpad>/routing.json
```

Cost: **$1.10** (ceiling 4). Duration 182s. Cases passed: **15/16**. Each case ran once (runs: 1), so results are single samples.

Graders: `reads-X` = Read of references/X at least once; `no-X` = Read of X zero times; `no-agent` = Agent never called (omitted for large and sec-audit); `route-named` = last message contains the route name (case-insensitive).

## Results

| Case | Score | Failed graders | Graders (pass/total) |
|---|---|---|---|
| overlay-fires | 1.00 PASS | - | 5/5 |
| overlay-silent | 1.00 PASS | - | 6/6 |
| route-bug | 1.00 PASS | - | 7/7 |
| route-ci-pr | 1.00 PASS | - | 6/6 |
| route-data-infra | 1.00 PASS | - | 5/5 |
| route-discover | 1.00 PASS | - | 6/6 |
| route-feature | 0.83 FAIL | no-security-secure-implementation | 5/6 |
| route-handoff | 1.00 PASS | - | 6/6 |
| route-large | 1.00 PASS | - | 3/3 |
| route-optimize | 1.00 PASS | - | 6/6 |
| route-release | 1.00 PASS | - | 5/5 |
| route-sec-audit | 1.00 PASS | - | 5/5 |
| route-sec-fix | 1.00 PASS | - | 5/5 |
| route-sec-review | 1.00 PASS | - | 6/6 |
| route-small | 1.00 PASS | - | 7/7 |
| route-ui | 1.00 PASS | - | 7/7 |

All security reference files were checked before the run; `ls references/security/` showed change-review, coverage-model, full-audit, secure-implementation at start. The sec-fix and sec-audit cases still read `remediation.md` and `findings.md` (graders passed), so those files existed by run time.

## Harness notes (not plugin bugs)
- `input_match` is a YAML single-quoted regex: write `\.`, not `\\.` (the doubled form matched a literal backslash and failed everything on the first run).
- Inline `(?i)` is rejected by the regex grader; use `flags: i`.
- Two earlier runs were discarded for those two grader mistakes; the table is from the final run.

## Routing findings
1. **route-feature reads `security/secure-implementation.md` (1 of 16 cases failed).** Prompt: "Add CSV export to the reports page... which columns are included." Agent read feature-planning.md, tdd.md and also secure-implementation.md. Arguably correct (data export and file download are on the overlay list: "personal or confidential data exposure, file upload or download"), so this is likely my grader being too strict, not a skill bug. But it shows the overlay trigger list fires on any export or download with no data-sensitivity qualifier. Proposed wording in SKILL.md §2 overlay: change "file upload or download or paths" to "file upload, or download/export of user-specific or tenant data, or file paths built from input". Low severity; if you want exports of plain public data to skip the overlay, apply it.
2. No over-planning found: small, overlay-silent, bug, ci-pr, optimize, release, handoff, discover, data-infra, ui read none of feature-planning.md or orchestration.md and never called Agent.
3. Overlay fired on the auth/tenant small change (read secure-implementation.md) and stayed silent on the pure string utility (read nothing, 1 turn). Sec routes (review, audit, fix) loaded exactly their listed references.
4. No wrong-route reference loads, and no skipped-overlay case was observed.

## Limits
Single run per case at temperature default; routing is stochastic so a 15/16 here is not a guarantee. The negative graders only check Read of references, not whether the agent followed the advice. Only the prompts above were tried; borderline prompts (for example a bug in auth code, a UI task that adds a form with file upload) were not covered and are worth adding.
