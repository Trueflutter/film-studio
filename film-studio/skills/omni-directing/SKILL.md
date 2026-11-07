---
name: omni-directing
description: Use for any video generation with people, a scene or a product - the default video model is Gemini Omni (1.2 Flash). Covers casting a person in motion (screen test), writing Omni prompts (references in plain words, timecodes, sound), growing a scene with extend while keeping the person and screen direction, editing a take instead of re-rolling it, upscaling, and when to fall back to Seedance 2.5. Trigger on "make a video", "a shot of", "screen test", "cast", "continue this clip", "make it longer", "extend", "fix this take", "change the background of this video", or any request that would otherwise go to seedance-directing.
---

# Omni directing: the default video model

**Gemini Omni 1.2 Flash** (Google, generally available 5 November 2026) is the studio's default video model. In the director's tests its faces read more natural than stills or Seedance, it costs about a fifth of Seedance per second, and its **extend** continues a clip with the same person and no reference photo. Seedance 2.5 stays as the fallback (end of this skill).

## Routes and models

| Job | EvoLink model (`film gen --via evolink --model ...`) | Notes |
|---|---|---|
| Cast a person, or a shot from words | `gemini-omni-1.2-flash-text-to-video` | 3-15 s |
| Animate a start frame (place, product, a still the director approved) | `gemini-omni-1.2-flash-image-to-video` | 1 image (3-15 s) or first + last frame (3-10 s) |
| A known person or product in a new place | `gemini-omni-1.2-flash-reference-to-video` | up to 10 images (Google advises 6 or fewer), up to 3 reference videos |
| Continue a clip | `gemini-omni-1.2-flash-video-extend` | `--video-ref <take id>`, adds 3-10 s to a clip of up to 30 s |
| Change one thing in a take | `gemini-omni-1.2-flash-video-edit` | clip up to 15 s, keeps its length and shape |
| Sharpen a 720p take | `gemini-omni-1.2-flash-video-upscale` | to 1080p or 4k, no prompt |

On **Aristotto**, take the newest Omni it lists (`list_capabilities`, modality video): Gemini Omni Flash 1.2 once listed, 1.1 until then (Google moves 1.1 requests to 1.2 on 3 December 2026). Read the operation's input fields there before quoting; extend and edit are its video-to-video task.

**Cost (EvoLink, billed by tokens):** about $0.07 a second at 720p, $0.10 at 1080p, $0.20 at 4k, plus a few cents of input per job. A 5 s 720p shot is about $0.34; a 5 s extend about $0.34 (only the new seconds are billed as video). `film gen` costs it from `rates.json`.

**Sound is always on.** There is no audio switch: name the sound you want and write "Do not add music" or "No dialogue" when you don't want them.

**Resolution:** ask for 720p. In our tests a 1080p request came back as 720x1280; use the upscale route for a sharper final, and judge faces at 720p.

## How Omni wants to be prompted (Google's guide, and our tests)

Omni reads plain, detailed prose. It is not Seedance: do not paste a Seedance block prompt into it.

1. **Open with what it is:** "Realistic footage, like a scene from a quiet, grounded film. Vertical 9:16, six seconds."
2. **Say what each reference image is for, in plain words, in the order you send them.** No `@image1` or `<IMAGE_REF_0>` tags (Google calls those deprecated). "The two reference images show the agent: use them only for her face, hair and clothes. Do not copy their grey wall, flat light, framing or pose."
3. **The story in one or two sentences, then the place:** where things are in frame, who stays on which side.
4. **The camera:** who is holding it and how it moves ("handheld on the shoulder of an unseen operator, a small breathing sway, never a smooth glide"). Faces three-quarter; nobody looks at the camera unless they are presenting.
5. **Shots with timecodes:** `[0-2s] ... [2-3s] ... [3-6s] ...`. Omni cuts between shots on its own when it thinks it should: for one take, say "in a single continuous shot, no cuts".
6. **Light as a time of day and its sources:** "dusk: deep blue window, warm amber lamps, the edges of the room falling into shadow". Light still makes it a film.
7. **Sound last:** what we hear, the exact words if anyone speaks, then the negatives: "Do not add music. No other dialogue. No subtitles, no on-screen text, no logos."
8. **Don't re-describe what a reference already shows.** Spend the words on action, place, light and sound.
9. English only; negatives inside the prompt ("Do not..."), there is no negative-prompt field.

Keep the directing craft from `seedance-directing` (the feeling and its physical signs, a target for the eyes, motivated light, one change per take): it carries over. What changes is the format above.

## Cast in motion (the screen test)

Cast every person in video, never from a generated still: frames from video read as filmed. The director's verdict on Omni's first screen test: "the realism of the face is phenomenal".

- `film gen ST01 --via evolink --model gemini-omni-1.2-flash-text-to-video --prompt-file <screen test> --duration 5 --res 720p --aspect 9:16`
- The screen test: a close-up, the face in the upper half, a plain wall and soft window light, wardrobe A in the words, a slow head turn from three-quarter, to the lens, to three-quarter the other way, holding about a second at each position. Cast them attractive and real, the way `image-prompt` describes people: one particular person, quiet imperfection, never a model's symmetrical face and never scarred or worn down.
- Roll two or three, pick one, and keep the take: it is the person's master. Cut a face pack from the holds with `film frames` (see `bible-builder`) only for scenes that jump to a new place.

## Grow the scene with extend

Extend continues a clip: the same person, clothes and light, with no reference photo. The director called the first one "seamless".

- `film gen S01 --via evolink --model gemini-omni-1.2-flash-video-extend --video-ref <take id> --duration 5 --res 720p --prompt-file <next beat>`. The output is the whole clip plus the new seconds.
- **Start every extend prompt with where the clip ends, and continue that exact direction:** which way the head is turned, which way the body faces and moves, where in the frame. "She has just turned her head to her right, toward the window on the right of frame. She keeps turning right and walks toward the window." In our first extend the clip ended on a turn to the right and the continuation began with a turn to the left: the director caught it at once.
- Keep extend prompts short: "Continue the scene in a single continuous shot. ... Keep everything else the same."
- Omni reads only the **last 10 seconds**. If a person or object appeared earlier, name them again in the prompt or pass their face frames as reference images.
- Extend only adds to the end. A new place, a new day or a cutaway is a new generation: reference-to-video with the face pack from the screen test.
- Chain extends up to the 30 s input limit, then start a new shot.

## Fix a take instead of re-rolling it

`gemini-omni-1.2-flash-video-edit` with `--video-ref <take id>`: one short instruction and "Keep everything else the same." ("Remove the coffee cup from the table. Keep everything else the same.") Long edit prompts change things you didn't ask for. Speech can't be edited.

## When to fall back to Seedance 2.5 (`seedance-directing`)

Switch for the step, and say so in one line, when:
- Omni answers "service busy" twice in a row (it happened on launch day);
- the shot must be longer than 15 s in one generation (Seedance goes to 30 s);
- the director needs native 1080p rather than an upscale;
- a scene needs audio references (a voice to lip-sync); Omni takes no audio input.

Write the Seedance version with `seedance-directing`'s block format: the two models want different prompts.
