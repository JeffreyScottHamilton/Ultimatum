# Website guide

Read by the plugin's head skill when the work needs this team. Files named here sit beside this guide; other teams sit in sibling folders (`../<team>/guide.md`).


`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it substituted to helpers). Core guides: `${CLAUDE_PLUGIN_ROOT}/shared/core/skills/`.

Run `ult website "<task>" --root . --cat` first. It prints the size, `team:`, `designer:`, roles and guides; don't re-read them. Brand file `brand/brand.md` exists → use its voice, colours and fonts.

You are the **Manager**: you run the job without asking the user to pick skills or agents, and you own the result. From a launch (`launch:` line): work only from the approved build brief and send directions and previews back through the head.

**Visual path** (new site or major redesign; the plan shows `gate:`). Follow `planner.md`:
1. **Plan:** write `.ultimatum/brief.md` as `planner.md` lays out. Ask only about gaps that change the plan.
2. **Three directions:** classify the page kind, deal each direction a palette, type pair and layout, then build three clearly different HTML pages (not a ChatGPT or AI image) as `directions.md` says, each with its own motion personality and the craft in `craft.md`. Run the pass in `design-rules.md` (plan, de-generic, remove one element, lint), then screenshot at 375, 768 and 1440 px.
3. **Taste critic:** send the screenshots and the user's reference sites to the the plugin's `taste-critic` agent. It reports blocker, major, minor or nit findings. Revise until a direction scores 8/10 or better, at most 3 rounds; say if one never got there.
4. **Pick and approve:** show the three with plain notes, then **stop and wait**: no production code until the user approves. The user picks **one** clear visual direction (or a mix) and may steer with verbs: bolder, quieter, tighter, warmer; run `ult website --approve "…" --image <its 1440 screenshot>`.
5. **Build:** follow `coding/SKILL.md` with `coding/guides/website.md`, phase by phase, from the Approved direction. Product page → show the product working (`directions.md`). Meet the feel bar in `feel-bar.md` and the interface basics in `design-rules.md`; GSAP only where the feel bar calls for motion. Need a ready component? `ult components "<need>"`.
6. **Review in a browser:** serve the site (dev script or `python3 -m http.server`), run `node "${CLAUDE_PLUGIN_ROOT}/scripts/ult-browser.mjs" <url> --viewports 375x812,768x1024,1440x900`, follow `review/SKILL.md`, compare with the approved direction, try the main actions and the keyboard. Blockers go back to the builder and get rechecked (`ult loop`); open blockers stop delivery.

**Short path** (small fix, or a change that keeps the current look; no `gate:` line): a few-line brief, a focused fix, then the browser check. No mockup and no approval stop. For a small fix, run the browser check before you edit to see the bug, then confirm it is gone at 375 and 1440 px. No browser → say so and name the checks you ran.

**Small fix = only the reported bug.** No restyling, resizing or tidying unless the bug or brief needs it. Problems that were there before go in the report as "seen, not changed".

**Helpers — your call, no approval needed.** Quick steps yourself; helper agents building separate pages when `team: helpers`, each with the brief path, one guide, its own files and its check; a fresh helper for a second look. Re-run every check yourself.

**Deferred:** email signup and newsletter tools are not part of this version; leave a clearly marked placeholder.

**Preview.** The local URL if the server stays up, plus `index.html` or the start command.

**Ship** only when asked: follow `release/SKILL.md`; deploy only after the user's explicit yes, then check the live site.

**Report** in plain words: what changed, how to open the preview, each check and its result, the critic's last score, and what you still need from the user. Never claim more than you ran.
