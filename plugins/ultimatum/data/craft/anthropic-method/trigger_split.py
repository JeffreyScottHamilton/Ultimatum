#!/usr/bin/env python3
"""Split a trigger query set into train and held-out halves, and score trigger runs against it.

queries.json: [{"query": str, "should_trigger": bool}, ...]
results.json: [{"query": str, "should_trigger": bool, "fired": [bool, ...]}, ...]  # one bool per run

Usage: trigger_split.py split queries.json [--holdout 0.4] [--seed 7]   -> {"train": [...], "test": [...]}
       trigger_split.py score results.json [--split split.json] [--threshold 0.5]
       trigger_split.py --self-check
Exit: 0 printed (score: every query correct), 1 score has misses, 2 bad usage or input.
"""
from __future__ import annotations

import argparse
import json
import sys
from random import Random

HOLDOUT = 0.4  # share of each label kept unseen


def split(items: list[dict], holdout: float, seed: int) -> dict:
    rng = Random(seed)
    train, test = [], []
    for label in (True, False):
        group = [q for q in items if bool(q["should_trigger"]) is label]
        rng.shuffle(group)
        k = round(len(group) * holdout)
        if len(group) >= 2:
            k = min(max(k, 1), len(group) - 1)
        test += group[:k]
        train += group[k:]
    return {"train": train, "test": test}


def score(results: list[dict], threshold: float, test_queries: set[str] | None) -> dict:
    rows = []
    for r in results:
        fired = [bool(x) for x in r["fired"]]
        rate = sum(fired) / len(fired) if fired else 0.0
        ok = (rate >= threshold) == bool(r["should_trigger"])
        part = "test" if test_queries is not None and r["query"] in test_queries else "train"
        rows.append({"query": r["query"], "should_trigger": bool(r["should_trigger"]),
                     "rate": round(rate, 2), "runs": len(fired), "ok": ok, "part": part})
    summary = {}
    for part in ("train", "test"):
        sel = [x for x in rows if x["part"] == part]
        if sel:
            summary[part] = {"correct": sum(x["ok"] for x in sel), "total": len(sel),
                             "missed_should": sum(1 for x in sel if x["should_trigger"] and not x["ok"]),
                             "false_fires": sum(1 for x in sel if not x["should_trigger"] and not x["ok"])}
    return {"summary": summary, "misses": [x for x in rows if not x["ok"]]}


def self_check() -> int:
    qs = [{"query": f"q{i}", "should_trigger": i < 10} for i in range(20)]
    s = split(qs, 0.4, 7)
    assert len(s["test"]) == 8 and len(s["train"]) == 12, s
    assert sum(q["should_trigger"] for q in s["test"]) == 4
    assert split(qs, 0.4, 7) == s, "same seed, same split"
    res = [{"query": "a", "should_trigger": True, "fired": [True, True, False]},
           {"query": "b", "should_trigger": True, "fired": [False, False, True]},
           {"query": "c", "should_trigger": False, "fired": [True, True, False]},
           {"query": "d", "should_trigger": False, "fired": [False, False, False]}]
    out = score(res, 0.5, {"b", "d"})
    assert out["summary"]["train"] == {"correct": 1, "total": 2, "missed_should": 0, "false_fires": 1}, out
    assert out["summary"]["test"] == {"correct": 1, "total": 2, "missed_should": 1, "false_fires": 0}, out
    print("self-check passed: split 20 -> 12/8, score 4 queries")
    return 0


def _load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list) or not all(isinstance(x, dict) and "query" in x and "should_trigger" in x for x in data):
        raise ValueError("expected a list of objects with query and should_trigger")
    return data


def main(argv: list[str]) -> int:
    if argv == ["--self-check"]:
        return self_check()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("split")
    a.add_argument("file")
    a.add_argument("--holdout", type=float, default=HOLDOUT)
    a.add_argument("--seed", type=int, default=7)
    b = sub.add_parser("score")
    b.add_argument("file")
    b.add_argument("--split")
    b.add_argument("--threshold", type=float, default=0.5)
    try:
        args = ap.parse_args(argv)
        items = _load(args.file)
        if args.cmd == "split":
            print(json.dumps(split(items, args.holdout, args.seed), indent=2))
            return 0
        test = None
        if args.split:
            with open(args.split, encoding="utf-8") as fh:
                test = {q["query"] for q in json.load(fh)["test"]}
        out = score(items, args.threshold, test)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2))
    return 0 if not out["misses"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
