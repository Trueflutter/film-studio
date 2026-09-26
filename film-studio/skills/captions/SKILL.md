---
name: captions
description: Makes captions and subtitles that look finished - transcription with word timings, authored caption lines checked against the audio, the house caption look (bold type, soft stroke behind the fill, blurred shadow, no box, spoken-word highlight), readability checks, safe zones, burn-in, sidecar SRT, Arabic/RTL captions, and an animated Remotion caption track for premium work. Use for any captions, subtitles, SRT, burnt-in text on a cut, or a language version.
---

# Captions

Captions are part of the picture. Done well they read instantly, sit clear of faces and platform buttons, and feel designed. This skill carries the studio's tested caption craft so you don't rebuild it each time. Background: `${CLAUDE_PLUGIN_ROOT}/handbook/14-qc-and-delivery.md` (captions QC).

## The house look

Bold geometric sans (bundled Poppins Bold; IBM Plex Sans Arabic Bold for Arabic), white fill, a soft dark stroke painted *behind* the fill, a separate blurred drop shadow, no box. Social style highlights the word being spoken and reveals words as they're said, with the line's layout fixed so nothing jumps. Clean style shows the phrase at once with a short fade. Film style is quiet festival subtitling.

## Workflow (filmkit, needs only ffmpeg with libass)

Captions go on last: after the mix, the master and `film deliver`, once per delivered shape (a 9:16 frame needs different line lengths and position from a 16:9 one). The master stays caption-free.

1. **Get word timings** from the *master* (the final mix), never a draft; once is enough for every shape:
   ```
   film captions transcribe 07_delivery/masters/<slug>_master.mp4 --lang en [--speakers 2]
   ```
   (ElevenLabs Scribe; needs `ELEVENLABS_API_KEY`.) Or use any word-timed JSON (WhisperX, Scribe, `{text,start,end}`), or an SRT (timings then estimated per word).
2. **Proof the transcript.** Names, brand terms, dialect and loanwords are where transcription goes wrong. Fix meaning, not timing.
3. **Author the lines** in `06_edit/captions.txt`, one caption per line, in order, covering every spoken word. Rules:
   - Break on phrases, never inside a fixed phrase or name ("artificial / intelligence" split across captions reads broken).
   - Social: 2-4 words per caption, one idea each. Clean: up to ~7 words. Film: up to 2 lines of ≤ 42 characters.
   - New speaker, new caption. Try not to run a caption across a picture cut.
   - Drop trailing full stops and commas at the end of a caption; keep ? and !.
   - Numbers as digits; spell brand names the brand's way.
4. **Build and check**, per shape (`--video` sets the frame size, `--out` names the files):
   ```
   film captions build 07_delivery/masters/<slug>_master.words.json --lines 06_edit/captions.txt --style social \
     --video 07_delivery/masters/<slug>_9x16_v001.mp4 --out 07_delivery/masters/<slug>_9x16 [--accent "#F5C542"] [--y 0.66]
   ```
   The build matches every authored line against the transcript in order: word mismatches are printed for you to check (usually the transcript's mistakes); if a line mostly doesn't match, it stops, because lines have drifted from the audio. It writes `<name>.social.ass` (styled) and `<name>.srt` (upload this to platforms as closed captions) and runs the readability check (≤ 17 characters/second, ≤ 42 characters/line, ≤ 2 lines, ≥ 0.83 s on screen, no flicker gaps).
5. **Burn in and look**:
   ```
   film captions burn 07_delivery/masters/<slug>_9x16_v001.mp4 07_delivery/masters/<slug>_9x16.social.ass
   film frames 07_delivery/masters/<slug>_9x16_v001_captioned.mp4 --at 1.2,4.5,9.8
   film qc 07_delivery/masters/<slug>_9x16_v001_captioned.mp4
   ```
   Look at frames at several caption times: nothing covers a face, a product or on-screen text; clear of the 9:16 platform zones (top ~15%, bottom ~20%, right-edge buttons). Check costume prints, signs and screens against the caption band for the *whole* film and move the band once (`--y`) rather than per shot.

## Choosing a style

| Platform / use | Style | Notes |
|---|---|---|
| Reels, TikTok, Shorts (9:16) | `social` | accent colour from the brand; `--y` around 0.62-0.70 |
| Feed ads (1:1, 4:5), LinkedIn | `social` or `clean` | many watch muted: captions are the script |
| Films, festivals, YouTube 16:9 | `film` | also upload the `.srt` |
| Talking-head explainers | `clean` | calmer, full phrases |

## Arabic and other right-to-left scripts

- Author the lines (never auto-group Arabic by word count); the tool warns if you don't.
- The bundled IBM Plex Sans Arabic Bold is used automatically; the stroke sits behind the fill so joined letters don't show seams.
- Phrase-at-once is used for RTL (per-word effects can break joining and reading order).
- Transcribe dialect with more than one engine when accuracy matters; the words the engines disagree on are the ones a native speaker must check.
- Mixed-script tokens join correctly with a tatweel ("وبالـAI").
- **Check one burnt frame.** Arabic shaping needs a libass built with HarfBuzz (standard Homebrew ffmpeg has it). If letters appear as boxes or disconnected, use the Remotion route below.

## Premium route: animated captions in Remotion

For motion-graphic captions (word pop, brand-coloured "signal words", custom fonts, captions integrated with titles), use `${CLAUDE_SKILL_DIR}/remotion/CaptionTrack.tsx` in a Remotion project:
1. `npx create-video@latest captions --blank` (or use an existing Remotion project); `npm i @remotion/google-fonts`.
2. Copy `CaptionTrack.tsx` into `src/`; build events with `film captions build ... --lines ...` and convert the words JSON to the component's `events` prop (Claude can write that conversion), or pass the words directly.
3. Register a composition at the video's size and fps with the cut as `<OffthreadVideo>` underneath, or render the captions alone on a transparent background and overlay them.
4. Render with PNG frames and BT.709 colour to avoid banding on gradients and colour shifts against the footage (studio-tested): `npx remotion render <id> out.mp4 --image-format=png --color-space=bt709`.
All animation in Remotion must derive from the frame number (`useCurrentFrame`, `interpolate`, `spring`), never CSS transitions or timers.

## Sidecar and accessibility

Always deliver the `.srt` alongside burnt-in versions: platforms index it, and viewers can turn it off. For accessibility versions, include meaningful sound cues in brackets ([door slams]).
