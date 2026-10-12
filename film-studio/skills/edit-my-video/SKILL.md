---
name: edit-my-video
description: Use when the director gives you their own footage to edit: a phone recording, a yapping or talking-to-camera video, a vlog, a talking head, an interview, a screen recording, a travel or product clip, "edit this", "make this look professional", "add captions / b-roll / motion graphics / sound effects", or an edit brief.
---

# Edit my video: own footage into a finished piece

Their real face, voice and timing are the most believable things they have. Your job is to make a plain recording look produced, following their **edit brief**, and to take the initiative where the brief is silent.

## 1. Read the footage first

1. `film new "<title>" --format social --aspect 9:16` (or 16:9 to match the footage), and copy the file(s) into `04_shots/source/`.
2. Transcribe with word timings: `film captions transcribe <file>`. Pick the best take when there are several (clearest words, fewest stumbles, most alive) and say why in one line.
3. Write the **edit plan** to `06_edit/edit_plan.md` as a table: time, words, what we see (them full frame, a punch-in, B-roll, a full-screen graphic, them with a graphic beside them), sound. Show it and wait for one OK. Nothing is generated before the OK.

## 2. The edit brief (fill the gaps yourself)

The director may give some of these; propose the rest in the plan:

- **Cut:** remove dead air, false starts and "ums". Jump cuts get a punch-in (about 1.15x) or a cutaway, never a bare jump. Keep breaths that carry meaning.
- **Hook:** the first second, already moving: the strongest line first, a bold on-screen hook line, or a punch-in.
- **Captions:** word-by-word, 2 to 4 words per card, safe zones (top 220 px, bottom 380 px, right 180 px on 9:16), highlight the key word, never over another graphic.
- **Punch-ins:** on the words that matter, alternating closer and wider so no stretch is one size.
- **B-roll:** on nouns and places, generated multi-angle takes (Seedance 2.5) cut **inside** their shots, never longer than the line they cover. No B-roll on emotional lines: stay on the face.
- **Motion graphics** (HyperFrames, one composition with the edit underneath): for each one, say *what* appears, *on which word*, *where*, *how it moves* (springs in, types, counts up, draws, wipes), *how it leaves*, *in what style*. Numbers count up, lists stack, comparisons split, steps connect. Brand colours and fonts from the director's notes; one accent colour.
- **Sound:** a whoosh on cuts and transitions, a pop or tick on each graphic, ambience under B-roll, music ducked under the voice and lifted at the end. `film mix` with `--cues` and `--duck-db`.
- **End:** an end card or call to action built in code; their logo file if they have one, never a generated logo.

## 3. Build

1. `film assemble` the base edit (picture + their voice) from the plan; it keeps B-roll inside its shots and lands cuts on exact frames.
2. Generate B-roll on Aristotto (one card per batch), log with `film take add`, then reassemble.
3. One HyperFrames composition: the base edit as the bottom track, every graphic and caption on top, landing on its word from the transcript. Use the `hyperframes` skills (`/talking-head-recut` is the closest workflow) and the `graphics` skill's rules.
4. Snapshots at every cut, every graphic and the first second; fix the worst problems before the director sees anything.
5. Mix and render; check loudness (-14 LUFS for social) and that every word still transcribes.

## 4. Notes

Ask for one note at a time, in edit language: "the price lands half a second late", "punch in on 'free'", "less music under the second line". Change one thing per round and say which.
