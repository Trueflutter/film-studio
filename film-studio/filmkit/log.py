"""The generation log: every take recorded, rated and costed.

Cost per usable shot, not cost per generation, is the number that matters.
"""
from __future__ import annotations

import datetime as dt
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from . import ff
from .core import LAYOUT, TEMPLATE, Production, die, fill_template, to_float

VERDICTS = ("select", "maybe", "reject")

# Diagnosis codes: where did the failure come from? (handbook/12-diagnosis-and-iteration.md)
FAIL_CODES = {
    "CONCEPT": "the shot does not communicate its story purpose, however well it renders",
    "REF": "reference image weak, conflicting, wrong angle/light, or carries an AI look",
    "PROMPT": "ambiguous, overloaded, contradictory or wrong vocabulary",
    "MODEL": "wrong model for this job (realism, motion, faces, audio, style)",
    "MODE": "wrong generation mode (t2v / i2v / reference / first-last / multishot / v2v)",
    "CAMERA": "camera instruction ignored, unmotivated or fighting the action",
    "ACTION": "too much action for the duration; more than one beat in the shot",
    "FRAME": "start frame composition, pose or light set the shot up to fail",
    "IDENTITY": "character, wardrobe, product or location drift",
    "PHYSICS": "weight, contact, cloth, liquid or collision reads false",
    "PERFORMANCE": "face or body performance wooden, exaggerated or off-emotion",
    "SYNC": "lip sync, dialogue timing or audio artefacts",
    "ARTEFACT": "hands, morphing, flicker, melting, extra limbs, garbled text",
    "WORKFLOW": "should have been solved another way: post, composite, real footage, split shot",
}


def _now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def _safe(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9.]+", "-", s).strip("-") or "x"


def next_take_id(prod: Production, shot: str) -> str:
    n = sum(1 for t in prod.takes() if t["shot"] == shot) + 1
    return f"{shot}_t{n:03d}"


def add_take(prod: Production, shot: str, file: str, stage: str = "draft", tool: str = "",
             model: str = "", mode: str = "", res: str = "", duration: str = "",
             cost: str = "", prompt: str = "", refs: str = "", seed: str = "",
             notes: str = "", move: bool = False, verdict: str = "") -> dict:
    src = Path(file).expanduser()
    if not src.exists():
        die(f"take file not found: {src}")
    shot = shot.upper()
    known = {s["shot"].upper() for s in prod.shots()}
    if known and shot not in known:
        print(f"note: {shot} is not in the shot list yet (logging anyway)")
    take_id = next_take_id(prod, shot)
    dest_dir = prod.dir("shots") / shot / "takes"
    dest_dir.mkdir(parents=True, exist_ok=True)
    tag = "_".join(_safe(x) for x in (model, res) if x)
    dest = dest_dir / f"{take_id}{'_' + tag if tag else ''}{src.suffix.lower()}"
    (shutil.move if move else shutil.copy2)(str(src), str(dest))
    if not duration and src.suffix.lower() in (".mp4", ".mov", ".webm", ".mkv"):
        try:
            duration = f"{ff.probe(dest)['duration']:.2f}"
        except Exception:  # probing is a convenience, never a blocker
            duration = ""
    if prompt:
        pp = Path(prompt)
        prompt = prod.rel(pp) if pp.exists() else prompt
    row = {
        "take": take_id, "shot": shot, "created": _now(), "stage": stage, "tool": tool,
        "model": model, "mode": mode, "res": res, "duration_s": duration,
        "cost_usd": f"{to_float(cost):.2f}" if cost else "", "file": prod.rel(dest),
        "prompt": prompt, "refs": refs, "seed": seed, "verdict": verdict, "fail": "",
        "notes": notes,
    }
    rows = prod.takes()
    rows.append(row)
    prod.save_takes(rows)
    return row


def rate_take(prod: Production, take_id: str, verdict: str, fail: str = "", note: str = "") -> dict:
    verdict = verdict.lower()
    if verdict not in VERDICTS:
        die(f"verdict must be one of {', '.join(VERDICTS)}")
    codes = [c.strip().upper() for c in re.split(r"[+,; ]+", fail) if c.strip()]
    unknown = [c for c in codes if c not in FAIL_CODES]
    if unknown:
        die(f"unknown failure code(s) {unknown}. Use: {', '.join(FAIL_CODES)}")
    rows = prod.takes()
    hit = next((r for r in rows if r["take"].upper() == take_id.upper()), None)
    if not hit:
        die(f"no take {take_id}")
    hit["verdict"] = verdict
    if codes:
        hit["fail"] = "+".join(codes)
    if note:
        hit["notes"] = (hit.get("notes", "") + " | " + note).strip(" |")
    prod.save_takes(rows)
    return hit


