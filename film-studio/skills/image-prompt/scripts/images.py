#!/usr/bin/env python3
"""Make images through your ChatGPT subscription (via the Codex CLI) and show them on one board.

  python3 images.py gen   PROMPT_FILE OUT_DIR [--count 4] [--name take] [--ref IMG ...] [--shape portrait|landscape|square]
  python3 images.py board OUT_DIR [--title "..."] [--prompt PROMPT_FILE] [--no-open]
  python3 images.py check

gen runs one `codex exec` per image in parallel, saves OUT_DIR/<name>_<n>.png, then builds and opens the board.
board builds OUT_DIR/board.html from every image in the folder (use it for Aristotto downloads too).
check confirms Codex is installed and signed in with ChatGPT.
Standard library only.
"""
import argparse, html, json, os, platform, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

GEN_DIR = Path.home() / ".codex" / "generated_images"
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}
SHAPES = {
    "portrait": "Portrait orientation (taller than wide, about 3:4 or 2:3).",
    "landscape": "Landscape orientation (wider than tall, about 3:2 or 16:9).",
    "square": "Square, 1:1.",
}


def check():
    if not shutil.which("codex"):
        sys.exit("Codex is not installed. Install it with: npm i -g @openai/codex  then run: codex login")
    out = subprocess.run(["codex", "login", "status"], capture_output=True, text=True)
    status = (out.stdout + out.stderr).strip()
    if "ChatGPT" not in status:
        sys.exit(f"Codex is installed but not signed in with ChatGPT ({status}). Run: codex login")
    print(f"ok: {status}")


def _newest_since(t0, taken):
    if not GEN_DIR.exists():
        return None
    found = [p for p in GEN_DIR.rglob("*") if p.suffix.lower() in IMG_EXT
             and p.stat().st_mtime >= t0 and str(p) not in taken]
    return max(found, key=lambda p: p.stat().st_mtime) if found else None


def _one(prompt_file, dest, shape, refs, taken):
    t0 = time.time()
    ask = (
        "Use your built-in image generation tool to create exactly ONE image. "
        f"The image prompt is the full text of the file {prompt_file}; use it word for word, "
        "do not rewrite, shorten or add to it. "
        + (f"The attached image(s) are references: follow the prompt about what to keep and what to change. " if refs else "")
        + f"{SHAPES[shape]} Highest quality. "
        f"Then copy the generated image file to {dest} (it is saved under ~/.codex/generated_images). "
        "Reply with one line: the pixel size and the saved path."
    )
    cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "workspace-write",
           "-C", str(dest.parent), "-c", "model_reasoning_effort=low"]
    for r in refs:
        cmd += ["-i", str(r)]
    cmd.append(ask)
    log = dest.with_suffix(".log")
    with open(log, "w") as fh:
        subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    if not dest.exists():  # Codex didn't copy it: take the newest unclaimed image made since we started
        src = _newest_since(t0, taken)
        if src:
            taken.add(str(src))
            shutil.copy(src, dest)
    secs = round(time.time() - t0)
    if dest.exists():
        log.unlink(missing_ok=True)
        return f"{dest.name}  {secs}s"
    return f"FAILED {dest.name}  {secs}s  (see {log.name})"


def gen(a):
    check()
    prompt_file = Path(a.prompt_file).resolve()
    out = Path(a.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy(prompt_file, out / "prompt.txt") if prompt_file != out / "prompt.txt" else None
    refs = [Path(r).resolve() for r in (a.ref or [])]
    n0 = len([p for p in out.glob(f"{a.name}_*.png")])
    dests = [out / f"{a.name}_{n0 + i + 1}.png" for i in range(a.count)]
    taken = set()
    print(f"Making {a.count} image(s) through ChatGPT, about 1 to 2 minutes...")
    with ThreadPoolExecutor(max_workers=min(a.count, 4)) as ex:
        for line in ex.map(lambda d: _one(out / "prompt.txt", d, a.shape, refs, taken), dests):
            print(line)
    board_path = build_board(out, a.title or out.name, out / "prompt.txt", "ChatGPT via Codex")
    if not a.no_open:
        open_file(board_path)
    print(f"board: {board_path}")


def build_board(out, title, prompt_file=None, route=""):
    imgs = sorted([p for p in out.iterdir() if p.suffix.lower() in IMG_EXT],
                  key=lambda p: p.stat().st_mtime)
    prompt = Path(prompt_file).read_text() if prompt_file and Path(prompt_file).exists() else ""
    cards = "\n".join(
        f'<figure><img src="{html.escape(p.name)}" loading="lazy"><figcaption>{i}. {html.escape(p.name)}</figcaption></figure>'
        for i, p in enumerate(imgs, 1))
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>
:root{{--bg:#0e0e10;--ink:#f5f5f7;--mute:#a0a0a6;--line:#2a2a2e;--card:#17171a}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}
main{{max-width:1600px;margin:0 auto;padding:24px 16px 60px}} h1{{font-weight:500;font-size:26px;margin:0 0 4px}}
.meta{{color:var(--mute);margin:0 0 18px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px}}
img{{width:100%;border-radius:8px;display:block;cursor:zoom-in}} figcaption{{color:var(--mute);font-size:13px;padding:6px 2px 0}}
details{{margin-top:22px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px}}
pre{{white-space:pre-wrap;font:13px/1.55 system-ui,sans-serif;margin:10px 0 0}}
.lb{{position:fixed;inset:0;background:rgba(0,0,0,.94);display:none;align-items:center;justify-content:center}}
.lb img{{max-width:96vw;max-height:96vh;width:auto;cursor:zoom-out}}
</style></head><body><main><h1>{html.escape(title)}</h1>
<p class="meta">{len(imgs)} image(s){(' · ' + html.escape(route)) if route else ''} · click to enlarge · tell Claude the number you want</p>
<div class="grid">{cards}</div>
{f'<details><summary>Prompt</summary><pre>{html.escape(prompt)}</pre></details>' if prompt else ''}
</main><div class="lb" onclick="this.style.display='none'"><img></div>
<script>document.querySelectorAll('.grid img').forEach(i=>i.onclick=()=>{{const l=document.querySelector('.lb');l.querySelector('img').src=i.src;l.style.display='flex'}})</script>
</body></html>"""
    path = out / "board.html"
    path.write_text(doc)
    return path


def open_file(path):
    sysname = platform.system()
    if sysname == "Darwin":
        subprocess.run(["open", str(path)])
    elif sysname == "Windows":
        os.startfile(str(path))  # type: ignore[attr-defined]
    else:
        subprocess.run(["xdg-open", str(path)])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen")
    g.add_argument("prompt_file"); g.add_argument("out_dir")
    g.add_argument("--count", type=int, default=4)
    g.add_argument("--name", default="take")
    g.add_argument("--ref", nargs="*")
    g.add_argument("--shape", choices=list(SHAPES), default="portrait")
    g.add_argument("--title"); g.add_argument("--no-open", action="store_true")
    b = sub.add_parser("board")
    b.add_argument("out_dir"); b.add_argument("--title"); b.add_argument("--prompt")
    b.add_argument("--route", default=""); b.add_argument("--no-open", action="store_true")
    sub.add_parser("check")
    a = p.parse_args()
    if a.cmd == "check":
        check()
    elif a.cmd == "gen":
        gen(a)
    else:
        out = Path(a.out_dir).resolve()
        path = build_board(out, a.title or out.name, a.prompt or (out / "prompt.txt"), a.route)
        if not a.no_open:
            open_file(path)
        print(f"board: {path}")


if __name__ == "__main__":
    main()
