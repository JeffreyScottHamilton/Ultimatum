"""Covers ultlib.posts, ultlib.postspecs, ultlib.postmedia and ultlib.postvariants through the CLI."""
import json
import shutil
import struct
import subprocess
import unittest
import zlib

from _harness import UltCase


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


class TestPostsMedia(UltCase):
    SPEC = {"platform": "instagram-story", "brand": {"name": "A & B"},
            "slides": [{"title": "One <b>", "body": "first"}, {"title": "Two", "body": "second", "alt": "chart"}]}

    def test_slides_html_is_exact_size_and_escaped(self):
        self.write("s.json", json.dumps(self.SPEC))
        r = self.ult("posts", "slides", "s.json", "--out", "sl")
        self.assertEqual(r.code, 0, r.all)
        page = (self.root / "sl" / "slide-01.html").read_text()
        self.assertIn("width:1080px;height:1920px", page)
        self.assertIn("One &lt;b&gt;", page)
        self.assertIn("A &amp; B", page)
        self.assertIn("slide 2: chart", (self.root / "sl" / "alt-text.txt").read_text())
        if shutil.which("node"):
            self.assertEqual(subprocess.run(["node", "--check", str(self.root / "sl" / "render.cjs")]).returncode, 0)

    def test_slides_bad_spec(self):
        self.write("s.json", json.dumps({"platform": "myspace", "slides": [{}]}))
        self.assertEqual(self.ult("posts", "slides", "s.json").code, 2)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg")
    def test_captions_from_script_burn_in(self):
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=black:s=360x640:d=2",
                        "-f", "lavfi", "-i", "sine=d=2", "-shortest", "-pix_fmt", "yuv420p", str(self.root / "v.mp4")],
                       check=True)
        self.write("script.txt", "one two three\nfour\n")
        r = self.ult("posts", "captions", "v.mp4", "--script", "script.txt", "--platform", "tiktok", "--out", "o.mp4",
                     timeout=300)
        self.assertEqual(r.code, 0, r.all)
        self.assertTrue((self.root / "o.mp4").stat().st_size > 0)
        srt = (self.root / "o-captions" / "captions.srt").read_text()
        self.assertIn("00:00:01,500 --> 00:00:02,000\nfour", srt)
        ass = (self.root / "o-captions" / "captions.ass").read_text()
        self.assertIn("PlayResX: 360", ass)

    def test_transcribe_without_model_says_what_to_do(self):
        if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
            self.skipTest("needs ffmpeg")
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-f", "lavfi", "-i", "color=s=64x64:d=1",
                        str(self.root / "v.mp4")], check=True)
        r = self.ult("posts", "captions", "v.mp4", "--transcribe", "--model", "missing.bin")
        self.assertEqual(r.code, 2)
        self.assertIn("--script", r.out)


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


if __name__ == "__main__":
    unittest.main()
