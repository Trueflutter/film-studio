"""Generate through a provider API and log the take automatically (cost included).

Three adapters, one shape: submit JSON → poll → download → `film take add`.
  ark      ByteDance ModelArk / Volcengine (Seedance direct). Supports linked drafts:
           --draft renders a cheap draft; --from-draft <take> renders the final FROM that
           draft task, so the approved composition, motion and performance carry over.
  evolink  EvoLink aggregator (Seedance, Kling, Veo, image models), async tasks.
  fal      fal.ai queue API (hundreds of image/video/audio models).

Keys come from the environment or the studio's .env file (never printed):
  ARK_API_KEY (+ optional ARK_BASE_URL), EVOLINK_API_KEY, FAL_KEY.
Model ids, parameters and prices change monthly: check the provider's model page, pass
provider-specific fields with --param key=value, and keep filmkit/rates.json current.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from .core import KIT_ROOT, PROJECT_ROOT, Production, die, to_float
from .log import add_take

PROVIDERS = {
    "ark": {"key": "ARK_API_KEY", "base": "https://ark.ap-southeast.bytepluses.com/api/v3"},
    "evolink": {"key": "EVOLINK_API_KEY", "base": "https://api.evolink.ai/v1"},
    "fal": {"key": "FAL_KEY", "base": "https://queue.fal.run"},
}
MEDIA_EXT = (".mp4", ".mov", ".webm", ".png", ".jpg", ".jpeg", ".webp", ".wav", ".mp3")


def load_env() -> None:
    """Read KEY=value lines from the project's .env (never printed, never committed)."""
    for env in (PROJECT_ROOT / ".env", KIT_ROOT / ".env"):
        if not env.exists():
            continue
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _key(via: str) -> str:
    name = PROVIDERS[via]["key"]
    val = os.environ.get(name)
    if not val:
        die(f"{name} is not set. Add it to {PROJECT_ROOT / '.env'} (see .env.example).")
    return val


def _http(method: str, url: str, headers: dict, body: dict | None = None, timeout: int = 90) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"User-Agent": "filmkit/1.3", **headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode() or "{}"
    except urllib.error.HTTPError as e:
        die(f"{method} {url.split('?')[0]} → HTTP {e.code}: {e.read().decode()[:600]}")
    except urllib.error.URLError as e:
        raise ConnectionError(str(e))
    return json.loads(raw)


def _value(v: str):
    """--param values: numbers, true/false, JSON objects/arrays, else strings."""
    try:
        return json.loads(v)
    except ValueError:
        return v


def _image_ref(src: str, allow_data_uri: bool) -> str:
    """A URL passes through; a local image or audio file becomes a data URI where allowed."""
    if src.startswith(("http://", "https://", "data:")):
        return src
    p = Path(src).expanduser()
    if not p.exists():
        die(f"file not found: {src}")
    if not allow_data_uri:
        die(f"this provider needs a public URL for reference files; upload {p.name} and pass the URL")
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


HOSTED_TTL_S = 23 * 3600  # EvoLink output links last about 24 hours
UPLOAD_URL = "https://files-api.evolink.ai/api/v1/files/upload/base64"  # files kept 72 hours


def _upload(prod: Production, p: Path) -> str:
    """Upload a local file to EvoLink's file store once; reuse the link until it nearly expires."""
    import hashlib
    cache_f = prod.dir("shots") / ".uploads.json"
    cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
    digest = hashlib.sha1(p.read_bytes()).hexdigest()
    hit = cache.get(digest)
    if hit and hit["until"] - time.time() > 3600:
        return hit["url"]
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    data = f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"
    print(f"  uploading {p.name} to EvoLink (kept 72 hours)")
    r = _http("POST", UPLOAD_URL, {"Authorization": f"Bearer {_key('evolink')}"},
              {"base64_data": data, "file_name": p.name}, timeout=300)
    d = r.get("data") or {}
    link = d.get("file_url")
    if not link:
        die(f"EvoLink upload failed: {json.dumps(r)[:400]}")
    cache[digest] = {"url": link, "until": time.time() + 71 * 3600, "file": p.name}
    cache_f.write_text(json.dumps(cache, indent=1))
    return link


