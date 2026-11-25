"""Hidden check for h1. Runs the CLI in TARGET_DIR on generated rows and compares with exact Decimal math.
Rounding rule is half up (stated in the README). Prints a JSON dict of checks."""
import csv, json, os, random, subprocess, sys, tempfile
from decimal import Decimal as D, ROUND_FLOOR

target = os.environ.get("TARGET_DIR", ".")
random.seed(1)
rows, ok_sets = [], []
for i in range(2000):
    p = f"{random.randint(1, 5000) / 100:.2f}"; q = random.randint(1, 9)
    t = random.choice(["0", "5", "7.5", "8.25", "10", "19", "20"])
    exact = D(p) * q * (1 + D(t) / 100) * 100
    lo = int(exact.to_integral_value(rounding=ROUND_FLOOR))
    frac = exact - lo
    ok = {lo + 1} if frac >= D("0.5") else {lo}  # documented rule: round half up
    rows.append((f"S{i}", p, q, t)); ok_sets.append(ok)
with tempfile.TemporaryDirectory() as d:
    path = os.path.join(d, "in.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["sku", "unit_price", "qty", "tax_pct"]); w.writerows(rows)
    r = subprocess.run([sys.executable, "-m", "billing", path], cwd=target, capture_output=True, text=True)
res = {"cli_runs": r.returncode == 0}
try:
    lines = [l.split(",") for l in r.stdout.strip().splitlines()]
    got = {k: int(D(v) * 100) for k, v in lines[:-1]}
    res["rows_correct"] = len(got) == len(rows) and all(got[s] in ok for (s, *_), ok in zip(rows, ok_sets))
    tot = int(D(lines[-1][1]) * 100)
    res["grand_total_correct"] = lines[-1][0] == "TOTAL" and abs(tot - sum(got.values())) == 0 and res["rows_correct"]
except Exception:
    res.update(rows_correct=False, grand_total_correct=False)
print(json.dumps(res))
