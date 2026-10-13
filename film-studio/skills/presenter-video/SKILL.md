---
name: presenter-video
description: Use when the video needs a generated person talking: a presenter, host or anchor, an explainer, a property or product launch presented on camera, a news or update episode, a weekly series with a recurring character, a UGC or yapping-style clip with an AI person, or an AI spokesperson.
---

# Presenter video: a generated person, done properly

The recipe that works: a short, spoken script → one character image → the voice first → short lip-synced clips at different angles and distances → B-roll and motion graphics carrying the middle → the person again for the close. The person is on screen for punctuation, not the whole time.

## 1. Script first (one OK)

- Research when it's news or a real product: verified sources, dates, who can use it. One story, gone into deeply ("what it is, how to set it up, one real example, the catch"), beats a list of headlines.
- Written for the ear: short sentences, contractions, the way a person talks across a table. 2.5 to 3 words a second; a 45 to 60 s piece is 120 to 160 words.
- Hook from something that really happened. Recency and context ("Two weeks ago...", "If you'd like to stay up to date..."). The call to action says what they get and where.
- Mark the on-camera lines: open, one middle beat, close. Everything else is narration over pictures.
- Put the script on a text board or in the chat; wait for the OK.

## 2. Character, then the place (one board each)

- Use the `image-prompt` skill: four options on one board (through the director's ChatGPT when connected), the pick made as a **GPT Image 2.5 Sunburst 2K** master on Aristotto.
- Then the **reference pack** as edits of the master: face close-up (the one that keeps the face in video), mid shot, full body, three-quarter, side. Notes in `02_design/<name>.md`. Next episodes: same face, new outfit by editing the master, never by re-describing her.
- The place: where she talks plus the B-roll places, each from several angles of the same space. Never name the city in an image prompt (landmark clichés).

## 3. Voice first

- The `voice-audition` skill: the newest ElevenLabs model only (auto-picked), 3 voices on one line in one board; lighter accents read more natural. Voice the whole script once (one consistent read), then tighten for the platform's pace. Check the transcript word by word.
- Cut the on-camera lines out of the tightened narration, padded with 0.15 s before and silence after to a whole-second clip length.

## 4. Talking clips

- **Seedance 2.5 reference-to-video**: the face close-up plus the pack shot nearest the clip's framing as references, the line as the audio. On Aristotto the audio goes in through the upload card (it doesn't take links); on EvoLink `film gen ... --audio-ref <file>` does it without a card.
- Plan one line per clip with a **different opening angle and distance** each: e.g. arc and push-in from three-quarter / front close-up / low side tracking into close-up. 5 to 11 s each.
- Prompt: "she speaks on camera" in the style, the beat and the constraints; start already speaking; eyes on the lens for a presenter; "mouth closes after the last word"; no music, no text.
- Transcribe each clip; cut out stutters or repeats and cover the cut with a punch-in.

## 5. The middle, B-roll and graphics

For anything over about 45 s, or with graphs, slides or many numbers, plan the layers with the `motion-design` skill first (presenter 15 to 25%, motion graphics 30 to 40%, stills with camera moves, slides, a little B-roll).

- B-roll as multi-angle 10 to 15 s takes (3 to 5 shots each, every cut a different camera move, no face held over 3 s), planned against the narration, used **inside** their shot boundaries.
- Graphics in ONE HyperFrames composition over the assembled edit: notifications, typed fields, counters, connectors, comparisons, each landing on its word (from the word timings). Full-screen graphic scenes where there's no good picture. Brand rules from the director's notes. Lower third with the presenter's full name and the series; no duplicate title tag.
- End on the brand sting built from the real logo file.

## 6. Finish

`film assemble` (picture + dialogue) → HyperFrames render → `film bed align` so the music's payoff lands on the sting → `film mix` with effect cues and ambience → check every cut frame by frame, the transcript and loudness (-14 LUFS) → deliver, with a phone-size copy.
