# 09 · Editing and Finishing

A generated clip is raw material, not a shot. The edit decides which 1-3 seconds the audience sees, where the eye lands at every join, and whether twenty clips from three engines feel like one film. Most of what reads as "AI" in a finished piece was left in by the editor, so this is where realism levers 9 (short takes, best seconds), 10 (edit to hide and to breathe) and 12 (one finish) do their work.

## The short version

1. **Selects first.** Find the best 1-3 seconds of every take before you build anything. Clips degrade late.
2. **Never hard-cut two separately generated clips of the same subject at the same size and angle.** Never cross-dissolve two AI clips.
3. **Cut on motion.** Keep eyelines, screen direction and the 180° line.
4. **Rhythm is bimodal:** long honest holds for the hardest line, short bursts for change. Uniform shot lengths are a tell.
5. **Fix in post before you regenerate:** trim, reframe, retime, cut away, region-edit.
6. **Text and UI are never generated.** Composite them.
7. **One finish:** one grade and one grain pass over everything. Upscale only locked clips.
8. **Version every cut and lock picture** before you finish sound, colour and captions.

## Where realism is made

| Lever | In the edit it means | You are failing it when |
|---|---|---|
| 9 short takes, best seconds | Use the best window of each take; trim heads and tails | Shots run to the engine's default length; late morphs stay in |
| 10 edit to hide and to breathe | Cut on action, cut away before a flaw, hold where the performance is honest | Jump cuts between same-size generations; cuts on a held end pose; no room for a beat to land |
| 12 one finish | One grade, grain and halation once, one sound space | Each shot keeps its engine's look; grain baked into some shots and not others |

The judges of Higgsfield's March 2026 action-scene contest (8,752 entries) said they rewarded "storytelling and directorial intent over technical polish" (reported Sep 2026). Intent shows up most clearly in what you choose to leave out.

## Selects first

Before the first cut, build selects: one chosen take per shot, with an in point and an out point for its best seconds.

1. Compare takes side by side: `film contact --shot S05` (one row per take).
2. Rate them in the log (`select`, `maybe`, `reject`, with a diagnosis code on rejects; handbook 12).
3. Frame-step the select. Find the window where the performance is honest, the camera has settled and hands are still hands. In a 5-10 second generation that window is usually 1-3 seconds long.
4. Write the in and out points into `06_edit/cut.txt`.

Generate a little longer than the shot needs and front-load the action, so the best seconds sit early with handles on both sides.

**Where generated clips go wrong**

| Part of the clip | What goes wrong | What to do |
|---|---|---|
| First 0.1 s | Generation jitter: a frame or two of settling | `film assemble` trims 0.1 s off the head and tail of every whole take by default (studio-tested Apr 2026) |
| First 0.5-1 s (some engines) | The camera "finds" the shot; a character starting with a turn passes through mid-rotation mush; lip sync not yet locked | Trim it. Prompt the next one to start already in pose (studio-tested Jun 2026) |
| Middle | Usually the best seconds | Build the cut from here |
| Last 0.5-1 s and beyond | Morphing, identity drift, lip sync slipping (Veo lip sync drops toward the end of clips, studio-tested Apr 2026) | Cut before it. The tail is where degradation lives |
| A line split across two clips | Some engines render the whole line in both clips, so the viewer hears it twice (studio-tested Apr 2026) | Mute the second clip's scratch audio and trim its head harder (0.5 s) |

## The transition hard rule

The eye tracks the same subject across a join. When two separate generations of the same person at the same size and angle butt together, every small difference (a strand of hair, a collar, the key light) jumps, and the audience sees a skip. In the studio's productions this was the single most common amateur tell (studio-tested Jun 2026).

Every same-subject join must be one of these:

