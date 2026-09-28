# 08 · Sound

Viewers forgive a soft frame when the sound is right, and reject a perfect frame when the room sounds wrong. AI video hands you pictures with a guide track at best; the space, the contact of hands and feet, and a mix that leaves room for the voice are yours to build. It is your cheapest realism lever (lever 11, the sound of the space).

## The short version

1. **Generated clip audio is a guide track, not the mix.** Keep what's locked to picture (usually the voice) and rebuild the rest.
2. **Keep stems separate until the final mix:** dialogue, room tone, ambience, foley, hard effects, music.
3. **One continuous room tone per location, under every cut.** It makes separate generations feel like one place.
4. **Foley at every contact point:** feet, hands, cloth, cups, doors.
5. **Drop the music under the key line.** Silence (room tone, never digital zero) is a tool.
6. **Choose music by licence first, sound second.** Log tool, plan, date and download for every track.
7. **Mix dialogue first; everything else fits around it.** Master to the delivery spec, then check on a phone speaker.
8. **Plan sound per scene in `05_sound/sound_plan.md` before you generate.**

## Sound is half the picture

Sound does three jobs picture can't:

- **It extends the world.** Off-screen traffic or a neighbour's door makes a world bigger than your 5-second frame.
- **It glues the seams.** A continuous bed and a J-cut carry the ear across two generations that don't quite match.
- **It gives weight.** A heavy door sounds heavy even when the picture floats (lever 5).

Model audio is not a mix. It is usually near-mono, bakes voice and effects together, changes room from clip to clip, and smears the sharp transients of contact sounds. Use it as the dialogue source when it is locked to the lips (handbook 07), as a timing reference for spotting effects, and as animatic scratch. Isolate the voice; replace the rest.

## The stems

| Stem | What's in it | Folder | Why separate |
|---|---|---|---|
| Dialogue | On-screen lines and voice-over | `dialogue/` | Levelled once; drives the music ducking; removed for the M&E |
| Room tone | The room with nobody talking | `ambience/` | Glues cuts; fills gaps so silence isn't a dropout |
| Ambience | The world outside: traffic, birds, wind, crowd | `ambience/` | Sets place and time; changes at scene boundaries |
| Foley | Human contact: steps, cloth, hands, props | `sfx/` | Sync-critical; gives weight and presence |
| Hard effects | Doors, cars, phones, impacts | `sfx/` | Story events, often motivated off-screen |
| Music | Score, source music, stings | `music/` | Ducks under dialogue; its licence is tracked separately |

Folders are under `05_sound/`. Separate stems let you fix one layer alone, duck the music under the voice, deliver an M&E (music and effects, no dialogue) for translation, and swap one track if its licence fails. Work in 48 kHz WAV and name files so they sort: `TITLE_DIA_v03.wav`.

## Room tone and ambience per location

Every generated clip has its own noise floor, so a cut between two clips of one room audibly changes rooms. Isolate the dialogue from each clip, then lay **one continuous room tone for the whole scene** underneath.

- **Get the tone.** Record 30 seconds or more of a real room with everyone silent, or generate a loop. Text-to-SFX tools make seamless ambience loops (ElevenLabs SFX v2: 0.5-30 s with a loop option, verified Sep 2026). Loop it to the scene's length:

```bash
ffmpeg -stream_loop -1 -i 05_sound/ambience/kitchen_tone_loop.wav -t 32 05_sound/ambience/kitchen_tone_32s.wav
```

- **Describe it physically:** size, surfaces, machines. "Small tiled kitchen, fridge hum, faint wall clock, no voices."
- **Layer ambience in two or three levels:** a continuous bed (distant traffic), occasional events (a passing car), one motivated specific (a dog bark after the line). More becomes mush.
- **Change ambience at scene boundaries**, usually as a J-cut: the next location arrives half a second to a second before its picture.

## Foley at contact points

Most AI films skip foley. Every time a body touches the world, the ear expects a sound. Spot the picture shot by shot and list the contacts:

| Contact | Examples | Tip |
|---|---|---|
| Feet | steps, a scuff, weight shifting on a floorboard | Match surface and shoe; hear the stop |
| Hands | cup on counter, keys, paper, a phone set down | The hit lands on the frame the object touches |
| Cloth | a jacket as an arm moves, a sleeve on a table | Quiet, but its absence reads as dubbed |
| Props | spoon in a cup, a pen click, a zip | One clean hit beats three smeared ones |
| Doors and furniture | handle, latch, chair scrape | Heavy objects need low end |

