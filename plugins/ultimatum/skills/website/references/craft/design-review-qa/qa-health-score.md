# QA health score, baseline and framework notes

Read when scoring a QA run, writing or comparing `baseline.json`, or when the site's framework changes what a "bug" looks like.

## Score

Score each category 0 to 100, then take the weighted sum.

| Category | Weight |
|---|---|
| Functional | 20% |
| Accessibility | 15% |
| Console | 15% |
| UX | 15% |
| Links | 10% |
| Performance | 10% |
| Visual | 10% |
| Content | 5% |

Each category starts at 100 and loses points per finding in it: 25 for critical, 15 for high, 8 for medium and 3 for low. It never goes below 0.

Two categories use counts instead:

- **Console:** 0 errors = 100, 1 to 3 = 70, 4 to 10 = 40, 11 or more = 10.
- **Links:** 100, minus 15 for each broken link (floor 0).

Performance may also use measured numbers when you have them (load time, request count); say which you used. Report the total as a whole number and the per-category scores beside it. A score from a Quick run is marked "quick, not comparable" next to a Full one.

## Baseline file

Save one per run beside the report. Our own schema:

```json
{
  "date": "2026-01-31",
  "target": "http://127.0.0.1:3000/",
  "mode": "full",
  "score": 82,
  "categories": { "console": 70, "links": 100, "visual": 92, "functional": 77, "ux": 85, "performance": 100, "content": 97, "accessibility": 85 },
  "findings": [
    { "id": "F-001", "title": "Quote form accepts empty submit", "severity": "medium", "category": "ux", "page": "/contact" }
  ]
}
```

Regression compares by `id` and title: list fixed (in the old file, not the new), new (the reverse), still open, and the score change. If the old file is missing or unreadable, say so and run Full instead.

## Report top

Lead with the score, the one-line verdict, and the three things to fix first, each with a screenshot or log line. Findings follow in severity order. Every finding has: id, title, severity, category, page, steps to repeat, what you expected, what happened, evidence path. Repro steps are written so a stranger can follow them. Never pad: five well-evidenced findings beat fifteen vague ones.

## Framework notes

- **Next.js:** hydration mismatch warnings in the console are findings; check that client-side navigation does not break the back button; look for large first-load bundles and images without `next/image` sizing; test pages that fetch data on the client for their loading and error states ([Next.js docs](https://nextjs.org/docs)).
- **Rails:** flash messages should show on the next page; Turbo or Turbolinks can leave stale content after a form submit; check CSRF failures on a form left open a long time; N+1 queries show as slow list pages ([Rails guides](https://guides.rubyonrails.org/)).
- **WordPress:** plugin conflicts show as console errors and layout breaks; check the admin bar overlap when signed in, the mixed-content warnings after a move to https, and a 404 on pretty permalinks ([WordPress developer docs](https://developer.wordpress.org/)).
- **Single-page apps:** a hard refresh on a deep link must not 404; client route changes must move focus and update the title; watch for requests that fire twice; memory and listener leaks show as slowing scroll after many navigations.
- **Static sites:** broken relative links and missing assets after deployment under a sub-path are the common fault.

## Our additions

- Local business: weight the click-to-call, directions and booking paths as functional criticals.
- App: sign-up, sign-in, pricing and checkout are scored under functional even when the fault looks visual (a hidden pay button).
- Map severity to the `blocker/major/minor/nit` words in `../../website/design-rules.md` § 6 when handing findings to the design loop: critical to blocker, high to major, medium to minor, low to nit.
