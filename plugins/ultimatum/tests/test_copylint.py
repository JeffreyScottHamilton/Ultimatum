"""Checks for ultlib.copylint, the page-copy lint (Taste copy.md § Tells)."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(P / "scripts"))
from ultlib import copylint  # noqa: E402

KIT = P / "data" / "craft" / "taste" / "kit"


def _page(body: str) -> str:
    return f"<!doctype html><html><head><style>.x{{content:'delve'}}</style></head><body>{body}</body></html>"


class CopyLint(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, text: str, name: str = "page.html") -> Path:
        path = Path(self.tmp.name) / name
        path.write_text(text, encoding="utf-8")
        return path

    def rules(self, body: str, **kw) -> dict[str, str]:
        return {f["rule"].split(" (")[0]: f["level"] for f in copylint.lint(self.write(_page(body)), **kw)}

    def run_cli(self, *argv: str) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return copylint.main(list(argv))

    def test_clean_copy_passes(self):
        body = ("<h1>Bike repairs in Leith</h1><p>Drop it off on Monday and ride it home by Friday.</p>"
                "<a href='#b'>Book a service</a><footer>&copy; 2026 Spoke and Chain</footer>")
        self.assertEqual(self.rules(body, year=2026), {})

    def test_banned_words_fail(self):
        found = self.rules("<p>We delve into a seamless, passionate journey!</p>")
        for rule in ("worn word", "virtue word", "metaphor frame", "exclamation"):
            self.assertEqual(found.get(rule), "fail", rule)

    def test_hidden_text_is_skipped(self):
        body = ("<script>var a = 'seamless';</script><code>robust</code>"
                "<p data-copy-ok>Our honest promise</p><span aria-hidden='true'>calm</span>")
        self.assertEqual(self.rules(body), {})

    def test_allow_exempts_a_client_word(self):
        self.assertNotIn("virtue word", self.rules("<p>Calm Bay Kayaks</p>", allow={"calm"}))

    def test_headings(self):
        found = self.rules("<h1>Welcome to Leith</h1><h2>Why choose us?</h2><h3>Fast repairs.</h3>"
                           "<h3>OUR PRICES</h3>")
        for rule in ("welcome headline", "headline posed as a question", "heading ends with a full stop",
                     "heading in capitals"):
            self.assertEqual(found.get(rule), "fail", rule)

    def test_vague_action_labels(self):
        found = self.rules("<a href='#'>Learn more</a><button>Book a fitting</button>")
        self.assertEqual(found, {"vague action label": "fail"})
        self.assertEqual(self.rules("<a href='#'>Book a service</a><a href='#'>More</a>"),
                         {"vague action label": "fail"})

    def test_old_copyright_year(self):
        self.assertEqual(self.rules("<p>&copy; 2023 Spoke</p>", year=2026), {"old copyright year": "fail"})
        self.assertEqual(self.rules("<p>&copy; 2019&ndash;2026 Spoke</p>", year=2026), {})

    def test_capped_device_warns_then_fails(self):
        dash = "<p>Wheels — trued.</p>"
        self.assertEqual(self.rules(dash * 2), {})
        self.assertEqual(self.rules(dash * 3), {"em dash": "warn"})
        self.assertEqual(self.rules(dash * 5), {"em dash": "fail"})

    def test_markdown_headings(self):
        path = self.write("# Our story.\n\nWe fix bikes.\n", "copy.md")
        self.assertEqual({f["rule"] for f in copylint.lint(path)}, {"heading ends with a full stop"})

    def test_exit_codes(self):
        good = self.write(_page("<p>We fix bikes.</p>"), "good.html")
        bad = self.write(_page("<p>Look no further.</p>"), "bad.html")
        self.assertEqual(self.run_cli(str(good)), 0)
        self.assertEqual(self.run_cli(str(bad)), 1)
        self.assertEqual(self.run_cli(str(Path(self.tmp.name) / "missing.html")), 2)
        self.assertEqual(self.run_cli(), 2)

    def test_kit_pages_pass(self):
        found = [f for page in copylint.files([str(KIT)]) for f in copylint.lint(page) if f["level"] == "fail"]
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
