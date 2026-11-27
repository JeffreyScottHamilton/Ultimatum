"""Checks for the UI UX Pro Max guides (brand, design system, UI styling) and the starter tokens."""
from __future__ import annotations

import json, os, re, sys
from subprocess import run as run_cmd
from pathlib import Path
import unittest

P = Path(__file__).resolve().parents[1]
GUIDES = P / "skills" / "website" / "references" / "craft" / "ui-ux-pro-max"
TOKENS = P / "data" / "design-own" / "tokens"
REPO = P.parents[1]
BUILD = REPO / "tools" / "build_tokens.py"
SOURCE = Path(os.environ.get("UIUX_SOURCE", "/tmp/src/uiux"))

URL = re.compile(r"\bhttps?://[^\s)`>\]|]+")
TICKED = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|csv|json|css|py))`(?:[ \t]*§[ \t]*([A-Z0-9][^`|)\n]*))?")
EXPECTED = {
    "brand-flow.md", "brand-voice.md", "brand-visual.md", "brand-assets.md", "brand-review.md",
    "brand-guidelines-template.md", "token-architecture.md", "token-templates.md",
    "states-and-variants.md", "component-specs.md", "shadcn-components.md", "shadcn-theming.md",
    "shadcn-accessibility.md", "tailwind-utilities.md", "tailwind-customisation.md", "canvas-design.md",
    "later.md",
}
# paths in a user's project, named in the guides as examples; they do not live in this repo
PROJECT_EXAMPLES = {"BRAND.md", "docs/brand-guidelines.md", "design/tokens.json"}


def _md() -> list[Path]:
    return sorted(GUIDES.glob("*.md"))


def _headings(path: Path) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"^#{1,4}\s+(.+)$", path.read_text(encoding="utf-8"), re.M)}


def _resolve(path: Path, ref: str) -> Path | None:
    """A ticked path is relative to the file; `tools/...` names are relative to the repo root."""
    for base in (path.parent, REPO):
        target = (base / ref).resolve()
        if target.exists():
            return target
    return None


class UiuxGuides(unittest.TestCase):
    def test_index_lists_every_file_and_each_exists(self):
        index = (GUIDES / "index.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"^- `([a-z0-9-]+\.md)`:", index, re.M))
        for name in sorted(listed):
            with self.subTest(file=name):
                self.assertTrue((GUIDES / name).is_file())
        on_disk = {p.name for p in _md()} - {"index.md"}
        self.assertEqual(on_disk, listed, "index.md must list every guide once")
        self.assertEqual(listed, EXPECTED)

    def test_files_are_small_and_open_with_when_to_read(self):
        for path in _md():
            lines = path.read_text(encoding="utf-8").splitlines()
            with self.subTest(file=path.name):
                self.assertLessEqual(path.stat().st_size, 15 * 1024)
                self.assertTrue(lines[0].startswith("# "))
                self.assertEqual(lines[1], "")
                self.assertTrue(lines[2].startswith("Read "), "line 3 says when to read the file")

    def test_links_are_https(self):
        for path in _md() + [TOKENS / "README.md"]:
            for url in URL.findall(path.read_text(encoding="utf-8")):
                with self.subTest(file=path.name, url=url):
                    local = re.match(r"http://(localhost|127\.0\.0\.1)[:/]", url)
                    self.assertTrue(url.startswith("https://") or local, "use https, or a local dev URL")

    def test_relative_references_and_sections_resolve(self):
        for path in _md():
            for ref, section in TICKED.findall(path.read_text(encoding="utf-8")):
                if ref in PROJECT_EXAMPLES:
                    continue
                target = _resolve(path, ref)
                if "/" not in ref and target is None and ref.endswith((".json", ".css", ".py")):
                    continue  # a bare file name in an example, such as `tailwind.config.js`
                with self.subTest(file=path.name, ref=ref):
                    self.assertIsNotNone(target, f"{ref} not found")
                if section and target is not None and target.suffix == ".md":
                    with self.subTest(file=path.name, ref=ref, section=section):
                        heads = _headings(target)
                        want = section.strip()
                        # a heading that ends in ")" is cut there by the pattern, so match either way round
                        self.assertTrue(any(want.startswith(h) or h.startswith(want) for h in heads),
                                        f"{ref} has no heading at the start of: {want}")

    def test_no_credentials_or_real_addresses(self):
        secret = re.compile(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}", re.I)
        email = re.compile(r"[\w.+-]+@([\w-]+\.[a-z]{2,})", re.I)
        for path in _md() + sorted(TOKENS.iterdir()):
            text = path.read_text(encoding="utf-8")
            with self.subTest(file=path.name):
                self.assertIsNone(secret.search(text))
                for domain in email.findall(text):
                    self.assertEqual(domain.lower(), "example.com", "only example addresses")

    def test_no_font_files_bundled(self):
        fonts = [p for p in (P / "data").rglob("*") if p.suffix.lower() in {".ttf", ".otf", ".woff", ".woff2"}]
        self.assertEqual(fonts, [], "fonts are linked, never shipped")

    def test_token_file_shape(self):
        data = json.loads((TOKENS / "starter.tokens.json").read_text(encoding="utf-8"))
        for layer in ("primitive", "semantic", "pairs", "component"):
            self.assertIn(layer, data)
        for role, modes in data["semantic"].items():
            with self.subTest(role=role):
                self.assertEqual(set(modes), {"light", "dark"})
        self.assertGreaterEqual(len(data["pairs"]), 10)

    def test_generated_css_is_current_and_every_pair_passes(self):
        res = run_cmd([sys.executable, str(BUILD), "--check"], capture_output=True, text=True, timeout=60)
        self.assertEqual(res.returncode, 0, res.stdout[-2000:] + res.stderr[-2000:])
        lines = [ln for ln in res.stdout.splitlines() if " on " in ln]
        self.assertTrue(lines)
        self.assertTrue(all(ln.startswith("ok ") for ln in lines), "\n".join(lines))

    def test_tailwind_theme_has_the_expected_blocks(self):
        css = (TOKENS / "starter.theme.css").read_text(encoding="utf-8")
        for needle in ('@import "tailwindcss";', "@custom-variant dark", "@theme {", "@theme inline", ".dark {",
                       "--color-primary: var(--primary);"):
            with self.subTest(needle=needle):
                self.assertIn(needle, css)

    def test_toolbelt_stays_stdlib(self):
        text = BUILD.read_text(encoding="utf-8")
        imports = set(re.findall(r"^(?:from|import)\s+([a-zA-Z_]+)", text, re.M))
        self.assertLessEqual(imports, {"__future__", "json", "re", "sys", "argparse", "pathlib", "build_palettes"})
        self.assertNotRegex(text, r"\b(urllib|http\.client|socket|requests)\b")

    @unittest.skipUnless(SOURCE.is_dir(), "source checkout not present (set UIUX_SOURCE)")
    def test_copy_check_passes(self):
        res = run_cmd([sys.executable, str(REPO / "tools" / "copy_check.py"), str(GUIDES), str(SOURCE)],
                             capture_output=True, text=True, timeout=300)
        self.assertEqual(res.returncode, 0, res.stdout[-2000:])


if __name__ == "__main__":
    unittest.main()
