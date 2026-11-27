"""Covers ultlib.posts, ultlib.postspecs and ultlib.postvariants through the CLI."""
import json
import struct
import unittest
import zlib

from _harness import UltCase
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ultlib import route  # noqa: E402



def png(w, h):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    raw = b"".join(b"\x00" + b"\x00" * (w * 3) for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


class TestPostsCheck(UltCase):
    def test_image_size_and_caption(self):
        (self.root / "ok.png").write_bytes(png(1080, 1350))
        (self.root / "wide.png").write_bytes(png(1600, 900))
        r = self.ult("posts", "check", "ok.png", "wide.png", "--platform", "instagram-feed",
                     "--caption", "Hook " + "#t " * 40, "--json")
        self.assertEqual(r.code, 1, r.all)
        texts = [p["text"] for p in json.loads(r.out)["problems"]]
        self.assertFalse(any(t.startswith("ok.png") for t in texts), texts)
        self.assertTrue(any("wide.png: 1600x900 does not match" in t for t in texts), texts)
        self.assertTrue(any("hashtags" in t for t in texts), texts)

    def test_specs_dated(self):
        r = self.ult("posts", "specs", "tiktok")
        self.assertEqual(r.code, 0)
        self.assertIn("check before relying", r.out)


class TestPostsCalendar(UltCase):
    PLAN = [{"date": "2026-12-01", "time": "18:30", "channel": "instagram", "format": "carousel",
             "hook_type": "mistake", "caption": "Three, mistakes; really"},
            {"date": "2026-12-01", "channel": "tiktok", "format": "short"}]

    def test_ics_and_csv(self):
        self.write("plan.json", json.dumps({"posts": self.PLAN}))
        r = self.ult("posts", "calendar", "plan.json", "--to", "ics", "--out", "cal.ics")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("nothing is scheduled or posted", r.out)
        self.assertIn("more than one post on 2026-12-01", r.out)
        self.assertIn("1 posts have no hook_type", r.out)
        ics = (self.root / "cal.ics").read_bytes().decode()
        self.assertEqual(ics.count("BEGIN:VEVENT"), 2)
        self.assertIn("DTSTART:20261201T090000", ics)
        self.assertIn(r"Three\, mistakes\; really", ics)
        self.assertIn("\r\n", ics)
        self.assertEqual(self.ult("posts", "calendar", "plan.json", "--out", "c.csv").code, 0)
        rows = (self.root / "c.csv").read_text().splitlines()
        self.assertTrue(rows[0].startswith("date,time,channel"))
        self.assertIn("needs approval", rows[1])

    def test_bad_plan(self):
        self.write("plan.json", json.dumps([{"channel": "x"}]))
        self.assertEqual(self.ult("posts", "calendar", "plan.json").code, 2)


class TestPostsPlan(UltCase):
    GOOD = {"date": "2026-12-01", "time": "18:30", "channel": "linkedin", "format": "text",
            "hook_type": "mistake", "caption": "Most bike shops lose winter sales the same way.",
            "link": "https://example.com/?utm_source=linkedin&utm_medium=social&utm_campaign=winter"}

    def plan(self, *posts):
        self.write("plan.json", json.dumps({"posts": list(posts)}))
        return self.ult("posts", "plan", "plan.json", "--json")

    def codes(self, r):
        return {f["code"]: f["kind"] for f in json.loads(r.out)["findings"]}

    def test_clean_plan_passes(self):
        r = self.plan(self.GOOD)
        self.assertEqual(r.code, 0, r.all)
        self.assertEqual(json.loads(r.out)["blockers"], 0)

    def test_sponsored_without_disclosure_blocks(self):
        r = self.plan({**self.GOOD, "sponsored": True})
        self.assertEqual(r.code, 1, r.all)
        self.assertEqual(self.codes(r).get("P11"), "blocker")
        self.assertEqual(self.plan({**self.GOOD, "sponsored": True, "paid_label": True}).code, 0)

    def test_ai_generated_needs_label(self):
        r = self.plan({**self.GOOD, "ai_generated": True})
        self.assertEqual(r.code, 1, r.all)
        self.assertEqual(self.codes(r).get("P12"), "blocker")

    def test_link_without_utm_is_flagged(self):
        r = self.plan({**self.GOOD, "link": "https://example.com/winter"})
        self.assertIn("P05", self.codes(r), r.all)

    def test_image_without_alt_is_flagged(self):
        r = self.plan({**self.GOOD, "channel": "instagram", "format": "carousel",
                       "link": "", "next_step": "link in bio"})
        self.assertIn("P07", self.codes(r), r.all)

    def test_tiktok_caption_over_api_limit(self):
        r = self.plan({**self.GOOD, "channel": "tiktok", "format": "short", "caption": "a" * 2500,
                       "link": "", "next_step": "follow"})
        texts = " ".join(f["text"] for f in json.loads(r.out)["findings"] if f["code"] == "P03")
        self.assertIn("2200", texts, r.all)

    def test_unreadable_plan(self):
        self.write("plan.json", "{not json")
        self.assertEqual(self.ult("posts", "plan", "plan.json").code, 2)

    def test_text_output_says_nothing_was_posted(self):
        self.write("plan.json", json.dumps([self.GOOD]))
        r = self.ult("posts", "plan", "plan.json")
        self.assertIn("nothing was scheduled or posted", r.out)


class TestPostsVariants(UltCase):
    def test_ranks_by_entered_results_only(self):
        self.ult("posts", "variant", "add", "a", "--hook-type", "question", "--text", "Why?")
        self.ult("posts", "variant", "add", "b", "--hook-type", "mistake", "--text", "Stop doing this")
        self.ult("posts", "variant", "add", "c", "--hook-type", "story", "--text", "Last year")
        self.assertEqual(self.ult("posts", "variant", "add", "a", "--hook-type", "x", "--text", "y").code, 1)
        self.assertEqual(self.ult("posts", "variant", "result", "zz", "--views", "1").code, 2)
        self.ult("posts", "variant", "result", "a", "--views", "1000", "--signups", "1")
        self.ult("posts", "variant", "result", "b", "--views", "2000", "--signups", "6")
        r = self.ult("posts", "variant", "next", "--json")
        data = json.loads(r.out)
        self.assertEqual([g["hook_type"] for g in data["ranked"]], ["mistake", "question"])
        self.assertEqual(data["ranked"][0]["signups_per_1k"], 3.0)
        self.assertEqual(data["waiting"], ["c"])
        r = self.ult("posts", "variant", "next")
        self.assertIn("treat it as a lead", r.out)


class TestSocialRouting(unittest.TestCase):
    def test_social_tasks_route_to_the_skill(self):
        for task in ("plan a month of Instagram posts for the bike shop", "write TikTok captions for the launch",
                     "make a LinkedIn content calendar", "suggest hashtags for these reels",
                     "write three hook variants for a short-form video"):
            with self.subTest(task=task):
                self.assertEqual(route.decide(task, root=None)["workflow"], "social-media")

    def test_site_and_app_tasks_do_not(self):
        for task in ("add social media icons to the footer", "fix the og image social card",
                     "add a homepage carousel", "fix the failing date parser test",
                     "submit my Expo app to the App Store"):
            with self.subTest(task=task):
                self.assertNotEqual(route.decide(task, root=None)["workflow"], "social-media")

    def test_security_review_keeps_its_route(self):
        task = "security review of the social login and the social posts scheduler"
        self.assertEqual(route.workflow_for(task, "sec-review", None), "default")


class TestSocialSkillFiles(unittest.TestCase):
    SKILL = ROOT / "skills" / "social-media"

    def test_frontmatter_and_router(self):
        self.assertTrue((self.SKILL / "SKILL.md").read_text().startswith("---\nname: social-media\n"))
        self.assertIn("social-media", (ROOT / "skills" / "work" / "SKILL.md").read_text())

    def test_every_plan_code_is_documented(self):
        src = (ROOT / "scripts" / "ultlib" / "posts.py").read_text()
        doc = (self.SKILL / "references" / "checker.md").read_text()
        for code in sorted(set(re.findall(r'"(P\d{2})"', src))):
            with self.subTest(code=code):
                self.assertIn(code, doc)


if __name__ == "__main__":
    unittest.main()