def _hosted_ref(prod: Production, src: str, upload: bool = True) -> str:
    """For providers that only take URLs: a take id (S01_t003) or a logged take's file becomes the
    provider link it came from while that link lives; any other local file is uploaded."""
    if src.startswith(("http://", "https://", "data:")):
        return src
    p = Path(src).expanduser()
    row = None
    for t in prod.takes():
        if t["take"].upper() == p.name.upper() or (p.exists() and t.get("file") and
                                                 (prod.root / t["file"]).resolve() == p.resolve()):
            row = t
            break
    if row:
        link, made = row.get("source_url", ""), to_float(row.get("source_at"))
        if link and time.time() - made < HOSTED_TTL_S:
            return link
        p = prod.root / row["file"]
    if not p.exists():
        die(f"file not found: {src}")
    return _upload(prod, p) if upload else f"<uploaded at run time: {p.name}>"


def _video_url(src: str) -> str:
    if not src.startswith(("http://", "https://")):
        die(f"video references must be public URLs (upload {Path(src).name} to your storage and pass the link)")
    return src


def _find_media_url(obj) -> str | None:
    """Walk any provider response and return the most likely output media URL."""
    found: list[str] = []

    def walk(o, key=""):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, key)
        elif isinstance(o, str) and o.startswith("http"):
            score = 2 if o.split("?")[0].lower().endswith(MEDIA_EXT) else 0
            score += 1 if key in ("video_url", "url", "video", "image", "results", "audio_url") else 0
            if key not in ("status_url", "response_url", "cancel_url", "last_frame_url"):
                found.append((score, o))
    walk(obj)
    found.sort(key=lambda x: -x[0])
    return found[0][1] if found else None


def _download(url: str, dest: Path, tries: int = 3) -> None:
    for n in range(1, tries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "filmkit"})
            with urllib.request.urlopen(req, timeout=120) as r, dest.open("wb") as f:
                while True:
                    chunk = r.read(1 << 18)
                    if not chunk:
                        break
                    f.write(chunk)
            return
        except (TimeoutError, urllib.error.URLError, ConnectionError) as e:
            if n == tries:
                die(f"download failed after {tries} tries ({e}). The job is done and still pending: "
                    "run `film jobs --resume` to collect it without paying again.")
            print(f"  download hiccup ({e}); retrying")
            time.sleep(3 * n)


def _poll(fetch, done, failed, label: str, max_wait: int = 900, every: int = 5) -> dict:
    t0, last = time.time(), ""
    while True:
        try:
            d = fetch()
        except ConnectionError as e:  # the job keeps running server-side; keep asking
            print(f"  poll hiccup ({e}); retrying")
            d = {}
        st = str(d.get("status", "")).lower()
        if st and st != last:
            print(f"  {label}: {st}")
            last = st
        if st in done:
            return d
        if st in failed:
            die(f"generation failed: {json.dumps(d)[:600]}")
        if time.time() - t0 > max_wait:
            die(f"still '{st}' after {max_wait}s. It is still recorded as pending: run `film jobs --resume` later.")
        time.sleep(every)


def rate_for(via: str, model: str, res: str) -> float | None:
    rates_file = Path(__file__).with_name("rates.json")
    if not rates_file.exists():
        return None
    rates = json.loads(rates_file.read_text()).get("per_second", {})
    for key in (f"{via}:{model}:{res}", f"{via}:{model}"):
        if key in rates:
            return rates[key]
    # A key's model part contained in the real id (e.g. "seedance-2-5" in "dreamina-seedance-2-5-260628").
    for key, value in rates.items():
        parts = key.split(":")
        if len(parts) >= 2 and parts[0] == via and parts[1] and parts[1] in model \
                and (len(parts) < 3 or parts[2] == res):
            return value
    return None


