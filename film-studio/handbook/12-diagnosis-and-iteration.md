# 12 · Diagnosis and iteration

A bad generation is information. The skill that separates a filmmaker from a slot-machine player is naming *where* the failure came from and choosing the *cheapest* fix that addresses it. This chapter gives you a vocabulary (the codes), an order of operations (the remedy ladder) and a table of the failures you will meet most.

## The short version

1. **Watch it in motion, full screen, before you judge.** Stills lie; a verdict made from a frame grab flipped in our own tests.
2. **Name the failure with a code** before touching the prompt. Wrong diagnosis, wrong fix.
3. **Ask three questions in order:** is it the idea, is it the input, is it the tool?
4. **Climb the remedy ladder from the bottom.** Most failures are fixed on the first three rungs.
5. **Change one variable per attempt.** Otherwise you can't tell what worked.
6. **Three strikes on the same approach = redesign.** A strike is the same failure coming back after a one-variable fix. Never a fourth identical roll.
7. **Log the verdict and the code** (`film take rate`). Your codes are your habits; the cost report shows which ones cost most.

## The three questions

**1. Is it the idea?** Would this shot do its job even if it rendered perfectly? If the answer is no, no prompt will save it. (CONCEPT)

**2. Is it the input?** Did the model get what it needed: the right start frame, references with jobs, a prompt that asks for one clear thing, a camera instruction that fits the action, an action that fits the duration? (REF, FRAME, PROMPT, CAMERA, ACTION)

**3. Is it the tool?** Is this the right engine and the right mode for this job, or should it be done another way entirely (post, composite, real footage, a different shot)? (MODEL, MODE, WORKFLOW)

Everything else (IDENTITY, PHYSICS, PERFORMANCE, SYNC, ARTEFACT) is a symptom category: log it, then trace it back through the three questions.

## The codes

| Code | Means | Usually traced to |
|---|---|---|
| **CONCEPT** | the shot doesn't communicate its story purpose, however well it renders | purpose never written; pretty instead of meaningful |
| **REF** | reference image weak, conflicting, wrong angle or light, or carrying an AI look | reference pack, reference job not stated |
| **PROMPT** | ambiguous, overloaded, contradictory, or the wrong vocabulary | adjectives instead of causes; two ideas in one prompt |
| **MODEL** | the wrong engine for this job | habit; not routing by shot type |
| **MODE** | wrong generation mode (text-to-video, image-to-video, reference, first/last frame, multishot, video-to-video, audio reference) | didn't choose the mode deliberately |
| **CAMERA** | move ignored, unmotivated, or fighting the action | two moves; move with no cause; vague verb |
| **ACTION** | too much for the duration; more than one beat | a sequence written as one shot |
| **FRAME** | start frame's composition, pose or light set it up to fail | start frame shows the wrong first state of the action |
| **IDENTITY** | character, wardrobe, product or location drift | references, anchor line paraphrased, small faces, chaining too deep |
| **PHYSICS** | weight, contact, cloth, liquid or collision reads false | physics not named; action too fast; wrong engine |
| **PERFORMANCE** | wooden, exaggerated or off-emotion | emotion words instead of behaviour; line too long |
| **SYNC** | lip sync, dialogue timing, audio artefacts | transcript missing, noisy audio, floating VO |
| **ARTEFACT** | hands, morphing, flicker, melting, extra limbs, garbled text | late-clip degradation; text asked of the model |
| **WORKFLOW** | should have been solved another way | using generation where post, compositing or a real shot is cheaper and better |

`film take codes` prints this list.

## The remedy ladder

Start at the bottom. Each rung costs more than the one below it.

| Rung | Remedy | Use when |
|---|---|---|
| 0 | **Keep it and cut around it** | the good part is 1-2 seconds long: use only that (most shots in a finished film are trimmed hard) |
| 1 | **Fix in post** | reframe or punch in, trim the bad head/tail, crop out an artefact, flip, speed-ramp, reverse, stabilise, region-edit one frame, cover with an insert or a reaction, fix the colour |
| 2 | **Re-roll the same inputs** (max 2) | the failure looks random (a stray hand, a one-off flicker) rather than systematic |
| 3 | **Change one variable** | the failure is systematic: rewrite the one clause, remove an adjective stack, name the physics, fix the camera verb |
| 4 | **Change the start frame or references** | FRAME, REF, IDENTITY: the input is teaching the model the wrong thing |
| 5 | **Simplify or split the shot** | ACTION, CAMERA: one action per shot, one move per shot; two beats become two shots |
| 6 | **Change mode** | e.g. text-to-video → image-to-video for control; separate shots → native multishot for coverage; floating VO → audio reference for sync |
| 7 | **Change engine** | the engine is weak at this job (fast action, faces at speed, dialogue, product text) |
| 8 | **Redesign** | CONCEPT or three strikes: a different angle, an insert instead, a sound-only beat, real footage, or cut the shot |

**Three strikes.** Three failed attempts on the same approach means you are at rung 5 or above. Don't pay for a fourth identical roll.

## Symptom → cause → cheapest fix

