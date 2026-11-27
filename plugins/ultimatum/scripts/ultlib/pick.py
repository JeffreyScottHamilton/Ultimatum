"""Pick the workflow for a plain-chat message: "website", "work" or "chat".

Used by the `ult-pick` UserPromptSubmit hook so Ultimatum starts without a slash command:
- website: a website named outright, or interface words inside a website project;
- work: a request to change, fix, test, review, debug or ship code in this project;
- chat: everything else (general questions, writing help, small talk), which gets nothing.
Questions about how code works stay in chat; Claude answers them without a workflow.
"""
from __future__ import annotations

import re
from pathlib import Path

from .route import _CONCRETE_RE, SECURITY_ROUTES, decide

# A request to do something, near the start (after an optional polite lead-in).
_LEAD = r"^\s*(?:(?:please|pls|ok|okay|so|now|hey|hi|also|and|then)[,!\s]+)*" \
        r"(?:(?:can|could|would|will)\s+you\s+(?:please\s+)?|(?:help\s+me|i\s+(?:need|want)\s+(?:you\s+)?to|let'?s|we\s+(?:need|should)(?:\s+to)?|go\s+ahead\s+and)\s+)?"
_ACT = r"(?:fix|add|implement|build|refactor|debug|investigate|migrate|optimi[sz]e|speed\s+up|review|audit|deploy|ship|release|upgrade|bump|rename|remove|delete|drop|update|change|make|write|create|set\s+up|configure|port|convert|integrate|test|profile|patch|harden|secure|scan|clean\s+up|resolve|handle|support|wire|hook\s+up|split|extract|move|replace|escape|parse|validate|sanitize|skip|stop|prevent|allow|enable|disable|cache|paginate|log|retry|rotate|score|measure|reduce|get|run|re-?run|merge|rebase|address|apply|restore|revert|finish|continue|resume|pick\s+up|map\s+out|map|document|lint|format|type-?check)"
_ACTION_RE = re.compile(_LEAD + _ACT + r"\b", re.I)
# The same request later in the message ("slugify drops digits; fix it").
_ACT_ANY_RE = re.compile(r"(?:^|[,;.:!]\s*|\b(?:and|then|please)\s+)" + _ACT + r"\b", re.I)
_NEED_RE = re.compile(r"^\s*(?:we|i)\s+(?:need|want|would\s+like)\b", re.I)

# Words that almost always mean code. A trailing "s" is allowed (routes, helpers).
_STRONG_RE = re.compile(
    r"\b(?:code|codebase|repo|repository|api|endpoint|route|handler|function|method|class|module|component|"
    r"script|cli|test|spec|ci|build|pipeline|pr|pull\s+request|branch|commit|diff|"
    r"bug|crash|exception|traceback|stack\s+trace|regression|flaky|typo|log|helper|caller|"
    r"navbar|tooltip|dashboard|dark\s+mode|a11y|playwright|column|importer|exporter|dedupe|postgres|mysql|sqlite|"
    r"replica|etl|release\s+note|smoke\s+test|migration|tool\s+call|subagent|mcp|cve|lodash|monorepo|jest|vitest|"
    r"middleware|p95|database|db|query|queries|schema|sql|orm|redis|queue|cron|worker|webhook|server|backend|"
    r"frontend|sdk|dependency|dependencies|dep|lockfile|config|env|docker|dockerfile|terraform|helm|deploy|"
    r"deployment|staging|prod|production|auth|login|logout|logged\s+(?:in|out)|session|cookie|jwt|oauth|"
    r"password|permission|tenant|csrf|xss|cors|csp|upload|download|export|csv|json|yaml|xml|payload|parser|regex|"
    r"button|modal|css|ui|ux|feature\s+flag|setting|pagination|scheduler|notification|email\s+template|readme|"
    r"changelog|typescript|javascript|npm|pip|yarn|node|django|flask|rails|eslint|prettier|"
    r"memory\s+leak|latency|bundle|holdout|eval|plugin|handoff|vulnerabilit(?:y|ie)|secret|"
    r"date\s+picker|picker|dropdown|input\s+field|form\s+field|signup|sign-up|checkout|startup\s+time|"
    r"rate\s+limit\w*|retr(?:y|ie)|s3|500|404|toml|ini|usage|coach)s?\b",
    re.I)

