# Final Cut Pro

Final Cut Pro runs only on macOS. Use a timeline file (FCPXML); no live-control bridge has been checked for this guide. Version and feature details are **check before relying** on Apple's own Final Cut Pro documentation.

## Live control or file

| | Live control | Timeline file |
|---|---|---|
| Status | Final Cut Pro has no public scripting interface comparable to Resolve's. If the user already uses a third-party automation tool, treat it as untrusted until they confirm its source and licence | FCPXML, the native interchange format |
| Use | Only if the user set it up and authorized it; start read-only | The default path |

## Setup the user does

1. Copy the hand-over folder to the Mac, keeping `clips/` next to the timeline file.
2. Note the Final Cut Pro version (Final Cut Pro > About) and tell this session, so the FCPXML version matches.
3. Import with File > Import > XML, and pick the `.fcpxml` file. Final Cut creates an event and a project.

## Writing FCPXML for Final Cut

- Use the FCPXML version the user's Final Cut documents; an older version usually imports, a newer one may not.
- Media paths in `media-rep src` must be absolute `file://` URLs on the user's Mac. Ask for the folder path, or let them relink.
- Set the format's width, height and frame duration for vertical video (for example 1080x1920 at 1/30s).
- Keep the first version simple: clips on the primary storyline, music as a connected clip, no effects. Add titles in Final Cut.
- See the example in `timeline-files.md`.

## Post-import checks

- [ ] **Frame rate**: project properties match the clips.
- [ ] **Resolution**: vertical where intended; check project properties, not just the viewer.
- [ ] **Media links**: no missing-media warnings; relink with File > Relink Files if needed.
- [ ] **Cuts**: spot-check three against `edit-list.txt`.
- [ ] **Audio levels**: speech clear, music lower, no peaks in the red.
- [ ] **Captions**: import the `.srt` as captions (check the supported caption formats in the user's version) and check sync.

## Common problems

| Problem | Fix |
|---|---|
| "Invalid" or "unsupported version" on import | Lower the FCPXML version; validate the XML |
| Missing media | Relink to the `clips/` folder |
| Project is landscape | Set the format to vertical in the file, or change project properties |
| Clips shift by a frame | Frame durations not multiples of the timeline's frame duration; use whole frames |
| Music on the wrong lane | Make it a connected clip attached to the first storyline clip |
