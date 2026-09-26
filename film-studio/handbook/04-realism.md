# 04 · Realism: the 12 levers

Audiences don't check pixels; they check physics, behaviour and attention. A shot reads as real when the light has a source, the camera behaves like a camera, bodies have weight, faces do what faces do, the space sounds like a space, and the edit never lets you stare at a weakness. None of that comes from one model or one magic word. It comes from twelve decisions you make on every shot.

## The short version

1. **Realism is the floor, not the product.** It earns belief; the idea and the direction earn attention. Contest judges in 2026 rewarded "storytelling and directorial intent over technical polish" (reported, Higgsfield contest, Mar 2026).
2. **Describe causes, not results.** Not "cinematic, realistic, beautiful": say where the light comes from, what lens, what the hands are doing.
3. **Restraint reads as real.** Default camera still, default performance small, default take short.
4. **Physics lives at contact points.** Feet, hands, cups, doors, cloth, water. Name them and add their sound.
5. **Behaviour, not emotion words.** Faces caricature adjectives; they believe tasks.
6. **Judge in motion, full screen, with sound.** Never on a still.
7. **Hide what's weak.** The edit, sound and one consistent finish carry as much realism as the generation.

## What breaks belief: the AI tells

| Tell | Avoid it at generation | Fix it in post |
|---|---|---|
| Waxy, poreless, symmetrical skin | describe surface and wear; no beauty words; boring references; don't regenerate faces twice | grain; least-creative upscaler; region-edit from the master |
| Dead or drifting eyes | give the eyes a target and a reason to move | cut on the blink; use a reaction elsewhere |
| Floating camera that drifts on its own | "locked-off"; every move has a cause | stabilise; crop; trim the drift |
| Everything in slow motion | name speed and weight; shorter clips | speed up 110-125%; cut earlier |
| Weightless bodies and objects | name contact and mass | foley at contact; cut on the impact |
| Flat, sourceless light | one motivated key with a direction and a colour | grade shadows darker; vignette |
| Over-saturated "AI grade" | name white balance; avoid tinting stock words | one grade over everything |
| Over-sharp, grainless detail | don't bake grain into start frames; keep it for post | one grain pass, slight softening, halation |
| Identity or wardrobe drift | reference pack with jobs; verbatim anchor line | cut away; region-edit |
| Morphing hands | give hands a task and a prop; keep them out of close-up | trim; insert; crop |
| Garbled text and screens | never ask for text | composite real text and UI |
| Ghost or frozen background people | fewer extras; "only [name] in frame" | crop; blur; cut |
| Failed contact (feet sliding, cups passing through tables) | simpler action, contact named | cut before the contact; cover with an insert |
| Last-second degradation | generate slightly long | use the best seconds |
| Every shot the same length | plan rhythm | vary lengths in the cut |
| Every shot a centred hero shot | compose with intent (thirds, depth, negative space, OTS) | reframe |
| Pristine, showroom sets | wear, clutter, history in the set | grade; grain; sound of use |
| Generic TTS voice, sterile audio | voice first; room tone; foley | rebuild the sound in layers |

## The 12 levers

### Picture

**1. Motivated light.** Every light has a source you could point to: a window, a lamp, a screen, the sun, a streetlight. Say where it is, what it's like and what it does to the face. _"Cold light from a phone screen below her face, warm hallway light spilling in from frame left behind her, the rest of the kitchen dark."_ Not: "moody lighting". One dominant source per shot is more believable than a lit studio.

**2. Honest lens.** Real cameras have real focal lengths, real heights and depth of field that matches them. Pick from a small lens kit (your style bible names three) and use them for what they do: wide lenses put people in places, 35-50mm feel like being in the room, 85mm and longer isolate faces and compress backgrounds. Keep the camera at a height a person could hold it. Match depth of field to the lens and light (a night interior is not deep focus at f/11).

**3. Restrained camera.** The default is still. Movement is a decision with a cause: we follow someone who moves, we push in because something is being realised, we drift because the character is unmoored. One move per shot. Unmotivated drift is the most common tell in AI video.

**4. Texture and wear.** Real surfaces have history: chipped paint, a mug ring on the desk, a creased collar, skin with pores, lines, a shaving nick, flushed cheeks. Describe the surface, not "realistic skin". Never use "beautiful", "stunning", "flawless": they trigger smoothing. Grain and halation go on once, in post, over everything (lever 12); baked-in grain on start frames made our videos soft (studio-tested).

