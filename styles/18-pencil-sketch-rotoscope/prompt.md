# 18 — Pencil Sketch Rotoscope

**Look:** the a-ha "Take On Me" look. Every frame is traced over in graphite on toothy grey-white sketch paper. Confident dark contours, hand cross-hatching that builds the shadows, dark scribbled hair and clothes, faces left mostly as clean paper, loose construction lines, smudges. The lines are redrawn every frame, so the drawing boils.

**Also called / where it trends:** "Take On Me effect", "a-ha sketch effect", "pencil rotoscope", "sketch rotoscope", "Fake Drawn Me" (Red Giant / Maxon tutorial name), "boiling line animation", "pencil sketch filter edit". It shows up in After Effects and Nuke VFX tutorials on YouTube, Reddit r/VideoEditing, r/kdenlive and r/NukeVFX threads, and Pinterest boards of rotoscope and Take On Me pencil frames.

**References:**
- https://www.pinterest.com/search/pins/?q=take%20on%20me%20pencil%20sketch%20rotoscope (screenshot `refs/ref_1.png`): rotoscoped pencil figures, hatching blocks in the shadows, dark scribbled hair, faces left as open paper.
- https://www.cartoonbrew.com/tools/recreate-a-has-iconic-take-on-me-video-with-this-after-effects-template-207487.html (screenshot `refs/ref_2.png`): Cartoon Brew on the "Fake Drawn Me" template. Note the grey paper, the heavy scribble shading and the loose swirl strokes.
- https://www.maxon.net/en/article/fake-drawn-me-new-take-on-me-music-video-vfx-tutorial: Maxon / Red Giant "VFX Side Quest" tutorial that turns live footage into the hand-drawn Take On Me look.
- https://digitalproduction.com/2021/08/05/fake-drawn-me-tutorial/: Digital Production write-up of the same tutorial.
- https://www.youtube.com/watch?v=ncik0D5b7Pk: "Take On Me" music video VFX tutorial with a free template.
- https://www.reddit.com/r/VideoEditing/comments/jf3a0o/the_classic_music_video_take_on_me_how_to/: editors discussing how to get the effect today. The consensus is that real rotoscoping per frame beats a single filter.
- https://www.reddit.com/r/kdenlive/comments/jl13u2/update_one_method_for_achieving_the_rotoscoping/: an open-source workflow for the same look.
- https://www.reddit.com/r/NukeVFX/comments/1igm5vd/rotoscope_take_on_me/: Nuke compositors rotoscoping "Take On Me".
- https://forum.derivative.ca/t/aha-take-on-me-effect/497764: a real-time (TouchDesigner) attempt at the effect.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV + person masks). Each frame gets new DoG contour lines warped differently, three randomised hatching layers keyed to tone, scribble fill in the darkest areas, construction lines, graphite smudge and paper tooth.

## Prompt

