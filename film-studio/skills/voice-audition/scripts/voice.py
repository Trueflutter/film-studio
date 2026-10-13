#!/usr/bin/env python3
"""Pick, voice and tighten a narration with ElevenLabs. Standard library plus ffmpeg.

  python3 voice.py check
  python3 voice.py voices   [--search TEXT] [--library] [--accent A] [--gender G] [--age A] [--language en] [--limit 20]
  python3 voice.py audition --line "..." --voices ID1,ID2,ID3 --out DIR [--model auto] [--no-open]
  python3 voice.py read     SCRIPT.txt --voice ID --out FILE.mp3 [--model auto] [--stability 0.5] [--similarity 0.8]
  python3 voice.py tighten  IN.mp3 [--wps 3.0] [--gap 0.2] [--min-gap 0.28] [--tempo X] [--script SCRIPT.txt] [--out OUT.mp3]
  python3 voice.py verify   AUDIO.mp3 SCRIPT.txt
  python3 voice.py save     CHARACTER.md --audio NARRATION.mp3 [--voice ID] [--note "..."]
  python3 voice.py board    DIR [--no-open]

The key is read from ELEVENLABS_API_KEY in the environment, else from a .env in this
folder or any folder above it. The key is never printed or written anywhere.
A voice can be written as ID, or as OWNER/ID for a shared-library voice (it is added to
your account first).
"""
import argparse, difflib, html, json, mimetypes, os, platform, re, shutil, subprocess, sys
import tempfile, threading, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

API = "https://api.elevenlabs.io"
OUTPUT_FORMAT = "mp3_44100_128"   # 192 kbps returns 403 on common plans
PREFERRED_MODELS = ["eleven_v4", "eleven_v3"]  # newest first; never fall back to older ones silently
FALLBACK_MODEL = "eleven_v3"
STABILITY, SIMILARITY = 0.5, 0.8
_voice_locks = {}
_voice_locks_guard = threading.Lock()


# ---------------------------------------------------------------- key and http

def _key():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if k:
        return k
    d = Path.cwd().resolve()
    for folder in [d, *d.parents]:
        env = folder / ".env"
        if env.is_file():
            for line in env.read_text(errors="ignore").splitlines():
                m = re.match(r"\s*(?:export\s+)?ELEVENLABS_API_KEY\s*=\s*(.*)", line)
                if m:
                    v = m.group(1).strip().strip("'\"")
                    if v:
                        return v
    sys.exit("No ElevenLabs key found. Add this line to your studio .env file yourself "
             "(do not paste it into chat):\n  ELEVENLABS_API_KEY=your_key_here\n"
             "Then run the command again from the studio folder.")


def _request(method, path, body=None, raw=False, headers=None, retries=4):
    url = path if path.startswith("http") else API + path
    h = {"xi-api-key": _key(), "Accept": "*/*"}
    data = None
    if body is not None:
        if isinstance(body, (bytes, bytearray)):
            data = bytes(body)
        else:
            data = json.dumps(body).encode()
            h["Content-Type"] = "application/json"
    h.update(headers or {})
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers=h, method=method)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                payload = r.read()
                return payload if raw else (json.loads(payload) if payload else {})
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="ignore")[:400]
            if e.code in (409, 429, 500, 502, 503) and attempt < retries:
                time.sleep(2 * (attempt + 1))
                continue
            raise ApiError(e.code, detail)
        except urllib.error.URLError as e:
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
                continue
            raise ApiError(0, f"network error: {e.reason}")


class ApiError(Exception):
    def __init__(self, code, detail):
        super().__init__(f"HTTP {code}: {detail}")
        self.code, self.detail = code, detail


def _explain(e):
    hints = {401: "The key was rejected. Check ELEVENLABS_API_KEY in your .env.",
             402: "Your plan does not allow this (voice or model).",
             403: "Your plan or key does not allow this (permissions, voice or format).",
             404: "Voice not found. Use an id from `voices`, or OWNER/ID for a library voice.",
             422: "The request was rejected. Check the voice id, the model and the text.",
             429: "Too many requests. Wait a minute and run it again."}
    return f"{e}\n{hints.get(e.code, '')}".strip()


# ---------------------------------------------------------------- third-party text

