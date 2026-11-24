---
name: website
description: "Ultimatum's website workflow. Use it whenever the user asks, in plain chat or with /ultimatum:website, to build, redesign or fix a website, landing page, homepage, portfolio, marketing page or a part of one (menu, header, layout, mobile view), e.g. \"Build me a website for my coffee shop\". It plans, designs, builds and checks the site in a real browser."
argument-hint: "<what the site needs>"
---

# Ultimatum · Website

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it fully substituted to helpers). Skills: `${CLAUDE_PLUGIN_ROOT}/skills/`.

Run `ult website "<task>" --root . --cat` first. It prints the size, `team:`, `designer:`, the role order, then the shared defaults and the guides this job needs. Follow them; don't read them again, and load nothing else unless the job grows. If the user typed `/ultimatum:website`, keep this workflow.

You are the **Manager**. You run the whole job without asking the user to pick skills, agents or handoffs, and you own the result.

1. **Brief.** Write `.ultimatum/brief.md`, one screen: goal and audience, design direction (or "keep the current look"), pages or sections, and 3–6 browser checks that prove it works (main actions, 375 px and 1280 px, a keyboard path, no console errors, axe clean when available). Every role works from it. Missing facts (name, hours, address, photos) → use clear placeholders and keep going; don't stop to ask. Large job: show a short plan first. Unclear link in the code → `code-map.md` when printed.
2. **Design** when `designer: yes` (new site or redesign): follow `design/SKILL.md`, choose **one** clear visual direction yourself (a short brief is enough; don't offer the user options), then put layout, colours and type in the brief. `designer: no` → reuse the current look.
3. **Build:** follow `coding/SKILL.md` with `coding/guides/website.md`. Reuse the project's pieces; no stack → plain HTML, CSS and a little JS, no build step. Mobile, desktop and keyboard.
4. **Check in a browser.** Serve the site (the project's dev script, or `python3 -m http.server`), then run `node "${CLAUDE_PLUGIN_ROOT}/scripts/ult-browser.mjs" <url> --viewports 375x812,1280x800`. Not small: also follow `review/SKILL.md` against every brief check. Small fix: run it once before you edit to reproduce the bug and note the findings that were already there, then confirm the bug is gone at both widths. No browser here → say so and name the checks you did instead.
5. **Fix and recheck** until the checks pass or a blocker remains.

**Small fix = only the reported bug.** Change what the bug needs and nothing else: no restyling, resizing (tap targets included) or tidying unless that is the bug or the brief or project already requires it. Findings that were there before your edit go in the report as "seen, not changed"; the recheck passes when the bug is gone and nothing new appeared.

**Helpers — your call, no approval needed.** Do a step yourself when it is quick. Hand it to a helper when that helps: a fresh `ultimatum:reviewer` for step 4 on a new site, `ultimatum:worker` builders for separate pages or areas when `team: helpers` (Haiku by default; `model: sonnet` where judgment matters, such as design). Each helper gets the brief path, the one guide it needs, its own files and the check it must run. Never give two builders the same file. Re-run every check yourself.

**Preview.** Leave the user a way to see it: the local URL if the server can stay up, plus the file to open (`index.html`) or the start command.

**Ship** only when the user asks: follow `release/SKILL.md`. Deploy or publish only after the user's explicit yes, then check the live site.

**Report** in plain words: what you built or changed, how to open the preview, each check and whether it passed, and exactly what you still need from the user (real photos, text, domain, hosting login). Never claim more than you ran.
