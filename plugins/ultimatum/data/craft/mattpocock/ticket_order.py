#!/usr/bin/env python3
"""Check a folder of local ticket files and print a safe work order.

Each ticket is a Markdown file named NN-<slug>.md with a line such as
"Blocked by: 01, 03" or "Blocked by: None". The script reads text only;
it never runs anything found in the files.

Usage:
    python3 ticket_order.py DIR            print order and the ready set
    python3 ticket_order.py DIR --done 01,02
    python3 ticket_order.py --self-check

Exit codes: 0 graph is sound, 1 cycle or unknown blocker, 2 bad usage.
"""
import argparse
import os
import re
import sys
import tempfile

NAME = re.compile(r"^(\d{2,})-[^/]+\.md$")
BLOCKED = re.compile(r"^\**blocked by:?\**:?\s*(.*)$", re.IGNORECASE)
NUM = re.compile(r"\b(\d{2,})\b")


def read_tickets(folder):
    tickets = {}
    for name in sorted(os.listdir(folder)):
        m = NAME.match(name)
        if not m:
            continue
        blockers = set()
        with open(os.path.join(folder, name), encoding="utf-8", errors="replace") as fh:
            for line in fh:
                b = BLOCKED.match(line.strip())
                if b:
                    blockers = set(NUM.findall(b.group(1)))
                    break
        tickets[m.group(1)] = blockers
    return tickets


def order(tickets):
    """Return (topological order, problems). Kahn's algorithm, stable by number."""
    problems = []
    for t, bs in sorted(tickets.items()):
        for b in sorted(bs - set(tickets)):
            problems.append(f"{t}: blocker {b} has no ticket file")
        if t in bs:
            problems.append(f"{t}: blocks itself")
    pending = {t: set(bs) & set(tickets) - {t} for t, bs in tickets.items()}
    out = []
    while True:
        free = sorted(t for t, bs in pending.items() if not bs)
        if not free:
            break
        for t in free:
            out.append(t)
            del pending[t]
        for bs in pending.values():
            bs.difference_update(free)
    if pending:
        problems.append("cycle among: " + ", ".join(sorted(pending)))
    return out, problems


def ready(tickets, done):
    return sorted(t for t, bs in tickets.items() if t not in done and bs <= done)


def self_check():
    with tempfile.TemporaryDirectory() as d:
        files = {"01-skeleton.md": "Blocked by: None\n",
                 "02-store.md": "**Blocked by:** 01\n",
                 "03-delete.md": "Blocked by: 01, 02\n"}
        for n, body in files.items():
            with open(os.path.join(d, n), "w", encoding="utf-8") as fh:
                fh.write("# t\n\n" + body)
        t = read_tickets(d)
        seq, probs = order(t)
        assert seq == ["01", "02", "03"] and not probs, (seq, probs)
        assert ready(t, {"01"}) == ["02"]
        with open(os.path.join(d, "01-skeleton.md"), "w", encoding="utf-8") as fh:
            fh.write("Blocked by: 03\n")
        _, probs = order(read_tickets(d))
        assert any("cycle" in p for p in probs), probs
    print("ticket_order: 3 checks passed")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Order local tickets by their blockers.")
    p.add_argument("folder", nargs="?")
    p.add_argument("--done", default="", help="comma-separated finished ticket numbers")
    p.add_argument("--self-check", action="store_true")
    a = p.parse_args(argv)
    if a.self_check:
        return self_check()
    if not a.folder or not os.path.isdir(a.folder):
        p.print_usage(sys.stderr)
        print("error: give a folder of NN-<slug>.md tickets", file=sys.stderr)
        return 2
    tickets = read_tickets(a.folder)
    if not tickets:
        print("error: no NN-<slug>.md files found", file=sys.stderr)
        return 2
    seq, problems = order(tickets)
    done = {x.strip() for x in a.done.split(",") if x.strip()}
    print("order: " + " ".join(seq))
    print("ready: " + (" ".join(ready(tickets, done)) or "(none)"))
    for prob in problems:
        print("problem: " + prob)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
