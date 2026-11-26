# Changelog

All notable changes to Ultimatum are listed here. Versions follow [Semantic Versioning](https://semver.org/); the version in `plugins/ultimatum/.claude-plugin/plugin.json` is the source of truth and must be bumped for installs to update.

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
