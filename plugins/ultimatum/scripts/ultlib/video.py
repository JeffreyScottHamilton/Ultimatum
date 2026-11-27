"""`ult video`: edit short social videos in a named style, then check the result has that style's feel.

  ult video styles [ID]                         the style recipes (built in, plus social/styles/*.json)
  ult video jumpcuts WORDS.json --src CLIP      cut the pauses out of a talking clip; prints an edit
  ult video check EDIT.json                     the edit against its style and platform, before rendering
  ult video render EDIT.json --out FILE         cut, caption, grade and mix with the local ffmpeg
  ult video sample EDIT.json --styles a,b       a few seconds in each style, for the user to pick from
  ult video measure FILE [--recipe-out F]       cuts, pace, loudness and colour of any video
  ult video feel FILE --edit EDIT.json          the finished file against the recipe; frames to look at

Standard library only. Needs ffmpeg and ffprobe on PATH for render, sample, measure and feel; nothing
is downloaded or installed. Media paths in an edit must stay inside the project (--root).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import statistics
import subprocess
import tempfile
from pathlib import Path

from ultlib.postspecs import ALIASES, PLATFORMS

STYLES_DIR = Path(__file__).resolve().parents[2] / "data" / "video" / "styles"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,40}$")
RECIPE_KEYS = ("id", "name", "feel", "duration", "hook_by", "shot", "captions", "look", "audio")
MAX_FRAMES = 24


class EditError(Exception):
    """An edit or recipe that cannot be used as written."""


# ---------- recipes ----------

def load_styles(root: Path) -> dict:
    out = {}
    for d in (STYLES_DIR, root / "social" / "styles"):
        for f in sorted(d.glob("*.json")) if d.is_dir() else []:
            try:
                r = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                raise EditError(f"{f.name}: not valid JSON ({e})") from e
            problems = recipe_problems(r)
            if problems:
                raise EditError(f"{f.name}: " + "; ".join(problems))
            out[r["id"]] = r
    return out


def recipe_problems(r) -> list[str]:
    if not isinstance(r, dict):
        return ["a recipe is a JSON object"]
    p = [f"missing {k}" for k in RECIPE_KEYS if k not in r]
    if p:
        return p
    if not ID.match(str(r["id"])):
        p.append("id: lowercase letters, digits and dashes")
    s = r["shot"]
    if not (0 < s.get("min", 0) <= s.get("max", 0)) or len(s.get("avg", [])) != 2:
        p.append("shot needs 0 < min <= max and avg [low, high]")
    c = r["captions"]
    if c.get("mode") not in ("word", "line", "none"):
        p.append("captions.mode is word, line or none")
    for k in ("color", "highlight"):
        if k in c and not HEX.match(str(c[k])):
            p.append(f"captions.{k} must be #RRGGBB")
    if not 0 < float(c.get("y", 0.5)) < 1 or not 0 < float(c.get("size", 0.05)) < 0.3:
        p.append("captions.y and captions.size are fractions of the frame height")
    return p


def cmd_styles(args) -> int:
    styles = load_styles(Path(args.root).resolve())
    if args.id:
        if args.id not in styles:
            print(f"no style {args.id!r}; have: {', '.join(sorted(styles))}")
            return 2
        print(json.dumps(styles[args.id], indent=2))
        return 0
    for s in styles.values():
        lo, hi = s["shot"]["avg"]
        print(f"{s['id']}: {s['name']}. {s['feel']}\n    shots {lo}-{hi} s on average, cut on {s.get('cut_on', '?')}, "
              f"{s['duration'][0]}-{s['duration'][1]} s, captions {s['captions']['mode']}, "
              f"best for {', '.join(s.get('best_for', []))}")
    return 0


# ---------- the edit ----------

def _inside(root: Path, base: Path, rel) -> Path:
    if not isinstance(rel, str) or not rel or "\x00" in rel:
        raise EditError(f"bad path {rel!r}")
    p = (base / rel).resolve()
    if p != root and root not in p.parents:
        raise EditError(f"{rel}: outside the project; keep media inside {root}")
    return p


def _platform(name) -> tuple[str, dict]:
    key = ALIASES.get(str(name), str(name))
    if key not in PLATFORMS:
        raise EditError(f"unknown platform {name!r}")
    return key, PLATFORMS[key]


def load_edit(path: Path, root: Path, style_override: str | None = None) -> dict:
    """Read and normalise an edit: absolute media paths, timeline, recipe and caption words."""
    try:
        e = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise EditError(f"{path.name}: cannot read ({exc})") from exc
    if not isinstance(e, dict) or not isinstance(e.get("shots"), list) or not e["shots"]:
        raise EditError("an edit is an object with a non-empty shots list")
    styles = load_styles(root)
    sid = style_override or e.get("style")
    if sid not in styles:
        raise EditError(f"unknown style {sid!r}; have: {', '.join(sorted(styles))}")
    base = path.parent.resolve()
    pkey, pspec = _platform(e.get("platform", "tiktok"))
    w, h = e.get("size") or pspec["sizes"][0]
    shots, t = [], 0.0
    for i, s in enumerate(e["shots"]):
        if not isinstance(s, dict):
            raise EditError(f"shot {i + 1}: must be an object")
        s = dict(s)
        if "src" in s:
            s["path"] = _inside(root, base, s["src"])
            a, b = float(s.get("in", 0)), float(s.get("out", 0))
            if b <= a:
                raise EditError(f"shot {i + 1}: out must be after in")
            s["dur"] = b - a
        elif "card" in s:
            s["dur"] = float(s.get("dur", 0))
            if s["dur"] <= 0:
                raise EditError(f"shot {i + 1}: a card needs dur > 0")
            if not HEX.match(str(s.get("bg", "#111111"))):
                raise EditError(f"shot {i + 1}: bg must be #RRGGBB")
        else:
            raise EditError(f"shot {i + 1}: needs src (a clip) or card (text on colour)")
        s["start"], t = t, t + s["dur"]
        shots.append(s)
    out = {"style": styles[sid], "platform": pkey, "spec": pspec, "size": (int(w), int(h)),
           "fps": int(e.get("fps", 30)), "shots": shots, "duration": t, "base": base, "root": root, "raw": e}
    for k in ("music",):
        if e.get(k):
            out[k] = dict(e[k], path=_inside(root, base, e[k].get("src")))
    out["sfx"] = [dict(x, path=_inside(root, base, x.get("src"))) for x in e.get("sfx", [])]
    if e.get("lut"):
        out["lut"] = _inside(root, base, e["lut"])
    out["words"] = _caption_words(e.get("captions") or {}, shots, root, base)
    out["lines"] = [dict(x) for x in (e.get("captions") or {}).get("lines", [])]
    return out


def read_words(path: Path) -> list[dict]:
    """Words with times from our own format or a Whisper-style JSON (segments[].words[])."""
    data = json.loads(path.read_text(encoding="utf-8"))
    raw = data.get("words") if isinstance(data, dict) else data
    if raw is None and isinstance(data, dict):
        raw = [w for seg in data.get("segments", []) for w in seg.get("words", [])]
    out = []
    for w in raw or []:
        text = str(w.get("w", w.get("word", w.get("text", "")))).strip()
        if text:
            out.append({"w": text, "start": float(w["start"]), "end": float(w["end"])})
    return out


def _caption_words(c: dict, shots: list, root: Path, base: Path) -> list[dict]:
    words = [dict(w) for w in c.get("words", [])]
    if c.get("whisper"):
        words = read_words(_inside(root, base, c["whisper"]))
    if not c.get("source"):
        return words
    # Times are in the source clip: keep the words that survive the cut and move them onto the timeline.
    src = _inside(root, base, c["source"])
    out = []
    for w in words:
        mid = (w["start"] + w["end"]) / 2
        for s in shots:
            if s.get("path") == src and float(s.get("in", 0)) <= mid < float(s["out"]):
                off = s["start"] - float(s.get("in", 0))
                out.append({"w": w["w"], "start": max(s["start"], w["start"] + off),
                            "end": min(s["start"] + s["dur"], w["end"] + off)})
                break
    return out


def check_edit(ed: dict) -> list[tuple[str, str]]:
    """Problems with an edit before rendering: ("blocker" | "fix", message)."""
    r, found = ed["style"], []
    T, spec = ed["duration"], ed["spec"]
    w, h = ed["size"]
    if (w, h) not in [tuple(x) for x in spec["sizes"]]:
        found.append(("blocker", f"size {w}x{h} is not one {ed['platform']} takes: "
                                 f"{', '.join(f'{a}x{b}' for a, b in spec['sizes'])}"))
    if T > spec["video_max"]:
        found.append(("blocker", f"{T:.1f} s is longer than {ed['platform']}'s {spec['video_max']} s"))
    lo, hi = r["duration"]
    if not lo <= T <= hi:
        found.append(("fix", f"{T:.1f} s; {r['id']} works best at {lo}-{hi} s"))
    for s in ed["shots"]:
        if "path" in s and not s["path"].is_file():
            found.append(("blocker", f"{s['src']}: file not found"))
    durs = [s["dur"] for s in ed["shots"]]
    sm = r["shot"]
    n = sum(1 for d in durs[:-1] if not sm["min"] <= d <= sm["max"])  # the last shot may hold longer
    if n:
        found.append(("fix", f"{n} shots outside {sm['min']}-{sm['max']} s, the {r['id']} range"))
    avg = statistics.mean(durs)
    if len(durs) > 1 and not sm["avg"][0] <= avg <= sm["avg"][1]:
        found.append(("fix", f"average shot {avg:.2f} s; {r['id']} feels right at {sm['avg'][0]}-{sm['avg'][1]} s"))
    first_text = min([x["start"] for x in ed["words"]] + [float(x["start"]) for x in ed["lines"]]
                     + [s["start"] for s in ed["shots"] if "card" in s] + [T])
    if first_text > r["hook_by"] and "hook" not in (ed["shots"][0].get("tags") or []):
        found.append(("fix", f"nothing to read or hear until {first_text:.1f} s; land the hook by {r['hook_by']} s "
                             "(or tag the first shot \"hook\" if the picture is the hook)"))
    cap = r["captions"]
    if cap["mode"] != "none" and not ed["words"] and not ed["lines"] and not any("card" in s for s in ed["shots"]):
        found.append(("fix", "no captions; most people watch with the sound off"))
    if cap["mode"] != "none":
        top, bottom, _left, right = spec["safe"]
        y, size = float(ed["raw"].get("caption_y", cap["y"])), float(cap["size"])
        if (y + size) * h > h - bottom or (y - size) * h < top:
            found.append(("fix", f"captions at {y:.2f} of the height sit under {ed['platform']}'s buttons; "
                                 f"keep them between {top}px and {h - bottom}px"))
    if ed["words"]:
        span = max(x["end"] for x in ed["words"]) - min(x["start"] for x in ed["words"])
        wps = len(ed["words"]) / max(T, span, 0.1)
        plo, phi = r.get("pace_wps", [0, 99])
        if not plo <= wps <= phi:
            found.append(("fix", f"{wps:.1f} words a second; {r['id']} wants {plo}-{phi}"))
    story = r.get("story")
    if story:
        prod = [s["start"] for s in ed["shots"] if "product" in (s.get("tags") or [])]
        if prod and min(prod) < story["product_after"] * T:
            found.append(("fix", f"the product shows at {min(prod):.1f} s; hold it until after "
                                 f"{story['product_after'] * T:.1f} s so it arrives at the turn"))
        if not any(s["dur"] >= story["hold_min"] and "hold" in (s.get("tags") or []) for s in ed["shots"]):
            found.append(("fix", f"no held moment; tag one quiet shot of {story['hold_min']} s or more \"hold\""))
    if ed.get("music") and not ed["music"].get("licence"):
        found.append(("fix", "music has no licence noted; record where the track came from and what it allows"))
    for s in ed["shots"]:
        if s.get("ai") and not ed["raw"].get("ai_label"):
            found.append(("fix", "generated footage is in the edit; set \"ai_label\": true and turn on the "
                                 "platform's AI label when posting"))
            break
    return found


def _print_found(title: str, found, as_json: bool, extra=None) -> int:
    blockers = sum(1 for k, _ in found if k == "blocker")
    if as_json:
        print(json.dumps(dict(extra or {}, problems=[{"kind": k, "text": m} for k, m in found]), indent=2))
    else:
        print(f"{title}: {blockers} blockers, {len(found) - blockers} fixes")
        for k, m in found:
            print(f"  {k}: {m}")
    return blockers


def cmd_check(args) -> int:
    try:
        ed = load_edit(Path(args.edit), Path(args.root).resolve(), args.style)
    except EditError as e:
        print(f"video check: {e}")
        return 2
    found = check_edit(ed)
    title = (f"video check ({ed['style']['id']}, {ed['platform']}, {ed['duration']:.1f} s, "
             f"{len(ed['shots'])} shots)")
    return 1 if _print_found(title, found, args.json, {"style": ed["style"]["id"], "duration": ed["duration"]}) else 0


# ---------- jump cuts ----------

def jumpcuts(words: list[dict], gap: float, pad: float) -> list[tuple[float, float]]:
    """Keep speech, drop pauses longer than gap; pad each kept stretch a little."""
    spans = []
    for w in words:
        if spans and w["start"] - spans[-1][1] <= gap:
            spans[-1][1] = w["end"]
        else:
            spans.append([w["start"], w["end"]])
    out = []
    for a, b in spans:
        a, b = max(0.0, a - pad), b + pad
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], b)
        else:
            out.append((a, b))
    return [(round(a, 3), round(b, 3)) for a, b in out]


def cmd_jumpcuts(args) -> int:
    words = read_words(Path(args.words))
    if not words:
        print("jumpcuts: no timed words in that file")
        return 2
    cuts = jumpcuts(words, args.gap, args.pad)
    src, wfile = args.src, args.words
    if args.out:  # paths in an edit are relative to the edit's folder
        here = Path(args.out).resolve().parent
        src, wfile = (os.path.relpath(Path(x).resolve(), here) for x in (args.src, args.words))
    edit = {"style": args.style, "platform": args.platform,
            "shots": [{"src": src, "in": a, "out": b} for a, b in cuts],
            "captions": {"whisper": wfile, "source": src}}
    kept = sum(b - a for a, b in cuts)
    text = json.dumps(edit, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"jumpcuts: {len(cuts)} shots, {kept:.1f} s kept of {words[-1]['end']:.1f} s; wrote {args.out}")
    else:
        print(text)
    return 0


# ---------- ffmpeg ----------

def _tools() -> tuple[str, str]:
    ff, fp = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ff or not fp:
        raise FileNotFoundError("ffmpeg and ffprobe are needed (apt install ffmpeg, or brew install ffmpeg)")
    return ff, fp


def _run(cmd: list[str], cwd: Path | None = None, timeout: int = 900) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        tail = "\n".join(r.stderr.strip().splitlines()[-6:])
        raise EditError(f"ffmpeg failed ({r.returncode}):\n{tail}")
    return r


def probe(path: Path) -> dict:
    _ff, fp = _tools()
    r = _run([fp, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)], timeout=60)
    d = json.loads(r.stdout or "{}")
    streams = d.get("streams") or []
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    num, _, den = str(v.get("avg_frame_rate", "0/1")).partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 0.0
    return {"duration": float((d.get("format") or {}).get("duration") or 0), "width": v.get("width"),
            "height": v.get("height"), "fps": round(fps, 3),
            "audio": any(s.get("codec_type") == "audio" for s in streams)}


def _ass_colour(hexstr: str) -> str:
    h = hexstr.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def _ass_text(s: str) -> str:
    # Captions are data: no override tags or line breaks may come from the edit.
    return s.replace("\\", "/").replace("{", "(").replace("}", ")").replace("\n", " ")


def _ts(t: float) -> str:
    t = max(0.0, t)
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def build_ass(ed: dict, limit: float | None = None) -> str:
    """Subtitles for the captions and cards, styled from the recipe."""
    cap, (w, h) = ed["style"]["captions"], ed["size"]
    y = float(ed["raw"].get("caption_y", cap["y"]))
    size = int(cap["size"] * h)
    up = (lambda s: s.upper()) if cap.get("upper") else (lambda s: s)
    col, hi = _ass_colour(cap.get("color", "#FFFFFF")), _ass_colour(cap.get("highlight", "#FFFFFF"))
    font = re.sub(r"[^A-Za-z0-9 \-]", "", str(cap.get("font", "Inter"))) or "Inter"
    head = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {w}", f"PlayResY: {h}", "WrapStyle: 0", "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
            "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
            "Alignment, MarginL, MarginR, MarginV, Encoding",
            f"Style: Cap,{font},{size},{col},{col},&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,"
            f"{cap.get('outline', 4)},0,5,60,60,0,1",
            f"Style: Card,{font},{int(max(cap['size'], 0.09) * h)},{col},{col},&H00000000,&H00000000,-1,0,0,0,"
            f"100,100,0,0,1,0,0,5,80,80,0,1", "", "[Events]",
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    pos = f"\\an5\\pos({w // 2},{int(y * h)})"
    pop = "\\fscx82\\fscy82\\t(0,90,\\fscx100\\fscy100)" if cap.get("pop") else ""
    ev = []
    end_all = ed["duration"] if limit is None else min(limit, ed["duration"])

    def add(a, b, style, text):
        if a < end_all and b > a:
            ev.append(f"Dialogue: 0,{_ts(a)},{_ts(min(b, end_all))},{style},,0,0,0,,{text}")

    for s in ed["shots"]:
        if "card" in s:
            add(s["start"], s["start"] + s["dur"], "Card", "{\\an5\\pos(%d,%d)%s}%s" % (
                w // 2, int(0.45 * h), pop, _ass_text(up(str(s["card"])))))
    if cap["mode"] != "none":
        for ln in ed["lines"]:
            add(float(ln["start"]), float(ln["end"]), "Cap", "{%s}%s" % (pos, _ass_text(up(str(ln["text"])))))
        words, n = ed["words"], max(1, int(cap.get("words_per_card", 3)))
        cards = [words[i:i + n] for i in range(0, len(words), n)]
        for ci, card in enumerate(cards):
            nxt = cards[ci + 1][0]["start"] if ci + 1 < len(cards) else card[-1]["end"] + 0.4
            card_end = min(nxt, card[-1]["end"] + 0.6)
            for wi, wd in enumerate(card):
                a = wd["start"] if wi else card[0]["start"]
                b = card[wi + 1]["start"] if wi + 1 < len(card) else card_end
                parts = [("{\\c%s}%s{\\c%s}" % (hi, _ass_text(up(x["w"])), col)) if j == wi and cap["mode"] == "word"
                         else _ass_text(up(x["w"])) for j, x in enumerate(card)]
                add(a, b, "Cap", "{%s%s}%s" % (pos, pop if wi == 0 else "", " ".join(parts)))
    return "\n".join(head + ev) + "\n"


def _look_filters(ed: dict, lut_name: str | None) -> list[str]:
    lk = ed["style"]["look"]
    f = [f"eq=contrast={lk.get('contrast', 1)}:saturation={lk.get('saturation', 1)}:"
         f"brightness={lk.get('brightness', 0)}:gamma={lk.get('gamma', 1)}"]
    if lk.get("warmth"):
        wv = float(lk["warmth"])
        f.append(f"colorbalance=rm={wv}:bm={-wv}:rh={wv / 2}:bh={-wv / 2}")
    if lut_name:
        f.append(f"lut3d=file={lut_name}")
    if lk.get("vignette"):
        f.append("vignette=angle=PI/6")
    if lk.get("grain"):
        f.append(f"noise=alls={int(lk['grain'])}:allf=t")
    return f


def _zoom_for(ed: dict, i: int, s: dict) -> float:
    if "zoom" in s:
        return float(s["zoom"])
    z = ed["style"].get("zoom") or {}
    every = int(z.get("every", 0))
    return float(z.get("scale", 1)) if every and i % every == every - 1 else 1.0


def render(ed: dict, out: Path, limit: float | None = None, keep_dir: Path | None = None) -> dict:
    ff, _fp = _tools()
    (w, h), fps = ed["size"], ed["fps"]
    T = ed["duration"] if limit is None else min(limit, ed["duration"])
    tmp = Path(tempfile.mkdtemp(prefix="ultvideo-", dir=keep_dir))
    try:
        segs = []
        for i, s in enumerate(ed["shots"]):
            if s["start"] >= T:
                break
            dur = min(s["dur"], T - s["start"])
            name = f"seg{i:03d}.mkv"
            vf = []
            if "path" in s:
                has_audio = probe(s["path"])["audio"] and not s.get("mute")
                ins = ["-ss", f"{float(s.get('in', 0)):.3f}", "-t", f"{dur:.3f}", "-i", str(s["path"])]
                z = _zoom_for(ed, i, s)
                vf = [f"scale={w}:{h}:force_original_aspect_ratio=increase", f"crop={w}:{h}"]
                if z > 1.0:
                    vf += [f"scale={int(w * z) // 2 * 2}:{int(h * z) // 2 * 2}", f"crop={w}:{h}"]
            else:
                has_audio = False
                ins = ["-f", "lavfi", "-i", f"color=c=0x{s.get('bg', '#111111').lstrip('#')}:s={w}x{h}:r={fps}:d={dur:.3f}"]
            ins += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
            vf += ["setsar=1", f"fps={fps}", "format=yuv420p"]
            af = ["aresample=48000", "aformat=channel_layouts=stereo", "apad", f"atrim=0:{dur:.3f}"]
            if s.get("fade_in"):
                vf.append(f"fade=t=in:st=0:d={float(s['fade_in'])}")
                af.append(f"afade=t=in:st=0:d={float(s['fade_in'])}")
            if s.get("fade_out"):
                st = max(0.0, dur - float(s["fade_out"]))
                vf.append(f"fade=t=out:st={st:.3f}:d={float(s['fade_out'])}")
                af.append(f"afade=t=out:st={st:.3f}:d={float(s['fade_out'])}")
            fc = f"[0:v]{','.join(vf)}[v];[{0 if has_audio else 1}:a]{','.join(af)}[a]"
            _run([ff, "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                  "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                  "-c:a", "pcm_s16le", name], cwd=tmp)
            segs.append(name)
        (tmp / "list.txt").write_text("".join(f"file '{n}'\n" for n in segs), encoding="utf-8")
        (tmp / "captions.ass").write_text(build_ass(ed, T), encoding="utf-8")
        lut_name = None
        if ed.get("lut"):
            lut_name = "look.cube"
            shutil.copyfile(ed["lut"], tmp / lut_name)
        ins = ["-f", "concat", "-safe", "0", "-i", "list.txt"]
        vchain = _look_filters(ed, lut_name) + ["ass=captions.ass"]
        fc = [f"[0:v]{','.join(vchain)}[v]"]
        mix, k = ["[voice]"], 1
        audio = ed["style"]["audio"]
        music = ed.get("music")
        fc.append("[0:a]asplit=2[voice][key]" if music and audio.get("music") == "under" else "[0:a]anull[voice]")
        if music:
            ins += ["-stream_loop", "-1", "-ss", f"{float(music.get('start', 0)):.3f}", "-i", str(music["path"])]
            gain = float(music.get("gain_db", audio.get("music_db", -14)))
            fade = max(0.0, T - 1.0)
            fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T:.3f},volume={gain}dB,"
                      f"afade=t=out:st={fade:.3f}:d=1[m0]")
            if audio.get("music") == "under":
                fc.append("[m0][key]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=350[m]")
            else:
                fc.append("[m0]anull[m]")
            mix.append("[m]")
            k += 1
        for x in ed["sfx"]:
            at = float(x.get("at", 0))
            if at >= T:
                continue
            ms = int(at * 1000)
            ins += ["-i", str(x["path"])]
            fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={float(x.get('gain_db', -6))}dB,"
                      f"adelay={ms}:all=1[s{k}]")
            mix.append(f"[s{k}]")
            k += 1
        lufs, peak = float(audio.get("lufs", -14)), float(audio.get("peak", -1))
        fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0,"
                  f"loudnorm=I={lufs}:TP={peak - 0.5}:LRA=11,aresample=48000,atrim=0:{T:.3f}[a]")
        target = out.resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        _run([ff, "-y", "-v", "error", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
              "-t", f"{T:.3f}", "-r", str(fps), "-c:v", "libx264", "-preset", "medium", "-crf", "19",
              "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", str(target)], cwd=tmp)
        return {"out": str(target), "duration": T, "shots": len(segs)}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _out_path(root: Path, rel: str) -> Path:
    p = (Path.cwd() / rel).resolve()
    if p != root and root not in p.parents:
        raise EditError(f"{rel}: write inside the project ({root})")
    return p


def cmd_render(args) -> int:
    root = Path(args.root).resolve()
    try:
        ed = load_edit(Path(args.edit), root, args.style)
        found = check_edit(ed)
        if any(k == "blocker" for k, _ in found):
            _print_found("video render: fix these first", found, False)
            return 1
        res = render(ed, _out_path(root, args.out), args.sample)
    except (EditError, FileNotFoundError) as e:
        print(f"video render: {e}")
        return 2
    print(f"video render ({ed['style']['id']}): {res['out']}, {res['duration']:.1f} s, {res['shots']} shots. "
          f"Next: ult video feel {args.out} --edit {args.edit}")
    for k, m in found:
        print(f"  {k}: {m}")
    return 0


def cmd_sample(args) -> int:
    root = Path(args.root).resolve()
    try:
        outdir = _out_path(root, args.out_dir)
        made = []
        for sid in [x.strip() for x in args.styles.split(",") if x.strip()]:
            ed = load_edit(Path(args.edit), root, sid)
            res = render(ed, outdir / f"{sid}.mp4", args.seconds)
            still = outdir / f"{sid}.png"
            _frame(Path(res["out"]), min(res["duration"] / 2, 1.5), still)
            made.append((sid, res["out"], str(still)))
    except (EditError, FileNotFoundError) as e:
        print(f"video sample: {e}")
        return 2
    print(f"video sample: {len(made)} styles, {args.seconds:g} s each. Show these and let the user pick:")
    for sid, vid, still in made:
        print(f"  {sid}: {vid} (still {still})")
    return 0


# ---------- measuring ----------

def _frame(video: Path, t: float, out: Path) -> None:
    ff, _ = _tools()
    _run([ff, "-y", "-v", "error", "-ss", f"{max(0.0, t):.3f}", "-i", str(video), "-frames:v", "1",
          "-vf", "scale=540:-2", str(out)], timeout=60)


def measure(path: Path, threshold: float = 0.3) -> dict:
    ff, _ = _tools()
    info = probe(path)
    r = _run([ff, "-hide_banner", "-nostats", "-i", str(path), "-filter:v",
              f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"])
    cuts = [round(float(x), 3) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    T = info["duration"] or 0.0
    bounds = [0.0] + cuts + [T]
    shots = [b - a for a, b in zip(bounds, bounds[1:]) if b - a > 0.04]
    m = {"file": path.name, "duration": round(T, 3), "width": info["width"], "height": info["height"],
         "fps": info["fps"], "cuts": cuts, "shots": len(shots),
         "avg_shot": round(statistics.mean(shots), 3) if shots else None,
         "median_shot": round(statistics.median(shots), 3) if shots else None,
         "min_shot": round(min(shots), 3) if shots else None, "max_shot": round(max(shots), 3) if shots else None,
         "cuts_per_second": round(len(cuts) / T, 3) if T else None, "first_cut": cuts[0] if cuts else None}
    r = _run([ff, "-hide_banner", "-nostats", "-i", str(path), "-vf", "fps=2,scale=160:-2,signalstats,"
              "metadata=print:key=lavfi.signalstats.YAVG,metadata=print:key=lavfi.signalstats.SATAVG",
              "-an", "-f", "null", "-"])
    y = [float(x) for x in re.findall(r"YAVG=([0-9.]+)", r.stderr)]
    s = [float(x) for x in re.findall(r"SATAVG=([0-9.]+)", r.stderr)]
    m["brightness"] = round(statistics.mean(y) / 255, 3) if y else None
    m["saturation"] = round(statistics.mean(s) / 128, 3) if s else None
    if info["audio"]:
        r = _run([ff, "-hide_banner", "-nostats", "-i", str(path), "-vn", "-af", "ebur128=peak=true",
                  "-f", "null", "-"])
        summary = r.stderr[r.stderr.rfind("Summary:"):]
        i = re.search(r"I:\s+(-?[0-9.]+) LUFS", summary)
        p = re.search(r"True peak:\s+Peak:\s+(-?[0-9.]+|-inf) dBFS", summary)
        m["lufs"] = float(i.group(1)) if i else None
        m["true_peak"] = float(p.group(1)) if p and p.group(1) != "-inf" else None
    else:
        m["lufs"] = m["true_peak"] = None
    return m


def recipe_from(m: dict, base: dict, new_id: str) -> dict:
    """A draft recipe from measurements of a reference video, starting from the closest built-in style."""
    r = json.loads(json.dumps(base))
    avg = m.get("avg_shot") or base["shot"]["avg"][0]
    r.update({"id": new_id, "name": f"Measured from {m['file']}",
              "feel": f"Measured: about {avg:.1f} s a shot, {m.get('cuts_per_second') or 0:.2f} cuts a second. "
                      "Describe the feel in your own words after looking at the frames.",
              "duration": [max(1, int(m["duration"] * 0.7)), max(2, int(m["duration"] * 1.3) + 1)],
              "shot": {"min": round(max(0.2, (m.get("min_shot") or avg) * 0.8), 2),
                       "max": round((m.get("max_shot") or avg) * 1.2, 2),
                       "avg": [round(avg * 0.8, 2), round(avg * 1.2, 2)]},
              "reference": {k: m.get(k) for k in ("file", "brightness", "saturation", "avg_shot", "cuts_per_second")}})
    r.pop("story", None)
    return r


def cmd_measure(args) -> int:
    root = Path(args.root).resolve()
    try:
        m = measure(Path(args.file), args.threshold)
        if args.recipe_out:
            styles = load_styles(root)
            if args.base not in styles or not ID.match(args.id or ""):
                print("video measure: --base must be a style id and --id lowercase letters, digits and dashes")
                return 2
            r = recipe_from(m, styles[args.base], args.id)
            out = _out_path(root, args.recipe_out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(r, indent=2) + "\n", encoding="utf-8")
    except (EditError, FileNotFoundError, subprocess.SubprocessError) as e:
        print(f"video measure: {e}")
        return 2
    if args.json:
        print(json.dumps(m, indent=2))
    else:
        print(f"video measure {m['file']}: {m['duration']:.1f} s, {m['width']}x{m['height']} at {m['fps']:g} fps, "
              f"{m['shots']} shots (avg {m['avg_shot']} s, shortest {m['min_shot']} s, longest {m['max_shot']} s), "
              f"first cut {m['first_cut']} s, loudness {m['lufs']} LUFS, peak {m['true_peak']} dBTP, "
              f"brightness {m['brightness']}, saturation {m['saturation']}")
        print("  cuts are found by picture change, so jump cuts within one shot can be missed")
    if args.recipe_out:
        print(f"  draft recipe: {args.recipe_out} (based on {args.base}; set captions and feel by eye, "
              "in your own words)")
    return 0


def feel(ed: dict, m: dict) -> list[tuple[str, str]]:
    r, found = ed["style"], []
    w, h = ed["size"]
    if (m["width"], m["height"]) != (w, h):
        found.append(("blocker", f"file is {m['width']}x{m['height']}, the edit is {w}x{h}"))
    if abs(m["duration"] - ed["duration"]) > 0.35:
        found.append(("fix", f"file is {m['duration']:.2f} s, the edit is {ed['duration']:.2f} s"))
    a = r["audio"]
    if m["lufs"] is None:
        found.append(("fix", "no audio track"))
    else:
        if abs(m["lufs"] - a["lufs"]) > 1.0:
            found.append(("fix", f"loudness {m['lufs']} LUFS; aim for {a['lufs']} (within 1)"))
        if m["true_peak"] is not None and m["true_peak"] > a["peak"] + 0.2:
            found.append(("fix", f"peak {m['true_peak']} dBTP; keep it at or under {a['peak']}"))
    ref = r.get("reference") or {}
    for k, tol in (("brightness", 0.08), ("saturation", 0.15)):
        if ref.get(k) is not None and m.get(k) is not None and abs(m[k] - ref[k]) > tol:
            found.append(("fix", f"{k} {m[k]} against the reference's {ref[k]}"))
    sm = r["shot"]
    if m.get("avg_shot") and m["shots"] > 1 and m["avg_shot"] > sm["avg"][1] * 1.6 and len(ed["shots"]) > m["shots"]:
        found.append(("fix", f"only {m['shots']} picture changes found for {len(ed['shots'])} shots; "
                             "neighbouring shots may look the same, so the cuts may not read"))
    return found + [x for x in check_edit(ed) if x[0] == "fix"]


def cmd_feel(args) -> int:
    root = Path(args.root).resolve()
    try:
        ed = load_edit(Path(args.edit), root, args.style)
        video = Path(args.file)
        m = measure(video, args.threshold)
        found = feel(ed, m)
        frames = []
        if args.frames:
            d = _out_path(root, args.frames)
            d.mkdir(parents=True, exist_ok=True)
            times = [0.2] + [s["start"] + s["dur"] / 2 for s in ed["shots"]]
            for i, t in enumerate(times[:MAX_FRAMES]):
                f = d / f"frame{i:02d}.png"
                _frame(video, min(t, max(0.0, m["duration"] - 0.05)), f)
                frames.append(str(f))
    except (EditError, FileNotFoundError, subprocess.SubprocessError) as e:
        print(f"video feel: {e}")
        return 2
    problems = len(found)
    if args.json:
        print(json.dumps({"style": ed["style"]["id"], "measured": m, "frames": frames,
                          "problems": [{"kind": k, "text": t} for k, t in found]}, indent=2))
    else:
        print(f"video feel ({ed['style']['id']}): {problems} problems; measured {m['duration']:.1f} s, "
              f"{m['lufs']} LUFS, peak {m['true_peak']} dBTP, avg picture change {m['avg_shot']} s")
        for k, t in found:
            print(f"  {k}: {t}")
        if frames:
            print(f"  look at {len(frames)} frames in {args.frames}: hook frame first, then one per shot. "
                  "Check captions are readable and clear of the buttons, the look matches the recipe, faces are not cut")
    return 1 if problems else 0


def register(sub):
    p = sub.add_parser("video", help="edit short videos in a named style and check the feel (needs ffmpeg)")
    p.add_argument("--root", default=".", help="project folder; media must stay inside it")
    s = p.add_subparsers(dest="video_cmd", required=True)
    c = s.add_parser("styles", help="list style recipes, or print one")
    c.add_argument("id", nargs="?")
    c.set_defaults(func=cmd_styles)
    c = s.add_parser("jumpcuts", help="cut pauses out of a talking clip from its timed words")
    c.add_argument("words")
    c.add_argument("--src", required=True)
    c.add_argument("--gap", type=float, default=0.35)
    c.add_argument("--pad", type=float, default=0.08)
    c.add_argument("--style", default="talking-head")
    c.add_argument("--platform", default="tiktok")
    c.add_argument("--out")
    c.set_defaults(func=cmd_jumpcuts)
    for name, fn, hlp in (("check", cmd_check, "check an edit against its style before rendering"),
                          ("render", cmd_render, "render an edit with ffmpeg")):
        c = s.add_parser(name, help=hlp)
        c.add_argument("edit")
        c.add_argument("--style", help="use this style instead of the edit's")
        if name == "check":
            c.add_argument("--json", action="store_true")
        else:
            c.add_argument("--out", required=True)
            c.add_argument("--sample", type=float, help="render only the first N seconds")
        c.set_defaults(func=fn)
    c = s.add_parser("sample", help="render the start of the edit in several styles")
    c.add_argument("edit")
    c.add_argument("--styles", required=True)
    c.add_argument("--seconds", type=float, default=4.0)
    c.add_argument("--out-dir", default="social/samples")
    c.set_defaults(func=cmd_sample)
    c = s.add_parser("measure", help="cuts, pace, loudness and colour of a video")
    c.add_argument("file")
    c.add_argument("--threshold", type=float, default=0.3)
    c.add_argument("--recipe-out")
    c.add_argument("--base", default="talking-head")
    c.add_argument("--id")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_measure)
    c = s.add_parser("feel", help="check a finished video against its edit and style")
    c.add_argument("file")
    c.add_argument("--edit", required=True)
    c.add_argument("--style")
    c.add_argument("--frames", help="folder for frames to look at")
    c.add_argument("--threshold", type=float, default=0.3)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_feel)
