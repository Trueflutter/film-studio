# 16 · Tool landscape (as of 26 Sep 2026)

AI tools change monthly: between June and September 2026 the leaderboard top three turned over, Seedance 2.5 gained a draft mode and Sora's API closed. This is the one dated page in the handbook: every other chapter teaches the capability and workflow and points here for names, routes and prices. Re-verify it before each cohort with the 30-minute checklist at the end.

**Tags.** (verified Sep 2026): confirmed in the course research from code, repos, official docs or cross-checked figures. (studio-tested): our own productions. (reported): vendor, reseller or third-party claim. (verify before cohort): uncertain. Tables carry the tag in the last column.

## The short version

1. Choose by job, then by tool. The job doesn't change; the tool list does.
2. Core stack: Claude Code, plus one all-in-one UI (Higgsfield) and/or one API route (BytePlus for Seedance 2.5 drafts, fal for breadth).
3. Drafts are only predictive on purpose-built paths: Seedance 2.5 Draft, MiniMax H3 Regenerate, or upscaling a chosen take. Everything else is a re-roll.
4. Faces and close-ups finish at 1080p or above.
5. Leaderboards are a taste signal, not a routing table.
6. Price from the provider's live page on the day. The same model can cost twice as much on another route.
7. Prefer official APIs and MCP servers. Resellers are cheap rails, not licensors.
8. Any fact not re-checked in the last 30 days is (verify before cohort).

## 1. Story and writing

| Capability | Recommended | Alternatives | Notes |
|---|---|---|---|
| Concept, treatment, script, ad script | Claude in Claude Code with a structured workflow: bible, beat sheet, scene cards, continuity ledger, critique passes (`story-engine`, handbook 01) | NovelCrafter, Sudowrite (prose-first) | No specialised tool found that beats this for screen writing (reported, Sep 2026) |
| Screenplay format | Fountain, then Final Draft, Highland or WriterSolo | Arc Studio, WriterDuet | Final Draft's current AI features (verify before cohort) |
| Serial and micro-drama season planning | Claude | Sherpa by Pocket FM (optional elective) | See below |