Native audio usually misses these or smears them. Generate or pull clean hits and place them on the frame.

## Sound perspective

Match the sound to the camera's distance. A close-up voice is close and dry; in a wide it is quieter, with more room. Voice-first stems and TTS are all close and dry, so a wide needs a small level drop and a touch of room reverb, or the voice sounds pasted on. Keep perspective consistent per shot size. Off-screen sounds sit lower and softer, with less top end.

## Silence as a tool

The loudest moment in a scene is often the quiet one. **Drop the music under the key line** so the words land alone. Film silence is never digital zero: it is room tone. A true dropout reads as a fault (`film qc` flags dead air over 1.5 s below -50 dB). A subjective trick: let one sound in the room stop at the turn (the fridge hum cuts out) and the audience leans in.

## J and L cuts

A **J-cut** starts the next shot's sound before its picture; an **L-cut** runs the current sound over the next picture. In AI films they hide model seams (continuous sound carries the ear across a visual mismatch), carry a line over the listener's reaction (which also covers weak sync), and pull the audience into a new scene. Cutting them: handbook 09.

## Sonic branding and stings

For ads, a sonic logo (a 2-4 second signature) stays identical across a campaign and lands on the cut to the end card. If the logo animation ships with its own sound and your music bed carries the outro, mute one; never play two endings (studio-tested). Lift the bed when the talking stops: the studio's spot ran the music about 7 dB higher under the silent outro than under dialogue (studio-tested). Let the last note ring, then hold a beat of room tone before black.

## Music

### Score the arc, not the genre

Brief music from the emotional arc: where it enters, lifts, drops out and resolves, as timecodes on the cut. Most AI films over-score; wall-to-wall music tells the audience how to feel and flattens every beat. Start later than you think, drop out under the key line, land the payoff on a cut.

Decide the role first: underscore (outside the story), source music (a radio in the room, so it needs perspective) or a sonic logo.

### Briefing a music model

```
Role: underscore under dialogue, 45 s, instrumental only, no vocals, no humming.
Arc: patient and uncertain; lifts at 0:28 (the reveal); warm resolve by 0:40.
Instrumentation: felt piano, soft analogue pad, low cello from 0:28. No drums.
Register: dialogue-friendly low register, sparse, lots of space.
Tempo: 72 BPM. Key: G major.
Structure: [Intro] sparse piano · [Verse] pad enters · [Bridge] cello lift · [Outro] resolve and ring out.
```

- **"Dialogue-friendly low register" is load-bearing.** It keeps the harmonic content below about 1 kHz, out of the voice's way (studio-tested, Apr 2026).
- **70-75 BPM** suited patient, cinematic beds under conversation (studio-tested).
- **Use the tool's structure controls** (section tags such as [Intro] and [Outro] in Suno, studio-tested; section-by-section composition plans in ElevenLabs Music, verified Sep 2026) to put the lift where the cut needs it.
- **Describe sound, never artists.** Name instruments, register, tempo and space. Artist names add licence risk.
- **Audition under the real dialogue**, never solo.

### Landing a chorus on a cut: extend by whole bars

When the lift arrives too early, don't time-stretch the track. Repeat whole bars before it (studio-tested, Sep 2026):

1. **Find the bar length.** One 4/4 bar lasts 4 × 60 / BPM seconds, so four bars at 107 BPM last 8.972 s. The studio confirmed the loop length to the sample by correlating 2-second windows around the splice.
2. **Splice where the music matches on both sides.** A high-correlation point joins cleanly; a point where the arrangement changes jumps.
3. **Join with a short equal-gain crossfade** (about 15 ms). Both sides are the same music, so an equal-power fade bumps the level at the join.
4. **Check the landing with the same rule you used on the source.** A quick peak check "found" the chorus half a second early because the pre-chorus tail still peaked; the onset rule did not.

Bonus: a pre-chorus rest can land in the pause after the last line and set up the hit on the end-card cut.

### Cutting picture to the beat

Montage, hooks and campaign spots feel driven when the cuts land with the music. Dialogue scenes don't work that way: the performance sets the cut and the music follows.

