# Later: source kit, tooling and video

Read when a rule elsewhere points here, or when planning what to build next. These items come from the source skill but are not shipped in this plugin yet; each says what it would take.

## Source kit

The source ships ready-made front-end assets. We keep their rules (in the files named) but not their code, because rewriting them is real work and copying is not allowed.

| Asset family | What it holds | Rules live in | To ship it |
|---|---|---|---|
| CSS grounds | 16 grounds with a picker and a contrast checker | `grounds-and-effects.md` § Named grounds | write our own CSS per ground and a pixel-contrast check |
| Effects | 25 WebGL effects, gallery and parameter lab | `grounds-and-effects.md` § Effects catalogue | write shaders from scratch, one per effect; budget per `performance.md` § WebGL |
| Effect parts | headline, stat and button fills, rings, charts, feature-card panels | `effect-parts.md` | same as effects |
| Objects and prints | print objects, photo prints, scene objects, product-render builder and poster maker | `objects.md` | a small ray-marcher reading our own spec format, plus a still exporter |
| Moments and scenes | moment and scene modules with demos | `moments-and-scenes.md` | per-moment modules on the patterns there |
| UI fragments | 19 interface fragments, among them an app window, chat, code, a diff review, a terminal run, a pipeline board, a calendar, search and integrations | `cards-and-ui.md` § Interface fragments | write as plain HTML and CSS partials |
| Icons | resolver, local SVG folder, layouts CSS, demo page | `icons-and-diagrams.md` | a stdlib script that copies from pinned packages |
| Diagrams | engine, 27 presets, builder lab | `icons-and-diagrams.md` § Diagrams | an SVG generator from a small JSON spec |
| Page system | reset, tokens, layout and motion CSS, starter page | `system.md`, `layout-and-heroes.md` | one starter page and stylesheet |
| Phone app showcase | a device-frame hero (about 280 × 570) | `layout-and-heroes.md` § Hero catalogue | a CSS device frame around a real screenshot |

- Mount any kit piece exactly as its own docs say; copy only hero markup and replace every word and picture.
- Never edit shared kit files to clear a check (`quality-gate.md` § Waivers).

## Source tooling

The source runs its checks with Node scripts and a Stop hook. Under this plugin's rules (stdlib-only Python toolbelt, no network, never install a source hook) they are not adopted. What each did, and our stand-in:

| Source tool | Did | Our stand-in now |
|---|---|---|
| finish gate + Stop hook (Claude Code, Codex, Antigravity) | blocked the agent from stopping until checks passed; rounds, waivers, exit codes | the manual loop in `quality-gate.md` § Rounds; hooks are a user setting, never added by a skill |
| consistency checker | browser checks across layout, text, nav, buttons, motion, visuals, copy, wiring and contrast | `quality-gate.md` and `../../website/feel-bar.md` with Playwright |
| copy lint | counted copy tells; failed on residue, worn words and stock lines | `copy.md` § Tells, read by hand or by a reviewer |
| perf script | bytes, requests, fonts, images, contexts, paints, long tasks | the Playwright script in `performance.md` § Measure |
| shoot | full-page and per-section screenshots with live effects | Playwright `page.screenshot({ fullPage: true })` |
| deal / start | dealt heroes, palettes, fonts and grounds by kind and trade, with history | `page-plans.md` § Deal lists |
| photos | searched and fetched licensed stand-ins, wrote credit lines | `photos.md` § Sources, in order (by hand) |
| icons | found, fetched, scanned, checked and measured icons | `icons-and-diagrams.md` § Serving icons (by hand) |
| ground picker and checker | dealt grounds per section; measured contrast from pixels | `grounds-and-effects.md` § Named grounds |
| poster maker, shader lint | rendered product stills; flagged reserved words in shaders | `objects.md` § Client renders |
| street-map baker | baked a still map from OpenStreetMap | `effect-parts.md` (street map row) |

A stdlib Python copy lint and a contrast checker are the most useful next ports; both fit the toolbelt rules.

## Video

Not in scope yet. When added, the rules are:

- **Only on tech pages,** and only in two places, the hero or the data-visual frame, where it counts as the single effect or the single loop. Anywhere else, show a still image; clicking it opens the film.
- `muted`, `playsinline`, a `poster` that shows first, either a 6–12 s loop or a short sequence that runs one time and stops on its final frame.
- A visible pause button (WCAG 2.2.2); still under reduced motion.
- Separate phone and desktop files, chosen by media query.
- A client's own video is a real `<video>` element; a play control only when the file exists.
- A game trailer sits in a 16 : 9 frame with a real, centred play button.

```html
<video class="hero-film" muted playsinline loop preload="none" poster="/media/hero-poster.avif"
       aria-label="The editor running a branch preview">
  <source src="/media/hero-390.mp4"  type="video/mp4" media="(max-width: 700px)">
  <source src="/media/hero-1440.mp4" type="video/mp4">
</video>
<button class="pause" type="button" aria-pressed="false">Pause</button>
<script type="module">
  const v = document.querySelector('.hero-film'), b = document.querySelector('.pause');
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) v.play().catch(() => {});
  b.addEventListener('click', () => {
    const paused = !v.paused; paused ? v.pause() : v.play();
    b.setAttribute('aria-pressed', String(paused)); b.textContent = paused ? 'Play' : 'Pause';
  });
</script>
```

`<source media>` for video: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/source
