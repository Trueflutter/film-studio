# The visual plan and the spec

## visual_plan.md

One header block, then one row per beat:

```markdown
# <Title> · visual plan
Shape: 16:9 1920×1080 30 fps · Length: 2:48 (voice) · Brand: brand.md
Generation: 5 presenter clips (about 6,500 credits) + 2 B-roll takes (about 5,200) · everything else in code or ChatGPT stills
Layer shares: presenter 21% · presenter + graphic 14% · motion graphics 38% · stills 22% · B-roll 5%

| # | Time | Words (short) | Layer | What we see | Graphic, and the word it lands on | Sound |
|---|---|---|---|---|---|---|
| 1 | 0:00-0:05.2 | "Buying off-plan sounds risky..." | presenter | Clip 1: close-up, three-quarter left, slow push-in | lower third on "I'm": name + series | soft whoosh |
| 2 | 0:05.2-0:11.0 | "...so here's how a 60/40 plan works." | motion graphic | full-screen dark scene | "60/40" types in on "60/40", bar splits 60 | 40 on "works" | tick, pop |
| 3 | 0:11.0-0:16.4 | "Sixty percent during construction..." | graphic | timeline 2026 to 2028 draws left to right | instalment dots pop on "during", handover pin on "rest" | draw, pop x4 |
| 4 | 0:16.4-0:20.0 | "...the creek, ten minutes from Downtown." | still + move | place pack, wide, slow push | map pin + "10 min" chip on "ten minutes" | ambience |
```

Presenter rows name the clip (from the presenter-video plan), its angle and distance. Still rows name the file from the pack. Every graphic names its word.

## SPEC.md (for the HyperFrames build)

```markdown
# <Title>: motion graphics spec

Build <one composition / sections A to D, each its own composition>, <W×H>, 30 fps, <length>, render to `out/<name>.mp4` with base.mp4's audio.

## Inputs (assets/)
- base.mp4: the locked edit (picture + voice). Bottom track, played in full, never retimed.
- words.json: every word with start/end in output seconds. Land every graphic on its word: arrive 0.10 s before it.
- Fonts: <files>. Logo: <file> (never redraw). Stills: <files>.

## Brand
<tokens from brand.md: surface, ink, secondary, muted, hairline, ONE accent and where it may appear>. Sentence case. Banned list: see look.md.

## Motion
Presets from motion.md: enter, spring-ui, type-reveal, count, draw, bar-grow, exit, drift, push. Every full-screen scene drifts. Exits 0.2 s and finish before the next arrival.

## Timeline
1. 0.00-5.20 presenter. Lower third at 0.6-3.8: "<Name>" / "<Series>", hairline draws left to right.
2. 5.20-11.00 GRAPHIC (base is dark here). "<headline>" type-reveal on "<word>"; ...
...

## Deliverables
- Project lint/check clean.
- Snapshots at <each arrival + 0.4 s>, saved to out/snapshots/ and looked at; scores and fixes in out/review_log.md.
- out/<name>.mp4 (H.264, AAC) with the voice as the only audio (music and effects are mixed after).
- out/CUES.md: the output time and type of every arrival.
```

## Long explainers (over 60 s)

Split at section boundaries (each section starts on the presenter or a title scene). Build, check and render each section; join with `ffmpeg -f concat` (same codec settings) or the kit's `film assemble`; then mix sound once over the whole thing. Keep one shared `brand.css` and presets file so the sections match.
