# My AI video studio

<!-- studio-rules v3 -->

This folder is an AI video studio. Productions live in `productions/`, one folder each, created with `film new "Title"`. The **film-studio** plugin does the work: its `studio` skill routes every request.

## How we work (always)

I am the director: I describe, approve and give notes. You take the initiative and do the making. Don't make me manage every step.

- **The simple loop:** brief → the script or plan for my OK → one approval card per batch → the result → my one note → the fix. No option boards unless I ask for options; when I do, show them in ONE view (one board page, or one Aristotto card with several outputs), never a feed of separate results.
- **Use the newest, best model** for each job and check the list before defaulting: stills GPT Image 2.5 (Sunburst), video Seedance 2.5, voice the newest ElevenLabs model (Eleven v4 as of Oct 2026; the voice-audition skill picks it). Name the model you use.
- **Push the craft without being asked.** Direct it like a top commercial director: every shot earns its place, the first second stops the scroll, the camera moves (low tracking, push-ins, orbits, whip pans), cuts land on motion, real light and texture, never a glossy AI look.

## People on screen

- **The order:** the person, the voice, the place, then video. Once a person is picked, make the reference pack (face close-up, mid shot, full body, three-quarter, side) as edits of the pick; the place from several angles of the same space (`image-prompt`).
- **Real, not porcelain:** skin with pores and sheen, small asymmetries, grooming right for the role. Never name a city in an image prompt (the model plants its landmark); describe the street.
- **Never hold a generated face longer than 4 seconds.** Cut to what they see, their hands, the world or a graphic, then come back.
- **Vary angle AND distance** across split clips: close-up, zoom out, tracking, side or three-quarter. No two clips open the same way.
- **Voice first.** Make the voice (ElevenLabs, newest model), then drive the lips from it. About 2.5 to 3 words a second; one short line per talking shot (10 to 12 words in 4 to 5 s). Write it as it sounds ("A.I.", names spelled phonetically).
- **Tighten the pace in the edit, not the voice:** `film voice tighten`.
- **A narrator over pictures always works.** Lip sync only when the idea needs a face talking.
- **Check every talking shot's transcript** against the script before showing it to me.

## Editing and graphics

- **Long pieces are layered** (`motion-design`): the voice the whole way, the presenter 15 to 25% of the time, the rest motion graphics, stills with camera moves and slides built in code. Show the layer shares and credit cost in the plan.
- **Never generate text, logos, numbers or UI** inside images or video. Build them in code with HyperFrames (the `graphics` skill) and composite them, each landing on the word it shows.
- **Cut B-roll inside its shots.** Generated clips contain their own hard cuts; a piece must never run into the next shot (`film assemble` guards this).
- **Sound:** dialogue on top, effects on graphics and cuts, ambience under each place, music ducked under the voice and lifted for the payoff (`film mix`, `film bed align`).
- **Look before I watch:** check frames at every cut, every graphic and the first second, and fix what you see.

## Money, keys and rights

- Pictures and video are made on Aristotto: show me the price, I approve it on the card, then log the result at once with `film take add` (links expire). When Aristotto credits run out, or it isn't connected, switch to EvoLink (`film gen --via evolink`) and tell me in one line.
- API keys live in `.env`, which I fill in myself. Never ask me for a key in the chat, and never read, print or commit `.env`; `film doctor` says whether a key is set.
- Never use a real person's face or voice without written consent, and never get around a provider's safety or real-person filter. My own photos, voice and footage are fine.
- End every session with `film cost` and the next three actions.

## My studio notes

<!-- Add what you learn here, so every production starts smarter. For example:
- My presenter: <name>, master image <file>, voice <voice id>.
- My brand: colours, fonts, logo file, sting.
- My call to action: ...
-->
