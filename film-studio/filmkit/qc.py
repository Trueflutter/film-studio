"""QC: the machine checks (spec, loudness, dead frames, dead air) plus the human rubric."""
from __future__ import annotations

import re
from pathlib import Path

from . import ff
from .core import ASPECTS, Production, today

# The creative rubric lives in handbook/14-qc-and-delivery.md; this is the scoring sheet it refers to.
RUBRIC = [
    ("Story", "Does every shot do a job? Is the point/turn/payoff clear without explanation?"),
    ("Emotion", "Does the key moment land? Performance + camera + sound pulling the same way?"),
    ("Realism", "Skin, light, texture, lens, motion weight. Would a first-time viewer clock AI?"),
    ("Continuity", "Face, wardrobe, props, light direction, screen direction, geography across cuts."),
    ("Composition", "Deliberate frames: eyelines, headroom, depth, negative space, no default centring."),
    ("Motion & physics", "Weight, contact, cloth, liquid, speed. Camera motivated, not floaty."),
    ("Faces & anatomy", "Stable eyes/teeth/hands, no morphing, no dead stare, no extra fingers."),
    ("Lip sync & voice", "Phonemes land, voice fits face/age/space, no robotic cadence."),
    ("Sound", "Dialogue clear, room tone present, foley at contact points, music serves not smothers."),
    ("Edit & pacing", "Cuts motivated, no same-size jumps, weak frames hidden, rhythm varies."),
    ("Artefacts & text", "No garbled text/UI, flicker, melting, ghost extras, compression mush."),
    ("Brand / brief fit", "Delivers the brief: audience, message, tone, CTA, mandatories, legal."),
]

SPECS = {
    "social": {"lufs": -14.0, "tp": -1.0},
    "web": {"lufs": -16.0, "tp": -1.0},
    "broadcast": {"lufs": -23.0, "tp": -2.0},
    "cinema-ish": {"lufs": -24.0, "tp": -2.0},
}


def _row(status: str, check: str, detail: str) -> str:
    return f"| {status} | {check} | {detail} |"


def qc(prod: Production, file: Path, spec: str | None = None) -> Path:
    file = Path(file)
    info = ff.probe(file)
    cfg = prod.cfg
    rows = []
    fails = warns = 0

    def add(ok: bool | None, check: str, detail: str) -> None:
        nonlocal fails, warns
        status = "PASS" if ok else ("WARN" if ok is None else "FAIL")
        fails += status == "FAIL"
        warns += status == "WARN"
        rows.append(_row(status, check, detail))

    w, h = prod.size
    size = f"{info['width']}x{info['height']} (production {w}x{h})"
    if (info["width"], info["height"]) == (w, h):
        add(True, "Frame size", size)
    elif info["width"] * h == info["height"] * w:
        add(None, "Frame size", size + ": same aspect, different resolution")
    elif (info["width"], info["height"]) in ASPECTS.values():
        add(True, "Frame size", size + ": a standard deliverable variant")
    else:
        add(False, "Frame size", size + ": non-standard size and aspect")
    add(abs(info["fps"] - prod.fps) < 0.05 or None, "Frame rate", f"{info['fps']} fps (production {prod.fps})")
    target = float(cfg.get("target_duration_s") or 0)
    if target:
        off = abs(info["duration"] - target) / target
        add(True if off <= 0.1 else None, "Duration", f"{info['duration']:.2f}s (target {target:.0f}s)")
    add(info["has_audio"] or None, "Audio track", "present" if info["has_audio"] else "MISSING: silent file")

    if info["has_audio"]:
        s = SPECS.get(spec or "", {"lufs": float(cfg.get("loudness_lufs", -14)), "tp": -1.0})
        loud = ff.loudness(file)
        if loud["lufs"] is not None:
            add(abs(loud["lufs"] - s["lufs"]) <= 1.0, "Loudness",
                f"{loud['lufs']:.1f} LUFS integrated (spec {s['lufs']:.0f} ±1)")
        if loud["true_peak"] is not None:
            add(loud["true_peak"] <= s["tp"], "True peak", f"{loud['true_peak']:.1f} dBTP (max {s['tp']:.0f})")
        if loud["lra"] is not None:
            add(True if loud["lra"] <= 15 else None, "Loudness range", f"{loud['lra']:.1f} LU")
        silences = [sp for sp in ff.detect(file, af="silencedetect=n=-50dB:d=1.5")]
        add(None if silences else True, "Dead air (>1.5s below -50 dB)",
            ", ".join(f"{a:.1f}-{b:.1f}s" if b >= 0 else f"{a:.1f}s-end" for a, b in silences) or "none")

    blacks = ff.detect(file, vf="blackdetect=d=0.25:pix_th=0.10")
    inner = [b for b in blacks if b[0] > 0.05 and b[1] < info["duration"] - 0.05]
    add(None if inner else True, "Black frames mid-programme",
        ", ".join(f"{a:.2f}-{b:.2f}s" for a, b in inner) or "none" + (" (head/tail black is fine)" if blacks else ""))
    freezes = ff.detect(file, vf="freezedetect=n=0.003:d=0.8")
    add(None if freezes else True, "Frozen picture (>0.8s)",
        ", ".join(f"{a:.2f}-{b:.2f}s" if b >= 0 else f"{a:.2f}s-end" for a, b in freezes) or "none")

    out = prod.dir("delivery") / "qc" / f"{file.stem}_qc_{today()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    verdict = "FAIL" if fails else ("PASS with warnings" if warns else "PASS")
    lines = [
        f"# QC: {file.name}", "",
        f"Production: {cfg['title']} · checked {today()} · technical verdict: **{verdict}**", "",
        "## 1. Technical (machine)", "", "| | check | result |", "|---|---|---|", *rows, "",
        "WARN = look at it and decide; intentional choices (a held freeze, a silent beat) are fine.", "",
        "## 2. Creative (human)", "",
        "Score 1-5. Anything under 3 gets a timecode, a diagnosis code "
        "(see handbook/12-diagnosis-and-iteration.md) and a fix.", "",
        "| area | question | score | timecodes / notes | fix |", "|---|---|---|---|---|",
        *[f"| {a} | {q} |  |  |  |" for a, q in RUBRIC], "",
        "## 3. Viewing protocol", "",
        "- [ ] Watched once full screen with sound, no stopping (gut reaction noted first)",
        "- [ ] Watched once muted (does the picture tell the story?)",
        "- [ ] Listened once with eyes closed (does the sound tell the story?)",
        "- [ ] Watched on a phone at arm's length (captions, safe zones, legibility)",
        "- [ ] Scrubbed frame by frame through every cut point",
        "- [ ] Shown to one person who has not seen it: what did they think it was about?", "",
        "## 4. Decision", "", "- Ship / fix / re-cut:", "- Top 3 fixes, cheapest first:", "",
    ]
    out.write_text("\n".join(lines))
    return out


