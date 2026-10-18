# 19 — Watercolor Ink Wash

**Look:** a loose urban-sketcher painting on every frame. A fine sepia-black ink line catches the faces, glasses, hands and clothes. Transparent watercolour washes sit on top, painted loosely and a few millimetres off the line. Highlights are left as white paper. Pigment pools into dark drying edges, cauliflower blooms and grainy granulation, with a few splatter flicks. The figures dissolve into white paper toward the edges of the frame. Every frame is repainted, so the washes breathe.

**Also called / where it trends:** "watercolor effect", "watercolor animation", "ink and wash", "line and wash", "urban sketch style", "watercolor AI video filter", "painted memories edit". AI video tools sell it as a named style preset (Filmaris, Media.io, FrameJam, Flick, Morphic), and Pinterest is full of loose line-and-wash portrait boards.

**References:**
- https://www.pinterest.com/search/pins/?q=loose%20watercolor%20ink%20line%20portrait (screenshot `refs/ref_1.png`): loose line-and-wash portraits. A confident ink line, colour spilling past it, white paper left for the light, washes fading out at the edges.
- https://filmaris.com/styles/watercolor (screenshot `refs/ref_2.png`): a watercolour video style page. It names the key traits: soft edges, transparent washes, paper glow, blooms and granulation.
- https://www.media.io/ai/video-to-video/watercolor-animation: a video-to-video watercolour animation tool, with examples of whole-frame painted motion.
- https://www.framejam.ai/styles/ink-wash: the ink-wash style preset. The ink carries the drawing and the wash carries the mood.
- https://flick.art/tools/watercolor: a watercolour video filter, useful as a contrast to what the "flat filter" look gets wrong.
- https://morphic.com/resources/videos/watercolor-animation-videos: a gallery of watercolour animation examples.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV + person masks). Each frame gets:
- CLAHE + DoG ink line with a new wobble
- soft local colour pushed toward a painter's pigment set and misregistered from the line
- two subtractive glazes with edge darkening and granulation
- ragged coverage that leaves white paper
- blooms in the lower half
- splatter

## Prompt

