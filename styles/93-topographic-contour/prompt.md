# 93 — Topographic Contour Lines

**Look:** The footage becomes a printed topographic map. Brightness is read as elevation, and the whole frame is drawn as thin closed contour lines in brown map ink on cream map paper: faces turn into hills with rings around the nose, cheeks and eyes, striped shirts turn into ridges and valleys, the window becomes a plateau. Every fifth line is a heavier index contour with small elevation numbers set along it. Low ground is a deeper tan, high ground pale paper, like a layer-tinted relief map, with a faint blue grid, a double neatline border and a small legend box. Paper, grid and labels hold still; only the terrain moves with the people.

**Also called / where it trends:** "topographic lines", "topo map art", "contour line portrait", "topography aesthetic", "isoline art", "terrain map effect". A long-running Pinterest / Instagram / Behance look (contour-line portraits, topo-map posters and wallpapers) and a TouchDesigner / After Effects motion-graphics staple ("contour experiments", "generative topography", animated topographic backgrounds).

**References:**
- https://www.pinterest.com/search/pins/?q=topographic%20contour%20lines%20art (screenshot `refs/ref_1.png`, from the D2 discovery sweep): topo-line art, single-ink contour fields on plain paper, heavier index lines.
- https://www.pinterest.com/search/pins/?q=topographic%20contour%20line%20portrait (screenshot `refs/ref_2.png`): faces drawn entirely from contour lines; nose, eyes and lips as tight rings.
- https://www.instagram.com/popular/topographic-lines/: Instagram topographic-lines posts (topo posters, contour portraits, map-paper prints).
- https://www.youtube.com/watch?v=DPWZV4OTAn4: "Contour Experiments in TouchDesigner" (isolines from an image or noise field, animated).
- https://www.youtube.com/watch?v=xQtw-rLFDYQ: "Generative Topography — TouchDesigner tutorial".
- https://derivative.ca/community-post/tutorial/creating-topography-inspired-structures-touchdesigner/68332: Derivative community tutorial, topography-inspired structures in TouchDesigner.
- https://www.motionelements.com/stock-video-30457303-abstract-animated-contour-topographic-contour-map: animated topographic contour map stock clip (moving isolines on a plain ground).
- Differs from **39 LiDAR Point Cloud** (the scene as scanned dots in 3D space: here it is flat closed isolines printed on paper) and **27 Signal Relief** (horizontal scanlines displaced by brightness: here the lines follow equal brightness, closed loops in every direction, with the map paper, labels and legend of a printed survey sheet).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. A local approximation made with `render.py` (numpy + OpenCV + Pillow + the person masks). Each frame's luminance is flattened with two edge-preserving bilateral passes (so batik and stripes don't turn to noise) and becomes the elevation; the people are raised a little more as broad hills from the blurred masks, and a fixed gentle terrain swell is added to the room. Contour lines are drawn at a fixed interval as constant-width anti-aliased lines (distance to the nearest level divided by the gradient), every fifth one heavier; where lines crowd closer than about 3 px they fade out, like on a cliff. The paper has fibre texture, a faint blue grid, a layer tint by elevation and a soft hillshade; elevation numbers sit on index contours at fixed anchor points in the room, rotated along the line, plus a neatline and legend box. Paper and labels are static, so only the terrain changes from frame to frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a TOPOGRAPHIC CONTOUR LINES frame-by-frame animation: the whole scene drawn as a printed topographic map, brightness read as elevation, thin closed contour lines in brown map ink on cream map paper, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Topographic map, contour line art, isolines, USGS survey sheet, layer-tinted relief, map paper print.
Transform the footage into a frame built from:
* CONTOUR LINES only: thin, closed, never crossing, one per elevation level
* brightness read as ELEVATION: light areas are high ground, dark areas low ground
* every fifth line a heavier INDEX CONTOUR
* small ELEVATION NUMBERS set along some index contours, upright to the line, in the background only
* BROWN MAP INK on CREAM MAP PAPER with fine fibre texture
* a faint LAYER TINT: low ground a deeper tan, high ground pale paper
* a soft HILLSHADE so hills read as raised
* a faint pale-blue GRID
* a thin double NEATLINE border and a small LEGEND BOX in a corner ("CONTOUR INTERVAL 10 METERS")
The result should feel like someone:
FILMED THE SCENE
→ TREATED EACH FRAME'S BRIGHTNESS AS A TERRAIN HEIGHT MAP
→ SURVEYED IT AT A FIXED CONTOUR INTERVAL
→ PRINTED IT AS A TOPOGRAPHIC MAP SHEET
→ PLAYED THE SHEETS BACK AT 12 FPS.
CHARACTER — DRAWN IN CONTOURS, STILL RECOGNIZABLE
The people are made of contour lines like everything else, but must stay recognizable.
Faces become hills:
* the nose a tight cluster of rings
* eyes and mouth as small closed valleys
* cheekbones and forehead as rounded slopes
* hair and the face outline as bands of close lines
Each person is a broad raised hill above the room, so their silhouette reads.
Preserve the person's exact:
* identity
* face shape and features
* expression
* hairstyle
* glasses
* clothing (patterns become contour textures: stripes as parallel ridges, batik as small rings)
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT replace faces with generic contour patterns.
Do NOT put elevation numbers or the legend on a person.
THE LINES
* Constant thin width, smooth, anti-aliased, closed loops or running off the frame edge.
* Lines never cross or touch.
* Evenly spaced on gentle slopes, packed tight on steep ones; where they would merge, let them drop out (cliff).
* Index contours about twice as heavy.
* No fill inside the lines other than the soft layer tint.
PALETTE
Cream map paper.
Brown ink (sepia / USGS contour brown).
Tan layer tint.
Very faint pale blue grid.
Dark grey neatline and legend text.
Do NOT use photo colours, skin tones or saturated colour.
OBJECT CONTINUITY
Objects in a hand are drawn in contours too and stay in the hand.
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
The terrain must follow the source frame exactly: when a person moves, their hill moves with them.
NO lines that ignore the people.
NO photo showing through.
FRAME-TO-FRAME MAP CONTINUITY
THIS IS CRITICAL.
It must feel like one map sheet whose terrain shifts with the footage, not a new drawing every frame.
Keep FIXED in every frame:
* the paper, its texture and the grid
* the neatline and the legend box
* the contour interval and line weights
* the label style and their rough positions
Between consecutive frames:
* lines shift smoothly with the moving people
* still areas of the room keep the same lines
* no new random lines appear and vanish
DO NOT
Do NOT show the original photo.
Do NOT draw outlines or sketch strokes instead of contours.
Do NOT make lines cross, break or scribble.
Do NOT use horizontal scanlines.
Do NOT turn it into dots or a point cloud.
Do NOT use 3D perspective or a tilted terrain view: the map is flat and straight-on.
Do NOT redraw the people in a different pose.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
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
* NO contour lines
* NO map paper
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
Do NOT begin the topographic transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – TOPOGRAPHIC CONTOUR STYLING (AFTER MY CONFIRMATION ONLY)
First, style ONE frame as the master map sheet and show it to me: paper, grid, neatline, legend, contour interval, line weights, label style.
Then style EVERY extracted frame individually with Seedream 5.0 Pro, using the master sheet as the style reference.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the terrain follows that exact frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing or map continuity broke — regenerate those frames only.
The final video must feel like A LIVING TOPOGRAPHIC MAP: the scene and the people surveyed as terrain, brown contour lines on cream paper, shifting with the footage at 12 frames per second.
The image should deliberately contain:
* thin closed contour lines everywhere
* heavier index contours with small elevation numbers
* faces readable as contour hills
* cream paper, faint grid, layer tint, neatline and legend.
Avoid photo show-through, scanlines and crossing lines.
```
