"""Sound: mixing (dialogue first, music under it, beds and cues, loudness to spec), tightening a
voice-over for pace, and aligning a music bed so its payoff lands on a chosen moment.

Only ffmpeg is needed. The signal work in `bed_align` is plain Python over short PCM arrays.
"""
from __future__ import annotations

import array
import itertools
import json
import math
import operator
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

from . import ff
from .core import Production, die


def _prep(idx: int) -> str:
    return f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo"


def parse_placed(item: str) -> tuple[str, float]:
    """'sfx/door.wav@12.4' -> ('sfx/door.wav', 12.4): place a stem at a time in the cut."""
    if "@" in item:
        path, _, at = item.rpartition("@")
        try:
            return path, float(at)
        except ValueError:
            pass
    return item, 0.0


def parse_lift(item: str) -> tuple[float, float]:
    """'30.5:-12' -> (30.5, -12.0): at 30.5 s the music rises to -12 dB."""
    t, sep, db = item.partition(":")
    try:
        if not sep:
            raise ValueError
        return float(t), float(db)
    except ValueError:
        die(f"--lift expects <seconds>:<db>, e.g. 30.5:-12, got '{item}'")
    raise AssertionError


BED_SPEC = re.compile(r"^(?P<file>.+)@(?P<a>\d+(?:\.\d+)?)-(?P<b>\d+(?:\.\d+)?)(?::(?P<db>-?\d+(?:\.\d+)?))?$")


def parse_bed(item: str, default_db: float = -24.0) -> tuple[str, float, float, float]:
    """'rain.wav@4-20:-26' -> ('rain.wav', 4.0, 20.0, -26.0): a looped ambience bed from 4 s to 20 s."""
    m = BED_SPEC.match(item)
    if not m or float(m["b"]) <= float(m["a"]):
        die(f"--amb expects <file>@<start>-<end>:<db> (db optional), e.g. rain.wav@4-20:-26, got '{item}'")
    return m["file"], float(m["a"]), float(m["b"]), float(m["db"]) if m["db"] is not None else default_db


def load_cues(path: Path, resolve=lambda p: Path(p)) -> list[dict]:
    """cues.json: [{"file": "sfx/hit.wav", "at": 12.4, "db": -6, "max": 1.5}, ...].
    at = seconds into the cut; db = gain on the file (default 0); max = trim to this many seconds."""
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        die(f"{path}: can't read the cue list ({e})")
    if not isinstance(raw, list):
        die(f"{path}: expected a list of cues like " + '{"file": "sfx/hit.wav", "at": 12.4, "db": -6}')
    cues = []
    for i, c in enumerate(raw, 1):
        if not isinstance(c, dict) or "file" not in c or "at" not in c:
            die(f"{path}: cue {i} needs at least \"file\" and \"at\"")
        cues.append({"file": resolve(c["file"]), "at": float(c["at"]), "db": float(c.get("db", 0.0)),
                     "max": float(c["max"]) if c.get("max") else None})
    return cues


