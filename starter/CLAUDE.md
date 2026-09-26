# My AI film studio

This folder is an AI film studio. Productions live in `productions/`, one folder each, created with `film new "Title"`.

## How to work here

- For any film, ad, spot or video work, use the **film-studio** plugin: start with the `studio` skill (`/film-studio:studio`), which routes to the right skill for each stage.
- Run `film status` at the start of every session and tell me where the current production stands and the one next step.
- I am the director. Propose options and explain trade-offs; I make the creative calls.
- Follow the ladder: still → draft → lock → final → fix. No premium render without an approved draft or still. Log and rate every take.
- Prompts live in files. Change one variable per retry. Three strikes on the same approach (the same failure returning after a one-variable fix) means we redesign the shot.
- Never generate text, logos or UI inside images or video: composite them in post.
- Never use a real person's face or voice without written consent, and never try to get around a provider's safety or real-person filter.
- API keys live in `.env` (never print them, never commit them).
- End every session with `film cost` and the next three actions.

## My studio notes

<!-- Add rules you learn from your wrap notes here, so every production starts smarter. Examples:
- My lens kit: 28mm, 50mm, 85mm.
- Seedance drafts predict my blocking well, but hands change on the final: always check hands.
- My voice for narrator work: <voice id>.
-->