| Option | How | Best for |
|---|---|---|
| **Native multishot cut** | Generate the coverage in one pass with hard cuts. Kling 3.0 multishot renders up to three angles in one generation (studio-tested May 2026). It sometimes blends the cuts into one continuous shot, so generate 2 and keep the take that actually cut | One place, one moment, one main character |
| **Size AND angle change, cut on motion** | Change the shot size and move the angle at least 30° (MS front to CU profile). Cut mid-movement, never on a held end pose | Shots built from separate start frames |
| **Matched continuation** | Generate the next beat from a locked start frame and a locked end frame. Forward-only last-frame chaining drifts: keep chains 2-3 deep (studio-tested Jun 2026) | A continuous action that must stay at one angle |
| **Masked cut** | A whip pan or motion blur prompted into the generation, or a J-cut or L-cut so sound bridges the seam | Energy moments; dialogue |
| **Cutaway insert** | Hands, a prop, a screen or a reaction between the two shots of the same person | Anywhere; see "Inserts" below |

**Never** butt two same-size, same-angle separate generations together. **Never cross-dissolve two AI clips:** a dissolve shows both mismatched states at once and reads as a morph (studio-tested Jun 2026). To show time passing, cut to black, to a card, or put a time overlay ("DAY 14") on the live scene.

## Rhythm

The studio's teardown of two long-form AI drama ads found a **bimodal rhythm**. Average shot length was 2.6-2.8 s, but almost nothing was average: long honest holds of 8-13 s carried the protagonist's hardest line, and bursts of 0.9-1.5 s carried the transformation (studio-tested, reference teardown May 2026). The rhythm does the emotional pacing, so the picture does not have to perform anything subtle.

- **A long hold needs a take that survives that long.** Use your steadiest engine, a static or near-static camera, one face and little hand action.
- **Vary adjacent shots** in size, movement (static next to moving) and length. Two static MCUs in a row feel like a slideshow.
- **Uniform shot lengths are a tell.** Every cut landing at the engine's 5-second default says "generated".
- **Let the key line land.** Hold on the listener for a beat after it, then cut. Drop the music under that line (handbook 08).

**Pacing starting points** (studio defaults, not laws; cut by feel first, then check):

| Format | Typical shot | Longest hold | Bursts | Note |
|---|---|---|---|---|
| 6-15 s hook or bumper | 1-2 s | 3-4 s on the payoff | 0.5-1 s | The first shot must read in a second |
| 15-30 s spot | 1.5-2.5 s | 4-6 s | 0.9-1.5 s | One hold on the proposition |
| 30-60 s dialogue spot | 2.5-3 s | 6-10 s on the key line | 0.9-1.5 s | Bimodal |
| 45-90 s narrative short | 3-5 s | 8-13 s | At the turn | Holds carry the performance |
| 2-3 min ad drama | 2.6-2.8 s average | 8-13 s | 0.9-1.5 s | The teardown references |

## Continuity in the cut

**Cut on action.** Cut in the middle of a movement: a stand, a turn, a reach, a door. The outgoing shot ends a few frames into the move and the incoming shot picks it up. If the two clips move at different speeds, retime one so the move matches across the join.

**Eyeline is an entrance.** If a character looks frame-right, whatever they are looking at enters from frame-right. In the studio case below, a call beat was regenerated so the recruiter's glance pointed at the doorway his colleague walks in from.

**Screen direction.** Movement left to right continues left to right across cuts unless you show the change.

**The 180° rule in the edit.** When a generated shot lands on the wrong side of the line, you have three options: flip it (only if nothing asymmetric is in frame), put a neutral shot between (on the axis, or an insert), or replace it. Log the break and the fix in `03_board/continuity.md` (handbook 05).

## Inserts are editorial insurance

Pre-plan inserts in the shot list: hands, props, screens, textures. They are cheap to generate, have a high hit rate, carry tactile detail that sells realism, and every one is a place to cut away from a flaw or to separate two shots of the same face. Plan at least one per scene and mark it in the notes column: `pre-planned insert: editorial insurance`. Generate screens dark or blank, then composite the UI.

## Fix in post before you regenerate

"Fix in post" is the second rung of the remedy ladder, right after "keep and cut around" (handbook 12). Try these before you spend a credit:

