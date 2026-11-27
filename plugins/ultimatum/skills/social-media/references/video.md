# Editing a video

Read this when a post is a video and the user wants it cut, captioned or styled, not just scripted. Pick the style first (`styles.md`), then work through the steps below in order.

Everything runs on the user's machine through `ult video` and the local ffmpeg. Nothing is uploaded. If `ffmpeg` is missing, `ult video` says so and exits 2: tell the user how to install it (`brew install ffmpeg`, `apt install ffmpeg`, or the build from ffmpeg.org) and stop there. Do not install it for them.

## 1. Gather the footage

Where footage can come from, best first:

1. **The user's own clips and photos.** Ask for them by name and put them under `social/media/`.
2. **Text cards.** A card is a colour plus a few words. They need no footage at all and suit kinetic text.
3. **Stock the user licenses.** Note the site and the licence in the edit (`"licence"` on music; a line in `social/media/SOURCES.md` for clips).
4. **AI-generated clips.** Only when the user says yes to the tool and to its cost. Mark each such shot `"ai": true` and set `"ai_label": true` on the edit. Never generate a real, identifiable person without their consent.

Every media path in an edit must sit inside the project. `ult video` refuses paths that climb out with `..`, absolute paths elsewhere, and symlinks that point outside.

## 2. Get word timings (talking videos)

Captions that land on each word need word times. Ask the user to run Whisper or a similar speech-to-text tool locally on the clip with word timestamps on, and to save the JSON next to the clip. `ult video` reads both its own `{"words": [{"w", "start", "end"}]}` list and Whisper's `segments[].words[]`.

To cut the pauses out of a talking clip:

```
ult video jumpcuts social/media/take1.words.json --src social/media/take1.mp4 --out social/edit.json
```

It joins words with gaps up to `--gap` seconds (0.35 by default) and pads each kept stretch by `--pad`. The edit it writes maps the caption times onto the cut timeline for you, with paths relative to the edit file.

## 3. Write the edit

`social/edit.json` is the cut list:

```json
{
  "style": "talking-head",
  "platform": "tiktok",
  "size": [1080, 1920],
  "fps": 30,
  "shots": [
    {"card": "You are doing mornings wrong", "bg": "#111111", "dur": 1.0},
    {"src": "media/take1.mp4", "in": 0.4, "out": 2.9, "tags": ["hook"]},
    {"src": "media/broll.mp4", "in": 3.0, "out": 4.2, "zoom": 1.15, "fade_in": 0.2}
  ],
  "captions": {"whisper": "media/take1.words.json", "source": "media/take1.mp4"},
  "music": {"src": "media/track.mp3", "start": 12.0, "gain_db": -20, "licence": "Artlist, licence 1234"},
  "sfx": [{"src": "media/whoosh.wav", "at": 1.0, "gain_db": -8}],
  "lut": "looks/warm.cube"
}
```

- `in` and `out` are seconds in the source clip. Cards take `dur`.
- Tags the check reads: `hook` (the picture is the hook), `product` and `hold` (story film).
- Caption times are on the finished timeline, unless `captions.source` names the clip they came from. Then only the words inside kept shots are shown, and their times are moved to match the cut.
- `captions.lines` (`text`, `start`, `end`) suits story film; `captions.words` suits word-by-word styles.
- `caption_y` (a fraction of the height) moves the caption band. `mute: true` on a shot drops its sound.

## 4. Check before rendering

```
ult video check social/edit.json
```

**Blockers** (exit 1):
- wrong size for the platform
- longer than the platform allows
- missing files
- paths outside the project

**Fixes:**
- length outside the style's range
- shots too long or short for the style
- no words before the hook time
- captions under the platform's buttons
- pace in words a second
- story-film order
- music with no licence noted
- AI footage with no label

Fix what you can. If you leave a fix in place, say why.

## 5. Taste test

Before the full render, render the first few seconds in two or three styles:

```
ult video sample social/edit.json --styles talking-head,meme-cuts,kinetic-text --seconds 4
```

Each style gets an MP4 and a still in `social/samples/`. Show the user the stills, or send the files, and ask which feels right. One question, three choices. Then set `style` in the edit to their pick.

## 6. Render

```
ult video render social/edit.json --out social/out/post1.mp4
```

What the render does:
1. Cuts and scales each shot to the frame, applying punch-in zooms (from the shot, or every Nth shot as the style sets) and fades.
2. Burns in the captions and cards, styled from the recipe.
3. Applies the style's grade, grain and vignette, plus the LUT if one is given.
4. Mixes the voice, the music (ducked under speech when the style says so) and the sound effects.
5. Sets the loudness to the style's target (−14 LUFS, true peak under −1 dBTP).

`--sample N` renders only the first N seconds.

## 7. Feel check, then fix (up to 3 rounds)

```
ult video feel social/out/post1.mp4 --edit social/edit.json --frames social/out/frames
```

It measures the file:
- length, size and frame rate
- the picture changes it can find
- loudness and true peak
- brightness and colour against a reference, if the style has one

It compares these with the edit and the style, and re-runs the edit checks. It writes one frame at 0.2 s, then one at the middle of each shot (up to 24 frames).

Then look at the frames yourself:
- **Hook:** does the first frame make someone stop?
- **Captions:** are they readable at phone size, and clear of the buttons?
- **Faces:** is any face cut off by the crop?
- **Look:** does the grade match the style?
- **Cards:** does the text on each card fit?

If anything is off, change the edit, render again and re-run `feel`. Stop after three rounds and tell the user what still is not right and why. Exit codes: 0 clean, 1 problems found, 2 could not run.

The measured cuts come from picture changes, so two shots that look alike count as one. Neither the numbers nor the frames prove the video is good. They catch the mechanical misses. The user's eye decides the rest.

## 8. Hand over

Run `ult posts check social/out/post1.mp4 --platform tiktok` for the platform's file limits. Then add the file to `social/plan.json` and follow `publish.md`. Report:
- the style
- the length
- the `feel` summary line
- the rounds you took
- anything you left as it was

Never say "posted".

## Music and rights

- Use music only when the user has the right to use it on that platform, for that purpose. A platform's in-app sound library is the safest choice for organic posts. A business account may only get part of that library.
- Write the source and licence in `music.licence`.
- No covers of famous songs, and no "inspired by" sound-alikes of a named track.
