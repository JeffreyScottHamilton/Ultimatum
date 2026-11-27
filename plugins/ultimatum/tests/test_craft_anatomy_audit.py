"""Checks for the anatomy figure audit script and its guide."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
CRAFT = P / "skills" / "website" / "references" / "craft" / "anatomy"
DATA = P / "data" / "craft" / "anatomy"
AUDIT = DATA / "figure_audit.py"
CLEAN = DATA / "examples" / "clean-scene.json"
FAULTY = DATA / "examples" / "faulty-scene.json"


def run(*args):
    return subprocess.run([sys.executable, str(AUDIT), *args], capture_output=True, text=True)


def checks():
    return [line.split(":")[0] for line in run("--checks").stdout.splitlines()]


def scene_file(d, scene):
    path = Path(d, "scene.json")
    path.write_text(json.dumps(scene), encoding="utf-8")
    return str(path)


class FigureAudit(unittest.TestCase):
    def test_clean_scene_counts_zero(self):
        r = run(str(CLEAN), "--json")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertTrue(all(v == 0 for v in json.loads(r.stdout)["counts"].values()))

    def test_faulty_scene_trips_every_check(self):
        r = run(str(FAULTY), "--json")
        self.assertEqual(r.returncode, 1)
        counts = json.loads(r.stdout)["counts"]
        self.assertEqual(set(counts), set(checks()))
        self.assertTrue(all(v >= 1 for v in counts.values()), counts)

    def test_verify_table_matches_checks(self):
        text = (CRAFT / "verify.md").read_text(encoding="utf-8")
        self.assertEqual(set(re.findall(r"^\| `([a-z-]+)` \|", text, re.M)), set(checks()))

    def test_guide_script_path_resolves(self):
        text = (CRAFT / "audit.md").read_text(encoding="utf-8")
        m = re.search(r"python3 (\S+figure_audit\.py)", text)
        self.assertEqual((CRAFT / m.group(1)).resolve(), AUDIT.resolve())
        for name in re.findall(r"`[./]*[a-z/]*?([a-z-]+-scene\.json)`", text):
            self.assertTrue((DATA / "examples" / name).is_file(), name)

    def test_pipe_through_named_part_is_allowed(self):
        scene = {"parts": [{"name": "a", "at": [0, 0, 0], "size": [1, 1, 1], "ports": {"o": [1, 0.5, 0.5]}},
                           {"name": "wall", "at": [2, -1, -1], "size": [0.2, 3, 3]},
                           {"name": "b", "at": [4, 0, 0], "size": [1, 1, 1], "ports": {"i": [4, 0.5, 0.5]}}],
                 "pipes": [{"name": "p", "from": "a.o", "to": "b.i", "radius": 0.1,
                            "points": [[1, 0.5, 0.5], [4, 0.5, 0.5]]}]}
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(scene_file(d, scene), "--only", "clearance").returncode, 1)
            scene["pipes"][0]["passes"] = ["wall"]
            self.assertEqual(run(scene_file(d, scene), "--only", "clearance").returncode, 0)

    def test_right_angle_bend_is_not_a_fold(self):
        scene = {"parts": [], "pipes": [{"name": "p", "points": [[0, 0, 0], [1, 0, 0], [1, 1, 0]]}]}
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(scene_file(d, scene), "--only", "folds").returncode, 0)

    def test_bad_input(self):
        self.assertEqual(run().returncode, 2)
        self.assertEqual(run(str(CLEAN), "--only", "nope").returncode, 2)
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(scene_file(d, {"parts": [{"name": "x"}]})).returncode, 2)
            self.assertEqual(run(scene_file(d, {"parts": [{"name": "x", "at": [0, 0, 0], "size": [1, 1, 1]}] * 2})).returncode, 2)
            Path(d, "bad.json").write_text("{", encoding="utf-8")
            self.assertEqual(run(str(Path(d, "bad.json"))).returncode, 2)

    def test_stdlib_only(self):
        text = AUDIT.read_text(encoding="utf-8")
        mods = set(re.findall(r"^(?:import|from) ([a-z_]+)", text, re.M))
        self.assertLessEqual(mods, {"__future__", "argparse", "json", "math", "sys"})


if __name__ == "__main__":
    unittest.main()