| Fix | Solves | Watch for |
|---|---|---|
| **Trim** | Head jitter, late morphs, a bad blink, a hand that melts at the end | If the shot gets too short, cut to an insert |
| **Reframe / punch-in** | Same-size jump cuts, a ghost figure at the edge, a bad hand at frame bottom, default centred framing | Resolution: a 1.35x punch-in on a 1080x1920 frame uses 800x1422 pixels. Upscale the source first if it softens |
| **Flip** | Wrong screen direction, a 180° break | Only if nothing asymmetric shows: text, logos, watches, rings, hair parting, scars, button side, driving side |
| **Speed ramp / retime** | Slow-motion bias, weightless motion, mismatched speeds across a cut on action. Try 110-120% first | Any speed change on a lip-synced line breaks sync |
| **Reverse** | A new action from the same clip (setting down becomes lifting; push-in becomes pull-out) | Liquids, smoke, footsteps, falling hair and cloth give it away |
| **Freeze** | Extending a hold for a line or a beat | A dead freeze reads as a mistake: add a slow push and grain so it breathes |
| **Crop out artefacts** | Melting background detail, ghost extras, a morphing edge | Check that the new framing still has a job |
| **Cut away** | Anything you can't fix: go to an insert or reaction, come back | Needs a planned insert |
| **Region edit / inpaint a frame** | A wrong prop, a sixth finger for a few frames, a stray object | Paint frames in the NLE or compositor. Seedance 2.5 offers localised region editing on video (reported Sep 2026; mask support: verify before cohort). Edit the region; never regenerate a whole image twice |
| **Stabilise** | Floaty drift, micro-shake | Check faces and edges for warping afterwards |
| **Frame interpolation** | Slow motion, frame-rate conform | **Locked clips only.** It invents in-between frames and can morph hands and fast motion |
| **Upscale** | Resolution | **Locked clips only.** See below |

Log each fix as a take so the cost report counts it: `--stage fix` (handbook 13).

## Text and UI are never generated

Models scramble letters. In the studio's reference teardown, every generated phone screen carried gibberish in the body text (studio-tested May 2026). Product names, screens, signs, lower thirds and end cards are composited:

- **Editor titles** (Resolve, Premiere, CapCut) for simple supers.
- **HTML → PNG** through a headless browser for cards and screen UI: exact fonts, exact layout.
- **Remotion** for animated text, UI and end cards. Render stills with `--image-format=png --color-space=bt709`: the default JPEG bands soft gradients, and the default colour space shifts colours once the card joins BT.709 footage (studio-tested Sep 2026).
- Generate the screen or sign **blank** so there is a clean surface to track onto.
- Captions are text too: the `captions` skill builds them, and handbook 14 covers caption QC.

## One finish: colour, grain, halation

Work in this order, once, across the whole timeline:

| Step | What | Why |
|---|---|---|
| 1 Conform | Every clip to the production frame size and fps, crop to fill | Black bars inside a cut read as a mistake. `film assemble` does this |
| 2 Upscale | Locked clips only | The upscaler should never see your grain |
| 3 Balance | Per shot: black level, white balance, exposure | Each engine ships its own default grade |
| 4 Match | Each shot to the scene's hero shot, skin tones first | Grade shifts between cuts are a known multishot failure (reported Mar 2026) |
| 5 Look | One look over everything | Grade down from AI's default saturation and HDR-style contrast; let shadows fall |
| 6 Texture | Film grain and halation, once, subtle | Unifies engines and hides over-sharp "4K plastic" |

- **Fix colour casts at generation when you can.** A warm film-stock token (Portra 400) cast a whole shot orange with a vignette (studio-tested Jun 2026). Neutral stock tokens grade more easily.
- **Never bake grain into start frames.** Grain-stylised start frames produced softer, grainier, less clear video that needed a clarity pass (studio-tested Apr 2026). Texture belongs in post, where it is uniform.
- **Grain over noisy clips reads as noise.** Judge it full screen and on a phone.

## Upscaling