| Symptom | Likely code | Cheapest fix that usually works |
|---|---|---|
| Face gets younger, smoother, more symmetrical | IDENTITY / REF | re-anchor on the master reference; describe skin surface and age marks; region-edit the face, don't regenerate the image |
| Wardrobe or pattern changes between shots | IDENTITY | wardrobe reference with a stated job; list garments by colour and material in the verbatim anchor line |
| A second person appears | PROMPT | "only [name] in frame, no other people"; check the reference doesn't contain extras |
| Camera floats, drifts or pushes in by itself | CAMERA | "locked-off, tripod"; or give the move a cause ("the camera follows her as she stands") |
| Camera move ignored | CAMERA / MODE | one move, a precise verb; for exact moves use a motion reference video or camera controls |
| Everything in slow motion, weightless | PHYSICS / ACTION | name speed and weight ("quick, heavy step; the chair scrapes"); shorter clip; stronger action verb |
| Hands melt or gain fingers | ARTEFACT | keep hands out of close-up, give them a task with a prop, trim to the good frames, cut to an insert |
| Garbled text, signs, screens | WORKFLOW | never ask the model for text: composite it in post; keep screens angled away or blurred |
| Last second of the clip degrades | ARTEFACT | trim; generate a little longer than needed and use the best seconds |
| Colour shifts cool or orange between shots | PROMPT / REF | state white balance ("warm white balance, 4500K"); remove film-stock tokens that tint (a warm stock word gave us an orange cast); match in the grade |
| Lips move but say other words | SYNC | put the exact transcript in the prompt; clean the audio; play the clip's own embedded audio |
| Voice timbre changes mid-line | SYNC | speech-to-speech the clip's own audio to the locked voice (timing kept, lips stay locked) |
| The same line appears in two clips | SYNC | mute the second clip's copy, trim its head |
| Actor overacts | PERFORMANCE | replace emotion words with a task and a tell; shorten the line; add "natural, understated" |
| Actor is dead-eyed | PERFORMANCE / FRAME | give the eyes somewhere to go; a neutral start frame gives deadpan video, so start from the right expression state |
| Starts on an awkward half-turn | FRAME | start frame already in the first state of the action; never open on a turn to camera |
| Multishot rendered one continuous shot | MODE | "render as N distinct hard cuts, not crossfades"; generate 2, keep the one that cut |
| Two separate clips jar when cut together | WORKFLOW | the transition rule: change size and angle, cut on action, cut away, or generate the coverage natively |
| Characters swap sides between cuts | IDENTITY / FRAME | 180° line and screen sides stated in every prompt; fresh start frame per angle; never chain a last frame across an angle change |
| Room rearranges itself | REF / PROMPT | location plate with a job plus the verbatim landmark lock line; never describe the room in fresh prose per shot |
| Camera gear, drones or floating limbs appear | PROMPT | "no production equipment visible", "no drone", "all bodies attached and grounded" (studio-tested re-roll clauses) |
| Beautiful but meaningless | CONCEPT | go back to the purpose line; change the action, not the adjectives |

## Working the problem: an example

Shot S05: a man sets a mug down hard and walks out. Draft 1 fails.

1. **Watch in motion.** The mug floats down, the man glides out, and the camera slowly pushes in. It reads as calm, the opposite of the purpose (anger he won't voice).
2. **Code it.** PHYSICS (floaty mug), CAMERA (unmotivated push), ACTION (two beats: slam *and* exit in 4 seconds).
3. **Three questions.** Idea: fine. Input: yes, two actions and a push the story doesn't need. Tool: fine.
4. **Ladder.** Rung 5: split. S05a: insert, 85mm, locked-off, the mug hits the table hard, coffee jumps, a ring of liquid on the wood. S05b: medium, 35mm, locked-off, he's already turning away, the door swings. Sound carries the anger: the knock of ceramic, the door not quite slammed.
5. **Result:** two drafts each; S05a locked on draft 2, S05b on draft 1. Four drafts at about $0.50 instead of re-rolling the original combined shot at 1080p.

## Iteration hygiene

- **One variable per attempt**, and name the file after it: `prompt_v4_locked-cam.md`.
- **Prompts live in files** so every take is reproducible and `takes.csv` points at the exact text.
- **Keep rejects** in the log with codes. They are the data behind your next style-bible rule.
- **Review in `film dailies`**, not in a download folder. Verdicts and codes only; discussion later.
- **A/B properly:** change one thing, generate two per arm, judge in motion, blind if you can. Our studio's A/B of two prompt styles was reversed once the clips were watched in motion rather than as stills.

## In the studio

- `take-doctor` skill: give it a take (or the dailies page) and the shot's purpose; it proposes a code and the cheapest rung, and rewrites only the one variable.
- `film take rate S05_t001 reject --fail PHYSICS+CAMERA+ACTION --note "split into insert + exit"`
- `film take codes` · `film dailies` · `film contact --shot S05` (spot drift across takes at a glance) · `film cost` (see which codes cost most).

## Drills

1. **Code ten takes (15 min).** Pick ten rejected takes (yours or a classmate's). Code each, then name the cheapest rung. Compare with a partner.
2. **One variable (20 min).** Take a failing shot and fix it by changing exactly one thing per attempt. Stop after three and write what you learned.
3. **Split it (15 min).** Find a shot in your shot list with two actions. Rewrite it as two shots and board both.
4. **Fix it in post (15 min).** Take a rejected take and rescue two usable seconds from it with trims, a reframe and an insert, without generating anything.
