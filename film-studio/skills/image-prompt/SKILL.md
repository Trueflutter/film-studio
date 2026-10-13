---
name: image-prompt
description: Use when the user wants a realistic image of a person, character, presenter, product shot, location or start frame for a video; asks for a portrait, headshot, character, "make an image", "a still", a thumbnail or a keyframe; wants to fix an image that looks AI, waxy, glossy or fake; or wants a character kept the same across scenes or outfits. Also when they ask to connect or set up ChatGPT image generation.
---

# Image prompt: believable pictures with GPT Image 2.5

Real-looking people come from a **coherent photographic situation and specific visible details**, not from words like "8K", "ultra-realistic" or "not AI". Your job: turn the user's few lines into one strong prompt, make a small batch, show it on **one board**, and repair the chosen picture one problem at a time.

## 1. Compile the prompt (don't ask, decide)

Ask at most one question, and only if the answer changes the picture (e.g. "vertical for a reel or horizontal for YouTube?"). Otherwise choose sensible defaults and say them in one line.

Write the prompt as natural prose in this order (details in `reference/method.md`):

1. **The picture:** what it is ("a still frame from a premium evening news broadcast"), the crop and orientation **in words** ("framed from mid-chest up, vertical, a little headroom"). The image tool does not always obey a separate size setting; the words do.
2. **The person:** a fictional adult, a few stable traits, grooming and makeup **as their role would really have it** (a presenter on air is made up; realism is "right for the situation", not "plain"), and **two or three small asymmetries** (one brow higher, smile fuller on one side, a mark on a named side). Add: "one particular person, not a symmetrical model's face."
3. **The moment:** one action, the expression and where the eyes go ("has just looked up from her notes, about to speak, eyes on the lens"). Hands touch something specific.
4. **The place:** only the props the story needs; the background softens but "still reads as a real place".
5. **The camera:** height, distance and perspective ("eye level, a comfortable distance, the unexaggerated look of an 85 mm lens"); what is sharp.
6. **The light:** one dominant source and its **visible effects** ("key to camera left, the right side of her face falls gently darker, soft shadow under the jaw, a window-shaped catchlight").
7. **Texture matched to distance:** a close portrait shows pores and sheen; a full-body shot shows fabric and ground contact instead.
8. **One short exclusion line:** "No skin smoothing, glamour retouching or glossy finish. No text or logos."

Never write: "not a render", "not AI", "8K", "masterpiece", "hyper-realistic", "flawless", "beautiful", camera brands, seeds or settings in the prose.

Save the prompt to `<project>/images/<subject>/prompt.txt`.

## 2. Make a batch, show one board

**Route A: ChatGPT (default for exploring).** Free on the user's ChatGPT plan, about 1024×1536, 1 to 2 minutes for 4 images in parallel:

```bash
python3 <skill>/scripts/images.py gen <project>/images/<subject>/prompt.txt <project>/images/<subject> --count 4 --shape portrait --title "<subject>"
```

It opens `board.html` with all four. If `check` fails, run the setup in `reference/setup-chatgpt.md`.

**Route B: Aristotto (the master for video).** When the picture will be animated or shown large: `gpt-image-2.5`, variant `sunburst`, 2K, 4 outputs in ONE quote, same prompt. Download the outputs into the same folder and run `images.py board <folder>`. Never show four separate result cards.

Then ask one thing: "Which number?"

## 3. Repair, one problem at a time

Look at the chosen picture yourself at full size first (face, hands, light direction, text, makeup). Fix the **highest-impact** problem with an **edit of that picture**, not a new prompt: say what must stay, then the one or two things that change. Recipes in `reference/repairs.md`. Compare every edit to the approved original, not to the last edit. If edits keep degrading it, go back to the original and simplify.

## 4. The person's reference pack (right after the pick)

Video models keep a face only as well as their references show it. As soon as the user picks a person, make the pack as **edits of the approved picture** (same face, hair, outfit, light), in ONE batch and ONE board:

1. **Face close-up:** head and shoulders filling the frame, eyes sharp. This is the one that keeps the face in video.
2. **Mid shot:** waist up, hands visible.
3. **Full body:** head to shoes, standing, the whole outfit.
4. **Three-quarter** and 5. **side** views, so clips don't all open on the same front shot.

Save to `<subject>/pack/` and write `<subject>.md`: the identity record (stable traits the pictures actually show), the wardrobe record, each file with its job or media id. Every video clip of this person gets the close-up plus the pack shot nearest its framing as references. New outfits or places later are edits of the approved master ("keep this exact woman... change only her outfit to..."), never a re-description; then redo the pack.

## 5. The place, from several angles

Make the location once, then the **same space** from 3 or 4 camera positions (wide establishing, reverse angle, a side or low angle, a detail), as edits of the approved wide: "Keep this exact room: same furniture, materials, windows, light and time of day. Show it from [position]." Empty of people unless the shot needs them; the person goes in at the video step.

**No landmark clichés.** Don't name the city in an image prompt: say "Dubai" and the model plants the Burj Khalifa in the window. Describe what's really there instead ("a Gulf city at dusk: low-rise villas, palms, a few glass towers in the distance, no recognisable landmarks"), and add "no famous landmarks" when there's a skyline.

## Rules

- Newest model only: GPT Image 2.5 (Sunburst for masters, ChatGPT/Flare for exploring).
- Fictional adults unless the user owns the rights to the face. Never present a synthetic person as a real customer or witness.
- Never generate text, logos or UI that must be right; add them later in code.
- The user signs in to ChatGPT themselves. Never ask for, read or print a password, token or key.
