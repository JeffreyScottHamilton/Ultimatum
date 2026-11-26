"""Platform sizes, caption limits and safe zones, and the file and caption checks that use them."""
from __future__ import annotations

import re
import struct
from pathlib import Path

SPECS_AS_OF = "November 2026"
# Sizes in pixels, video length in seconds, caption limit in characters. Platforms change these:
# confirm on the platform's own help page before relying on them.
PLATFORMS = {
    "tiktok": {"sizes": [(1080, 1920)], "video_max": 600, "caption_max": 4000, "safe": (150, 270, 0, 120), "hashtags_max": 5},
    "reels": {"sizes": [(1080, 1920)], "video_max": 180, "caption_max": 2200, "safe": (220, 420, 0, 0), "hashtags_max": 5},
    "shorts": {"sizes": [(1080, 1920)], "video_max": 180, "caption_max": 100, "safe": (150, 300, 0, 100), "hashtags_max": 3},
    "instagram-feed": {"sizes": [(1080, 1350), (1080, 1080), (1080, 566)], "video_max": 900, "caption_max": 2200,
                       "safe": (0, 0, 0, 0), "hashtags_max": 5},
    "instagram-story": {"sizes": [(1080, 1920)], "video_max": 60, "caption_max": 0, "safe": (250, 250, 0, 0), "hashtags_max": 0},
    "linkedin": {"sizes": [(1080, 1350), (1080, 1080), (1200, 627)], "video_max": 600, "caption_max": 3000,
                 "safe": (0, 0, 0, 0), "hashtags_max": 3},
    "x": {"sizes": [(1600, 900), (1080, 1350), (1080, 1080)], "video_max": 140, "caption_max": 280, "safe": (0, 0, 0, 0),
          "hashtags_max": 2},
    "facebook": {"sizes": [(1080, 1350), (1080, 1080), (1080, 1920)], "video_max": 900, "caption_max": 5000,
                 "safe": (0, 0, 0, 0), "hashtags_max": 3},
    "pinterest": {"sizes": [(1000, 1500)], "video_max": 300, "caption_max": 500, "safe": (0, 0, 0, 0), "hashtags_max": 0},
}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm"}
MAX_IMAGE_BYTES = 8_000_000
MAX_VIDEO_BYTES = 1_000_000_000


def image_size(path: Path) -> tuple[int, int] | None:
    """Width and height of a PNG, JPEG or WebP, read from the header bytes."""
    data = path.read_bytes()[:256 * 1024]
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        if data[12:16] == b"VP8X":
            return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
        if data[12:16] == b"VP8 ":
            w, h = struct.unpack("<HH", data[26:30])
            return w & 0x3FFF, h & 0x3FFF
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker, seg = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + seg
    return None


def _ratio_ok(w: int, h: int, sizes) -> tuple[bool, bool]:
    """(aspect matches one allowed size, size is at least that big)."""
    for sw, sh in sizes:
        if abs(w / h - sw / sh) < 0.02:
            return True, w >= sw * 0.98
    return False, False


def check_caption(text: str, spec: dict) -> list[tuple[str, str]]:
    out = []
    if spec["caption_max"] == 0 and text.strip():
        out.append(("fix", "this format shows no caption: put the words on the image"))
    elif len(text) > spec["caption_max"]:
        out.append(("blocker", f"caption is {len(text)} characters, limit {spec['caption_max']}"))
    tags = re.findall(r"(?<!\w)#\w+", text)
    if spec["hashtags_max"] and len(tags) > spec["hashtags_max"]:
        out.append(("fix", f"{len(tags)} hashtags; {spec['hashtags_max']} or fewer reads better"))
    first = text.strip().splitlines()[0] if text.strip() else ""
    if len(first) > 125:
        out.append(("fix", "first line is long; the feed cuts it near 125 characters, so the hook may be hidden"))
    return out


def check_file(path: Path, spec: dict) -> list[tuple[str, str]]:
    out, name = [], path.name
    if not path.is_file():
        return [("blocker", f"{name}: file not found")]
    size_b = path.stat().st_size
    if path.suffix.lower() in VIDEO_EXT:
        from ultlib.media import probe  # noqa: PLC0415 - needs ffprobe only for video
        try:
            m = probe(path)
        except Exception as e:  # noqa: BLE001 - missing ffprobe or a broken file
            return [("blocker", f"{name}: could not read the video ({e.__class__.__name__}); is ffprobe installed?")]
        w, h = m.get("width") or 0, m.get("height") or 0
        if m["duration"] > spec["video_max"]:
            out.append(("blocker", f"{name}: {m['duration']:.0f} s, longer than {spec['video_max']} s"))
        if not m["audio"]:
            out.append(("fix", f"{name}: no audio track"))
        if m.get("video_codec") not in ("h264", "hevc", None):
            out.append(("fix", f"{name}: codec {m.get('video_codec')}; H.264 uploads most reliably"))
        if size_b > MAX_VIDEO_BYTES:
            out.append(("blocker", f"{name}: {size_b // 1_000_000} MB is very large; export smaller"))
    else:
        wh = image_size(path)
        if not wh:
            return [("blocker", f"{name}: not a PNG, JPEG or WebP image this check can read")]
        w, h = wh
        if size_b > MAX_IMAGE_BYTES:
            out.append(("fix", f"{name}: {size_b // 1_000_000} MB; compress below 8 MB"))
    if w and h:
        ok, big = _ratio_ok(w, h, spec["sizes"])
        allowed = ", ".join(f"{a}x{b}" for a, b in spec["sizes"])
        if not ok:
            out.append(("blocker", f"{name}: {w}x{h} does not match {allowed}; it will be cropped or letterboxed"))
        elif not big:
            out.append(("fix", f"{name}: {w}x{h} is smaller than {allowed}; it may look soft"))
    return out
