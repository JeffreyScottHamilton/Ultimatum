"""Shared helpers for Ultimatum's local tools.

Design rules (see skills/work/references/context-efficiency.md):
- Python standard library only. No network access anywhere in this package.
- State lives in `<project>/.ultimatum/`, which ignores itself via its own
  .gitignore so nothing in the user's repository settings changes.
- Raw evidence is stored verbatim (mode 0600). Anything *printed* for the model
  or written into summaries/handoffs passes through `redact()` first.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

STATE_DIRNAME = ".ultimatum"


def project_root(start: Path | None = None) -> Path:
    """Git top-level if inside a work tree, else the current directory.

    ULTIMATUM_ROOT overrides (used by tests and by workers in worktrees).
    """
    env = os.environ.get("ULTIMATUM_ROOT")
    if env:
        return Path(env).resolve()
    start = (start or Path.cwd()).resolve()
    try:
        out = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0 and out.stdout.strip():
            return Path(out.stdout.strip()).resolve()
    except (OSError, subprocess.SubprocessError):
        pass
    return start


def _refuse_symlink(p: Path) -> None:
    # A cloned repository could ship `.ultimatum/...` as symlinks pointing at
    # files outside the project; writing through them would clobber the target.
    if p.is_symlink():
        raise SystemExit(f"[ult] refusing to use {p}: it is a symlink (possible repository-planted path)")


def state_dir(root: Path | None = None, sub: str | None = None) -> Path:
    root = root or project_root()
    # ULTIMATUM_STATE_DIR keeps all state outside the project, for tasks where
    # the user forbids any write inside the repository (e.g. a strict read-only audit).
    ext = os.environ.get("ULTIMATUM_STATE_DIR")
    d = Path(ext).resolve() if ext else root / STATE_DIRNAME
    _refuse_symlink(d)
    if not d.exists():
        d.mkdir(mode=0o700, parents=True, exist_ok=True)
    gi = d / ".gitignore"
    if not gi.exists() and not gi.is_symlink():
        write_private(gi, "# Ultimatum local state: logs, index, notes. Never commit.\n*\n")
    if sub:
        d = d / sub
        _refuse_symlink(d)
        d.mkdir(mode=0o700, parents=True, exist_ok=True)
    return d


def write_private(path: Path, data: str | bytes) -> None:
    """Write a file readable only by the current user."""
    path.parent.mkdir(parents=True, exist_ok=True)
    _refuse_symlink(path)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(data.encode("utf-8", "replace") if isinstance(data, str) else data)


def new_id(prefix: str) -> str:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    salt = hashlib.sha1(f"{time.time_ns()}{os.getpid()}".encode()).hexdigest()[:4]
    return f"{prefix}-{stamp}-{salt}"


SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,120}$")


def safe_id(value: str) -> str:
    """Reject ids that could escape .ultimatum/ (path separators, '..')."""
    if not SAFE_ID.match(value) or ".." in value:
        raise ValueError(f"invalid id: {value!r}")
    return value


def raw_lines(text: str) -> list[str]:
    """Split on '\n' only, so line numbers match `wc -l`/editors and nothing else
    (form feeds, lone CR, unicode separators) is treated as a line break."""
    parts = text.split("\n")
    if parts and parts[-1] == "":
        parts.pop()
    return parts


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def dump_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=False, ensure_ascii=False)


# --------------------------------------------------------------------------
# Secret redaction. Patterns are original, high-signal, and deliberately few:
# a false redaction costs a little readability; a missed one leaks a secret
# into a summary, handoff, or worker prompt.
# --------------------------------------------------------------------------
SECRET_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("private-key", re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----[\s\S]*?(?:-----END (?:[A-Z0-9]+ )*PRIVATE KEY-----|\Z)")),
    ("aws-access-key-id", re.compile(r"\b(?:AKIA|ASIA|AGPA|AIDA|AROA|ANPA|ANVA|APKA)[A-Z0-9]{16}\b")),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{22,255})\b")),
    ("gitlab-token", re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}\b")),
    ("slack-webhook", re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/_-]+")),
    ("stripe-key", re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}\b")),
    ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b")),
    ("openai-key", re.compile(r"(?<![A-Za-z0-9_-])sk-(?:proj-|svcacct-)?[A-Za-z0-9_\-]{32,}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("npm-token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("sendgrid-key", re.compile(r"\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\b")),
    ("url-credentials", re.compile(r"(?<=://)[^/\s:@]+:[^/\s@]{3,}(?=@)")),
    ("bearer", re.compile(r"(?i)(?<=authorization: bearer )[A-Za-z0-9._\-]{16,}")),
    # key = "value" assignments for names that strongly imply a secret
    ("assigned-secret", re.compile(
        r"(?i)(?<![A-Za-z0-9])((?:[A-Za-z0-9]+[_-])*(?:api[_-]?key|secret[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|password|passwd|private[_-]?key)"
        r"[\"']?\s*[:=]\s*[\"'])([^\"'\s]{8,})([\"'])")),
    # .env style: UPPER_NAME_WITH_SECRET_WORD=value (unquoted)
    ("env-secret", re.compile(
        r"(?m)^(\s*(?:export\s+)?[A-Z0-9_]*(?:API_KEY|SECRET|TOKEN|PASSWORD|PASSWD|PRIVATE_KEY)[A-Z0-9_]*=)([^\s\"'#]{8,})()")),
]


def redact(text: str) -> str:
    """Replace likely secrets with `[REDACTED:<kind>:<last4>]`.

    Keeps the last 4 characters so two findings can still be told apart
    without exposing the value.
    """
    if not text:
        return text
    for kind, pat in SECRET_PATTERNS:
        if kind in ("assigned-secret", "env-secret"):
            text = pat.sub(lambda m: f"{m.group(1)}[REDACTED:{kind}:{m.group(2)[-4:]}]{m.group(3)}", text)
        elif kind == "private-key":
            text = pat.sub(f"[REDACTED:{kind}]", text)
        else:
            text = pat.sub(lambda m, k=kind: f"[REDACTED:{k}:{m.group(0)[-4:]}]", text)
    return text


def eprint(*a):
    print(*a, file=sys.stderr)