**Sherpa: the verdict.**
- Launched publicly 18 Sep 2026 (verified Sep 2026). Web app, "free to try"; limits unknown (verify before cohort).
- Built for long serialised prose and audio drama running to hundreds of episodes. No screenplay, shot-list or ad output evidenced (reported).
- Evidence gaps: no independent review (only a sponsored #ad), no verifiable samples, no method behind its "fewest canon violations" claim, no terms or IP policy seen, unknown export formats (reported).
- **Use:** optional micro-drama elective only: plan a season in Sherpa, convert to scene cards and script in Claude. First, a 60-90 minute instructor check of sign-up, terms, export and episode length, plus one blind comparison with Claude.
- Its best idea is already in the kit: the continuity ledger tracks who knows what, reveal order, and open setups and payoffs (handbook 05).

## 2. Stills and look development

| Job | Recommended | Alternatives | Notes | Confidence |
|---|---|---|---|---|
| Identity-locked stills, wardrobe, edits | GPT Image 2 (Apr 2026); GPT Image 2.5 shipped 8 Sep 2026 (`flare` fast, `sunburst` precise) | Nano Banana 2 / Pro | Up to 16 inputs. Best on wardrobe (studio-tested); edits soften skin, locations skew yellow. 2.5 claims better light, texture and reference fidelity at the same price: test it live | reported |
| Faces, multi-turn edits | Nano Banana 2 (`gemini-3.1-flash-image`, GA 28 May 2026) | Nano Banana Pro for 4K and complex frames | Up to 14 inputs, 6 at high fidelity; aspect 1:8 to 8:1; takes video as input. About $0.067 per 1K image, Pro $0.134 | verified Sep 2026 (specs); reported (prices) |
| Look development, mood | Midjourney V8.2 (default since 24 Jul 2026) | Seedream 5, FLUX.2 | Edit Model in public test since 27 Aug 2026: up to 4 references, replaces Omni and Character Reference. No official API (verify before cohort). Not for identity lock | reported |
| Creatures, style range | Seedream 5.0 Pro (12 Aug 2026) | | Up to 14 references; about $0.045 per image | reported |
| Photoreal texture, open LoRAs | FLUX.2 [pro / flex / max] | FLUX.2 [klein] 4B (Apache-2.0) | $0.03-0.07 per first megapixel (Jul 2026). [dev] and [klein] 9B are non-commercial | verified Sep 2026 (licences); reported (prices) |
| In-world text: signs, props | Ideogram 4.0 (3 Jun 2026, open, Apache-2.0) | GPT Image 2 | About $0.03 per image. On-screen titles still go in post | reported |
| Clean a frame, no restyle | Qwen-Image-Edit-2511 / Qwen-Image 2.0 (Apache-2.0) | Nano Banana 2 ("upscale, change nothing") | Our clean-up for frames pulled from 720p video | studio-tested |
| Commercially safe stills | Adobe Firefly Image 5 + Custom Models | | Indemnity on qualifying enterprise plans only (handbook 15) | reported |

**Retired:** Reve API shut down 14 Aug 2026; Luma Photon retired in favour of Uni-1/1.1; FLUX 3's image tier had no public endpoint in early September (all reported).

## 3. Character consistency

| Approach | Use when | Tools | Notes | Confidence |
|---|---|---|---|---|
| Reference pack + multi-reference (**default**) | Fictional characters in a short or an ad | 3-image sheet (3/4 face close-up, headless full body front, full body back) plus a text descriptor; GPT Image 2/2.5, Nano Banana, Seedream 5 | Field routing, Aug 2026: faces to Nano Banana 2, wardrobe to GPT Image 2, creatures to Seedream 5, locations to Higgsfield Soul Cinema | reported |
| Higgsfield Soul ID | A recurring face across many stills in Higgsfield | Trains from 5-20 face photos in minutes, paid plan | Held identity through Kling multishot; drifted on wardrobe against GPT Image 2 (May 2026) | verified Sep 2026; studio-tested |
| Higgsfield Elements | Reusable @Character, @Location, @Prop | Cinema Studio 3.0: 9 images, 3 videos, 3 audio, 12 files max | | reported |
| LoRA or custom model | A consenting real face across hundreds of images; a very unusual design; an open pipeline | ai-toolkit on FLUX.2 [klein] 4B or Qwen-Image; fal and Replicate trainers; Firefly Custom Models | Dataset curation is the real cost. Check the base model's licence | verified Sep 2026 (licences) |

## 4. Video generation

### Routing matrix by job

| Job | First choice | Alternatives | Why | Confidence |
|---|---|---|---|---|
| Photoreal close-ups | Seedance 2.5 at 1080p via Draft → Final | Seedance 2.0 4K; Veo 3.1 Standard; Gemini Omni 1.1 1080p; MiniMax H3 2K | Faces expose the 720p ceiling; Kling close-ups show eye flicker (studio-tested) | reported: A/B on day 1 |
| Dialogue, lip sync | Seedance 2.0/2.5 with the voice track as an audio reference | MiniMax H3 (audio refs, 11 languages incl. Arabic, claimed); Kling 3.0 (max 12-15 words per 5 s); Gemini Omni (no audio reference) | Your cast voice drives the mouth | studio-tested |
| Action, physics | Kling 3.0 Pro/4K with motion control | Gemini Omni 1.1; Wan 3.0; Veo 3.1 | Seedance 2.5 blurs in fast motion | reported |
| Product, ad shots | Veo 3.1 Standard, or Seedance 2.5 with product references and a localised edit | Kling 3.0 4K; Luma Ray 3.2 keyframes | Composite real logos and packshots in post | reported |
| Stylised, animation | Kling 3.0 or Seedance with style references | Midjourney video; LTX-2.5 or Wan 2.2 with a LoRA | Open models win for a trained house style | verify before cohort |
| Cheapest drafting | Seedance 2.5 Draft (480p, predicts the 1080p final) | H3 Max Turbo, then Regenerate to 2K; Veo 3.1 Lite; Omni 1.1 at 360p plus upscale; Ray 3.2 at 360p | Only Seedance Draft, H3 Regenerate and upscales carry a chosen take forward | verified Sep 2026 |
| Restyle real footage | Runway Aleph 2 | Luma Ray 3.2 Edit and Reframe; Seedance 2.5 edit; Kling 3.0 Omni V2V; Wan-Animate-2 (open) | Pick by how much of the plate must survive | verified Sep 2026 |
| Camera control | Kling 3.0 (camera control, 6-shot storyboard, motion control to 30 s) | Seedance 2.5 with a moving grey-box video reference; Cinema Studio presets; Ray 3.2 keyframes; first/last frame on Veo or Omni | A static floor plan is ignored; a moving blockout works (studio-tested) | reported |

### Per-engine notes

| Engine | What to know | Confidence |
|---|---|---|
| **Seedance 2.5** | 4-30 s; 480/720/1080p (no API 4K); up to 30 image, 10 video, 10 audio references; T2V, I2V, reference, edit, extend; always outputs audio. **Draft Mode (22 Sep 2026):** a 480p draft, then a 1080p final from the draft's task id, reusing prompt, references, seed, duration and ratio. Camera, blocking and motion carry; text, hands and crowd faces can change, so re-check them. Draft ids last 7 days. Weak on fast motion, two-hand work, and voice casting without an audio reference (reported) | verified Sep 2026 |
| **Seedance 2.0** | 4-15 s; the only Seedance 4K tier; up to 12 references; proven audio-reference dialogue; no draft mode | verified Sep 2026; studio-tested |
| **Kling 3.0 / Omni / Turbo** | 3-15 s; 720p, 1080p, 4K; multishot up to 6 shots per generation; native audio; motion control to 30 s; no seed, so every run is a re-roll | verified Sep 2026 |
| **Veo 3.1 / Fast / Lite** | 4-8 s; up to 4K (not Lite); 16:9 and 9:16. Fast and Lite are separate models: re-rolls, not drafts. Lip sync fades late in clips (studio-tested) | verified Sep 2026 |
| **Gemini Omni 1.1 Flash** (27 Aug 2026) | 3-10 s per call, chains to 40 s; 360p to 4K; first/last frame; edit, extend; no audio reference; 16:9 and 9:16 only; SynthID; non-deterministic | verified Sep 2026 |
| **MiniMax H3 / H3 Max** | H3: open weights (local use excluded in the US, EU, UK and South Korea), native 2K, stereo audio; Regenerate to 2K re-renders a chosen 768p take. H3 Max: fal's post-trained variant (1 Sep 2026), 480/768p, about 3 s to render 5 s, reads Blender playblasts as motion reference | verified Sep 2026 (specs); reported (quality) |
| **Wan 3.0** | API-only beta (Aug 2026); 2-30 s up to 1080p; top of the no-audio arena; weak lip sync and text; not open weights | reported |
| **LTX-2.3 / 2.5** | Open weights; 2.5 up to 4K with audio and LoRA training; LTX-2.3 3DREAL render-to-real LoRA (26 Jun 2026) | verified Sep 2026 |
| **Runway Aleph 2 / Gen-4.5 / Act-Two** | Aleph 2 (21 May 2026): restyle, relight, add or remove, new angle on 2-30 s of real footage. Gen-4.5 generates. Act-Two drives a character image from a performance video. Runway also hosts third-party models | verified Sep 2026 |
| **Luma Ray 3.2** | 5 or 10 s; up to 1080p; 21:9; keyframes (16 per clip per Luma's launch post, 2-64 in the API node: verify before cohort); Edit, Reframe, Extend; no native audio | verified Sep 2026 |

**Gone:** the Sora API closed on 24 Sep 2026; strip it from any skill or workflow that still names it. Veo 2 and 3.0 were deprecated in ComfyUI on 26 Aug 2026 (both verified Sep 2026). No evidence "Veo 4" exists. Midjourney video and Moonvalley Marey (verify before cohort).

### Leaderboards: taste signal only

Artificial Analysis Video Arena, text-to-video, snapshot from after 26 Aug, retrieved 26 Sep 2026 (reported):

| Rank | Without audio (Elo) | With audio (Elo) |
|---|---|---|
| 1 | Wan 3.0, 1335 | Gemini Omni Flash, 1233 |
| 2 | Gemini Omni Flash, 1332 | Wan 3.0, 1229 |
| 3 | MiniMax H3, 1302 | MiniMax H3 Max (fal), 1227 |
| 4 | HappyHorse 1.0, 1286 | MiniMax H3, 1220 |
| 5 | HappyHorse 1.1, 1272 | Seedance 2.0 720p, 1210 |

The top three sit within 33 Elo: a tie. Arena votes judge first impressions of short clips, not identity lock or lip sync.

## 5. Platforms and routes

| Route | What it is | Strengths | Watch out | Confidence |
|---|---|---|---|---|
| **Higgsfield** | All-in-one UI, MCP (`mcp.higgsfield.ai/mcp`, OAuth), CLI, skills plugin; credits | Cinema Studio, Soul ID, Elements, Topaz upscale, Seedance 2.5 Draft (24 credits per 8 s at 480p vs 52 at 720p) | MCP and CLI jobs spend credits even on "Unlimited" plans (re-check the newer "Unlimited MCP" offer); credits don't roll over; plan prices vary by source | verified Sep 2026 (MCP, CLI); reported (credits) |
| **BytePlus ModelArk** | ByteDance's official Seedance API | Home of Draft Mode; list prices | Reportedly not sold in the US, Canada, UK, Australia or New Zealand; onboarding friction | verified Sep 2026 (Draft); reported (regions) |
| **fal** | API marketplace, 600+ models; hosted MCP with cost lookup | Breadth; H3 Max; 3DREAL; Topaz | No Seedance draft flag as of 24 Sep 2026 | verified Sep 2026 |
| **EvoLink** | Cheap reseller, one async API | Low prices, wide catalogue | Result links expire after 24 h; unofficial Suno and Midjourney routes; real-person filter trips on photoreal start frames (studio-tested); Draft support unknown | verified Sep 2026 |
| **Runway** | Own models plus a third-party hub; Media Router (23 Jul 2026) picks a model by quality, speed or cost | Aleph 2, Act-Two, Seedance 2.5 "Enhance Draft" | Output links expire after 24 h | verified Sep 2026 |
| **Replicate** | API marketplace with a hosted MCP | Breadth | | reported |
| **Official APIs** | Gemini API (Veo 3.1, Omni, Nano Banana, Lyria); Kling developer API (prepaid packages; consumer plans include no API); Luma API | First-party terms | Kling's MCP status (verify before cohort) | reported |

### Price table (USD per second of output)

Research-pass figures. Re-price on the provider's page before you budget, and update `filmkit/rates.json`.

| Model | Route | Resolution | $/s | Date | Confidence |
|---|---|---|---|---|---|
| Seedance 2.5 draft | BytePlus list | 480p | ~0.10 | Sep 2026 | reported (savings claims reproduce from it) |
| Seedance 2.5 | BytePlus list | 720p | ~0.23 | Sep 2026 | reported (savings claims reproduce from it) |
| Seedance 2.5 final | BytePlus list | 1080p | ~0.57 | Sep 2026 | reported (savings claims reproduce from it) |
| Seedance 2.5 | EvoLink | 720p | 0.293 | 22 Aug 2026 | reported |
| Seedance 2.5 | fal | standard | ~0.30 | Aug 2026 | reported |
| Seedance 2.0 Fast / Standard | EvoLink | 720p | 0.161 / 0.199 | Apr 2026 | studio-tested (billed) |
| Kling 3.0 | official API | 1080p | 0.112 silent, 0.168 with audio | Sep 2026 | verified Sep 2026 |
| Kling 3.0 | official API | 4K | 0.42 | Sep 2026 | verified Sep 2026 |
| Veo 3.1 Standard | Gemini API | 720p/1080p | 0.20 silent, 0.40 with audio | Sep 2026 | verified Sep 2026 |
| Veo 3.1 Fast | Gemini API | 720p | 0.08-0.15 (sources differ) | Sep 2026 | verify before cohort |
| Veo 3.1 Lite | Gemini API | 720p | 0.03-0.05 | Sep 2026 | verified Sep 2026 |
| Gemini Omni Flash | Gemini API | 720p | ~0.10 | Jun 2026 | reported |
| MiniMax H3 Max | fal | 768p | 0.08 | 1 Sep 2026 | verified Sep 2026 |
| Wan 3.0 | Alibaba list | 480/720/1080p | 0.05 / 0.10 / 0.20 | Aug 2026 | reported |
| Luma Ray 3.2 | ComfyUI partner node | 720p / 1080p | 0.06 / 0.24 | Sep 2026 | verified Sep 2026 |
| Runway Gen-4.5 | Runway API | | 0.12 | Aug 2026 | reported |
| Runway Aleph 2 | Runway API | matches input | 0.28 (56-credit minimum) | Aug 2026 | reported |
| Topaz video upscale | fal | 1080p | ~0.08 | Sep 2026 | reported |

A 5-second Seedance 2.5 experiment costs about $0.51 as a 480p draft and $2.84 at 1080p. Four drafts plus one final: about $4.90, against $11.37 for four finals (57% less; ByteDance's claim reproduces exactly from list prices).

### Weak vs strong: a tool fact

| | Fact |
|---|---|
| **Weak** | "Seedance is about 30 cents a second and it's the best model." |
| **Strong** | "Seedance 2.5 at 720p: ~$0.23/s on BytePlus list (reported Sep 2026), ~$0.30/s on fal (reported, Aug 2026). Not in the arena top five on 26 Sep 2026. Still our first choice for close-ups, via Draft → Final at 1080p, because the draft predicts the final's camera and blocking." |

Route, resolution, date, tag, reason. Write every tool claim in your generation plan that way.

## 6. Voice, lip sync, music, SFX

Workflows: handbook 07 (performance and dialogue) and 08 (sound). Rights: handbook 15.

| Need | Recommended | Alternatives | Notes | Confidence |
|---|---|---|---|---|
| Voices, dialogue | ElevenLabs Creator ($22/month, $11 first month): Eleven v3 audio tags, Voice Design, Text to Dialogue | Runway TTS | Starter ($6) is the commercial minimum; professional cloning from Creator; API WAV needs Pro | verified Sep 2026 |
| Re-voice, keep timing | ElevenLabs speech-to-speech | Runway speech-to-speech | Timing preserved 1:1, so lip sync holds | studio-tested |
| Lip-sync fix, localisation | sync-3 | LatentSync (open) | About $0.04-0.133/s by API; free tier | verified Sep 2026 |
| Performance capture | Runway Act-Two | Luma Ray 3.2 Modify; Wan-Animate-2 (open) | 3-30 s driving video | verified Sep 2026 |
| Music, client-safe | Library music; Adobe Firefly Generate Music (GA 20 Aug 2026); ElevenLabs Music v2.5 (11 Sep 2026; self-serve excludes film and TV) | Stable Audio 2.5/3.0; Lyria 3.5 (4 Sep 2026, ~$0.08 a song, SynthID) | | reported |
| Music, creative and social | Suno v6 (9 Sep 2026): Pro $10 (20 downloads a month), Premier $30 (60) | | New terms 3 Sep 2026; UMG and Sony complaint 18 Sep 2026 | verified Sep 2026 (terms); reported (prices, lawsuit) |
| SFX, ambience | ElevenLabs SFX v2 (0.5-30 s, seamless loops) | Firefly sound effects; libraries | MMAudio and ThinkSound are non-commercial | verified Sep 2026 |
| Transcripts | ElevenLabs Scribe | WhisperX (local, free) | | verified Sep 2026 |

## 7. Edit and finish

| Job | Recommended | Alternatives | Notes | Confidence |
|---|---|---|---|---|
| Rough cut, mix, captions, QC, delivery | `film` | | Frame-exact assembly from `06_edit/cut.txt` | studio-tested |
| Edit and grade | DaVinci Resolve (free or Studio) | Premiere Pro (Runway plugins for Adobe, 17 Sep 2026); CapCut | We run Resolve 20.x; whether 21 has shipped (verify before cohort) | reported |
| Titles, cards, animated text | HyperFrames (the `graphics` skill; Apache 2.0, Claude Code plugin `hyperframes@hyperframes`) | Remotion (official skills; Claude Code plugin since 16 Jul 2026; free up to three employees, then a paid company licence); editor titles | Text never lives in the generation. Transparent MOV renders go on each shape with `film overlay` | verified Sep 2026 (HyperFrames 0.8.81); studio-tested (Remotion) |
| Upscale locked clips | Topaz via Higgsfield `upscale_video` (about 4 credits a clip) or fal (~$0.08/s at 1080p) | Magnific (stills) | Desktop Topaz is subscription-only since Oct 2025 | studio-tested |
| Frame rate | Runway Enhance Frame Rate (17 Sep 2026) | Topaz | Interpolate only after picture lock | reported |

## 8. Previs

| Job | Recommended | Alternatives | Notes | Confidence |
|---|---|---|---|---|
| Boards | Nano Banana 3x3 grid | Cinema Studio grids; LTX Studio; Midjourney for mood | Panels are low-res: isolate and upscale | reported |
| 3D blocking | Blender 5.2 LTS with pre-built scenes, or driven by Claude through Blender MCP | Previs Pro; Unreal | A 24 fps playblast becomes the motion reference | verified Sep 2026 |
| Render-to-real | LTX-2.3 3DREAL (fal endpoint, open weights) | H3 / H3 Max reference-to-video; Seedance 2.5 with the playblast as video reference | Weeks old: re-test 7-10 days before the cohort. A controlled test showed H3 reads the blockout, unwanted foot shuffle included | reported |
| Virtual scouting | World Labs Marble; Tencent HY-World 2.0 (open, strong GPU) | | | verify before cohort |

## 9. Claude Code plumbing

| Server | How to add it | Notes | Confidence |
|---|---|---|---|
| Higgsfield | `claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp` | OAuth; the Higgsfield CLI uses fewer tokens | studio-tested |
| fal | `claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp --header "Authorization: Bearer $FAL_KEY"` | Search models, check cost, run jobs | verified Sep 2026 |
| ElevenLabs | Hosted MCP at `https://api.elevenlabs.io/v1/mcp` (OAuth) | The local open-source server was archived 20 Aug 2026: remove it | verified Sep 2026 |
| Runway | Official `runwayml/runway-api-mcp-server`; hosted at `https://mcp.runwayml.com/mcp` | | verified Sep 2026 (repo); reported (hosted) |
| Luma | First-party `lumalabs/luma-api-mcp` | | reported |

- MCP tool search is on by default, and MCP calls over 2 minutes move to the background, which suits video jobs (verified Sep 2026).
- **Budget-guard hooks:** a PreToolUse hook on `mcp__higgsfield__*` and `mcp__fal-ai__*` blocks generations over a per-student cap; a PostToolUse hook downloads results and logs the take before 24-hour links expire (handbook 13).
- **Plugins** bundle skills, hooks and MCP config: `/plugin marketplace add <org>/<repo>`, then `/plugin install <name>@<marketplace>`. The film-studio kit installs this way; Higgsfield publishes its own skills plugin (verified Sep 2026).
- **Claude plan:** Pro ($20/month) minimum; Max 5x (about $100) recommended for a 4-day intensive (verified Sep 2026).
- **Effort:** set it in `/model`. Medium for small fixes and re-renders; xhigh for a new sequence, a graphic or a review pass; max when the first seconds of a launch must carry it. The widely shared one-prompt motion pieces all ran on xhigh or max (reported Sep 2026).

## 10. Not for this course

- **NVIDIA Cosmos:** research-grade world models for robotics data on data-centre GPUs. One slide at most (verify before cohort).
- **Google Vids:** optional 15-20 minute demo for pitch videos and simple animatics, not for finished films (verify before cohort).

## How to re-verify this page in 30 minutes

Run it the week before every cohort, then change the date in the title.

| Min | Check | Update |
|---|---|---|
| 5 | Screenshot the Artificial Analysis text-to-video and image-to-video boards | Leaderboard; any new top-five model gets a routing test |
| 5 | Price pages: BytePlus Seedance, fal (Seedance, Kling, Veo, H3 Max), Gemini API, Runway API | Price table; `filmkit/rates.json` and its `verified` date |
| 5 | Higgsfield: plans, credits per Seedance 2.5 clip at 480p and 720p, MCP credit policy, Cinema Studio version | Section 5 |
| 3 | Is Seedance Draft on fal or EvoLink yet? Any new predictive draft elsewhere? | Routing matrix, section 5 |
| 4 | Retirements: search "deprecated" for each engine in the matrix; skim the ComfyUI API-node changelog | The "Gone" line |
| 4 | ElevenLabs pricing and music terms, Suno terms and download caps, music litigation news | Section 6, handbook 15 |
| 2 | Run `/mcp`: does every server connect? | Section 9 |
| 2 | `film doctor`, then one `film gen --dry-run` per route | Keys and model ids |

Anything you couldn't check gets (verify before cohort).

## In the studio

- `prompt-director` proposes an engine per shot from the routing matrix and records it in `03_board/generation_plan.md`.
- `take-doctor` uses the matrix at the "change engine" step of the remedy ladder (handbook 12).
- `studio` sets up routes and keys in `.env` and runs `film doctor`.

```
film doctor
film gen S03 --via ark --model dreamina-seedance-2-5-260628 --prompt-file 04_shots/S03/prompt_v2.md --image 02_design/characters/mara/refs/face_34.png --draft --duration 5 --count 2
film take rate S03_t002 select --note "blocking and eyeline right"
film gen S03 --via ark --from-draft S03_t002
film gen S07 --via fal --model <endpoint id from the fal model page> --prompt-file 04_shots/S07/prompt_v1.md --dry-run
film cost
```

The ModelArk id above is the one seen in the research (verified Sep 2026). Copy ids from the provider's model page on the day.

## Drills

1. **Price your capstone (15 min).** From `03_board/generation_plan.md`, price every shot on two routes with the price table. Which route wins per shot, and why?
2. **Route five shots (15 min).** For five shots from your shot list, write the job, first choice, fallback and a one-line reason in the "strong" format above.
3. **Re-verify one row (10 min).** Pick one fact on this page, find the live source, and update the value, date and tag.
