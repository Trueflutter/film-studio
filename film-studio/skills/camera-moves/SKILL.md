---
name: camera-moves
description: Use when writing any video generation prompt (Seedance or similar) and choosing how the camera moves; when the user asks for cinematic, dynamic or "more interesting" shots, a one-take or oner, a multi-angle take, drone or aerial shots, an orbit, push-in, pan, tracking or crane move; when clips feel static, floaty, samey or boring; or when every clip opens on the same angle.
---

# Camera moves: shots that feel filmed, not generated

Camera movement is what makes generated video feel expensive. It also goes wrong in predictable ways: floating drifts, moves the model ignores, three moves mashed into one, the same front angle in every clip. This skill turns "make it cinematic" into moves Seedance 2.5 actually performs.

## The rules

1. **Every move has a cause.** The camera moves because something happens: she stands and it rises with her; the car turns and it whips round with it; we learn something and it pushes in. Write the cause into the prompt. No cause, no move (or lock it off).
2. **One move per shot.** Two moves are two shots, or a oner with a cause handing one move to the next.
3. **Write it in four parts:** where the camera **starts** (size and angle), the **move** (verb and direction), its **speed** (slow, steady, fast, snapping), where it **ends** (the framing it settles on). "Low three-quarter close-up; the camera arcs slowly to the front and pushes in, settling on her eyes."
4. **Vary angle AND distance across clips.** No two clips of a person open the same way: a close-up push-in, a wide that pulls back, a low side track, a three-quarter arc. Plan it in a table before writing prompts.
5. **Faces get slow moves.** Fast moves are for cars, cities, products and transitions. A generated face holds at most 4 s; the move should be finishing by then.
6. **Timestamps are honoured.** In Seedance 2.5, 1-second-precise beats with no gaps (`0-3s`, `3-6s`...). "Hard cut to" between beats gives a real cut within about 0.4 s; "Still the same take, no cut" gives a continuous move. Say the take type three times: in the style line, in each beat, in the constraints.
7. **Name what stays still.** "The camera settles and holds for the last second" gives you an edit point. Real camera operators land their moves; models drift unless told to stop.
8. **Describe places, never name the city** (the model adds the landmark), and never ask for readable text on screens or signs.

The full list of moves, with the wording that works and what to avoid, is in `reference/moves.md`. Ready-made shot plans (presenter clips, multi-angle B-roll, the one-take brand film, product, property) are in `reference/recipes.md`.

## How to work

1. **Plan the coverage first** as a small table: clip, purpose, start framing, move, speed, end framing, cause, duration. Check it against rule 4 and show it with the prompts in one view.
2. **Write each prompt**: STYLE (the look, the take type), the subject and place, the timestamped beats (one move each), SOUND, CONSTRAINTS (take type again, no text or logos, who speaks).
3. **Critique once before generating**: does every beat have a cause, one move, an end framing? Is any face held over 4 s? Would a real crew be able to shoot it?
4. **After generating, check the moves happened**: detect the cuts (a scene-change scan), look at the first and last frame of each beat, and compare with the plan. A move that didn't happen is a note for one re-roll with the move stated more plainly, not a rewrite.

## Stills that move

Pictures in an edit get 2D camera moves in code (push, pan, parallax), not generation. The numbers live in the `motion-design` skill (`drift`, `push`). Direction follows the story: into the building, push in; along the waterfront, pan with it.
