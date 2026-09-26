# 15 · Rights and ethics

AI tools make it trivially easy to put a real face, a real voice or someone else's music into a film, and to publish something that looks like evidence. That ease is why rights work has to be a habit, not a last-day chore: one missing consent form or one uncleared track can get a finished film taken down, a client campaign pulled, or a real person hurt.

> **Practical guidance, not legal advice.** Laws differ by country and change fast. For client work, paid media, broadcast, festivals, or anything involving a real person, get sign-off from a lawyer who practises where you publish.

## The short version

1. No real person's face, voice or performance without their written consent. Classmates included.
2. No public figures, no deceased performers, no real children. The only exception is a licensed route that grants exactly that use.
3. A provider's real-person filter is a consent check, not a technical obstacle. Never try to get around it.
4. Read the licence of everything you publish: plan tier, download caps, what "commercial" covers and what it excludes.
5. Log provenance as you go (tool, version, plan, date, permitted use, receipt or consent) in `07_delivery/delivery.md`.
6. Label AI content where platforms or law require it, and keep watermarks and content credentials intact.
7. Never fake proof: no invented testimonials, no results the product can't deliver, no AI character claiming a real life story.
8. When in doubt: fictional character, designed voice, library music.

## 1. Likeness and consent

"Using" a person covers far more than putting them on screen. Every row below needs written consent.

| Use | Example | What the consent must name |
|---|---|---|
| Face as a reference | a photo in a character sheet or an @Element | reference use, this project |
| Training | Soul ID, a LoRA, a custom model | training, and deletion when consent ends |
| Voice | a clone, a speech-to-speech target, a sample used as an audio reference | cloning or conversion, this project |
| Performance | a classmate acts a take for performance capture | capture and transfer to a generated character |
| Real footage | EX5 plates with people in shot | appearance release |
| Resemblance | prompting "looks like [actor]" | nothing can fix this: don't do it |

Course rules:
- **Written consent before you upload anyone's photo, voice or performance, classmates included.** Use the form in section 10. A verbal "sure" in class is not consent: it must name the project, the uses and how long.
- **No public figures** (politicians, celebrities, athletes, influencers) and **no deceased performers**, except through a licensed route that grants the specific use, such as a voice licensed by its rights holder through the vendor's own marketplace (verify before cohort). "It's obviously a parody" is not a defence to rely on in a class project.
- **No real children's faces or voices.** Keep child characters out of capstones; if the story needs a child, keep them off screen or implied.
- **Fictional faces still need a check.** A face generated from a description can land close to a real person. If a test viewer says "that's [someone]", regenerate. Never put a real name in a character prompt.

**Why providers filter real-person photos.** Face references are how deepfakes, harassment and fraud get made, so vendors block or restrict them. Runway's performance-capture API carries a public-figure moderation threshold (verified Sep 2026). Seedance restricted real-human references at launch and added a separate real-human route later (verified Sep 2026). The studio hit Higgsfield `ip_detected` blocks and an EvoLink "real person photo" filter on photoreal start frames (studio-tested).

When a filter fires:
1. Stop and ask: do I have written consent for this face?
2. If yes, use the provider's sanctioned route for consented likeness (a verified identity feature, a consented training flow, or a real-footage workflow from handbook 11), or ask the instructor.
3. If there is no sanctioned route, change the plan: a fictional character built from a description (handbook 05).
4. **If the face is synthetic and the filter is wrong** (a false positive on a character you designed), take a legitimate path: try another provider or route that accepts synthetic faces; generate the shot text-to-video with the anchor line and the character's references attached as references rather than as the start frame; or ask the provider to review the block. Log it as a MODEL failure with the error text.

Never alter, crop, rename, re-grade or stylise an image to slip it past a filter. It breaches the provider's terms, can cost you the account, and defeats the one safeguard between your tools and someone's face. The studio's older notes held workarounds like this; they are not part of this kit.

## 2. Voice cloning: consent and the class policy

Voice is the most personal asset in a film and the easiest to misuse.

| Voice source | Allowed in class? | Condition |
|---|---|---|
| Designed voice (built from a text description) | Yes | The default for fictional characters: no consent problem |
| Stock voice inside your plan | Yes | Within the vendor's terms for your tier |
| Your own voice | Yes | Fill your own consent form so the log is complete |
| A classmate or friend | Yes | Signed form naming this project, uses, duration and revocation |
| A hired voice actor | Yes | Written agreement that covers AI cloning and reuse, and pay |
| A clip from YouTube, a podcast or a film | **No** | "Public" is not consent |
| Public figures, deceased performers | **No** | Unless licensed for that exact use |

