# 18 · Short-form, series and volume

Most of what you make will be watched on a phone, with the sound off, by someone whose thumb is already moving. This chapter turns the craft of the other chapters into content: reels and TikToks that stop the scroll, formats a brand can use, series people come back to, and a way of working that makes several good pieces a week without the quality dropping.

## The short version

1. **The first second decides.** Open on the most interesting image you have, already in motion. No logo, no fade-in, no warm-up.
2. **Design for sound off, then reward sound on.** The picture and the text carry the idea; the sound makes it land.
3. **Short-form pacing is not "cut faster".** Change something every one or two seconds while you earn attention, then hold the moment that matters.
4. **Text and captions are designed, not added.** Built in code, placed in the safe zone, on screen long enough to read twice.
5. **A series is a format, not a pile of episodes.** Write the format bible and ten episode titles before you make episode one.
6. **One idea, many formats.** Plan the reel, the cutdown and the second aspect at shot design, and give each version its own hook.
7. **Speed comes from reuse and batching, never from skipping the ladder.** Characters, looks, graphics and sound are built once and reused (`film new --from`).
8. **Nothing ships below the floor.** Every piece gets `film review`, `film qc` and the phone test, however fast it was made.

## Cinematic on a phone screen

Everything in chapters 03 and 04 still applies. Vertical changes the frame, not the craft:
- **Faces are bigger.** Mediums and close-ups carry vertical; a wide shows a small figure in a tall frame, so use it to show place, briefly.
- **Depth runs top to bottom.** Foreground at the bottom of the frame, the subject in the middle third, the world above. A doorway, a staircase or a street pulls the eye through the frame.
- **Movement is vertical too.** A tilt, a rise or someone walking towards the lens works in 9:16; a wide pan mostly shows you the edges of a narrow frame.
- **Keep the subject in the centre third.** The top 15%, the bottom 20% and the right edge belong to the platform's buttons and captions (handbook 14).
- **Generate vertical for vertical.** A 9:16 crop of a 16:9 frame keeps less than a third of the width. When 9:16 is the main shape, generate it natively and derive the 16:9, not the other way round.

## The first second

The viewer decides in the first second whether to watch the second one. The first frame must read at thumbnail size, and something must already be happening.

Openings that work:
- **Mid-action.** The cup is already falling; the door is already opening.
- **The result first.** Show the finished dish, the finished room, the transformed shot; the video explains how.
- **A contradiction.** Something that shouldn't be there: a camel in a lift, snow on a Dubai street, a CEO answering the support line.
- **A face with a question.** Someone reacting to something we can't see yet.
- **The stakes in words.** One line of on-screen text that names the problem ("Your first week in a new job"), over a picture that shows it.

Openings that lose people: a logo, a slow fade from black, an establishing wide with nothing happening, a title card, "Hi everyone".

**Check it:** `film frames <file> --at 0,0.5,1 --width 360` shows you the first second at phone size. If the first frame alone doesn't make you curious, change the opening shot, not the caption.

## Pacing for short-form

- **Earn attention, then spend it.** In the first three seconds, change something every second or two: a cut, a move, a text beat, a sound. Once the viewer is in, hold the moment that matters (handbook 09: rhythm is bimodal).
- **Uniform lengths are still an AI tell.** `film review` prints the rhythm of the cut and warns when every shot is the same length.
- **End on a button.** A final beat that pays off the hook: the reveal, the punchline, the result. Then stop. Reels that end a beat late lose the rewatch.
- **Loops are a choice.** If the last frame leads naturally into the first, the viewer often watches twice before noticing. Plan it at shot design; don't force it at the edit.
- **Cut on the music** when there is music: the biggest change on a downbeat (`film review --bpm`; handbook 08).

## On-screen text and captions

On-screen text (a hook line, a step number, a label) and captions (the spoken words) do different jobs, and both are part of the design.

