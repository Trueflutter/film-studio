# 10 · Planning and Previs

AI video has no set, no crew and no memory: every generation re-imagines the room, the light and the blocking from scratch. Planning is how you hand the model what it lacks, and it is the cheapest stage of the pipeline. Every decision you make on paper is a re-roll you don't pay for.

## The short version

1. **Decide on paper, spend on pixels.** A question answered in the shot list costs a minute; answered by generating, it costs drafts.
2. **Plan to the shot's difficulty.** Most shots need a shot-list row and a board. A few need a phone reference or a grey-box.
3. **Boards carry the world; text carries the order.** Paste the plain-text scene list verbatim into every generation and every retry.
4. **Lock timing in the animatic, then generate only the shots that survived it.**
5. **Models read moving references, not maps.** For camera, geography and eyelines, give them a phone clip or a grey-box render. A floor plan is for you.
6. **Plan rhythm before you render:** adjacent shots change size and move; an insert every 8-10 s of dialogue.
7. **Write the generation plan before the first draft:** route, draft budget and stop rule per shot.
8. **Simpler is often enough.** A one- or two-character social piece needs boards and an animatic, not Blender.

## Why planning is cheaper than generating

A 5-second Seedance 2.5 draft at 480p costs about $0.50 (BytePlus list, reported Sep 2026); a still costs cents; a shot-list line costs nothing. The economics ladder (still → draft → lock → final → fix, handbook 13) only pays off if every question that doesn't need motion is answered before motion.

| Question | Answer it with | If you answer it by generating |
|---|---|---|
| Does the scene need all 14 shots? | Animatic (free) | You finish shots that get cut |
| Which side of the line is the camera on? | Overhead sketch + `continuity.md` (free) | Eyelines miss across cuts; re-rolls per shot |
| Does the move land on the music hit? | Phone reference or grey-box (minutes) | Timing becomes a lottery at full price |

**Studio case (Apr 2026).** A 15-clip vertical ad, three characters in a living room. Every clip was photoreal; cut together, characters faced the wrong walls and eyelines didn't connect (studio-tested). No prompt was wrong: the shots were never planned as one space, and the model had no space to remember. That is CAMERA plus WORKFLOW (handbook 12), and no prompt fixes it afterwards.

## The planning stack, and when each layer is worth it

Use the lowest layer that answers your question.

| Layer | What it decides | Worth it when | Skip when |
|---|---|---|---|
| Shot list | Purpose, size, lens, move, action, line, sound, duration, route | Always | Never |
| Thumbnails / stick figures | Composition, screen side, eyeline and move arrows (1-2 min each) | Every piece | Never |
| Generated frame per shot | The exact look of one shot; a possible start frame | Shots in different places; hero compositions | Coverage of one scene |
| 3x3 grid / contact sheet | A coherent coverage set: one face, light and set | Several angles of one scene | Shots across locations |
| Production board | The whole world on one sheet, for review | A new world; team or client sign-off | A locked world (use a tone sheet) |
| Animatic | Timing, order, what to cut | More than three shots | A single shot |
| Motion animatic | Whether moves and performances play | Hero and doubtful shots | Shots the board already answers |
| Phone reference video | Camera move, pacing, rough blocking | A specific move; a shot failed on CAMERA twice | Static shots |
| 3D grey-box | Geography, eyelines, timed camera beats | 3+ characters, fixed geography, a beat on a hit, vehicles, occlusion | One- or two-character social pieces |
| Render-to-real | Photoreal shot keeping the blockout's camera and timing | A blockout exists and its timing matters | No blockout |
| Motion grid | Order and shape of multi-step action | Dance, fights, ritual, sport | Single actions, dialogue |

Two-person dialogue usually needs only boards, axis notes in `continuity.md` and native multi-shot coverage (handbook 06). Three or more characters with eyelines need a grey-box: nothing else reliably holds them (studio-tested).

## The shot list (always)

`03_board/shotlist.csv` is the spine: `film boards` and `film animatic` read it, and Claude checks prompts against it. One main action, one camera move and one dominant light cue per shot. The `purpose` column is the filter: if you can't write why a shot exists, cut it now, for free.

