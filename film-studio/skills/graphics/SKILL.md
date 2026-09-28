---
name: graphics
description: Builds the text and graphics layer in code - end cards, title and time cards, supers, lower thirds, product and phone-screen UI, kinetic type, logo stings - with HyperFrames. Claude renders stills, critiques them and fixes them before anyone watches, lays out each aspect ratio separately, and hands over a transparent overlay that `film overlay` or the editor puts on the picture. Use for any end card, title, on-screen text, UI insert or motion graphic in a film or ad.
---

# Graphics

Models scramble letters, so text and UI are never generated (handbook 09). They're built in code: exact words, exact fonts, the real product, and a program Claude can render, look at and fix. Read `${CLAUDE_PLUGIN_ROOT}/handbook/09-editing-and-finishing.md` ("Text and graphics in code") first.

## Setup (once per machine)

- Node 22 or later (`film doctor` shows it).
- The HyperFrames plugin (Apache 2.0: free for any company, commercial use included): `claude plugin marketplace add heygen-com/hyperframes`, then `claude plugin install hyperframes@hyperframes`. Its `/hyperframes` skills own the framework (timing attributes, animation, rendering). This skill owns what the film needs from it.
- Optional: `npx hyperframes telemetry disable` turns off its anonymous usage telemetry. Never run `hyperframes publish` on client work: it uploads the project.

## Brief first, no code before it

Write `06_edit/graphics/<name>/brief.md` in five lines and get the director's OK:
1. **The words**, exactly as approved. On an ad they come from the brief's proposition and CTA; never invent a claim, a price or a statistic.
2. **The job:** land the proposition, name the product, set time and place ("DAY 14"), label a speaker, show a real screen.
3. **Where it sits:** a full-frame card at the end, or over which shot, from what time, for how long.
4. **Brand:** font files, one accent colour, the logo file. Put them in the project's `assets/`.
5. **Sound:** the cue it lands on (the sonic logo, the music's resolve; handbook 08).

## Build

- One HyperFrames project per graphic per shape: `npx hyperframes init 06_edit/graphics/endcard_9x16 --example blank --resolution portrait --non-interactive` (`landscape` for 16:9, `square` for 1:1; for 4:5 or 2.39:1, have the hyperframes skill set the canvas size). The second shape is its own layout built from the first, never a crop of it.
- **Over picture** (supers, lower thirds, UI on a screen generated blank): a transparent page (`html, body { background: transparent }`). **A full-frame card** has its own background: match it to the last shot or the outro so they flow (handbook 17, ONE APPLICANT v11).
- **Real UI only.** Use the product's real screenshots and logo (the client's files, or a capture of the live site with the hyperframes skill). Never draw a product screen from imagination.
- Everything the page needs lives in the project folder: fonts, logo, screenshots. No random values, clocks or network calls in the animation: every render must come out the same.

## The look

- **Banned defaults:** a centred title on a gradient, everything fading in, bouncy easing on type, glows, frame borders and corner labels, particle bursts, two accent colours fighting.
- One display face and one text face; one accent unless the brand says otherwise.
- **Motion with mass:** elements arrive, overshoot a hair and settle (a tiny overshoot on UI, none on type). Hold the proposition still long enough to read twice.
- **Readable on a phone:** nothing that must be read smaller than about 40 px on a 1080-wide frame. On 9:16 keep text out of the top 15%, the bottom 20% and the right edge where the platform's buttons sit (handbook 14).
- **One thing first:** a clear order of reading; the CTA last.

## Look before anyone watches

1. `npx hyperframes check 06_edit/graphics/<name>` until it's clean.
2. `npx hyperframes snapshot 06_edit/graphics/<name> --at <arrival>,<settled read>,<exit>` and open the PNGs it lists. Phone test on the render: `film frames <render> --at <t> --width 360`.
3. Score 1-10: reads at phone size · one thing first · motion (arrives with mass, no dead or frantic moments) · brand accuracy · composition and safe zones · fit with the film (colour, pace, the sound cue).
4. Fix the three worst, snapshot again. Repeat until every score is 8 or more, two rounds at least. Log each round in `06_edit/graphics/<name>/review_log.md`. Never score 8 out of politeness.
5. Only then render and show the director.

## Render and hand over

- Render at the production's frame rate: `npx hyperframes render 06_edit/graphics/endcard_9x16 --format mov --fps 24 -o 06_edit/graphics/endcard_9x16/renders/endcard.mov`. MOV keeps the transparency (ProRes 4444). If an editor drops it, render `--format png-sequence` and import the frames.
- In the cut, keep the card's place with a `slate` of its length at the end of `cut.txt`; the master stays text-free (handbook 14).
- After `film deliver`, put each shape's graphics on its own file: `film overlay 07_delivery/masters/<slug>_9x16_v001.mp4 06_edit/graphics/endcard_9x16/renders/endcard.mov@38.5` (add more `render@seconds` for supers). Captions go on after that, on the `_gfx` file.
- Or composite them on the track above the picture in Resolve or Premiere for your main shape.
