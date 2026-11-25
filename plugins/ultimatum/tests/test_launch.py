"""Launch, Business and Social Media: plain-chat routing, the shared brief, and every approval gate.

These run the real `ult` CLI and the real UserPromptSubmit hook in a temp project. They check
the workflow state Claude follows (approvals, hand-offs, blocks), not Claude's own judgment.
"""
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

from _harness import PY, SCRIPTS, UltCase

sys.path.insert(0, SCRIPTS)
PLUGIN = Path(SCRIPTS).parent

FILLED = ("- Audience: busy parents in Leeds\n- Offer: Saturday baking class, 40 GBP\n"
          "- Main visitor action: book a class\n- Pages: home, classes, book\n"
          "- Known business details: 3 years trading\n- Open questions: photos\n"
          "- Checks that show it works: booking form sends\n")


def hook(prompt, cwd):
    env = dict(os.environ)
    env.pop("ULTIMATUM_AUTO", None)
    data = json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": prompt, "cwd": str(cwd)})
    cp = subprocess.run([PY, os.path.join(SCRIPTS, "ult-pick")], input=data, capture_output=True,
                        text=True, env=env, timeout=30)
    assert cp.returncode == 0, cp.stderr
    return cp.stdout


class Base(UltCase):
    def u(self, *a):
        return self.ult(*a, "--root", str(self.root))

    def brief(self):
        return (self.root / ".ultimatum" / "brief.md").read_text()

    def fill_brief(self):
        self.assertEqual(self.u("business", "--start-brief").code, 0)
        text = self.brief()
        head, _, rest = text.partition("## Build brief")
        body, sep, tail = rest.partition("\nStatus:")
        self.write(".ultimatum/brief.md", head + "## Build brief\n\n" + FILLED + sep + tail)

    def approved_brief(self):
        self.fill_brief()
        r = self.u("gate", "approve", "brief", "yes, go with this")
        self.assertEqual(r.code, 0, r.all)


class PlainChatRouting(Base):
    CASES = {
        "Help me launch my business": "ultimatum:launch",
        "What's stopping people from booking?": "ultimatum:business",
        "What’s stopping people from booking?": "ultimatum:business",
        "Build a website": "ultimatum:website",
        "Fix the mobile menu": "ultimatum:website",
        "Plan a week of posts": "ultimatum:social-media",
        "Make a motion graphic": "ultimatum:motion-graphics",
        "Fix the signup form validation bug": "ultimatum:work",
    }
    SKILLS = {"ultimatum:launch", "ultimatum:business", "ultimatum:website", "ultimatum:social-media",
              "ultimatum:motion-graphics", "ultimatum:work"}

    def test_each_plain_prompt_starts_one_workflow(self):
        self.write("index.html", "<nav class='menu'></nav>")
        for prompt, skill in self.CASES.items():
            with self.subTest(prompt=prompt):
                out = hook(prompt, self.root)
                self.assertIn(skill, out)
                for other in self.SKILLS - {skill}:
                    self.assertNotIn(f'\\"{other}\\"', out)

    def test_plain_questions_get_an_answer(self):
        for q in ("What is a content calendar?", "How does a soft launch work?"):
            self.assertEqual(hook(q, self.root), "", q)

    def test_slash_commands_win(self):
        for p in ("/ultimatum:website plan a week of posts", "/ultimatum:social-media build a website"):
            self.assertEqual(hook(p, self.root), "", p)

    def test_engineering_words_stay_work(self):
        from ultlib.pick import pick
        for t in ("Add conversion tracking to the checkout", "Launch the release to staging"):
            self.assertEqual(pick(t), "work", t)


