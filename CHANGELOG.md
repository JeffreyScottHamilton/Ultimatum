# Changelog

All notable changes to Ultimatum are listed here. Versions follow [Semantic Versioning](https://semver.org/); the version in `plugins/ultimatum/.claude-plugin/plugin.json` is the source of truth and must be bumped for installs to update.

## [0.0.62] - 2026-11-27

Social media workflow (no video styles yet)

- New skill `skills/social-media/` plans, writes, checks and hands over social posts: scope questions, content pillars and cadence, a `social/plan.json` calendar, hooks, captions, hashtags, alt text, tracked links, dated platform limits, claims and disclosure review, the hand-over order and a 48-hour and weekly results loop. Video styles, editing and rendering are left out on purpose; it writes the script and checks the finished file.
- New `ult posts plan FILE [--json]` checks a whole plan (P01 to P15): dates, channels, caption limits including the TikTok API limit, hook type, UTM tags matching the channel, one link, alt text on image posts, two posts on one channel in a day, hashtag counts, long first lines, missing disclosure on sponsored posts and missing AI labels (both blockers), missing files, duplicate captions and no next step. Exit 0 clean, 1 blockers, 2 bad input. Nothing is posted or scheduled.
- `ult posts specs|check|calendar|variant` return: dated limits, file and caption checks (local ffprobe for video, if installed), ICS or CSV calendars, and hook variants ranked only by results the user enters. Pinterest description limit is now 800; Instagram hashtags 5.
- New gate `ult gate approve post "<words>" --file social/plan.json`: needs the plan file, reopens if it changes, used once.
- `ult route` adds `workflow: social-media` for posts, captions, calendars, hashtags and platform content, but not for footer icons, social cards, social login or security routes. `work/SKILL.md` sends that line to the new skill.
- Tests: `tests/test_posts.py` (plan checks, routing, skill files), plus gate and size tests.

## [0.0.61] - 2026-11-27

App Store workflow for Expo apps

- New skill `skills/app-store/` takes an Expo (React Native) app from working code to an App Store submission: project setup (bundle ID, version and build number, icon, splash, permission text), EAS Build profiles with credentials kept by EAS, TestFlight and a two-size device checklist, a pre-submission review check that tells the reader to fetch the current App Review Guidelines (privacy manifest and required-reason APIs, nutrition labels, account deletion, sign-in, in-app purchase, demo account), the store listing with screenshot and App Preview specs, EAS Submit, rejections and Resolution Center replies, and EAS Update versus a new build. Third-party App Store Connect MCP servers are documented as an option only.
- New `ult appstore check [--root .] [--config FILE] [--since REF] [--json]`: reads app.json or app.config.json, eas.json, package.json and the store config, and reports 52 kinds of finding (AS002 to AS093) such as a missing or placeholder bundle ID, a build number not raised since a git ref, missing or vague usage strings for installed permission packages, privacy manifest mistakes, icon size and alpha, production profiles that cannot be uploaded, missing privacy policy URL, listing limits, and signing files or secrets in the project. Standard library only, no network. Exit 0 clean, 1 findings, 2 bad input.
- `ult route` adds `workflow: app-store` for App Store, TestFlight, App Review, EAS build, submit and update tasks (not on security routes); `work/SKILL.md` sends that line to the new skill.
- Tests: `tests/test_appstore.py` with four small fixture projects (clean, risky, dynamic-only, bad JSON); signing-file cases are built in temp folders so no key-shaped file is in the repo.
- Credits: expo/skills (MIT), CharlesWiltgen/Axiom (MIT) and dpearson2699/swift-ios-skills (PolyForm Perimeter, topics only) in `CREDITS.md`, `research/REVISIONS.md` and `data/upstreams.json`.

## [0.0.60] - 2026-11-27

Anatomy: turned parts, coils, knurl and ticks

- `figure_draw.py` draws `"shape": "lathe"` parts from a `[radius, height]` profile (kettle bodies, knobs, bottles, domes) as convex frusta with the joins left unpainted, so depth order and the move checks stay exact; refuses profiles that are too wide, go down or reach a zero radius.
- Pipes may give a `"coil"` (centre, radius, pitch, turns) instead of points: heater elements, springs, wound cables. Each segment is ordered on its own, so the back half hides behind the part it wraps. Coils whose turns would touch are refused, and `figure_audit.py` reads coils with the same helix.
- Cylinders take `"knurl"` (grip ridges) and `"ticks"` (a ring of marks on the top rim); both turn with the part's group and only the facing ridges are drawn.
- New example `examples/turned-scene.json`; `draw.md` and `later.md` updated. Closes the gap where the upstream anatomy kit had lathe, coil, knurl and tick helpers and ours did not (`docs/plans/comparison.md`).
- Tests: five new checks in `tests/test_craft_anatomy_draw.py` (pieces and segments drawn, coil hidden behind the body, true-shape turn audit with no order cycle round the orbit, bad profiles, coils and marks refused, static audit reads coils); the self-check covers the kettle.

## [0.0.59] - 2026-11-27

Taste: 66 contrast-checked palettes

- 26 new palettes in `data/craft/taste/presets/palettes.json` (66 in all), for trades the first 40 missed, such as clinics, nurseries, mechanics, breweries, theatres, newsrooms, labs and food markets. Every one passes the same checks as the first set: text, muted and accent contrast in light and dark, and no clash with an existing trade or mood word.
- `craft/taste/page-plans.md` and `later.md` give the new count. Closes the gap where taste-skill's palette list was longer than ours (`docs/plans/comparison.md`).

## [0.0.58] - 2026-11-27

Deck builder: content file to checked HTML deck

- New `data/craft/decks/deck_build.py` (stdlib only): `starter TYPE` prints a content file laid out from the deck type's plan; `build deck.json -o deck.html` renders all 18 layouts into the template frame (fit to window, keys, print to PDF), escapes every text field, refuses images without alt text, `javascript:` image paths, unknown theme keys and theme colours below contrast (ink 7:1, muted 4.5:1, accent 3:1), then runs `deck_check.py` and `deck_plan.py` on the result. Exit 1 when the built deck has findings.
- `craft/decks/build.md` §2 explains the build route; `later.md` no longer lists the slide generator as left out. Closes the last gap where ui-ux-pro-max's slides beat ours (`docs/plans/comparison.md`).
- Tests: `tests/test_deck_build.py` (self-check across all 8 deck types, frame kept, escaping, bad content refused, theme applied, CLI exit codes, stdlib only).

## [0.0.57] - 2026-11-27

Marketing for the site, rebuilt from marketingskills

- New guide set `skills/website/references/craft/marketing/` (index plus six files): copy and proof, turning visitors into enquiries, offers and pricing, search and AI answers, tracking and A/B tests, launch and email. Written in our own words from the topics in Corey Haines's marketingskills (MIT); `tools/copy_check.py` finds 0 shared runs of 8+ words. Ads, outreach, sales, PR and app-store work are left out on purpose. The website skill's build step links the index.
- New `ult market`, stdlib only. `page` checks title, description, h1, viewport, canonical, social tags, alt text, field labels, form length and JSON-LD (parse errors, required properties, self-serving review stars, FAQ and HowTo rich results that no longer show), plus repeated titles and descriptions across a site. `abtest plan` gives the visitors each version needs and a run length in whole weeks; `abtest read` gives rates, lift, p-value, a 95% interval and a verdict, and exits 1 on a broken traffic split. `events` checks a tracking plan for name shape, past tense, duplicates and personal data.
- Fixed `pages-and-seo.md`: it suggested `Review` markup on the business's own page, which Google doesn't show as stars, and didn't say FAQ rich results are now limited to government and health sites.
- Credits, `data/upstreams.json` (pin 2bf95ed, module website), a coverage map (`docs/plans/coverage/marketingskills.md`: 22 done, 9 partial, 22 out of scope) and a comparison row.
- New tests in `tests/test_market.py` (17).

## [0.0.56] - 2026-11-27

Ship flow, our take on Claude Ship

- New `skills/work/references/ship.md`: shipping one change as a pull request. Review your own diff before the PR exists, open the PR only with a yes, steward it through failing checks, merge conflicts (merge, never rebase) and review comments, then report. It has named stops (merged or closed, user stop, 5 rounds, same failure twice, human gate) and a fixed list of things it never does: approve, merge, auto-merge, force-push, change branch rules, weaken tests. The pattern comes from Anthropic's Claude Ship (Code Review, PR Steward, Claude Approvals); the wording is ours.
- New `ult approvals`, an observe-only approval-policy report. It reads `.claude/ultimatum-approvals.json` (rules with path globs, `if` conditions, overrides and the verdicts approve, comment, people N and block) and says what the policy would require for the current change, including uncommitted and untracked files. Path-based risk (low, medium, high) is built in. Files no rule decides always need a person, and approve holds only when the review found 0 Important issues. It never approves, comments or calls a network service. `--starter` prints a starting policy and `--check` validates one.
- Reviews now tag each finding Important, Nit or Pre-existing (`review/SKILL.md`, `agents/reviewer.md`). `release/SKILL.md`, `release.md` and `ci-and-pr.md` link the ship guide.
- New tests in `tests/test_approvals.py` (17).

## [0.0.55] - 2026-11-27

Interaction kit, our take on Watermelon UI

- New `data/craft/interaction-kit/`: 32 React components (press, copy, tabs, segmented control, split button, hold to confirm, toast, drawer, morph popover, expandable cards, command palette, number ticker, text reveal, marquee, carousel, swipe deck, scrub number, tag input, OTP input, reorder list, rating, stepper, dock, theme toggle, tilt and spotlight cards, and more). They use theme tokens only, honour reduced motion, have keyboard paths and labelled icons, and depend on `react` and `motion` only. Written new; the ideas come from Watermelon UI (MIT).
- `catalog.csv` describes all 131 Watermelon UI components in our words and maps 110 of them to a kit part; `blocks.csv` points to their 189 page blocks and 12 dashboards.
- New `ult kitlint`, which checks components for missing reduced motion, `transition-all`, raw colours, squashed press scales, clickable divs, unnamed icon buttons, hidden focus and replaying presence. On the kit it reports 0 findings in 32 files. On Watermelon UI's components it reports at least one failure in 130 of 131 files (both variants).
- `gallery/` renders every component and checks it in Chromium at phone and desktop sizes, with reduced motion and in dark mode, covering overflow, keyboard paths, focus return and axe. All four views pass with 0 violations.
- New guides in `website/references/craft/interaction-kit/` (choosing, components, details), linked from `website/craft.md`. Watermelon UI is added to `data/components.json`, CREDITS.md and the comparison table.
- New tests in `tests/test_craft_interaction_kit.py`.

## [0.0.54] - 2026-11-27

Solo by default, one Sonnet coder

- `ultimatum:worker` now runs on Sonnet instead of Haiku. It is the one coder the session hands a bounded chunk to (payments, data wiring, an API, tests), while the session keeps the design-heavy work itself.
- `work/SKILL.md`, `orchestration.md` and `context-efficiency.md` now start from solo: every helper starts cold and re-reads, so most jobs are cheapest done by the session alone. A large job gets one coder at most, a scout for wide reading and one review at the end. The old rule that the manager never edits files is gone, and fix rounds drop from five to two.
- New tests in `tests/test_subagents.py`.

## [0.0.53] - 2026-11-27

Token check for pages, components and brand assets

- New `data/design-own/tokens/token_check.py` (standard library, no network). `scan` reads a token stylesheet and flags values that skip it in CSS, HTML, SVG and component files. Errors: `raw-color` and `unknown-var`. Warnings: `named-color`, `raw-font` and `off-scale`. A raw colour that equals a token gets the role as its fix, not the primitive behind it.
- `embed` puts the tokens inside a one-file HTML page. Running it again replaces the block instead of adding another, and `--used` keeps only the tokens the page reads and the tokens those point to.
- `colors` lists the colours in a PNG, SVG, HTML or CSS file and measures each against the nearest token in OKLab. A colour more than 2 away fails as `off-palette`. The PNG reader matched Pillow pixel for pixel on RGBA, RGB, palette and grey exports.
- New guide `craft/ui-ux-pro-max/token-check.md`. `later.md`, the index, the tokens README, the coverage table and the comparison row are updated. Four upstream script rows (html-token-validator, embed-tokens, extract-colors and validate-asset) are now expanded, and the coverage counts were recounted.
- New tests in `tests/test_token_check.py`.

## [0.0.52] - 2026-11-27

Choice boards for questions better seen than read

- New `data/craft/superpowers/choice_board.py` (standard library): turns a JSON spec of visual questions into one offline HTML page. The user clicks cards and pastes back one answer line, and `read` checks that line against the spec. No server, no open port, and it works in cloud sessions.
- `check` and `build` enforce ids, labels, inert local fragments (no scripts, handlers, frames or remote URLs), and local images up to 2 MB, and warn on more than four pick-one options or a question that shows nothing. The page allows only its own hashed script.
- New guide `craft/superpowers/choice-board.md`: the seen-or-read test, the spec, the rules and the loop. The index, `shaping-conversation.md` and `later.md` point to it.
- New tests in `test_craft_superpowers.py`: self-check, build with an embedded image, answer round trip and refusals, and the guide's rule table matched against the script.

## [0.0.51] - 2026-11-27

Draw isometric figures and audit turning groups

- New `data/craft/anatomy/figure_draw.py` (standard library): draws a figure's JSON scene to an accessible SVG at any camera and pose, with four tones from one light, cylinders, pipes, labels with leaders, and exact depth order for convex parts from separating planes.
- `figure_draw.py turn` sweeps each turn, slide and hinge group (and, with `--orbit`, the camera) and reports collision, crowding, order-cycle, tether and fixed-in-group faults at the first pose where each shows.
- New guide `craft/anatomy/draw.md` and example `examples/turning-scene.json`, which fails the motion audit on purpose; index, kit-api, turning-groups, later and the data README point to it.
- New tests `test_craft_anatomy_draw.py`: SVG structure and tones, camera and pose, bad input, the example's faults, a fixed scene that passes with the orbit, and the guide's check table against the script.

## [0.0.50] - 2026-11-27

Deck plan and structure check

- New `data/craft/decks/deck-types.csv`: eight deck types (seed, growth, sales, launch, demo, update, talk, proposal) with their usual length, arc, beats in order with the layouts that carry each, and what changes when the deck is sent ahead.
- New `data/craft/decks/layouts.csv`: 18 layouts with what each is for, the one thing it holds, its word budget and whether it resets attention.
- New `deck_plan.py` (stdlib): `plan TYPE` prints the slide list to fill in (`--read` for decks sent ahead, `--html` for marked section skeletons); `check DECK --type TYPE` reports missing beats, beats out of order, layouts over their word budget, three same-layout slides in a row, seven slides without a reset, an ask that is not last, and an early agenda; `--self-check` checks every type's own plan.
- `deck_check.py --type` takes the slide limit from the deck type. `template.html` is marked with beats and layouts, and a new `examples/seed-deck.html` passes both checks.
- New guide `craft/decks/plan-check.md`; `build.md`, `index.md`, `later.md`, the coverage map and the comparison table are updated.
- Tests: the self-check, the example passing both checks, each structural rule firing on a broken deck, plan output, the type limit, and the guide's rule table matching the script.

## [0.0.49] - 2026-11-27

Base paths for vague UI requests

- New `frontend-budget/vague-requests.md`: the four-step path for a request that names an area but no fault (match the area, ask once with at most four questions, measure one thing first, route on the answer), a table of 13 areas, four worked examples and what goes wrong.
- New `data/craft/frontend-budget/vague-paths.csv`: per area, the words that point to it, the questions to ask, the guide each answer leads to, a first measurement and a fallback.
- New `vague_path.py` (stdlib): `match TEXT` names the area, the questions and the routes, and exits 4 when no area matches so the agent asks which area instead of guessing; `check` proves every route file exists; `--self-check` runs sample complaints.
- `phase-routing.md` § 4 points to the new guide; `later.md`, the coverage map and the comparison table are updated.
- Tests: the script's self-check and route check, a JSON match, exit codes 4 and 2, and each worked example in the guide must match what the script says.

## [0.0.48] - 2026-11-27

Expo and React Native motion

- New `emil-motion/expo-motion.md`: the native tool ladder (native navigation first, then layout animations, shared values, gestures, scroll and keyboard, Lottie, Skia), what may animate, worklet and UI-thread rules, timing versus spring with numbers, press instead of hover, haptics, reduced motion with `useReducedMotion` and `ReduceMotion.System`, native-stack screen and sheet options, the 120 fps setting, and a device checklist.
- New `emil-motion/expo-recipes.md`: drag-to-close sheet with rubber band and release velocity, swipe-to-delete row, collapsing header on transform only, capped list entrance, keyboard-riding composer, measured tab indicator, toast, and a fire-once threshold for haptics. All code is our own, type-checked in strict mode against react-native 0.81 and Reanimated 4.8; none has been run on a device yet.
- New `tests/test_expo_recipes.py`: every tsx block type-checks when `EXPO_TYPES_DIR` points at the type packages (skipped otherwise), and no gesture callback sets React state. The Expo rows leave `later.md`.

## [0.0.47] - 2026-11-27

Mockup board for design reviews

- New `data/craft/design-review-qa/mockup_board.py`: `build` lays two or more HTML mockups side by side on a local board, live at 1280 and 390 px, with a pick, a 1-5 rating and a comment per mockup and an overall note; the board saves `feedback.json` or shows it for copying. It warns when two mockups are 90% alike, when one has no axis, and when two claim the same axis. `--baseline` adds the current state as `now` for "show me the 10"; `--shots` saves PNGs (exit 3 with no browser). `read` checks the feedback against its board and prints the pick (exit 4 with none, 2 for another board or a bad file).
- New `design-review-qa/mockup-step.md`: when to build mockups before the plan review, the brief, two or three directions on named axes, linting them, the board, reading the pick, and the built 10 for any dimension under 7. `plan-review-passes.md` Step 0 points to it; the parked image-generator row in `later.md` now names the board instead.
- New `tests/test_mockup_board.py` (8 tests, one drives the board in Chromium and reads the saved pick back).

## [0.0.46] - 2026-11-27

Feedback moves and UX laws

- New `emil-motion/feedback-and-laws.md`: five feedback moves (pulse to confirm, grow from the same element, icon swap with blur, rubber band past the edge, mask reveal), each with numbers, a never, CSS or JS and a still version for reduced motion.
- The same guide adds staging the focus and the three laws we had not named: Fitts's law (44 px touch, 24 px WCAG 2.2 floor, distance and edges), Hick's law (one primary action, grouped long menus, defaults) and the Doherty threshold (a response in 100 ms, progress past 400 ms, steps past 10 s), each with a check that measures it.
- Listed in `emil-motion/index.md`.

## [0.0.45] - 2026-11-27

Dealt page presets

- New `ult design deal "<trade or brief>" --kind KIND`: deals a palette, a type pairing, a hero, the page parts (nav, footer, close, rhythm, buttons, radius) and, for tech kinds, two section grounds that never clash plus a page ground.
- New `data/craft/taste/presets/`: 40 original palettes tagged by kind, trade and mood, and 43 type sets drawn from our own font table. Every palette is tested for 7:1 ink, 4.5:1 muted and button text, and 3:1 accent; the deal says whether the accent may also be link text.
- Brief words steer the deal toward matching trades and moods; a history in `.ultimatum/deal-history.json` keeps each pick out of the next few pages of the same kind. `--seed`, `--fresh`, `--no-save`, `--no-photos` (swaps photo-led parts), `--footage` (allows the film hero), `--css` (writes the tokens), `--json`.
- `page-plans.md` § Deal lists now points at the command; the taste `later.md` row and the comparison table are updated. New `tests/test_taste_deal.py` (17 tests).

## [0.0.44] - 2026-11-27

Render pass in a real browser

- New `data/craft/design-review-qa/render_check.py`: opens built pages in headless Chromium at 320 to 1920 wide and measures 28 rules a static lint cannot see: sideways scroll, wrapped buttons, painted contrast, tiny or tight text, line length, first-screen fit and dead bands, section spacing, covered text, text hidden at rest, broken images and script errors.
- Local pages only: non-local URLs are refused and requests to other hosts are blocked unless `--allow-remote` is passed. No browser means exit 3 and a skip line, never a pass.
- Reasoned waivers (`render-check: allow RULE: reason`), `--genre`, `--format github`, `--json`, `--shots` for a full-page PNG per width, `--rules`.
- Tuned against Hallmark's four exemplar pages: visually hidden text, hanging punctuation, manual line breaks, overlays and a declared full-palette posture no longer trip it.
- New examples `render-clean.html` (clean), `render-sloppy.html` and `render-sloppy-2.html` (together trigger every rule).
- New guide `render-check.md`; `page-lint.md`, the comparison and Hallmark `later.md` point at it.
- Tests: `test_render_check.py` (browser tests skip when no browser is found).

## [0.0.43] - 2026-11-27

Page lint covers every static gate

- `data/craft/design-review-qa/page_lint.py` rewritten: 87 rules (was 18) across colour, type, layout, effects, copy, motion, states, images and icons, each tied to a slop tell or a Hallmark gate.
- Real CSS parsing (nesting, `@keyframes`, `@media`), `var()` resolved from token blocks, WCAG contrast for hex, rgb, hsl, oklch and named colours.
- Reads component files (`.jsx`, `.tsx`, `.vue`, `.svelte`, `.astro`): class strings, `cn()`/`clsx()`, Tailwind utilities and variants, icon-library imports.
- New: `--genre` exemptions, reasoned waivers (`page-lint: allow RULE: reason`; no reason waives nothing), `--format github` annotations, `--rules`.
- New examples `sloppy-more.css`, `sloppy-more.html`, `sloppy-component.tsx`; together the sloppy examples trigger every rule and `clean.html` stays clean.
- `page-lint.md` rewritten with the full rule table; comparison and Hallmark `later.md` updated.
- Tests: `test_page_lint.py` (15).

## [0.0.42] - 2026-11-27

Landing and settings page anatomy

- New `website/references/craft/pages/`: `landing.md` (the questions a marketing page answers and their order, navigation, action pairs, explaining devices, a five-question first-screen test), `devtool-landing.md` (real code, catalogue, billing unit, path to a first request, text for coding agents) and `settings.md` (scopes, structure, save model, the row, danger actions, desktop, CLI and terminal UI settings, build order).
- `website/craft.md` points to the folder; frontend-budget `later.md` and its coverage map now point to it.
- Closes the frontend-budget gap in `docs/plans/comparison.md`.
- Tests: `test_craft_pages.py` (9).

## [0.0.41] - 2026-11-27

Anatomy figure audit

- New `data/craft/anatomy/figure_audit.py`: stdlib audit of a figure's JSON scene with the ten checks from the audit table (clearance, terminals, loose ends, folds, overlaps, crowding, stand-ins, wobble, seats, depth order); prints a count per check and each fault by name.
- New `craft/anatomy/audit.md`: the scene format, what each check means and what it cannot see; clean and faulty example scenes.
- `verify.md` audit table now uses the script's check names; `kit-api.md` and `later.md` point to the script.
- Closes the anatomy gap in `docs/plans/comparison.md`.
- Tests: `test_craft_anatomy_audit.py` (8).

## [0.0.40] - 2026-11-27

Interface icons and banner sizes

- New `craft/identity/icons.md`: choosing one icon library, drawing the few icons it lacks on a set grid, clean SVG export, accessibility.
- New `data/craft/identity/icon_check.py`: stdlib checker for a folder of SVG icons with 12 rules (viewBox, canvas size, fixed colours, mixed stroke and caps, text, rasters, transforms, editor leftovers, out of bounds, complexity); refuses DOCTYPE and entities.
- New `craft/identity/banners.md`: one-message banner rules, web ad sizes, dated social cover sizes, email headers, printed banners.
- Closes the third gap in `docs/plans/comparison.md`; UI UX Pro Max icon and banner rows remapped in the coverage map.
- Tests: `test_craft_identity_icons.py` (14).

## [0.0.39] - 2026-11-27

Slide decks: story, layouts, charts, a template and a checker.

- New `skills/website/references/craft/decks/`: `story.md` (audience, point and ask, deck types, arcs, a seed pitch slide by slide, headlines as sentences, copy patterns), `slides.md` (1920x1080 grid, type sizes for a room and a screen, fifteen layouts, bullets, colour, images, motion), `charts.md` (one message per chart, which chart, making the point visible) and `build.md` (format choice, PDF export, speaker notes, checking).
- New `data/craft/decks/template.html`: a four-slide HTML deck with keyboard navigation, hidden speaker notes and print styles that export one 1920x1080 page per slide.
- New `data/craft/decks/deck_check.py` (standard library, no network): twelve rules for headlines, word and bullet counts, nested bullets, big tables, missing alt text, small type, missing notes and deck length, with `--only`, `--json`, `--rules` and `--max-slides`.
- Topics checked against UI UX Pro Max's slides references (MIT); none of its text, data or scripts are used. The coverage map and `docs/plans/comparison.md` are updated; `craft.md` points to the new folder.
- Tests: `test_craft_decks.py`.

## [0.0.38] - 2026-11-27

A page linter for the checkable slop tells.

- New `data/craft/design-review-qa/page_lint.py` (standard library, no network): reads HTML and CSS, follows local stylesheets, and flags 18 tells from `slop-tells.csv` and `gates.csv`: purple gradients, gradient text, pure black or white, system or default main font, one radius everywhere, left-border cards, glows, frosted glass, marquees, a flat type scale, emoji headings, stock copy, vague calls to action, eyebrow chips, nested cards, placeholders and images without alt. Has `--only`, `--json` and `--rules`. Sample pages are in `examples/`.
- New guide `skills/website/references/craft/design-review-qa/page-lint.md`, linked from the design-review-qa index, `slop-tells.md`, and the hallmark and impeccable sets.
- New `docs/plans/comparison.md`: each rebuilt guide set scored against its upstream, with a list of what to fix.
- Tests: `test_page_lint.py`. The design-review-qa credential test now skips folders.

## [0.0.37] - 2026-11-27

React performance pack, in our own words.

- New `skills/work/references/craft/react-performance/`: ten worked before-and-after fixes (serial awaits, await in loops, streaming, client boundaries, dynamic imports, derived state, context values, deferred filtering, keys, pointer state), a measuring guide (build output, bundle analyzer, request timing, Profiler, Performance panel, Web Vitals, Lighthouse) and a guide to the scanner.
- New `data/craft/react-performance/react_scan.py` (standard library): a line-pattern scan for eleven rules, each tied to a rule in `react.md`, with `--only`, `--json` and `--rules`. Example files in `examples/`.
- These cover the topics of vercel-labs/agent-skills, which has no LICENSE file, so none of its text was used. `upstreams.json` and both CREDITS files say so.
- `react.md` points to the new folder. Tests: `test_craft_react_performance.py`.

## [0.0.36] - 2026-11-27

Coding discipline, in our own words.

- New `skills/work/references/craft/coding-discipline/`: think first (assumptions out loud, the two-readings test, when to ask, when to push back), smallest change (what not to build yet, a size test, a worked example), surgical diff (every changed line traces to the request) and checkable goals (a check that fails now, plans as step and check, when to stop looping).
- New `data/craft/coding-discipline/diff_scope.py` (standard library): reads `git diff -U0` and flags whitespace-only, quote-only, comment-only and reorder-only hunks and files outside an allow list.
- These cover the topics of multica-ai/andrej-karpathy-skills, which has no LICENSE file, so none of its text was read into or used in them. `upstreams.json` and both CREDITS files say so.
- `feature-planning.md` and `tdd.md` point to the new files. Tests: `test_craft_coding_discipline.py`.

## [0.0.35] - 2026-11-27

Apps: five checks before an AI-written login ships.

- `skills/website/references/app/auth.md` gains five checks, each with a test to run on the preview URL: no secret key in the code or bundle, the server decides who the user is and what they may touch, every table locked by row-level security, a sign-out that clears cookies and caches (with sign-out everywhere), and one error message for real and unknown emails.
- `app/checklist.md` lists the five checks under Sign-in. Tests: `test_auth_five_checks.py`.

## [0.0.34] - 2026-11-27

Apps: launch-day load and real-world conditions.

- New `skills/website/references/app/launch-load.md`: 20 launch-day items in five groups (spend limits that pause, attack protection, free-plan limits, pooler, region, indexes, pagination, N+1, CDN caching, images, signed uploads, background jobs, AI and email and SMS limits, live connections, a 10x load test on staging, phone alerts, rollback). Vendor names and numbers are marked to confirm on the vendor's page.
- New `skills/website/references/app/field-conditions.md`: 11 situations real users hit (network switch, slow 3G, captive portals, 30-second APIs, AI provider down, double submits, expired login, broken images, blank-screen errors, deleted deep links, no signal after paying), each with what to build and how to test.
- Worked example `data/app/field-demo.html` and `data/app/field-check.cjs`: Playwright against a local server, 12 checks, run in the tests when node and Playwright are present.
- `app/checklist.md` gains a load and real-world conditions section. Tests: `test_app_launch_guides.py`.

## [0.0.33] - 2026-11-27

UI UX Pro Max's brand, design-system and UI-styling topics rebuilt in our own words, with a starter token file built to CSS and Tailwind v4.
- The starter type scale lists `base` first, so the generated CSS shares no 8-word run with the bundled UI UX Pro Max data (the copy-check test).

## [0.0.32] - 2026-11-27

Frontend load budgets, rule precedence and phase routing rebuilt in our own words.

- Added frontend-budget craft references: 4 short files under `skills/work/references/craft/frontend-budget/`, indexed, each with a "Read when" opener.
- Covers how many skills load per phase (one base, one lead, at most two supports), loading at the start of a phase, a one-line load report, stacking rules, a precedence ladder for skill collisions, phase routing with ask-first for vague complaints, and who owns what among Ultimatum's own website packs with default rulings for common collisions.
- Adds what the source lacked: skill text treated as untrusted data, questions only when they change the outcome, and quoted measurements instead of guessed costs.
- Adds a stdlib script, `data/craft/frontend-budget/load_budget.py`: `size` estimates per-file token cost against limits, `plan` checks a phase plan and prints load lines. Tests: `test_craft_frontend_budget.py`.
- The third-party pack table and rulings, identity flow, page-type guides, agents and the network sync script are listed in `later.md`, not shipped.
- Test pin for Impeccable updated to `3c5e75f`, the commit the 0.0.26 rebuild was read at.

## [0.0.31] - 2026-11-27

Anthropic's skill, eval, MCP and web app testing methods rebuilt in our own words, with local lint and smoke scripts.

- Added Anthropic-method craft references: 7 short files under `skills/work/references/craft/anthropic-method/`, indexed, each with a "Read when" opener.
- Covers skill frontmatter limits and layout, eval iteration folders with baselines, grading records and reviewer roles, trigger tuning with a held-out split, MCP tool design (names, hints, results, two error channels, transport), MCP eval question sets, web app test recipes, and a design brief pass that points to the website craft.
- Adds what the source lacked: hint annotations are not a security control, HTTP transport checks from the security overlay, untrusted text in skills you update, and asking before any paid eval run.
- Adds six stdlib scripts in `data/craft/anthropic-method/`: `skill_lint.py`, `bench_summary.py`, `trigger_split.py`, `mcp_eval_check.py`, `mcp_smoke.py` and `with_ports.py`. Tests: `test_craft_anthropic_method.py`.
- Office documents, brand guidelines, fonts, the eval viewer, packaging, model-driven loops and SDK listings are listed in `later.md`, not shipped.

## [0.0.30] - 2026-11-27

gstack engineering skills rebuilt in our own words: office hours, plan and scope review, pre-landing review, ship, docs and retros.

- Added gstack engineering craft references: 9 short files under `skills/work/references/craft/gstack-eng/`, indexed, each with a "Read when" opener.
- Covers product office hours, scope review with grow/pick/hold/cut stances, engineering plan review with design-twice and red flags, an error and rescue map, a two-pass pre-landing review with quoted evidence and confidence, a ship pipeline with version states and bisectable commits, a docs release pass, retros from git history, and deny/ask/allow safety modes with an edit boundary.
- Adds what the source lacked: PR text and diffs treated as untrusted input, the security overlay on review and scope work, and the user's yes before scope changes, version bumps, pushes or hooks.
- Adds two stdlib scripts in `data/craft/gstack-eng/`: `command_guard.py` (tiers a shell command or path, and answers as a pre-tool hook that fails closed) and `retro_stats.py` (sessions, sizes, hotspots, focus and streak from `git log --numstat`). Tests: `test_craft_gstack_eng.py`.
- Investigate (absent at the pinned commit), specialist fan-out, helper binaries, hook installs and pitch coaching are listed in `later.md`, not shipped.

## [0.0.29] - 2026-11-27

Matt Pocock's skills rebuilt in our own words: questions, specs, tickets, design and test seams.

- Added Matt Pocock craft references for planning, design and tests: 7 short files under `skills/work/references/craft/mattpocock/`, indexed, each with a "Read when" opener.
- Covers question rounds over a decision frontier and questionnaires for absent experts, spec synthesis and ticket graphs with blocking edges, deep-module design words and design-it-twice, glossary entries and the bar for a decision record, logic and layout prototypes, test-seam agreement and client-shaped fakes, and TypeScript test data without casts plus package entry-point rules.
- Adds what the source lacked: answers, tickets and ADRs treated as untrusted input, a negative acceptance check for security-relevant slices, and the user's yes before remote issues or new dependencies.
- Adds two stdlib scripts in `data/craft/mattpocock/`: `ticket_order.py` (dependency order, ready set, cycle check for local tickets) and `entry_imports.py` (finds imports that bypass a package's entry files). Tests: `test_craft_mattpocock.py`.
- Setup, hook and install steps, and skills outside the brief, are listed in `later.md`, not shipped.

## [0.0.28] - 2026-11-27

Superpowers rebuilt in our own words: shaping, plans, debugging, review and branch close.

- Added Superpowers craft references for the build loop: 8 short files under `skills/work/references/craft/superpowers/`, indexed, each with a "Read when" opener.
- Covers the shaping conversation and build gate, writing and carrying out a plan (ledger, rulings, final review), deeper debugging moves, test judgement and mocks, review rounds, evidence per "done" claim, and worktree start and branch close.
- Adds what the source lacked: the security overlay on review focus and layered guards, review text treated as untrusted input, and the user's own words for push, merge and PR.
- Adds two stdlib scripts in `data/craft/superpowers/`: `wait_until.py` (poll with a timeout) and `find_polluter.py` (find the test that leaves a file behind; no shell). Tests: `test_craft_superpowers.py`.
- The SessionStart bootstrap, the brainstorm server and the source shell scripts are listed in `later.md`, not shipped.

## [0.0.27] - 2026-11-27

Caveman rebuilt in our own words: terse voice levels and memory-file compression.

- Work craft: new `caveman` folder: terse voice in three levels with a never-cut list and the cases that force full sentences; short commit, review and helper-report forms; compressing a memory file; task stances with stop rules.
- `check_compressed.py`, a stdlib checker that fails a compressed memory file when code, URLs, headings, numbers or negations went missing, with a passing and a failing example.
- Pointer from `context-efficiency.md` § 2 to the deeper terse-voice file.
- Source: JuliusBrussee/caveman at 47c61be, Apache-2.0; all wording and code are our own.

## [0.0.26] - 2026-11-27

Impeccable rebuilt in our own words: website audit, critique, hardening and copy.

- Website craft: new `impeccable` folder with 12 topics: audit scorecard, critique, hardening, microcopy, refine moves, adapting to contexts, native iOS and Android, direction process, surface details, delight and onboarding, and heavy browser techniques.
- Pointers from Taste, Hallmark, Emil motion and design review QA to the deeper Impeccable topics, instead of second copies.
- An example page for hardening (long text, right-to-left, Intl formats, top-layer popover, interrupted drag) with a 15-check Playwright script.
- Source: pbakaus/impeccable at 3c5e75f, Apache-2.0; all wording and code are our own.

## [0.0.25] - 2026-11-27

Taste part 2: the kit, effects and two new `ult` tools.

- Taste kit, our own code in `data/craft/taste/kit/`: a starter page and system stylesheet, all 16 named grounds, 19 interface fragments with a phone frame, 16 icon glyphs, and a diagram page.
- Three WebGL effects (grain-gradient, orb-sphere, grid-pulse), each inside the performance budget, with a CSS poster for reduced motion, phones and missing WebGL2.
- New stdlib scripts: `scripts/ultlib/copylint.py` flags generic page copy, and `scripts/ultlib/diagram.py` draws a diagram as SVG from a small JSON spec. Both are now `ult copylint` and `ult diagram`.
- Repo test tools: `tools/taste_contrast.cjs` measures text contrast on real pixels; `tools/taste_fx_check.cjs` checks the effects' budget and fallbacks in Chromium.
- All 129 keyword-matched coverage rows were reviewed; `later.md` now lists what ships and what is left (22 effects, effect parts, objects, moments, the icon resolver, more diagram layouts).

## [0.0.24] - 2026-11-27

Logo and identity guide, in our own words.

- New `skills/website/references/craft/identity/`: `logo.md` (kinds of mark, brief, drawing, lockups, tests, hand-over files, accessible SVG), `logo-colour.md` (one-colour first, contrast, a WCAG ratio snippet), `ai-logo.md` (prompting image models, copyright and trademark risks), `identity-kit.md` (favicons, manifest and app icons, social images, print sizes, file layout), `index.md` and `later.md`.
- `website/craft.md` points to it.
- New `tests/test_craft_identity.py`: shape, index, references, https links and the pointer.
- The topic list was checked against UI UX Pro Max's logo and identity references; none of its text or generators are used (copy check exit 0).

## [0.0.23] - 2026-11-27

Our own Google Fonts catalogue.

- `data/design-own/fonts.csv`: all 2,043 Google Fonts families, built by `tools/build_fonts.py` from Google Fonts' own METADATA.pb files and human-assessed tags (licence, kind, weights, italic, axes, scripts, designer, date added, specimen and CSS links); search words, mood and style columns and the quality score are ours.
- `ult design search "<need>" --in font` searches it; ties go to the better-made families.
- The website skill and `shared/design-skills.md` point to it.
- `tests/test_design_own_fonts.py`: builder check, known facts, real requests.

## [0.0.22] - 2026-11-27

Website: a legal-risk pass before launch.

- New `skills/website/references/app/legal-risk.md`: ten checks before going live, each ending in evidence. It covers: a data map built from the code, with fields that are never used deleted; a privacy page that names every outside service; account deletion that really deletes; a signed-out public-key test; children under 13; cancelling as easily as subscribing; no ad pixels or analytics before consent; a trademark search before buying the domain; keys moved to the server, with an AI spend cap; safe uploads and XSS; and asset licences.
- Says plainly that it is a risk check, not legal advice. Laws are named only as examples of what to look up for where the owner's users live.
- Linked from the go-live step, `app/checklist.md` and `launch-checklist.md` (which gains consent, trademark and licence items). New `tests/test_legal_risk.py`.

## [0.0.21] - 2026-11-26

Website design data: our own stack guideline tables.

- Own stack guideline tables for 12 stacks (astro, flutter, html-tailwind, nextjs, nuxtjs, react, react-native, shadcn, svelte, swiftui, threejs, vue; 707 rows), written from each framework's official docs and built by `tools/build_stacks.py`. Each row links its doc page on an allow-listed https host.
- Rows cover WCAG 2.2, reduced motion, forms, images, click-to-call, booking forms, sign-in, and Stripe Checkout where the stack has an official way to do it.
- `ult design` now lists our stack tables as well as the bundled ones; ours win when names match. New `tests/test_design_own_stacks.py`. The docs links were not fetched (blocked here), and only the three.js snippets were syntax-checked.

## [0.0.20] - 2026-11-26

Website design data: our own UX guideline and UI reasoning tables.

- Own `ux-guidelines.csv` (232 rows), each tied to a WCAG 2.2 success criterion where one applies, with a bad and a good code example and an https docs link, built by `tools/build_ux.py`; the build rejects any criterion number that is not in WCAG 2.2.
- Own `ui-reasoning.csv` (224 rows, one per product type), built by `tools/build_reasoning.py`; every style must exist in `styles.csv`, and habits the anti-generic lint bans may appear only under Anti_Patterns.
- New `tests/test_design_own_ux.py`, including 30 real `ult design search --in ux` requests. The docs links were not fetched (blocked here).

## [0.0.19] - 2026-11-26

Website design data: our own icon table.

- Own `icons.csv` (195 icons: 137 Lucide, 58 Phosphor), built by `tools/build_icons.py`, with local-business icons (phone, map pin, calendar, reviews, trades, health, food), Style, Licence and Accessible Name columns.
- Icon facts come from the projects' own metadata, cached in `icons-meta.json` (names, tags, licence, commit and npm version; no artwork): Lucide (ISC) and Phosphor (MIT). The build fails if an icon's React export was not found in the published package.
- New `tests/test_design_own_icons.py`, including 26 real `ult design search --in icon` requests.

## [0.0.18] - 2026-11-26

Website design data: our own app-interface, React performance, chart and motion tables.

- Own `app-interface.csv` (38 rows), `react-performance.csv` (49), `charts.csv` (27) and `motion.csv` (26, including three motion personalities), built by `tools/build_tables.py` from hand-written rows with a docs link on each row.
- App and React rows carry a bad and a good example; React docs links are limited to react.dev and nextjs.org; every chart library names its permissive licence; every motion row has a reduced-motion fallback.
- The app HTML and CSS examples were loaded in headless Chromium and the React examples syntax-checked with TypeScript; the docs links were not fetched (blocked here). New `tests/test_design_own_tables.py`.

## [0.0.17] - 2026-11-26

Website design data: our own product and landing-page tables.

- Own `data/design-own/products.csv` (224 product types: every line of `product-types.txt` plus every type in the third-party table) and `landing.csv` (52 page patterns: 21 local, 20 marketing, 17 app), built by `tools/build_products.py` and `tools/build_landing.py` from hand-written rows; `--check` fails if a CSV drifts from its rows.
- New columns for local businesses: Main Action, Trust Signals, Booking/Quote; landing adds Kind, Use When, Avoid When, Mobile, Accessibility and Slop Habits. `Landing Pattern Match` is kept so `ult design system` still joins the two.
- New `tests/test_design_own_products.py`: every style and pattern resolves, 47 product searches and 8 design-system briefs land on the right row, and a copy check against the third-party tables is clean.

## [0.0.16] - 2026-11-26

Website craft: Hallmark rebuilt in our own words.

- Website craft: new `skills/website/references/craft/hallmark/` (30 files plus `index.md`), rebuilt in our own words from the MIT-licensed Hallmark skill (nutlope/hallmark @ 04977e1): the floor and gate tiers, stamps and waivers, page shapes, hero postures, section compositions, themes, imagery slots, interaction states, motion and finish checks.
- Adds what the source lacks: local-business jobs (calls, bookings, quotes, trust signals), app screens (sign-up, pricing, dashboards, checkout), WCAG 2.2 and reduced-motion rules, and ties to the anti-generic lint.
- Five new tables under `data/craft/hallmark/` (90 gates, 21 page shapes, 8 hero postures, 17 compositions, 50 themes) with a README.
- Overlaps with Taste, `craft.md`, `copy.md` and `design-rules.md` point to those files instead of repeating them. Code snippets were run in headless Chromium; one reduced-motion bug found and fixed.
- Not shipped yet: the source's Node linters, theme tool, photo library and theme pictures (`later.md`). New `tests/test_craft_hallmark.py`.

## [0.0.15] - 2026-11-26

Website craft: gstack's design review and QA, rebuilt in our own words.

- Website craft: new `skills/website/references/craft/design-review-qa/` (23 files plus `index.md`), rebuilt in our own words from the design-review, plan-design-review, qa and qa-only parts of the MIT-licensed gstack (garrytan/gstack @ 7dace1f): review modes, first impression, page modes, visual and behaviour checklists, generic-look tells, flows, scoring and baselines, the fix loop, craft audit, plan review, second opinions, and QA taxonomy, health score, functional tests, reports and regression tests.
- Two Playwright scripts of our own: a design audit (fonts, overflow, tap targets, heading order, console errors, reduced motion) and a one-page QA sweep (broken links, dead buttons, silent forms, console errors), both run against a local scratch page with planted flaws.
- Three new tables under `data/craft/design-review-qa/` (74 design checks, 44 generic-look tells, 12 QA issue kinds) with a README.
- Findings use the blocker, major, minor and nit scale from `design-rules.md` and WCAG 2.2 criteria. Uses only the preinstalled Playwright, not gstack's browser daemon.
- `craft.md` points to the folder; `taste-critic` uses its second-opinion checks. Upstream record and credits updated; some gstack design rule names trace back to Impeccable (Apache-2.0), and only names and ideas were kept.
- Not shipped yet: image mockups, outside-model review, the fixture preview server and the shared dashboard (`later.md`). New `tests/test_craft_design_review_qa.py`.

## [0.0.14] - 2026-11-26

Website craft: Emil Kowalski's animation skills, rebuilt in our own words.

- Website craft: new `skills/website/references/craft/emil-motion/` (17 files plus `index.md`), rebuilt in our own words from the MIT-licensed skills at emilkowalski/skills @ 715c180: a motion gate, easing and duration, springs, component recipes, choreography, gestures, performance, reduced motion, review and audit, vocabulary, UI details, fluid interfaces, mobile web, worst-case data, prototype variants, and library and toast picks.
- Merges with the existing motion rules (`work` design motion, Taste motion, `libraries.md`) by pointer instead of repeating them.
- Five new tables under `data/craft/emil-motion/` (timing, symptoms, vocabulary, worst-case values, libraries) with a README.
- `craft.md` points to the folder; `taste-critic` checks product-UI motion against its gate and reduced-motion rules. Upstream record and credits updated.
- Not shipped yet: the native, Expo and Swift material (listed in `later.md`). New `tests/test_craft_emil_motion.py`.

## [0.0.13] - 2026-11-26

Website craft: the Anatomy skill, rebuilt in our own words.

- Website craft: new `skills/website/references/craft/anatomy/` (20 files plus `index.md`), rebuilt in our own words from the MIT-licensed Anatomy skill (wheresryan22/anatomy @ 1482e84): explanatory isometric figures, from when a figure earns its place through solid-part craft, shading, motion, WebGL and light-theme effects, turning parts, verification, print sheets, publishing and React.
- Adds WCAG 2.2 and reduced-motion rules, local-business and app uses, a worked bakery example, and ties to the anti-generic lint.
- New data table `data/craft/anatomy/figures.csv` (27 techniques) with a README, and our own isometric sketch `iso-slabs.html`, checked in Chromium.
- `craft.md` points to the Anatomy folder; `taste-critic` checks figures against its verify checklist. Upstream record and credits added.
- Not shipped yet: the source's kit code and scripts (listed in `later.md`). New `tests/test_craft_anatomy.py`.

## [0.0.12] - 2026-11-26

Website craft: the Taste skill, rebuilt in our own words.

- Website craft: new `skills/website/references/craft/taste/` (20 files plus `index.md`), rebuilt in our own words from the MIT-licensed Taste skill (Leonxlnx/taste-skill @ f6b7657): principles, copy and voice, page plans, system, layout and heroes, sections, place pages, cards and UI, photos, icons and diagrams, motion, moments and scenes, grounds and effects, effect parts, objects, accessibility, performance, quality gate, and a `later.md` of what is not shipped yet.
- Adds local-business and app sections, WCAG 2.2 AA and reduced-motion rules to every craft move, and keeps effects to software, gaming and hardware pages.
- New data table `data/craft/taste/patterns.csv` (grounds, effects, recipes, moments, scenes, heroes, pane pairings) with a README.
- `craft.md` points to the Taste craft folder; `taste-critic` scores Taste-built pages against its quality gate.
- Upstream record and credits updated to the commit rebuilt from (f6b7657).
- New `tests/test_craft_taste.py`: index completeness, file size and opening line, https links, relative references and § headings, CSV shape, no credentials, and the copy check against a local source checkout.

## [0.0.11] - 2026-11-26

Design tables, part 3: our own style guide replaces UI UX Pro Max's.

- `data/design-own/styles.csv`: 88 styles, every one of theirs by name (so the product table still finds them) plus eight new local ones: Local Service Clear, Neighbourhood Warm, Craft Workshop, Clinical Calm, Quiet Luxury, Photo-led Documentary, Public Service Plain and Print Zine.
- Each style says what it looks like, when to use it and when not, a starting palette, type, layout, motion with a reduced-motion fallback, the slop habits it invites, accessibility risks with WCAG 2.2 criteria, cost, CSS tokens, a CSS starter and a pre-ship checklist.
- Built by `tools/build_styles.py` from hand-written rows in `tools/style_rows/`; the build rejects rows that recommend a habit the anti-generic lint bans.
- `ult design system` now lists each chosen style's tokens and the slop to avoid.

## [0.0.10] - 2026-11-26

Design tables, part 2: our own font pairings replace UI UX Pro Max's.

- `data/design-own/typography.csv`: 85 pairings (theirs had 74) for local services, shops, apps, health, culture, community, games and eight non-Latin scripts, each with mood, uses, the weights to load, licence, fallback stacks, a Google Fonts link and notes on where it breaks.
- Built by `tools/build_typography.py`; weights, licences and scripts are checked against Google Fonts' own metadata, cached in `fonts-meta.json` so tests run offline.
- Tests hold the table to the type lint: no generic display face, no monospace body text, no body face in more than four pairings.
- Fix: searches for "news" no longer drop the word (plural trimming turned it into the stop word "new").
- `tools/copy_check.py --skip` leaves out cached third-party facts.

## [0.0.9] - 2026-11-26

Design tables, part 1: our own colour palettes replace UI UX Pro Max's.

- `data/design-own/colors.csv`: 224 palettes (all 194 business types plus 30 local services such as barbers, roofers, locksmiths, tutors and food trucks), in 17 colour families with notes on why they fit and the colour habits to avoid.
- Built by `tools/build_palettes.py` in OKLCH; every text pair meets WCAG 2.2 contrast (4.5:1) and the focus ring 3:1, and the brand colour stays clear of the error red. The tests re-check every row.
- `ult design` reads our table first and says which tables are ours; business searches understand everyday words ("coffee shop", "vet").
- `tools/copy_check.py` (shared with the skill rebuilds) confirms no 8-word run is shared with the upstream data.

## [0.0.8] - 2026-11-26

Website builder: every size of site, up to web apps with sign-in, a database and payments.

- New app guides in `skills/website/references/app/`: when a site needs to be an app, the default stack, Supabase (keys, data model, row-level security, the second-user test, migrations), sign-in (flows, server checks, redirects, abuse), Stripe (Checkout, webhooks as the source of truth, the customer portal, test mode, going live) and an app go-live checklist.
- Two new approvals: `ult gate approve data-model ... --file <migration>` (reopens when the file changes) and `live-payments` (used once).
- Intake asks about accounts, roles, data and payments when the site needs them; the route covers content sites and apps. The old "shops and apps are out of scope" rule is gone; the simplest fit (a payment link, a hosted shop) is still offered first.
- Member sites, client portals and online shops now go to the website workflow.

## [0.0.7] - 2026-11-26

Website designs: more AI-design habits to avoid.

- The anti-generic lint adds: arrows on every button, middle dots between words, cream backgrounds by default, sparkle icons, pulsing green "live" dots, blurry glows behind the hero, coloured left borders, three icon cards in a row, sections fading in on scroll, clipped two-word sentences, stock words ("quiet", "real" and similar) and stats nobody can back up.
- `copy.md`: "How it works" is the real steps as a short list, not three matching boxes.

## [0.0.6] - 2026-11-26

Website designs: a longer list of AI-design habits to avoid.

- The anti-generic lint in `design-rules.md` is grouped into type, layout, colour and words, and adds: default display serifs, italics in every title, tight letter-spacing everywhere, monospace for prose, ALL CAPS subtitles and eyebrow labels, full stops in titles, bordered boxes and squircles everywhere, decorative pills and tags, dividers everywhere, code-style labels, over-detailed mockups and diagrams, many tints of one colour, gradient backgrounds, dithering and ASCII art, and padded or repeated copy.
- `ultimatum:taste-critic` checks the full lint and marks each hit as major.

## [0.0.5] - 2026-11-26

Ultimatum is now a website builder plus the coding core. Shops, launches, social media and video are on hold; everything removed can be restored from commit `9643d69`.

- Removed the six head plugins (`ultimatum-app-launch`, `-ecommerce-launch`, `-event-launch`, `-website-launch`, `-social-media`, `-video`), the shared `teams/` folder, `tools/sync_plugins.py`, and the social, video, motion, business and launch skills and toolbelt commands.
- New `ultimatum:website` skill: intake, a one-page brief the owner approves, three design directions, the build, a browser check, the review loop and go-live. Website guides now live in `skills/website/references/`.
- `ultimatum:taste-critic` and `ultimatum:compliance-reviewer` review websites only; their film checks are gone.
- Approval gates are brief, mockup, publish and deploy.
- `ult-start` no longer lists plugins. The marketplace lists one plugin.
- README, CONTRIBUTING, CI and the image prompts cover the website workflow only.

## [0.0.4] - 2026-11-26

Design tables: `ult design` searches UI UX Pro Max's design data offline. All seven plugins move to 0.0.4.

- New `data/design/`: 12 tables (products, styles, palettes, font pairs, landing patterns, UI reasoning, UX guidelines, app interface, React performance, charts, motion, icons) and 12 stack guides, from nextlevelbuilder/ui-ux-pro-max-skill at `3442615`, shipped with its MIT licence. `NOTICE.md` lists the changes: deprecated styles and bookkeeping columns dropped, each product linked to a landing pattern that exists, cells trimmed. `tools/import_design_data.py` repeats the import.
- New `ult design search "<words>" --in DOMAIN` (BM25 ranking) and `ult design system "<brief>" [--stack NAME]`: a starting style, palette, fonts, page pattern, things to avoid, and the most severe UX and stack checks for the brief. Everyday words ("coffee", "gym", "nonprofit", "plumber") map to the table's business types; niche checks (maps, AI, spatial, security) only show when the brief names them. Search code is original.
- The design skill, website directions and shared design-skills guide use `ult design system` when there is no brand yet.
- `ult website`/`ult motion` now recognise installed `ui-ux-pro-max`, `hallmark`, `anatomy` and `animejs` skills.
- Head plugins get a copy of `data/design/` through `tools/sync_plugins.py`.

## [0.0.3] - 2026-11-26

Creator Cut: a third video style for short-form talking-head content. All seven plugins move to 0.0.3.

- New `teams/creator-cut/` (guide, hooks, edit): intake, transcript, a paper edit approved before rendering, rough cut, finish, review and delivery for vertical shorts cut from someone talking to camera, a podcast or a stream.
- New `ult cut`: `silences` finds pauses with ffmpeg and writes a cut plan, `check` flags slow hooks, long takes and over-length cuts, `render` makes jump cuts with optional punch-ins and a 9:16 1080x1920 crop, `deliver` runs the export check and records it.
- New `papercut` gate.
- Plain-chat routing: talking-head, jump-cut, shorts and clip requests go to `ultimatum-video:video` as the `creator` workflow.

## [0.0.2] - 2026-11-26

Design skills and cleaner code. All seven plugins move to 0.0.2 because each ships the same toolbelt.

- `ult website` and `ult motion` print a `design-skill:` line on visual jobs. It names an installed design skill (for example Anthropic's `frontend-design`, or a renderer's own skill such as Remotion's) to read before the directions or storyboard, or says none is installed. It only looks in local skill folders and skips Ultimatum's own.
- New `teams/shared/design-skills.md`: how to use an installed design skill without skipping a gate, and how to start from a design the user made in Claude Design (tokens, critique, approval, build, compare).
- The core design skill starts by using the user's design skill or Claude Design file.
- Code quality: removed unused imports and variables, re-raised parse errors without the extra traceback, and added a `ruff.toml` with real-bug rules plus a CI lint job.
- Tests no longer see the machine's installed skills (`ULTIMATUM_SKILL_DIRS`).

## [0.0.1] - 2026-11-26

Version numbers restart here. Every plugin carries 0.0.1, and later releases go 0.0.2, 0.0.3 and so on. The 1.0.0 to 1.0.3 builds below were never released; everything in them ships in 0.0.1.

### Audio files (was 1.0.3)

Music and voice end as real, licensed, mixed files instead of prompts.

- New `ult audio` commands (local ffmpeg only):
  - `mix VOICE MUSIC --out FILE`: ducks the music under the voice with a sidechain compressor, normalises in two passes to -14 LUFS with true peak at most -1 dBTP, can put the mix on a video, and prints the measured numbers (exit 1 when out of range).
  - `credits add` and `credits check`: rows in `brand/sound-credits.md`; the check blocks non-commercial or missing licences, flags owed credits and audio files with no row, and has a stricter `--use paid-ad` mode.
- Audio guide order: ElevenLabs (with a yes before spending credits), then own or licensed tracks, then Suno only by hand when asked.
- Shared defaults gain rule 7, "Real files first": deliver the made and checked file, not a prompt, unless no local tool or authorized connector can make it.

### Finished social files (was 1.0.2)

Social Media now makes finished, checked files instead of only scripts and prompts.

- New `ult posts` commands (local only; nothing is posted or scheduled):
  - `slides`: carousel or story slides as HTML at the platform's exact size inside its safe zone, rendered to PNG with the local Playwright (`--render`), plus `alt-text.txt`.
  - `captions`: burns captions into a video above the platform's bottom buttons, from a script (timing spread by word count), an SRT file, or a local whisper.cpp model; keeps the SRT for upload.
  - `check`: image and video size, aspect, length, file size, caption length and hashtag count per platform; exit 1 on blockers.
  - `specs`: the sizes, limits and safe zones the checks use, dated so they are confirmed before relying on them.
  - `calendar`: the posting plan as a CSV sheet (for a scheduler's bulk import) or an .ics calendar, with warnings for more than one post a day or a missing hook type.
  - `variant add|result|next`: hook variants and their real numbers; ranks hook types by signups per 1,000 views and never fills in missing numbers.
- Social media guides (`guide.md`, `loop.md`, `formats.md`, carousel style) and the Social Media skill point to these commands.

### Store building (was 1.0.1)

E-commerce Launch now builds and checks a real store instead of only describing one. Every plugin ships the same `ult` toolbelt, so all seven carry it.

- New `ult shop` commands (standard library, local files only):
  - `catalog`: reads a product sheet or an Etsy export, lists blockers (missing price, repeated SKU, cost at or above price) and fixes (no weight, image, alt text), and writes a Shopify or WooCommerce import CSV with every product as a draft.
  - `numbers`: money left per sale after cost, shipping, fees and returns, the most an ad can cost per sale, break-even ROAS and sales needed for monthly costs.
  - `scaffold`: a starter static store from the sheet, with Product structured data, policy stubs, a 404 page and Stripe Payment Link buttons.
  - `check`: pre-launch check of any folder of store pages (title, description, viewport, h1, alt text, heavy or missing images, dead links, Product data, link previews).
  - `emails`: welcome, abandoned cart, order and shipping email templates with a placeholder list.
  - `test-order`: writes a Playwright script that walks home to checkout at phone size with a screenshot per step, typing a card only on a Stripe test-mode checkout.
- E-commerce Launch: new `store-build.md` (Shopify, WooCommerce and Stripe build paths, and the test order); the skill, catalogue, checkout and launch checklist use the new commands; a "real files first" rule.

### The plugin suite (was 1.0.0)

Ultimatum is a suite of plugins released together from one marketplace. Each one stands alone: none depends on another.

| Plugin | What it does |
|---|---|
| `ultimatum` | The default way of answering: short answers first, coding work, and a pointer to the right plugin for everything else |
| `ultimatum-website-launch` | Launching small business, local service, portfolio and creator sites |
| `ultimatum-ecommerce-launch` | Launching online stores |
| `ultimatum-app-launch` | Launching web apps, mobile apps and subscription products |
| `ultimatum-event-launch` | Promoting workshops, classes, webinars, openings, fundraisers and ticketed shows |
| `ultimatum-social-media` | Social posts, campaigns and video, on their own or outside a launch |
| `ultimatum-video` | One finished video: product ads, explainers and brand films |

Each launch plugin is one head skill, `launch`, that runs its own Business, Website, Social Media, Brand Film and Motion Graphics teams from guides shipped inside it, with its own `taste-critic` and `compliance-reviewer` agents and its own copy of the `ult` toolbelt. `ultimatum-social-media` is a head of its own, `social-media`, with the Social Media, Motion Graphics, Brand Film and Editors guides. Heads register no hooks.


#### ultimatum

- New `ult-start` SessionStart hook: when a chat starts, one line with the version, a self-check of the work skill and toolbelt, the Ultimatum plugins that are on, and whether the chat is held to 200K tokens. `ult context --cap 200000` sets that cap (`autoCompactWindow` in your user settings) from the next chat. `ULTIMATUM_START=0` turns the line off.
- The default way of working: short plain answers first, deeper only when needed, helpers only when they save time. Coding goes to `/ultimatum:work`.
- `ult-pick` (the UserPromptSubmit hook) adds a short style note to plain questions (`ULTIMATUM_STYLE=0` drops it), starts `ultimatum:work` for coding, and sends launch, business, social and video prompts to the matching plugin's skill, or says to install it with `/plugin install <plugin>@ultimatum`.
- Writing style (shared by every plugin through `shared/defaults.md`): a one-line result by default ("Login works."), with fix and check details only when asked, when a check failed or was skipped, or when the user must decide; otherwise terse bullets, no recap or filler, questions as a numbered list with a recommended answer, and one next step at the end. Easier to scan and fewer tokens.
- `ult board` and `ult notes` (in every plugin's toolbelt): on big projects, one Markdown card per piece of work (backlog, doing, blocked, done, with its check and files) and linked notes for decisions (`[[topic]]` links between notes and cards, so `.ultimatum/notes/` also opens as an Obsidian vault). Every head and the `work` skill run `ult board show` first on a big project, so work resumes from the right card after lost context. Local and git-ignored; small jobs skip it.
- Graphify on big codebases: used from the start when installed (refreshing a stale graph with the no-model `graphify update .`); when missing, the report suggests installing it once. Ultimatum never installs it.
- Longer intake: every head now asks in rounds of 4 questions (AskUserQuestion's limit), repeated until each brief field is filled, instead of one batch of 5-8. Each question has a recommended answer and a "Skip, use your pick" option.
- `/ultimatum:status` and `/ultimatum:doctor` can be invoked by the model; `/ultimatum:setup` stays user-only.
- Film routing: requests for a brand film, cinematic or emotional ad, or documentary-style spot route to `film` before motion. `ult film` plans the film, checks the footage manifest, tracked media and voiceover pace (`--check`) and runs the export check (`--deliver`). New gates: `story`, `sourcing`, `animatic`.
- `ult launch` prints the launch kind (website, ecommerce, app or event) and the head plugin that handles it; `--kind` sets it by hand. Event launches (workshops, classes, webinars, meetups, openings, fundraisers, ticketed shows) are detected before the other kinds.
- Launch routing recognises store, app and local-business launches ("launch my online candle shop", "launch our SaaS app"). Developer phrases such as "launch the app in debug mode" stay with coding.
- TikTok, Instagram Reels and YouTube Shorts requests route to social media; plain questions such as "What is TikTok?" stay in chat.
- The toolbelt finds team guides inside whichever head runs it (`teams/<team>/...` resolves to `skills/<head>/references/<team>/...`).

#### Team guides (`teams/`, shipped inside each head)

- Business: positioning before visuals, kept in one `brand/brand.md`, with brief, interview and numbers guides.
- Website: three HTML directions with distinct motion, screenshotted at 375, 768 and 1440 px and scored by the taste critic (8/10 within 3 rounds), plus design rules, a planner and a craft guide (commit to one tone, display and body type pair, colour variables with one accent, deliberate grid breaks, surface texture, one designed motion moment). Small fixes skip the mockup but keep the browser check.
- Social Media: picks Brand Film or Motion Graphics per piece, a hook type per post, a results loop read about 48 hours after posting, a weekly top and bottom three, and a learnings log. Nothing is posted without approval.
- Motion Graphics: storyboard, audio sheet, animation timed to voice and beats, sound effects, and a loudness check (about -14 LUFS, -1 dBTP). Sound effects are CC0 first, with credits logged.
- Brand Film: story, sourcing, animatic and video gates; legal footage lanes (own footage, free stock, paid stock, AI b-roll) with costs and consent; score-first editing, grading and sound. Spend needs approval, a photoreal AI person is never the hero, and media stays out of Git.
- Editors: hand-off to DaVinci Resolve, Premiere Pro or Final Cut Pro (timeline files, project layout, export), with HyperFrames when there is no editor.
- Website libraries: when to use React Bits, Watermelon UI and Anime.js, with licence notes.
- Social Media scope and style guides (own footage, product demo, carousels and stills).
- Video: one pipeline for every video (script, shots, pictures, audio, assembly, review, yes); Higgsfield through its MCP for product video with a credit check before each generation; ElevenLabs by default for voice, music and sound effects, Suno by hand as an option.
- Shared licence notes and the two read-only reviewer agents.
- `tools/sync_plugins.py` copies the guides, agents and toolbelt into every head; `--check` runs in CI and fails on drift. Edit `teams/` and core, never the copies.

#### ultimatum-website-launch

- Launch manager for small business, local service, portfolio and creator sites.
- References: intake, route (site size, host, domain), pages and local SEO, playbooks for restaurants, salons, clinics, trades, consultants, portfolios and studios, a copy guide (headlines, buttons, service and about pages, reviews, meta), and a launch checklist with 30-day numbers.

#### ultimatum-ecommerce-launch

- Launch manager for online stores.
- References: store intake, platform and theme choice, catalogue (with a CSV example) and product photos, checkout and operations (payment tests, tax, shipping rates, theme licences), policy pages, a launch week day by day with a real test order, a first-30-days review, and common beginner mistakes.

#### ultimatum-app-launch

- Launch manager for web apps, mobile apps, B2B tools, APIs and subscriptions.
- References: product intake, waitlist, beta and public paths, pricing and billing (with a billing test script and pricing page examples), sign-up and activation, onboarding emails, a launch-week plan, trust basics, 30-day metrics, and common beginner mistakes.

#### ultimatum-event-launch

- Launch manager for public events, working back from the date.
- References: event intake, route, ticketing and sign-up, a countdown promotion plan, a day-of run sheet, follow-up afterwards and a launch checklist.

#### ultimatum-ecommerce-launch (video)

- Higgsfield through its MCP is the default for product and social video, with the credit-check loop in `video/higgsfield.md`.

#### ultimatum-social-media

- Social media head for single posts, campaigns and ongoing channels.
- Picks a video style per piece, plans carousels and posts, and hands edits to the user's editor. Nothing is posted without approval.
- Every video now follows the shared video pipeline in `video/guide.md`.

#### ultimatum-video

- New head for making one finished video: product ads, UGC-style clips, explainers, feature demos and brand films (`/ultimatum-video:video`).
- One fixed pipeline: script, shots (storyboard approval), pictures, audio, assembly, review with both reviewer agents, then the user's yes.
- Product and social video uses Higgsfield through its MCP: credit check, plan with costs, yes, one generation, review. Motion graphics is the second choice.
- ElevenLabs is the default for voice, music and sound effects; Suno stays as a manual option.

## Core development build

The core-only build of `ultimatum` that came before the suite. Everything below is new since the 0.x previews.



#### Added
- `ult route "<task>"`: a local, deterministic router (no model call). It picks a mode (FAST, STANDARD, DEEP, RECOVERY), one route, up to two add-ons and the security overlay, and lists only the reference files to read with their token cost. Routes and add-ons live in `skills/work/modules.json`. `--eval FILE` scores it against labelled tasks.
- New guidance modules: UI design (`design/design.md`), motion (`design/motion.md`), component selection (`design/components.md`), MCP server building and skill authoring.
- `ult components "<need>"`: offline lookup of permissively licensed component and animation libraries. Restricted or unlicensed ones are hidden unless `--all`, and then flagged, with MIT alternatives listed.
- `ult upstreams`: the reviewed upstream projects with pinned revisions, licences and decisions.
- `ult learn`: local lessons (`add`, `list`, `prune`), automatic observation at the end of each turn (counts and categories only; `ULTIMATUM_OBSERVE=0` turns it off), and `propose`, which writes redacted improvement proposals from a fixed allow-list. Nothing leaves the machine unless you approve `/ultimatum:learn submit`.
- `ult budget`, `ult sync export|import` (copy lessons to a folder such as a clone of your own private repo), and `ult update status|setup|migrate`.
- Management skills that cost nothing at startup (`disable-model-invocation`): `/ultimatum:status`, `setup`, `sync`, `learn`, `skills`, `budget`, `eval`, `doctor`, `rollback`, `migrate`.
- `/ultimatum:setup` turns on marketplace auto-update once (with a backup of `~/.claude/settings.json`), and explains the cloud and running-session steps.
- CI fails a pull request that changes the plugin without bumping the version and adding a changelog entry.
- Static size tests for the always-loaded skill body, descriptions, management skills and references.
- Live A/B runner arms for plain Claude Code, 0.4.1 and 1.0, with a total spend cap (`--max-total-usd`).
- Architecture Guardian. `ult arch check` finds import cycles (Python and JS/TS, plus Graphify's EXTRACTED import edges when `graphify-out/graph.json` exists), duplicated blocks, oversized files and functions, placeholder code, naming outliers, unused private functions and untested changed modules. `--changed` limits it to the git diff. `ult arch baseline` plus `--drift` report only new findings. `--strict` exits 1 on cycles or placeholders. `--record` adds finding counts (no paths or code) to local observations.
- `architecture` add-on (`references/architecture.md`). It loads for the large route, refactors, structural words and code reviews, and never for small, handoff, improve or security routes. Add-ons gained a `with_routes` field for this.
- The live A/B gates its pass on code quality: a task passes only if its graders pass and `ult arch` finds no new cycle or placeholder. New architecture findings are reported next to tokens and cost.
- `ult audit start` and `ult audit finish`. Start creates the audit ledger, runs the offline scan and writes a findings skeleton that records which scanners did not run. Finish checks the ledger, validates the findings and renders the report. Together they produce the audit deliverables without the model reading the long audit procedure.
- `ult route` prints a one-line `do:` contract for routes that have a deterministic deliverable: sec-audit, bug and ci-pr.
- `ult arch deps <path> [--reverse] [--depth N]`: lists one file's neighbours in the import graph, so the full graph never enters the chat.
- `evals/live/analyze.py` reports token waste from live A/B transcripts: first-call context, cache writes, large tool results, rereads, polling, and tests run without `ult run`.
- The router sends defect reports that never say "bug" (symptoms such as "drops", "returns None", `KeyError` or HTTP 500s) to the bug route. A lone symptom verb in a feature request still routes to feature. Route accuracy did not drop on any held-out set; holdout3 went from 46/60 to 47/60.
- Three local learning signals, saved as counts only: `poll-sleep`, `raw-test-output` and `reread`. Each one maps to a fixed lesson.
- `ult route --cat` prints the listed references (and the security guide when the overlay is on) after the routing lines, so routing and reading take one tool call instead of two.

- **Launch team.** A plain request such as "Help me launch my business" starts `/ultimatum:launch`. The Launch Manager keeps one shared brief and every approval: Business drafts a build brief, the user approves it, Website shows its mockup for a separate approval, Social drafts while Website builds, and publishing waits for the user's yes plus a checked live link. `ult launch` shows the board and the next step.
- **Business** (`/ultimatum:business`, or "What's stopping people from booking?"): researcher, marketing planner and analyst roles; each point is labelled observed or guessed. Advice changes nothing; a requested change is handed off within its scope. `ult business --start-brief` adds a draft build brief. Ideas from Corey Haines's MIT Marketing Skills, in our own wording (see CREDITS).
- **Social Media** (`/ultimatum:social-media`, or "Plan a week of posts"): one channel, posts with one clear next step, what to measure, a video step to Motion when one helps, a claims/links/tracking review, then the publish gate. `ult social --results` records what the campaign did for Business and Launch.
- **Approvals.** `ult gate status|check|approve|revise|done` for brief, mockup, storyboard, video, publish and deploy, kept in `.ultimatum/approvals.json`. Each approval stores the user's words and a fingerprint of the build brief (and of the approved file); a later edit reads "changed", so a resumed project never treats a draft as approved. Publish and deploy approvals are used once. A brief with empty Audience, Offer or Main visitor action cannot be approved.
- Motion: `--deliver FILE` blocks on open review blockers or export warnings and records the checked export; `--save-style` writes the reusable style guide only after the finished video is approved; later videos reuse it, and a reference or "fresh style" request starts standalone. /brag is optional for the first launch video.
- Shared rules: Context7 for library docs, Composio only read-only and when the user authorized the app, no credentials anywhere, and say what was actually accessed. Every deploy, publish, post, campaign, customer-record change or spend needs its own yes.
- **Motion Graphics workflow.** `/ultimatum:motion-graphics` (or a plain request such as "Make a 15 second logo reveal video") plans a clip as brief → story and sound → storyboard, then **stops for storyboard approval** before production animation. Small changes to an existing clip skip the storyboard. The Animator prefers HyperFrames when installed, then HTML captured with Playwright, then plain ffmpeg; timing and easing follow `coding/guides/motion.md`. `ult motion "<task>"` prints the plan; `ult motion --approve "…"` records the approved storyboard in the shared brief.
- `ult beats FILE`: beat times from librosa when installed (labelled **suggested beats**), otherwise loud onsets found with ffmpeg (labelled **possible cues**). Both are suggestions to check against the audio before timing cuts. `ult media FILE`: duration, size, fps, codecs and loudness (LUFS) of an export, with warnings for common export problems.
- **Review loop.** The Reviewer reports to the Manager, who marks blockers and sends them back to the Builder or Animator; the Reviewer rechecks each fix. Open blockers stop delivery; minor findings go in the report. `ult loop add|triage|fixed|recheck|status` tracks this when there are several findings.
- **Chat mode.** Plain questions are answered directly with no workflow; the prompt hook now routes questions to chat, coding to Work, websites (including animations inside a site) to Website, and standalone clips to Motion Graphics. Typed commands still win.
- Search escalation: after two focused searches, or when a change spans 3+ areas, run `ult map`, then Graphify for one question, then confirm in the code.
- Credits and upstream pins for HyperFrames, gstack, Matt Pocock's skills, shadcn/ui, Graphify, Caveman and the Karpathy guidelines.

- **Two workflows.** `/ultimatum:work` stays the default for chat and coding. The new `/ultimatum:website` handles website work: the Manager writes one brief (goal, design direction, 3 to 6 browser checks), an optional Designer runs only when a new look is needed, the Builder works mobile, desktop and keyboard, the Reviewer checks the real page, and the Manager fixes, rechecks and reports. Small website jobs stay solo. `ult website "<task>" [--json|--cat]` prints the plan and only the files it needs, and never loads the Work skill.
- **Website starts from plain chat.** A new `UserPromptSubmit` hook (`scripts/ult-pick`, local, stdlib only) adds one line pointing Claude to `/ultimatum:website` when a prompt is clearly website work: a website named outright ("Build me a website for my coffee shop"), or interface words such as "mobile menu" inside a project that is a website (an `index.html` or a web framework in `package.json`). Other prompts get nothing. Prompts starting with `/` are left alone, so explicit commands still win. `ULTIMATUM_AUTO=0` turns it off.
- **Work starts from plain chat too.** The same hook now sends other coding requests ("Fix the CSV export") to `/ultimatum:work`, so it no longer depends on a line in the user's `CLAUDE.md`. `ultlib/pick.py` decides website, work or chat offline. Plain questions, questions about how code works, writing help and small talk get nothing. Measured offline: 362/386 labelled coding tasks start a workflow (the 23 code questions plus one task that starts with `/` stay in chat on purpose); 40/40 plain-chat messages stay in chat; on two unseen sets written afterwards, 30/30 + 20/20 coding and 30/30 + 19/20 chat (first set scored 23/30 and 26/30 before fixes).
- **Small website fixes stay on the bug.** The browser check runs before the edit; findings that were already there are reported as "seen, not changed", and tap targets are resized only in new or redesigned parts. `ult website` prints the scope line.
- **Visual planning for new sites and redesigns.** The Manager acts as Planner and writes one brief (audience, first action, pages and sections, mobile layout, assumptions, `[[PLACEHOLDER: …]]` for missing business facts, build phases each with a check). The Designer adds one visual direction to the same brief. The Planner turns it into a ready-to-paste ChatGPT mockup prompt (a grayscale wireframe first when the layout needs review), shows a mockup when an image tool is available, explains it in plain words and stops: no production code until the user approves the look. `ult website --approve "…" [--image PATH]` records the approval in the brief's Approved direction section, which the Builder builds from and the Reviewer compares against on phone and desktop. `ult website` prints a `gate:` line and loads the new `skills/website/planner.md` only on this path. Small fixes keep the short path (brief, focused fix, browser check) with no approval stop.
- `ult route` adds `workflow: website` on the same rule. The Work skill then switches to the website workflow, unless the user typed `/ultimatum:work`.
- The Website Manager runs the whole job: a new site or redesign gets Design, Build and a browser Review; a plain fix keeps the current look, reproduces the bug, fixes it and checks it in a browser at 375 and 1280 px. It decides on its own when a helper (Designer, Builder, Reviewer) is worth it, leaves the user a preview, and lists exactly what it still needs (photos, text, domain, hosting login).
- **Shared defaults** in one file (`shared/defaults.md`): answer first in plain words, reuse what works, plan to fit the job, report only what was checked. Every `--cat` prints it first.
- **Shared skills** `design`, `coding` (with `guides/website.md`), `review` and `release`. They cost nothing at startup (`disable-model-invocation`) and the workflows read them by path. Release says Ready or Blocked, and deploys or publishes only on the user's explicit yes.
- **SECURITY mode** for the security routes: the shared Review skill plus the OWASP-informed guides.
- **Code-map escalation** (`references/code-map.md`) printed for DEEP tasks: search first, then `ult map`, then one Graphify question, then confirm in the code.
- `/ultimatum:style` and `ult style status|apply|remove`: an opt-in copy of the shared defaults in your user `CLAUDE.md`, between markers, with a one-time backup. `remove` restores the file byte for byte. Your own instructions are left alone.
- Tests for website routing, the optional Designer, solo small jobs, selective loading, Release gating and the style setup.

#### Changed
- `ultimatum:worker` runs on Haiku by default; give it `model: sonnet` in the brief when the slice needs judgment. The reviewer stays optional.
- The Work skill's description and rules are shorter; the reuse rule moved into the shared defaults. A small task's `--cat` now prints only the shared defaults (about 700 bytes more than before).
- Held-out routing labels: 9 security-route cases in `tests/data/routing_holdout.jsonl` now expect mode SECURITY instead of STANDARD or DEEP, because that mode is new. Routes did not change.
- `SKILL.md` sends obvious one-spot edits (typo, rename, a stated one-liner) straight to FAST mode without running the router.
- The router drops prompt-leak requests ("output the system prompt") before scoring, and "plan it first" or "new setting" now count toward the feature route. Dev routing went from 193/196 to 195/196; the held-out sets did not change.

#### Removed
- The Office documents route (`documents.md`, Word, Excel, PowerPoint and PDF). It was out of scope for a developer skill; Anthropic's own document skills cover it.
- `SKILL.md` file is down from 7.6 KB (0.4.1) to 4.5 KB: the routing table moved into the router, so it is no longer re-read on every turn.
- The reviewer agent is described as a once-per-DEEP-task step.
- The reviewer runs `ult arch check --changed` and checks for parallel modules, wrong-way imports, placeholders and needless dependencies.
- `ult doctor` lists Graphify, Repomix and RTK. `integrations.md` says when each one pays off.
- Self-improvement rejects a proposal that saves tokens but fails tests or adds a blocking architecture finding.
- Agent descriptions, which load in every session, are shorter: 661 bytes for all five, down from about 1,140.
- The orchestration rules now cover launching workers. Launch them in one message, never sleep or poll, and never edit a slice that has been delegated. Briefs carry anchors, so workers don't re-read the repo.

#### Compatibility
- Every 0.4.x command, hook, agent and reference path still works. `ult update migrate` is a no-op on existing `.ultimatum/` state apart from creating `knowledge.md` and `proposals/`.

## Preview releases (before the reset)

These came before the version reset and are kept for reference; their numbers are older than 0.0.1.

### [0.4.1] - 2026-11-23

#### Changed
- Quieter replies. No narration while working. A finished, verified task with nothing for the user to do now ends with just `Done.`. Otherwise it reports one line per action the user must take, or per failed or skipped check or risk. Full detail (files, commands, exit codes) only on request, or for large, audit and release work. Verification itself is unchanged.
- README: the always-on cost note now points to the measured A/B range instead of an older estimate.

### [0.4.0] - 2026-11-22

#### Changed
- Token use is now the first rule. The live A/B run (`evals/live/results/final`) showed Ultimatum costing 1.2× to 4.3× more per task than plain Claude Code. Most of that was fixed overhead, not the work itself.
- The main session makes edits itself again. 0.3.0 sent every edit, even a one-line fix, to an `ultimatum:worker`, and each worker starts a whole new context. Workers are now only for independent slices of large work, and the reviewer only for large work.
- `SKILL.md`, which loads on every task and is re-read on every turn, is down from 12.4 KB to 7.0 KB. The optional-integrations table moved to `references/integrations.md`, read only before using one of those tools. The skill description is shorter too.
- Terse replies by default: short sentences, no preamble or restated plan. A small task's report is one to three lines. Code, paths, errors and evidence stay exact.
- `ult retro` runs only after long tasks (roughly 15+ turns) or a user correction, not after every task.
- README: the "unmeasured" line now gives the measured A/B numbers. 0.4.0 itself has not been re-measured.

### [0.3.1] - 2026-11-21

#### Fixed
- The chat-size guard no longer blocks small chats for being idle. The idle rule now applies only when the chat also re-reads more than 150k tokens (`ULTIMATUM_GUARD_IDLE_TOKENS`). A small chat paused for 14 hours was blocked before, although re-reading it once costs little.
- The guard could lock a chat: a blocked prompt is not added to the transcript, so the chat stayed "idle" and every retry was blocked again. It now blocks a chat once: sending a message again in that chat goes through, and the block message says so.

#### Changed
- UI route: more distinctive interfaces. Before choosing a direction, Ultimatum sketches three directions from different sources and drops any that fail a swap test (still fits with a competitor's name). The direction card gains a concept line that every choice must follow.
- New `ui.md` §3a, "Sources of distinctiveness": domain artifacts, real content as the graphic, typography as voice, a named color source built in OKLCH, composition with tension, a structural constraint, edge details and copy with a point of view.
- Cards are appended to `.ultimatum/ui-directions.md`. A new card must change the concept, display face and accent from the last two, unless the brief or existing identity pins them.
- The UI critique gate adds a distinctiveness check on screenshots (swap, memory, squint and card-drift tests) within the same 3-round limit.
- README: how to turn on marketplace auto-update (`"autoUpdate": true` in user settings).

### [0.3.0] - 2026-11-17

#### Changed
- **The main session only orchestrates.** New rule 7: it never edits project files; every edit, including a one-line fix, goes to `ultimatum:worker`, searches across many files go to `ultimatum:scout`, and anything beyond a small change gets `ultimatum:reviewer`. A small change uses one worker with a brief of a few lines. `orchestration.md`, `feature-planning.md`, `context-efficiency.md`, and the worker agent follow.
- **Never asks for a new chat or a manual `/compact`.** `ult context` HIGH now means "write the handoff, compaction is close", not "open a fresh chat". The README documents setting the auto-compact window to 200k with `CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000`.
- The coach no longer treats compactions or a high subagent share as waste in themselves.

#### Added
- `hooks/hooks.json`: one `SessionStart` hook (source `compact`) that prints `ult handoff show` after each compaction, so work resumes in the same chat. It is local and read-only, and sits beside the opt-in guard hooks from 0.2.7.
- Learn step in the default loop, run without being asked: `ult retro` checks the current chat and its subagents for repeated failures, re-reads, oversized outputs, search churn, and corrections. Project lessons become one-line rules in the project's `CLAUDE.md` under `## Learned`; lessons about Ultimatum are flagged as `Skill lesson:` in the report.
- Daily self-improvement run (`self-improvement.md` §2): a scheduled cloud session reads recent sessions, makes at most one tested change to the plugin, and opens a pull request. It never merges.
- Repository `CLAUDE.md` and `.claude/settings.json` (200k window) for sessions that work on Ultimatum itself.

Not measured: the cost and quality effect of always delegating. The last live A/B (`docs/TEST-REPORT.md`) predates this change.

### [0.2.9] - 2026-11-16

#### Changed
- Auto-compact is the main control for long chats; the guard is now a safety net. Guard defaults rise to 400k tokens per turn and 240 idle minutes, because a new chat starts at ~78k tokens per turn and must re-learn the work, so switching at 150k saved little.
- Rule 7: when `ult context` reports HIGH, write a handoff and ask the user to type `/compact` (same chat, same machine and files) instead of opening a fresh chat.

### [0.2.8] - 2026-11-16

#### Added
- Auto-resume after a guard block: a `SessionStart` hook (new chat or `/clear`, only with `ULTIMATUM_GUARD=1`) loads the guard's handoff into the next chat once, so the first message can be anything. Blocks older than 7 days are dropped.

### [0.2.7] - 2026-11-16

#### Added
- Opt-in chat-size guard (`hooks/hooks.json`, `scripts/ult-guard`): a `UserPromptSubmit` hook, off unless `ULTIMATUM_GUARD=1`. When a chat's last turn re-read over 150k tokens or it was idle over 60 minutes, it blocks the prompt with exit code 2 (zero model tokens), writes a handoff, and prints "Chat too large. Start a new chat and type: /ultimatum:work resume". Thresholds: `ULTIMATUM_GUARD_TOKENS`, `ULTIMATUM_GUARD_IDLE_MIN`.
- `ult handoff write --keep`: fills unset fields from the existing handoff, so an automatic write never erases the recorded goal, decisions, or next step.

### [0.2.6] - 2026-11-15

#### Added
- `ult context`: one line showing how many tokens each turn of the current chat re-reads (exit 3 when over 150k). In a 636-turn chat it reported ~566k tokens per turn, which is why usage drained in minutes.
- Rule 7: before substantial work in a long chat, check `ult context`; if HIGH, save a handoff and continue in a fresh chat (`/ultimatum:work resume`) instead of paying the huge re-read on every step.

### [0.2.5] - 2026-11-12

#### Changed
- Routing is explicitly zero-overhead: Ultimatum decides the route from the task itself, never runs tools or opens references just to decide, and loads an extra reference only when the task proves to need it.

### [0.2.4] - 2026-11-12

#### Added
- Rule 7, "Keep the conversation small": every turn re-reads the whole chat, so Ultimatum keeps bulk out of it (`ult run`, ranged reads, capped searches), batches tool calls, sends broad exploration to the scout subagent, keeps replies short, and suggests `/compact` or a fresh session from the handoff when the chat grows long.

### [0.2.3] - 2026-11-12

#### Added
- `ult scan --history`: gitleaks scans every commit, finding secrets that were committed and later deleted. Without gitleaks the report says "git history secrets: NOT checked" instead of implying a clean result. Full audits now use it.

#### Fixed
- `ult scan` no longer reports the same secret twice when gitleaks and the built-in patterns both catch it. The external lead is kept and notes the agreeing built-in rule.

### [0.2.2] - 2026-11-12

#### Added
- Compaction guidance: on longer tasks Ultimatum refreshes the handoff at milestones, and re-checks the handoff and evidence after a compaction (SKILL.md §3, `handoff.md`).
- README: how to cap context at about 200k tokens (`claude --autocompact 200000`, or `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=20` in cloud settings).

### [0.2.1] - 2026-11-12

#### Fixed
- `ult note` could give two notes the same reference when they were saved within the same millisecond, so the second overwrote the first in lookups. References now carry a random suffix. Found as an intermittent CI failure; this was also the undiagnosed one-off unit-test failure noted in the 0.1.0 test report.

### [0.2.0] - 2026-11-11

#### Added
- **Efficiency coach** (`improve` route): ask "efficiency review" or "daily coach". It reads this machine's Claude Code transcripts (including subagents), reports where tokens went by task category, and flags avoidable work: oversized tool output, repeated reads, repeated failing commands, search churn, user corrections, context compactions, heavy delegation. It then proposes one change, applied only with your approval.
- `ult usage report`: the local analyzer. It stores counts, categories, tool names and redacted paths/commands only, never prompt text or tool output. No network.
- `ult improve`: an experiment ledger (propose → apply with a baseline snapshot → measure after ≥3 sessions → keep or roll back). Verdicts weigh tokens per session against quality signals (corrections, tool errors).
- Reference `self-improvement.md`: the review procedure, allowed changes, privacy rules, and how to schedule it on your own machine.

### [0.1.1] - 2026-11-11

#### Fixed
- `ult search` crashed with a traceback on an invalid regex and on a `--path` outside the project when ripgrep was not installed. Found by the first CI run (CI runners have no ripgrep). Both now exit with a clear error, on both the ripgrep and pure-Python paths.

#### Added
- CI on every push: unit tests on Python 3.9, 3.11 and 3.13 (without ripgrep, so the fallback search path is covered) and `claude plugin validate --strict`.

### [0.1.0] - 2026-11-11 (preview)

First public preview. Tested on small fixture projects only; see `docs/TEST-REPORT.md` for exactly what was and was not tested.

#### Added
- One entry command, `/ultimatum:work <task>`, routing to workflows for small changes, discovery, features, large features with parallel workers, debugging, CI/PR feedback, UI with browser verification, data and infrastructure, bounded optimization, releases, handoff and resume.
- Three security workflows: a secure-implementation pass that runs automatically on sensitive changes, security review of a change, and full audit with a coverage ledger, a fresh verifier, and confirmed / needs-validation / rejected findings.
- Five subagents: `scout`, `worker`, `reviewer`, `security-hunter`, `security-verifier`.
- `ult` toolbelt (Python 3.9+ standard library, no network): `run`/`log` with raw-log recovery, `search`/`symbols`/`refs`, `map`, `note`/`find`/`get`, `handoff`, `scan` (wraps Semgrep, Gitleaks and OSV-Scanner when installed), `findings`, `doctor`.
- `ult-browser.mjs`: Playwright-based viewport, interaction, and accessibility checks, with axe-core when installed.
- `ULTIMATUM_STATE_DIR` to keep all state outside the repository for strict read-only work.

#### Known limitations
- Not yet tested on large real-world repositories or with models other than `sonnet`.
- Costs about 1.5–1.8x plain Claude Code per task in the recorded evals; no token-savings claim is made.
- CI/PR, production, data/infra, optimization and release workflows were tested for routing only.
