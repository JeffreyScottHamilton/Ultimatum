# Brand Film · Edit

Read by the Editor and Colorist for gates 3 (animatic) and 4 (video), and by the Film critic for the rubric. Files in `film/`.

## Order of work

1. **Shot list** (`shots.md`) from the approved story and sourcing plan.
2. **Animatic:** one still or preview frame per shot, timed to the chosen track's phrases (see `sound.md`). Render a rough `animatic.mp4`. AI frames are fine here. This is gate 3.
3. **Timeline first.** Write `film/timeline.json` before any render: per shot the file, in and out, beat, transition; title layers; music; VO; the look. The render only follows this file, so the same input gives the same cut.
4. **Render** with ffmpeg: trim, concat or `xfade`, scale and crop, then the look chain, then audio mix.
5. **Self-check at every cut.** After each render, extract frames either side of each cut and the shot's midpoint. Look for black frames, wrong shot, jump, wrong crop, freeze. Fix the timeline and re-render the cut. At most 3 retries per cut, then report it and move on.
6. **Review pack**, then critic, then compliance, then gate 4.

## Cutting

- Cut on musical phrases (4 or 8 bars), not on every beat. Story beats sit on phrase boundaries. The turn lands on the swell, or on the drop to silence just before it.
- Inside a phrase, cut on action in the picture.
- Shots 2.5 to 6 s. Hold a face up to 8 to 10 s. Speed up only when the story does.
- Prefer cuts and short dissolves. Fancy transitions need a reason.
- Reframe for 9:16 from the safe centre of each shot.

## Look

- Match shots first (exposure, white balance). Use ffmpeg `signalstats` for per-shot brightness and colour numbers.
- Then **one** look for the whole timeline: a `.cube` LUT with `lut3d=file.cube`. Use a LUT you made or one with a clear licence.
- Add grain **once**, at timeline level, not per clip.
- Save the approved look, typeface and sonic motif in `film/style.md` for later films.

## Titles and end card

Titles, supers and the end card come from HyperFrames layers, as in Motion Graphics (`ult motion` finds the renderer). The end card carries logo, line and call to action, with the URL or call to action before the final logo frame, plus any legal text. This stays a film job.

## Cutdowns

Cut each aspect from the timeline, not by cropping the finished hero.
- 16:9 hero, 60 to 90 s, with a safe 9:16 centre.
- 9:16 at about 30 s and 15 s. Brand cue within 2 s. Keep the setup, hush and turn; drop friction first.
- 1:1 only if asked.
Each cutdown gets its own timeline and its own self-check and loudness check.

## OTIO export

If the user finishes by hand in Resolve or Premiere, export the timeline to `film/timeline.otio` (OpenTimelineIO, Apache-2.0). Note the FCPXML adapter drops transitions. Tell the user which parts to rebuild.

## Review pack

Build it with ffmpeg and show it at gates 3 and 4:
- a contact sheet (one frame per shot, labelled with shot number and beat);
- a timeline PNG: filmstrip, audio waveform, beat markers, the hush and turn marked;
- cut list with times and lanes;
- loudness reading and VO words per second;
- the manifest check result and total cost.
Give 2 or 3 stills in chat. Findings carry timestamps.

## Film critic rubric

The critic (the plugin's `taste-critic` agent, film mode) watches the export or reads the pack, scores each line 1 to 5 and gives timestamps. Anything under 3 is a finding.
1. No 10 s stretch without emotion or curiosity.
2. An earned peak at the turn.
3. Feeling builds; it does not stay flat.
4. A specific character with recognisable stakes.
5. Brand recognisable without the end card; brand cue within 2 s on 9:16.
6. The product enables the turn; it does not interrupt it.
7. Honest warmth, not manipulation.
8. Originality: compare logline, lines and shot list with the references; block near-copies of another brand's line, structure or branding.

Blockers go into `ult loop`. The Editor fixes, the critic rechecks. Open blockers stop delivery.

## Tools

| Tool | Licence | Use |
|---|---|---|
| ffmpeg | LGPL/GPL build dependent; use as an external tool | render, LUT, loudness, frames |
| HyperFrames | Apache-2.0 | titles, end card |
| OpenTimelineIO | Apache-2.0 | hand-off to Resolve |
| PySceneDetect | BSD-3 | shot boundaries in supplied footage |
| Whisper / faster-whisper | MIT | word times to check VO pace |
| librosa | ISC | beat grid, energy |
| colour-science | BSD-3 | colour statistics |

Avoid aubio (GPL-3.0) and madmom models (non-commercial). Check the licence of allin1 or beat_this before use. Remotion only if the user qualifies for it or pays (see `licenses.md`). Licences: **check before relying**.
