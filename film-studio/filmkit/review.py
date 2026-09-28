"""Watching with frames: every join of a cut side by side, the rhythm in numbers, cuts against the
beat, and the same measurements for a reference film you want to learn from."""
from __future__ import annotations

import re
import statistics
import tempfile
from pathlib import Path

from . import ff
from .core import FilmError, Production, die
from .media import frames, parse_edl, plan

SHEET_W, SHEET_H = 1440, 1400  # kept under ~1500 px so an image model sees a sheet at full size
BG = "0x111111"
BURST, HOLD_MIN = 1.5, 3.0


def _layout(w: int, h: int, per_cell: int) -> tuple[int, int, int]:
    """(cells per row, frame width, rows per page) for frames of w x h, per_cell frames per cell."""
    cols = (3 if h > w else 2) * (2 // per_cell)
    fw = (SHEET_W // cols - 20 - 6 * (per_cell - 1)) // per_cell // 2 * 2
    fh = round(fw * h / w)
    return cols, fw, max(1, SHEET_H // (fh + 20))


def _pages(cells: list[Path], out_base: Path, cols: int, rows: int) -> list[Path]:
    """Tile same-sized images onto numbered pages: <out_base>_1.png, _2.png ..."""
    for old in out_base.parent.glob(f"{out_base.name}_[0-9]*.png"):
        old.unlink()
    pages = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, c in enumerate(cells):
            (Path(tmp) / f"c{i:04d}.png").write_bytes(c.read_bytes())
        per = cols * rows
        for n, start in enumerate(range(0, len(cells), per), 1):
            page = out_base.with_name(f"{out_base.name}_{n}.png")
            used = -(-min(per, len(cells) - start) // cols)  # a short last page gets only the rows it fills
            ff.run(["-framerate", "1", "-start_number", str(start), "-i", Path(tmp) / "c%04d.png",
                    "-vf", f"tile={cols}x{used}:color={BG}", "-frames:v", "1", "-update", "1", page])
            pages.append(page)
    return pages


def _frames_at(video: Path, indices: list[int], width: int, out_dir: Path) -> dict[int, Path]:
    """Exact frames by index in one decode pass (select counts decoded frames from 0)."""
    wanted = sorted(set(indices))
    expr = "+".join(f"eq(n\\,{i})" for i in wanted)
    ff.run(["-i", video, "-an", "-vf", f"select='{expr}',setpts=N/(FRAME_RATE*TB),scale={width}:-2",
            out_dir / "f%04d.png"])
    got = sorted(out_dir.glob("f[0-9][0-9][0-9][0-9].png"))
    if len(got) != len(wanted):
        die(f"expected {len(wanted)} frames from {video.name}, got {len(got)}: is it a cut made by film assemble?")
    return dict(zip(wanted, got))


def rhythm(lengths: list[float]) -> list[str]:
    """Shot lengths as a readable row, the summary numbers and the tells worth a warning."""
    if not lengths:
        return ["no shots"]
    med = statistics.median(lengths)
    hold = max(HOLD_MIN, 2 * med)
    row = " ".join(f"{x:.1f}" + ("H" if x >= hold else "b" if x < BURST else "") for x in lengths)
    longest = max(range(len(lengths)), key=lengths.__getitem__)
    lines = [f"  {row}   (seconds · H hold · b burst)",
             f"  {len(lengths)} shots · average {statistics.mean(lengths):.1f} s · median {med:.1f} s · "
             f"longest {lengths[longest]:.1f} s (shot {longest + 1}) · shortest {min(lengths):.1f} s"]
    if len(lengths) >= 4 and statistics.pstdev(lengths) / statistics.mean(lengths) < 0.25:
        lines.append("  ! lengths are nearly uniform: that reads as generated. Hold one moment, burst through another.")
    default = sum(1 for x in lengths if min(abs(x - 5), abs(x - 10)) <= 0.25)
    if default >= 2 and default >= len(lengths) / 4:
        lines.append(f"  ! {default} shots run at an engine's default length (about 5 or 10 s): trim to the best seconds.")
    return lines


def _beat(t: float, bpm: float, offset: float, fps: float) -> tuple[str, bool]:
    """Where a cut at t sits on the grid: ('beat 7 -2f', False). Beat 1 is at offset; every 4th is a downbeat."""
    beat = 60 / bpm
    k = round((t - offset) / beat)
    if k < 0:
        return "before the music", False
    off = round((t - offset - k * beat) * fps)
    where = "downbeat" if k % 4 == 0 else "beat"
    return f"{where} {k + 1} " + ("on" if abs(off) <= 1 else f"{off:+d}f"), abs(off) <= 1


def _cuts(prod: Production) -> list[Path]:
    folder = prod.dir("edit") / "cuts"
    found = [(int(m.group(1)), p) for p in folder.glob("cut_v*.mp4") if (m := re.fullmatch(r"cut_v(\d+)", p.stem))]
    return [p for _, p in sorted(found)]


def _detect(video: Path, dur: float, threshold: float) -> list[float]:
    """Times of hard cuts, found by picture change (the first frame of each new shot)."""
    err = ff.analyse(["-i", str(video), "-an", "-vf",
                      f"setpts=PTS-STARTPTS,scale=320:-2,select='gt(scene,{threshold})',showinfo", "-f", "null", "-"])
    cuts: list[float] = []
    for t in (float(x) for x in re.findall(r"pts_time:([\d.]+)", err)):
        if t - (cuts[-1] if cuts else 0.0) >= 0.15 and dur - t >= 0.15:  # a flash or a double trigger is not a shot
            cuts.append(t)
    return cuts


def review(prod: Production, cut: Path | None = None, edl: Path | None = None,
           bpm: float = 0.0, offset: float = 0.0, threshold: float = 0.3) -> str:
    """Sheets of every join (last frame out | first frame in), the rhythm, and flags for the joins
    most likely to break the transition rule. Claude reads the sheets; the director watches the cut.

    Joins come from the cut list that made the cut (exact). An editor export has no cut list, so its
    cuts are found by picture change instead."""
    cut = cut or (_cuts(prod) or [None])[-1]
    if cut is None:
        die("no cut yet: build one with `film assemble`")
    info = ff.probe(cut)
    snapshot = cut.with_suffix(".txt")
    listed = edl or (snapshot if snapshot.exists() else prod.dir("edit") / "cut.txt")
    events, notes = None, []
    if listed.exists():
        text = listed.read_text(encoding="utf-8")
        m = re.search(r"--trim ([\d.]+)", text.splitlines()[0] if text else "")
        try:
            events = plan(prod, parse_edl(text), float(m.group(1)) if m else 0.1) or None
        except FilmError:  # a take in the list has moved since: the picture still has the cuts
            if edl:
                raise
            events = None
        total = sum(ev["frames"] for ev in events or []) / prod.fps
        if events and abs(info["duration"] - total) > max(0.1, 2 / prod.fps):
            if edl:
                die(f"{prod.rel(edl)} lasts {total:.2f} s but {cut.name} lasts {info['duration']:.2f} s: "
                    "they don't match. Re-assemble, or pass the cut list that made it.")
            events = None
        elif events and listed != snapshot:
            notes.append(f"note: using {prod.rel(listed)}; no cut list was saved beside {cut.name}")
    if events:
        fps = prod.fps
        starts = [0]
        for ev in events:
            starts.append(starts[-1] + ev["frames"])
        names = [ev["src"] for ev in events]
        lengths = [ev["frames"] / fps for ev in events if ev["kind"] != "slate"]
        whole = sum(1 for ev in events if ev["whole"])
    else:
        notes.append(f"note: no cut list matches {cut.name} (an editor export?): cuts found by picture change, "
                     "so a dissolve or a soft cut can be missed")
        fps = info["fps"] or prod.fps
        starts = [0, *(round(t * fps) for t in _detect(cut, info["duration"], threshold)),
                  round(info["duration"] * fps)]
        names = [f"shot {i}" for i in range(1, len(starts))]
        lengths = [(b - a) / fps for a, b in zip(starts, starts[1:])]
        whole = 0

    takes = {t["take"].upper(): t for t in prod.takes()}
    shots = {s["shot"].upper(): s for s in prod.shots()}

    def shot_of(src: str) -> str:
        return takes.get(src.upper(), {}).get("shot", "").upper()

    def frame(src: str) -> tuple[str, str]:
        s = shots.get(shot_of(src), {})
        return s.get("size", "").strip(), s.get("angle", "").strip()

    lines, on_beat = [], 0
    for k in range(1, len(names)):
        a, b = names[k - 1], names[k]
        t = starts[k] / fps
        flag = ""
        if events and "slate" not in (a.lower(), b.lower()):
            if a.upper() == b.upper():
                flag = "same take twice: a jump cut unless it's a deliberate time cut"
            elif shot_of(a) and shot_of(a) == shot_of(b):
                flag = f"two takes of {shot_of(a)} back to back: same framing unless one is punched in"
            elif all(frame(a)) and [x.lower() for x in frame(a)] == [x.lower() for x in frame(b)]:
                flag = f"same size and angle in the shot list ({', '.join(frame(a))}): check the transition rule"
        beat = ""
        if bpm:
            where, on = _beat(t, bpm, offset, fps)
            beat, on_beat = f"  {where:<16}", on_beat + on
        lines.append(f"  J{k:02d}  {t:6.2f}s{beat}  {a} → {b}" + (f"   ! {flag}" if flag else ""))

    cols, fw, rows = _layout(info["width"] or prod.size[0], info["height"] or prod.size[1], 2)
    delivery = prod.dir("delivery")
    base = (delivery / "qc" if delivery.resolve() in cut.resolve().parents else cut.parent) / f"{cut.stem}_joins"
    base.parent.mkdir(parents=True, exist_ok=True)
    sheets = []
    if len(names) > 1:
        with tempfile.TemporaryDirectory() as tmp:
            picks = _frames_at(cut, [i for s in starts[1:-1] for i in (s - 1, s)], fw, Path(tmp))
            pairs = []
            for k, s in enumerate(starts[1:-1], 1):
                pair = Path(tmp) / f"pair{k:04d}.png"
                ff.run(["-i", picks[s - 1], "-i", picks[s], "-filter_complex",
                        f"[0]pad=iw+6:ih:0:0:{BG}[o];[o][1]hstack,pad=iw+20:ih+20:10:10:{BG}",
                        "-frames:v", "1", "-update", "1", pair])
                pairs.append(pair)
            sheets = _pages(pairs, base, cols, rows)

    unit = "events" if events else "shots"
    out = [f"Review of {prod.rel(cut)}: {len(names)} {unit}, {starts[-1] / fps:.2f} s at {fps:g} fps", *notes, ""]
    per = cols * rows
    if sheets:
        out.append("Sheets (each pair: last frame out | first frame in; left to right, top to bottom):")
        for n, sheet in enumerate(sheets):
            first, last = n * per + 1, min((n + 1) * per, len(names) - 1)
            out.append(f"  {prod.rel(sheet)}   J{first:02d}-J{last:02d}")
        out.append("")
    out += ["Rhythm:", *rhythm(lengths)]
    if whole:
        out.append(f"  ! {whole} event(s) use a whole take: most shots want only their best 1-3 seconds.")
    if bpm:
        out.append(f"  {on_beat} of {len(lines)} cuts within a frame of the beat ({bpm:g} BPM, first beat at {offset:g} s)")
    out += ["", "Joins:", *(lines or ["  one shot: no joins"]), "",
            "Look at every pair: same person at the same size and angle? An eyeline or a movement that flips "
            "direction? A jump in colour or light? Fix the three worst, then review again before the director watches."]
    return "\n".join(out)


def teardown(video: Path, out_dir: Path | None = None, threshold: float = 0.3) -> str:
    """Cut list, shot lengths and one frame per shot of a film you want to learn from."""
    info = ff.probe(video)
    if not info["has_video"]:
        die(f"{video} has no picture")
    dur = info["duration"]
    cuts = _detect(video, dur, threshold)
    bounds = [0.0, *cuts, dur]
    lengths = [b - a for a, b in zip(bounds, bounds[1:])]
    out_dir = out_dir or video.with_name(f"{video.stem}_teardown")
    out_dir.mkdir(parents=True, exist_ok=True)
    cols, fw, rows = _layout(info["width"] or 16, info["height"] or 9, 1)
    with tempfile.TemporaryDirectory() as tmp:
        stills = frames(video, Path(tmp), at=[(a + b) / 2 for a, b in zip(bounds, bounds[1:])], width=fw)
        cells = []
        for i, s in enumerate(stills):
            cell = Path(tmp) / f"cell{i:04d}.png"
            ff.run(["-i", s, "-vf", f"pad=iw+20:ih+20:10:10:{BG}", "-frames:v", "1", "-update", "1", cell])
            cells.append(cell)
        sheets = _pages(cells, out_dir / "shots", cols, rows)
    holds = sorted(range(len(lengths)), key=lengths.__getitem__, reverse=True)[:3]
    per = cols * rows
    report = [f"Teardown of {video.name}: {len(lengths)} shots in {dur:.1f} s "
              f"({len(cuts) / dur * 60:.0f} cuts a minute; scene threshold {threshold:g})", "",
              "Rhythm:", *rhythm(lengths),
              "  longest holds: " + ", ".join(f"shot {i + 1} at {bounds[i]:.1f} s ({lengths[i]:.1f} s)" for i in holds),
              "", "Sheets (one frame from the middle of each shot, in order):",
              *(f"  {s}   shots {n * per + 1}-{min((n + 1) * per, len(lengths))}" for n, s in enumerate(sheets)),
              "", "Cuts (s): " + " ".join(f"{t:.2f}" for t in cuts), "",
              "Detection finds hard cuts. Dissolves, whips and match cuts can be missed or split: check the sheets. "
              "Write the grammar up from them: shot sizes in order, how the camera moves, transitions, how text "
              "enters and leaves, where the holds fall. Take the grammar, never the content, and keep the "
              "reference file private."]
    text = "\n".join(report)
    (out_dir / "teardown.md").write_text(text + "\n", encoding="utf-8")
    return text