### Weak vs strong: a shot-list row and its board

**Weak row and board prompt**
```
S04,2,,,MS,,,,She reacts to the news,What?,,5,,,,
```
`Cinematic storyboard of a woman reacting emotionally to shocking news in a kitchen, dramatic lighting, 8K, masterpiece.`

**Strong row**
```
S04,2,TURN,She learns her brother got the job she was promised,MCU,eye level; she is frame left looking right,50mm,static,She stops drying the mug; her thumb keeps circling the rim,"You got it?",tap drip; fridge hum; no music,3,still → seedance-2.5 draft 480p → final from draft,maya_face_34; wardrobe_A; LOC-01 plate,planned,cover: S04a insert thumb on rim
```
**Strong board prompt**
```
Storyboard frame, 16:9. S04: medium close-up, 50mm, eye level, static.
Maya (face ref maya_face_34; wardrobe A: faded green cardigan, white T-shirt) stands
at the sink in the left third, body three-quarters to frame right, eyes on her
brother, off-screen right. Her hands have stopped on a white mug; her thumb rests on the rim.
Kitchen from the LOC-01 plate: window behind her, frame left.
Light: soft grey daylight from that window. The light over the sink is off.
Plain, unpolished frame. No text, no panels, no captions.
```

| The strong version... | Because |
|---|---|
| Names beat and purpose | The animatic can test whether the film needs it |
| Fixes screen side and eyeline | The reverse on her brother (S05) must look frame left (handbook 05) |
| Gives behaviour, not emotion | "Thumb keeps circling" plays; "reacts emotionally" produces mugging (lever 6) |
| Plans 3 s, not 5 | The engine renders 5; you keep the best 3 (lever 9) |
| Writes sound, route, refs, a cover shot | Silence lands (lever 11); S04a hides a drift (lever 10) |
| Gives light a source and a side | Motivated light survives into motion (lever 1) |

## Boards: sketches and generated frames

**Thumbnails first.** Stick figures, 1-2 minutes each: frame edges, subject position, an arrow for the eyeline, an arrow for the move. Save them as `03_board/boards/S01.png` (named by shot id) and `film boards` and `film animatic` use them. For many pieces, sketches are all the animatic needs.

| | Single frame per shot | 3x3 grid (contact sheet) |
|---|---|---|
| How | One image prompt per shot, same refs each time | One prompt, nine panels of one scene: wide, two-shot, OTS x2, MCU x2, CU x2, insert |
| Strength | Full control of each composition | One sampling pass holds face, light and set across panels |
| Weakness | Face, light and set drift between frames | Panels are about 680 px each at 2K: isolate and upscale a panel (identity-preserving, lowest strength) before it becomes a start frame |

Rules for both:
- **Image models have no 3D scene either.** Boards hold characters well and rooms only moderately; layouts flip between panels (studio-tested).
- **A video model reads a grid as shot order, not exact panels** (reported, Aug 2026). Keep to 15 panels or fewer, map panels to timestamps, state the reading order, and say what to ignore: "do not render line-art style or placeholder figures".
- **Don't retrofit a grid mid-production.** New geometry forces re-renders of locked takes.
- **A board plans a shot; it isn't always the best start frame.** Crisp generated stills can carry an "AI look" into motion. Where identity doesn't matter, generate natively or harvest a frame from motion with `film frames` (studio-tested; handbook 04).

## The production board: one master sheet

One 16:9 image holding the whole world: character references (front, side, back, close-up, relaxed pose), the environment and a top-down plan, a numbered storyboard strip with lens, size and move per panel, palette, light and mood cards, camera notes. It is a review document: one agreed world before anyone spends. In a locked world, a tone sheet (title, numbered strip, one mood line) is enough.

Four studio lessons (studio-tested):

