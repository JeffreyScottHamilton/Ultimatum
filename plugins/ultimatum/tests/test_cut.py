"""Creator Cut: silence-based jump cuts (`ult cut`), its routing, and its team guides."""
import json
import shutil
import subprocess
import sys
import unittest

from _harness import LAUNCH_SCRIPTS, REPO, TEAMS, LaunchCase, pick_hooks

sys.path.insert(0, LAUNCH_SCRIPTS)
HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


class Plan(unittest.TestCase):
    def test_silences_become_padded_takes(self):
        from ultlib.cut import keep_segments, parse_silences
        log = ("[silencedetect @ 0x1] silence_start: 1.2\n[silencedetect @ 0x1] silence_end: 2.6 | silence_duration: 1.4\n"
               "[silencedetect @ 0x1] silence_start: 4.2\n")
        sil = parse_silences(log, 5.0)
        self.assertEqual(sil, [(1.2, 2.6), (4.2, 5.0)])
        self.assertEqual(keep_segments(sil, 5.0, pad=0.1), [(0.0, 1.3), (2.5, 4.3)])

    def test_close_takes_merge_and_crumbs_drop(self):
        from ultlib.cut import keep_segments
        self.assertEqual(keep_segments([(1.0, 1.1)], 3.0, pad=0.1), [(0.0, 3.0)])
        self.assertEqual(keep_segments([(0.0, 2.0), (2.1, 4.0)], 4.0, pad=0.0), [])

    def test_check_flags_blockers_and_fixes(self):
        from ultlib.cut import check_plan
        plan = {"duration": 20, "segments": [{"in": 0, "out": 5}, {"in": 4, "out": 14}, {"in": 15, "out": 15.1}]}
        kinds = check_plan(plan, max_s=60)
        text = " ".join(m for _, m in kinds)
        self.assertIn("hook", text)
        self.assertIn("share footage", text)
        self.assertIn("with no cut", text)
        self.assertIn("only 0.10s", text)
        self.assertFalse([k for k, _ in kinds if k == "blocker"])
        self.assertIn("blocker", [k for k, _ in check_plan(plan, max_s=10)])
        self.assertIn("blocker", [k for k, _ in check_plan({"duration": 3, "segments": [{"in": 1, "out": 9}]})])

    def test_graph_punches_every_other_take_and_crops_vertical(self):
        from ultlib.cut import filter_graph
        g = filter_graph({"segments": [{"in": 0, "out": 1}, {"in": 2, "out": 3}]}, vertical=True, punch=1.1)
        v0, v1 = g.split(";")[0], g.split(";")[2]
        self.assertNotIn("crop=iw/1.1", v0)
        self.assertIn("crop=iw/1.1", v1)
        self.assertIn("ih*9/16", v0)
        self.assertIn("scale=1080:1920", v0)
        self.assertTrue(g.endswith("concat=n=2:v=1:a=1[v][a]"))


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg not installed")
class Render(LaunchCase):
    def test_silences_then_vertical_render(self):
        src = self.root / "take.mp4"
        tone = "if(between(t,1.2,2.6)+gt(t,4.2),0,0.5*sin(440*2*PI*t))"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=size=640x360:rate=24:duration=5",
                        "-f", "lavfi", "-i", f"aevalsrc='{tone}':s=44100:d=5", "-shortest", "-c:v", "libx264",
                        "-c:a", "aac", str(src)], check=True, timeout=60)
        r = self.ult("cut", "silences", "take.mp4")
        self.assertEqual(r.code, 0, r.all)
        plan = json.loads((self.root / "cut" / "take.json").read_text())
        self.assertEqual(len(plan["segments"]), 2)
        self.assertEqual(self.ult("cut", "check", "cut/take.json", "--platform", "tiktok").code, 0)
        r = self.ult("cut", "render", "cut/take.json", "--out", "media/out.mp4", "--vertical", "--punch", "1.12")
        self.assertEqual(r.code, 0, r.all)
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration",
                                "-of", "json", str(self.root / "media" / "out.mp4")], capture_output=True, text=True)
        info = json.loads(probe.stdout)
        self.assertEqual((info["streams"][0]["width"], info["streams"][0]["height"]), (1080, 1920))
        self.assertAlmostEqual(float(info["format"]["duration"]), 3.1, delta=0.15)

    def test_render_refuses_a_broken_plan(self):
        self.write("cut/bad.json", json.dumps({"source": "x.mp4", "duration": 2, "segments": [{"in": 1, "out": 5}]}))
        r = self.ult("cut", "render", "cut/bad.json", "--out", "o.mp4")
        self.assertEqual(r.code, 1)
        self.assertIn("not rendered", r.out)


class Routing(LaunchCase):
    def test_talking_head_jobs_go_to_the_video_plugin(self):
        from ultlib.pick import pick
        for t in ("Cut my talking head video into shorts", "remove the silences from my recording",
                  "Make clips from my podcast episode", "turn this interview into 5 tiktoks"):
            with self.subTest(t=t):
                self.assertEqual(pick(t, root=self.root), "creator")
                self.assertIn("ultimatum-video:video", pick_hooks(t, self.root))
        self.assertEqual(pick("Make an emotional brand film", root=self.root), "film")
        self.assertEqual(pick("Fix the jump cut bug in the player component", root=self.root), "work")
        self.assertEqual(pick("What is a talking head video?", root=self.root), "chat")


class Guides(unittest.TestCase):
    def test_guide_is_small_and_wired_into_social_and_video(self):
        self.assertLessEqual(len((TEAMS / "creator-cut" / "guide.md").read_bytes()), 4096)
        for f in ("teams/social-media/video-style.md", "teams/social-media/scope.md", "teams/video/guide.md",
                  "plugins/ultimatum-video/skills/video/SKILL.md"):
            self.assertIn("creator-cut/guide.md", (REPO / f).read_text(), f)
        for head in ("ultimatum-video/skills/video", "ultimatum-social-media/skills/social-media"):
            self.assertTrue((REPO / "plugins" / head / "references" / "creator-cut" / "edit.md").is_file(), head)

    def test_guides_name_the_cut_commands(self):
        text = "".join((TEAMS / "creator-cut" / f).read_text() for f in ("guide.md", "hooks.md", "edit.md"))
        for cmd in ("cut silences", "cut check", "cut render", "cut deliver", "posts captions", "gate approve papercut"):
            self.assertIn(cmd, text)


if __name__ == "__main__":
    unittest.main()
