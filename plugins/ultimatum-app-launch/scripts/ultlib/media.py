"""`ult beats` and `ult media` — local audio and video checks for Motion Graphics.

  ult beats FILE      beat times from librosa when installed ("suggested beats");
                      otherwise loud onsets found from ffmpeg-decoded audio ("possible cues").
                      Both are suggestions: listen and confirm before timing cuts.
  ult media FILE      ffprobe facts (duration, size, fps, codecs, audio) and loudness, with warnings.

Uses ffmpeg/ffprobe from PATH when present; never installs or contacts the network.
"""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
from array import array
from pathlib import Path

RATE = 11025
HOP = 256


def _librosa_beats(path: Path) -> tuple[list[float], float] | None:
    try:
        import librosa  # optional
    except Exception:
        return None
    y, sr = librosa.load(str(path), mono=True)
    tempo, frames = librosa.beat.beat_track(y=y, sr=sr)
    times = [round(float(t), 3) for t in librosa.frames_to_time(frames, sr=sr)]
    return times, float(getattr(tempo, "item", lambda: tempo)())


def _decode(path: Path) -> array:
    out = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", str(path), "-ac", "1", "-ar", str(RATE),
                          "-f", "s16le", "-"], capture_output=True, timeout=300, check=True).stdout
    a = array("h")
    a.frombytes(out[: len(out) // 2 * 2])
    return a


def onset_cues(samples, rate: int = RATE, hop: int = HOP, min_gap: float = 0.12) -> list[float]:
    """Times where loudness jumps (energy flux peaks above mean + 1.5 sd). Rough, stdlib only."""
    env = []
    for i in range(0, max(len(samples) - hop, 0), hop):
        s = 0
        for v in samples[i:i + hop]:
            s += v * v
        env.append(math.sqrt(s / hop))
    flux = [max(env[i] - env[i - 1], 0.0) for i in range(1, len(env))]
    if not flux:
        return []
    mean = sum(flux) / len(flux)
    sd = math.sqrt(sum((f - mean) ** 2 for f in flux) / len(flux))
    cut = mean + 1.5 * sd
    cues: list[float] = []
    for i in range(1, len(flux) - 1):
        if flux[i] > cut and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]:
            t = round((i + 1) * hop / rate, 3)
            if not cues or t - cues[-1] >= min_gap:
                cues.append(t)
    return cues


def beats(path: Path, use_librosa: bool = True) -> dict:
    got = _librosa_beats(path) if use_librosa else None
    if got:
        times, tempo = got
        return {"kind": "suggested beats", "source": "librosa", "tempo": round(tempo, 1), "times": times}
    if not shutil.which("ffmpeg"):
        return {"kind": "none", "source": "none", "times": [],
                "note": "neither librosa nor ffmpeg found: mark cues by listening"}
    times = onset_cues(_decode(path))
    return {"kind": "possible cues", "source": "ffmpeg onset estimate", "times": times}


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams",
                          str(path)], capture_output=True, text=True, timeout=120, check=True).stdout
    info = json.loads(out or "{}")
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    a = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    fps = None
    if v and v.get("avg_frame_rate", "0/0") != "0/0":
        n, _, dnm = v["avg_frame_rate"].partition("/")
        fps = round(float(n) / float(dnm or 1), 3) if float(dnm or 1) else None
    return {
        "duration": round(float(info.get("format", {}).get("duration", 0) or 0), 3),
        "width": v and v.get("width"), "height": v and v.get("height"), "fps": fps,
        "video_codec": v and v.get("codec_name"), "pix_fmt": v and v.get("pix_fmt"),
        "audio": bool(a), "audio_codec": a and a.get("codec_name"),
        "sample_rate": a and int(a.get("sample_rate", 0) or 0),
    }


def loudness(path: Path) -> float | None:
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path), "-vn", "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, timeout=300)
    m = re.findall(r"\bI:\s+(-?\d+(?:\.\d+)?)\s+LUFS", r.stderr)
    return float(m[-1]) if m else None


def warnings(m: dict) -> list[str]:
    w = []
    if not m["video_codec"]:
        w.append("no video stream")
    if m["width"] and (m["width"] % 2 or m["height"] % 2):
        w.append("odd width or height: many players reject it")
    if m["pix_fmt"] and m["pix_fmt"] != "yuv420p" and m["video_codec"] in ("h264", "hevc"):
        w.append(f"pix_fmt {m['pix_fmt']}: use yuv420p so phones and browsers play it")
    if m["fps"] and m["fps"] < 23.9:
        w.append(f"{m['fps']} fps: motion may look choppy (24-60 is usual)")
    if not m["audio"]:
        w.append("no audio track")
    lu = m.get("lufs")
    if lu is not None and lu > -9:
        w.append(f"loudness {lu} LUFS: very loud, may distort or be turned down (about -14 for social)")
    if lu is not None and lu < -24:
        w.append(f"loudness {lu} LUFS: quiet (about -14 for social)")
    return w


def cmd_beats(args) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"ult beats: no such file: {path}")
        return 2
    try:
        r = beats(path, use_librosa=not args.no_librosa)
    except (subprocess.SubprocessError, OSError) as e:
        print(f"ult beats: could not read audio: {e}")
        return 1
    if args.json:
        print(json.dumps(r, indent=2))
        return 0
    head = f"{r['kind']} ({r['source']}" + (f", ~{r['tempo']} bpm" if r.get("tempo") else "") + f"): {len(r['times'])}"
    print(head)
    print("times (s): " + ", ".join(f"{t:.2f}" for t in r["times"][: args.max]) + (" ..." if len(r["times"]) > args.max else ""))
    print("these are suggestions: listen and confirm each cue before timing cuts to it" if r["times"] else r.get("note", ""))
    return 0


def cmd_media(args) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"ult media: no such file: {path}")
        return 2
    if not shutil.which("ffprobe"):
        print("ult media: ffprobe not found; check the export by playing it and say it was not measured")
        return 1
    try:
        m = probe(path)
        m["lufs"] = loudness(path) if m["audio"] and shutil.which("ffmpeg") else None
    except (subprocess.SubprocessError, OSError, ValueError) as e:
        print(f"ult media: could not read {path}: {e}")
        return 1
    m["warnings"] = warnings(m)
    if args.json:
        print(json.dumps(m, indent=2))
    else:
        print(f"{path.name}: {m['duration']}s  {m['width']}x{m['height']}  {m['fps']} fps  "
              f"video {m['video_codec']}/{m['pix_fmt']}  audio {m['audio_codec'] or 'none'}"
              + (f" {m['sample_rate']} Hz" if m["audio"] else "") + (f"  loudness {m['lufs']} LUFS" if m["lufs"] is not None else ""))
        for w in m["warnings"]:
            print(f"warn: {w}")
        if not m["warnings"]:
            print("ok: no export problems found (still watch it once at normal speed)")
    return 0


def register(sub):
    b = sub.add_parser("beats", help="suggested beats (librosa) or possible cues (ffmpeg) in an audio or video file")
    b.add_argument("file")
    b.add_argument("--json", action="store_true")
    b.add_argument("--max", type=int, default=40, help="times to print (default 40)")
    b.add_argument("--no-librosa", action="store_true", help="use the ffmpeg fallback even if librosa is installed")
    b.set_defaults(func=cmd_beats)
    m = sub.add_parser("media", help="check a video export: duration, size, fps, codecs, audio, loudness")
    m.add_argument("file")
    m.add_argument("--json", action="store_true")
    m.set_defaults(func=cmd_media)
