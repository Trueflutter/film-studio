"""Production discovery, config and the two CSV spines (shotlist, takes)."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import shutil
from pathlib import Path

# KIT_ROOT: where filmkit is installed (the plugin folder): templates, fonts, rates.
# PROJECT_ROOT: the student's studio (where productions and .env live). Resolved as
# FILM_PROJECT, else the nearest folder above cwd holding productions/ or .env, else cwd.
KIT_ROOT = Path(__file__).resolve().parent.parent


def _project_root() -> Path:
    if os.environ.get("FILM_PROJECT"):
        return Path(os.environ["FILM_PROJECT"]).expanduser().resolve()
    here = Path.cwd().resolve()
    for d in [here, *here.parents]:
        if (d / "productions").is_dir() or (d / ".film-studio").exists():
            return d
    return here


PROJECT_ROOT = _project_root()
PRODUCTIONS = PROJECT_ROOT / "productions"
TEMPLATE = KIT_ROOT / "templates" / "production"
CURRENT = PRODUCTIONS / ".current"

ASPECTS = {
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
    "2.39:1": (1920, 804),
}

SHOT_FIELDS = ["shot", "scene", "beat", "purpose", "size", "angle", "lens", "move",
               "action", "dialogue", "sound", "duration_s", "route", "refs", "status", "notes"]
TAKE_FIELDS = ["take", "shot", "created", "stage", "tool", "model", "mode", "res",
               "duration_s", "cost_usd", "file", "prompt", "refs", "seed", "job", "verdict",
               "fail", "notes"]

# Where each kind of thing lives inside a production. One place to change it.
LAYOUT = {
    "brief": "00_brief",
    "story": "01_story",
    "design": "02_design",
    "board": "03_board",
    "shots": "04_shots",
    "sound": "05_sound",
    "edit": "06_edit",
    "delivery": "07_delivery",
}


class FilmError(Exception):
    """A user-facing error: printed without a traceback."""


def die(msg: str) -> None:
    raise FilmError(msg)


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "untitled"


def today() -> str:
    return dt.date.today().isoformat()


class Production:
    def __init__(self, root: Path):
        self.root = root
        cfg_path = root / "production.json"
        if not cfg_path.exists():
            die(f"{root} is not a production (no production.json)")
        self.cfg = json.loads(cfg_path.read_text())

    # --- paths -----------------------------------------------------------
    def dir(self, key: str) -> Path:
        return self.root / LAYOUT[key]

    @property
    def shotlist_path(self) -> Path:
        return self.dir("board") / "shotlist.csv"

    @property
    def takes_path(self) -> Path:
        return self.dir("shots") / "takes.csv"

    @property
    def size(self) -> tuple[int, int]:
        return int(self.cfg["width"]), int(self.cfg["height"])

    @property
    def fps(self) -> float:
        return float(self.cfg.get("fps", 24))

    @property
    def slug(self) -> str:
        return self.cfg["slug"]

    def rel(self, p: Path) -> str:
        try:
            return str(Path(p).resolve().relative_to(self.root.resolve()))
        except ValueError:
            return str(p)

    def next_version(self, folder: Path, stem: str, ext: str) -> Path:
        """cut_v001.mp4, cut_v002.mp4 ... never overwrite a previous version."""
        folder.mkdir(parents=True, exist_ok=True)
        n = 1
        pattern = re.compile(rf"^{re.escape(stem)}_v(\d+)$")
        for f in folder.glob(f"{stem}_v*{ext}"):
            m = pattern.match(f.stem)
            if m:
                n = max(n, int(m.group(1)) + 1)
        return folder / f"{stem}_v{n:03d}{ext}"

    # --- spines ----------------------------------------------------------
    def shots(self) -> list[dict]:
        return read_csv(self.shotlist_path)

    def takes(self) -> list[dict]:
        return read_csv(self.takes_path)

    def save_takes(self, rows: list[dict]) -> None:
        write_csv(self.takes_path, TAKE_FIELDS, rows)


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        key = (reader.fieldnames or [""])[0]
        out = []
        for r in reader:
            # Blank rows and rows whose first cell starts with '#' are notes, not data.
            first = (r.get(key) or "").strip()
            if first and not first.startswith("#"):
                out.append({k: (v or "").strip() for k, v in r.items() if k is not None})
    return out


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
    tmp.replace(path)


def find_production(explicit: str | None = None) -> Production:
    if explicit:
        p = Path(explicit)
        if not p.exists():
            p = PRODUCTIONS / explicit
        return Production(p)
    here = Path.cwd().resolve()
    for d in [here, *here.parents]:
        if (d / "production.json").exists():
            return Production(d)
    if CURRENT.exists():
        slug = CURRENT.read_text().strip()
        if (PRODUCTIONS / slug / "production.json").exists():
            return Production(PRODUCTIONS / slug)
    die("No production selected. Run `film new <title>` or `film use <slug>`, or pass --prod.")
    raise AssertionError  # unreachable, keeps type checkers calm


FORMAT_DEFAULTS = {"film": ("16:9", 60), "ad": ("9:16", 30), "social": ("9:16", 15)}


def resolve_path(p, prod: "Production | None" = None) -> Path:
    """Relative paths work from anywhere in the studio: tried from the current folder, then
    from the current production's folder (where every documented path starts)."""
    path = Path(p).expanduser()
    if path.is_absolute() or path.exists():
        return path
    try:
        prod = prod or find_production()
    except FilmError:
        return path
    alt = prod.root / path
    return alt if alt.exists() else path


