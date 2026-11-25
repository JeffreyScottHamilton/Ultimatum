# Motion graphics guide

Read by the plugin's head skill when the work needs this team. Files named here sit beside this guide; other teams sit in sibling folders (`../<team>/guide.md`).


`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it substituted to helpers). Core guides: `${CLAUDE_PLUGIN_ROOT}/shared/core/skills/` (design, coding, review, release).

**Feeling or people story, not a feature or number?** Hand it to the Brand Film guide (`../brand-film/guide.md`) instead.

Run `ult motion "<task>" --root . --cat` first: size, roles, renderer, `gate:` and the guides to follow. Don't read them again. You are the **Manager** and own the result.

**New clip** (`gate:` waiting), audio first:
1. **Brief:** goal, audience, length, format, assets. Ask only about gaps that change the plan. A reference clip is for pacing, never to copy.
2. **Storyboard** (`storyboard.md`, design guide): key frames, rough timings, transitions, the words. Explain in plain words, then **stop and wait**: no production animation until the user approves. On approval: `ult motion --approve "…"`.
3. **Audio sheet** (`audio-sheet.md`): voiceover text with exact ElevenLabs settings, and a Suno prompt in the locked style from `brand/sound.md` (written on the first video, reused later). The user pastes the files back, or, with the ElevenLabs connector, ask before spending credits and generate. Say once that Suno's free plan is non-commercial only.
4. **Timings:** the voiceover is the skeleton. Get word times (ElevenLabs timestamps, a timestamped transcript, or listening), write a frame-timing document per scene, and confirm music beats (`ult beats <file>` gives suggested beats or possible cues; listen first).
5. **Animate** to those timings (coding guide + `coding/guides/motion.md`): rough cut with the audio, then polish.
6. **Sound effects last** (`sfx-sourcing.md`): a CC0 pack first, other sources only for gaps, each file's licence logged in `brand/sound-credits.md`.
7. **Check:** `ult media <file>`; loudness and peak per `audio-sheet.md`, music ducked under voice, audio length matches video. Review stills at each key frame, then watch at normal speed (review guide): pacing, sync, text readable, safe margins. Findings carry timestamps.

**Kind** (`kind:` line). *First launch video:* /brag ideas are optional inside step 2, never a reason to skip approval. *Later video:* reuse `.ultimatum/motion/style.md` and `brand/sound.md`, with a new storyboard that still needs approval.

**Deliver.** On the user's yes to the finished video: `ult gate approve video "<their words>" --file <export>`, then `ult motion --deliver <export>` (exits 1 while a blocker is open or the export has warnings), which records `## Delivered video` in the brief for Marketing. After the first launch video: `ult motion --save-style "<pacing, cuts, text movement, sound cues, ending>" --video <export>`.

**Small change** (trim, swap text, retime; no `gate:`): change only what was asked, re-export, run `ult media` and the audio check, watch once. No storyboard stop.

**Review loop.** The Reviewer (you, or a fresh helper agent) reports findings; you mark blockers and send them to the Animator; the Reviewer rechecks. Open blockers stop delivery. With several findings use `ult loop` (`status` exits 1 while a blocker is open).

**Helpers.** On a long job hand one step to a helper agent with the brief path, its guide, its files and its check. Re-run every check yourself.

**Rules.** Packs and downloaded audio stay local, out of Git. Skip any file marked non-commercial (NC). Credit attribution files. Publish only through the release guide and the user's explicit yes.

**Preview and report:** the export path, two or three stills, each check and its result (beats were suggestions; say how you confirmed them), credits used, and what you still need from the user. Never claim more than you ran.
