---
name: hybrid-footage
description: Combines real footage with generated footage - shooting for the model, restyling or relighting real clips, keeping the actor while changing the world (wardrobe, set, era, weather), performance capture onto a character, generated backgrounds behind keyed actors, render-to-real from 3D blockouts, and integration checks. Use whenever real video or a 3D previs render is an input.
---

# Hybrid footage

Read `${CLAUDE_PLUGIN_ROOT}/handbook/11-hybrid-filmmaking.md` (and `10-planning-and-previs.md` for render-to-real). Current engines and limits: `16-tool-landscape.md`.

## Before anything: consent

Only footage of people who have signed the consent form (handbook 15, section 10) for the uses you need (course screening, portfolio, publication); record it in the provenance rows of `07_delivery/delivery.md`. Never transform someone into a real public figure. Never work around a provider's face or safety filter.

## Shooting for the model (tell the director before they shoot)

Steady camera (tripod or braced), constant 24/25 fps (turn off variable frame rate if the phone allows), locked exposure and focus, even soft light, two 15-20 second takes, the action already underway at the start, 5 seconds of clean plate (the empty frame), no fast motion blur on faces, the lens you intend to imply, room tone recorded for 30 seconds.

## Keep the actor, change the world

1. **Trim** the take in the editor to the usable section; save to `04_shots/<SHOT>/source/`.
2. **Write the brief:** what must stay (face, performance, timing, eyeline, hands) and what changes (wardrobe, set, era, weather, style).
3. **Look on frame one:** extract a frame (`film frames source.mp4 --at 0.5`), edit it into the target look with an identity-preserving image edit, and approve it.
4. **Generate** video-to-video with the look frame as reference. Prompt: what stays first, then what changes, then constraints ("keep the actor's face, expression, timing and eyeline exactly; change the kitchen into a 1970s diner at night; no new people"). Two drafts at different transformation strengths. Log as takes: `film take add <SHOT> <file> --mode v2v --tool <tool> --cost <usd>`.
5. **Check** with `film contact --shot <SHOT>` and frames at several times: identity, hands, lips if speaking, flicker, edges, light direction. Ask the director about motion. Rate with a code: `film take rate <take> reject --fail IDENTITY --note "..."`.
6. **Fix locally, cheapest first:** trim around the bad seconds, crop or punch in past a broken edge, then mask the original face or hands back in or region-edit a frame. Log each fix with `film take add <SHOT> <file> --stage fix`. Regenerate everything only as a last resort.
7. **Finish:** upscale the locked take, grade to match the film, add grain once, rebuild the sound of the new world.

## Other hybrid moves

- **Performance capture:** the director's filmed performance drives a designed character; then speech-to-speech into the character's voice keeps the human timing (`performance-voice`).
- **Generated plate behind a keyed actor:** key (or AI matte), build the plate with matching lens and horizon, relight the actor to the plate's light, composite; locked-off shots are far easier.
- **Render-to-real:** a moving grey-box blockout (Blender or similar) with the camera move and timing → a render-to-real engine. The model reads the blockout's camera, layout and motion (including motion you didn't want), and invents surfaces; review what carried over.

## Integration checklist

Light direction and colour · black levels · grain and sharpness · edges and hair · contact shadows · perspective and lens · motion blur · colour of reflected light on skin · sound perspective. Log failures with codes (ARTEFACT, IDENTITY, PHYSICS, WORKFLOW) and hand to `take-doctor` if needed.

## When not to go hybrid

When the shot works fine generated, when the real footage is shaky, badly lit or variable frame rate, when the transformation is so large that nothing of the source survives, or when consent is unclear.
