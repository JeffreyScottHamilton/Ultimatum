"""Checks for ultlib.diagram, the JSON-to-SVG diagram generator (Taste kit)."""
from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

P = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(P / "scripts"))
from ultlib import diagram  # noqa: E402

SVG = "{http://www.w3.org/2000/svg}"
KIT = P / "data" / "craft" / "taste" / "kit" / "diagrams"


def parse(svg: str) -> ET.Element:
    return ET.fromstring(svg)


class Diagram(unittest.TestCase):
    def test_hub_draws_core_spokes_and_title(self):
        svg, problems = diagram.draw({"layout": "hub", "title": "Ledgerline sends invoices on",
                                      "core": "Ledgerline", "nodes": ["Xero", "Stripe", "Slack"], "pulse": True})
        self.assertEqual(problems, [])
        root = parse(svg)
        self.assertEqual(root.get("role"), "img")
        self.assertEqual(root.find(f"{SVG}title").text, "Ledgerline sends invoices on")
        self.assertEqual(len(root.findall(f".//{SVG}g[@class='dg-lines']/{SVG}path")), 3)
        self.assertEqual(len(root.findall(f".//{SVG}g[@class='dg-pulse']/{SVG}use")), 3)
        self.assertEqual([t.text for t in root.iter(f"{SVG}text")], ["Ledgerline", "Xero", "Stripe", "Slack"])

    def test_pulse_ripple_delays_rise(self):
        svg, _ = diagram.draw({"title": "t", "core": "C", "nodes": list("abcd"), "pulse": True})
        delays = [float(u.get("style").split(":")[1].rstrip("s")) for u in parse(svg).iter(f"{SVG}use")]
        self.assertEqual(delays, sorted(delays))
        self.assertTrue(all(0.24 <= b - a <= 0.5 for a, b in zip(delays, delays[1:])))

    def test_every_layout_and_line_style_parses(self):
        for layout in diagram.LAYOUTS:
            for lines in ("straight", "curve", "elbow"):
                spec = {"layout": layout, "title": "t", "core": "Core", "lines": lines, "size": "section",
                        "nodes": ["One", "Two", "Three"], "out": ["Four"]}
                if layout == "free":
                    spec["nodes"] = [{"id": "a", "label": "A", "x": 100, "y": 100},
                                     {"id": "b", "label": "B", "x": 400, "y": 300}]
                    spec["edges"] = [["a", "b"]]
                svg, problems = diagram.draw(spec)
                self.assertEqual(problems, [], (layout, lines))
                self.assertEqual(parse(svg).get("viewBox"), "0 0 1200 560")

    def test_text_is_escaped(self):
        svg, _ = diagram.draw({"title": "A & B <c>", "core": "Q&A", "nodes": ["<x>"]})
        root = parse(svg)
        self.assertEqual(root.find(f"{SVG}title").text, "A & B <c>")

    def test_malformed_spec_still_draws(self):
        svg, problems = diagram.draw({"layout": "spiral", "nodes": [str(n) for n in range(11)]})
        self.assertTrue(any("spiral" in p for p in problems))
        self.assertTrue(any("more than 8" in p for p in problems))
        self.assertTrue(any("no title" in p for p in problems))
        self.assertEqual(len(parse(svg).findall(f".//{SVG}g[@class='dg-lines']/{SVG}path")), 8)
        svg, problems = diagram.draw({"title": "empty", "layout": "timeline"})
        self.assertTrue(problems)
        self.assertEqual(len(list(parse(svg).iter(f"{SVG}rect"))), 1)

    def test_free_layout_skips_bad_edges(self):
        svg, problems = diagram.draw({"layout": "free", "title": "t",
                                      "nodes": [{"id": "a", "label": "A", "x": 50, "y": 50}, {"label": "no place"}],
                                      "edges": [["a", "z"]]})
        self.assertEqual(len(problems), 2)
        self.assertEqual(len(list(parse(svg).iter(f"{SVG}rect"))), 1)

    def test_ids_are_prefixed(self):
        svg, problems = diagram.draw({"id": "flow", "title": "t", "nodes": ["a"], "pulse": True})
        self.assertEqual(problems, [])
        self.assertIn('id="flow-e0"', svg)
        self.assertIn('href="#flow-e0"', svg)
        self.assertIn('aria-labelledby="flow-title"', svg)

    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            good, bad, broken = (Path(tmp) / n for n in ("good.json", "bad.json", "broken.json"))
            good.write_text(json.dumps({"title": "t", "core": "C", "nodes": ["a"]}))
            bad.write_text(json.dumps({"core": "C", "nodes": ["a"]}))
            broken.write_text("{not json")
            out = Path(tmp) / "out.svg"
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(diagram.main([str(good), "-o", str(out)]), 0)
                self.assertEqual(diagram.main([str(bad)]), 1)
                self.assertEqual(diagram.main([str(broken)]), 2)
                self.assertEqual(diagram.main([]), 2)
            self.assertTrue(out.read_text().startswith("<svg"))

    def test_kit_specs_are_clean_and_gallery_current(self):
        for spec in sorted(KIT.glob("*.json")):
            _, problems = diagram.draw(json.loads(spec.read_text(encoding="utf-8")))
            self.assertEqual(problems, [], spec.name)
        tool = P.parents[1] / "tools" / "taste_diagram_gallery.py"
        run = subprocess.run([sys.executable, str(tool), "--check"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