_BAD = re.compile(r"[^\w .,'()&-]")
_ID = re.compile(r"^[A-Za-z0-9_-]{1,80}$")
_OWNER = re.compile(r"^[A-Za-z0-9_-]{1,100}$")


def clean(s, n=160):
    """Voice names and descriptions come from other people. Keep letters, digits and
    . , ' ( ) & - only, drop newlines and control characters, cap the length."""
    s = re.sub(r"[\x00-\x1f\x7f-\x9f\u2028\u2029]+", " ", str(s or ""))
    s = _BAD.sub("", s)
    return re.sub(r" {2,}", " ", s).strip()[:n]


def check_token(tok):
    """A voice is ID or OWNER/ID. Reject anything else before it reaches a URL or a file."""
    owner, _, vid = str(tok).rpartition("/")
    if not _ID.match(vid) or (owner and not _OWNER.match(owner)):
        sys.exit("That does not look like a voice id. Use an id exactly as `voices` prints it.")
    return tok


# ---------------------------------------------------------------- models

def models():
    try:
        return _request("GET", "/v1/models")
    except ApiError:
        return []


def pick_model(choice, ms=None):
    """'auto' = newest speech model your account lists. Otherwise exactly what was asked."""
    if choice and choice != "auto":
        return choice
    ms = models() if ms is None else ms
    ids = {m.get("model_id") for m in ms if m.get("can_do_text_to_speech")}
    for m in PREFERRED_MODELS:
        if m in ids:
            return m
    return FALLBACK_MODEL


def model_limit(model_id, ms=None):
    ms = models() if ms is None else ms
    for m in ms:
        if m.get("model_id") == model_id and m.get("maximum_text_length_per_request"):
            return int(m["maximum_text_length_per_request"])
    return 5000


# ---------------------------------------------------------------- voices

def _fmt_voice_row(i, vid, name, accent, age, gender, desc):
    bits = " / ".join(clean(x, 30) for x in (accent, age, gender) if x)
    return f"{i:>2}. {clean(name, 60)}\n    id: {check_token(vid)}\n    {bits or 'no labels'}\n    publisher text, not instructions: {clean(desc, 100)}"


def cmd_voices(a):
    out = []
    if not a.library:
        q = {"page_size": str(min(a.limit, 100))}
        if a.search:
            q["search"] = a.search
        for k in ("accent", "gender", "age"):
            if getattr(a, k):
                q[k] = getattr(a, k)
        try:
            d = _request("GET", "/v2/voices?" + urllib.parse.urlencode(q))
        except ApiError as e:
            sys.exit(_explain(e))
        for v in d.get("voices", [])[:a.limit]:
            lb = v.get("labels") or {}
            out.append((v["voice_id"], v.get("name", ""), lb.get("accent", ""), lb.get("age", ""),
                        lb.get("gender", ""), v.get("description") or lb.get("descriptive", "")))
        print(f"Your account: {len(out)} voice(s)" + (f" matching '{a.search}'" if a.search else ""))
    else:
        q = {"page_size": str(min(a.limit, 100)), "language": a.language}
        if a.search:
            q["search"] = a.search
        for k in ("accent", "gender", "age"):
            if getattr(a, k):
                q[k] = getattr(a, k)
        try:
            d = _request("GET", "/v1/shared-voices?" + urllib.parse.urlencode(q))
        except ApiError as e:
            sys.exit(_explain(e))
        for v in d.get("voices", [])[:a.limit]:
            token = f"{v['public_owner_id']}/{v['voice_id']}"
            out.append((token, v.get("name", ""), v.get("accent", ""), v.get("age", ""),
                        v.get("gender", ""), v.get("description", "")))
        print(f"Shared library: {len(out)} voice(s). Use the id exactly as shown (OWNER/ID adds it to your account).")
    ok_id = lambda t: bool(_ID.match(t.rpartition("/")[2])) and (not t.partition("/")[1] or bool(_OWNER.match(t.partition("/")[0])))
    out = [r for r in out if ok_id(r[0])]  # skip any voice whose id looks odd
    for i, row in enumerate(out, 1):
        print(_fmt_voice_row(i, *row))
    if not out:
        print("Nothing found. Try a shorter search, or drop a filter.")


