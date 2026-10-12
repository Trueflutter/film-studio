"""Review pages: a printable storyboard and a dailies page of every take, grouped by shot."""
from __future__ import annotations

import html
import re
import os
from pathlib import Path

from .core import Production, today, to_float
from .log import FAIL_CODES
from .media import _board_for

CSS = """
:root{--bg:#f7f5f1;--card:#fff;--ink:#1a1a18;--mute:#666;--line:#e3ded5;--sel:#0f7b5f;--rej:#b3261e;--may:#a86b00}
@media (prefers-color-scheme:dark){:root{--bg:#141413;--card:#1e1e1c;--ink:#eee;--mute:#9a9a94;--line:#33332f}}
*{box-sizing:border-box}body{margin:0;padding:24px;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
h1{font-weight:500;margin:0 0 4px}h2{font-weight:500;margin:28px 0 8px}.meta{color:var(--mute);margin-bottom:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.card img,.card video{display:block;width:100%;background:#000;aspect-ratio:var(--ar);object-fit:contain}
.slate{display:flex;align-items:center;justify-content:center;aspect-ratio:var(--ar);background:#222;color:#aaa;font-size:28px}
.body{padding:10px 12px}.id{font-weight:600}.tags{color:var(--mute);font-size:12px;margin:2px 0 6px}
.line{margin:4px 0}.dlg{font-style:italic}.k{color:var(--mute);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
.badge{display:inline-block;padding:1px 8px;border-radius:999px;font-size:12px;border:1px solid currentColor}
.select{color:var(--sel)}.reject{color:var(--rej)}.maybe{color:var(--may)}
.shotrow{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin-bottom:10px}
pre{white-space:pre-wrap;font-size:12px;color:var(--mute);max-height:140px;overflow:auto;margin:6px 0 0}
@media print{body{background:#fff;padding:0}.card{break-inside:avoid}}
"""


def _page(title: str, sub: str, body: str, ar: str) -> str:
    return (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' "
            f"content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title>"
            f"<style>{CSS}:root{{--ar:{ar}}}</style></head><body><h1>{html.escape(title)}</h1>"
            f"<div class='meta'>{sub}</div>{body}</body></html>")


def _src(page: Path, target: Path) -> str:
    return html.escape(os.path.relpath(target, page.parent).replace(os.sep, "/"))


def storyboard(prod: Production) -> Path:
    out = prod.dir("board") / "storyboard.html"
    shots = prod.shots()
    total = sum(to_float(s.get("duration_s")) for s in shots)
    cards = []
    for s in shots:
        board = _board_for(prod, s["shot"])
        pic = (f"<img src='{_src(out, board)}' alt='{html.escape(s['shot'])}'>" if board
               else f"<div class='slate'>{html.escape(s['shot'])}</div>")
        tags = " · ".join(x for x in (s.get("size"), s.get("angle"), s.get("lens"), s.get("move"),
                                         (s.get("duration_s") + "s") if s.get("duration_s") else "") if x)
        rows = []
        for key, label in (("purpose", "purpose"), ("action", "action"), ("sound", "sound")):
            if s.get(key):
                rows.append(f"<div class='line'><span class='k'>{label}</span> {html.escape(s[key])}</div>")
        if s.get("dialogue"):
            rows.append(f"<div class='line dlg'>“{html.escape(s['dialogue'])}”</div>")
        cards.append(f"<div class='card'>{pic}<div class='body'><div class='id'>{html.escape(s['shot'])} "
                     f"<span class='tags'>{html.escape(s.get('scene', ''))} {html.escape(s.get('beat', ''))}</span></div>"
                     f"<div class='tags'>{html.escape(tags)}</div>{''.join(rows)}</div></div>")
    sub = f"{len(shots)} shots · {total:.1f}s planned · {prod.cfg['aspect']} · updated {today()}"
    ar = prod.cfg["aspect"].replace(":", "/")
    out.write_text(_page(f"{prod.cfg['title']}: storyboard", sub, f"<div class='grid'>{''.join(cards)}</div>", ar))
    return out


