# Set up the AI video studio

**For Claude.** A student has asked you to set up their studio from this repository. Do every step yourself; the student only answers your questions. Speak in plain words, one short line per step, and never show or repeat an API key.

## 1. Get the kit and run the installer

```bash
rm -rf /tmp/film-studio-setup
git clone --depth 1 https://github.com/Trueflutter/film-studio.git /tmp/film-studio-setup
bash /tmp/film-studio-setup/setup/install.sh
```

It installs ffmpeg-full, Node 22+, Python if needed, the `film-studio` plugin (auto-updating, so course fixes arrive by themselves) and the `hyperframes` plugin, and creates the studio folder at `~/Documents/my-studio`. It is safe to run again. Use a long timeout (ffmpeg-full can take several minutes).

- **Homebrew missing:** the installer prints one line for the student to paste into the Terminal app (it needs their Mac password, which you must never ask for or type). Wait, then run step 1 again.
- **Any other ✗:** read the message, fix what you can, run the installer again. If git is missing, macOS offers to install the developer tools: tell the student to accept, then run step 1 again.
- **Windows:** run `winget install Gyan.FFmpeg OpenJS.NodeJS Python.Python.3.12`, then in Claude Code `/plugin marketplace add Trueflutter/film-studio`, `/plugin install film-studio@saqr-film`, `/plugin marketplace add heygen-com/hyperframes`, `/plugin install hyperframes@hyperframes` (ask the student to type these), copy `starter/` to `Documents\my-studio`, and continue at step 2.

## 2. Add the keys

Work in `~/Documents/my-studio` from now on. Ask the student for their **EvoLink** key, then their **ElevenLabs** key, one at a time. Write each into `.env` yourself (`EVOLINK_API_KEY=` and `ELEVENLABS_API_KEY=`). Never print the file or echo a key back; confirm with "EvoLink key saved".

## 3. Check

```bash
cd ~/Documents/my-studio && /tmp/film-studio-setup/film-studio/bin/film doctor
```

Everything that matters shows ✓. Explain anything red in one plain sentence and fix it.

## 4. Hand over

Tell the student, in three lines:
1. Setup is done: the studio, the film command, graphics in code, and the keys.
2. Start a new Claude Code session in the `my-studio` folder (or type `/reload-plugins`) so the studio skills load.
3. Updates install themselves; nothing else to install this week.
