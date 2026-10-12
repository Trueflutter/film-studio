# My AI video studio

This folder is an AI video studio. Productions live in `productions/`, one folder each, created with `film new "Title"`.

## How to work here

- For any film, ad, spot or video work, use the **film-studio** plugin: start with the `studio` skill (`/film-studio:studio`), which routes to the right skill for each stage.
- Run `film status` at the start of every session and tell me where the current production stands and the one next step.
- I am the director. Propose options and explain trade-offs; I make the creative calls.
- Follow the ladder: still → draft → lock → final → fix. No premium render without an approved draft or still. Log and rate every take.
- Prompts live in files. Change one variable per retry. Three strikes on the same approach (the same failure returning after a one-variable fix) means we redesign the shot.
- Never generate text, logos or UI inside images or video: build them with the `graphics` skill and composite them in post.
- Before you show me a cut or a graphic, look at it yourself (`film review` for a cut, snapshots for a graphic) and fix the worst problems first.
- Never use a real person's face or voice without written consent, and never try to get around a provider's safety or real-person filter.
- Pictures and video are made on Aristotto: show me the price, I approve it on the card, then log the result at once with `film take add` (links expire). When Aristotto credits run out (or it isn't connected), switch to EvoLink (`film gen --via evolink`) and tell me in one line.
- API keys live in `.env`, which I fill in myself. Never ask me for a key in the chat, and never read, print or commit `.env`; `film doctor` tells you whether a key is set.
- End every session with `film cost` and the next three actions.

## My studio notes

<!-- Add rules you learn from your wrap notes here, so every production starts smarter. Examples:
- My lens kit: 28mm, 50mm, 85mm.
- Seedance drafts predict my blocking well, but hands change on the final: always check hands.
- My voice for narrator work: <voice id>.
-->