def credit_usd(tool: str) -> float | None:
    """USD per credit for a credit platform (rates.json "per_credit"), e.g. aristotto."""
    rates = json.loads((KIT_ROOT / "filmkit" / "rates.json").read_text())
    v = rates.get("per_credit", {}).get((tool or "").lower())
    return float(v) if v is not None else None


def build_payload(via: str, model: str, prompt: str, images: list[str], image_role: str,
                  duration: int | None, res: str, aspect: str, audio: bool | None,
                  seed: str, draft: bool, draft_task: str | None, params: dict,
                  kind: str = "video", audio_refs: list[str] | None = None,
                  audio_role: str = "", video_refs: list[str] | None = None) -> tuple[str, dict]:
    """Return (url, body) for the provider's create call."""
    base = os.environ.get(f"{via.upper()}_BASE_URL", PROVIDERS[via]["base"]).rstrip("/")
    if via == "ark":
        if draft_task:
            # Promotion: the final inherits prompt, refs, seed, duration, ratio and audio from
            # the draft. The API rejects those fields here; resolution must be 1080p.
            body = {"model": model, "content": [{"type": "draft_task", "draft_task": {"id": draft_task}}],
                    "resolution": res or "1080p"}
            return f"{base}/contents/generations/tasks", {**body, **params}
        content = [{"type": "text", "text": prompt}]
        for i, img in enumerate(images):
            role = image_role or ("first_frame" if i == 0 else "reference_image")
            content.append({"type": "image_url", "image_url": {"url": _image_ref(img, True)}, "role": role})
        for a in audio_refs or []:
            content.append({"type": "audio_url", "audio_url": {"url": _image_ref(a, True)},
                            "role": audio_role or "reference_audio"})
        for v in video_refs or []:
            content.append({"type": "video_url", "video_url": {"url": _video_url(v)},
                            "role": "reference_video"})
        body = {"model": model, "content": content}
        opt = {"resolution": "480p" if draft else res, "ratio": aspect, "duration": duration,
               "generate_audio": audio, "seed": int(seed) if seed else None,
               "draft": True if draft else None, "return_last_frame": True}
        body.update({k: v for k, v in opt.items() if v not in (None, "")})
        return f"{base}/contents/generations/tasks", {**body, **params}
    if via == "evolink":
        body = {"model": model, "prompt": prompt}
        if images:
            body["image_urls"] = [_image_ref(i, False) for i in images]
        if audio_refs:
            body["audio_urls"] = [_image_ref(a, False) for a in audio_refs]
        if video_refs:
            body["video_urls"] = [_video_url(v) for v in video_refs]
        if kind == "image":  # size/quality for images go in via --param (e.g. size=1536x1024)
            return f"{base}/images/generations", {**body, "n": 1, **params}
        # image-to-video takes its shape from the start frame (EvoLink rejects anything but "adaptive")
        opt = {"duration": duration, "quality": res,
               "aspect_ratio": "adaptive" if "image-to-video" in model else aspect, "generate_audio": audio,
               "seed": int(seed) if seed else None}
        body.update({k: v for k, v in opt.items() if v not in (None, "")})
        return f"{base}/videos/generations", {**body, **params}
    # fal: field names differ per model; the common ones here, the rest via --param.
    body = {"prompt": prompt}
    if images:
        refs = [_image_ref(i, True) for i in images]
        body["image_url"] = refs[0]
        if len(refs) > 1:
            body["image_urls"] = refs
    if audio_refs:
        body["audio_url"] = _image_ref(audio_refs[0], True)
    if video_refs:
        body["video_url"] = _video_url(video_refs[0])
    opt = {"duration": duration, "resolution": res, "aspect_ratio": aspect,
           "generate_audio": audio, "seed": int(seed) if seed else None}
    body.update({k: v for k, v in opt.items() if v not in (None, "")})
    return f"{base}/{model}", {**body, **params}


