# Ours vs upstream: guide-set comparison

Date: 2026-11-27. Compared each rebuilt set in `plugins/ultimatum/skills/*/references/craft/` with the upstream it was built from (checkouts in `/tmp/src/`, read only) using the coverage maps in `docs/plans/coverage/`. Karpathy guidelines and Vercel React have no LICENSE file, so their text was not read; those two sets are compared on topic only.

Sizes are Markdown in the guide folder (ours) against Markdown in the whole upstream checkout, which includes docs, changelogs and translations, so they show scale, not a like-for-like word count. "Gaps" are rows marked `later` in the coverage map.

## How each set was judged

Five questions, each scored ours better / even / upstream better:

1. **Coverage:** does upstream teach something useful that ours leaves out?
2. **Correct and current:** versions, standards, facts.
3. **Checkable:** does a rule come with a test, a tool or a measurable threshold?
4. **Cost to load:** how much an agent must read to get the answer.
5. **Routing:** does the right file get loaded for the task?

## Results

| Set | Ours | Upstream | Gaps | Verdict | Where upstream still wins |
|---|---|---|---|---|---|
| anatomy | 22 files, 53 KB, 1 script | 392 KB | 36 (kit modules) | even (was upstream on tooling) | Fixed in 0.0.41: `figure_audit.py` runs the ten audit checks on a JSON scene; upstream's kit also draws the parts and audits turning groups |
| anthropic-method | 9 files, 29 KB, 6 scripts | 2.2 MB | 10 (eval viewer, packaging, office formats) | ours | Office-format skills, out of scope |
| caveman | 6 files, 19 KB, 1 script | 880 KB | 16 (runtime, hooks, cloud) | ours | Hook-driven mode; runtime, out of scope |
| coding-discipline | 5 files, 1 script | not read (no licence) | n/a | ours on checkability (`diff_scope.py`) | Unknown; text not read |
| design-review-qa | 24 files, 97 KB, 3 tables | 13 MB (whole gstack) | 7 | even | Mockup comparison step ("show me a 10") |
| emil-motion | 18 files, 89 KB, 5 tables | 339 KB | 4 (Expo, Swift) | ours for web | Expo and React Native recipes |
| frontend-budget | 6 files, 16 KB, 1 script, plus 4 page guides (14 KB) in the website skill | 3.4 MB | 15 (identity flow, pack rulings) | ours on load cost; even on page anatomy (was upstream) | Fixed in 0.0.42: `website/references/craft/pages/` covers landing order, developer-product landings and settings areas. Upstream's still has more worked examples |
| gstack-eng | 11 files, 34 KB, 2 scripts | 13 MB | 11 (runtime, YC coaching) | ours | Nothing in scope |
| hallmark | 31 files, 172 KB, 5 tables | 685 KB | 20 (all scripts) | ours on checks, judged (was upstream) | 0.0.43: `page_lint.py` runs every machine-checkable gate. 0.0.44: `render_check.py` opens the page in Chromium at the same 8 widths and measures 28 rendered rules, blocks remote requests by default, takes reasoned waivers. On upstream's own four exemplar pages it reports one edge-text and three low sign-up questions (remote photos blocked) |
| impeccable | 13 files, 57 KB | 12 MB | 21 (command menu, visualize) | ours on checks, judged (was upstream) | 0.0.43 static rules; 0.0.44 `render_check.py` adds the rendered pass (contrast as painted, covered and hidden-at-rest text, first-screen fit) with exit 3 when no browser, so a skip is never read as a pass |
| mattpocock | 9 files, 31 KB, 1 script | 697 KB | 3 | ours | Nothing in scope |
| react-performance | 4 files, 1 script | not read (no licence) | n/a | ours on checkability (`react_scan.py`, measuring guide) | Unknown; text not read |
| decks | 6 files, 1 script, 1 template | ui-ux-pro-max slides (MIT) | 6 (lookup tables, generator) | ours on checkability (`deck_check.py`) | Searchable layout and strategy tables |
| superpowers | 10 files, 42 KB, 2 scripts | 925 KB | 9 (visual companion) | ours | Visual brainstorming companion |
| taste | 21 files, 198 KB, 29 data | 557 KB | 160 | even | Long tail of style presets |
| ui-ux-pro-max | 18 files, 107 KB | 1.2 MB | 43 (mostly generators, search tables, bundled fonts) | even (was upstream) | Searchable style tables and the long tail of presets. Decks fixed in 0.0.39 (`craft/decks/`, `deck_check.py`); icons and banners in 0.0.40 (`identity/icons.md`, `identity/banners.md`, `icon_check.py`); logo and identity in `craft/identity/` |

## What to fix, in order

1. **A page linter** (hallmark and impeccable win). Done in 0.0.38. Stdlib script that reads HTML and CSS and flags the machine-checkable tells already written in `data/craft/hallmark/gates.csv` and `data/craft/design-review-qa/slop-tells.csv`. Turns two lists into a check.
2. **Slides and decks** (ui-ux-pro-max wins). Done in 0.0.39. Nothing in the plugin covers building a deck; launch and business work needs one.
3. **Icons and image sizes** (ui-ux-pro-max wins). Done in 0.0.40. Icon style rules and a size table for social cards, banners and favicons.
4. Later, lower value: Expo motion recipes, a mockup comparison step. The figure audit script landed in 0.0.41 and the landing and settings page anatomy in 0.0.42.

Each fix ships as its own release with tests, and this table is updated when it lands.
