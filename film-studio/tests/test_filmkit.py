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
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg")


def film(project: Path, *args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "FILM_PROJECT": str(project), "PYTHONPATH": str(KIT)}
    return subprocess.run([sys.executable, "-m", "filmkit", *args], cwd=project, env=env,
                          capture_output=True, text=True)


class StudioCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
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
        sys.path.insert(0, str(KIT))
        from filmkit import ff
        info = ff.probe(cut)
        self.assertEqual((info["width"], info["height"]), (1920, 1080))
        expected = (round(2.8 * 24) + round(1.2 * 24) + round(0.5 * 24) + round(1.3 * 24)) / 24
        self.assertAlmostEqual(info["duration"], expected, delta=0.06)
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
