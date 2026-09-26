"""Picture tools: stills from motion, contact sheets, animatics, rough-cut assembly."""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

from . import ff
from .core import Production, die, to_float

IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp")


def frames(video: Path, out_dir: Path, at: list[float] | None = None, every: float = 0.0,
           last: bool = False, width: int = 0) -> list[Path]:
    """Harvest stills: specific times, a regular interval, or the last frame (for chaining)."""
    video = Path(video)
    out_dir.mkdir(parents=True, exist_ok=True)
    scale = ["-vf", f"scale={width}:-2"] if width else []
    made: list[Path] = []
    if last:
        out = out_dir / f"{video.stem}_last.png"
        ff.run(["-sseof", "-0.1", "-i", video, "-frames:v", "1", "-update", "1", *scale, out])
        made.append(out)
    for t in at or []:
        out = out_dir / f"{video.stem}_{int(round(t * 1000)):06d}ms.png"
        ff.run(["-ss", f"{t}", "-i", video, "-frames:v", "1", "-update", "1", *scale, out])
        made.append(out)
    if every:
        pattern = out_dir / f"{video.stem}_%03d.png"
        vf = f"fps=1/{every}" + (f",scale={width}:-2" if width else "")
        ff.run(["-i", video, "-vf", vf, pattern])
        made += sorted(out_dir.glob(f"{video.stem}_[0-9][0-9][0-9].png"))
    if not made:
        die("say what to extract: --at 1.5,3, --every 0.5 or --last")
    return made


