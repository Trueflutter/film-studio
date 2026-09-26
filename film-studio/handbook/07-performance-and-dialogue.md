# 07 · Performance and Dialogue

Audiences forgive a soft background. They do not forgive a face that lies. In AI films the performance is where viewers stop believing, and dialogue doubles the risk: the voice, the lips and the emotion all have to agree, and each comes from a different machine.

## The short version

1. **Direct behaviour, not emotion.** Give the character a task, a place to look and one small tell. Never write "sad".
2. **Voice first.** Lock the read, then drive the picture from it. The voice is usually the weakest link, so spend your care there.
3. **Budget the words.** About 2.5 words per second; 20-23 words is the ceiling for an 8-second clip. Short lines act better.
4. **One emotional register per clip.** A big turn gets its own shot, and the cut does the acting.
5. **Start already speaking, already facing.** Never open a dialogue clip on a turn.
6. **In the edit, play the clip's own embedded audio.** The model re-times the delivery when it bakes the lips; your original file no longer matches them.
7. **Shoot coverage.** Singles, over-the-shoulders and listening shots. The listener carries half the scene and hides your worst sync.
8. **Clone only voices you have written consent for** (handbook 15).

## Why performance is the hardest realism problem

We are wired to read faces. Anyone feels a smile that arrives a beat late, or eyes that stay still while the mouth works. Video models make four recurring performance errors:

| Failure | What it looks like | Why it happens |
|---|---|---|
| Stock emotion | "Sad" becomes wet eyes and a trembling lip on every face | The model averages the word toward its most common picture |
| Over-playing | Bug-eyed surprise, grins that fill the face | Intensity words stack and nothing tells the model to hold back |
| Dead eyes | The mouth moves; eyes and brow stay frozen | Sync drives the mouth region; nothing drives the rest of the face |
| Late drift | Sync and expression hold for 4 seconds, then slip | Models degrade toward the end of a clip (realism lever 9) |

The hardest format is sustained dialogue drama between realistic humans in ordinary light. Formats that lower the bar (vox-pop, interview, found footage, one line to camera) are easier. Choose your battles in the script.

## Behaviour over emotion

This is realism lever 6. Actors don't play emotions; they play actions, and the emotion leaks out. Direct the model the same way.

| Tool | What you write | Example |
|---|---|---|
| **Task** | Something the hands do that the line interrupts or ignores | "keeps drying a mug that is already dry" |
| **Eyes** | Where they look, and when they look away or back | "eyes on the mug for the first sentence; looks up on the last word" |
| **Listening** | What the silent character does while the other speaks | "stops chewing; doesn't look up" |
| **The tell** | One small physical giveaway of the hidden feeling | "thumb worries the ring on her finger" |
| **Subtext** | The line says one thing, the behaviour another | Line: "I'm fine." Behaviour: sets the cup down too carefully |

Rewrite every emotion word before it reaches a prompt:

| Instead of | Write |
|---|---|
| "She is heartbroken" | "She folds the letter smaller and smaller and doesn't read it again" |
| "He is nervous" | "He checks the door, then his watch, then the door" |
| "He is angry" | "He speaks quietly and very slowly; his jaw sets between phrases" |

A controlled face with a clear task reads as depth; a crying face reads as a stock photo.

## Directing an AI actor

### Plain named cues, not muscle codes

Name the expression in plain words, give it two or three physical cues, and stop: "quiet relief: shoulders drop, a slow breath out, the start of a smile she doesn't finish."

Don't write FACS action-unit stacks (AU1+AU2+AU5 and so on). The studio ran an A/B on a dialogue close-up in June 2026: the dense AU stack caricatured the emotion into bug-eyed alarm, while a plain named cue ("eager delight: brows lift, a quick grin") produced a believable smile (studio-tested). The follow-up review added the caveat that matters most: judged in motion, not on stills, both styles could over-play. The rule that survived: **understate, name the behaviour, and judge performance in motion, never on a frame grab.**

