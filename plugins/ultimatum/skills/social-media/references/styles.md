# Video styles

Read this when picking how a video should feel, or when the user says "make it feel like this one". A style is a recipe: a few numbers for pace, captions, grade and sound, plus rules for the editor. The four built-in recipes live in the plugin's `data/video/styles/`. To list them, run `ult video styles`. To see one in full, run `ult video styles <id>`.

Feel comes from a few choices made the same way all the way through:
- how long each shot holds
- what the cut follows (speech, beat or phrase)
- how the words appear
- how the picture is graded
- how loud the music sits against the voice

A recipe writes those choices down so they can be checked, not guessed.

## The four built-in styles

**talking-head**: one person talking straight to camera.
- **Feel:** close and quick.
- **Cuts:** every pause is cut out.
- **Captions:** big, three words at a time, with the spoken word lit up.
- **Zoom:** a slight punch-in on every third shot keeps the frame alive.
- **Music:** low, and it ducks under the voice.
- **Best for:** tips, opinions and founder posts.
- **Lengths:** 15–60 s.
- **Pace:** 2.2–3.6 words a second.

**kinetic-text**: the words are the picture.
- **Picture:** bold cards on flat colour, cut on the beat, two words at a time.
- **Music:** leads.
- **Best for:** announcements, lists and quotes, and any time there is no footage.
- **Lengths:** 7–30 s.

**story-film**: a short human story.
- **Story:** one person, one small want, a quiet held moment, then a turn.
- **Product:** shows up late (after 60% of the running time) and helps rather than sells.
- **Cuts and captions:** long shots cut on the phrase; captions are lines, small and low.
- **Look:** a softer, warmer grade with grain and a vignette.
- **Music:** leads.
- **Best for:** brand films, launches and customer stories.
- **Lengths:** 15–90 s.
- **Pace:** under 1.8 words a second.

**meme-cuts**: loud, quick and in on the joke.
- **Cuts:** shots under a second.
- **Zoom:** a hard punch-in every other shot.
- **Sound:** a sound effect on each beat of the joke.
- **Look:** punchy colour.
- **Captions:** heavy outlines.
- **Best for:** trends and reactions, for brands whose voice allows it.
- **Lengths:** 6–30 s.

## Picking one

Start from what the user has. Then ask which way they want to go only if two styles fit equally well.

| They have | Start with |
|---|---|
| A talking clip | talking-head (meme-cuts if the brand is playful) |
| No footage, only words | kinetic-text |
| Footage of people and places, and a story | story-film |
| A trend or joke format | meme-cuts |

When unsure, render samples of two or three styles (`video.md`, step 5) and let the user choose by eye. Seeing four seconds settles it faster than describing it.

## "Make it feel like this"

When the user points at a video they like:

1. **Get the file.** Ask them for a copy they are allowed to use for reference, saved inside the project. Do not download it from a platform for them.
2. **Measure it.**
   ```
   ult video measure ref.mp4 --recipe-out social/styles/like-ref.json --id like-ref --base talking-head
   ```
   - **What it reads:** cut times, shot lengths, loudness, true peak, brightness and saturation.
   - **What it writes:** a draft recipe built on the closest built-in style (`--base`), with the shot pacing and a `reference` block from the measurements.
3. **Look at it.** Use frames from `feel` on the reference, or the user's own description. Then set by eye, **in your own words**:
   - the caption mode, size and colour
   - the grade
   - the music level
   - the `feel` sentence
4. **Use it.** Recipes in `social/styles/` load with the built-ins, and a project recipe with a built-in's id replaces it. Run `ult video styles like-ref` to check it loads. Then use `"style": "like-ref"` in the edit.

Copy how it feels, not what it contains:
- Measure the pace, cut rhythm, caption treatment and grade, then make your own version.
- Never reuse the reference's footage, music, words, logo or on-screen text.
- Never imitate a living creator so closely that viewers would think it is them.

`feel` compares a render's brightness and saturation with the reference numbers, so you can tell when a grade drifts.

## Writing a new recipe by hand

Copy a built-in recipe to `social/styles/<id>.json`, change the `id`, then adjust:

- `shot`: `min`, `max` and the `avg` range, in seconds.
- `cut_on`: `speech`, `beat` or `phrase`.
- `hook_by`: the time something must be read or heard by, in seconds.
- `pace_wps`: the speaking pace range, in words a second.
- `captions`:
  - `mode`: `word`, `line` or `none`
  - `words_per_card`
  - `size` and `y`: fractions of the frame height
  - `upper`
  - `color` and `highlight`: `#RRGGBB`
  - `outline`
  - `pop`
- `zoom`: punch in on every Nth shot by `scale`.
- `look`: `contrast`, `saturation`, `brightness`, `gamma`, `warmth` (−0.3 to 0.3), `grain` (0–20) and `vignette`.
- `audio`:
  - `music`: `under` (ducked under the voice) or `lead`
  - `music_db`
  - `lufs`
  - `peak`
- `rules`: plain sentences for the editor (you), which no tool checks.

A broken recipe stops `ult video` with the file name and the problem.