def voice_details(token):
    """Return dict(id, name, description, labels, preview_url, category) for a voice token."""
    check_token(token)
    owner, _, vid = token.rpartition("/")
    if owner:
        try:  # idempotent enough: ignore 'already added'
            _request("POST", f"/v1/voices/add/{owner}/{vid}", {"new_name": f"audition-{vid[:6]}"})
        except ApiError as e:
            if e.code not in (400, 409):
                raise
    try:
        v = _request("GET", f"/v1/voices/{vid}")
    except ApiError:
        v = {}
    lb = v.get("labels") or {}
    shared = v.get("sharing") or {}
    name = shared.get("name") if (v.get("name") or "").startswith("audition-") and shared.get("name") else v.get("name")
    return {"id": vid, "name": clean(name, 60) or vid, "description": clean(v.get("description"), 160),
            "labels": " / ".join(clean(x, 30) for x in (lb.get("accent"), lb.get("age"), lb.get("gender")) if x),
            "category": v.get("category", "")}


# ---------------------------------------------------------------- speech

def tts(voice_id, text, model, stability=STABILITY, similarity=SIMILARITY):
    """One request, serialized per voice (the same voice twice at once returns 409)."""
    with _voice_locks_guard:
        lock = _voice_locks.setdefault(voice_id, threading.Lock())
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": stability, "similarity_boost": similarity}}
    with lock:
        return _request("POST", f"/v1/text-to-speech/{voice_id}?output_format={OUTPUT_FORMAT}",
                        body, raw=True)


def _sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n{2,}", text.strip())
    return [p.strip() for p in parts if p.strip()]


def chunk_text(text, limit):
    chunks, cur = [], ""
    for s in _sentences(text):
        while len(s) > limit:  # one monster sentence: split at a comma or space
            cut = max(s.rfind(", ", 0, limit), s.rfind(" ", 0, limit))
            cut = cut if cut > 0 else limit
            chunks.append(s[:cut + 1].strip()); s = s[cut + 1:].strip()
        if len(cur) + len(s) + 1 > limit and cur:
            chunks.append(cur); cur = s
        else:
            cur = f"{cur} {s}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def clean_script(raw):
    lines = [l.rstrip() for l in raw.splitlines() if not l.lstrip().startswith("#")]
    text = re.sub(r"[ \t]+", " ", "\n".join(lines)).strip()
    warns = []
    if "..." in text or "…" in text:
        warns.append("The script has ellipses. They make the voice hesitate. Use a full stop instead.")
    if chr(0x2014) in text or chr(0x2013) in text:
        warns.append("The script has dashes. Use commas or full stops, the voice reads them oddly.")
    return text, warns


def words_in(text):
    text = re.sub(r"\[[^\]]*\]", " ", text)  # v3 audio tags like [softly] are not spoken words
    return re.findall(r"[\w'\u2019]+", text)


def ffmpeg_ok():
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        sys.exit("ffmpeg is not installed. On a Mac: brew install ffmpeg")


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    try:
        return float(r.stdout.strip())
    except ValueError:
        sys.exit(f"Could not read the length of {path}.")


def join_mp3(parts, dest):
    if len(parts) == 1:
        Path(dest).write_bytes(Path(parts[0]).read_bytes())
        return
    cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
    for p in parts:
        cmd += ["-i", str(p)]
    n = len(parts)
    cmd += ["-filter_complex", "".join(f"[{i}:a]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]",
            "-map", "[o]", "-ar", "44100", "-b:a", "128k", str(dest)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg could not join the chunks:\n" + r.stderr[-400:])


def cmd_read(a):
    ffmpeg_ok()
    check_token(a.voice)
    raw = Path(a.script).read_text()
    text, warns = clean_script(raw)
    for w in warns:
        print("note:", w)
    ms = models()
    model = pick_model(a.model, ms)
    limit = max(500, min(model_limit(model, ms) - 500, 4500))
    chunks = chunk_text(text, limit)
    out = Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"Voicing {len(words_in(text))} words in {len(chunks)} piece(s) on {model}, stability {a.stability}, similarity {a.similarity}.")
    tmp = Path(tempfile.mkdtemp(prefix="voice_"))
    parts = []
    try:
        for i, c in enumerate(chunks, 1):  # one at a time: same voice, no 409
            try:
                audio = tts(a.voice, c, model, a.stability, a.similarity)
            except ApiError as e:
                sys.exit(_explain(e))
            p = tmp / f"part{i:02d}.mp3"; p.write_bytes(audio); parts.append(p)
            print(f"  piece {i}/{len(chunks)} done")
        join_mp3(parts, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    out.with_suffix(".txt").write_text(text + "\n")
    out.with_suffix(".json").write_text(json.dumps(
        {"model": model, "voice_id": a.voice, "stability": a.stability, "similarity_boost": a.similarity,
         "output_format": OUTPUT_FORMAT, "date": date.today().isoformat(), "words": len(words_in(text))}, indent=1))
    d, w = duration(out), len(words_in(text))
    print(f"saved: {out}\n  {d:.1f}s, {w} words, {w / d:.2f} words per second (script copy: {out.with_suffix('.txt').name})")


# ---------------------------------------------------------------- tighten

def find_silences(path, min_gap):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-i", str(path), "-af",
                        f"silencedetect=noise=-35dB:d={min_gap}", "-f", "null", "-"],
                       capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(starts, ends))  # a trailing unmatched start (silence to the end) is left alone


