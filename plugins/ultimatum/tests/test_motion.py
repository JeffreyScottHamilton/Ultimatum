"""Motion Graphics: plain-chat routing, storyboard gate, beats/media checks, and the review loop."""
import json
import math
import os
import shutil
import subprocess
import sys
import unittest
from array import array
from pathlib import Path

from _harness import LAUNCH, LAUNCH_SCRIPTS, TEAMS, LaunchCase as UltCase, pick_hooks

sys.path.insert(0, LAUNCH_SCRIPTS)
PLUGIN = LAUNCH


def hook(prompt, cwd):
    return pick_hooks(prompt, cwd)


class PlainChatRouting(UltCase):
    """The five plain-chat prompts from the plan, through the real hook."""

    def site(self):
        self.write("index.html", "<nav class='menu'></nav>")
        self.write("styles.css", "nav{}")

    def test_five_prompts_pick_the_right_workflow(self):
        from ultlib.pick import pick
        self.site()
        self.assertNotIn("ultimatum:work", hook("How does the export module work?", self.root))
        cases = {
            "Fix the CSV export": "work",
            "Build me a website for my coffee shop": "website",
            "Fix the mobile menu": "website",
            "Make a 15 second logo reveal video for my bakery": "motion",
        }
        for prompt, kind in cases.items():
            with self.subTest(prompt=prompt):
                self.assertEqual(pick(prompt, root=self.root), kind)
                out = hook(prompt, self.root)
                # Only coding work goes to ultimatum:work; the rest go to their plugin.
                self.assertEqual("ultimatum:work" in out, kind == "work")

    def test_animation_inside_a_website_stays_website(self):
        from ultlib.pick import pick
        self.site()
        self.assertEqual(pick("Animate the hamburger menu on the landing page", root=self.root), "website")

    def test_motion_questions_get_an_answer_not_a_project(self):
        from ultlib.pick import pick
        for q in ("What is motion graphics?", "How do I animate a title sequence?"):
            self.assertEqual(pick(q), "chat", q)
        self.assertEqual(pick("Can you make a logo reveal video for my bakery?"), "motion")

    def test_video_engineering_stays_work(self):
        from ultlib.pick import pick
        for t in ("Fix the video upload endpoint", "Render the video thumbnail in the player component"):
            self.assertEqual(pick(t), "work", t)

    def test_route_prints_the_motion_workflow(self):
        r = self.ult("route", "Make a beat-synced promo clip with this song", "--root", str(self.root))
        self.assertIn("workflow: motion", r.out)


class StoryboardGate(UltCase):
    def test_new_clip_stops_for_storyboard_approval(self):
        r = self.ult("motion", "Make a 15 second logo reveal video for my bakery", "--root", str(self.root))
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("user approves storyboard", r.out)
        self.assertIn("no production animation before that", r.out)
        self.assertIn("teams/motion-graphics/storyboard.md", r.out)
        self.assertLess(r.out.index("user approves storyboard"), r.out.index("animator"))

    def test_approval_is_recorded_and_opens_the_gate(self):
        self.write(".ultimatum/brief.md", "# Brief\n\n## Approved direction\n\nwarm site\n\n## Phases\n\n1. home\n")
        self.assertEqual(self.ult("motion", "--approve", "", "--root", str(self.root)).code, 2)
        r = self.ult("motion", "--approve", "6 shots, reveal at 0:08 on the drop", "--root", str(self.root))
        self.assertEqual(r.code, 0, r.all)
        brief = (self.root / ".ultimatum" / "brief.md").read_text()
        self.assertIn("## Approved storyboard", brief)
        self.assertIn("## Approved direction", brief)
        self.assertIn("## Phases", brief)
        r = self.ult("motion", "Make a 15 second logo reveal video", "--root", str(self.root))
        self.assertIn("gate: approved", r.out)
        self.assertNotIn("user approves storyboard", r.out)

    def test_small_change_to_an_existing_clip_skips_the_storyboard(self):
        r = self.ult("motion", "Trim the intro video to 6 seconds", "--root", str(self.root))
        self.assertIn("size: small", r.out)
        self.assertNotIn("storyboard", r.out.split("load:")[0])
        self.assertIn("scope: only the change asked for", r.out)

    def test_music_points_to_beats_as_suggestions(self):
        r = self.ult("motion", "Make a beat-synced promo clip with this song", "--root", str(self.root))
        self.assertIn("ult beats", r.out)
        self.assertIn("confirm before timing cuts", r.out)

    def test_skill_files_say_stop_and_wait(self):
        skill = (TEAMS / "motion-graphics/guide.md").read_text()
        board = (TEAMS / "motion-graphics/storyboard.md").read_text()
        self.assertIn("stop and wait", skill)
        self.assertIn("no production animation until the user approves", skill)
        self.assertIn("Open blockers stop delivery", skill)
        self.assertIn("possible cues", board)
        self.assertIn("suggested", board)
        self.assertLessEqual(len(skill.encode()), 4096)


