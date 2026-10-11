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

One prompt in Claude Code does everything:

```
Set up my AI video studio. Follow the instructions at https://github.com/Trueflutter/film-studio/blob/main/SETUP.md and do every step for me. Ask me for my keys when you need them.
```

Claude clones this repo and runs `setup/install.sh` (macOS): ffmpeg-full, Node 22+, Python if needed, the `film-studio` and `hyperframes` plugins with auto-update on, and the studio folder at `~/Documents/my-studio`. Then it adds the EvoLink and ElevenLabs keys to `.env` and runs `film doctor`. The only manual step is Homebrew on a Mac that lacks it (it needs the Mac password). Windows: `SETUP.md` has the winget route.

Without git access, the zip works from disk: unzip it and run `bash film-studio-kit/setup/install.sh`.

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
