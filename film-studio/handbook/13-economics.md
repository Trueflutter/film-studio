# 13 · Economics: explore cheap, finish locked

The fear of wasting credits is the most expensive habit in AI filmmaking. It makes people accept the first mediocre generation instead of iterating to a good one. This chapter separates what it costs to *find* a shot from what it costs to *finish* it, so that exploring feels safe and finishing is disciplined.

## The short version

1. **Two budgets.** Exploration (stills and drafts) is where the film is found: spend it, all of it. Production (finals, upscales, fixes) only ever touches locked shots.
2. **Every shot climbs the ladder:** still → draft → lock → final → fix. Skipping a rung is where money burns.
3. **A draft is a cheap direction test.** Lock the take, then promote or upscale *that take*. Never re-roll the prompt at higher quality and hope.
4. **Measure cost per usable shot**, not cost per generation. A $0.51 draft you learn from is cheaper than a $2.84 final you reject.
5. **Change one variable at a time.** Random re-rolling teaches you nothing and costs the same.
6. **Three strikes, then redesign.** A strike is the same failure coming back after a one-variable fix. Three on the same approach means a different design, not a fourth roll.
7. **Fix in post before you regenerate.** Trimming, reframing and cutting away cost nothing.
8. **Know your numbers.** `film cost` after every session.

## Why fear is the real cost

Students who are afraid of spending do two things: they generate once and accept what they get, or they spend their premium credits on the first idea and have nothing left to explore. Both produce mediocre films. Professionals generate a lot: a solo commercial director reported 300-400 generations for about 15 usable clips (reported, 2025); Higgsfield's feature *Hell Grind* kept roughly 1% of images and 1.5% of videos (vendor-reported, 2026). The ratio isn't the point. The point is that **the finished shot is the survivor of many cheap experiments**, and the experiments are part of the craft.

The fix is structural: make experiments cheap enough that you can run many of them, and make premium renders conditional on proof.

## The ladder

| Rung | What you decide | Typical cost | Stage in the log |
|---|---|---|---|
| **1. Still** | composition, light, lens, identity, wardrobe | cents per image | `still` |
| **2. Draft** | action, camera move, timing, gross performance, whether the idea works in motion | ~$0.50 per 5 s (Seedance 2.5 Draft at 480p) | `draft` |
| **3. Lock** | this is the take; write down why | free | verdict `select` |
| **4. Final** | resolution, skin, fine texture | **default: upscale the locked take** (~$0.40 per 5 s); promote to 1080p (~$2.84 per 5 s) for hero shots and close-ups | `upscale` / `final` |
| **5. Fix** | the last 5%: a region edit, a lip-sync repair, a cleanup | varies | `fix` |

