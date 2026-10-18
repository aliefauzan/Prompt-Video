# 24 — Cobalt Pixel Halftone

**Look:** Every frame is reprinted as a coarse grid of square cells in ONE cobalt-blue ink on cool white card. Deep shadows become solid navy cells, mid tones cobalt, light tones pale blue, and highlights bare paper, with thin white gutters between cells. The people get the full tonal range and a ring of cobalt cells around their silhouette. The room fades to a sparse pale ghost or disappears. In some sections the card becomes a slightly tilted sticker with a white border and a drop shadow, pasted on a collage wall of black-and-white photo tiles, red squares, black squares and wavy op-art tiles. Cell thresholds and stray cells flicker every frame.

**Also called / where it trends:** "viral halftone effect", "pixel halftone", "blue pixel effect", "mosaic threshold effect", "bitmap grid effect", "8-bit poster edit". In epicuts.studio's After Effects tutorial reel, the whole look is built from built-in effects (Mosaic → threshold → tint) and shown as a blue pixel card on a collage wall. The look spreads through "how to make the viral … effect" tutorials on Reels and TikTok.

**References:**
- https://www.instagram.com/epicuts.studio/reel/DdyktpOsI60/ (screenshots: `refs/ref_1.png` post page with the blue pixel AirPods card on the collage wall; `refs/ref_2.png` 12-frame contact sheet of the reel). "How to create the viral halftone effect entirely inside After Effects" by **epicuts.studio**. The method shown is Mosaic to about 64 blocks, pixelate, threshold into a few levels, tint one blue, then place the card on a collage wall. No written prompt was shared; this prompt is written from the visible result and that method. Credit: epicuts.studio.
- https://www.instagram.com/epicuts.studio/: creator page.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV):
- CLAHE luminance plus Canny edges, averaged into 12 px cells and cut into 5 levels (paper plus 4 blues) with per-frame threshold jitter.
- People keep the full range; the room is reduced to 0–2 levels or dropped.
- A cobalt ring of cells around each person; stray cells flip each frame; 2 px white gutters; ink density noise and paper grain.
- Four sections: full card with room, wall with room, full card people-only, wall people-only.
- The wall is 135 px tiles of B&W photo crops, red, black, grey and wavy pattern. The card is scaled to 80%, rotated about −1.6° with hand-held jitter, with a white border and drop shadow.

## Prompt

```text
I'm uploading one video clip. Convert it into a ONE-INK COBALT-BLUE PIXEL HALFTONE frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame is re-printed as a coarse PIXEL HALFTONE in ONE ink:
* a grid of SQUARE cells (about 1/130 of the frame width per cell)
* thin WHITE gutters between the cells
* ONE ink colour: COBALT BLUE, in 4 strengths plus bare paper
* deep shadows = solid deep navy-cobalt cells
* dark mid tones = cobalt cells
* light mid tones = light cobalt cells
* light tones = pale blue cells
* highlights = bare cool-white card
* slightly uneven ink inside each cell, like a real print
* a faint paper grain on the card
The result should feel like someone:
TOOK EACH VIDEO FRAME
→ BLOCKED IT INTO A COARSE MOSAIC
→ THRESHOLDED IT INTO FOUR TONES
→ PRINTED IT IN ONE COBALT INK ON WHITE CARD
→ PASTED SOME CARDS ON A COLLAGE WALL
→ PHOTOGRAPHED THEM AGAIN
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — BUILT FROM CELLS
The people become images made ONLY of blue square cells.
Even at this coarse grid the person must stay recognizable from:
* face structure (eyes, glasses, nose shadow, mouth)
* hairstyle silhouette
* clothing pattern (stripes, prints) as cell patterns
* pose
* body proportions
* movement
* hand position
* interaction with objects
Keep important edges (jaw, glasses rims, collar, arms) as continuous lines of darker cells.
SILHOUETTE RING
Around every person, put a ONE-cell-wide ring of solid cobalt cells.
This ring separates the person from the background at phone size.
TONE RULES
Use EXACTLY 5 values: paper, pale blue, light cobalt, cobalt, deep navy.
No other colours on the card.
No gradients inside a cell.
No anti-aliased soft cell edges.
Faces: mostly paper and pale blue, with the eyes, brows, glasses and shadows in cobalt and navy.
Dark clothing: mostly navy and cobalt.
Striped clothing: alternating rows of dark and light cells following the stripes.
BACKGROUND RULES
The room is a GHOST:
* in "room" sections, only its darkest shapes (TV, window frames, furniture edges) appear, as sparse pale-blue and light-cobalt cells
* in "people only" sections, the room disappears completely: bare white card with only the people
Plan which sections are which.
COLLAGE WALL SECTIONS
In some sections, the halftone card becomes a printed STICKER on a wall:
* the card is scaled to about 80% of the frame, tilted 1–2°, with a white border and a soft drop shadow
* the wall is a grid of square tiles:
  high-contrast black-and-white photo crops,
  some photo tiles tinted red,
  solid red squares,
  solid black squares,
  grey squares,
  black-and-white wavy op-art stripes
* the wall stays FIXED within a section (same tiles every frame)
* the card wobbles very slightly, as if hand-held or freshly stuck
Alternate between full-frame card sections and wall sections, changing only at section boundaries.
OBJECT CONTINUITY
If a person holds an object (phone, cup, bag), the object is also built from blue cells.
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
The cell image must match the source frame exactly in position, pose and timing.
The grid itself stays FIXED to the frame (cells do not slide with the person).
The person moves THROUGH the grid, so cells switch on and off as they pass.
NO lagging silhouettes.
NO previous-frame cells left behind.
FRAME-TO-FRAME BEHAVIOUR
THIS IS CRITICAL.
Every frame is a separate print.
Allow between consecutive frames:
* the four tone thresholds to drift very slightly, so borderline cells flicker between two blues
* a few stray cells to drop out or double up (misprints)
* ink density inside cells to vary
* paper grain to change
* the sticker card to wobble by a pixel or two and a fraction of a degree
Keep FIXED within a section:
* the cell size and the grid position
* the ink colours
* the wall tiles
* the card's scale and rough tilt
DO NOT
Do NOT use round halftone dots; cells are SQUARE.
Do NOT use more than one ink colour on the card.
Do NOT use smooth gradients or a soft blur.
Do NOT make the grid so fine that it reads as a normal photo.
Do NOT make it so coarse that faces are unreadable.
Do NOT let the grid slide or rotate within a full-frame section.
Do NOT add glow, chromatic aberration or scanlines.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
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
* NO mosaic or pixel grid
* NO threshold or blue tint
* NO collage wall
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
Do NOT begin the halftone transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – COBALT PIXEL HALFTONE STYLING (AFTER MY CONFIRMATION ONLY)
1. Plan the sections and list them for me: frame range, layout (full-frame card or sticker on the wall), and whether the room is a ghost or removed.
2. For each wall section, generate the collage wall ONCE with Seedream 5.0 Pro and reuse that same wall image for every frame of the section.
3. Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame (and, in wall sections, the section's wall image).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the grid or the one-ink rule broke — regenerate those frames only.
The final video must feel like a ONE-INK COBALT PIXEL PRINT come to life: square blue cells, white gutters, people readable from cells alone, sometimes pasted as a sticker on a black, red and photo-tile wall.
The image should deliberately contain:
* a fixed grid of square cells
* white gutters
* exactly four cobalt strengths plus paper
* a cobalt ring around each person
* a ghosted or removed room
* flickering borderline cells and misprints
* a collage-wall sticker layout in some sections.
Avoid a smooth blue photo filter.
```