- **One beat lasts 60 / BPM seconds:** 0.5 s at 120 BPM, 0.83 s at 72. The tempo is in your music brief or the track's listing.
- **Cut on the beat, or a frame or two before it.** A cut slightly ahead of the beat often feels more in time than one exactly on it; try both.
- **Save the biggest change for a downbeat**, the first beat of a bar: the reveal, the product, the cut to the end card.
- **Check it:** `film review --bpm 120 --offset 0.42` lists every cut against the grid ("beat 7 on", "beat 9 -2f"). The offset is where the first beat falls in the cut; find the first strong transient on your editor's waveform.

### Licensing is a first-class decision

Choose by what the client and platform allow, then by sound. Ranked by safety for client work:

| Rank | Source | Status (dated) | Client-work verdict |
|---|---|---|---|
| 1 | Stock libraries, human composers | Human-made, contractually licensed | Default for hero pieces, broadcast and festivals. Check use, term and territory |
| 2 | Adobe Firefly Generate Music | GA 2026-08-20; described as commercially safe, licensed, instrumental (verified Sep 2026). IP indemnity only on qualifying enterprise plans (reported) | Safest turnkey generator for ads |
| 3 | Stable Audio | 2.5 trained on a licensed dataset (verified Sep 2026). 3.0 (2026-05-20) partly open-weight, community licence free under $1M revenue; indemnity with Enterprise (reported) | Very safe with Enterprise; best for beds and ambience |
| 4 | ElevenLabs Music | Self-serve paid plans: commercial use except film, TV and games; film/TV needs Enterprise; free plan non-commercial (verified Sep 2026). v2.5 on 2026-09-11 (reported) | Online ads and social only on self-serve. A festival or broadcast short counts as film |
| 5 | Google Lyria | Lyria 3.5 on 2026-09-04 (reported). SynthID watermark on every track (verified Sep 2026). No published music-specific training or indemnity statement (reported) | Social content; legal sign-off before broadcast |
| 6 | Suno v6 | Launched 2026-09-09 (verified Sep 2026). Terms from 2026-09-03: Pro 20 downloads a month, Premier 60; commercial rights only for downloads within the plan allowance; free-tier songs never gain rights (verified Sep 2026). UMG and Sony filed a new suit targeting v6 on 2026-09-18 (reported). Suno's own help centre warns fully AI music may not be copyrightable (verified Sep 2026) | Low-stakes social only, with the client's informed, written acceptance. Not for risk-averse brands |
| none | Udio | Downloads disabled since late October 2025; walled garden (reported) | Can't supply a deliverable |

- **The terms govern, not the pricing page.** ElevenLabs' music marketing mentions film and TV; its terms exclude them on self-serve plans.
- **Log every track:** tool, model version, plan tier, generation date, prompt, download receipt and permitted use, in the Music brief of `sound_plan.md` and the provenance log (handbook 15).
- **Never register generated music with Content ID** or a "protect my audio" service on client work; false claims can hit the client's own uploads.
- **Never upload copyrighted audio as a reference.**

## Sound effects: generation and licence traps

- **Text-to-SFX:** ElevenLabs SFX v2 (0.5-30 s, loops, a prompt-influence control; verified Sep 2026) and Adobe Firefly Generate Sound Effects (GA 2026-08-20, described as commercially safe; verified Sep 2026). Prompt like a foley artist: object, material, action, distance, room. "Ceramic mug set down on a wooden counter, close, small kitchen, single hit."
- **Video-to-audio** models watch the clip and make synced sound, and the best open ones are licence traps: MMAudio's weights are non-commercial (CC BY-NC 4.0), ThinkSound's README prohibits commercial use, and HunyuanVideo-Foley's licence does not apply in the EU, UK or South Korea (all verified Sep 2026). Class experiments only. For client work use Firefly, ElevenLabs, Stable Audio Enterprise or library effects.
- **Generated hits are weakest on sharp, layered transients.** For a hero door slam or a punch, a library effect usually wins.

## Cleanup

- **Isolate voices** from model audio (this strips noise, music and baked-in effects) before you use, convert or lip-sync them. API examples: ElevenLabs Voice Isolator and Runway voice isolation (verified Sep 2026); Resolve Fairlight and iZotope RX do the same on the desktop (verify before cohort).
- **Don't over-process.** Heavy enhancement makes a voice sound synthetic; blend in the original.
- **Level voices once**, over the assembled dialogue track, never per clip (studio-tested).

## The mix

