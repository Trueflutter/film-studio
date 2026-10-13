# Motion: the numbers

Use these unless the brand says otherwise. All animation is a pure function of time (seek-safe): set every from-state at t=0, no CSS transitions, timers or random values.

## Eases in GSAP (copy this, don't improvise)

GSAP has no cubic-bezier or spring ease without plugins. Paste these at the top of the timeline script and use the constants:

```js
function bez(x1, y1, x2, y2) {            // CSS cubic-bezier as a GSAP ease
  const cx = 3*x1, bx = 3*(x2-x1)-cx, ax = 1-cx-bx, cy = 3*y1, by = 3*(y2-y1)-cy, ay = 1-cy-by;
  const X = t => ((ax*t+bx)*t+cx)*t, Y = t => ((ay*t+by)*t+cy)*t, dX = t => (3*ax*t+2*bx)*t+cx;
  return p => { if (p <= 0) return 0; if (p >= 1) return 1; let t = p;
    for (let i = 0; i < 8; i++) { const e = X(t)-p; if (Math.abs(e) < 1e-5) break; const d = dX(t); if (Math.abs(d) < 1e-6) break; t -= e/d; }
    return Y(t); };
}
function spring(stiff, damp, dur) {        // damped spring over `dur` seconds as a GSAP ease
  const w0 = Math.sqrt(stiff), z = damp/(2*w0), wd = w0*Math.sqrt(1-z*z);
  return p => { if (p <= 0) return 0; if (p >= 1) return 1; const t = p*dur;
    return 1 - Math.exp(-z*w0*t)*(Math.cos(wd*t) + (z*w0/wd)*Math.sin(wd*t)); };
}
const EASE_ENTER = bez(0.16, 1, 0.3, 1), EASE_DRAW = bez(0.65, 0, 0.35, 1);
const SPRING_UI = spring(220, 22, 0.8), SPRING_SOFT = spring(140, 20, 1.0);
// use the spring's own duration as the tween duration: { duration: 0.8, ease: SPRING_UI }
```

Build gotchas found in testing:
- **SVG shapes scale from the wrong point** with `transformOrigin`; use `svgOrigin: "x y"` (SVG coordinates).
- **Push transitions:** put the scene's background on the wrapper that slides, not on the clip, or the push shows an empty frame.
- **Two `fromTo` tweens on one element** (a push in, then a push out): give the second `immediateRender: false`.
- Lint warnings that every top-level scene "needs a subcomposition", or that an intentional heading swap overlaps, are fine for a single-section piece. Errors are not.

## Timing to the voice

- Arrive **0.10 s before** the word starts (the eye leads the ear). Big reveals (a headline, the price) 0.15 s before.
- A list stacks **one item per word**, never all at once.
- Exits are quick (0.20 to 0.25 s) and finish **before** the next graphic arrives. Nothing overlaps unless it's one graphic transforming into the next.
- Hold anything to be read for **at least 2x its reading time** (about 0.3 s per word, minimum 1.2 s). If the voice moves on sooner, **the voice wins**: the graphic leaves on time and you cut its words down instead (fewer words on screen, or a number without its label).
- **No scene holds over about 6 s unchanged.** A long beat (a 60/40 explanation of 8 s) becomes two or three states of the same graphic: the bar, then the first amount counting, then the second, each on its word, or a push to a closer framing.
- A graphic that isn't spoken about leaves. Dead holds over 1 s with nothing moving get a slow drift.

## Presets

| Preset | Use | Values |
|---|---|---|
| `enter` | cards, chips, panels | 0.45 s, ease-out cubic-bezier(0.16, 1, 0.3, 1), from y+24 px and opacity 0 |
| `spring-ui` | notifications, buttons, pins | spring stiffness 220, damping 22 (one small overshoot, about 4%) |
| `spring-soft` | large panels, presenter PiP | stiffness 140, damping 20, no visible bounce |
| `type-reveal` | headlines | masked wipe up by line, 0.5 s, stagger 0.06 s per line; never bounce type |
| `word-stagger` | kinetic type | 0.05 s per word, 0.35 s each, from y+12 px |
| `count` | numbers | 0.8 to 1.2 s, ease-out, land exactly on the spoken figure; tabular figures |
| `draw` | lines, chart strokes, connectors | stroke-dashoffset, 0.6 to 1.0 s, ease-in-out cubic-bezier(0.65, 0, 0.35, 1) |
| `bar-grow` | bar charts | from the baseline, 0.6 s each, stagger 0.12 s, value labels count with them |
| `exit` | everything | 0.2 s ease-in, opacity to 0 and y-8 px or scale 0.98 |
| `drift` | full-screen scenes, stills | scale 1.00 to 1.05 over the whole scene, linear, or a 2 to 4% pan |
| `push` | scene change | the new scene slides over 0.35 s while the old moves 30% the other way (parallax), no crossfade |

## Transitions between scenes

- Prefer a **cut on the word** or an **object-driven** transition (a chart bar becomes the next panel, the map pin opens into the card).
- Banned: crossfades between designed scenes, spins, flips, zoom blurs, "swoosh" wipes with trails.
- One primary move per transition.

## Stills and B-roll moves

- Every still moves: a slow push (1.00 to 1.06), a pan along the subject's direction, or a parallax split of foreground and background. Direction follows the story (into the building = push in).
- Cut stills on the voice's phrase boundaries, 2.5 to 5 s each.

## Charts and numbers

- One message per chart; label the one bar or point that matters in the accent colour, the rest in muted ink.
- Axes minimal (a baseline, no grid or a hairline grid). Units in the label, not a legend.
- The spoken number and the on-screen number must match exactly ("from AED 1.4m" on screen as "AED 1.4m").