```text
I'm uploading one video clip. Convert it into a hand-drawn GRAPHITE PENCIL ROTOSCOPE frame-by-frame animation in the style of the a-ha "TAKE ON ME" music video, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a raw hand-drawn pencil animation built from:
* soft graphite pencil on paper (HB to 6B)
* confident dark contour lines
* hand cross-hatching for all shading
* dense scribbled darks in hair and dark clothing
* faces and skin left mostly as clean paper
* loose construction lines and overshooting strokes
* doubled, searching lines where the artist re-drew a contour
* graphite smudges and finger-blending
* eraser lifts and highlights
* visible paper tooth breaking up every stroke
* warm grey-white sketch paper
* "boiling" lines that are redrawn every frame
* 1980s rotoscoped music-video animation
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ PUT IT ON A LIGHT BOX
→ LAID A FRESH SHEET OF SKETCH PAPER ON TOP
→ TRACED THE PEOPLE AND THE ROOM IN PENCIL
→ SHADED EVERYTHING WITH HAND HATCHING
→ SMUDGED AND ERASED BY HAND
→ SCANNED THE SHEET
→ DID IT AGAIN FOR THE NEXT FRAME
→ ANIMATED THE SHEETS FRAME-BY-FRAME.
CHARACTER — TRACED, NOT REINVENTED
The MAIN HUMAN SUBJECT becomes a PENCIL DRAWING, but a FAITHFUL TRACING of the real frame.
This is rotoscoping: the drawing sits exactly on top of the photographed person.
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
Do NOT turn them into a cartoon, anime or caricature.
Do NOT simplify them into a generic sketch person.
Proportions, features and silhouette come from the photo, line for line.
GRAPHITE LINE WORK
Draw the line work like a skilled illustrator tracing fast.
Use:
* a strong, slightly darker OUTER CONTOUR around each person
* thinner inner lines for eyes, brows, nose, lips, ears, glasses, collar, folds and seams
* lines that taper and change pressure
* small breaks where the pencil lifted
* occasional DOUBLED lines, 2–6 pixels apart, where the contour was re-drawn
* short overshoots past corners
* a few faint CONSTRUCTION LINES running off the figure into the background
The line should NOT be a uniform digital stroke.
It should NOT look like an edge-detection filter.
It must look DRAWN.
CROSS-HATCHING SHADES EVERYTHING
Build all tone with hand hatching, never with smooth grey fills.
Use:
LIGHT TONES → paper left blank
MID TONES → one layer of parallel diagonal hatching
SHADOWS → a second layer crossing the first
DEEP SHADOWS → a third layer + dense scribble
DARKEST AREAS (hair, black clothes, pupils) → heavy back-and-forth scribble, almost solid graphite
Hatching rules:
* strokes are short, straight-ish and slightly curved at the ends
* spacing is uneven
* direction follows the form where it can (around the arm, down the shirt)
* hatch boundaries are ragged, not clean
* patterns in clothing (stripes, batik, prints) are DRAWN as pattern, not photographed
FACES STAY CLEAN
Keep faces readable.
Skin should be mostly blank paper with:
* clean feature lines
* light hatching only under the jaw, under the nose, in the eye sockets and along one side of the face
* no heavy cross-hatching across the cheeks
The person must remain recognizable in every frame.
SMUDGE + ERASER
Add hand-made graphite texture:
* finger smudges beside dark areas
* soft grey haze where graphite dragged
* eraser lifts on bright highlights (forehead, cheekbones, lit shirt areas)
* faint ghost lines from erased earlier attempts
Keep it subtle.
PAPER
Every frame is ONE SHEET of sketch paper.
The paper should feel like:
* warm grey-white drawing paper
* visible tooth / grain that breaks up the graphite
* slightly darker, handled edges
* tiny fibres and dust
It should NOT look like a clean digital white canvas.
BACKGROUND — DRAWN LIGHTER
Trace the original environment in the SAME pencil style, but lighter and looser than the people:
* walls, windows, furniture, plants and screens as loose outlines
* only sparse hatching in the darkest background areas
* some background lines left unfinished or fading out
* more empty paper than in the figures
The people should always read as the most finished, darkest drawing in the frame.
OPTIONAL — REAL ↔ SKETCH CROSSOVER
For one or two short moments (if I ask for it), use the Take On Me crossover:
the person stays PHOTOGRAPHIC but their edges, hair and clothes dissolve into pencil hatching, or a pencil-drawn hand reaches out of the sketch world.
Default: the WHOLE frame is pencil.
PALETTE RULES
Keep the palette almost completely MONOCHROME.
Use only:
GRAPHITE BLACK
GRAPHITE GREYS
PAPER WHITE / WARM GREY.
About 100% of the frame stays graphite on paper.
Do NOT add colour.
Do NOT add sepia filters, coloured pencils or tinted highlights.
LAYER ORDER
A typical frame reads:
GREY-WHITE SKETCH PAPER
↓
LIGHT BACKGROUND TRACING
↓
CONSTRUCTION LINES AND SMUDGES
↓
FIGURE HATCHING (1–3 LAYERS)
↓
DARK SCRIBBLE IN HAIR AND DARK CLOTHES
↓
CONTOUR AND FEATURE LINES ON TOP
↓
ERASER HIGHLIGHTS.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object and draw it.
Examples:
* phone
* glasses
* chair
* bag
* microphone
* clothing accessory
If an object is essential to the action, it is traced in the same pencil style.
Do NOT accidentally drop it from the drawing.
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
The LINES boil.
The HUMAN MOTION does NOT.
If the head moves:
the drawing follows.
If the hand moves:
the drawing follows.
If the body turns:
the contour and hatching follow.
If the character interacts with an object:
the object moves exactly with the original action.
NO drawing lagging behind the body.
NO contour from the previous frame.
NO face that stays still while the head moves.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame must look like a NEW drawing traced by hand on a new sheet.
The artwork should visibly change between consecutive frames.
Allow:
* contour lines to wobble 1–4 pixels
* doubled lines to appear and disappear
* hatching direction to rotate slightly (about ±15°)
* hatching spacing and stroke breaks to change
* scribble texture to be completely redrawn
* construction lines to move and change
* smudges to shift
* paper tooth and fibres to change
* paper position to shift by a pixel or two
This creates the classic BOILING pencil animation.
CONTROLLED BOIL
The boil must stay SMALL.
Feature lines (eyes, mouth, glasses) wobble but stay on the features.
Do NOT let faces melt, shift or change shape between frames.
Do NOT let the hatching flicker so hard it becomes noise.
DO NOT
Do NOT use a generic "sketch filter" or edge-detection look.
Do NOT use smooth grey gradients instead of hatching.
Do NOT add colour.
Do NOT make it clean vector line art.
Do NOT make it a comic-book / manga inking style.
Do NOT make it glossy or polished.
Do NOT over-hatch faces.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT beautify or stylize the face into a cartoon.
Do NOT freeze the paper texture across frames.
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
* NO pencil lines
* NO hatching
* NO paper texture
* NO black-and-white conversion
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
Do NOT begin the pencil transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – PENCIL ROTOSCOPE STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the tracing sits exactly on the real pose.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe: the boil only works if every frame is drawn separately.
Lock the look first: generate frame_01, show it to me with the paper tone, line weight and hatching density you chose, and keep those settings for every frame.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like THE TAKE ON ME SKETCH WORLD: real people, traced in pencil, boiling on paper at 12 drawings per second.
The image should deliberately contain:
* visible graphite grain
* paper tooth
* hand hatching
* doubled and searching lines
* smudges
* eraser marks
* construction lines
* slight sheet-to-sheet registration shifts.
Avoid polished digital perfection.
```
