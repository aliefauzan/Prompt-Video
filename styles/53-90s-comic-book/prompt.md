# 53 — 90s Comic Book

**Look:** An early-1990s comic book page (the Image Comics / X-Men era), re-inked in every frame. Heavy spot blacks fill whole shadow shapes. Aggressive feathering and cross-hatching grow out of every black into the mid-tones. Faces and clothes are over-rendered with thick brush contours and many small inked lines. The colour is early digital "computer colouring": saturated flat holds shaded with smooth airbrush gradients, purple/indigo shadows, hot warm highlights, a coloured rim light along the figures and a dramatic vignette. Everything is printed on matte, slightly yellowed newsprint. There are no speech balloons, no panel borders, no Ben-Day pop-art dots and no CMYK misregistration.

**Also called / where it trends:** "90s comic book style", "Image Comics style", "90s X-Men comic art", "Jim Lee / Marc Silvestri / Rob Liefeld style", "gritty comic filter", "90s American comic". It is a preset on AI video tools (frameloop.ai: 90s Comic Book) and a common LoRA / template on SeaArt and Tensor.Art. This style differs from `07-pop-art` (flat primaries, big Ben-Day dots, 60s Lichtenstein) and from `30-spider-verse` (halftone, offset misregistration, neon, modern animation). 53 is ink-first: heavy blacks and hatching with gradient computer colour on newsprint.

**References:**
- https://frameloop.ai/visual-styles: frameloop's style library (public grid; per-style links go to a sign-in page, which was not used). `refs/ref_1.png` is the **90s Comic Book** card. frameloop's own style prompt, credited verbatim: "Early 90s comic book art style, highly dynamic and kinetic, heavy dark ink outlines, aggressive cross-hatching, exaggerated musculature and anatomy, bold saturated computer coloring with gradients, high contrast shadows and highlights, dot matrix or matte comic book paper texture, gritty and dramatic". The prompt below expands it into the staged invideo / Seedream frame-by-frame workflow of the Punk Photocopy Collage prompt (`_source/reference_prompt_punk_collage.txt`). It drops "exaggerated musculature and anatomy", because the brief keeps body proportions exact.
- https://tensor.art/template/698666255909048091 (`refs/ref_2.png`): Tensor.Art "90s American comic style" template, a before/after photo-to-90s-comic conversion.
- Also seen: https://www.seaart.ai/models/detail/71bbadc8025a28fa37852588b55d6d3e (Marc Silvestri '90s Image / Top Cow style model), https://www.classcentral.com/course/youtube-digital-inking-in-procreate-rendering-tutorial-248052 (90s-style inking: feathering and cross-hatching tutorial).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV):
- **Colour:** mean-shift flat holds with a gentle saturation lift. Value is posterised into 4 hard steps, then airbrush gradient shading is laid back on from a broad light falloff. Shadows get an indigo/purple tint and highlights go warm. A gold rim light runs down the figures, then a vignette.
- **Inks:** decided on a CLAHE-normalised value. Spot blacks are solid fills. Tapered feathering lines grow out of the blacks and the shadow side, with cross-hatching only in the darkest band. Hatch lines are wobbly and redrawn every 2 frames, so the inks boil.
- **Lines:** XDoG brush contours, with finer facial lines and a heavier silhouette on the figures.
- **Print:** everything is multiplied into yellowed newsprint with fibre texture, then a little ink spread and grain.

## Prompt

