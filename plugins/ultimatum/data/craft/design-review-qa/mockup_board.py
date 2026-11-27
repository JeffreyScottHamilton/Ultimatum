#!/usr/bin/env python3
"""Lay built HTML mockups side by side on a local board, and read back the pick.

  mockup_board.py build calm.html dense.html editorial.html --brief "pricing page" --out designs/pricing
  mockup_board.py build ideal-hierarchy.html --baseline now.html --brief "..." --out designs/ideal
  mockup_board.py read designs/pricing/feedback.json

`build` copies each mockup into OUT/variants/, writes OUT/board.json (the brief, the
variants, their axes and hashes) and OUT/board.html: every variant live at desktop
and phone width, with a 1-5 rating, a comment, a pick and an overall note. The board
saves feedback.json by download and also shows it for copying. It warns when two
variants are near copies or a variant has no stated axis.

`read` checks feedback.json against the board it came from and prints the pick,
ratings and comments. Exit 0 with a pick, 4 with no pick, 2 on a bad file.

`--shots` also saves PNGs at each width into OUT/shots/ when the Python playwright
package and a Chromium are present (exit 3 if asked and missing).

Standard library only; no network. The board loads only the copied files.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path

WIDTHS = (1280, 390)
NEAR_COPY = 0.9
SLUG = re.compile(r"[^a-z0-9]+")


def slug(name: str) -> str:
    return SLUG.sub("-", name.lower()).strip("-") or "variant"


def shape(text: str) -> str:
    """Tag names, classes and CSS declarations: what makes two mockups look alike."""
    tags = re.findall(r"<\s*([a-zA-Z][\w-]*)", text)
    css = re.findall(r"[\w-]+\s*:\s*[^;{}]+;", "".join(re.findall(r"<style[^>]*>(.*?)</style>", text, re.S)))
    words = re.findall(r"\w+", re.sub(r"<[^>]+>", " ", text))
    return " ".join(tags + css + words[:400])


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, shape(a).split(), shape(b).split(), autojunk=False).ratio()


def parse_axes(items: list[str]) -> dict[str, str]:
    out = {}
    for it in items:
        name, sep, axis = it.partition("=")
        if not sep or not axis.strip():
            raise ValueError(f"--axis takes NAME=what this variant changes, got {it!r}")
        out[slug(name)] = axis.strip()
    return out


def plan(files: list[Path], baseline: Path | None, axes: dict[str, str]) -> tuple[list[dict], list[str]]:
    variants, warnings = [], []
    seen: set[str] = set()
    for i, f in enumerate(([baseline] if baseline else []) + files):
        text = f.read_text(encoding="utf-8", errors="replace")
        vid = "now" if baseline and i == 0 else slug(f.stem)
        while vid in seen:
            vid += "-2"
        seen.add(vid)
        title = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
        axis = axes.get(vid) or axes.get(slug(f.stem)) or ""
        meta = re.search(r'<meta\s+name=["\']variant-axis["\']\s+content=["\']([^"\']+)', text, re.I)
        if not axis and meta:
            axis = meta.group(1).strip()
        if vid == "now":
            axis = axis or "the design as it stands"
        variants.append({"id": vid, "file": f"variants/{vid}.html", "source": f.name,
                         "title": (title.group(1).strip() if title else f.stem)[:80], "axis": axis,
                         "sha256": hashlib.sha256(text.encode()).hexdigest(), "_text": text})
    for v in variants:
        if not v["axis"]:
            warnings.append(f"{v['id']}: no axis; say what it changes (--axis {v['id']}=..., or "
                            '<meta name="variant-axis" content="...">)')
    axes_seen: dict[str, str] = {}
    for v in variants:
        k = v["axis"].lower()
        if k and k in axes_seen:
            warnings.append(f"{v['id']} and {axes_seen[k]} name the same axis ({v['axis']})")
        axes_seen.setdefault(k, v["id"])
    for i, a in enumerate(variants):
        for b in variants[i + 1:]:
            r = similarity(a["_text"], b["_text"])
            if r >= NEAR_COPY:
                warnings.append(f"{a['id']} and {b['id']} are {r:.0%} alike; one direction, not two")
    return variants, warnings


CSS = """
:root{--bg:#f4f3ef;--ink:#1b1b1a;--muted:#5a5954;--line:#d6d4cc;--card:#fff;--accent:#1f4fd1}
@media (prefers-color-scheme:dark){:root{--bg:#161615;--ink:#efeee9;--muted:#a6a49c;--line:#34332f;--card:#1f1f1d;--accent:#8aa8ff}}
*{box-sizing:border-box}body{background:var(--bg);margin:0;color:var(--ink);font:15px/1.5 system-ui,sans-serif}
header,footer{padding:20px 24px;max-width:1400px;margin:auto}h1{font-size:20px;margin:0 0 4px}
.brief{color:var(--muted);margin:0}.warn{border-left:3px solid #c77700;padding:6px 10px;margin:8px 0;color:var(--ink)}
main{gap:24px;display:grid;grid-template-columns:100%;min-width:0;padding:0 24px;max-width:1400px;margin:auto}
section{min-width:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}
.top{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}.top h2{font-size:17px;margin:0}
.axis{color:var(--muted)}.frames{display:flex;gap:16px;overflow-x:auto;margin:12px 0}
.frame{flex:none;border-radius:6px;border:1px solid var(--line);overflow:hidden;background:#fff}
.frame span{display:block;font-size:12px;color:var(--muted);padding:4px 8px;border-bottom:1px solid var(--line)}
iframe{border:0;display:block;transform-origin:0 0}
.controls{display:flex;gap:16px;flex-wrap:wrap;align-items:center}
textarea{width:100%;min-height:56px;font:inherit;color:inherit;background:transparent;border-radius:6px;border:1px solid var(--line);padding:8px}
label{display:inline-flex;gap:6px;align-items:center;min-height:44px}
button{font:inherit;min-height:44px;padding:0 18px;border-radius:8px;border:0;background:var(--accent);color:#fff;cursor:pointer}
#out{min-height:120px;font:12px/1.4 ui-monospace,monospace}
"""

JS = """
const board=JSON.parse(document.getElementById('board').textContent);
function collect(){const v={};for(const x of board.variants){const s=document.querySelector('[name=rate-'+x.id+']:checked');
v[x.id]={rating:s?Number(s.value):null,comment:document.getElementById('c-'+x.id).value.trim()}}
const p=document.querySelector('[name=pick]:checked');
return {board:board.id,pick:p?p.value:null,variants:v,overall:document.getElementById('overall').value.trim()}}
function show(){document.getElementById('out').value=JSON.stringify(collect(),null,2)}
document.addEventListener('input',show);show();
document.getElementById('save').onclick=()=>{const b=new Blob([JSON.stringify(collect(),null,2)],{type:'application/json'});
const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='feedback.json';a.click();URL.revokeObjectURL(a.href)};
"""


def frame(v: dict, width: int, scale: float) -> str:
    h = 760 if width > 600 else 780
    return (f'<div class="frame" style="width:{int(width * scale) + 2}px"><span>{width}px</span>'
            f'<iframe src="{html.escape(v["file"])}" title="{html.escape(v["title"])} at {width}px" '
            f'loading="lazy" style="width:{width}px;height:{h}px;transform:scale({scale});'
            f'margin-bottom:{int(h * scale - h)}px"></iframe></div>')


def board_html(brief: str, board_id: str, variants: list[dict], warnings: list[str]) -> str:
    esc = html.escape
    parts = [f"<!doctype html><html lang=en><meta charset=utf-8><meta content='width=device-width,initial-scale=1' name=viewport>"
             f"<title>Board: {esc(brief[:60])}</title><style>{CSS}</style><body><header><h1>Pick a direction</h1>"
             f"<p class=brief>{esc(brief)}</p>"]
    parts += [f"<p class=warn>{esc(w)}</p>" for w in warnings]
    parts.append("</header><main>")
    for v in variants:
        rates = "".join(f"<label><input type=radio name='rate-{v['id']}' value={n}>{n}</label>" for n in range(1, 6))
        parts.append(
            f"<section aria-labelledby='h-{v['id']}'><div class=top><h2 id='h-{v['id']}'>{esc(v['title'])}</h2>"
            f"<span class=axis>{esc(v['axis'] or 'no axis stated')}</span></div>"
            f"<div class=frames>{frame(v, WIDTHS[0], 0.5)}{frame(v, WIDTHS[1], 0.75)}</div>"
            f"<div class=controls><label><input type=radio name=pick value='{v['id']}'>Pick this one</label>"
            f"<span>Rating:</span>{rates}</div>"
            f"<label for='c-{v['id']}' style='min-height:0'>What works, what doesn't</label>"
            f"<textarea id='c-{v['id']}'></textarea></section>")
    manifest = json.dumps({"id": board_id, "variants": [{"id": v["id"]} for v in variants]}).replace("</", "<\\/")
    parts.append(
        "</main><footer><label for=overall style='min-height:0'>Overall: mix, change, or another round?</label>"
        "<textarea id=overall></textarea><p><button id=save type=button>Save feedback.json</button></p>"
        "<label for=out style='min-height:0'>Or copy this back to the agent</label><textarea id=out readonly></textarea>"
        f"</footer><script type=application/json id=board>{manifest}</script>"
        f"<script>{JS}</script></body></html>")
    return "".join(parts)


def shots(out: Path, variants: list[dict]) -> str:
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from render_check import launch  # same browser search as the render check
    pw, browser, why = launch()
    if not browser:
        return why
    try:
        (out / "shots").mkdir(exist_ok=True)
        for v in variants:
            for w in WIDTHS:
                page = browser.new_page(viewport={"width": w, "height": 900})
                page.route("**/*", lambda r: r.continue_() if r.request.url.startswith(("file:", "data:"))
                           else r.abort())
                page.goto((out / v["file"]).resolve().as_uri())
                page.screenshot(path=str(out / "shots" / f"{v['id']}-{w}.png"), full_page=True)
                page.close()
    finally:
        browser.close()
        pw.stop()
    return ""


def cmd_build(a) -> int:
    files = [Path(f) for f in a.variants]
    base = Path(a.baseline) if a.baseline else None
    missing = [str(f) for f in files + ([base] if base else []) if not f.is_file()]
    if missing:
        print("mockup-board: no such file " + ", ".join(missing), file=sys.stderr)
        return 2
    if len(files) + bool(base) < 2:
        print("mockup-board: a board needs two or more mockups (or one and --baseline)", file=sys.stderr)
        return 2
    try:
        axes = parse_axes(a.axis)
    except ValueError as e:
        print("mockup-board: " + str(e), file=sys.stderr)
        return 2
    variants, warnings = plan(files, base, axes)
    out = Path(a.out)
    (out / "variants").mkdir(parents=True, exist_ok=True)
    srcs = ([base] if base else []) + files
    for v, src in zip(variants, srcs):
        shutil.copyfile(src, out / v["file"])
        for extra in a.assets:  # shared css/js/images the mockups link to
            p = Path(extra)
            dest = out / "variants" / p.name
            if p.is_dir():
                shutil.copytree(p, dest, dirs_exist_ok=True)
            elif p.is_file():
                shutil.copyfile(p, dest)
    board_id = hashlib.sha256((a.brief + "".join(v["sha256"] for v in variants)).encode()).hexdigest()[:12]
    for v in variants:
        v.pop("_text")
    (out / "board.json").write_text(json.dumps({"id": board_id, "brief": a.brief, "variants": variants,
                                                "warnings": warnings}, indent=2), encoding="utf-8")
    (out / "board.html").write_text(board_html(a.brief, board_id, variants, warnings), encoding="utf-8")
    print(f"board {board_id}: {out / 'board.html'}")
    for v in variants:
        print(f"  {v['id']:16} {v['axis'] or '(no axis)'}")
    for w in warnings:
        print("  warn: " + w)
    if a.shots:
        why = shots(out, variants)
        if why:
            print(f"mockup-board: no screenshots ({why})")
            return 3
        print(f"  shots: {out / 'shots'}")
    return 0


def cmd_read(a) -> int:
    fb_path = Path(a.feedback)
    board_path = Path(a.board) if a.board else fb_path.parent / "board.json"
    try:
        fb = json.loads(fb_path.read_text(encoding="utf-8"))
        board = json.loads(board_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"mockup-board: cannot read ({e})", file=sys.stderr)
        return 2
    ids = [v["id"] for v in board.get("variants", [])]
    if not isinstance(fb, dict) or fb.get("board") != board.get("id"):
        print("mockup-board: this feedback is for another board", file=sys.stderr)
        return 2
    votes = fb.get("variants") if isinstance(fb.get("variants"), dict) else {}
    pick = fb.get("pick")
    if pick is not None and pick not in ids:
        print(f"mockup-board: pick {pick!r} is not on the board", file=sys.stderr)
        return 2
    print(f"brief: {board.get('brief', '')}")
    print(f"pick: {pick or 'none'}")
    axes = {v["id"]: v.get("axis", "") for v in board["variants"]}
    for vid in ids:
        row = votes.get(vid) if isinstance(votes.get(vid), dict) else {}
        r = row.get("rating")
        r = r if isinstance(r, int) and 1 <= r <= 5 else "-"
        c = str(row.get("comment") or "")[:500]
        print(f"  {vid:16} {r}/5  {axes[vid]}" + (f"\n      {c}" if c else ""))
    if fb.get("overall"):
        print("overall: " + str(fb["overall"])[:1000])
    return 0 if pick else 4


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("variants", nargs="+")
    b.add_argument("--brief", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--baseline", default="")
    b.add_argument("--axis", action="append", default=[], help="NAME=what it changes")
    b.add_argument("--assets", action="append", default=[], help="file or folder the mockups link to")
    b.add_argument("--shots", action="store_true")
    r = sub.add_parser("read")
    r.add_argument("feedback")
    r.add_argument("--board", default="")
    a = ap.parse_args(argv)
    return cmd_build(a) if a.cmd == "build" else cmd_read(a)


if __name__ == "__main__":
    sys.exit(main())
