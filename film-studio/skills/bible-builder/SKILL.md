---
name: bible-builder
description: Builds character bibles, anchor lines, reference packs (master face, turnarounds, headless full-body views, expressions, wardrobe states), location plates with lock lines, world bibles and the style bible. Use when designing a character, location or the look of a production, when identity or wardrobe drifts, or before any multi-shot generation.
---

# Bible builder

You design the things that must stay the same. Read `${CLAUDE_PLUGIN_ROOT}/handbook/05-continuity.md` and `04-realism.md` first.

## Character

1. `film character "Name"` creates `02_design/characters/<name>/bible.md`.
2. **Inside half first** (want, need, wound, contradiction, how they hide what they feel, voice, arc). Ask the director; don't invent a psychology they haven't chosen.
3. **Anchor line** (≤ 35 words): age, build, face shape, skin tone and surface, hair, 2-3 unmistakable features, signature garment. This exact line goes into every prompt with the character. Never paraphrase it later.
4. **Reference pack** into `refs/`. Write each prompt to a file, generate, and log against a look-development id `LOOK-<NAME>` (not a shot id), e.g. `film take add LOOK-MAYA 02_design/characters/maya/refs/face_34.png --stage still --cost <usd>`; `film cost` counts it as exploration, not as a shot:
   - `face_34.png`: the master. Face close-up, three-quarter view, neutral expression. Describe skin as a surface (pores, fine lines, freckles, stubble, flush), light as flat and even, background neutral grey. Never "beautiful", "flawless", "stunning". Iterate until the director approves.
   - `face_front.png`, `face_profile.png`: derived **from the master** with an identity-preserving edit model ("same person, same face; change only the camera angle").
   - `body_front.png`, `body_back.png`: full body in wardrobe A, **head cropped out or tiny**, neutral grey, flat light.
   - `expressions.png`: only the 4-6 expressions the script needs, derived from the master.
   - `wardrobe_<state>.png`: one per costume state; garments listed by colour and material.
   - Optional turnaround: a 3x3 grid, or burst frames (a video pass where only the camera orbits; harvest with `film frames <clip> --every 0.6`).
5. **Keep sheets boring**: neutral grey, flat light, no grain, no grade, no dramatic lens. The look belongs to the shot.
6. **Audit**: `film contact` or place the pack side by side and compare against the master (face, age, skin, hair, wardrobe). Fix drift by editing the region from the master and compositing, never by regenerating the whole image again. Move rejects to `refs/_rejected/` with a reason. Mark approved images in the bible.

## Locations (`02_design/world.md`, `02_design/locations/`)

- A **plate**: 3/4-view wide of the empty set, landscape, no people, one **anchor object**, one **light logic** sentence.
- A **reverse**: from an empty-set walk-through video or an edit of the plate.
- **Landmarks by screen side** from the master angle, and a paste-able **lock line**: _"Same room as the plate: [landmark] on the left wall, [landmark] behind her, window light from screen right."_
- Props with continuity weight and their state changes.

## Style bible (`02_design/style.md`)

Ask the director, then write concise, testable rules: the look in one line; three lenses; the movement rule; the light motivation rule and colour temperatures; palette (dominant, accent, forbidden); texture (grain goes on in post, once); performance rules; sound palette; the AI tells they refuse; the model routing table with draft and final routes per shot type (check `${CLAUDE_PLUGIN_ROOT}/handbook/16-tool-landscape.md`, it's dated).

## Product (ads)

Product references from several angles plus material and hardware close-ups, each with a stated job. Real labels, logos and UI are composited in post, never generated.

## Output

Everything saved in the production folder; tell the director what was created and what needs their approval. Never mark a reference approved yourself.
