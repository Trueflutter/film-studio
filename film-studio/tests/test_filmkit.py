"""filmkit tests. Run from studio-kit/:  python3 -m unittest discover -s tests

Logic tests always run. Media tests run when ffmpeg is on PATH (or FFMPEG is set).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT))
from filmkit import ff  # noqa: E402

FFMPEG = ff.find("ffmpeg")


def film(project: Path, *args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "FILM_PROJECT": str(project), "PYTHONPATH": str(KIT)}
    return subprocess.run([sys.executable, "-m", "filmkit", *args], cwd=project, env=env,
                          capture_output=True, text=True)


class StudioCase(unittest.TestCase):
    def setUp(self):
        # resolve(): on macOS the temp dir (/var/...) is a symlink to /private/var/..., and film prints real paths
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.studio = self.tmp / "project"
        (self.studio / "productions").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def ok(self, *args: str) -> str:
        r = film(self.studio, *args)
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        return r.stdout

    def media(self, name: str, lavfi: str, extra: list[str]) -> Path:
        out = self.tmp / name
        subprocess.run([FFMPEG, "-nostdin", "-loglevel", "error", "-y", "-f", "lavfi", "-i", lavfi, *extra, str(out)],
                       check=True)
        return out


class TestLogic(StudioCase):
    def test_new_status_and_character(self):
        self.ok("new", "Night Call", "--format", "ad", "--aspect", "9:16", "--duration", "30")
        prod = self.studio / "productions" / "night-call"
        self.assertTrue((prod / "00_brief" / "brief.md").exists())
        self.assertFalse((prod / "00_brief" / "brief_film.md").exists())
        self.assertIn("Ad brief: Night Call", (prod / "00_brief" / "brief.md").read_text())
        out = self.ok("status")
        self.assertIn("brief                    not started", out)
        (prod / "01_story" / "concept.md").write_text("x" * 5000)
        self.assertIn("concept + stress test    in progress", self.ok("status"))
        self.ok("character", "Maya Haddad")
        self.assertIn("Maya Haddad", (prod / "02_design/characters/maya-haddad/bible.md").read_text())

    def test_new_from_reuses_cast_look_and_kit(self):
        self.ok("new", "Desk Diaries", "--format", "social", "--duration", "20", "--budget", "15")
        pilot = self.studio / "productions" / "desk-diaries"
        (pilot / "00_brief/brief.md").write_text("series brief")
        self.ok("character", "Noor")
        (pilot / "02_design/style.md").write_text("pilot style")
        (pilot / "06_edit/graphics/endcard_9x16/renders").mkdir(parents=True)
        (pilot / "06_edit/graphics/endcard_9x16/renders/endcard.mov").write_bytes(b"mov")
        (pilot / "05_sound/music/theme.wav").write_bytes(b"wav")
        (pilot / "05_sound/dialogue/ep1_line.wav").write_bytes(b"wav")
        (pilot / "01_story/script.md").write_text("episode one")
        out = self.ok("new", "Desk Diaries Ep 2", "--from", "desk-diaries")
        self.assertIn("from desk-diaries", out)
        self.assertIn("social · 9:16 · 20s · $15", out)
        ep2 = self.studio / "productions" / "desk-diaries-ep-2"
        self.assertEqual((ep2 / "00_brief/brief.md").read_text(), "series brief")
        self.assertEqual((ep2 / "02_design/style.md").read_text(), "pilot style")
        self.assertTrue((ep2 / "02_design/characters/noor/bible.md").exists())
        self.assertTrue((ep2 / "06_edit/graphics/endcard_9x16/renders/endcard.mov").exists())
        self.assertTrue((ep2 / "05_sound/music/theme.wav").exists())
        # episode-specific work starts fresh
        self.assertFalse((ep2 / "05_sound/dialogue/ep1_line.wav").exists())
        self.assertNotEqual((ep2 / "01_story/script.md").read_text(), "episode one")
        self.assertIn('"from": "desk-diaries"', (ep2 / "production.json").read_text())
        self.assertIn("16:9", self.ok("new", "Desk Diaries Wide", "--from", "desk-diaries", "--aspect", "16:9"))

    def test_takes_rating_and_economics(self):
        self.ok("new", "Econ", "--budget", "20")
        f = self.tmp / "clip.mp4"
        f.write_bytes(b"not really a video")
        for stage, cost in (("draft", "0.50"), ("draft", "0.50"), ("final", "2.85")):
            self.ok("take", "add", "S01", str(f), "--stage", stage, "--cost", cost, "--duration", "5")
        self.ok("take", "add", "S02", str(f), "--stage", "final", "--cost", "1.00", "--duration", "5")
        self.ok("take", "rate", "S01_t001", "reject", "--fail", "ACTION+CAMERA")
        self.ok("take", "rate", "S01_t002", "select")
        self.ok("take", "rate", "S01_t003", "select")
        bad = film(self.studio, "take", "rate", "S01_t003", "reject", "--fail", "NOPE")
        self.assertNotEqual(bad.returncode, 0)
        report = self.ok("cost")
        self.assertIn("Spend: **$4.85**", report)
        self.assertIn("$0.50 per experiment", report)
        self.assertIn("Cost per usable shot: $4.85", report)
        self.assertIn("Premium renders with no approved draft before them: 1", report)  # S02
        self.assertIn("avg 2.0", report)

    def test_format_defaults_rates_and_look_ids(self):
        out = self.ok("new", "Spot", "--format", "ad")
        self.assertIn("9:16", out)
        self.assertIn("30s", out)
        sys.path.insert(0, str(KIT))
        from filmkit.gen import rate_for
        self.assertEqual(rate_for("ark", "dreamina-seedance-2-5-260628", "480p"), 0.10)
        self.assertIsNone(rate_for("ark", "unknown-model", "480p"))
        prod = self.studio / "productions" / "spot"
        (prod / "03_board/shotlist.csv").write_text(
            "shot,scene,beat,purpose,size,angle,lens,move,action,dialogue,sound,duration_s,route,refs,status,notes\n"
            "S01,1,,,WS,,,,,,,2,,,planned,\n")
        f = self.tmp / "still.png"
        f.write_bytes(b"png")
        self.ok("take", "add", "LOOK-MAYA", str(f), "--stage", "still", "--cost", "0.10")
        self.ok("take", "rate", "LOOK-MAYA_t001", "select")
        report = self.ok("cost")
        self.assertIn("Shots with a selected take: 0 of 1 planned", report)
        self.assertIn("no pending jobs", self.ok("jobs"))

    def test_edl_and_subtitles(self):
        sys.path.insert(0, str(KIT))
        from filmkit.media import parse_edl
        from filmkit.qc import check_subs
        ev = parse_edl("# note\nS01_t002\nS02_t001 0.4 3.1  # trim\nslate 1.5\n")
        self.assertEqual(ev, [("S01_t002", None, None), ("S02_t001", 0.4, 3.1), ("slate", 1.5, None)])
        srt = self.tmp / "a.srt"
        srt.write_text("1\n00:00:00,000 --> 00:00:02,000\nFine.\n\n2\n00:00:02,000 --> 00:00:02,400\n"
                       "A line far too long to read in under half a second on screen\n")
        report = check_subs(srt)
        self.assertIn("chars/sec", report)
        self.assertIn("on screen 0.40s", report)

    def test_rhythm_and_beat_grid(self):
        from filmkit.review import _beat, rhythm
        flat = "\n".join(rhythm([5.0, 4.8, 5.1, 4.9]))
        self.assertIn("nearly uniform", flat)
        self.assertIn("engine's default length", flat)
        varied = "\n".join(rhythm([0.9, 8.0, 2.0, 1.2, 2.4]))
        self.assertIn("0.9b 8.0H 2.0 1.2b 2.4", varied)
        self.assertNotIn("!", varied)
        self.assertEqual(_beat(2.0, 120, 0.0, 24), ("downbeat 5 on", True))
        self.assertEqual(_beat(1.8, 120, 0.0, 24), ("downbeat 5 -5f", False))
        self.assertEqual(_beat(0.2, 120, 1.0, 24), ("before the music", False))

    def test_gen_dry_run_payloads(self):
        self.ok("new", "Gen")
        prompt = self.tmp / "p.md"
        prompt.write_text("A woman sits alone in a dark kitchen.")
        out = self.ok("gen", "S01", "--via", "ark", "--model", "seedance-2-5", "--prompt-file", str(prompt),
                      "--draft", "--duration", "5", "--dry-run")
        self.assertIn('"draft": true', out)
        self.assertIn('"resolution": "480p"', out)
        out = self.ok("gen", "S01", "--via", "fal", "--model", "fal-ai/some-model", "--prompt-file", str(prompt),
                      "--param", "duration=\"5\"", "--dry-run")
        self.assertIn("https://queue.fal.run/fal-ai/some-model", out)

    def test_take_add_costs_platform_credits(self):
        self.ok("new", "Credits")
        clip = self.tmp / "clip.mp4"
        clip.write_bytes(b"mp4")
        out = self.ok("take", "add", "S01", str(clip), "--stage", "draft", "--tool", "aristotto",
                      "--model", "seedance-2.5-image-to-video", "--credits", "1000")
        self.assertIn("($0.30)", out)  # 1,000 credits at the course rate in rates.json
        self.assertIn("1000 credits", self.ok("take", "list") + (self.studio / next(self.studio.glob("productions/*/04_shots/takes.csv")).relative_to(self.studio)).read_text())

    def test_evolink_uses_a_takes_provider_link(self):
        # EvoLink only takes URLs: a still made with film gen starts a video by its take id
        import csv
        import time
        self.ok("new", "Links")
        still = self.tmp / "still.png"
        still.write_bytes(b"png")
        self.ok("take", "add", "S01", str(still), "--stage", "still")
        takes = next(self.studio.glob("productions/*/04_shots/takes.csv"))
        with takes.open() as f:
            rows = list(csv.DictReader(f))
            fields = list(rows[0].keys())
        rows[0]["source_url"], rows[0]["source_at"] = "https://cdn.example/still.png", str(int(time.time()))
        with takes.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        prompt = self.tmp / "p.md"
        prompt.write_text("She sets the cup down.")
        out = self.ok("gen", "S01", "--via", "evolink", "--model", "seedance-2.0-fast-image-to-video",
                      "--prompt-file", str(prompt), "--image", "S01_t001", "--dry-run")
        self.assertIn("https://cdn.example/still.png", out)


class TestFfmpegDiscovery(unittest.TestCase):
    def test_env_then_full_build_then_path_and_paired_ffprobe(self):
        from unittest import mock
        tmp = Path(tempfile.mkdtemp())
        try:
            for d in ("env", "full"):
                (tmp / d).mkdir()
                for exe in ("ffmpeg", "ffprobe"):
                    (tmp / d / exe).write_text("")
            clean = {k: v for k, v in os.environ.items() if k not in ("FFMPEG", "FFPROBE")}
            with mock.patch.dict(os.environ, clean, clear=True), \
                    mock.patch.object(ff, "FULL_BUILDS", (tmp / "missing", tmp / "full")):
                self.assertEqual(ff.find("ffmpeg"), str(tmp / "full" / "ffmpeg"))
                self.assertEqual(ff.find("ffprobe"), str(tmp / "full" / "ffprobe"))
                os.environ["FFMPEG"] = str(tmp / "env" / "ffmpeg")
                self.assertEqual(ff.find("ffmpeg"), str(tmp / "env" / "ffmpeg"))
                self.assertEqual(ff.find("ffprobe"), str(tmp / "env" / "ffprobe"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


@unittest.skipUnless(FFMPEG, "ffmpeg not available")
class TestMedia(StudioCase):
    def test_pipeline_end_to_end(self):
        self.ok("new", "Pipe", "--duration", "6")
        prod = self.studio / "productions" / "pipe"
        (prod / "03_board/shotlist.csv").write_text(
            "shot,scene,beat,purpose,size,angle,lens,move,action,dialogue,sound,duration_s,route,refs,status,notes\n"
            "S01,1,,,WS,,,,,,,2,,,planned,\nS02,1,,,CU,,,,,,,1.5,,,planned,\n")
        clip = self.media("a.mp4", "testsrc2=s=640x360:r=24:d=3",
                          ["-f", "lavfi", "-i", "sine=f=440:d=3", "-shortest", "-pix_fmt", "yuv420p"])
        tall = self.media("b.mp4", "testsrc=s=360x640:r=30:d=2", ["-pix_fmt", "yuv420p"])
        music = self.media("m.wav", "sine=f=220:d=8", [])
        self.ok("take", "add", "S01", str(clip), "--cost", "0.5")
        self.ok("take", "add", "S02", str(tall), "--cost", "0.5")
        self.ok("animatic")
        self.ok("contact", "--shot", "S01")
        self.ok("boards")
        self.ok("dailies")
        (prod / "06_edit/cut.txt").write_text("S01_t001\nS02_t001 0.2 1.4\nslate 0.5\nS01_t001 1 2.3\n")
        cut = Path(self.ok("assemble").strip())
        info = ff.probe(cut)
        self.assertEqual((info["width"], info["height"]), (1920, 1080))
        expected = (round(2.8 * 24) + round(1.2 * 24) + round(0.5 * 24) + round(1.3 * 24)) / 24
        self.assertAlmostEqual(info["duration"], expected, delta=0.02)  # no timestamp holes at the joins
        # paths relative to the production resolve from the studio root
        (prod / "05_sound/sfx").mkdir(parents=True, exist_ok=True)
        shutil.copy(self.media("hit.wav", "sine=f=900:d=0.3", []), prod / "05_sound/sfx/hit.wav")
        rel_cut = str(cut.relative_to(prod))
        mixed = Path(self.ok("mix", "--video", rel_cut, "--music", str(music),
                             "--fx", "05_sound/sfx/hit.wav@2.5").strip())
        loud = ff.loudness(mixed)
        self.assertAlmostEqual(loud["lufs"], -16, delta=0.6)
        self.assertTrue(Path(self.ok("qc", str(mixed.relative_to(prod))).strip()).exists())
        outs = self.ok("deliver", str(mixed), "--aspects", "9:16,1:1").split()
        self.assertEqual(ff.probe(outs[0])["height"], 1920)

    def test_review_teardown_and_frame_exact_joins(self):
        self.ok("new", "Rev", "--aspect", "16:9")
        prod = self.studio / "productions" / "rev"
        (prod / "03_board/shotlist.csv").write_text(
            "shot,scene,beat,purpose,size,angle,lens,move,action,dialogue,sound,duration_s,route,refs,status,notes\n"
            "S01,1,,,MCU,front,,,,,,2,,,planned,\nS02,1,,,MCU,front,,,,,,1,,,planned,\n")
        for shot, colour in (("S01", "red"), ("S02", "blue")):
            clip = self.media(f"{colour}.mp4", f"color=c={colour}:s=320x180:r=24:d=2", ["-pix_fmt", "yuv420p"])
            self.ok("take", "add", shot, str(clip))
        # a whole take starts 0.1 s in: part of a frame, which used to leave a timestamp hole at the join
        (prod / "06_edit/cut.txt").write_text("S01_t001\nS02_t001 0.5 1.5\n")
        cut = Path(self.ok("assemble").strip())
        self.assertTrue(cut.with_suffix(".txt").read_text().startswith("# cut_v001.mp4 from cut.txt"))
        self.assertAlmostEqual(ff.probe(cut)["duration"], (43 + 24) / 24, delta=0.02)
        out = self.ok("review", "--bpm", "120")
        self.assertIn("J01    1.79s  downbeat 5 -5f", out)
        self.assertIn("same size and angle in the shot list (MCU, front)", out)
        sheet = cut.with_name("cut_v001_joins_1.png")
        pixel = lambda x: subprocess.run([FFMPEG, "-v", "error", "-i", str(sheet), "-vf", f"crop=1:1:{x}:107",
                                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        red, blue = pixel(183), pixel(535)  # the middle of the frame out and the frame in
        self.assertGreater(red[0], 200); self.assertLess(red[2], 60)
        self.assertGreater(blue[2], 200); self.assertLess(blue[0], 60)
        # an editor export has no cut list: the joins are found by picture change
        export = prod / "06_edit/cuts/cut_v002.mp4"
        shutil.copy(cut, export)
        (prod / "06_edit/cut.txt").write_text("S01_t001\n")
        out = self.ok("review")
        self.assertIn("cuts found by picture change", out)
        self.assertIn("J01    1.79s  shot 1 → shot 2", out)
        report = self.ok("teardown", str(cut))
        self.assertIn("2 shots", report)
        self.assertIn("Cuts (s): 1.79", report)
        self.assertTrue((cut.parent / "cut_v001_teardown" / "shots_1.png").exists())

    def test_overlay_graphics_per_shape(self):
        self.ok("new", "Gfx", "--aspect", "16:9")
        bg = self.media("bg.mp4", "color=c=blue:s=320x180:r=24:d=2",
                        ["-f", "lavfi", "-i", "sine=f=440:d=2", "-shortest", "-pix_fmt", "yuv420p"])
        # a transparent card: the left half opaque red, the right half clear
        card = self.media("card.mov", "color=c=red:s=160x180:r=24:d=1,format=rgba,pad=320:180:0:0:color=black@0",
                          ["-c:v", "prores_ks", "-pix_fmt", "yuva444p10le"])
        out = Path(self.ok("overlay", str(bg), f"{card}@0.5").strip())
        self.assertTrue(ff.probe(out)["has_audio"])
        rgb = lambda t, x: subprocess.run([FFMPEG, "-v", "error", "-ss", str(t), "-i", str(out), "-frames:v", "1",
                                           "-vf", f"format=rgb24,crop=1:1:{x}:90", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                          capture_output=True).stdout
        self.assertGreater(rgb(0.2, 80)[2], 150)   # before the card: the picture
        self.assertGreater(rgb(1.0, 80)[0], 150)   # the card's opaque half
        self.assertGreater(rgb(1.0, 240)[2], 150)  # the card's clear half shows the picture
        self.assertGreater(rgb(1.8, 80)[2], 150)   # after the card ends: the picture again

    def test_captions_build_and_burn(self):
        import json
        self.ok("new", "Caps", "--aspect", "9:16")
        words = [{"text": w, "start": 0.3 + i * 0.4, "end": 0.6 + i * 0.4}
                 for i, w in enumerate("Most people use AI to help them work.".split())]
        wj = self.tmp / "words.json"
        wj.write_text(json.dumps(words))
        lines = self.tmp / "lines.txt"
        lines.write_text("Most people use AI\nto help them work.\n")
        out = self.ok("captions", "build", str(wj), "--lines", str(lines), "--style", "social")
        self.assertIn("2 captions", out)
        ass = self.tmp / "words.social.ass"
        self.assertIn("PlayResY: 1920", ass.read_text())
        bad = self.tmp / "bad.txt"
        bad.write_text("Completely different words here\n")
        self.assertNotEqual(film(self.studio, "captions", "build", str(wj), "--lines", str(bad)).returncode, 0)
        bg = self.media("bg.mp4", "color=c=gray:s=360x640:r=24:d=3", ["-pix_fmt", "yuv420p"])
        r = film(self.studio, "captions", "burn", str(bg), str(ass))
        if "no subtitles filter" not in r.stderr:
            self.assertEqual(r.returncode, 0, msg=r.stderr)


if __name__ == "__main__":
    unittest.main()
