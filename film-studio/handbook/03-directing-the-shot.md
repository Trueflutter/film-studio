# 03 · Directing the shot

A director doesn't describe a picture; a director decides what the audience sees, from where, for how long, and why. AI models respond to that kind of decision far better than to adjectives, because film grammar is in their training data: shot sizes, lenses, moves and light setups have names, and the names carry meaning. This chapter is the grammar, and how to say it to a model.

## The short version

1. **One shot, one job.** Write the purpose before anything else.
2. **Decide the frame:** size, angle, lens, where things sit, what's in focus.
3. **One subject, one action, one move** per shot. Two beats are two shots.
4. **Every camera move has a cause.** No cause, no move.
5. **Every light has a source.** Name it, place it, colour it.
6. **Hold the line.** 180° rule, screen direction and eyelines are stated, not hoped for.
7. **Plan the cut** while you plan the shot: what comes before and after decides the size and angle.

## The shot card

Every shot starts here (`04_shots/_prompt_template.md`):

| Field | Question | Example |
|---|---|---|
| **Purpose** | what must the audience understand or feel? | she has already decided to leave |
| **Subject + action** | who, doing one visible thing | she turns her phone face-down and keeps her hand on it |
| **Frame** | size, angle, lens, composition | MCU, eye level, 50mm, her on the right third, dark doorway on the left |
| **Camera** | one move and its cause, or none | locked-off |
| **Light** | source, direction, quality, colour | phone glow from below, warm hallway spill from frame left |
| **Performance** | inner state → one visible behaviour | doesn't look at the phone; thumb presses the case |
| **Sound** | what we hear | rain on the window, the phone buzzing against wood |
| **Continuity** | anchor line, wardrobe, screen side, light side | Maya, grey cardigan; screen right; key from left |

## Shot size: how close says how much it matters

| Size | Frame | Says | Use for |
|---|---|---|---|
| Extreme wide (EWS) | a tiny figure in a huge place | the world is bigger than them | openings, isolation, scale |
| Wide (WS) | whole body plus the space | here is where and who | establishing, blocking, action |
| Medium wide / cowboy | knees or thighs up | a person in a situation | walking, confrontations |
| Medium (MS) | waist up | conversation distance | dialogue, gestures |
| Medium close-up (MCU) | chest up | attention on the person | most dialogue, reactions |
| Close-up (CU) | face | this matters | decisions, realisations |
| Extreme close-up (ECU) | eyes, mouth, a detail | this is everything | peaks, used rarely |
| Insert | an object or hand | a detail carries the story | props, screens (composited), tells |
| Over-the-shoulder (OTS) | past one person to another | a relationship | dialogue coverage |
| Two-shot | two people in frame | the space between them | tension, intimacy |
| POV | what a character sees | we are them | discovery, suspense |

AI note: faces are most stable at MCU and CU. In wides the model invents small faces, so carry identity with silhouette and wardrobe. Tight ECUs of hands and mouths are where artefacts show.

## Angle and height

| Angle | Effect |
|---|---|
| Eye level | neutral, equal, documentary |
| High angle (looking down) | smaller, vulnerable, observed |
| Low angle (looking up) | larger, powerful, threatening |
| Overhead / top-down | pattern, fate, clinical distance |
| Dutch (tilted 5-12°) | unease; use once, not as style |
| Camera height below eyes, level | quietly heroic |

## Lenses: the emotional grammar of focal length

| Focal length (full-frame equivalent) | What it does | Feels like |
|---|---|---|
| 14-24mm | exaggerates depth and distance; distorts faces up close | worlds, energy, disorientation |
| 28-35mm | natural wide; people in their place | being in the room, documentary |
| 40-50mm | close to the eye's perspective | honest, observational |
| 65-85mm | flattering faces, soft backgrounds | intimacy, attention |
| 100mm+ | compresses space, isolates | surveillance, longing, heat haze |
| Macro | the world of a detail | inserts, texture |

Depth of field follows the lens, the distance and the light: long lens + close + low light = shallow; wide lens + far + bright = deep. Say both lens and aperture feel ("85mm, shallow depth of field, background soft") and keep them consistent within a scene. Name three lenses in your style bible and use only those: consistency reads as intention.

## Composition

- **Place things on purpose.** Thirds for balance; centre for power, symmetry or confrontation. The model's default is a centred hero; fight it by saying where the subject sits.
- **Look room.** Leave space in the direction someone looks or moves. Cutting it off creates tension; do it on purpose.
- **Headroom.** Tight headroom in close-ups feels intimate; lots feels small and alone.
- **Depth.** Foreground, subject, background: something between the lens and the subject (a door frame, a shoulder, a glass) makes a frame feel photographed, not rendered.
- **Negative space** can carry the emotion: the empty chair, the dark doorway.
- **Frames within frames:** doorways, windows, mirrors isolate a character inside their world.

## Movement: every move needs a cause

