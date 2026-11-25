# Timeline files and the hand-over folder

A timeline file describes the cut (which clip, which part of it, where on the timeline) without containing the media. The user's editor reads it and links to the clips in the hand-over folder. Every import-support claim below is **check before relying**: confirm it in the editor's current manual and test-import a tiny file before building a long one.

## The three formats

| Format | What it is | Good for | Watch out for |
|---|---|---|---|
| FCPXML | XML interchange from Apple's Final Cut Pro, versioned (1.x) | Final Cut Pro; also read by DaVinci Resolve | Version numbers matter; an editor may reject a newer version than it knows |
| OTIO (`.otio`) | JSON from the OpenTimelineIO project (Academy Software Foundation, Apache-2.0); a modern edit list with an API | Several tracks, markers, metadata; converting to other formats | Format adapters other than native `.otio` now live in a separate plug-ins package |
| EDL (CMX 3600) | Plain-text edit decision list from the tape era | The widest import support; one video track and simple audio | Reel names are short, one video track per file, no effects or titles |

## Which editor imports what

| Editor | FCPXML | OTIO | EDL | Notes |
|---|---|---|---|---|
| DaVinci Resolve | Yes, in recent versions | Yes, in recent versions | Yes | Check the import menu of the user's version |
| Final Cut Pro | Yes (native format) | No native import known; check | No native import known; check | FCPXML is the path |
| Premiere Pro | No native FCPXML import known; check | Check the current version | Yes | Premiere also reads the older Final Cut Pro 7 XML (a different format); use EDL unless you have tested otherwise |

If unsure, send EDL plus OTIO: one of them will import nearly anywhere, and the plain edit list covers the rest.

## The hand-over folder

```
handover-example-reel/
  README.txt          what is here, frame rate, resolution, how to import
  timeline/
    example-reel.fcpxml
    example-reel.otio
    example-reel.edl
  clips/              original media, unchanged names
  music/              tracks plus licence notes
  captions/
    example-reel.srt
  edit-list.txt       plain list of cuts with timecodes
```

- Keep the original clip file names; the timeline refers to them.
- Use relative or clearly documented paths. Tell the user they may need to relink media after import.
- Put the licence or source for every music, stock or generated file in `music/` or `README.txt`.
- Keep the folder out of Git. Commit only the timeline files, `edit-list.txt`, `README.txt` and any script that wrote them.

### Plain edit list

The fallback for any editor, and a way for the user to check the cut by reading:

```
Example reel, 30 fps, 1080x1920, total 00:00:05:00

#   record in    record out   clip                 source in    source out   note
1   00:00:00:00  00:00:03:00  interview_a.mov      00:00:02:00  00:00:05:00  hook line
2   00:00:03:00  00:00:05:00  broll_shop.mov       00:00:10:00  00:00:12:00  covers jump cut
```

### Captions (`.srt`)

```
1
00:00:00,000 --> 00:00:01,800
We bake every loaf before sunrise.

2
00:00:01,800 --> 00:00:03,000
Here is why.
```

## Minimal examples

All clip names are fictional. Each file below is small enough to write by hand or with a short Python script using only the standard library (`json`, `xml.etree.ElementTree`, plain string formatting). Test-import each one before relying on it.

### EDL (CMX 3600)

```
TITLE: EXAMPLE REEL
FCM: NON-DROP FRAME

001  INTERVA  V     C        00:00:02:00 00:00:05:00 00:00:00:00 00:00:03:00
* FROM CLIP NAME: interview_a.mov
002  BROLLSH  V     C        00:00:10:00 00:00:12:00 00:00:03:00 00:00:05:00
* FROM CLIP NAME: broll_shop.mov
```

Columns: event number, reel name (short, letters and digits), track (`V` video, `A` audio), transition (`C` cut), source in, source out, record in, record out.

### OTIO

```json
{
  "OTIO_SCHEMA": "Timeline.1",
  "name": "Example reel",
  "tracks": {
    "OTIO_SCHEMA": "Stack.1",
    "name": "tracks",
    "children": [
      {
        "OTIO_SCHEMA": "Track.1",
        "name": "V1",
        "kind": "Video",
        "children": [
          {
            "OTIO_SCHEMA": "Clip.1",
            "name": "interview_a",
            "source_range": {
              "OTIO_SCHEMA": "TimeRange.1",
              "start_time": {"OTIO_SCHEMA": "RationalTime.1", "rate": 30.0, "value": 60.0},
              "duration": {"OTIO_SCHEMA": "RationalTime.1", "rate": 30.0, "value": 90.0}
            },
            "media_reference": {
              "OTIO_SCHEMA": "ExternalReference.1",
              "target_url": "clips/interview_a.mov"
            }
          }
        ]
      }
    ]
  }
}
```

Times are frames at a rate: value 60 at 30 fps is two seconds. Add a second clip to `children` for each cut; add another `Track.1` with `"kind": "Audio"` for music.

### FCPXML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.9">
  <resources>
    <format id="r1" frameDuration="1/30s" width="1080" height="1920"/>
    <asset id="r2" name="interview_a" start="0s" duration="600/30s"
           hasVideo="1" hasAudio="1" format="r1">
      <media-rep kind="original-media" src="file:///path/to/clips/interview_a.mov"/>
    </asset>
  </resources>
  <library>
    <event name="Example">
      <project name="Example reel">
        <sequence format="r1" duration="90/30s" tcStart="0s" tcFormat="NDF">
          <spine>
            <asset-clip ref="r2" name="interview_a" offset="0s"
                        start="60/30s" duration="90/30s"/>
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
```

`offset` is where the clip sits on the timeline, `start` is the source in point, `duration` is the length; all are rational seconds. The `src` must be an absolute file URL on the user's computer, so ask for the path or tell them to relink. Use the FCPXML version their editor documents.

### Writing timecode in Python

```python
def tc(frames, fps=30):
    s, f = divmod(frames, fps)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"
```

This is for whole-number frame rates. For 29.97 or 59.94 drop-frame timecode, do not hand-roll it: use whole-frame rates or ask the user to export from their editor.

## Common problems

| Problem | Likely cause | Fix |
|---|---|---|
| Import rejected | Wrong format version or a syntax slip | Validate the XML or JSON; try a lower FCPXML version; test with a one-clip file |
| Media offline after import | Paths differ on the user's computer | Relink to the `clips/` folder |
| Cuts land a frame or two off | Frame rate mismatch between file, clips and timeline | Use one frame rate everywhere and state it in `README.txt` |
| Vertical video imports as landscape | Timeline resolution not set | Set width and height in the file, or set the timeline to 1080x1920 before import |
| Audio missing | EDL lists only video events | Add audio events, or send OTIO with an audio track |