# What a new production reuses from an earlier one (`film new --from`): the brief, the look and
# the cast, the graphics and the sound kit. Story, boards, shots, cuts and deliveries start fresh.
REUSE = ("00_brief", "02_design", "05_sound/ambience", "05_sound/music", "05_sound/sfx", "06_edit/graphics")


def create_production(title: str, fmt: str | None, aspect: str | None, fps: float | None, duration: int | None,
                      budget: float | None, slug: str | None = None, base: Production | None = None) -> Production:
    """A new production from the template, or from an earlier production (`base`): an episode, a
    cutdown campaign or the next piece in a series keeps its format, look, cast, graphics and sound kit."""
    b = base.cfg if base else {}
    fmt = fmt or b.get("format", "film")
    aspect = aspect or b.get("aspect") or FORMAT_DEFAULTS[fmt][0]
    duration = duration or b.get("target_duration_s") or FORMAT_DEFAULTS[fmt][1]
    fps = fps or b.get("fps", 24)
    budget = budget if budget is not None else b.get("budget_usd", 60)
    if aspect not in ASPECTS:
        die(f"aspect must be one of {', '.join(ASPECTS)}")
    if not TEMPLATE.exists():
        die(f"template missing at {TEMPLATE}")
    slug = slugify(slug or title)
    root = PRODUCTIONS / slug
    if root.exists():
        die(f"{root} already exists")
    shutil.copytree(TEMPLATE, root)
    w, h = ASPECTS[aspect]
    cfg = {
        "slug": slug,
        "title": title,
        "format": fmt,
        "aspect": aspect,
        "width": w,
        "height": h,
        "fps": fps,
        "target_duration_s": duration,
        "budget_usd": budget,
        "loudness_lufs": -14 if fmt in ("ad", "social") else -16,
        "created": today(),
    }
    if base:
        cfg["from"] = base.cfg.get("slug", base.root.name)
    (root / "production.json").write_text(json.dumps(cfg, indent=2) + "\n")
    for f in root.rglob("*.md"):
        f.write_text(fill_template(f.read_text(encoding="utf-8"), cfg), encoding="utf-8")
    # The ad and film variants of the brief live side by side in the template.
    brief_dir = root / LAYOUT["brief"]
    keep, drop = ("brief_ad.md", "brief_film.md") if fmt in ("ad", "social") else ("brief_film.md", "brief_ad.md")
    (brief_dir / drop).unlink()
    (brief_dir / keep).rename(brief_dir / "brief.md")
    for rel in REUSE if base else ():
        if (base.root / rel).is_dir():
            shutil.copytree(base.root / rel, root / rel, dirs_exist_ok=True)
    PRODUCTIONS.mkdir(exist_ok=True)
    CURRENT.write_text(slug)
    return Production(root)


def fill_template(text: str, cfg: dict) -> str:
    subs = {"{{title}}": cfg["title"], "{{format}}": cfg["format"], "{{aspect}}": cfg["aspect"],
            "{{duration}}": str(cfg["target_duration_s"]), "{{date}}": cfg["created"],
            "{{slug}}": cfg["slug"]}
    for k, v in subs.items():
        text = text.replace(k, v)
    return text


def to_float(v, default: float = 0.0) -> float:
    try:
        return float(str(v).replace("$", "").strip() or default)
    except ValueError:
        return default
