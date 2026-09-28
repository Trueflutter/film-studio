# 14 · QC and Delivery

AI films fail in two places a normal production rarely does: in single frames (a sixth finger for four frames, a line of gibberish on a screen) and in the gaps between shots (a face that changes, a room tone that vanishes). You will not catch these by watching your own film the way you made it. QC is a habit you run at every stage, with a fixed protocol, machine checks and a rubric, so the audience never becomes your quality control.

## The short version

1. **QC is a habit, not a gate.** Check takes in dailies, story in the rough cut, everything at lock, and every deliverable file.
2. **Watch the same way every time:** full screen with sound once without stopping, then muted, then eyes closed, then on a phone, then frame by frame through every cut.
3. **Gut note first.** Write your first reaction before you analyse anything.
4. **Machines check the numbers** (`film qc`); **humans check the film** (the 12-area rubric).
5. **Every note gets a timecode, a diagnosis code and a fix.** A note without a fix is a complaint.
6. **Fix the biggest problem with the cheapest fix first.**
7. **Deliver from a textless master.** Reframe, caption and label per platform, and keep provenance intact.
8. **Archive a rebuild kit** so the next re-cut never pays for generation again.

## QC at every stage

| Stage | What you check | Tool |
|---|---|---|
| Dailies | Each take: select, maybe or reject, with a code | `film dailies`, `film contact --shot S03` |
| Animatic | Story, order, timing | `film animatic`, one fresh viewer |
| Rough cut | Story, emotion, what's missing | Viewing protocol, rubric areas 1-2 |
| Fine cut / lock | All 12 areas | `film qc` on the cut, full protocol |
| Each deliverable | Spec, captions, safe zones, loudness | `film qc --spec ...`, phone check |

A problem found in dailies costs a re-roll. The same problem found after lock costs a re-roll plus a re-cut, a re-mix and new captions.

## The viewing protocol

Run all six steps on every cut you might ship. `film qc` puts this checklist into each QC report.

| Step | How | What it catches |
|---|---|---|
| 1. Full screen, with sound, no stopping | Write your gut note before any analysis | Story, emotion, pacing: the audience's experience |
| 2. Muted | Watch the picture alone | Does the picture tell the story? Feeds autoplay muted |
| 3. Eyes closed | Listen only | Missing room tone, level jumps at cuts, voice that doesn't fit the space |
| 4. Phone at arm's length | The way most people will see it | Caption size, safe zones, faces too small, text you can't read |
| 5. Frame-step every cut | Last 5 frames out, first 5 frames in | Flash frames, morphs at joins, same-size jumps, black frames |
| 6. One fresh viewer | Show it once, then ask: "What was it about?" | Whether your intent survives contact with a stranger |

Step 6 is the one people skip. Don't explain before or during. If their answer differs from your logline, that's a Story note, not a viewer problem.

## The machine checks: `film qc`

`film qc master.mp4 [--spec social|web|broadcast|cinema-ish]` probes the file, measures it and writes a report to `07_delivery/qc/<file>_qc_<date>.md` with three parts: the technical table, a blank creative rubric, and the viewing protocol checklist.

| Check | Measures | PASS | WARN | FAIL |
|---|---|---|---|---|
| Frame size | Width x height vs the production | Matches, or is a standard deliverable size (1080x1920, 1080x1080, 1080x1350...) | Same aspect, different resolution | A non-standard size and aspect |
| Frame rate | fps vs the production | Within 0.05 fps | Anything else | |
| Duration | Length vs target | Within 10% | Further off | |
| Audio track | Present or not | Present | Missing: a silent file | |
| Loudness | Integrated LUFS vs spec | Within ±1 LU | | Outside ±1 LU |
| True peak | dBTP vs spec ceiling | At or below | | Above |
| Loudness range | LU | 15 LU or less | Above 15 | |
| Dead air | Silence below -50 dB for more than 1.5 s | None | Timecodes listed | |
| Black frames mid-programme | 0.25 s or more of black, head and tail excluded | None | Timecodes listed | |
| Frozen picture | Picture frozen for more than 0.8 s | None | Timecodes listed | |

**Specs used:**

| `--spec` | Integrated | True peak ceiling |
|---|---|---|
| `social` | -14 LUFS | -1 dBTP |
| `web` | -16 LUFS | -1 dBTP |
| `broadcast` | -23 LUFS | -2 dBTP |
| `cinema-ish` | -24 LUFS | -2 dBTP (a sanity check only; cinema works to a distributor spec) |
| none | the production's own target (`-14` for ad and social productions, `-16` for film) | -1 dBTP |