Professional voice cloning on the main platform asks the speaker to pass a voice verification step (verify before cohort). Treat that as the tool enforcing consent, not as a hurdle. In the US, *Lehrman & Sage v. Lovo* (SDNY, 2025) held that voices as such aren't copyrightable but let right-of-publicity and consumer-protection claims go ahead (verify before cohort): "voices aren't copyrighted" does not make cloning one legal. Union agreements such as SAG-AFTRA's require informed consent and pay for digital replicas (verify before cohort).

Speech-to-speech into a designed or licensed voice (handbook 07) is fine. You are changing the timbre of your own or a consented performance, not taking someone's identity.

## 3. Music: the licensing summary

Handbook 08 ranks music sources for client safety. The rules that catch people:

| Source | Commercial use | The catch | Confidence |
|---|---|---|---|
| Stock / production library | Yes, per licence | Check the tier covers paid ads, broadcast or cinema | (verify before cohort) |
| Adobe Firefly Generate Music | "Commercially safe", royalty-free | Instrumental beds; IP indemnity only on qualifying enterprise plans | (reported) |
| ElevenLabs Music, self-serve paid plans | Online and offline commercial use | **Excludes film, TV and studio games**, which need Enterprise. Free plan: no commercial use, must credit | (verified Sep 2026) |
| Stable Audio | Community licence under $1M revenue | Indemnity only with Enterprise | (reported) |
| Google Lyria | Usable for social | SynthID on every track; no published music indemnity | (reported) |
| Suno Pro / Premier | Yes, **only for permitted downloads** | Pro 20 downloads a month, Premier 60, no rollover; stems count as that song's download; free-tier songs never gain commercial rights. UMG and Sony filed a new complaint targeting v6 on 18 Sep 2026 (reported) | (verified Sep 2026) |
| Udio | No | Downloads disabled | (reported) |

**What "commercial use" usually covers:** ads, sponsored and monetised social, client deliverables. **What it often excludes:** film and TV (ElevenLabs self-serve), selling or distributing the track on its own, and registering it with Content ID or "protect my audio" services. Never register AI music from a client ad: false claims can hit the client's own uploads. A short film headed for festivals or broadcast counts as film.

For a client or hero piece: library music, or a commercially safe generator with indemnity. Suno only with the client's informed, written acceptance of the litigation risk.

Licence traps in the wider toolkit:

| Tool | Trap | Confidence |
|---|---|---|
| MMAudio, ThinkSound (open foley) | Non-commercial | (verified Sep 2026) |
| HunyuanVideo-Foley | Licence does not apply in the EU, UK or South Korea | (verified Sep 2026) |
| MiniMax H3 open weights | Local use excluded in the US, EU, UK and South Korea; revenue cap. Hosted APIs have their own terms | (reported) |
| FLUX.2 [dev] and [klein] 9B | Non-commercial licence ([klein] 4B is Apache-2.0) | (verified Sep 2026) |

## 4. Training data and indemnity: questions for client work

A client's legal team will ask these. Ask them first, of every tool in the pipeline:

