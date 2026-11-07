# Update the AI video studio

**For Claude.** A student has asked you to update their AI video studio to the latest course kit. Do every step yourself and say one short line per step. Never ask for, print or change their API keys.

**The kit's only home:** https://github.com/Trueflutter/film-studio (marketplace `saqr-film`, plugin `film-studio`). If the student installed from any other link, a zip or a folder on disk, this link replaces it.

**The rule for every update:** the plugin update replaces every kit file by itself. You never copy or edit kit files by hand. The student's own files are never overwritten.

| | What | What you do |
|---|---|---|
| **Replaced by the update** | Everything inside the plugin: skills, the `film` command, handbook, templates | Nothing: step 2 does it |
| **Refreshed once** | The studio rules at the top of the studio's `CLAUDE.md` (above `## My studio notes`) | Step 5 checks it |
| **Remove** | A standalone copy of a kit skill (for example `seedance-directing`) installed from a folder or zip | Step 4 |
| **Keep: never overwrite** | `.env` (keys), `.mcp.json`, everything under `## My studio notes` in `CLAUDE.md`, and everything in `productions/` (briefs, bibles, prompts, takes, edits) | Leave them exactly as they are |

## 1. Check what is installed

```bash
claude plugin marketplace list
claude plugin list
```

- `saqr-film` shows `Source: GitHub (Trueflutter/film-studio)`: go to step 2.
- `saqr-film` shows any other source (another repo, a folder, a zip): replace it, then go to step 2.

  ```bash
  claude plugin marketplace remove saqr-film
  claude plugin marketplace add Trueflutter/film-studio
  claude plugin install film-studio@saqr-film
  ```

- `film-studio@saqr-film` is not installed at all: set the studio up with https://github.com/Trueflutter/film-studio/blob/main/SETUP.md instead, then continue here at step 4.

## 2. Update the plugin

```bash
claude plugin marketplace update saqr-film
claude plugin update film-studio@saqr-film
claude plugin update hyperframes@hyperframes
claude plugin list
```