1. **Boards routinely misplace dialogue.** Check every panel against the script before you spend. If it's wrong, regenerate the whole board; patched panels drift.
2. **Video models don't read the top-down floor plan.** Seedance ignored a numbered plan given as a reference. The plan is for the human; blocking reaches the model through panel annotations, keyframes, prompt text or a moving reference.
3. **Paste the plain-text scene list verbatim into every generation and every retry.** Models don't reliably read text inside an image; boards that looked right still produced cuts in the wrong order. Edit the list in its one file, never inline in a prompt.
4. **Give the board a job or leave it out.** Feed clean per-shot keyframes. If the board goes in: "use only for identity, wardrobe and palette; ignore all text and panel layout".

```
MAYA / scene 2: 5 cuts, 13 s, 9:16   (S02 was cut in the animatic)
1) S01 Kitchen wide (24mm | WS | static): Maya at the sink, frame left; her brother at the table, frame right. Tap drips.
2) S03 Brother (35mm | MS | static): he looks up toward frame left. "They gave it to me."
3) S04 Maya (50mm | MCU | static): she stops drying the mug, eyes frame right. "You got it?"
4) S04a Mug insert (85mm | INSERT | static): her thumb circles the rim.
5) S05 Brother (85mm | CU | slow push-in): he holds her look, frame left, and says nothing.
```

**Audit before any spend:** dialogue in the right panels · sizes and moves alternate · identity holds across views · wardrobe and environment match in every panel.

## The animatic

Boards held for their planned durations under temp sound: the cheapest place to decide pacing.

1. One board per shot in `03_board/boards/`. Sketches are fine; a missing board shows as a dark slate.
2. Fill `duration_s` for every row.
3. Record temp VO (your own voice memo is fine) and a temp music bed; bounce to one file.
4. `film animatic --audio temp.wav` builds a timed MP4 in `03_board/` (or cut it in Resolve or CapCut for push-ins and beat cuts).
5. Watch three times: for story, for rhythm, and eyes closed for sound.
6. Set a dead shot's `status` to `cut` (the animatic skips it), adjust durations, re-run.
7. Lock timing. Screen duration sets generation length: add handles, round up to the engine's minimum, keep the best seconds.
8. Generate only the survivors.

| The animatic shows | Fix it before generating |
|---|---|
| The turn arrives too late | Cut setup shots, never the payoff |
| Two shots say the same thing | Keep the one with behaviour in it |
| A line has no picture | Add an insert or a reaction |
| It only works with the VO | The picture isn't telling the story (handbook 02) |

**Motion animatic (optional).** Swap key panels for cheap drafts: a Seedance 2.5 480p draft (about $0.10/s, reported Sep 2026) or a fast low-res engine (fal says H3 Max renders a 5 s clip in about 3 s, reported). A draft that plays and is rated `select` can later be promoted to its final. It spends exploration budget, so reserve it for hero and doubtful shots.

## Reference video for camera: the no-3D fallback

Shoot the move on a phone: 5-10 s, classmates or objects as stand-ins, the path, speed and height you want. Give it one job: "@video1 as camera movement and pacing reference only; do not copy the people, the room or the light." Video references are excellent for camera moves and only partial for blocking: the model copies rough positions but doesn't reliably keep who is where (studio-tested).

One move per clip, exposure locked, 24 or 25 fps, framed at the size you want (use the longer lens for tight shots).

## 3D previs: the grey-box

Video models have no persistent 3D scene (studio research, Apr 2026). A grey-box is the scene they lack, and for 3+ characters with eyelines, fixed geography across many cuts, or a camera beat timed to the frame, it is the only method that reliably holds (studio-tested).

Build it in Blender or any 3D tool: primitives for walls and landmarks; mannequins at the right heights facing the right way; a camera with real focal lengths, animated at 24 fps, 5-15 s per shot; a playblast to MP4. Include only the motion you want: the model copies mistakes too.

