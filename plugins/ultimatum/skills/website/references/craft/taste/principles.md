# Principles

Read first, once per build: the bar a page has to clear, the order of work, and the few things never done. Every other file in this folder serves these.

## The bar

- The target is a clear, direct business site as polished as what the biggest product companies release. It states what is on offer, puts the actual product or place on every screen, and feels built for this one client, neither a template nor a gallery piece.
- One system (`system.md`), one section per screen or two (`layout-and-heroes.md`), equal edges, copy that is plain yet sounds like this client alone (`copy.md`, `voice.md`).
- More and better real pictures than a template would use: true photographs (or licensed borrowed shots if the client has none, `photos.md`), real product interface, real logos.
- Every page has a hero entrance, one or two dealt moments and a full hover layer (`motion.md`). Scenes and shader effects belong to software, gaming and tech pages alone (`grounds-and-effects.md`).
- The house rules still apply on top: the anti-generic lint (`../../website/design-rules.md` §2), the craft notes (`../../website/craft.md`), and WCAG 2.2 AA (`accessibility.md`).
- Beyond the source: the local-business jobs (calls, bookings, quotes, directions, opening hours, trust) and the app jobs (sign-up, pricing, dashboards, checkout) are first-class. Their sections are in `sections.md`, `place-pages.md` and `cards-and-ui.md`.

## Stack

- **Empty folder:** plain static HTML and CSS with small modules; no framework unless asked.
- **Existing project:** use its framework, components and assets; add only what the page needs. React, Next.js, Vue, Svelte, Astro and Tailwind all work.
- **Next.js:** build a static export and check the built page, not only the dev server.
- Checks need Playwright with Chromium (`quality-gate.md` § Tools); ffmpeg only for video posters.

## Order of work

1. **Brief.** Write the kind (software, gaming, hardware, product, service, place), the offer, the buyer, the main action and the real material you have (photos, figures, quotes, hours). The house brief format is in `../../website/planner.md` § 1.
2. **Copy, all of it, before any layout** (`copy.md`, `voice.md`). The words decide the sections.
3. **Plan as screens:** one line per section with its id, its idea, its picture, its kind, its height in screens and its moment, if any (`page-plans.md` § Plan).
4. **Deal** the variable choices (below).
5. **Build** from the system, section by section (`sections.md`, `cards-and-ui.md`, `place-pages.md`).
6. **Gate:** run the checks, fix, re-run; at most three rounds (`quality-gate.md`).
7. **Report** what was dealt, assumed and checked (`quality-gate.md` § Report).

## Deal

Choices that would otherwise fall to habit are dealt from a list, not picked by taste: hero layout, palette, font pair, brand treatment and moments.

- Deal from the lists for the page's kind (`page-plans.md` § Deal lists, `layout-and-heroes.md` § Hero catalogue, `moments-and-scenes.md` § Dealing).
- Keep a short history of recent deals so the next page differs; never repeat the last page's hero and palette together.
- A brief that names a choice overrides the deal. Write the dealt line at the top of the plan (the house rule, `../../website/design-rules.md` §4).

The deal function and the per-kind lists are in `page-plans.md` § Deal lists.

## Never

- Copy another site's code, copy, pictures or signature effect. Reference sites teach structure only.
- Invent proof, prices, people or figures (`copy.md` § Truth).
- An effect on a calm kind; a render where a photo belongs; a caption under a visual.
- Edit shared kit files or hide anything from a checker to pass a check (`quality-gate.md` § Honest checks).
- Hand over a page that hasn't been looked at, at 1440 and 390, with and without reduced motion.
