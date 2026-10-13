# Connect ElevenLabs (one time, about 2 minutes)

Needs: an ElevenLabs account (the paid Starter plan or higher is best), Python 3 and ffmpeg.

1. The student creates an API key in their ElevenLabs account (Developers, API Keys). Allow text to speech, voices (read) and speech to text.
2. The student opens their studio `.env` file and adds one line themselves: `ELEVENLABS_API_KEY=...`. Never ask for the key in chat. Never read the file out loud, print it or copy it anywhere. Make sure `.env` is in `.gitignore`.
3. Run `python3 <skill>/scripts/voice.py check` from the studio folder. It should say `key: found (not shown)` and name the newest model.
4. If ffmpeg is missing: `brew install ffmpeg` (Mac) or install it from ffmpeg.org.

Library voices need a paid plan to be used through the API. If one is refused, pick a voice from the student's own account instead (`voices` without `--library`).
