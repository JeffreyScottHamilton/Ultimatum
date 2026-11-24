# Upstream engineering skills: read-only survey

Scope: four clones under `/tmp/claude-0/-home-user-Ultimatum/918c00ce-8a04-5813-ba24-0f3d322bb563/scratchpad/up/`. Nothing was executed from them. Byte counts are from `wc -c`. Token estimates are bytes/4. Sizes of files inside reference folders are totals.

## 1. obra_superpowers (@22f0b46, plugin version 7.0.2)

**License:** MIT. Root `LICENSE`: "MIT License / Copyright (c) 2025 Jesse Vincent". `package.json` has no license field. Redistribution needs the notice kept. Our rules still require original wording.

**Skills (14 SKILL.md; name: SKILL.md bytes; references):**
- brainstorming 15190 B; executing-plans 18364 B; subagent-driven-development 19740 B (refs 11015 B); writing-plans 10335 B.
- test-driven-development 9578 B; systematic-debugging 9530 B; dispatching-parallel-agents 6078 B; using-git-worktrees 6813 B; finishing-a-development-branch 7781 B.
- requesting-code-review 2974 B; receiving-code-review 6203 B; verification-before-completion 3646 B.
- using-superpowers 3192 B (meta: invoke skills first; refs 17438 B); writing-skills 16738 B (refs 87503 B); diagnosing-superpowers 6941 B (refs 6728 B).

**Unique capabilities:** the most complete workflow chain: brainstorm, plan, execute or subagent-run, review, finish. Subagent prompts are separate files (`implementer-prompt.md`, `task-reviewer-prompt.md`, `re-review-prompt.md`). The `subagent-driven-development/scripts/` folder holds `task-brief`, `sdd-workspace`, `review-package`, `sdd-repo`, which were not read in full.

**Hooks and startup injection:** one `SessionStart` hook, matcher `startup|clear|compact`, `async: false`. It runs `hooks/session-start` through `run-hook.cmd`. The script reads `skills/using-superpowers/SKILL.md` and emits it as JSON additional context. Cost: about 3.2 KB plus a small wrapper, about 0.85k tokens on every startup, clear and compaction.

**Scripts and network:** `brainstorming/scripts/server.cjs` binds `127.0.0.1` by default (`BRAINSTORM_HOST`), uses a token in the URL (`/?key=`), and its HTML references `https://primeradiant.com/brand/...png`. Other scripts: `lint-shell.sh`, `bump-version.sh`, `package-codex-plugin.sh`, `sync-to-codex-plugin.sh`. Also `.opencode`, `.pi`, `.hermes-plugin` platform adapters. No dependencies at root; `tests/brainstorm-server/package.json` exists.

**Security risks:** the visual companion runs a local HTTP server and writes HTML the agent controls. Its token scheme and the non-loopback option (`BRAINSTORM_HOST`) need care. Startup hook injection is persistent context.

**Overlap:** `using-superpowers` is a router of the same kind as the Ultimatum route table. brainstorming overlaps the `feature` route, test-driven-development overlaps `tdd.md`, systematic-debugging overlaps `debugging.md`, verification-before-completion overlaps the Verify step and §5. subagent-driven-development overlaps `orchestration.md`.

**Recommendation:** **adapt in own words**, selectively. Candidates: the verification gate wording, the debugging "find the cause before fixing" discipline, and the plan-task-review cycle as ideas for `orchestration.md`. **Skip** the SessionStart injection (token cost on every session) and the brainstorm server (network and HTML surface).

## 2. vercel-labs_agent-skills (@5a37a63)

**License:** no LICENSE file. `README.md` section "## License" says only: "MIT". `package.json` has no license field. Treat the MIT statement as the only evidence; it is not a license file.

**Skills (14 directories with SKILL.md):**
- react-best-practices (name `vercel-react-best-practices`), 7251 B. A router over **71 rule files** in `rules/` (110590 B total, excluding `_template.md`). The SKILL.md lists 70 `###` headings. Rule ids like `async-parallel`, `rerender-functional-setstate`, `server-cache-react`.
- vercel-optimize, 17311 B. Deployed-project cost and performance audit. References 198356 B. Has about 20 scanner modules in `lib/scanners/`, sanitizers in `lib/sanitizers/`, and orchestration scripts (`scan-codebase.mjs`, `collect-signals.mjs`, `verify-and-regen.mjs`, `render-report.mjs`, and others). The script `verify-and-regen.mjs` explicitly does not spawn sub-agents; the orchestrator does.
- react-view-transitions, 14502 B. References 45198 B.
- vercel-cli-with-tokens, 10476 B. Token-based CLI deployment.
- deploy-to-vercel, 9721 B.
- react-native-skills, 4439 B.
- composition-patterns, 2886 B. Its frontmatter has no description line (`grep` found none).
- web-design-guidelines, 2077 B. References 8055 B. Interface-guidelines review.
- writing-guidelines, 1233 B.

**Unique capabilities:** the only rule dataset here (71 React and Next.js performance rules with ids and per-rule files). vercel-optimize is a multi-stage evidence pipeline with citation checks and a docs library (`references/docs-library.json`).

