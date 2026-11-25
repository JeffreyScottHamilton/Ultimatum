# Audio sheet

Make it after the storyboard is approved and before any animation. The animation follows the audio, not the other way round.

## brand/sound.md (written once)

On the first video, agree these with the user and save them; later videos reuse them unchanged unless the user asks:

```markdown
# Sound
- Voice: <ElevenLabs voice name and voice_id, from the user or the voice list>
- Voice settings: model <id>, stability <0–1>, similarity <0–1>, style <0–1>, speed <0.7–1.2>, speaker boost <on/off>
- Music style (locked): <genre, tempo in BPM, mood, 2–3 instruments, "no vocals" or not>
- Loudness target: -14 LUFS integrated, -1 dBTP true peak
- SFX pack: <name, licence>
```

## The sheet for one video

```
Video: <name>, <length> s, <format>
Voiceover
  Text: <exact words, one line per storyboard shot; use punctuation for pauses>
  Voice: <from brand/sound.md>  Settings: <copied exactly from brand/sound.md>
  Output: mp3 44.1 kHz or wav; file name vo-<name>.mp3
Music
  Suno prompt: <the locked style> + <length>, <energy curve: e.g. calm intro, lift at 0:08, end on a hit>
  Instrumental: yes/no   Output: music-<name>.mp3
```

Then either:

- the user generates both and pastes the files (or their paths) back, or
- with the ElevenLabs connector available: say what will be generated and that it spends the user's credits, wait for a yes, generate once (never repeat a call to retry), and save the files under `media/audio/`.

Say once per project: Suno's free plan allows non-commercial use only; a business video needs a paid plan, or use a music source whose licence allows commercial use (see the launch licence notes, and check before relying on them).

## Timings

- Voice: get word or line start times from a timestamped transcript (the connector's transcription, or listening) and write them next to each shot.
- Music: `ult beats music-<name>.mp3` gives suggested beats or possible cues. Listen and confirm before cutting on them.

## Audio check (after the mix)

```bash
ffmpeg -hide_banner -i final.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=summary -f null -
ffmpeg -hide_banner -i final.mp4 -af astats=metadata=1 -f null - 2>&1 | grep -i "peak level"
ffprobe -v error -show_entries format=duration:stream=codec_type,duration -of compact final.mp4
```

Pass when: integrated loudness is within about 1 LU of -14 LUFS, true peak is at most -1 dBTP, no peak reaches 0 dBFS (clipping), and the audio and video durations match within a frame or two. If loudness is off, normalise with a two-pass `loudnorm` and check again. Report the numbers you measured.
