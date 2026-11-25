# Style: the user's own footage

Use this when the user has recorded clips: a talking head, an interview, an event, behind the scenes, a walk-through of a place. The job is to find the strongest moments and cut them into a short vertical video that holds attention and ends on one next step. Platform specifications here are **check before relying** on each platform's own help pages; they change.

## Before cutting

1. Ask for the raw files, not a pre-edited version. Keep them outside Git (a `media/` folder listed in `.gitignore`, or the user's own drive).
2. List what arrived: file name, length, frame rate, resolution, orientation. Read these with `ffprobe` if it is installed; if not, ask the user.
3. Ask who appears on camera and whether each person agreed to be posted. No consent, no use.

## Selecting takes from a transcript

Working from a transcript is faster than scrubbing video.

1. Make a transcript with timecodes. A local tool the user already has is fine; a paid transcription service needs the user's yes first.
2. Read it and mark candidate lines: a clear claim, a surprising detail, a short story with an ending, a strong reaction.
3. For each candidate, note the in and out timecodes and a one-line reason.
4. Pick one idea per video. A 30-second video holds one point, not three.
5. Show the user the shortlist as text before cutting. Changing a line on paper costs nothing; changing a cut costs time.

## The first two seconds

The opening decides whether anyone sees the rest.

- Start on the strongest line or image, not on a greeting, a logo or a breath.
- If the best line sits in the middle of the take, move it to the front as a cold open, then cut back to the build-up.
- Put the hook on screen as text too, because many people watch with sound off.
- Avoid an opening that needs context to make sense.

## Cutting dead air

- Remove pauses, false starts, filler words and repeated phrases. Keep a short breath between sentences so speech does not sound mechanical.
- Jump cuts on a talking head are normal on short-form platforms. Hide a jarring one with a slight punch-in (crop in a little) or a b-roll cut.
- Never cut words in a way that changes what the person meant. If a cut joins two sentences into a new claim, the compliance reviewer must see it.
- Check each cut by listening, not only by looking at the waveform.

## Captions and safe zones

- Burned-in captions for short vertical video; also an `.srt` file when the platform accepts uploaded captions.
- Short lines, two at most on screen, in sync with speech. Check names, numbers and product terms by hand; automatic captions get these wrong most often.
- Use the brand font if it reads well small; otherwise a plain heavy sans-serif with an outline or a soft box behind it.
- Keep captions and on-screen text away from the edges. Each platform overlays buttons, the caption and the account name in different places. Check the current safe-zone guide for each platform before relying on any margin, and preview a frame with a mock overlay.

| Platform | What to check before relying |
|---|---|
| TikTok | Right-side buttons, bottom caption area, maximum length for the account |
| Instagram Reels | Bottom caption and audio label, how the grid crops the cover |
| YouTube Shorts | Bottom title and subscribe area, current length limit |
| LinkedIn, Facebook | Whether vertical or square plays better in the feed today |

## Pacing

- Change something on screen every few seconds: a cut, a punch-in, a caption change, a b-roll shot. This is a habit, not a rule; a calm brand can hold longer.
- Match the pace to the speaker. A thoughtful founder cut like a gaming clip feels wrong.
- End when the point is made. Cut the sign-off that repeats the hook.
- Final beat: the one next step, said and shown as text.

## B-roll

- Cover cuts, show what the speaker describes, and add variety.
- Use the user's own b-roll first, then licensed stock with a recorded licence, then generated shots only after the user's yes and a label where the platform asks for one.
- Never use b-roll that implies something untrue (another company's premises, a crowd that was not there).

## Music under speech

- Speech comes first. Keep music low enough that every word is clear on a phone speaker.
- Use music the user owns, a licensed library track (record the licence), or the platform's in-app library at upload. Licences for in-app music often do not cover the same track in an uploaded file or an ad: check before relying.
- Lower the music under speech (ducking) and bring it up in gaps.
- If a track has lyrics, keep them away from speech.

## Rough-cut review

Before polishing, show the user a rough cut and ask five questions:

1. Is the opening line the strongest one we have?
2. Is the one point clear by the end?
3. Does anything misrepresent what someone said?
4. Is everyone on screen happy to be posted?
5. Is the next step right?

Log each problem with `ult loop add "<finding>" --where "<file and timecode>" --blocker` (or `--minor`). Fix, then show the fine cut. Run the compliance reviewer on claims, consent, music and any AI shots before the final export.

## Hand-off or finish here

- If the user named an editor, follow `editors/guide.md` and hand over a timeline file or work through live control.
- If not, cut here with `ffmpeg` if it is installed, and record each command so the cut can be repeated.

## Beginner mistakes

| Mistake | Fix |
|---|---|
| Opening with "Hi everyone" | Open on the strongest line |
| Three points in one video | One point; make the others separate posts |
| Captions over the platform's buttons | Check safe zones with a mock overlay |
| Music louder than speech | Duck the music; test on a phone speaker |
| Posting someone without asking | Written consent before export |
| Editing on the only copy | Work on copies; keep the originals untouched |
