# Repairs: edit the chosen picture, one problem at a time

Every repair is an **edit of the approved picture** (Aristotto `image-to-image` on gpt-image-2.5 Sunburst with the picture as the input, or `images.py gen ... --ref <picture>` on ChatGPT). Structure: what must stay, then the one or two things that change, then "Nothing else changes."

- **Waxy skin:** "Preserve her identity, expression, framing, clothes and lighting. Remove the smoothed skin treatment. Restore subtle, localized texture and natural tonal variation, without heavy wrinkles, dirt or exaggerated pores."
- **Makeup wrong for the role:** match the person's situation, don't strip it. A TV presenter wears professional on-air makeup (defined lashes, groomed brows, even base, set skin); a creator filming at home wears little; a runner after a race wears none. Taking a presenter's makeup off made her look less real in testing. Edit only if the makeup doesn't fit the role: "Preserve everything, including skin texture and freckles. Her makeup becomes [the right state for the role]."
- **A mark on the wrong side:** "The beauty mark sits under her left eye, which is the eye on the right side of the picture. Remove it from the other cheek."
- **Face drifted during an edit:** "Use the approved picture as the authority for face and hairline. Keep this scene, pose, outfit and light. Correct the face toward the approved picture without beautifying or changing her age."
- **A bad hand:** "Correct only the right hand and its contact with the page. Keep the pose and gesture; coherent fingers, wrist and contact shadow. Keep the rest unchanged."
- **Floating full body:** "Preserve the person and clothes. Correct the feet and leg loading so the right leg carries most of the weight and both shoes meet the ground."
- **Pasted-on background blur:** "Preserve the composition and subject. Replace the cut-out blur with a continuous transition from the subject to the room, especially around hair and shoulders."
- **Light disagrees:** "Make the window at camera left the dominant source; align the face, hand and object shadows with it; keep gentle fill."
- **Everything glossy:** "Keep exposure and skin tone. Reduce the uniform polished finish: cloth matte, skin with only localized sheen, glass with its own reflections."
- **Posed smile:** "Keep everything. Her expression relaxes: lips together or just parted, a slight lift at one corner, the eyes doing more of the smiling than the mouth."

New outfit or place for a recurring character: "Keep this exact woman: the same face, bone structure, eyes, brows, hairline and hair. Change only her outfit to [specific garment, fabric, colour]. Same framing and light." One change per edit.
