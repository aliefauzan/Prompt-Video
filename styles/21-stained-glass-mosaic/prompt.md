# 21 — Stained Glass Mosaic

**Look:** every frame is a backlit stained-glass window. Hand-cut glass pieces are joined by dark lead came: small, fine pieces on the people and their faces, large bold pieces in the room. The background is cobalt and azure glass with ruby, amber, emerald and violet accents. Skin becomes pale rose-white glass, with the features, hair and folds painted on in dark grisaille. Light glows through the glass with a soft bloom, streaks and bubbles. The cuts are re-made every frame, so the window shimmers and boils while the people move exactly as in the video.

**Also called / where it trends:** "stained glass transformation", "stained glass AI filter", "stained glass effect", "cathedral glass", "mosaic AI video", "lead-line glass art". It appears as a template on AI video platforms (Magic Hour, Oakgen, VEED, Crreo), in "stained-glass film style" motion-graphics skills, and on Pinterest boards of stained-glass portraits.

**References:**
- https://www.pinterest.com/search/pins/?q=stained%20glass%20portrait%20art (screenshot `refs/ref_1.png`): stained-glass portraits. Two dominant hues (cobalt plus ruby/amber) carry the picture, faces are pale glass with painted features, and the black came gets heavier at the figure outline.
- https://magichour.ai/templates/details/cmnh529no01hm2x0z4x3dbsc5-stained-glass-transformation (screenshot `refs/ref_2.png`): the Magic Hour "Stained Glass Transformation" template, made with Kling 3.0. Its own prompt: "Black leading outlines sections, translucent colors glow with backlight".
- https://oakgen.ai/template-tool/stained-glass: a stained-glass template tool showing the image-to-glass conversion.
- https://www.veed.io/tools/ai-image-editor/stained-glass-generator: a stained-glass generator. A useful contrast: uniform Voronoi cells read as a filter, not as a window.
- https://motionsites.org/skills/motion-graphics/stained-glass-film-style: a stained-glass film-style guide (lead weight, backlight glow, colour families).
- https://www.reclip.io/claude-opus-5-5-video-prompts/lemo-stained-glass: an example stained-glass video prompt and result. Key rule: the glass never bends or morphs, only the light changes.
- https://www.crreo.ai/styles/mosaic-ai-video: mosaic AI video style.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV + person masks). Each frame gets:
- Voronoi pieces dense on people, split by k-means colour zones and the person outline, with the cut re-made every second and jittered every frame
- wobbly lead, heavier at the figure outline
- jewel-toned glass, with the background re-glazed in cobalt plus accents and skin as pale rose glass
- core glow, streaks and bubbles
- grisaille paint for features
- backlight bloom and a shifting sun

## Prompt

