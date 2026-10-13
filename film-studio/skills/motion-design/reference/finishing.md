# Finishing: the cinematic edit layer

Video models do single moves, light, atmosphere and materials beautifully. They do transitions and effects badly. So the effects go on in the edit, with `scripts/finish.py` (ffmpeg only):

```bash
python3 <skill>/scripts/finish.py take.mp4 take_fin.mp4 --flash 8.0 --zoom 8.0 --ramp 9.4-11.6:0.5 --whip 12.0 --leak 12.1:0.9 --halation 0.2 --grain 5
```

All times are in the take's own seconds; the script prints where each effect lands in the output (ramps change the length), so graphics and sound cues use the printed times.

| Effect | Use | Default |
|---|---|---|
| `--flash T` | the music drop, the moment the lights come on | 2 frames |
| `--zoom T` | a punch into a hard cut, adds energy | 1.0 to 1.14 over 0.25 s, eases back |
| `--ramp A-B:S` | slow motion on the hero (0.4 to 0.6), or a speed-up through a transition (1.5 to 2) | eased edges, interpolated slow motion |
| `--whip T` | hide a cut inside a horizontal blur | about 0.12 s |
| `--leak T:D` | a warm bloom on the reveal or the end card | 0.55 strength |
| `--halation K` | glow around highlights, a filmic look | 0.15 to 0.25 |
| `--grain N` | ties generated shots together | 4 to 6 |

Rules: one flash per film (on the drop), at most two zoom punches, one slow-motion ramp on the hero, one whip. More than that reads as a template. Slow motion is computed frame by frame: a 15 s take takes about 3 minutes on a laptop. Then the graphics composition goes on top (logo end card with a light sweep, any supers), then the sound mix (the ramps change timing, so mix after finishing).
