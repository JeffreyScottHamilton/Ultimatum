# Video · Guide

One fixed pipeline for every video, whatever makes the pictures. Each step has an owner file and an output; never skip ahead.

| Step | Do | Output | Stop for |
|---|---|---|---|
| 1. Script | Hook in the first 2 s, one idea, one call to action. Spoken words at about 2.5 words per second (1.2-1.8 for a brand film). | `video/<name>/script.md` | — |
| 2. Shots | One row per shot: time, picture, words on screen, voice line, sound cue, **source** (own footage, motion graphics, Higgsfield, stock). | `video/<name>/shots.md` | user's yes (`ult gate approve storyboard`) |
| 3. Pictures | Make each shot from its source: motion graphics with `../motion-graphics/guide.md`; generated video with `higgsfield.md`; own footage or stock with `../brand-film/footage.md`. | `media/<name>/shots/` | yes before any paid generation |
| 4. Audio | Voice, music and effects with `audio.md` (ElevenLabs by default). Voice first: its timings set the cut. | `media/<name>/audio/` | yes before spending credits |
| 5. Assemble | Cut to the voice, then the music phrases. Locally with ffmpeg or HyperFrames, in the ElevenLabs Composition or Video Editor node, or in the user's editor (`../editors/guide.md`). Captions burned in or as a file. | `media/<name>/<name>.mp4` | — |
| 6. Review | `ult media FILE`, the audio check in `../motion-graphics/audio-sheet.md`, stills at each cut, then the reviewer agents. Log issues with `ult loop add`. | findings fixed | open blockers stop delivery |
| 7. Yes | Show the export and the licence log. Only the user's words approve it: `ult gate approve video "<their words>"`. | approved file | — |

## Choosing the picture source

- **Product ad, UGC-style, e-commerce product video:** Higgsfield first (`higgsfield.md`), from the user's own product photos. Motion graphics second.
- **Explainer, feature, number, how it works:** motion graphics.
- **Feeling carried by people (brand film):** `../brand-film/guide.md`; own footage or licensed stock first, generated shots only for gaps and labelled.
- **Someone talking to camera, made into shorts:** `../creator-cut/guide.md` (paper edit, `ult cut` jump cuts, captions).
- **The user has footage:** use it first; generation fills gaps only.

## Rules

- One shot list is the contract. A change to the story goes back to step 2 and a fresh yes.
- Every paid call: say what it makes, which tool, the cost or credits if known, wait for a yes, run it once (never repeat a call to retry), then review the result before the next one.
- Keep media out of Git (`media/` git-ignored). Keep a licence line for every asset in `brand/sound-credits.md` or `video/<name>/licences.md`.
- Label AI-generated people, voices and scenes where the platform asks for it. Real people need consent; never clone a voice or face without the owner's written yes.
- Prices, models and limits change: check the vendor's own page or tool list before relying on them.