| Move | Motivated by | Says |
|---|---|---|
| **Static (locked-off)** | nothing needs to move | observation, stillness, control (the default) |
| **Pan / tilt** | following something that moves; revealing | attention shifting |
| **Push in (dolly in)** | a realisation, rising tension | getting closer to the truth |
| **Pull out (dolly out)** | revealing context, isolation | the bigger picture, loneliness |
| **Tracking / follow** | a moving character | we go with them |
| **Crane / rise** | leaving a scene, scale | an ending, a verdict |
| **Handheld** | urgency, subjectivity | we're in it, off balance |
| **Orbit** | a moment that holds the world still | significance (use once) |
| **Crash zoom** | shock, comedy | a punchline |

For AI, write the cause into the prompt: _"as she stands, the camera rises with her"_ rather than _"crane up"_. A motivated continuous shot (a oner) is a chain of causes: each new subject entering frame hands the camera on (the `prompt-director` skill has the template).

## Blocking: where people are and how they move

Blocking is the geography of a scene: positions, entrances, exits, distances, who faces whom, who moves and who doesn't.
- **Power geometry:** standing over sitting, centre over edge, facing the door vs back to it.
- **Distance is emotion:** close in intimacy or threat, far in estrangement.
- **Movement reveals decision:** a character who crosses the room has decided something.
- **Eyeline equals entrance:** if someone looks or gestures left, the next subject enters from the left (studio-tested).
- **Write it down** in `03_board/continuity.md`: who is on which side, who looks where.

## Light: what it is and where it comes from

- **Key** (the main light and its direction), **fill** (how much the shadows are lifted), **back/rim** (separation from the background), **practicals** (lamps, screens and windows visible in frame).
- **Hard vs soft:** a small source (bare bulb, direct sun) makes hard shadows; a big source (overcast sky, a window with a curtain) makes soft ones.
- **Contrast** sets mood: deep shadows for secrecy, low contrast for openness.
- **Colour temperature:** warm (tungsten, candle, sunset) vs cool (overcast, screens, moonlight); mixing them in one frame is how night interiors feel real.
- **Motivation:** every light has a source the audience would accept. Name it in the prompt and keep it on the same side across the scene.

## Coverage and the cut

- **Coverage** is the set of shots that lets a scene be edited: a master (or wide), singles, over-the-shoulders, reactions, inserts.
- **180° rule:** keep the camera on one side of the line between two characters; each stays on their side of the frame. Cross it only on purpose, and show the crossing.
- **30° rule:** when cutting between two shots of the same subject, change the angle by at least 30° and the size noticeably, or it jumps.
- **The transition rule for AI:** never hard-cut two *separately generated* clips of the same subject at the same size and angle; the tiny differences read as a glitch. Generate the coverage natively in one multishot pass, or change size and angle, cut on action, or cut away (studio-tested; the number-one amateur tell in our reviews).
- **Screen direction:** a character leaving frame right enters the next shot from frame left if they keep going the same way.
- **Cut on action:** start a movement in one shot, finish it in the next; the motion hides the cut.
- **Inserts are editorial insurance:** plan them before you need them.

## Saying it to the model

Order that works across engines: **frame and camera → subject and action → light → performance → sound → constraints.**

> _"Medium close-up, 50mm, eye level, locked-off. [Subject and one action]. [Light source, direction, quality, colour]. [Behaviour: task, eyes, tell]. [Sound]. Only [name] in frame; no text."_

Rules:
- Real names for lenses, sizes and moves. Skip "cinematic", "8k", "masterpiece".
- One action, one move, one light logic.
- State continuity every time (anchor line, screen side, light side). The model remembers nothing between generations.
- Put the purpose in the prompt file as a comment for yourself; the model doesn't need it, but you do when you review.

## Weak vs strong

**Weak:** _"Dramatic cinematic shot of a boss firing an employee in an office, intense, 4k."_

**Strong (two shots, because it's two beats):**
- _S07 · Wide, 28mm, eye level, locked-off. A glass meeting room, late afternoon. The manager (right, standing) and Sami (left, seated) with a desk between them; city through the window behind the manager, sun low and hard from behind him, Sami's face in the soft bounce. The manager slides a single sheet of paper across the desk. Air-conditioning hum, distant traffic._
- _S08 · Close-up, 85mm, slightly high, locked-off. Sami, screen left, looking toward frame right at the paper below frame. He reads; his jaw sets; he nods once, too quickly. Same hard window light behind the manager now reaching the edge of his cheek._

What changed: the story beat is two decisions (the act, the reaction); sizes and lenses differ by design; the camera doesn't move because nothing motivates it; the light has a source that stays on the same side; screen sides are stated; performance is behaviour.

## In the studio

- `shot-designer` skill: script → shot list with sizes, lenses, moves, coverage and rhythm checks.
- `prompt-director` skill: shot card → engine-specific prompt with references and their jobs.
- `03_board/shotlist.csv`, `03_board/continuity.md`, `04_shots/<SHOT>/prompt_vN.md`; `film boards` to see the shot list as a storyboard.

## Drills

1. **Three sizes (15 min).** One moment as a WS, an MCU and a CU. Write what each makes the audience feel.
2. **Motivate it (10 min).** Rewrite five camera moves from your shot list so each names its cause, or delete the move.
3. **Coverage (20 min).** A 4-line argument between two people. Plan a master, two singles, one reaction and one insert; mark the 180° line and screen sides.
4. **Light from a source (15 min).** Take one shot and relight it three times with three motivated sources. Keep everything else identical.
