# Upstream design-skill survey (read-only)

Scope: `emil` (@64eb3de), `pbakaus_impeccable` (@b49177d), `nextlevelbuilder_ui-ux-pro-max-skill` (@a4fc248), `Leonxlnx_taste-skill` (@6c0b5c7). Method: file listings and byte counts, reads of LICENSE, README, SKILL.md frontmatter and reference headers, grep for network, subprocess and hook declarations. No upstream script was executed. Token figures are bytes/4. "Folder bytes" means every file in a skill folder except its SKILL.md. Other folders in the same scratchpad (JaimeJunr, anthropics, obra, remotion, vercel) were not inspected.

## 1. emil (emilkowalski/skills)

- **License:** MIT, root LICENSE, "Copyright (c) 2026 Emil Kowalski". No per-folder licences. Copies must keep the notice.
- **Skills (20):**

| Skill | Purpose (own words) | SKILL.md B | Folder B |
|---|---|---|---|
| emil-design-eng | polish and motion philosophy for components | 28,257 | 0 |
| animate / animate-expo | build one animation, web / React Native-Expo | 12,122 / 18,046 | 8,060 / 16,954 |
| animation-performance | keep motion on composited properties | 14,002 | 0 |
| animation-vocabulary | map vague motion wording to exact terms | 13,363 | 0 |
| apple-design | physical, interruptible motion principles | 22,852 | 0 |
| gestures | drag, swipe and sheet tracking | 8,823 | 0 |
| choreograph | sequencing a group of moving elements | 15,666 | 10,079 |
| find-animation-opportunities | read-only search for where motion helps | 9,884 | 0 |
| remove-animations | subtract motion that serves nothing | 11,555 | 0 |
| improve-animations | audit plus self-contained plan files | 8,666 | 10,977 |
| review-animations | strict review against a stated bar | 8,309 | 10,347 |
| break-ui | render worst-case data | 14,660 | 8,215 |
| mobile-native | web-as-app CSS and meta fixes | 16,904 | 0 |
| prototype | several variants behind a picker | 8,095 | 7,705 |
| learn-taste | turn design corrections into DESIGN.md rules | 9,251 | 0 |
| pick-ui-library | curated library lookup | 4,699 | 0 |
| ask-sonner | guide to the Sonner toast library | 7,326 | 4,663 |
| ask-emil | router across the other skills | 4,948 | 0 |
| write-swift | modern Swift guidance | 42,776 | 0 |

  Totals: SKILL.md 280,204 B; folder files 77,000 B. Two root cheat-sheets exist.
- **Unique:** a decision order for springs, gestures and interruption; `pick-ui-library`, a task-to-library table (no script). `learn-taste` is the only skill that writes project rules.
- **Scripts and data:** none. Install commands appear only in docs (`npx expo install`, `npx skills add`).
- **Startup cost:** 8,707 B of frontmatter, about 2,180 tokens.
- **Security:** no executable content, hooks or fetches.
- **Overlap:** motion (taste, impeccable `animate`); review (impeccable audit, taste gate).
- **Recommendation: adapt in own words.** Keep the animation decision checklist and a small library table of our own. Skip `write-swift` (out of scope), and skip the Sonner skill (single vendor).

## 2. impeccable (pbakaus/impeccable)

