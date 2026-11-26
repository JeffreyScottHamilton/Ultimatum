#!/usr/bin/env python3
"""Write the Taste kit's diagram demo page from the JSON specs beside it.

    python3 tools/taste_diagram_gallery.py [--check]

Each kit/diagrams/*.json spec is drawn with ultlib.diagram and inlined into
kit/diagrams/index.html inside a card. --check exits 1 when the page is stale.
Exit 2 on a spec the generator reports a problem with. Standard library only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "ultimatum"
sys.path.insert(0, str(PLUGIN / "scripts"))
from ultlib.diagram import draw  # noqa: E402

FOLDER = PLUGIN / "data" / "craft" / "taste" / "kit" / "diagrams"
NAMES = {"hub": "Spokes from one centre", "bowtie": "Bow-tie with curves",
         "timeline": "Timeline, still", "free": "Free layout with elbows"}


def page() -> str:
    cards = []
    for spec_path in sorted(FOLDER.glob("*.json")):
        svg, problems = draw(json.loads(spec_path.read_text(encoding="utf-8")))
        if problems:
            raise ValueError(f"{spec_path.name}: {'; '.join(problems)}")
        name = NAMES.get(spec_path.stem, spec_path.stem)
        cards.append(f'    <figure class="dg-card tile" tabindex="0">\n      <h2>{name}</h2>\n'
                     f'      <p><code>{spec_path.name}</code></p>\n      {svg.strip()}\n    </figure>')
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>Diagrams | Taste kit</title>
<meta content="initial-scale=1, width=device-width" name="viewport">
<link href="../system.css" rel="stylesheet">
<link href="diagram.css" rel="stylesheet">
<style>
  .boards {{ display: flex; flex-wrap: wrap; gap: 24px; }}
  .boards > * {{ flex: 1 1 480px; min-inline-size: 0; }}
  .dg-card {{ margin: 0; }}
  .dg-card h2 {{ font-size: 20px; margin: 0; }}
  .dg-card p {{ margin: 4px 0 16px; }}
</style>
</head>
<body>
<!-- Written by tools/taste_diagram_gallery.py from the *.json specs here. Do not edit by hand. -->
<main class="block">
  <div class="wrap">
    <header class="intro">
      <h1>Diagrams</h1>
      <p>Each card is drawn by <code>ult diagram</code> from the spec named under its title. Hover or tab into a card to run its pulse again.</p>
    </header>
    <div class="boards">
{chr(10).join(cards)}
    </div>
  </div>
</main>
<script defer src="diagram.js"></script>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    if argv not in ([], ["--check"]):
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    try:
        text = page()
    except ValueError as err:
        print(f"taste_diagram_gallery: {err}", file=sys.stderr)
        return 2
    target = FOLDER / "index.html"
    if argv:
        current = target.exists() and target.read_text(encoding="utf-8") == text
        print("index.html is current" if current else "index.html is stale: run tools/taste_diagram_gallery.py")
        return 0 if current else 1
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)} ({text.count('dg-card tile')} diagrams)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
