# Quality gate

Read before calling a page finished. It sets the checks, the widths, how many fix rounds to run, what may be waived and what the report says.

## Tools

- Serve the page over http on `127.0.0.1` (or `localhost`, or a `.test` host), never from `file://`. Check only local pages.
- Framework builds (Next.js, Astro, Vite) are checked on the dev URL or on a fresh static build; rebuild before every round.
- Use headless Chromium through Playwright (the house tool, `../../website/feel-bar.md`). Give each run a new context, a 10-minute limit and the foreground, and never run two browsers at once.
- A helper or subagent that builds a page runs the same checks itself before handing back.
- The check block, in order: copy lint, consistency (one wording per fact), layout at each width, screenshots, performance (`performance.md`).

## Widths

- **Full run:** 1440, 1280, 1024, 820 × 1180, 768 × 1024, 390, 375 and 320.
- **Quick run (fix rounds):** 1440 and 390.
- At 390 also check that nothing collides and every tap target is at least 44 × 44 px (WCAG 2.5.8 sets 24 px as the minimum; the house uses 44). At 820, 768, 390 and 320: one column, full-width buttons.
- At 320 walk the page for sideways scroll (WCAG 1.4.10 Reflow).
- With scripts off, every section's content is still there.

```js
// Sideways-overflow and tap-size walk: run inside page.evaluate at each width.
() => {
  const out = { overflow: [], small: [] };
  const box = el => el.getBoundingClientRect();
  for (const el of document.querySelectorAll('body *')) {
    const { left, right, width } = box(el);
    if (width > 0 && (left < -1 || right > innerWidth + 1)) out.overflow.push(`${el.tagName}.${el.className}`);
  }
  const tappable = 'a, button, input, select, textarea, [role="button"]';
  for (const el of document.querySelectorAll(tappable)) {
    const { width, height } = box(el);
    const inline = el.closest('p, li');            // links inside running text are exempt
    if (width > 0 && !inline && Math.min(width, height) < 44) out.small.push(el.textContent.trim().slice(0, 30));
  }
  return out;
}
```

Links inside running text are exempt from the size rule (WCAG 2.5.8 inline exception).

## Visuals

- At 390, 768, 1024 and 1440 every visual has rendered; no section shows an empty ground where a picture belongs.
- Empty area: warn when more than 35% of a section is empty, fail over 50%.
- In screenshots, outline in red any placeholder text and any visual that failed to draw, and name pictures still loading, so a reviewer cannot miss them.
- Wait for pending stills and lazy images before a screenshot.

## Copy

- Run the copy lint (`copy.md` § Tells, `voice.md` § Device budget, `../../website/design-rules.md` §2). Failures block; warnings are listed and fixed or justified.
- Blocking copy failures: chatbot residue, worn words, stock lines, devices over double their budget, cliché coined names.
- The client's own brand word is exempt from the worn-word list. The copy lint needs no browser.
- Read the copy aloud, then re-read every screenshot.

## Checklist

The first screen:
- says what is sold, carries one hard fact, and holds the main button.

Sections:
- each one or two screens tall, none half empty.

Edges:
- everything on the grid; no sideways scroll at any width.

Content:
- no captions under visuals, placeholders, brackets, demo addresses or "sample" notes visible.

Kind fit:
- the page follows its kind's limits (`grounds-and-effects.md` § Who gets effects): no effects on calm kinds, photographs where photographs belong.

Motion:
- every control answers on hover, focus and press; nothing tilts; loops run 2.5–4 s; motion lasting over 5 s gets a pause control (WCAG 2.2.2); reduced motion shows finished states (`motion.md`).

Accessibility:
- names, alt text, labels, heading order, a Tab walk, `lang`, the head tags, and assumed facts marked (`accessibility.md`).

## Severity

- **Fail:** blocks hand-over. **Warn:** fix or give a reason; warnings never block except a missing hero entrance or a missing dealt moment.
- Run status words: PASS (finish), FAIL (fix and run again), OPEN (rounds used up: report what remains), QUICK (a quick run; not a counted round), ERROR (the check itself broke: report the line, don't loop).

## Rounds

- At most three counted fix rounds per page (the house cap, `../../website/design-rules.md` §4). A round counts only when the page or its waivers changed since the last.
- Fix rounds use the quick run; the last round is a full run.
- When rounds are used up, stop and report what is still failing. Never keep looping on an ERROR.

## Waivers

A waiver is a written reason to accept one finding. It names the check, the exact target (selector or text) and a reason of at least a full sentence.

```json
{ "check": "worn-word", "target": "curated", "reason": "The gallery's own exhibition title, used as the client wrote it." }
```

- A waiver that could match more than one finding is ignored. Every waived finding still appears in the report.
- More than five waivers on one page is itself a failure.
- The client's own words are waived hit by hit, never as a block.
- Never edit shared kit files, or hide elements from the checker, to clear a check.

## Honest checks

- Code that detects the checker (sniffing `navigator.webdriver`, testing the user agent for "Headless", stripping `aria-hidden` only for bots) is a finding in itself.
- A check you didn't run is reported as not run, never as passed.

## Eyes

- Put the page side by side with two professional sites in the same trade. It should read as a real business at the same level: plain, specific, complete.
- Look for the template feel: every section the same height, every card the same length, the same device repeated.

## Report

One block, plain words:

- The gate status line, waivers used, and any open failures.
- What was dealt (hero, palette, fonts, moment) and the one-line voice card (`voice.md`).
- Each check run, with its command and exit code.
- Every assumed fact and stand-in (photos, hours, prices), the demo form address, the domain search, and what the client must still supply.
