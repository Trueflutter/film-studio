"""Mixing: dialogue first, music ducked under it, beds and effects, then loudness to spec."""
from __future__ import annotations

import tempfile
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


def mix(prod: Production, video: Path | None = None, dialogue: Path | None = None,
        music: Path | None = None, ambience: list | None = None, fx: list | None = None,
        music_db: float = -18.0, ambience_db: float = -24.0, target: float | None = None,
        use_video_audio: bool = True) -> Path:
    """Build a mix and (if a video is given) lay it onto the picture without re-encoding it.

    Dialogue is loudness-normalised, music sits at `music_db` and ducks under the dialogue via
    sidechain compression, ambience beds sit low, effects play at level, and the finished mix is
    gain-matched to the delivery loudness (default: production.json loudness_lufs).
    """
    # ambience/fx items are Paths or (Path, start seconds) pairs
    ambience = [a if isinstance(a, tuple) else (a, 0.0) for a in ambience or []]
    fx = [f if isinstance(f, tuple) else (f, 0.0) for f in fx or []]
    target = target if target is not None else float(prod.cfg.get("loudness_lufs", -14))
    inputs: list = []
    dia_idx = mus_idx = None
    if video:
        inputs += ["-i", video]
        if dialogue is None and use_video_audio and ff.probe(video)["has_audio"]:
            dia_idx = 0
    if dialogue:
        dia_idx = len(inputs) // 2
        inputs += ["-i", dialogue]
    if music:
        mus_idx = len(inputs) // 2
        inputs += ["-i", music]
    amb_idx = []
    for a, at in ambience:
        amb_idx.append((len(inputs) // 2, at))
        inputs += ["-i", a]
    fx_idx = []
    for f, at in fx:
        fx_idx.append((len(inputs) // 2, at))
        inputs += ["-i", f]
    if dia_idx is None and mus_idx is None and not amb_idx and not fx_idx:
        die("nothing to mix: pass --dialogue/--music/--ambience/--fx or a --video with audio")

    ref = video or dialogue or music or (ambience[0][0] if ambience else fx[0][0])
    dur = ff.probe(ref)["duration"]
    if not dur:
        die(f"can't read the duration of {ref}")

    chains, labels = [], []
    if dia_idx is not None:
        split = "asplit=2[dia][key]" if mus_idx is not None else "anull[dia]"
        chains.append(f"{_prep(dia_idx)},loudnorm=I=-16:TP=-1.5:LRA=11,{split}")
        labels.append("[dia]")
    if mus_idx is not None:
        fade_out = max(dur - 2.0, 0)
        chains.append(f"{_prep(mus_idx)},volume={music_db}dB,afade=t=in:d=1.5,"
                      f"afade=t=out:st={fade_out:.2f}:d=2[mus]")
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
    # normalize=0 keeps each stem at the level we set instead of dividing by the input count.
    chains.append(f"{''.join(labels)}amix=inputs={len(labels)}:duration=longest:normalize=0,"
                  f"atrim=duration={dur:.3f},apad=whole_dur={dur:.3f}[pre]")

    out_wav = prod.next_version(prod.dir("sound") / "mix", "mix", ".wav")
    with tempfile.TemporaryDirectory() as tmp:
        pre = Path(tmp) / "pre.wav"
        ff.run([*inputs, "-filter_complex", ";".join(chains), "-map", "[pre]", "-ar", "48000", pre])
        match_loudness(pre, out_wav, target)
    if not video:
        return out_wav
    out_mp4 = prod.next_version(Path(video).parent, Path(video).stem.split("_mix")[0] + "_mix", ".mp4")
    ff.run(["-i", video, "-i", out_wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
            *ff.AUDIO_OUT, "-shortest", out_mp4])
    return out_mp4


def match_loudness(src: Path, dest: Path, target: float, ceiling_db: float = -1.5,
                   tolerance: float = 0.3, passes: int = 4) -> dict:
    """Linear gain + true-peak limiter, re-measured until within tolerance of target.

    Gain (not single-pass loudnorm) keeps the mix's dynamics intact; the limiter catches peaks.
    The limiter works on sample peaks, so the ceiling sits 0.5 dB under the -1 dBTP spec to
    leave room for inter-sample (true) peaks.
    """
    gain = 0.0
    measured = ff.loudness(src)
    if measured["lufs"] is None or measured["lufs"] == float("-inf"):
        die(f"{src} is silent: nothing to normalise")
    limit = 10 ** (ceiling_db / 20)
    for _ in range(passes):
        gain += target - measured["lufs"]
        ff.run(["-i", src, "-af", f"volume={gain:.2f}dB,alimiter=limit={limit:.4f}:level=disabled",
                "-ar", "48000", dest])
        measured = ff.loudness(dest)
        if measured["lufs"] is not None and abs(measured["lufs"] - target) <= tolerance:
            break
    return measured
