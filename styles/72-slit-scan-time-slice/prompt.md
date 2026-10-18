# 72 — Slit-Scan Time-Slice (时间切片)

**Look:** Every frame is cut into parallel diagonal strips, and each strip shows a different moment of the clip. Strips step from about 1.3 s in the past on the left to 1.3 s in the future on the right. A face, an arm or a shoulder breaks at each cut into its earlier and later pose, and the handheld background jumps across the seams too. Each strip stays perfectly sharp, with a thin white seam and a soft shadow, like photo prints laid side by side. The strip grid drifts slowly to the left, so the cuts keep re-slicing the people.

**Also called / where it trends:** "时间切片" (time slice), "狭缝扫描" (slit scan), "时间切片转场" (time-slice transition), "slit-scan", "time displacement", "time slice effect", "time-warp scan" — Bilibili Premiere Pro / After Effects tutorials (the PR教程 / AE教程 series), CapCut and TikTok "time warp scan" filters. Its roots are Douglas Trumbull's 2001 Stargate slit-scan and the slit-scan video art catalogued by Golan Levin. Browser tools ditherer ("Time Slice", "Stargate"), KRKART SlitScan and Modulate offer it as a preset.

**References:**
- https://www.bilibili.com/video/av857120801, https://www.bilibili.com/video/av1253209917, https://www.bilibili.com/video/av772306622 (contact sheet `refs/ref_1.png`, from the discovery sweep D4): Bilibili 时间切片 tutorials; the frame is cut into tilted strips, each a different moment or shot.
- https://www.pinterest.com/search/pins/?q=slit%20scan%20time%20displacement (screenshot `refs/ref_2.png`): slit-scan / time-displacement stills and the AE "Slit-Scan Displacement" tutorial thumbnail.
- http://www.flong.com/archive/texts/lists/slit_scan/index.html (screenshot `refs/ref_3.png`): Golan Levin, "An Informal Catalogue of Slit-Scan Video Artworks and Research"; slices extracted from a sequence of frames and concatenated into one image.
- https://krkart.cc/effects/slit-scan.html: KRKART SlitScan; "each row, column, or ring is sampled from a different point in the recent past".
- https://modulate.to/effects/slit-scan/: Modulate, "Slit-scan: the effect that trades space for time".
- https://nofilmschool.com/2016/11/how-to-create-2001-slit-scanning-effect: No Film School on recreating the 2001 slit-scan effect digitally.
- https://www.tiktok.com/@mr.alexaa/video/6879344833576602881 and https://www.youtube.com/watch?v=HJvIfcbk3lA (from discovery D1): the TikTok "time warp scan" filter, the continuous one-line cousin of this look.

How it differs from taken styles: **26 Slow Shutter Smear** blends earlier moments into soft streaked ghosts. Here every strip is one crisp moment with a hard edge, and nothing is blended. **29 Hyperspace Burst** is radial motion, not time slicing. **70 Pixel Stretch** repeats one pixel line from one frame; this shows real pixels from many frames.

**Why it needs multi-frame context:** each output frame is assembled from nine different source frames (the current one and four on each side, 4 frames = 1/3 s apart). A model that only sees the current frame cannot know where an arm or a head was a second earlier or later, and would have to invent those poses. So the prompt makes the generator take the neighbouring frames as extra image inputs. A video model with the whole clip in context would also work.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV). It works on the full 179-frame sequence. Nine diagonal bands are tilted 22° from vertical, and band k copies its pixels from source frame n + (k − 4) × 4, so the bands run from 16 frames back to 16 frames ahead. Indices mirror at the clip ends, so the first and last seconds still slice. Each band has a 3 px white seam and a soft shadow. The band grid drifts 2.2 px per frame. The masks are not needed, because the pixels come straight from real frames.

## Prompt

