---
name: seedance-directing
description: Use when writing a Seedance 2.5 video prompt (or any reference-driven video model) for a shot with people, a face, acting, dialogue, an action beat or several cuts in one generation; when clips feel "AI", lifeless, stiff, mugging, floaty, glossy or evenly paced; when a take is right except for one element; when the final lost what the draft had; or when building a scene from several angles. The PJ Ace / Chris Capel "Nexus" method, adapted to our routes.
---

# Seedance directing: direct it, don't roll the dice

Lifelike AI video is directed, not generated. Every gap a prompt leaves is filled with the model's average, and the average is what audiences now read as "AI": a symmetrical face, front-on, blank or mugging, moving at one speed under a camera that glides. This skill fills the gaps with physical decisions and keeps every good result while you fix the next problem.

Source: the Nexus process (PJ Ace and Dan Weller, director Chris Capel; Dreamina Seedance 2.5, Omni reference, October 2026). PJ Ace published the full process, with three real production prompts, in an X thread on 30 October 2026. Read those prompts for density and tone; copy their discipline, never their content.

## The rule

Three wins, never in the same pass:

1. **Composition** (the frame): where everything sits, the lens, the light. Lock it as an image.
2. **Staging and camera**: who moves where, how the camera moves. Lock it as harvested frames or a video reference.
3. **Performance**: the face and the body. Iterate it last, on locked frames, one change at a time.

Keep what works. Regenerate only what doesn't.

## What to do when

| Situation | Do this |
|---|---|
| a scene with dialogue or several angles | coverage pass, harvest, then per-shot performance passes (section 2) |
| a hero shot with a face | start frame (blank face if it is a staging frame) + face reference, then performance passes |
| the take is right except one element | paint-out repair (section 4) |
| a camera move or staging the model won't follow | graybox or phone blockout as a video reference (section 4) |
| the final lost what the draft had | harvest the approved draft's frames as start frames for the final (section 2) |
| non-identity B-roll, establishing | native text-to-video, one roll; the anatomy still applies, shorter |
| stills, start frames, character packs | `image-prompt` (the person, the pack, the place) |

## 1. Before any video

- **A script with a performance target per character.** Their archetype, or the kind of comic or dramatic energy they bring, written for you, the prompt writer. Translate it into physical behaviour in every prompt. Never put a real actor's name in a generation prompt.
- **An asset kit per character.** A front, side and back turnaround on a neutral background (face blanked or tiny on the body views), a separate face close-up, and a short voice clip if they speak. Optional: a six-panel grid of angles to fit many views into one reference slot.
- **A reference budget per route.** Dreamina caps a generation at 12 files; EvoLink reference-to-video is reliable with 1-8 images; check `list_capabilities` on Aristotto. Merge angles into grids and drop the least useful reference before you drop a role line.

## 2. The coverage pass (dialogue and multi-angle scenes)

1. Write one long prompt (20-30 s) for the whole scene with every angle in shot order: wide, over-the-shoulder, singles, close-ups, inserts.
2. Run it at draft resolution. Judge only whether the angles and the order are right. Ignore performance at this stage.
3. When a run has the coverage, cut it apart: one clean frame per shot (`film frames <take> --at t1,t2,...`), each upscaled.
4. Generate each shot from its own frame, short (2-5 s), until the acting lands. The frame fixes the angle and the framing, so every retry works on one problem: performance.

Shots from one coverage pass share light, wardrobe and set, so they cut as one scene, and short generations hold a performance better than long ones.

**Draft to final on routes without a seed or a linked draft** (Aristotto, EvoLink): the final is a new roll, so it can lose the approved draft's composition. Harvest the draft's frames at each cut and give them to the final as start frames or composition references with that role stated.

## 3. The prompt

Write every shot or sequence in the block anatomy: `references/prompt-anatomy.md`. A full original example: `references/worked-example.md`.

**Length follows the number of decisions.** A single 4-5 s shot: up to about 500 words. A 6-10 s sequence of 3-5 shots: 800-1,000 words. Every sentence is a physical decision; no quality words anywhere ("cinematic", "stunning", "8k", "masterpiece", "hyper-realistic"). **Aristotto caps a Seedance prompt at 6,000 characters** (about 1,000 words); stay under it. If a route truncates or rejects the prompt, cut in this order: repeated LOCK lines, then AUDIO detail, then the spatial-map prose. Never cut a shot's CAMERA, ACTION or TIMING.

### Writing rules

