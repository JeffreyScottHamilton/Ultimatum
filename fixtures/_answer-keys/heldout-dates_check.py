"""Hidden check for h6. Run with cwd=TARGET_DIR. Behaviour table recorded from the untouched fixture."""
import json, os, re, subprocess, sys
from pathlib import Path

root = Path(os.environ.get("TARGET_DIR", ".")).resolve()
sys.path.insert(0, str(root))
from reports.dates import parse_report_date
from schedule.dates import parse_due_date

inputs = ["2024-03-05", "05/03/2024", "5 Mar 2024", "  05   Mar  2024 ", "29/02/2024", "2023-02-29", "soon", "", "2024/03/05",
          "31 Dec 1999", "1 sep 2020", 20240305, None]
def run(fn, x):
    try:
        return ["ok", fn(x).isoformat()]
    except ValueError as e:
        return ["err", str(e)]
    except Exception as e:
        return ["exc", type(e).__name__]
res = {"due": [run(parse_due_date, x) for x in inputs], "report": [run(parse_report_date, x) for x in inputs]}
expected = json.loads((Path(__file__).with_suffix(".expected.json")).read_text())
src = [p for p in root.rglob("*.py") if "tests" not in p.parts and "__pycache__" not in p.parts]
n = sum(len(re.findall(r"strptime\(|fromisoformat\(", p.read_text())) for p in src)
print(json.dumps({"behaviour_unchanged": res == expected, "single_implementation": n == 1,
                  "both_public_names_exist": True}))