```text
I'm uploading one video clip. Convert it into a BACKLIT STAINED-GLASS WINDOW frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a hand-made stained-glass window built from:
* hand-cut pieces of coloured glass
* dark lead came joining every piece
* small, fine pieces on the people and faces
* large, bold pieces in the background
* deep jewel colours: cobalt, azure, ruby, amber, emerald, violet
* pale rose-white / opal glass for skin
* dark grisaille paint for features, hair strands and folds
* light glowing THROUGH the glass from behind
* soft bloom around the brightest pieces
* streaks, ripples and bubbles inside each sheet of glass
* each piece slightly darker near its lead, brighter in the middle
* a cathedral / Tiffany window feeling
The result should feel like someone:
PRINTED THE VIDEO FRAME AS A CARTOON (FULL-SIZE PATTERN)
→ CUT EVERY SHAPE FROM COLOURED GLASS BY HAND
→ PAINTED THE FACES AND DETAILS IN GRISAILLE AND FIRED THEM
→ JOINED THE PIECES WITH LEAD CAME
→ HUNG THE WINDOW IN FRONT OF THE SUN
→ PHOTOGRAPHED IT
→ CUT A NEW WINDOW FOR THE NEXT FRAME
→ ANIMATED THE WINDOWS FRAME-BY-FRAME.
CHARACTER — CUT IN GLASS, NOT REINVENTED
The MAIN HUMAN SUBJECT becomes STAINED GLASS, but a FAITHFUL portrait of the real frame.
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
Do NOT turn them into a saint, icon or medieval figure.
Do NOT change their clothes into robes.
The silhouette and pose come from the photo, piece by piece.
GLASS PIECES
Cut the picture like a real glazier, not like a mosaic filter:
* follow the real forms: one piece for a cheek, one for the forehead, pieces that follow the folds of a shirt, the shape of the hair, the arms
* SMALL pieces on faces, hands and hair
* MEDIUM pieces on clothes and the body
* LARGE pieces in the walls, floor and windows
* shapes are irregular but cuttable: gentle curves and straight cuts, no impossible spikes
* every piece is ONE colour of glass (with its own internal streaks)
* clothing patterns become groups of differently coloured pieces
Do NOT use uniform hexagons, tiles or a regular Voronoi grid.
LEAD CAME
* dark charcoal / near-black lead lines between ALL pieces
* the HEAVIEST lead runs around the outline of each person
* medium lead in the background
* thinner lead between pieces inside faces and hands
* lead is slightly uneven and hand-bent, with a faint metallic highlight along one edge
* small solder blobs at some joints
GRISAILLE — FACES STAY RECOGNIZABLE
Glass pieces alone cannot hold a likeness, so paint the details on the glass:
* eyes, brows, nose, lips, glasses and ear shapes in dark brown-black grisaille line
* soft matting (half-tone shading) for the shadow side of the face and the eye sockets
* hair strands and clothing folds painted on top of the glass
* skin in pale rose-white, opal or very light amber glass
The person must remain recognizable in every frame.
BACKLIGHT
The window is lit from BEHIND.
* bright pieces glow and bloom softly into their neighbours
* deep colours stay rich and dark, not grey
* light varies slowly across the window, as if the sun moves behind it
* the edges and corners of the window are slightly darker
* no front-lit reflections, no shiny plastic look
BACKGROUND — THE WINDOW FIELD
Turn the original environment into the window's background glass:
* keep the main shapes of the room (walls, windows, furniture, screens, plants) as large pieces
* neutral walls and greys become COBALT / AZURE / DEEP BLUE glass
* about 15% of the background pieces are accents: RUBY, AMBER, EMERALD, VIOLET
* background pieces are bigger and simpler than the figures
The people must stand out clearly against the blue field.
PALETTE RULES
Two hues should carry the picture: COBALT BLUE and RUBY / AMBER.
Use:
COBALT / AZURE / DEEP BLUE (background field)
RUBY RED
AMBER / GOLD
EMERALD GREEN
VIOLET (sparingly)
PALE ROSE-WHITE / OPAL (skin)
CHARCOAL LEAD
BROWN-BLACK GRISAILLE.
Keep the person's clothing colours, translated into the nearest jewel glass.
Do NOT use pastel, neon or muddy colour.
Do NOT make skin orange or saturated pink.
LAYER ORDER
A typical frame reads:
BACKLIGHT (SUN BEHIND THE WINDOW)
↓
COLOURED GLASS PIECES
↓
STREAKS, RIPPLES AND BUBBLES IN THE GLASS
↓
GRISAILLE MATTING AND LINE PAINT
↓
LEAD CAME + SOLDER
↓
GLOW / BLOOM
↓
DARKER WINDOW EDGES.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object and cut it in glass.
Examples:
* phone
* glasses
* chair
* bag
* microphone
* clothing accessory
If an object is essential to the action, it gets its own pieces of glass.
Do NOT let it merge into the background.
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
The GLASS CUT shimmers.
The HUMAN MOTION does NOT.
If the head moves:
the pieces of the head move with it.
If the hand moves:
the glass hand follows.
If the body turns:
the lead outline and pieces follow.
If the character interacts with an object:
the object moves exactly with the original action.
NO pieces lagging behind the body.
NO window from the previous frame.
NO glass that bends, melts or morphs.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame must look like a NEWLY CUT window.
The artwork should visibly change between consecutive frames.
Allow:
* lead lines to shift by a few pixels
* pieces to be cut slightly differently (a little larger, smaller, split or merged)
* glass streaks and bubbles to change
* the brightness of individual pieces to flicker slightly
* the light behind the window to drift
About once per second, allow a bigger re-cut of the background pieces, keeping the same colour families.
This creates a shimmering, BOILING stained-glass animation.
CONTROLLED BOIL
The boil must stay SMALL.
The colour of each element (shirt, hair, skin, wall) stays the SAME across frames.
Faces keep the same grisaille features and the same glass colour.
Do NOT let colours jump between frames.
Do NOT let the pieces flicker so hard it becomes noise.
DO NOT
Do NOT use a uniform Voronoi / hexagon / tile mosaic filter.
Do NOT use a cracked-glass or broken-mirror effect.
Do NOT make it a flat vector illustration.
Do NOT make it look like plastic or a front-lit poster.
Do NOT make faces out of tiny confetti pieces with no painted features.
Do NOT make skin orange or saturated.
Do NOT let the glass bend or morph like liquid.
Do NOT turn the people into religious icons or robed figures.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT freeze the same cut across all frames.
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
* NO glass pieces
* NO lead lines
* NO glow
* NO colour changes
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
Do NOT begin the stained-glass transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – STAINED GLASS STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the window sits exactly on the real pose.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe: the boil only works if every window is cut separately.
Lock the look first: generate frame_01, show it to me with the glass colour you chose for each element (skin, hair, shirt, background field, accents) and the lead weight, and keep those choices for every frame.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, palette or the style rules broke — regenerate those frames only.
The final video must feel like A CATHEDRAL WINDOW THAT CAME ALIVE: real people, cut in jewel glass and lead, glowing in the sun, re-cut 12 times per second.
The image should deliberately contain:
* visible lead came
* hand-cut irregular pieces
* glass streaks and bubbles
* grisaille painted features
* backlight glow and bloom
* uneven light across the window
* slight cut-to-cut shifts.
Avoid polished digital perfection.
```
