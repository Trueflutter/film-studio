# Set up the AI video studio

**For Claude.** A student has asked you to set up their studio from this repository. Do every step yourself; the student only answers your questions. Speak in plain words, one short line per step, and never show or repeat an API key.

## 1. Get the kit and run the installer

```bash
rm -rf /tmp/film-studio-setup
git clone --depth 1 https://github.com/Trueflutter/film-studio.git /tmp/film-studio-setup
bash /tmp/film-studio-setup/setup/install.sh
```

It works on a Mac and on a Windows PC (Claude Code runs it in Git Bash there). It installs ffmpeg (with captions support), Node 22+, Python if needed, the `film-studio` plugin (auto-updating, so course fixes arrive by themselves) and the `hyperframes` plugin, and creates the studio folder at `~/Documents/my-studio`. It is safe to run again. Use a long timeout (ffmpeg-full can take several minutes).

- **Mac, Homebrew missing:** the installer prints one line for the student to paste into the Terminal app (it needs their Mac password, which you must never ask for or type). Wait, then run step 1 again.
- **Any other ✗:** read the message, fix what you can, run the installer again. If git is missing, macOS offers to install the developer tools: tell the student to accept, then run step 1 again.
- **Windows:** Claude Code needs Git for Windows (it provides the Git Bash shell and `git`). If `git` or bash is missing, the student installs it from https://git-scm.com/download/win with the default options, restarts Claude, and asks again. The installer uses winget. Tell the student to click Yes if Windows asks for permission (the Node installer does). If it says winget is missing, the student installs "App Installer" from the Microsoft Store. If it can't find Claude Code to add the plugins, it prints four `/plugin` lines: ask the student to type them in Claude Code, one at a time. A tool installed today may only be found after a new Claude session: if step 3 says "not found", start one and run step 3 again.

## 2. Connect Aristotto and add the keys

Pictures and video are made on **Aristotto** (a monthly subscription; students use the code **SAQR** at checkout for 70% off the first month), with **EvoLink** (pay as you go) as the fallback when Aristotto credits run out. The studio plugin brings the Aristotto connection. After step 1, ask the student to start a new Claude session in `~/Documents/my-studio`, type `/mcp`, choose **aristotto** and sign in with their Aristotto account. No Aristotto account yet: skip it, the studio runs on EvoLink until they sign up. Then check it works by calling Aristotto's `list_capabilities` for video and saying "Aristotto connected". If the student already added Aristotto as a connector in Claude's settings, that works too: skip the sign-in.

Then work in `~/Documents/my-studio`. Ask the student for their **EvoLink** key (the fallback, `EVOLINK_API_KEY=`), then their **ElevenLabs** key (voices, music, sound effects, captions; `ELEVENLABS_API_KEY=`), one at a time, and write each into `.env` yourself. Never print the file or echo a key back; confirm with "EvoLink key saved".

## 3. Check

```bash
cd ~/Documents/my-studio && sh /tmp/film-studio-setup/film-studio/bin/film doctor
```

Everything that matters shows ✓. Explain anything red in one plain sentence and fix it.

## 4. Hand over

Tell the student, in three lines:
1. Setup is done: the studio, the film command, graphics in code, Aristotto and the keys.
2. Every picture or clip on Aristotto shows its price in a card first; nothing is spent until they click Approve. When Aristotto credits run out, Claude switches to EvoLink and says so.
3. Updates install themselves; nothing else to install this week.