**Reading the verdict.** Any FAIL makes the verdict FAIL: loudness, true peak or a non-standard frame. Fix them before shipping. A deliberate aspect variant (a 9:16 file from a 16:9 production) passes as a standard deliverable size; still check it's the right one for the platform. WARN means "look at it and decide". Intentional choices are fine: an end card is a frozen picture, a `slate` in the cut is black, a held silence is dead air. Write "intended" next to each one you keep.

**What the WARNs usually mean in an AI film:**
- **Dead air** often means there's no room tone under a generated clip whose scratch audio you muted. That silence is a realism failure (lever 11), not just a technical one. Lay a room tone bed (handbook 08).
- **Black mid-programme** is often a forgotten `slate` placeholder in `cut.txt`.
- **Frozen picture** you didn't intend is often a still used where motion was planned, or a clip held past its last frame in the NLE.

**Fixing FAILs.** Loudness: re-run `film mix` with `--target`, or let `film deliver` normalise each variant (`--lufs` sets the target). True peak failing by a few tenths after encoding: lower the limiter ceiling in your audio tool and re-export. `film mix` and `film deliver` limit sample peaks at -1.5 dB to leave headroom for inter-sample peaks; a broadcast spec (-2 dBTP) may need a lower ceiling.

## The creative rubric: 12 areas

Score each area 1-5 in the QC report. Anything under 3 gets a **timecode, a diagnosis code** (handbook 12) **and a fix**.

| Score | Meaning |
|---|---|
| 1 | Breaks the film |
| 2 | A first-time viewer will notice |
| 3 | Only a careful viewer will notice |
| 4 | Clean |
| 5 | A strength of the film |

**What to look for** (the AI tells, with their usual codes and cheapest fixes):

| Area | Look for | Usual codes | Cheapest fix |
|---|---|---|---|
| **Story** | Shots with no job; a turn or payoff that needs explaining | CONCEPT, WORKFLOW | Cut the shot, reorder, add an insert or a line |
| **Emotion** | Caricatured emotion (bug-eyed, over-acted); music pulling against the moment | PERFORMANCE | Pick the subtler take, cut shorter, drop the music under the line |
| **Realism** | Waxy skin, flat even light, oversaturated "AI grade", grainless over-sharpness, pristine sets with no wear | REF, PROMPT, MODEL | Grade down, one grain pass, crop; regenerate only hero shots |
| **Continuity** | Identity or wardrobe drift, hair colour change, light direction flips, broken screen direction | IDENTITY, REF | Cut around, insert, region edit, flip if nothing asymmetric |
| **Composition** | Every shot a centred, eye-level hero shot; dead headroom | FRAME, CAMERA | Reframe or punch in; reorder to vary sizes |
| **Motion & physics** | Floaty camera, weightless or slow-motion movement, failed contact (sliding feet, hands through cups) | CAMERA, PHYSICS, ACTION | Speed up 110-120%, stabilise, trim; insert plus foley at the contact |
| **Faces & anatomy** | Dead eyes, morphing hands, extra fingers, shifting teeth | ARTEFACT, IDENTITY | Cut before it, crop, region-edit the frames |
| **Lip sync & voice** | Drift late in the clip, generic TTS timbre, robotic cadence, voice not in the room | SYNC, PERFORMANCE | Constant audio nudge; re-drive lips from audio; speech-to-speech to the cast voice; room reverb |
| **Sound** | No room tone, sterile silence, music smothering dialogue, level jumps at cuts | WORKFLOW | Room tone bed, foley at contact points, duck the music |
| **Edit & pacing** | Uniform shot lengths, same-size jump cuts, late-clip degradation left in | WORKFLOW | Re-trim to best seconds, bimodal rhythm, punch-in or insert (handbook 09) |
| **Artefacts & text** | Gibberish text or UI, ghost background people, flicker, melting, compression mush | ARTEFACT | Composite the text; crop or blur the extras; re-export at a higher bitrate |
| **Brand / brief fit** | Wrong or missing CTA, mandatories, legal lines, disclosure; wrong audience or tone | CONCEPT | Fix the card or caption; recut to the brief |

## Prioritise: biggest problem, cheapest fix

Sort the notes in two passes.

