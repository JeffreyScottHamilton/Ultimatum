"""`ult scan` — security lead generator. Runs installed scanners offline-safe,
otherwise (and always) runs built-in pattern checks.

Contract (tested in tests/test_scan.py):
1. Output is LEADS, never findings. Every lead carries source, rule_id, class,
   file, line, a redacted snippet, and why. A person or verifier decides.
2. Secrets are never printed or stored raw: snippets pass through `redact()`.
3. Every external command that ran is printed verbatim with its exit code;
   every tool that did not run is listed with the reason.
4. Dependency advisories are `unknown` unless osv-scanner ran to completion.
5. Exit 0 when the scan completed (leads or not); exit 2 on usage/scan error.

semgrep runs only when the user passes --semgrep-config (local rules, or a
registry pack such as p/... which downloads rules over the network: passing it
is the consent). osv-scanner runs with --offline when a local DB directory is
configured, or online only with --osv-online. gitleaks needs no network.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
from pathlib import Path

from .common import SECRET_PATTERNS, dump_json, new_id, project_root, raw_lines, redact, state_dir, write_private

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".ultimatum", "__pycache__", ".venv", "venv",
             "env", "target", ".next", ".nuxt", "coverage", ".tox", ".mypy_cache", ".pytest_cache", "bower_components"}
LOCKFILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lock", "poetry.lock", "Pipfile.lock", "uv.lock",
             "Cargo.lock", "Gemfile.lock", "composer.lock", "go.sum", "pdm.lock"}
MANIFESTS = {"package.json": "npm", "requirements.txt": "PyPI", "pyproject.toml": "PyPI", "Pipfile": "PyPI",
             "go.mod": "Go", "Cargo.toml": "crates.io", "Gemfile": "RubyGems", "composer.json": "Packagist",
             "pom.xml": "Maven", "build.gradle": "Maven"}
LOCK_FOR = {"package.json": ("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lock", "bun.lockb"),
            "Pipfile": ("Pipfile.lock",), "Cargo.toml": ("Cargo.lock",), "Gemfile": ("Gemfile.lock",),
            "composer.json": ("composer.lock",), "go.mod": ("go.sum",)}
MAX_BYTES = 1_000_000
TEST_PARTS = {"test", "tests", "__tests__", "spec", "specs", "fixtures", "fixture", "examples", "example", "docs",
              "doc", "testdata", "samples", "sample", "mocks", "__mocks__"}
SEV_ORDER = {"high": 0, "medium": 1, "low": 2}
NOT_COVERED = ("Not covered by built-in checks: taint/dataflow, authorization logic, business logic, cross-file "
               "reasoning, deployment facts, dependency advisories. A clean scan is not evidence of absence.")

PY = {".py"}
JS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte"}
GO = {".go"}
JAVA = {".java", ".kt", ".kts", ".scala"}
RB = {".rb", ".erb"}
PHP = {".php"}
SH = {".sh", ".bash", ".zsh"}
TPL = {".html", ".htm", ".jinja", ".jinja2", ".j2", ".njk", ".hbs", ".ejs"}
CODE = PY | JS | GO | JAVA | RB | PHP | {".cs", ".rs", ".c", ".cc", ".cpp", ".swift"}
CFG = {".yml", ".yaml", ".json", ".tf", ".toml", ".ini", ".cfg", ".conf", ".env", ".properties", ".hcl"}
ANY = None  # every text file

F = re.compile
_SECRETY = r"(?:secret|token|passw(?:or)?d|pwd|api[_-]?key|private[_-]?key|session[_-]?key|signing|jwt|otp|nonce|salt|reset)"

# (rule_id, class, severity_hint, extensions, regex, why, standards)
RULES: list[tuple[str, str, str, set | None, re.Pattern, str, list[str]]] = [
    # --- injection: SQL / shell / code / template ---
    ("sql-string-build", "injection", "high", CODE,
     F(r"""(?ix)(\bf["'][^"'\n]*\b(select|insert\s+into|update|delete\s+from)\b[^"'\n]*\{)
         |(["'][^"'\n]*\b(select\s.+\sfrom|insert\s+into|update\s+\w+\s+set|delete\s+from)\b[^"'\n]*["']\s*(\+|%\s*[\w(]|\.format\())
         |(`[^`\n]*\b(select|insert\s+into|update|delete\s+from)\b[^`\n]*\$\{)
         |(\b(Query|Exec|QueryRow)(Context)?\(\s*(ctx\s*,\s*)?fmt\.Sprintf)"""),
     "SQL text built from string formatting/concatenation; check whether any part is caller-controlled and not bound as a parameter",
     ["CWE-89", "ASVS:V1.2.4", "WSTG-INJT-05"]),
    ("shell-exec", "injection", "high", CODE | SH,
     F(r"""(subprocess\.\w+\([^)\n]*shell\s*=\s*True)|\bos\.(system|popen)\(|\bexec(Sync)?\(\s*(`[^`\n]*\$\{|["'][^"'\n]*["']\s*\+|\w)
         |spawn(Sync)?\([^)\n]*shell\s*:\s*true|exec\.Command\(\s*"(sh|bash|cmd)"\s*,\s*"(-c|/c)"|Runtime\.getRuntime\(\)\.exec\(
         |\b(shell_exec|passthru|proc_open|popen)\(|\bsystem\(\s*[^)\n]*(\$|\#\{|\+)|`[^`\n]*\#\{[^}]+\}[^`\n]*`""", re.X),
     "command executed through a shell or with a built string; check whether input reaches it unquoted", ["CWE-78", "ASVS:V1.2.5", "WSTG-INJT-12"]),
    ("py-eval", "injection", "high", PY, F(r"(?<![\w.])(eval|exec|compile)\(\s*(?![\"'])"),
     "dynamic code evaluation of a non-literal", ["CWE-95", "ASVS:V1.3.2", "WSTG-INJT-11"]),
    ("js-eval", "injection", "high", JS, F(r"(?<![\w.])eval\(|new\s+Function\(|\bvm\.runIn\w*\(|setTimeout\(\s*[\"'`]"),
     "dynamic code evaluation", ["CWE-95", "ASVS:V1.3.2"]),
    ("ssti", "injection", "high", PY | JS, F(r"render_template_string\(|Template\([^)\n]*(request\.|req\.)|Environment\([^)\n]*\)\.from_string\("),
     "template compiled from a string; check whether user input becomes template source", ["CWE-1336", "WSTG-INJT-18"]),
    ("deserialization", "injection", "high", CODE,
     F(r"\b(pickle|cPickle|marshal|dill)\.loads?\(|\bshelve\.open\(|yaml\.load\((?![^)\n]*SafeLoader)|yaml\.unsafe_load\(|jsonpickle\.decode\("
       r"|ObjectInputStream\(|\.readObject\(\)|\bunserialize\(|Marshal\.load\(|YAML\.load\(|node-serialize|serialize\.unserialize\("),
     "unsafe deserialization API; check whether the bytes can come from a caller", ["CWE-502", "ASVS:V1.5", "WSTG-INJT-23"]),
    ("mass-assignment", "injection", "medium", CODE,
     F(r"\*\*\s*request\.(json|form|data|get_json\(\))|Object\.assign\([^)\n]*req\.body|\.(update|create|build|new)\(\s*(request\.(json|form|data)|req\.body|params(\.permit!)?\s*\))|\.permit!"),
     "request body bound wholesale to a model; check that protected fields (role, owner, price) cannot be set", ["CWE-915", "WSTG-INJT-20"]),
    # --- SSRF / redirects / files ---
    ("ssrf-variable-url", "ssrf", "medium", PY | JS | GO | RB | PHP | JAVA,
     F(r"\b(requests|httpx|session)\.(get|post|put|patch|delete|head|request)\(\s*(?![\"'])[\w(]|urlopen\(\s*(?![\"'])|urllib\.request\.Request\(\s*(?![\"'])"
       r"|\baxios(\.(get|post|put|request))?\(\s*(?![\"'`/{])\w|(?<!def )(?<!function )\bfetch\(\s*(?![\"'`/])(req|request|params|query|body|url|target|input|u)\b|http\.(Get|Post)\(\s*(?!\")|file_get_contents\(\s*\$|Net::HTTP\.get\("),
     "outbound request with a non-literal URL; check whether the caller chooses host/scheme and whether internal addresses are blocked", ["CWE-918", "WSTG-INJT-19"]),
    ("open-redirect", "redirect", "medium", CODE,
     F(r"redirect\(\s*(request\.(args|values|form|GET|POST|query_params)|req\.(query|body|params)|params\[)|redirect\([^)\n]*\.get\(\s*[\"'](next|url|return\w*|redirect\w*|continue|dest\w*)[\"']|res\.redirect\([^)\n]*req\.(query|body|params)|redirect_to\s+params\["),
     "redirect target taken from the request; check for an allowlist or same-origin check", ["CWE-601", "WSTG-CLNT-04"]),
    ("path-from-request", "files", "high", CODE,
     F(r"(open|send_file|send_from_directory|os\.path\.join|Path|safe_join|readFile\w*|createReadStream|sendFile|path\.(join|resolve)|unlink\w*|File\.(read|open))\([^)\n]*(request\.(args|form|files|values|json|GET|POST|query_params|path_params)|req\.(query|params|body|file)|params\[|\$_(GET|POST|REQUEST)|filename|file_?name|user_path)"),
     "filesystem path built from request data; check normalization and containment in the intended directory", ["CWE-22", "ASVS:V5.3.2", "WSTG-ATHZ-01"]),
    ("archive-extract", "files", "medium", CODE, F(r"\.extractall\(|\.extract\(\s*\w+\s*,|unzip(Sync)?\(|AdmZip\("),
     "archive extraction; check member paths for traversal (zip-slip) and size limits", ["CWE-22", "CWE-409"]),
    ("xml-parser", "injection", "low", CODE, F(r"\b(etree\.(parse|fromstring)|minidom\.parse\w*|xml\.sax\.parse|DocumentBuilderFactory\.newInstance|SAXParserFactory|XMLInputFactory|libxml_disable_entity_loader\(\s*false|resolve_entities\s*=\s*True)"),
     "XML parsing; check external-entity handling if input is untrusted", ["CWE-611", "ASVS:V1.5.1", "WSTG-INJT-07"]),
    # --- browser output ---
    ("html-sink", "xss", "medium", JS | TPL | PY,
     F(r"\.(innerHTML|outerHTML)\s*\+?=|insertAdjacentHTML\(|document\.write(ln)?\(|dangerouslySetInnerHTML|v-html\s*=|\{\{\{[^}]+\}\}\}|\|\s*safe\b|\bmark_safe\(|\bMarkup\(|<%-\s"),
     "raw HTML sink; check whether the value can contain caller-controlled markup", ["CWE-79", "ASVS:V3.2.2", "WSTG-CLNT-01"]),
    # --- crypto / randomness / tokens ---
    ("weak-hash-password", "crypto", "high", CODE,
     F(r"(?i)(hashlib\.(md5|sha1|sha256)\(|createHash\(\s*[\"'](md5|sha1|sha256)[\"']|MessageDigest\.getInstance\(\s*\"(MD5|SHA-?1|SHA-?256)\"|\bmd5\(|\bsha1\(|Digest::(MD5|SHA1))[^\n]*(passw|pwd)"
       r"|(passw|pwd)[^\n]*(hashlib\.(md5|sha1|sha256)\(|createHash\(\s*[\"'](md5|sha1|sha256)[\"']|\bmd5\(|\bsha1\()"),
     "password hashed with a fast general-purpose hash; passwords need a slow salted KDF (bcrypt/scrypt/argon2/PBKDF2)", ["CWE-916", "ASVS:V11.4", "WSTG-CRYP-04"]),
    ("weak-hash", "crypto", "low", CODE, F(r"(?i)hashlib\.(md5|sha1)\(|createHash\(\s*[\"'](md5|sha1)[\"']|MessageDigest\.getInstance\(\s*\"(MD5|SHA-?1)\"|\bcrypto/(md5|sha1)\b|AES/ECB|\bDES\b|\bRC4\b"),
     "weak hash/cipher; matters only if used for security (signatures, passwords, integrity)", ["CWE-327", "ASVS:V11.3"]),
    ("insecure-random", "crypto", "medium", CODE,
     F(r"(?i)(\brandom\.(random|randint|choice|choices|getrandbits)\(|Math\.random\(\)|math/rand|\brand\(\)|mt_rand\()[^\n]*" + _SECRETY
       + r"|" + _SECRETY + r"[^\n]*(\brandom\.(random|randint|choice|choices|getrandbits)\(|Math\.random\(\)|\brand\(\)|mt_rand\()"),
     "non-cryptographic RNG near a token/secret; use a CSPRNG (secrets, crypto.randomBytes)", ["CWE-338", "ASVS:V11.5"]),
    ("tls-verify-off", "crypto", "medium", CODE | CFG,
     F(r"verify\s*=\s*False|rejectUnauthorized\s*:\s*false|InsecureSkipVerify\s*:\s*true|NODE_TLS_REJECT_UNAUTHORIZED\s*[=:]\s*[\"']?0|CURLOPT_SSL_VERIFYPEER\s*,\s*(0|false)|ssl\._create_unverified_context"),
     "TLS certificate verification disabled", ["CWE-295", "ASVS:V12.2"]),
    ("jwt-unverified", "authn", "high", CODE,
     F(r"algorithms\s*=\s*\[\s*[\"']none[\"']|[\"']verify_signature[\"']\s*:\s*False|jwt\.decode\([^)\n]*verify\s*=\s*False|algorithm[s]?\s*:\s*\[?\s*[\"']none[\"']|ignoreExpiration\s*:\s*true"),
     "token signature/expiry verification disabled or 'none' algorithm allowed", ["CWE-347", "ASVS:V9.1.1", "WSTG-SESS-10"]),
    ("jwt-decode-only", "authn", "low", JS, F(r"\bjwt\.decode\(|jwt_decode\("),
     "token decoded without verification; fine for display, not for authorization decisions", ["CWE-345", "ASVS:V9.1.1"]),
    # --- config: debug, CORS, cookies ---
    ("debug-enabled", "config", "medium", CODE | CFG,
     F(r"(?<![\w.])DEBUG\s*=\s*True\b|\.run\([^)\n]*debug\s*=\s*True|app\.debug\s*=\s*True|[\"']?debug[\"']?\s*:\s*true\b|DEBUG\s*=\s*(1|true)\s*$|display_errors\s*=\s*On"),
     "debug mode on; check whether this setting reaches a deployed environment (debug consoles can run code)", ["CWE-489", "ASVS:V13.4", "WSTG-ERRH-02"]),
    ("cors-wildcard", "config", "medium", CODE | CFG,
     F(r"Access-Control-Allow-Origin[\"']?\s*[,:=]\s*[\"']\*|\borigins?\s*[:=]\s*(\[\s*)?([\"']\*[\"']|true\b)|CORS\([^)\n]*(origins|resources)\s*=\s*[\"'{]?\s*[\"']?\*|@CrossOrigin\(\s*(\)|\"\*\"|origins\s*=\s*\"\*\")|allow_origins\s*=\s*\[\s*[\"']\*|AllowedOrigins[^\n]*\*|CORS_ORIGIN_ALLOW_ALL\s*=\s*True|CORS_ALLOW_ALL_ORIGINS\s*=\s*True"),
     "CORS allows any origin; serious only with credentials or sensitive responses", ["CWE-942", "ASVS:V3.4.2", "WSTG-CLNT-07"]),
    ("cookie-flags", "session", "medium", CODE | CFG,
     F(r"(SESSION|CSRF)_COOKIE_(SECURE|HTTPONLY)\s*=\s*False|httpOnly\s*:\s*false|\bsecure\s*:\s*false|httponly\s*=\s*False|secure\s*=\s*False|SameSite\s*[=:]\s*[\"']?None"),
     "cookie protection flag explicitly disabled", ["CWE-614", "CWE-1004", "ASVS:V3.3.1", "WSTG-SESS-02"]),
    ("cookie-set", "session", "low", CODE, F(r"\.set_cookie\(|res\.cookie\(|setcookie\(|cookies\[[^\]]+\]\s*=|http\.SetCookie\("),
     "cookie set; check Secure/HttpOnly/SameSite if it carries a session or secret (flags missing on this line)", ["CWE-614", "ASVS:V3.3.1"]),
    # --- secrets with insecure defaults ---
    ("fallback-secret", "secrets", "high", CODE,
     F(r"(?i)((environ\.get|getenv|env\.get|ENV\.fetch)\(\s*[\"'][A-Z0-9_]*(SECRET|KEY|TOKEN|PASSWORD|PASS|SALT)[A-Z0-9_]*[\"']\s*,\s*[\"'][^\"'\n]+[\"']"
       r"|process\.env\.[A-Z0-9_]*(SECRET|KEY|TOKEN|PASSWORD|PASS|SALT)[A-Z0-9_]*\s*(\|\||\?\?)\s*[\"'`][^\"'`\n]+[\"'`])"),
     "secret read from the environment with a hardcoded fallback; when the variable is missing the literal is used", ["CWE-1188", "CWE-798", "ASVS:V13.3"]),
    ("hardcoded-secret-name", "secrets", "medium", CODE | CFG,
     F(r"(?i)(?<![\w])(SECRET_KEY|JWT_SECRET|SESSION_SECRET|APP_SECRET|SIGNING_KEY|secret_key_base|secret)\s*[:=]\s*[\"'][^\"'\s]{4,}[\"']"),
     "secret-named value assigned a literal", ["CWE-798", "ASVS:V13.3"]),
    # --- IaC / container / shell ---
    ("iac-open-ingress", "iac", "medium", CFG, F(r"0\.0\.0\.0/0|::/0"), "network rule open to the internet; check port and intent", ["CWE-284"]),
    ("iac-wildcard-principal", "iac", "high", CFG, F(r"[\"']?Principal[\"']?\s*[:=]\s*(\{\s*[\"']AWS[\"']\s*:\s*)?[\"']\*[\"']|[\"']Action[\"']\s*:\s*[\"']\*[\"']"),
     "policy grants to any principal / any action", ["CWE-732"]),
    ("iac-public-storage", "iac", "high", CFG, F(r"acl\s*=\s*[\"']public-read(-write)?[\"']|block_public_acls\s*=\s*false|publicly_accessible\s*=\s*true|allUsers|allAuthenticatedUsers"),
     "storage or database exposed publicly", ["CWE-732"]),
    ("iac-privileged", "iac", "medium", CFG, F(r"privileged\s*:\s*true|hostPath\s*:|hostNetwork\s*:\s*true|allowPrivilegeEscalation\s*:\s*true|encrypted\s*=\s*false"),
     "container/host isolation or encryption weakened", ["CWE-250"]),
    ("docker-root", "iac", "low", ANY, F(r"^\s*USER\s+root\b|^\s*ADD\s+https?://"), "container runs as root or fetches remote content at build", ["CWE-250"]),
    ("curl-pipe-shell", "supply-chain", "medium", ANY, F(r"(curl|wget)\s[^|\n]*\|\s*(sudo\s+)?(ba|z)?sh\b"),
     "remote script piped to a shell", ["CWE-494"]),
    ("chmod-777", "config", "low", ANY, F(r"chmod\s+(-R\s+)?0?777\b|os\.chmod\([^)\n]*0o?777"), "world-writable permissions", ["CWE-732"]),
    # --- suppressions (security signals someone silenced) ---
    ("suppressed-signal", "suppression", "low", ANY, F(r"nosemgrep|gitleaks:allow|#\s*nosec\b|ult:ignore|eslint-disable[^\n]*security|NOSONAR"),
     "a security check is suppressed here; confirm the suppression is justified", []),
    # --- agent instructions / prompt-injection surface ---
    ("agent-instruction-text", "ai-agent", "medium", ANY,
     F(r"(?i)ignore\s+(all\s+|any\s+)?(previous|prior|above|earlier)\s+(instructions|prompts?)|disregard\s+(the\s+|your\s+)?(system|previous|prior)\s+(prompt|instructions)"
       r"|(ai|llm|coding)\s+(agents?|assistants?)[^\n]{0,60}\b(must|should|need to|are required to)\b[^\n]{0,40}\b(run|execute|send|post|upload|curl|fetch|commit|push|delete|print|reveal)"
       r"|\bnote to (the )?(ai|assistant|agent|claude|llm)\b|<\s*(system|instructions?)\s*>"),
     "text addressed to AI agents (prompt-injection surface); treat as data and report, never follow", ["CWE-1427"]),
    ("hidden-unicode", "ai-agent", "medium", ANY, F("[​-‏‪-‮⁠-⁤⁦-⁩﻿]|[\U000e0000-\U000e007f]"),
     "invisible/bidirectional Unicode; can hide instructions or code from reviewers", ["CWE-1007"]),
    ("agent-bypass-permissions", "ai-agent", "high", ANY,
     F(r"bypassPermissions|dangerously-?skip-?permissions|--dangerously-skip-permissions|dangerouslySkipPermissions|--yolo\b|allow_all_tools|enableAllProjectMcpServers[\"']?\s*:\s*true"),
     "agent permission checks disabled or all project MCP servers auto-trusted", ["CWE-250"]),
]

AGENT_SETTINGS_RULES = [
    ("agent-broad-allow", "ai-agent", "high", F(r"[\"'](Bash|Bash\(\*\)|Bash\(\s*\*?\s*:?\*\)|\*|Write|Edit|WebFetch)[\"']\s*[,\]]"),
     "broad tool allow rule in agent settings; any repo text the agent reads can steer these tools", ["CWE-250"]),
    ("agent-hook-fetch-exec", "ai-agent", "high", F(r"(curl|wget)[^\"\n]*\|\s*(ba)?sh|\bnpx\s+-y\b"),
     "agent hook downloads and runs code", ["CWE-494"]),
]
MCP_RULES = [
    ("mcp-unpinned-launcher", "ai-agent", "low", F(r"[\"'](npx|uvx|pipx|bunx)[\"']|[\"']-y[\"']|@latest"),
     "MCP server launched through a package runner; check that the package version is pinned", ["CWE-494"]),
    ("mcp-inline-secret", "ai-agent", "high", F(r"(?i)[\"'][A-Z0-9_]*(TOKEN|KEY|SECRET|PASSWORD|PAT)[A-Z0-9_]*[\"']\s*:\s*[\"'](?!\$\{|\$[A-Z_]|<|env:)[^\"'\s]{8,}[\"']"),
     "credential written inline in MCP config instead of read from the environment", ["CWE-798"]),
]

UNTRUSTED_EXPR = F(r"\$\{\{\s*([^}]*\b(github\.event\.[\w.\[\]'*-]+|github\.head_ref|inputs\.[\w-]+)[^}]*)\}\}")
SAFE_EXPR_TAIL = F(r"\.(number|id|sha|merged|draft|run_id|run_number|size|created_at|state)\s*$")
REMOVED_GUARD = F(r"(?i)(login_required|requires?_\w+|authori[sz]\w*|permission|is_admin|has_role|role\s*[!=]=|check_\w*|owner|tenant|"
                  r"user_id\s*[!=]=|current_user|csrf|verify\w*|validate\w*|@auth\w*|before_action|ensure_\w+|forbid\w*|"
                  r"abort\(\s*40[13]|Forbidden|Unauthorized|PermissionDenied|status\(\s*40[13]|sanitize\w*|escape\w*|allowlist|whitelist|rate_?limit)")
PLACEHOLDER = F(r"(?i)example|sample|dummy|fake|placeholder|changeme|change_me|your[_-]|xxxx|redacted|<[^>]+>|\*{3}|0{6}|123456|abcdef|not[_-]?a[_-]?real|lorem|\btest\b|testing|mock")


# --------------------------------------------------------------------------
def _tool_path() -> str | None:
    return os.environ.get("ULTIMATUM_SCAN_PATH")  # tests/overrides: where to look for external tools


def which(name: str) -> str | None:
    return shutil.which(name, path=_tool_path())


def _rel(p: Path, root: Path) -> str:
    try:
        return p.resolve().relative_to(root).as_posix()
    except ValueError:
        return p.as_posix()


def is_test_path(rel: str) -> bool:
    parts = rel.lower().split("/")
    name = parts[-1]
    return (any(x in TEST_PARTS for x in parts[:-1]) or name.startswith("test_") or
            re.search(r"(_test\.(go|py|rb)|\.(test|spec)\.[jt]sx?|_spec\.rb|Test\.java|\.example|\.sample|\.md)$", name) is not None)


def _git(root: Path, *a, timeout=60):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, timeout=timeout,
                          encoding="utf-8", errors="replace")


def tracked_files(root: Path) -> set[str] | None:
    try:
        r = _git(root, "ls-files")
    except (OSError, subprocess.SubprocessError):
        return None
    return set(r.stdout.splitlines()) if r.returncode == 0 else None


def parse_diff(root: Path, base: str, target_rel: str | None):
    """Return ({file: set(new_lines)}, [(file, old_line, text)] removed, error)."""
    args = ["diff", "--unified=0", "--no-color", "--no-ext-diff", base, "--"]
    if target_rel:
        args.append(target_rel)
    try:
        r = _git(root, *args)
    except (OSError, subprocess.SubprocessError) as e:
        return {}, [], f"git diff failed: {e}"
    if r.returncode != 0:
        return {}, [], f"git diff {base} failed (exit {r.returncode}): {r.stderr.strip()[:300]}"
    changed: dict[str, set[int]] = {}
    removed: list[tuple[str, int, str]] = []
    cur = old_cur = None
    new_ln = old_ln = 0
    for line in r.stdout.splitlines():
        if line.startswith("--- "):
            old_cur = line[6:] if line.startswith("--- a/") else None
            continue
        if line.startswith("+++ "):
            cur = line[6:] if line.startswith("+++ b/") else None
            if cur:
                changed.setdefault(cur, set())
            continue
        m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
        if m:
            old_ln, new_ln = int(m.group(1)), int(m.group(3))
            continue
        if line.startswith("+") and cur:
            changed[cur].add(new_ln)
            new_ln += 1
        elif line.startswith("-") and old_cur:
            removed.append((old_cur, old_ln, line[1:]))
            old_ln += 1
    try:
        u = _git(root, "ls-files", "--others", "--exclude-standard", *( [target_rel] if target_rel else []))
        for f in u.stdout.splitlines():
            changed[f] = {-1}  # -1 = whole file is new
    except (OSError, subprocess.SubprocessError):
        pass
    return changed, removed, None


def iter_files(target: Path, root: Path, only: set[str] | None, skipped: dict):
    if target.is_file():
        cands = [target]
    else:
        cands = []
        for dp, dns, fns in os.walk(target):
            dns[:] = sorted(d for d in dns if d not in SKIP_DIRS and not d.endswith(".egg-info"))
            for fn in sorted(fns):
                cands.append(Path(dp) / fn)
    for p in cands:
        rel = _rel(p, root)
        if only is not None and rel not in only:
            continue
        if p.is_symlink():
            skipped["symlink"] = skipped.get("symlink", 0) + 1
            continue
        try:
            size = p.stat().st_size
        except OSError:
            skipped["unreadable"] = skipped.get("unreadable", 0) + 1
            continue
        if size > MAX_BYTES:
            skipped["over-1MB"] = skipped.get("over-1MB", 0) + 1
            continue
        if p.name.endswith((".min.js", ".min.css", ".map")):
            skipped["minified"] = skipped.get("minified", 0) + 1
            continue
        try:
            data = p.read_bytes()
        except OSError:
            skipped["unreadable"] = skipped.get("unreadable", 0) + 1
            continue
        if b"\0" in data[:8192]:
            skipped["binary"] = skipped.get("binary", 0) + 1
            continue
        yield p, rel, data.decode("utf-8", "replace")


def _snippet(line: str) -> str:
    s = redact(line.strip())
    return s[:200] + ("…" if len(s) > 200 else "")


def _mask_literal(line: str) -> str:
    """For rules whose literal is a secret not covered by redact(): keep last 4 chars."""
    return re.sub(r"([\"'`])([^\"'`\n]{4,})\1", lambda m: m.group(0) if re.fullmatch(r"[A-Z0-9_]+", m.group(2)) else f"{m.group(1)}[REDACTED:literal:{m.group(2)[-4:]}]{m.group(1)}", line)


def _lead(rule, cls, sev, rel, ln, snippet, why, standards, conf="medium", low_reason=None, extra=None):
    d = {"source": "builtin", "rule_id": rule, "class": cls, "severity_hint": sev, "confidence": conf,
         "file": rel, "line": ln, "snippet": snippet, "why": why, "standards": standards}
    if low_reason:
        d["low_confidence_reason"] = low_reason
    if extra:
        d.update(extra)
    return d


def scan_secrets(rel: str, text: str, lines: list[str], tracked: set[str] | None) -> list[dict]:
    out = []
    name = rel.rsplit("/", 1)[-1]
    if name in LOCKFILES:
        return out
    test = is_test_path(rel)
    for kind, pat in SECRET_PATTERNS:
        for m in pat.finditer(text):
            ln = text.count("\n", 0, m.start()) + 1
            value = m.group(2) if kind == "assigned-secret" else m.group(0)
            if kind == "assigned-secret" and re.match(r"^(\$\{?|%\(|\{\{|process\.env|os\.environ|env\()", value):
                continue
            reasons = []
            if PLACEHOLDER.search(value) or len(set(value)) <= 4:
                reasons.append("value looks like a placeholder/example")
            if test:
                reasons.append("test/example/docs path")
            extra = {"secret_kind": kind, "value_length": len(value)}
            if name.startswith(".env") and tracked is not None:
                extra["tracked_by_git"] = rel in tracked
                if rel not in tracked:
                    reasons.append(".env file not tracked by git (local only)")
            snippet = "[REDACTED:private-key]" if kind == "private-key" else _snippet(lines[ln - 1] if ln - 1 < len(lines) else "")
            out.append(_lead(f"secret-{kind}", "secrets", "low" if reasons else "high", rel, ln, snippet,
                             f"possible {kind} in source; rotate if real and remove from history", ["CWE-798", "ASVS:V13.3"],
                             conf="low" if reasons else "medium", low_reason="; ".join(reasons) or None, extra=extra))
    return out


def scan_ci(rel: str, lines: list[str]) -> list[dict]:
    out = []
    text = "\n".join(lines)
    prt = re.search(r"(?m)^\s*(on:\s*\[?[^\n]*\bpull_request_target\b|pull_request_target\s*:|-\s*pull_request_target\b)", text) is not None \
        or re.search(r"(?m)^on:\s*pull_request_target\b", text) is not None
    in_run, run_indent = False, -1

    def check_expr(ln, s):
        for m in UNTRUSTED_EXPR.finditer(s):
            expr = m.group(2)
            if SAFE_EXPR_TAIL.search(expr):
                continue
            out.append(_lead("ci-expression-injection", "ci", "high", rel, ln, _snippet(lines[ln - 1]),
                             f"untrusted `{expr}` expanded directly into a shell script; pass it through env and quote it",
                             ["CWE-78", "CWE-94"]))

    for i, l in enumerate(lines, 1):
        stripped = l.lstrip()
        ind = len(l) - len(stripped)
        if in_run and stripped and ind <= run_indent:
            in_run = False
        m = re.match(r"^(\s*)(-\s+)?run:\s*(.*)$", l)
        if m:
            run_indent = len(m.group(1)) + (len(m.group(2)) if m.group(2) else 0)
            rest = m.group(3)
            check_expr(i, rest)
            in_run = rest.strip() == "" or rest.strip()[:1] in ("|", ">")
            continue
        if in_run:
            check_expr(i, l)
        if re.search(r"^\s*-?\s*script:\s*", l):  # actions/github-script inline JS
            check_expr(i, l)
        if re.search(r"permissions:\s*write-all", l):
            out.append(_lead("ci-permissions-write-all", "ci", "high", rel, i, _snippet(l),
                             "workflow token gets write access to everything; grant per-scope minimum", ["CWE-250"]))
        if prt and re.search(r"ref:\s*\$\{\{\s*(github\.event\.pull_request\.head\.(sha|ref)|github\.head_ref)|github\.event\.pull_request\.head\.repo\.full_name", l):
            out.append(_lead("ci-prt-checkout-head", "ci", "high", rel, i, _snippet(l),
                             "pull_request_target runs with base-repo secrets/token; checking out the PR head runs attacker code with them",
                             ["CWE-829"]))
        if prt and re.search(r"\$\{\{\s*secrets\.", l):
            out.append(_lead("ci-prt-secrets", "ci", "medium", rel, i, _snippet(l),
                             "secret used in a pull_request_target workflow; check that no fork-controlled code or text reaches it", ["CWE-200"]))
        um = re.search(r"uses:\s*([^@\s#]+)@([^\s#]+)", l)
        if um and not um.group(1).startswith(("./", "docker://")) and not re.fullmatch(r"[0-9a-f]{40}", um.group(2)) \
                and not um.group(1).startswith(("actions/", "github/")):
            out.append(_lead("ci-action-unpinned", "ci", "low", rel, i, _snippet(l),
                             "third-party action pinned by tag/branch, not commit SHA", ["CWE-829"]))
    if prt:
        for i, l in enumerate(lines, 1):
            if "pull_request_target" in l:
                out.append(_lead("ci-pull-request-target", "ci", "low", rel, i, _snippet(l),
                                 "pull_request_target trigger: privileged context for fork PRs; check checkout and secret use", ["CWE-829"]))
                break
    return out


def scan_text_rules(rel: str, ext: str, lines: list[str]) -> list[dict]:
    out = []
    test = is_test_path(rel)
    name = rel.rsplit("/", 1)[-1]
    is_dockerish = name.startswith("Dockerfile") or name.endswith(".dockerfile")
    for i, l in enumerate(lines, 1):
        if len(l) > 2000:
            continue
        for rid, cls, sev, exts, pat, why, std in RULES:
            if exts is not None and ext not in exts:
                if not (rid == "debug-enabled" and name.startswith(".env")):
                    continue
            if rid == "docker-root" and not is_dockerish:
                continue
            if not pat.search(l):
                continue
            snippet = _snippet(_mask_literal(l) if rid in ("fallback-secret", "hardcoded-secret-name") else l)
            reason = "test/example/docs path" if test and cls not in ("ai-agent", "suppression") else None
            out.append(_lead(rid, cls, "low" if reason else sev, rel, i, snippet, why, std,
                             conf="low" if reason else "medium", low_reason=reason))
    return out


def scan_agent_config(rel: str, lines: list[str]) -> list[dict]:
    out = []
    name = rel.rsplit("/", 1)[-1]
    is_settings = "/.claude/" in "/" + rel and name.startswith("settings") and name.endswith(".json")
    is_mcp = name in (".mcp.json", "mcp.json", "mcp_servers.json", "claude_desktop_config.json") or (name.endswith(".json") and "mcp" in name.lower())
    if not (is_settings or is_mcp):
        return out
    rules = (AGENT_SETTINGS_RULES if is_settings else []) + (MCP_RULES if is_mcp else [])
    for i, l in enumerate(lines, 1):
        for rid, cls, sev, pat, why, std in rules:
            if pat.search(l):
                out.append(_lead(rid, cls, sev, rel, i, _snippet(_mask_literal(l) if rid == "mcp-inline-secret" else l), why, std))
    return out


def dependency_inventory(root: Path, files: list[str]) -> tuple[list[dict], list[dict]]:
    inv, leads = [], []
    present = set(files)
    for rel in files:
        name = rel.rsplit("/", 1)[-1]
        d = rel.rsplit("/", 1)[0] + "/" if "/" in rel else ""
        if name in MANIFESTS or name in LOCKFILES or re.fullmatch(r"requirements[\w.-]*\.txt", name):
            inv.append({"file": rel, "kind": "lockfile" if name in LOCKFILES else "manifest",
                        "ecosystem": MANIFESTS.get(name, "PyPI" if name.startswith("requirements") else "")})
        if name in LOCK_FOR and not any((d + lf) in present or (root / (d + lf)).exists() for lf in LOCK_FOR[name]):
            leads.append(_lead("dep-no-lockfile", "dependencies", "low", rel, 1, name,
                               "manifest without a lockfile: installs resolve to whatever is newest", ["CWE-1104"]))
        if re.fullmatch(r"requirements[\w.-]*\.txt", name):
            try:
                for i, l in enumerate(raw_lines((root / rel).read_text("utf-8", "replace")), 1):
                    s = l.split("#", 1)[0].strip()
                    if s and not s.startswith(("-", "git+", "http")) and "==" not in s and "@" not in s:
                        leads.append(_lead("dep-unpinned", "dependencies", "low", rel, i, _snippet(s),
                                           "requirement not pinned to an exact version", ["CWE-1104"]))
                    if re.search(r"--(trusted-host|index-url\s+http://|extra-index-url)", l):
                        leads.append(_lead("dep-index-risk", "dependencies", "medium", rel, i, _snippet(l),
                                           "non-default or insecure package index", ["CWE-829"]))
            except OSError:
                pass
        if name == "package.json":
            try:
                pj = json.loads((root / rel).read_text("utf-8", "replace"))
                for k in ("preinstall", "install", "postinstall", "prepare"):
                    if isinstance(pj.get("scripts"), dict) and k in pj["scripts"]:
                        leads.append(_lead("dep-install-script", "dependencies", "low", rel, 1, f"scripts.{k}",
                                           "install-time script runs on every install", ["CWE-829"]))
            except (OSError, ValueError):
                pass
    return inv, leads


# --------------------------------------------------------------------------
# External tools
# --------------------------------------------------------------------------
def _run_tool(cmd: list[str], cwd: Path, timeout: int = 900):
    try:
        cp = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout,
                            encoding="utf-8", errors="replace")
        return cp.returncode, cp.stdout, cp.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"timed out after {timeout}s"
    except OSError as e:
        return 127, "", str(e)