Prices: BytePlus ModelArk list for Seedance 2.5, 5-second clip without video input (reported Sep 2026; ByteDance's savings claims reproduce exactly from it). The Draft Mode mechanism itself is verified in ByteDance's own SDK. Other routes charge 2x more or less for the same model; check handbook 16 and `filmkit/rates.json`.

### What a draft can and can't tell you

| A 480p draft reliably shows | A 480p draft does NOT reliably show |
|---|---|
| composition and blocking | skin texture and pores |
| the camera move and its timing | small text, signs, screens |
| the action and its readability | hands and fingers in detail |
| the gross performance (the turn, the look away) | micro-expressions |
| whether the shot does its job | faces in a crowd |
| cut points and rhythm | lip-sync precision on hard consonants |

So: judge the *direction* on the draft; judge the *surface* on the final.

### When 480p is enough, and when a premium final is justified

480p (or a draft tier) is enough for: exploring, animatics and motion animatics, boards in motion, client concept approval, the EX6 spot, internal reviews, and any shot that will sit under 1.5 seconds in a fast cut behind grain and motion.

A premium final is justified when **all three** are true:
1. the shot is **locked** (a `select` draft or still exists and the reason is written down);
2. the shot **needs** the resolution: a close-up face, a held shot over about 3 seconds, a hero product shot, a big-screen deliverable, or a client master;
3. no cheaper path gets there: upscaling the locked draft (roughly $0.08/s for a video upscale, reported Sep 2026) doesn't hold up on the face or texture.

## Linked drafts vs re-rolls (this matters)

Not every "cheap version" predicts the expensive one.

| Mechanism | Does the draft predict the final? |
|---|---|
| **Seedance 2.5 Draft Mode** (launched 22 Sep 2026): a `draft` render at 480p returns a task id; the final is rendered *from that task* at 1080p, reusing prompt, references, seed, duration, ratio and audio | **Yes** for composition, camera and motion. Local textures, small text and crowd counts can still change. Re-check faces and text on the final. The draft id is valid for 7 days (reported). Mechanism verified in ByteDance's SDK, Sep 2026 |
| **MiniMax H3 "Regenerate to 2K"**: re-renders the chosen 768p take at 2K | Yes, by construction (it's conditioned on the take) (verified Sep 2026) |
| **Upscaling a locked take** (Topaz and similar) | Yes: it *is* the take, sharper. Least creative setting on faces. |
| **Cheap tier vs premium tier of a different model** (Veo Fast/Lite vs Veo, Kling Standard vs Pro, Runway Turbo vs full) | **No.** Different model or mode = a different sample. A re-roll, not a draft. |
| **Same prompt and seed at a higher resolution** | **No.** A different resolution means different noise; the composition changes. |

Seedance 2.0 does not have Draft Mode (the API rejects the parameter). As of 24 Sep 2026 fal exposed no draft flag for Seedance; BytePlus ModelArk, Higgsfield and Runway ("Enhance Draft") do (reported). Where no linked draft exists, use the other predictive paths: lock composition with a still first, draft motion on a cheap engine, then either upscale the locked take or render the final from the same start frame and accept that it is a new roll (budget 1-3 attempts).

### The Seedance 2.5 flow in the studio

```
# 1. drafts (480p, cheap): change one variable between them
film gen S03 --via ark --model <seedance-2.5 model id> --prompt-file 04_shots/S03/prompt_v2.md \
  --image 04_shots/S03/start_v2.png --image 02_design/characters/maya/refs/face_34.png \
  --duration 5 --draft --count 2      # start frame first (pins the shot), identity reference second

# 2. review and lock
film dailies
film take rate S03_t004 select --note "the hesitation before she turns the phone over"

# 3. promote the locked draft to the 1080p final (inherits prompt, refs, seed, duration)
film gen S03 --via ark --from-draft S03_t004
```

The final is logged as stage `final` with a note `from S03_t004`, so `film cost` knows it was earned.

## The numbers that matter

`film cost` reports these after every session. Learn to read them.

| Metric | What it tells you | Healthy for a student capstone |
|---|---|---|
| **Cost per experiment** | exploration spend ÷ exploration takes | $0.05-0.60 |
| **Cost per usable shot** | total spend ÷ shots with a `select` | $3-8 (about $6 for a shot with 6 drafts and one promoted 1080p final; less when the final is an upscale) |
| **Takes per usable shot** | all takes ÷ shots with a `select` | 4-10 (more on hero shots) |
| **Iterations before lock** | takes up to and including the first `select`, per shot | 3-8; over 10 means redesign the shot |
| **Exploration / production split** | where the money went | 60-75% exploring |
| **Finals kept** | finals selected ÷ finals rendered | over 70%; lower means your drafts aren't predicting your finals |
| **Premium with no approved draft** | finals rendered without a `select`/`maybe` draft before them | zero |
| **Most common fail code** | your most expensive habit | a different one each production |

**The worked maths behind "drafts first."** Four attempts straight at 1080p: 4 × $2.84 = $11.37. Four drafts and one promoted final: 4 × $0.51 + $2.84 = $4.90. That's 57% cheaper, and you saw four variations instead of guessing. At 20 attempts it is 77% cheaper (BytePlus list prices; ByteDance's claims reproduce exactly from them).

## Planning a budget

In `03_board/generation_plan.md`, before generating:

| Line | Share of a $60 capstone |
|---|---|
| Look development (stills, boards, reference packs) | 10-15% |
| Motion drafts | 50-60% |
| Finals and upscales (locked shots only; upscale by default, promote hero shots) | 15-25% |
| Fixes and pick-ups | 5-10% |
| Reserve | 10-15% |

**Hero shots** (no more than about 20% of the film: the emotional peak, the product reveal, the ending) may take three times the average per-shot budget. Everything else is designed and edited to hide: shorter holds, motion, inserts, grain.

**Stop rules** (write one per shot): after N drafts without convergence, simplify the action, change the angle, split the shot, replace it with an insert, or cut it. Three strikes on the same approach is always a stop.

## Habits that save the most money

1. **Stills before motion.** Composition and light cost cents to find as images.
2. **Variation sprints.** Generate 4 deliberately different options (lens, angle, light, performance) at once, then converge. Divergent first, convergent second.
3. **Generate 2, pick 1** for any engine with high variance (e.g. multishot that sometimes forgets to cut).
4. **Change one variable at a time** and write it in the prompt file name (`prompt_v3_85mm.md`).
5. **Round durations up and trim in the edit.** A 5-second generation cut to 2.5 seconds is normal.
6. **Upscale locked clips instead of regenerating for resolution.** Regenerating re-rolls the approved performance and costs far more.
7. **Fix in post first.** Crop, reframe, flip (only if nothing asymmetric shows), speed, cut away, region-edit a frame.
8. **Reuse assets.** Reference packs, location plates, voices, room tones and music are built once per production and reused in every shot.
9. **Batch with Claude.** Queue drafts for a whole scene while you do sound; review in `film dailies` with verdicts and codes only.
10. **Log everything.** Unlogged spend is how budgets disappear.

## In the studio

- `film take add ... --stage still|draft|final|upscale|fix --cost X` for anything made in a web UI; `film gen` logs automatically using `filmkit/rates.json`.
- `film take rate <take> select|maybe|reject --fail CODE` after every review.
- `film cost` (and `--save` into `04_shots/cost_report.md`); `film cost --check` exits with code 2 when the production is over budget (use it in a Claude Code hook as a budget guard).
- `film dailies` to review takes like a director.
- Skills: `prompt-director` (routes each shot to a draft path and a final path), `take-doctor` (decides re-roll vs change vs redesign), `studio` (enforces the ladder).

## Drills

1. **The draft challenge (20 min).** Spend exactly $3 on one shot at draft tier: at least five drafts, one variable changed each time. Lock one and write why. Compare the locked draft with your first draft.
2. **Predictiveness test (20 min).** Promote one locked draft to final. Make two lists: what held, what changed. Add the list to your style bible under "draft behaviour".
3. **Read your numbers (10 min).** Run `film cost` on EX1-EX2. Which fail code cost you most? Write the habit that would have prevented it.
4. **Budget a capstone (15 min).** Fill `generation_plan.md` for your capstone with hero shots marked, draft budgets and stop rules, total and reserve.
