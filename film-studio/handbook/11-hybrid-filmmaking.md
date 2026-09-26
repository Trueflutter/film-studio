# 11 · Hybrid Filmmaking

The most believable performance in any AI film is a real one, and the most believable light is light that actually fell on something. Hybrid filmmaking shoots what cameras are good at (people, timing, weight, real light) and generates only what they can't (the creature, the era, the world). Since mid-2026 the tools that transform real footage while keeping its motion and timing are good enough to use in a class, which makes this the top-end method, not an exotic one.

## The short version

1. **Shoot the performance, generate the impossible.** Real people for behaviour and timing; generation for what you can't film.
2. **Shoot for the model:** steady camera, 24 or 25 fps, even light, clean background, sharp faces, a clean plate.
3. **Set the look on frame 1 first.** Iterate on a still for cents, then carry that look through the clip.
4. **Say what must stay before what changes:** face, performance, timing, eyeline, camera.
5. **Change as little as the idea needs.** The heavier the change, the more of the performance you lose.
6. **Fix locally before you regenerate:** region edits, or mask the original face back in.
7. **Integration is the craft.** Light, grain, edges, contact shadows, lens, motion blur and sound perspective have to match.
8. **Only transform people who agreed to it, in writing** (handbook 15).

## Why hybrid is the top-end method

Three things are still hard to generate and cheap to film:

- **Performance.** Breath, hesitation, a hand that finds a pocket: behaviour a model approximates and a person simply does (lever 6, behaviour over emotion).
- **Light and physics.** A plate carries real light direction, real falloff and real contact: feet on floors, cloth on skin, a cup set down (levers 1 and 5).
- **Timing.** A real take has the rhythm of a real moment. Keep it and the edit breathes (lever 10).

Generation then does what no budget could film. Two reference points:
- **Simon Meyer's alien interviews** (with Daniel Lwowski, April 2025): real people interviewed on camera, with AI aliens placed into the scenes (reported Sep 2026). Real faces and voices carry the authenticity; AI supplies the impossible element.
- **ANCESTRA** (Eliza McNitt, Tribeca 2025): live-action performances combined with generated sequences for imagery that couldn't be filmed, such as the cosmos and the womb (verify before cohort).

The pattern in both: **AI for the impossible, humans for the performance.**

## The capability map

Seven things you can do with real footage. Examples are current as of September 2026; specs and prices live in handbook 16.

| Capability | What stays | What changes | Current examples |
|---|---|---|---|
| **(a) Restyle / transform** | Motion, timing, camera | Look, materials, style | Runway Aleph 2 with Edit Studio (edit one frame, then propagate across the clip); Luma Ray 3.2 Modify / video edit (adhere, flex or reimagine strengths); Kling 3.0 Omni edit; Seedance 2.5 edit; Gemini Omni edit (all verified Sep 2026) |
| **(b) Keep the actor, change the world** | Face, performance, eyeline | Wardrobe, set, time of day, weather, era | The same engines, run at low-to-medium change strength. Luma pitches Modify as "variable appearance, invariant performance" (reported) |
| **(c) Performance capture onto a character** | Head, face, body and hand motion, lip movement | Who performs it | Runway Act-Two: driving video plus a character image (verified Sep 2026); Wan-Animate-2, open weights, Apache-2.0, up to 720p (verified Sep 2026) |
| **(d) AI plates behind real actors** | The actor, keyed or matted | Everything behind them | Green screen, or an AI matte (SAM, Resolve Magic Mask: verify before cohort); a generated plate; relight the actor to the plate; composite. Keep the camera locked off in a course. Seedance 2.5 accepts green-screen plates as references (reported) |
| **(e) Relighting** | Everything but the light | Direction, colour, time of day | Aleph 2 and Ray 3.2 relight (verified Sep 2026); Beeble-style relighting from derived normal and depth passes (verify before cohort) |
| **(f) Render-to-real from a blockout** | Camera, layout, timing of a 3D grey-box | Everything visible | See handbook 10 |
| **(g) Extend or reframe real shots** | The shot you have | Length, aspect, angle | Ray 3.2 reframe (outpaint to a new aspect) and extend; Seedance 2.5 and Gemini Omni extend (verified Sep 2026); Aleph 2 new camera angles (reported) |

