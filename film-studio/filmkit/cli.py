"""`film`: the command line for a production. Run `film <command> -h` for details."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from . import __version__
from .core import (to_float, ASPECTS, CURRENT, KIT_ROOT, PRODUCTIONS, TEMPLATE, FilmError, create_production, die,
                   find_production, resolve_path, slugify)


def R(p):
    """Resolve a path argument from the current folder or the current production."""
    return resolve_path(p) if p else p


def _floats(s: str) -> list[float]:
    return [float(x) for x in s.split(",") if x.strip()]


def cmd_new(a):
    base = find_production(a.base) if a.base else None
    prod = create_production(a.title, a.format, a.aspect, a.fps, a.duration, a.budget, a.slug, base)
    cfg = prod.cfg
    if base:
        print(f"from {base.root.name}: brief, characters, locations, style, graphics and sound kit copied")
    print(f"created {prod.root}  [{cfg['format']} · {cfg['aspect']} · {cfg['target_duration_s']}s · ${cfg['budget_usd']:.0f}]\n"
          "now current. Paths like 04_shots/... work from anywhere in your studio.\n"
          "Start with 00_brief/brief.md, then `film status`. To change aspect or budget later, edit production.json.")


def cmd_use(a):
    if not (PRODUCTIONS / a.slug / "production.json").exists():
        die(f"no production '{a.slug}' in {PRODUCTIONS}")
    CURRENT.write_text(a.slug)
    print(f"current production: {a.slug}")


def cmd_list(a):
    cur = CURRENT.read_text().strip() if CURRENT.exists() else ""
    rows = sorted(p.parent.name for p in PRODUCTIONS.glob("*/production.json"))
    print("\n".join(("* " if r == cur else "  ") + r for r in rows) or "no productions yet: film new \"Title\"")


def cmd_status(a):
    from .log import status
    print(status(find_production(a.prod)))


def cmd_character(a):
    prod = find_production(a.prod)
    src = TEMPLATE / "02_design" / "characters" / "_template"
    dest = prod.dir("design") / "characters" / slugify(a.name)
    if dest.exists():
        die(f"{dest} already exists")
    shutil.copytree(src, dest)
    for f in dest.rglob("*.md"):
        f.write_text(f.read_text(encoding="utf-8").replace("{{name}}", a.name), encoding="utf-8")
    print(f"created {prod.rel(dest)}: fill bible.md, then build the reference pack into refs/")


def cmd_take(a):
    from . import log
    prod = find_production(a.prod)
    if a.take_cmd == "add":
        cost = a.cost
        if a.credits:  # credit platforms (Aristotto): convert with the per-credit rate in rates.json
            from .gen import credit_usd
            rate = credit_usd(a.tool)
            if rate is None:
                print(f"note: no credit rate for '{a.tool}' in rates.json; logging without a cost")
            else:
                cost = cost or f"{float(a.credits) * rate:.2f}"
        notes = (a.notes + " " if a.notes else "") + (f"{a.credits} credits" if a.credits else "")
        src, move = a.file, a.move
        with tempfile.TemporaryDirectory() as tmp:
            if src.startswith(("http://", "https://")):  # a provider link: download it now (links expire)
                from .gen import _download
                name = Path(src.split("?")[0]).name or "take.mp4"
                local = Path(tmp) / name
                _download(src, local)
                src, move = str(local), True
            else:
                src = str(R(src))
            row = log.add_take(prod, a.shot, src, stage=a.stage, tool=a.tool, model=a.model, mode=a.mode,
                               res=a.res, duration=a.duration or "", cost=cost, prompt=str(R(a.prompt)) if a.prompt else "",
                               refs=a.refs, seed=a.seed, notes=notes.strip(), move=move)
        if a.file.startswith(("http://", "https://")):
            rows = prod.takes()
            for r in rows:
                if r["take"] == row["take"]:
                    r["source_url"], r["source_at"] = a.file, str(int(time.time()))
            prod.save_takes(rows)
        print(f"logged {row['take']} → {row['file']}" + (f"  (${to_float(cost):.2f})" if cost else ""))
    elif a.take_cmd == "rate":
        row = log.rate_take(prod, a.take, a.verdict, a.fail, a.note)
        print(f"{row['take']}: {row['verdict']} {row['fail']}".strip())
    elif a.take_cmd == "list":
        print(log.list_takes(prod, a.shot))
    else:
        print("fail codes (use with `film take rate <take> reject --fail CODE+CODE`):")
        for k, v in log.FAIL_CODES.items():
            print(f"  {k:<12} {v}")


def cmd_gen(a):
    from .gen import generate
    prod = find_production(a.prod)
    audio = True if a.audio else (False if a.no_audio else None)
    local = lambda xs: [x if x.startswith(("http://", "https://", "data:")) else str(R(x)) for x in xs or []]
    generate(prod, a.shot.upper(), a.via, a.model, str(R(a.prompt_file)) if a.prompt_file else None,
             local(a.image), a.image_role, a.duration, a.res, a.aspect, audio, a.seed, a.count, a.stage,
             a.draft, a.from_draft, a.cost, a.param, a.mode, "image" if a.image_gen else "video", a.dry_run,
             local(a.audio_ref), a.audio_role, a.video_ref or [])


def cmd_jobs(a):
    from .gen import jobs
    jobs(find_production(a.prod), a.resume)


def cmd_cost(a):
    from .log import cost_report, economics
    prod = find_production(a.prod)
    if a.check:
        from .core import to_float
        spent, budget = economics(prod)["total"], to_float(prod.cfg.get("budget_usd"))
        print(f"{prod.slug}: ${spent:.2f} of ${budget:.2f}")
        if budget and spent >= budget:
            print("over budget: raise it in production.json on purpose, or stop generating", file=sys.stderr)
            raise SystemExit(2)
        return
    report = cost_report(prod)
    print(report)
    if a.save:
        out = prod.dir("shots") / "cost_report.md"
        out.write_text(report)
        print(f"saved {prod.rel(out)}")


def cmd_frames(a):
    from .media import frames
    out = Path(a.out) if a.out else R(a.video).parent / "frames"
    for p in frames(R(a.video), out, _floats(a.at) if a.at else None, a.every, a.last, a.width):
        print(p)


def cmd_contact(a):
    from .media import contact_sheet
    prod = None
    videos = [R(v) for v in a.videos]
    if a.shot:
        prod = find_production(a.prod)
        videos += [prod.root / t["file"] for t in prod.takes()
                   if t["shot"] == a.shot.upper() and t["file"].lower().endswith((".mp4", ".mov", ".webm"))]
    if not videos:
        die("give video files or --shot S03")
    out = Path(a.out) if a.out else (
        (prod.dir("shots") / a.shot.upper() / f"{a.shot.upper()}_contact.png") if prod else videos[0].with_suffix(".contact.png"))
    print(contact_sheet(videos, out, a.cols, a.width))


def cmd_boards(a):
    from .pages import storyboard
    print(storyboard(find_production(a.prod)))


def cmd_dailies(a):
    from .pages import dailies
    print(dailies(find_production(a.prod)))


def cmd_board(a):
    """Options board: from logged takes (--shot/--stage) or files ('path' or 'path|caption')."""
    from .pages import board
    prod = find_production(a.prod)
    items = []
    if a.shot:
        for t in prod.takes():
            if t["shot"].upper() == a.shot.upper() and (not a.stage or t["stage"] == a.stage):
                items.append((prod.root / t["file"], f"{t['take']} {t.get('model', '')}".strip()))
    for f in a.files or []:
        path, _, cap = f.partition("|")
        items.append((Path(str(R(path.strip()))), cap.strip() or Path(path).stem))
    if not items:
        die("nothing to show: pass --shot (with --stage) or files")
    out = board(prod, a.title, items, a.ask)
    print(out)
    if not a.no_open:
        opener = {"darwin": ["open"], "win32": ["cmd", "/c", "start", ""]}.get(sys.platform, ["xdg-open"])
        try:
            subprocess.Popen(opener + [str(out)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            pass


def cmd_animatic(a):
    from .media import animatic
    print(animatic(find_production(a.prod), R(a.audio) if a.audio else None))


def cmd_assemble(a):
    from .media import assemble
    prod = find_production(a.prod)
    print(assemble(prod, R(a.edl) if a.edl else None, a.trim, a.fit))


def cmd_review(a):
    from .review import review
    print(review(find_production(a.prod), R(a.cut) if a.cut else None, R(a.edl) if a.edl else None,
                 a.bpm, a.offset, a.threshold))


def cmd_teardown(a):
    from .review import teardown
    print(teardown(R(a.video), Path(a.out) if a.out else None, a.threshold))


def cmd_mix(a):
    from .sound import mix, parse_placed
    prod = find_production(a.prod)
    placed = lambda xs: [(R(p), at) for p, at in (parse_placed(x) for x in xs or [])]
    out = mix(prod, R(a.video), R(a.dialogue), R(a.music), placed(a.ambience), placed(a.fx),
              a.music_db, a.ambience_db, a.target, not a.ignore_video_audio)
    print(out)


def cmd_qc(a):
    from .qc import qc
    print(qc(find_production(a.prod), R(a.file), a.spec))


def cmd_captions(a):
    from . import captions as cap
    from .qc import check_subs
    if a.cap_cmd == "check":
        print(check_subs(R(a.srt), max_cps=a.cps))
        return
    if a.cap_cmd == "transcribe":
        out = Path(a.out) if a.out else R(a.media).with_suffix(".words.json")
        print(cap.transcribe(R(a.media), out, a.lang, a.speakers))
        return
    if a.cap_cmd == "burn":
        out = Path(a.out) if a.out else R(a.video).with_name(R(a.video).stem + "_captioned.mp4")
        print(cap.burn(R(a.video), R(a.ass), out))
        return
    # build
    words = cap.load_words(R(a.words))
    style = cap.STYLES[a.style]
    if a.lines:
        events, notes = cap.from_lines(words, R(a.lines).read_text(encoding="utf-8").splitlines())
        for n in notes:
            print("check:", n)
    else:
        if any(cap.ARABIC.search(w["text"]) for w in words):
            print("warning: Arabic/RTL text. Auto-grouping splits phrases (e.g. 'الذكاء / الاصطناعي'). "
                  "Author your lines and pass --lines. Check one burnt frame for boxes (needs libass with HarfBuzz).")
        events = cap.segment(words, a.max_words or style["words"], style["dur"])
    if a.video:
        from . import ff
        info = ff.probe(R(a.video))
        w, h = info["width"], info["height"]
    else:
        prod = find_production(a.prod)
        w, h = prod.size
    base = Path(a.out) if a.out else R(a.words).with_suffix("")
    ass = base.with_suffix(f".{a.style}.ass")
    ass.write_text(cap.render_ass(events, w, h, a.style, a.accent, a.colour, a.y), encoding="utf-8")
    srt = base.with_suffix(".srt")
    srt.write_text(cap.to_srt(events), encoding="utf-8")
    print(f"{len(events)} captions\n{ass}\n{srt}  (upload this one to platforms as closed captions)")
    print(check_subs(srt, max_cps=a.cps))


def cmd_deliver(a):
    from .deliver import deliver
    prod = find_production(a.prod)
    for p in deliver(prod, R(a.master), [x.strip() for x in a.aspects.split(",")], a.fit, a.lufs):
        print(p)


def cmd_overlay(a):
    from .deliver import overlay
    from .sound import parse_placed
    placed = [(R(p), at) for p, at in (parse_placed(x) for x in a.graphics)]
    print(overlay(R(a.video), placed, Path(a.out) if a.out else None))


def cmd_doctor(a):
    ok = True
    print(f"filmkit {__version__} · python {sys.version.split()[0]}")
    if sys.version_info < (3, 9):
        print("  ✗ python 3.9+ required"); ok = False
    from . import ff
    ffm = ff.find("ffmpeg")
    print(f"  {'✓' if ffm else '✗'} ffmpeg {ffm or f'missing ({ff.INSTALL_HINT})'}")
    ok &= bool(ffm)
    fp = ff.find("ffprobe")
    print(f"  {'✓' if fp else '·'} ffprobe {fp or 'missing (optional)'}")
    node = shutil.which("node")
    ver = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip() if node else ""
    major = int(ver.lstrip("v").split(".")[0]) if ver[1:2].isdigit() else 0
    print(f"  {'✓' if major >= 22 else '·'} node {ver or 'missing'}"
          f"{'' if major >= 22 else ' (optional: the graphics skill needs Node 22+ for HyperFrames)'}")
    if ffm:
        filters = subprocess.run([ffm, "-hide_banner", "-filters"], capture_output=True, text=True).stdout
        for f, why in (("subtitles", "burnt-in captions (libass)"), ("sidechaincompress", "music ducking"),
                       ("ebur128", "loudness QC")):
            has = f" {f} " in filters
            ok &= has
            print(f"  {'✓' if has else '✗'} {f:<18} {why}{'' if has else ' (not in this build)'}")
        if " subtitles " not in filters:
            print(f"    captions need an ffmpeg with libass: {ff.INSTALL_HINT}. "
                  "film finds Homebrew's ffmpeg-full by itself; no PATH change needed.")
    from .gen import PROVIDERS, load_env
    load_env()
    for via, p in PROVIDERS.items():
        print(f"  {'✓' if os.environ.get(p['key']) else '·'} {p['key']:<18} ({via}) {'set' if os.environ.get(p['key']) else 'not set'}")
    print(f"  · {'Aristotto':<18} (pictures and video) signs in through Claude: /mcp, then aristotto")
    el = os.environ.get("ELEVENLABS_API_KEY")
    print(f"  {'✓' if el else '·'} {'ELEVENLABS_API_KEY':<18} (captions transcribe, voices) {'set' if el else 'not set'}")
    print(f"  film lives at {KIT_ROOT / 'bin' / 'film'} (outside Claude Code: alias film=\"{KIT_ROOT / 'bin' / 'film'}\")")
    print("  ✓ studio ready" if ok else "  fix the ✗ items above")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="film", description="Production spine for AI filmmaking.")
    ap.add_argument("--version", action="version", version=__version__)
    ap.add_argument("--prod", help="production slug or path (default: current)")
    sub = ap.add_subparsers(dest="cmd", required=True, metavar="command")

    p = sub.add_parser("new", help="create a production from the template")
    p.add_argument("title")
    p.add_argument("--format", choices=["film", "ad", "social"], help="default: film, or --from's")
    p.add_argument("--aspect", choices=list(ASPECTS), help="default: 16:9 film, 9:16 ad/social")
    p.add_argument("--fps", type=float, help="default: 24")
    p.add_argument("--duration", type=int, help="target seconds (default: film 60, ad 30, social 15)")
    p.add_argument("--budget", type=float, help="generation budget in USD (default: 60)")
    p.add_argument("--slug")
    p.add_argument("--from", dest="base", metavar="PRODUCTION",
                   help="start from an earlier production: reuse its brief, cast, look, graphics and sound kit")
    p.set_defaults(fn=cmd_new)

    p = sub.add_parser("use", help="switch the current production"); p.add_argument("slug"); p.set_defaults(fn=cmd_use)
    sub.add_parser("list", help="list productions").set_defaults(fn=cmd_list)
    sub.add_parser("status", help="where is this production?").set_defaults(fn=cmd_status)
    p = sub.add_parser("character", help="add a character bible folder"); p.add_argument("name"); p.set_defaults(fn=cmd_character)

    p = sub.add_parser("take", help="log, rate and list takes")
    ts = p.add_subparsers(dest="take_cmd", required=True)
    t = ts.add_parser("add", help="log a generated file as a take of a shot")
    t.add_argument("shot"); t.add_argument("file", help="a local file or a provider link (downloaded now)")
    t.add_argument("--stage", default="draft", choices=["still", "draft", "final", "upscale", "fix"])
    for f in ("tool", "model", "mode", "res", "duration", "cost", "prompt", "refs", "seed", "notes"):
        t.add_argument(f"--{f}", default="")
    t.add_argument("--credits", default="", help="credits the platform charged (Aristotto); costed via rates.json")
    t.add_argument("--move", action="store_true", help="move instead of copy")
    t = ts.add_parser("rate", help="select / maybe / reject a take, with failure codes")
    t.add_argument("take"); t.add_argument("verdict", choices=["select", "maybe", "reject"])
    t.add_argument("--fail", default="", help="e.g. PROMPT+CAMERA (film take codes)")
    t.add_argument("--note", default="")
    t = ts.add_parser("list"); t.add_argument("--shot")
    ts.add_parser("codes", help="list diagnosis codes")
    p.set_defaults(fn=cmd_take)

    p = sub.add_parser("gen", help="generate via a provider API and log the take")
    p.add_argument("shot")
    p.add_argument("--via", required=True, choices=["ark", "evolink", "fal"])
    p.add_argument("--model", default="")
    p.add_argument("--prompt-file")
    p.add_argument("--image", action="append", help="start frame / reference: path, URL or a take id (EvoLink reuses the take's link); repeatable")
    p.add_argument("--image-role", default="", help="ark: first_frame | last_frame | reference_image")
    p.add_argument("--audio-ref", action="append", help="voice/audio reference for lip sync (path or URL)")
    p.add_argument("--audio-role", default="", help="ark audio role (default reference_audio; check provider docs)")
    p.add_argument("--video-ref", action="append", help="video reference (public URL): camera/motion/blockout")
    p.add_argument("--duration", type=int)
    p.add_argument("--res", default="", help="e.g. 480p, 720p, 1080p")
    p.add_argument("--aspect", default="", help="default: production aspect")
    p.add_argument("--audio", action="store_true"); p.add_argument("--no-audio", action="store_true")
    p.add_argument("--seed", default="")
    p.add_argument("--count", type=int, default=1, help="takes to render (generate 2, pick 1)")
    p.add_argument("--stage", default="", choices=["", "still", "draft", "final", "upscale", "fix"])
    p.add_argument("--draft", action="store_true", help="ark: cheap linked draft (Seedance 2.5)")
    p.add_argument("--from-draft", help="ark: render the final from this approved draft take")
    p.add_argument("--image-gen", action="store_true", help="evolink: image model endpoint")
    p.add_argument("--cost", default="", help="USD for this take (else looked up in rates.json)")
    p.add_argument("--mode", default="", help="label: t2v, i2v, ref, multishot, v2v ...")
    p.add_argument("--param", action="append", help="extra provider field key=value; repeatable")
    p.add_argument("--dry-run", action="store_true", help="print the request, spend nothing")
    p.set_defaults(fn=cmd_gen)

    p = sub.add_parser("jobs", help="generations submitted but not yet logged")
    p.add_argument("--resume", action="store_true", help="wait for them and log them")
    p.set_defaults(fn=cmd_jobs)

    p = sub.add_parser("cost", help="economics: spend, cost per usable shot, exploration vs production")
    p.add_argument("--save", action="store_true")
    p.add_argument("--check", action="store_true", help="exit 2 if spend >= budget (for hooks)")
    p.set_defaults(fn=cmd_cost)

    p = sub.add_parser("frames", help="stills from motion: --at 1.2,3 | --every 0.5 | --last")
    p.add_argument("video"); p.add_argument("--at"); p.add_argument("--every", type=float, default=0)
    p.add_argument("--last", action="store_true"); p.add_argument("--width", type=int, default=0)
    p.add_argument("--out"); p.set_defaults(fn=cmd_frames)

    p = sub.add_parser("contact", help="contact sheet of takes (one row per take)")
    p.add_argument("videos", nargs="*"); p.add_argument("--shot")
    p.add_argument("--cols", type=int, default=6); p.add_argument("--width", type=int, default=320)
    p.add_argument("--out"); p.set_defaults(fn=cmd_contact)

    sub.add_parser("boards", help="printable storyboard page from shotlist + boards").set_defaults(fn=cmd_boards)
    sub.add_parser("dailies", help="review page of every take, grouped by shot").set_defaults(fn=cmd_dailies)
    p = sub.add_parser("board", help="an options page to choose from: images, clips, audio or text cards (.md) (opens in the browser)")
    p.add_argument("title"); p.add_argument("files", nargs="*", help="path or 'path|caption'")
    p.add_argument("--shot"); p.add_argument("--stage", default="")
    p.add_argument("--ask", default="I pick", help="the sentence the copied pick starts with")
    p.add_argument("--no-open", action="store_true"); p.set_defaults(fn=cmd_board)
    p = sub.add_parser("animatic", help="timed animatic from boards + shot durations")
    p.add_argument("--audio", help="temp VO / music to lay under it"); p.set_defaults(fn=cmd_animatic)

    p = sub.add_parser("assemble", help="rough cut from 06_edit/cut.txt")
    p.add_argument("--edl"); p.add_argument("--trim", type=float, default=0.1, help="head/tail trim for whole takes")
    p.add_argument("--fit", default="crop", choices=["crop", "pad"]); p.set_defaults(fn=cmd_assemble)

    p = sub.add_parser("review", help="every join of a cut as frames, the rhythm, cuts against the beat")
    p.add_argument("cut", nargs="?", help="default: the latest 06_edit/cuts/cut_vNNN.mp4 (an editor export works too)")
    p.add_argument("--edl", help="the cut list that made it (default: the copy saved beside the cut)")
    p.add_argument("--bpm", type=float, default=0, help="music tempo: show where each cut sits on the beat")
    p.add_argument("--offset", type=float, default=0, help="seconds into the cut of the music's first beat")
    p.add_argument("--threshold", type=float, default=0.3, help="scene-change sensitivity when finding cuts by picture")
    p.set_defaults(fn=cmd_review)

    p = sub.add_parser("teardown", help="cut list, shot lengths and one frame per shot of a reference film")
    p.add_argument("video")
    p.add_argument("--threshold", type=float, default=0.3, help="scene-change sensitivity (lower finds softer cuts)")
    p.add_argument("--out", help="folder for the sheets and teardown.md (default: <video>_teardown/)")
    p.set_defaults(fn=cmd_teardown)

    p = sub.add_parser("mix", help="dialogue + ducked music + beds + fx, loudness-matched")
    p.add_argument("--video"); p.add_argument("--dialogue"); p.add_argument("--music")
    p.add_argument("--ambience", action="append", help="bed; add @seconds to start it later")
    p.add_argument("--fx", action="append", help="effect; place it with @seconds, e.g. sfx/door.wav@4.2")
    p.add_argument("--music-db", type=float, default=-18); p.add_argument("--ambience-db", type=float, default=-24)
    p.add_argument("--target", type=float, help="LUFS (default: production.json)")
    p.add_argument("--ignore-video-audio", action="store_true"); p.set_defaults(fn=cmd_mix)

    p = sub.add_parser("qc", help="technical QC + creative rubric sheet")
    p.add_argument("file"); p.add_argument("--spec", choices=["social", "web", "broadcast", "cinema-ish"])
    p.set_defaults(fn=cmd_qc)

    p = sub.add_parser("captions", help="transcribe, build styled captions, check, burn in")
    cs = p.add_subparsers(dest="cap_cmd", required=True)
    c = cs.add_parser("transcribe", help="word-timed transcript via ElevenLabs Scribe")
    c.add_argument("media"); c.add_argument("--lang", default="", help="e.g. en, ar")
    c.add_argument("--speakers", type=int, default=0); c.add_argument("--out")
    c = cs.add_parser("build", help="words/SRT → styled .ass (+ .srt)")
    c.add_argument("words", help="words .json (Scribe/WhisperX/filmkit) or .srt")
    c.add_argument("--lines", help="authored caption lines, one per line (recommended)")
    c.add_argument("--style", default="social", choices=["social", "clean", "film"])
    c.add_argument("--video", help="read frame size from this video (else the production's)")
    c.add_argument("--accent", default="#F5C542", help="highlight colour for the spoken word")
    c.add_argument("--colour", default="#FFFFFF")
    c.add_argument("--y", type=float, help="baseline as a fraction of height (e.g. 0.62)")
    c.add_argument("--max-words", type=int, default=0)
    c.add_argument("--cps", type=float, default=17); c.add_argument("--out")
    c = cs.add_parser("check", help="readability check of an SRT")
    c.add_argument("srt"); c.add_argument("--cps", type=float, default=17)
    c = cs.add_parser("burn", help="burn a .ass into the picture (bundled fonts)")
    c.add_argument("video"); c.add_argument("ass"); c.add_argument("--out")
    p.set_defaults(fn=cmd_captions)

    p = sub.add_parser("deliver", help="aspect variants + loudness to spec")
    p.add_argument("master"); p.add_argument("--aspects", default="16:9")
    p.add_argument("--fit", default="crop", choices=["crop", "pad", "blur"]); p.add_argument("--lufs", type=float)
    p.set_defaults(fn=cmd_deliver)

    p = sub.add_parser("overlay", help="composite transparent graphics over a delivered shape")
    p.add_argument("video")
    p.add_argument("graphics", nargs="+", help="render@seconds, e.g. 06_edit/graphics/endcard_9x16/renders/endcard.mov@38.5")
    p.add_argument("--out"); p.set_defaults(fn=cmd_overlay)

    sub.add_parser("doctor", help="check this machine is ready").set_defaults(fn=cmd_doctor)
    return ap


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):  # Windows pipes default to a code page without ✓ or →
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        args.fn(args)
    except FilmError as e:
        print(f"film: {e}", file=sys.stderr)
        return 1
    return 0
