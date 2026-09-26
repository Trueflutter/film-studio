# 05 · Continuity: characters, worlds, light and story

A film is dozens of separate generations that must look like one camera, one cast and one world. Models make this hard: every generation starts from nothing. Continuity is a system of images, fixed wording and checks that you set up once per production and reuse on every shot.

## The short version

1. **Understand the drift.** Each generation re-casts your character from a lossy description; fine details get refilled from the model's habits.
2. **Hold identity with images, not adjectives.** A reference pack plus a verbatim anchor line.
3. **Keep reference sheets boring:** neutral grey, flat light, real skin, no grade. The look belongs to the shot.
4. **Face master at 3/4; full-body views headless.** The model must take the face from the face image.
5. **Name every reference's job** and the leak you don't want.
6. **Never regenerate a whole image twice** to fix a detail. Edit the region, composite it back.
7. **Locations are plates** with named landmarks and one light logic.
8. **Track story continuity too:** who knows what, and when.

## Why models drift (plain version)

| What happens | Why | What it looks like |
|---|---|---|
| A new actor every time | each generation samples a new person from your description | faces "close but not him" |
| Coarse traits survive, fine ones don't | references are compressed; moles, jawlines, fabric patterns get refilled from training habits | younger, smoother, more symmetrical faces; generic wardrobe |
| Small faces are invented | a face that's 40 pixels tall in a wide has almost no information | wides show a stranger |
| Conflicting words average out | two slightly different descriptions blend | a face halfway between |
| Every full re-generation copies a copy | detail and character erode with each pass | after two passes, "plastic", symmetrical faces |
| Rooms are re-imagined | prose descriptions of a room produce a new room each time | furniture moves, windows swap walls |
| Light and grade wander | each shot re-decides the light | one scene in three colour temperatures |

Each technique below targets one of these.

## Character continuity

### The bible (two halves)

`film character "Name"` creates `02_design/characters/<name>/bible.md`:
- **Inside** (story): want, need, wound, contradiction, how they hide what they feel, voice, arc. This drives performance.
- **Outside** (identity lock): the **anchor line**, 35 words or fewer: age, build, face shape, skin tone and texture, hair, two or three unmistakable features, signature garment. Paste it verbatim into every prompt that includes the character. Never paraphrase it.

### The reference pack

| Image | Why | Notes |
|---|---|---|
| **Face, 3/4 view, neutral** | the master identity image | iterate this until it's right; everything else derives from it |
| Face front, face profile | angles the model will need | derived with an identity-preserving edit from the master |
| **Full body front and back, head cropped out or tiny** | wardrobe and build | models copy the face from whatever image shows one; keep the face out of the body views |
| Expression sheet (4-6) | only the expressions the script needs | derived from the master |
| One image per wardrobe state | costume changes | list garments by colour and material in the anchor line too |
| (optional) turnaround | many angles that match | burst frames or a grid |

**Keep sheets boring.** Neutral grey background, flat even light, real skin texture, no grain, no cinematic grade, no dramatic lens. A dramatic reference locks its look into every shot that uses it (reported, *Hell Grind* pipeline, 2026).

### Making the pack

1. Generate the master face with your best still engine: describe surface and wear, never "beautiful".
2. Derive the other views with an identity-preserving edit model (handbook 16 lists current options), always from the master, never from a derivative.
3. Check each view against the master side by side. Fix drift by editing the region (eyes, jaw, hairline), then compositing it back onto the image. Don't regenerate the whole image again.
4. Mark approved images in the bible; move rejects to `refs/_rejected/` with a reason.

### Turnarounds

- **Grid method:** one generation of a 3x3 sheet of the same character from several angles shares face, light and set across panels. Panels are small (about 680 px at 2K), so isolate and upscale the ones you use.
- **Burst frames:** one video pass where only the camera orbits a still character (12-15 s), then harvest about 20 frames with `film frames --every 0.6`. Because the frames come from one physically continuous render, they match (studio-tested).

### Identity in video

