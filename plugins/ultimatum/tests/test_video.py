"""ult video: style recipes, edit checks, path boundary, captions, and a real ffmpeg render when available."""
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

from _harness import SCRIPTS, UltCase

sys.path.insert(0, SCRIPTS)
from ultlib import video  # noqa: E402

HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
BUILT_IN = {"talking-head", "kinetic-text", "story-film", "meme-cuts"}


def make_clip(path: Path, colour="red", seconds=4, tone=True):
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c={colour}:s=320x180:r=30:d={seconds}"]
    if tone:
        cmd += ["-f", "lavfi", "-i", f"sine=f=330:d={seconds}", "-shortest"]
    subprocess.run(cmd + [str(path)], check=True, timeout=60)


class VideoCase(UltCase):
    def edit(self, **over):
        e = {"style": "talking-head", "platform": "tiktok", "size": [1080, 1920], "fps": 30,
             "shots": [{"card": "Stop doing this", "bg": "#111111", "dur": 1.0},
                       {"src": "clips/a.mp4", "in": 0, "out": 2.0, "tags": ["hook"]},
                       {"src": "clips/b.mp4", "in": 0.5, "out": 2.5},
                       {"src": "clips/a.mp4", "in": 2.0, "out": 3.5}],
             "captions": {"words": [{"w": w, "start": 1.0 + i * 0.3, "end": 1.25 + i * 0.3}
                                    for i, w in enumerate("this one habit wastes your whole morning".split())]}}
        e.update(over)
        self.write("edit.json", json.dumps(e))
        return e

    def touch_clips(self):
        for n in ("a", "b"):
            p = self.root / "clips" / f"{n}.mp4"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"")


class TestRecipes(VideoCase):
    def test_built_in_styles_load_and_validate(self):
        styles = video.load_styles(self.root)
        self.assertTrue(BUILT_IN <= set(styles))
        for s in styles.values():
            self.assertEqual(video.recipe_problems(s), [], s["id"])

    def test_styles_command_lists_and_shows(self):
        r = self.ult("video", "styles")
        self.assertEqual(r.code, 0, r.all)
        for sid in BUILT_IN:
            self.assertIn(sid, r.out)
        r = self.ult("video", "styles", "story-film")
        self.assertEqual(json.loads(r.out)["id"], "story-film")
        self.assertEqual(self.ult("video", "styles", "nope").code, 2)

    def test_project_style_overrides_and_bad_one_is_refused(self):
        base = json.loads((video.STYLES_DIR / "meme-cuts.json").read_text())
        base["name"] = "Ours"
        self.write("social/styles/meme-cuts.json", json.dumps(base))
        self.assertEqual(video.load_styles(self.root)["meme-cuts"]["name"], "Ours")
        base["captions"]["color"] = "red"
        self.write("social/styles/meme-cuts.json", json.dumps(base))
        with self.assertRaises(video.EditError):
            video.load_styles(self.root)


