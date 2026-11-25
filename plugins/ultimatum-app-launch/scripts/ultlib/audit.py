"""`ult audit` — the mechanical half of a repository security audit.

  ult audit start [--scope TEXT] [--profile quick|standard|deep]
      ledger init (if absent) + offline scan + empty findings.json skeleton (if absent)
  ult audit finish
      ledger check + findings validate + report render (.ultimatum/security/report.md)

Everything is built from `ult scan` and `ult findings`; this module only
sequences them and records which scanners did not run. All writes go under the
state dir (ULTIMATUM_STATE_DIR is honoured).
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json

from . import findings as F
from . import scan as S
from .common import dump_json, project_root, redact, state_dir, write_private


def _quiet(fn, args) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = fn(args)
    return int(code or 0), buf.getvalue()


def _tools_line(rep: dict) -> str:
    ran, missing = ["built-in checks"], []
    for name, t in (rep.get("tools") or {}).items():
        if t.get("ran"):
            ran.append(name)
        else:
            missing.append(name)
    parts = ["ran: " + ", ".join(ran)]
    if missing:
        parts.append("NOT run: " + ", ".join(missing))
    if not (rep.get("tools") or {}).get("osv-scanner", {}).get("ran"):
        parts.append("dependency advisories: not checked")
    if not (rep.get("tools") or {}).get("gitleaks", {}).get("ran"):
        parts.append("git history secrets: NOT checked")
    return "; ".join(parts)


def _scan_report(sec) -> dict:
    try:
        return json.loads((sec / "scan-last.json").read_text("utf-8"))
    except (OSError, ValueError):
        return {}


def cmd_start(args) -> int:
    root = project_root()
    sec = state_dir(root, "security")
    led_path, fp = sec / "ledger.json", sec / "findings.json"
    scope = redact(args.scope or "whole repository")
    if led_path.exists():
        led_note = "ledger kept (exists)"
    else:
        _quiet(F.cmd_ledger, argparse.Namespace(action="init", file=None, force=False, preset="audit",
                                                profile=args.profile, scope=scope))
        led_note = "ledger created"
    ns = argparse.Namespace(path=None, diff=None, json=None, no_external=False, semgrep_config=None,
                            history=True, osv_online=False, max_print=0)
    code, _ = _quiet(S.cmd_scan, ns)
    if code:
        print("[ult audit] scan failed; run `ult scan` to see why")
        return code
    rep = _scan_report(sec)
    tools = _tools_line(rep)
    if fp.exists():
        sk_note = "findings.json kept (exists)"
    else:
        write_private(fp, dump_json({"version": 1, "scope": scope, "tools": tools, "findings": []}) + "\n")
        sk_note = "findings.json skeleton written"
    try:
        led = F.load_ledger(led_path)
        unfinished = len(F.ledger_problems(led)[1])
    except (ValueError, OSError):
        unfinished = -1
    print(f"[ult audit] start: {led_note}; {sk_note}")
    print(f"  state: {sec}")
    print(f"  tools {tools}")
    print(f"  leads: {len(rep.get('leads', []))} (details: {sec / 'scan-last.json'}); open ledger items: {unfinished}")
    print("  next: mark ledger areas (`ult findings ledger mark ID --state checked --evidence ...`),")
    print("        `ult findings add < file`, then `ult audit finish`")
    return 0


def cmd_finish(args) -> int:
    root = project_root()
    sec = state_dir(root, "security")
    led_path, fp = sec / "ledger.json", sec / "findings.json"
    if not fp.exists():
        print("[ult audit] finish: no findings.json; run `ult audit start` first")
        return 1
    lcode, lout = (1, "")
    led = None
    if led_path.exists():
        lcode, lout = _quiet(F.cmd_ledger, argparse.Namespace(action="check", file=None))
        try:
            led = F.load_ledger(led_path)
        except (ValueError, OSError):
            led = None
    vcode, vout = _quiet(F.cmd_validate, argparse.Namespace(file=None))
    errors = [ln.strip() for ln in vout.splitlines() if ln.strip().startswith("error ")]
    try:
        container, items = F.load_findings(fp)
    except (ValueError, OSError) as e:
        print(f"[ult audit] INVALID findings.json: {e}")
        return 1
    if not container.get("tools"):
        container = dict(container, tools=_tools_line(_scan_report(sec)))
    report = sec / "report.md"
    write_private(report, F.render(container, [f for f in items if isinstance(f, dict)], led))
    open_n = len(F.ledger_problems(led)[1]) if led else -1
    print(f"[ult audit] finish: {'INVALID' if vcode else 'OK'} findings={len(items)} errors={len(errors)}; "
          f"ledger {'complete' if lcode == 0 else f'INCOMPLETE ({open_n} open)' if led else 'missing'}")
    for e in errors[:6]:
        print(f"  {e}")
    print(f"  tools {container.get('tools')}")
    print(f"  report: {report}")
    return 1 if vcode else 0


def register(sub):
    p = sub.add_parser("audit", help="start/finish a repository security audit (ledger, scan, findings, report)")
    a = p.add_subparsers(dest="audit_cmd", required=True)
    s = a.add_parser("start", help="init ledger, run offline scan, write empty findings.json")
    s.add_argument("--scope", help="scope statement")
    s.add_argument("--profile", choices=["quick", "standard", "deep"], default="standard")
    s.set_defaults(func=cmd_start)
    f = a.add_parser("finish", help="ledger check, findings validate, render report")
    f.set_defaults(func=cmd_finish)
