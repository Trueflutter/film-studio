---
name: sound-design
description: Plans and builds the soundtrack - scene-by-scene sound plan, room tone, ambience beds, foley at contact points, effects, music briefs with licence checks, and the final mix to platform loudness with `film mix`. Use for anything about sound, SFX, music, scoring, ambience, foley, silence, loudness or the mix.
---

# Sound design

Read `${CLAUDE_PLUGIN_ROOT}/handbook/08-sound.md` first. Model audio is a guide track, not the mix.

## 1. The plan (`05_sound/sound_plan.md`)

Per scene: room tone, ambience, foley at every contact point (feet, hands, cups, doors, cloth), hard effects, where music enters and exits, and where silence carries the moment (drop the music under the key line). Ask the director where the audience should *hear* the story.

## 2. Build the stems

Keep separate files until the mix: `dialogue/`, `ambience/` (room tone 30 s+ per location, beds), `sfx/` (foley and effects), `music/`.
- **Generated effects** (e.g. ElevenLabs sound effects): describe the source, the action, the surface and the space: _"a ceramic mug set down hard on a wooden kitchen table, close, small room, slight rattle of a spoon"_. Loopable ambience for beds. Generate 2-3 and pick.
- **Libraries** for hero hits when they're better.
- Watch licences on open video-to-audio models (several are non-commercial).

## 3. Music

- **Brief:** role (underscore, source music, sonic logo), the emotional arc against the timeline (where it enters, lifts, drops out, resolves), instrumentation, tempo, and for dialogue scenes "sparse, low register, leaves room for the voice".
- **Licence first, taste second.** Record tool, plan, date and permitted use in `07_delivery/delivery.md`. For client and broadcast work prefer licensed or commercially safe sources; check plan terms (download caps, film/TV exclusions) before using generated music. Current landscape and risks: handbook 08 and 16.
- To land a musical hit on a cut, extend or shorten the runway by whole bars (splice at a repeat, short equal-gain crossfade) rather than time-stretching.

## 4. The mix

```
film mix --video 06_edit/cuts/cut_v004.mp4 \
  --ambience 05_sound/ambience/room_tone.wav --ambience 05_sound/ambience/street.wav@2.0 \
  --fx 05_sound/sfx/door.wav@4.2 --music 05_sound/music/score.wav \
  --music-db -18 --ambience-db -24
```
What it does: the cut's own audio is the dialogue stem (voice-first clips are lip-locked, so keep it), normalised to -16 LUFS; music at `--music-db` ducked under it by sidechain compression; beds low; effects at level, each placed with `@seconds`; stems summed without level loss; then gain-matched to the production's loudness (`production.json`: film -16, ad and social -14) behind a limiter (sample peaks at -1.5 dB). Use `--dialogue <stem>` only for a separately cleaned stem, `--ignore-video-audio` to drop the cut's audio, and `--target` only when a written spec differs from the production's.

Run it on the locked cut to hear the mix, then again on the graded export (`cut_v005.mp4`) to make the master; captions go on after delivery, per shape (the `captions` skill).

Targets: social -14 LUFS, web -16, broadcast -23 (EBU R128), true peak ≤ -1 dBTP. Check with `film qc`. Ask the director to listen once on headphones and once on a phone speaker; dialogue must be clear on the phone.

## 5. Common problems

| Problem | Fix |
|---|---|
| sounds fake, "dead" | room tone under everything; ambience per scene |
| weightless actions | foley at the contact point, slightly ahead of or on the frame of impact |
| music fights the voice | lower register, sparser arrangement, more ducking, or cut the music under the line |
| clicks at cuts | 30 ms fades at every join (`film assemble` does this) |
| levels jump between clips | normalise dialogue once over the assembled stem, not per clip |

You can't listen: ask the director what they hear, and use `film qc` numbers (loudness, dead air) as evidence.
