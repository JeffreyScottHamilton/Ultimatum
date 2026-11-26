"""Finished social media files: carousel slides rendered to PNG, and video with burned-in captions.

  ult posts slides SPEC.json [--out DIR] [--render]
      one HTML page per slide at the platform's exact size, plus render.cjs (Playwright) that saves each as PNG;
      --render runs it with the local node and checks the PNGs
  ult posts captions VIDEO (--srt FILE | --script FILE | --transcribe --model PATH) [--platform P] [--out FILE]
      captions kept above the platform's bottom safe zone, burned in with the local ffmpeg

Only local programs run (node, ffmpeg, whisper.cpp); nothing is uploaded.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
from pathlib import Path

from ultlib.postspecs import PLATFORMS, check_file

SLIDE_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden}}
body{{background:{bg};color:{fg};font-family:{font};display:flex;flex-direction:column;justify-content:center;
box-sizing:border-box;padding:{pt}px {pr}px {pb}px {pl}px}}
.n{{font-size:{small}px;color:{accent};font-weight:700;letter-spacing:.04em}}
h1{{font-size:{big}px;line-height:1.08;margin:.3em 0}} p{{font-size:{mid}px;line-height:1.35;margin:0;opacity:.88}}
img{{max-width:100%;max-height:{imgh}px;object-fit:contain;border-radius:16px;margin-bottom:32px}}
.brand{{position:absolute;left:{pl}px;bottom:{brandb}px;font-size:{small}px;opacity:.7}}
</style></head><body>{image}<div class="n">{num}</div><h1>{title}</h1><p>{body}</p><div class="brand">{brand}</div></body></html>
"""
RENDER_JS = """// Saves each slide-NN.html in this folder as slide-NN.png at its exact size. Run: node render.cjs
const {{ chromium }} = require("playwright");
const path = require("path");
const fs = require("fs");
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage({{ viewport: {{ width: {w}, height: {h} }}, deviceScaleFactor: 1 }});
  const files = fs.readdirSync(__dirname).filter((f) => /^slide-\\d+\\.html$/.test(f)).sort();
  for (const f of files) {{
    await page.goto("file://" + path.join(__dirname, f));
    await page.waitForLoadState("load");
    await page.screenshot({{ path: path.join(__dirname, f.replace(".html", ".png")) }});
    console.log("saved " + f.replace(".html", ".png"));
  }}
  await browser.close();
}})();
"""


def _size(spec: dict) -> tuple[int, int]:
    if spec.get("size"):
        w, _, h = str(spec["size"]).partition("x")
        return int(w), int(h)
    return PLATFORMS[spec.get("platform", "instagram-feed")]["sizes"][0]


def write_slides(spec: dict, out: Path) -> list[Path]:
    platform = spec.get("platform", "instagram-feed")
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform}; see `ult posts specs`")
    w, h = _size(spec)
    b = {"bg": "#ffffff", "fg": "#111111", "accent": "#d9480f", "font": "system-ui, sans-serif", "name": ""}
    b.update(spec.get("brand", {}))
    top, bottom, left, right = PLATFORMS[platform]["safe"]
    pad = round(w * 0.08)
    slides = spec.get("slides") or []
    if not slides:
        raise ValueError("the spec has no slides")
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for i, s in enumerate(slides, 1):
        img = s.get("image", "")
        tag = f'<img src="{html.escape(Path(img).resolve().as_uri() if img and not re.match(r"https?:", img) else img)}" alt="">' if img else ""
        page = SLIDE_HTML.format(
            w=w, h=h, bg=b["bg"], fg=b["fg"], accent=b["accent"], font=b["font"], pt=pad + top, pr=pad + right,
            pb=pad + bottom + round(h * 0.05), pl=pad + left, small=round(w * 0.028), mid=round(w * 0.042),
            big=round(w * (0.075 if len(s.get("title", "")) < 40 else 0.06)), imgh=round(h * 0.4),
            brandb=pad // 2 + bottom, image=tag, num=f"{i}/{len(slides)}", title=html.escape(s.get("title", "")),
            body=html.escape(s.get("body", "")), brand=html.escape(b.get("name", "")))
        p = out / f"slide-{i:02d}.html"
        p.write_text(page, encoding="utf-8")
        written.append(p)
    (out / "render.cjs").write_text(RENDER_JS.format(w=w, h=h), encoding="utf-8")
    alt = [f"slide {i}: {s.get('alt') or (s.get('title', '') + '. ' + s.get('body', '')).strip()}" for i, s in enumerate(slides, 1)]
    (out / "alt-text.txt").write_text("\n".join(alt) + "\n", encoding="utf-8")
    return written


def cmd_slides(args) -> int:
    try:
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        pages = write_slides(spec, Path(args.out))
    except (OSError, ValueError) as e:
        print(f"slides: {e}")
        return 2
    out = Path(args.out)
    print(f"wrote {len(pages)} slides, render.cjs and alt-text.txt to {out}")
    if not args.render:
        print(f"render: node {out / 'render.cjs'}  (or add --render), then look at every PNG")
        return 0
    if not shutil.which("node"):
        print("node is not installed: the HTML slides are ready but no PNG was made")
        return 1
    r = subprocess.run(["node", str(out / "render.cjs")], capture_output=True, text=True, timeout=300)
    if r.returncode:
        print("render failed (is Playwright installed?):\n" + (r.stderr or r.stdout)[-800:])
        return 1
    spec_p = PLATFORMS[spec.get("platform", "instagram-feed")]
    if spec.get("size"):
        spec_p = {**spec_p, "sizes": [_size(spec)]}
    problems = [m for p in pages for k, m in check_file(p.with_suffix(".png"), spec_p) if k == "blocker"]
    print(f"rendered {len(pages)} PNGs; {len(problems)} size problems")
    for m in problems:
        print(f"  blocker: {m}")
    print("look at every PNG before showing it; text near the edges is the usual fault")
    return 1 if problems else 0


