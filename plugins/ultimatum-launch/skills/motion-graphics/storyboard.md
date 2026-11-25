# Motion planning and storyboard (Planner and Designer)

Used for a new clip before any production animation. Write everything in the shared brief (`.ultimatum/brief.md`) so the Animator and Reviewer read one file.

## 1. Brief

- **Goal:** what the viewer should feel or do at the end (remember the name, visit the site, feel the launch).
- **Audience and place:** who watches and where (Instagram reel 1080x1920, YouTube 1920x1080, a website hero loop, a slide).
- **Length:** a target in seconds. Short is better: 6, 10, 15 or 30 seconds.
- **Assets:** logo files, colours, fonts, words on screen, music, voice-over, footage. Missing → mark `[[PLACEHOLDER: …]]` and keep going.
- **Reference:** if the user shares a clip they like, note what to borrow (pace, energy, how it builds), never its look or content.

## 2. Story and sound

Plan the clip as a build toward **one reveal** (the logo, the product, the line that matters):

1. **Hook** (first 1-2 s): something moves at once.
2. **Build:** each shot adds one idea; cuts get closer together as it rises.
3. **Reveal:** the payoff lands on the strongest sound (a drop, a hit, a pause before it).
4. **Hold:** keep the final frame still long enough to read (about 1.5-2 s).

With music, run `ult beats <file>`:
- With librosa installed, it prints **suggested beats**.
- Without it, it prints **possible cues** (loud onsets found with ffmpeg).
- Either way the times are suggestions. Listen and adjust each cue you will cut on, and write the confirmed times in the brief.
- With no tool and no music, plan timing by counts (for example, a cut every 0.5 s at 120 bpm).

## 3. Storyboard

A table in the brief, one row per shot:

| # | Time (rough) | Frame: what we see | Motion and transition in | Sound cue |
|---|---|---|---|---|

- Rough times are fine. Mark each one "suggested" until it is checked against the audio.
- Give 4-8 key frames for a 10-15 s clip.
- Every word on screen stays up long enough to read: about 0.3 s per word, and never under 1 s.
- Keep text inside safe margins: about 5% from each edge, more for vertical social video, where buttons cover the bottom and right.

**Frames.** If an image tool is available, make one picture per key frame from the same style notes. If not, write one image prompt per key frame, each with:
- format and aspect
- background and palette
- the main subject and where it sits
- the exact words on screen
- the type style
- the mood

Keep the style notes identical across the frames so they look like one clip.

## 4. Show it and stop

Show the storyboard table and the frames, or the prompts. Explain the idea in plain words: how it opens, how it builds and what the reveal is. Then end your turn. No production animation until the user approves.

When the user approves, or asks for changes and then approves, record it in their words:

`ult motion --approve "<what was approved: shots, timing, style, changes asked for>" [--image <frames image if saved>]`

This writes an **Approved storyboard** section in the brief. The Animator builds from it, and the Reviewer checks the export against it.

Ideas from HyperFrames' story and sound guidance (heygen-com/hyperframes, Apache-2.0); the wording is Ultimatum's own.
