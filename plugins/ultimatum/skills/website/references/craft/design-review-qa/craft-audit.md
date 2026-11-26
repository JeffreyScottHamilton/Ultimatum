# Craft audit for Persuade pages and redesigns

Read when the page's job is to convince (landing, pricing, campaign, a local business home page) or when the owner asked for a redesign. It adds checks that scripts cannot see. Run it in the same pass as the page-by-page audit; each failed item is a finding.

## 1. Scan first, then look

Where a scripted scan of the rendered HTML is available, run it per page and file each hit under its rule id (`slop-tells.md`). Without one, judge the tells by eye and say the scan was not run. A hit that real content explains (a customer who is really named "Nexus") is noted, not filed. Never delete a claim because a rule says so; defer it and ask the owner for proof.

## 2. Claims come from the owner, never from you

- Testimonials, customer names, logos, results, uptime figures, prices and guarantees are the owner's to supply. Without them the slot stays empty.
- A stand-in that cannot be mistaken for the real thing is fine: a visible `[Needs proof: what is missing]` tag in a warning colour. A believable invented claim does more harm than an honest gap.
- This is the same stance as `../../copy.md` (every claim true and shown) and `../../website/design-rules.md` § 2 (numbers nobody can back up).

## 3. Sample content must look real

For example data in product shots and tables:

- Skip stock names and brands (Jane Doe, Acme, Nexus). Give each avatar a different face and each row a different date.
- Round sample figures read as made up: 99.99 per cent, exactly 50 per cent, "1,000+", "10x". Use odd, specific values.
- Avoid filler vocabulary: elevate, seamless, effortless, supercharge, streamline, revolutionise, unlock, empower, unleash, next-gen, game-changer, delve, tapestry.
- Headings in sentence case. An error message says what went wrong and the next step, never "Oops!". Success messages stay calm, with no exclamation mark.

## 4. Ship floor (full HTML documents)

- Head: `<title>`, meta description, favicon (an inline SVG of the brand mark if no file exists). A page meant for sharing also gets `og:title` and `og:description`; `og:image` only when a URL was supplied.
- Accessibility basics: a skip link that comes first in tab order, stays hidden until focused and jumps to `<main>` ([bypass blocks](https://www.w3.org/TR/WCAG22/#bypass-blocks)); header, nav, main and footer landmarks; descriptive `alt` on meaningful images and an empty `alt` on decorative ones.
- Footer: privacy and terms links, pointing at the owner's real URLs.
- Forms: required fields and email format checked as the person types, tied to the message with `aria-invalid` and `aria-describedby`.
- Links: each one leads somewhere real. No `href="#"` and no guessed path; a control without a destination is disabled. The nav marks the current page with `aria-current="page"`.
- Dead ends: an unknown address shows a designed 404 with a way back, every page offers a next move, and a cookie notice appears only where the law asks for one.
- Local business: opening hours and address as real text (not baked into an image) and business schema (`../../pages-and-seo.md`).

## 5. Motion rules for the one authored moment

These rules shape the single motion moment and the state changes. They never grant extra motion.

- The page must work with the animation absent. A script adds the hidden starting state only once its observer is ready (a class on `<html>` works), so a crashed script or a crawler still sees all content and the main action never waits on motion.
- Trigger reveals with `IntersectionObserver`: threshold 0, a bottom margin near minus 20 per cent, unobserve after the first fire ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)). Never an unthrottled scroll handler; effects tied to scroll position read it inside `requestAnimationFrame`.
- Animate only `transform`, `opacity`, `filter` and `clip-path`, and keep blur at 14 px or below.
- No element starts from `scale(0)`; begin at 0.85 or higher. Lines and bars may grow from nothing. A data bar fills with a left-to-right `clip-path` wipe lasting 0.7 to 1.1 s.
- Stagger items in reading order, 30 to 80 ms apart, within one section and never page-wide.
- Name the easing as a token: the design doc's own, or else a firm ease-out for entrances and ease-in-out for wipes. Use `linear` only for steady motion.
- Loops stop when off-screen. With `prefers-reduced-motion: reduce` the end state appears immediately.
- Hero and other full-height sections take `min-height: 100dvh` rather than `100vh`, so a phone's browser bars do not clip them.

## 6. Persuade checks (a failed one is a deferred high)

1. **A single named main action.** Nothing above the fold competes with it, and the last section repeats it.
2. **Objections met where they occur:** each major doubt gets an answer at the point it arises (a real FAQ, a comparison, a guarantee).
3. **Proof next to the claim,** from the owner: a customer, quote or figure placed beside the statement it backs, not a detached row of numbers.
4. **A risk reversal the business truly offers** (free quote, trial, no card needed, cancel any time, refund). Never invented.
5. **A deliberate index choice:** ad-only or time-limited pages get `noindex`; an indexed page needs its own title and description, and its FAQ is marked up as FAQPage JSON-LD (`../../pages-and-seo.md`).

Conversion habits: a page reached from an ad echoes the ad's promise and tone in its hero; state the benefit concretely ("A fixed quote within one working day", not "fast service"); when the offer asks a lot, raise the FAQ.

## 7. Fix order and stack

Order and stack rules are in `fix-loop.md`.