class TestCheck(VideoCase):
    def test_short_edit_gets_fixes_not_blockers(self):
        self.edit()
        self.touch_clips()
        r = self.ult("video", "check", "edit.json", "--json")
        self.assertEqual(r.code, 0, r.all)
        texts = " ".join(p["text"] for p in json.loads(r.out)["problems"])
        self.assertIn("works best at 15-60 s", texts)

    def test_missing_file_and_wrong_size_block(self):
        self.edit(size=[1000, 1000])
        r = self.ult("video", "check", "edit.json")
        self.assertEqual(r.code, 1)
        self.assertIn("file not found", r.out)
        self.assertIn("not one tiktok takes", r.out)

    def test_caption_in_button_zone(self):
        self.edit(caption_y=0.93)
        self.touch_clips()
        self.assertIn("under tiktok's buttons", self.ult("video", "check", "edit.json").out)

    def test_story_rules(self):
        shots = [{"card": "x", "dur": 3.0, "tags": ["product"]}] + [{"card": "y", "dur": 3.0}] * 5
        self.edit(style="story-film", shots=shots, captions={"lines": [{"text": "hi", "start": 0, "end": 2}]},
                  music={"src": "m.wav"})
        out = self.ult("video", "check", "edit.json").out
        self.assertIn("hold it until after", out)
        self.assertIn("no held moment", out)
        self.assertIn("no licence", out)

    def test_ai_footage_needs_label(self):
        e = self.edit()
        e["shots"][1]["ai"] = True
        self.write("edit.json", json.dumps(e))
        self.touch_clips()
        self.assertIn("ai_label", self.ult("video", "check", "edit.json").out)

    def test_unknown_style_and_bad_shot(self):
        self.edit(style="nope")
        self.assertEqual(self.ult("video", "check", "edit.json").code, 2)
        self.edit(shots=[{"src": "clips/a.mp4", "in": 2, "out": 1}])
        self.assertIn("out must be after in", self.ult("video", "check", "edit.json").out)


class TestBoundary(VideoCase):
    """Media and outputs stay inside --root: no `..`, absolute paths or symlinks out."""

    def test_parent_path_refused(self):
        self.edit(shots=[{"src": "../outside.mp4", "in": 0, "out": 1}])
        r = self.ult("video", "check", "edit.json")
        self.assertEqual(r.code, 2)
        self.assertIn("outside the project", r.out)

    def test_absolute_path_refused(self):
        self.edit(shots=[{"src": "/etc/passwd", "in": 0, "out": 1}])
        self.assertIn("outside the project", self.ult("video", "check", "edit.json").out)

    def test_symlink_out_refused(self):
        outside = self.tmp.parent / (self.tmp.name + "-outside")
        outside.mkdir()
        self.addCleanup(shutil.rmtree, outside, True)
        os.symlink(outside, self.root / "link")
        self.edit(shots=[{"src": "link/x.mp4", "in": 0, "out": 1}])
        self.assertIn("outside the project", self.ult("video", "check", "edit.json").out)

    def test_music_lut_and_whisper_paths_checked(self):
        for extra in ({"music": {"src": "../m.wav"}}, {"lut": "../x.cube"},
                      {"captions": {"whisper": "../w.json"}}, {"sfx": [{"src": "/tmp/s.wav"}]}):
            self.edit(**extra)
            self.assertIn("outside the project", self.ult("video", "check", "edit.json").out, extra)

    def test_render_output_outside_root_refused(self):
        self.edit()
        self.touch_clips()
        r = self.ult("video", "render", "edit.json", "--out", "../x.mp4")
        self.assertEqual(r.code, 2)
        self.assertIn("write inside the project", r.out)