def _source_line(root: Path, rel: str, ln: int) -> str:
    try:
        lines = raw_lines((root / rel).read_text("utf-8", "replace"))
        return _snippet(lines[ln - 1]) if 0 < ln <= len(lines) else ""
    except OSError:
        return ""


def run_semgrep(exe, cfg, target, root, base, rep):
    cmd = [exe, "scan", "--config", cfg, "--json", "--metrics=off", "--disable-version-check", "--quiet"]
    if base:
        cmd += ["--baseline-commit", base]
    cmd.append(str(target))
    code, out, err = _run_tool(cmd, root)
    status = "completed" if code in (0, 1) else "incomplete"
    entry = {"tool": "semgrep", "command": shlex.join(cmd), "exit_code": code, "status": status}
    leads = []
    try:
        data = json.loads(out) if out.strip() else {}
    except ValueError:
        data, status = {}, "incomplete"
        entry["status"] = status
    for r in data.get("results", []) or []:
        rel = _rel(Path(r.get("path", "")) if Path(r.get("path", "")).is_absolute() else root / r.get("path", ""), root)
        ln = int((r.get("start") or {}).get("line") or 1)
        sev = {"ERROR": "high", "WARNING": "medium"}.get((r.get("extra") or {}).get("severity", ""), "low")
        leads.append({"source": "semgrep", "rule_id": r.get("check_id", "?"), "class": "semgrep", "severity_hint": sev,
                      "confidence": "medium", "file": rel, "line": ln, "snippet": _source_line(root, rel, ln),
                      "why": redact(str((r.get("extra") or {}).get("message", "")))[:300], "standards": []})
    errs = data.get("errors") or []
    skipped = (data.get("paths") or {}).get("skipped") or []
    if errs or skipped or status != "completed":
        entry["note"] = f"errors={len(errs)} skipped_paths={len(skipped)}" + (f"; stderr: {redact(err.strip())[:300]}" if status != "completed" else "")
    rep["commands_run"].append(entry)
    rep["tools"]["semgrep"].update(ran=True, status=entry["status"])
    return leads


