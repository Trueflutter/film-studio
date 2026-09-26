# 06 · Generation craft

The model is your camera crew, cast and art department, and it follows instructions literally and forgets everything between takes. Generation craft is choosing the right *mode* for the job, giving every input a *job*, and writing prompts that direct rather than decorate. Engines change monthly; these habits don't.

## The short version

1. **Choose the mode before the words.** Text-to-video, image-to-video, first/last frame, reference-to-video, multishot, video-to-video, audio-driven, extend or edit: each solves a different problem.
2. **Every input gets a job**, stated in the prompt. An unlabelled reference is noise.
3. **"Use as first frame" pins; "reference" borrows.** Know which one you mean.
4. **Prompt like a shot card:** frame and camera → subject and one action → light → performance → sound → constraints.
5. **The model has no memory.** Restate the anchor line, the screen sides, the location lock in every prompt, verbatim.
6. **Fresh start frame for every new angle.** Chain last frames only to continue the same angle.
7. **Generate 2, pick 1** on high-variance modes. Draft first, always.
8. **Prompts live in files** (`04_shots/S03/prompt_v2.md`), so every take is reproducible.

## Modes: what each is for

| Mode | Use it when | Watch out for |
|---|---|---|
| **Text-to-video** (native) | B-roll, establishing, one-off characters, organic "filmed" texture; exploring | little control over identity and composition |
| **Image-to-video** (start frame) | composition, light and identity must be exact | the still's look (and any synthetic sheen) carries into motion |
| **First + last frame** | a controlled transformation or move between two known states | unnatural in-between motion if the frames are far apart |
| **Reference-to-video** (multi-reference) | identity, wardrobe, product and location held by images without pinning the first frame | references leaking their background, light or grade; say "identity only" |
| **Multishot** (several hard cuts in one generation) | coverage of one moment in one place with one main character | sometimes renders one continuous move instead of cuts: generate 2, keep the one that cut |
| **Video reference** | borrowing camera movement, blocking, rhythm or an effect from a clip (incl. a phone-shot or blockout reference) | the model may copy unwanted motion too |
| **Audio-driven** (audio reference) | dialogue with real lip sync, beat-synced cuts | needs the exact transcript and clean audio (handbook 07) |
| **Video-to-video / edit** | restyle, relight, replace the world around real or generated footage | identity and hands drift; check every frame (handbook 11) |
| **Extend** | continue a take in the same angle | drift accumulates; keep chains short |

## Inputs and their jobs

The strongest prompts assign every input a job in the first lines:

```
@image1 as the first frame (pins composition and light)
@image2 as identity reference for Maya: face only, do not copy its background, light or grade
@image3 as wardrobe reference: the grey cardigan and white shirt
@video1 as camera movement reference: the slow push-in and its timing
@audio1 as the exact voice and timing for lip sync
```

Rules:
- **Pinning vs borrowing.** "Use as first frame" makes the video start on that image. "Reference" borrows identity, mood, camera or material without forcing the frame. Mixing them up is the most common "why doesn't it start on my image" complaint.
- **Priority when slots run out:** motion or camera reference first, subject consistency second, mood third.
- **Name the leak you don't want.** Identity references pass on their grey background and flat light unless told not to.
- Reference limits vary widely by engine (from 3 to 50 inputs in Sept 2026; handbook 16).

## The prompt

Structure that works across engines:

```
[Frame and camera]  Medium close-up, 50mm, eye level, locked-off.
[Subject + action]  Maya (same face as @image2), grey cardigan, sits at the kitchen table and turns her phone face-down, keeping her hand on it.
[Light]             Only the phone's cold glow from below; warm hallway light spilling in from frame left behind her.
[Performance]       She doesn't look at the phone. Her thumb presses the edge of the case. Small, still.
[Sound]             Rain on the window; the phone buzzes against the wood.
[Constraints]       Only Maya in frame. No text, no music. Same kitchen as @image1.
```

- **Length:** as long as the decisions, no longer. Most good video prompts are 60-200 words. Adjective stacks don't add control; they add noise.
- **Vocabulary:** real names for sizes, lenses, moves, light setups and film stocks do real work in one word. Some tokens tint: a warm film-stock word gave us an orange cast (studio-tested). Test stock words before you rely on them.
- **Timecodes** for multi-beat shots on engines that follow them: `[0-2s] ... [2-5s] ...`. Still one action per beat.
- **Physics must be named** (cloth, liquid, weight, contact); models don't infer it reliably.
- **Negatives:** a short constraints line works ("only Maya in frame; no text; no camera movement"). Long "avoid" lists compete with the direction.
- **Language:** some creators report better adherence prompting ByteDance models in Chinese. Treat it as a hypothesis: A/B it on your shot, judged in motion (dialogue stays in the spoken language).

## Keeping the world together across shots

