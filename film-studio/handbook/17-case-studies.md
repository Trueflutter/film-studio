# 17 · Case studies

You learn AI filmmaking fastest from other people's decision logs: what they tried, what failed, and what they changed. These teardowns show that convincing AI films are made in direction, reference discipline and the edit, and that every good result sits on a pile of rejected takes. Read them for the decisions, not the tool names: the tools will change, the decisions hold.

## The short version

1. Idea and format first. Judges and audiences reward intent over polish.
2. Plan in stills, lock characters with boring references, then route each shot to the engine that does it best.
3. Treat seams as the enemy: native multishot cuts, or a change of size and angle, cut on motion, or a cutaway.
4. Voice is usually the weakest link. Lock it with a real performance or speech-to-speech.
5. Keep text, UI and logos out of generation. Composite them.
6. Approve cheap, finish locked: upscale or promote the approved take, never re-roll for resolution.
7. Expect a low keep rate and budget for it.
8. Every case here was finished in the edit: short takes, rhythm, sound, one grade.

**Tags.** (studio-tested): this studio's own production logs. (reported): a vendor, press or creator account. "(reported, verify before quoting)": prior knowledge the course research could not re-check, fine for discussion but not for a slide until you check the source.

## Case 1 · Studio case: ONE APPLICANT (studio-tested)

**The brief.** A ~39-second 9:16 dialogue ad for a training programme. A tired recruiter finds an applicant's "portfolio" that looks like a big-budget agency car commercial. His boss assumes it is the agency's work. The twist: one applicant made all of it with AI. Structure: hook, twist, call to action, cold open on a face and a line (never a silent establisher).

| # | Beat | Line |
|---|---|---|
| 1 | Recruiter notices something on his screen | |
| 2 | He reacts: pleasantly surprised, not shocked | |
| 3 | He calls his boss | "Sarah, come check this out." |
| 4 | She walks in from the side he looked toward and leans in | "Wait, is that the campaign from the agency?" |
| 5 | Cutaway: the car film on the laptop | |
| 6 | Recruiter | "No… it's a portfolio. From someone applying for the marketing role." |
| 7 | Sarah, the button | "One applicant made all of this?" |
| 8 | Dark end card flowing into a muted logo sting; narrator | "It's a lot easier than you think." |

**The method.** Script → board and blocking → generate at low resolution (two takes, pick one) → approve each beat from a preview → voice (speech-to-speech to the cast) → text and cards in post → music bed → assemble → review → upscale the locked clips → master. Nothing expensive happens before approval.

### The decision log, v1 to v12

| Cut | What changed | Why | Lesson |
|---|---|---|---|
| v1 | First assembly (22.7 s) from approved plates, lip-synced lines and narrator VO | Prove the pipeline end to end | Assemble early: the cut shows problems that stills hide |
| v2 | Two-shot and dialogue regenerated at 1080p, anchored on a clean frame of shot 1; dense house prompt style kept after an A/B | 720p multi-character shots read grainy and "AI". The alternative prompt style won on stills and lost in motion | Hero and dialogue shots at 1080p; keep anchor chains shallow; judge in motion |
| v3 | New, female narrator; dialogue voices made distinct; animated brand text on the car beats, built in post | Viewers thought the narrator was the man on screen | The narrator must sound unlike every on-screen voice |
| v4 | Punch-ins (1.35× and 1.25×) on two same-size neighbours | Same angle and size across a join read as a glitch | Try the free editorial fix first |
| v5 | A walk-in bridge: Sarah enters and leans in | She "appeared" between two shots | Show entrances |
| v6 | Call beat regenerated with his eyeline toward her entrance; second car shot cut; close VO moved onto the end card | The eyeline must predict the entrance; the repeated car film read as a repeat | Eyeline = entrance. Never repeat a payoff shot |
| v7 | The three stitched opening shots replaced by one Kling multishot generation with three native cuts | Stitched same-subject clips kept showing seams | Let the model author the cuts: identity and grade hold inside one generation |
| v8 | Everything after the opening rebuilt in Kling, chained frame to frame; Sarah enters from the left to match his gaze | Match the opening's look and eyeline | One engine per sequence where you can |
| v9 | +150 ms audio nudge on the opening line; one clip extended so a line finishes before the cut | Native multishot sync drifted on one beat; a line was chopped mid-word | Native sync isn't locked. Try a constant nudge (review a ladder of offsets), then re-drive the lips from audio |
| v10 | Close VO rewritten from "You can learn to do this" to "It's a lot easier than you think", chosen from three options | The first read sounded robotic | Audition lines as a ladder of options |
| v11 | Instrumental music bed, low under dialogue and lifting under the outro; end card darkened to match the logo sting; logo only in the (muted) sting | The music carries the arc; a card that flows into the sting avoids a double logo | Mix the bed with `amix` and `normalize=0` so it doesn't pull the voices down |
| v12 | The three dialogue clips upscaled 720p → 1080p (13 credits in total), locked audio re-muxed | True hi-res without touching approved performances | Upscale locked clips; never regenerate for resolution |

