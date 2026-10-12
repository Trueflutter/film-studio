"""Picture tools: stills from motion, contact sheets, animatics, rough-cut assembly."""
from __future__ import annotations

import math
import re
import sys
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


def shot_cuts(path: Path, threshold: float = 0.3) -> list[float]:
    """Times of every hard cut inside a source clip (the first frame of each new shot).

    Generated clips often hold a cut of their own (multishot modes, a model that "cuts away"),
    so a range taken from one can leak a frame or two of the neighbouring shot. Unlike
    `review`'s detector nothing is filtered out: a cut right at an edge is exactly the risk.
    """
    err = ff.analyse(["-i", str(path), "-an", "-vf",
                      f"setpts=PTS-STARTPTS,scale=320:-2,select='gt(scene,{threshold})',showinfo", "-f", "null", "-"])
    return sorted(float(x) for x in re.findall(r"pts_time:(-?[\d.]+)", err) if float(x) > 0.0)


GUARD_MARGIN = 0.05   # seconds a range must stay inside a shot
STRETCH_WARN = 0.08   # warn when keeping the requested length takes more than 8% slowing


def guard_range(cuts: list[float], start: float, end: float, clip_dur: float,
                margin: float = GUARD_MARGIN) -> tuple[float, float, float | None]:
    """Keep [start, end) inside one shot of a clip whose internal hard cuts are `cuts`.

    Returns (start, end, cut): unchanged with cut=None when the range stays clear of every cut by
    `margin`; otherwise the longest piece of the range that sits at least `margin` inside one shot
    (the earlier one on a tie) and the first cut that forced it.
    """
    hit = next((c for c in cuts if start - margin < c < end + margin), None)
    if hit is None:
        return start, end, None
    edges = [0.0] + [c for c in cuts if 0 < c < clip_dur] + [max(clip_dur, end)]
    best = None
    for i in range(len(edges) - 1):
        lo = max(start, edges[i] + (margin if i > 0 else 0.0))
        hi = min(end, edges[i + 1] - (margin if i < len(edges) - 2 else 0.0))
        if hi - lo > 1e-6 and (best is None or hi - lo > best[1] - best[0] + 1e-6):
            best = (lo, hi)
    if best is None:  # the range sits in a sliver narrower than the margins: nothing safe to take
        return start, end, hit
    return best[0], best[1], hit


def frame_counts(durations: list[float], fps: float) -> list[int]:
    """Whole frames per event from cumulative rounded boundaries, round(t * fps).

    Rounding each event on its own lets errors pile up (ten 0.52 s events at 24 fps would each
    round down to 12 frames and the cut would end 0.5 s early); rounding the running total puts
    every cut on the frame it was asked for, and the pieces always add up to the total.
    """
    out, t, prev = [], 0.0, 0
    for d in durations:
        t += d
        bound = max(int(math.floor(t * fps + 0.5 + 1e-9)), prev + 1)
        out.append(bound - prev)
        prev = bound
    return out


def plan(prod: Production, events: list[tuple[str, float | None, float | None]], trim: float = 0.1,
         guard: float | None = None) -> list[dict]:
    """Where each cut.txt event comes from and how many whole frames it lasts in the cut.

    `assemble` builds the cut from this plan and `review` finds the joins with it, so the two agree.
    trim: seconds shaved off the head and tail of whole takes (generation jitter lives there).
    guard: scene-change threshold; when set, clip ranges are kept inside one shot (see guard_range)
    and the event carries `stretch` (slow-down to keep its length), `src_len` and `notes`.
    """
    fps = prod.fps
    out, durs, cache = [], [], {}
    for src, a, b in events:
        ev = {"src": src, "path": None, "start": 0.0, "kind": "slate", "audio": False, "stretch": 1.0, "notes": []}
        if src.lower() == "slate":
            dur = a or 1.0
        else:
            ev["path"] = path = _resolve(prod, src)
            if path.suffix.lower() in IMAGE_EXT:
                ev["kind"] = "still"
                dur = (b - a) if (a is not None and b is not None) else (a or 2.0)
            else:
                info = ff.probe(path)
                start = a if a is not None else trim
                end = b if b is not None else max(info["duration"] - trim, start + 0.1)
                ev.update(kind="clip", start=start, audio=info["has_audio"])
                dur = end - start
                if guard is not None:
                    if path not in cache:
                        cache[path] = shot_cuts(path, guard)
                    s2, e2, cut = guard_range(cache[path], start, end, info["duration"])
                    if cut is not None and (s2, e2) == (start, end):
                        ev["notes"].append(f"{src}: a cut at {cut:.2f}s sits in a shot too short to avoid it; "
                                           "check the join for a frame of the other shot")
                    elif cut is not None:
                        k = dur / (e2 - s2)
                        ev.update(start=s2, src_len=e2 - s2, stretch=k, guarded=True)
                        msg = (f"{src}: {start:.2f}-{end:.2f} crosses a cut at {cut:.2f}s; kept {s2:.2f}-{e2:.2f} "
                               f"and slowed {100 * (k - 1):.0f}% to hold the length")
                        ev["notes"].append(("warning: " + msg + f" (over {STRETCH_WARN:.0%}: choose a range inside one shot)")
                                           if k - 1 > STRETCH_WARN else "shot guard: " + msg)
        durs.append(dur)
        ev["whole"] = ev["kind"] == "clip" and a is None
        out.append(ev)
    for ev, n in zip(out, frame_counts(durs, fps)):
        ev["frames"] = n
    return out


