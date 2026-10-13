# Connect ChatGPT for images (one time, about 3 minutes)

Needs: a paid ChatGPT plan and Node.js (already installed with the studio kit). The user signs in themselves in their browser; you never see or type their password.

1. Check: `python3 <skill>/scripts/images.py check`. If it prints `ok: Logged in using ChatGPT`, you're done.
2. Install the Codex command-line tool if missing: `npm i -g @openai/codex`. Confirm with `codex --version`.
3. Sign in: run `codex login`. A browser window opens; tell the user to choose **Sign in with ChatGPT** and finish there. If it can't open a browser, run `codex login --device-auth` and ask them to open the link it prints and enter the code.
4. Run step 1 again.
5. Test: write a one-line prompt ("a ceramic coffee cup on a wooden table by a window, morning light, vertical") to `images/test/prompt.txt` and run `images.py gen images/test/prompt.txt images/test --count 1`. The board should open with one picture.

If generation fails with a usage or rate limit, the ChatGPT plan's image allowance is used up for now: switch to Aristotto for the rest of the session.

Optional, for coding help rather than images: OpenAI's Codex plugin for Claude Code (`/plugin marketplace add openai/codex-plugin-cc`, then `/plugin install codex@openai-codex`, then `/codex:setup`). The user types those slash commands themselves.
