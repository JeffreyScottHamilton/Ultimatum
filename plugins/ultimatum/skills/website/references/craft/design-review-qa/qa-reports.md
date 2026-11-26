# QA report formats

Read when writing the output of a QA run: the folder layout, the browser report, the functional report, and the rules for a report-only (qa-only) run.

## Folder

```
.ultimatum/qa/<timestamp>/
  report.md          the human report
  baseline.json      see qa-health-score.md
  evidence/          screenshots, logs, command output (redacted)
  probes.md          numbered probe notes
```

Everything in `evidence/` is named by finding id (`F-003-after.png`). A finding without evidence is marked "not reproduced".

## Browser report

1. **Header:** target, date, mode, duration, pages visited, tool.
2. **Verdict and score:** one sentence, the health score, the three fixes to do first (`qa-health-score.md`).
3. **Findings**, in severity order. Each: id, title, severity, category, page, steps, expected, actual, evidence.
4. **Console and network summary:** new errors, failed requests, with counts.
5. **Not tested:** pages skipped and why (login wall, destructive, out of time).
6. **Regression block** (only when a baseline exists): fixed, new, open, score change.
7. **Top three** repeated at the end, as a short action list.

## Functional report

1. **Header:** surface, target, fixtures used, commands, time limits.
2. **Charters:** one per tested contract (`qa-modes-and-loop.md`).
3. **Results table:** contract, probe, pass, fail or not run, evidence file.
4. **Findings** as above, with the smallest reproduction.
5. **Left behind:** anything the run started or wrote that still exists.

## Report-only runs

- The report is the only deliverable. Do not change source, config or fixtures you do not own.
- Evidence first: every claim points to a file. Do not guess at root cause; say "likely" and why.
- Put timing fields in the header: start, end and the time limit that applied.
- Mark every probe that was refused, blocked or out of time as "not run", never as a pass.
- End with "Ready to fix?" style hand-off lines only as a plain list of the findings worth fixing, ordered by severity.

## Summary for a pull request

Three lines is enough: the score before and after (if known), how many findings by severity, and anything still open that a reviewer should see. Link the report path. Claim only what the run did.

## Writing style

Plain words. Steps a stranger can follow. One finding per root cause. No filler findings. No screenshots that do not show the problem; crop or annotate the area.