def dailies(prod: Production) -> Path:
    out = prod.dir("shots") / "dailies.html"
    takes = prod.takes()
    shots = prod.shots() or [{"shot": s} for s in sorted({t["shot"] for t in takes})]
    known = {s["shot"] for s in shots}
    shots += [{"shot": s} for s in sorted({t["shot"] for t in takes} - known)]
    blocks = []
    for s in shots:
        these = [t for t in takes if t["shot"] == s["shot"]]
        spend = sum(to_float(t["cost_usd"]) for t in these)
        head = (f"<h2>{html.escape(s['shot'])} <span class='tags'>{len(these)} takes · ${spend:.2f}"
                f"</span></h2><div class='shotrow'><span class='k'>plan</span> "
                f"{html.escape(' · '.join(x for x in (s.get('size'), s.get('move'), s.get('action')) if x) or 'not in shot list')}"
                + (f"<div class='line dlg'>“{html.escape(s['dialogue'])}”</div>" if s.get("dialogue") else "")
                + "</div>")
        cards = []
        for t in these:
            f = prod.root / t["file"]
            media = (f"<video src='{_src(out, f)}' controls preload='metadata' muted loop playsinline></video>"
                     if f.suffix.lower() in (".mp4", ".mov", ".webm") else f"<img src='{_src(out, f)}'>")
            v = t["verdict"]
            badge = f"<span class='badge {v}'>{v}</span>" if v else "<span class='badge'>unrated</span>"
            fails = "".join(f"<div class='line'><span class='k'>{c}</span> {html.escape(FAIL_CODES.get(c, ''))}</div>"
                            for c in t["fail"].split("+") if c)
            prompt = ""
            pf = prod.root / t["prompt"] if t["prompt"] else None
            if pf and pf.is_file():
                prompt = f"<pre>{html.escape(pf.read_text(encoding='utf-8')[:900])}</pre>"
            meta = " · ".join(x for x in (t["stage"], t["model"], t["mode"], t["res"],
                                           (t["duration_s"] + "s") if t["duration_s"] else "",
                                           f"${to_float(t['cost_usd']):.2f}" if t["cost_usd"] else "") if x)
            cards.append(f"<div class='card'>{media}<div class='body'><div class='id'>{html.escape(t['take'])} {badge}</div>"
                         f"<div class='tags'>{html.escape(meta)}</div>{fails}"
                         + (f"<div class='line'>{html.escape(t['notes'])}</div>" if t["notes"] else "")
                         + f"{prompt}</div></div>")
        blocks.append(head + f"<div class='grid'>{''.join(cards) or '<div class=meta>no takes yet</div>'}</div>")
    total = sum(to_float(t["cost_usd"]) for t in takes)
    sub = f"{len(takes)} takes · ${total:.2f} · updated {today()} · rate takes with <code>film take rate</code>"
    ar = prod.cfg["aspect"].replace(":", "/")
    out.write_text(_page(f"{prod.cfg['title']}: dailies", sub, "".join(blocks), ar))
    return out


BOARD_CSS = """
.opts{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
.opt{background:var(--card);border:2px solid var(--line);border-radius:12px;overflow:hidden;cursor:pointer}
.opt.on{border-color:var(--sel)}.opt img,.opt video{display:block;width:100%;background:#000}
.opt audio{width:100%;margin:14px 0 4px}.opts.text{grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}
.txt{padding:18px 18px 0;line-height:1.5}.txt h3{margin:0 0 8px;font-size:19px}.txt p{margin:6px 0}.txt ul{margin:6px 0;padding-left:20px}.num{font-size:22px;font-weight:600}.cap{color:var(--mute);margin-top:2px}
.bar{position:sticky;bottom:0;margin-top:22px;background:var(--card);border:1px solid var(--line);border-radius:12px;
 padding:12px;display:flex;gap:10px;align-items:center}.bar input{flex:1;font:inherit;padding:10px;border:1px solid var(--line);
 border-radius:8px;background:var(--bg);color:var(--ink)}.bar button{font:inherit;padding:10px 18px;border:0;border-radius:999px;
 background:var(--sel);color:#fff;cursor:pointer}.hint{color:var(--mute);font-size:13px}
"""