def generate(prod: Production, shot: str, via: str, model: str, prompt_file: str | None,
             images: list[str], image_role: str = "", duration: int | None = None, res: str = "",
             aspect: str = "", audio: bool | None = None, seed: str = "", count: int = 1,
             stage: str = "", draft: bool = False, from_draft: str | None = None,
             cost: str = "", params: list[str] | None = None, mode: str = "",
             kind: str = "video", dry_run: bool = False, audio_refs: list[str] | None = None,
             audio_role: str = "", video_refs: list[str] | None = None) -> list[dict]:
    load_env()
    if via not in PROVIDERS:
        die(f"--via must be one of {', '.join(PROVIDERS)}")
    extra = {}
    for p in params or []:
        if "=" not in p:
            die(f"--param expects key=value, got {p}")
        k, v = p.split("=", 1)
        extra[k] = _value(v)
    prompt = ""
    if prompt_file:
        pf = Path(prompt_file)
        if not pf.exists():
            die(f"prompt file not found: {prompt_file}")
        prompt = pf.read_text(encoding="utf-8").strip()
    draft_task = None
    cost_duration = float(duration or 0)
    if from_draft:
        if via != "ark":
            die("--from-draft is a ModelArk feature (linked draft→final). Elsewhere: lock the prompt, "
                "start frame and seed from the draft and render again, or upscale the locked draft.")
        src = next((t for t in prod.takes() if t["take"].upper() == from_draft.upper()), None)
        if not src or not src.get("job"):
            die(f"{from_draft} has no provider job id in takes.csv (was it generated with film gen --via ark --draft?)")
        draft_task = src["job"]
        model = model or src["model"]
        prompt_file = prompt_file or src["prompt"]
        res = res or "1080p"
        cost_duration = cost_duration or to_float(src.get("duration_s"))  # the final inherits it
        if src.get("verdict") != "select":
            print(f"note: {from_draft} is not rated 'select'. Promote only drafts you have approved.")
    if not prompt and not draft_task:
        die("--prompt-file is required (prompts live in files so every take is reproducible)")
    stage = stage or ("draft" if draft else "final" if from_draft else "draft")
    if draft:
        res = "480p"  # Seedance 2.5 drafts are always 480p
    aspect = aspect or prod.cfg["aspect"]
    payload_images = [_hosted_ref(prod, i, not dry_run) for i in images] if via == "evolink" else images
    if via == "evolink":
        audio_refs = [_hosted_ref(prod, a, not dry_run) for a in audio_refs or []]
    url, body = build_payload(via, model, prompt, payload_images, image_role, duration, res, aspect,
                              audio, seed, draft, draft_task, dict(extra), kind, audio_refs, audio_role,
                              video_refs)
    if dry_run:
        shown = json.loads(json.dumps(body))
        for c in shown.get("content", []):
            for key in ("image_url", "audio_url"):
                if isinstance(c, dict) and key in c and c[key]["url"].startswith("data:"):
                    c[key]["url"] = c[key]["url"][:40] + "…"
        for k in ("image_url", "image_urls", "audio_url", "audio_urls"):
            v = shown.get(k)
            if isinstance(v, str) and v.startswith("data:"):
                shown[k] = v[:40] + "…"
            elif isinstance(v, list):
                shown[k] = [x[:40] + "…" if isinstance(x, str) and x.startswith("data:") else x for x in v]
        print(f"POST {url}\n{json.dumps(shown, indent=2, ensure_ascii=False)}")
        return []

    key = _key(via)
    headers = {"Authorization": f"Key {key}"} if via == "fal" else {"Authorization": f"Bearer {key}"}
    rate = rate_for(via, model, res)
    if not cost and rate is None:
        print("warning: no price known for this model/resolution. Pass --cost or add it to "
              "filmkit/rates.json, otherwise your cost report under-counts.")
    rows = []
    for n in range(count):
        print(f"[{n + 1}/{count}] {via} {model} {res or ''} {'DRAFT' if draft else ''}".rstrip())
        created = _http("POST", url, headers, body)
        job = created.get("request_id" if via == "fal" else "id", "")
        rec = {"job": job, "shot": shot, "via": via, "model": model, "stage": stage, "res": res,
               "mode": mode or ("draft→final" if draft_task else "draft" if draft else ""),
               "prompt": str(prompt_file or ""), "refs": " ".join(images + (audio_refs or []) + (video_refs or [])),
               "seed": seed, "cost": cost, "rate": rate, "duration": cost_duration,
               "notes": f"from {from_draft}" if from_draft else "",
               "poll": created.get("status_url") if via == "fal" else
                       f"{url}/{job}" if via == "ark" else f"{url.rsplit('/', 2)[0]}/tasks/{job}",
               "response": created.get("response_url", "")}
        # Record the job before waiting: if this command is interrupted, `film jobs --resume`
        # finishes it (the provider is already billing for it).
        _pending(prod, add=rec)
        result = created if via == "evolink" and (created.get("results") or created.get("data")) \
            else _wait(rec, headers)
        rows.append(_finish(prod, rec, result))
    return rows