- **Build text in code** with the `graphics` skill, never in the generated picture (handbook 09).
- **One idea per text beat,** short enough to read at a glance, on screen long enough to read twice.
- **Give them separate homes.** Captions sit in the lower middle, above the bottom 20%; hook text and labels sit in the upper third, below the top 15%. Never let the two collide.
- **Captions are the voice when the sound is off.** Use the house style from the `captions` skill (bold, soft stroke, spoken-word highlight). Author the lines, check them, then burn them in per shape (handbook 14).
- **The text stays off the master.** Graphics go on per delivered shape with `film overlay`, then captions go on top (handbook 14).

## Formats a brand can use

### Scenario videos

A short, performed moment that puts the audience in a situation they recognise: a customer's problem, a workplace moment, a before and after. They carry training, onboarding, product benefits and brand values without anyone presenting.

- **Shape:** the situation → the moment it goes wrong, or the tension → the turn (what changes it, often the product or the right behaviour) → the result.
- **"Wrong way, right way"** is a strong training form: the same scene twice, one choice different.
- **Craft:** it's a dialogue scene (handbook 07). Voice first, behaviour over emotion, lines under the budget of about 2.5 words a second, a reaction shot for every line that matters.
- **Recurring cast.** The same two or three characters across a set of scenarios turns a one-off into a series (below).

### Tutorials without a presenter

A tutorial teaches one outcome in a few steps. You don't need a face on camera.

