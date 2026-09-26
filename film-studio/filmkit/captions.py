"""Captions that look finished: word timings → caption events → styled .ass → burnt in.

The house look (ported from the studio's production caption work): bold white type, a soft
dark stroke painted behind the fill, a blurred drop shadow on its own layer, no box. The
`social` style highlights the spoken word and reveals words as they are said; `clean` shows
the phrase at once; `film` is quiet festival subtitling. Arabic and other RTL text use the
bundled IBM Plex Sans Arabic and the phrase-at-once behaviour (per-word effects can break
letter joining and reading order).

Only ffmpeg (with libass) is needed. Fonts ship in assets/fonts (SIL Open Font License).
For motion-graphic captions beyond this, the captions skill carries a Remotion component.
"""
from __future__ import annotations

import json
import os
import re
import tempfile
import urllib.request
import uuid
from pathlib import Path

from . import ff
from .core import KIT_ROOT, die

FONTS = KIT_ROOT / "assets" / "fonts"
ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
PUNCT = re.compile(r"[^\w؀-ۿ]+", re.UNICODE)

STYLES = {
    #          size = fraction of the short side · y = baseline as fraction of height
    "social": {"size": 0.072, "words": 4, "dur": 2.6, "chars": 18, "highlight": True,
               "y_tall": 0.68, "y_wide": 0.86, "stroke": 0.040, "stroke_a": 0x61},
    "clean":  {"size": 0.058, "words": 7, "dur": 3.5, "chars": 24, "highlight": False,
               "y_tall": 0.70, "y_wide": 0.88, "stroke": 0.036, "stroke_a": 0x61},
    "film":   {"size": 0.042, "words": 14, "dur": 6.0, "chars": 42, "highlight": False,
               "y_tall": 0.76, "y_wide": 0.93, "stroke": 0.045, "stroke_a": 0x40},
}


# --- word timings ------------------------------------------------------------

def _norm(word: str) -> str:
    return PUNCT.sub("", word.lower().replace("ـ", ""))


def load_words(path: Path) -> list[dict]:
    """Accepts filmkit/Scribe/WhisperX JSON, the studio's {t,s,e} words, or an SRT."""
    path = Path(path)
    if path.suffix.lower() == ".srt":
        from .qc import parse_srt
        words = []
        for a, b, text in parse_srt(path.read_text(encoding="utf-8")):
            toks = text.split()
            total = sum(len(t) for t in toks) or 1
            t = a
            for tok in toks:  # no word timings in an SRT: spread by character count
                d = (b - a) * len(tok) / total
                words.append({"text": tok, "start": t, "end": t + d, "speaker": ""})
                t += d
        return words
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "words" in data:
        raw = [w for w in data["words"] if w.get("type", "word") == "word"]
    elif isinstance(data, dict) and "segments" in data:
        raw = [w for s in data["segments"] for w in s.get("words", [])]
    elif isinstance(data, list):
        raw = data
    else:
        die(f"{path.name}: unrecognised transcript format")
    words = []
    for w in raw:
        text = (w.get("text") or w.get("word") or w.get("t") or "").strip()
        start, end = w.get("start", w.get("s")), w.get("end", w.get("e"))
        if text and start is not None and end is not None:
            words.append({"text": text, "start": float(start), "end": float(end),
                          "speaker": str(w.get("speaker_id") or w.get("speaker") or w.get("spk") or "")})
    if not words:
        die(f"{path.name}: no timed words found")
    # Aligners sometimes stretch a word over a pause; cap it so captions don't linger.
    for i, w in enumerate(words):
        if w["end"] - w["start"] > 0.6:
            nxt = words[i + 1]["start"] if i + 1 < len(words) else w["start"] + 0.6
            w["end"] = max(w["start"] + 0.1, min(w["start"] + 0.6, nxt - 0.05))
    return words


