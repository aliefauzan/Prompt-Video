# 58 — LEGO Brick Build

**Look:** every frame is rebuilt out of real LEGO: the people become studs-out brick mosaics on a fine stud grid (every stud a moulded cylinder with a rim light, drop shadow and specular dot), the room becomes a bigger-brick backdrop. Colours are quantised to the real LEGO palette (white, light/dark bluish grey, reddish brown, nougat skin tones, dark green, sand blue...), same-colour studs merge into 1x1–1x4 bricks with seams and bevels, glossy ABS plastic sheen, warm macro photography with shallow depth of field and tilt-shift blur on the backdrop. Static bricks hold still; only the bricks the people move through get "rebuilt" each frame, like brick-built stop-motion.

**Also called / where it trends:** "LEGO style", "LEGO filter", "brick world / brick build video filter", "AI LEGO animation", "brickfilm", "LEGO mosaic", "LEGO minifigure trend" — AI video-effect tools (frameloop, Pollo, Mootion, VidGuru, Flixly), TikTok / Reels "turn yourself into LEGO" edits, GitHub LEGO-mosaic shaders (2026).

**References:**
- https://frameloop.ai/visual-styles — Frameloop "Lego" visual style card, screenshot `refs/ref_1.png`. Frameloop's own style prompt: *"lego style, macro shot, lego blocks, plastic lego bricks, primary colors, minifigure proportions"* (this prompt credits and expands it into the full video workflow below; the card's "try it" link goes to a sign-in page)
- https://www.vidguru.ai/video-effects/video-to-brick-world — "AI Brick World Video Filter", screenshot `refs/ref_2.png`: a person rebuilt from studded bricks, room as brick backdrop
- https://pollo.ai/app/lego-video-generator — LEGO video generator / filter
- https://www.mootion.com/use-cases/en/lego-animation-video-filter — LEGO animation video filter
- https://www.flixly.ai/dashboard/video-tools/lego-style — Flixly "lego style" video effect
- https://github.com/chriscarrollsmith/legofield-shader — open-source LEGO-field shader (stud grid, stud lighting)

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (all 179 frames at 12 fps), `preview.webp`. Local approximation rendered with `render.py` (numpy + OpenCV + person masks: 12 px stud grid for the people, 24 px for the room, Lab nearest LEGO colour with hysteresis, procedural stud sprites); the six sheet frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a LEGO BRICK BUILD frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
STYLE SOURCE
This look starts from the Frameloop "Lego" visual style (frameloop.ai/visual-styles), whose style prompt is:
"lego style, macro shot, lego blocks, plastic lego bricks, primary colors, minifigure proportions".
Everything below expands that prompt into a full frame-by-frame video workflow.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a brick-built world made from:
* REAL LEGO bricks and plates, studs facing the camera (studs-out mosaic build)
* a visible STUD GRID: every stud a moulded cylinder, all studs the same size
* the people built from SMALL bricks (fine stud grid, enough studs for eyes, brows, mouth, glasses)
* the room built from BIGGER bricks (coarser grid) as a backdrop
* colours QUANTISED to the real LEGO colour palette, no in-between colours
* bricks of 1x1, 1x2, 1x3, 1x4 with thin dark SEAMS between them
* glossy ABS PLASTIC: rim light on every stud, small specular dot, soft drop shadow beside each stud
* bevelled brick edges catching the light
* MACRO PHOTOGRAPHY: shallow depth of field, the backdrop softly out of focus, tilt-shift falloff top and bottom
* warm toy-photography light from the upper left, soft bloom on bright plastic
* a slight vignette and very fine sensor noise
The result should feel like someone:
FILMED THE CLIP
→ SORTED A HUGE TUB OF LEGO BY COLOUR
→ REBUILT EVERY FRAME STUD BY STUD
→ BUILT THE ROOM AS A BRICK BACKDROP
→ LIT IT LIKE A TOY PHOTOGRAPHER
→ SHOT IT WITH A MACRO LENS
→ ANIMATED IT FRAME-BY-FRAME, BRICK BY BRICK.
CHARACTER — BRICK-BUILT PEOPLE
The MAIN HUMAN SUBJECT(S) are rebuilt as brick mosaics, NOT replaced by stock minifigures.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* clothing
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT turn them into generic yellow minifigures.
Do NOT change body proportions into a minifigure body.
Do NOT smooth the face into a flat plastic mask: the eyes, brows, nose shadow, mouth and glasses must still be readable as stud colours.
LEGO PALETTE RULES
Use only real LEGO colours, for example:
* White, Light Bluish Gray, Dark Bluish Gray, Pearl Dark Gray, Black
* Red, Dark Red, Reddish Brown, Dark Brown, Medium Brown
* Light Nougat, Nougat, Medium Nougat, Dark Nougat (skin tones)
* Tan, Dark Tan, Yellow, Dark Orange
* Olive Green, Green, Dark Green
* Medium Azure, Medium Blue, Blue, Dark Blue, Sand Blue
* Bright Pink, Dark Pink (blush, lips, accents only)
Skin uses the NOUGAT range that matches the person's real skin tone (never classic minifigure yellow).
Hair uses Black / Dark Brown / Reddish Brown.
Each clothing area keeps its real colour, mapped to the nearest LEGO colour.
Patterns (stripes, prints) are rebuilt from studs of the matching colours.
No gradients inside a single stud.
PEOPLE BRICKS
* fine grid: about 130–140 studs across the frame width
* every stud fully one colour
* same-colour studs in a row merge into longer bricks (1x2–1x4), different colours always start a new brick
* the silhouette edge follows whole studs (stepped, pixel-like edge), no soft matte
* lone single studs of a stray colour are removed (cleaner build)
* the people stay SHARP: they are the focus plane
ROOM / BACKDROP BRICKS
* coarse grid: about half the stud count of the people (bigger bricks)
* same palette, the room's real colours mapped to LEGO colours
* windows, walls, desks, plants and screens remain recognisable as brick shapes
* the backdrop sits behind a MACRO depth-of-field blur: studs still visible but soft
* stronger tilt-shift blur toward the top and bottom of the frame
* a soft contact shadow of the brick figures falls on the backdrop
BACKGROUND OPTIONS
ORIGINAL ENVIRONMENT:
the real room, rebuilt in bigger bricks, softly out of focus.
BASEPLATE STUDIO (for selected sections, optional):
a plain LIGHT BLUISH GRAY or WHITE stud wall behind the people, still out of focus.
The people stay exactly where they are in the original frame.
LAYER ORDER
A typical frame reads:
BRICK BACKDROP (coarse grid, macro blur)
↓
CONTACT SHADOW
↓
BRICK-BUILT PEOPLE (fine grid, sharp)
↓
STUD LIGHTING (rim light, drop shadow, specular dot, seams, bevels)
↓
PLASTIC SHEEN + BLOOM
↓
WARM GRADE, VIGNETTE, FINE NOISE.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object, rebuilt in bricks.
Examples:
* phone
* cup
* chair
* bag
* microphone
* headphones
If the object is essential to the person's action, build it on the FINE grid together with the person.
Do NOT accidentally merge it into the backdrop or drop it.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame.
Never change:
* identity
* facial structure
* hairstyle
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
The BRICKS change.
The HUMAN MOTION does NOT change.
If the head moves:
the brick head moves exactly with it, stud by stud.
If the hand moves:
the brick hand moves in that same frame.
If the body turns:
the bricks are rebuilt to the new pose in that same frame.
If the character interacts with an object:
the brick object moves exactly with the original action.
NO lagging bricks.
NO ghost studs from previous frames.
NO bricks drifting between frames.
BRICK CONSISTENCY
THIS IS CRITICAL.
The stud grid is LOCKED for the whole clip:
* same stud size, same grid position, same lighting direction in every frame
* studs never slide, scale or rotate
Areas that do not change (walls, windows, desks, still body parts) keep EXACTLY the same bricks and colours from frame to frame.
Only the bricks that the people move through are rebuilt — like a stop-motion brickfilm where only the moving parts are swapped.
Do NOT re-randomise brick lengths, seams or colours every frame.
Do NOT let colours flicker between two neighbouring LEGO colours.
Allow, every frame:
* very fine sensor noise to change
* plastic highlights to shift slightly where the bricks are rebuilt
DO NOT
Do NOT replace the people with stock minifigures.
Do NOT use classic minifigure yellow for skin.
Do NOT use colours that do not exist in the LEGO palette.
Do NOT draw studs of different sizes.
Do NOT render smooth plastic without studs.
Do NOT blur the people.
Do NOT let the stud grid move or swim.
Do NOT add LEGO logos on the studs, brand marks or packaging.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT add text, watermarks or UI.
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
* NO bricks
* NO stud grid
* NO colour quantising
* NO depth of field
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
Do NOT begin the LEGO transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – LEGO BRICK STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Before generating, lock and report the build settings: stud count across (people grid and room grid), the LEGO colour list used, light direction, depth-of-field strength.
Use the previous styled frame as a consistency reference for the next one so unchanged bricks stay identical; if Seedream cannot hold the grid perfectly, quantise each frame to the locked stud grid and LEGO palette first and let Seedream only add the stud lighting and plastic finish.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, the stud grid or the palette broke — regenerate those frames only.
The final video must feel like a BRICKFILM: real LEGO, real studs, toy-photography light, only the moving bricks changing.
The image should deliberately contain:
* a crisp, evenly spaced stud grid
* real LEGO colours only
* brick seams and bevels
* glossy plastic studs with rim light and specular dots
* macro depth of field on the backdrop
* warm toy-photography light
* a slight vignette.
Avoid clutter: no extra props, no minifigure accessories that were not in the source.
```
