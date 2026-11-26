# QA taxonomy: severity, categories and the per-page walk

Read when logging a bug and choosing its severity and category, or when planning what to poke at on a page. Rows are also in `../../../../../data/craft/design-review-qa/qa-issues.csv`.

## Severity

| Level | Meaning | Examples |
|---|---|---|
| critical | blocks a core workflow, loses data, crashes, or exposes private data | form submit lands on an error page; checkout broken; data deleted with no confirmation |
| high | a major feature is broken and there is no workaround | search returns the wrong results; an upload fails silently; sign-in redirect loop |
| medium | works, with a noticeable problem and a workaround | page takes over 5 s to load; a missing validation that still lets submit through; a layout that breaks only on phones |
| low | cosmetic or polish | typo in the footer; 1 px misalignment; inconsistent hover |

Choose the highest level that truly applies and write down the impact and any workaround.

## Categories (one primary category per finding)

1. **Visual:** overlap, clipped text, sideways scrollbar, broken or missing images, wrong stacking order, font or colour drift, animation glitches, off-grid alignment, dark-mode problems.
2. **Functional:** broken links, buttons that do nothing, missing or bypassable validation, wrong redirects, state lost on refresh or back, double-submit and stale data races, wrong or empty search results.
3. **UX:** confusing navigation, dead ends, no loading indicator, interactions over about 500 ms with no feedback, vague errors ("Something went wrong"), no confirmation before destructive actions, patterns that differ page to page.
4. **Content:** typos, outdated text, leftover lorem ipsum, text cut off with no ellipsis, wrong labels, missing or unhelpful empty states.
5. **Performance:** loads over 3 s, janky scroll, layout shift after load, over 50 requests on one page, large unoptimised images, script that blocks the page.
6. **Console and errors:** uncaught exceptions, failed requests (4xx, 5xx), deprecation warnings, cross-origin errors, mixed content, content-security-policy violations.
7. **Accessibility:** missing alt text, unlabelled inputs, keyboard path broken, focus traps, wrong or missing ARIA, low contrast, content a screen reader cannot reach.

When one root cause shows up on several pages, file it once. When a finding fits two categories, prefer whichever comes first in this list: links, accessibility, functional, then performance, visual, content, UX and console.

## Per-page walk

For each page visited:

1. **Look.** Full-page screenshot; scan for layout breaks, broken images, alignment.
2. **Poke.** Press each control and follow each link. Does it do what its label says?
3. **Forms.** Empty submit, invalid data, very long text, special characters. Only on local or owner-approved targets.
4. **Navigation.** All paths in and out: breadcrumbs, the back button, deep links, the phone menu.
5. **States.** Empty, loading, error, and full or overflowing.
6. **Console.** Print the errors after every interaction; any new error or failed request counts.
7. **Responsive.** Phone and tablet widths where relevant.
8. **Auth edge.** Do not log out or change accounts on your own. When the logged-out or other-role view matters, have the owner switch and then run again.

## Our additions

- Local business: the click-to-call, directions and booking paths are core workflows; a broken one is high at least, critical if it is the only way to book.
- App: sign-up, sign-in, password reset, pricing and checkout are core workflows; a dead pay button, a double charge on double-click or a missing confirmation email step is critical or high.
- Accessibility findings map to WCAG 2.2 success criteria by number in the report ([WCAG 2.2](https://www.w3.org/TR/WCAG22/)); `ult-browser.mjs` covers part of them (`../../../../work/references/browser-verification.md`).
