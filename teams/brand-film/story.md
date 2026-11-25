# Brand Film · Story

The Writer reads this for gate 1. Text only, no search, no spend. The user approves story before anything else happens.

## Logline

One sentence: **one person, one want, one obstacle.** Example shape: "A night-shift nurse wants to be home for her daughter's recital, but the ward will not let her leave." Write your own. Reference films set mood and structure only; never reuse their character, situation or lines.

If the message is a belief and not a person (an anthem), the logline is the belief plus the line that flips it.

## Pick one sub-genre

| | Character arc | Anthem montage |
|---|---|---|
| Spine | One named person, one situation | Many people, one repeated line |
| Setup | Their normal, and the want | The line, said plainly, over ordinary effort |
| Friction | The obstacle tightens; small failures | Faces working, failing, trying again; the line repeats |
| Hush | One held shot, near silence | The music drops; the line is not said |
| Turn | The person acts, helped by the product | The line returns changed (it flips its meaning) |
| Resolution | The want met, or honestly changed | The same faces, lighter |
| Brand | Last | Last |

## Beat sheet (share of runtime)

| Beat | Share | Job |
|---|---|---|
| Setup | 0 to 20% | Who, where, what they want. One image of their world. |
| Friction | 20 to 60% | The obstacle grows. Feeling must build, not stay flat. |
| Near-silence | 1 to 3 s, just before the turn | Music thins or stops. A face, a breath, a sound from the room. |
| Turn | 65 to 80% | The earned peak. The music swells or lands. The product enables it. |
| Resolution | after the turn | Show the result, not an explanation. |
| Brand | last | Logo, line, call to action. |

For a 75 s film: setup to 15 s, friction to 45 s, hush near 48 s, turn at 49 to 60 s, brand in the last 5 to 8 s.

## Brand codes throughout

The product waits for the turn, so the brand must still be felt from the first seconds. Carry a palette, a typeface for any text, and a sonic motif (a sound or two-note cue) through the whole film. On the 9:16 cutdowns the brand cue lands within 2 s.

## Pace

- **Voiceover:** 1.2 to 1.8 words per second on average, with whole stretches silent. A 75 s film needs at most about 110 words. Check with `ult film --vo FILE --seconds N`.
- **Shots:** 2.5 to 6 s. Hold on a face up to 8 to 10 s. Short bursts only when the story speeds up.
- **No 10 s stretch** without emotion or curiosity.
- Honest warmth and quiet hope. No manufactured tears, no sad-for-sale tricks.

## What the Writer returns

Fill every field. Keep it under one page.

```
Logline:
Sub-genre: character | montage
Audience and the one feeling to leave them with:
Length: hero __ s (60 to 90); cutdowns 30 s, 15 s
Character (age, place, stakes) or the line and how it flips:
Beats (with target seconds):
  Setup:
  Friction:
  Near-silence:
  Turn:
  Resolution:
  Brand (logo, line, call to action):
Brand codes (palette, typeface, sonic motif):
Voiceover draft (words, words per second):
Product's role in the turn:
Real people needed (who films them):
References (mood only) and what is deliberately different:
Open questions for the user:
```

Save as `film/story.md`.

## Showing it at the story gate

Tell it in plain words first: the logline, then the film as a short run of moments with times, then the voiceover lines. Say which sub-genre and why. Name the real people it needs and that AI will only stand in for places and b-roll. Give one alternative if the user may want another angle. Then **stop and wait.** On yes: `ult gate approve story "<their words>"`.
