#!/usr/bin/env python3
"""Build the Taste kit's fragment gallery from its partials.

    python3 tools/taste_ui_gallery.py           # write kit/ui/index.html
    python3 tools/taste_ui_gallery.py --check   # exit 1 if index.html is stale

Every *.html in kit/ui except index.html is a partial: one <figure>. The gallery
shows each at true size under its file name, so they can be screenshotted and
measured at 390 px. Standard library only, no network.
"""
from __future__ import annotations

import sys
from pathlib import Path

UI = Path(__file__).resolve().parents[1] / "plugins/ultimatum/data/craft/taste/kit/ui"

HEAD = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta content="initial-scale=1, width=device-width" name="viewport">
<title>Interface fragments | Taste kit</title>
<link href="../system.css" rel="stylesheet">
<link href="ui.css" rel="stylesheet">
<style>
  .shelf { margin-top: 40px; display: grid; gap: 40px 32px; grid-template-columns: repeat(auto-fill, minmax(min(100%, 440px), 1fr)); }
  .shelf > section { display: grid; gap: 10px; align-content: start; justify-items: start; }
  .shelf h2 { font: 500 var(--fs-label)/1.3 var(--face-text); margin: 0; }
</style>
</head>
<body>
<main class="block g-paper">
<div class="wrap">
<h1>Interface fragments</h1>
<p class="lead">Generated from the partials in this folder by tools/taste_ui_gallery.py. Edit the partials, not this page.</p>
<div class="shelf">
"""
FOOT = """</div>
</div>
</main>
</body>
</html>
"""


def partials() -> list[Path]:
    return sorted(p for p in UI.glob("*.html") if p.name != "index.html")


def build() -> str:
    parts = [HEAD]
    for path in partials():
        body = path.read_text(encoding="utf-8").strip()
        parts.append(f'<section id="{path.stem}">\n<h2>{path.stem}</h2>\n{body}\n</section>\n')
    parts.append(FOOT)
    return "".join(parts)


def main(argv: list[str]) -> int:
    if argv not in ([], ["--check"]):
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    page, target = build(), UI / "index.html"
    if argv:
        fresh = target.is_file() and target.read_text(encoding="utf-8") == page
        print("index.html is current" if fresh else "index.html is stale: run tools/taste_ui_gallery.py")
        return 0 if fresh else 1
    target.write_text(page, encoding="utf-8")
    print(f"wrote {target.relative_to(UI.parents[6])} ({len(partials())} partials)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
