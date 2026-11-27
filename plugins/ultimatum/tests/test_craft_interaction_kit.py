"""Checks for the interaction kit (data/craft/interaction-kit), its guides and `ult kitlint`."""
import ast
import csv
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from ultlib import kitlint  # noqa: E402

KIT = os.path.join(ROOT, "data", "craft", "interaction-kit")
COMP = os.path.join(KIT, "components")
GUIDES = os.path.join(ROOT, "skills", "website", "references", "craft", "interaction-kit")
ULT = os.path.join(ROOT, "scripts", "ult")
RULES = ["reduced-motion", "transition-all", "will-change-all", "raw-colour", "press-scale",
         "click-target", "icon-label", "focus-hidden", "presence-initial"]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def exports():
    names = set()
    for f in os.listdir(COMP):
        names.update(re.findall(r"^export (?:function|const) (\w+)", read(os.path.join(COMP, f)), re.M))
    return names


def rules_of(src):
    return {f["rule"] for f in kitlint.lint_text(src)}


class Guides(unittest.TestCase):
    def test_files_listed_and_shaped(self):
        index = read(os.path.join(GUIDES, "index.md"))
        names = sorted(os.listdir(GUIDES))
        self.assertGreaterEqual(len(names), 4)
        for name in names:
            path = os.path.join(GUIDES, name)
            lines = read(path).splitlines()
            self.assertTrue(lines[0].startswith("# "), name)
            self.assertTrue(lines[2].startswith("Read "), name)
            self.assertLess(os.path.getsize(path), 15000, name)
            if name not in ("index.md", "later.md"):
                self.assertIn("`%s`" % name, index, name)

    def test_credit_line(self):
        index = read(os.path.join(GUIDES, "index.md"))
        self.assertIn("Watermelon UI", index)
        self.assertIn("MIT", index)
        self.assertIn("None of its code or text is copied", index)

    def test_craft_md_points_here(self):
        craft = read(os.path.join(ROOT, "skills", "website", "references", "website", "craft.md"))
        self.assertIn("../craft/interaction-kit/index.md", craft)

    def test_rule_table_matches_linter(self):
        guide = read(os.path.join(GUIDES, "details.md"))
        src = read(os.path.join(ROOT, "scripts", "ultlib", "kitlint.py"))
        found = set(re.findall(r'add\("([\w-]+)"', src))
        self.assertEqual(found, set(RULES))
        for r in RULES:
            self.assertIn("| `%s` |" % r, guide, r)

    def test_components_guide_covers_every_export(self):
        guide = read(os.path.join(GUIDES, "components.md"))
        for name in exports() - {"cn", "focusRing", "settle", "lively", "useToast"}:
            self.assertIn("## %s" % name, guide, name)


class Kit(unittest.TestCase):
    def test_kit_is_clean(self):
        out = io.StringIO()
        self.assertEqual(kitlint.run([COMP], strict=True, out=out), 0, out.getvalue())
        self.assertIn("0 fail, 0 warn", out.getvalue())

    def test_imports_only_react_motion_and_local(self):
        for f in os.listdir(COMP):
            for mod in re.findall(r"""from\s+["']([^"']+)["']""", read(os.path.join(COMP, f))):
                self.assertTrue(mod in ("react", "motion/react") or mod.startswith("./"), (f, mod))

    def test_catalog(self):
        rows = list(csv.DictReader(io.StringIO(read(os.path.join(KIT, "catalog.csv")))))
        self.assertEqual(len(rows), 131)
        self.assertEqual(len({r["id"] for r in rows}), 131)
        names = exports()
        mapped = [r for r in rows if r["our_component"]]
        self.assertEqual(len(mapped), 110)
        for r in mapped:
            self.assertIn(r["our_component"], names, r["id"])
        for r in rows:
            self.assertEqual(r["install"], "https://registry.watermelon.sh/r/%s.json" % r["id"])
            self.assertTrue(r["what_it_does"] and r["when_to_use"], r["id"])

    def test_blocks(self):
        rows = list(csv.DictReader(io.StringIO(read(os.path.join(KIT, "blocks.csv")))))
        self.assertEqual(len(rows), 201)
        self.assertEqual(sum(1 for r in rows if r["kind"] == "dashboard"), 12)
        for r in rows:
            self.assertTrue(r["install"].startswith("https://registry.watermelon.sh/r/"), r["id"])

    def test_readme_credits(self):
        readme = read(os.path.join(KIT, "README.md"))
        self.assertIn("Watermelon UI", readme)
        self.assertIn("MIT", readme)

    def test_gallery_ignores_build_output(self):
        ignore = read(os.path.join(KIT, "gallery", ".gitignore"))
        for item in ("node_modules/", "app.js", "out.css", "shots/", "theme.css"):
            self.assertIn(item, ignore)

    @unittest.skipUnless(os.environ.get("KIT_TYPECHECK") and shutil.which("npx"), "set KIT_TYPECHECK=1 with gallery deps installed")
    def test_gallery_typechecks(self):
        p = subprocess.run(["npx", "tsc", "--noEmit", "-p", "."], cwd=os.path.join(KIT, "gallery"),
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)


