# Pace and accent

## Pace

- Target: **3 words per second** for social and news (`--wps 3.0`). **2.6** for YouTube and long explainers. Past 3.6 feels rushed.
- Models differ. In our test the same 80-word script came out at 2.7 words per second on Eleven v3 and 3.3 on Eleven v4 before any tightening. That is why `tighten` measures and aims at a target instead of using a fixed speed-up.
- `tighten` works in two steps: (1) every pause longer than 0.28 s is cut down to 0.2 s, in the middle of the silence so there are no clicks; (2) it measures the pace left and speeds up or slows down (ffmpeg `atempo`, pitch stays) to hit the target. Speed is limited to 0.9x to 1.25x, and skipped within 3% of the target.
- Words come from the script copy `read` saves, or `--script FILE`, or a transcript if neither exists.
- Pauses are where a read feels human. If the result sounds breathless, raise `--gap` to 0.25 or lower `--wps`.
- If the limit is hit (the read is much too slow or fast), choose a different voice or fix the script instead of forcing the tempo.
- Output stays `mp3_44100_128`. The original file is never overwritten.

## Accent

- Lighter accents read more natural and are understood by more people. A soft British, neutral American or light Gulf-English accent is the safe choice.
- A thick accent can sound like a caricature in a short clip. Use it only when the character needs it, and audition it against a lighter one.
- Match the accent to the character's story. A presenter from Dubai who grew up in London can have a light British accent; do not use a heavy regional one just to make the point.
- Age and energy matter as much as accent: "calm, mid thirties, warm" beats "British".
- Library filters: `--accent`, `--gender` (male, female), `--age` (young, middle_aged, old), `--language`. Search also matches words in the description ("calm", "news", "storyteller").

## When the read goes wrong

| Problem | Fix |
|---|---|
| Robotic, flat | Lower stability to 0.35 to 0.45 for more range. Add one bracket tag. Shorten sentences. |
| Wobbly, unstable | Raise stability to 0.6 to 0.7. |
| Name said wrong | Respell it as it sounds in the script copy, re-read that sentence. |
| Joins between pieces sound different | Use fewer, larger pieces. Do not change settings between pieces. |
| 409 error | Two requests for the same voice at once. The script already runs them one at a time; do not start a second run on the same voice. |
| 403 on output | The plan does not allow that format. Stay on `mp3_44100_128`. |