def segment(words: list[dict], max_words: int, max_dur: float, tail: float = 0.15) -> list[dict]:
    """Group words into caption events: sentence ends always break, commas break once a
    group is half full, speaker changes always break, then word-count and duration caps."""
    events, cur = [], []

    def flush():
        if cur:
            events.append({"start": cur[0]["start"], "end": cur[-1]["end"] + tail,
                           "words": list(cur), "text": " ".join(w["text"] for w in cur)})
            cur.clear()

    for w in words:
        if cur and w["speaker"] != cur[-1]["speaker"]:
            flush()
        cur.append(w)
        t = w["text"]
        if re.search(r"[.!?؟…]$", t):
            flush()
        elif len(cur) >= max(2, max_words // 2) and re.search(r"[,،;:\u2014\u2013-]$", t):
            flush()
        elif len(cur) >= max_words or cur[-1]["end"] - cur[0]["start"] >= max_dur:
            flush()
    flush()
    return _tidy(events)


def from_lines(words: list[dict], lines: list[str], tail: float = 0.15) -> tuple[list[dict], list[str]]:
    """Authored captions: your phrasing, the transcript's timing.

    Each line consumes as many transcript words as it has words. Mismatched words are
    reported (they are usually the transcript's mistakes, which is why you author). If a line
    mostly mismatches, the lines have drifted from the audio and we stop.
    """
    events, notes, k = [], [], 0
    for n, line in enumerate(l.strip() for l in lines if l.strip()):
        toks = line.split()
        got = words[k:k + len(toks)]
        if len(got) < len(toks):
            die(f"line {n + 1} '{line}' runs past the end of the transcript")
        bad = [(a, b["text"]) for a, b in zip(toks, got) if _norm(a) != _norm(b["text"])]
        if len(bad) > max(1, len(toks) // 3):
            die(f"line {n + 1} '{line}' doesn't match the audio here "
                f"(transcript: '{' '.join(w['text'] for w in got)}' at {got[0]['start']:.2f}s). "
                "A line is missing, merged or split differently.")
        for a, b in bad:
            notes.append(f"line {n + 1}: you wrote '{a}', transcript heard '{b}' (check which is right)")
        if len({w['speaker'] for w in got}) > 1:
            notes.append(f"line {n + 1} '{line}' spans two speakers: split it")
        timed = [{**w, "text": t} for w, t in zip(got, toks)]
        events.append({"start": timed[0]["start"], "end": timed[-1]["end"] + tail, "words": timed, "text": line})
        k += len(toks)
    if k < len(words):
        notes.append(f"{len(words) - k} transcript words after the last line have no caption")
    return _tidy(events), notes


def _tidy(events: list[dict]) -> list[dict]:
    """No overlaps, and no tiny gaps (a < 0.1s gap reads as flicker): close them."""
    for a, b in zip(events, events[1:]):
        if a["end"] > b["start"] or b["start"] - a["end"] < 0.1:
            a["end"] = b["start"]
    return [e for e in events if e["end"] - e["start"] > 0.05]


# --- rendering ---------------------------------------------------------------

def _ts(t: float) -> str:
    cs = max(0, int(round(t * 100)))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("{", "(").replace("}", ")")


def _bgr(hex_colour: str, alpha: int = 0) -> str:
    h = hex_colour.lstrip("#")
    if len(h) != 6:
        die(f"colour must be like #F5C542, got {hex_colour}")
    return f"&H{alpha:02X}{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def _lines(tokens: list[str], max_chars: int) -> list[list[int]]:
    """Split token indices into one or two balanced lines."""
    total = len(" ".join(tokens))
    if total <= max_chars or len(tokens) < 2:
        return [list(range(len(tokens)))]
    best, cut = None, 1
    for i in range(1, len(tokens)):
        a, b = len(" ".join(tokens[:i])), len(" ".join(tokens[i:]))
        score = abs(a - b) + (4 if a > b else 0)  # prefer a shorter top line (pyramid)
        if best is None or score < best:
            best, cut = score, i
    return [list(range(cut)), list(range(cut, len(tokens)))]


def render_ass(events: list[dict], width: int, height: int, style: str = "social",
               accent: str = "#F5C542", colour: str = "#FFFFFF", y: float | None = None) -> str:
    if style not in STYLES:
        die(f"style must be one of {', '.join(STYLES)}")
    s = STYLES[style]
    rtl = any(ARABIC.search(e["text"]) for e in events)
    highlight = s["highlight"] and not rtl
    short = min(width, height)
    size = round(s["size"] * short)
    stroke = max(1.0, round(s["stroke"] * size, 1))
    font = "IBM Plex Sans Arabic" if rtl else "Poppins"
    ypos = round((y if y is not None else (s["y_tall"] if height > width else s["y_wide"])) * height)
    x = width // 2
    shadow_off = max(2, round(size * 0.05))
    blur = max(3, round(size * 0.1))
    white, gold = _bgr(colour), _bgr(accent)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Text,{font},{size},{white},{white},{_bgr('#000000', s['stroke_a'])},&H00000000,-1,0,0,0,100,100,0,0,1,{stroke},0,2,40,40,40,1
Style: Shade,{font},{size},{_bgr('#000000', 0x66)},{white},&HFF000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,2,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    out = [header]

    def emit(a: float, b: float, body_text: str, body_shade: str, extra: str = "") -> None:
        if b - a < 0.01:
            return
        out.append(f"Dialogue: 0,{_ts(a)},{_ts(b)},Shade,,0,0,0,,{{\\pos({x},{ypos + shadow_off})\\blur{blur}{extra}}}{body_shade}\n")
        out.append(f"Dialogue: 1,{_ts(a)},{_ts(b)},Text,,0,0,0,,{{\\pos({x},{ypos}){extra}}}{body_text}\n")

    for e in events:
        tokens = [_esc(w["text"]) for w in e["words"]] if e.get("words") else _esc(e["text"]).split()
        layout = _lines(tokens, round(s["chars"] * (1.4 if rtl else 1)))
        if not highlight:
            body = "\\N".join(" ".join(tokens[i] for i in line) for line in layout)
            emit(e["start"], e["end"], body, body, "\\fad(80,80)")
            continue
        words = e["words"]
        # One line per word onset: earlier words shown, the new word fades in highlighted,
        # later words present but invisible so the layout never jumps.
        for i, w in enumerate(words):
            a = max(e["start"], w["start"])
            b = words[i + 1]["start"] if i + 1 < len(words) else min(e["end"], w["end"] + 0.25)
            parts_t, parts_s = [], []
            for line in layout:
                lt, ls = [], []
                for j in line:
                    tok = tokens[j]
                    if j < i:
                        lt.append(tok); ls.append(tok)
                    elif j == i:
                        lt.append(f"{{\\c{gold}\\alpha&HFF&\\t(0,80,\\alpha&H00&)}}{tok}{{\\c{white}}}")
                        ls.append(f"{{\\alpha&HFF&\\t(0,80,\\alpha&H66&)}}{tok}")
                    else:
                        lt.append(f"{{\\alpha&HFF&}}{tok}{{\\alpha&H00&}}")
                        ls.append(f"{{\\alpha&HFF&}}{tok}{{\\alpha&H66&}}")
                parts_t.append(" ".join(lt)); parts_s.append(" ".join(ls))
            emit(a, b, "\\N".join(parts_t), "\\N".join(parts_s))
            if i == len(words) - 1 and e["end"] > b:
                plain = "\\N".join(" ".join(tokens[j] for j in line) for line in layout)
                emit(b, e["end"], plain, plain)
    return "".join(out)


def to_srt(events: list[dict]) -> str:
    def t(x: float) -> str:
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    return "".join(f"{n}\n{t(e['start'])} --> {t(e['end'])}\n{e['text']}\n\n" for n, e in enumerate(events, 1))


def _filter_path(p: Path) -> str:
    return str(Path(p).resolve()).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")


def burn(video: Path, ass: Path, out: Path) -> Path:
    vf = f"subtitles='{_filter_path(ass)}':fontsdir='{_filter_path(FONTS)}'"
    try:
        ff.run(["-i", video, "-vf", vf, *ff.VIDEO_OUT, "-c:a", "copy", out])
    except Exception as e:
        if "No such filter" in str(e):
            die(f"this ffmpeg ({ff.ffmpeg_bin()}) has no subtitles filter (libass). Install a build with it "
                f"({ff.INSTALL_HINT}) or use the Remotion captions route in the captions skill.")
        raise
    return out


# --- transcription (ElevenLabs Scribe) ---------------------------------------

def transcribe(media: Path, out_json: Path, language: str = "", speakers: int = 0,
               model: str = "scribe_v2") -> Path:
    """Word-timed transcript via ElevenLabs Scribe. Needs ELEVENLABS_API_KEY."""
    from .gen import load_env
    load_env()
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        die("ELEVENLABS_API_KEY is not set (studio .env). Or transcribe elsewhere and pass the JSON/SRT.")
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "audio.wav"
        ff.run(["-i", media, "-vn", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", wav])
        fields = {"model_id": model, "timestamps_granularity": "word", "tag_audio_events": "false",
                  "diarize": "true" if speakers != 1 else "false"}
        if language:
            fields["language_code"] = language
        if speakers > 1:
            fields["num_speakers"] = str(speakers)
        boundary = uuid.uuid4().hex
        body = b""
        for k, v in fields.items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"audio.wav\"\r\n"
                 f"Content-Type: audio/wav\r\n\r\n").encode() + wav.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body, method="POST",
                                     headers={"xi-api-key": key,
                                              "Content-Type": f"multipart/form-data; boundary={boundary}"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                raw = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            die(f"Scribe → HTTP {e.code}: {e.read().decode()[:400]}")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.with_suffix(".raw.json").write_text(json.dumps(raw, ensure_ascii=False, indent=1))
    words = [{"text": w["text"], "start": w["start"], "end": w["end"], "speaker": w.get("speaker_id", "")}
             for w in raw.get("words", []) if w.get("type") == "word"]
    out_json.write_text(json.dumps(words, ensure_ascii=False, indent=1))
    return out_json
