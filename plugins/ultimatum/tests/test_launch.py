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

from _harness import LAUNCH, LAUNCH_SCRIPTS, TEAMS, LaunchCase, pick_hooks

sys.path.insert(0, LAUNCH_SCRIPTS)
PLUGIN = LAUNCH

FILLED = ("- Audience: busy parents in Leeds\n- Offer: Saturday baking class, 40 GBP\n"
          "- Main visitor action: book a class\n- Pages: home, classes, book\n"
          "- Known business details: 3 years trading\n- Open questions: photos\n"
          "- Checks that show it works: booking form sends\n")


def hook(prompt, cwd, scopes=("core",)):
    """Core's UserPromptSubmit hook, as Claude Code runs it."""
    return pick_hooks(prompt, cwd, scopes)


class Base(LaunchCase):
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
    """ultlib.pick sorts plain prompts; core's hook sends each job to the right place.

    The launch and social media plugins have no hook: each is one head skill Claude
    picks from its description, so only core's note is checked here.
    """
    CASES = {
        "Help me launch my business": "launch",
        "What's stopping people from booking?": "business",
        "What’s stopping people from booking?": "business",
        "Build a website": "website",
        "Fix the mobile menu": "website",
        "Plan a week of posts": "social",
        "write a week of tiktok posts": "social",
        "plan instagram reels for my bakery": "social",
        "make 5 youtube shorts ideas": "social",
        "Make a motion graphic": "motion",
        "Make a 30 second launch video": "motion",
        "Make an emotional brand film for our launch": "film",
        "Create a cinematic ad about a nurse coming home": "film",
        "Fix the signup form validation bug": "work",
    }

    def test_each_plain_prompt_picks_one_workflow(self):
        from ultlib.pick import pick
        self.write("index.html", "<nav class='menu'></nav>")
        for prompt, kind in self.CASES.items():
            with self.subTest(prompt=prompt):
                self.assertEqual(pick(prompt, root=self.root), kind)

    HEAD = {"launch": None, "business": None, "website": "ultimatum-website-launch:launch",
            "social": "ultimatum-social-media:social-media", "motion": "ultimatum-video:video",
            "film": "ultimatum-video:video"}

    def test_core_hook_sends_each_job_to_its_plugin(self):
        self.write("index.html", "<nav class='menu'></nav>")
        for prompt, kind in self.CASES.items():
            with self.subTest(prompt=prompt):
                out = hook(prompt, self.root)
                self.assertIn('"additionalContext"', out)
                if kind == "work":
                    self.assertIn("ultimatum:work", out)
                    continue
                self.assertNotIn("ultimatum:work", out)
                self.assertIn("/plugin install ultimatum-", out)
                if self.HEAD[kind]:
                    self.assertIn(self.HEAD[kind], out)

    def test_launch_kind_names_its_plugin(self):
        self.assertIn("ultimatum-ecommerce-launch:launch", hook("launch my online candle shop", self.root))
        self.assertIn("ultimatum-event-launch:launch", hook("help me fill my workshop launch", self.root))
        self.assertIn("ultimatum-event-launch:launch", hook("promote our opening night", self.root))
        for q in ("What is an event?", "How do events work in JavaScript?"):
            self.assertNotIn("event-launch", hook(q, self.root), q)

    def test_plain_questions_get_only_the_style_line(self):
        for q in ("What is a brand film?", "What is a content calendar?", "How does a soft launch work?", "What is TikTok?",
                  "How do instagram reels work?"):
            out = hook(q, self.root)
            self.assertIn("Ultimatum style", out, q)
            self.assertNotIn("/plugin install", out, q)

    def test_style_line_can_be_turned_off(self):
        env = dict(os.environ, ULTIMATUM_STYLE="0")
        env.pop("ULTIMATUM_AUTO", None)
        self.assertEqual(pick_hooks("What is TikTok?", self.root, env=env), "")
        self.assertIn("ultimatum:work", pick_hooks("Fix the signup form validation bug", self.root, env=env))

    def test_slash_commands_win(self):
        for p in ("/ultimatum-website-launch:launch fix the signup form validation bug",
                  "/ultimatum-social-media:social-media fix the signup form validation bug",
                  "/ultimatum:work build a website"):
            self.assertEqual(hook(p, self.root), "", p)

    def test_other_scopes_say_nothing(self):
        out = pick_hooks("Fix the signup form validation bug", self.root, ("launch",))
        self.assertEqual(out, "")

    def test_only_core_registers_a_hook(self):
        from _harness import CORE, REPO
        self.assertIn("--scope core", (CORE / "hooks/hooks.json").read_text())
        for head in sorted((REPO / "plugins").glob("ultimatum-*")):
            with self.subTest(plugin=head.name):
                self.assertFalse((head / "hooks").exists())

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
        self.assertIn("teams/business/brief.md", r.out)


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
        skill = (TEAMS / "website/guide.md").read_text()
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
        self.assertIn("Brand Film when the message is a feeling", r.out)
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