def _ts(t: float, sep: str = ",") -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{sep}{ms % 1000:03d}"


def script_to_cues(lines: list[str], duration: float) -> list[tuple[float, float, str]]:
    """Spread script lines over the video by word count. Timings are a first guess to check by watching."""
    lines = [x.strip() for x in lines if x.strip()]
    words = [max(len(x.split()), 1) for x in lines]
    total, t, cues = sum(words) or 1, 0.0, []
    for line, n in zip(lines, words):
        d = duration * n / total
        cues.append((t, t + d, line))
        t += d
    return cues


def parse_srt(text: str) -> list[tuple[float, float, str]]:
    cues = []
    for block in re.split(r"\n\s*\n", text.replace("\r", "").strip()):
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", block)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        body = block[m.end():].strip()
        if body:
            cues.append((start, end, " ".join(body.splitlines())))
    return cues


def to_srt(cues) -> str:
    return "\n".join(f"{i}\n{_ts(a)} --> {_ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1))


def to_ass(cues, w: int, h: int, bottom_safe: int) -> str:
    size = round(min(w, h) * 0.06)
    margin = bottom_safe + round(h * 0.06)
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: {w}\nPlayResY: {h}\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, "
            "Shadow, Alignment, MarginL, MarginR, MarginV\n"
            "Style: Default,DejaVu Sans,{size},&H00FFFFFF,&H00000000,&H80000000,1,1,{ol},0,2,{ml},{ml},{mv}\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Text\n").format(w=w, h=h, size=size, ol=max(2, size // 12),
                                                                         ml=round(w * 0.08), mv=margin)
    ev = [f"Dialogue: 0,{_ts(a, '.')[1:-1]},{_ts(b, '.')[1:-1]},Default,{t.replace(chr(10), ' ')}" for a, b, t in cues]
    return head + "\n".join(ev) + "\n"


def _transcribe(video: Path, model: str, work: Path) -> str | None:
    exe = shutil.which("whisper-cli") or shutil.which("whisper-cpp") or shutil.which("main")
    if not exe or not model or not Path(model).is_file():
        return None
    wav = work / "audio.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(video), "-ar", "16000", "-ac", "1",
                    str(wav)], check=True, timeout=600)
    subprocess.run([exe, "-m", model, "-f", str(wav), "-osrt", "-of", str(work / "transcript")],
                   capture_output=True, check=True, timeout=1800)
    srt = work / "transcript.srt"
    return srt.read_text(encoding="utf-8") if srt.is_file() else None


def _cues_for(args, video: Path, duration: float, work: Path):
    if args.srt:
        return parse_srt(Path(args.srt).read_text(encoding="utf-8")), "the SRT file"
    if args.script:
        return script_to_cues(Path(args.script).read_text(encoding="utf-8").splitlines(), duration), \
            "the script, spread by word count (rough timing: watch it and fix the SRT)"
    text = _transcribe(video, args.model, work)
    if text is None:
        return None, ("no local transcriber: install whisper.cpp and pass --model <ggml model file>, "
                      "or give --script with the spoken lines, or --srt")
    return parse_srt(text), "whisper.cpp on this machine (read it for misheard words)"


def cmd_captions(args) -> int:
    from ultlib.media import probe  # noqa: PLC0415
    video = Path(args.video)
    if not video.is_file() or not shutil.which("ffmpeg"):
        print("captions need the video file and ffmpeg")
        return 2
    m = probe(video)
    out = Path(args.out or video.with_name(video.stem + "-captioned.mp4"))
    work = out.parent / (out.stem + "-captions")
    work.mkdir(parents=True, exist_ok=True)
    cues, source = _cues_for(args, video, m["duration"], work)
    if not cues:
        print(f"captions: {source}")
        return 2
    w, h = m["width"] or 1080, m["height"] or 1920
    bottom = PLATFORMS[args.platform]["safe"][1] if args.platform else 0
    (work / "captions.srt").write_text(to_srt(cues), encoding="utf-8")
    (work / "captions.ass").write_text(to_ass(cues, w, h, bottom), encoding="utf-8")
    r = subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(video.resolve()), "-vf", "ass=captions.ass",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "copy", str(out.resolve())],
                       cwd=str(work), capture_output=True, text=True, timeout=1800)
    if r.returncode:
        print("ffmpeg could not burn the captions:\n" + r.stderr[-800:])
        return 1
    print(f"wrote {out} with {len(cues)} captions from {source}; SRT kept at {work / 'captions.srt'} for platforms "
          "that take a caption file")
    print(f"check: `ult media {out}`, then watch it on a phone")
    return 0


def register(sub):
    c = sub.add_parser("slides", help="carousel slides at the platform's exact size, rendered to PNG")
    c.add_argument("spec")
    c.add_argument("--out", default="social/slides")
    c.add_argument("--render", action="store_true")
    c.set_defaults(func=cmd_slides)
    c = sub.add_parser("captions", help="burn captions into a video, above the platform's bottom safe zone")
    c.add_argument("video")
    g = c.add_mutually_exclusive_group(required=True)
    g.add_argument("--srt")
    g.add_argument("--script", help="text file, one caption line per line")
    g.add_argument("--transcribe", action="store_true", help="use a local whisper.cpp (needs --model)")
    c.add_argument("--model", help="local whisper.cpp ggml model file")
    c.add_argument("--platform", choices=sorted(PLATFORMS))
    c.add_argument("--out")
    c.set_defaults(func=cmd_captions)