- **Show the result first,** then the steps. Five steps at most; one step per beat, numbered on screen.
- **Real screens, real products.** Record the real screen (the computer's built-in screen recorder is enough) or film the real product; never generate a product screen or a label. Callouts, highlights and step numbers are built in code with the `graphics` skill over the recording.
- **The voice carries it.** A voiceover (ElevenLabs or your own voice, recorded close to the microphone) with generated or filmed B-roll between the steps.
- **End on the result again** and one next step (the CTA).

### Cornerstone brand video

The longer hero piece (45-90 seconds) that says who a brand is, and the source of many shorter pieces. Make it with the full method (story, bibles, boards, performance, sound, one finish), and plan its cutdowns in the shot list from day one.

### Product video

- **The product is real.** Film it (a phone on a steady surface, clean light) or use the client's photography, and generate the world around it (handbook 11). Labels, logos and packaging are never generated: composite the real ones.
- **Hero shots** show the product doing its job or being used, not rotating on a plinth.
- **A short product ad** is one audience, one insight, one proposition, with the product as the hero of the turn (handbook 01).

## Series and recurring formats

People follow series. A series is a promise that the next episode will give them the same kind of pleasure, so the format matters more than any one episode.

Write the format bible in `00_brief/format.md` before episode one:
1. **The promise** in one line: what every episode gives the viewer.
2. **The recurring character or characters,** with their want and one tell (their bible and reference pack in `02_design/`).
3. **The episode engine:** the shape every episode follows, for example "Noor tries one shortcut at work; it half works; the button".
4. **Fixed runtime and shape** (for example 20-30 seconds, 9:16).
5. **The signature:** a recurring visual or sound (a sting, a framing, a text style) the audience learns to recognise. It never delays the hook: the hook comes first.
6. **The end button** and how an episode points to the next.
7. **Ten episode titles.** If you can't write ten, the engine doesn't work yet. Fix it before you spend anything.

**Make episode one fully,** with the whole method. Then every later episode starts from it:

```
film new "Desk Diaries Ep 2" --from desk-diaries
```

`--from` copies the brief (and the format bible), the characters and locations with their reference packs, the style bible, the graphics projects and the sound kit (ambience, music, effects). Story, boards, shots, cuts and deliveries start fresh. Change the words in the graphics projects and render again; the look and the timing stay.

## One idea, many formats

One idea or one shoot should come out as several pieces. Decide which at shot design, not at delivery:

| Version | How |
|---|---|
| **Master** | the main shape (9:16 if social comes first, 16:9 for web or screens) |
| **Second aspect** | reframed shot by shot, never a blind crop (`film deliver`, then fix by hand the shots that lose the story; handbook 14) |
| **15-second cutdown** | its own cut list, best seconds only: `film assemble --edl 06_edit/cutdown_15.txt` |
| **6-second bumper** | one idea, one image, the brand; often the hook shot and the end card |
| **Teaser or loop** | the strongest moment, built to be watched twice |
| **Still** | the thumbnail or a post: `film frames <file> --at <t>` from the best frame |

Rules:
- **Every version gets its own hook.** A cutdown is not the first 15 seconds of the master; it opens on its own strongest moment.
- **Mark it in the shot list:** `9:16 safe`, `generate both`, `hook candidate`, `cutdown` in the notes column (handbook 10).
- **Each shape gets its own graphics layout and captions,** never a scaled copy (the `graphics` and `captions` skills).

## Speed and volume

Volume without a method makes a feed of forgettable pieces. Volume with a method makes a body of work. The method is the same ladder (still → draft → lock → final → fix); speed comes from not rebuilding what you already have, and from batching.

**Build once, reuse forever:**
- characters and their reference packs, location plates, the style bible;
- graphics projects (end card, lower third, hook text, step numbers): change the words and render again;
- a sound kit: the series sting, room tones, ambience beds, a licensed music bed;
- the caption style.

`film new --from` carries all of it into the next piece.

**Batch the work, not the judgement:**
1. Write every shot card for the week's pieces in one sitting.
2. Ask Claude to run all the drafts as one batch (`film gen ... --count 2` per shot; `film jobs` to collect them).
3. Review the dailies once (`film dailies`) and lock or reject every take with a code.
4. Promote or upscale only the locked takes, in one batch.
5. Assemble, review and QC each piece; captions and graphics per shape last.

**A week of content on the ladder** (course rates, September 2026; check yours with `film cost`):

| | Per shot | Per 15-second reel (5 shots) | Five reels |
|---|---|---|---|
| Four drafts at about $0.51 | $2.04 | $10.20 | $51 |
| One upscale of the locked take at about $0.40 | $0.40 | $2.00 | $10 |
| **Total** | **about $2.44** | **about $12** | **about $61** |

Stills, voice and music come on top. Reuse brings it down: a shot from last week's library, a location plate that needs no new stills, a character who needs no new reference pack.

**The quality floor:** every piece, however fast, goes through `film review` (Claude checks every join), `film qc` and the phone test before it's posted. Speed that skips the floor is just noise.

**Label AI content** where the platform asks for it, and keep consent on file for any real person's face or voice (handbook 15).

## In the studio

| Skill | What it does here |
|---|---|
| `story-engine` | pressure-tests a series engine, a scenario, a hook, a tutorial outline |
| `shot-designer` | marks `9:16 safe`, `hook candidate` and `cutdown` in the shot list |
| `graphics` | hook text, step numbers, callouts over real screens, end cards per shape |
| `captions` | the house caption style, per shape |
| `editor` | cutdowns, loops, the first-second check, `film review` |
| `studio` | `film new --from` for episodes and the next piece |

```
film new "Desk Diaries" --format social --duration 25        # the pilot
film new "Desk Diaries Ep 2" --from desk-diaries             # the next episode, same cast and look
film frames 07_delivery/masters/desk-diaries_9x16_v001.mp4 --at 0,0.5,1 --width 360   # the first second at phone size
film assemble --edl 06_edit/cutdown_15.txt                   # the cutdown
```

Ask Claude: "Here is my series idea. Interrogate the format: the promise, the engine, the end button. Then ask me for ten episode titles and tell me which ones break the engine."

## Drills

1. **Hook swap (15 min).** Take any of your finished pieces. Make three versions that differ only in the first second (mid-action, result first, a text line). Check each with `film frames --at 0,0.5,1 --width 360` and pick one without watching past two seconds.
2. **Ten titles (10 min).** Write the format bible for a series you'd follow. Write ten episode titles. Cross out any that break the engine.
3. **Five from one (30 min).** From one finished piece, make the second aspect, a 15-second cutdown with its own hook, a 6-second bumper and a thumbnail. Put all five on a phone and watch them in a row.
