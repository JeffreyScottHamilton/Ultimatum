# Later: source kit, tooling and video

Read when a rule elsewhere points here, or when planning what to build next. These items come from the source skill but are not shipped in this plugin yet; each says what it would take.

## Shipped kit

Our own code, written for this plugin, under `../../../../../data/craft/taste/kit/`. Paths below are relative to that folder. Each piece opens from `file://` with no build step and no network.

| Piece | Files | Checked by |
|---|---|---|
| Page system | `system.css`, `starter.html` | `tools/taste_contrast.cjs` on the starter |
| Named grounds, all 16 | `grounds.css`, `grounds.html`, `grain.svg` | `tools/taste_contrast.cjs grounds.html` (4.5:1 on real pixels, 1440 and 390) |
| UI fragments, 19, and a phone frame | `ui/ui.css`, `ui/*.html`, `ui/index.html` | `tools/taste_ui_gallery.py --check` |
| Icons: 16 glyphs and layout classes | `icons/glyphs.svg`, `icons/icons.css`, `icons/index.html` | `test_taste_icons.py` |
| Diagrams: hub, fan-in (bow-tie), timeline, free | `diagrams/*.json`, `diagrams/diagram.css`, `diagrams/diagram.js`; generator `scripts/ultlib/diagram.py` | `test_diagram.py`, `tools/taste_diagram_gallery.py --check` |
| Effects, 3 of 25: grain-gradient, orb-sphere, grid-pulse | `effects/effects.js`, `effects/effects.css`, `effects/index.html` | `test_taste_effects.py`, `tools/taste_fx_check.cjs effects/index.html` |
| Copy lint | `scripts/ultlib/copylint.py` | `test_copylint.py` |

- Each effect runs 8 s, then holds its last frame; a CSS poster stands in under reduced motion, below 700 px, without WebGL2 and when a shader fails. Budget per `performance.md` § WebGL.
- `ult diagram` and `ult copylint` run as `python3 scripts/ultlib/<name>.py` until the toolbelt wires them in.
- Copy only hero markup from a kit page and replace every word and picture. Never edit kit files to clear a check (`quality-gate.md` § Waivers).

## Source kit still to do

The rules for these live in the files named; the code does not exist here yet.

| Asset family | What is left | Rules live in | To ship it |
|---|---|---|---|
| Effects | 22 of the 25, the gallery palette switcher and the parameter lab | `grounds-and-effects.md` § Effects catalogue | one shader per effect on `effects/effects.js`, same budget and poster rule |
| Effect parts | headline, stat and button fills, rings, charts, feature-card panels | `effect-parts.md` | small mounts on the effects runtime |
| Objects and prints | print objects, photo prints, scene objects, product-render builder, poster maker | `objects.md` | a small ray-marcher reading our own spec format, plus a still exporter |
| Moments and scenes | moment and scene modules with demos | `moments-and-scenes.md` | per-moment modules on the patterns there |
| Icons | a resolver for brand, file-type and tool icons; a brand-mark slot | `icons-and-diagrams.md` | a stdlib script that copies from pinned packages |
| Diagrams | ring, tree, lanes, sync and grid layouts; 27 presets; a builder page; a phone layout (today the board scrolls sideways under 560 px) | `icons-and-diagrams.md` § Diagrams | more layouts in `diagram.py` |
| Photo library | 413 vetted frames with credits | `photos.md` § Sources, in order | not planned; live search stays |

## Source tooling

The source runs its checks with Node scripts and a Stop hook. Under this plugin's rules (stdlib-only Python toolbelt, no network, never install a source hook) they are not adopted. What each did, and our stand-in:

| Source tool | Did | Our stand-in now |
|---|---|---|
| finish gate + Stop hook (Claude Code, Codex, Antigravity) | blocked the agent from stopping until checks passed; rounds, waivers, exit codes | the manual loop in `quality-gate.md` § Rounds; hooks are a user setting, never added by a skill |
| consistency checker | browser checks across layout, text, nav, buttons, motion, visuals, copy, wiring and contrast | `quality-gate.md` and `../../website/feel-bar.md` with Playwright |
| copy lint | counted copy tells; failed on residue, worn words and stock lines | `scripts/ultlib/copylint.py` (shipped; coined-name, cast-name and company-name checks still by hand) |
| perf script | bytes, requests, fonts, images, contexts, paints, long tasks | the Playwright script in `performance.md` § Measure |
| shoot | full-page and per-section screenshots with live effects | Playwright `page.screenshot({ fullPage: true })` |
| deal / start | dealt heroes, palettes, fonts and grounds by kind and trade, with history | `page-plans.md` § Deal lists |
| photos | searched and fetched licensed stand-ins, wrote credit lines | `photos.md` § Sources, in order (by hand) |
| icons | found, fetched, scanned, checked and measured icons | `icons-and-diagrams.md` § Serving icons (by hand) |
| ground picker and checker | dealt grounds per section; measured contrast from pixels | picking by hand per `grounds-and-effects.md` § Named grounds; contrast by `tools/taste_contrast.cjs` (shipped, repo test tool) |
| poster maker, shader lint | rendered product stills; flagged reserved words in shaders | `objects.md` § Client renders |
| street-map baker | baked a still map from OpenStreetMap | `effect-parts.md` (street map row) |

The browser checks (`tools/taste_*.cjs`) are repo test tools that need Playwright; they are not part of the stdlib toolbelt. The perf script is the most useful next port.

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