Useful restraint words: "barely", "the start of", "held back", "a flicker of", "she doesn't let it show". Delete: "very", "extremely", "intense", "dramatic", "emotional".

### One register per clip, a small trajectory inside it

A model can carry one emotional register through a clip, plus one small shift. It cannot carry a big swing: extreme transitions inside a 4-15 second clip go uncanny (studio-tested). So:

- Write the trajectory as **start state, turn word, end state**: "guarded; on 'sold' she stops; flat and final."
- Tie the turn to a word in the script, so the voice and the face turn together.
- Keep the shift small. Laughter to tears is two shots. Cut at the pivot.

### Start already speaking

Open on the line, or one breath before it, with the character already facing where they need to face. A clip that starts on a turn spends its first frames in a mid-rotation smear, exactly when a hook must land (studio-tested). End with half a second of silent tail: "mouth closes after the last word; she holds the look." That tail is your cutting room.

### State the eyeline every time

Every dialogue prompt says where the eyes go: "off-camera left, just past the lens, never into it." Leave it out and models drift to camera. Only a presenter or a deliberate fourth-wall break looks down the lens.

## Writing dialogue for AI

AI dialogue fails on density first. Write lines that fit the clip.

| Clip length | Word budget (about 2.5 words/s) | Notes |
|---|---|---|
| 3 s | 6-7 words | A reply, a question, a reaction |
| 5 s | 10-12 words | Kling talking heads get jerky above 12-15 words per 5 s (studio-tested) |
| 8 s | 18-20 words | 20-23 words is the comfortable ceiling (studio-tested) |
| 12-14 s | 30-35 words | The practical limit for one audio-driven clip; split anything longer |

- **Short lines act better.** People interrupt, trail off and answer questions with questions. Write that.
- **Cut exposition.** If a picture can carry it, the line shouldn't (handbook 02).
- **Ask for an unhurried pace.** Voices and video models both rush (studio-tested).
- **Split long speeches at breaths**, each clip ending on a complete phrase. One speaker per clip is easiest to fix.

**Lines that cross a cut repeat.** When a line is meant to span clip N and clip N+1, the model often generates the whole line in both, and the viewer hears it twice. Mute clip N+1's audio and trim its head harder (0.5 s instead of 0.1 s) (studio-tested). Don't fix it by re-voicing: the same words in a different voice is worse.

## The four dialogue routes

| Route | How it works | Strength | Weakness | Use for |
|---|---|---|---|---|
| **A. Voice first, audio-driven** | Record or design the line, then feed it to the video model as an audio reference | Locked voice, phoneme-level sync, the face follows real prosody | Only as good as the read; extreme emotion goes uncanny | The default for scripted dialogue |
| **B. Native audio** | The model invents voice and picture in one pass | Fast; breath, head and eyes come from one pass | Casting is a lottery; voices change shot to shot; sync drifts late | Speed, one-liners, background voices, previs |
| **C. Lip-sync in post** | Generate picture, then re-mouth it to new audio | Works on any footage, including real actors | Mouth only: the face keeps the old emotion; can read "dubbed" | Translation, a line changed after lock, fixes |
| **D. Performance capture** | A real performance drives the character | The most directable and human: real timing, eyelines, pauses | Needs a performer, a camera and discipline | Hero moments, emotional close-ups |

Human-timed audio (a real read or a chosen TTS take) driving picture through A or D is the most convincing. A model inventing the delivery (B) is fast but rarely believed on a hero line.

### Route A: voice first, then audio-driven generation

The studio's canonical dialogue method since May 2026, using Seedance's audio-reference role (studio-tested). Seedance 2.5 takes up to 10 audio references (verified Sep 2026); Gemini Omni takes none, so it cannot sync to your voice (verified Sep 2026).