class BuildBriefGate(Base):
    def test_draft_brief_cannot_be_approved_until_filled(self):
        self.assertEqual(self.u("gate", "approve", "brief", "yes").code, 2)  # no brief yet
        self.u("business", "--start-brief")
        self.assertIn("Status: draft (not approved)", self.brief())
        r = self.u("gate", "approve", "brief", "yes")
        self.assertEqual(r.code, 2)
        self.assertIn("empty fields: Audience, Offer, Main visitor action", r.err)
        self.assertEqual(self.u("gate", "approve", "brief").code, 2)  # the user's words are required

    def test_website_waits_for_the_approved_brief_and_drift_reopens_it(self):
        self.fill_brief()
        r = self.u("website", "Build the bakery site")
        self.assertIn("launch: the build brief is waiting", r.out)
        self.assertEqual(self.u("gate", "check", "brief").code, 1)
        self.u("gate", "approve", "brief", "yes, go with this")
        self.assertEqual(self.u("gate", "check", "brief").code, 0)
        self.assertNotIn("launch:", self.u("website", "Build the bakery site").out)
        self.write(".ultimatum/brief.md", self.brief().replace("40 GBP", "55 GBP"))
        r = self.u("gate", "check", "brief")
        self.assertEqual(r.code, 1)
        self.assertIn("changed", r.out)
        self.assertIn("launch: the build brief is changed", self.u("website", "Build the bakery site").out)

    def test_revise_is_not_approval(self):
        self.approved_brief()
        self.u("gate", "revise", "brief", "make it about kids' classes")
        r = self.u("gate", "check", "brief")
        self.assertEqual(r.code, 1)
        self.assertIn("revise", r.out)

    def test_launch_board_follows_the_handoff_order(self):
        self.assertIn("business --start-brief", self.u("launch").out)
        self.fill_brief()
        self.assertIn("show the build brief to the user and wait", self.u("launch").out)
        self.u("gate", "approve", "brief", "yes")
        out = self.u("launch").out
        self.assertIn("send the approved brief to Website", out)
        self.assertIn("social: drafts from the approved offer while Website builds: open", out)

    def test_state_survives_a_resume(self):
        self.approved_brief()
        data = json.loads((self.root / ".ultimatum" / "approvals.json").read_text())
        self.assertEqual(data["items"]["brief"]["state"], "approved")
        self.assertEqual(data["items"]["brief"]["note"], "yes, go with this")
        r = self.u("gate", "status", "--json")
        self.assertEqual(json.loads(r.out)["mockup"]["state"], "waiting")


class Business(Base):
    def test_advice_changes_nothing(self):
        r = self.u("business", "What's stopping people from booking?")
        self.assertIn("mode: advice", r.out)
        self.assertIn("no files, site or records are changed", r.out)
        self.assertIn("observed (with its source) or guessed", r.out)
        self.assertFalse((self.root / ".ultimatum" / "brief.md").exists())

    def test_requested_change_is_scoped(self):
        self.assertIn("mode: change", self.u("business", "Change the headline to mention Saturdays").out)

    def test_launch_mode_loads_the_brief_guide(self):
        r = self.u("business", "Help me launch my bakery")
        self.assertIn("mode: launch", r.out)
        self.assertIn("skills/business/brief.md", r.out)


class MockupGate(Base):
    def test_mockup_approval_is_a_separate_gate(self):
        self.approved_brief()
        self.assertEqual(self.u("gate", "check", "mockup").code, 1)
        img = self.write("mock.png", "fake image bytes")
        r = self.u("website", "--approve", "warm cream, big book button", "--image", str(img))
        self.assertEqual(r.code, 0, r.all)
        self.assertEqual(self.u("gate", "check", "mockup").code, 0)
        Path(img).write_text("another image")
        self.assertIn("changed", self.u("gate", "check", "mockup").out)

    def test_small_fix_skips_the_mockup_but_keeps_the_browser_check(self):
        r = self.u("website", "Fix the mobile menu")
        self.assertNotIn("gate:", r.out)
        skill = (PLUGIN / "skills/website/SKILL.md").read_text()
        self.assertIn("No mockup and no approval stop", skill)
        self.assertIn("then the browser check", skill)


class SocialAndPublish(Base):
    def test_social_waits_for_the_offer_and_the_publish_gate(self):
        self.fill_brief()
        r = self.u("social", "Plan a week of posts")
        self.assertIn("offer: waiting", r.out)
        self.assertIn("wait: the launch brief is not approved yet", r.out)
        self.assertIn("publish: waiting for the user's yes", r.out)
        self.assertIn("--need-link", r.out)
        self.assertIn("no posting, sending, spending", r.out)

    def test_video_step_is_added_when_a_video_helps(self):
        r = self.u("social", "Plan a week of posts with a short reel")
        self.assertIn("send one video brief to Motion Graphics", r.out)
        self.assertNotIn("Motion", self.u("social", "Plan a week of posts").out)

    def test_publish_needs_a_checked_link_and_is_used_once(self):
        self.approved_brief()
        self.u("gate", "approve", "publish", "yes, post them")
        r = self.u("gate", "check", "publish", "--need-link")
        self.assertEqual(r.code, 1)
        self.assertIn("live link is not checked", r.out)
        self.u("gate", "approve", "publish", "yes, post them", "--link", "https://example.test/book")
        self.assertEqual(self.u("gate", "check", "publish", "--need-link").code, 0)
        self.assertEqual(self.u("gate", "done", "publish").code, 0)
        self.assertEqual(self.u("gate", "check", "publish").code, 1)
        self.assertEqual(self.u("gate", "done", "publish").code, 1)

    def test_results_go_back_to_the_brief(self):
        self.assertEqual(self.u("social", "--results", "").code, 2)
        self.assertEqual(self.u("social", "--results", "120 visits, 4 bookings").code, 0)
        self.assertIn("## Campaign results\n\n120 visits, 4 bookings", self.brief())
        self.assertIn("publish and measure; results back to Business: done", self.u("launch").out)


