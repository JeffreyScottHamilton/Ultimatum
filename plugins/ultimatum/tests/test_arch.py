"""Architecture Guardian: `ult arch` and its graph builder."""
from __future__ import annotations

import json
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from _harness import UltCase  # noqa: E402
from ultlib import arch, archgraph  # noqa: E402

DUP_BODY = "\n".join(f"    total_{i} = compute_value(record, field_{i}, default=None) + offset" for i in range(10))


class ArchCase(UltCase):
    def write(self, rel: str, text: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
        return p

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True,
                       env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
                            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
                            "PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(self.root)})

    def report(self, **kw) -> arch.Report:
        return arch.analyze(self.root, **kw)

    def kinds(self, report) -> dict:
        return report.counts()


class Cycles(ArchCase):
    def test_python_relative_import_cycle_is_found(self):
        self.write("pkg/__init__.py", "")
        self.write("pkg/a.py", "from .b import g\n\ndef f():\n    return g()\n")
        self.write("pkg/b.py", "from . import a\n\ndef g():\n    return a\n")
        r = self.report()
        cyc = [f for f in r.findings if f.kind == "cycle"]
        self.assertEqual(len(cyc), 1)
        self.assertEqual(cyc[0].detail, "pkg/a.py -> pkg/b.py -> pkg/a.py")

    def test_js_cycle_through_index_and_extensionless_specifiers(self):
        self.write("src/ui/index.ts", "export { Button } from './button'\n")
        self.write("src/ui/button.tsx", "import { theme } from '../theme'\nexport const Button = () => theme\n")
        self.write("src/theme.ts", "import { Button } from './ui'\nexport const theme = Button\n")
        cyc = [f for f in self.report().findings if f.kind == "cycle"]
        self.assertEqual(len(cyc), 1)
        self.assertIn("src/theme.ts", cyc[0].detail)
        self.assertIn("src/ui/index.ts", cyc[0].detail)

    def test_acyclic_graph_has_no_cycle(self):
        self.write("app/main.py", "from app import util\n")
        self.write("app/util.py", "import os\n")
        self.assertNotIn("cycle", self.kinds(self.report()))

    def test_ambiguous_module_names_are_not_guessed(self):
        # Two `common.py` files: `import common` must not invent an edge to either one.
        self.write("a/common.py", "import b_user\n")
        self.write("b/common.py", "")
        self.write("b_user.py", "import common\n")
        graph, _ = archgraph.build_graph(self.root, arch.source_files(self.root), {
            rel: __import__("ast").parse((self.root / rel).read_text()) for rel in ("a/common.py", "b/common.py", "b_user.py")})
        self.assertEqual(graph["b_user.py"], set())

    def test_tarjan_reports_each_component_once(self):
        g = {"a": {"b"}, "b": {"c"}, "c": {"a"}, "d": {"e"}, "e": {"d"}, "f": set()}
        self.assertEqual(archgraph.cycles(g), [["a", "b", "c"], ["d", "e"]])


class GraphifyMerge(ArchCase):
    def test_only_extracted_import_edges_are_used(self):
        self.write("x.py", "")
        self.write("y.py", "")
        self.write("z.py", "")
        graph = {"nodes": [{"id": "n1", "source_file": "x.py"}, {"id": "n2", "source_file": "y.py"},
                           {"id": "n3", "source_file": "z.py"}],
                 "links": [{"source": "n1", "target": "n2", "relation": "imports", "confidence": "EXTRACTED"},
                           {"source": "n2", "target": "n1", "relation": "imports", "confidence": "EXTRACTED"},
                           {"source": "n2", "target": "n3", "relation": "imports", "confidence": "INFERRED"},
                           {"source": "n3", "target": "n2", "relation": "calls", "confidence": "EXTRACTED"}]}
        self.write("graphify-out/graph.json", json.dumps(graph))
        r = self.report()
        self.assertIn("graphify(2)", r.graph_sources)
        cyc = [f.detail for f in r.findings if f.kind == "cycle"]
        self.assertEqual(cyc, ["x.py -> y.py -> x.py"])

    def test_malformed_graph_is_ignored(self):
        self.write("x.py", "")
        self.write("graphify-out/graph.json", "{not json")
        self.assertEqual(self.report().graph_sources, ["local"])


class Checks(ArchCase):
    def test_duplicate_block_is_reported_once_with_both_locations(self):
        self.write("svc/a.py", f"def a(record):\n{DUP_BODY}\n    return total_1\n")
        self.write("svc/b.py", f"def b(record):\n{DUP_BODY}\n    return total_2\n")
        dups = [f for f in self.report().findings if f.kind == "dup"]
        self.assertEqual(len(dups), 1)
        self.assertEqual(dups[0].path, "svc/a.py")
        self.assertIn("svc/b.py:2-", dups[0].detail)

    def test_short_or_import_only_repeats_are_not_duplicates(self):
        imports = "\n".join(f"import mod{i}" for i in range(12))
        self.write("a.py", imports + "\nx = 1\n")
        self.write("b.py", imports + "\ny = 2\n")
        self.assertNotIn("dup", self.kinds(self.report()))

    def test_sizes_respect_thresholds(self):
        body = "\n".join(f"    v{i} = {i}" for i in range(30))
        self.write("big.py", f"def long_one():\n{body}\n    return v0\n" + "x = 1\n" * 40)
        r = self.report(max_lines=50, max_func=20)
        kinds = {f.kind: f for f in r.findings}
        self.assertIn("size", kinds)
        self.assertEqual(kinds["func-size"].line, 1)
        self.assertNotIn("size", self.kinds(self.report()))  # defaults: 500 / 80

    def test_placeholders_found_but_abstract_methods_and_prose_are_not(self):
        self.write("impl.py", """
            import abc

            class Base(abc.ABC):
                @abc.abstractmethod
                def run(self):
                    raise NotImplementedError

            def later():
                raise NotImplementedError("soon")

            # TODO: wire the cache
            todo_list = "the todo list"
            """)
        self.write("web.ts", "export function f() { throw new Error('Not implemented') }\n")
        stubs = sorted((f.path, f.line) for f in self.report().findings if f.kind == "stub")
        self.assertEqual(stubs, [("impl.py", 9), ("impl.py", 11), ("web.ts", 1)])

    def test_unreferenced_private_function_is_a_lead(self):
        self.write("m.py", "def _unused():\n    return 1\n\ndef _used():\n    return 2\n\nVALUE = _used()\n")
        dead = [f for f in self.report().findings if f.kind == "dead"]
        self.assertEqual([(f.detail, f.lead) for f in dead], [("_unused is never referenced", True)])

    def test_naming_outliers_and_unimportable_python_names(self):
        for n in ("user_service", "order_service", "cart_service"):
            self.write(f"svc/{n}.py", "")
        self.write("svc/paymentService.py", "")
        self.write("tools/load-data.py", "")
        names = sorted((f.path, f.detail) for f in self.report().findings if f.kind == "naming")
        self.assertEqual(names, [("svc/paymentService.py", "camel name in a snake-case directory"),
                                 ("tools/load-data.py", "Python module name contains '-' (not importable)")])

    def test_fixture_dirs_and_excludes_are_skipped(self):
        self.write("tests/fixtures/stub.py", "raise NotImplementedError\n")
        self.write("gen/out.py", "raise NotImplementedError\n")
        self.assertNotIn("stub", self.kinds(self.report(exclude=("gen/*",))))

    def test_typing_ratio_counts_fully_annotated_functions(self):
        self.write("t.py", "def a(x: int) -> int:\n    return x\n\ndef b(x):\n    return x\n")
        self.assertEqual(self.report().typed_ratio, 0.5)


class ChangedAndDrift(ArchCase):
    def setUp(self):
        super().setUp()
        self.git("init", "-q")
        self.write("core/old.py", "raise NotImplementedError\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")

    def test_changed_limits_findings_and_flags_untested_modules(self):
        self.write("core/pricing.py", "def price(x: int) -> int:\n    return x\n")
        r = self.ult("arch", "check", "--changed", "--json")
        data = json.loads(r.out)
        paths = {(f["kind"], f["path"]) for f in data["findings"]}
        self.assertEqual(paths, {("untested", "core/pricing.py")})
        self.write("tests/test_pricing.py", "from core.pricing import price\n")
        data = json.loads(self.ult("arch", "check", "--changed", "--json").out)
        self.assertEqual(data["findings"], [])

    def test_strict_fails_only_on_blocking_kinds(self):
        self.assertEqual(self.ult("arch", "check", "--strict").code, 1)
        self.assertEqual(self.ult("arch", "check", "--strict", "--changed").code, 0)

    def test_baseline_then_drift_shows_only_new_findings(self):
        self.assertEqual(self.ult("arch", "check", "--drift").code, 2)
        self.ult("arch", "baseline")
        self.write("core/new.py", "def f():\n    raise NotImplementedError\n")
        r = self.ult("arch", "check", "--drift")
        self.assertEqual(r.code, 0)
        self.assertIn("core/new.py:2", r.out)
        self.assertNotIn("core/old.py", r.out)

    def test_record_feeds_counts_only_into_observations(self):
        self.write("core/a.py", "from core import b\n")
        self.write("core/b.py", "from core import a\n")
        self.ult("arch", "check", "--record")
        obs = (self.root / ".ultimatum" / "observations.jsonl").read_text()
        rec = json.loads(obs.splitlines()[-1])
        self.assertEqual(rec["category"], "refactor")
        self.assertEqual(rec["signals"], {"arch-cycle": 1, "arch-stub": 1})
        self.assertNotIn("core/", obs)
        self.assertNotIn("NotImplementedError", obs)

    def test_output_is_capped(self):
        for i in range(20):
            self.write(f"core/s{i}.py", "raise NotImplementedError\n")
        lines = self.ult("arch", "check", "--limit", "5").out.splitlines()
        self.assertLessEqual(len(lines), 7)
        self.assertIn("more", lines[-1])


class Deps(ArchCase):
    def setUp(self):
        super().setUp()
        self.write("pkg/__init__.py", "")
        self.write("pkg/core.py", "def base():\n    return 1\n")
        self.write("pkg/mid.py", "from pkg import core\n")
        self.write("pkg/top.py", "from pkg import mid\n")
        self.write("pkg/leaf.py", "from pkg import top\n")

    def lines(self, *args):
        return self.ult("arch", "deps", *args).out.splitlines()

    def test_forward_deps_depth_one_and_two(self):
        self.assertEqual(self.lines("pkg/top.py"), ["deps: pkg/top.py -> 1 (local)", "  pkg/mid.py"])
        out = self.lines("pkg/top.py", "--depth", "2")
        self.assertEqual(out, ["deps: pkg/top.py -> 2 (local)", "  pkg/mid.py (depth 1)",
                               "  pkg/core.py (depth 2)"])

    def test_reverse_lists_importers_as_blast_radius(self):
        self.assertEqual(self.lines("pkg/core.py", "--reverse"), ["deps: pkg/core.py <- 1 (local)", "  pkg/mid.py"])
        out = self.lines("pkg/core.py", "--reverse", "--depth", "3")
        self.assertEqual(out[0], "deps: pkg/core.py <- 3 (local)")
        self.assertEqual(out[1:], ["  pkg/mid.py (depth 1)", "  pkg/top.py (depth 2)", "  pkg/leaf.py (depth 3)"])

    def test_graphify_extracted_import_counts_and_inferred_does_not(self):
        self.write("gx/a.py", "x = 1\n")
        self.write("gx/b.py", "y = 2\n")
        self.write("gx/c.py", "z = 3\n")
        graph = {"nodes": [{"id": "a", "source_file": "gx/a.py"}, {"id": "b", "source_file": "gx/b.py"},
                           {"id": "c", "source_file": "gx/c.py"}],
                 "links": [{"source": "a", "target": "b", "relation": "imports", "confidence": "EXTRACTED"},
                           {"source": "c", "target": "a", "relation": "imports", "confidence": "INFERRED"}]}
        self.write("graphify-out/graph.json", json.dumps(graph))
        self.assertEqual(self.lines("gx/a.py"), ["deps: gx/a.py -> 1 (local+graphify(1))", "  gx/b.py"])
        self.assertEqual(self.lines("gx/c.py"), ["deps: gx/c.py -> 0 (local+graphify(1))"])
        self.assertEqual(self.lines("gx/b.py", "--reverse"), ["deps: gx/b.py <- 1 (local+graphify(1))", "  gx/a.py"])

    def test_limit_caps_output_with_more_line(self):
        for i in range(5):
            self.write(f"fan/m{i}.py", f"from pkg import core\n")
        self.write("fan/hub.py", "".join(f"from fan import m{i}\n" for i in range(5)))
        out = self.lines("fan/hub.py", "--limit", "2")
        self.assertEqual(out[0], "deps: fan/hub.py -> 5 (local)")
        self.assertEqual(out[1:], ["  fan/m0.py", "  fan/m1.py", "  … 3 more (--limit N)"])

    def test_unknown_path_exits_2_with_one_line(self):
        r = self.ult("arch", "deps", "pkg/nothere.py")
        self.assertEqual(r.code, 2)
        self.assertEqual(len(r.out.strip().splitlines()), 1)
        self.assertIn("unknown path: pkg/nothere.py", r.out)

    def test_json_reports_total_and_depths(self):
        data = json.loads(self.ult("arch", "deps", "pkg/top.py", "--depth", "2", "--json").out)
        self.assertEqual(data["total"], 2)
        self.assertEqual(data["deps"], [{"path": "pkg/mid.py", "depth": 1}, {"path": "pkg/core.py", "depth": 2}])


class Activation(unittest.TestCase):
    """The guardian loads for structural work and reviews, never for trivial edits."""

    def addons(self, task):
        from ultlib import route
        return route.decide(task, use_deps=False, lessons_on=False)

    def test_large_route_always_brings_architecture(self):
        d = self.addons("Split the utility layer across the repo into domain packages")
        self.assertEqual(d["route"], "large")
        self.assertIn("architecture", d["addons"])

    def test_structural_words_activate_it_on_other_routes(self):
        for task in ("we have a circular dependency between billing and orders, untangle it",
                     "code review of the new export module: look for duplicated code and dead code"):
            with self.subTest(task=task):
                self.assertIn("architecture", self.addons(task)["addons"])

    def test_trivial_and_security_work_stay_cheap(self):
        for task in ("Fix the typo in the README heading 'Instalation'",
                     "security review of this PR's auth changes, check the refactor of the session code"):
            with self.subTest(task=task):
                self.assertNotIn("architecture", self.addons(task)["addons"])

    def test_architecture_reference_exists_and_is_listed(self):
        d = self.addons("refactor the plugin loader to remove the circular import")
        self.assertIn("architecture.md", " ".join(d.get("read", [])))


if __name__ == "__main__":
    unittest.main()
