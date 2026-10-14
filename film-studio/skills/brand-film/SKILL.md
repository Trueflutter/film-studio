---
name: brand-film
description: Use when the user wants a brand film, brand video, cinematic ad, luxury ad, a "Hollywood" or "cinematic" video for a client or product, a concept or idea for an ad, or says an ad feels flat, boring, generic or "just okay"; also for product or brand videos with or without people, with or without a voice-over.
---

# Brand film: an idea, made believable

Craft (camera moves, light, finishing, sound) is the baseline. What clients pay for is **the idea**. A sequence of beautiful product details is forgettable; a moment people want to be in is not.

## 1. Find the idea (one board, one pick)

Research the brand's site: its real logo and colours, the exact products, who buys and **what they want to feel** (exclusivity, romance, being seen, safety, pride, freedom). Then write three concepts with **Truth → Twist → Take → Tag**:

- **Truth:** one true thing about the brand.
- **Twist:** an impossible-but-real idea that dramatises it, from one of six engines: **Scale** (impossible size), **Transformation** (one thing becomes the product), **Arrival** (an extraordinary delivery), **Nature** (wind, sand, water, light obey it), **Through** (the camera passes through into another world), **Time** (before and after, years in one move).
- **Take:** shoot it as if it really happened.
- **Tag:** the reveal, the real logo, one line.

Show the three on one board (a line each, a still each through `image-prompt`), each from a different engine, each naming the feeling it sells. Wait for a number.

**With people or without:** with people, they are the audience and the evidence (hands, a silhouette, a real reaction, neighbours watching); the product stays the star of every frame. Without people, the product is the character: it wakes, moves, arrives.

## 2. Make it believable

Run `reference/believability.md` on the concept before writing a prompt. The audience catches anything a real day wouldn't have: night deliveries, white gloves, a cluster of phones, suits on a Saturday, a cartoon gasp, a palace instead of a real street, a landmark the brief didn't ask for.

## 3. Write it so the physics holds

- **One change of state per shot, and never across a cut.** Anything that changes (a cover sliding off, a door opening, a room filling) happens inside one continuous shot.
- **Fewer props that change.** A cover sliding off beats four crate walls falling.
- **Nothing moves by itself:** a person or a clear cause does it.
- **The hero action gets its own close-up** (the ribbon untying, the key turning), then the wide.
- **A CONTINUITY block** in the prompt: what stays true after each change, who stands where, same light.
- Name the exact product. Ask the video model for **sound effects only** ("strictly no music, no score, no BGM", three times). Camera moves from the `camera-moves` skill.

## 4. Draft, check, then final

1. **480p draft** (15 s: about 1,830 credits, about 4 to 5 minutes).
2. **Continuity check:** the frame either side of every cut and the last frame; who is where; props in the same state; nothing vanished or appeared; same light and time of day. Report what passes and what to fix.
3. **Final** at 1080p (about 9,660 credits, 5 to 7 minutes) from the corrected prompt. It's a new generation, so fix the prompt, don't expect the same take.

## 5. Sound and finish

See `reference/sound.md`: with a voice-over the music serves the voice and captions are a must; without one the music is the script. Finish with `motion-design/scripts/finish.py` (one flash, one slow-motion ramp, grain), the real logo end card, -14 LUFS.