**1. By severity.**
- **Blockers:** the story doesn't read, a legal line or CTA is wrong, any `film qc` FAIL, sync off on a hero line.
- **Visible:** anything scored 1-2.
- **Pixel-level:** only visible frame by frame.

**2. Within each tier, cheapest first.** Follow the remedy ladder:

| Rung | Typical fix | Cost |
|---|---|---|
| Keep and cut around | Re-trim, reorder, cut away | Minutes, free |
| Fix in post | Audio nudge, room tone, reframe, grade, region edit, composite | An hour, usually free |
| Re-roll (max 2) | A new draft of the same shot | Cents to dollars |
| Change one variable, then frames or refs, then simplify or split the shot | A redesigned shot | More drafts |
| Change mode or engine, redesign | A new approach | Expensive; replan |

Three strikes on the same approach means redesign, never a fourth re-roll. **Ship when there are no blockers and no area scores below 3.** Pixel-level notes go on a list for the next version.

## Captions QC

Captions are part of the picture on social and part of accessibility everywhere. `film captions check file.srt` runs these checks (common broadcast and streaming subtitle guidance):

| Rule | Limit | Fix when broken |
|---|---|---|
| Reading speed | 17 characters per second or fewer | Cut words or extend the cue; don't shrink the font |
| Line length | 42 characters or fewer | Rebalance the lines |
| Lines per caption | 2 or fewer | Split into two cues |
| Time on screen | 0.83 s minimum, 7 s maximum | Merge short cues, split long ones |
| Gap between cues | None, or at least 0.083 s | Close tiny gaps (they flicker) or open them up |
| Overlap | None | Fix the timings |

**Authored lines, checked against the transcript.** Transcription mishears names and dialect. Write your caption lines yourself and pass them with `--lines`: `film captions build` times each line from the transcript, reports every word where you and the transcript disagree ("you wrote X, transcript heard Y"), flags a line that spans two speakers, and stops when more than about a third of a line's words don't match (the lines have drifted from the audio). Resolve every "check" note by listening.

**Arabic and other right-to-left scripts** (studio-tested Sep 2026):
- Never auto-group by word count; it split "الذكاء / الاصطناعي" (artificial / intelligence) across two captions. Author phrase lines.
- For dialect, compare two or three transcription engines; the words they disagree on are the ones to check by ear.
- Drop trailing full stops and commas at the end of a caption: bidirectional text moves them to the far left.
- Check one burnt frame for boxes or broken letter joins.

**Text on screen vs the caption band.** A printed word on a costume sat exactly under the caption line in a character's close-ups (studio-tested Sep 2026). Measure every sign, print and screen per shot, and move the band for the whole film rather than shot by shot.

**Safe zones on 9:16.** Platform UI covers roughly the top 15% and the bottom 20% of a vertical frame (studio-tested), and the action buttons sit along the right edge. All three caption styles keep the baseline clear of the bottom zone on tall frames (`social` 68%, `clean` 70%, `film` 76% of the height); pass `--y` to move them, for example above a lower third.

## Delivery specs by platform

Platform specs change without notice. This table reflects the studio's research (Sep 2026); check each platform's current page before a client delivery (verify before cohort).

| Destination | Aspect (size) | Loudness | Captions | Safe zones and notes |
|---|---|---|---|---|
| TikTok, Reels, Shorts | 9:16 (1080x1920) | -14 LUFS, -1 dBTP (practice; no published spec) | Burnt in; also upload the SRT where accepted | Top ~15%, bottom ~20%, right edge. Hook in the first shot |
| Instagram / Facebook feed | 4:5 (1080x1350) or 1:1 (1080x1080) | -14 LUFS practice | Burnt in | Autoplays muted: the picture carries the story |
| LinkedIn | 1:1 or 16:9 | -14 LUFS practice | Burnt in plus SRT | Autoplays muted (studio-tested) |
| YouTube | 16:9 (1920x1080 or higher) | Normalises to about -14 LUFS; master at -14, -1 dBTP | SRT sidecar as closed captions | Keep text inside 90% of the frame |
| Web / landing page | As designed, often 16:9 | -16 LUFS (`--spec web`) | Burnt in if it autoplays muted; otherwise a sidecar | Check the player's caption format |
| Broadcast | Per the broadcaster, usually 1920x1080 | EU: -23 LUFS (EBU R128); US: -24 LKFS (ATSC A/85) | Closed captions to the broadcaster's spec; never burnt unless asked | The broadcaster's delivery sheet overrides everything here |
| Festival / screening | 16:9 or 2.39:1, per the festival | Festival or distributor spec | Burnt subtitles only for foreign-language dialogue; SRT on request | Ask for the screening format early |