class Rules(unittest.TestCase):
    def test_each_rule_fires(self):
        cases = {
            "reduced-motion": 'import { motion } from "motion/react";\nexport const A = () => <motion.p animate={{ x: 4 }}>a</motion.p>;',
            "transition-all": '<p className="transition-all">a</p>',
            "will-change-all": "const s = { willChange: 'all' };",
            "raw-colour": '<p className="text-[#ff0000]">a</p>',
            "press-scale": "<motion.button whileTap={{ scale: 0.9 }}>Go</motion.button>",
            "click-target": "<div onClick={go}>Open</div>",
            "icon-label": '<button type="button"><svg viewBox="0 0 1 1"></svg></button>',
            "focus-hidden": '<button className="outline-none">Go</button>',
            "presence-initial": "<AnimatePresence>{x}</AnimatePresence>",
        }
        self.assertEqual(set(cases), set(RULES))
        for rule, src in cases.items():
            self.assertIn(rule, rules_of(src), rule)

    def test_good_versions_pass(self):
        good = "\n".join([
            'import { motion, useReducedMotion, AnimatePresence } from "motion/react";',
            "<motion.button whileTap={{ scale: 0.97 }}>Go</motion.button>",
            '<button type="button" aria-label="Close"><svg aria-hidden="true"></svg></button>',
            '<button className="outline-none focus-visible:ring-2">Go</button>',
            '<div role="button" onClick={go} onKeyDown={key}>Open</div>',
            '<div aria-hidden="true" onClick={close} />',
            '<li role="option" onClick={pick}>One</li>',
            "<AnimatePresence initial={false}>{x}</AnimatePresence>",
            '<p className="transition-colors text-primary">a</p>',
            "const r = useReducedMotion();",
        ])
        self.assertEqual(kitlint.lint_text(good), [])

    def test_mask_hex_and_comments_ignored(self):
        self.assertIn("raw-colour", rules_of('const bg = "linear-gradient(#000, transparent)";'))
        self.assertNotIn("raw-colour", rules_of('const maskImage = "linear-gradient(#000, transparent)";'))
        self.assertNotIn("transition-all", rules_of("// never use transition-all here\n<p />"))

    def test_suppression(self):
        src = "{/* kitlint-ok: click-target pointer shortcut, keys handled on the parent */}\n<div onClick={go}>x</div>"
        self.assertNotIn("click-target", rules_of(src))
        self.assertIn("click-target", rules_of("{/* kitlint-ok: icon-label wrong rule */}\n<div onClick={go}>x</div>"))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            bad = os.path.join(d, "bad.tsx")
            warn = os.path.join(d, "warn.tsx")
            with open(bad, "w") as fh:
                fh.write("<div onClick={go}>x</div>\n")
            with open(warn, "w") as fh:
                fh.write("<AnimatePresence>{x}</AnimatePresence>\n")
            nm = os.path.join(d, "node_modules")
            os.makedirs(nm)
            with open(os.path.join(nm, "x.tsx"), "w") as fh:
                fh.write("<div onClick={go}>x</div>\n")

            def ult(*a):
                return subprocess.run([sys.executable, ULT, "kitlint", *a], capture_output=True, text=True)

            p = ult(bad)
            self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
            self.assertIn("click-target", p.stdout)
            self.assertEqual(ult(warn).returncode, 0)
            self.assertEqual(ult(warn, "--strict").returncode, 1)
            self.assertEqual(ult(os.path.join(d, "missing.tsx")).returncode, 2)
            p = ult(d, "--json")
            self.assertIn('"files": 2', p.stdout)

    def test_stdlib_only(self):
        tree = ast.parse(read(os.path.join(ROOT, "scripts", "ultlib", "kitlint.py")))
        allowed = set(sys.stdlib_module_names) | {"__future__"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    self.assertIn(a.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], allowed)


if __name__ == "__main__":
    unittest.main()
