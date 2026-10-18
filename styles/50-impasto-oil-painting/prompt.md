# 50 — Impasto Oil Painting

**Look:** Every frame is a thick oil painting on canvas. Paint is laid on with palette knives and loaded bristle brushes, so every stroke stands up as a raised ridge that catches a raking studio light. The bright side of each ridge gets a small specular glint and the dark side a soft shadow. Big flat knife swipes sit in the background wall, and smaller directional strokes follow the form of faces, hair and clothes. The colour is rich and luminous: warm highlights, cool shadows, saturated mid-tones, with glazes and canvas weave showing where the paint is thin. The strokes are re-laid in every frame, so the whole painting boils gently while the people stay recognizable.

**Also called / where it trends:** "impasto oil painting", "palette knife painting", "luminous oil painting", "oil paint animation", "living painting", "Van Gogh / Loving Vincent style" (hand-painted oil frames), "AI oil painting video effect". It is a standard style preset on AI video tools: frameloop.ai lists three presets (Impasto Ilustration, Oil Painting, Luminous Oil Painting), and crreo.ai, Morphic and motionsites list oil-paint video looks too.

**References:**
- https://frameloop.ai/visual-styles: frameloop's style library (public grid; the per-style links go to a sign-in page, which was not used). `refs/ref_1.png` is the **Impasto Ilustration** card, `refs/ref_2.png` the **Oil Painting** card and `refs/ref_3.png` the **Luminous Oil Painting** card. frameloop's own style prompts, credited verbatim:
  - Impasto Ilustration: "thick impasto oil painting style, highly textured visible brush strokes, palette knife technique, stylized whimsical illustration, flat textured white background, scattered abstract colorful paint dabs, hard shadows, contemporary digital painting"
  - Oil Painting: "oil painting style, textured brushstrokes, rich colors, layered pigments, impasto technique, canvas texture, blended transitions, depth through shading, painterly realism, glazing effects, visible brush marks, chiaroscuro lighting, classical composition, palette knife textures"
  - Luminous Oil Painting: "Luminous oil painting with soft impasto texture and delicate blended brushwork, pastel color palette of blush pink, lavender, pale peach, sky blue, and cream, impressionist technique, whimsical surreal elegance, airy romantic atmosphere, soft-focus fine art portrait."
  The prompt below merges the three (impasto relief + rich layered colour + luminous warm/cool light) and expands them into the staged invideo / Seedream frame-by-frame workflow of the Punk Photocopy Collage prompt (`_source/reference_prompt_punk_collage.txt`).
- https://www.morphic.com/resources/videos/oil-paint-animation-videos (`refs/ref_4.png`): Morphic's oil-paint animation examples, painted characters with visible strokes in motion.
- Also seen: https://www.crreo.ai/styles/oil-painting-ai-video (oil painting AI video style), https://motionsites.org/skills/motion-graphics/impasto-film-style (impasto film look), https://artstyles.com/s/palette-knife-painting-style/3ObVzrPsjvoJ3CxhMoX2 (palette-knife style description).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV):
- Colours get a luminous grade: saturation ×1.55, warm highlights and cool shadows.
- The canvas is painted in three Hertzmann-style passes of oriented strokes (radius 13 → 6 → 4 px). Each pass is placed where the canvas still differs from the frame, and every stroke is aligned to the image's structure-tensor direction.
- Every stroke also writes a height plateau with bristle grooves into a height map. 26 palette-knife slabs and a few loose colour dabs are added on the wall.
- The height map is lit with a raking light (diffuse shading + small specular), with canvas weave where paint is thin.
- The stroke seed changes every frame on the people and every 3 frames on the background, so the paint boils.

## Prompt