- Give the video model the master face (and body/wardrobe views if it takes several references) with explicit jobs: _"@image2 identity only: same face, same bone structure; don't copy background or light."_
- Faces hold best at medium close-up and close-up. In wides, carry identity with silhouette, hair and wardrobe, or avoid showing the face.
- In native multishot, put the face in the first cuts; make the last cut an insert, a wide or an over-the-shoulder.
- Short chains only (2-3 generations), then re-anchor on the original references.

### Trained identity (LoRA, Soul ID and similar): when it's worth it

Default to a disciplined reference pack. Train an identity only when:
- a recurring character appears in hundreds of images or across many productions;
- the design is unusual and models keep "normalising" it;
- you work in an open-weights pipeline where training is cheap.
Our own results were mixed: a trained identity won on identity lock in one engine and lost on wardrobe and texture to a strong image-edit workflow (studio-tested, 2026).

## World continuity

### Location plates

For each location, in `02_design/locations/`:
- a **3/4-view wide of the empty set**, landscape (it gives the model room to reframe), no people;
- **one anchor object** that is always visible and proves it's the same place;
- **one light logic** in a sentence ("warm window light from screen right, practical lamp behind the sofa");
- a **reverse angle**: generate an empty-set walk-through video and pull the reverse from it, or edit the plate into a reverse;
- a **paste-able lock line** naming landmarks by screen side from the master angle.

Never describe a room in fresh prose per shot; each description is a new room.

### Props with continuity weight

Track state changes (full → empty glass, clean → broken, open → closed) in `continuity.md`. A prop that changes state in the middle of a scene is a classic tell.

### Optional: 3D worlds

For productions that return to a location many times, a 3D representation (splats, meshes or panoramas from world-model tools) lets you move a virtual camera for plates and reverses. Useful, not required (handbook 16).

## Light and colour continuity

- One key-light side per scene, written in `continuity.md`, stated in every prompt.
- One colour temperature per time of day; practicals named.
- State white balance when an engine drifts ("warm white balance, 4500K"; some engines default cool).
- Final match happens in the grade: one look over everything (handbook 09).

## Screen continuity

- **180° rule and screen sides** stated in every prompt of a scene.
- **Eyelines match** across singles: if Maya looks frame right at Sami, Sami looks frame left at Maya.
- **Screen direction** carries across cuts: exits right, enters left.
- **Fresh start frame for every new angle**, built from references and the plate.

## Product continuity (ads)

- References from several angles plus material and hardware details, each with a job.
- Real labels, logos, UI and text are **composited in post**, never generated; generated text scrambles.
- One hero angle and one light setup for the product across the spot.

## Story continuity: the knowledge ledger

Visual continuity is half of it. The other half is what the audience and the characters know, and when. `03_board/continuity.md` has a ledger per scene: what the audience learns, who knows it on screen, who doesn't, setups planted, payoffs delivered, and open setups not yet paid off. Claude checks each new scene against it before you write or generate. (The idea comes from "narrative world model" research for long serials; it's just as useful for a 60-second film with one reveal.)

## The continuity check (every scene)

1. `film contact --shot S0X` for each shot, plus the reference master, side by side.
2. Face · age · skin · hair · wardrobe · props · light side · screen side · room landmarks.
3. Log failures as IDENTITY, REF or FRAME. Fix the cheapest way: cut around, region-edit, new start frame from references, then regenerate.

## In the studio

- `bible-builder` skill: bibles, anchor lines, reference-pack prompts, location plates, the audit.
- `film character "Name"` · `film contact` · `film frames --every 0.6` (burst harvest) · `03_board/continuity.md`.
- `prompt-director` pastes anchor and lock lines verbatim into every prompt.

## Drills

1. **Drift demo (15 min).** Generate a character three times from prose only, then three times from a reference pack. Contact-sheet both sets.
2. **Headless body (10 min).** Make a full-body wardrobe reference with the head cropped out; use it with the face master in one shot.
3. **Plate and reverse (20 min).** One location plate and its reverse angle; write the lock line.
4. **Ledger (10 min).** Fill the knowledge ledger for your capstone. Find one setup without a payoff, or a payoff without a setup.
