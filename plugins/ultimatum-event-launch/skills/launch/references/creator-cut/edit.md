# Creator Cut: the edit

From an approved paper edit to a finished vertical short. Platform specifications are **check before relying** on each platform's own help pages (`ult posts specs`).

## Rough cut with `ult cut`

1. `ult cut silences media/raw/take1.mp4` writes `cut/take1.json` with every spoken stretch as a take. Start at the defaults (`--noise -35`, `--min 0.35`, `--pad 0.1`). A noisy room needs a higher threshold (for example `--noise -30`); a speaker who sounds clipped needs more `--pad`.
2. Edit the plan to match the paper edit: delete dropped takes, move the hook take first, split a take by copying it and changing the times. Write why in each take's `note`.
3. `ult cut check cut/take1.json --platform tiktok`: blockers (takes past the source end, over the length limit) stop the render. Fixes flag a slow first take, takes over 8 s with no change, and fragments under 0.3 s.
4. `ult cut render cut/take1.json --out media/<name>/rough.mp4 --vertical --punch 1.12`. `--vertical` center-crops to 9:16 at 1080x1920; frame the speaker near the middle when filming. `--punch` zooms in on every other take, which hides jump cuts. Add `--print` to see the ffmpeg command and keep it in the notes.
5. Watch every join. Re-cut any that drops the start or end of a word, sounds breathless, or joins two sentences into a new meaning.

## Pace

- Something changes on screen every 2 to 4 seconds: a cut, a punch-in, a caption, b-roll, a text card. This is a habit, not a law; a calm teacher can hold longer.
- Keep one short breath between sentences. Removing every pause sounds robotic.
- Match the speaker. Fast cuts for an energetic creator, gentler ones for a thoughtful founder.
- Never speed up speech past what sounds natural. Cut words instead.

## Captions

- Burned in, synced to speech: `ult posts captions VIDEO --srt FILE --platform P` (or `--transcribe --model PATH` with whisper.cpp). Also keep the `.srt` for platforms that accept caption files.
- One to two short lines on screen, or a few words at a time for a fast pace. Heavy sans-serif with an outline or a soft box; the brand font only if it reads small.
- Check names, numbers and product terms by hand.
- Keep text above the platform's bottom safe zone and clear of the right-side buttons. `ult posts check` warns on size and length; preview one frame with a mock overlay for layout.
- Highlight a key word in the brand accent sparingly, once or twice per short.

## B-roll and text cards

- Cover a jump cut, show what the speaker names, or prove a claim (a screen, a product, a result).
- The user's own clips first, licensed stock with a logged licence next, AI shots only after a yes and labelled where the platform asks.
- Never imply something untrue: another company's office, a crowd that was not there, a result not achieved.
- A text card (a number, a list item) is a motion-graphics layer; keep it on brand and short.

## Sound

- Speech first and clear on a phone speaker. Normalise the voice; `ult media` reports loudness.
- Music is optional. Use owned or licensed music and log it (`ult audio credits add`), then `ult audio mix VOICE MUSIC --out FILE` ducks it under speech. In-app platform music added at upload often does not cover ads: check before relying.
- A small sound effect on a punch-in or a text card is enough; more becomes noise.

## Finish checks

| Check | Command or how |
|---|---|
| Export facts and loudness | `ult media FILE` |
| Platform size, length, caption | `ult posts check FILE --platform P --caption-file F` |
| Music licences | `ult audio credits check --dir media/audio` |
| Hook lands by 2 s, one idea, one next step | watch it, then the `taste-critic` agent |
| Claims, consent, music, AI | the `compliance-reviewer` agent |

## Cover and title

- Pick a frame with the speaker's face and a clear expression, or add a short title in the safe area.
- The title states the idea in a few words; it can match the hook but should not repeat the caption word for word.
- Series: keep the same title format and position, for example a part number, so the grid reads as one set.

## Beginner mistakes

| Mistake | Fix |
|---|---|
| Every pause removed | Keep a short breath; raise `--pad` |
| Hook said at 0:08 | Move that take to the top of the plan |
| Captions under the buttons | Check safe zones in `ult posts specs` |
| Crop cuts off the speaker | Re-film centered, or cut in the editor with manual framing |
| Same punch-in on every take | Alternate; `--punch` does every other take |
| Music louder than speech | `ult audio mix` with ducking; test on a phone |
