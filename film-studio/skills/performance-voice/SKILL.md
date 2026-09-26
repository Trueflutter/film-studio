---
name: performance-voice
description: Directs performance and dialogue - voice casting and design, generating lines (ElevenLabs v3, text-to-dialogue, your own recording), audio-driven lip-synced generation, native-audio shots, post lip sync, performance capture, speech-to-speech voice swaps, sync fixes and dialogue coverage. Use for any shot where someone speaks or where an emotional close-up must land.
---

# Performance and voice

Read `${CLAUDE_PLUGIN_ROOT}/handbook/07-performance-and-dialogue.md` first; `08-sound.md` for the mix.

## Direct behaviour, not emotion

Models caricature emotion words. For every performance beat write: the inner state (for you) → a task, where the eyes go, what's avoided, one tell (for the model). Name the expression plainly with two or three physical cues ("brows lift, a quick grin", "jaw sets, nods once too quickly") and stop; use restraint words ("barely", "the start of", "held back"). Studio tests: dense facial-coding stacks caricatured faces, and plain cues could still over-play in motion, so ask the director to judge performance in motion, never on a frame. Plan the listener: reaction shots carry scenes.

## Lines

- Budget: about 2.5 words per second; 20-23 words fill an 8-second clip; Kling-style talking heads get jerky above 12-15 words per 5 seconds.
- Start the clip already speaking; never open on a turn to camera.
- Phonetic spelling for names and acronyms ("A.I.", "Sah-kur"); read every line aloud.
- One dialogue line should not span two clips; if it does, the second clip often repeats it: mute that copy and trim its head.

## Voice first (default for lines that matter)

1. **Cast or design the voice** (ElevenLabs voice design or library; or the director's own recording). A narrator must sound clearly different from on-screen voices. Written consent for any real person's voice (`07_delivery/delivery.md`).
2. **Generate the line** (ElevenLabs v3 with audio tags like `[whispers]`, `[laughs]` where they serve; Text-to-Dialogue for exchanges). Generate 2-3 reads; the director picks.
3. **Prepare the audio:** clean, dialogue only, normalised around -16 LUFS; pad every line with silence to the clip's length (never under 2.2 s) so the model doesn't invent gibberish in the tail; keep clips ≤ ~14 s. Save to `05_sound/dialogue/<SHOT>_line.wav`.
4. **Audio-driven generation** (e.g. Seedance audio reference). Prompt skeleton:
   ```
   @image1 as character identity reference: [anchor line verbatim]
   @audio1 as the exact speech timing and voice for lip sync
   [Shot size], [lens], [camera]. The character speaks the line to [whom/where].
   Script (matches @audio1 exactly): "[the line, word for word]"
   Performance: [behaviour, eyes, one tell; pace]. Accurate lip sync.
   Light: [source, direction]. Constraints: no extra dialogue, no music, only [name] in frame.
   ```
   The verbatim transcript is essential. Generate 2 per line; pick on performance first, sync second.
5. **In the edit, play the clip's own embedded audio**, not the original file on a separate track: the model re-times delivery, so a floating VO drifts (studio-tested). Only narration over B-roll floats.

## Other routes

- **Native audio** (the model voices it): fast, fine for drafts and throwaway lines; casting is unpredictable. Constant drift → nudge the audio 100-250 ms; variable drift → re-drive from audio.
- **Lip-sync in post** (e.g. sync-3): dubbing and fixes; only the mouth changes, the body keeps its old emotion.
- **Performance capture** (e.g. Runway Act-Two): film the director's own performance and drive the character; then speech-to-speech into the character's voice keeps the human timing. Best for subtle scenes.

## Fixes

- **Voice sounds re-synthesised or wrong timbre:** speech-to-speech the clip's own audio to the locked voice. Choose the model by language (a multilingual STS model for Arabic; the English one for English-only voices). Background-noise removal on; keep timing.
- **Lips land late or early by a constant amount:** nudge.
- **Lines rushed:** "unhurried pace" in the performance; shorter line; longer clip.

## Coverage

Singles, an over-the-shoulder, a reaction per exchange; 180° line and eyelines stated in every prompt; plan one J or L cut per scene (the next line starts under the reaction).

## Log

Voices and lines into `05_sound/dialogue/`; each generated clip logged as a take with the audio file in `refs`. Note voice ids in the character bible.
