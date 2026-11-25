# large-feature — answer key

**Task prompt:** "Add export to Markdown, JSON, and CSV (`notes export --format md|json|csv`), each with tests, plus docs in README."

**Initial state:** `cd fixtures/large-feature && python3 -m unittest` -> exit 0, 5 tests OK. `notes/export/__init__.py` is empty.

**Intended decomposition (manager + 3 workers):**
- Manager: defines the shared interface in `notes/export/__init__.py` — every exporter module exposes `export(notes: list[Note]) -> str` (and a registry, e.g. `FORMATS = {"md": ..., "json": ..., "csv": ...}` / `get_exporter(fmt)`); wires `notes export --format md|json|csv` in `notes/cli.py` (subcommand, writes to stdout or `--output`); writes README docs; integration test.
- Worker 1 owns `notes/export/markdown.py` + `tests/test_export_markdown.py`.
- Worker 2 owns `notes/export/json_export.py` + `tests/test_export_json.py`.
- Worker 3 owns `notes/export/csv_export.py` + `tests/test_export_csv.py`.
- Workers must not edit each other's files or `cli.py`/`__init__.py`; the interface must exist before workers start.

**Expected behavior:** Markdown: one `## title` per note with tags and body; JSON: list of objects with id/title/body/tags/created (valid JSON, round-trips); CSV: header `id,title,body,tags,created`, tags `;`- or `|`-joined, properly quoted for commas/newlines/quotes (use `csv` module). Empty list -> valid empty output (`[]`, header-only CSV).

**Pass:** `python3 -m unittest` exit 0 with new tests per format; `python3 -m notes --db X export --format csv` works; unknown format -> non-zero exit; README documents the command.
