# React performance: worked fixes, measuring, and a scanner

Read when a React or Next.js change touches data loading, bundle size or render cost and the rules in `../../react.md` need an example, a number or a quick scan.

Written by us on the topics of vercel-labs/agent-skills (React best practices and composition, commit 5a37a63). That repository ships no LICENSE file, so none of its text was read into or used in these files. The rule list itself lives in `../../react.md`; these files add depth.

- `worked-fixes.md`: before-and-after code for the highest-payoff rules (waterfalls, boundaries, bundle, re-renders, lists), each with the number that proves it.
- `measuring.md`: how to get that number: build output, bundle analyzer, request timing, the React Profiler, and Web Vitals in the field.
- `react-scan.md`: `react_scan.py`, a pattern scanner for common slow or fragile code, what each flag means and how to read false positives.

Not covered, with reasons: `later.md`.