def run_gitleaks(exe, target, root, rep):
    sd = state_dir(root, "security")
    report = sd / f"gitleaks-{new_id('r')}.json"
    cmd = [exe, "dir", str(target), "--redact", "--exit-code", "3", "--report-format", "json", "--report-path", str(report)]
    code, out, err = _run_tool(cmd, root)
    status = {0: "completed", 3: "completed"}.get(code, "incomplete")
    entry = {"tool": "gitleaks", "command": shlex.join(cmd), "exit_code": code, "status": status}
    if status != "completed":
        entry["note"] = redact(err.strip())[:300]
    leads = []
    try:
        items = json.loads(report.read_text()) if report.exists() else []
    except ValueError:
        items = []
    for it in items or []:
        f = it.get("File", "")
        rel = _rel(Path(f) if Path(f).is_absolute() else root / f, root)
        ln = int(it.get("StartLine") or 1)
        leads.append({"source": "gitleaks", "rule_id": it.get("RuleID", "?"), "class": "secrets", "severity_hint": "high",
                      "confidence": "medium", "file": rel, "line": ln, "snippet": _source_line(root, rel, ln),
                      "why": redact(str(it.get("Description", "")))[:200], "standards": ["CWE-798"]})
    if report.exists():  # contains only redacted values (--redact); keep it private anyway
        os.chmod(report, 0o600)
    rep["commands_run"].append(entry)
    rep["tools"]["gitleaks"].update(ran=True, status=status)
    return leads


