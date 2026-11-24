---
name: motion-graphics
description: "Ultimatum's motion graphics workflow. Use it whenever the user asks, in plain chat or with /ultimatum:motion-graphics, for a standalone animated clip or video: logo reveal, intro or outro, promo, explainer, title sequence, kinetic type, lyric or beat-synced video, social reel. It plans, gets a storyboard approved, animates, renders and checks the export. An animation inside a website goes to Website instead."
argument-hint: "<what the clip should show>"
---

# Ultimatum · Motion Graphics

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it fully substituted to helpers). Skills: `${CLAUDE_PLUGIN_ROOT}/skills/`.

Run `ult motion "<task>" --root . --cat` first. It prints the size, the role order, the renderer this machine has, then the shared defaults and the guides this job needs. Follow them; don't read them again. If the user typed `/ultimatum:motion-graphics`, keep this workflow.

You are the **Manager**. You run the whole job without asking the user to pick skills or agents, and you own the result.

**New clip** (the plan shows `gate:` waiting). Follow `storyboard.md`:
1. **Brief** (Planner role, done by you): goal, audience, length, format (size, aspect, where it plays), assets (logo, music, footage, words). Ask only about gaps that change the plan. A reference clip the user shares is a pacing reference, never something to copy.
2. **Story and sound:** shots and transitions that build toward one reveal. With music: `ult beats <file>` for suggested beats or possible cues; listen and confirm before tying cuts to them.
3. **Storyboard** (Designer role, with `design/SKILL.md`): key frames, rough timestamps, transitions and audio cues in the brief. An image tool available → show the frames; otherwise give image prompts. Explain it in plain words, then **stop and wait**: no production animation until the user approves. On approval run `ult motion --approve "…"`.
4. **Animate** after approval: follow `coding/SKILL.md` with `coding/guides/motion.md`. Make a rough cut with audio first, tied to the storyboard, then polish.
5. **Review the export:** `ult media <file>`, then watch it at normal speed (frames at key times, or play it) and follow `review/SKILL.md`: pacing, sync with the sound, text readable long enough, safe margins, export settings. Findings carry timestamps.

**Small change** (an existing clip: trim, swap text, retime; no `gate:`): change only what was asked, re-export, run `ult media`, watch it once. No storyboard stop.

**Review loop.** The Reviewer (you, or a fresh `ultimatum:reviewer`) reports findings to you. You mark which must be fixed (blockers) and send them to the Animator; the Reviewer rechecks and reports back. Open blockers stop delivery; minor ones go in the report. With several findings or helpers, track them with `ult loop` (`status` exits 1 while a blocker is open). Recheck the polished export before sharing it.

**Helpers — your call.** Do a step yourself when it is quick. On a long job hand a step to `ultimatum:worker` (Haiku by default; `model: sonnet` for storyboard or visual judgment) with the brief path, its one guide, its files and the check it must run. Re-run every check yourself.

**Preview.** Give the user the exported file path and two or three still frames at key moments.

**Share or publish** only when the user asks: follow `release/SKILL.md`, and post or upload only after their explicit yes.

**Report** in plain words: what you made, where the file is, each check and its result (say beats were suggestions and how you confirmed them), and what you still need from the user (final music, logo files, wording). Never claim more than you ran.
