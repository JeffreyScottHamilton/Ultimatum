"""`ult run` — run a noisy command, keep the evidence, print only what matters.

Guarantees (tested in tests/test_run.py):
1. The command's exit code is printed and returned unchanged.
2. The full combined stdout+stderr is saved verbatim to .ultimatum/logs/<id>.log
   and can be retrieved exactly with `ult log <id> [--lines A:B | --grep RE]`.
3. Selected lines are printed verbatim with their line numbers (no rewording,
   no summarising of error text). Omitted regions are reported as ranges.
4. Printed output is secret-redacted; the raw log is not (it is local, 0600).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

from .common import dump_json, new_id, redact, sha256_bytes, state_dir, write_private

# --------------------------------------------------------------------------
# Command families. Each has: detector (on argv), "block start" patterns whose
# whole block is evidence, "signal" line patterns, "summary" line patterns, and
# "noise" patterns that are only counted.
# --------------------------------------------------------------------------
F = re.compile

FAMILIES: dict[str, dict] = {
    "unittest": {
        "detect": F(r"\bunittest\b|manage\.py test\b"),
        "block": [F(r"^(FAIL|ERROR): ")],
        "block_end": F(r"^(={20,}|-{20,}\s*$|Ran \d+ tests?)"),
        "signal": [F(r"^Traceback \(most recent call last\)"), F(r"^\w*(Error|Exception)\b.*")],
        "summary": [F(r"^Ran \d+ tests? in"), F(r"^(OK|FAILED)\b.*")],
    },
    "pytest": {
        "detect": F(r"\bpytest\b|\bpy\.test\b"),
        "block": [F(r"^_{3,} .+ _{3,}$")],
        "block_end": F(r"^(_{3,} .+ _{3,}|=+ .+ =+)$"),
        "signal": [F(r"^E\s{2,}"), F(r"^(FAILED|ERROR) "), F(r"^\S+\.py:\d+: \w*(Error|Exception)")],
        "summary": [F(r"^=+ .*\b(passed|failed|error|errors|skipped|xfailed|no tests ran)\b.* =+$"), F(r"^=+ short test summary info =+$")],
    },
    "jest": {
        "detect": F(r"\b(jest|vitest|react-scripts test|bun test)\b|\b(npm|pnpm|yarn)( run)? test\b"),
        "block": [F(r"^\s*● "), F(r"^\s*(FAIL|×|✗|❯) .*(\.test|\.spec)\.[jt]sx?")],
        "block_end": F(r"^\s*(● |PASS |FAIL |Test Suites:|Tests:|⎯{5,})"),
        "signal": [F(r"^\s*(Expected|Received)\b"), F(r"AssertionError"), F(r"^\s*at .+:\d+:\d+\)?$")],
        "summary": [F(r"^\s*(Test Suites|Tests|Snapshots|Time|Test Files|Duration):"), F(r"^\s*(✓|√)?\s*\d+ (passed|failed)")],
    },
    "go": {
        "detect": F(r"^go (test|vet|build)\b"),
        "block": [F(r"^\s*--- FAIL: "), F(r"^panic: ")],
        "block_end": F(r"^\s*(--- (FAIL|PASS|SKIP): |=== RUN |FAIL\s|ok\s)"),
        "signal": [F(r"_test\.go:\d+:"), F(r"\.go:\d+:\d+: ")],
        "summary": [F(r"^(ok|FAIL|---)\s+\S+"), F(r"^FAIL$"), F(r"^PASS$")],
    },
    "cargo": {
        "detect": F(r"^cargo (test|build|check|clippy)\b"),
        "block": [F(r"^error(\[E\d+\])?: "), F(r"^---- .+ stdout ----$")],
        "block_end": F(r"^(\s*$|error(\[E\d+\])?: |warning: |---- .+ stdout ----|failures:)"),
        "signal": [F(r"^\s+--> "), F(r"panicked at")],
        "summary": [F(r"^test result: "), F(r"^error: could not compile"), F(r"^\s*Finished ")],
        "noise": [F(r"^warning: ")],
    },
    "tsc": {
        "detect": F(r"\btsc\b|vue-tsc|type-?check"),
        "block": [],
        "signal": [F(r"error TS\d+:")],
        "summary": [F(r"Found \d+ errors?")],
    },
    "eslint": {
        "detect": F(r"\b(eslint|biome|ruff|flake8|pylint|mypy|golangci-lint|rubocop)\b"),
        "block": [],
        "signal": [F(r"^\s*\d+:\d+\s+(error|warning)\b"), F(r"^\S+:\d+(:\d+)?: (error|E\d|F\d|W\d)"), F(r"\berror\b:")],
        "summary": [F(r"✖ \d+ problems?"), F(r"^Found \d+ errors?"), F(r"^Success: no issues"), F(r"^All checks passed")],
    },
    "install": {
        "detect": F(r"\b(npm|pnpm|yarn|bun) (i|install|ci|add)\b|\bpip3? install\b|\buv (pip|sync|add)\b|\bpoetry (install|add)\b|\bbundle install\b"),
        "block": [F(r"npm (ERR!|error) ")],
        "block_end": F(r"^(?!npm (ERR!|error))"),
        "signal": [F(r"\bERESOLVE\b|\bE404\b|\bEACCES\b|\bENOTFOUND\b"), F(r"^ERROR: "), F(r"Could not (find|build)")],
        "summary": [F(r"^(added|removed|changed|up to date)\b"), F(r"\b\d+ vulnerabilit"), F(r"^Successfully installed"), F(r"^Done in")],
        "noise": [F(r"\bWARN\b.*deprecated|npm warn deprecated")],
    },
    "git": {
        "detect": F(r"^git (log|diff|show|status|blame)\b"),
        "block": [],
        "signal": [F(r"^(diff --git|@@ |\+\+\+ |--- )"), F(r"^commit [0-9a-f]{7,}"), F(r"^(fatal|error): ")],
        "summary": [F(r"^\s*\d+ files? changed")],
    },
}

GENERIC_SIGNAL = [
    F(r"(?i)\b(error|errors|failed|failure|failing|fatal|panic|exception|traceback|assert(ion)?error|segmentation fault|denied|refused|timed? ?out|not found|cannot|could not|unable to)\b"),
]
GENERIC_NOISE = [F(r"(?i)\b(deprecat\w*|warn(ing)?)\b")]


CONTENT_SNIFF = [
    ("pytest", F(r"^=+ test session starts =+$", re.M)),
    ("unittest", F(r"^Ran \d+ tests? in [\d.]+s$", re.M)),
    ("jest", F(r"^\s*(Test Suites|Test Files):", re.M)),
    ("go", F(r"^(--- FAIL: |ok\s+\S+\s+[\d.]+s)", re.M)),
    ("cargo", F(r"^test result: ", re.M)),
    ("tsc", F(r"error TS\d+:")),
]


def detect_family(argv: list[str], text: str = "") -> str:
    joined = " ".join(argv)
    for name, fam in FAMILIES.items():
        if fam["detect"].search(joined):
            return name
    for name, pat in CONTENT_SNIFF:  # e.g. `python3 run_tests.py`, `make test`
        if pat.search(text):
            return name
    return "generic"


def _merge(ranges: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    """Merge overlapping [a,b] inclusive line ranges; keep highest-priority tag."""
    prio = {"summary": 0, "block": 1, "signal": 2, "tail": 3, "head": 4}
    out: list[list] = []
    for a, b, tag in sorted(ranges):
        if out and a <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], b)
            if prio[tag] < prio[out[-1][2]]:
                out[-1][2] = tag
        else:
            out.append([a, b, tag])
    return [tuple(x) for x in out]


def select(lines: list[str], family: str, max_lines: int = 80, tail: int = 12, context: int = 2):
    """Return (ranges, noise_counts, failure_headers).

    ranges: list of (start, end, tag) 0-based inclusive, verbatim to print.
    """
    fam = FAMILIES.get(family, {})
    n = len(lines)
    blocks: list[tuple[int, int, str]] = []
    signals: list[tuple[int, int, str]] = []
    summaries: list[tuple[int, int, str]] = []
    headers: list[tuple[int, str]] = []
    noise = Counter()
    noise_pats = fam.get("noise", []) + GENERIC_NOISE
    sig_pats = fam.get("signal", []) + (GENERIC_SIGNAL if family == "generic" else [])

    i = 0
    while i < n:
        line = lines[i]
        if any(p.search(line) for p in fam.get("block", [])):
            j = i + 1
            end_pat = fam.get("block_end")
            while j < n and j - i < 60 and not (end_pat and end_pat.search(lines[j]) and j > i + 1):
                j += 1
            blocks.append((i, j - 1, "block"))
            headers.append((i, line.strip()))
            i = j
            continue
        if any(p.search(line) for p in fam.get("summary", [])):
            summaries.append((i, i, "summary"))
        elif any(p.search(line) for p in sig_pats):
            signals.append((max(0, i - context), min(n - 1, i + context), "signal"))
        elif any(p.search(line) for p in noise_pats):
            key = re.sub(r"\d+", "N", line.strip())[:100]
            noise[key] += 1
        i += 1

    chosen: list[tuple[int, int, str]] = []
    budget = max_lines

    def take(rs):
        nonlocal budget
        for a, b, tag in rs:
            size = b - a + 1
            if budget <= 0:
                return
            if size > budget:
                b = a + budget - 1
                size = budget
            chosen.append((a, b, tag))
            budget -= size

    take(summaries)
    tail_r = (max(0, n - tail), n - 1, "tail") if n else None
    if tail_r:
        budget -= tail_r[1] - tail_r[0] + 1
    take(blocks)
    take(signals)
    if tail_r:
        chosen.append(tail_r)
    if n and n <= max_lines:  # small output: show everything verbatim
        chosen = [(0, n - 1, "head")]
    return _merge(chosen), noise, headers


def render(lines, ranges, noise, headers, meta) -> str:
    out = []
    shown = sum(b - a + 1 for a, b, _ in ranges)
    out.append(
        f"[ult run] exit={meta['exit_code']} duration={meta['duration_s']}s family={meta['family']} "
        f"lines={meta['lines']} shown={shown} log={meta['id']}"
    )
    out.append(f"[ult run] cmd: {meta['cmd']}")
    prev = -1
    for a, b, tag in ranges:
        if a > prev + 1:
            out.append(f"  … L{prev + 2}-L{a} omitted ({a - prev - 1} lines)")
        out.append(f"--- L{a + 1}-L{b + 1} [{tag}]")
        for k in range(a, b + 1):
            out.append(lines[k])
        prev = b
    if prev < len(lines) - 1 and lines:
        out.append(f"  … L{prev + 2}-L{len(lines)} omitted ({len(lines) - prev - 1} lines)")
    if len(headers) > 0:
        listed = [h for h in headers if not any(a <= h[0] <= b for a, b, _ in ranges)]
        if listed:
            out.append(f"[ult run] {len(listed)} more failure block(s) not shown:")
            for ln, h in listed[:20]:
                out.append(f"  L{ln + 1}: {h}")
    if noise:
        total = sum(noise.values())
        out.append(f"[ult run] counted {total} warning/noise line(s); top:")
        for k, v in noise.most_common(3):
            out.append(f"  ×{v} {k}")
    out.append(f"[ult run] raw: ult log {meta['id']} --lines A:B | --grep RE  (exact output)")
    return redact("\n".join(out))


def cmd_run(args) -> int:
    argv = args.command
    if argv and argv[0] == "--":
        argv = argv[1:]
    if not argv:
        print("usage: ult run [--max-lines N] [--shell] -- <command> [args...]", file=sys.stderr)
        return 2
    logs = state_dir(sub="logs")
    rid = new_id(args.name or "run")
    if args.shell:
        popen_argv = ["bash", "-c", " ".join(argv)]
        display = " ".join(argv)
    else:
        popen_argv = argv
        display = shlex.join(argv)
    t0 = time.time()
    chunks: list[bytes] = []
    try:
        proc = subprocess.Popen(popen_argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=args.cwd or None)
    except FileNotFoundError as e:
        print(f"[ult run] exit=127 command not found: {e.filename}", file=sys.stderr)
        return 127
    timed_out = False
    try:
        out, _ = proc.communicate(timeout=args.timeout)
        chunks.append(out or b"")
    except subprocess.TimeoutExpired:
        proc.kill()
        out, _ = proc.communicate()
        chunks.append(out or b"")
        timed_out = True
    raw = b"".join(chunks)
    code = proc.returncode if not timed_out else 124
    text = raw.decode("utf-8", "replace")
    lines = text.splitlines()
    family = args.family or detect_family(argv, text)
    meta = {
        "id": rid,
        "cmd": display,
        "argv": popen_argv,
        "cwd": str(Path(args.cwd or os.getcwd()).resolve()),
        "exit_code": code,
        "timed_out": timed_out,
        "duration_s": round(time.time() - t0, 2),
        "family": family,
        "lines": len(lines),
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "started": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t0)),
    }
    write_private(logs / f"{rid}.log", raw)
    write_private(logs / f"{rid}.json", dump_json(meta))
    ranges, noise, headers = select(lines, family, max_lines=args.max_lines)
    print(render(lines, ranges, noise, headers, meta))
    try:  # best-effort index for `ult find`
        from .store import index_log
        index_log(rid, lines, meta)
    except Exception as e:  # pragma: no cover - index is optional
        print(f"[ult run] note: search index not updated ({e.__class__.__name__})", file=sys.stderr)
    return code


def _resolve_log(lid: str) -> Path:
    logs = state_dir(sub="logs")
    if lid == "last":
        metas = sorted(logs.glob("*.json"), key=lambda p: p.stat().st_mtime)
        if not metas:
            raise SystemExit("no logs yet")
        return metas[-1].with_suffix(".log")
    p = logs / f"{lid}.log"
    if not p.exists():
        cands = sorted(logs.glob(f"*{lid}*.log"))
        if len(cands) == 1:
            return cands[0]
        raise SystemExit(f"log not found: {lid}")
    return p


def cmd_log(args) -> int:
    p = _resolve_log(args.id)
    lines = p.read_text("utf-8", "replace").splitlines()
    if args.meta:
        print(p.with_suffix(".json").read_text())
        return 0
    sel: list[int]
    if args.lines:
        a, _, b = args.lines.partition(":")
        a = max(1, int(a or 1))
        b = min(len(lines), int(b or len(lines)))
        sel = list(range(a - 1, b))
    elif args.grep:
        pat = re.compile(args.grep)
        hits = [i for i, l in enumerate(lines) if pat.search(l)]
        keep = set()
        for h in hits:
            keep.update(range(max(0, h - args.context), min(len(lines), h + args.context + 1)))
        sel = sorted(keep)
        print(f"[ult log] {len(hits)} match(es) for /{args.grep}/ in {p.stem}")
    else:
        sel = list(range(len(lines)))
    prev = None
    for i in sel:
        if prev is not None and i != prev + 1:
            print("--")
        text = lines[i] if args.raw else redact(lines[i])
        print(f"{i + 1}\t{text}" if args.number else text)
        prev = i
    return 0


def cmd_logs(args) -> int:
    logs = state_dir(sub="logs")
    metas = sorted(logs.glob("*.json"), key=lambda p: p.stat().st_mtime)[-args.limit:]
    for m in metas:
        try:
            d = json.loads(m.read_text())
        except json.JSONDecodeError:
            continue
        print(f"{d['id']}  exit={d['exit_code']}  lines={d['lines']}  {redact(d['cmd'])[:100]}")
    return 0


def register(sub):
    p = sub.add_parser("run", help="run a command; print exit code + key failure lines; save raw log")
    p.add_argument("--max-lines", type=int, default=80)
    p.add_argument("--name", help="id prefix, e.g. 'tests'")
    p.add_argument("--family", choices=sorted(FAMILIES) + ["generic"], help="override output family")
    p.add_argument("--timeout", type=float, default=None, help="seconds; exit 124 on timeout")
    p.add_argument("--cwd")
    p.add_argument("--shell", action="store_true", help="run through bash -c (pipes, &&); explicit opt-in")
    p.add_argument("command", nargs=argparse.REMAINDER)
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("log", help="print a saved log exactly (by id or 'last')")
    p.add_argument("id")
    p.add_argument("--lines", help="A:B, 1-based inclusive")
    p.add_argument("--grep", help="regex; prints matches with context")
    p.add_argument("--context", type=int, default=3)
    p.add_argument("-n", "--number", action="store_true", help="prefix line numbers")
    p.add_argument("--raw", action="store_true", help="do not redact (local terminal use only)")
    p.add_argument("--meta", action="store_true", help="print the run's metadata JSON")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("logs", help="list recent runs")
    p.add_argument("--limit", type=int, default=15)
    p.set_defaults(func=cmd_logs)
