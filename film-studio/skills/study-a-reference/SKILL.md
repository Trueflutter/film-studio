---
name: study-a-reference
description: Use when the director gives an inspiration video and wants to know how it was made or to make theirs like it - "reverse engineer this video", "how did they do this effect", "study this ad", "make mine look like this", "what makes this work", "copy this style". Measures the video frame by frame (cuts, holds, how text and objects move, transitions, colour, sound hits), names every technique, maps each one to how this studio builds it (HyperFrames, Seedance, the edit or the mix), and proves it with a short piece made from the director's own brand and content. Takes the technique, never the content.
---

# Study a reference: how they did it, made yours

People learn fastest from a video they love. The job is not a copy. It is a recipe the director can use on their own brand, proven with a short piece of their own. A frame-for-frame copy of someone else's video can't be published, and it teaches less.

## The rules

- **Take the technique, never the content.** None of their footage, people, logos, characters, music, script or exact layout goes into what we make. Keep the reference file private, in `00_brief/reference/`.
- **Measure before you describe.** A sheet of one frame a second hides what makes a video feel expensive: most transitions, text entrances and flashes last 2 to 12 frames.
- **Everything here is free and local.** No HeyGen account and no HyperFrames Pro. Their `reverse-any-video` makes a paid frame-for-frame copy, which is not this job.

## 1. Get the file

- The director supplies the video: a file they're allowed to have, or a screen recording. It goes in `00_brief/reference/`.
- Once: `npx hyperframes telemetry disable`.
- `npx hyperframes@latest measure probe <ref>`: size, frame rate, duration, sound. The `measure` tools need HyperFrames 0.9 or later, which `@latest` makes sure of. Without HyperFrames, `film teardown <ref>` and `film frames` do steps 2 and 3 more coarsely.

## 2. Map the whole video

1. `npx hyperframes@latest measure cuts <ref>`: every cut, including jump cuts and punch-ins inside one take. Write the average, shortest and longest shot.
2. `npx hyperframes@latest measure events <ref> --map`: cuts, flashes, things appearing and disappearing, holds, and the sound's hits. This is the list of moments to study.
3. `npx hyperframes@latest measure look <ref>`: brightness, contrast, saturation and warmth; per section with `--start` and `--end` when the look changes.
4. `film teardown <ref>`: one frame per shot on sheets, for shot sizes and composition at a glance.

Write the map in `00_brief/reference/STUDY.md`: one row per section with its time, what happens, the shot lengths and what is on screen.

## 3. Study every technique

At each moment from step 2, read consecutive frames, not sample sheets: `npx hyperframes@latest measure frames <ref> --events` gives one strip per moment, and `--range a,b` one stretch. Look at them yourself. Then name each technique, measure it and say how we build it:

| What you see | Measure it | How we build it |
|---|---|---|
| Text or a shape moving: kinetic type, a sliding card, a counter | `measure curve <ref> --start a --end b --roi x,y,w,h` gives the duration, the overshoot and the closest GSAP ease | HyperFrames with that ease and duration; search `/hyperframes-registry` first for charts, transitions and effects |
| A transition: whip, zoom, mask wipe, flash, match cut | its strip with `measure frames --range a,b` | a registry transition or HyperFrames; a match cut is planned in the shots |
| Text style: weight, size, colour, captions | a frame at full size; `measure look <ref> --at t --grid 8x6` for the colours | `graphics` and `captions`, in the director's own fonts and colours |
| A filmed or generated shot: camera move, lens, light | the shot's strip; `measure look` for the light | `seedance-directing` with `camera-moves`: a cause for every move, motivated light |
| The grade | `measure look` per section | the grade in the edit, checked with `measure look <ref> --compare <ours>` |
| Pacing and rhythm | `measure cuts`; `measure events --map` for the beats | `editor`: a cut list on the same rhythm |
| Sound: whooshes, pops, hits, music drops | `measure events --map` | `sound-design`: a cue sheet at the same moments |
| A presenter or a person | `measure face` for size and position over time | the director's own footage or `presenter-video`; never their person |

Write each technique as a card in STUDY.md (template: `reference/recipe-card.md`): what it is, where it happens, its numbers, how we build it and what it costs.

## 4. Prove it with the director's own content

1. Pick the two or three techniques that make the reference work: usually the pacing, one signature move, and the type or the grade.
2. Build a 5 to 10 s proof with the director's own brand, product and words: HyperFrames for graphics, their footage or one cheap draft for shots. Show the cost before anything is generated.
3. Compare the technique, not the picture: `measure curve <ref> ... --compare <ours> --compare-start t` for the signature move, `measure look <ref> --compare <ours>` for the grade, `measure energy <ref> <ours>` for how much it moves.
4. Show the reference and the proof side by side and ask what to push further.

## 5. Hand over

STUDY.md ends with the recipe in plain words, reusable on every video in that style, for example: "Cuts every 0.8 s in the hook, then 2 s. Each line of text arrives on a 0.35 s back-out ease and leaves before the next. A white flash frame on every beat. Warm and contrasty, matched with `measure look`."
