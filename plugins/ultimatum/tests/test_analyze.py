import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "analyze", Path(__file__).resolve().parents[3] / "evals" / "live" / "analyze.py")
analyze = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyze)


def pair(i, name, inp, content):
    return [
        {"type": "assistant", "message": {"id": f"m{i}", "usage": {"input_tokens": 3, "cache_read_input_tokens": 10,
                                                                    "cache_creation_input_tokens": 7},
                                          "content": [{"type": "tool_use", "id": f"t{i}", "name": name, "input": inp}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": f"t{i}", "content": content}]}},
    ]


class TestAnalyze(unittest.TestCase):
    def test_metrics(self):
        calls = [("Bash", {"command": "sleep 20"}, "ok"), ("Monitor", {}, "ok"),
                 ("Bash", {"command": "pytest -q"}, "x" * 9000),
                 ("Bash", {"command": "python3 ult run -- pytest -q"}, "ok"),
                 ("Bash", {"command": "python3 /p/ult route"}, "route: bug"),
                 ("Read", {"file_path": "/a/skills/work/references/x.md"}, "ok"),
                 ("Read", {"file_path": "/a/skills/work/references/x.md"}, "ok"),
                 ("Agent", {"run_in_background": True}, "ok")]
        entries = []
        for i, (n, inp, out) in enumerate(calls):
            entries += pair(i, n, inp, out)
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "c1__armA.jsonl").write_text("\n".join(json.dumps(e) for e in entries))
            res = analyze.analyze_dir(Path(d))
            m = res["armA"]["c1"]
            self.assertEqual(m["first_ctx"], 20)
            self.assertEqual(m["cache_creation"], 7 * len(calls))
            self.assertEqual(m["polls"], 2)
            self.assertEqual((m["tests_raw"], m["tests_ult"]), (1, 1))
            self.assertEqual(m["routes"], 1)
            self.assertEqual((m["ref_reads"], m["rereads"], m["bg_agents"]), (2, 1, 1))
            self.assertEqual(m["largest"][0], 9000)
            self.assertIn("raw-test", [w[0] for w in analyze.waste_list(res["armA"])] + [w[0] for w in m["waste"]])
            self.assertIn("| armA |", analyze.render(res))
            self.assertEqual(analyze.analyze_dir(Path(d), ["other"]), {})


if __name__ == "__main__":
    unittest.main()
