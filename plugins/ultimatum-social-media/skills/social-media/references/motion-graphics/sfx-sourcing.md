# Sound effects

Add them last, once voice and music timings are locked. Keep effects under the voice and music (duck or lower them if they mask words).

## Order of sources

0. **ElevenLabs sound effects, when connected** (the default): follow `../video/audio.md`; ask before spending credits and log each clip.
1. **One CC0 pack first**, e.g. Kenney's audio packs (CC0, no credit needed). Download it once to a local folder outside the project or in a git-ignored folder (`media/sfx/`, add it to `.gitignore`). Never commit packs.
2. **Test every file before using it:** play it, check `ffprobe` reads it, note its length, and listen for clicks or noise at the start and end.
3. **Gaps only:** if the pack has nothing that fits, look on Pixabay or Freesound, one file at a time.

## Per-file licence check (Pixabay, Freesound and anything else)

- Read the licence on that file's own page, not the site's summary.
- **Non-commercial (NC) → skip it.**
- Attribution (CC BY) → allowed; add the credit.
- CC0 or the site's own licence that allows commercial use → allowed; still log it.
- Unclear licence → skip it.

Licence terms change; these notes are a starting point, so check before relying on them.

## brand/sound-credits.md

One line per file used:

```
| File | Source URL | Author | Licence | Credit needed | Used in |
|---|---|---|---|---|---|
| whoosh-01.ogg | <pack or file page> | Kenney | CC0 | no | launch-video |
```

Put required credits in the video description or the site's credits page, and tell the user where they went.
