#!/usr/bin/env python3
"""Build a one-file choice board for questions that are easier to see than read.

Standard library only. No server, no open port, no network: the board is a
single offline HTML file. The person clicks their picks, copies one answer
line, and pastes it back into the chat, where `read` turns it into JSON.

    python3 choice_board.py check spec.json
    python3 choice_board.py build spec.json --out board.html [--theme auto|light|dark]
    python3 choice_board.py read spec.json "pick homepage: layout=b; palette=a,c"
    python3 choice_board.py rules
    python3 choice_board.py --self-check

Exit 0 clean, 1 findings (or an answer that does not fit the spec), 2 bad
arguments or an unreadable spec.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import mimetypes
import re
import sys
from pathlib import Path

ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,31}$")
REMOTE = re.compile(r"""(?:https?:)?//[a-z0-9]""", re.I)
ACTIVE = re.compile(r"<\s*(script|iframe|object|embed|link|meta|base|form)\b|\son[a-z]+\s*=|javascript:", re.I)
IMAGE_TYPES = {"image/png", "image/jpeg", "image/gif", "image/webp", "image/svg+xml"}
IMAGE_MAX = 2 * 1024 * 1024
MAX_ONE = 4

RULES = {
    "ids": ("error", "question and option ids are short lower-case words with hyphens, unique where they live"),
    "label": ("error", "every question has a prompt and every option a label; the answer line and screen readers use them"),
    "offline": ("error", "shown fragments stay inert and local: no scripts, handlers, frames, forms or remote URLs"),
    "image": ("error", "an image path exists, is PNG, JPEG, GIF, WebP or SVG, and is at most 2 MB"),
    "too-many": ("warn", "a pick-one question offers at most four options; more is a list to read, not a choice to see"),
    "visual": ("warn", "a question shows at least one option; one with only words belongs in the chat"),
}


class SpecError(ValueError):
    pass


def load(path):
    try:
        spec = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SpecError(f"cannot read {path}: {exc}") from None
    if not isinstance(spec, dict) or not isinstance(spec.get("questions"), list) or not spec["questions"]:
        raise SpecError("the spec needs a non-empty 'questions' list")
    for q in spec["questions"]:
        if not isinstance(q, dict) or not isinstance(q.get("options"), list) or not q["options"]:
            raise SpecError("every question needs a non-empty 'options' list")
        if q.get("pick", "one") not in ("one", "many"):
            raise SpecError(f"question {q.get('id')!r}: 'pick' is 'one' or 'many'")
        if not all(isinstance(o, dict) for o in q["options"]):
            raise SpecError(f"question {q.get('id')!r}: every option is an object")
    return spec


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s[:32].strip("-") or "board"


def check(spec, base):
    """Return findings as (rule, where, message)."""
    out = []
    seen_q = set()
    for qi, q in enumerate(spec["questions"]):
        qid = q.get("id")
        where = f"question {qid or qi + 1}"
        if not isinstance(qid, str) or not ID.match(qid) or qid == "note" or qid in seen_q:
            out.append(("ids", where, "id missing, malformed, reserved ('note') or repeated"))
        seen_q.add(qid)
        if not str(q.get("prompt", "")).strip():
            out.append(("label", where, "no prompt"))
        seen_o = set()
        shown = 0
        for oi, o in enumerate(q["options"]):
            oid = o.get("id")
            ow = f"{where}, option {oid or oi + 1}"
            if not isinstance(oid, str) or not ID.match(oid) or oid in seen_o:
                out.append(("ids", ow, "id missing, malformed or repeated"))
            seen_o.add(oid)
            if not str(o.get("label", "")).strip():
                out.append(("label", ow, "no label"))
            frag = o.get("show")
            if frag is not None:
                if not isinstance(frag, str):
                    out.append(("offline", ow, "'show' is an HTML or SVG string"))
                elif ACTIVE.search(frag):
                    out.append(("offline", ow, "fragment has a script, handler, frame, form or javascript: URL"))
                elif REMOTE.search(frag):
                    out.append(("offline", ow, "fragment loads something remote; embed it or use 'image'"))
                shown += 1
            img = o.get("image")
            if img is not None:
                shown += 1
                problem = image_problem(img, base)
                if problem:
                    out.append(("image", ow, problem))
        if q.get("pick", "one") == "one" and len(q["options"]) > MAX_ONE:
            out.append(("too-many", where, f"{len(q['options'])} options; keep it to {MAX_ONE} or split the question"))
        if not shown:
            out.append(("visual", where, "nothing is shown; ask it in the chat instead"))
    return out


