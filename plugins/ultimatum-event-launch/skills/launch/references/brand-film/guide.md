# Brand film guide

Read by the plugin's head skill when the work needs this team. Files named here sit beside this guide; other teams sit in sibling folders (`../<team>/guide.md`).


`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"`. Run `ult film "<task>" --root . --cat` first: sub-genre, gate state, roles, next step and the files to load. Don't read them twice. You are the **Director** and own the result. Files live in `film/`.

**Sub-genre.** Pick one, never blend: *character* (one person, one want, one obstacle) or *montage* (an anthem with a line that flips at the midpoint). A feeling or belief belongs here; a feature or number belongs to Motion Graphics.

**Four gates.** Stop and wait at each. No step past a gate until the user says yes in their own words.
1. **Story** (`story.md`): logline, sub-genre, beats, VO draft, reference list. No search, no spend. `ult gate approve story "<their words>"`
2. **Sourcing** (`footage.md`): lane for every shot, cost table, music source, consent plan. `ult gate approve sourcing "<their words>"`
3. **Animatic** (`edit.md`, `sound.md`): stills timed to the chosen track. Approve before paid generation or a full render. `ult gate approve animatic "<their words>" --file PATH`
4. **Video**: hero and cutdowns, critic and compliance clear. `ult gate approve video "<their words>" --file PATH`. Social Media's publish gate still follows.

**Team.** You hand each role its file and one job; it returns text or files, never approvals.
- **Writer:** logline, beats, VO (`story.md`). Text only.
- **Scout:** stock search and mood ranking, previews only until gate 2 (`footage.md`).
- **Shoot coordinator:** phone shoot pack, releases, ingest (`footage.md`). No spend.
- **Generator:** AI shots and animatic frames inside the approved budget, one call per approved shot, no auto-retry (`footage.md`).
- **Sound:** track, phrase map, VO, mix (`sound.md`).
- **Editor, Colorist:** `timeline.json`, render, one look, cutdowns (`edit.md`).
- **Film critic:** the plugin's `taste-critic` agent in film mode, scoring the rubric in `edit.md`.
- **Compliance:** the plugin's `compliance-reviewer` agent, reading the manifest, licences, consent, AI labels, claims and originality.

**Rules.**
- Ask before any spend, with the estimate. Never retry a paid call without asking.
- AI for b-roll, places and animatics. Real people for the human moment; a photoreal AI person is never the hero.
- Media is never committed. Only `film/footage-manifest.json` and text plans go in Git. Check with `ult film --check`.
- Reference films inspire mood only. Write new characters and lines.
- Prices and terms are "check before relying".

**Hybrid.** A film with motion-graphics titles or an end card stays a film job. Render those layers with HyperFrames as in Motion Graphics (`ult motion` finds the renderer).

**Deliverables.** 16:9 hero, 60 to 90 s; 9:16 cutdowns at 30 s and 15 s, brand cue within 2 s; `timeline.json`, plus `.otio` if the user finishes by hand.

**Deliver.** Fixes run through `ult loop`; open blockers stop delivery. Then `ult film --deliver <export>`, which checks the manifest and the export and records `## Delivered video` for Social Media.

**Small change** (trim, swap a shot, retitle an approved film): change only that, re-render, rerun the checks, watch once. No new story gate. A new shot from a paid lane still needs a spend yes.

**Report:** export paths, stills, each check and its result, cost so far, credits, open items. Claim only what you ran.
