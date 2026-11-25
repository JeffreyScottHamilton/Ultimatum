# Video · Audio (ElevenLabs by default)

Voice, music and sound effects come from ElevenLabs when its connector or API is available, so one account covers all three. Otherwise the user makes them by hand and pastes the files back. Checked against the ElevenLabs connector's own model list in November 2026; check the current list (`creative_get_flow_node_types`, or the API reference) before relying on any name below.

## Before any generation

1. Read `brand/sound.md` (voice, voice settings, locked music style, loudness target). Missing: agree it with the user and write it (template in `../motion-graphics/audio-sheet.md`).
2. Put every generation for one video on **one flow** (create it first), so voice, music and effects can be wired into a composition.
3. Show the plan: each clip, its length, the model, and that it spends the user's credits. Wait for a yes. Generate once per clip; never repeat a call to retry. Poll for the result, listen, then move on.
4. Free plans are non-commercial. A business or ad video needs a paid plan; check ElevenLabs' current terms for the user's plan.

## Voice (first)

- Text to speech node, voice_id only from the voice list or the user. Keep model and settings from `brand/sound.md` for every video.
- New voice: voice design from the user's description, then save it. Never clone a real person's voice without that person's written yes.
- Word timings: transcribe the finished voice (speech to text) and build the frame-timing document from it.

## Music

- Music node, instrumental unless the user wants vocals, length set to the cut (3 s to 10 min). Prompt: the locked style from `brand/sound.md` plus the energy curve (calm intro, lift at the hook, end on a hit).
- Already have the picture? The video-to-music node scores a connected video; add the locked style as the prompt.
- **Suno (optional, by hand):** if the user prefers Suno, write the prompt for them; they generate it and paste the file. Suno has no official public API; free-plan tracks are non-commercial.

## Sound effects

- Sound effects node (0.5 to 30 s each, loop on for beds). Describe the sound, its length and how it starts and ends ("short soft whoosh, 0.6 s, fast attack, quick fade").
- Through the API it is `POST /v1/sound-generation`; with a set duration it was billed per second (40 credits a second in November 2026). Keep effects short and few.
- No ElevenLabs: follow `../motion-graphics/sfx-sourcing.md` (one CC0 pack first, then single files with a per-file licence check).

## Mix

- ElevenLabs Composition node: connect voice, music and effects; it levels each clip by role and ducks music under speech. Or mix locally with ffmpeg (`sidechaincompress`, then two-pass `loudnorm`).
- Target -14 LUFS integrated, true peak at most -1 dBTP; run the audio check in `../motion-graphics/audio-sheet.md` and report the measured numbers.
- Log every clip in `brand/sound-credits.md`: file, tool and model, date, plan, licence.
