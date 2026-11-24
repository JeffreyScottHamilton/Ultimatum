---
name: website
description: "Ultimatum's website workflow. Use it whenever the user asks, in plain chat or with /ultimatum:website, to build, redesign or fix a website, landing page, homepage, portfolio, marketing page or a part of one (menu, header, layout, mobile view), e.g. \"Build me a website for my coffee shop\". It plans, gets a mockup approved for new looks, builds and checks the site in a real browser."
argument-hint: "<what the site needs>"
---

# Ultimatum · Website

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it fully substituted to helpers). Skills: `${CLAUDE_PLUGIN_ROOT}/skills/`.

Run `ult website "<task>" --root . --cat` first. It prints the size, `team:`, `designer:`, the role order, then the shared defaults and the guides this job needs. Follow them; don't read them again, and load nothing else unless the job grows. If the user typed `/ultimatum:website`, keep this workflow.

You are the **Manager**. You run the whole job without asking the user to pick skills, agents or handoffs, and you own the result. There are two paths; `ult website` tells you which.

**Visual path** (new site or major redesign: the plan shows `gate:`). Follow `planner.md`:
1. **Plan** (Planner role, done by you): write `.ultimatum/brief.md` as `planner.md` lays out (audience, first action, pages, mobile, assumptions, placeholders, phases with checks). Ask only about gaps that would change the plan.
2. **Design** (when `designer: yes`): follow `design/SKILL.md` and put **one** clear visual direction in the same brief.
3. **Mockup and approval:** turn the brief into a ready-to-paste ChatGPT mockup prompt (a grayscale wireframe first when the layout itself needs review). An image tool available → show one mockup; otherwise give the prompt and ask the user to bring the image back. Explain the idea in plain words, then **stop and wait**: no production code until the user approves the look. On approval run `ult website --approve "…"` so the brief records it.
4. **Build** after approval: follow `coding/SKILL.md` with `coding/guides/website.md`, phase by phase, from the brief's Approved direction. Reuse the project's pieces; no stack → plain HTML, CSS and a little JS, no build step.
5. **Review in a browser:** serve the site (the project's dev script, or `python3 -m http.server`), run `node "${CLAUDE_PLUGIN_ROOT}/scripts/ult-browser.mjs" <url> --viewports 375x812,1280x800`, and follow `review/SKILL.md`: compare with the approved direction, try the main actions, use the keyboard. Fix and recheck until the checks pass or a blocker remains.

**Short path** (small fix, or a change that keeps the current look; no `gate:` line): a few-line brief (the bug or change and its browser check), then a focused fix, then the browser check. No mockup and no approval stop. For a small fix, run the browser check once before you edit to reproduce the bug and note what was already there, then confirm the bug is gone at 375 and 1280 px. No browser here → say so and name the checks you did instead.

**Small fix = only the reported bug.** Change what the bug needs and nothing else: no restyling, resizing (tap targets included) or tidying unless that is the bug or the brief or project already requires it. Findings that were there before your edit go in the report as "seen, not changed"; the recheck passes when the bug is gone and nothing new appeared.

**Helpers — your call, no approval needed.** Do a step yourself when it is quick. Hand it to a helper when that helps: a separate Planner or Designer only on a large job, a fresh `ultimatum:reviewer` for step 4 on a new site, `ultimatum:worker` builders for separate pages or areas when `team: helpers` (Haiku by default; `model: sonnet` where judgment matters, such as design). Each helper gets the brief path, the one guide it needs, its own files and the check it must run. Never give two builders the same file. Re-run every check yourself.

**Preview.** Leave the user a way to see it: the local URL if the server can stay up, plus the file to open (`index.html`) or the start command.

**Ship** only when the user asks: follow `release/SKILL.md`. Deploy or publish only after the user's explicit yes, then check the live site.

**Report** in plain words: what you built or changed, how to open the preview, each check and whether it passed, and exactly what you still need from the user (real photos, text, domain, hosting login). Never claim more than you ran.
