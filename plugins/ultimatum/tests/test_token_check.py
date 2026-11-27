"""Checks for token_check.py (raw values, embedding, asset colours) and its guide."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1]
TOKENS = P / "data" / "design-own" / "tokens"
TOOL = TOKENS / "token_check.py"
STARTER = TOKENS / "starter.tokens.css"
GUIDE = P / "skills" / "website" / "references" / "craft" / "ui-ux-pro-max" / "token-check.md"

sys.path.insert(0, str(TOKENS))
sys.dont_write_bytecode = True
import token_check  # noqa: E402


def run(*args):
    return subprocess.run([sys.executable, "-I", "-B", str(TOOL), *map(str, args)],
                          capture_output=True, text=True, timeout=120)


def scan_text(name, text, *extra):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / name
        f.write_text(text, encoding="utf-8")
        r = run("scan", "--tokens", STARTER, f, "--json", *extra)
    return r.returncode, json.loads(r.stdout) if r.stdout.strip().startswith("{") else r


class Scan(unittest.TestCase):
    def test_self_check(self):
        r = run("--self-check")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("0 problem(s)", r.stdout)

    def test_clean_component_passes(self):
        code, out = scan_text("card.css", ".card { color: var(--foreground); padding: 1rem 12px; gap: 24px;"
                                          " font-size: 0.875rem; border-radius: var(--radius); border: 1px solid var(--border); margin: 0; }\n")
        self.assertEqual(code, 0, out)
        self.assertEqual(out["findings"], [])

    def test_raw_colour_suggests_the_role(self):
        code, out = scan_text("button.css", ".b { background: #2F6B4F; }\n")
        self.assertEqual(code, 1)
        [f] = out["findings"]
        self.assertEqual((f["rule"], f["line"]), ("raw-color", 1))
        self.assertIn("var(--primary)", f["fix"])

    def test_each_rule_fires_where_expected(self):
        css = ("a { color: rgb(10 20 30); }\n"
               "b { background: white; }\n"
               "c { font-family: 'Inter', sans-serif; }\n"
               "d { padding: 13px; }\n"
               "d2 { font-size: 17px; border-radius: 0.5rem; }\n"
               "e { color: var(--colour-typo); }\n"
               "#add:hover { color: var(--primary); }\n")
        code, out = scan_text("x.css", css)
        got = sorted((f["rule"], f["line"]) for f in out["findings"])
        self.assertEqual(got, sorted([("named-color", 2), ("off-scale", 4), ("raw-color", 1), ("raw-font", 3),
                               ("off-scale", 5), ("unknown-var", 6)]))
        self.assertEqual(code, 1)

    def test_html_svg_and_components_are_read(self):
        html = ('<html><head><style>.x{color:#c4322b}</style></head><body>'
                '<svg><rect fill="#123456"/><path stroke="url(#g)"/></svg>'
                '<p style="background-color: hsl(0 0% 100%)">x</p></body></html>\n')
        _, out = scan_text("p.html", html)
        self.assertEqual(sorted(f["rule"] for f in out["findings"]), ["raw-color"] * 3)
        _, out = scan_text("c.tsx", "const s = { backgroundColor: '#ffffff', color: 'var(--primary)' }; // #abcdef\n")
        self.assertEqual([f["rule"] for f in out["findings"]], ["raw-color"])

    def test_ignores_and_warnings_mode(self):
        code, out = scan_text("x.css", "a { color: #123456; } /* token-check: ignore */\nb { margin: 13px; }\n")
        self.assertEqual(code, 0)
        self.assertEqual([f["rule"] for f in out["findings"]], ["off-scale"])
        code, _ = scan_text("x.css", "b { margin: 13px; }\n", "--strict")
        self.assertEqual(code, 1)
        code, out = scan_text("x.css", "/* token-check: ignore-file */ a { color: red; }\n")
        self.assertEqual((code, out["files"]), (0, 0))

    def test_folders_skip_vendored_and_token_files(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "node_modules" / "lib").mkdir(parents=True)
            (d / "node_modules" / "lib" / "a.css").write_text("a{color:#000}", encoding="utf-8")
            (d / "tokens.css").write_text(":root{--ink:#111111;}", encoding="utf-8")
            (d / "site.css").write_text("a{color:var(--ink)}", encoding="utf-8")
            r = run("scan", "--tokens", d / "tokens.css", d, "--json")
        out = json.loads(r.stdout)
        self.assertEqual((r.returncode, out["files"], out["findings"]), (0, 1, []))

    def test_bad_arguments_exit_2(self):
        for args in (["scan", "--tokens", "missing.css", "."], ["scan", "--tokens", STARTER, "nowhere/"],
                     ["scan", "--tokens", STARTER, ".", "--only", "nope"], ["colors", "--tokens", STARTER, "x.jpg"], []):
            with self.subTest(args=args):
                self.assertEqual(run(*args).returncode, 2)


class Embed(unittest.TestCase):
    def test_embed_is_idempotent_and_prunes(self):
        page = "<!doctype html><html><head><title>t</title></head><body style=\"color: var(--primary)\"></body></html>\n"
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d) / "p.html", Path(d) / "o.html"
            src.write_text(page, encoding="utf-8")
            self.assertEqual(run("embed", "--tokens", STARTER, src, "--out", out, "--used").returncode, 0)
            once = out.read_text(encoding="utf-8")
            self.assertEqual(run("embed", "--tokens", STARTER, out, "--out", out, "--used").returncode, 0)
            twice = out.read_text(encoding="utf-8")
            self.assertEqual(run("embed", "--tokens", STARTER, src, "--out", out).returncode, 0)
            whole = out.read_text(encoding="utf-8")
        self.assertEqual(once, twice)
        self.assertEqual(once.count("<style data-tokens"), 1)
        self.assertLess(once.index("data-tokens"), once.index("<title>"))
        self.assertIn("--primary:", once)
        self.assertIn("--color-moss-600:", once)   # pointed at by --primary
        self.assertIn(".dark {", once)             # dark override of --primary kept
        self.assertNotIn("--color-ink-50:", once)
        self.assertIn("--color-ink-50:", whole)

    def test_used_refuses_nested_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            tok, page = Path(d) / "t.css", Path(d) / "p.html"
            tok.write_text("@media (prefers-color-scheme: dark) { :root { --a: #000; } }", encoding="utf-8")
            page.write_text("<head></head>", encoding="utf-8")
            r = run("embed", "--tokens", tok, page, "--out", page, "--used")
        self.assertEqual(r.returncode, 2)


class Colors(unittest.TestCase):
    def test_png_colours_against_the_palette(self):
        moss, paper, off = (47, 107, 79, 255), (246, 247, 246, 255), (90, 40, 160, 255)
        rows = [[moss] * 6 + [paper] * 3 + [off] for _ in range(10)]
        with tempfile.TemporaryDirectory() as d:
            png = Path(d) / "b.png"
            png.write_bytes(token_check.png_bytes(10, 10, rows))
            r = run("colors", "--tokens", STARTER, png, "--json")
        out = json.loads(r.stdout)
        self.assertEqual(r.returncode, 1)
        by = {c["color"]: c for c in out["colors"]}
        self.assertEqual(set(by), {"#2f6b4f", "#f6f7f6", "#5a28a0"})
        self.assertAlmostEqual(by["#2f6b4f"]["share"], 0.6)
        self.assertFalse(by["#2f6b4f"]["off_palette"])
        self.assertTrue(by["#5a28a0"]["off_palette"])
        self.assertEqual(out["off_palette"], 1)

    def test_svg_colours_and_unsupported_png(self):
        with tempfile.TemporaryDirectory() as d:
            svg = Path(d) / "logo.svg"
            svg.write_text('<svg><rect fill="#2f6b4f"/><circle fill="rgb(246, 247, 246)"/></svg>', encoding="utf-8")
            r = run("colors", "--tokens", STARTER, svg)
            bad = Path(d) / "i.png"
            bad.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + bytes(13) + bytes(4))
            r2 = run("colors", "--tokens", STARTER, bad)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("2 colour(s), 0 off the palette", r.stdout)
        self.assertEqual(r2.returncode, 2)

    def test_png_filters_decode(self):
        # Rows written with each filter type by hand must decode to the same pixels.
        import struct
        import zlib
        px = [[(10 * x + y, 200 - x, 7 * y, 255) for x in range(4)] for y in range(4)]
        raw = b""
        prev = bytes(16)
        for y, row in enumerate(px):
            line = bytes(v for p in row for v in p)
            f = y % 5 if y else 1
            out = bytearray()
            for i, v in enumerate(line):
                a = line[i - 4] if i >= 4 else 0
                b, c = prev[i], prev[i - 4] if i >= 4 else 0
                pr = {0: 0, 1: a, 2: b, 3: (a + b) // 2}.get(f)
                if f == 4:
                    p = a + b - c
                    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                    pr = a if pa <= pb and pa <= pc else b if pb <= pc else c
                out.append((v - pr) & 255)
            raw += bytes([f]) + bytes(out)
            prev = line

        def chunk(k, body):
            return struct.pack(">I", len(body)) + k + body + struct.pack(">I", zlib.crc32(k + body))
        data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 4, 4, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
        self.assertEqual(list(token_check.png_pixels(data)), [p for row in px for p in row])


class Guide(unittest.TestCase):
    def test_guide_lists_every_rule(self):
        text = GUIDE.read_text(encoding="utf-8")
        in_guide = set(re.findall(r"^\| `([a-z-]+)` \|", text, re.M))
        listed = {line.split(":")[0] for line in run("rules").stdout.splitlines()}
        self.assertEqual(in_guide, listed)

    def test_tool_is_stdlib_and_offline(self):
        text = TOOL.read_text(encoding="utf-8")
        imports = set(re.findall(r"^(?:from|import)\s+([a-zA-Z_]+)", text, re.M))
        self.assertLessEqual(imports, {"__future__", "json", "math", "re", "struct", "sys", "tempfile", "zlib",
                                       "argparse", "pathlib"})
        self.assertNotRegex(text, r"\b(urllib|http\.client|socket|requests|subprocess)\b")


if __name__ == "__main__":
    unittest.main()