### The six rules this ad locked in

1. **The transition rule.** Never butt two separately generated clips of the same subject at the same size and angle. Every same-subject join is a native multishot cut, a clean cut (size and angle change of 30° or more, on motion), a matched continuation from a locked start and end frame, a masked cut (whip, J- or L-cut), or a cutaway. Never cross-dissolve two AI clips: the viewer sees both mismatched states at once. (Handbooks 03, 09.)
2. **Native multishot for coverage.** When one generation authors the cuts, there is no stitch seam. Render two and keep the one that actually cut; prompt "N distinct hard cuts, not crossfades".
3. **Speech-to-speech for voice.** Generate with a placeholder voice, then convert each clip's own embedded audio to the cast voice. S2S preserves timing 1:1, so lip sync holds. (Handbook 07.)
4. **Text in post.** Models scramble letters. Slogans, end cards and product names are built in motion graphics or HTML and composited. (Handbook 09.)
5. **One music bed.** One instrumental shaped to the arc (curious, lift at the reveal, confident resolve), ducked under dialogue, lifted where no one speaks. (Handbook 08.)
6. **Upscale the locked clips.** Approve at low resolution, then upscale only what was approved and re-mux the locked audio (frame counts match, so sync is untouched). Regenerating for resolution re-rolls the performance you approved. (Handbook 13.)

### Weak vs strong: the call-and-entrance cut

| | What the viewer sees | Why |
|---|---|---|
| **Weak (v2)** | One shot ends with him leaning forward, the next starts with him leaning back as he calls "Sarah"; hard cut to a two-shot where she is already beside him | A pose jump, then a woman who materialises: two tells in two cuts |
| **Strong (v8)** | He glances frame-left as he calls, inside one multishot generation; she walks in from frame-left in a clip chained from his last frame, and delivers her line | The eyeline predicts the entrance and motion carries the eye across the cut |

## Case 2 · Studio case: the reference-ad teardown (studio-tested)

The studio took apart two long-form paid social ads by an online AI-certificate brand (Coursiv): 2:38 and 3:11 long, same product, two scenarios. A nail technician gets advice from her neighbour; a new analyst is told she's "ten years behind" and finds her way back.

| Move | What they did | Why it works |
|---|---|---|
| Bimodal cut rhythm | Average shot length 2.6-2.8 s overall, but split into long holds of 8-13.5 s for the hardest lines and bursts of 0.9-1.5 s around the transformation | Holds carry honesty, bursts carry change, and neither asks the model for subtle performance |
| Brand arrives late | First named at 73 of 158 s and about 95 of 191 s: roughly 45-55% of runtime | The viewer is inside a story for about a minute before an ad exists |
| One signature thesis line | Held in tight close-up on the messenger: "You have ten years they don't have. Add the right tools. Nobody in that room touches you." | The whole pitch in one quotable breath |
| Specific small numbers | "$150 on ads", "four clients a week", "28 days", "15 minutes a day" | Integers, not adjectives: small enough to believe, specific enough to remember |
| Time-jumps that rhyme | A "28 days later" card; DAY 14 and DAY 28 overlaid on the live scene | The time-jump echoes the programme's own length |
| Music with one drop | Piano-led score that drops out at one critical line and swells into the end card | Silence makes the key line land |
| Visual rhyme payoff | The silent husband smiling at the busy salon; the analyst standing in the room where she was threatened, her boss seated | A planted line paid off as a picture. This is what gets forwarded |
| "Send me the link" | The share is acted inside the scene: a phone handed over, a link sent | Models the behaviour the ad wants |

Both films work **despite** visible AI tells (background ghost figures, hair-colour drift, waxy close-ups, gibberish phone screens) because the writing carries them.

**Three things not to take:**
1. **The "I was where you are" mentor.** An AI character claiming a biography breaks the studio's no-pretence rule (handbook 15). Replace it with observation plus a real, named graduate.
2. **Viewer-shaming lines** that compare the audience unfavourably with younger colleagues. Accusation doesn't build trust.
3. **AI-generated UI text.** Every screen in both ads contained gibberish. Composite real screenshots or motion graphics.

## Case 3 · Simon Meyer: direct, don't roll dice

Simon Meyer is a Berlin-based director, cinematographer and editor who came to AI from TV, commercials and social content (reported).

