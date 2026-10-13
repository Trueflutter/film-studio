# The method in detail

## Decide the picture before the texture

Write one sentence first: "A presenter looks up from her notes at the anchor desk, about to speak." Then decide distance, camera height, crop, the light source and the action. Texture cannot rescue a confused scene.

## Identity record vs shot record

- **Identity** (stays the same every time): age range, face shape, complexion, eyes, brows, hairline and hair texture, build, two or three distinguishing marks with their side.
- **Shot** (changes): clothes, place, expression, pose, light, crop.

Keeping them separate is what lets you change the outfit or the room later without changing the person. For a real person's photo, don't describe the face at all: say what to preserve and what to change.

## Causes and visible effects

Describe what the viewer can check, not adjectives:

| Vague | Specific |
|---|---|
| cinematic lighting | large window to camera left; the far cheek falls gently darker |
| detailed fabric | the lapels have real thickness and a soft roll; silk creases where the arms come forward |
| natural pose | forearms on the desk, hands loosely together on a single printed page |
| shallow depth of field | both eyes sharp; the room behind softens gradually but still reads as a room |
| realistic skin | subtle pores on nose and cheeks, slight sheen on the forehead, small tonal variation under the eyes |

## Match detail to distance

- **Close portrait:** pores, fine hairs, sheen, catchlights.
- **Waist-up:** expression, hands, fabric folds; skin texture "subtle at this distance".
- **Full body:** proportions, weight on one leg, shoes meeting the ground, clothes hanging with gravity. Don't ask for pores.

## Camera and light

- Perspective comes from distance. "A comfortable portrait distance" or "the look of an 85 mm lens" avoids wide-angle noses. Phones: "an arm's length away, moderately wide, small difference in scale between the near hand and the face".
- One dominant light. A practical lamp can be visible but "too dim to cast a second shadow on her face".
- Grain, flare and motion blur are optional, not proof of realism. Real photos can be clean.

## Priority

Picture, person, moment first. Then camera and light. Then texture. Then one exclusion line. If two wishes compete (a full-body shot and a face filling the frame), pick one.

## Worked example (Saqr Insights presenter, tested 13 Oct 2026)

The old prompt said "A real photograph, not a render, not an AI portrait" and listed features. The new one below gave visibly more natural skin at 2K on Sunburst, and the model added a clip-on microphone on its own because the scene was described as a real broadcast. It put the beauty mark on the wrong side, and it gave her polished on-air makeup despite "light, everyday makeup". The makeup turned out to be right: a repair that removed it made her look less believable, because no presenter goes on air without makeup. Realism means right for the situation, not "less".

```text
Create a believable still frame from a premium evening news broadcast: a fictional Arab woman presenter, about 32, at the anchor desk, framed from mid-chest up in a vertical picture with a little headroom.

She has warm olive skin, an oval face with defined cheekbones, deep-brown eyes and thick dark eyebrows, the left brow resting fractionally higher than the right. A small beauty mark sits under her left eye and faint freckles cross the bridge of her nose. Her long dark-brown hair falls in soft natural waves and is tucked behind her right ear; a few fine strands lift away near the parting. Her smile is slightly fuller on one side. Keep these small differences: she should look like one particular person, not a symmetrical model's face. Professional on-air broadcast makeup, natural and well blended.

She wears a fitted camel wool blazer over a cream silk top and a thin gold chain. The lapels have real thickness and a soft roll; the silk catches one narrow highlight where it drapes at the neckline and creases slightly where her arms come forward.

She has just looked up from her notes and is about to speak: lips relaxed and slightly parted, the beginning of a warm smile, eyes on the camera lens. Her forearms rest on a dark matte desk, hands loosely together on a single printed page, mostly below the crop.

The camera is at her eye level, a comfortable presenting distance away, with the natural, unexaggerated perspective of an 85 mm full-frame-equivalent lens. Both eyes are sharp. The newsroom behind her softens gradually but still reads as a real place several metres back: a glass partition with one colleague at a desk screen, a dark wall screen glowing soft blue-grey with nothing written on it, and the lights of a modern city at night through tall windows, no famous landmarks.

A large soft key light sits to camera left, slightly above her eye line, so the right side of her face falls gently darker, with soft shadow under the jaw. A warm practical lamp behind her on the right puts a thin rim of light on her hair and shoulder without lighting her face. The key leaves a soft window-shaped catchlight in her eyes.

At this distance her skin shows fine, localized texture: subtle pores on the nose and cheeks, a slight natural sheen on the forehead and the tip of the nose, small tonal variations around the mouth and under the eyes. Realistic highlight roll-off, true blacks in the desk, neutral broadcast colour.

No skin smoothing, glamour retouching or glossy finish. No on-screen text, captions or logos.
```

Lessons from the test: say the orientation in the prompt (the old prompt came back landscape on ChatGPT); describe makeup as the role would wear it ("professional on-air broadcast makeup, natural and well blended" for a presenter; "barely any" for a phone selfie) rather than "light"; name the side of a mark from her point of view **and** the picture's ("her left eye, the eye on the right side of the picture").

## Checking a result (0, 1 or 2 each)

1. Identity and expression: an individual face, natural gaze, matches the approved master.
2. Skin and hair: varied, scale-appropriate; not waxy, not etched.
3. Anatomy and action: hands, joints, grip, weight, contact.
4. Light and materials: one direction, shadows agree, skin vs fabric vs glass look different.
5. Camera and space: believable viewpoint, focus fall-off, background scale.
6. Usefulness: right crop, room for graphics, no stray text or logos.

A serious face or hand failure rejects the image whatever the total.
