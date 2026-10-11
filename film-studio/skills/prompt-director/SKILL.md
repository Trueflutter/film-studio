---
name: prompt-director
description: Turns a shot card into directed, engine-specific image and video prompts with every input given a job; chooses mode (text-to-video, image-to-video, first/last frame, reference, multishot, video reference, audio-driven, edit) and engine; plans the draft route and the final route; runs or logs the generation. Use whenever writing a prompt, picking a model, or generating a shot.
---

# Prompt director

You turn the director's intent into instructions a model can execute. Read `${CLAUDE_PLUGIN_ROOT}/handbook/06-generation-craft.md` and `04-realism.md`; check `16-tool-landscape.md` before naming engines, prices or limits (it's dated; say so if it's more than a month old).

## Procedure for a shot

1. **Read the row** in `03_board/shotlist.csv`, the bibles it references, `02_design/style.md` and `03_board/continuity.md`.
2. **Shot card** into `04_shots/<SHOT>/prompt_vN.md` (template `04_shots/_prompt_template.md`): purpose · subject and ONE action · frame (size, angle, lens, composition) · camera (one move and its cause, or locked-off) · light (source, direction, quality, colour) · performance (behaviour: a task, the eyes, one tell) · sound · continuity locks.
3. **Choose the mode**, and say why in one line:
   - identity/composition must be exact → image-to-video from a start frame;
   - non-identity B-roll/establishing → native text-to-video (or harvest a still from a native generation), because crisp generated stills can import a synthetic look;
   - one moment, one place, one main face, 2-3 angles → native multishot (generate 2);
   - dialogue that matters → audio-driven (hand to `performance-voice`);
   - a camera move that keeps failing → video reference (phone clip or blockout);
   - changing real footage → `hybrid-footage`.
4. **Choose the engine** from the style bible's routing table; mention an alternative.
5. **Write the inputs with jobs** at the top of the prompt:
   `@image1 as first frame` (pins) · `@image2 identity reference: face only, don't copy its background, light or grade` · `@image3 wardrobe reference` · `@video1 camera movement reference` · `@audio1 exact voice and timing`.
6. **Write the prompt** in this order: frame and camera → subject and action → light → performance → sound → constraints. Paste the character anchor line, the 180° line and the location lock line **verbatim**. For multi-cut generations paste the scene list verbatim. 60-200 words of decisions; no "cinematic, 8k, masterpiece, beautiful".
7. **Plan the ladder** in the prompt file: still route (if any) → draft route (480p / Draft Mode / cheapest tier; how many tries) → final route (promote the locked draft, upscale it, or premium re-render from the same start frame).
8. **Generate or hand over:**
   - API: `film gen <SHOT> --via ark|fal|evolink --model <id> --prompt-file 04_shots/<SHOT>/prompt_vN.md --image <start frame> --draft --count 2` (`--dry-run` first on any new model; provider-specific fields via `--param key=value`).
   - Seedance 2.5 linked final: `film gen <SHOT> --via ark --from-draft <SHOT>_tNNN` (only from a `select` draft).
   - `film gen` waits for the job (minutes per clip): run it with the longest Bash timeout, or in the background for a batch. After an interruption, `film jobs --resume` collects pending jobs without paying twice.
   - MCP or web UI: generate, download immediately, `film take add ...` with stage, tool, model, res, cost and the prompt file.
9. **Rebuild the review:** `film dailies`; ask the director to rate. Hand failures to `take-doctor`.

## Still prompts (start frames, boards)

Same order, as a photograph: frame and lens → subject and pose (the first state of the action, never mid-turn) → light → surfaces and wear → constraints ("no text, no watermark, no collage"). For identity shots, derive from the reference pack with an identity-preserving edit rather than generating from prose.

## The oner (motivated continuous shot)

A chain of causes: each subject entering frame hands the camera on (handbook 03). Two or three hand-offs in 12-15 s, one subject per beat:

```
One continuous shot, no cuts. Starts on [frame, lens, height].
Beat 1 (0-4 s): [subject A] [one action]; the camera [move] with them.
Beat 2 (4-8 s): as [subject B] enters frame [from where], the camera leaves A and [move] with B.
Beat 3 (8-12 s): B [action] toward [C]; the camera settles on [final frame] and holds.
The camera only moves when something in frame moves it. Light from [source], constant. [location lock line]
```
If the path keeps failing, give it a video reference (a phone walk-through or a blockout) rather than more words.

## Revising

- One variable per version; name it in the file (`prompt_v4_locked-cam.md`).
- Keep what worked verbatim; never "improve" wording that isn't the problem.
- The length rule: when asked to fix, replace, don't inflate.

## Engine notes (verify dates in handbook 16)

- **Seedance 2.5**: many references with roles; 4-30 s; **Draft Mode**: `--draft` gives a 480p draft; promotion inherits prompt, refs, seed, duration, ratio and audio, and must be 1080p; check faces, hands and text on the final.
- **Seedance 2.5 on EvoLink** (the course route): `seedance-2.5-text-to-video` (native, no refs), `-image-to-video` (start frame; shape comes from the image), `-reference-to-video` (character packs, product photos: 1-8 images are reliable). 480p to explore, 720p to finish; no seed and no linked draft, so the final is a new roll of the locked prompt, and the draft stays the master if the final is worse. Pass a take id or a local file to `--image`; `film gen` reuses or uploads the link. Prompt rules, each fixed a real failure: contiguous timestamped beats (`0-2s ... 2-5s ...`, no gaps) with hard cuts on the second; anything load-bearing (speaking on camera, silence, a smile) stated in the style, the beat and the constraints; override a reference positively ("IGNORE the night light in the reference; this is bright daytime"), never "does not control"; never ask for readable text, ask for its shape ("plain blocks, no readable words"); `--no-audio` on wordless clips (otherwise a music bed appears); dialogue at 2.4-2.9 words a second.
- **Seedance 2.0**: proven audio-reference lip sync; no draft mode.
- **Kling 3.0**: motion and action; multishot with "render as N distinct hard cuts, not crossfades"; face in early cuts; ≤ 12-15 words of speech per 5 s; no seed.
- **Veo 3.1**: polished product/light, native audio; Fast and Lite are different models (a cheap Veo take is a re-roll, not a draft).
- **Gemini Omni, MiniMax H3/H3 Max, Runway, Luma**: see handbook 16.
- Some creators prompt ByteDance models in Chinese for adherence: treat as an A/B, judged in motion.

## Never

- Generate text, logos, UI or signs (composite in post).
- Paraphrase an anchor or lock line.
- Chain a last frame across an angle change.
- Render a premium final for a shot without a `select` draft or still.
- Work around a provider's real-person or safety filter.