**GRANDMA vs WASP**, made with Muhannad Nassar, a two-minute action comedy (a grandmother against a wasp at a summer breakfast, shot in an extreme slow-motion style), won first place and $150,000 in Higgsfield's "Make Your Action Scene" contest in March 2026, out of 8,752 entries from 139 countries (reported, press, Mar 2026). Higgsfield's results said the judges prioritised "storytelling and directorial intent over technical polish" (reported).

| Stage | What they used | If you did it today |
|---|---|---|
| Tone exploration | Sora 2, "used like rough storyboards" | Sora's API closed 24 Sep 2026: use a cheap draft engine (handbook 16) |
| Character lock | Nano Banana, iterated | the same, with a boring reference sheet (handbook 05) |
| Composition | a 3x3 grid per scene: nine framings, the director picks | the same (handbook 10) |
| Motion | Kling for most shots | route per shot (handbook 06) |
| Fast action | Seedance for the high-speed beats | the same principle |
| Consistency | character reference in Higgsfield Cinema Studio | reference discipline (lever 7) |

Two directors who had never met worked a 24-hour relay across time zones for about a week (reported).

**Come to Germany** (2026), a spec tourism ad: the star is "Dieter", an ordinary, bespectacled older man whose ordinariness is the joke. Meyer locked him with one base image fed into Seedance text-to-video, and built every scene from multishot prompts describing lighting, wardrobe and location. Tools he named: InVideo Agent, Seedance 2.0 and 2.5, the base image edited with GPT Image, the edit in DaVinci Resolve. About $300 in credits, excluding testing (reported, Meyer's own figure).

**The critique.** Of his 2025 short *Frankenstein's Interview*, one commentator praised "intentionality and continuity" but said the AI voice had "a slight 'something' missing in the emotion and delivery" (reported). Another viewer argued that consistency isn't the real problem; knowing the people aren't real is (reported). Take both: voice is the weak link, and realism is a floor, not the product.

**What to steal:** premise-first concepts, formats that forgive AI (comedy, slow motion, interviews), a cinematographer's shot grammar, per-shot routing, and cutting like an editor so weak frames never stay on screen.

## Case 4 · Hell Grind, Higgsfield's feature (vendor-reported)

Every figure here comes from Higgsfield's own documentary about the project, as transcribed by a third party. Treat all of it as vendor-reported.

| Metric | Figure |
|---|---|
| Output | a 90-95 minute feature for Cannes, May 2026 |
| Team and time | 15 people, 14 days |
| Generations | 108,859; about $400k of generation, about $500k in total |
| Keep rate | **about 1% of images and 1.5% of videos** made the final cut |
| One lead character | **about 800 generations to lock** (about 600 in Soul Cinema plus 200 GPT Image 2 edits) |
| One 10-second establishing shot | 72 generations |
| Pace | about 2.5 minutes of finished footage per person per day; week 1 a rough assembly of everything, week 2 refining key moments |

The rules worth stealing:

| Rule | What it means | Handbook |
|---|---|---|
| The character sheet is three images | a 3/4 face close-up, a full body front **with the head removed**, a full body back (the model had been taking the face from the tiny full-body figure) | 05 |
| Keep the sheet deliberately boring | grey background, flat light, real pores, no grain, no cinematic lens: the scene carries the look, not the sheet | 04, 05 |
| An asset is a descriptor plus an image | the text description is pasted word for word into every prompt | 06 |
| Never regenerate twice | never run an image through a model twice in full: point-edit one region, then mask-composite it back onto the original | 05 |
| Shoot locations in 3/4 | with one anchor object and one light logic ("never two suns") | 05 |
| Assemble first | rough-cut everything before polishing anything | 09, 13 |

## Case 5 · Historical lessons

| Project | What happened | Lesson | Confidence |
|---|---|---|---|
| **Air Head**, Shy Kids (2024, early Sora) | About 300:1 generated to used footage. The model kept putting a face on the yellow balloon and changing its colour, and defaulted to slow motion. Fixed in post with rotoscoping, colour correction and retiming | "AI film" means generation plus post. Fix in post before regenerating | (reported, verify before quoting) |
| **Kalshi NBA Finals ad**, PJ Accetturo (June 2025, Veo 3) | About 300-400 generations for about 15 usable clips, around $2,000, 2-3 days. Script and jokes first; hard cuts every 1-2 seconds | Fast comedic cutting hides tells: no shot stays up long enough to be scrutinised | (reported, verify before quoting) |

Air Head's footage ratio was about 300:1; the Kalshi ad needed about 20-27 generations per usable clip. Different measures, same direction: waste falls as planning moves upstream into stills and boards.

## The teardown method (pre-work)

The pre-work before Day 1, and a habit worth keeping for any film you want to learn from.

1. **Watch once for feeling.** No pausing, no notes. Then write three words for what you felt, and the moment you felt it most.
2. **Watch again and build the shot table.** One row per shot.
3. **Average shot length** = runtime ÷ number of shots. Note the longest hold and the fastest burst. Is the rhythm uniform or bimodal? `film teardown` does the counting: cut list, shot lengths, average, holds and bursts, and a sheet with one frame per shot to fill the table from. It finds hard cuts only, so check the sheet for dissolves and whips.
4. **Where does the turn (film) or the brand (ad) land**, as a percentage of runtime?
5. **One thing to steal**, with the reason it works.
6. **One thing to avoid**, with the reason.

```
| # | Time      | Shot size | Move | What we learn | What we feel | Sound |
|---|-----------|-----------|------|---------------|--------------|-------|
```

Example from the studio's own ad: in ONE APPLICANT the turn ("No… it's a portfolio") starts at 19.3 s of 39.4 s, just under halfway (studio-tested, from the build scripts): the same zone where the reference ads name their brand.

### Weak vs strong: one teardown row

| | Time | Shot size | Move | What we learn | What we feel | Sound |
|---|---|---|---|---|---|---|
| **Weak** | 0:12 | nice shot | camera moves | she's sad | sad | music |
| **Strong** | 0:12-0:25 | CU, long-lens feel, shallow focus | locked off | she's been told she is behind and doesn't argue | shame held in; we lean closer | music drops out, room tone only |

The weak row describes. The strong row explains how the shot makes you feel it, which is the part you can steal.

## What these cases agree on

| Pattern | Seen in | Where it lives in the course |
|---|---|---|
| Idea and format before tools | Meyer, Kalshi, the reference ads | handbook 01; judges reward intent |
| Boring references, one base image, the descriptor pasted verbatim | Hell Grind, Meyer, ONE APPLICANT | lever 7 · reference discipline |
| Route per shot | Meyer (Kling for motion, Seedance for action), ONE APPLICANT (Kling multishot for coverage, Seedance audio reference for dialogue) | lever 8 · the right engine per shot |
| Short takes, cut on motion, bimodal rhythm | Kalshi, the reference ads, ONE APPLICANT | lever 9 · short takes, best seconds; lever 10 · edit to hide and to breathe |
| Fix in post before you regenerate | Air Head, ONE APPLICANT v4 and v9 | lever 10; the remedy ladder (handbook 12) |
| Behaviour, not big emotion | ONE APPLICANT ("pleasantly surprised, not shocked") | lever 6 · behaviour over emotion |
| Voice is the weak link; sound sells the space | Meyer's critics, ONE APPLICANT v3, v10, v11 | lever 11 · the sound of the space; handbook 07 |
| One grade, text composited, one look across models | the reference ads (what not to take), ONE APPLICANT, Meyer's Resolve finish | lever 12 · one finish |
| A low keep rate, and money spent only on locked shots | Hell Grind (1-1.5%), Kalshi (about 15 of 300-400), ONE APPLICANT v12 | the economics ladder: still → draft → lock → final → fix |

The economics lesson under all of it: spend your exploration budget freely on stills and drafts, and spend the production budget only on locked shots. **A draft is a cheap direction test. Lock the take, then promote or upscale that take. Never re-roll the prompt at higher quality and hope.**

## In the studio

| Skill | Use it for |
|---|---|
| `story-engine` | Test your concept against these patterns: a forgiving format, one thesis line, a plant paid off as a picture |
| `editor` | Rhythm (ASL, holds, bursts) and the transition rule on every same-subject join |
| `take-doctor` | Fail codes and the remedy ladder, as in v4 (fix in post) and v9 (nudge before re-drive) |
| `performance-voice` | Voice first, S2S to the cast, a distinct narrator |
| `studio` | The decision log you write up in `07_delivery/wrap.md` |

```
film teardown 00_brief/refs/reference_ad.mp4 # cut list, rhythm and one frame per shot, for a private teardown
film contact --shot S04                      # every take of one shot, side by side
film dailies                                 # verdicts, fail codes and prompts: your decision log
film cost --save                             # keep rate, cost per usable shot, iterations before lock
```

Frames pulled from someone else's film are for private study. Don't publish them (handbook 15).

## Drills

1. **Teardown (20 min).** Pick a 30-90 second ad or short you admire. Run the six-step method. Share the table, your ASL, where the turn lands, and your steal and avoid.
2. **Your decision log (10 min).** Write the v1 to vN log for your EX2 sequence in the ONE APPLICANT format: what changed, why, lesson.
3. **Plant and pay off (15 min).** Find one line in your capstone script and rewrite the ending so it pays that line off as a picture, not as more dialogue.
4. **Keep-rate check (10 min).** Run `film cost`. Compare your keep rate with Hell Grind (vendor-reported) and Kalshi (reported), then adjust the generation counts in `03_board/generation_plan.md`.
