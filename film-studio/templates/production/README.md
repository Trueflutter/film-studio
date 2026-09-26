# {{title}}

{{format}} · {{aspect}} · target {{duration}}s · started {{date}}

**Logline:** _one sentence, filled in once 01_story/concept.md survives the stress test_

## The pipeline (and the gate at the end of each stage)

| Stage | Folder | You are done when… |
|---|---|---|
| Brief | `00_brief/` | One page. You can say who it's for and what they should feel. |
| Story | `01_story/` | The concept scores ≥ 3 on every stress-test line. The script/treatment reads in under 2 minutes. |
| Design | `02_design/` | Every character has a bible + reference pack. The style bible names a lens kit, light rules and a palette. |
| Board | `03_board/` | Shot list complete, every shot boarded, animatic watched with temp sound. Generation plan has a budget. |
| Shots | `04_shots/` | Every shot has a `select` in `takes.csv`. Finals only rendered for shots whose draft was approved. |
| Sound | `05_sound/` | Dialogue, room tone, foley, effects, music as separate stems. Mix hits the loudness target. |
| Edit | `06_edit/` | Picture locked. No same-size jump cuts, weak frames hidden, rhythm varies. |
| Delivery | `07_delivery/` | QC report passes, masters exported per platform, provenance log complete, wrap notes written. |

## Commands you'll use most

```
film status                 where am I?
film take add S03 file.mp4 --stage draft --model ... --cost 0.50
film take rate S03_t002 reject --fail ACTION+CAMERA
film dailies                review page of every take
film cost                   exploration vs production spend, cost per usable shot
film animatic · film assemble · film mix · film qc · film deliver
```
