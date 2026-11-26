# Video · Audio (ElevenLabs by default)

Order of sources: (1) ElevenLabs through its connector or API, when available and the user said yes to the credits; (2) the user's own recordings, or music and effects whose licence allows commercial use (CC0, or a paid library plan that fits the use), each logged; (3) Suno by hand, only when the user asks for it. Every file ends up as a real file in `media/audio/` with a row in `brand/sound-credits.md`; a prompt alone is not a delivery. Checked against the ElevenLabs connector's own model list in November 2026; check the current list (`creative_get_flow_node_types`, or the API reference) before relying on any name below.

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
- **No ElevenLabs:** ask for the user's own track or a licensed one first (`../shared/licenses.md`); log it with `ult audio credits add <file> --source <page> --licence "<licence>"`.
- **Suno (last, by hand):** only if the user asks; write the prompt, they generate it and paste the file. Suno has no official public API; free-plan tracks are non-commercial, and `ult audio credits check` blocks them.

## Sound effects

- Sound effects node (0.5 to 30 s each, loop on for beds). Describe the sound, its length and how it starts and ends ("short soft whoosh, 0.6 s, fast attack, quick fade").
- Through the API it is `POST /v1/sound-generation`; with a set duration it was billed per second (40 credits a second in November 2026). Keep effects short and few.
- No ElevenLabs: follow `../motion-graphics/sfx-sourcing.md` (one CC0 pack first, then single files with a per-file licence check).

## Mix

- ElevenLabs Composition node: connect voice, music and effects; it levels each clip by role and ducks music under speech. Or mix here: `ult audio mix vo.wav music.mp3 --out media/audio/mix.m4a [--video cut.mp4] [--loop]` ducks the music under the voice (about 8 dB, `--duck`), normalises in two passes and prints the measured loudness and true peak; exit 1 when out of range.
- Target -14 LUFS integrated, true peak at most -1 dBTP; run the audio check in `../motion-graphics/audio-sheet.md` and report the measured numbers.
- Log every clip in `brand/sound-credits.md`: `ult audio credits add <file> --source <tool or page> --licence "<plan or licence>"`. Before delivery run `ult audio credits check --dir media/audio` (add `--use paid-ad` for paid ads); blockers stop delivery.