```text
I'm uploading one video clip. Convert it into a loose hand-painted INK LINE + WATERCOLOUR WASH frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a raw hand-painted sketchbook animation built from:
* fine waterproof ink line (sepia-black fineliner / dip pen)
* loose transparent watercolour washes
* colour that spills past the line and misses it
* white paper left for every highlight
* dark pigment pooling at the drying edge of each wash
* cauliflower blooms where wet paint met wet paint
* granulating pigment settling into the paper
* soft wet-in-wet bleeds between colours
* splatter flicks from a loaded brush
* edges of the picture dissolving into white paper
* cold-press watercolour paper texture
* urban-sketcher / travel-journal painting
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ TRACED THE PEOPLE AND THE ROOM IN INK
→ FLOODED LOOSE WASHES OVER THE TOP
→ DROPPED IN DARKER COLOUR WHILE IT WAS WET
→ LET IT BLOOM AND DRY
→ SCANNED THE PAGE
→ PAINTED THE NEXT FRAME ON A NEW SHEET
→ ANIMATED THE PAGES FRAME-BY-FRAME.
CHARACTER — PAINTED, NOT REINVENTED
The MAIN HUMAN SUBJECT becomes a WATERCOLOUR SKETCH, but a FAITHFUL portrait of the real frame.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing and clothing pattern
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT invent a new face.
Do NOT turn them into an anime, cartoon or children's-book character.
Do NOT idealize or beautify them.
The ink line carries the likeness; the wash only adds colour and light.
INK LINE
Draw the line like a confident sketcher working fast.
Use:
* a fine, slightly varying line, darker on the outer contour of each person
* selected inner lines: eyes, brows, nose, mouth, glasses, ears, hands, collar, main folds
* NOT every edge — leave some edges for the wash to describe
* small breaks where the pen lifted
* short overshoots and an occasional second searching line
* lighter, sparser ink in the background
The line should NOT be uniform vector line art.
It should NOT look like an edge-detection filter.
WATERCOLOUR WASH
The wash is the heart of the style.
Paint it like a loose sketcher, not a colouring book:
* washes are TRANSPARENT — the ink line and paper show through
* the wash is offset from the line by a few millimetres; it misses edges and spills past them
* big simple shapes: one wash for the shirt, one for the hair, one for the skin, one for the shadow side
* a second, darker glaze only in the shadows
* LIGHT AREAS ARE WHITE PAPER, never white paint
* colours mix and bleed into each other where they touch
* every wash has a hard, slightly darker drying edge
WATER EFFECTS
Add the real behaviour of water on paper:
* cauliflower blooms / back-runs in large flat areas (clothes, walls, floor)
* granulation: speckled pigment settling in the paper texture
* soft wet-in-wet bleeds
* a few splatter dots and flicks
* uneven pigment density inside each wash
Keep blooms OFF the faces.
FACES STAY CLEAN
Keep faces readable.
Skin should be:
* a light, warm, transparent wash
* white paper left on the forehead, nose and cheekbones
* one cooler shadow glaze on the shadow side
* clean ink features
* no heavy blooms, splatter or muddy colour across the face
The person must remain recognizable in every frame.
VIGNETTE INTO WHITE PAPER
The painting should NOT fill the frame edge to edge.
The figures are the most finished part.
The room is painted more loosely and lightly around them.
Toward the frame edges and the bottom of the frame, the washes break up and dissolve into ragged white paper, like an unfinished sketchbook page.
BACKGROUND — LOOSE AND LIGHT
Paint the original environment in the SAME style, but lighter and looser:
* walls, windows, furniture, plants and screens as a few light ink lines
* one or two pale washes
* more white paper than in the figures
The people should always read as the most saturated, most finished part of the frame.
PALETTE RULES
Use a painter's watercolour palette derived from the original colours:
* ultramarine and cerulean blue
* burnt and raw sienna
* rose madder / permanent rose
* sap green
* Payne's grey for the darkest shadows
* sepia-black ink for the line
Colours should be:
* clear and luminous, not muddy
* slightly more saturated than the photo
* allowed to drift (blue shadows, warm sienna light) like a painter would choose them
Do NOT use neon, digital gradients or opaque gouache colour.
LAYER ORDER
A typical frame reads:
WHITE COLD-PRESS PAPER
↓
FIRST LIGHT WASH (BIG SHAPES)
↓
WET-IN-WET BLEEDS AND BLOOMS
↓
SECOND SHADOW GLAZE
↓
GRANULATION AND DRYING EDGES
↓
INK LINE ON TOP
↓
SPLATTER FLICKS.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object and paint it.
Examples:
* phone
* glasses
* chair
* bag
* microphone
* clothing accessory
If an object is essential to the action, it is inked and washed in the same style.
Do NOT let it dissolve away.
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
The underlying character movement must remain exactly faithful to the source footage.
The PAINT breathes.
The HUMAN MOTION does NOT.
If the head moves:
the ink line and wash follow.
If the hand moves:
the painting follows.
If the body turns:
the contour and the washes follow.
If the character interacts with an object:
the object moves exactly with the original action.
NO washes trailing behind the body.
NO paint from the previous frame left on the page.
FRAME-BY-FRAME BREATHING EFFECT
THIS IS CRITICAL.
Every frame must look like a NEW painting on a NEW sheet.
The artwork should visibly change between consecutive frames.
Allow:
* wash edges and their offset from the line to change
* blooms to appear in new places and new shapes
* granulation and pigment density to change
* splatter to be completely new
* the ink line to wobble 1–3 pixels and break in new places
* the white-paper edge of the vignette to change shape
* paper texture to change
This creates a living, BREATHING watercolour animation.
CONTROLLED BREATHING
The variation must stay SMALL.
Colour choices for each element (shirt, hair, skin, walls) stay the SAME across frames.
Faces keep the same features and the same light pattern.
Do NOT let colours jump or flicker between frames.
Do NOT let the composition or the vignette jump wildly.
DO NOT
Do NOT use a generic "watercolor filter" or a smooth blur look.
Do NOT paint opaque, flat, poster-like colour.
Do NOT fill every area evenly edge to edge.
Do NOT paint white highlights — leave the paper.
Do NOT make muddy brown/grey colour.
Do NOT make it clean vector line art or a colouring-book look.
Do NOT make it anime or a children's-book illustration.
Do NOT put blooms or splatter across faces.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT freeze the paper and washes across frames.
Do NOT smooth the motion.
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
* NO ink lines
* NO watercolour washes
* NO paper texture
* NO colour grading
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
Do NOT begin the watercolour transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – WATERCOLOUR INK WASH STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the painting sits exactly on the real pose.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe: the breathing only works if every frame is painted separately.
Lock the look first: generate frame_01, show it to me with the palette you chose for each element (skin, hair, shirt, walls) and the line weight, and keep those choices for every frame.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, palette or the style rules broke — regenerate those frames only.
The final video must feel like A SKETCHBOOK THAT CAME ALIVE: real people, inked and washed by hand, repainted 12 times per second.
The image should deliberately contain:
* visible paper texture
* transparent overlapping washes
* hard drying edges
* blooms and back-runs
* granulation
* splatter
* misregistered colour
* white paper left for the light.
Avoid polished digital perfection.
```