Build it in this order: dialogue, then room tone and ambience, then foley and effects, then music. Every decision serves intelligibility.

### The studio recipe (studio-tested, Apr-Sep 2026)

| Step | Setting | Why |
|---|---|---|
| Dialogue | Loudness-normalise the assembled track: -16 LUFS, true peak -1.5 dBTP, LRA 11 | Consistent voices before anything else |
| Music base | -18 dB; 1.5 s fade in, 2 s fade out | Sits under, not with |
| Duck | Sidechain from dialogue: threshold 0.05 (about -26 dB), ratio 8, attack 20 ms, release 500 ms | Hard duck when anyone speaks; natural recovery without pumping |
| Sum | `amix` with `normalize=0` | Default `amix` divides every input by the input count, so adding a bed quietly turns your voices down |
| Master | Gain to the delivery target, limiter with headroom so true peak stays under -1 dBTP | Meets spec without squashing dynamics |

The ducker is a safety net. On a hero line, ride the music down (or out) by hand in the music stem before mixing.

### Loudness targets

| Destination | Integrated loudness | True peak |
|---|---|---|
| Social (TikTok, Reels, Shorts) | -14 LUFS (common practice; platforms publish no spec, verify before cohort) | ≤ -1 dBTP |
| Web and YouTube | -14 to -16 LUFS | ≤ -1 dBTP |
| EU broadcast, EBU R128 | -23 LUFS | ≤ -1 dBTP |
| US broadcast, ATSC A/85 | -24 LKFS | ≤ -2 dBTP |

These are the published standards; a broadcaster's written delivery spec overrides them. `film qc --spec social|web|broadcast` checks -14, -16 or -23 LUFS (±1 LU). The broadcast check uses a -2 dBTP ceiling, so one master clears both peak limits. For ATSC, mix with `--target -24` and check with `--spec cinema-ish` (-24 LUFS, -2 dBTP).

### Check on a phone

Most of your audience hears the film through a phone speaker with no bass. Play the master on a phone at arm's length. Is every word clear? Does the music mask the voice? Did the low-end drama (a rumble, a bass hit) vanish? If dialogue gets lost, lower the music or thin its low-mids; don't just raise the master.

### How `film mix` implements it

`film mix` is the recipe as one command:

