---
name: website
description: "Ultimatum's website workflow: build, redesign or fix a website, landing page, homepage, portfolio or marketing page, from one short brief through optional design, build and a real browser check. Use when the user runs /ultimatum:website <task> or clearly asks for website work."
argument-hint: "<what the site needs>"
---

# Ultimatum · Website

Task: $ARGUMENTS

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it fully substituted to helpers). Skills: `${CLAUDE_PLUGIN_ROOT}/skills/`.

Run `ult website "<task>" --root . --cat` first. It prints the size, `team:`, `designer:`, the role order, and then the shared defaults and the guides this job needs. Follow them; don't read them again, and load nothing else unless the job grows. The user chose this workflow if they typed `/ultimatum:website`: keep it.

You are the **Manager** and own the final result.

1. **Brief.** Write `.ultimatum/brief.md`, one screen: goal and audience, design direction (or "keep the current look"), pages or sections, and 3–6 browser checks that prove it works (main actions, 375 px and 1280 px, a keyboard path, no console errors, axe clean when available). Every role works from this one brief. Bigger job: show the user a short plan first. If an important link in the code is unclear, follow `code-map.md` when printed.
2. **Design**, only when `designer: yes`: follow `design/SKILL.md` and write the layout, colours and type into the brief. `designer: no` → go straight to Build.
3. **Build:** follow `coding/SKILL.md` with `coding/guides/website.md`. Reuse the project's own pieces first; mobile, desktop and keyboard.
4. **Review:** follow `review/SKILL.md` against the brief's checks. Open the real page, try the main actions, and report each problem with the steps to see it.
5. **Fix and recheck:** fix it yourself or send it back to the Builder, re-run the failed checks, then report.

**Team.** `team: solo`: play every role yourself in this chat; no helpers. `team: helpers`: brief one `ultimatum:worker` per page or area, each with its own files (Haiku by default; pass `model: sonnet` where judgment matters, such as design). Each brief gets the brief path, the one guide it needs, its owned files and the check it must run. `ultimatum:reviewer` may run step 4 fresh. Never give two builders the same file. You re-run every check yourself.

**Ship** only when asked: follow `release/SKILL.md`. Deploy or publish only after the user's explicit yes, then check the live site.

**Report** in plain words: what changed, what passed (with the check), and what is still open. Never claim more than you ran.
