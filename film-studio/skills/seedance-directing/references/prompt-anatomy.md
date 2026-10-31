# Prompt anatomy

One block order for every shot or sequence. The three Nexus production prompts all follow it; the field notes below are ours. Keep the labels in capitals: they help the model and they make versions easy to diff.

```
SCENE CONTEXT: [genre and tone in one line]. [Who, where, what happens, and the emotional core]. [N shots], [photoreal / stylised], [the camera language in three words], joined by HARD CUTS.
OUTPUT: [aspect], [total seconds], [N shots] of [s1, s2, s3 ... seconds, uneven, payoff longest], hard cuts only, 24fps, real-time motion. NO MUSIC: no score, no soundtrack, no background music, no musical tones or beats of any kind. No subtitles, no on-screen text.
ACTIVE REFERENCES:
@Image1: [what it is]. Use it only for [environment / appearance / composition of shot N / start frame]. Never use it for [what it must not set]. [Placeholder note if it has white or gray shapes.]
@Image2: ...
@Video1: [voice / performance / camera move]. Use only its [sound / motion]. Never any picture from it.
SPATIAL MAP: [only when sides matter: LEFT half / RIGHT half, who and what lives where, mirror logic for hands, "never swaps"].
THE CAMERA: [the global camera: rig, operator, energy, what disturbs it, readable framing]. [Shot size limits]. [Face angle rule: THREE-QUARTER, never front-on].
THE PERFORMANCE: [each character's state and intensity from first frame to last; physical signs; where it lives; what never happens].
THE LINE: [exact dialogue, spelled normally, in order], [delivery: pitch, pace, volume, accent; which voice reference].

SHOT 1 (0:00 to 0:0X)
OPTICS: [focal-length look], [depth of field], [what is soft behind].
CAMERA: [size], [angle and side], [height], [the move, its rig and its cause].
ACTION: [the one physical action, with screen direction; first-frame state].
TIMING: [0-0.6s: beat] [0.6-1.2s: beat] ... [each beat ends; where the shot ends: held look or mid-motion on the cut].
AUDIO: [diegetic sounds for this shot only, in order].
LOCK: [1-2 non-negotiables for this shot].

SHOT 2 (0:0X to 0:0Y)
[same six lines; say if it continues the previous shot's motion or emotion with no pause]

GLOBAL LOCK: [cut count and cut times], [same characters and wardrobe in every shot], [screen sides], [which references never set composition], [placeholders never rendered], [words allowed and in what order], [no music, no text, no logos].
LIGHTING: [quality, colour, direction and source], [what it does to skin, eyes and surfaces].
```

## Field notes

- **SCENE CONTEXT** is the brief to the whole crew. Put the emotional core here in plain words; the performance blocks then make it physical.
- **OUTPUT** carries the numbers the model must hit. Spell out the music lock in full; a bare "no music" lets a score in.
- **ACTIVE REFERENCES:** the strongest language in the prompt. A face reference says it is a face reference only and lists everything it must not set. A grid says it is never rendered with its borders. A staging frame with white face ovals says the ovals are placeholders and identity comes from the face reference.
- **SPATIAL MAP:** write it when props, hands or two characters must hold their sides. Describe it from the camera's point of view, then from the character's, and say they never swap.
- **THE CAMERA:** a person holding a camera, not a direction of travel. Name the rig (shoulder, tripod, dolly, car mount, drone), the operator's movement and what bumps them, and the promise that the face stays readable.
- **THE PERFORMANCE:** state, intensity, signs, region. If a state must stay small, describe the small version physically rather than forbidding the big one.
- **THE LINE:** the exact words. Names and acronyms spelled the way they sound ("A.I."). A long word described as held longer, never stretched.
- **Per-shot blocks:** six lines, every shot, even when the shot is simple. TIMING carries the acting; AUDIO carries the space; LOCK carries the one thing this shot gets wrong most often.
- **GLOBAL LOCK** restates the cut times and everything that must stay the same. Repetition here is deliberate.
- **LIGHTING** last, as a single physical description that holds across all shots.

## Sizes

| Generation | Shots | Typical length |
|---|---|---|
| single shot, 4-5 s | 1 | 250-500 words |
| sequence, 6-10 s | 3-5 | 800-1,500 words |
| coverage pass, 20-30 s | 6-12 | as long as the route accepts; per-shot blocks can drop to CAMERA, ACTION, TIMING because only angles and order are judged |

## Before and after (same shot)

**Short (what our older rules produced):**

```
Medium close-up, 50mm, eye level, locked-off. A woman in her thirties at a kitchen table at night turns her phone face-down and keeps her hand on it; she doesn't look at it. Cold phone glow from below, warm hallway light from frame left. Rain on the window. No music.
```

**Directed (the anatomy, one shot):**

```
SCENE CONTEXT: A quiet domestic drama at night. Nadia, mid-thirties, has just decided not to answer a call from someone she loves; the choice costs her. One shot, photoreal, observational.
OUTPUT: 9:16, 5 seconds, one continuous shot, 24fps, real-time motion. NO MUSIC: no score, no soundtrack, no background music, no musical tones or beats of any kind. No subtitles, no on-screen text.
ACTIVE REFERENCES:
@Image1: the start frame. Use it for composition, lens and light. Nadia's face in it is painted out as a plain white oval: a placeholder mask, never rendered; her face comes only from @Image2.
@Image2: Nadia's face. FACE REFERENCE ONLY: skin, eyes, brows, hair. Never use it for composition, framing, camera angle, pose, head turn or expression.
THE CAMERA: on a tripod across the table, a person behind it; one slow, slightly uneven tilt down of a few degrees as her hand moves, then still. Her face THREE-QUARTER from her LEFT, never front-on.
THE PERFORMANCE: controlled grief she will not show. It lives in the jaw, the breath and the thumb, never in tears. Low intensity, held.
SHOT 1 (0:00 to 0:05)
OPTICS: 50mm look, shallow depth of field, the dark hallway soft behind her.
CAMERA: MEDIUM CLOSE-UP, THREE-QUARTER from her LEFT, at seated eye height, the slow tilt following her hand at 1.0-1.8s, then locked.
ACTION: the phone is already buzzing on the wood in the first frame; she turns it face-down with her RIGHT hand and leaves the hand on it.
TIMING: 0-0.4s she looks at the screen; 0.4-1.0s her jaw sets and her eyes leave the phone, down and to frame left; 1.0-1.8s the hand turns the phone over, unhurried; 1.8-3.2s one long breath in through the nose, shoulders rising a little; 3.2-4.4s the breath leaves slowly and her thumb presses the edge of the case twice; 4.4-5.0s still, eyes on the table, the buzzing stops. The shot ends on the held look.
AUDIO: the phone buzzing against the wood until 4.6s, rain on the window, the fridge hum, her breath.
LOCK: no tears; eyes never return to the phone after 0.4s.
GLOBAL LOCK: one continuous shot, no cuts. The white oval in @Image1 is a placeholder mask, never rendered. Nobody speaks. No text, no logos, no music.
LIGHTING: cold phone glow from below on her chin and the underside of her nose until the phone turns over, then only the warm tungsten spill from the hallway at frame left and behind her; the far side of her face falls into shadow; a small warm catchlight in her eyes.
```

The second is about five times longer and has no adjective that isn't a physical fact. That is the target.