Novice routes: a pre-built scene (supplied in class), or Claude building the blockout through a Blender MCP server (reported: fal's own clay-to-real showcase used an agent-driven Blender blockout).

**The distinction to remember:** a *moving* blockout clip is a motion reference, and render-to-real engines are built to read it. A *static* floor plan is ignored (studio-tested).

## Render-to-real

Render-to-real turns a grey-box clip into photoreal video that keeps its layout, camera and timing. Three vendors converged on it between June and September 2026 and every engine is weeks old: the technique is core, the engines are swappable.

| Engine | What it is | Notes |
|---|---|---|
| LTX-2.3 3DREAL (fal + Lovis Odin) | Purpose-built render-to-real LoRA guided by a photoreal first frame; open weights and a hosted endpoint | v1 June 2026; Strong v2 July 2026 adds multi-scene coherence (verified Sep 2026) |
| fal H3 Max | fal's post-trained MiniMax H3; reference-to-video reads the blockout | Launched 1 Sep 2026; 480p or 768p; 5-15 s; about $0.08/s at 768p (verified Sep 2026). An independent test on base H3 showed it reads the blockout, unwanted motion included: a foot shuffle came through |
| Seedance 2.5 blockout | The blockout goes in as a rendered video reference; no 3D-file input | Route verified Sep 2026; quality claims are the vendor's (reported) |

1. Block the shot at 24 fps, 5-15 s; playblast to MP4.
2. Restyle frame 1 into one photoreal keyframe with an image model, so look development stays separate from motion.
3. Generate with playblast + keyframe + character and location refs. The prompt names subject, action to preserve, camera, materials, light, environment, secondary motion, sound and forbidden changes ("do not add people; do not alter the camera path").
4. QC for identity drift, motion artefacts carried over from the blockout, and physics.
5. Upscale the locked take (output is often 768p), then grade and cut.

**Pre-course test protocol.** Seven to ten days before each cohort, instructors run three blockouts (a walk-and-turn, a vehicle on a curve, three people at a table with eyelines) through each candidate engine, score camera, layout, timing, identity and artefacts, and pick the class default. Rerun your own three whenever a new engine appears.

## Camera-controlled generation

When you don't need 3D, control the camera inside the generator. Specs live in handbook 16.

| Control | Use when | Current examples |
|---|---|---|
| Vocabulary and presets | One named move per shot | Kling 3.0 treats dolly, crane and orbit as distinct: lead the prompt with the move (studio-tested). Higgsfield Cinema Studio presets camera body, lens, focal length, aperture and move, but knows nothing of the 180° line or eyelines (studio-tested) |
| Camera and motion control | A specific path, or motion from a reference | Kling 3.0 camera control and motion control; motion control runs 3-10 s from an image, up to 30 s from a video (verified Sep 2026) |
| Keyframes | A precise path through set compositions | Luma Ray 3.2 keyframes-to-video (verified Sep 2026) |
| First and last frame | You know both ends: a door opening, a reveal | Veo 3.1, Gemini Omni 1.1 (verified Sep 2026) |

Research tools that re-shoot a clip along a new path (ReCamMaster, Uni3C) are powerful but fragile, GPU-heavy and ComfyUI-only (verify before cohort). Advanced track only.

## Motion grids for choreographed action

When motion has steps, prompt the steps as an image; a sentence of moves gets blended and skipped. The studio method, from the repo skill `motion-grid-reference` (studio-tested):

1. **Pose plan:** 6-9 poses with timecodes, each a precise body description (feet, knees, hips, torso, shoulders, arms, hands, gaze).
2. **Grid:** one numbered 3x3 image, each panel labelled `POSE N | timecode`. Same character, wardrobe, light and background, same camera distance and angle: only the body changes.
3. **Generate:** grid as motion reference, character image as identity reference, first panel as start frame, the timing map as text, one camera move, "one continuous take, no cuts".

If poses blend: more distinct panels, fewer poses, or two halves sharing an overlap pose. If one panel drifts, regenerate the whole grid.

## Shot rhythm planning

Check the shot list against these studio defaults before you render:
- Adjacent shots change size and move; neighbours never share both.
- Never cut two separately generated shots of one subject at the same size and angle (handbook 03, 09).
- An insert every 8-10 s of dialogue. Pre-plan 2-3 as editorial insurance.
- At least three focal lengths per 15 s.

```
1  WS    static    24mm
2  INS   push-in   85mm   ok
3  MCU   static    50mm   ok
4  MCU   static    50mm   FIX: same size and move as 3. Make it an insert, or a push-in on a new lens
5  WS    push-in   24mm   ok
```

## The generation plan

`03_board/generation_plan.md` decides spend before spend: a budget table (look development, drafts, finals, upscales and fixes, sound, a 20% reserve) and a per-shot plan. Handbook 13 covers the economics.

| Shot | Hero? | Draft route | Final route | Drafts | Stop rule |
|---|---|---|---|---|---|
| S01 kitchen WS | no | native t2v, Seedance 2.5 draft 480p | final from draft | 4 | Harvest a frame from the best draft; use it as start frame |
| S04 Maya line | yes | still → i2v draft, VO as audio reference | final from draft, upscale | 8 | Split line and reaction into two shots |
| S07 three at table | yes | grey-box → render-to-real 768p | upscale locked take | 6 | Simplify to two singles and a wide |

Stop rules come from the remedy ladder (handbook 12): a shot that hasn't converged inside its budget gets simplified, split or redesigned. Three strikes means replan. Hero shots (a fifth of the film at most) may take three times the average budget.

## Google Vids (optional)

A Workspace video editor with Gemini features: script to draft storyboard, AI voiceover, preset avatars, generated clips (Gemini Omni reached Vids in 2026, verified Sep 2026). Good for a pitch video, a slide-style animatic or an explainer rough cut a team comments on; not a production timeline. Features and tiers: verify before cohort.

## Simpler is often enough

Students over-plan easy pieces and under-plan hard ones. A 15-30 s piece with one or two characters needs a shot list, boards and an animatic. Move up a layer only when dailies say so: a shot rejected twice for CAMERA gets a phone reference; eyelines that break across cuts get a grey-box.

## In the studio

- **`/film-studio:shot-designer`**: script to `shotlist.csv`, rhythm and axis checks, board, grid and production-board prompts, the scene list; ask it for a pose plan and grid when a shot has choreography. Try: "Build the shot list for scene 2, 9:16, about 20 seconds, and check the rhythm."
- **`/film-studio:studio`**: runs the stage gates; no `04_shots` until the animatic is watched and the plan has a budget.
- **`/film-studio:bible-builder`**: the references every board uses (handbook 05).
- **`/film-studio:prompt-director`**: a locked row plus the scene list into `04_shots/<SHOT>/prompt_v1.md`.
- **`/film-studio:hybrid-footage`**: phone references, grey-box and render-to-real prompts (handbook 11).
- **`/film-studio:take-doctor`**: sends shots failing on CAMERA or ACTION back up the planning stack instead of re-rolling.

```
film boards                                    # printable storyboard.html
film animatic --audio 05_sound/temp/temp_mix.wav    # timed animatic in 03_board/
film gen S04 --via ark --model <seedance-2.5 id> --prompt-file 04_shots/S04/prompt_v1.md \
  --image 04_shots/S04/start_frame.png --draft --duration 5 --count 2
film gen S07 --via fal --model <render-to-real endpoint id> --prompt-file 04_shots/S07/prompt_v1.md \
  --image 04_shots/S07/keyframe_f1.png --param video_url=<playblast url> --dry-run
film frames 04_shots/S01/takes/<take file>.mp4 --every 0.5
film cost
```

Field names differ between fal endpoints: check the model page and `--dry-run` before you spend.

## Drills

1. **Paper before pixels (15 min).** Write a 30-45 s scene as 6-10 shot-list rows with a purpose each. Delete any row whose purpose repeats another's. Run the rhythm check.
2. **Animatic cut-down (20 min).** Sketch a board per shot, record temp VO, run `film animatic --audio`. Cut at least one shot, re-run, and write one line on why the shorter version plays better.
3. **Phone camera reference (15 min).** Shoot three 6-second moves (push-in, lateral track, slow orbit). Write the "one job" line for each, test one at draft resolution and rate it with `film take rate`.
4. **Board audit (10 min).** Generate a production board or 3x3 grid for a short scene, audit it against your scene list, and count the errors you would otherwise have paid to find.
