"""Thin ffmpeg layer. Works with ffmpeg alone; uses ffprobe when present."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from .core import die


# Homebrew's plain `ffmpeg` has no libass (burnt-in captions). `ffmpeg-full` does, but is keg-only
# (not on PATH), so look for it before PATH.
FULL_BUILDS = (Path("/opt/homebrew/opt/ffmpeg-full/bin"), Path("/usr/local/opt/ffmpeg-full/bin"))
INSTALL_HINT = ("macOS: `brew install ffmpeg-full`; Windows: `winget install Gyan.FFmpeg`; "
                "Linux: your package manager's ffmpeg")


def find(name: str) -> str | None:
    """ffmpeg or ffprobe: the FFMPEG/FFPROBE env var, then Homebrew's ffmpeg-full, then PATH.
    ffprobe is taken from beside the chosen ffmpeg when it's there, so the pair always match."""
    env = os.environ.get(name.upper())
    if env:
        return env
    if name == "ffprobe":
        exe = find("ffmpeg")
        mate = Path(exe).with_name("ffprobe" + Path(exe).suffix) if exe else None
        return str(mate) if mate and mate.exists() else shutil.which("ffprobe")
    full = next((d / name for d in FULL_BUILDS if (d / name).exists()), None)
    return str(full) if full else shutil.which(name)


def ffmpeg_bin() -> str:
    exe = find("ffmpeg")
    if not exe:
        die(f"ffmpeg not found. Install it ({INSTALL_HINT}) or set FFMPEG=/path/to/ffmpeg.")
    return exe


def run(args: list[str], quiet: bool = True) -> subprocess.CompletedProcess:
    """Run ffmpeg. -nostdin matters: without it ffmpeg eats the stdin of shell loops."""
    cmd = [ffmpeg_bin(), "-nostdin", "-hide_banner", "-y"]
    if quiet:
        cmd += ["-loglevel", "error"]
    cmd += [str(a) for a in args]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        tail = "\n".join(res.stderr.strip().splitlines()[-8:])
        die(f"ffmpeg failed:\n{tail}")
    return res


def analyse(args: list[str]) -> str:
    """Run an analysis pass (filters that log to stderr) and return stderr."""
    cmd = [ffmpeg_bin(), "-nostdin", "-hide_banner", "-nostats"] + [str(a) for a in args]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stderr


def probe(path: Path) -> dict:
    """duration (s), width, height, fps, has_audio, has_video."""
    path = Path(path)
    if not path.exists():
        die(f"not found: {path}")
    fp = find("ffprobe")
    if fp:
        res = subprocess.run([fp, "-v", "error", "-print_format", "json", "-show_format",
                              "-show_streams", str(path)], capture_output=True, text=True)
        if res.returncode == 0:
            data = json.loads(res.stdout or "{}")
            v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
            a = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
            fps = 0.0
            if v and v.get("avg_frame_rate", "0/0") != "0/0":
                num, den = v["avg_frame_rate"].split("/")
                fps = float(num) / float(den) if float(den) else 0.0
            dur = data.get("format", {}).get("duration")
            return {
                "duration": float(dur) if dur not in (None, "N/A") else 0.0,
                "width": int(v["width"]) if v else 0,
                "height": int(v["height"]) if v else 0,
                "fps": round(fps, 3),
                "has_video": v is not None,
                "has_audio": a is not None,
            }
    err = analyse(["-i", str(path)])
    info = {"duration": 0.0, "width": 0, "height": 0, "fps": 0.0, "has_video": False, "has_audio": False}
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    if m:
        h, mi, s = m.groups()
        info["duration"] = int(h) * 3600 + int(mi) * 60 + float(s)
    vline = next((ln for ln in err.splitlines() if "Video:" in ln), "")
    if vline:
        info["has_video"] = True
        m = re.search(r"\b(\d{2,5})x(\d{2,5})\b", vline)
        if m:
            info["width"], info["height"] = int(m.group(1)), int(m.group(2))
        m = re.search(r"([\d.]+) fps", vline) or re.search(r"([\d.]+) tbr", vline)
        if m:
            info["fps"] = float(m.group(1))
    info["has_audio"] = "Audio:" in err
    return info


def loudness(path: Path) -> dict:
    """Integrated loudness (LUFS), loudness range (LU) and true peak (dBTP)."""
    err = analyse(["-i", str(path), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    summary = err[err.rfind("Summary:"):] if "Summary:" in err else err
    out = {"lufs": None, "lra": None, "true_peak": None}
    m = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)
    if m:
        out["lufs"] = float(m.group(1))
    m = re.search(r"LRA:\s+(-?[\d.]+) LU", summary)
    if m:
        out["lra"] = float(m.group(1))
    m = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary)
    if m:
        out["true_peak"] = float("-inf") if m.group(1) == "-inf" else float(m.group(1))
    return out


def detect(path: Path, vf: str | None = None, af: str | None = None) -> list[tuple[float, float]]:
    """Run blackdetect/freezedetect/silencedetect and return (start, end) spans."""
    args = ["-i", str(path)]
    if vf:
        args += ["-an", "-vf", vf]
    if af:
        args += ["-vn", "-af", af]
    args += ["-f", "null", "-"]
    err = analyse(args)
    spans = []
    if vf and vf.startswith("blackdetect"):
        for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", err):
            spans.append((float(m.group(1)), float(m.group(2))))
        return spans
    starts = [float(x) for x in re.findall(r"(?:freeze|silence)_start: ?([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"(?:freeze|silence)_end: ?([\d.]+)", err)]
    for i, s in enumerate(starts):
        spans.append((s, ends[i] if i < len(ends) else -1.0))
    return spans


def fit_filter(w: int, h: int, fps: float, mode: str = "crop") -> str:
    """Conform any clip to the production frame.

    crop (default) scales to fill and crops the overflow: generated clips often come back at
    odd sizes (e.g. 2:3), and black bars inside a cut read as a mistake. pad letterboxes.
    """
    if mode == "crop":
        scale = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    else:
        scale = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
                 f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black")
    return f"{scale},setsar=1,fps={fps},format=yuv420p"


VIDEO_OUT = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
             "-movflags", "+faststart"]
AUDIO_OUT = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
