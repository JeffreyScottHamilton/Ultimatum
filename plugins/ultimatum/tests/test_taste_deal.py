"""Tests for `ult design deal` and the taste presets it deals from."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ultlib import deal as D  # noqa: E402

ULT = ROOT / "scripts" / "ult"
SOURCE = Path(os.environ.get("TASTE_SOURCE", "/tmp/src/taste"))


class Presets(unittest.TestCase):
    def test_every_palette_meets_contrast(self):
        bad = [x for p in D.palettes() for x in D.check_palette(p)]
        self.assertEqual(bad, [])

    def test_palette_fields_and_ids(self):
        ids = [p["id"] for p in D.palettes()]
        self.assertEqual(len(ids), len(set(ids)))
        for p in D.palettes():
            with self.subTest(p=p["id"]):
                self.assertIn(p["mode"], ("light", "dark"))
                self.assertTrue(set(p["kinds"]) <= set(D.KINDS), p["kinds"])
                self.assertTrue(p["trades"] and p["moods"] and p["note"])
                # dark palettes really are dark, light ones light
                self.assertEqual(D.luminance(p["bg"]) < 0.2, p["mode"] == "dark")

    def test_every_kind_has_choice(self):
        for k in D.KINDS:
            with self.subTest(kind=k):
                self.assertGreaterEqual(sum(k in p["kinds"] for p in D.palettes()), 4)
                self.assertGreaterEqual(sum(k in t["kinds"] for t in D.type_presets()), 4)

    def test_type_presets_name_real_pairings(self):
        names = [t["pairing"] for t in D.type_presets()]  # raises if one is missing
        self.assertEqual(len(names), len(set(names)))
        for t in D.type_presets():
            self.assertTrue(t["url"].startswith("https://fonts.googleapis.com/"), t["pairing"])

    def test_contrast_maths(self):
        self.assertAlmostEqual(D.contrast("#000000", "#FFFFFF"), 21.0, places=2)
        self.assertAlmostEqual(D.contrast("#777777", "#FFFFFF"), 4.48, places=2)
        with self.assertRaises(ValueError):
            D.luminance("#12345")

    @unittest.skipUnless((SOURCE / "skills").is_dir(), "source checkout not present (set TASTE_SOURCE)")
    def test_no_upstream_palette_or_hexes(self):
        up = json.loads(next(SOURCE.rglob("library/palettes.json")).read_text(encoding="utf-8"))
        up_ids = {p.get("id") for p in up} | {str(p.get("name", "")).lower() for p in up}
        up_sets = {(p.get("bg", "").upper(), p.get("ink", "").upper(), p.get("accent", "").upper()) for p in up}
        for p in D.palettes():
            self.assertNotIn(p["id"], up_ids)
            self.assertNotIn((p["bg"].upper(), p["ink"].upper(), p["accent"].upper()), up_sets)


class Dealing(unittest.TestCase):
    def test_seed_repeats(self):
        a = D.deal("api monitoring", "software", seed=7)
        b = D.deal("api monitoring", "software", seed=7)
        self.assertEqual(a, b)

    def test_brief_words_steer_the_palette(self):
        seen = {D.deal("bakery pizzeria deli", "place", seed=s)["palette"] for s in range(20)}
        self.assertIn("crust", seen)
        self.assertTrue(seen <= {"crust", "orchard", "terracotta-noon", "rosemary", "espresso"}, seen)

    def test_history_keeps_consecutive_pages_apart(self):
        hist: list[dict] = []
        prev = None
        for s in range(12):
            d = D.deal("dev tools api", "software", seed=s, history=hist)
            if prev:
                for part in ("palette", "type", "hero", "nav"):
                    self.assertNotEqual(d[part], prev[part], (s, part))
            hist.append({k: d[k] for k in ("kind", "palette", "type", "hero", "nav", "footer", "close",
                                           "rhythm", "buttons", "radius")})
            prev = d

    def test_grounds_never_clash(self):
        clashes = {g["name"]: g["clashes"] for g in D.grounds()}
        for s in range(60):
            d = D.deal("", "software", seed=s)
            a, b = (g["name"] for g in d["grounds"])
            self.assertNotEqual(a, b)
            self.assertNotIn(b, clashes[a])
            self.assertNotIn(a, clashes[b])
            self.assertNotIn(a, D.PAGE_GROUNDS)

    def test_calm_kinds_get_no_named_grounds(self):
        for k in ("service", "place", "product"):
            self.assertEqual(D.deal("", k, seed=1)["grounds"], [])

    def test_no_photos_swaps_photo_parts(self):
        for s in range(40):
            d = D.deal("", "place", seed=s, photos=False)
            self.assertNotEqual(d["nav"], "cards")
            self.assertNotEqual(d["close"], "photo")
            d = D.deal("", "service", seed=s, photos=False)
            self.assertNotEqual(d["hero"], "photo")

    def test_film_hero_only_with_footage(self):
        heroes = {D.deal("", "game", seed=s)["hero"] for s in range(30)}
        self.assertNotIn("film", heroes)
        heroes = {D.deal("", "game", seed=s, footage=True)["hero"] for s in range(30)}
        self.assertIn("film", heroes)

    def test_kind_guess(self):
        self.assertEqual(D.guess_kind("an indie rpg on steam"), "game")
        self.assertEqual(D.guess_kind("a coffee bar in Leeds"), "place")
        self.assertEqual(D.guess_kind("a plumber in Leeds"), "service")
        self.assertEqual(D.guess_kind("crm for plumbers"), "software")  # the product, not its users
        self.assertEqual(D.guess_kind("something new"), "software")

    def test_css_tokens(self):
        text = D.css(D.deal("", "software", seed=3))
        for tok in ("--bg:", "--ink:", "--accent:", "--accent-ink:", "--font-display:", "--radius:"):
            self.assertIn(tok, text)


class Cli(unittest.TestCase):
    def run_ult(self, *args, state):
        env = dict(os.environ, ULTIMATUM_STATE_DIR=state)
        return subprocess.run([sys.executable, str(ULT), "design", "deal", *args],
                              capture_output=True, text=True, env=env, timeout=60)

    def test_cli_deal_writes_history_and_css(self):
        with tempfile.TemporaryDirectory() as d:
            css = Path(d) / "out" / "tokens.css"
            p = self.run_ult("a bakery", "--css", str(css), state=d)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("palette", p.stdout)
            self.assertIn("--accent:", css.read_text())
            hist = json.loads((Path(d) / D.HISTORY_FILE).read_text())
            self.assertEqual(hist[-1]["kind"], "place")
            p = self.run_ult("a bakery", "--no-save", "--json", state=d)
            self.assertEqual(json.loads(p.stdout)["kind"], "place")
            self.assertEqual(len(json.loads((Path(d) / D.HISTORY_FILE).read_text())), 1)

    def test_cli_bad_kind(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.run_ult("x", "--kind", "spaceship", state=d)
            self.assertEqual(p.returncode, 2)
            self.assertIn("unknown kind", p.stdout)


if __name__ == "__main__":
    unittest.main()