class TestCaptions(VideoCase):
    def test_ass_text_cannot_inject_tags(self):
        self.assertEqual(video._ass_text("a{\\pos(0,0)}b\nc"), "a(/pos(0,0))b c")

    def test_colour_and_time(self):
        self.assertEqual(video._ass_colour("#FFD400"), "&H0000D4FF")
        self.assertEqual(video._ts(61.234), "0:01:01.23")

    def test_build_ass_word_highlight_and_cards(self):
        self.edit()
        self.touch_clips()
        ed = video.load_edit(self.root / "edit.json", self.root)
        ass = ed and video.build_ass(ed)
        self.assertIn("STOP DOING THIS", ass)
        hi = video._ass_colour(ed["style"]["captions"]["highlight"])
        self.assertIn("\\c" + hi, ass)
        self.assertEqual(ass.count("Style: Cap,"), 1)

    def test_whisper_words_and_source_mapping(self):
        self.write("w.json", json.dumps({"segments": [{"words": [
            {"word": " hello", "start": 0.1, "end": 0.4}, {"word": " gone", "start": 1.0, "end": 1.3},
            {"word": " world", "start": 2.1, "end": 2.4}]}]}))
        self.assertEqual([w["w"] for w in video.read_words(self.root / "w.json")], ["hello", "gone", "world"])
        self.edit(shots=[{"src": "clips/a.mp4", "in": 0, "out": 0.6}, {"src": "clips/a.mp4", "in": 2.0, "out": 2.6}],
                  captions={"whisper": "w.json", "source": "clips/a.mp4"})
        self.touch_clips()
        ed = video.load_edit(self.root / "edit.json", self.root)
        self.assertEqual([w["w"] for w in ed["words"]], ["hello", "world"])
        self.assertAlmostEqual(ed["words"][1]["start"], 0.7, places=3)

    def test_jumpcuts(self):
        words = [{"w": "a", "start": 0.5, "end": 0.8}, {"w": "b", "start": 0.9, "end": 1.2},
                 {"w": "c", "start": 3.0, "end": 3.4}]
        self.assertEqual(video.jumpcuts(words, 0.35, 0.1), [(0.4, 1.3), (2.9, 3.5)])

    def test_jumpcuts_command_writes_paths_relative_to_edit(self):
        self.write("social/media/t.words.json", json.dumps({"words": [
            {"w": "a", "start": 0.2, "end": 0.5}, {"w": "b", "start": 2.0, "end": 2.3}]}))
        (self.root / "social/media/t.mp4").write_bytes(b"")
        r = self.ult("video", "jumpcuts", "social/media/t.words.json", "--src", "social/media/t.mp4",
                     "--out", "social/edit.json")
        self.assertEqual(r.code, 0, r.all)
        e = json.loads((self.root / "social/edit.json").read_text())
        self.assertEqual(e["shots"][0]["src"], "media/t.mp4")
        self.assertEqual(len(e["shots"]), 2)
        ed = video.load_edit(self.root / "social/edit.json", self.root)
        self.assertEqual([w["w"] for w in ed["words"]], ["a", "b"])


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg not installed")
class TestRender(VideoCase):
    def setUp(self):
        super().setUp()
        make_clip(self.root / "clips" / "a.mp4", "red")
        make_clip(self.root / "clips" / "b.mp4", "blue", tone=False)
        self.edit()

    def test_render_feel_and_measure(self):
        r = self.ult("video", "render", "edit.json", "--out", "out/x.mp4", timeout=300)
        self.assertEqual(r.code, 0, r.all)
        out = self.root / "out" / "x.mp4"
        info = video.probe(out)
        self.assertEqual((info["width"], info["height"]), (1080, 1920))
        self.assertAlmostEqual(info["duration"], 6.5, delta=0.2)
        r = self.ult("video", "feel", "out/x.mp4", "--edit", "edit.json", "--frames", "out/frames", "--json",
                     timeout=300)
        rep = json.loads(r.out)
        self.assertLessEqual(abs(rep["measured"]["lufs"] + 14), 1.5, rep["measured"])
        self.assertEqual(len(rep["frames"]), 5)
        self.assertTrue(all(Path(f).is_file() for f in rep["frames"]))
        self.assertGreaterEqual(rep["measured"]["shots"], 3)
        r = self.ult("video", "measure", "out/x.mp4", "--recipe-out", "social/styles/mine.json", "--id", "mine",
                     "--base", "meme-cuts", timeout=300)
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("mine", video.load_styles(self.root))

    def test_sample_two_styles(self):
        r = self.ult("video", "sample", "edit.json", "--styles", "kinetic-text,story-film", "--seconds", "2",
                     timeout=300)
        self.assertEqual(r.code, 0, r.all)
        for sid in ("kinetic-text", "story-film"):
            p = self.root / "social" / "samples" / f"{sid}.mp4"
            self.assertAlmostEqual(video.probe(p)["duration"], 2.0, delta=0.2)
            self.assertTrue((self.root / "social" / "samples" / f"{sid}.png").is_file())


if __name__ == "__main__":
    unittest.main()