def list_takes(prod: Production, shot: str | None = None) -> str:
    rows = [t for t in prod.takes() if not shot or t["shot"] == shot.upper()]
    if not rows:
        return "no takes logged yet"
    lines = [f"{'take':<12} {'stage':<7} {'model':<18} {'mode':<10} {'cost':>6}  {'verdict':<7} fail"]
    for t in rows:
        lines.append(f"{t['take']:<12} {t['stage']:<7} {t['model'][:18]:<18} {t['mode'][:10]:<10} "
                     f"{to_float(t['cost_usd']):>6.2f}  {t['verdict']:<7} {t['fail']}")
    return "\n".join(lines)


EXPLORE = ("still", "draft")        # creative iteration: cheap, fast, expected to be thrown away
PRODUCE = ("final", "upscale", "fix")  # production: spend only on locked shots
STAGES = EXPLORE + PRODUCE


def economics(prod: Production) -> dict:
    """The numbers behind the cost report, also used by tests."""
    takes = prod.takes()
    planned = [s["shot"].upper() for s in prod.shots() if s.get("status", "").lower() != "cut"]
    spend = lambda rows: sum(to_float(t["cost_usd"]) for t in rows)
    explore = [t for t in takes if t["stage"] in EXPLORE]
    produce = [t for t in takes if t["stage"] in PRODUCE]
    selected = {t["shot"] for t in takes if t["verdict"] == "select"}
    if planned:  # look-development ids (e.g. LOOK-MAYA) cost money but aren't shots in the film
        selected = {s for s in selected if s in planned}
    # Iterations before lock: takes logged for a shot up to and including its first select.
    iters = []
    for shot in selected:
        rows = [t for t in takes if t["shot"] == shot]
        first = next(i for i, t in enumerate(rows) if t["verdict"] == "select")
        iters.append(first + 1)
    # Premium spent before the shot was proven: a final with no approved draft/still before it.
    blind = []
    for t in produce:
        if t["stage"] != "final":
            continue
        prior = [x for x in takes if x["shot"] == t["shot"] and x["stage"] in EXPLORE
                 and x["verdict"] in ("select", "maybe") and x["take"] < t["take"]]
        if not prior and "from " not in t.get("notes", ""):
            blind.append(t)
    finals = [t for t in produce if t["stage"] == "final"]
    return {
        "takes": takes, "planned": planned, "selected": selected,
        "total": spend(takes), "explore": spend(explore), "produce": spend(produce),
        "n_explore": len(explore), "n_produce": len(produce),
        "iters": iters, "blind": blind,
        "finals": len(finals), "finals_kept": sum(1 for t in finals if t["verdict"] == "select"),
    }


def cost_report(prod: Production) -> str:
    e = economics(prod)
    takes, total, usable = e["takes"], e["total"], len(e["selected"])
    by_stage, by_model = defaultdict(float), defaultdict(float)
    model_takes, model_hits = Counter(), defaultdict(set)
    for t in takes:
        c = to_float(t["cost_usd"])
        by_stage[t["stage"] or "?"] += c
        m = t["model"] or "?"
        by_model[m] += c
        model_takes[m] += 1
        if t["verdict"] == "select":
            model_hits[m].add(t["shot"])
    rejected = sum(to_float(t["cost_usd"]) for t in takes if t["verdict"] == "reject")
    unrated = [t["take"] for t in takes if not t["verdict"]]
    fails = Counter(c for t in takes for c in t["fail"].split("+") if c)
    budget = to_float(prod.cfg.get("budget_usd"), 0)

    out = [f"# Cost report: {prod.cfg['title']}", ""]
    out.append(f"- Spend: **${total:.2f}**" + (f" of ${budget:.0f} budget ({total / budget:.0%})" if budget else ""))
    out.append(f"- Takes: {len(takes)} ({len(unrated)} unrated)")
    out.append(f"- Shots with a selected take: {usable}" + (f" of {len(e['planned'])} planned" if e["planned"] else ""))
    if usable:
        out.append(f"- **Cost per usable shot: ${total / usable:.2f}**  ·  takes per usable shot: {len(takes) / usable:.1f}")
    if e["planned"] and usable:
        remaining = [s for s in e["planned"] if s not in e["selected"]]
        out.append(f"- Projected cost to finish {len(remaining)} remaining shots at this rate: "
                   f"${len(remaining) * total / usable:.2f}")

    out += ["", "## Exploration vs production", ""]
    out.append(f"- Creative iteration (stills + drafts): **${e['explore']:.2f}** over {e['n_explore']} experiments"
               + (f" · **${e['explore'] / e['n_explore']:.2f} per experiment**" if e["n_explore"] else ""))
    out.append(f"- Production (finals + upscales + fixes): **${e['produce']:.2f}** over {e['n_produce']} renders")
    if total:
        out.append(f"- Split: {e['explore'] / total:.0%} exploring / {e['produce'] / total:.0%} producing")
    if e["iters"]:
        out.append(f"- Iterations before a shot locks: avg {sum(e['iters']) / len(e['iters']):.1f} "
                   f"(min {min(e['iters'])}, max {max(e['iters'])})")
    if e["finals"]:
        kept = e["finals_kept"] / e["finals"]
        out.append(f"- Finals kept: {e['finals_kept']}/{e['finals']}"
                   + (" (under 70%: your drafts are not predicting your finals; lock more in the draft)"
                      if kept < 0.7 else ""))
    if e["blind"]:
        out.append(f"- Premium renders with no approved draft before them: {len(e['blind'])} "
                   f"(${sum(to_float(t['cost_usd']) for t in e['blind']):.2f}): "
                   + ", ".join(t["take"] for t in e["blind"][:8]))
    out.append(f"- Spend on rejected takes: ${rejected:.2f} (rejected drafts are the cheap way to learn; "
               "rejected finals are the expensive way)")

    out += ["", "## By stage", "", "| stage | spend |", "|---|---:|"]
    out += [f"| {k} | ${v:.2f} |" for k, v in sorted(by_stage.items())]
    out += ["", "## By model", "", "| model | takes | spend | shots won | $ per shot won |", "|---|---:|---:|---:|---:|"]
    for m, v in sorted(by_model.items(), key=lambda kv: -kv[1]):
        won = len(model_hits[m])
        out.append(f"| {m} | {model_takes[m]} | ${v:.2f} | {won} | {('$%.2f' % (v / won)) if won else '-'} |")
    if fails:
        out += ["", "## Why takes failed (most expensive habits first)", ""]
        for code, n in fails.most_common():
            out.append(f"- **{code}** × {n}: {FAIL_CODES.get(code, '')}")
    return "\n".join(out) + "\n"