1. **Record or generate the line.** Audition it aloud. Lock the read before any picture spend.
2. **Prep the stem.** Voice only, mono, no music or room, about -16 LUFS with peaks near -3 dBFS, silence trimmed to 0.1 s at each end, under 180 words per minute (studio-tested).
3. **Pad short lines.** Audio under about 1.5 s made generations fail, and failed jobs can still cost credits. Pad to at least 2.2 s and add "mouth closes after the word, silent listening tail" to the prompt (studio-tested, May 2026). Then pad the tail with silence to the clip's full length, or the model fills the gap with invented speech.
4. **Keep each clip to about 14 s or less** (studio-tested on Seedance 2.0). Split longer speeches.
5. **Paste the transcript into the prompt, verbatim.** The model takes timing from the waveform and word boundaries from the text. Leaving it out is the top cause of "the lips said different words" (studio-tested).
6. **Pilot one clip and check it** before fanning out: watch the plosives (p, b, m) and transcribe the take to confirm the words.
7. **In the edit, play the clip's own embedded audio.** The model subtly re-times the delivery when it bakes the lips, so the original file drifts against them, worst on long clips (studio-tested, June 2026). Only narration over B-roll keeps a separate voice track.
8. **About 1 render in 10 comes back with a re-synthesised or pitch-shifted voice** (studio-tested). Don't re-roll. Run that clip's embedded audio through speech-to-speech to the locked voice; timing is kept 1:1, so the lips stay locked.

```bash
# normalise and pad a line to the clip length for upload (here 5 s; never under 2.2 s)
ffmpeg -i 05_sound/dialogue/S05_line.wav -af "loudnorm=I=-16:TP=-3:LRA=11,apad=whole_dur=5" -ac 1 -ar 48000 05_sound/dialogue/S05_line_ref.wav
```

### Route B: native audio generation

Veo 3.1, Kling 3.0, Seedance and Gemini Omni all generate speech with picture; Kling 3.0 Omni adds voice binding and multi-character dialogue (verified Sep 2026). It is the fastest route, and body, breath and face cohere. The costs:

- **Casting is inferred.** One reviewer got an unprompted British accent from Seedance 2.5 until the prompt said "American" (reported, Sep 2026). State accent, age, pitch and pace in every prompt.
- **Voices change between clips.** Convert each clip's audio with speech-to-speech to one cast voice; that is how the studio voiced its multishot ads (studio-tested).
- **Sync drifts late.** Veo 3.1 lip sync drops toward the end of clips (studio-tested). Use the best seconds.
- **Native sync is not locked.** If lips and voice are out by a constant amount, nudge that clip's audio by 100-250 ms and it snaps. If the drift grows through the clip, re-drive the lips from the audio (route A) or lip-sync it (route C) (studio-tested).

### Route C: generate, then lip-sync in post

Lip-sync models replace the mouth region to match new audio. The current example, sync-3, detects obstructions such as hands and mics and works at 4K (verified Sep 2026). Use it for translation, a line changed after picture lock, or one bad word.

The limit is structural: only the mouth and jaw change. Brows, eyes and body keep the original emotion. Record the new line in the same register as the old one, and never use lip-sync to turn a calm take into an angry line.

### Route D: performance capture

A person performs the scene to a phone and that performance drives the character. Runway Act-Two takes a character image or video plus a 3-30 s driving performance, with controls for expression intensity (1-5) and body motion, and it moderates recognisable public figures (verified Sep 2026). Luma Ray3.2 transfers performance for up to 8 faces (verified Sep 2026).

Pair it with speech-to-speech: record the performer's voice with the take, then convert it to the character's voice. The timing is kept, so the lips stay locked and every pause is human. This is the director's route: you can give a note ("slower on the second line") and get it. Shooting the driving performance: handbook 11.

## Voice casting and design

Cast voices like faces: against the character bible, with auditions.