```text
I'm uploading one video clip. Convert it into a frame-by-frame THICK IMPASTO OIL PAINTING animation, luminous colour, palette-knife ridges and loaded brushstrokes on canvas, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame becomes a hand-painted oil painting on canvas:
* thick IMPASTO paint that stands up off the canvas
* PALETTE KNIFE swipes: flat slabs of paint with sharp ridged edges
* loaded BRISTLE brushstrokes with visible bristle grooves
* strokes that follow the form (around the face, down the hair, along the folds)
* a raking studio light: every ridge has a lit edge, a tiny glint and a soft shadow side
* rich, LUMINOUS colour: warm golden highlights, cool blue-violet shadows, saturated mid-tones
* layered pigment and thin glazes where the paint is thinner
* canvas weave showing through only in the thinnest areas
* a few loose, colourful paint dabs in the background
* no photographic surface anywhere
The result should feel like someone:
PRIMED A CANVAS
→ BLOCKED IN THE SCENE WITH A PALETTE KNIFE
→ PAINTED THE PEOPLE WITH LOADED BRUSHES
→ BUILT UP THICK IMPASTO IN THE LIGHTS
→ GLAZED THE SHADOWS
→ LIT THE WET PAINTING FROM THE SIDE
→ PHOTOGRAPHED IT
→ REPAINTED IT FOR THE NEXT FRAME
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — PAINTED PORTRAIT
The people become OIL-PAINTED portraits that keep the photograph's structure.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* clothing
* accessories
* glasses
* pose
* body proportions
* movement
* hand position
* interaction with objects
This is painterly realism, NOT a cartoon and NOT a smooth digital painting.
Keep facial proportions, eye shape, glasses and hairline exact.
STROKE RULES
Background: big palette-knife swipes and broad brushstrokes, a few bold colour dabs.
People: smaller strokes, smallest on faces, eyes, glasses, hands.
Strokes follow the direction of the form:
* across the forehead and cheeks with the curve of the face
* along the hair in long strands
* along the folds of the clothing
Each stroke is a single decisive mark with a clear start and end.
Lights get the thickest paint; shadows are thinner, with glaze.
IMPASTO & LIGHT RULES
The paint must look PHYSICALLY THICK:
* raised ridges with a lit edge and a shadowed edge
* small specular glints on the wet paint ridges
* bristle grooves inside each brushstroke
* knife edges where paint was pushed
Use ONE consistent raking light direction (top-left) for the paint relief in every frame.
The scene's own lighting stays as painted colour; the raking light only lights the paint surface.
COLOUR RULES
Rich and luminous, never muddy:
* warm golden / peach highlights
* cool blue / violet shadows
* saturated, clean mid-tones
* colours mixed on the canvas, not blended smooth
* no grey photo tones
OBJECT CONTINUITY
If a person holds an object, paint the object with the same strokes and impasto.
It moves exactly with the hand.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame.
Never change:
* identity
* facial structure
* hairstyle
* glasses
* clothing
* accessories
* body proportions
* anatomy
* expression
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.
PERFECT MOTION TRACKING
The painting must match the source frame exactly in position, pose and timing.
If the head moves:
the painting follows.
If the hand moves:
the painting follows.
If the body turns:
the painting follows.
NO floating figure.
NO previous-frame silhouette.
NO delayed strokes.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel separately repainted.
Allow between consecutive frames:
* brushstrokes to be laid down again in slightly different places
* knife swipes to shift and change their edges
* impasto ridges and glints to change
* small colour variations inside the same colour area
Keep FIXED in every frame:
* the light direction on the paint relief
* the colour palette of every person and object
* the identity and features of every face
* the stroke size for each area (background big, faces small)
Do NOT make the boil so strong that faces flicker or change.
DO NOT
Do NOT use a smooth digital-painting or oil-paint filter look.
Do NOT blur strokes into each other.
Do NOT leave any photographic surface.
Do NOT make a flat or matte paint surface; the relief must show.
Do NOT turn the people into cartoons or anime.
Do NOT use a swirling Van Gogh pattern over everything.
Do NOT make the colours muddy or grey.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT interpolate new in-between frames.
STAGE 1 – FRAME EXTRACTION (STRICT)
1. Read the source clip's frame rate and duration.
Report both to me BEFORE doing anything else.
2. Extract frames as follows:
* If the source is 24 fps:
keep every SECOND frame, discard the one in between.
Nothing else.
* If the source is 30 fps:
conform to 24 fps first, then keep every second frame.
* Target in both cases:
exactly 12 unique frames per second of source.
3. Hard limits on the extraction:
* Total extracted frames must equal duration in seconds × 12, rounded down.
* State this number BEFORE extracting and confirm it AFTER extraction.
* Do NOT extract every frame "to be safe."
* Do NOT extract at a higher rate and downsample later.
* Do NOT extract from only part of the clip.
* Cover the video from the first frame through the last frame.
* No interpolation.
* No optical flow.
* No artificial in-between frames.
* No motion blur.
* No frame smoothing.
4. Name frames sequentially:
frame_01
frame_02
frame_03
frame_04
...
Continue in exact playback order.
STAGE 2 – TIMELINE VERIFICATION (STOP HERE)
Before generating or stylizing ANYTHING, build a verification timeline.
Place every extracted frame onto the timeline as its own individual clip.
Keep them in exact chronological playback order.
Each frame must last exactly:
1/12 second.
At this stage:
Use ONLY the original UNMODIFIED extracted frames.
* NO effects
* NO styling
* NO painting
* NO brushstrokes
* NO impasto
* NO Seedream generation
This stage exists ONLY to verify timing.
REPORT BACK
Report:
(a) Total frame count on the timeline.
(b) Total timeline duration in seconds.
(c) Original source clip duration in seconds.
The timeline duration and original clip duration MUST match.
If they do not match, something went wrong during Stage 1.
SAY SO AND STOP.
Do not compensate using interpolation, duplicated frames, stretched frames, optical flow or timing manipulation.
After successfully building and reporting the verification timeline:
THEN STOP AND WAIT.
Do NOT begin Seedream generation.
Do NOT stylize any frames.
Do NOT begin the oil-painting transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – IMPASTO OIL PAINT STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input.
For consistency, also give the first approved styled frame as a style reference for all later frames (same stroke size, same light direction on the paint, same palette).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, or the style rules broke (smooth filter look, lost relief, face drift) — regenerate those frames only.
The final video must feel like a THICK, LUMINOUS OIL PAINTING that moves: every frame repainted, the paint standing off the canvas.
The image should deliberately contain:
* thick impasto ridges with lit edges and soft shadows
* palette-knife swipes
* directional bristle brushstrokes that follow the form
* warm luminous highlights and cool shadows
* a few loose colour dabs
* canvas weave in the thinnest paint
* recognizable faces painted in small strokes.
Avoid a smooth digital oil-paint filter.
```