def mix(prod: Production, video: Path | None = None, dialogue: Path | None = None,
        music: Path | None = None, ambience: list | None = None, fx: list | None = None,
        music_db: float = -18.0, ambience_db: float = -24.0, target: float | None = None,
        use_video_audio: bool = True, duck_db: float | None = None, lifts: list | None = None,
        cues: list | None = None, beds: list | None = None, fade_out: float = 0.0,
        true_peak: float = -1.0) -> Path:
    """Build a mix and (if a video is given) lay it onto the picture without re-encoding it.

    Dialogue is loudness-normalised first (-16 LUFS). By default music sits at `music_db` and ducks
    under the dialogue via sidechain compression; ambience beds sit low; effects play at level.

    Fixed-level mode (`duck_db` or `lifts` given): the music is first gain-matched to the dialogue's
    loudness, then held at `duck_db` (dB under the dialogue, e.g. -21) for the whole cut, and each
    lift (seconds, dB) ramps it to that level over 0.3 s, e.g. into a chorus or a sting.
    `cues` place sound effects at exact times ({file, at, db, max}); `beds` are looped ambience
    (file, start, end, db) with 0.3 s fades; `fade_out` fades the whole mix out at the end.
    The finished mix is gain-matched to the delivery loudness (default: production.json
    loudness_lufs) with the true peak held under `true_peak` dBTP.
    """
    # ambience/fx items are Paths or (Path, start seconds) pairs
    ambience = [a if isinstance(a, tuple) else (a, 0.0) for a in ambience or []]
    fx = [f if isinstance(f, tuple) else (f, 0.0) for f in fx or []]
    cues, beds = list(cues or []), list(beds or [])
    lifts = sorted(lifts or [])
    fixed = duck_db is not None or bool(lifts)
    target = target if target is not None else float(prod.cfg.get("loudness_lufs", -14))
    inputs: list = []
    count = 0

    def add(path, loop: bool = False) -> int:
        nonlocal count
        inputs.extend((["-stream_loop", "-1"] if loop else []) + ["-i", path])
        count += 1
        return count - 1

    dia_idx = mus_idx = None
    if video:
        add(video)
        if dialogue is None and use_video_audio and ff.probe(video)["has_audio"]:
            dia_idx = 0
    if dialogue:
        dia_idx = add(dialogue)
    if music:
        mus_idx = add(music)
    amb_idx = [(add(a), at) for a, at in ambience]
    fx_idx = [(add(f), at) for f, at in fx]
    cue_idx = [(add(c["file"]), c) for c in cues]
    bed_idx = [(add(f, loop=True), a, b, db) for f, a, b, db in beds]
    if dia_idx is None and mus_idx is None and not (amb_idx or fx_idx or cue_idx or bed_idx):
        die("nothing to mix: pass --dialogue/--music/--ambience/--fx/--cues/--amb or a --video with audio")
    if lifts and mus_idx is None:
        die("--lift needs --music")

    ref = video or dialogue or music or (ambience[0][0] if ambience else fx[0][0] if fx else None)
    if ref:
        dur = ff.probe(ref)["duration"]
    elif bed_idx:
        dur = max(b for _, _, b, _ in bed_idx)
    else:
        dur = max(c["at"] + min(c["max"] or 1e9, ff.probe(c["file"])["duration"]) for c in cues)
    if not dur:
        die(f"can't read the duration of {ref}")

    chains, labels = [], []
    if dia_idx is not None:
        split = "asplit=2[dia][key]" if mus_idx is not None and not fixed else "anull[dia]"
        chains.append(f"{_prep(dia_idx)},loudnorm=I=-16:TP=-1.5:LRA=11,{split}")
        labels.append("[dia]")
    if mus_idx is not None:
        tail = "" if fade_out else f",afade=t=out:st={max(dur - 2.0, 0):.2f}:d=2"  # --fade-out takes over the ending
        if fixed:
            # Match the music to the dialogue's loudness so "-21" means 21 dB under the voice.
            lufs = ff.loudness(music)["lufs"]
            if lufs is None or lufs == float("-inf"):
                die(f"{music} is silent")
            base = duck_db if duck_db is not None else music_db
            gain = lambda db: 10 ** (db / 20)
            expr, prev = f"{gain(base):.5f}", gain(base)
            for t, db in lifts:
                expr += f"+({gain(db) - prev:.5f})*clip((t-{t:.3f})/0.3,0,1)"
                prev = gain(db)
            chains.append(f"{_prep(mus_idx)},volume={-16 - lufs:.2f}dB,volume='{expr}':eval=frame,"
                          f"afade=t=in:d=1.5{tail}[mus]")
            labels.append("[mus]")
        else:
            chains.append(f"{_prep(mus_idx)},volume={music_db}dB,afade=t=in:d=1.5{tail}[mus]")
            if dia_idx is not None:
                # The studio recipe: ~-26 dB threshold, hard ratio, fast attack, natural release.
                chains.append("[mus][key]sidechaincompress=threshold=0.05:ratio=8:attack=20:"
                              "release=500:makeup=1[mduck]")
                labels.append("[mduck]")
            else:
                labels.append("[mus]")

    def delay(at: float) -> str:
        return f",adelay={int(round(at * 1000))}:all=1" if at > 0 else ""

    for n, (i, at) in enumerate(amb_idx):
        chains.append(f"{_prep(i)},volume={ambience_db}dB{delay(at)}[amb{n}]")
        labels.append(f"[amb{n}]")
    for n, (i, at) in enumerate(fx_idx):
        chains.append(f"{_prep(i)}{delay(at)}[fx{n}]")
        labels.append(f"[fx{n}]")
    for n, (i, c) in enumerate(cue_idx):
        trim = ""
        if c["max"] and c["max"] < ff.probe(c["file"])["duration"]:  # cut short: close it with a quick fade
            f = min(0.03, c["max"] / 2)
            trim = f",atrim=duration={c['max']:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={c['max'] - f:.3f}:d={f}"
        chains.append(f"{_prep(i)}{trim},volume={c['db']}dB{delay(c['at'])}[cue{n}]")
        labels.append(f"[cue{n}]")
    for n, (i, a, b, db) in enumerate(bed_idx):
        span = b - a
        f = min(0.3, span / 2)
        chains.append(f"{_prep(i)},atrim=duration={span:.3f},asetpts=PTS-STARTPTS,volume={db}dB,"
                      f"afade=t=in:d={f},afade=t=out:st={span - f:.3f}:d={f}{delay(a)}[bed{n}]")
        labels.append(f"[bed{n}]")
    # normalize=0 keeps each stem at the level we set instead of dividing by the input count.
    ending = f",afade=t=out:st={max(dur - fade_out, 0):.3f}:d={min(fade_out, dur):.3f}" if fade_out else ""
    chains.append(f"{''.join(labels)}amix=inputs={len(labels)}:duration=longest:normalize=0,"
                  f"atrim=duration={dur:.3f},apad=whole_dur={dur:.3f}{ending}[pre]")

    out_wav = prod.next_version(prod.dir("sound") / "mix", "mix", ".wav")
    with tempfile.TemporaryDirectory() as tmp:
        pre = Path(tmp) / "pre.wav"
        ff.run([*inputs, "-filter_complex", ";".join(chains), "-map", "[pre]", "-ar", "48000", pre])
        got = match_loudness(pre, out_wav, target, true_peak=true_peak)
    print(f"mix: {got['lufs']:.1f} LUFS (target {target:g}), true peak {got['true_peak']:.1f} dBTP", file=sys.stderr)
    if not video:
        return out_wav
    out_mp4 = prod.next_version(Path(video).parent, Path(video).stem.split("_mix")[0] + "_mix", ".mp4")
    ff.run(["-i", video, "-i", out_wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
            *ff.AUDIO_OUT, "-shortest", out_mp4])
    return out_mp4