def cmd_tighten(a):
    ffmpeg_ok()
    src = Path(a.input).resolve()
    out = Path(a.out).resolve() if a.out else src.with_name(src.stem + "_tight.mp3")
    if out == src:
        sys.exit("--out must be a different file. The original is always kept.")
    d0 = duration(src)
    gaps = [(s, e) for s, e in find_silences(src, a.min_gap) if e - s > a.min_gap and s > 0.05]
    segs, pos = [], 0.0
    for s, e in gaps:  # keep GAP of the silence, cut the rest from its middle
        segs.append((pos, s + a.gap / 2))
        pos = e - a.gap / 2
    segs.append((pos, None))
    parts = []
    for i, (s, e) in enumerate(segs):
        trim = f"atrim=start={s:.4f}" + (f":end={e:.4f}" if e is not None else "")
        parts.append(f"[0:a]{trim},asetpts=PTS-STARTPTS[a{i}]")
    labels = "".join(f"[a{i}]" for i in range(len(segs)))
    cut = sum(e - s - a.gap for s, e in gaps)
    d_gap = d0 - cut  # length after the pauses are trimmed, before any speed-up
    # words: the script copy if there is one, else a transcript of the audio
    sp = Path(a.script) if a.script else src.with_suffix(".txt")
    words, source = None, ""
    if sp.is_file():
        words, source = len(words_in(sp.read_text())), "script"
    elif a.tempo is None:
        heard, via = transcribe(src)
        if heard:
            words, source = len(words_in(heard)), f"transcript ({via})"
    # tempo: manual override, else the speed that lands on the target pace
    if a.tempo is not None:
        tempo, why = a.tempo, "manual --tempo"
    elif words:
        now = words / d_gap
        raw = a.wps / now
        tempo = min(1.25, max(0.9, raw))
        why = f"target {a.wps} words per second"
        if abs(now - a.wps) / a.wps <= 0.03:
            tempo, why = 1.0, f"already within 3% of {a.wps} words per second"
        elif tempo != raw:
            why += f" (wanted x{raw:.2f}, limited to x{tempo:.2f}: past that the voice sounds rushed or drags)"
    else:
        tempo, why = 1.0, "no script or transcript to measure, pauses only"
    tempo = round(tempo, 3)
    chain = f"concat=n={len(segs)}:v=0:a=1" + (f",atempo={tempo}" if abs(tempo - 1.0) > 0.001 else "")
    fc = ";".join(parts) + f";{labels}{chain}[o]"
    r = subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(src),
                        "-filter_complex", fc, "-map", "[o]",
                        "-ar", "44100", "-b:a", "128k", str(out)], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + r.stderr[-500:])
    d1 = duration(out)
    side = src.with_suffix(".json")
    if side.is_file():  # the tightened file inherits the read record, so `save` still finds the real model
        try:
            rec = json.loads(side.read_text()); rec.update({"tightened_from": src.name, "tempo": tempo})
            out.with_suffix(".json").write_text(json.dumps(rec, indent=1))
        except ValueError:
            pass
    print(f"original kept: {src.name}\nsaved: {out}")
    print(f"pauses longer than {a.min_gap}s shortened to {a.gap}s: {len(gaps)} found, {cut:.1f}s removed")
    print(f"tempo: x{tempo} ({why})")
    print(f"duration: {d0:.1f}s -> {d1:.1f}s")
    if words:
        print(f"words: {words} (from {source})   words per second: {words / d0:.2f} -> {words / d1:.2f}")
    else:
        print("No word count, so no words per second. Pass --script SCRIPT.txt.")