def image_problem(img, base):
    if not isinstance(img, str) or REMOTE.match(img) or img.startswith("data:"):
        return "'image' is a local file path"
    p = (base / img) if not Path(img).is_absolute() else Path(img)
    if not p.is_file():
        return f"no file at {img}"
    kind = mimetypes.guess_type(p.name)[0]
    if kind not in IMAGE_TYPES:
        return f"{p.suffix or 'this file'} is not an allowed image type"
    if p.stat().st_size > IMAGE_MAX:
        return "larger than 2 MB; export a smaller copy"
    return None


def data_uri(img, base):
    p = (base / img) if not Path(img).is_absolute() else Path(img)
    kind = mimetypes.guess_type(p.name)[0]
    return f"data:{kind};base64," + base64.b64encode(p.read_bytes()).decode("ascii")


SCRIPT = """
(function () {
  var form = document.getElementById('board');
  var line = document.getElementById('answer');
  var copy = document.getElementById('copy');
  var status = document.getElementById('status');
  function quote(s) { return '"' + s.replace(/\\\\/g, '\\\\\\\\').replace(/"/g, '\\\\"').replace(/\\s+/g, ' ').trim() + '"'; }
  function build() {
    var parts = [];
    form.querySelectorAll('fieldset[data-q]').forEach(function (fs) {
      var picked = [];
      fs.querySelectorAll('input:checked').forEach(function (i) { picked.push(i.value); });
      if (picked.length) parts.push(fs.dataset.q + '=' + picked.join(','));
    });
    var note = form.querySelector('textarea').value.trim();
    if (note) parts.push('note=' + quote(note));
    line.value = 'pick ' + form.dataset.board + ': ' + (parts.length ? parts.join('; ') : '(nothing picked yet)');
    copy.disabled = !parts.length;
  }
  form.addEventListener('input', build);
  form.addEventListener('change', build);
  form.addEventListener('submit', function (e) { e.preventDefault(); });
  copy.addEventListener('click', function () {
    var done = function () { status.textContent = 'Copied. Paste it into the chat.'; };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(line.value).then(done, function () { line.select(); status.textContent = 'Selected. Copy it with your keyboard.'; });
    } else { line.select(); status.textContent = 'Selected. Copy it with your keyboard.'; }
  });
  build();
})();
""".strip()