Choose by how much of the plate must survive. Minimal change (a relight, a new jacket, a new sky): Aleph 2 or Ray's "adhere" strength. Heavy change (a new world, a new era): "reimagine" strengths or Omni, and expect to fight for identity. Interpolate frame rates only after the edit is locked; interpolation magnifies generated artefacts.

## How to shoot for the model

Every flaw in the plate becomes something the model has to guess around. Care on set is cheaper than any fix in post.

| Do | Because |
|---|---|
| **Steady camera:** tripod, a phone on a stack of books, or slow smooth moves | Engines track steady motion well; shake turns into swimming backgrounds |
| **24 or 25 fps, constant.** Phones can record variable frame rate: set a fixed rate or conform before upload | Some engines cap input at 30 fps (Aleph 2, verified Sep 2026); variable rates can drift lip sync |
| **Even light, exposure and focus locked** (tap and hold on most phones) | Pumping exposure reads as flicker after a restyle |
| **15-20 s takes, trimmed later** | Engine windows run from about 3-10 s (Kling Omni edit) to 18 s (Ray 3.2 edit) to 30 s (Aleph 2) (verified Sep 2026) |
| **Clean background, wardrobe that contrasts with it** | A clear silhouette survives the transform; busy backgrounds invent objects |
| **No motion blur on faces:** bright light on the face, no fast head turns or whip pans | A smeared face gives the model nothing to hold; identity drifts |
| **A clean plate:** 5 s of the empty set, same framing | For composites, clean-up and masking the original back in |
| **Match the lens you'll imply.** Want a tight close-up? Use the phone's longer lens from further back, not the wide lens up close or a crop | The model keeps the plate's perspective. A wide lens close to a face distorts it and no restyle fixes that (lever 2, honest lens) |
| **Note the light:** direction, colour, one photo of the set | You'll match the generated world to it |
| **Record clean sound and 30 s of room tone** | The real voice carries much of the real performance (handbook 08) |

## The recipe: keep the actor, change the world

