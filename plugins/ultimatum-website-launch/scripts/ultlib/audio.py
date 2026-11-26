"""`ult audio` — the sound credits log and a local voice-over-music mix.

  ult audio credits add FILE --source S --licence L [--author A] [--credit yes|no] [--used-in NAME]
      adds a row to brand/sound-credits.md (the table the compliance reviewer reads)
  ult audio credits check [--use paid-ad|organic] [--dir media/audio]
      flags non-commercial or unclear licences, credits owed, and audio files in --dir with no row; exit 1 on blockers
  ult audio mix VOICE MUSIC --out FILE [--music-db -16] [--duck 8] [--target -14] [--tp -1] [--video V] [--loop]
      music under the voice with sidechain ducking, two-pass loudnorm, then the measured loudness and true peak

Local ffmpeg only. Licence words are matched as text: a match is a prompt to read the licence, not a ruling.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

CREDITS = Path("brand/sound-credits.md")
HEADER = ["File", "Source URL", "Author", "Licence", "Credit needed", "Used in", "Added"]
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".opus"}
NON_COMMERCIAL = re.compile(r"\bnc\b|non-?commercial|personal use|personal licen|free plan|free tier|editorial", re.I)
COMMERCIAL_OK = re.compile(r"\bcc0\b|public domain|\bcc[- ]by\b(?!.*\bnc\b)|commercial|royalty[- ]free|paid plan|"
                           r"pro plan|business plan|own recording|our own|self-made|pixabay content licen|work for hire", re.I)
PAID_AD_RISK = re.compile(r"personal|creator plan|organic only|social only", re.I)


def read_rows(path: Path = CREDITS) -> list[dict]:
    if not path.is_file():
        return []
    rows, head = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            head = None if not line.strip() else head
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if head is None:
            head = [c.lower() for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append({h: (cells[i] if i < len(cells) else "") for i, h in enumerate(head)})
    return rows


def _cell(s: str) -> str:
    return (s or "").replace("|", "/").replace("\n", " ").strip()


def cmd_credits_add(args) -> int:
    path = CREDITS
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        path.write_text("# Sound credits\n\nOne row per voice, music track and sound effect used.\n\n"
                        "| " + " | ".join(HEADER) + " |\n|" + "---|" * len(HEADER) + "\n", encoding="utf-8")
    elif any(r.get("file") == args.file for r in read_rows(path)):
        print(f"{args.file} is already logged; edit its row in {path}")
        return 1
    credit = args.credit or ("yes" if re.search(r"\bby\b", args.licence, re.I) and "cc0" not in args.licence.lower() else "no")
    row = [args.file, args.source, args.author or "", args.licence, credit, args.used_in or "", date.today().isoformat()]
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + "| " + " | ".join(_cell(c) for c in row) + " |\n", encoding="utf-8")
    print(f"logged {args.file} ({args.licence}) in {path}")
    return 0


def judge(row: dict, use: str) -> list[tuple[str, str]]:
    name, lic = row.get("file", "?"), row.get("licence", "")
    out = []
    if not lic or lic.lower() in ("?", "unknown", "tbd"):
        out.append(("blocker", f"{name}: no licence recorded"))
    elif NON_COMMERCIAL.search(lic):
        out.append(("blocker", f"{name}: '{lic}' reads as non-commercial; business content needs another source or a paid plan"))
    elif not COMMERCIAL_OK.search(lic):
        out.append(("fix", f"{name}: '{lic}' does not say commercial use is allowed; read the licence and note it"))
    if use == "paid-ad" and lic and PAID_AD_RISK.search(lic):
        out.append(("blocker", f"{name}: '{lic}' may not cover paid or promoted posts; check the plan"))
    if not (row.get("source url") or row.get("source")):
        out.append(("fix", f"{name}: no source recorded"))
    if (row.get("credit needed") or "").lower().startswith("y"):
        out.append(("fix", f"{name}: credit owed to {row.get('author') or 'the author'}; put it in the description or credits page"))
    return out


def cmd_credits_check(args) -> int:
    rows = read_rows()
    found = []
    for r in rows:
        found += judge(r, args.use)
    if args.dir:
        logged = {Path(r.get("file", "")).name for r in rows}
        for f in sorted(Path(args.dir).rglob("*")):
            if f.suffix.lower() in AUDIO_EXT and f.name not in logged:
                found.append(("blocker", f"{f}: used but not in {CREDITS}"))
    blockers = sum(1 for k, _ in found if k == "blocker")
    if args.json:
        print(json.dumps({"rows": len(rows), "problems": [{"kind": k, "text": t} for k, t in found]}, indent=2))
    else:
        print(f"sound credits: {len(rows)} rows, {blockers} blockers, {len(found) - blockers} fixes ({args.use})")
        for k, t in found:
            print(f"  {k}: {t}")
        if not rows:
            print(f"  no {CREDITS} yet: add each file with `ult audio credits add`")
        print("licence terms change: check before relying on the provider's current terms")
    return 1 if blockers else 0


def _measure(path: Path) -> tuple[float | None, float | None]:
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path), "-vn", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True, timeout=600)
    i = re.findall(r"\bI:\s+(-?\d+(?:\.\d+)?)\s+LUFS", r.stderr)
    tp = re.findall(r"True peak:\s+Peak:\s+(-?(?:\d+(?:\.\d+)?|inf))\s+dBFS", r.stderr)
    return (float(i[-1]) if i else None, float(tp[-1]) if tp and tp[-1] != "-inf" else None)


def mix_graph(music_db: float, duck: float, tail: float, dur: float) -> str:
    ratio = max(2.0, min(20.0, round(1 + duck / 2, 1)))
    fade_at = max(dur + tail - 1.5, 0)
    return (f"[1:a]volume={music_db}dB,afade=t=out:st={fade_at:.2f}:d=1.5[m];"
            f"[0:a]apad=pad_dur={tail},asplit=2[v][key];"
            f"[m][key]sidechaincompress=threshold=0.02:ratio={ratio}:attack=20:release=400[d];"
            "[v][d]amix=inputs=2:duration=first:normalize=0[mix]")


def _ffmpeg(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-y"] + cmd, capture_output=True, text=True, timeout=1800)


def cmd_mix(args) -> int:
    from ultlib.media import probe  # noqa: PLC0415
    voice, music, out = Path(args.voice), Path(args.music), Path(args.out)
    if not (voice.is_file() and music.is_file()) or not shutil.which("ffmpeg"):
        print("mix needs the voice file, the music file and ffmpeg")
        return 2
    dur = probe(voice)["duration"]
    out.parent.mkdir(parents=True, exist_ok=True)
    rough = out.with_name(out.stem + "-premix.wav")
    loop = ["-stream_loop", "-1"] if args.loop else []
    graph = mix_graph(args.music_db, args.duck, args.tail, dur)
    # With a video, cut the mix to the picture first so the loudness is measured on what is kept.
    trim = ["-t", f"{probe(Path(args.video))['duration']:.3f}"] if args.video else []
    r = _ffmpeg(["-i", str(voice)] + loop + ["-i", str(music), "-filter_complex", graph, "-map", "[mix]",
                 "-ar", "48000"] + trim + [str(rough)])
    if r.returncode:
        print("ffmpeg could not mix:\n" + r.stderr[-800:])
        return 1
    norm = f"loudnorm=I={args.target}:TP={args.tp}:LRA=11"
    first = _ffmpeg(["-i", str(rough), "-af", norm + ":print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", first.stderr)
    if m:
        j = json.loads(m.group(0))
        norm += (f":measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
                 f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    if args.video:
        cmd = ["-i", args.video, "-i", str(rough), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", norm,
               "-ar", "48000", "-c:a", "aac", "-b:a", "192k", str(out)]
    else:
        cmd = ["-i", str(rough), "-af", norm, "-ar", "48000"] + (["-b:a", "192k"] if out.suffix != ".wav" else []) + [str(out)]
    r = _ffmpeg(cmd)
    rough.unlink(missing_ok=True)
    if r.returncode:
        print("ffmpeg could not normalise:\n" + r.stderr[-800:])
        return 1
    lufs, tp = _measure(out)
    ok = lufs is not None and abs(lufs - args.target) <= 1 and (tp is None or tp <= args.tp + 0.1)
    print(f"wrote {out}: measured {lufs} LUFS integrated, true peak {tp} dBTP "
          f"(target {args.target} LUFS, at most {args.tp} dBTP) -> {'pass' if ok else 'out of range'}")
    print("listen to the whole mix: the voice must stay clear wherever the music lifts")
    return 0 if ok else 1


def register(sub):
    p = sub.add_parser("audio", help="sound credits log and a local voice-over-music mix")
    s = p.add_subparsers(dest="acmd", required=True)
    cr = s.add_parser("credits", help="brand/sound-credits.md").add_subparsers(dest="ccmd", required=True)
    c = cr.add_parser("add")
    c.add_argument("file")
    c.add_argument("--source", required=True, help="page or tool the file came from")
    c.add_argument("--licence", required=True, help='e.g. "CC0", "CC BY 4.0", "ElevenLabs paid plan", "own recording"')
    c.add_argument("--author")
    c.add_argument("--credit", choices=("yes", "no"))
    c.add_argument("--used-in")
    c.set_defaults(func=cmd_credits_add)
    c = cr.add_parser("check")
    c.add_argument("--use", choices=("organic", "paid-ad"), default="organic")
    c.add_argument("--dir", help="folder of audio files that must all be logged")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_credits_check)
    c = s.add_parser("mix", help="duck music under a voice and normalise the loudness")
    c.add_argument("voice")
    c.add_argument("music")
    c.add_argument("--out", required=True)
    c.add_argument("--music-db", type=float, default=-16.0, help="music gain before ducking (dB)")
    c.add_argument("--duck", type=float, default=8.0, help="about how many dB the music drops under speech")
    c.add_argument("--tail", type=float, default=1.5, help="seconds of music after the last word")
    c.add_argument("--target", type=float, default=-14.0)
    c.add_argument("--tp", type=float, default=-1.0)
    c.add_argument("--video", help="put the mix on this video (video stream copied)")
    c.add_argument("--loop", action="store_true", help="loop music shorter than the voice")
    c.set_defaults(func=cmd_mix)
