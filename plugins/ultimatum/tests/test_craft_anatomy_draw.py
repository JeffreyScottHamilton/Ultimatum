"""Checks for the anatomy drawer and turning-group audit, and their guide."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "website" / "references" / "craft" / "anatomy"
DATA = P / "data" / "craft" / "anatomy"
DRAW = DATA / "figure_draw.py"
TURNING = DATA / "examples" / "turning-scene.json"
CLEAN = DATA / "examples" / "clean-scene.json"
NS = "{http://www.w3.org/2000/svg}"


def run(*args):
    return subprocess.run([sys.executable, "-I", str(DRAW), *args], capture_output=True, text=True, timeout=120)


def drawn(scene_path, *extra):
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "fig.svg"
        r = run("draw", str(scene_path), "--out", str(out), *extra)
        svg = out.read_text(encoding="utf-8") if out.exists() else ""
    return r, svg


def parts(svg):
    root = ET.fromstring(svg)
    return root, [g for g in root.iter(NS + "g") if g.get("data-part")]


class FigureDraw(unittest.TestCase):
    def test_self_check(self):
        r = run("--self-check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("0 problem(s)", r.stdout)

    def test_draws_valid_accessible_svg(self):
        r, svg = drawn(CLEAN)
        self.assertEqual(r.returncode, 0, r.stderr)
        root, groups = parts(svg)
        self.assertEqual(root.get("role"), "img")
        self.assertTrue(root.find(NS + "title").text)
        self.assertTrue(root.find(NS + "desc").text)
        self.assertEqual([g.get("data-part") for g in groups], ["base", "pump", "tank", "gauge"])
        for g in groups:
            self.assertEqual(len(g), 3, g.get("data-part"))  # a box shows three faces
        self.assertEqual(len([g for g in root.iter(NS + "g") if g.get("data-pipe")]), 2)

    def test_four_tones_per_part(self):
        _, svg = drawn(CLEAN)
        _, groups = parts(svg)
        for g in groups:
            fills = {poly.get("fill") for poly in g}
            strokes = {poly.get("stroke") for poly in g}
            self.assertEqual(len(fills), 3, g.get("data-part"))
            self.assertEqual(len(strokes), 1)
            self.assertNotIn(strokes.pop(), fills)

    def test_camera_and_pose_change_the_drawing(self):
        _, front = drawn(TURNING)
        _, back = drawn(TURNING, "--az", "225")
        _, open_lid = drawn(TURNING, "--pose", "lid-hinge=60")
        self.assertNotEqual(front, back)
        self.assertNotEqual(front, open_lid)
        _, groups = parts(open_lid)
        self.assertIn("lid", [g.get("data-part") for g in groups])
        labels = [g for g in ET.fromstring(front).iter(NS + "g") if g.get("data-label")]
        self.assertEqual(len(labels), 3)

    def test_bad_arguments_exit_2(self):
        for args in (["draw", str(TURNING), "--out", "x.svg", "--pose", "nope=3"],
                     ["draw", str(TURNING), "--out", "x.svg", "--pose", "lid-hinge=wide"],
                     ["draw", str(TURNING), "--out", "x.svg", "--el", "90"],
                     ["turn", str(TURNING), "--steps", "1"],
                     ["turn", "missing.json"], []):
            with self.subTest(args=args):
                self.assertEqual(run(*args).returncode, 2)

    def test_bad_group_is_rejected(self):
        scene = json.loads(TURNING.read_text(encoding="utf-8"))
        for change in ({"kind": "spin"}, {"axis": [0, 0, 0]}, {"parts": ["ghost"]}, {"range": [5, 1]}):
            bad = json.loads(json.dumps(scene))
            bad["groups"][0].update(change)
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                f = Path(d) / "s.json"
                f.write_text(json.dumps(bad), encoding="utf-8")
                r = run("turn", str(f))
                self.assertEqual(r.returncode, 2)
                self.assertIn("bad scene", r.stderr)


class TurnAudit(unittest.TestCase):
    def audit(self, path, *extra):
        r = run("turn", str(path), "--json", *extra)
        return r.returncode, json.loads(r.stdout)

    def test_example_faults_are_found(self):
        code, out = self.audit(TURNING)
        self.assertEqual(code, 1)
        found = {(f["check"], f["what"]) for f in out["faults"]}
        self.assertIn(("collision", "lid / post"), found)
        self.assertIn(("tether", "lead"), found)
        self.assertEqual(set(out["counts"]), {"collision", "crowding", "order-cycle", "tether", "fixed-in-group"})

    def test_fixed_scene_is_clean(self):
        scene = json.loads(TURNING.read_text(encoding="utf-8"))
        scene["parts"][3]["at"] = [2.5, -3.5, 0]  # move the post out of the lid's swing
        scene["groups"][0]["range"] = [0, 40]
        scene["pipes"][0]["flex"] = True  # the lead becomes a hose with slack
        scene["pipes"][0]["points"] = [[6, 2, 1.5], [6.6, 2, 3], [7.6, 2.6, 2], [7, 2.3, 0.4]]
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "s.json"
            f.write_text(json.dumps(scene), encoding="utf-8")
            code, out = self.audit(f, "--orbit", "--steps", "12")
        self.assertEqual(code, 0, out)

    def test_static_scene_has_nothing_to_turn(self):
        code, out = self.audit(CLEAN)
        self.assertEqual(code, 0)
        self.assertEqual(sum(out["counts"].values()), 0)

    def test_scene_still_passes_the_static_audit_shape(self):
        r = subprocess.run([sys.executable, "-I", str(DATA / "figure_audit.py"), str(TURNING), "--only",
                            "seats,loose-ends,terminals"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)


class DrawGuide(unittest.TestCase):
    def test_guide_lists_every_turn_check(self):
        guide = (CRAFT / "draw.md").read_text(encoding="utf-8")
        in_guide = set(re.findall(r"^\| `([a-z-]+)` \|", guide, re.M))
        listed = {line.split(":")[0] for line in run("checks").stdout.splitlines()}
        self.assertEqual(in_guide, listed)

    def test_guide_commands_name_real_files(self):
        guide = (CRAFT / "draw.md").read_text(encoding="utf-8")
        for name in re.findall(r"examples/([a-z-]+\.json)", guide):
            self.assertTrue((DATA / "examples" / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