| Source | Use it for | Notes |
|---|---|---|
| **Designed voice** (e.g. ElevenLabs Voice Design) | Fictional characters | Built from a text description; no consent problem (verified Sep 2026) |
| **Expressive TTS with audio tags** (e.g. Eleven v3) | Directed reads | Bracketed tags such as [sighs], [whispers], [laughs], [worried] act as direction, not words (verified Sep 2026). Generate 3-4 takes per line and choose, like a VO session |
| **Text to Dialogue** | Two-handers that need natural turn-taking | Up to 10 voices and 2,000 characters per request, with a seed for repeatable takes (verified Sep 2026) |
| **Your own recorded voice** | Timing, rhythm, real pauses | Record in a soft, quiet space (a wardrobe full of clothes works), then convert |
| **Speech-to-speech** | New timbre, same performance | Keeps timing 1:1 (studio-tested) |
| **Cloned voice** | A real person who consented in writing | Handbook 15 first. Professional cloning includes a voice-verification step (verify before cohort) |

Speech-to-speech rules the studio paid to learn (studio-tested, Apr-June 2026):

- **Pick the conversion model by the target voice's language**: the English model for English voices, the multilingual model for Arabic. Multilingual on an English voice lets the source bleed through.
- **Turn on background-noise removal** for every conversion.
- **Extract from the original render, never a muted intermediate**, or you convert silence into a silent mix.
- **Level voices once, over the assembled dialogue track** (handbook 08).

**The narrator must sound distinct from every on-screen voice** (studio-tested). If the voice-over and a character share a timbre, the audience assumes the character is narrating. Change gender, age, register or distance: a close, dry narrator against roomier on-screen voices.

## Pronunciation

- **Initialisms:** write "A.I." with periods to force the letters; "AI" is sometimes read as a word (studio-tested).
- **Names and loanwords:** spell them phonetically in the text the voice model reads ("Siobhan" as "Shiv-awn") and keep the correct spelling in the captions (studio-tested).
- **Fix residual errors on the voice, not the picture.** Regenerate the word and use speech-to-speech so the timing holds (studio-tested).
- **Check with a transcript.** Transcribe the take and compare it to the script word by word.

## Coverage for dialogue

Dialogue is cut, not held. Plan what the editor needs (handbook 03):

- **Singles** of each speaker, matched in size and lens across the reverse.
- **Over-the-shoulders (OTS)** to tie both speakers into one space.
- **Listening shots:** at least one reaction per exchange. A listening shot lets you cut away from weak sync, shorten a line or hide a seam (realism lever 10).
- **An insert** every 8-10 seconds of dialogue (hands, the object in question) to compress lines invisibly (studio-tested).
- **Eyeline match:** if A looks off-camera left, B looks off-camera right, at the same height.
- **The 180° rule:** keep the camera on one side of the line between the speakers for the whole scene, and record it in `continuity.md` (handbook 05).
- **J and L cuts:** start a line over the previous shot (J) or run it over the listener (L). An L-cut over a reaction is the cheapest sync fix there is (handbook 09).

The transition hard rule still applies: never hard-cut two separate generations of the same subject at the same size and angle. Change size, move the angle 30° or more, cut on action, or cut away (handbook 06 covers native multishot coverage).

## Weak vs strong: a dialogue shot prompt

Scene: Maya tells her brother she has sold their late father's house. Shot S05, medium close-up, 6 seconds.

**Weak**

```
Emotional scene. A sad woman tells her brother she sold their late father's house.
She is heartbroken and crying, very emotional. AU1+AU4+AU15, intense sadness.
Realistic, cinematic, 8K. She says: "I sold it. I signed everything this morning,
the house is gone and there's nothing you can do about it now."
```

What's wrong: emotion words plus an AU stack (stock, over-played grief); 21 words crammed into 6 seconds; no task or eyeline, so she talks to camera; no audio instruction, so the model casts a stranger; no identity or room reference.

**Strong** (route A; the voice was recorded first as `[sighs] I signed the papers this morning. The house is sold.`, 10 words, 4.1 s)