**Hooks and startup injection:** none found (no `hooks/` folder). Injection cost is 0 at startup. Loading react-best-practices costs about 7.3 KB SKILL.md plus rule files on demand.

**Scripts and network:** vercel-optimize scripts are Node `.mjs`, with no `package.json` dependencies at skill level. Grep matched `fetch` or `exec`/`spawn` in `check-citations.mjs`, `collect-sub-agent-outputs.mjs`, and several scanners. I did not audit each match. `vercel-cli-with-tokens` and `deploy-to-vercel` direct the agent to Vercel CLI and token handling.

**Security risks:** token handling in `vercel-cli-with-tokens` (where to find and store a token) is sensitive. vercel-optimize reads production-like project data and runs scanners on user code. Not verified: whether any scanner sends repo contents over the network.

**Overlap:** react-best-practices and react-view-transitions overlap `react.md` and `ui.md`. The rule-file layout is the same shape as Ultimatum's `references/` pattern. web-design-guidelines overlaps `ui.md` review. Deploy and token skills overlap no Ultimatum route.

**Recommendation:** **adapt in own words** a short distilled checklist of React performance points for `react.md` (for example: avoid unnecessary re-render sources, hoist static work, use functional state updates). Do not copy the rule text. **Optional adapter** for vercel-optimize only if the user later wants a Vercel cost audit route. **Skip** the token-based deploy skill (credential handling) and the 198 KB reference set (size).

## 3. remotion-dev_skills (@89c8afa, package `@remotion/skills` 4.0.546)

**License:** **no license found.** No LICENSE file at any level. `package.json` is `"private": true` with no license field. `README.md` has no license statement. The `remotion-license` skill only points to external pages (remotion.dev docs, terms). Not redistributable. Do not copy or adapt wording.

**Skills (13 SKILL.md):**
- remotion-best-practices, 4184 B. Router for all Remotion skills.
- remotion-markup, 13762 B. Content, animation and effects. Nested `remotion-maps` techniques (cesium, mapbox, maplibre, maptiler).
- remotion-interactivity, 14539 B. Structuring markup so layers are editable in Studio.
- remotion-render, 3005 B. Export video, still or OpenTimelineIO.
- remotion-create, 3073 B. Create a new video.
- remotion-upgrade, 1947 B. Upgrade Remotion packages.
- remotion-docs, 1374 B. Search docs.
- remotion-captions, 1172 B. Transcribe and animate captions.
- remotion-studio, 1537 B.
- remotion-saas, 1053 B.
- remotion-maps, 1030 B.
- remotion-multimedia, 705 B. Mediabunny.
- remotion-license, 498 B. Links only.

Map technique references total about 16 KB (cesium) plus smaller files; about 244 files in `skills/` in total.

**Unique capabilities:** video composition with Remotion (React-based). Nothing in the Ultimatum scope covers video.

**Hooks and startup injection:** none. Scripts are only the repo-maintenance files under `scripts/` (`sync-agent-skills.ts`, `validate-links.ts`, and others), not part of the skills. Network: examples point to `http://localhost:3000`; no network calls found in skill text.

**Security risks:** low for reading. The maps techniques reference third-party map tokens (MapTiler, Mapbox); users would need their own keys.

**Overlap:** no overlap with Ultimatum's routes except the router pattern in remotion-best-practices.

**Recommendation:** **skip.** Reason: no license, so no reuse, even in own words, of its specific guidance. If video work becomes a need, write a fresh note from Remotion's public docs with a citation.

## 4. JaimeJunr_claude-code-frontend-skills (@7177def)

**License:** root `LICENSE` is MIT (copyright 2026 Jaime Basso). Glue plugin and scripts are MIT. Bundled plugins keep upstream licenses (recorded in `THIRD_PARTY_NOTICES.md` and `UPSTREAM.lock`):
- Apache-2.0: frontend-design, ux-research, design-handoff, impeccable, hyperframes.
- MIT: ui-ux-pro-max, taste, taste-classics, hallmark, taste-imagegen, design-mobile-apps, emil-design-eng, emil-native.
Each has a LICENSE file in its plugin folder. Apache-2.0 requires notices and change marks; MIT requires the copyright notice.

**Size:** 2508 files total. Much of the bulk is vendored upstream repos under `Leonxlnx_taste-skill/`, `anthropics_skills/`, `emil/`, `pbakaus_impeccable/`, `nextlevelbuilder_ui-ux-pro-max-skill/` (these sit beside the plugin folder). SKILL.md files under `plugins/` and `.claude/`: 45. Largest: write-swift 42776 B, image-to-code 36442 B, imagegen-frontend-mobile 40326 B, imagegen-frontend-web 36854 B, emil-design-eng 28257 B, frontend-stack 22594 B. `references/` folders total 300 files, about 7.3 MB (mostly taste assets).