1. What was the model trained on, and does the vendor say so in writing?
2. Does my plan grant commercial rights to output? Which uses are excluded?
3. Is there IP indemnity? On which plan, with what cap, on what conditions?
4. Who owns the output? Does the vendor train on my uploads and prompts?
5. Are there territory limits on the tool or its licence?
6. Is output watermarked or labelled? (Keep it. See section 6.)
7. Can I get an invoice or receipt showing plan and date?
8. What happens if the model is retired mid-project? (Sora's API closed on 24 Sep 2026.)

**Who offers indemnity (Sep 2026):** Adobe Firefly on qualifying enterprise plans (reported); Stable Audio Enterprise (reported); Google Cloud's generative AI indemnity may cover some models on Vertex (verify before cohort). Moonvalley's Marey video model was marketed as trained only on licensed footage, but its current availability is unclear (verify before cohort).

**Read "commercially safe" carefully.** It usually means the vendor trained on licensed or owned material and will stand behind output on certain plans. It does not cover what *you* feed in: a real person's photo, a logo you don't own, a prompt that names a brand or an artist. Indemnities are usually capped and conditional. File the plan invoice with the provenance log.

## 5. Who owns AI output

In the US, material generated purely by AI is not protected by copyright: the Copyright Office's January 2025 report and the *Thaler v. Perlmutter* appeal (March 2025) point the same way (verify before cohort), and Suno's own help centre warns that music made 100% with AI would not qualify (verified Sep 2026). Practical meaning: your client can *use* the film but may not be able to stop others copying the raw generated parts.

Human authorship helps: the script, your selection of takes, the arrangement, the edit, the sound design and mix, your own recorded voice or footage, graphics you designed. Your production folder is the evidence: script versions in `01_story`, boards and plans in `03_board`, every take and verdict in `04_shots/takes.csv`, cut versions in `06_edit/cuts`. Keep it after delivery.

Other jurisdictions treat computer-generated works differently (the UK, for example, has its own provision). Check yours before you promise a client ownership (verify before cohort).

## 6. Disclosure and labelling

| Where | What to do | Confidence |
|---|---|---|
| YouTube | Use the altered or synthetic content disclosure for realistic AI content | (verify before cohort) |
| TikTok | Apply the AI-generated label to realistic AI content; TikTok reads C2PA content credentials | (verify before cohort) |
| Meta (Instagram, Facebook) | Expect or apply an "AI info" label | (verify before cohort) |
| EU audiences | AI Act Article 50 transparency obligations apply from 2 Aug 2026: providers machine-mark synthetic media, deployers disclose deepfakes; clearly artistic or fictional work carries a lighter duty. Check whether later amendments moved dates | (verify before cohort) |
| Clients, festivals | Tell them in writing which elements are AI-generated | studio practice |

Keep machine marks intact:
- Google's SynthID is on every Gemini Omni clip and every Lyria track (verified Sep 2026). Some open voice tools watermark every output (verified Sep 2026).
- Never strip, crop out or re-encode to remove a watermark or content credentials. Check whether your editor's export keeps embedded credentials, and keep the original downloads either way (verify before cohort).
- Add a plain credit line in the end credits or post caption: "Images, video and voices generated with AI. Tools: …".

## 7. Advertising claims

AI makes it free to show anything. Advertising law and platform policy still require it to be true.

- **No fabricated testimonials.** A generated "customer" saying the product changed their life is a fake endorsement. Real testimonials come from real people, with permission, shown as what they are: a named lower-third with their own words.
- **No results the product can't deliver.** No cream that erases wrinkles in a cut, no app screen showing features that don't exist.
- **Numbers must be true.** Specific small numbers persuade (handbook 17); invented ones deceive.
- **The no-pretence rule.** An AI character never claims a real biography. It can observe, ask and react. Proof comes from real, named, consenting people.
- **UI and product text** are composited from real screenshots or built in motion graphics, never generated (handbook 09). Gibberish on a product screen reads as fake; invented features read as false advertising.

### Weak vs strong: the mentor line

| | Line | Why |
|---|---|---|
| **Weak** | AI mentor: "I was exactly where you are two years ago. Same speech, same feeling. This course fixed it." | A synthetic person claims a life story and a result. That is a fake testimonial |
| **Strong** | AI mentor: "Most people walking into rooms like this are mid-career. The ones walking back in eight weeks later did the same thing." Over the listener's face, a lower-third: a real graduate's name and their approved quote | The character observes; the proof is real, named and consented |

## 8. UAE and GCC notes (verify before cohort)

These come from background research, not a legal review. **Get local counsel to sign off the consent form and disclosure policy before the cohort.**

- UAE Federal Decree-Law 34 of 2021 makes it an offence to capture or publish a person's image or voice without consent, and covers impersonation and defamation (verify before cohort). In practice: classmates in class footage need consent before anything is published, including a behind-the-scenes post.
- The UAE Personal Data Protection Law applies to photos and recordings of identifiable people (verify before cohort).
- UAE media and advertising rules, including advertiser permits for people publishing paid or promotional content, apply to ads you post for clients (verify before cohort).
- Other GCC states have their own media and data laws. Check before shooting or publishing there.

## 9. The provenance log

Fill `07_delivery/delivery.md` as you go, one row per external asset. It is the page a client, a platform or a festival will ask for, and it takes minutes if you do it daily and hours if you do it at the end.

| Asset | Tool / model | Version | Plan / licence | Date | Permitted use | Receipt or consent file |
|---|---|---|---|---|---|---|
| S03 final | Seedance via BytePlus | 2.5, draft promoted to 1080p | pay-as-you-go | 2026-09-29 | commercial per ToS | `invoice_ark_0929.pdf` |
| Music bed | Suno | v6 | Premier | 2026-09-30 | commercial, permitted download | `suno_download_receipt.png` |
| Lead's voice | ElevenLabs | designed voice, v3 | Creator | 2026-09-29 | commercial | `elevenlabs_invoice_sep.pdf` |
| EX5 performance | real footage, classmate | n/a | consent form | 2026-09-30 | this capstone, portfolio, 2 years | `consent_AK_2026-09-30.pdf` |

Generation-level provenance (which take came from which prompt, model and cost) lives in `04_shots/takes.csv` through `film take add` and `film gen`. The delivery log is the asset-level summary. Keep receipts and signed forms in `07_delivery/` too.

## 10. Consent form (short)

```
LIKENESS AND VOICE CONSENT                        Consent ID: ________

I, ____________________ (name), allow ____________________ (maker)
to use my  [ ] face / appearance  [ ] voice  [ ] performance  [ ] name
in the project "____________________", including with AI tools that
  [ ] use my photos or recordings as references
  [ ] train a model on my likeness or voice
  [ ] generate new images, video or speech that look or sound like me

Uses allowed:  [ ] course screening   [ ] maker's portfolio   [ ] social media
               [ ] paid advertising   [ ] festivals / broadcast   [ ] other: ______
Territories: ______________      Valid until: ______________
Not allowed: any other project; sexual, political or defamatory content;
any suggestion that I endorse a product, unless ticked above.
Payment / credit: ______________________________________________
I can withdraw consent in writing for future uses at any time. When consent
ends or expires, the maker deletes trained models and my source files.

Signed: ______________  Date: ________    Maker: ______________  Date: ________
```

Put the Consent ID in the provenance log. Adapt the form with local counsel for client work.

## 11. Red lines

Never acceptable, in class or out, whatever the tool allows:

1. **Non-consensual intimate or sexual imagery** of any real person.
2. **Any sexualised or harmful depiction of a minor**, generated or real.
3. **Impersonation**: putting words in a real person's mouth, fake endorsements, fraud, political deepfakes.
4. **Deception presented as fact**: fake news footage, fake evidence, fabricated testimonials or reviews.
5. **Targeting a private person**: harassment, humiliation, "pranks" at their expense.
6. **Evading safety systems**: getting around content, likeness or age filters by any method.

If a brief asks for any of these, the answer is no, and you say why.

## In the studio

| Skill | What it does for rights |
|---|---|
| `studio` | Asks at brief time where the film will be seen (class, portfolio, client, broadcast); that sets the licence bar for every later choice |
| `bible-builder` | Builds characters from description; stops on any real-person reference until a consent ID is logged |
| `performance-voice` | Checks every voice source against the class policy before cloning or speech-to-speech |
| `sound-design` | Checks each music and SFX source against its licence and the intended use |
| `hybrid-footage` | Asks for releases before real footage with people goes into EX5 |
| `qc-review` | Won't sign off a master while provenance rows, consent rows or the disclosure checklist are incomplete |

```
film take add S03 04_shots/S03/takes/S03_t004.mp4 --stage final --tool ark --model seedance-2.5 --res 1080p --cost 2.85 --prompt 04_shots/S03/prompt_v3.md
film take list --shot S03                 # the full generation trail for one shot
film qc 07_delivery/masters/master.mp4 --spec social
film deliver 07_delivery/masters/master.mp4 --aspects 9:16,1:1
```

Ask Claude: "Audit `07_delivery/delivery.md` against `takes.csv` and `05_sound`, and list every asset with no licence or consent row."

## Drills

1. **Licence audit (15 min).** List every external asset in your capstone so far: stills, clips, voices, music, SFX, fonts, footage. Fill a provenance row for each. Circle anything with no receipt or consent, and fix or replace it.
2. **Consent in practice (10 min).** Fill the form for a classmate whose face, voice or performance you plan to use. Tick only the uses you need and set an expiry. Swap forms and check each other's.
3. **Claims pass (15 min).** Take your spot's script. Underline every claim, number and testimonial. Mark each one true and provable, or cut it. Rewrite any line where an AI character implies a real biography.
4. **Disclosure plan (10 min).** For each platform you will post to, write the label you'll apply, your credit line, and which original files you will keep.
