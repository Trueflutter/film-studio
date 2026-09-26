---
name: qc-review
description: Quality control and delivery - runs `film qc` machine checks (frame, fps, duration, loudness, true peak, dead air, black and frozen frames), leads the viewing protocol, scores the 12-area creative rubric with timecodes and diagnosis codes, prioritises fixes cheapest first, and prepares deliverables (aspect variants, captions, disclosure, provenance). Use before sharing, submitting or publishing any cut.
---

# QC and delivery

Read `${CLAUDE_PLUGIN_ROOT}/handbook/14-qc-and-delivery.md` first.

## 1. Machine checks

`film qc <file> [--spec social|web|broadcast]` writes `07_delivery/qc/<name>_qc_<date>.md`. Explain every FAIL and WARN in plain words:
- FAIL (loudness, true peak, a non-standard frame) must be fixed before shipping.
- WARN means decide: an intentional held freeze, an end card, a black beat, or a held silence is fine: note "intended". Dead air usually means missing room tone; a black span usually means a leftover `slate`.

## 2. The viewing protocol (the director watches; you record)

You can't watch or listen, so run the protocol with the director and write their answers into the QC file:
1. once full screen with sound, no stopping: gut reaction first;
2. once muted: does the picture tell the story?
3. once with eyes closed: does the sound tell it?
4. once on a phone at arm's length: captions, safe zones, legibility;
5. frame-step every cut (you can help: `film frames <file> --at <cut times>` and look for flashes, jumps, duplicated frames);
6. one fresh viewer: "what was it about?"

## 3. The creative rubric

Score 1-5 with the director: Story · Emotion · Realism · Continuity · Composition · Motion & physics · Faces & anatomy · Lip sync & voice · Sound · Edit & pacing · Artefacts & text · Brief fit. Anything under 3 gets a timecode, a diagnosis code (CONCEPT, REF, PROMPT, MODEL, MODE, CAMERA, ACTION, FRAME, IDENTITY, PHYSICS, PERFORMANCE, SYNC, ARTEFACT, WORKFLOW) and a fix.

## 4. Prioritise

Order fixes by severity, then cheapest first (cut or trim → post fix → re-mix → caption edit → pick-up generation). Ship rule: no FAIL, no rubric area below 3. Offer the top three fixes and their cost in time and money.

## 5. Deliver

- Aspect variants: `film deliver <master> --aspects 9:16,1:1 --fit crop|pad|blur`. Warn when an automatic crop loses the story; recommend a manual reframe for the priority deliverable.
- Loudness per platform (`--lufs`), captions per variant (`captions` skill), sidecar `.srt`.
- Naming: `<slug>_<aspect>_vNNN.mp4`; masters kept textless where possible.
- `07_delivery/delivery.md`: deliverables table ticked, AI disclosure planned per platform, provenance log complete (tool, model, plan/licence, date, permitted use, receipts), consent forms for any real person's face or voice.
- Re-run `film qc` on each deliverable.
- Finally `film cost --save` and prompt the director to write `07_delivery/wrap.md`.