STYLE = """
:root{--bg:#f7f6f2;--card:#fff;--ink:#1c1b19;--soft:#5d5a53;--line:#d9d5cc;--pick:#2f5d50;--pick-bg:#e6efe9;--focus:#1f4fa8}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#161615;--card:#21201e;--ink:#eeebe4;--soft:#aaa59a;--line:#3a3833;--pick:#8cc5b0;--pick-bg:#1f2e29;--focus:#8fb4ff}}
:root[data-theme=dark]{--bg:#161615;--card:#21201e;--ink:#eeebe4;--soft:#aaa59a;--line:#3a3833;--pick:#8cc5b0;--pick-bg:#1f2e29;--focus:#8fb4ff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1080px;margin:0 auto;padding:32px 16px 220px}
h1{font-size:1.6rem;line-height:1.2;margin:0 0 4px}
.lede,.hint{color:var(--soft);margin:0 0 24px}
fieldset{border:0;margin:0 0 40px;padding:0;min-width:0}
legend{font-size:1.2rem;font-weight:650;padding:0;margin-bottom:4px}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr))}
.opt{position:relative;display:flex;flex-direction:column;background:var(--card);border:2px solid var(--line);border-radius:12px;overflow:hidden;cursor:pointer}
.opt input{position:absolute;width:1px;height:1px;margin:-1px;padding:0;border:0;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}
.opt:has(input:checked){border-color:var(--pick);background:var(--pick-bg)}
.opt:has(input:focus-visible){outline:3px solid var(--focus);outline-offset:3px}
.show{min-height:120px;display:grid;place-items:center;border-bottom:1px solid var(--line);background:var(--bg);overflow:hidden}
.show>img,.show>svg{display:block;max-width:100%;height:auto}
.text{padding:12px 14px 14px}
.text b{display:flex;gap:8px;align-items:baseline}
.key{font:600 .8rem/1 ui-monospace,monospace;color:var(--soft)}
.text p{margin:4px 0 0;color:var(--soft);font-size:.95rem}
.mark{margin-left:auto;font-size:.85rem;color:var(--pick);visibility:hidden}
.opt:has(input:checked) .mark{visibility:visible}
label.note{display:block;font-weight:650;margin-bottom:6px}
textarea{width:100%;min-height:72px;font:inherit;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px}
.bar{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);padding:12px 16px}
.bar div{max-width:1080px;margin:0 auto;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.bar output{flex:1 1 320px;min-width:0}
#answer{width:100%;font:14px/1.4 ui-monospace,monospace;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:inherit}
button{font:inherit;font-weight:600;padding:9px 16px;border-radius:8px;border:0;background:var(--pick);color:var(--card);cursor:pointer;min-height:44px}
button:disabled{opacity:.5;cursor:not-allowed}
#status{color:var(--soft);font-size:.9rem;min-height:1.2em;flex-basis:100%}
@media (prefers-reduced-motion:no-preference){.opt{transition:border-color .15s,background-color .15s}}
""".strip()


def render(spec, base, theme="auto"):
    e = html.escape
    title = str(spec.get("title") or "Pick one")
    board = slug(spec.get("board") or title)
    sha = base64.b64encode(hashlib.sha256(SCRIPT.encode("utf-8")).digest()).decode("ascii")
    csp = f"default-src 'none'; img-src data:; style-src 'unsafe-inline'; script-src 'sha256-{sha}'; form-action 'none'; base-uri 'none'"
    theme_attr = f' data-theme="{theme}"' if theme in ("light", "dark") else ""
    out = [
        "<!doctype html>",
        f'<html lang="{e(str(spec.get("lang") or "en"))}"{theme_attr}>',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<meta http-equiv="Content-Security-Policy" content="{csp}">',
        f"<title>{e(title)}</title>",
        f"<style>{STYLE}</style>",
        "</head>",
        "<body>",
        "<main>",
        f"<h1>{e(title)}</h1>",
    ]
    if spec.get("intro"):
        out.append(f'<p class="lede">{e(str(spec["intro"]))}</p>')
    out.append(f'<form id="board" data-board="{e(board)}" novalidate>')
    for q in spec["questions"]:
        many = q.get("pick", "one") == "many"
        kind = "checkbox" if many else "radio"
        qid = str(q["id"])
        out.append(f'<fieldset data-q="{e(qid)}">')
        out.append(f"<legend>{e(str(q['prompt']))}</legend>")
        hint = q.get("note") or ("Pick any that fit." if many else "Pick one.")
        out.append(f'<p class="hint">{e(str(hint))}</p>')
        out.append('<div class="grid">')
        for o in q["options"]:
            oid = str(o["id"])
            label = str(o["label"])
            out.append(f'<label class="opt">')
            out.append(f'<input type="{kind}" name="{e(qid)}" value="{e(oid)}">')
            if o.get("image"):
                alt = str(o.get("alt") or label)
                out.append(f'<span class="show"><img src="{data_uri(o["image"], base)}" alt="{e(alt)}"></span>')
            elif o.get("show"):
                out.append(f'<span class="show" aria-hidden="true">{o["show"]}</span>')
            out.append(f'<span class="text"><b><span class="key">{e(oid)}</span> {e(label)}'
                       f'<span class="mark">Picked</span></b>')
            if o.get("note"):
                out.append(f"<p>{e(str(o['note']))}</p>")
            out.append("</span></label>")
        out.append("</div></fieldset>")
    out += [
        '<label class="note" for="note">Anything to add?</label>',
        '<textarea id="note" name="note" placeholder="Optional: what to keep or change"></textarea>',
        "</form>",
        "<noscript><p class=\"hint\">Scripts are off, so no answer line is built. Tell me your picks in the chat "
        f"by question and option id, for example <code>{e(str(spec['questions'][0]['id']))}="
        f"{e(str(spec['questions'][0]['options'][0]['id']))}</code>.</p></noscript>",
        "</main>",
        '<div class="bar" role="region" aria-label="Your answer"><div>',
        '<output for="board"><label class="note" for="answer">Paste this line back into the chat</label>'
        '<input id="answer" readonly></output>',
        '<button type="button" id="copy" disabled>Copy answer</button>',
        '<p id="status" role="status" aria-live="polite"></p>',
        "</div></div>",
        f"<script>{SCRIPT}</script>",
        "</body>",
        "</html>",
    ]
    return "\n".join(out) + "\n"