**5. Weight and contact.** The eye believes mass at the moment of contact: the heel landing, the mug meeting the table, the coat pulling on the shoulder, water finding its level. Name physics explicitly (models don't infer it well): _"the glass is full and heavy; she sets it down carefully and a little spills."_ Then give the contact its sound. Fast, heavy actions beat slow, floaty ones; if a model makes everything slow, shorten the clip and speed it slightly in the edit.

**6. Behaviour over emotion.** People rarely show what they feel; they do things. Direct the task (folding a letter, not looking at the phone), where the eyes go, what's avoided, and one tell (a jaw that tightens, a thumb that rubs a ring). Understate: name the behaviour in plain words and stop. Dense technical facial coding caricatured emotion in our tests, and even plain cues can over-play once you watch them in motion (studio-tested), so judge performance in motion. Listening is performance: reactions sell scenes.

### Process

**7. Reference discipline.** What you feed the model shapes the realism it returns.
- **Boring references** for identity (neutral grey, flat light, real skin, no grade): the look belongs to the shot.
- **Every reference has a job** stated in the prompt ("identity only; do not copy its background, light or grade").
- **Native vs anchor.** A crisp generated still used as a start frame can import a synthetic look that the video model keeps. For shots where identity isn't critical (establishing, B-roll, one-off characters) generate natively (text-to-video) or harvest a start frame from a native generation ("stills from motion", `film frames`). For identity-locked shots, keep a strong image anchor and fight the look with texture and the finish (studio-tested, June 2026: native wins clearly against a weak anchor, roughly ties with a strong one).

**8. The right engine per shot.** Engines have personalities: some are better at faces, some at motion and physics, some at dialogue, some at product. Route per shot, and revisit monthly (handbook 16 has the dated matrix). Mixing engines is normal; lever 12 makes them match.

**9. Short takes, best seconds.** Generated clips are least stable at their head and tail and degrade late. Generate a little longer than you need, use the best 1-3 seconds, trim 0.1 s off every end. Start the action in progress; never open on stillness or on a turn toward camera.

### Finish

**10. Edit to hide and to breathe.** The cut decides what the audience has time to scrutinise. Cut on action, cut to reactions and inserts, keep weak shots short, and hold only what can bear it: the one honest moment. Vary shot lengths (uniform lengths read as generated). Never hard-cut two separate generations of the same subject at the same size and angle (handbook 09).

**11. The sound of the space.** Probably the biggest realism multiplier. Room tone under everything (digital silence sounds fake), an ambience that tells us where we are, foley at every contact point, voices that sit in the room's acoustics, music that knows when to stop. A picture with honest sound is forgiven a great deal (handbook 08).

**12. One finish.** One grade across every shot so different engines and days match; one grain and halation pass over everything; one upscale path, used only on locked clips and re-checked on faces. A consistent finish turns forty generations into one film.

## Realism in stylised work

"Realism" doesn't mean photographic. An animated or stylised film is believable when its world obeys its own rules consistently: the same light logic, the same material behaviour, the same character proportions, weight that feels right for that world. The levers still apply; only the target changes. Write the rules in your style bible and hold them.

## Weak vs strong

**Weak:** _"Hyper-realistic cinematic shot of a man in a café, emotional, beautiful lighting, 8k, film grain, shallow depth of field."_

**Strong:** _"Medium close-up, 50mm, eye level, locked-off. A man in his late fifties at a café window table, grey stubble, reading glasses pushed up on his forehead, a paper cup he hasn't touched. Overcast daylight from the window on his left side, the room behind him darker. He reads a folded letter, stops, and slowly folds it smaller. He doesn't look up. Street noise through the glass, a coffee machine hissing behind him."_

What changed: a named lens and height (2), a locked camera (3), a motivated source and a darker background (1), age and wear (4), a task and a tell instead of "emotional" (6), the sound of the space (11), no grain in the prompt (12: it goes on in post).

## In the studio

- `prompt-director` writes prompts through the levers; `take-doctor` maps a tell back to its lever.
- `film frames clip.mp4 --at 1.2` (stills from motion) · `film contact --shot S04` (compare takes) · `film qc` creative rubric (the Realism row).
- Style bible (`02_design/style.md`): the lens kit, the light rule, the tells you refuse.

## Drills

1. **Tell hunt (15 min).** Watch a popular AI clip twice. List every tell with a timecode and the lever that would have prevented it.
2. **One lever at a time (20 min).** Take a flat shot and improve it by changing only lever 1 (light), then only lever 3 (camera), then only lever 6 (behaviour). Which moved belief most?
3. **Sound test (10 min).** Play one of your shots muted, then with room tone and one foley hit. Note how much more you believe the second.
4. **Native vs anchor (20 min).** One B-roll shot both ways; judge in motion, full screen.