- **Solve geometry at image time.** Each new angle gets a fresh start frame made from the reference pack and the location plate; the video render reframes approved geometry instead of inventing it.
- **Chain last frames only for the same angle** continuing (`film frames clip.mp4 --last`). A frame from A's over-the-shoulder cannot build B's reverse.
- **Keep chains short:** 2-3 links, then re-anchor on the original references. Each full regeneration is a photocopy of a photocopy.
- **Lock lines, verbatim, every prompt:**
  - 180°: _"Camera stays on one side of the line. Maya screen left looking right; Sami screen right looking left. Don't swap or mirror them."_
  - Geography: _"Same room as the plate: the fridge on the left wall, the window behind Maya, the doorway frame right."_
- **Paste the scene list.** For multi-cut generations, paste the plain-text list of cuts (`N) label (lens | size | move) action. dialogue`) verbatim; a board image alone doesn't carry cut order or dialogue reliably (studio-tested).

## Multishot and coverage

For one moment in one place with one main character, generating the coverage *in one pass* gives cuts that match (same light, same room, same face) and avoids the jarring join of separate generations.
- Up to about three cuts in 10 seconds is the reliable range (Kling 3.0 multishot, studio-tested May 2026).
- Write it as hard cuts: _"render as three distinct hard cuts, not crossfades"_.
- Put the face where the engine holds it best (early cuts); make the last cut an insert, a wide or an over-the-shoulder.
- Generate 2 and keep the take that actually cut.
- A "cut to" prompt on some engines produces one continuous move through several sizes instead of cuts; that's useful too: harvest frames from it as start frames (stills from motion).

## Stills from motion and burst frames

- **Stills from motion:** generate a short native video and pull frames (`film frames clip.mp4 --every 0.5`). Frames from a video model often look more "filmed" than a crisp image model's still, and one generation gives a coverage set.
- **Burst frames:** one video pass where only the camera moves around a still character; harvest ~20 matching angles for a turnaround (handbook 05).
- Clean a harvested frame (same-resolution cleanup or an upscale) before it becomes a hero start frame.

## Engines (September 2026 snapshot)

Personalities, not rankings. Prices, limits and routes: handbook 16.

| Engine | Strong at | Watch out |
|---|---|---|
| **Seedance 2.5** | reference-heavy shots (up to 50 inputs), 4-30 s, dialogue with audio reference, edit and extend, **Draft Mode** (480p draft → 1080p final from the same task) | reviewers note soft faces on 720p push-ins and blur in fast motion (reported) |
| **Seedance 2.0** | proven audio-reference lip sync (studio-tested), 4K tier | no draft mode; ≤ 9 images, 3 videos, 3 audio |
| **Kling 3.0** | motion and action, camera and motion control, multishot coverage | talking heads jerk above ~12-15 words per 5 s (studio-tested); no seed, non-deterministic |
| **Veo 3.1** | polished product and lighting, native audio, extension | lip sync can fade late in clips (studio-tested); Fast/Lite are different models, not drafts |
| **Gemini Omni 1.1 Flash** | new top of the with-audio arena (reported Sep 2026); edit, extend, first/last frame | non-deterministic regardless of seed; no audio reference |
| **MiniMax H3 / H3 Max** | very fast and cheap drafting, "Regenerate to 2K" of a chosen take, render-to-real from blockouts | 768p native on H3 Max; physics weaker on demanding action (reported) |
| **Runway Aleph 2, Luma Ray 3.2** | editing real or generated footage (restyle, relight, reframe, keyframes) | identity and hands need checking |

Route by job: the style bible's routing table, reviewed each production.

## Weak vs strong

**Weak:** _"@image1 @image2 @image3 cinematic scene of Maya in her kitchen at night, sad, rain, beautiful, 8k"_

**Strong:**
```
@image1 as the first frame. @image2 as identity reference for Maya: face only, don't copy its background or light.
Medium close-up, 50mm, eye level, locked-off.
Maya turns her phone face-down on the table and keeps her hand on it; she doesn't look at it.
Cold phone glow from below; warm hallway light from frame left behind her; the kitchen otherwise dark.
Rain on the window; the phone buzzes against the wood. No music.
Only Maya in frame. Same kitchen as @image1: fridge on the left wall, window behind her.
```

## In the studio

- `prompt-director` skill: turns a shot card into an engine-specific prompt with inputs and jobs, and chooses the draft and final routes.
- `film gen S03 --via ark|evolink|fal --model <id> --prompt-file 04_shots/S03/prompt_v2.md --image <start frame> --draft --count 2` (generate and log); or generate in a web UI and `film take add`.
- `film frames` (stills from motion, last frame for chaining) · `film contact` (compare takes) · `film dailies`.

## Drills

1. **Assign jobs (10 min).** Take a messy multi-reference prompt and rewrite only the first lines so every input has a job.
2. **Mode swap (20 min).** One shot in two modes (text-to-video and image-to-video). Which gave control, which gave life?
3. **Multishot (20 min).** Three cuts of one moment in one pass. Generate 2; keep the one that cut; note where the face held.
4. **Chain or re-anchor (15 min).** Continue a take by chaining its last frame; then make the next angle from a fresh start frame. Compare continuity.