- **Only locked clips.** Approve at draft resolution, then upscale that take. Never re-roll the prompt at higher resolution and hope (handbook 13).
- **Studio case:** the locked 720p dialogue clips of a 9:16 ad were upscaled to 1080p with Topaz (through Higgsfield), with real reconstructed detail. The original locked audio was re-muxed; frame counts matched, so lip sync held (studio-tested Jun 2026).
- **Least-creative upscaler on faces.** Creative, detail-inventing upscalers can change a face; keep them for environments and textures.
- **Re-check every face** against the character's reference pack after every upscale. Drift here is an IDENTITY failure you paid for.
- Log it: `film take add S06 S06_1080.mp4 --stage upscale`.

## Versions and the three passes

| Pass | Goal | Where | Done when |
|---|---|---|---|
| **Rough cut** | Order, story, what's missing | `film assemble` from `cut.txt` | The story reads with temp sound; you know which shots to cut, fix or regenerate |
| **Fine cut** | Rhythm, trims, transitions, inserts, J/L cuts, punch-ins | Your NLE | No same-size jumps, weak frames hidden, rhythm varies |
| **Lock** | Picture frozen | | No more timing changes. Then upscale, grade, mix, captions, QC |

`film assemble` writes `06_edit/cuts/cut_v001.mp4`, then `cut_v002.mp4`, and never overwrites. Copy `cut.txt` beside each version (`cuts/cut_v004.txt`) and put one line at its top saying what changed (`#` lines are comments). Every change after lock ripples into the mix, the captions and every deliverable, which is why lock is a decision, not a mood.

## Editing tools

| Tool | Use it for | Notes |
|---|---|---|
| **`film assemble`** | Fast, frame-exact rough cuts from `cut.txt` | Conforms every event to the production frame (crop to fill; `--fit pad` letterboxes), quantises each event to whole frames so audio can't creep ahead of picture at the joins, and adds 30 ms audio fades so joins don't click. Accepts stills and `slate` lines (black placeholders). Claude can write `cut.txt` for you |
| **DaVinci Resolve** (free or Studio) | Fine cut, colour, sound | The free version covers the course. Some effects, and scripting from outside the app, need Studio (verify before cohort) |
| **Premiere Pro** | Fine cut in an Adobe workflow | Subscription |
| **CapCut** | Fast social cuts, mobile | Less control over colour and export |

**The round trip.** Use `film assemble` for the rough, an NLE for the fine cut. `film assemble` doesn't export a timeline: import the latest `cut_vNNN.mp4` onto the top track as a guide and rebuild underneath from the original takes, using the in and out points in `cut.txt`, so you keep handles for trimming. Tool choices and prices live in handbook 16.

## Studio case: ONE APPLICANT in twelve versions

A 39-second 9:16 dialogue ad: a recruiter notices a portfolio, calls a colleague over, and the reveal is that one applicant made it all. The edit decision log shows how a cut improves: mostly by free editorial decisions, with generation spent on coverage and bridges, never on resolution (studio-tested Jun 2026).

| Version | What was wrong | Decision | Cost |
|---|---|---|---|
| v4 | Two jump cuts between same-size separate generations | Punch-in 1.35x on shot 2 and a 1.25x push on shot 7, so each cut reads as a deliberate move tighter. Durations unchanged | Free |
| v5 | The colleague "magically appears" between shots 3 and 4 | A walk-in bridge: one new generation starting on shot 3's last frame and ending in shot 4's pose (about 2 s) | 1 generation |
| v6 | His glance didn't lead to her entrance; a second payoff shot read as a repeat | Call beat regenerated so his eyeline points where she will enter; the repeat cut | 1 generation |
| v7 | The stitched three-shot opening still showed seams | Replaced by one Kling 3.0 multishot generation: three native cuts, identity and grade locked | 1 generation |
| v8 | Two engines, two looks | The rest rebuilt in the same engine, chained frame to frame, with her entrance on the side he looks | Several generations |
| v9 | The opening line read out of sync; a later line chopped mid-word ("is that the ca-") | Audio delayed +150 ms, picked from a ladder of nudges; the out point extended so the line completes, then a clean cut | Free |
| v11 | Sound had no arc; the end card clashed with the outro | One instrumental bed, ducked under dialogue and lifted under the silent outro; end card background matched to the outro so they flow | Music only |
| v12 | Dialogue clips were 720p | Locked clips upscaled 720 → 1080; locked audio re-muxed | A few credits |

