"""`ult sync` — copy lessons and project knowledge to or from a folder you choose.

  ult sync export --to DIR     global lessons + this project's knowledge.md
  ult sync import --from DIR   merge them back in

Layout in DIR:
  lessons.jsonl                         global lessons (learn.py format)
  projects/<name>-<hash8>/knowledge.md  one folder per project

Local-only: no git, no network. Point DIR at a clone of your own private repo
and let `/ultimatum:sync` run git with your approval. Import is a merge: lessons
are matched by text, the newer entry's module wins, counts take the maximum,
and knowledge lines are appended only when missing. Incoming text is untrusted
and goes through the same cleaning as `learn add`.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from . import learn
from .common import project_root, state_dir, write_private


def project_key(root: Path) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]", "-", root.name)[:40] or "project"
    return f"{name}-{hashlib.sha1(str(root).encode('utf-8')).hexdigest()[:8]}"


def _check_dir(d: Path) -> Path:
    if d.is_symlink():
        raise ValueError(f"refusing to use {d}: it is a symlink")
    return d


def export_to(dest: Path, root: Path) -> dict:
    _check_dir(dest).mkdir(mode=0o700, parents=True, exist_ok=True)
    lessons = learn.load_lessons(learn.global_home() / "lessons.jsonl")
    learn.write_lessons(dest / "lessons.jsonl", lessons)
    k = state_dir(root) / "knowledge.md"
    has_k = k.is_file() and not k.is_symlink()
    if has_k:
        target = dest / "projects" / project_key(root)
        _check_dir(target).mkdir(mode=0o700, parents=True, exist_ok=True)
        write_private(target / "knowledge.md", k.read_text(encoding="utf-8", errors="replace"))
    return {"lessons": len(lessons), "knowledge": has_k}


def _merge_lessons(src: Path) -> tuple[int, int]:
    """Returns (added, updated) for the global store."""
    path = learn.global_home() / "lessons.jsonl"
    local = learn.load_lessons(path)
    by_id = {r["id"]: r for r in local}
    added = updated = 0
    for inc in learn.load_lessons(src / "lessons.jsonl"):
        cur = by_id.get(inc["id"])
        if cur is None:
            local.append(inc)
            by_id[inc["id"]] = inc
            added += 1
            continue
        cur["count"] = max(cur["count"], inc["count"])
        if inc["updated"] > cur["updated"]:
            cur["updated"] = inc["updated"]
            cur["module"] = inc["module"] or cur["module"]
            updated += 1
    if added or updated:
        learn._mkdir_private(learn.global_home())
        learn.write_lessons(path, learn.prune(local))
    return added, updated


def _clean_lines(text: str) -> list[str]:
    return [c for c in (learn.clean_lesson(l) for l in text.splitlines()) if c]


def _merge_knowledge(src: Path, root: Path) -> int:
    inc_path = src / "projects" / project_key(root) / "knowledge.md"
    if not inc_path.is_file() or inc_path.is_symlink():
        return 0
    local_path = state_dir(root) / "knowledge.md"
    local_text = local_path.read_text(encoding="utf-8", errors="replace") if local_path.is_file() else ""
    have = set(_clean_lines(local_text))
    new = []
    for line in _clean_lines(inc_path.read_text(encoding="utf-8", errors="replace")):
        if line not in have:
            have.add(line)
            new.append(line)
    if new:
        sep = "" if not local_text or local_text.endswith("\n") else "\n"
        write_private(local_path, local_text + sep + "\n".join(new) + "\n")
    return len(new)


def import_from(src: Path, root: Path) -> dict:
    if not src.is_dir() or src.is_symlink():
        raise ValueError(f"not a folder: {src}")
    added, updated = _merge_lessons(src)
    lines = _merge_knowledge(src, root)
    return {"added": added, "updated": updated, "knowledge_lines": lines}


def cmd_sync(args) -> int:
    try:
        root = project_root()
        if args.action == "export":
            r = export_to(Path(args.to).expanduser().resolve(), root)
            print(f"[ult sync] exported {r['lessons']} global lesson(s); "
                  f"project knowledge {'included' if r['knowledge'] else 'not present'}")
            return 0
        r = import_from(Path(args.src).expanduser().resolve(), root)
        print(f"[ult sync] imported: {r['added']} new lesson(s), {r['updated']} updated, "
              f"{r['knowledge_lines']} knowledge line(s) added")
        return 0
    except ValueError as e:
        print(f"[ult sync] {e}")
        return 2


def register(sub):
    p = sub.add_parser("sync", help="export or import lessons and project knowledge to a folder you choose")
    ss = p.add_subparsers(dest="action", required=True)
    e = ss.add_parser("export", help="copy lessons and knowledge to a folder")
    e.add_argument("--to", required=True, metavar="DIR")
    i = ss.add_parser("import", help="merge lessons and knowledge from a folder")
    i.add_argument("--from", dest="src", required=True, metavar="DIR")
    p.set_defaults(func=cmd_sync)