def match_loudness(src: Path, dest: Path, target: float, ceiling_db: float = -1.5,
                   tolerance: float = 0.3, passes: int = 4, true_peak: float | None = None) -> dict:
    """Linear gain + true-peak limiter, re-measured until within tolerance of target.

    Gain (not single-pass loudnorm) keeps the mix's dynamics intact; the limiter catches peaks.
    The limiter works on sample peaks, so the ceiling sits 0.5 dB under the -1 dBTP spec to
    leave room for inter-sample (true) peaks. With `true_peak` set, the result is measured and the
    ceiling lowered until the true peak is under it (loudness gives way before the peak does).
    """
    if true_peak is not None:
        ceiling_db = true_peak - 0.5
    gain = 0.0
    measured = ff.loudness(src)
    if measured["lufs"] is None or measured["lufs"] == float("-inf"):
        die(f"{src} is silent: nothing to normalise")

    def render() -> dict:
        limit = 10 ** (ceiling_db / 20)
        ff.run(["-i", src, "-af", f"volume={gain:.2f}dB,alimiter=limit={limit:.4f}:level=disabled",
                "-ar", "48000", dest])
        return ff.loudness(dest)

    for _ in range(passes):
        gain += target - measured["lufs"]
        measured = render()
        if measured["lufs"] is not None and abs(measured["lufs"] - target) <= tolerance:
            break
    for _ in range(3):
        tp = measured["true_peak"]
        if true_peak is None or tp is None or tp <= true_peak + 0.05:
            break
        ceiling_db -= (tp - true_peak) + 0.1
        measured = render()
    return measured


# --- PCM helpers (stdlib only) ------------------------------------------------