- **License:** Apache-2.0 at root. `NOTICE.md` lists three further terms: `skill/reference/ios.md` and `android.md` derive from ehmo's platform-design-skills (MIT); `extension/walks/consent-rules.js` is MPL-2.0; two bundled fonts are OFL-1.1. Apache-2.0 requires keeping the license and NOTICE and marking modified files. The built `.claude` SKILL.md has no license field; the source template names Apache 2.0.
- **Layout:** canonical source is `skill/` (SKILL.src.md 13,745 B, 45 references). Per-harness copies are generated. The `.claude/skills/impeccable` copy has SKILL.md 12,679 B and 46 references totalling 445,886 B.
- **Skill:** one skill with 24 commands (craft, init, audit, critique, live, polish, typeset and 17 more) plus references on hooks, foundations and component review.
- **Unique:** `audit` (a five-dimension diagnostic scoring 0 to 4, web only; `audit.native.md` covers iOS and Android); `critique` (two independent assessments, saved snapshot); `live` (browser-side variant picking, hot-swapped through the dev server's HMR); a detector engine with per-project ignore config; `DESIGN.md` and `PRODUCT.md` artifacts.
- **Scripts:** POSIX sh launcher `scripts/impeccable` (13.7 KB) and a Windows twin; `live-browser.js` (566 KB bundle); `data/font-index.json` (1.1 MB). The engine binary is not in the repo. `allowed-tools` also references `npx impeccable`.
- **Network:** when the engine is missing, the launcher downloads it from GitHub releases (base overridable by `IMPECCABLE_DOWNLOAD_BASE`). It checks SHA-256 against `engine-checksums.txt` (engine 0.1.27) and fails closed without a digest. That manifest ships in the same repo, so it proves a match with this repo's record, not the publisher's identity. `live-browser.js` has no non-localhost host literal; its `fetch(` sites were not reviewed individually.
- **Hooks and security:** `plugin/hooks/hooks.json` runs the launcher on SessionStart, PostToolUse and Stop (5 s timeout). A downloaded native binary therefore runs at session start. The live helper injects into local dev servers.
- **Overlap:** critique and audit overlap taste's gate and ui-ux-pro-max's UX rules.
- **Recommendation: optional adapter.** The user installs upstream. Do not vendor the engine or the live bundle. Our toolbelt is stdlib-only with no network, and this launcher downloads at run time. If needed, adapt only the five audit dimensions in own words.

## 3. ui-ux-pro-max (nextlevelbuilder)

- **License:** MIT at root (Copyright (c) 2024 Next Level Builder). `.claude/skills/ui-styling/LICENSE.txt` is Apache-2.0, a per-folder licence. Each font under `ui-styling/canvas-fonts/` ships an OFL text. `data-provenance.json` and `google-font-licenses.json` record data origins.
- **Skills (7):**

| Skill | SKILL.md B | Folder B (includes data, scripts, fonts) |
|---|---|---|
| ui-ux-pro-max | 18,640 | 3,699,455 |
| ui-styling | 10,945 | 5,697,577 (TTF fonts) |
| design | 14,850 | 288,469 |
| design-system | 7,458 | 177,874 |
| brand | 3,926 | 104,351 |
| banner-design | 7,071 | 4,993 |
| slides | 1,720 | 18,095 |

- **Startup cost:** 2,750 B of frontmatter, about 690 tokens; SKILL.md about 4,700 on invoke.
- **Unique:** searchable CSVs and a search script. Domains: 22 stack files (react, nextjs, vue, flutter, swiftui and others), styles (89 rows; SKILL.md claims 80 styles, 51 active, not reconciled), colors (194), typography (74 pairings), ux-guidelines (141), icons (105), motion (17 GSAP presets), charts (25), landing (34), products (194), react-performance (44), google-fonts (1,934, 747 KB).
- **Search engine:** `scripts/search.py` calls `core.py`, a BM25 engine over CSVs, standard library only. `design_system.py` (82 KB) emits DTCG or CSS tokens. `preview.py` writes HTML that loads Google Fonts in the browser.
- **Other scripts:** `validate_data.py` is stdlib-only. Repo-level `scripts/refresh-google-fonts.py` and `refresh-icon-catalog.py` are maintainer tools outside the skill folder; they contact Google Fonts and GitHub. Not read in full.
- **Design skill:** logo, icon and CIP generators call Gemini (`GEMINI_API_KEY`), Atlas Cloud and MUAPI. `fetch-background.py` downloads Pexels images. `shadcn_add.py` runs `npx shadcn@<version> add`.
- **Security:** API keys read from environment; network downloads; a run-time `npx` fetch. Shipped test artifacts (`scripts/.coverage`, 53 KB; `coverage-ui.json`, 35 KB) sit in the skill folder.
- **Overlap:** motion (GSAP) with emil; UX rules with impeccable audit; colors and typography with taste's `palettes.json` and `type.json`; stacks with emil's library table.
- **Recommendation: optional adapter for search, adapt the idea for our own use.** The data is 3.7 MB and the search needs no network, but vendoring it bloats the plugin. If wanted, write a small BM25 over our own short table. Skip the logo, icon and CIP generators (API keys, out of scope), and skip the canvas fonts (large, OFL obligations).

## 4. taste (Leonxlnx/taste-skill)

- **License:** MIT at root (Copyright (c) 2026 Leonxlnx). Third-party terms apply to content: `assets/photos/photos.json` holds 413 records: Unsplash 274, CC0 53, and CC BY-family or Public Domain Mark for the rest, each with its own attribution or ShareAlike terms. `icons.mjs` fetches icon sets under CC0 (logos, simple-icons), MIT (vscode-icons) and ISC (Lucide).
- **Skill:** one folder `skills/taste-skill`, but the frontmatter `name` is `design-taste-frontend`. The description says 2.5.1, the heading says 2.5.
- **Sizes:** SKILL.md 30,970 B. Reference folder: 22 files, 407,143 B (largest `sections-library.md` 66 KB, `sections.md` 54 KB, `photos.md` 28 KB). Assets 34.5 MB across 932 files. Scripts: 12 `.mjs` and HTML templates, 1.56 MB, of which `consistency.mjs` is 1.0 MB. `library/`: `palettes.json` 43 KB, `type.json` 23 KB.
- **Startup cost:** 948 B of frontmatter, about 240 tokens; SKILL.md about 7,700 on invoke.
- **Unique:** nine house rules (no caption under visuals; visuals render at four widths; one section per screen; equal content edges; real photos and icons; shader scenes only for technical subjects; no real addresses or phone numbers) and a "never" list (no violet in the page's own design; no scroll fade-ins; no stock photos presented as the client's). A business-kind page plan. A finish gate (`gate.mjs`) that blocks a build while fixable FAILs remain, plus a headless-Chrome checker (`consistency.mjs`) and copy linter.
- **Dependencies:** Node 22+, Chrome or Chromium, optional ffmpeg. No npm packages.
- **Network and processes:** `photos.mjs` calls the Wikimedia Commons API and downloads from upload.wikimedia.org and picsum.photos. `icons.mjs` fetches from cdn.jsdelivr.net at pinned versions. `consistency.mjs` fetches URLs it is given. Browser helpers spawn Chrome with a remote-debugging port and a local HTTP server on 127.0.0.1.
- **Hooks:** the SKILL.md frontmatter declares a `Stop` hook running `gate.mjs` with a 600 s timeout. `install.sh` symlinks the skill into the user's Claude Code or Codex skills directory.
- **Overlap:** motion with emil and impeccable `animate`; anti-slop rules with impeccable critique and emil review; palettes and type with ui-ux-pro-max data.
- **Recommendation: adapt in own words** the nine rules and "never" list as our own checklist. Skip the scripts (Stop hook, build-time fetches, Chrome; these conflict with our stdlib-only, no-network rule) and the photo and icon assets (mixed licences).

## 5. Cross-repo summary

- **Startup (frontmatter only):** emil about 2,180 tokens; ui-ux-pro-max about 690; taste about 240; impeccable about 50.
- **Overlaps:** motion (emil, taste, impeccable, ui-ux GSAP); critique and anti-generic rules (impeccable, taste, emil review); palettes and type (ui-ux, taste); library choice (emil, ui-ux stacks).
- **Recommendations:**

| Repo | Recommendation | Reason |
|---|---|---|
| emil | adapt in own words | MIT, no code, short checklists fit |
| impeccable | optional adapter | Apache-2.0, but runtime binary download conflicts with no-network rule |
| ui-ux-pro-max | optional adapter; idea only for search | MIT, large data; a small own BM25 covers the need |
| taste | adapt rules in own words; skip scripts and assets | network fetches, Stop hook, mixed photo licences |

- **Licence obligations:** MIT: keep the notice. Apache-2.0: keep licence and NOTICE, mark changes. OFL-1.1: keep font licence with the font. Per-record CC BY and BY-SA photos: attribution and ShareAlike.
