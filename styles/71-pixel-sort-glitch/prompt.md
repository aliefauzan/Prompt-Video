# 71 — Pixel Sort Glitch

**Look:** The frame melts downwards in clean vertical streaks. In every column, runs of pixels inside a brightness band are sorted by brightness, so the window, wall, plants, TV and wood cabinet turn into smooth light-to-dark gradient drips with hard, jagged ends. The cream stripes of the shirts drip into the beige. Near-black areas (hair, the TV frame, the chair, shadows) and the faces stay intact. The interval breaks are re-cut every frame, so the drips shimmer.

**Also called / where it trends:** "pixel sorting", "pixel sort", "ASDF pixel sort", "pixel sort glitch", "sorted pixels", "vertical bleed sort", "melting glitch" — glitch art since Kim Asendorf's 2010 Processing script (ASDFPixelSort, open-sourced 2012). On Instagram (#pixelsorting, about 673K reels), Pinterest and Behance glitch boards, and as an AI video preset on Morphic (horizontal streak, vertical bleed, threshold-band, radial and animated-sweep sorts). It is also an After Effects / TouchDesigner / Processing tutorial staple.

**References:**
- https://www.pinterest.com/search/pins/?q=pixel%20sorting%20glitch%20art (screenshot `refs/ref_1.png`, from the discovery sweep D2): portraits, buildings, mountains and fire melting into sorted vertical and horizontal streaks.
- https://github.com/kimasendorf/ASDFPixelSort (screenshot `refs/ref_2.png`): Kim Asendorf's original Processing script. A threshold decides which runs of pixels are sorted (white / black / brightness modes), and dark areas keep their structure.
- https://morphic.com/resources/videos/pixel-sort-effect-videos (screenshot `refs/ref_3.png`, from the discovery sweep D3): Morphic's AI pixel-sort video preset and its variations (horizontal streak, vertical bleed, threshold band, radial burst, animated sweep, fine thread).
- https://kimasendorf.com/mountain-tour/pixel-sorting-meeting-chaos-half-way/: Sarah Zucker's essay on pixel sorting: each line is sorted by luminosity, "no actual glitch", a deliberate generative process.
- https://www.instagram.com/popular/pixel-sorting/: Instagram tag page (Reels).
- https://www.behance.net/search/projects?search=glitch%20art%20motion and https://dribbble.com/search/pixel-sort-glitch: glitch motion projects.
- https://studio-ity.com/pixelsort/: free browser pixel-sort tool for images and video (threshold, direction, interval controls).
- https://vimeo.com/227273336: pixel-sort code / video demo.

How it differs from taken styles: **05 Datamosh** is codec damage: old pixels dragged by new motion vectors, macroblocks, colour blooms, RGB split. Pixel sort is a deterministic per-column brightness sort. It gives clean gradient bands, keeps the image readable and has no blocks, smears or ghosting from other frames. **70 Pixel Stretch** repeats one pixel line; pixel sort reorders the pixels already there.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). Each column is split into intervals of pixels inside a luminance band (wide in the room, only the brighter half on the people). Intervals break at the person edge and at random points that are re-drawn every frame. Inside each interval the pixels are sorted with the brightest at the top, using one vectorised argsort per frame. Faces are protected with solid ellipses from Apple Vision face boxes (`faces.json`, made by `faces.swift`), kept only inside the person mask.

## Prompt