class BrandFilm(Base):
    def manifest(self, clips):
        self.write("film/footage-manifest.json", json.dumps({"clips": clips}))

    def test_four_gates_in_order(self):
        r = self.u("film", "Make an anthem film about people who bake at dawn")
        self.assertIn("sub-genre: montage", r.out)
        self.assertIn("next: write the logline", r.out)
        self.assertIn("teams/brand-film/story.md", r.out)
        self.u("gate", "approve", "story", "yes, the grandmother story")
        r = self.u("film", "Make a brand film")
        self.assertIn("sub-genre: character", r.out)
        self.assertIn("nothing is bought, generated or shot", r.out)
        self.assertIn("teams/brand-film/footage.md", r.out)
        self.u("gate", "approve", "sourcing", "ok, 40 dollars of stock")
        self.assertIn("cut the rough timeline", self.u("film", "Make a brand film").out)

    def test_manifest_needs_sources_costs_and_releases(self):
        self.assertEqual(self.u("film", "--check").code, 1)
        ok = {"file": "a.mp4", "source": "pexels", "id": "123", "license": "Pexels", "date": "2026-11-25",
              "cost": 0, "ai": False, "people": True, "release": "stock licence"}
        self.manifest([ok, {"file": "b.mp4", "source": "user", "id": "phone-2", "license": "owned",
                            "date": "2026-11-25", "cost": 0, "ai": False, "people": True}])
        r = self.u("film", "--check")
        self.assertEqual(r.code, 1)
        self.assertIn("b.mp4: shows people but has no release", r.out)
        self.manifest([ok, {"file": "c.mp4", "source": "ai", "id": "veo-1", "license": "generated",
                            "date": "2026-11-25", "cost": 4.5, "ai": True, "people": False}])
        r = self.u("film", "--check")
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("spend 4.50, 1 AI-made", r.out)
        self.assertIn("C2PA", r.out)

    def test_voiceover_pace(self):
        self.manifest([{"file": "a.mp4", "source": "user", "id": "1", "license": "owned", "date": "x",
                        "cost": 0, "ai": False, "people": False}])
        vo = self.write("film/vo.txt", " ".join(["word"] * 60))
        r = self.u("film", "--check", "--vo", str(vo), "--seconds", "20")
        self.assertIn("too dense: 3.00 words/s", r.out)
        r = self.u("film", "--check", "--vo", str(vo), "--seconds", "40")
        self.assertIn("ok: 1.50 words/s", r.out)


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
        for name in ("business", "social-media"):
            text = (TEAMS / name / "guide.md").read_text()
            with self.subTest(team=name):
                self.assertIn("Composio", text)
                self.assertIn("authorized", text)
        from _harness import REPO
        for head in sorted((REPO / "plugins").glob("ultimatum-*-launch")):
            text = (head / "skills/launch/SKILL.md").read_text()
            with self.subTest(head=head.name):
                self.assertIn("authorized", text)
                self.assertIn("Never put credentials", text)
        defaults = (PLUGIN / "shared/defaults.md").read_text()
        self.assertIn("Context7", defaults)


if __name__ == "__main__":
    unittest.main()
