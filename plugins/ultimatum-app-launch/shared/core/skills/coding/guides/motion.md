# Motion guide (Animator)

Build from the brief's **Approved storyboard**. Each shot, its timing and its transitions come from that table. If something must change, tell the Manager. Do not drift from it quietly.

## Renderer (use the first one this machine has; `ult motion` prints which)

1. **HyperFrames**, when installed. This is the preferred tool. Write each scene as HTML and CSS, then render it to MP4 with its CLI. Follow its docs from the installed package; do not install it without the user's yes.
2. **HTML and CSS captured in a browser** (node and Playwright are present):
   - Build one page that plays the whole clip on a timeline.
   - Drive time from one variable, so frame N is always the same picture.
   - Screenshot every frame at the target fps.
   - Join the frames and the audio with ffmpeg:
     `ffmpeg -framerate 30 -i f%05d.png -i music.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest out.mp4`
3. **ffmpeg only:** use filters (`drawtext`, `drawbox`, `overlay`, `xfade`, `fade`) with time expressions. This is fine for simple type and logo work.

If no renderer is found, deliver the animation code and the storyboard, and say the video was not rendered.

## Timing and easing

- **Rough cut first:**
  - Put the cuts on the confirmed cues, with placeholder shapes and the real audio.
  - Watch it.
  - Then add detail.
- **Easing:**
  - Things that enter decelerate (ease-out).
  - Things that leave accelerate (ease-in).
  - Things that move across the frame use ease-in-out.
  - Avoid linear motion except for constant drifts or spins.
- **Durations:**
  - Small elements: 150-300 ms.
  - Big moves and scene transitions: 400-800 ms.
  - The reveal can take longer.
  - Nothing important moves faster than the eye can follow.
- **Rhythm:**
  - Stagger related items by 40-80 ms.
  - Hold still for a beat before the reveal, so it lands.
- **Movement:**
  - Move only transform and opacity in HTML.
  - Keep motion purposeful: each animation shows where to look or what changed.
- **Clip on a website:** honour `prefers-reduced-motion` with a still frame or a gentle fade.

## Export

- **Video:** H.264, `yuv420p`, even width and height, 30 fps (or 24 or 60 to match the brief).
- **Audio:** AAC 48 or 44.1 kHz.
- **Size:** match the brief's format: 1080x1920 for vertical social, 1920x1080 for landscape.
- **Loudness:** about -14 LUFS for social. `ult media` measures it.
- **Hand back** the file path, `ult media <file>` output, and stills at the key times:
  `ffmpeg -ss 2.5 -i out.mp4 -frames:v 1 still.png`

Ideas from HyperFrames (Apache-2.0) and Emil Kowalski's animation notes (MIT); the wording is Ultimatum's own.