def _pending_file(prod: Production) -> Path:
    return prod.dir("shots") / ".pending_jobs.json"


def _pending(prod: Production, add: dict | None = None, remove: str | None = None) -> list[dict]:
    f = _pending_file(prod)
    jobs = json.loads(f.read_text()) if f.exists() else []
    if add:
        jobs.append(add)
    if remove:
        jobs = [j for j in jobs if j["job"] != remove]
    if add or remove:
        f.write_text(json.dumps(jobs, indent=1))
    return jobs


def _wait(rec: dict, headers: dict) -> dict:
    via, label = rec["via"], rec["job"][:14]
    if via == "fal":
        _poll(lambda: _http("GET", rec["poll"], headers), {"completed"}, {"failed", "error"}, label)
        return _http("GET", rec["response"], headers)
    if via == "ark":
        return _poll(lambda: _http("GET", rec["poll"], headers), {"succeeded"},
                     {"failed", "cancelled", "expired"}, label)
    return _poll(lambda: _http("GET", rec["poll"], headers),
                 {"completed", "succeeded", "success"}, {"failed", "error"}, label)


def _finish(prod: Production, rec: dict, result: dict) -> dict:
    media = _find_media_url(result.get("content", result) if rec["via"] == "ark" else result)
    if not media:
        die(f"finished but no media URL found in the response: {json.dumps(result)[:600]}")
    ext = Path(media.split("?")[0]).suffix.lower() or ".mp4"
    with tempfile.TemporaryDirectory() as tmp:
        local = Path(tmp) / f"out{ext}"
        _download(media, local)
        dur_s = rec["duration"] or result.get("duration") or 0
        spent = rec["cost"] or (f"{rec['rate'] * float(dur_s):.2f}" if rec["rate"] and dur_s else "")
        row = add_take(prod, rec["shot"], str(local), stage=rec["stage"], tool=rec["via"], model=rec["model"],
                       mode=rec["mode"], res=rec["res"], cost=spent, prompt=rec["prompt"], refs=rec["refs"],
                       seed=str(result.get("seed", rec["seed"]) or ""), move=True, notes=rec["notes"])
    rows_all = prod.takes()
    for r in rows_all:
        if r["take"] == row["take"]:
            r["job"] = rec["job"]
            r["source_url"], r["source_at"] = media, str(int(time.time()))
    prod.save_takes(rows_all)
    _pending(prod, remove=rec["job"])
    row["job"] = rec["job"]
    print(f"  logged {row['take']} → {row['file']}" + (f"  (${to_float(row['cost_usd']):.2f})" if row["cost_usd"] else ""))
    return row


def jobs(prod: Production, resume: bool = False) -> None:
    """List generations submitted but not yet logged; --resume waits for them and logs them."""
    load_env()
    pending = _pending(prod)
    if not pending:
        print("no pending jobs")
        return
    for rec in pending:
        print(f"{rec['job']}  {rec['shot']}  {rec['via']} {rec['model']} {rec['res']}  {rec['stage']}")
        if resume:
            key = _key(rec["via"])
            headers = {"Authorization": f"Key {key}"} if rec["via"] == "fal" else {"Authorization": f"Bearer {key}"}
            _finish(prod, rec, _wait(rec, headers))
