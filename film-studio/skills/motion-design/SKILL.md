---
name: motion-design
description: Use when a video needs motion graphics, animated charts or graphs, counters, maps, diagrams, kinetic type, lower thirds, slides inserted into a video, an explainer, a presenter or talking-head video "with graphics", a YouTube or Shorts explainer, a product or property walkthrough, a logo sting, or an edit brief that mentions graphics; also when graphics look template-like, cheap, cluttered or off the beat of the voice.
---

# Motion design: the explainer that stays economical

A 3 to 5 minute explainer is never 3 to 5 minutes of generated video. **The voice runs the whole way; the picture changes layer by layer**, and most layers are built in code for free. Generated video is the spice, not the meal.

| Layer | Share of runtime | Cost |
|---|---|---|
| Presenter on camera (lip-synced clips, one setting, varied angle and distance) | 15 to 25% | the expensive part: 4 to 6 short clips |
| Presenter beside a graphic (split, picture-in-picture) | 10 to 20% | reuses the same clips |
| Full-screen motion graphics: charts drawing, counters, maps, steps, comparisons, kinetic type | 30 to 40% | free (code) |
| Stills with a slow camera move (GPT Image, the place pack, product shots) | 15 to 25% | free on ChatGPT |
| Slides inserted as designed full-screen scenes | as needed | free (code) |
| Short generated B-roll where real motion matters (aerial, a door opening) | 0 to 10% | a few takes |

A faceless piece (no presenter) splits the presenter's share between motion graphics and stills.

**Length:** after tightening, voices run about 2.7 to 3 words a second. 90 words is about 30 s; a 3 minute explainer is about 500 words.

## 1. Inputs (ask once, then decide)

The approved script and its final voice file with **word timings** (`words.json`: transcribe the final, tightened voice, never the pre-tightened one), the presenter's reference pack, the place pack, the brand (fonts, one accent colour, the real logo file; for an invented or spec brand with no logo, set the name as a wordmark in the display face and say so), the shape (16:9 YouTube or 9:16 Shorts: build each shape as its own layout).

## 2. The visual plan (one OK)

Write `visual_plan.md` (format in `reference/plan-and-spec.md`): one row per sentence or beat, with the time from `words.json`, the words, the **layer** (from the table), what we see, the graphic and **the word it lands on**, and the sound cue. Rules:

- Change what we see every 3 to 6 seconds, but **one idea per scene**. A number gets a counter or a chart; a process gets steps that connect; a comparison gets a split; a place gets a still or B-roll; a claim gets kinetic type.
- The presenter opens, returns at each new section, and closes. Never more than 4 s on the face before the frame changes (a punch-in, a cut to a different angle, or a graphic beside her).
- Check the layer shares against the table and show the total generation cost in one line.

Show the plan on one board or as one table. Nothing is built before the OK.

## 3. Build

1. `SPEC.md` from the plan (template in `reference/plan-and-spec.md`), then the HyperFrames skills do the framework work: `/talking-head-recut` for graphics over the presenter, `/motion-graphics` or `/faceless-explainer` for full-screen scenes, `/slideshow` for slide inserts, `/hyperframes-registry` **before hand-building** any chart, map, terminal, transition or effect. Search it once per graphic; if nothing fits the exact idea (a split bar, a payment timeline), hand-build it with the presets and note "built by hand" in the spec.
2. One composition per section of 30 to 60 s for long pieces (render and check each, then join), one composition for short ones. The base edit (presenter clips + stills + B-roll + voice) is the bottom track; never retime it.
3. Every graphic arrives **0.1 s before its word** and exits before the next one arrives. Motion numbers are in `reference/motion.md`: use them, don't improvise easing.
4. The house look and the banned list are in `reference/look.md`. Read it before writing any CSS.
5. Write `CUES.md`: the output time and type of every arrival (whoosh, pop, tick, type, impact) for the sound mix.

## Finishing a generated film

For brand films and anything cinematic: flash, zoom punch, speed ramps, whip, light leak, halation and grain go on in the edit with `scripts/finish.py`, never in the video prompt. Usage and limits in `reference/finishing.md`. Finish first, then graphics, then the sound mix.

## 4. Look before anyone watches

`npx hyperframes check`, then snapshots at the first second, every arrival + 0.4 s (settled), and every scene change. Open them and score each 1 to 10 on: reads at phone size, one thing first, motion with mass, brand, clears the face and the platform's buttons, matches the voice. Fix the worst three and snapshot again; render only when everything is 8 or more. Then decode stills from the **final MP4** at the same times and scan for one-frame pops. "It compiled" is not done.

## Rules

- Hero stills shown full screen for more than 3 s: make them at 2K (Aristotto Sunburst); ChatGPT landscape stills are about 1672×941 and go soft when they drift.
- Never generate text, numbers, logos, charts or UI with an image or video model. Code only, with the exact approved words and numbers. Never invent a statistic.
- One accent colour, one display face, one text face. Brand from the user's files.
- Name the build tool and the presets in the spec, so the next episode comes out the same.
- Ask for one note at a time, in edit language ("the 60/40 lands late", "less on screen during the price").