1. **Trim.** Conform to a constant 24 or 25 fps, trim to the engine's window, export a high-quality 1080p file. Keep the untouched source in `04_shots/<SHOT>/source/`.
2. **Set the look on frame 1.** `film frames source.mp4 --at 0` gives you frame 1. Edit it in an image model (or Aleph 2's single-frame edit) until the look is right: wardrobe, set, era, light. Stills cost cents, so iterate here, not in motion. Check the face still reads as the same person.
3. **Generate with the look reference.** Give the source clip and the approved frame their jobs, and list what must stay (face, performance, timing, eyeline, camera move, hand positions) before what changes. Test a short trim first, at low resolution where the engine allows; then run the whole clip once, and upscale the take you lock rather than re-running it at a higher setting (handbook 13). Log every attempt with `film take add`.
4. **Check in motion, not on stills:**
   - Identity: jaw, eyes, hairline, especially on turns (IDENTITY).
   - Hands: finger counts, grip, contact with props (PHYSICS).
   - Lip sync against the original audio (SYNC).
   - Flicker, swimming backgrounds, texture crawl (ARTEFACT).
5. **Fix locally.** Climb the remedy ladder (handbook 12): cut around the bad second; region-edit the one broken element (Aleph 2, Seedance 2.5 localised edit); or mask the original face back in (roto the real face, composite it over the restyle, grade to match). Re-roll the whole clip only when the problem is everywhere.
6. **Upscale, grade, mix.** Upscale the locked take only. Grade the hybrid shot with its neighbours as one film (lever 12). Keep the production dialogue, and replace the room tone with the sound of the new world (lever 11).

### Weak vs strong: a restyle prompt

Same source clip: a woman at a desk in a modern office, slow push-in, she looks up to frame right and speaks one line.

**Weak**
```
Make this video cinematic, 1970s style, vintage vibe, change the background to an
old newsroom, epic moody lighting, 8K, masterpiece, make her look amazing.
```

**Strong**
```
@video1 is the source performance. @image1 is the approved look for frame 1.

KEEP EXACTLY: her face and identity; every head, hand and shoulder movement; the timing
of each gesture; her lip movement; her eyeline to frame right; the slow push-in and
the framing.

CHANGE: the office becomes a 1970s newspaper office at night. Her grey hoodie becomes
a brown corduroy jacket over a cream roll-neck. The laptop becomes a typewriter in the
same position under her hands.

LIGHT: keep the key from frame left, where the real window was. It is now a warm desk
lamp, about 3200K. Cool street light spills from the window behind her.

TEXTURE: 35mm film grain, gentle highlight halation.

Do not add people. Do not change her hair, face shape or skin. Do not change the camera move.
```

| The strong version... | Because |
|---|---|
| Gives each input a job | An unassigned reference is noise (handbook 06) |
| Lists what stays before what changes | Models preserve what you name; "make her look amazing" invites a new face (IDENTITY) |
| Puts new objects where the old ones were | Her hands already touch the laptop; a typewriter in that spot keeps the contact real (lever 5) |
| Keeps the light direction of the plate | Light that contradicts the plate is the fastest tell (lever 1) |
| Names grain, not "cinematic" | One concrete texture beats a stack of adjectives |
| Ends with forbidden changes | The usual failures (new people, new face, new camera) are closed off |

Engines take inputs differently (keyframes, prompt images, @-references, strength sliders). Keep the structure and adapt the syntax; `prompt-director` knows the current format for each.

## Integration checklist

A hybrid shot fails on its seams. Check every one, in motion, at full screen.

| Check | Look for | Fix |
|---|---|---|
| **Light direction and colour** | Key from the same side as the plate; skin and set in the same colour temperature | Relight pass, or grade the new element toward the plate |
| **Grain** | Real footage has sensor noise, generated footage often has none, or a different grain | Degrain both, then add one matched grain over the whole shot |
| **Edges** | Halos, fringing, hair that cuts off hard | Soften the matte, add light wrap, re-roto the hair |
| **Contact shadows** | Feet, elbows and props touching the new world cast shadows into it | Paint or generate the contact shadow; never leave a subject floating |
| **Perspective and lens** | Horizon height, vanishing point and depth of field match the plate's lens | Regenerate the plate at the right angle; match the blur |
| **Motion blur** | New elements blur like the real ones at the same shutter | Add matched motion blur, or generate at the same speed |
| **Black levels and highlights** | Same black point and roll-off across the seam | One grade across the whole shot |
| **Sound perspective** | The voice sounds like it's in the new space: a cathedral is not a car interior | Reverb and room tone that fit the picture; change ambience with the world (handbook 08) |

## In class: EX5 Real Meets Generated

A worked example of the whole chapter in about an hour.

1. **Consent first.** Partners sign the class release, both ways, covering AI transformation of their likeness for the course and the screening (handbook 15).
2. **Ten minutes of shooting.** In pairs on phones. Each student directs two 15-20 s locked-off takes of their partner doing a single action from a brief card (reading a letter, waiting for a call, putting on a coat). Then 5 s of clean plate and 30 s of room tone. The consent form (handbook 15, section 10) is signed before the camera rolls. Snap one photo of the light setup.
3. **Trim and frame 1.** Conform, trim to the engine window, `film frames` for frame 1, three to five look edits, pick one.
4. **Test the transform.** A keep/change prompt, two attempts on a short trim at low resolution, rated in `takes.csv` with fail codes.
5. **Fix and integrate.** One local fix, then the integration checklist and a sound pass that places the voice in the new world.
6. **Screen it side by side:** source and hybrid, with the one thing the room should notice (and the one thing it shouldn't).

A render-to-real station runs alongside for students whose idea needs a new camera move rather than a new look (handbook 10).

## Consent and likeness

Transforming a real person is a use of their likeness, even when the result looks nothing like them.

- **Written consent** for the specific use: what will be changed, where it will be shown, for how long, and how they can withdraw. Classmates too.
- **No transformations of people who haven't agreed:** passers-by, public figures, found footage, anyone whose image you don't have the rights to. Keep bystanders out of the frame or remove them.
- **Platform face filters exist because likeness needs consent.** When a tool blocks a real face, get consent and use a permitted route, or cast a synthetic character. Never work around the filter.
- **Disclose** altered footage where platforms or clients require it, and keep the provenance log in `07_delivery/`.

Full practice, templates and disclosure rules: handbook 15.

## When NOT to go hybrid

| Situation | Why hybrid hurts | Do this instead |
|---|---|---|
| The performance isn't good | A transform inherits every flaw of the take | Reshoot, or generate the shot |
| The change is total (a person becomes a creature with a different body) | Restyle loses the performance anyway | Performance capture (Act-Two, Wan-Animate-2) or full generation |
| The camera travels through space and you need composites | Camera tracking is beyond a four-day course | Lock the camera off, or render-to-real from a blockout |
| You can't control the shoot: bad light, crowds, no consent from people in frame | Every flaw becomes a guess | Generate |
| On-screen text, logos, UI | Models scramble letters | Composite real graphics in post |
| A stylised or animated piece | Real plates add little | Full generation is cheaper |
| No time for finishing | Hybrid shots cost more integration time than pure generation | Save hybrid for the hero shot |

## In the studio

- **`/film-studio:hybrid-footage`**: the shoot checklist, frame-1 look development, keep/change prompts per engine, local fixes and the integration checklist. Try: "I shot S05 on my phone. Plan a keep-the-actor, change-the-world pass: 1970s newsroom at night."
- **`/film-studio:prompt-director`**: turns your keep/change notes into the current syntax for the engine you picked.
- **`/film-studio:take-doctor`**: names the failure (IDENTITY, SYNC, ARTEFACT, PHYSICS) and picks the cheapest fix, usually local.
- **`/film-studio:sound-design`**: sound perspective and room tone for the new world (handbook 08).
- **`/film-studio:qc-review`**: the integration checklist at delivery (handbook 14).

```
film frames 04_shots/S05/source/take3.mp4 --at 0            # frame 1 for look development
film take add S05 04_shots/S05/look_v3.png --stage still --tool gpt-image --mode edit
film take add S05 restyle_a.mp4 --stage draft --tool runway --model aleph-2 --mode v2v \
  --cost <what you paid> --prompt 04_shots/S05/prompt_v2.md
film take rate S05_t003 reject --fail IDENTITY --note "jaw reshapes on the turn at 2.1 s"
film gen S05 --via fal --model <v2v endpoint id> --prompt-file 04_shots/S05/prompt_v2.md \
  --image 04_shots/S05/look_v3.png --param video_url=<source clip url> --dry-run
film contact --shot S05                                     # every attempt side by side
film dailies
```

Field names differ between fal endpoints: check the model page and `--dry-run` before you spend.

## Drills

1. **Shoot it twice (15 min).** Film yourself doing the same 10 s action twice: once badly (handheld, backlit, a fast head turn) and once for the model (phone propped on books, lit from the front and side, a slow turn). Run both through the same restyle at low resolution and list what broke in the bad one.
2. **Keep/change lists (10 min).** For three shots from your capstone, write the KEEP and CHANGE blocks only. Then watch each source clip with the sound off and add anything that must stay but isn't named yet.
3. **Integration spotting (15 min).** Take any hybrid shot (yours or one from the class reel) and score each row of the integration checklist 0, 1 or 2. Fix the lowest-scoring row.
4. **Frame-1 look development (15 min).** Pull frame 1 from a real clip and make five looks with an image model. Pick one and write two lines: why it serves the story, and what in it will be hardest to hold in motion.
