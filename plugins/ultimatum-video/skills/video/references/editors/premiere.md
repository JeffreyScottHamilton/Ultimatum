# Premiere Pro

Live control is possible only through a third-party bridge with the desktop app running; otherwise hand over a timeline file. Version and feature details are **check before relying** on Adobe's own help pages and the bridge project's own repository.

## Live control or file

| | Live control | Timeline file |
|---|---|---|
| Needs | Premiere Pro desktop app running on a computer this session can reach, a UXP or panel plug-in loaded in it, a local proxy or MCP server the user installed and authorized | Any recent Premiere Pro |
| Good for | Iterating on a sequence, reading project state | One hand-over, a cloud session |
| Risk | Changes land in the user's open project | Low: the user imports into a new sequence |

### A bridge you can name

**adb-mcp** (https://github.com/mikechambers/adb-mcp), MIT licence per the repository page, observed 2026-11-25. It connects an MCP server through a local proxy to a UXP plug-in inside Photoshop or Premiere; the page says Premiere support is more limited than Photoshop's, that the app must be running with the plug-in panel connected, and that the project is not endorsed or supported by Adobe. Check before relying: read its README for the Premiere version it needs, and do not install it for the user.

Other community bridges exist; describe the capability to the user rather than recommending one whose licence and repository you have not checked.

## Setup the user does (live control)

1. Open Premiere Pro.
2. Install and load the bridge's plug-in panel, start its local proxy and MCP server, following its README.
3. Add the MCP server to their Claude Code configuration and tell this session it is ready.
4. Start read-only: list the open project's sequences, frame rate and bins.

## Working live

- Build in a new sequence; never edit the user's existing sequences unless asked.
- Ask before exporting, rendering, deleting, or saving over the project file.
- After each change, read the sequence back and compare it with the edit list.

## Import a timeline file

- **EDL**: File > Import, choose the `.edl`; Premiere asks for sequence settings, then creates a sequence with offline clips to relink.
- **Final Cut Pro 7 XML** (an older XML format, not FCPXML) also imports; only send it if you have test-imported one.
- **OTIO**: check whether the user's version imports it before relying on it.

Set the sequence to the agreed resolution and frame rate (vertical 1080x1920 for short-form) before or right after import.

## Post-import checks

- [ ] **Frame rate**: sequence and clips match.
- [ ] **Resolution**: vertical where intended; no scaling surprises (check "scale to frame size" settings).
- [ ] **Media links**: relink offline clips to `clips/`; check the first and last frame of a few clips.
- [ ] **Cuts**: spot-check three against `edit-list.txt`.
- [ ] **Audio levels**: speech clear, music lower, no clipping.
- [ ] **Captions**: `.srt` imported as a caption track and in sync.

## Common problems

| Problem | Fix |
|---|---|
| Bridge panel does not connect | Premiere closed, plug-in not loaded, or proxy not running; use a file |
| EDL imports with audio missing | Add audio events or relink audio separately |
| Clips offline after import | Relink using the hand-over folder; keep original file names |
| Sequence is landscape | Change sequence settings to vertical, then reposition |
| Cuts drift | Frame rate mismatch; use one rate everywhere |