ITEM = re.compile(r'\s*([a-z0-9][a-z0-9-]*)\s*=\s*("(?:[^"\\]|\\.)*"|[^;]*)\s*(?:;|$)')


def read_answer(spec, text):
    """Parse a pasted answer line. Returns (result, problems)."""
    problems = []
    text = text.strip()
    m = re.match(r"pick\s+([a-z0-9-]+)\s*:\s*", text)
    board = None
    if m:
        board = m.group(1)
        text = text[m.end():]
        want = slug(spec.get("board") or spec.get("title") or "Pick one")
        if board != want:
            problems.append(f"line is for board '{board}', this spec builds '{want}'")
    questions = {str(q.get("id")): q for q in spec["questions"]}
    picks, labels, note = {}, {}, ""
    pos = 0
    while pos < len(text):
        m = ITEM.match(text, pos)
        if not m or m.end() == pos:
            problems.append(f"cannot read from: {text[pos:pos + 40]!r}")
            break
        pos = m.end()
        key, value = m.group(1), m.group(2).strip()
        if key == "note":
            if value.startswith('"'):
                value = re.sub(r"\\(.)", r"\1", value[1:-1])
            note = value
            continue
        q = questions.get(key)
        if q is None:
            problems.append(f"no question '{key}'")
            continue
        ids = [v.strip() for v in value.split(",") if v.strip()]
        known = {str(o.get("id")): str(o.get("label")) for o in q["options"]}
        bad = [v for v in ids if v not in known]
        if bad:
            problems.append(f"{key}: no option {', '.join(bad)}")
        ids = [v for v in ids if v in known]
        if q.get("pick", "one") == "one" and len(ids) > 1:
            problems.append(f"{key}: pick one, got {len(ids)}")
        if key in picks:
            problems.append(f"{key}: answered twice")
        picks[key] = ids
        labels[key] = [known[v] for v in ids]
    missing = [k for k in questions if not picks.get(k)]
    return {"board": board, "picks": picks, "labels": labels, "note": note, "missing": missing}, problems


def demo_spec():
    def tile(fill, rows):
        bars = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}"/>' for x, y, w, h in rows)
        return f'<svg viewBox="0 0 200 120" width="200" height="120" role="presentation">{bars}</svg>'
    return {
        "title": "Homepage direction",
        "intro": "Two quick picks before I build the page.",
        "questions": [
            {"id": "layout", "prompt": "Which layout reads best?", "options": [
                {"id": "a", "label": "Single column", "note": "One path down the page.",
                 "show": tile("#8a8478", [(40, 12, 120, 14), (40, 34, 120, 30), (40, 72, 120, 10), (40, 88, 120, 10)])},
                {"id": "b", "label": "Split hero", "note": "Words left, product right.",
                 "show": tile("#8a8478", [(12, 16, 80, 12), (12, 36, 70, 8), (12, 52, 50, 14), (108, 12, 80, 90)])},
            ]},
            {"id": "accents", "prompt": "Which accents could work?", "pick": "many", "options": [
                {"id": "moss", "label": "Moss", "show": tile("#2f5d50", [(0, 0, 200, 120)])},
                {"id": "rust", "label": "Rust", "show": tile("#9c4a2c", [(0, 0, 200, 120)])},
                {"id": "ink", "label": "Ink", "show": tile("#24324f", [(0, 0, 200, 120)])},
            ]},
        ],
    }