class Cues(unittest.TestCase):
    def test_onset_cues_find_regular_hits(self):
        from ultlib.media import RATE, onset_cues
        a = array("h")
        for n in range(RATE * 3):
            t = n / RATE
            a.append(int(20000 * math.sin(2 * math.pi * 110 * t) * math.exp(-14 * (t % 0.5))))
        cues = onset_cues(a)
        expected = [0.5, 1.0, 1.5, 2.0, 2.5]
        self.assertEqual(len(cues), len(expected), cues)
        for got, want in zip(cues, expected):
            self.assertAlmostEqual(got, want, delta=0.05)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg not installed")
class MediaOnARealExport(UltCase):
    def setUp(self):
        super().setUp()
        self.clip = self.root / "clip.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=640x360:r=30:d=3",
                        "-f", "lavfi", "-i", "aevalsrc='0.8*sin(2*PI*55*t)*exp(-14*mod(t,0.5))':s=44100:d=3",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(self.clip)],
                       check=True, timeout=120)

    def test_media_reports_the_export(self):
        r = self.ult("media", str(self.clip), "--json")
        self.assertEqual(r.code, 0, r.all)
        m = json.loads(r.out)
        self.assertAlmostEqual(m["duration"], 3.0, delta=0.1)
        self.assertEqual((m["width"], m["height"], m["fps"]), (640, 360, 30.0))
        self.assertTrue(m["audio"])
        self.assertIsNotNone(m["lufs"])
        self.assertEqual(m["warnings"], [])

    def test_ffmpeg_fallback_labels_possible_cues(self):
        r = self.ult("beats", str(self.clip), "--no-librosa")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("possible cues", r.out)
        self.assertIn("confirm each cue", r.out)
        self.assertIn("1.00", r.out)

    def test_missing_file_is_a_clear_error(self):
        self.assertEqual(self.ult("media", str(self.root / "nope.mp4")).code, 2)


class ReviewLoop(UltCase):
    def loop(self, *a):
        return self.ult("loop", *a, "--root", str(self.root))

    def test_blockers_hold_delivery_until_rechecked_and_minor_ones_do_not(self):
        self.assertEqual(self.loop("status").code, 0)
        self.loop("add", "Title gone before it can be read", "--at", "0:04")
        self.loop("add", "Logo edge slightly soft", "--at", "0:09")
        r = self.loop("status")
        self.assertEqual(r.code, 1)
        self.assertIn("unsorted", r.out)
        self.loop("triage", "F1", "--blocker", "--to", "animator")
        self.loop("triage", "F2", "--minor")
        self.assertEqual(self.loop("status").code, 1)
        self.assertEqual(self.loop("recheck", "F1", "--pass").code, 2)  # nothing fixed yet
        self.loop("fixed", "F1")
        self.loop("recheck", "F1", "--fail")
        self.assertEqual(self.loop("status").code, 1)
        self.loop("fixed", "F1")
        self.loop("recheck", "F1", "--pass")
        r = self.loop("status")
        self.assertEqual(r.code, 0, r.out)
        self.assertIn("1 minor", r.out)

    def test_triage_needs_one_choice(self):
        self.loop("add", "x")
        self.assertEqual(self.loop("triage", "F1").code, 2)
        self.assertEqual(self.loop("triage", "F9", "--minor").code, 2)


if __name__ == "__main__":
    unittest.main()
