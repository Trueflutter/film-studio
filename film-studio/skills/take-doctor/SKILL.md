---
name: take-doctor
description: Diagnoses failed or weak generations and prescribes the cheapest fix. Use when a take looks wrong, drifts, feels fake, ignores the camera, has bad lip sync or artefacts, when deciding whether to re-roll, change the prompt, change references, split the shot, switch engine or fix in post, and to rate takes with diagnosis codes.
---

# Take doctor

You diagnose before you prescribe. Read `${CLAUDE_PLUGIN_ROOT}/handbook/12-diagnosis-and-iteration.md` (and `04-realism.md` for AI tells).

## What you can see

You can't watch video or hear audio. Get evidence:
- `film contact --shot <SHOT>` (one row per take) and `film frames <take file> --at t1,t2` around the problem moment; look at those images.
- Ask the director what they saw in motion and heard ("where does it go wrong, at what second, what does it feel like?"). Motion, performance, sync and sound verdicts are theirs.
- Read the take's row in `04_shots/takes.csv`, its prompt file, the shot row and purpose, and the references used.

## The procedure

1. **Purpose check.** Would this shot do its job if it rendered perfectly? If not: CONCEPT, and go straight to redesign options.
2. **Name the failure** with one or more codes: CONCEPT, REF, PROMPT, MODEL, MODE, CAMERA, ACTION, FRAME, IDENTITY, PHYSICS, PERFORMANCE, SYNC, ARTEFACT, WORKFLOW (`film take codes`).
3. **Trace it:** is it the idea, the input (REF, FRAME, PROMPT, CAMERA, ACTION), or the tool (MODEL, MODE, WORKFLOW)?
4. **Prescribe the cheapest rung** of the remedy ladder, and say what the rung above would be if it fails:
   0 keep and cut around (use the good 1-2 seconds) · 1 fix in post · 2 re-roll the same inputs (max 2, only for random-looking failures) · 3 change ONE variable · 4 change the start frame or references · 5 simplify or split the shot · 6 change mode · 7 change engine · 8 redesign (different angle, insert, sound-only beat, real footage, cut).
5. **Three strikes:** if this approach has already failed three times, you're at rung 5 or above. Say so plainly.
6. **Write the fix:** if it's a prompt change, create the next version file changing only the one variable, and name the variable in the file name.
7. **Log it:** `film take rate <take> reject --fail CODE+CODE --note "next: <rung and change>"`.
8. Periodically run `film cost` and tell the director which fail code is costing them most.

## Quick table (symptom → first fix)

| Symptom | Code | First fix |
|---|---|---|
| face younger/smoother/symmetrical | IDENTITY/REF | re-anchor on the master; describe skin surface; region-edit, don't regenerate twice |
| wardrobe drift | IDENTITY | wardrobe reference with a job; garments by colour and material in the anchor line |
| extra people | PROMPT | "only [name] in frame"; check references for extras |
| camera drifts or pushes in | CAMERA | "locked-off"; or give the move a cause |
| move ignored | CAMERA/MODE | one precise verb; motion reference video; camera controls |
| slow, floaty, weightless | PHYSICS/ACTION | name speed and weight; shorter clip; speed up in post |
| melting hands | ARTEFACT | hands on a task with a prop; out of close-up; trim; insert |
| garbled text | WORKFLOW | composite text in post |
| late-clip degradation | ARTEFACT | trim; generate a little longer |
| colour cast | PROMPT/REF | state white balance; drop tinting stock words; fix in grade |
| wrong words on lips | SYNC | exact transcript in prompt; clean audio; play embedded audio |
| voice timbre shifts | SYNC | speech-to-speech the clip's own audio to the locked voice |
| overacting | PERFORMANCE | task + tell instead of emotion words; shorter line |
| dead eyes / deadpan | PERFORMANCE/FRAME | give the eyes a target; start frame in the right expression state |
| starts on an awkward turn | FRAME | start frame in the first state of the action |
| multishot didn't cut | MODE | "N distinct hard cuts, not crossfades"; generate 2 |
| separate clips jar at the cut | WORKFLOW | transition rule: change size and angle, cut on action, cut away, or generate coverage natively |
| sides swap between cuts | IDENTITY/FRAME | 180° line in every prompt; fresh start frame per angle |
| room rearranges | REF/PROMPT | location plate with a job + verbatim lock line |
| gear/drones/floating limbs | PROMPT | "no production equipment", "no drone", "bodies attached and grounded" |
| pretty but meaningless | CONCEPT | back to purpose; change the action, not the adjectives |

## Tone

Be specific and brief. One diagnosis, one fix, one fallback. Never recommend a fourth identical re-roll.
