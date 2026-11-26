#!/usr/bin/env python3
"""Summarise a git log for a retro.

Input is the text of:
  git log --no-merges --format='@@%H|%an|%aI|%s' --numstat
read from a file or stdin. Nothing is executed and no network is used.

Exit codes: 0 summary printed, 1 log had no commits, 2 bad usage.
"""
import argparse
import collections
import datetime as dt
import json
import re
import sys
import tempfile
import os

KIND = re.compile(r"^([a-z]+)(\([^)]*\))?!?:")
TEST_PATH = re.compile(r"(^|/)(tests?|spec|__tests__)/|(^|/)test_[^/]+$|_test\.[a-z]+$|\.(test|spec)\.[a-z]+$")


def parse(text):
    commits = []
    cur = None
    for line in text.splitlines():
        if line.startswith("@@"):
            parts = line[2:].split("|", 3)
            if len(parts) != 4:
                continue
            sha, author, when, subject = parts
            try:
                stamp = dt.datetime.fromisoformat(when)
            except ValueError:
                continue
            cur = {"sha": sha, "author": author, "when": stamp, "subject": subject, "files": []}
            commits.append(cur)
        elif cur is not None and line.strip():
            cols = line.split("\t")
            if len(cols) != 3:
                continue
            add, rem, path = cols
            add = int(add) if add.isdigit() else 0  # binary files show "-"
            rem = int(rem) if rem.isdigit() else 0
            cur["files"].append((add, rem, path))
    return commits


def sessions(commits, gap_minutes):
    times = sorted(c["when"] for c in commits)
    out = []
    for t in times:
        if out and (t - out[-1][1]).total_seconds() <= gap_minutes * 60:
            out[-1][1] = t
        else:
            out.append([t, t])
    return out


def streak(commits):
    days = {c["when"].date() for c in commits}
    if not days:
        return 0, None
    end = max(days)
    n, d = 0, end
    while d in days:
        n += 1
        d -= dt.timedelta(days=1)
    return n, end.isoformat()


def bucket(lines):
    if lines < 100:
        return "<100"
    if lines < 500:
        return "100-500"
    if lines < 1500:
        return "500-1500"
    return ">1500"


def summarise(commits, gap):
    kinds = collections.Counter()
    authors = collections.Counter()
    files = collections.Counter()
    tops = collections.Counter()
    sizes = collections.Counter()
    added = removed = test_added = 0
    for c in commits:
        m = KIND.match(c["subject"])
        kinds[m.group(1) if m else "other"] += 1
        authors[c["author"]] += 1
        total = 0
        for a, r, p in c["files"]:
            added += a
            removed += r
            total += a + r
            files[p] += 1
            tops[p.split("/", 1)[0] if "/" in p else "."] += 1
            if TEST_PATH.search(p):
                test_added += a
        sizes[bucket(total)] += 1
    sess = sessions(commits, gap)
    minutes = sum((b - a).total_seconds() / 60 for a, b in sess)
    run, anchor = streak(commits)
    changes = sum(tops.values())
    top_dir, top_n = (tops.most_common(1)[0] if tops else ("-", 0))
    return {
        "commits": len(commits),
        "authors": dict(authors.most_common()),
        "lines_added": added,
        "lines_removed": removed,
        "test_share_pct": round(100 * test_added / added) if added else None,
        "kinds": dict(kinds.most_common()),
        "fix_share_pct": round(100 * kinds["fix"] / len(commits)) if commits else None,
        "sessions": len(sess),
        "single_commit_sessions": sum(1 for a, b in sess if a == b),
        "active_minutes": round(minutes),
        "hotspots": files.most_common(10),
        "size_buckets": {k: sizes[k] for k in ("<100", "100-500", "500-1500", ">1500")},
        "focus": {"dir": top_dir, "pct": round(100 * top_n / changes) if changes else None},
        "streak_days": run,
        "streak_ends": anchor,
    }


SAMPLE = """@@a1|Ana|2026-03-02T09:00:00+00:00|feat: add export
10\t2\tapp/export.py
20\t0\ttests/test_export.py

@@a2|Ana|2026-03-02T09:30:00+00:00|fix: export empty file
3\t1\tapp/export.py

@@a3|Ben|2026-03-03T14:00:00+00:00|docs: usage
-\t-\tdocs/logo.png
5\t0\tREADME.md

@@a4|Ana|2026-03-04T08:00:00+00:00|Refine export
700\t100\tapp/export.py
"""


def self_check():
    s = summarise(parse(SAMPLE), 45)
    assert s["commits"] == 4, s
    assert s["kinds"] == {"feat": 1, "fix": 1, "docs": 1, "other": 1}, s["kinds"]
    assert s["sessions"] == 3 and s["single_commit_sessions"] == 2, s
    assert s["lines_added"] == 738 and s["lines_removed"] == 103, s
    assert s["test_share_pct"] == 3, s
    assert s["hotspots"][0] == ("app/export.py", 3), s["hotspots"]
    assert s["size_buckets"]["500-1500"] == 1 and s["size_buckets"]["<100"] == 3, s
    assert s["focus"]["dir"] == "app", s["focus"]
    assert s["streak_days"] == 3 and s["streak_ends"] == "2026-03-04", s
    assert summarise(parse(SAMPLE), 1)["sessions"] == 4
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "empty.log")
        open(p, "w").close()
        assert main([p]) == 1
    print("self-check ok")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("log", nargs="?", help="log file; '-' or omitted reads stdin")
    ap.add_argument("--gap", type=int, default=45, help="minutes between commits that still count as one session")
    ap.add_argument("--json", action="store_true", help="print JSON")
    ap.add_argument("--self-check", action="store_true")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    if args.self_check:
        return self_check()
    if args.gap <= 0:
        print("--gap must be positive", file=sys.stderr)
        return 2
    if args.log in (None, "-"):
        text = sys.stdin.read()
    else:
        try:
            with open(args.log, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError as e:
            print(f"cannot read {args.log}: {e}", file=sys.stderr)
            return 2
    commits = parse(text)
    if not commits:
        print("no commits in log")
        return 1
    s = summarise(commits, args.gap)
    if args.json:
        print(json.dumps(s, indent=2))
        return 0
    print(f"commits {s['commits']}  authors {len(s['authors'])}  +{s['lines_added']} -{s['lines_removed']}")
    print("kinds " + "  ".join(f"{k} {v}" for k, v in s["kinds"].items()) + f"  (fix share {s['fix_share_pct']}%)")
    print(f"sessions {s['sessions']} ({s['single_commit_sessions']} single-commit), active {s['active_minutes']} min")
    print("sizes " + "  ".join(f"{k} {v}" for k, v in s["size_buckets"].items()))
    ts = s["test_share_pct"]
    print(f"focus {s['focus']['dir']} {s['focus']['pct']}%  test share {'unavailable' if ts is None else str(ts) + '%'}")
    print(f"streak {s['streak_days']} days ending {s['streak_ends']}")
    print("hotspots:")
    for path, n in s["hotspots"]:
        print(f"  {n:3d}  {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
