# Creator Cut guide

Read by the plugin's head skill when the work needs this team. Files named here sit beside this guide; other teams sit in sibling folders (`../<team>/guide.md`).

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"`. Creator Cut turns a person talking to camera into short vertical videos: one point, a hook in the first 2 seconds, tight jump cuts, captions, a next step. Files live in `cut/` (plans, transcripts, notes) and `media/` (git-ignored video).

**Is it this team?** Someone talking to camera (founder, creator, coach, expert), a podcast or a live stream to clip, or a series of tips → here. A feeling carried by people with a story arc → `../brand-film/guide.md`. A feature, number or diagram with no presenter → `../motion-graphics/guide.md`. Titles, a lower third or an end card on top of a creator cut stay a creator job; make those layers as in Motion Graphics.

**Steps.** Stop at each gate for the user's own words.
1. **Intake.** Raw takes (not a pre-edited version), platform, target length (15, 30 or 60 s), who is on camera and their consent, brand fonts, editor if any. `ult media FILE` for each take.
2. **Transcript.** Timecoded, from a local tool (`ult posts captions --transcribe` uses whisper.cpp if installed). A paid service needs a yes first.
3. **Paper edit** (`hooks.md`). Pick one idea per short. Write the hook line, the kept lines in order and the last line, with in and out times, in `cut/<name>.md`. For a long recording, list several shorts, each with its own hook. Show it as text. `ult gate approve papercut "<their words>"`.
4. **Rough cut** (`edit.md`). `ult cut silences TAKE` writes `cut/<take>.json`; delete takes the paper edit dropped, move the hook take first, then `ult cut check PLAN --platform P`. Render with `ult cut render PLAN --out media/<name>/rough.mp4 --vertical --punch 1.12`. Watch every join.
5. **Finish** (`edit.md`). Captions (`ult posts captions`), b-roll and text, music under speech (`ult audio mix`), then `ult media` and `ult posts check --platform P`.
6. **Review.** Log problems with `ult loop add "<finding>" --where "<file and time>" --blocker` (or `--minor`). The plugin's `taste-critic` agent checks hook, pace and caption layout; the `compliance-reviewer` agent checks claims, consent, music licences and any AI shots. Open blockers stop delivery.
7. **Yes.** Show the export, its length and the licence log. `ult cut deliver FILE` records it (`## Delivered video`); on yes `ult gate approve video "<their words>" --file PATH`. Posting is Social Media's publish gate.

**Rules.**
- Never change what someone meant. A join that makes a new claim goes to the compliance reviewer.
- Real people need consent before export. Never clone a voice or a face.
- Media stays out of Git; plans and the paper edit go in.
- Cut by ear, not only by waveform: `ult cut silences` suggests, the listener decides.
- Platform lengths, safe zones and caption limits are "check before relying" (`ult posts specs`).

**Series.** One recording can make 3 to 6 shorts. Give each its own card (`ult board add`), its own hook and one next step, and post them as a series with a shared title format.

**Hand-off.** If the user named an editor, follow `../editors/guide.md`: the cut plan's in and out times become the timeline.

**Small change** (trim, recaption, new hook on an approved cut): change only that, re-render, rerun the checks, watch once. No new paper edit.

**Report:** export paths and lengths, each check and its result, what was cut and why, open items. Claim only what you ran.