```
@image1 Maya: identity reference. @image2 the kitchen at dawn: location reference.
@audio1 exact speech timing and voice for lip sync.

Medium close-up, 50mm, eye level, locked off with a very slow push-in.
Maya, early 40s, stands at the kitchen counter drying a mug that is already dry.

Script (matches @audio1 verbatim): "I signed the papers this morning. The house is sold."

Performance: already speaking at the first frame. Eyes on the mug through the
first sentence. On "sold" she stops drying, sets the mug down and looks up at
her brother, off-camera left, just past the lens. Guarded, then flat and final.
Jaw set, no tears. Natural blinks. Mouth closes after the last word; she holds
his look through the silent tail.

Light: cold window light from camera left, warm under-cabinet strip behind her.
Audio: voice from @audio1 only. No music, no added words, no other voices.
Constraints: identical to @image1, same room as @image2, no scene change,
never looks into the lens.
```

Why it works: a task carries the grief; the eyeline is stated and tied to the turn word; one small trajectory; 10 words in 6 seconds leaves a head and a tail; a verbatim transcript; an audio block that stops the model inventing sound. Draft it cheaply, lock the take, then promote it and check the lips again on the final (whether sync survives draft-to-final promotion unchanged: verify before cohort).

## In the studio

Skills:

- `/film-studio:performance-voice`: picks the route per line, casts voices, preps stems (normalise, trim, pad), runs speech-to-speech and fills the Voice table in `05_sound/sound_plan.md`.
- `/film-studio:prompt-director`: writes the dialogue prompt with verbatim transcript, behaviour, eyeline and audio block.
- `/film-studio:shot-designer`: plans singles, OTS, listening shots and inserts, and checks the 180° line.
- `/film-studio:take-doctor`: diagnoses PERFORMANCE and SYNC failures and picks the cheapest rung of the remedy ladder (keep and cut around first: cut to the listener).
- `/film-studio:editor`: routes each clip's embedded audio and builds J and L cuts.
- `/film-studio:captions`: word-timed transcripts to check what the lips actually said.

Commands:

```bash
# log a take made in a UI with the line as an audio reference
film take add S05 ~/Downloads/maya_s05_a.mp4 --stage draft --tool higgsfield --model seedance-2.0 --mode ref --res 480p --prompt 04_shots/S05/prompt_v2.md

# or by API: inspect the request first (audio-reference field names and roles differ per provider; check the model page)
film gen S05 --via ark --model <seedance-2.5-id> --prompt-file 04_shots/S05/prompt_v2.md --image 02_design/characters/maya/refs/face_34.png --image 02_design/locations/kitchen_dawn.png --image-role reference_image --audio-ref 05_sound/dialogue/S05_line_ref.wav --draft --duration 6 --dry-run

# did the lips say the script?
film captions transcribe 04_shots/S05/takes/S05_t002.mp4 --lang en

# verdicts with codes
film take rate S05_t001 reject --fail SYNC --note "lips late from 3.5 s, growing drift"
film take rate S05_t002 select --note "audio nudged +160 ms in the edit"

# promote the locked draft
film gen S05 --via ark --model <seedance-2.5-id> --from-draft S05_t002
```

## Drills

1. **Behaviour rewrite (10 min).** Rewrite five emotion-word stage directions from your script as a task, an eyeline and one tell. Can a partner name the feeling without the word?
2. **Word budget (15 min).** Take a 60-word speech from your capstone. Cut it into clips of 5, 8 and 5 seconds at 2.5 words per second or less, each starting mid-line and ending on a complete phrase. Mark the one turn word in each.
3. **Casting session (20 min).** Design two voices for one character and generate three takes of one line in each, varying one audio tag. Then record the line yourself and convert it to the winner with speech-to-speech. Which timing do you believe?
4. **Sync pilot (20 min).** Push one line through route A at draft resolution. Transcribe it, rate it with a code, and if the offset is constant, fix it with a nudge in the edit, not a re-roll.