```text
I'm uploading one video clip. Convert it into a PIXEL SORT GLITCH frame-by-frame animation: in every frame, bright and mid-tone areas melt down into clean vertical streaks of brightness-sorted pixels, while dark areas and the faces stay intact, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a pixel-sorted glitch frame built from:
* VERTICAL sorted-pixel streaks ("vertical bleed sort")
* runs of pixels sorted by BRIGHTNESS inside each column: brightest at the top of each run, darkest at the bottom
* smooth light-to-dark GRADIENT drips with HARD, jagged ends
* thin 1–3 px wide streak columns, each ending at a different height
* a brightness THRESHOLD: only pixels inside a mid-to-bright band are sorted
* near-black areas left INTACT: hair, the TV frame, the chair, deep shadows
* clothing that drips: cream stripes bleeding down into the beige, light fabric streaking
* FACES left completely intact
* the original colours of the footage, only rearranged, never recoloured
The result should feel like someone:
EXPORTED EVERY FRAME AS A STILL
→ RAN KIM ASENDORF'S PIXEL-SORT SCRIPT DOWN EVERY COLUMN
→ SET A BRIGHTNESS THRESHOLD SO THE DARKS SURVIVE
→ MASKED THE FACES BACK IN
→ RANDOMISED THE INTERVAL BREAKS EACH FRAME
→ PLAYED IT BACK AS A SHIMMERING GLITCH LOOP.
CHARACTER — READABLE, FACES INTACT
The people stay recognisable photographs where the sort does not reach.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing silhouette
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Faces (forehead to chin, ear to ear, including glasses) are NEVER sorted.
The outline of every person stays exactly where it is: sorting happens INSIDE a person or INSIDE the room, never across the person's edge.
Do NOT redraw the character.
Do NOT beautify or re-sculpt faces.
HOW THE SORT WORKS
* Work column by column, top to bottom.
* A pixel is "sortable" if its brightness is inside the band. In the room the band is wide (everything except near-black). On the people it is only the brighter half (cream stripes, light fabric, bright skin highlights on arms and hands).
* Consecutive sortable pixels form an interval. An interval also ends at the edge of a person and at a few random break points, so the streaks have different lengths (roughly 1/3 to 2/3 of the frame height at most).
* Inside each interval, reorder the pixels by brightness: brightest at the top, darkest at the bottom. Do not invent colours: every colour in the output is a pixel that was already in that interval.
* Non-sortable pixels stay exactly where they were.
* The white window and wall become pale gradient rain; the plants, wood cabinet and TV screen become coloured streaks; the striped shirt becomes vertical cream drips.
* Arms and hands may get thin sorted highlights inside their own outline, but their outline and position never change.
PALETTE
Only the footage's own colours: window white and pale blue, wall white, plant green and pink, wood tan, TV blue, skin, batik brown, beige and cream stripes, charcoal grey.
Slightly crisper contrast on the sorted streaks.
Do NOT add neon, RGB split, chromatic aberration or new colours.
BACKGROUND
* The whole room is sorted (except its near-black parts).
* Room streaks stop at the people's outlines; they never spill over a person.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand; it may be sorted inside its own outline like clothing.
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
The people must match the source frame exactly.
Each frame is sorted from its OWN source frame: the streaks always come from the pixels that are there in that frame.
NO streak pattern copied from a previous frame.
NO pixels dragged in from earlier frames.
FRAME-TO-FRAME GLITCH SHIMMER
THIS IS CRITICAL.
It must feel like a live pixel-sort video, not one sorted still.
Allow between consecutive frames:
* the random interval breaks to be re-drawn, so streak lengths and end points jump
* streak columns to flicker in length
Keep FIXED:
* the sort direction (vertical, brightest at top)
* the brightness threshold
* the intact faces
* the original colours
DO NOT
Do NOT make datamosh smears, macroblocks or frame blending.
Do NOT add RGB split, scanlines, VHS noise or chromatic aberration.
Do NOT sort the faces.
Do NOT sort across a person's outline.
Do NOT use soft blur or a "melting" warp instead of real sorted pixels.
Do NOT sort horizontally.
Do NOT invent colours that are not in the frame.
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
* NO pixel sorting
* NO threshold or face masks
* NO contrast change
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
Do NOT begin the pixel sort transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – PIXEL SORT STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the brightness band you will use for the room and for the people, the sort direction, and how you will keep faces out of the sort.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame and the streaks are made of that frame's own pixels.
Apply every style rule above, with the SAME direction and threshold on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, a face, pose, timing or the sort direction broke — regenerate those frames only.
The final video must feel like THE FOOTAGE IS MELTING INTO SORTED PIXELS: vertical gradient drips, intact faces and darks, shimmering interval breaks, 12 frames per second.
The image should deliberately contain:
* vertical brightness-sorted streaks with hard ends
* pale gradient rain where the window was
* cream drips in the striped shirt
* intact faces, hair and dark areas
* only the footage's own colours.
Avoid smooth motion blur.
```
