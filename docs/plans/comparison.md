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
| anatomy | 23 files, 61 KB, 2 scripts | 392 KB | 36 (kit modules) | even (was upstream on tooling) | `figure_audit.py` (0.0.41) runs the ten static checks; `figure_draw.py` (0.0.51) draws the scene at any camera with exact convex depth order and audits turning groups and the orbit. Upstream still has lathe, coil and canvas helpers |
| anthropic-method | 9 files, 29 KB, 6 scripts | 2.2 MB | 10 (eval viewer, packaging, office formats) | ours | Office-format skills, out of scope |
| caveman | 6 files, 19 KB, 1 script | 880 KB | 16 (runtime, hooks, cloud) | ours | Hook-driven mode; runtime, out of scope |
| coding-discipline | 5 files, 1 script | not read (no licence) | n/a | ours on checkability (`diff_scope.py`) | Unknown; text not read |
| design-review-qa | 25 files, 3 tables, 3 scripts | 13 MB (whole gstack) | 6 | ours (was even) | 0.0.47: `mockup_board.py` puts built HTML mockups side by side at 1280 and 390 with pick, ratings and comments, warns on near copies and missing axes, and reads the pick back; "show me the 10" is a built page beside `now`. Upstream generates pictures with a paid image service; ours needs none and the mockups can be linted and rendered |
| emil-motion | 20 files, 112 KB, 5 tables | 339 KB | 2 (Swift) | ours (was ours for web only) | 0.0.48: `expo-motion.md` and `expo-recipes.md` cover the native tool ladder, UI-thread rules, press, haptics, reduced motion, 120 fps and ten recipes; every code block is type-checked in strict mode by `test_expo_recipes.py` when the types are installed. Not yet run on a device. Upstream still has Swift |
| frontend-budget | 7 files, 23 KB, 2 scripts, 1 table, plus 4 page guides (14 KB) in the website skill | 3.4 MB | 14 (identity flow, pack rulings) | ours (was ours on load cost) | 0.0.49: `vague-requests.md` with four worked examples, and `vague_path.py` routes a vague complaint to one of 13 areas with up to four questions, a guide per answer and a first measurement; `check` proves every route exists. Upstream still has a dated gallery of other companies' sites, left out on purpose |
| gstack-eng | 11 files, 34 KB, 2 scripts | 13 MB | 11 (runtime, YC coaching) | ours | Nothing in scope |
| hallmark | 31 files, 172 KB, 5 tables | 685 KB | 20 (all scripts) | ours on checks, judged (was upstream) | 0.0.43: `page_lint.py` runs every machine-checkable gate. 0.0.44: `render_check.py` opens the page in Chromium at the same 8 widths and measures 28 rendered rules, blocks remote requests by default, takes reasoned waivers. On upstream's own four exemplar pages it reports one edge-text and three low sign-up questions (remote photos blocked) |
| impeccable | 13 files, 57 KB | 12 MB | 21 (command menu, visualize) | ours on checks, judged (was upstream) | 0.0.43 static rules; 0.0.44 `render_check.py` adds the rendered pass (contrast as painted, covered and hidden-at-rest text, first-screen fit) with exit 3 when no browser, so a skip is never read as a pass |
| mattpocock | 9 files, 31 KB, 1 script | 697 KB | 3 | ours | Nothing in scope |
| react-performance | 4 files, 1 script | not read (no licence) | n/a | ours on checkability (`react_scan.py`, measuring guide) | Unknown; text not read |
| decks | 7 files, 2 scripts, 2 tables, 1 template, 2 examples | ui-ux-pro-max slides (MIT) | 4 (generator, background keywords) | ours (0.0.50: deck-type and layout tables the built deck is checked against, `deck_plan.py`) | A slide generator; ours prints marked skeletons instead |
| superpowers | 11 files, 49 KB, 3 scripts | 925 KB | 7 (per-harness launch notes) | ours (0.0.52: `choice_board.py`, a serverless visual companion that also works in cloud sessions) | A live page that updates while the chat runs; ours is rebuilt per question |
| taste | 21 files, 198 KB, 29 data, 2 preset tables | 557 KB | 159 | ours on checks, judged (was even) | 0.0.45: `ult design deal` deals palette, type, hero, parts and grounds by kind and trade with history. Upstream has more presets (64 palettes, 39 type sets against our 40 and 43) but does not test their contrast; every one of ours passes 7:1 ink and 4.5:1 muted and button text in `test_taste_deal.py` |
| ui-ux-pro-max | 18 files, 107 KB | 1.2 MB | 43 (mostly generators, search tables, bundled fonts) | even (was upstream) | Searchable style tables and the long tail of presets. Decks fixed in 0.0.39 (`craft/decks/`, `deck_check.py`); icons and banners in 0.0.40 (`identity/icons.md`, `identity/banners.md`, `icon_check.py`); logo and identity in `craft/identity/` |

## What to fix, in order

1. **A page linter** (hallmark and impeccable win). Done in 0.0.38. Stdlib script that reads HTML and CSS and flags the machine-checkable tells already written in `data/craft/hallmark/gates.csv` and `data/craft/design-review-qa/slop-tells.csv`. Turns two lists into a check.
2. **Slides and decks** (ui-ux-pro-max wins). Done in 0.0.39. Nothing in the plugin covers building a deck; launch and business work needs one.
3. **Icons and image sizes** (ui-ux-pro-max wins). Done in 0.0.40. Icon style rules and a size table for social cards, banners and favicons.
4. Later, lower value: done. Expo motion recipes landed in 0.0.48. The mockup comparison step landed in 0.0.47. The figure audit script landed in 0.0.41 and the landing and settings page anatomy in 0.0.42.

Each fix ships as its own release with tests, and this table is updated when it lands.