1. **Every reference gets a role and a never.** "Use it only for X. Never use it for composition, framing, camera angle, lens, pose, head turn or expression." For grids: the grid and its panel borders are never rendered.
2. **Placeholders are named as placeholders.** White paint-outs and gray blockout shapes are placeholder masks that are never rendered. Say it in the reference line and again in the GLOBAL LOCK.
3. **The camera has a body.** Name the rig, the operator and what disturbs them: a shoulder handheld that jolts and reframes but keeps the face readable; a dolly push that is a physical move, not a zoom; a tripod with a slow pan; an operator walking backward who is jostled. A cause beats an adjective: say why it shakes, not "shaky".
4. **Faces three-quarter by default.** THREE-QUARTER, never front-on, never a perfect profile, both eyes visible. Front-on only for a presenter or a deliberate look to lens.
5. **A lens per shot.** An OPTICS line with the focal-length look (24, 28, 35, 50, 85 mm, macro) and its depth of field. Adjacent shots differ.
6. **Performance: state, signs, region, time.** Name the state and its intensity, then its physical signs (brows, lids, eyes, nostrils, lips, jaw, neck, breath, shoulders, hands), then where it lives ("mostly in the eyes and brows"), then a time window for each change. Intensity is a choice: big when the scene is big, physically small when it is small. Write it positively: what the face does, not what it doesn't.
7. **Time every beat, with an end.** Inside a shot, windows of a few tenths of a second (`0-0.5s`, `0.5-1.1s`); each spoken word placed in time; each beat says when it finishes ("the exhale is finished by 2.6 s"). A beat with no end tends to get cut off. **Cuts go on whole seconds** (`SHOT 2 (0:02 to 0:04)`): in our A/B, whole-second cuts landed within about 0.2 s and sub-second ones up to 0.9 s off.
8. **Say the first and the last frame.** The first frame is already mid-action or already speaking. The shot ends either on a held look (dialogue: an edit tail) or mid-motion on the cut (action: a cut on action); say which. When a reference shows a pose, say whether it is where they start or where they end up.
9. **Perform the cut.** The next shot continues the motion or the emotion with no pause, and it is a plain cut to a new size, not a zoom.
10. **Uneven shot lengths; the payoff gets the most time** (for example 2, 1, 2, 3 s on whole seconds). Even lengths read as generated. The model holds lengths only roughly, so generate each shot a little long and set the final lengths in the edit.
11. **A spatial map when sides matter.** Split the frame into LEFT and RIGHT halves and say what lives where; spell out mirror logic (a character facing camera holds in their own right hand what appears on frame-left); say that it never swaps.
12. **Physics with scale and duration.** Exact real-world sizes, speeds, counts and frame counts for objects and effects.
13. **Audio per shot, and a complete music lock.** Each shot lists its diegetic sounds. When music goes on in post: NO MUSIC, with no score, soundtrack, background music, musical tones or beats of any kind, stated in OUTPUT and again in the GLOBAL LOCK.
14. **Capitals for the words models get wrong** (LEFT, RIGHT, HARD CUTS, THREE-QUARTER, NO MUSIC), sparingly.
15. **Positive first, then short locks.** Describe what you want in full; negatives live only in one-line LOCKs after it ("never front-on", "her mouth stays closed").
16. **Spell words normally.** Describe a long shout as held much longer than the others; never stretch the spelling.
17. **One word can flip a performance.** In the Nexus case the word "nod" made an officer read as knowing and sarcastic; a single flat movement of the head with a completely blank face got the laugh. When a performance reads wrong, change the verb before anything else.

## 4. Repair, don't re-roll

**Paint it out and let the model fill it back in** (the camera and composition are right, something inside is wrong):

1. Take the frame with the angle and composition you want, ideally from the generation itself, so light and lens already match.
2. In an image editor, paint the wrong elements flat white. Cover the whole area with a little overlap, not just the outline.
3. Attach it as the start frame and call it the start frame in the prompt.
4. Attach appearance references for what fills the gap, each for appearance only, never for composition.
5. Describe the new elements' direction, speed and behaviour physically (running from frame left to frame right across the foreground and out past the lens).
6. State that the white shapes are placeholder masks and are never rendered. Without that line, white blobs appear in the video.

**Blank-face staging frames.** In start frames and lineups used for composition, paint the faces as plain white ovals and say so; identity then comes only from the face reference. This stops a weak face in a staging frame from becoming the character.

**Graybox for staging and camera.** A quick 3D blockout (Blender or Maya), or a phone walk-through for simple moves: a tall box for a creature, small boxes for people, one flat colour per character. A still from the camera position is a composition reference; a render of the move is a video reference for camera and staging only, never appearance. Keep the move simple: a handheld push-in or a slow pull-back reads even in rough blockout.

**One change per iteration.** Edit the latest working version, change only what failed, save it as a new file named for the change (`prompt_v4_flat-head.md`), and keep a one-line log of what each version fixed.

## 5. Check before you send

- [ ] Every reference has a role and a never.
- [ ] Every shot has OPTICS, CAMERA, ACTION, TIMING, AUDIO and a LOCK.
- [ ] Every camera move has a rig, an operator and a cause.
- [ ] Faces three-quarter unless it is a presenter.
- [ ] Every performance beat has a state, its signs, a region and a window with an end.
- [ ] Cuts on whole seconds; shot lengths uneven and the payoff the longest (finished in the edit).
- [ ] Under the route's prompt cap (6,000 characters on Aristotto).
- [ ] Screen sides and hands are mapped where they matter.
- [ ] The music lock is stated twice if music goes on in post; each shot has its own diegetic sound.
- [ ] No quality adjectives, no generated text, logos or UI, no real person's name.
- [ ] One change from the last version, named in the file name.

## Routes (check your tool's live capabilities first)

- **Aristotto Seedance 2.5** (the course default): `reference-to-video` for character packs; `image-to-video` from a harvested or painted frame. Prompts up to 6,000 characters. No seed: anchor the final on harvested frames.
- **EvoLink Seedance 2.5** (fallback): the same rows; 1-8 reference images are reliable.
- **Dreamina, Omni reference** (the Nexus route): up to 12 files, 10 s per generation; a video slot can carry a voice clip used only for its sound.
- **Voice:** on routes with an audio slot, `@audio1` with the line padded to the clip length (`performance-voice`); where only video slots exist, a clip whose only job is its sound ("use only its sound, never any picture from it").

## The evidence

- **Nexus** (Dreamina, 720p): the method behind a series with 62 million views.
- **Our A/B** (31 October 2026, Seedance 2.5 text-to-video, the same scene and character, 5 takes): with the directed prompt the character was three-quarter or in profile, looking at what she reacted to, framed off-centre in motivated light, in 3 of 3 takes. With the short prompt she was front-on, centred, looking into the lens and ending in a presenter pose in 2 of 2, despite "she doesn't look at the camera". Sub-second cut times were not honoured (hence whole-second cuts), and wardrobe drifted with text alone in both arms (use reference images for clothes). The winning prompt and its result: `references/tested-example.md`.