def _pcm(path: Path, rate: int, channels: int) -> array.array:
    """Decode any audio file to signed 16-bit samples (interleaved when stereo)."""
    cmd = [ff.ffmpeg_bin(), "-nostdin", "-hide_banner", "-loglevel", "error", "-i", str(path), "-vn",
           "-ac", str(channels), "-ar", str(rate), "-f", "s16le", "-"]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0:
        die(f"ffmpeg failed reading {path}:\n" + res.stderr.decode(errors="replace")[-400:])
    out = array.array("h")
    out.frombytes(res.stdout[: len(res.stdout) // 2 * 2])
    if sys.byteorder == "big":
        out.byteswap()
    return out


def _write_wav(path: Path, samples: array.array, rate: int, channels: int) -> None:
    data = array.array("h", samples)
    if sys.byteorder == "big":
        data.byteswap()
    with wave.open(str(path), "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(data.tobytes())


def _clip16(v: float) -> int:
    return max(-32768, min(32767, int(round(v))))


# --- voice tighten ---------------------------------------------------------------

def speech_chunks(words: list[dict], total: float, split: float = 0.28, pre: float = 0.04,
                  post: float = 0.07) -> list[tuple[float, float]]:
    """(start, end) of each stretch of speech: words closer than `split` seconds belong together;
    each chunk runs from `pre` before its first word to `post` after its last."""
    groups: list[list[dict]] = []
    for w in words:
        if groups and w["start"] - groups[-1][-1]["end"] <= split:
            groups[-1].append(w)
        else:
            groups.append([w])
    spans: list[tuple[float, float]] = []
    for g in groups:
        a = max(0.0, g[0]["start"] - pre)
        b = min(total, g[-1]["end"] + post)
        if spans:
            a = max(a, spans[-1][1])
        if b > a:
            spans.append((a, b))
    return spans


def tighten(src: Path, words: list[dict], out: Path | None = None, gap: float = 0.2, tempo: float = 1.15,
            split: float = 0.28, pre: float = 0.04, post: float = 0.07) -> dict:
    """A brisker voice-over: keep the speech, shorten every pause to `gap`, then speed up by `tempo`.

    Speech is cut into chunks wherever the silence between words exceeds `split`; the chunks are
    rejoined with `gap` seconds of silence (8 ms fades hide the cut), then ffmpeg's atempo speeds
    the whole thing up with the pitch preserved. Output is mono 48 kHz. Returns the numbers.
    """
    if not words:
        die("no words to tighten around: the transcript is empty")
    if not 0.5 <= tempo <= 2.0:
        die("--tempo must be between 0.5 and 2.0 (1.15 is a brisk news read)")
    rate = 48000
    x = _pcm(src, rate, 1)
    total = len(x) / rate
    spans = speech_chunks(words, total, split, pre, post)
    if not spans:
        die("no speech found inside the audio: do the word times belong to this file?")
    fade = int(0.008 * rate)
    body = array.array("h")
    silence = array.array("h", bytes(2 * int(round(gap * rate))))
    for n, (a, b) in enumerate(spans):
        piece = x[int(round(a * rate)):int(round(b * rate))]
        f = min(fade, len(piece) // 2)
        for k in range(f):
            g = k / f
            piece[k] = _clip16(piece[k] * g)
            piece[len(piece) - 1 - k] = _clip16(piece[len(piece) - 1 - k] * g)
        if n:
            body.extend(silence)
        body.extend(piece)
    out = Path(out) if out else Path(src).with_name(Path(src).stem + "_tight.wav")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "joined.wav"
        _write_wav(raw, body, rate, 1)
        ff.run(["-i", raw, "-af", f"atempo={tempo:.4f}", "-ar", rate, *(["-q:a", "2"] if out.suffix.lower() == ".mp3" else []), out])
    new = ff.probe(out)["duration"]
    return {"out": out, "old": total, "new": new, "words": len(words), "chunks": len(spans),
            "old_wps": len(words) / total, "new_wps": len(words) / new if new else 0.0}


def tighten_report(r: dict) -> str:
    return (f"{r['out']}\n{r['chunks']} chunks of speech · {r['old']:.2f}s → {r['new']:.2f}s "
            f"({100 * (r['new'] / r['old'] - 1):+.0f}%) · {r['old_wps']:.2f} → {r['new_wps']:.2f} words/sec")


# --- music bed alignment -------------------------------------------------------

HZ = 4000          # analysis rate for the search
STEP = 40          # candidate splice points every 10 ms at 4 kHz
WINDOW = HZ        # 1 s correlation window
XFADE = 0.015      # equal-gain crossfade at each splice (seconds)


def _energy(x: array.array) -> list:
    return list(itertools.accumulate(map(operator.mul, x, x), initial=0))


def _corr(x: array.array, ps: list, i: int, j: int, n: int = WINDOW) -> float:
    """Normalised correlation of x[i:i+n] with x[j:j+n] (1 = identical shape, 0 = unrelated)."""
    if i < 0 or j < 0 or i + n > len(x) or j + n > len(x):
        return -1.0
    ea, eb = ps[i + n] - ps[i], ps[j + n] - ps[j]
    if ea <= 0 or eb <= 0:
        return 0.0
    return sum(map(operator.mul, x[i:i + n], x[j:j + n])) / math.sqrt(ea * eb)


def estimate_bpm(x: array.array, lo: float = 70.0, hi: float = 180.0) -> tuple[float, float]:
    """Tempo from the autocorrelation of the onset envelope: how well the track repeats at
    1, 2 ... 8 beats at each candidate tempo. Returns (bpm, confidence); confidence is the
    winning score over the median score (about 1 means no clear pulse)."""
    hop = 40  # 10 ms
    env = [sum(map(abs, x[i:i + hop])) for i in range(0, len(x) - hop, hop)]
    if len(env) < 600:
        die("the track is too short to estimate a tempo: pass --bpm")
    onset = [max(0.0, b - a) for a, b in zip(env, env[1:])]
    mean = sum(onset) / len(onset)
    onset = [o - mean for o in onset]
    n = len(onset)
    beats = 8
    max_lag = int(beats * 6000 / lo) + 2
    ac = []
    for lag in range(max_lag + 1):
        ac.append(sum(map(operator.mul, onset[:n - lag], onset[lag:])) / (n - lag) if lag < n else 0.0)
    scores = []
    for tenth in range(int(lo * 10), int(hi * 10) + 1):
        bpm = tenth / 10
        beat = 6000 / bpm  # beat length in 10 ms frames
        score = 0.0
        for k in range(1, beats + 1):
            pos = k * beat
            i = int(pos)
            frac = pos - i
            score += ac[i] * (1 - frac) + ac[min(i + 1, max_lag)] * frac
        scores.append((score, bpm))
    best = max(scores)
    ordered = sorted(s for s, _ in scores)
    median = ordered[len(ordered) // 2]
    conf = 0.0 if best[0] <= 0 else best[0] / median if median > 0 else float("inf")
    return best[1], conf


def find_loop(x: array.array, ps: list, lengths: list[int], limit: int) -> list[dict]:
    """For each loop length (samples at 4 kHz) the splice point p (before `limit`) where the second
    after p matches the second after p - length best. Coarse 10 ms search, then 0.25 ms refinement
    of the length and the point. Best first; on a near tie (within 0.01) the longer loop wins."""
    found = []
    for L0 in lengths:
        lo, hi = L0, limit - WINDOW
        if hi <= lo:
            continue
        score, p = max((_corr(x, ps, q, q - L0), q) for q in range(lo, hi + 1, STEP))
        L = L0
        for dl in range(-60, 61):  # tempo estimates are never exact: tune the length to the audio
            c = _corr(x, ps, p, p - (L0 + dl))
            if c > score:
                score, L = c, L0 + dl
        best_p = p
        for dp in range(-STEP, STEP + 1):
            q = p + dp
            if q - L >= 0 and q <= hi:
                c = _corr(x, ps, q, q - L)
                if c > score:
                    score, best_p = c, q
        found.append({"length": L, "point": best_p, "score": score})
    if not found:
        return []
    top = max(d["score"] for d in found)
    winner = max((d for d in found if d["score"] >= top - 0.01), key=lambda d: d["length"])
    return [winner] + sorted((d for d in found if d is not winner), key=lambda d: -d["score"])


def _blend(a: array.array, b: array.array) -> array.array:
    """Equal-gain crossfade: a fades out while b fades in (same length, interleaved ok)."""
    n = len(a)
    return array.array("h", (_clip16(a[i] * (1 - i / n) + b[i] * (i / n)) for i in range(n)))


def bed_align(src: Path, landing: float, at: float, bpm: float = 0.0, out: Path | None = None) -> dict:
    """A music bed whose payoff (`landing`, seconds into the track) falls exactly at `at` in the video.

    Enough runway (landing >= at): the head is trimmed. Otherwise the track is extended by looping a
    whole number of bars from a splice point before the landing: 4, 2, 1 and 8 bar loops are tried and
    the one whose splice correlates best wins. Repeats are joined with 15 ms equal-gain crossfades.
    Finally the output is checked against the source (cross-correlation around `at`).
    """
    src = Path(src)
    rate = 48000
    if landing < 0 or at < 0:
        die("--landing and --at are seconds, 0 or more")
    x48 = _pcm(src, rate, 2)
    frames = len(x48) // 2
    if landing * rate >= frames:
        die(f"--landing {landing:g}s is past the end of the track ({frames / rate:.1f}s)")
    x = _pcm(src, HZ, 1)
    ps = _energy(x)
    land48, at48 = int(round(landing * rate)), int(round(at * rate))
    info = {"loops": 0, "splice": None}
    if landing >= at:
        head, mid_out = land48 - at48, x48[2 * (land48 - at48):]
        built = mid_out
        info["note"] = f"the track has {landing - at:.2f}s of runway: trimmed the head"
    else:
        estimated = False
        if not bpm:
            bpm, conf = estimate_bpm(x)
            if conf < 1.5:
                die(f"can't hear a steady pulse to measure the tempo (confidence {conf:.1f}): pass --bpm N")
            estimated = True
            print(f"tempo estimated at {bpm:.1f} bpm (pass --bpm to override)", file=sys.stderr)
        bar = 4 * 60 / bpm
        lengths = [int(round(n * bar * HZ)) for n in (4, 2, 1, 8)]
        cands = find_loop(x, ps, lengths, int(landing * HZ))
        if not cands:
            die(f"no loop fits before the landing at {landing:g}s ({bpm:.1f} bpm): the track is too short "
                "before the payoff to take a bar from. Try a longer track or the intro as a head.")
        c = cands[0]
        p48, L48 = c["point"] * (rate // HZ), c["length"] * (rate // HZ)
        n = -(-(at48 - land48) // L48)
        head = land48 + n * L48 - at48
        f = int(XFADE * rate)
        parts = [x48[:2 * p48]]
        for _ in range(n):
            parts.append(_blend(x48[2 * p48:2 * (p48 + f)], x48[2 * (p48 - L48):2 * (p48 - L48 + f)]))
            parts.append(x48[2 * (p48 - L48 + f):2 * p48])
        parts.append(x48[2 * p48:])
        built = array.array("h")
        for part in parts:
            built.extend(part)
        built = built[2 * head:]
        info.update(loops=n, splice={**c, "bpm": bpm, "bars": c["length"] / (bar * HZ), "estimated": estimated,
                                      "others": cands[1:]})
    out = Path(out) if out else src.with_name(src.stem + "_aligned.wav")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        wav = out if out.suffix.lower() == ".wav" else Path(tmp) / "bed.wav"
        _write_wav(wav, built, rate, 2)
        if wav != out:
            ff.run(["-i", wav, out])
    info.update(out=out, achieved=_verify_landing(x, out, landing, at), duration=len(built) / 2 / rate)
    return info


def _verify_landing(src4k: array.array, out: Path, landing: float, at: float, span: float = 2.0,
                    search: float = 0.2) -> dict:
    """Where does the source's payoff really sit in the output? Cross-correlate the two seconds
    from `landing` in the source with the output around `at`, allowing +-0.2 s of lag."""
    y = _pcm(out, HZ, 1)
    n = min(int(span * HZ), len(src4k) - int(landing * HZ))
    t0 = int(landing * HZ)
    template = src4k[t0:t0 + n]
    et = sum(map(operator.mul, template, template))
    ps = _energy(y)
    best, lag = -1.0, 0
    for d in range(-int(search * HZ), int(search * HZ) + 1):
        i = int(round(at * HZ)) + d
        if i < 0 or i + n > len(y):
            continue
        ey = ps[i + n] - ps[i]
        if ey <= 0 or et <= 0:
            continue
        c = sum(map(operator.mul, template, y[i:i + n])) / math.sqrt(et * ey)
        if c > best:
            best, lag = c, d
    return {"time": at + lag / HZ, "corr": best}


def bed_report(r: dict, landing: float, at: float) -> str:
    lines = [str(r["out"])]
    if r["splice"]:
        s = r["splice"]
        lines.append(f"loop: {s['bars']:.0f} bars ({s['length'] / HZ:.2f}s at {s['bpm']:.1f} bpm"
                     f"{', estimated' if s['estimated'] else ''}) repeated {r['loops']}x, "
                     f"spliced at {s['point'] / HZ:.2f}s, splice correlation {s['score']:.2f}")
        if s["others"]:
            lines.append("other loops tried: " + ", ".join(
                f"{o['length'] / HZ:.2f}s at {o['point'] / HZ:.2f}s = {o['score']:.2f}" for o in s["others"]))
        if s["score"] < 0.5:
            lines.append("warning: weak splice (correlation under 0.5): it may sound like a jump. "
                         "Check --bpm, or pick a different --landing/track section.")
    else:
        lines.append(r["note"])
    a = r["achieved"]
    lines.append(f"payoff lands at {a['time']:.3f}s (asked {at:g}s, off by {1000 * (a['time'] - at):+.1f} ms), "
                 f"match to the source payoff {a['corr']:.3f} · bed is {r['duration']:.2f}s long")
    return "\n".join(lines)
