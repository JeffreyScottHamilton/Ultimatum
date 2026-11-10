# notes

A tiny command-line notes app. Notes are stored in a JSON file
(`~/.notes.json`, override with `--db PATH` or `$NOTES_DB`).

    python3 -m notes add "Buy milk" --tags errands,home
    python3 -m notes list
    python3 -m notes show 1
    python3 -m notes search milk

Layout:

- `notes/store.py` Note dataclass and JSON-backed store
- `notes/render.py` plain-text rendering used by `list` and `show`
- `notes/search.py` case-insensitive search
- `notes/cli.py` argparse entry point
- `notes/export/` reserved package for exporters

Run tests: `python3 -m unittest`