def assemble(prod: Production, edl_path: Path | None = None, trim: float = 0.1,
             fit: str = "crop", fade_ms: int = 30, guard: float | None = 0.3) -> Path:
    """Rough cut from cut.txt: conform every event to the production frame, then join.

    Every event gets a short audio fade in/out so joins don't click. A copy of the cut list is
    saved beside the cut (cut_v004.txt), so every version keeps the list that made it.

    Shot guard (on by default, `guard` = scene threshold, None to switch off): a range that
    crosses or comes within 0.05 s of a hard cut inside its source clip is pulled back inside the
    shot and slowed slightly to keep its length. Event lengths are cumulative-rounded frame counts,
    so every cut lands on the frame the cut list asked for.
    """
    edl_path = edl_path or prod.dir("edit") / "cut.txt"
    if not edl_path.exists():
        edl_path.parent.mkdir(parents=True, exist_ok=True)
        edl_path.write_text(EDL_HELP)
        die(f"wrote an empty {prod.rel(edl_path)}: list your takes in it, then run assemble again")
    edl_text = edl_path.read_text(encoding="utf-8")
    events = parse_edl(edl_text)
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
        for i, ev in enumerate(plan(prod, events, trim, guard)):
            for note in ev["notes"]:
                print(note, file=sys.stderr)
            seg = Path(tmp) / f"ev{i:03d}.mkv"
            frames = ev["frames"]
            dur = frames / fps
            if ev["kind"] == "slate":
                inputs = ["-f", "lavfi", "-t", f"{dur + 1}", "-i", f"color=c=black:s={w}x{h}:r={fps}"]
            elif ev["kind"] == "still":
                inputs = ["-loop", "1", "-t", f"{dur + 1}", "-i", ev["path"]]
            elif ev.get("guarded"):  # read exactly the safe range: nothing past it can leak in
                inputs = ["-ss", f"{ev['start']:.6f}", "-t", f"{ev['src_len']:.6f}", "-i", ev["path"]]
            else:
                inputs = ["-ss", f"{ev['start']}", "-t", f"{dur + 1}", "-i", ev["path"]]
            # Restart every event's clock at zero: after a seek the first frame can sit part of a frame
            # late, and the fps filter would round that into a one-frame hole at the join.
            vf = "setpts=PTS-STARTPTS," + (f"setpts=PTS*{ev['stretch']:.6f}," if ev["stretch"] != 1.0 else "") \
                + ff.fit_filter(w, h, fps, fit) + (",tpad=stop_mode=clone:stop=-1" if ev.get("guarded") else "")
            if ev["audio"]:
                audio_in, amap = [], "0:a:0"
            else:
                audio_in, amap = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"], "1:a"
            slow = f"atempo={1 / ev['stretch']:.6f}," if 0.5 <= 1 / ev["stretch"] < 0.9999 else ""
            af = (f"asetpts=PTS-STARTPTS,{slow}aresample=48000,aformat=channel_layouts=stereo,atrim=duration={dur:.6f},"
                  f"apad=whole_dur={dur:.6f},afade=t=in:d={fade},afade=t=out:st={max(dur - fade, 0):.4f}:d={fade}")
            ff.run([*inputs, *audio_in, "-map", "0:v:0", "-map", amap, "-vf", vf, "-af", af,
                    "-frames:v", str(frames), *ff.VIDEO_OUT[:-2], "-c:a", "pcm_s16le", "-t", f"{dur:.6f}", seg])
            parts.append(seg)
        concat = Path(tmp) / "list.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts))
        ff.run(["-f", "concat", "-safe", "0", "-i", concat, "-c:v", "copy", *ff.AUDIO_OUT,
                "-movflags", "+faststart", out])
    out.with_suffix(".txt").write_text(
        f"# {out.name} from {edl_path.name}: film assemble --trim {trim} --fit {fit}\n{edl_text}", encoding="utf-8")
    return out