def contact_sheet(videos: list[Path], out: Path, cols: int = 6, width: int = 320) -> Path:
    """One row per video, `cols` frames sampled evenly across each clip, rows stacked.

    The fastest way to compare takes: motion, drift and artefacts show up side by side.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    gap = 4
    row_w = cols * width + (cols - 1) * gap
    with tempfile.TemporaryDirectory() as tmp:
        rows = []
        for i, v in enumerate(videos):
            dur = ff.probe(v)["duration"] or 1.0
            n = cols if dur >= 0.5 else 1
            step = max(dur / n, 0.04)
            row = Path(tmp) / f"row{i:03d}.png"
            vf = (f"fps=1/{step:.4f},scale={width}:-2,tile={n}x1:padding={gap}:color=black,"
                  f"pad={row_w}:ih:0:0:black")
            ff.run(["-i", v, "-vf", vf, "-frames:v", "1", "-update", "1", row])
            rows.append(row)
        if len(rows) == 1:
            ff.run(["-i", rows[0], "-frames:v", "1", "-update", "1", out])
            return out
        inputs: list = []
        for r in rows:
            inputs += ["-i", r]
        chain = "".join(f"[{i}:v]" for i in range(len(rows))) + f"vstack=inputs={len(rows)}"
        ff.run([*inputs, "-filter_complex", chain, "-frames:v", "1", "-update", "1", out])
    return out


def _board_for(prod: Production, shot: str) -> Path | None:
    folder = prod.dir("board") / "boards"
    for ext in IMAGE_EXT:
        for cand in (folder / f"{shot}{ext}", folder / f"{shot.lower()}{ext}"):
            if cand.exists():
                return cand
    return None


def animatic(prod: Production, audio: Path | None = None, default_dur: float = 3.0) -> Path:
    """Boards + planned durations (+ temp audio) → a timed animatic. Missing boards become slates."""
    shots = [s for s in prod.shots() if s.get("status", "").lower() != "cut"]
    if not shots:
        die("shot list is empty: fill 03_board/shotlist.csv first")
    w, h = prod.size
    fps = prod.fps
    out = prod.next_version(prod.dir("board"), "animatic", ".mp4")
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i, s in enumerate(shots):
            dur = to_float(s.get("duration_s"), default_dur) or default_dur
            seg = Path(tmp) / f"seg{i:03d}.mp4"
            board = _board_for(prod, s["shot"])
            if board:
                args = ["-loop", "1", "-t", f"{dur}", "-i", board]
                vf = ff.fit_filter(w, h, fps, "pad")
            else:
                args = ["-f", "lavfi", "-t", f"{dur}", "-i", f"color=c=0x1a1a18:s={w}x{h}:r={fps}"]
                vf = f"fps={fps},format=yuv420p"
            ff.run([*args, "-vf", vf, "-an", *ff.VIDEO_OUT, "-t", f"{dur}", seg])
            parts.append(seg)
        concat = Path(tmp) / "list.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts))
        picture = Path(tmp) / "picture.mp4"
        ff.run(["-f", "concat", "-safe", "0", "-i", concat, "-c", "copy", picture])
        if audio:
            ff.run(["-i", picture, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    *ff.AUDIO_OUT, "-shortest", out])
        else:
            ff.run(["-i", picture, "-c", "copy", out])
    missing = [s["shot"] for s in shots if not _board_for(prod, s["shot"])]
    if missing:
        print(f"note: no board yet for {', '.join(missing)} (shown as dark slates)")
    return out


EDL_HELP = """# cut.txt: one line per event, top to bottom = order in the cut.
# <take id | file path | 'slate'>  [in seconds]  [out seconds]  [# comment]
# Examples:
#   S01_t003                  (whole take, minus the default head/tail trim)
#   S02_t001  0.4  3.1        (in at 0.4s, out at 3.1s of the take)
#   slate     1.5             (1.5s of black: a placeholder or a beat of silence)
#   ../05_sound/temp/insert.mp4 0 2
"""


def parse_edl(text: str) -> list[tuple[str, float | None, float | None]]:
    events = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        src = parts[0]
        vals = [float(x) for x in parts[1:3] if re.match(r"^-?\d+(\.\d+)?$", x)]
        a = vals[0] if len(vals) > 0 else None
        b = vals[1] if len(vals) > 1 else None
        if a is not None and b is not None and b <= a:
            die(f"cut.txt: out point must be after in point: {raw.strip()}")
        events.append((src, a, b))
    return events


def _resolve(prod: Production, src: str) -> Path:
    takes = {t["take"].upper(): t for t in prod.takes()}
    if src.upper() in takes:
        return prod.root / takes[src.upper()]["file"]
    p = Path(src)
    for base in (prod.dir("edit"), prod.root, Path.cwd()):
        if (base / p).exists():
            return (base / p).resolve()
    die(f"cut.txt: can't find '{src}' (not a logged take id or a file)")
    raise AssertionError


def assemble(prod: Production, edl_path: Path | None = None, trim: float = 0.1,
             fit: str = "crop", fade_ms: int = 30) -> Path:
    """Rough cut from cut.txt: conform every event to the production frame, then join.

    trim: seconds shaved off the head and tail of whole takes (generation jitter lives there).
    Every event gets a short audio fade in/out so joins don't click.
    """
    edl_path = edl_path or prod.dir("edit") / "cut.txt"
    if not edl_path.exists():
        edl_path.parent.mkdir(parents=True, exist_ok=True)
        edl_path.write_text(EDL_HELP)
        die(f"wrote an empty {prod.rel(edl_path)}: list your takes in it, then run assemble again")
    events = parse_edl(edl_path.read_text())
    if not events:
        die(f"{prod.rel(edl_path)} has no events yet")
    w, h = prod.size
    fps = prod.fps
    out = prod.next_version(prod.dir("edit") / "cuts", "cut", ".mp4")
    fade = fade_ms / 1000
    # Every event is quantised to whole frames and its audio padded/trimmed to exactly that
    # length. Intermediates carry PCM audio; AAC is encoded once at the end. Without this,
    # per-event frame rounding and AAC priming push audio ahead of picture at every cut.
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i, (src, a, b) in enumerate(events):
            seg = Path(tmp) / f"ev{i:03d}.mkv"
            if src.lower() == "slate":
                path, has_audio, start = None, False, 0.0
                dur = a or 1.0
                inputs = ["-f", "lavfi", "-t", f"{dur + 1}", "-i", f"color=c=black:s={w}x{h}:r={fps}"]
            else:
                path = _resolve(prod, src)
                info = ff.probe(path)
                if path.suffix.lower() in IMAGE_EXT:
                    dur = (b - a) if (a is not None and b is not None) else (a or 2.0)
                    inputs = ["-loop", "1", "-t", f"{dur + 1}", "-i", path]
                    has_audio = False
                else:
                    start = a if a is not None else trim
                    end = b if b is not None else max(info["duration"] - trim, start + 0.1)
                    dur = end - start
                    inputs = ["-ss", f"{start}", "-t", f"{dur + 1}", "-i", path]
                    has_audio = info["has_audio"]
            frames = max(1, round(dur * fps))
            dur = frames / fps
            vf = ff.fit_filter(w, h, fps, fit)
            if has_audio:
                audio_in, amap = [], "0:a:0"
            else:
                audio_in, amap = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"], "1:a"
            af = (f"aresample=48000,aformat=channel_layouts=stereo,atrim=duration={dur:.6f},"
                  f"apad=whole_dur={dur:.6f},afade=t=in:d={fade},afade=t=out:st={max(dur - fade, 0):.4f}:d={fade}")
            ff.run([*inputs, *audio_in, "-map", "0:v:0", "-map", amap, "-vf", vf, "-af", af,
                    "-frames:v", str(frames), *ff.VIDEO_OUT[:-2], "-c:a", "pcm_s16le", "-t", f"{dur:.6f}", seg])
            parts.append(seg)
        concat = Path(tmp) / "list.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts))
        ff.run(["-f", "concat", "-safe", "0", "-i", concat, "-c:v", "copy", *ff.AUDIO_OUT,
                "-movflags", "+faststart", out])
    return out
