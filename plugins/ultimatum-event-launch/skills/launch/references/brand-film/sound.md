# Brand Film · Sound

Read by the Sound role for gates 3 and 4. Music comes before the cut, and voiceover stays sparse.

## Music first

1. Pick or commission the track once the story is approved, and show it at gate 2 with its licence.
2. Listen. Build a **phrase map** in `film/phrases.md`: where each 4- or 8-bar phrase starts, where the music builds, swells, thins. Use `ult beats FILE` for suggested beats, then confirm by listening. Say which you confirmed.
3. Place story beats on phrase boundaries: setup on the opening phrase, friction as it builds, the hush on the thinning, the turn on the swell.
4. Cut the picture to that map, not to every beat.

## Near-silence

Before the turn, 1 to 3 s where the music thins or stops. Leave only room tone, a breath or one small sound. Do not fill it with sound effects. The swell that follows should feel earned.

## Voiceover

- 1.2 to 1.8 words per second on average, with stretches of none. Check with `ult film --vo FILE --seconds N`.
- Record the user's voice, a hired voice, or TTS. For ElevenLabs, follow `../motion-graphics/audio-sheet.md` for settings. Ask before spending credits. A free ElevenLabs plan is non-commercial. Avoid beta models for client or ad work.
- Whisper (MIT) gives word times if you need to check the pace against the timeline.
- Duck the music under voice by about 6 to 10 dB with ffmpeg `sidechaincompress`, and release it in the pauses.

## Room tone and effects

Use the 30 s of room tone from each location under every shot from it, so cuts do not jump. Sound effects come last and sparingly: follow `../motion-graphics/sfx-sourcing.md` (CC0 first, log each licence).

## Loudness

Target **-14 LUFS integrated, true peak at most -1 dBTP**. Measure with `ffmpeg -i IN -af ebur128=peak=true -f null -`. Normalise with two-pass `loudnorm` (measure, then apply the measured values with `linear=true`). Check each cutdown separately. Then `ult media FILE` and `ult film --deliver FILE`.

## Music licensing

All **check before relying**.
- **Paid ads:** a human-composed track on a business or ad-cleared plan carries the least risk. Epidemic Sound needs its Pro or Enterprise tier for ad campaigns. Artlist's personal licence excludes paid or promoted video. Reports differ on whether Musicbed's Business plan covers client paid ads; ask them.
- **Generated (default when connected):** ElevenLabs music on a paid plan, made with `../video/audio.md`; check its current terms for the user's plan.
- **Organic posts:** Suno on a paid plan can suit (commercial use only on paid plans; its ownership wording has changed). Free-plan Suno is non-commercial. Suno has no official public API; the user makes the track by hand.
- Skip anything marked non-commercial. Skip unofficial API wrappers.
- Purely AI-made music may not be copyrightable. Tell the client.

## Files

Write to the shared files, so later films and Motion Graphics reuse them:
- `brand/sound.md`: the sonic motif, track style, voice and settings (write once; reuse on later films).
- `brand/sound-credits.md`: every track, voice and effect, with source, licence, date and plan used.
Downloaded audio stays local and out of Git.