BOARD_JS = """
let pick=null;const opts=[...document.querySelectorAll('.opt')];
opts.forEach(o=>o.addEventListener('click',e=>{if(e.target.closest('audio,video[controls]'))return;
 opts.forEach(x=>x.classList.remove('on'));o.classList.add('on');pick=o.dataset.label;document.getElementById('msg').textContent='';}));
document.getElementById('copy').addEventListener('click',()=>{
 if(!pick){document.getElementById('msg').textContent='Click an option first.';return;}
 const note=document.getElementById('note').value.trim();
 const text=document.getElementById('lead').value+' '+pick+'.'+(note?' '+note:'');
 navigator.clipboard.writeText(text).then(()=>{document.getElementById('msg').textContent='Copied. Paste it into Claude.';});});
"""


def _inline(t: str) -> str:
    t = html.escape(t)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def _text_card(path: Path) -> str:
    """A concept, script or brief written as a short markdown file: '# heading', '- bullets', paragraphs."""
    out, items = [], []
    def flush():
        if items:
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")
            items.clear()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            flush()
        elif line.startswith("#"):
            flush(); out.append(f"<h3>{_inline(line.lstrip('#').strip())}</h3>")
        elif line.startswith(("- ", "* ")):
            items.append(_inline(line[2:]))
        else:
            flush(); out.append(f"<p>{_inline(line)}</p>")
    flush()
    return f"<div class='txt'>{''.join(out)}</div>"


def board(prod: Production, title: str, items: list[tuple[Path, str]], ask: str = "I pick") -> Path:
    """An options page the director chooses from: numbered cards (image, video or audio),
    click one, add a note, copy the pick into Claude."""
    slug = "".join(c if c.isalnum() else "-" for c in title.lower()).strip("-")[:48] or "options"
    out = prod.dir("board") / "options" / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    cards = []
    for i, (path, caption) in enumerate(items, 1):
        ext = path.suffix.lower()
        src = _src(out, path)
        if ext in (".mp4", ".mov", ".webm"):
            media = f"<video src='{src}' controls muted loop playsinline preload='metadata'></video>"
        elif ext in (".mp3", ".wav", ".m4a", ".aac", ".ogg"):
            media = f"<div class='body'><audio src='{src}' controls preload='none'></audio></div>"
        elif ext in (".md", ".txt"):
            media = _text_card(path)
            caption = "" if caption == path.stem else caption  # the card's own heading names it
        else:
            media = f"<img src='{src}' alt='option {i}' loading='lazy'>"
        label = f"{i}" + (f" ({html.escape(caption.split(' ')[0])})" if caption.startswith(("S", "C", "W", "P")) and "_t" in caption.split(" ")[0] else "")
        cards.append(f"<div class='opt' data-label='{html.escape(label)}'>{media}<div class='body'>"
                     f"<div class='num'>{i}</div><div class='cap'>{html.escape(caption)}</div></div></div>")
    bar = (f"<div class='bar'><input type='hidden' id='lead' value='{html.escape(ask)}'>"
           "<input id='note' placeholder='Anything to change? e.g. warmer light, older, closer'>"
           "<button id='copy'>Copy my pick</button><span id='msg' class='hint'></span></div>")
    kind = " text" if all(p.suffix.lower() in (".md", ".txt") for p, _ in items) else ""
    body = f"<style>{BOARD_CSS}</style><div class='opts{kind}'>{''.join(cards)}</div>{bar}<script>{BOARD_JS}</script>"
    out.write_text(_page(title, f"{len(items)} options · click one, add a note, copy it into Claude · {today()}", body, "auto"), encoding="utf-8")
    return out
