#!/usr/bin/env python3
"""Live A/B evaluation of Ultimatum against plain Claude Code.

Each case copies a fixture to a fresh git workspace and runs a headless
`claude -p` session twice under the same settings:
  arm "ultimatum": prompt prefixed with `/ultimatum:work`, plugin loaded via --plugin-dir
  arm "baseline" : same prompt text, no plugin
Both arms use an isolated CLAUDE_CONFIG_DIR (no user skills, plugins, hooks or
MCP servers), the same model, the same tool allowlist and the same budget cap.
Graders are deterministic Python checks against the fixture's answer key
(tests, exploit scripts, an independent Playwright probe, diff scope). Correctness
is recorded first; tokens/cost/turns/subagents are recorded second.

usage: python3 evals/live/run_live.py [--cases a,b] [--arms ultimatum,baseline]
                                      [--model sonnet] [--budget 3] [--out DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FIX = REPO / "fixtures"
KEYS = FIX / "_answer-keys"
PLUGIN = REPO / "plugins" / "ultimatum"
TOOLS = "Bash Read Edit Write Glob Grep Agent Skill TodoWrite"


def sh(cmd, cwd, env=None, timeout=300):
    r = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True,
                       timeout=timeout, env={**os.environ, **(env or {})})
    return r.returncode, r.stdout + r.stderr


def changed_files(ws: Path) -> list[str]:
    _, out = sh(["git", "status", "--porcelain", "-uall"], ws)
    files = []
    for line in out.splitlines():
        p = line[3:].split(" -> ")[-1].strip().strip('"')
        if not p.startswith(".ultimatum/") and "__pycache__" not in p:
            files.append(p)
    return files


def text_of(ws: Path, files: list[str]) -> str:
    out = []
    for f in files:
        p = ws / f
        if p.is_file():
            try:
                out.append(p.read_text("utf-8", "replace"))
            except OSError:
                pass
    return "\n".join(out)


def near(text: str, anchor: str, words: list[str], width: int = 500) -> bool:
    for m in re.finditer(re.escape(anchor), text, re.I):
        win = text[max(0, m.start() - width): m.end() + width].lower()
        if any(w in win for w in words):
            return True
    return False


# ----------------------------------------------------------------- graders
def g_one_file(ws, run):
    rc, _ = sh("python3 -m unittest", ws)
    ch = changed_files(ws)
    return {
        "tests_pass": rc == 0,
        "only_slugify_changed": bool(ch) and all(f == "textkit/slugify.py" or "test" in f for f in ch),
        "no_delegation": run["tools"].get("Agent", 0) == 0 and run["tools"].get("Task", 0) == 0,
        "no_plan_docs": not any(f.endswith(".md") for f in ch),
    }


def g_unfamiliar(ws, run):
    rc, _ = sh("python3 -m unittest", ws)
    rc2, out = sh("python3 -m billing.cli summary", ws)
    ch = changed_files(ws)
    code = text_of(ws, [f for f in ch if f.endswith(".py")])
    return {
        "tests_pass": rc == 0,
        "summary_runs": rc2 == 0,
        "amounts_correct": all(a in out for a in ("$1,999.50", "€49.99", "$0.00")),
        "reuses_format_money": "format_money" in code,
        "reuses_outstanding_for": "outstanding_for" in code,
        "no_legacy_decoy": "old_money" not in code,
        "test_added": any("test" in f for f in ch),
    }


def g_noisy(ws, run):
    rc, _ = sh("python3 -m unittest", ws)
    ch = changed_files(ws)
    raw_ok = False
    logs = ws / ".ultimatum" / "logs"
    if logs.is_dir():
        raw_ok = any("1234.5 != 1234.56" in p.read_text("utf-8", "replace") for p in logs.glob("*.log"))
    return {
        "tests_pass": rc == 0,
        "fixed_in_parse": "pipeline/parse.py" in ch,
        "tests_not_edited": not any(f.startswith("tests/") for f in ch),
        "key_failure_quoted": "1234.5 != 1234.56" in run["transcript_text"],
        "raw_output_recoverable": raw_ok,
    }


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def g_ui(ws, run):
    rc, _ = sh("python3 -m unittest", ws)
    app = (ws / "app.js").read_text("utf-8", "replace")
    port = free_port()
    srv = subprocess.Popen([sys.executable, "serve.py", str(port)], cwd=ws, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(0.8)
        _, out = sh(["node", str(REPO / "evals/live/ui_probe.mjs"), f"http://127.0.0.1:{port}/"], ws, timeout=120)
    finally:
        srv.terminate()
    try:
        probe = json.loads(out.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        probe = {"checks": {"probe_ran": False}, "notes": [out[-500:]]}
    t = run["tool_inputs_text"]
    res = {
        "tests_pass": rc == 0,
        "reuses_dialog": "Dialog.open" in app,
        "reuses_toast": "Toast.show" in app,
        "reuses_button": "Button.create" in app,
        "no_native_confirm": not re.search(r"(?<![.\w])confirm\(", app),
        "agent_checked_two_viewports": ("375" in t or "390" in t) and ("1280" in t or "1440" in t or "1024" in t),
        "agent_ran_real_browser": bool(re.search(r"playwright|ult-browser|chromium", t, re.I)),
    }
    res.update({f"probe_{k}": v for k, v in probe["checks"].items()})
    run["probe_notes"] = probe.get("notes", [])
    return res


SECURE_PROBE = r'''
import io, json, sys
sys.path.insert(0, ".")
from docs_app.server import app
from docs_app import storage
if hasattr(storage, "reset"): storage.reset()
if hasattr(storage, "seed"): storage.seed()
def call(path, tok=None):
    env = {"REQUEST_METHOD": "GET", "PATH_INFO": path, "wsgi.input": io.BytesIO(b""), "CONTENT_LENGTH": "0", "QUERY_STRING": ""}
    if tok: env["HTTP_AUTHORIZATION"] = "Bearer " + tok
    st = {}
    body = b"".join(app(env, lambda s, h: st.setdefault("s", s)))
    return int(st["s"].split()[0]), body.decode("utf-8", "replace")
own = call("/api/documents/1/download", "tok-alice")
cross = call("/api/documents/1/download", "tok-bob")
anon = call("/api/documents/1/download")
missing = call("/api/documents/999/download", "tok-alice")
print(json.dumps({"own": own, "cross": cross, "anon": anon, "missing": missing}))
'''


def g_secure(ws, run):
    rc, _ = sh("python3 -m unittest", ws)
    _, out = sh([sys.executable, "-c", SECURE_PROBE], ws)
    try:
        r = json.loads(out.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        r = None
    ch = changed_files(ws)
    tests = text_of(ws, [f for f in ch if "test" in f])
    secret = "alice private notes"
    return {
        "tests_pass": rc == 0,
        "probe_ran": r is not None,
        "owner_gets_200_content": bool(r) and r["own"][0] == 200 and secret in r["own"][1],
        "cross_account_blocked": bool(r) and r["cross"][0] in (403, 404) and secret not in r["cross"][1],
        "unauthenticated_401": bool(r) and r["anon"][0] == 401,
        "missing_404": bool(r) and r["missing"][0] == 404,
        "test_covers_cross_account": "download" in tests and ("tok-bob" in tests or "acct-2" in tests or "bob" in tests),
        "test_covers_authorized": "download" in tests and ("tok-alice" in tests or "alice" in tests),
    }


def g_audit(ws, run):
    ch = changed_files(ws)
    text = run["transcript_text"] + "\n" + text_of(ws, [str(p.relative_to(ws)) for p in (ws / ".ultimatum").rglob("*")
                                                         if p.suffix in (".md", ".json")] if (ws / ".ultimatum").exists() else [])
    low = text.lower()
    reject_words = ["reject", "false positive", "not exploitable", "allowlist", "allow-list", "whitelist", "not vulnerable",
                    "safe", "not a vulnerability", "not injectable", "mitigated"]
    findings = ws / ".ultimatum" / "security" / "findings.json"
    return {
        "read_only": not [f for f in ch if not f.startswith(".ultimatum")],
        "idor_confirmed": near(text, "invoices.py", ["idor", "tenant", "bola", "639", "authoriz", "cross-tenant"]),
        "sqli_lead_rejected_or_qualified": near(text, "reports.py", reject_words) or near(text, "order by", reject_words),
        "demo_key_not_confirmed": ("demo-key-not-secret" not in text) or near(text, "demo-key-not-secret", reject_words + ["test", "placeholder"]),
        "coverage_recorded": "coverage" in low or "ledger" in low,
        "structured_findings_file": findings.exists(),
        "states_missing_scanners": bool(re.search(r"(semgrep|gitleaks|osv)[^\n]{0,80}(not (installed|available|present|run)|unavailable|absent)|"
                                              r"(not (installed|available|run))[^\n]{0,60}(semgrep|gitleaks|osv)|advisor\w*[^\n]{0,40}(unknown|not checked)", low)),
    }


def g_remediation(ws, run):
    rc, _ = sh("python3 -m unittest", ws)
    rc_x, xout = sh([sys.executable, str(KEYS / "remediation_exploit.py")], ws, env={"TARGET_DIR": str(ws)})
    legit = r'''
import json, sys
sys.path.insert(0, ".")
from invoicer.app import create_app
from tests import fixtures as f
app = create_app(f.build_conn())
tok_a = getattr(f, "DEMO_API_KEY", None) or getattr(f, "TOKEN_A")
s1, b1 = f.call(app, "GET", "/api/invoices/2", tok_a)
s2, b2 = f.call(app, "PUT", "/api/invoices/2", tok_a, {"customer": "ok", "amount_cents": 5})
print(json.dumps([s1, s2]))
'''
    _, lout = sh([sys.executable, "-c", legit], ws)
    try:
        s1, s2 = json.loads(lout.strip().splitlines()[-1])
    except Exception:
        s1 = s2 = None
    ch = changed_files(ws)
    tests = text_of(ws, [f for f in ch if "test" in f])
    return {
        "tests_pass": rc == 0,
        "exploit_blocked_get_and_put": rc_x == 1,
        "same_tenant_get_200": s1 == 200,
        "same_tenant_put_200": s2 == 200,
        "regression_test_added": bool(tests) and ("TOKEN_B" in tests or "tenant" in tests.lower()),
        "regression_covers_put": "PUT" in tests,
    }


def g_large(ws, run):
    rc, _ = sh("python3 -m unittest", ws)
    db = ws / "_probe_notes.json"
    sh(["python3", "-m", "notes", "--db", str(db), "add", "Hello, world", "--body", 'a "quoted"\nline', "--tags", "x,y"], ws)
    res = {}
    for fmt in ("md", "json", "csv"):
        r, out = sh(["python3", "-m", "notes", "--db", str(db), "export", "--format", fmt], ws)
        res[f"export_{fmt}_runs"] = r == 0 and "Hello" in out
    rb, _ = sh(["python3", "-m", "notes", "--db", str(db), "export", "--format", "bogus"], ws)
    db.unlink(missing_ok=True)
    readme = (ws / "README.md").read_text("utf-8", "replace") if (ws / "README.md").exists() else ""
    return {
        "tests_pass": rc == 0,
        **res,
        "bogus_format_fails": rb != 0,
        "readme_documents_export": "export" in readme.lower(),
        "parallel_workers_used": run["agent_calls"] >= 2,
        "integrated_review": bool(re.search(r"review", " ".join(run["agent_types"] + run["agent_descriptions"]), re.I)),
    }


def g_handoff(ws, run):
    rc, _ = sh("python3 -m unittest", ws)
    ch = changed_files(ws)
    return {
        "tests_pass": rc == 0,
        "scope_kept": bool(ch) and all(f in ("ratelimit/config.py", "ratelimit/limiter.py") for f in ch),
        "tests_not_edited": not any(f.startswith("tests/") for f in ch),
        "read_handoff": "handoff" in run["tool_inputs_text"].lower(),
    }


CASES = {
    "1-one-file": ("one-file", "slugify drops digits; fix it.", g_one_file),
    "2-unfamiliar": ("unfamiliar-repo", "Add a `summary` CLI subcommand that prints each customer's outstanding total formatted as money.", g_unfamiliar),
    "3-noisy": ("noisy-test", "The test suite is failing. Find the cause and fix it.", g_noisy),
    "4-ui": ("ui-app", "Add a Delete action on each project row with a confirmation dialog; deleting removes the row and shows a toast. Verify it works in a real browser at a phone and a desktop width.", g_ui),
    "5-secure-feature": ("secure-feature", "Add GET /api/documents/<id>/download returning the file content.", g_secure),
    "6-audit": ("audit-target", "Perform a security audit of this repository. You are authorized to review the code and run its local tests; do not modify files. Report confirmed vulnerabilities, leads you rejected and why, and what you covered.", g_audit),
    "7-remediation": ("remediation", "Fix the invoice IDOR.", g_remediation),
    "8-large": ("large-feature", "Add export to Markdown, JSON, and CSV (`notes export --format md|json|csv`), each with tests, plus docs in README. Use parallel subagents for the three exporters and review the integrated result.", g_large),
    "9-handoff": ("handoff", "Resume the work.", g_handoff),
}


def parse_stream(lines: list[str]) -> dict:
    tools, inputs, texts, agent_types, agent_desc = {}, [], [], [], []
    result = {}
    for line in lines:
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "assistant":
            for c in d.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    tools[c["name"]] = tools.get(c["name"], 0) + 1
                    inp = c.get("input", {})
                    inputs.append(json.dumps(inp))
                    if c["name"] in ("Agent", "Task"):
                        agent_types.append(str(inp.get("subagent_type", "")))
                        agent_desc.append(str(inp.get("description", "")))
                elif c.get("type") == "text":
                    texts.append(c.get("text", ""))
        elif d.get("type") == "user":
            for c in d.get("message", {}).get("content", []) if isinstance(d.get("message", {}).get("content"), list) else []:
                if c.get("type") == "tool_result":
                    cc = c.get("content")
                    texts.append(cc if isinstance(cc, str) else json.dumps(cc)[:20000])
        elif d.get("type") == "result":
            result = d
    return {
        "tools": tools, "tool_inputs_text": "\n".join(inputs), "transcript_text": "\n".join(texts),
        "agent_calls": tools.get("Agent", 0) + tools.get("Task", 0), "agent_types": agent_types,
        "agent_descriptions": agent_desc, "final": result.get("result", ""),
        "is_error": result.get("is_error"), "num_turns": result.get("num_turns"),
        "duration_ms": result.get("duration_ms"), "cost_usd": result.get("total_cost_usd"),
        "usage": result.get("usage", {}), "model_usage": result.get("modelUsage", {}),
        "subagent_stats": result.get("subagent_stats"), "permission_denials": len(result.get("permission_denials", []) or []),
    }


def run_case(cid, arm, args, outdir: Path, scratch: Path):
    fixture, prompt, grader = CASES[cid]
    ws = scratch / f"{cid}__{arm}"
    if args.regrade:  # re-score an existing workspace + transcript; no new agent run
        lines = (scratch / f"{cid}__{arm}.jsonl").read_text().splitlines()
        return _grade(cid, arm, args, outdir, scratch, ws, grader, lines, None, 0.0)
    if ws.exists():
        shutil.rmtree(ws)
    shutil.copytree(FIX / fixture, ws, ignore=shutil.ignore_patterns("__pycache__"))
    sh("git init -q && git add -A && git -c user.email=e@x -c user.name=eval commit -qm fixture", ws)
    cfg = scratch / f"cfg-{arm}"
    cfg.mkdir(exist_ok=True)
    full_prompt = f"/ultimatum:work {prompt}" if arm == "ultimatum" else prompt
    argv = ["claude", "-p", full_prompt, "--model", args.model, "--output-format", "stream-json", "--verbose",
            "--strict-mcp-config", "--setting-sources", "project", "--allowedTools", *TOOLS.split(),
            "--max-budget-usd", str(args.budget), "--no-session-persistence"]
    if arm == "ultimatum":
        argv += ["--plugin-dir", str(PLUGIN)]
    env = {**os.environ, "CLAUDE_CONFIG_DIR": str(cfg), "CLAUDE_CODE_SYNC_SKILLS": "0", "CLAUDE_CODE_SYNC_PLUGINS": "0"}
    env.pop("ULTIMATUM_ROOT", None)
    t0 = time.time()
    try:
        p = subprocess.run(argv, cwd=ws, capture_output=True, text=True, env=env, timeout=args.timeout)
        lines, rc = p.stdout.splitlines(), p.returncode
    except subprocess.TimeoutExpired as e:
        lines, rc = (e.stdout or b"").decode("utf-8", "replace").splitlines() if isinstance(e.stdout, bytes) else (e.stdout or "").splitlines(), 124
    (scratch / f"{cid}__{arm}.jsonl").write_text("\n".join(lines))
    return _grade(cid, arm, args, outdir, scratch, ws, grader, lines, rc, round(time.time() - t0, 1))


def _grade(cid, arm, args, outdir, scratch, ws, grader, lines, rc, wall):
    run = parse_stream(lines)
    run["wall_s"] = wall
    run["claude_rc"] = rc
    try:
        checks = grader(ws, run)
    except Exception as e:  # grader crash is a recorded failure, not a pass
        checks = {"grader_error": False}
        run["grader_exception"] = repr(e)
    rec = {"case": cid, "arm": arm, "model": args.model, "checks": checks,
           "passed": all(checks.values()), "score": round(sum(checks.values()) / max(1, len(checks)), 3),
           **{k: v for k, v in run.items() if k not in ("tool_inputs_text", "transcript_text")},
           "workspace": str(ws), "transcript": str(scratch / f"{cid}__{arm}.jsonl")}
    (outdir / f"{cid}__{arm}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    u = run.get("usage") or {}
    print(f"{cid:18} {arm:9} pass={rec['passed']!s:5} score={rec['score']:.2f} cost=${run.get('cost_usd') or 0:.3f} "
          f"turns={run.get('num_turns')} agents={run['agent_calls']} in={u.get('input_tokens')} out={u.get('output_tokens')} "
          f"cache_r={u.get('cache_read_input_tokens')} wall={run['wall_s']}s", flush=True)
    failed = [k for k, v in checks.items() if not v]
    if failed:
        print(f"   failed: {', '.join(failed)}", flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=",".join(CASES))
    ap.add_argument("--arms", default="ultimatum,baseline")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--budget", type=float, default=3.0, help="max USD per run")
    ap.add_argument("--timeout", type=int, default=1500)
    ap.add_argument("--out", default=str(REPO / "evals/live/results" / time.strftime("%Y%m%d-%H%M%S")))
    ap.add_argument("--scratch", default=os.environ.get("ULT_EVAL_SCRATCH", "/tmp/ult-live"))
    ap.add_argument("-j", "--jobs", type=int, default=1)
    ap.add_argument("--regrade", action="store_true", help="re-run graders on existing workspaces/transcripts")
    args = ap.parse_args()
    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    scratch = Path(args.scratch); scratch.mkdir(parents=True, exist_ok=True)
    jobs = [(c, a) for c in args.cases.split(",") for a in args.arms.split(",")]
    if args.jobs > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(args.jobs) as ex:
            recs = list(ex.map(lambda ca: run_case(ca[0], ca[1], args, outdir, scratch), jobs))
    else:
        recs = [run_case(c, a, args, outdir, scratch) for c, a in jobs]
    (outdir / "summary.json").write_text(json.dumps([{k: r[k] for k in ("case", "arm", "passed", "score", "checks", "cost_usd",
                                                                          "num_turns", "agent_calls", "usage", "model_usage", "subagent_stats",
                                                                          "duration_ms", "wall_s", "permission_denials")} for r in recs], indent=2))
    print(f"results: {outdir}")


if __name__ == "__main__":
    main()
