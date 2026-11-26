#!/usr/bin/env python3
"""Lint a skill folder's SKILL.md frontmatter and size, without running anything in it.

Usage: skill_lint.py SKILL_DIR [SKILL_DIR ...] [--extra-keys k1,k2] [--json]
       skill_lint.py --self-check
Exit: 0 clean (warnings allowed), 1 at least one error, 2 bad usage.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

BASE_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
# Keys Claude Code itself reads on skills; accepted unless --strict-keys.
CLIENT_KEYS = {"argument-hint", "disable-model-invocation", "user-invocable", "model", "when_to_use", "version"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME, MAX_DESC, MAX_COMPAT = 64, 1024, 500
MAX_BODY_LINES, TOC_AFTER_LINES = 500, 300


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str, list[str]]:
    """Return (fields, body, problems). Handles `key: value`, quoted values and `>`/`|` blocks."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text, ["no frontmatter: the first line must be ---"]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, text, ["frontmatter is never closed with ---"]
    fields: dict[str, str] = {}
    problems: list[str] = []
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([\w-]+):[ \t]?(.*)$", line)
        if not m or line[0] in " \t":
            problems.append(f"frontmatter line {i + 1} is not `key: value`")
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        i += 1
        if value in {">", "|", ">-", "|-", ""}:
            block = []
            while i < end and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            joiner = "\n" if value.startswith("|") else " "
            value = joiner.join(b for b in block if b) if value else ("\n".join(block).strip() or "")
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key in fields:
            problems.append(f"key `{key}` appears twice")
        fields[key] = value
    return fields, "\n".join(lines[end + 1:]), problems


def lint(skill_dir: Path, extra: set[str], strict_keys: bool) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    entry = skill_dir / "SKILL.md"
    if not entry.is_file():
        return {"skill": str(skill_dir), "errors": ["SKILL.md not found"], "warnings": []}
    text = entry.read_text(encoding="utf-8", errors="replace")
    fields, body, problems = parse_frontmatter(text)
    errors += problems
    if fields is not None:
        allowed = BASE_KEYS | extra | (set() if strict_keys else CLIENT_KEYS)
        for key in sorted(set(fields) - allowed):
            errors.append(f"unexpected key `{key}`")
        name = fields.get("name", "")
        desc = fields.get("description", "")
        if not name:
            errors.append("missing `name`")
        elif not NAME_RE.match(name):
            errors.append(f"name `{name}` must be lower-case words joined by single hyphens")
        elif len(name) > MAX_NAME:
            errors.append(f"name is {len(name)} characters (limit {MAX_NAME})")
        elif name != skill_dir.name:
            warnings.append(f"name `{name}` differs from folder `{skill_dir.name}`")
        if not desc:
            errors.append("missing `description`")
        else:
            if len(desc) > MAX_DESC:
                errors.append(f"description is {len(desc)} characters (limit {MAX_DESC})")
            if "<" in desc or ">" in desc:
                errors.append("description contains < or >")
            if len(desc.split()) < 8:
                warnings.append("description is under 8 words: it may not say when to use the skill")
        if len(fields.get("compatibility", "")) > MAX_COMPAT:
            errors.append(f"compatibility is over {MAX_COMPAT} characters")
    body_lines = body.count("\n") + 1
    if body_lines > MAX_BODY_LINES:
        warnings.append(f"body is {body_lines} lines (aim under {MAX_BODY_LINES}; move detail to references)")
    shouty = len(re.findall(r"\b(?:MUST|NEVER|ALWAYS|CRITICAL)\b", body))
    if shouty > 5:
        warnings.append(f"{shouty} all-caps commands: say why instead")
    for ref in sorted(skill_dir.rglob("*.md")):
        if ref == entry:
            continue
        n = ref.read_text(encoding="utf-8", errors="replace").count("\n") + 1
        heads = len(re.findall(r"^#{2,3} ", ref.read_text(encoding="utf-8", errors="replace"), re.M))
        if n > TOC_AFTER_LINES and heads < 3:
            warnings.append(f"{ref.relative_to(skill_dir)} is {n} lines with few headings: add a contents list")
    return {"skill": str(skill_dir), "errors": errors, "warnings": warnings}


def self_check() -> int:
    cases = {
        "good-skill": ("---\nname: good-skill\ndescription: >\n  Use when a CSV export needs checking for\n"
                       "  broken quoting before it is shared.\n---\n# Body\n", 0, 0),
        "bad-name": ("---\nname: Bad--Name\ndescription: short\ncolour: blue\n---\n", 2, 1),
        "angle": ("---\nname: angle\ndescription: Use when <tag> soup needs cleaning in pasted HTML snippets today\n---\n", 1, 0),
        "nofront": ("# no frontmatter\n", 1, 0),
    }
    with tempfile.TemporaryDirectory() as tmp:
        for folder, (text, n_err, n_warn) in cases.items():
            d = Path(tmp) / folder
            d.mkdir()
            (d / "SKILL.md").write_text(text, encoding="utf-8")
            got = lint(d, set(), False)
            assert len(got["errors"]) == n_err, (folder, got)
            assert len(got["warnings"]) == n_warn, (folder, got)
    print(f"self-check passed: {len(cases)} cases")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("dirs", nargs="*", type=Path)
    parser.add_argument("--extra-keys", default="")
    parser.add_argument("--strict-keys", action="store_true", help="allow only the base keys")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.self_check:
        return self_check()
    if not args.dirs:
        parser.print_usage(sys.stderr)
        return 2
    extra = {k.strip() for k in args.extra_keys.split(",") if k.strip()}
    reports = [lint(d, extra, args.strict_keys) for d in args.dirs]
    if args.json:
        print(json.dumps(reports, indent=1))
    else:
        for r in reports:
            status = "FAIL" if r["errors"] else "ok"
            print(f"{status}  {r['skill']}")
            for e in r["errors"]:
                print(f"  error: {e}")
            for w in r["warnings"]:
                print(f"  warn:  {w}")
    return 1 if any(r["errors"] for r in reports) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
