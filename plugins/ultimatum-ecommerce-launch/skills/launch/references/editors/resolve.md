# DaVinci Resolve

Two ways in: live control through a scripting bridge, or a timeline file the user imports. Edition, version and feature details here are **check before relying** on Blackmagic Design's own pages and the bridge project's own repository.

## Live control or file

| | Live control | Timeline file |
|---|---|---|
| Needs | Resolve Studio (the paid edition), running on a computer this session can reach, external scripting enabled, an MCP server the user installed and authorized | Any edition |
| Good for | Many small changes, reading project state, building timelines step by step | One hand-over, a cloud session, the free edition |
| Risk | Changes land in the user's live project | Low: the user imports into a new timeline |

Blackmagic limits external scripting to the Studio edition. With the free edition, use a timeline file.

### A bridge you can name

**davinci-resolve-mcp** (https://github.com/samuelgursky/davinci-resolve-mcp), MIT licence per its LICENSE file, observed 2026-11-25. Its README describes controlling Resolve Studio through the official scripting API, with an in-app bridge for the free edition that its authors describe as unsupported in the long run. It is a community project, not a Blackmagic product. Check before relying: read its README and licence for the version the user has, and do not install it for them.

## Setup the user does (live control)

1. Install Resolve Studio and open it.
2. Turn on external scripting in Resolve's preferences (the setting name and location vary by version; check the Resolve manual).
3. Install the MCP server themselves, following its README, and add it to their Claude Code configuration.
4. Tell this session it is ready. Then start read-only: list projects, timelines, frame rate and media pool.

If any of these is missing, use the timeline-file path.

## Working live

- Create a new timeline for each cut; do not edit the user's existing timelines unless they ask.
- Before any render, export, delete or overwrite, show what will happen and wait for a yes.
- After each batch of changes, read the timeline back and compare it with the edit list.

## Import a timeline file

Resolve reads EDL, FCPXML and OTIO in recent versions (check the import menu). The usual route is File > Import > Timeline, then pick the file; Resolve offers to import the source clips into the media pool. Point it at the `clips/` folder of the hand-over.

## Post-import checks

Ask the user to confirm, or confirm through live control:

- [ ] **Frame rate**: timeline and clips match the file. Resolve locks a project's timeline frame rate once media is in it, so set it first.
- [ ] **Resolution**: 1080x1920 (or the agreed size) for vertical; not letterboxed.
- [ ] **Media links**: no clips shown offline; relink to `clips/` if needed.
- [ ] **Cuts**: spot-check three cuts against `edit-list.txt`.
- [ ] **Audio levels**: speech clear, music under it, no clipping on the meters.
- [ ] **Captions**: `.srt` imported onto a subtitle track and in sync.

## Common problems

| Problem | Fix |
|---|---|
| Scripting not reachable | Free edition, Resolve closed, or external scripting off; use a file |
| Timeline imports at the wrong frame rate | Create the project at the right rate before import |
| Clips offline | Relink to the hand-over folder |
| Vertical timeline shows black bars | Set the timeline resolution to vertical before import |
| Subtitle track empty | Import the `.srt` into the media pool, then drag it to the timeline |