def _doc_state(prod: Production, rel: str, tpl_rel: str | None = None) -> str:
    """missing / not started / started / in progress, judged against the untouched template."""
    path = prod.root / rel
    if not path.exists():
        return "missing"
    tpl = TEMPLATE / (tpl_rel or rel)
    if not tpl.exists():
        return "in progress"
    body = path.read_text(encoding="utf-8")
    blank = fill_template(tpl.read_text(encoding="utf-8"), prod.cfg)
    if body.strip() == blank.strip():
        return "not started"
    return "started" if len(body) < len(blank) + 200 else "in progress"


def status(prod: Production) -> str:
    cfg = prod.cfg
    out = [f"{cfg['title']}  [{cfg['format']} · {cfg['aspect']} · {cfg['fps']}fps · target {cfg['target_duration_s']}s]",
           f"folder: {prod.root}", ""]
    brief_tpl = "brief_ad.md" if cfg["format"] in ("ad", "social") else "brief_film.md"
    docs = [
        ("brief", LAYOUT["brief"] + "/brief.md", LAYOUT["brief"] + "/" + brief_tpl),
        ("concept + stress test", LAYOUT["story"] + "/concept.md", None),
        ("treatment", LAYOUT["story"] + "/treatment.md", None),
        ("script", LAYOUT["story"] + "/script.md", None),
        ("style bible", LAYOUT["design"] + "/style.md", None),
        ("world bible", LAYOUT["design"] + "/world.md", None),
        ("continuity notes", LAYOUT["board"] + "/continuity.md", None),
    ]
    out.append("Pre-production")
    for label, rel, tpl_rel in docs:
        out.append(f"  {label:<24} {_doc_state(prod, rel, tpl_rel)}")
    chars = [d.name for d in (prod.dir("design") / "characters").glob("*") if d.is_dir() and not d.name.startswith("_")]
    out.append(f"  {'characters':<24} {', '.join(chars) if chars else 'none yet (film character <name>)'}")
    shots = prod.shots()
    boards = {p.stem.upper() for p in (prod.dir("board") / "boards").glob("*.*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")}
    animatics = sorted((prod.dir("board")).glob("animatic_v*.mp4"))
    out.append(f"  {'shot list':<24} {len(shots)} shots, {sum(to_float(s.get('duration_s')) for s in shots):.1f}s planned")
    out.append(f"  {'boards':<24} {len([s for s in shots if s['shot'].upper() in boards])}/{len(shots)} shots boarded")
    out.append(f"  {'animatic':<24} {animatics[-1].name if animatics else 'not built (film animatic)'}")
    takes = prod.takes()
    sel = {t["shot"] for t in takes if t["verdict"] == "select"}
    spend = sum(to_float(t["cost_usd"]) for t in takes)
    out += ["", "Production", f"  takes logged: {len(takes)}  ·  spend ${spend:.2f}  ·  shots selected {len(sel)}/{len(shots)}"]
    missing = [s["shot"] for s in shots if s["shot"].upper() not in sel and s.get("status", "").lower() != "cut"]
    if missing:
        out.append(f"  still to land: {', '.join(missing[:20])}{' ...' if len(missing) > 20 else ''}")
    cuts = sorted((prod.dir("edit") / "cuts").glob("*.mp4"))
    qcs = sorted((prod.dir("delivery") / "qc").glob("*.md"))
    masters = sorted((prod.dir("delivery") / "masters").glob("*.mp4"))
    out += ["", "Post",
            f"  latest cut: {cuts[-1].name if cuts else 'none'}",
            f"  QC reports: {len(qcs)}  ·  masters: {len(masters)}"]
    return "\n".join(out)