```text
I'm uploading one video clip. Convert it into a SLIT-SCAN TIME-SLICE (时间切片) frame-by-frame animation: every frame is cut into parallel diagonal strips and each strip shows a DIFFERENT MOMENT of the clip, so one image holds a sweep of time, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
This style NEEDS MULTI-FRAME CONTEXT: every styled frame is assembled from NINE neighbouring source frames, one per strip. A single frame does not contain the earlier and later poses, so they must never be invented or redrawn. Give Seedream all nine source frames as image inputs for every generation (or, if a video model with the full clip in context is used, the same strip-to-frame mapping applies). If you cannot pass several source frames into one generation, SAY SO AND STOP instead of faking it.
CORE VISUAL STYLE
Transform the footage into a time-sliced frame built from:
* NINE parallel DIAGONAL strips across the frame, cut lines tilted about 22° from vertical (top leaning left, like a backslash)
* each strip a REAL, SHARP piece of a DIFFERENT source frame
* a STAIRCASE of time: strips step 4 extracted frames (1/3 second) apart, from 16 frames in the past on the left to 16 frames in the future on the right; the centre strip is the current frame
* HARD cut edges: no blending, no fade, no blur between strips
* a thin WHITE seam line on every cut (about 3 px at 1620 px width)
* a soft SHADOW, about 20 px wide, just to the right of each seam, like one print laid on another
* people BROKEN at the cuts: a head, arm or shoulder jumps to its earlier or later pose across each seam
* the background (handheld camera) also jumping slightly across the seams
* the original colour, sharpness and grain of the footage, untouched inside each strip
The result should feel like someone:
PRINTED NINE MOMENTS OF THE CLIP
→ CUT EACH PRINT INTO THE SAME DIAGONAL STRIPS
→ TOOK STRIP 1 FROM THE OLDEST PRINT, STRIP 2 FROM THE NEXT, AND SO ON
→ LAID THE STRIPS SIDE BY SIDE WITH THIN WHITE GAPS
→ SLID THE STRIP GRID A LITTLE FOR EVERY FRAME
→ FILMED IT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, SLICED IN TIME
Inside every strip the people are EXACTLY the source pixels of that strip's frame.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing
* accessories
* pose (as it was in that strip's moment)
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT repair or smooth the breaks at the seams: the misalignment IS the style.
Do NOT beautify or re-sculpt faces.
THE STRIPS
* Strips are equal width, about 230 px measured horizontally at 1620 px frame width, and run from the top edge to the bottom edge.
* Strip order, left to right: frame −16, −12, −8, −4, 0, +4, +8, +12, +16 relative to the current frame.
* Near the start and end of the clip, where −16 or +16 does not exist, MIRROR the time index (frame −3 becomes frame 3 counted from the start, and the same at the end) so every strip still shows a different moment.
* The strip grid slides about 2 px to the left on every output frame. As a cut line passes a strip boundary, the strip sequence continues (the time pattern repeats every nine strips).
* Strips are straight and parallel. No curves, waves or rings.
PALETTE
The footage's own colours, unchanged.
Seams: clean white.
Shadows: a soft darkening of the footage, not a colour.
Do NOT grade, tint or stylise inside the strips.
BACKGROUND
The room is sliced exactly like the people, from the same strip frames.
OBJECT CONTINUITY
An object in a hand belongs to the strip's moment: it may appear twice or be cut, exactly as the source frames show.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every strip of every frame.
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
Each strip must match its source frame exactly, pixel for pixel.
The centre strip is always the current frame.
NO pose invented to "fill" a strip.
NO strip copied from the wrong frame.
FRAME-TO-FRAME BEHAVIOUR
THIS IS CRITICAL.
Allow between consecutive frames:
* every strip to advance one frame in time (each strip is a moving piece of video)
* the strip grid to slide about 2 px sideways
Keep FIXED:
* the strip angle, width and count
* the 4-frame time step between strips
* the seam and shadow look
* the footage's colours and sharpness
DO NOT
Do NOT blend, cross-fade or ghost strips together.
Do NOT motion-blur or smear.
Do NOT use a continuous one-pixel slit scan that bends faces into rubber; this style is wide, crisp strips.
Do NOT make every strip the same moment.
Do NOT add colour grades, glitches, RGB split or noise.
Do NOT redraw or illustrate the people.
Do NOT create new poses.
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
* NO strips, seams or shadows
* NO frames mixed from other moments
* NO colour change
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
Do NOT begin the time-slice transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – TIME-SLICE STYLING (AFTER MY CONFIRMATION ONLY)
First, give me the strip table: for three sample frames (one near the start, one in the middle, one near the end), list which extracted frame feeds each of the nine strips, including any mirrored indices.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame plus the eight other strip frames (−16, −12, −8, −4, +4, +8, +12, +16) as image inputs, and tell it which strip comes from which input.
Apply every style rule above, with the SAME strip geometry and time step on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where a strip came from the wrong moment, a pose was invented, strips were blended or the grid jumped — regenerate those frames only.
The final video must feel like TIME HAS BEEN CUT INTO STRIPS: sharp diagonal slices of nine different moments side by side, people breaking at every seam, a slowly sliding grid, 12 frames per second.
The image should deliberately contain:
* nine sharp diagonal strips
* a past-to-future staircase of moments, left to right
* thin white seams with soft shadows
* people and background jumping across the cuts
* the footage's own untouched colours.
Avoid blur and blending.
```
