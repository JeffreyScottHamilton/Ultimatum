"""`ult doctor` — report which optional integrations exist. Changes nothing.

MCP-based integrations (Context7, Serena, Sentry, Chrome DevTools, Supabase,
Terraform) cannot be seen from a subprocess: the agent checks its own tool
list for them. This command covers command-line tools only.
"""
from __future__ import annotations

import shutil
import subprocess

TOOLS = [
    ("rg", "fast scoped search (ult search uses it; Python fallback otherwise)"),
    ("git", "diffs, worktrees, handoff facts"),
    ("semgrep", "static analysis (ult scan; fallback: built-in sink patterns)"),
    ("gitleaks", "secret scanning (ult scan; fallback: built-in secret patterns)"),
    ("osv-scanner", "dependency advisories (ult scan; no honest offline fallback — reported as not checked)"),
    ("node", "browser checks via Playwright (ult-browser.mjs)"),
    ("gh", "PR/CI status for iterate-pr workflow"),
    ("sentry-cli", "production issue lookups (or Sentry MCP)"),
    ("terraform", "infra validate/plan/test"),
    ("supabase", "local DB, migrations, advisors"),
    ("psql", "query plans (EXPLAIN) against an authorised database"),
]


def _node_has(mod: str) -> bool:
    if not shutil.which("node"):
        return False
    try:
        r = subprocess.run(["node", "-e", f"require.resolve('{mod}')"], capture_output=True, timeout=20)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def cmd_doctor(args) -> int:
    print("[ult doctor] optional command-line integrations (nothing is installed or changed)")
    for name, why in TOOLS:
        path = shutil.which(name)
        print(f"  {'✓' if path else '·'} {name:<12} {why}")
    for mod, why in (("playwright", "real-browser interaction, screenshots, viewports"),
                     ("axe-core", "full accessibility rule engine (fallback: built-in DOM checks)")):
        print(f"  {'✓' if _node_has(mod) else '·'} {mod:<12} {why} [node module]")
    print("  MCP tools (Context7, Serena, Sentry, Chrome DevTools, Supabase, Terraform): check the agent's tool list.")
    return 0


def register(sub):
    p = sub.add_parser("doctor", help="list optional integrations that are available")
    p.set_defaults(func=cmd_doctor)