```text
I'm uploading one video clip. Convert it into a frame-by-frame EARLY-1990s COMIC BOOK animation: heavy black inks, aggressive cross-hatching, gradient computer colouring on matte newsprint, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame becomes a panel drawn by a 1990s comic penciller / inker / colourist team:
* HEAVY SPOT BLACKS: whole shadow shapes filled solid black
* AGGRESSIVE FEATHERING and CROSS-HATCHING growing out of the blacks into the mid-tones
* thick, confident BRUSH contour lines, heavier on the outer silhouette
* over-rendered faces and folds: many small inked lines
* bold, saturated early-digital "COMPUTER COLOURING": flat colour holds shaded with smooth AIRBRUSH GRADIENTS
* purple / indigo shadows, hot warm highlights
* a coloured RIM LIGHT along the figures
* high contrast, gritty and dramatic, with a dark vignette
* printed on MATTE, slightly yellowed NEWSPRINT
The result should feel like someone:
PENCILLED EACH FRAME AS A 90s COMIC PANEL
→ INKED IT WITH A BRUSH: SPOT BLACKS, FEATHERING, CROSS-HATCHING
→ HANDED IT TO A COMPUTER COLOURIST
→ COLOURED IT WITH AIRBRUSH GRADIENTS AND RIM LIGHTS
→ PRINTED IT ON CHEAP NEWSPRINT
→ RE-INKED IT FOR THE NEXT FRAME
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — 90s COMIC RENDERING
The people become 90s comic-book characters that keep the photograph's structure.
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
Keep body proportions exact: dramatic rendering, NOT exaggerated anatomy or muscles.
Keep facial proportions, eye shape, glasses and hairline exact.
INK RULES
* heavy black fills in hair, deep shadows and dark clothing
* FEATHERING: tapered parallel lines that grow out of every black shape, thick at the black, hairline at the tip
* single-direction hatching on the shadow side of faces and forms
* CROSS-HATCHING only in the darkest mid-tones
* hatch lines are pen strokes with breaks, never a mechanical screen
* thick brush contours; the outer silhouette heaviest
* extra small lines on faces, cheekbones, eyes and clothing folds
Light areas of faces stay clean and open.
COMPUTER COLOURING RULES
* bold saturated colour holds
* smooth airbrush gradients across every form (early Photoshop colouring)
* shadows pushed toward purple / indigo
* highlights hot and warm (gold, orange, pale yellow)
* hard "hot spot" highlights on skin are allowed
* a coloured rim light (gold or cyan) along one side of each figure
* a dramatic darker vignette around the frame
PAPER RULES
* matte, slightly yellowed newsprint with fibre texture
* colours sit IN the paper (slightly absorbed, never glossy)
* blacks are dense but not pure digital black
NO speech balloons. NO panel borders. NO captions. NO sound-effect text.
NO big Ben-Day pop-art dots. NO CMYK misregistration.
OBJECT CONTINUITY
If a person holds an object, ink and colour the object in the same comic style.
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
The drawing must match the source frame exactly in position, pose and timing.
If the head moves:
the drawing follows.
If the hand moves:
the drawing follows.
If the body turns:
the drawing follows.
NO floating figure.
NO previous-frame silhouette.
NO delayed inks.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel re-inked by hand.
Allow between consecutive frames:
* hatching and feathering lines to be redrawn (same directions, new strokes)
* contour lines to wobble slightly
* small changes in where hatch lines break
* paper grain to change
Keep FIXED in every frame:
* the hatching directions
* the colour scheme (purple shadows, warm highlights, rim-light colour)
* the paper colour
* every face's features
Do NOT make the boil so strong that faces flicker or change.
DO NOT
Do NOT add speech balloons, captions, panel borders or text.
Do NOT use Ben-Day pop-art dots or flat 1960s primaries.
Do NOT use halftone misregistration or neon (that is a different style).
Do NOT make clean vector manga or anime lines.
Do NOT exaggerate muscles or anatomy.
Do NOT use a mechanical screen-door hatch pattern over everything.
Do NOT leave a photographic surface.
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
* NO inks
* NO hatching
* NO colouring
* NO paper texture
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
Do NOT begin the comic-book transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – 90s COMIC BOOK STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input.
For consistency, also give the first approved styled frame as a style reference for all later frames (same inking weight, same hatch directions, same colour scheme, same paper).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, or the style rules broke (exaggerated anatomy, balloons/text, screen-door hatching, face drift) — regenerate those frames only.
The final video must feel like an EARLY-90s COMIC BOOK brought to life: heavy blacks and hatching, airbrushed computer colour, printed on newsprint, every frame re-inked.
The image should deliberately contain:
* heavy spot blacks
* feathering and cross-hatching
* thick brush contours and over-rendered faces
* saturated airbrush-gradient colour with purple shadows and hot highlights
* a coloured rim light
* matte yellowed newsprint
* recognizable people with exact proportions.
Avoid a generic comic filter.
```