Native multishot audio was not locked to the lips on every beat. The fix order that worked: try a constant audio nudge of 100-250 ms first; if the drift isn't constant, re-drive the lips from the audio (studio-tested Jun 2026; handbook 07).

## Weak vs strong: an edit decision

**The situation.** Scene 2. S04 is an MCU of Maya from the front. S05 is a separate generation, also an MCU from the front, in which she says "Not tonight." Between the two generations her collar changed and the lamp behind her moved.

**Weak**

```
S04_t002
S05_t003
```

"Add a 12-frame cross-dissolve to smooth it."

Same size, same angle, separate generations: the jump is obvious. The dissolve shows two collars at once, which reads as a morph. Whole takes at default length also keep S05's late-clip drift.

**Strong**

```
S04_t002   0.6  2.9    # out as she starts to stand: cut on action
S04B_t001  0.2  1.4    # pre-planned insert: phone buzzing on the wood
S05_t003   1.1  3.6    # best seconds; 1.3x punch-in; line starts under the insert
```

The insert separates the two shots of her face and hides the collar change. The punch-in (done in the NLE) makes S05 a different size. Her line starts under the insert as a J-cut, so sound carries the viewer across. The trims keep only the best seconds. Cost: no generations, because the insert was planned.

## In the studio

| Skill | Use it for |
|---|---|
| `editor` | Builds `cut.txt` from your selects, applies the transition rule and rhythm, proposes fixes in post before regeneration |
| `take-doctor` | Codes a failed take and names the cheapest rung of the remedy ladder (often "cut around" or "fix in post") |
| `sound-design` | J/L cuts, room tone under the joins, the mix (handbook 08) |
| `captions`, `qc-review` | Captions and the final checks (handbook 14) |

```
film take list --shot S05                      # what have I got?
film contact --shot S05                        # takes side by side, one row each
film frames 04_shots/S05/takes/S05_t003_seedance-2.5_480p.mp4 --every 0.5
film take rate S05_t003 select --note "best 1.1-3.6s"
film assemble                                  # rough cut → 06_edit/cuts/cut_v001.mp4
film assemble --trim 0.5                       # an engine with a longer unstable head and tail
film assemble --fit pad                        # letterbox instead of crop (to inspect odd-sized clips)
film take add S06 S06_punchin.mp4 --stage fix --tool resolve --cost 0 --notes "1.3x punch-in, tail trimmed"
film take add S06 S06_1080.mp4 --stage upscale --tool topaz
film mix --video 06_edit/cuts/cut_v004.mp4 --dialogue 05_sound/dialogue/scene2.wav --music 05_sound/music/bed.wav
film qc 06_edit/cuts/cut_v004_mix_v001.mp4
```

Ask Claude in plain words: "Build a rough cut of scene 2 from my selects, best seconds only, and flag every same-subject join that breaks the transition rule."

## Drills

1. **Best seconds (10 min).** Take one 5-second generation. Frame-step it (`film frames ... --every 0.25`) and mark the best 1.5 seconds. Assemble it whole and trimmed, then watch both twice. Write one line on what the trim removed.
2. **Repair a jump cut (20 min).** Put two same-size generations of one character back to back. Fix the join three ways: a punch-in, an insert, and a J-cut. Show a neighbour all three without saying which is which, and ask which cut they noticed.
3. **Rhythm map (15 min).** Time every shot of a 30-second ad you admire. Write the lengths in a row and mark the holds and the bursts. Then re-cut your EX2 sequence so it has one hold and one burst.
4. **Post before pixels (15 min).** Take one rejected take. Try three fixes from the toolkit table before you allow yourself a re-roll. Log the best as `--stage fix`, or write down why none worked and which diagnosis code sends it back to generation.
