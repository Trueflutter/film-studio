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
    def test_board_text_cards(self):
        self.ok("new", "Monday Brief", "--format", "social")
        prod = self.studio / "productions" / "monday-brief"
        c = prod / "01_story" / "concepts"
        c.mkdir(parents=True)
        (c / "c1.md").write_text("# Now You Can\n**First second:** big type\n\n- Story card\n- Her line <ok>\n")
        (c / "c2.md").write_text("# The Monday Brief\nCalm desk read.\n")
        out = self.ok("board", "Concepts", str(c / "c1.md"), str(c / "c2.md") + "|Calm", "--no-open")
        page = Path(out.strip()).read_text()
        self.assertIn("class='opts text'", page)
        self.assertIn("<h3>Now You Can</h3>", page)
        self.assertIn("<b>First second:</b> big type", page)
        self.assertIn("<li>Her line &lt;ok&gt;</li>", page)
        self.assertIn("Calm", page)

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

    def test_frame_counts_are_cumulative(self):
        from filmkit.media import frame_counts
        # ten 0.52 s events at 24 fps: each alone rounds to 12 frames (6 s early overall); cumulative stays on the frame
        counts = frame_counts([0.52] * 10, 24)
        self.assertEqual(sum(counts), round(5.2 * 24))
        self.assertEqual(counts[:3], [12, 13, 12])
        self.assertEqual(frame_counts([0.001, 0.001], 24), [1, 1])  # never zero frames

    def test_guard_range_keeps_clear_of_cuts(self):
        from filmkit.media import guard_range
        # untouched: the cut is 0.3 s past the range
        self.assertEqual(guard_range([2.0], 0.5, 1.7, 4.0), (0.5, 1.7, None))
        # crossing: the bigger side (before the cut) wins, stopping 0.05 s short of it
        s, e, cut = guard_range([2.0], 1.0, 2.6, 4.0)
        self.assertEqual((round(s, 3), round(e, 3), cut), (1.0, 1.95, 2.0))
        # touching from the far side: starts 0.05 s inside the next shot
        s, e, cut = guard_range([2.0], 1.98, 3.5, 4.0)
        self.assertEqual((round(s, 3), round(e, 3), cut), (2.05, 3.5, 2.0))
        # an in point just after a cut is touching too
        self.assertEqual(guard_range([2.0], 2.02, 3.0, 4.0)[0], 2.05)

    def test_mix_option_parsers(self):
        from filmkit.sound import load_cues, parse_bed, parse_lift
        self.assertEqual(parse_lift("30.5:-12"), (30.5, -12.0))
        self.assertEqual(parse_bed("sfx/rain.wav@4-20:-26"), ("sfx/rain.wav", 4.0, 20.0, -26.0))
        self.assertEqual(parse_bed(r"C:\sfx\rain.wav@4.5-20", -24)[0], r"C:\sfx\rain.wav")
        self.assertEqual(parse_bed("r.wav@0-3", -24)[3], -24.0)
        for bad in ("rain.wav", "rain.wav@20-4:-20"):
            with self.assertRaises(Exception):
                parse_bed(bad)
        cues = self.tmp / "cues.json"
        cues.write_text('[{"file": "hit.wav", "at": 2.5, "db": -6, "max": 0.4}, {"file": "tick.wav", "at": 1}]')
        got = load_cues(cues)
        self.assertEqual((got[0]["at"], got[0]["db"], got[0]["max"]), (2.5, -6.0, 0.4))
        self.assertEqual((got[1]["db"], got[1]["max"]), (0.0, None))

    def test_speech_chunks_split_on_gaps(self):
        from filmkit.sound import speech_chunks
        words = [{"start": 0.2, "end": 0.6}, {"start": 0.7, "end": 1.1}, {"start": 1.9, "end": 2.3},
                 {"start": 2.5, "end": 2.6}, {"start": 3.2, "end": 3.6}]
        spans = speech_chunks(words, 4.0)
        self.assertEqual([(round(a, 2), round(b, 2)) for a, b in spans], [(0.16, 1.17), (1.86, 2.67), (3.16, 3.67)])

    def test_default_still_model_is_gpt_image_2_5(self):
        from filmkit.gen import default_image_model, rate_for
        self.assertEqual(default_image_model("evolink"), "gpt-image-2.5")
        self.assertEqual(default_image_model("ark"), "")
        self.assertEqual(rate_for("ark", "seedance-2-5", "480p"), 0.10)  # the rate table still reads
        self.ok("new", "Stills")
        prompt = self.tmp / "p.md"
        prompt.write_text("A kitchen at dawn.")
        out = self.ok("gen", "S01", "--via", "evolink", "--image-gen", "--prompt-file", str(prompt), "--dry-run")
        self.assertIn("gpt-image-2.5", out)
        self.assertNotEqual(film(self.studio, "gen", "S01", "--via", "ark", "--image-gen",
                                 "--prompt-file", str(prompt), "--dry-run").returncode, 0)

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

    def test_voice_tighten(self):
        import json
        import wave
        sr = 16000
        voice = self.tmp / "vo.wav"
        with wave.open(str(voice), "wb") as w:  # four 0.4 s "words" in a 4 s file, separated by pauses
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            import math
            for i in range(4 * sr):
                t = i / sr
                on = any(a <= t < a + 0.4 for a in (0.2, 0.7, 1.9, 3.2))
                w.writeframes(int(8000 * math.sin(2 * math.pi * 300 * t) * on).to_bytes(2, "little", signed=True))
        words = [{"text": f"w{i}", "start": a, "end": a + 0.4} for i, a in enumerate((0.2, 0.7, 1.9, 3.2))]
        wj = self.tmp / "vo.words.json"
        wj.write_text(json.dumps(words))
        out = self.tmp / "vo_tight.wav"
        report = self.ok("voice", "tighten", str(voice), "--words", str(wj), "--out", str(out))
        # chunks (0.16-1.17, 1.86-2.37?) hold 'w0 w1' and the two lone words: 3 chunks, 2 gaps of 0.2 s
        self.assertIn("3 chunks", report)
        self.assertIn("4.00s →", report)
        self.assertIn("words/sec", report)
        spans = [(0.16, 1.14), (1.86, 2.37), (3.16, 3.67)]
        expected = (sum(b - a for a, b in spans) + 0.4) / 1.15
        self.assertAlmostEqual(ff.probe(out)["duration"], expected, delta=0.04)
        # a pitch-preserving speed-up: the tone stays near 300 Hz (a resample would give ~345 Hz)
        zero = self.tmp / "t.raw"
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-ss", "0.08", "-t", "0.25", "-i", str(out), "-f", "s16le",
                        "-ac", "1", "-ar", "16000", str(zero)], check=True)
        pcm = zero.read_bytes()
        vals = [int.from_bytes(pcm[i:i + 2], "little", signed=True) for i in range(0, len(pcm), 2)]
        crossings = sum(1 for a, b in zip(vals, vals[1:]) if a < 0 <= b)
        self.assertAlmostEqual(crossings / 0.25, 300, delta=15)

    def test_assemble_shot_guard_and_frame_exact_cuts(self):
        self.ok("new", "Guard", "--aspect", "16:9")
        prod = self.studio / "productions" / "guard"
        (prod / "03_board/shotlist.csv").write_text(
            "shot,scene,beat,purpose,size,angle,lens,move,action,dialogue,sound,duration_s,route,refs,status,notes\n"
            "S01,1,,,WS,,,,,,,2,,,planned,\nS02,1,,,CU,,,,,,,1,,,planned,\n")
        # one source clip with a hard cut of its own at 1.0 s (red then blue), plus a plain green one
        multi = self.media("multi.mp4", "color=c=red:s=320x180:r=24:d=1[a];color=c=blue:s=320x180:r=24:d=1[b];"
                           "[a][b]concat=n=2:v=1:a=0", ["-pix_fmt", "yuv420p"])
        green = self.media("green.mp4", "color=c=green:s=320x180:r=24:d=2", ["-pix_fmt", "yuv420p"])
        self.ok("take", "add", "S01", str(multi))
        self.ok("take", "add", "S02", str(green))
        # 0.2-1.02 runs 0.02 s past the cut: without the guard its last frame is blue
        (prod / "06_edit/cut.txt").write_text("S01_t001 0.2 1.02\nS02_t001 0.1 0.62\nS02_t001 0.1 0.62\nS02_t001 0.1 0.62\n")
        r = film(self.studio, "assemble")
        self.assertEqual(r.returncode, 0, msg=r.stderr)
        self.assertIn("crosses a cut at 1.00s", r.stderr)
        self.assertIn("warning:", r.stderr)  # 0.75 s kept for 0.82 s asked: slowed 9%, over the 8% line
        cut = Path(r.stdout.strip())
        total = round((0.82 + 3 * 0.52) * 24)  # 0.82 + 1.56 s = 2.38 s -> 57 frames, not 20 + 3 * 12 = 56
        self.assertEqual(round(ff.probe(cut)["duration"] * 24), total)
        px = lambda t: subprocess.run([FFMPEG, "-v", "error", "-ss", str(t), "-i", str(cut), "-frames:v", "1",
                                       "-vf", "format=rgb24,crop=1:1:160:90", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                      capture_output=True).stdout
        last_red = px((20 - 1) / 24)
        self.assertGreater(last_red[0], 200); self.assertLess(last_red[2], 60)   # still red on the last frame
        self.assertGreater(px(20 / 24)[1], 100)                                   # green starts exactly on frame 20
        # opting out takes the range as written
        off = film(self.studio, "assemble", "--no-shot-guard")
        self.assertNotIn("crosses a cut", off.stderr)

    def test_bed_align_lands_the_payoff(self):
        import math
        import random
        import wave
        sr, bpm = 8000, 120
        rnd = random.Random(7)
        beat = 60 / bpm
        pat = [rnd.choice([220, 262, 330, 392, 440, 523, 659, 784]) for _ in range(8)]  # two bars, repeated
        samples = []
        for _ in range(3):
            for f in pat:
                n = int(beat * sr)
                samples += [int(12000 * math.exp(-6 * t / sr) * (math.sin(2 * math.pi * f * t / sr)
                            + 0.5 * math.sin(2 * math.pi * f * 2.01 * t / sr))) for t in range(n)]
        for t in range(4 * sr):  # the payoff at 12 s: a louder sustained chord
            samples.append(int(6300 * (math.sin(2 * math.pi * 196 * t / sr) + math.sin(2 * math.pi * 247 * t / sr)
                                       + math.sin(2 * math.pi * 294 * t / sr))))
        track = self.tmp / "track.wav"
        with wave.open(str(track), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes(b"".join(v.to_bytes(2, "little", signed=True) for v in samples))
        # not enough runway: the payoff is at 12 s but must land at 20 s -> one 4-bar (8 s) loop
        out = self.tmp / "bed.wav"
        report = self.ok("bed", "align", str(track), "--landing", "12", "--at", "20", "--bpm", "120", "--out", str(out))
        self.assertIn("repeated 1x", report)
        self.assertIn("4 bars", report)
        self.assertAlmostEqual(ff.probe(out)["duration"], 24.0, delta=0.01)
        landed = float(report.split("payoff lands at ")[1].split("s")[0])
        self.assertAlmostEqual(landed, 20.0, delta=0.005)
        corr = float(report.split("splice correlation ")[1].split()[0].rstrip(","))
        self.assertGreater(corr, 0.9)
        # no tempo given: it is estimated from the onsets, and an extension that is not a whole loop is trimmed at the head
        out2 = self.tmp / "bed2.wav"
        report = self.ok("bed", "align", str(track), "--landing", "12", "--at", "18", "--out", str(out2))
        self.assertAlmostEqual(float(report.split("payoff lands at ")[1].split("s")[0]), 18.0, delta=0.005)
        self.assertAlmostEqual(ff.probe(out2)["duration"], 22.0, delta=0.01)
        # runway to spare: the head is just trimmed
        report = self.ok("bed", "align", str(track), "--landing", "12", "--at", "9", "--out", str(self.tmp / "bed3.wav"))
        self.assertIn("runway", report)
        self.assertAlmostEqual(float(report.split("payoff lands at ")[1].split("s")[0]), 9.0, delta=0.005)
        # silence has no pulse: say so instead of guessing
        quiet = self.media("quiet.wav", "anullsrc=r=8000:cl=mono", ["-t", "30"])
        r = film(self.studio, "bed", "align", str(quiet), "--landing", "10", "--at", "20")
        self.assertNotEqual(r.returncode, 0)

    def test_mix_levels_lift_cues_beds_and_fade(self):
        import math
        self.ok("new", "Mixer", "--duration", "6")
        video = self.media("v.mp4", "color=c=black:s=320x180:r=24:d=6", ["-pix_fmt", "yuv420p"])
        dia = self.media("dia.wav", "sine=f=300:d=1.5", [])
        music = self.media("mus.wav", "sine=f=220:d=6", [])
        hit = self.media("hit.wav", "sine=f=900:d=2", [])
        rain = self.media("rain.wav", "anoisesrc=d=1:c=pink:a=0.3", [])
        cues = self.tmp / "cues.json"
        cues.write_text(f'[{{"file": "{hit}", "at": 4.0, "db": -6, "max": 0.5}}]')
        out = Path(self.ok("mix", "--video", str(video), "--dialogue", str(dia), "--music", str(music),
                           "--duck-db", "-21", "--lift", "3:-9", "--cues", str(cues),
                           "--amb", f"{rain}@0.5-5:-30", "--fade-out", "1", "--target", "-14").strip())
        loud = ff.loudness(out)
        self.assertAlmostEqual(loud["lufs"], -14, delta=0.6)
        self.assertLessEqual(loud["true_peak"], -0.9)
        from filmkit.sound import _pcm
        x = _pcm(out, 8000, 1)
        db = lambda a, b: 20 * math.log10(max(1e-9, math.sqrt(sum(v * v for v in x[int(a * 8000):int(b * 8000)]) / ((b - a) * 8000))) / 32768)
        # after the voice: the bed sits low, then the lift at 3 s raises it by about 12 dB
        before, after = db(2.0, 2.6), db(3.5, 3.9)
        self.assertGreater(after - before, 8)
        self.assertLess(after - before, 14)
        self.assertGreater(db(4.0, 4.4), after + 1)       # the cue (a loud 900 Hz hit) shows on top
        self.assertLess(db(5.85, 5.99), after - 15)       # the one-second fade-out has emptied the end
        # old options still work
        self.ok("mix", "--video", str(video), "--music", str(music), "--fx", f"{hit}@2.5")

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