def self_check():
    problems = []
    spec = demo_spec()
    if check(spec, Path(".")):
        problems.append(f"demo spec should be clean: {check(spec, Path('.'))}")
    page = render(spec, Path("."))
    for needle in ('type="radio" name="layout" value="b"', 'type="checkbox" name="accents"', "Content-Security-Policy",
                   'data-board="homepage-direction"', "<legend>Which layout reads best?</legend>"):
        if needle not in page:
            problems.append(f"page lacks {needle!r}")
    if re.search(r"https?://(?!www\.w3\.org)", page):
        problems.append("page names a remote URL")
    res, probs = read_answer(spec, 'pick homepage-direction: layout=b; accents=moss,ink; note="warmer \\"please\\""')
    if probs or res["picks"] != {"layout": ["b"], "accents": ["moss", "ink"]} or res["note"] != 'warmer "please"':
        problems.append(f"answer parse: {res} {probs}")
    _, probs = read_answer(spec, "pick homepage-direction: layout=a,b; colour=x")
    if len(probs) != 2:
        problems.append(f"bad answer should give 2 problems: {probs}")
    bad = json.loads(json.dumps(spec))
    bad["questions"][0]["options"][0]["show"] = '<img src="https://example.com/x.png">'
    bad["questions"][0]["options"][1]["show"] = "<svg onload=\"x()\"></svg>"
    bad["questions"][1]["options"] = [{"id": c, "label": c, "show": "<b>x</b>"} for c in "abcde"]
    bad["questions"][1].pop("pick")
    bad["questions"].append({"id": "words", "prompt": "Tone?", "options": [{"id": "a", "label": "Calm"}]})
    rules = sorted({r for r, _, _ in check(bad, Path("."))})
    if rules != ["offline", "too-many", "visual"]:
        problems.append(f"bad spec rules: {rules}")
    print(f"choice_board self-check: {len(problems)} problem(s)")
    for p in problems:
        print("  " + p)
    return 1 if problems else 0


def report(findings, as_json):
    if as_json:
        print(json.dumps([{"rule": r, "level": RULES[r][0], "where": w, "message": m} for r, w, m in findings], indent=2))
    else:
        for r, w, m in findings:
            print(f"{RULES[r][0]} {r}: {w}: {m}")
        print(f"{len(findings)} finding(s)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Offline choice boards for visual questions.")
    ap.add_argument("--self-check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("check")
    c.add_argument("spec")
    c.add_argument("--json", action="store_true")
    b = sub.add_parser("build")
    b.add_argument("spec")
    b.add_argument("--out", required=True)
    b.add_argument("--theme", choices=("auto", "light", "dark"), default="auto")
    r = sub.add_parser("read")
    r.add_argument("spec")
    r.add_argument("answer")
    sub.add_parser("rules")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    if args.self_check:
        return self_check()
    if args.cmd == "rules":
        for name, (level, text) in RULES.items():
            print(f"{name}: {level}: {text}")
        return 0
    if not args.cmd:
        ap.print_usage(sys.stderr)
        return 2
    try:
        spec = load(args.spec)
    except SpecError as exc:
        print(f"bad spec: {exc}", file=sys.stderr)
        return 2
    base = Path(args.spec).resolve().parent
    if args.cmd == "read":
        result, problems = read_answer(spec, args.answer)
        result["problems"] = problems
        print(json.dumps(result, indent=2))
        return 1 if problems else 0
    findings = check(spec, base)
    if args.cmd == "check":
        report(findings, args.json)
        return 1 if findings else 0
    errors = [f for f in findings if RULES[f[0]][0] == "error"]
    if errors:
        report(errors, False)
        print("not built: fix the errors first", file=sys.stderr)
        return 1
    Path(args.out).write_text(render(spec, base, args.theme), encoding="utf-8")
    for r_, w, m in findings:
        print(f"warn {r_}: {w}: {m}")
    print(f"wrote {args.out}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