`film-studio@saqr-film` must show the same version as `film-studio/.claude-plugin/plugin.json` in this repository (https://github.com/Trueflutter/film-studio/blob/main/film-studio/.claude-plugin/plugin.json). The new version is active after a restart (step 5).

## 3. Keep updates automatic

Open `~/.claude/settings.json`. Under `extraKnownMarketplaces`, the `saqr-film` entry must have `"autoUpdate": true` and the repo `Trueflutter/film-studio`. If it is missing or different, merge this in and keep every other setting as it is:

```json
"extraKnownMarketplaces": {
  "saqr-film": {
    "source": { "source": "github", "repo": "Trueflutter/film-studio" },
    "autoUpdate": true
  }
}
```

## 4. Remove standalone copies of kit skills

The plugin carries the newest version of every kit skill (for example `film-studio:seedance-directing`). A second copy with the same name makes it unclear which one runs. Check:

```bash
ls ~/.claude/skills ~/Documents/my-studio/.claude/skills 2>/dev/null
```

Any folder there with the same name as a folder in the plugin's `skills/` (for example `seedance-directing`) is an old copy of course material: move it into `~/Downloads/old-kit-skills/` and say so in one line. Leave every other skill alone.

If the student uploaded a kit skill to the **Claude app** (claude.ai, Settings, Capabilities, Skills), the app cannot use the plugin. Zip the new version from the installed plugin for them, for example:

```bash
P=$(ls -d ~/.claude/plugins/cache/saqr-film/film-studio/*/ | sort -V | tail -1)
(cd "$P/skills" && zip -qr ~/Downloads/seedance-directing.zip seedance-directing)
```

On Windows, if `zip` is missing in Git Bash, use PowerShell's `Compress-Archive` on the same folder. Then tell them to delete the old skill in the app and upload the new zip from Downloads. They do that themselves.

## 5. Restart and check the studio rules

Tell the student to quit Claude Code and start it again in `~/Documents/my-studio`. Then compare the rules version in their studio with the plugin's:

```bash
grep -n "studio-rules" ~/Documents/my-studio/CLAUDE.md
P=$(ls -d ~/.claude/plugins/cache/saqr-film/film-studio/*/ | sort -V | tail -1); grep -n "studio-rules" "$P/templates/studio-rules.md"
```

- The two match: done.
- The studio's is older: the `studio` skill swaps the rules on its first run. If it hasn't, do it yourself: replace everything **above** the `## My studio notes` heading in `~/Documents/my-studio/CLAUDE.md` with the part of `$P/templates/studio-rules.md` **above its own** `## My studio notes` heading. Keep the student's `## My studio notes` section and everything below it exactly as it is.
- There is no `## My studio notes` heading: show the student the file and ask before changing anything.

## 6. Existing productions

New templates apply to new productions (`film new`). Existing productions keep their own files: do not overwrite anything in `productions/`. Only if the student asks, copy the blank `templates/production/04_shots/_prompt_template.md` from the plugin into an existing production's `04_shots/` folder. It is a blank form, so it replaces only the old blank form, never a filled-in prompt.

## 7. Check and hand over

```bash
cd ~/Documents/my-studio && film doctor
```

Everything that matters shows ✓. Then tell the student, in a few short lines: the version they are on now; that updates install themselves from now on; what is new (from the list below, everything newer than the version they had); and that their keys, notes and productions are as they were.

## What's new

- **1.6.9:** Gemini Omni: always ask for 720p (it returns 720p whatever you request); upscale for a 1080p final.
- **1.6.8:** Gemini Omni 1.2 Flash is the default video model (new `omni-directing` skill): people cast in motion with a screen test, scenes grown with extend (same person, no reference photo, about a fifth of Seedance's price), takes fixed with an edit. Seedance 2.5 is the fallback. `film gen` calls all six Omni routes. Studio rules v6.
- **1.6.7:** stills on GPT Image 2.6 (Sunburst): on EvoLink now (about $0.19 an image at 2K), on Aristotto as soon as it lists it. The image skill writes prompts the way 2.6 reads them (a real photograph, light as a time of day and a direction, film grain, no retouching) and spells out named lighting setups such as Rembrandt. Studio rules v5.
- **1.6.6:** the `study-a-reference` skill. Give Claude an inspiration video and say "reverse engineer this": it measures every cut, move, transition, colour and sound hit with HyperFrames' free `measure` tools, writes a recipe, and proves it with a short piece in your own brand. The technique, never the content. HyperFrames updates with the kit; no HeyGen account or Pro needed.
- **1.6.5:** screen tests are close-ups at 1080p with a hold at each angle, so the cut frames are sharp; Seedance 2.5 stays the casting default (in the director's review it looked far better than Kling v4); light makes it a film (a time of day, two colour temperatures, the edges of the frame falling dark). `film gen` no longer sends a sound setting to Kling v4, and knows its price.
- **1.6.4:** cast people in motion. A short screen test (text-to-video, a slow head turn) and frames cut from it make the face pack: frames from video read as filmed, generated stills as stock photography. Image models stay for places, products, staging and final stills.
- **1.6.3:** people look normal but attractive, cast like a good commercial: one particular person with a few small features, never a model's symmetrical face and never scarred or worn down for the sake of "real".
- **1.6.2:** imperfection stays quiet. Small irregularities read as real; a dramatic scar reads as make-up. Marks only when the story needs them, drawn fainter than wanted on screen (video makes them stronger); flour and dirt on hands and clothes, not the face.
- **1.6.1:** how people look. Scars, moles, birthmarks and tattoos go on the face picture, not the words (words alone draw a fresh wound). Today's flour, sweat or mud goes in each shot's words. Faces are cast as one particular person. Skin texture varies across the face. The EvoLink picture model is fixed.
- **1.6.0:** the `seedance-directing` skill directs any shot with people, acting or several cuts like a film crew: a block per shot with lens, camera, action, timing, sound and a lock; faces three-quarter; the camera held by an unseen operator; repair a take instead of re-rolling it. Studio rules v4.
