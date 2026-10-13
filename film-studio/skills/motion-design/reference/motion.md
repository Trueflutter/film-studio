# Motion: the numbers

Use these unless the brand says otherwise. All animation is a pure function of time (seek-safe): set every from-state at t=0, no CSS transitions, timers or random values.

## Timing to the voice

- Arrive **0.10 s before** the word starts (the eye leads the ear). Big reveals (a headline, the price) 0.15 s before.
- A list stacks **one item per word**, never all at once.
- Exits are quick (0.20 to 0.25 s) and finish **before** the next graphic arrives. Nothing overlaps unless it's one graphic transforming into the next.
- Hold anything to be read for **at least 2x its reading time** (about 0.3 s per word, minimum 1.2 s).
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
