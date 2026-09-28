"""Delivery: aspect variants, loudness to spec, burnt-in subtitles, sensible names."""
from __future__ import annotations

import tempfile
from pathlib import Path

from . import ff
from .core import ASPECTS, Production, die
from .sound import match_loudness


def _fit(w: int, h: int, fps: float, mode: str) -> str:
    if mode == "blur":
        # Fill the frame with a blurred copy, the full picture centred on top. For 16:9 → 9:16
        # when a crop would lose the story. A reframed crop is still better when you can.
        return (f"split[a][b];[a]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
                f"boxblur=24:2,eq=brightness=-0.08[bg];[b]scale={w}:{h}:force_original_aspect_ratio=decrease[fg];"
                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps={fps},format=yuv420p")
    return ff.fit_filter(w, h, fps, mode)


def deliver(prod: Production, master: Path, aspects: list[str], fit: str = "crop",
            loudness: float | None = None) -> list[Path]:
    master = Path(master)
    info = ff.probe(master)
    target = loudness if loudness is not None else float(prod.cfg.get("loudness_lufs", -14))
    out_dir = prod.dir("delivery") / "masters"
    made = []
    with tempfile.TemporaryDirectory() as tmp:
        audio = None
        if info["has_audio"]:
            raw = Path(tmp) / "raw.wav"
            ff.run(["-i", master, "-vn", "-ar", "48000", raw])
            audio = Path(tmp) / "norm.wav"
            match_loudness(raw, audio, target)
        for aspect in aspects:
            if aspect not in ASPECTS:
                die(f"unknown aspect {aspect}; use {', '.join(ASPECTS)}")
            w, h = ASPECTS[aspect]
            token = aspect.replace(":", "x").replace(".", "")
            out = prod.next_version(out_dir, f"{prod.slug}_{token}", ".mp4")
            vf = _fit(w, h, prod.fps, fit)
            if fit == "blur":
                picture = ["-filter_complex", f"[0:v]{vf}[vout]", "-map", "[vout]"]
            else:
                picture = ["-map", "0:v", "-vf", vf]
            if audio:
                ff.run(["-i", master, "-i", audio, *picture, "-map", "1:a",
                        *ff.VIDEO_OUT, *ff.AUDIO_OUT, "-shortest", out])
            else:
                ff.run(["-i", master, *picture, *ff.VIDEO_OUT, out])
            made.append(out)
    return made


def overlay(video: Path, graphics: list[tuple[Path, float]], out: Path | None = None) -> Path:
    """Composite transparent graphics (end card, supers, lower thirds) over a delivered shape.

    Each graphic is a render with an alpha channel (a HyperFrames MOV, or a PNG held to the end)
    placed at a time in seconds. It's scaled to fit the frame and centred; the audio is copied
    untouched. Render every shape's graphics at that shape: a crop would cut the type.
    """
    from .media import IMAGE_EXT
    info = ff.probe(video)
    w, h = info["width"], info["height"]
    out = out or video.with_name(f"{video.stem}_gfx{video.suffix}")
    inputs, chain, last = [], [], "0:v"
    for i, (g, at) in enumerate(graphics, 1):
        g = Path(g)
        if not g.exists():
            die(f"not found: {g}")
        if g.suffix.lower() in IMAGE_EXT:
            inputs += ["-loop", "1", "-t", f"{max(info['duration'] - at, 0.1):.3f}", "-i", g]
        else:  # ffmpeg's own VP9 decoder drops alpha; libvpx keeps it
            inputs += (["-c:v", "libvpx-vp9"] if g.suffix.lower() == ".webm" else []) + ["-i", g]
        chain.append(f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,format=rgba,"
                     f"setpts=PTS-STARTPTS+{at}/TB[g{i}];[{last}][g{i}]overlay=(W-w)/2:(H-h)/2:eof_action=pass[v{i}]")
        last = f"v{i}"
    audio = ["-map", "0:a", "-c:a", "copy"] if info["has_audio"] else []
    ff.run(["-i", video, *inputs, "-filter_complex", ";".join(chain) + f";[{last}]format=yuv420p[vout]",
            "-map", "[vout]", *audio, *ff.VIDEO_OUT, out])
    return out