# Words that are code in a repo but also everyday words (job, order, list, report...).
_WEAK_RE = re.compile(
    r"\b(?:project|app|command|suite|workflow|merge|option|template|nav|menu|chart|toast|card|screenshot|row|"
    r"record|batch|generator|tag|version|release|gate|ship|traffic|roll\s*back|token|context|chat|agent|skill|"
    r"tool|hook|package|index|table|cache|job|service|client|library|kubernetes|k8s|import|pdf|page|form|layout|"
    r"screen|view|feature|flag|invoice|order|payment|cart|user|account|report|filter|search|sort|reminder|docs|"
    r"types|python|react|next|vue|go|rust|java|performance|admin|role|token|thumbnail|warehouse)s?\b",
    re.I)

# Plain writing or knowledge tasks: an edit verb aimed at prose, not code.
_PROSE_RE = re.compile(
    r"\b(?:email|e-mail|letter|paragraph|sentence|essay|poem|haiku|story|tweet|post|caption|bio|cover\s+letter|"
    r"message|text\s+message|speech|toast|recipe|grammar|spelling|wording|tone|translation|translate|joke|lyrics|"
    r"workout|meal|plan\s+for|itinerary|summary|summari[sz]e|article|text|list|notes|limerick|bio)\b", re.I)

# General knowledge or learning questions, even when they name a technology.
_GENERAL_RE = re.compile(
    r"\b(?:best\s+way\s+to\s+learn|worth\s+learning|should\s+i\s+learn|how\s+(?:do|can)\s+i\s+learn|difference\s+between|in\s+general|"
    r"like\s+i'?m\s+(?:five|5)|what\s+does\s+\S+\s+mean|what\s+is\s+an?\s+\w+\s+in\s+\w+\??$)", re.I)

# A question rather than a request.
_QUESTION_RE = re.compile(
    r"^\s*(?:what|what's|whats|who|whom|whose|why|how|where|when|which|is|are|was|were|do|does|did|should|"
    r"explain|tell\s+me|describe|walk\s+me\s+through|show\s+me\s+how|define|compare)\b|\?\s*$", re.I)
_FAILURE_RE = re.compile(
    r"\b(?:fail(?:s|ing|ed|ure)?|broken|break(?:s|ing)?|crash(?:es|ing|ed)?|error|exception|traceback|"
    r"bug|wrong|not\s+working|doesn'?t\s+work|isn'?t\s+working|red|flaky|timing\s+out|times\s+out|hangs?|"
    r"leak(?:s|ing)?|slow|vulnerab\w*|exploitable|skips?|drops?|loses?|duplicates?|missing|shows\s+up|raises|throws|blank|"
    r"returns\s+(?:the\s+)?wrong|off\s+by\s+one|stuck)\b", re.I)


_MAKE_RE = re.compile(r"\b(?:(?:can|could|would|will)\s+you|please|for\s+me|for\s+us|help\s+me\s+(?:make|create|render|animate|produce|cut|edit))\b", re.I)
_IDENT_RE = re.compile(r"\b[a-z]+[A-Z][A-Za-z0-9]*\b|\bre-?render")  # useEffect, getUserById


def _strong(text: str) -> bool:
    return bool(_STRONG_RE.search(text) or _CONCRETE_RE.search(text) or _IDENT_RE.search(text))


def pick(text: str, root: Path | None = None) -> str:
    """Return the workflow name for one plain-chat message (see the module docstring)."""
    text = (text or "").strip()
    if not text or text.startswith("/"):
        return "chat"
    d = decide(text[:2000], root=root, use_deps=False, lessons_on=False)
    if d.get("workflow") == "website":
        return "website"
    if d["route"] == "handoff" and not d["default"]:
        return "work"
    strong = _strong(text)
    code = strong or bool(_WEAK_RE.search(text))
    prose = bool(_PROSE_RE.search(text))
    if (prose and not strong and (d["default"] or not code)) or _GENERAL_RE.search(text):
        return "chat"
    if _QUESTION_RE.search(text):
        # "Why is the test failing?" is a debugging request; "How does X work?" is a question.
        if _FAILURE_RE.search(text) and code:
            return "work"
        if d["route"] in SECURITY_ROUTES and not d["default"]:
            return "work"
        if d["route"] not in ("discover",) and not d["default"] and code:
            return "work"
        return "chat"
    if d["route"] == "discover":
        return "chat"
    if _ACTION_RE.search(text) and code:
        return "work"
    if not d["default"] and (code or _ACT_ANY_RE.search(text)):
        return "work"
    if (_ACT_ANY_RE.search(text) or _NEED_RE.search(text)) and code:
        return "work"
    if _FAILURE_RE.search(text) and code:
        return "work"
    # A bug report written as a statement: "the export button downloads an empty file".
    if strong and not _ACTION_RE.search(text):
        return "work"
    return "chat"