def run_osv(exe, target, root, online, rep):
    dbdir = os.environ.get("OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY")
    cmd = [exe, "scan", "source", "-r", "--format", "json"]
    if not online:
        cmd.append("--offline")
    cmd.append(str(target))
    code, out, err = _run_tool(cmd, root)
    meaning = {0: "completed: packages scanned, no known vulnerabilities", 1: "completed: vulnerabilities found",
               127: "error", 128: "nothing scanned (no packages found) — not a clean result"}
    status = "completed" if code in (0, 1) else "incomplete"
    entry = {"tool": "osv-scanner", "command": shlex.join(cmd), "exit_code": code, "status": status,
             "note": meaning.get(code, "scan did not complete") + ("" if online else f"; offline DB: {dbdir or '(default cache)'}")}
    leads, groups = [], 0
    try:
        data = json.loads(out) if out.strip() else {}
    except ValueError:
        data = {}
    for res in data.get("results", []) or []:
        src = ((res.get("source") or {}).get("path")) or ""
        rel = _rel(Path(src), root) if src else "?"
        for pk in res.get("packages", []) or []:
            p = pk.get("package") or {}
            for g in pk.get("groups", []) or [{"ids": [v.get("id") for v in pk.get("vulnerabilities", [])]}]:
                groups += 1
                leads.append({"source": "osv-scanner", "rule_id": ",".join(x for x in g.get("ids", []) if x), "class": "dependencies",
                              "severity_hint": "medium", "confidence": "medium", "file": rel, "line": 1,
                              "snippet": f"{p.get('ecosystem', '')} {p.get('name', '')}@{p.get('version', '')}",
                              "why": "known advisory for this version; reachability not checked", "standards": ["CWE-1395"]})
    rep["commands_run"].append(entry)
    rep["tools"]["osv-scanner"].update(ran=True, status=status)
    if code == 0:
        rep["advisory_status"] = "checked (osv-scanner): no known vulnerabilities in scanned packages"
    elif code == 1:
        rep["advisory_status"] = f"checked (osv-scanner): {groups} vulnerable package advisory group(s)"
    else:
        rep["advisory_status"] = f"unknown (osv-scanner exit {code}: {meaning.get(code, 'incomplete')})"
    return leads