# --- subtitles ---------------------------------------------------------------

def parse_srt(text: str) -> list[tuple[float, float, str]]:
    def ts(s: str) -> float:
        h, m, rest = s.strip().replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(rest)
    cues = []
    for block in re.split(r"\n\s*\n", text.strip().replace("\r\n", "\n")):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        tline = next((i for i, ln in enumerate(lines) if "-->" in ln), None)
        if tline is None:
            continue
        a, b = lines[tline].split("-->")
        cues.append((ts(a), ts(b.split()[0]), "\n".join(lines[tline + 1:])))
    return cues


def check_subs(srt: Path, max_cps: float = 17.0, max_chars: int = 42, max_lines: int = 2,
               min_dur: float = 0.83, max_dur: float = 7.0, min_gap: float = 0.083) -> str:
    """Readability checks, based on common broadcast/streaming subtitle guidance."""
    cues = parse_srt(Path(srt).read_text(encoding="utf-8"))
    if not cues:
        return "no cues found"
    issues = []
    for n, (a, b, text) in enumerate(cues, 1):
        lines = text.splitlines()
        dur = b - a
        chars = len(" ".join(lines))
        if dur <= 0:
            issues.append(f"#{n} {a:.2f}s: end is not after start")
            continue
        if dur < min_dur:
            issues.append(f"#{n} {a:.2f}s: on screen {dur:.2f}s (< {min_dur}s)")
        if dur > max_dur:
            issues.append(f"#{n} {a:.2f}s: on screen {dur:.2f}s (> {max_dur}s)")
        if chars / dur > max_cps:
            issues.append(f"#{n} {a:.2f}s: {chars / dur:.1f} chars/sec (> {max_cps}): cut words or extend")
        if len(lines) > max_lines:
            issues.append(f"#{n} {a:.2f}s: {len(lines)} lines (> {max_lines})")
        for ln in lines:
            if len(ln) > max_chars:
                issues.append(f"#{n} {a:.2f}s: line of {len(ln)} chars (> {max_chars})")
        if n < len(cues):
            gap = cues[n][0] - b
            if gap < 0:
                issues.append(f"#{n}->{n + 1}: cues overlap by {-gap:.2f}s")
            elif 0 < gap < min_gap:
                issues.append(f"#{n}->{n + 1}: {gap * 1000:.0f}ms gap (flicker; close it or open to {min_gap}s)")
    head = f"{len(cues)} cues, {cues[-1][1]:.1f}s"
    return head + (": all readable" if not issues else f", {len(issues)} issue(s):\n  " + "\n  ".join(issues))
