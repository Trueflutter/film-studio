# Film Studio: the student kit

Everything a student needs to run productions from Claude Code, in one install. This folder is a **Claude Code plugin marketplace** (`saqr-film`) containing one plugin (`film-studio`) and a starter project.

```
studio-kit/
  .claude-plugin/marketplace.json   the marketplace
  film-studio/                      the plugin
    .claude-plugin/plugin.json
    skills/                         13 skills (studio, story-engine, bible-builder, shot-designer,
                                    prompt-director, take-doctor, performance-voice, sound-design,
                                    captions, editor, graphics, qc-review, hybrid-footage)
    bin/film                        the `film` command (added to PATH by Claude Code)
    filmkit/                        the Python behind it (stdlib only + ffmpeg)
    templates/production/           what `film new` creates
    handbook/                       18 chapters the skills read on demand
    assets/fonts/                   caption fonts (SIL Open Font License)
    tests/                          python3 -m unittest discover -s tests
  starter/                          the student's studio folder (CLAUDE.md, .env.example, .mcp.json)
```

## Install (student)

Requirements: Claude Code, Python 3.9+, ffmpeg with libass for captions (macOS: `brew install ffmpeg-full`, which `film` finds by itself; Homebrew's plain `ffmpeg` has no libass. Windows: `winget install Gyan.FFmpeg`). For the `graphics` skill: Node 22+ and the HyperFrames plugin (`/plugin marketplace add heygen-com/hyperframes`, then `/plugin install hyperframes@hyperframes`; Apache 2.0).

```
/plugin marketplace add <owner>/<repo>          # the repo where this folder is published
/plugin install film-studio@saqr-film
```
Then copy `starter/` to where you keep projects, open Claude Code in it, `cp .env.example .env`, add keys, and type `!film doctor`. Claude Code puts the plugin's `bin/` on its PATH, so `film` works inside Claude Code. For a normal terminal, `film doctor` prints the path to alias.

Update later with `/plugin marketplace update saqr-film` (or on session start); bump `version` in `film-studio/.claude-plugin/plugin.json` when you ship changes.

Without git access, the same folder works from disk: `/plugin marketplace add /path/to/studio-kit`.

## Publish for a cohort (instructor)

Students can't reach this private repo. Publish the kit as its own repository (private with student access, or public):

```
# from the video-creation repo root
git subtree split --prefix ai-filmmaking-bootcamp/studio-kit -b studio-kit-release
git push git@github.com:<org>/film-studio.git studio-kit-release:main
```
Students then run `/plugin marketplace add <org>/film-studio`. For a downloadable zip instead: `cd ai-filmmaking-bootcamp && zip -r film-studio-kit.zip studio-kit -x '*/__pycache__/*'`.

## The `film` command

```
film new "Title" [--format film|ad|social] [--aspect 16:9|9:16|1:1|4:5|2.39:1] [--duration 60] [--budget 60]
film status · film list · film use <slug> · film character "Name" · film doctor
film take add|rate|list|codes           log, rate (select/maybe/reject + fail codes), list
film gen <SHOT> --via ark|fal|evolink ...  generate + log (Seedance 2.5 --draft / --from-draft)
film cost [--save|--check]              exploration vs production, cost per usable shot, budget guard
film frames · film contact · film boards · film dailies · film animatic
film assemble · film review · film teardown    cut from cut.txt; every join as frames; a reference's rhythm
film mix · film captions transcribe|build|check|burn · film qc · film deliver · film overlay
```

## Test

```
cd film-studio && python3 -m unittest discover -s tests      # 11 tests; media tests need ffmpeg
claude plugin validate ./film-studio && claude plugin validate .
```