# --------------------------------------------------------------------------
def cmd_scan(args) -> int:
    root = project_root()
    target = (Path(args.path) if args.path else root)
    if not target.is_absolute():
        target = (Path.cwd() / target)
    target = target.resolve()
    if not target.exists():
        print(f"[ult scan] error: path not found: {args.path}")
        return 2
    target_rel = _rel(target, root) if target != root else None

    rep: dict = {"tool": "ult scan", "version": 1, "root": str(root), "target": target_rel or ".", "diff_base": args.diff,
                 "commands_run": [], "tools": {}, "advisory_status": "unknown (osv-scanner not run)",
                 "files_scanned": 0, "files_skipped": {}, "leads": [], "dependency_inventory": [], "not_covered": NOT_COVERED}

    only = None
    removed: list = []
    changed: dict = {}
    if args.diff:
        changed, removed, err = parse_diff(root, args.diff, target_rel)
        if err:
            print(f"[ult scan] error: {err}")
            return 2
        only = set(changed)

    # ---- external tools ----
    ext_leads: list[dict] = []
    for name in ("semgrep", "gitleaks", "osv-scanner"):
        exe = which(name)
        t = rep["tools"][name] = {"present": bool(exe), "ran": False}
        if args.no_external:
            t["status"] = "not run: --no-external"
            continue
        if not exe:
            t["status"] = "not run: not installed"
            continue
        if name == "semgrep":
            if not args.semgrep_config:
                t["status"] = ("not run: no rules given. Pass --semgrep-config <local rules file/dir>; a registry pack "
                               "(p/...) downloads rules over the network, so pass it only with the user's consent")
                continue
            ext_leads += run_semgrep(exe, args.semgrep_config, target, root, args.diff, rep)
        elif name == "gitleaks":
            ext_leads += run_gitleaks(exe, target, root, rep)
        else:
            dbdir = os.environ.get("OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY")
            if not args.osv_online and not (dbdir and Path(dbdir).is_dir()):
                t["status"] = ("not run: needs the OSV.dev service (sends package names/versions) or a local DB. "
                               "Pass --osv-online with the user's consent, or set OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY")
                rep["advisory_status"] = "unknown (osv-scanner present but not run: offline DB not configured)"
                continue
            ext_leads += run_osv(exe, target, root, args.osv_online, rep)
    if not rep["tools"]["osv-scanner"]["present"] or args.no_external:
        rep["advisory_status"] = "unknown (no advisory scanner ran; run `osv-scanner scan source -r --format json .` to check)"

    # ---- built-in checks ----
    tracked = tracked_files(root)
    leads: list[dict] = []
    files_seen: list[str] = []
    for p, rel, text in iter_files(target, root, only, rep["files_skipped"]):
        rep["files_scanned"] += 1
        files_seen.append(rel)
        lines = raw_lines(text)
        ext = p.suffix.lower() if p.suffix else ("." + p.name.lstrip(".").lower() if p.name.startswith(".env") else "")
        if p.name.startswith(".env"):
            ext = ".env"
        leads += scan_secrets(rel, text, lines, tracked)
        leads += scan_text_rules(rel, ext, lines)
        if re.match(r"^\.github/workflows/[^/]+\.ya?ml$", rel) or rel.endswith((".gitlab-ci.yml",)):
            leads += scan_ci(rel, lines)
        leads += scan_agent_config(rel, lines)
    inv, dep_leads = dependency_inventory(root, files_seen)
    rep["dependency_inventory"] = inv
    leads += dep_leads
    leads += ext_leads

    if args.diff:
        def keep(ld):
            lines_ = changed.get(ld["file"])
            return lines_ is not None and (-1 in lines_ or ld["line"] in lines_ or ld.get("rule_id", "").startswith("dep-"))
        leads = [ld for ld in leads if keep(ld) or ld["source"] == "semgrep"]
        for f, ln, txt in removed:
            if target_rel and not (f == target_rel or f.startswith(target_rel.rstrip("/") + "/")):
                continue
            if REMOVED_GUARD.search(txt) and txt.strip() and not txt.strip().startswith(("#", "//", "*")):
                leads.append(_lead("diff-removed-guard", "change", "high", f, ln, _snippet(txt),
                                   "a line that looks like a security check was removed; find what replaced it (line number is in BASE)",
                                   [], extra={"line_ref": "base"}))

    # dedupe identical (rule, file, line), sort deterministically
    seen, uniq = set(), []
    for ld in leads:
        k = (ld["source"], ld["rule_id"], ld["file"], ld["line"])
        if k not in seen:
            seen.add(k)
            uniq.append(ld)
    uniq.sort(key=lambda d: (SEV_ORDER.get(d["severity_hint"], 3), d["file"], d["line"], d["rule_id"]))
    rep["leads"] = uniq

    # ---- output ----
    out_json = dump_json(rep)
    last = state_dir(root, "security") / "scan-last.json"
    write_private(last, out_json)
    if args.json:
        jp = Path(args.json)
        write_private(jp if jp.is_absolute() else Path.cwd() / jp, out_json)

    print(f"[ult scan] target={rep['target']}" + (f" diff={args.diff} ({len(changed)} changed file(s))" if args.diff else "")
          + f" files_scanned={rep['files_scanned']}" + (f" skipped={rep['files_skipped']}" if rep["files_skipped"] else ""))
    for name, t in rep["tools"].items():
        if not t["ran"]:
            print(f"  {name}: {t['status']}")
    for c in rep["commands_run"]:
        print(f"  ran: {redact(c['command'])}  -> exit {c['exit_code']} ({c['status']})" + (f"  [{c['note']}]" if c.get("note") else ""))
    print("  built-in checks: ran (secrets, risky sinks, CI, IaC, agent config, dependency hygiene)")
    print(f"  dependency advisories: {rep['advisory_status']}")
    by_sev: dict[str, int] = {}
    for ld in uniq:
        by_sev[ld["severity_hint"]] = by_sev.get(ld["severity_hint"], 0) + 1
    print(f"[ult scan] {len(uniq)} lead(s) " + " ".join(f"{k}={v}" for k, v in sorted(by_sev.items(), key=lambda kv: SEV_ORDER.get(kv[0], 3)))
          + " — LEADS, not findings: read the code path before reporting anything.")
    for ld in uniq[: args.max_print]:
        lowr = f" [low confidence: {ld['low_confidence_reason']}]" if ld.get("low_confidence_reason") else ""
        ref = " (base)" if ld.get("line_ref") == "base" else ""
        print(f"  {ld['severity_hint']:<6} {ld['source']}:{ld['rule_id']}  {ld['file']}:{ld['line']}{ref}  {ld['snippet']}{lowr}")
    if len(uniq) > args.max_print:
        print(f"  … {len(uniq) - args.max_print} more in {_rel(last, root)}")
    print(f"[ult scan] full JSON: {_rel(last, root)}" + (f" and {args.json}" if args.json else ""))
    print(f"[ult scan] {NOT_COVERED}")
    return 0


def register(sub):
    p = sub.add_parser("scan", help="security leads: installed scanners (offline-safe) + built-in checks")
    p.add_argument("--path", help="file or directory to scan (default: project root)")
    p.add_argument("--diff", metavar="BASE", help="only changed files/lines vs BASE (git diff BASE, plus untracked)")
    p.add_argument("--json", metavar="OUT", help="also write the JSON report here")
    p.add_argument("--no-external", action="store_true", help="do not run semgrep/gitleaks/osv-scanner even if installed")
    p.add_argument("--semgrep-config", metavar="CFG", help="semgrep rules: local file/dir, or p/... (network; needs consent)")
    p.add_argument("--osv-online", action="store_true", help="let osv-scanner query OSV.dev (needs the user's consent)")
    p.add_argument("--max-print", type=int, default=60, help="leads printed (JSON keeps all)")
    p.set_defaults(func=cmd_scan)