- `--video cut.mp4` with no `--dialogue` uses the cut's own audio as the dialogue stem: right for voice-first clips, whose embedded audio is lip-locked (handbook 07), once their voices are isolated. `--dialogue` supplies a separate stem instead; `--ignore-video-audio` drops the cut's audio.
- Dialogue is normalised (-16 LUFS, -1.5 dBTP, LRA 11) and also keys the ducker.
- `--music` sits at `--music-db` (default -18), fades in and out, and ducks with the studio sidechain settings. When dialogue stops, it recovers to its base level: that is your outro lift.
- `--ambience` beds sit at `--ambience-db` (default -24) and don't duck. `--fx` plays at the level you exported.
- `--ambience` and `--fx` repeat, so you can layer as many beds and effects stems as you need.
- Everything is summed with `normalize=0`, trimmed to the picture, then gain-matched to `--target` (default: the production's loudness, -14 for ads and social, -16 for films) behind a limiter set to -1.5 dB sample peak (headroom for inter-sample peaks, so true peak stays under -1 dBTP), re-measured until within 0.3 LU.
- It writes a versioned WAV to `05_sound/mix/` and a copy of the cut with the new audio beside it; the picture is copied, not re-encoded.

**Every stem starts at 0:00 of the cut.** Export beds and effects from your editor as cut-aligned WAVs, or place a file with `adelay` (milliseconds, one value per channel); start a bed half a second early for a J-cut. Beds must run as long as their scene: `film mix` pads short files with silence; it doesn't loop them.

```bash
# kitchen tone under scene 2 (starts 0:14), a mug hit at 0:27.4
ffmpeg -i 05_sound/ambience/kitchen_tone_32s.wav -af "adelay=14000|14000" 05_sound/ambience/AMB_s2_kitchen.wav
ffmpeg -i 05_sound/sfx/mug_down.wav -af "adelay=27400|27400" 05_sound/sfx/FX_s2_mug.wav

film mix --video 06_edit/cuts/cut_v004.mp4 \
  --music 05_sound/music/bed_v2_extended.wav --music-db -20 \
  --ambience 05_sound/ambience/AMB_s1_street.wav \
  --ambience 05_sound/ambience/AMB_s2_kitchen.wav \
  --fx 05_sound/sfx/FX_foley_v03.wav --fx 05_sound/sfx/FX_s2_mug.wav
film qc 06_edit/cuts/cut_v004_mix_v001.mp4 --spec web
```

## Weak vs strong: a scene's sound plan

The template `05_sound/sound_plan.md` holds a stems table, one row per scene (room tone, ambience, foley, effects, music in/out, silence), a voice table, the music brief and mix targets. Here is one scene.

Scene 2 (0:14-0:46): Maya tells her brother Dan she has sold their late father's house (handbook 07). Shots: S04 wide, S05 Maya MCU (the line), S06 Dan listening CU, S07 mug insert, S08 Dan's reply over Maya's shoulder.

**Weak**

```
Scene 2: kitchen sounds. Sad piano music throughout. Dialogue from the clips.
```

"Kitchen sounds" can't be spotted or sourced. Music throughout flattens the turn. Dialogue straight from five clips means five different rooms. No silence, no perspective, no licence.

**Strong** (the scene's row and notes in `05_sound/sound_plan.md`)

| Layer | Plan |
|---|---|
| Room tone | Small tiled kitchen: fridge hum, faint wall clock. One 32 s bed under all five shots; voices isolated from every clip |
| Ambience | Dawn birds through a closed window (muffled), distant traffic; one car passes at 0:21. J-cut in 0.8 s before S04 |
| Foley | S04 Dan's steps on lino, chair scrape as he sits. S05 tea towel on the mug; mug set down on "sold" (0:27.4). S06 his hand stops on the table. S08 chair creak as he leans back |
| Effects | Kettle clicks off at 0:17 (motivates the first line). A neighbour's door off-screen at 0:40 |
| Perspective | S04 wide: steps and kettle further back, more room. S05, S06, S08: voices close and dry |
| Silence | 0:27.4-0:30: after "sold" the fridge hum cuts out; room tone only, no music, 2.5 s |
| Music | Enters 0:31 under Dan's reply: low piano, dialogue-friendly low register, 72 BPM; extended by whole bars so the cello lift lands on the cut to scene 3. Source: licensed library track; licence ID, date and permitted use in the provenance log |
| Voice | Maya: designed voice, synthetic (no consent needed). Dan: the student's own read converted with speech-to-speech (self-consent). Narrator: none |
| Mix | Web target -16 LUFS; re-master to the festival's written spec if selected. Checked on a phone |

Every line is something you can source, place on a frame and check.

## In the studio

Skills:

- `/film-studio:sound-design`: writes `sound_plan.md` scene by scene, spots contact points, briefs music and SFX, checks licences, runs `film mix`.
- `/film-studio:performance-voice`: dialogue stems, voice isolation, speech-to-speech (handbook 07).
- `/film-studio:editor`: J and L cuts; the cut the mix sits on.
- `/film-studio:captions`: captions once dialogue is final.
- `/film-studio:qc-review`: loudness, true peak and dead air against spec (handbook 14).

Commands:

```bash
film animatic --audio 05_sound/temp/temp_vo_and_bed.wav     # sound from day one
film mix --video 06_edit/cuts/cut_v004.mp4 --music 05_sound/music/bed_v2.wav
film mix --video 06_edit/cuts/cut_v004.mp4 --dialogue 05_sound/dialogue/dia_v03.wav --ambience 05_sound/ambience/street_60s.wav --target -16
film qc 06_edit/cuts/cut_v004_mix_v001.mp4 --spec web
film deliver 07_delivery/masters/title_master.mp4 --aspects 9:16,1:1
```

## Drills

1. **Spotting session (15 min).** Watch 20-30 seconds of your cut muted. List every contact point, the room tone and the ambience layers with timecodes, and fill that scene's row in `sound_plan.md`.
2. **One room (15 min).** Take three generated clips from one location. Isolate the voices, lay one continuous room tone under all three, and A/B the cut against the native audio. Can you hear the rooms change in the original?
3. **Music brief and licence card (15 min).** Write a music brief for your capstone with the template above, pick a source from the licence ranking for your actual use (online, festival, broadcast), and fill the licence line before you generate.
4. **Mix to spec (20 min).** Run `film mix` with dialogue, music, one bed and one effects stem, then `film qc`. Play it on a phone and adjust `--music-db` until every word survives the speaker.