class DeployGate(Base):
    def test_deploy_needs_its_own_yes(self):
        self.assertEqual(self.u("gate", "check", "deploy").code, 1)
        self.u("gate", "approve", "deploy", "ship it")
        self.assertEqual(self.u("gate", "check", "deploy").code, 0)
        self.u("gate", "done", "deploy", "deployed, live page checked")
        self.assertEqual(self.u("gate", "check", "deploy").code, 1)
        self.assertEqual(self.u("gate", "check", "bogus").code, 2)


class MotionKinds(Base):
    def test_storyboard_approval_records_the_gate(self):
        self.assertEqual(self.u("motion", "--approve", "6 shots, logo at 0:08").code, 0)
        self.assertEqual(self.u("gate", "check", "storyboard").code, 0)

    def test_first_launch_then_later_then_reference(self):
        self.approved_brief()
        r = self.u("motion", "Make a launch video for the bakery")
        self.assertIn("kind: first launch video; /brag is optional", r.out)
        clip = self.write("final.mp4", "pretend export")
        r = self.u("motion", "--save-style", "pacing fast, cuts on beat, text slides, sound whoosh, ending logo",
                   "--video", str(clip))
        self.assertEqual(r.code, 1)  # the finished video is not approved yet
        self.u("gate", "approve", "video", "love it", "--file", str(clip))
        r = self.u("motion", "--save-style", "pacing fast, cuts on beat", "--video", str(clip))
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("warn: the guide does not mention: text, sound, ending", r.out)
        style = (self.root / ".ultimatum" / "motion" / "style.md").read_text()
        self.assertIn(str(Path(clip).resolve().name), style)
        r = self.u("motion", "Make a video for the new menu")
        self.assertIn("kind: later video", r.out)
        self.assertIn("motion/style.md", r.out)
        self.assertIn("user approves storyboard", r.out)  # a later video still needs its own storyboard
        self.assertIn("kind: standalone", self.u("motion", "Make a video like this reference").out)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg not installed")
class DeliverRealExport(Base):
    def setUp(self):
        super().setUp()
        self.clip = self.root / "promo.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=orange:s=1280x720:r=30:d=4",
                        "-f", "lavfi", "-i", "sine=f=220:d=4", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-shortest", str(self.clip)], check=True, timeout=120)

    def test_open_blocker_stops_delivery_then_social_gets_the_export(self):
        self.u("loop", "add", "Title gone before it can be read", "--at", "0:02")
        self.u("loop", "triage", "F1", "--blocker", "--to", "animator")
        r = self.u("motion", "--deliver", str(self.clip))
        self.assertEqual(r.code, 1)
        self.assertIn("open blocker", r.out)
        self.u("loop", "fixed", "F1")
        self.u("loop", "recheck", "F1", "--pass")
        r = self.u("motion", "--deliver", str(self.clip))
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("## Delivered video", self.brief())
        r = self.u("social", "Plan posts with the launch reel")
        self.assertIn("checked export received", r.out)


class SkillText(unittest.TestCase):
    def test_connector_fallback_and_no_credentials(self):
        for name in ("launch", "business", "social-media"):
            text = (PLUGIN / f"skills/{name}/SKILL.md").read_text()
            with self.subTest(skill=name):
                self.assertIn("Composio", text)
                self.assertIn("authorized", text)
        defaults = (PLUGIN / "shared/defaults.md").read_text()
        self.assertIn("Context7", defaults)


if __name__ == "__main__":
    unittest.main()