# ---------------------------------------------------------------- verify

def _multipart(fields, file_field, path):
    b = "----voice" + str(int(time.time() * 1000))
    body = b""
    for k, v in fields.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body += (f'--{b}\r\nContent-Disposition: form-data; name="{file_field}"; filename="{path.name}"\r\n'
             f"Content-Type: {ctype}\r\n\r\n").encode() + path.read_bytes() + f"\r\n--{b}--\r\n".encode()
    return body, {"Content-Type": f"multipart/form-data; boundary={b}"}


def transcribe(path):
    tmp = Path(tempfile.mkdtemp(prefix="voice_stt_"))
    try:
        for exe in ("whisperx", "whisper"):
            if shutil.which(exe):
                cmd = ([exe, str(path), "--model", "small.en" if exe == "whisper" else "small",
                        "--output_dir", str(tmp), "--output_format", "txt"])
                if subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL).returncode == 0:
                    t = next(tmp.glob("*.txt"), None)
                    if t:
                        return t.read_text(), exe
        try:
            body, h = _multipart({"model_id": "scribe_v2"}, "file", path)
            return _request("POST", "/v1/speech-to-text", body, headers=h).get("text", ""), "ElevenLabs speech-to-text"
        except ApiError as e:
            print("Could not transcribe:", _explain(e))
            return None, None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def cmd_verify(a):
    for f in (a.audio, a.script):
        if not Path(f).is_file():
            sys.exit(f"File not found: {f}")
    script = clean_script(Path(a.script).read_text())[0]
    heard, via = transcribe(Path(a.audio).resolve())
    if heard is None:
        print("No transcript available. Listen to the whole file once, with the script in front of you.")
        return
    ones = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
            "fifteen sixteen seventeen eighteen nineteen twenty").split()
    numwords = {str(i): w for i, w in enumerate(ones)}
    numwords.update({"30": "thirty", "40": "forty", "50": "fifty", "60": "sixty", "70": "seventy",
                     "80": "eighty", "90": "ninety", "100": "hundred"})
    norm = lambda t: [numwords.get(w, w) for w in (x.lower().replace(chr(0x2019), "'") for x in words_in(t))]
    exp, got = norm(script), norm(heard)
    sm = difflib.SequenceMatcher(a=exp, b=got, autojunk=False)
    issues = [(op, " ".join(exp[i1:i2]), " ".join(got[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    print(f"Transcribed with {via}. Script {len(exp)} words, heard {len(got)} words, match {sm.ratio() * 100:.1f}%.")
    if not issues:
        print("Every word matches. Still listen once for tone.")
    for op, e, g in issues:
        print({"replace": "WRONG", "delete": "MISSING", "insert": "EXTRA"}[op] + f": script '{e}'  heard '{g}'")
    if issues:
        print("Fix by re-reading just that sentence, or respell the word the way it sounds. Numbers and names are the usual trouble.")


# ---------------------------------------------------------------- audition and board

def cmd_audition(a):
    toks = [t.strip() for t in a.voices.split(",") if t.strip()]
    toks = list(dict.fromkeys(toks))
    if not 2 <= len(toks) <= 6:
        sys.exit("Give 3 voice ids, separated by commas (2 to 6 is allowed).")
    out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    model = pick_model(a.model)
    print(f"Voicing one line with {len(toks)} voices on {model} ({len(a.line)} characters each)...")

    def one(i_tok):
        i, tok = i_tok
        try:
            info = voice_details(tok)
            audio = tts(info["id"], a.line, model)
        except ApiError as e:
            return i, {"id": tok, "name": tok, "error": _explain(e)}
        f = f"voice_{i}.mp3"
        (out / f).write_bytes(audio)
        info["file"] = f
        return i, info

    with ThreadPoolExecutor(max_workers=3) as ex:  # different voices in parallel is fine
        res = [r for _, r in sorted(ex.map(one, enumerate(toks, 1)), key=lambda x: x[0])]
    meta = {"line": a.line, "model": model, "settings": {"stability": STABILITY, "similarity_boost": SIMILARITY},
            "voices": res, "date": date.today().isoformat()}
    (out / "meta.json").write_text(json.dumps(meta, indent=1))
    for i, v in enumerate(res, 1):
        print(f"{i}. {v['name']}  {v['id']}  " + (v.get("error") or "ok"))
    path = build_board(out)
    if not a.no_open:
        open_file(path)
    print(f"board: {path}\nAsk the student: Which number?")


def build_board(out):
    out = Path(out).resolve()
    mp = out / "meta.json"
    if mp.exists():
        meta = json.loads(mp.read_text())
    else:
        files = sorted(out.glob("*.mp3"))
        meta = {"line": "", "model": "", "voices": [{"id": f.stem, "name": f.stem, "file": f.name} for f in files]}
    cards = []
    for i, v in enumerate(meta["voices"], 1):
        if v.get("error"):
            body = f'<p class="err">{html.escape(clean(v["error"], 300))}</p>'
        else:
            body = f'<audio controls preload="auto" src="{html.escape(re.sub(r"[^A-Za-z0-9._-]", "", str(v["file"])))}"></audio>'
        cards.append(
            f'<section><div class="n">{i}</div><div class="b"><h2>{html.escape(clean(v["name"], 60))}</h2>'
            f'<p class="m">{html.escape(clean(v.get("labels", ""), 90))}</p>'
            f'<p class="d">{html.escape(clean(v.get("description", ""), 160))}</p>{body}'
            f'<p class="id">id: {html.escape(re.sub(r"[^A-Za-z0-9/_-]", "", str(v["id"]))[:80])}</p></div></section>')
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Voice audition</title><style>
:root{{--bg:#0e0e10;--ink:#f5f5f7;--mute:#a0a0a6;--line:#2a2a2e;--card:#17171a;--acc:#ffb347}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}
main{{max-width:760px;margin:0 auto;padding:24px 16px 60px}} h1{{font-weight:500;font-size:26px;margin:0 0 4px}}
.meta{{color:var(--mute);margin:0 0 18px}} .line{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:0 0 18px}}
section{{display:flex;gap:16px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:0 0 14px}}
.n{{font-size:40px;font-weight:600;color:var(--acc);min-width:36px}} .b{{flex:1}} h2{{font-size:18px;margin:0}}
.m{{color:var(--acc);margin:2px 0}} .d{{color:var(--mute);margin:2px 0 10px}} .id{{color:var(--mute);font:12px ui-monospace,monospace;margin:8px 0 0;user-select:all}}
audio{{width:100%}} .err{{color:#ff7a7a}}
</style></head><body><main><h1>Which voice? Tell Claude the number.</h1>
<p class="meta">{html.escape(meta.get("model", ""))} · same line, same settings · listen with headphones</p>
{f'<div class="line">&ldquo;{html.escape(meta["line"])}&rdquo;</div>' if meta.get("line") else ''}
{"".join(cards)}</main></body></html>"""
    path = out / "board.html"
    path.write_text(doc)
    return path


def open_file(path):
    s = platform.system()
    if s == "Darwin":
        subprocess.run(["open", str(path)])
    elif s == "Windows":
        os.startfile(str(path))  # type: ignore[attr-defined]
    else:
        subprocess.run(["xdg-open", str(path)])


# ---------------------------------------------------------------- save to the character file

def cmd_save(a):
    path = Path(a.character_file).resolve()
    side = {}
    if a.audio:
        sc = Path(a.audio).resolve().with_suffix(".json")
        if not sc.is_file():  # tightened files: look for the original read next to it
            sc = sc.with_name(re.sub(r"_tight$", "", sc.stem) + ".json")
        if sc.is_file():
            side = json.loads(sc.read_text())
        else:
            sys.exit(f"No read record found next to {a.audio}. Pass --voice and --model instead.")
    voice = a.voice or side.get("voice_id")
    if not voice:
        sys.exit("Give --voice ID, or --audio FILE.mp3 from a `read`.")
    info = voice_details(check_token(voice))
    model = side.get("model") or pick_model(a.model)
    a.stability = side.get("stability", a.stability)
    a.similarity = side.get("similarity_boost", a.similarity)
    block = (f"\n## Voice\n\n- Name: {clean(info['name'], 60)}\n- Voice id: {info['id']}\n- Model: {model}\n"
             f"- Settings: stability {a.stability}, similarity_boost {a.similarity}, output {OUTPUT_FORMAT}\n"
             f"- Chosen: {date.today().isoformat()}\n"
             f"- Rule: every episode of this character uses this voice id, this model and these settings.\n")
    if a.note:
        block += f"- Note: {clean(a.note, 160)}\n"
    with open(path, "a") as fh:
        fh.write(block)
    print(f"appended the voice to {path}")


# ---------------------------------------------------------------- check

def cmd_check(a):
    ok = True
    try:
        k = _key()
        print("key: found (not shown)")
    except SystemExit as e:
        print(e); return 1
    for exe in ("ffmpeg", "ffprobe"):
        found = shutil.which(exe)
        print(f"{exe}: {'ok' if found else 'MISSING (brew install ffmpeg)'}")
        ok &= bool(found)
    try:
        ms = models()
        print(f"elevenlabs: reachable, newest speech model for reads: {pick_model('auto', ms)}")
    except ApiError as e:
        print("elevenlabs:", _explain(e)); ok = False
    try:
        s = _request("GET", "/v1/user/subscription")
        left = s["character_limit"] - s["character_count"]
        print(f"plan: {s.get('tier')}, {left:,} characters left this period")
    except (ApiError, KeyError):
        print("plan: could not read the character balance (the key may lack that permission; voicing can still work)")
    tools = [t for t in ("whisperx", "whisper") if shutil.which(t)]
    print("transcript check: " + (f"{tools[0]} installed" if tools else "ElevenLabs speech-to-text (no local whisper)"))
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    v = sub.add_parser("voices")
    v.add_argument("--search"); v.add_argument("--library", action="store_true")
    v.add_argument("--accent"); v.add_argument("--gender"); v.add_argument("--age")
    v.add_argument("--language", default="en"); v.add_argument("--limit", type=int, default=20)
    au = sub.add_parser("audition")
    au.add_argument("--line", required=True); au.add_argument("--voices", required=True)
    au.add_argument("--out", required=True); au.add_argument("--model", default="auto")
    au.add_argument("--no-open", action="store_true")
    r = sub.add_parser("read")
    r.add_argument("script"); r.add_argument("--voice", required=True); r.add_argument("--out", required=True)
    r.add_argument("--model", default="auto")
    r.add_argument("--stability", type=float, default=STABILITY)
    r.add_argument("--similarity", type=float, default=SIMILARITY)
    t = sub.add_parser("tighten")
    t.add_argument("input"); t.add_argument("--out"); t.add_argument("--script")
    t.add_argument("--gap", type=float, default=0.2); t.add_argument("--min-gap", type=float, default=0.28)
    t.add_argument("--tempo", type=float, default=None, help="manual speed-up, overrides --wps")
    t.add_argument("--wps", type=float, default=3.0, help="target words per second (3.0 social, 2.6 YouTube or long explainers)")
    ve = sub.add_parser("verify"); ve.add_argument("audio"); ve.add_argument("script")
    sv = sub.add_parser("save")
    sv.add_argument("character_file"); sv.add_argument("--voice"); sv.add_argument("--audio")
    sv.add_argument("--model", default="auto"); sv.add_argument("--note")
    sv.add_argument("--stability", type=float, default=STABILITY)
    sv.add_argument("--similarity", type=float, default=SIMILARITY)
    b = sub.add_parser("board"); b.add_argument("dir"); b.add_argument("--no-open", action="store_true")
    a = p.parse_args()
    try:
        if a.cmd == "check":
            sys.exit(cmd_check(a))
        elif a.cmd == "voices": cmd_voices(a)
        elif a.cmd == "audition": cmd_audition(a)
        elif a.cmd == "read": cmd_read(a)
        elif a.cmd == "tighten": cmd_tighten(a)
        elif a.cmd == "verify": cmd_verify(a)
        elif a.cmd == "save": cmd_save(a)
        else:
            path = build_board(a.dir)
            if not a.no_open:
                open_file(path)
            print(f"board: {path}")
    except ApiError as e:
        sys.exit(_explain(e))


if __name__ == "__main__":
    main()