## Multi-aspect planning starts at the shot list

A 9:16 crop from a 16:9 frame keeps less than a third of the width. Decide at shot design, not at delivery:

- In `shotlist.csv` notes, mark each shot: `9:16 safe` (subject central), `needs reframe`, or `generate both` (hero shots where both formats matter).
- Draw the vertical extraction box on 16:9 boards so you compose for both.
- Keep titles, end cards and captions out of the master. They are laid out per aspect: graphics with the `graphics` skill, put on each delivered shape with `film overlay`, then captions with `film captions burn`.

**Reframe rather than blind-crop.** `film deliver` applies one fit to the whole master:

| `--fit` | Does | Use when |
|---|---|---|
| `crop` (default) | Scales to fill and crops from the centre | Every shot keeps its subject central |
| `pad` | Letterboxes or pillarboxes in black | A deliberate framed look, e.g. 16:9 inside 1:1 |
| `blur` | Fills the frame with a blurred, darkened copy and centres the full picture on top | Wide shots where a crop would lose the story |

For the priority deliverable, reframe shot by shot in the NLE (keyframe the position where the subject moves). Use `film deliver` for secondary variants, then frame-step every shot of each variant.

**Order of operations:**
1. Lock, grade and mix the **textless master**; run `film qc` on it.
2. Make the aspect variants (`film deliver` or NLE reframes). `film deliver` also normalises loudness to the production target.
3. Put each variant's own graphics on: `film overlay <variant> <render>@<seconds>` (end card, supers; the `graphics` skill).
4. Build captions per variant (`--video` reads that variant's frame size) and burn them in.
5. Run `film qc --spec ...` on every file you will upload, and `film review` to frame-step every cut.
6. Name it, log it in `07_delivery/delivery.md`, upload with the right labels.

Never run `film deliver` on a file with graphics or captions: the crop cuts through the type.

## Names, versions, masters and deliverables

`film deliver` writes `07_delivery/masters/<slug>_9x16_v001.mp4` and never overwrites. For hand-off, name each file with everything a stranger needs:

`<slug>_<platform>_<aspect>_<length>_<language>_<captioned|textless>_v<NNN>.mp4`
e.g. `nightshift_reels_9x16_30s_en_captioned_v003.mp4`

No "final", "final2" or "FINAL_real". The version number should match the QC report for that file.

| | Master | Deliverable |
|---|---|---|
| What | The locked film at full quality: graded, mixed to programme loudness, textless | A platform-shaped copy: aspect, captions, loudness, file size |
| How many | One per cut (the film, the 15 s cutdown) | Platforms x languages |
| Alongside it | SRT per language; stems: dialogue, music, effects, and an M&E (music and effects, no dialogue) for dubbing | Its QC report |
| Kept | Forever | The ones you shipped; the rest can be rebuilt from the master |

## Disclosure and provenance

**Label AI content where platforms ask, and when in doubt.** YouTube asks for an "altered or synthetic content" disclosure on realistic content; TikTok requires AI-generated labels on realistic AI content and reads C2PA Content Credentials; Meta applies "AI info" labels. The EU AI Act's Article 50 transparency obligations apply from 2 August 2026 (all: verify before cohort). Tell the client or festival which elements are generated, and add a credit line where it helps ("Voices: AI-generated").

**Keep provenance intact.** Google's Gemini Omni video and Lyria music outputs carry a SynthID watermark (verified Sep 2026). Never crop, blur or strip a watermark or Content Credentials. If a visible watermark is unacceptable, buy a plan that doesn't add one. A re-encode can drop embedded metadata such as Content Credentials, so keep the original provider files in the archive (verify before cohort).

**The provenance log** is `07_delivery/delivery.md`: one row per external asset (tool or model, version, plan or licence, date, permitted use, receipt or consent file), plus the likeness and voice consent table. `takes.csv` already records every generated take. The rows that bite are music and voices. ElevenLabs Music self-serve plans cover online ads but not film and TV (verified Sep 2026), and Suno v6 has download caps and faces new record-label litigation (reported Sep 2026). Record the plan on the day you downloaded (handbook 15).

## Archive a rebuild kit

The studio keeps each project's media in three places (studio-tested Jun 2026):

| Folder | Holds | Maps to |
|---|---|---|
| `sources/` | Everything during production | Rejected takes, drafts, temp audio |
| `rebuild-kit/` | Locked clips promoted before cleanup, so a re-cut never re-pays generation | Selects, fixes and upscales from `04_shots/`, stems from `05_sound/`, `06_edit/cut.txt` and its versions, prompts and refs |
| `final/` | Approved deliverables, kept forever | `07_delivery/masters/`, QC reports, `delivery.md`, `wrap.md` |

Clean up safely: promote keepers first, review a dry-run list of what would go, move sources to a quarantine folder, and empty it as a separate, deliberate step. Never hard-delete in one shot.

## Weak vs strong: a QC note

**Weak**

> Looks a bit AI in the middle. Sound feels off. Maybe fix her hand?

No timecode, no area, no cause, no fix. Nobody can act on it, including you tomorrow.

**Strong**

> **00:14.2-00:15.0 · Faces & anatomy 2/5 · ARTEFACT**
> Her right hand gains a sixth finger as she lifts the cup (S06_t004, its last 0.8 s).
> **Fix:** out point 3.4 → 2.6 s and cut on the lift to the S07 cup insert. Free, 5 min.
>
> **00:21.0-00:23.5 · Sound 2/5 · WORKFLOW**
> Dead air WARN in `film qc`: scratch muted on S09, no room tone, the kitchen goes dead.
> **Fix:** kitchen room tone bed under S08-S10, re-run `film mix`. Free, 10 min.

Each note names where, what area, how bad, why (the code), and the cheapest fix with its cost. That's a to-do list, not an opinion.

## In the studio

| Skill | Use it for |
|---|---|
| `qc-review` | Runs `film qc`, walks you through the viewing protocol and rubric, and sorts the fixes cheapest first |
| `graphics` | End cards, titles and supers per shape, rendered transparent for `film overlay` |
| `captions` | Transcribe, author lines, build, check and burn captions |
| `editor`, `sound-design` | Carrying out the edit and mix fixes (handbooks 09, 08) |
| `studio` | Status, the delivery log, the wrap notes |

```
film qc 06_edit/cuts/cut_v007_mix_v001.mp4                  # QC the locked cut
film qc 07_delivery/masters/nightshift_master.mp4 --spec social
film deliver 07_delivery/masters/nightshift_master.mp4 --aspects 9:16,4:5 --fit crop
film deliver 07_delivery/masters/nightshift_master.mp4 --aspects 9:16 --fit blur
film captions transcribe 07_delivery/masters/nightshift_master.mp4 --lang en
film captions build 07_delivery/masters/nightshift_master.words.json --lines 06_edit/captions.txt --style social --video 07_delivery/masters/nightshift_9x16_v001.mp4
film captions check 07_delivery/masters/nightshift_master.srt
film overlay 07_delivery/masters/nightshift_9x16_v001.mp4 06_edit/graphics/endcard_9x16/renders/endcard.mov@41.5
film captions burn 07_delivery/masters/nightshift_9x16_v001_gfx.mp4 07_delivery/masters/nightshift_master.social.ass
film qc 07_delivery/masters/nightshift_9x16_v001_gfx_captioned.mp4 --spec social
film review 07_delivery/masters/nightshift_9x16_v001_gfx_captioned.mp4   # every cut on a sheet
film cost --save                                            # the numbers for wrap.md
```

Ask Claude: "QC this cut for a 9:16 social delivery. Run the machine checks, then take me through the rubric one area at a time and give me the top three fixes, cheapest first."

## Drills

1. **Tell hunt (15 min).** Pick any public AI ad. Run the viewing protocol and log ten notes in the strong format: timecode, area, score, code, cheapest fix.
2. **Read the machine (10 min).** Run `film qc` on your latest cut. For every WARN, write "intended" or a fix. For every FAIL, fix it and re-run until the verdict is PASS or PASS with warnings.
3. **Caption stress test (15 min).** Build captions for a 20-second dialogue passage with `--lines`. Run `film captions check` and fix every issue by editing the words or timings, never by shrinking the type. Then check one burnt frame on your phone.
4. **One master, three fits (20 min).** Deliver a 16:9 cut to 9:16 with `crop`, `pad` and `blur`. Frame-step all three and write down which shots need a hand reframe and which fit you'd ship.