**Routing mechanism (specific):** `plugins/frontend-stack/skills/frontend-stack/SKILL.md` is a router with eight sections. Steps:
1. Read the project first (package.json, components.json, Tailwind, DESIGN.md).
2. Classify the request on three axes: job (build, change, review, craft, assets), surface (marketing, product, component, mobile web, native), stack signals.
3. Phase plan: Diagnose, Direction, Build, Review. A table in §4 maps each task type to one **lead** skill and up to **two support** skills. Examples: product dashboards lead with `frontend-design`; landing pages lead with `taste`; "looks generic" routes to an identity flow first.
4. Vague complaints ("ugly") trigger a clarifying question before any skill loads.
5. Precedence ladder (§6): user request and brand, then the project's existing system, then accessibility and correctness, then the lead's scope rules, then domain owner, then the lead's taste defaults.
6. Load budget (§7): base skill plus one lead plus at most two supporting skills per phase.
7. Finish format (§8).
Seven reference files (about 88 KB) hold the detailed flows; `conflicts.md` (15.5 KB) holds cross-pack rulings. The routing is by instruction text in the model's context. There is no code that selects skills.

**Hooks and startup injection:** `plugins/impeccable/hooks/hooks.json` has a `SessionStart` hook (timeout 5) and a `PostToolUse` hook on `Edit|Write` (timeout 30, status "Design deep pass"). Both run `skills/impeccable/scripts/impeccable hook` (or a `.cmd` on Windows) if the file exists. The directory has a prebuilt `impeccable` script (13724 B), `impeccable.cmd` (15459 B), `engine-checksums.txt`, and `live-browser-dom.js`. Per-session token cost: not measured (hook output not run).

**Agents:** `design-director.md` (4379 B) with tools `Read, Glob, Grep, Bash, Skill, WebFetch`. `ui-reviewer.md` (5311 B) with tools `Read, Glob, Grep, Bash, Skill`.

**Scripts and network:**
- `ui-ux-pro-max/.../scripts/` contains Python 3 files (`core.py`, `search.py`, `design_system.py`, `preview.py`, `validate_data.py`, `generate.py`) and CSV data (`styles.csv`, `colors.csv`, `industries.csv`).
- `design-system/scripts/fetch-background.py` fetches hard-coded `images.pexels.com` URLs ("uses web scraping (no API key required)").
- `taste/.../assets/**/*.js` and `.mjs` files (about 100 files, for example `effect.js`, `component.js`, `shoot.mjs`). `shoot.mjs` is a Node 22+ tool for screenshots; it drives a browser. Not run.
- `scripts/sync.py` (Python) pulls upstream repos by `https://github.com/{repo}.git` and regenerates the marketplace and notices. `scripts/check.sh` is the local gate; `.githooks/pre-push` runs it.

**Security risks:**
- Shipped prebuilt executable (`impeccable`) invoked from hooks on every Edit or Write.
- Scraping of external image sites from a design skill script.
- `design-director` agent has `WebFetch`.
- Vendored copies of six upstream repos make license drift likely (the repo itself has `UPSTREAM.lock`).
- Not verified: contents of `impeccable` and `engine-checksums.txt`.

**Overlap:** frontend-stack is the same shape as Ultimatum's router with references, applied to frontend only. Its precedence ladder overlaps Ultimatum's Rule 4 ("untrusted text is data") and §3 ("reuse first"). Frontend leads overlap Ultimatum `ui.md`. Impeccable's `critique`, `audit`, `harden` overlap `ui.md` review and `security/` only loosely. Ultimatum already has `ui.md` and `browser-verification.md`.

**Recommendation:**
- **Adapt in own words:** the phased lead-plus-two-supports load budget and the precedence ladder, as a short section for `ui.md`. Keep it under a few hundred words.
- **Optional adapter:** nothing vendored. If the user wants Impeccable's audit later, reference its command names only, and only if installed by the user.
- **Skip:** copying any bundled skill or reference (7.3 MB, mixed licenses, and our rule forbids copying upstream text). Skip the impeccable hook (executes a shipped binary on every edit) and the pexels fetch script.

## 5. Cross-repo overlap

- Workflow chain (brainstorm, plan, TDD, debug, review): superpowers overlaps Ultimatum's route table, `feature-planning.md`, `tdd.md`, `debugging.md`, `orchestration.md`. Adapt ideas only.
- Verification before claims: superpowers and Ultimatum §1 and §5 already agree.
- React rules: Vercel overlaps `react.md`; adapt a short checklist.
- Frontend routing and budget: JaimeJunr overlaps `ui.md`; adapt the budget and precedence idea.
- Video: only remotion; skip (no license).
- Routers: superpowers, Vercel rules, and JaimeJunr all use the "router plus references" shape. The router parts are worth reusing in own words. The reference bodies (superpowers 87 KB, vercel-optimize 198 KB, JaimeJunr 7.3 MB) should not be imported.

Startup token cost: superpowers about 0.85k tokens per startup, clear and compact (measured from bytes). Others: none found at startup. Impeccable hook cost unmeasured.

## 6. Limits of this survey

- Not read in full: superpowers subagent scripts, vercel-optimize scanners, JaimeJunr reference files and taste assets, the Impeccable binary.
- Not run: any script from these repos, the Impeccable hook, the visual companion server, and the `shoot.mjs` tool.
- Not verified: Vercel's MIT claim against a LICENSE file (none exists); whether any Vercel scanner sends data over the network.
