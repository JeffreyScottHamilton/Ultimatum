"""`ult findings` — validate, append, and render security findings; keep the
coverage ledger honest.

  ult findings validate [FILE]                       schema + evidence rules; exit 1 on any error
  ult findings add [--file F]  < JSON                append candidate(s) from stdin (auto id, redacted)
  ult findings render [FILE] [--ledger L] --out R    markdown report grouped by status, sorted by severity
  ult findings ledger init|mark|check                coverage ledger with evidence/reason per item

Defaults: findings `.ultimatum/security/findings.json`, ledger `.ultimatum/security/ledger.json`.
Schemas (documentation): plugins/ultimatum/schemas/{findings,coverage-ledger}.schema.json.
These rules are the enforced contract; the JSON Schemas describe the same shape.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from .common import dump_json, project_root, redact, safe_id, state_dir, write_private

STATUSES = ("confirmed", "needs-validation", "rejected")
SEVERITIES = ("critical", "high", "medium", "low", "info")
SEV_RANK = {s: i for i, s in enumerate(SEVERITIES)}
CONFIDENCE = ("high", "medium", "low")
LEDGER_STATES = ("not-started", "in-progress", "checked", "not-applicable", "blocked")
KNOWN_KEYS = {
    "id", "title", "status", "file", "line", "endpoint", "entry_point", "actor", "input", "boundary", "preconditions",
    "impact", "evidence", "cwe", "refs", "severity", "suggested_severity", "confidence", "missing_evidence",
    "validation_plan", "rejection_reason", "rejected_by_pattern", "reproduction", "remediation", "fix_proof",
    "found_by", "verified_by", "verification_notes", "fingerprint", "summary", "notes", "source", "trace",
    "area", "variants",
}
CONFIRMED_REQUIRED = ("entry_point", "actor", "input", "boundary", "preconditions", "impact", "evidence", "severity", "confidence")


def _sec_dir() -> Path:
    return state_dir(project_root(), "security")


def _default_findings() -> Path:
    return _sec_dir() / "findings.json"


def _default_ledger() -> Path:
    return _sec_dir() / "ledger.json"


def _resolve(p: str | None, default) -> Path:
    if not p:
        return default()
    q = Path(p)
    return q if q.is_absolute() else Path.cwd() / q


def _filled(v) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, dict)):
        return len(v) > 0 and any(_filled(x) for x in (v.values() if isinstance(v, dict) else v))
    return True


def load_findings(path: Path) -> tuple[dict, list]:
    """Return (container, findings). Accepts {"findings": [...], ...} or a bare array."""
    if not path.exists():
        return {"version": 1, "findings": []}, []
    data = json.loads(path.read_text("utf-8"))
    if isinstance(data, list):
        return {"version": 1, "findings": data}, data
    if isinstance(data, dict) and isinstance(data.get("findings"), list):
        return data, data["findings"]
    raise ValueError("findings file must be a JSON array or an object with a 'findings' array")


def _safe_rel(p: str) -> str | None:
    if not isinstance(p, str) or not p.strip():
        return "must be a non-empty string"
    if p.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:[\\/]", p):
        return "must be repo-relative, not absolute"
    if ".." in re.split(r"[\\/]", p.split(":", 1)[0] if re.search(r":\d+$", p) else p):
        return "must not contain '..'"
    if re.search(r"[\x00-\x1f]", p):
        return "must not contain control characters"
    return None


def validate_finding(f, idx: int) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    if not isinstance(f, dict):
        return [f"[{idx}] finding must be an object"], []
    fid = f.get("id") or f"#{idx}"
    E = lambda m: errs.append(f"{fid}: {m}")  # noqa: E731
    W = lambda m: warns.append(f"{fid}: {m}")  # noqa: E731
    for k in ("id", "title", "status", "file", "boundary"):
        if not _filled(f.get(k)):
            E(f"missing required field '{k}'")
    st = f.get("status")
    if st is not None and st not in STATUSES:
        E(f"status '{st}' not in {list(STATUSES)} (note: hyphen, not underscore)")
    if isinstance(f.get("title"), str) and len(f["title"]) > 120:
        E("title longer than 120 characters")
    if f.get("file") is not None:
        why = _safe_rel(f.get("file"))
        if why:
            E(f"file {why}")
    if "line" in f and f["line"] is not None and (not isinstance(f["line"], int) or isinstance(f["line"], bool) or f["line"] < 1):
        E("line must be an integer >= 1")
    for k in ("severity", "suggested_severity"):
        v = f.get(k)
        if v is not None and v not in SEVERITIES + ("unrated",):
            E(f"{k} '{v}' not in {list(SEVERITIES) + ['unrated']}")
    if f.get("confidence") is not None and f["confidence"] not in CONFIDENCE:
        E(f"confidence '{f['confidence']}' not in {list(CONFIDENCE)}")
    if f.get("rejected_by_pattern") is not None and not re.fullmatch(r"FP-\d{2}", str(f["rejected_by_pattern"])):
        E("rejected_by_pattern must look like FP-01 (see references/security/findings.md)")
    sev = f.get("severity")
    if st == "confirmed":
        for k in CONFIRMED_REQUIRED:
            if not _filled(f.get(k)):
                E(f"confirmed finding needs '{k}'")
        if sev == "unrated":
            E("confirmed finding needs a real severity, not 'unrated'")
        if f.get("confidence") == "low":
            W("confirmed with low confidence: consider needs-validation")
        if not _filled(f.get("verified_by")):
            W("no verified_by: serious findings should be checked by a fresh verifier")
    elif st == "needs-validation":
        if not _filled(f.get("missing_evidence")):
            E("needs-validation finding needs 'missing_evidence' (the exact fact that would settle it)")
        if sev not in (None, "unrated"):
            E(f"needs-validation finding must not carry severity '{sev}' (use suggested_severity)")
    elif st == "rejected":
        if not _filled(f.get("rejection_reason")):
            E("rejected finding needs 'rejection_reason' (the control or fact that refutes it)")
        if sev not in (None, "unrated"):
            E(f"rejected finding must not carry severity '{sev}'")
    fb, vb = f.get("found_by"), f.get("verified_by")
    if _filled(fb) and _filled(vb) and str(fb).strip() == str(vb).strip():
        E("verified_by must differ from found_by (the proposer never signs off)")
    unknown = sorted(set(f) - KNOWN_KEYS)
    if unknown:
        W(f"unknown field(s) {unknown} (kept; check for typos)")
    blob = json.dumps(f, ensure_ascii=False)
    if redact(blob) != blob:
        kinds = sorted(set(re.findall(r"\[REDACTED:([\w-]+)", redact(blob))) - set(re.findall(r"\[REDACTED:([\w-]+)", blob)))
        E(f"contains an unredacted secret-looking value ({', '.join(kinds) or 'secret'}); replace it with [REDACTED:<kind>:<last4>]")
    return errs, warns


def validate_all(findings: list) -> tuple[list[str], list[str]]:
    errs, warns, seen = [], [], {}
    for i, f in enumerate(findings):
        e, w = validate_finding(f, i)
        errs += e
        warns += w
        if isinstance(f, dict) and f.get("id"):
            if f["id"] in seen:
                errs.append(f"{f['id']}: duplicate id")
            seen[f["id"]] = True
        if isinstance(f, dict) and f.get("fingerprint"):
            key = ("fp", f["fingerprint"])
            if key in seen:
                errs.append(f"{f.get('id')}: duplicate fingerprint '{f['fingerprint']}' (merge same root cause)")
            seen[key] = True
    return errs, warns


def cmd_validate(args) -> int:
    path = _resolve(args.file, _default_findings)
    try:
        _, findings = load_findings(path)
    except (ValueError, OSError) as e:
        print(f"[ult findings] INVALID {path.name}: {e}")
        return 1
    if not path.exists():
        print(f"[ult findings] INVALID: {path} does not exist")
        return 1
    errs, warns = validate_all(findings)
    for w in warns:
        print(f"  warn  {w}")
    for e in errs:
        print(f"  error {e}")
    counts = {s: sum(1 for f in findings if isinstance(f, dict) and f.get("status") == s) for s in STATUSES}
    tag = "INVALID" if errs else "OK"
    print(f"[ult findings] {tag} {len(findings)} finding(s) " + " ".join(f"{k}={v}" for k, v in counts.items())
          + f" errors={len(errs)} warnings={len(warns)}")
    return 1 if errs else 0


def _parse_stdin(text: str) -> list:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.S)
    if m:
        text = m.group(1).strip()
    try:
        data = json.loads(text)
    except ValueError:
        data = [json.loads(l) for l in text.splitlines() if l.strip().startswith("{")]  # JSON lines
    if isinstance(data, dict):
        data = data["findings"] if isinstance(data.get("findings"), list) else [data]
    if not isinstance(data, list):
        raise ValueError("expected a JSON object, array, or JSON lines")
    return data


def _redact_tree(v):
    if isinstance(v, str):
        return redact(v)
    if isinstance(v, list):
        return [_redact_tree(x) for x in v]
    if isinstance(v, dict):
        return {k: _redact_tree(x) for k, x in v.items()}
    return v


def cmd_add(args) -> int:
    path = _resolve(args.file, _default_findings)
    try:
        container, findings = load_findings(path)
        new = _parse_stdin(sys.stdin.read())
    except (ValueError, OSError, KeyError) as e:
        print(f"[ult findings] add failed: {e}")
        return 1
    used = {f.get("id") for f in findings if isinstance(f, dict)}
    nums = [int(m.group(1)) for i in used if isinstance(i, str) for m in [re.fullmatch(r"F-(\d+)", i)] if m]
    nxt = max(nums, default=0) + 1
    added, redactions = [], 0
    for f in new:
        if not isinstance(f, dict):
            print("[ult findings] add failed: every item must be an object")
            return 1
        r = _redact_tree(f)
        if r != f:
            redactions += 1
        f = r
        f.setdefault("status", "needs-validation")
        if not f.get("id") or f["id"] in used:
            f["id"] = f"F-{nxt:03d}"
            nxt += 1
        used.add(f["id"])
        added.append(f)
    errs, warns = validate_all(findings + added)
    errs = [e for e in errs if any(e.startswith(f"{a['id']}:") for a in added)]
    for w in warns:
        if any(w.startswith(f"{a['id']}:") for a in added):
            print(f"  warn  {w}")
    if errs:
        for e in errs:
            print(f"  error {e}")
        print(f"[ult findings] nothing written: {len(errs)} error(s) in new item(s)")
        return 1
    findings.extend(added)
    container["findings"] = findings
    write_private(path, dump_json(container) + "\n")
    print(f"[ult findings] added {', '.join(a['id'] for a in added)} -> {path}"
          + (f" ({redactions} item(s) had secret-looking text redacted)" if redactions else ""))
    return 0


# --------------------------------------------------------------------------
# Ledger
# --------------------------------------------------------------------------
PRESETS = {
    "audit": [
        ("authn", "authentication", "Login, password, reset, MFA, token issue paths", ["ASVS:V6", "WSTG-ATHN"]),
        ("session", "session", "Session/token lifecycle, cookies, logout, CSRF", ["ASVS:V7", "ASVS:V9", "WSTG-SESS"]),
        ("authz-function", "authorization", "Function-level access: roles, admin routes, privileged actions", ["ASVS:V8", "WSTG-ATHZ-02", "WSTG-ATHZ-03", "WSTG-APIT-04"]),
        ("authz-object", "authorization", "Object/tenant access: every id-taking read/write/list/export path", ["ASVS:V8", "WSTG-ATHZ-04", "WSTG-APIT-02"]),
        ("injection", "injection", "SQL/NoSQL/command/template/code injection sinks", ["ASVS:V1", "WSTG-INJT"]),
        ("output-xss", "frontend", "Raw HTML sinks, template escaping, client-side redirects", ["ASVS:V3", "WSTG-INJT-01", "WSTG-INJT-02", "WSTG-CLNT"]),
        ("files", "files", "Upload, download, path joins, archives", ["ASVS:V5", "WSTG-ATHZ-01", "WSTG-BUSL-08", "WSTG-BUSL-09"]),
        ("ssrf", "ssrf", "Outbound requests built from input; webhooks; URL fetchers", ["ASVS:V1", "ASVS:V12", "WSTG-INJT-19"]),
        ("parsing", "parsing", "Deserialization, XML, YAML, mass assignment of request bodies", ["ASVS:V1.5", "ASVS:V2", "WSTG-INJT-07", "WSTG-INJT-20", "WSTG-INJT-23"]),
        ("business-logic", "business-logic", "Money/credits, quotas, workflow order, races, idempotency", ["ASVS:V2.3", "ASVS:V15.4", "WSTG-BUSL"]),
        ("data-exposure", "data-protection", "Over-fetching, error leaks, logs, sensitive data in URLs", ["ASVS:V14", "ASVS:V16", "WSTG-ERRH", "WSTG-APIT-03"]),
        ("secrets", "secrets", "Hardcoded/fallback secrets, secret handling, rotation", ["ASVS:V13.3", "WSTG-CONF"]),
        ("crypto", "crypto", "Hashing, encryption, randomness, TLS verification", ["ASVS:V11", "ASVS:V12", "WSTG-CRYP"]),
        ("config", "config", "Debug flags, CORS, CSP/headers, cookie flags, defaults", ["ASVS:V3.4", "ASVS:V13", "WSTG-CONF"]),
        ("ci-cd", "ci", "Workflow triggers, token permissions, untrusted expressions, action pinning", ["WSTG-CONF"]),
        ("deploy-iac", "iac", "Dockerfile, compose, k8s, Terraform exposure and privileges", ["ASVS:V13", "WSTG-CONF-01", "WSTG-CONF-11"]),
        ("dependencies", "dependencies", "Lockfiles, advisories (osv-scanner), install scripts", ["ASVS:V15.2"]),
        ("ai-agent", "ai-agent", "Agent configs, MCP servers, tool permissions, untrusted text reaching tools", []),
    ],
    "review": [
        ("diff-read", "change", "Every hunk read with its execution path (callers, config, controls)", []),
        ("removed-checks", "change", "Removed or loosened checks traced to what replaced them", ["ASVS:V8"]),
        ("siblings", "change", "Sibling handlers/methods enforce the same rule", ["WSTG-ATHZ-04"]),
        ("tests", "change", "Security-relevant changes have a test that fails without the guard", []),
        ("scan", "change", "`ult scan --diff` leads read and resolved", []),
    ],
    "none": [],
}


def load_ledger(path: Path) -> dict:
    if not path.exists():
        raise ValueError(f"ledger not found: {path} (run `ult findings ledger init`)")
    data = json.loads(path.read_text("utf-8"))
    if isinstance(data, list):
        data = {"version": 1, "items": data}
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise ValueError("ledger must be an object with an 'items' array")
    return data


def ledger_problems(led: dict) -> tuple[list[str], list[str]]:
    """(errors, unfinished). Errors: malformed. Unfinished: items lacking a terminal state with evidence/reason."""
    errs, unfinished, seen = [], [], set()
    for i, it in enumerate(led.get("items", [])):
        if not isinstance(it, dict):
            errs.append(f"[{i}] item must be an object")
            continue
        iid = it.get("id") or f"#{i}"
        if not _filled(it.get("id")):
            errs.append(f"[{i}] missing id")
        elif iid in seen:
            errs.append(f"{iid}: duplicate id")
        seen.add(iid)
        stt = it.get("state")
        if stt not in LEDGER_STATES:
            errs.append(f"{iid}: state '{stt}' not in {list(LEDGER_STATES)}")
            continue
        if stt == "checked" and not _filled(it.get("evidence")):
            unfinished.append(f"{iid}: checked but no evidence")
        elif stt in ("not-applicable", "blocked") and not _filled(it.get("reason")):
            unfinished.append(f"{iid}: {stt} but no reason")
        elif stt in ("not-started", "in-progress"):
            unfinished.append(f"{iid}: still {stt}" + (" (mark checked with evidence, not-applicable/blocked with reason)"))
        blob = json.dumps(it, ensure_ascii=False)
        if redact(blob) != blob:
            errs.append(f"{iid}: contains an unredacted secret-looking value")
    return errs, unfinished


def _ledger_counts(led: dict) -> dict:
    c = {s: 0 for s in LEDGER_STATES}
    for it in led.get("items", []):
        if isinstance(it, dict) and it.get("state") in c:
            c[it["state"]] += 1
    return c


def cmd_ledger(args) -> int:
    path = _resolve(args.file, _default_ledger)
    if args.action == "init":
        if path.exists() and not args.force:
            print(f"[ult findings] ledger exists: {path} (use --force to replace; prior ledger kept)")
            return 1
        items = [{"id": i, "area": a, "title": t, "standards": s, "paths": [], "state": "not-started",
                  "evidence": "", "reason": ""} for i, a, t, s in PRESETS[args.preset]]
        led = {"version": 1, "profile": args.profile, "scope": redact(args.scope or ""),
               "created": time.strftime("%Y-%m-%dT%H:%M:%S"), "items": items}
        write_private(path, dump_json(led) + "\n")
        print(f"[ult findings] ledger initialised: {len(items)} item(s), preset={args.preset}, profile={args.profile} -> {path}")
        return 0
    try:
        led = load_ledger(path)
    except (ValueError, OSError) as e:
        print(f"[ult findings] {e}")
        return 1
    if args.action == "mark":
        if not args.id or not args.state:
            print("[ult findings] mark needs <id> --state STATE")
            return 2
        try:
            safe_id(args.id)
        except ValueError as e:
            print(f"[ult findings] {e}")
            return 2
        if args.state == "checked" and not _filled(args.evidence):
            print("[ult findings] refused: state 'checked' needs --evidence (file:line, command + exit code, or test name)")
            return 1
        if args.state in ("not-applicable", "blocked") and not _filled(args.reason):
            print(f"[ult findings] refused: state '{args.state}' needs --reason")
            return 1
        item = next((it for it in led["items"] if isinstance(it, dict) and it.get("id") == args.id), None)
        if item is None:
            item = {"id": args.id, "area": args.area or args.id, "title": args.title or "", "standards": [], "paths": [],
                    "state": "not-started", "evidence": "", "reason": ""}
            led["items"].append(item)
        item["state"] = args.state
        for k in ("evidence", "reason", "owner", "title", "area"):
            v = getattr(args, k, None)
            if v:
                item[k] = redact(v)
        if args.paths:
            item["paths"] = sorted(set(item.get("paths", [])) | set(args.paths))
        item["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        write_private(path, dump_json(led) + "\n")
        print(f"[ult findings] {args.id} -> {args.state}")
        return 0
    # check
    errs, unfinished = ledger_problems(led)
    c = _ledger_counts(led)
    for e in errs:
        print(f"  error {e}")
    for u in unfinished:
        print(f"  open  {u}")
    total = len(led["items"])
    ok = not errs and not unfinished
    print(f"[ult findings] ledger {'COMPLETE' if ok else 'INCOMPLETE'}: {total} item(s) "
          + " ".join(f"{k}={v}" for k, v in c.items()))
    return 0 if ok else 1


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------
def _txt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return "; ".join(_txt(x) for x in v if _filled(x))
    if isinstance(v, dict):
        return "; ".join(f"{k}: {_txt(x)}" for k, x in v.items() if _filled(x))
    return str(v)


def _cell(v) -> str:
    return _txt(v).replace("|", "\\|").replace("\n", " ")


def _loc(f) -> str:
    loc = f.get("file", "?")
    if f.get("line"):
        loc += f":{f['line']}"
    if f.get("endpoint"):
        loc += f" ({f['endpoint']})"
    return loc


def render(container: dict, findings: list, led: dict | None) -> str:
    conf = sorted([f for f in findings if f.get("status") == "confirmed"],
                  key=lambda f: (SEV_RANK.get(f.get("severity"), 9), f.get("id", "")))
    nv = sorted([f for f in findings if f.get("status") == "needs-validation"],
                key=lambda f: (SEV_RANK.get(f.get("suggested_severity"), 9), f.get("id", "")))
    rej = sorted([f for f in findings if f.get("status") == "rejected"], key=lambda f: f.get("id", ""))
    scope = container.get("scope") or (led or {}).get("scope") or "not stated"
    out = []
    if led is None:
        out.append("> **Coverage: unknown** — no coverage ledger supplied; treat this as a partial review.")
    else:
        c = _ledger_counts(led)
        total = len(led.get("items", []))
        done = c["checked"] + c["not-applicable"]
        _, unfinished = ledger_problems(led)
        if unfinished or c["blocked"]:
            out.append(f"> **Partial coverage:** {c['checked']}/{total} items checked, {c['not-applicable']} not applicable, "
                       f"{c['blocked']} blocked, {c['not-started'] + c['in-progress']} not finished.")
        else:
            out.append(f"> **Coverage:** {done}/{total} ledger items closed ({c['checked']} checked, {c['not-applicable']} not applicable).")
    out += ["", "# Security report", "", f"- **Scope:** {_txt(scope)}"]
    if led is not None and led.get("profile"):
        out.append(f"- **Profile:** {led['profile']}")
    for k in ("source_ref", "tools", "authorization"):
        if container.get(k):
            out.append(f"- **{k.replace('_', ' ').capitalize()}:** {_txt(container[k])}")
    out.append(f"- **Results:** {len(conf)} confirmed, {len(nv)} need validation, {len(rej)} rejected")
    if not conf:
        cov = ""
        if led is not None:
            c = _ledger_counts(led)
            cov = f"; coverage {c['checked'] + c['not-applicable']}/{len(led.get('items', []))} items"
        out.append(f"- No confirmed findings within {_txt(scope)}{cov}. This is not evidence of absence.")
    out += ["", "## Confirmed findings", ""]
    if conf:
        out += ["| Severity | ID | Title | Location | Boundary |", "|---|---|---|---|---|"]
        out += [f"| {f.get('severity')} | {f.get('id')} | {_cell(f.get('title'))} | {_cell(_loc(f))} | {_cell(f.get('boundary'))} |" for f in conf]
        for f in conf:
            out += ["", f"### {f.get('id')} — {_txt(f.get('title'))} ({f.get('severity')}, confidence {f.get('confidence')})", ""]
            for label, key in (("Location", None), ("Entry point", "entry_point"), ("Actor", "actor"), ("Input", "input"),
                               ("Boundary that fails", "boundary"), ("Conditions", "preconditions"), ("Impact", "impact"),
                               ("Evidence", "evidence"), ("Reproduction", "reproduction"), ("Fix", "remediation"),
                               ("Fix proof", "fix_proof"), ("Verified by", "verified_by"), ("References", "cwe"), ("Standards", "refs")):
                v = _loc(f) if key is None else f.get(key)
                if _filled(v):
                    out.append(f"- **{label}:** {_txt(v)}")
    else:
        out.append("None.")
    out += ["", "## Needs validation (no severity assigned)", ""]
    if nv:
        out += ["| ID | Title | Location | Missing evidence | Suggested |", "|---|---|---|---|---|"]
        out += [f"| {f.get('id')} | {_cell(f.get('title'))} | {_cell(_loc(f))} | {_cell(f.get('missing_evidence'))} | {f.get('suggested_severity') or '—'} |" for f in nv]
        for f in nv:
            if _filled(f.get("validation_plan")):
                out.append(f"- {f.get('id')} validation plan: {_txt(f['validation_plan'])}")
    else:
        out.append("None.")
    out += ["", "## Rejected candidates", ""]
    if rej:
        out += ["| ID | Title | Location | Why rejected | Pattern |", "|---|---|---|---|---|"]
        out += [f"| {f.get('id')} | {_cell(f.get('title'))} | {_cell(_loc(f))} | {_cell(f.get('rejection_reason'))} | {f.get('rejected_by_pattern') or '—'} |" for f in rej]
    else:
        out.append("None.")
    out += ["", "## Coverage", ""]
    if led is None:
        out.append("No ledger. Coverage was not tracked.")
    else:
        c = _ledger_counts(led)
        out.append("States: " + ", ".join(f"{k} {v}" for k, v in c.items()))
        out += ["", "| Item | Area | State | Evidence or reason |", "|---|---|---|---|"]
        for it in led.get("items", []):
            if isinstance(it, dict):
                out.append(f"| {_cell(it.get('id'))} | {_cell(it.get('area'))} | {it.get('state')} | {_cell(it.get('evidence') or it.get('reason') or '—')} |")
    out += ["", "## Limits", "",
            "Static reading plus local checks only, unless the scope above says active testing was authorized. "
            "Scanner hits are leads; only verified items appear as confirmed. Secrets are redacted."]
    return redact("\n".join(out) + "\n")


def cmd_render(args) -> int:
    path = _resolve(args.file, _default_findings)
    try:
        container, findings = load_findings(path)
    except (ValueError, OSError) as e:
        print(f"[ult findings] {e}")
        return 1
    errs, _ = validate_all(findings)
    led = None
    lp = _resolve(args.ledger, _default_ledger) if args.ledger else None
    if lp is None and _default_ledger().exists() and not args.file:
        lp = _default_ledger()
    if lp is not None:
        try:
            led = load_ledger(lp)
        except (ValueError, OSError) as e:
            print(f"[ult findings] {e}")
            return 1
    md = render(container, [f for f in findings if isinstance(f, dict)], led)
    outp = _resolve(args.out, lambda: _sec_dir() / "report.md")
    write_private(outp, md)
    print(f"[ult findings] report -> {outp}" + (f" (WARNING: findings file has {len(errs)} validation error(s); run validate)" if errs else ""))
    return 0


def register(sub):
    p = sub.add_parser("findings", help="validate / add / render security findings; coverage ledger")
    fs = p.add_subparsers(dest="findings_cmd", required=True)

    v = fs.add_parser("validate", help="check findings JSON against the schema rules")
    v.add_argument("file", nargs="?")
    v.set_defaults(func=cmd_validate)

    a = fs.add_parser("add", help="append finding(s) from JSON on stdin (auto id, redacted, validated)")
    a.add_argument("--file")
    a.set_defaults(func=cmd_add)

    r = fs.add_parser("render", help="write a markdown report from findings (+ ledger)")
    r.add_argument("file", nargs="?")
    r.add_argument("--ledger")
    r.add_argument("--out", help="default .ultimatum/security/report.md")
    r.set_defaults(func=cmd_render)

    lg = fs.add_parser("ledger", help="coverage ledger: init | mark | check")
    lg.add_argument("action", choices=["init", "mark", "check"])
    lg.add_argument("id", nargs="?", help="item id (mark)")
    lg.add_argument("--file", help="default .ultimatum/security/ledger.json")
    lg.add_argument("--state", choices=LEDGER_STATES)
    lg.add_argument("--evidence", help="required for checked: file:line, command + exit code, test name")
    lg.add_argument("--reason", help="required for not-applicable / blocked")
    lg.add_argument("--area")
    lg.add_argument("--title")
    lg.add_argument("--owner")
    lg.add_argument("--paths", nargs="*")
    lg.add_argument("--preset", choices=sorted(PRESETS), default="audit", help="init: seed items (default audit)")
    lg.add_argument("--profile", choices=["quick", "standard", "deep"], default="standard")
    lg.add_argument("--scope", help="init: scope statement")
    lg.add_argument("--force", action="store_true", help="init: replace an existing ledger")
    lg.set_defaults(func=cmd_ledger)
