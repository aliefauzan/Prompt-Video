# 95 — Red-Cyan Anaglyph 3D

**Look:** The clip becomes an old-school red/cyan 3D picture, the kind you watch through paper glasses. Every edge splits into a red fringe on one side and a cyan fringe on the other. The split is scaled by depth: the people, nearest the lens, split widest, the person closest to the camera most of all; the back wall splits the other way, a little. Colours go slightly muted and filmic, so the red and cyan fringes carry the image.

**Also called / where it trends:** "anaglyph 3D", "red cyan 3D", "3D glasses effect", "红蓝3D" (Bilibili), "retro 3D", "stereo 3D edit". It is a Bilibili staple (红蓝3D 视频 特效: compilations, "put on your red-blue glasses" clips, Photoshop 1-minute tutorials). On Pinterest and Instagram it is a poster and portrait look, and an After Effects / CapCut tutorial topic. The gyng/ditherer gallery ships it as the "Retro 3D" preset.

**References:**
- Bilibili search 红蓝3D 视频 特效 (screenshot `refs/ref_1.png`, from the discovery sweep): https://www.bilibili.com/video/av10386725 (红蓝3D视频合集), https://www.bilibili.com/video/av884424989 (红蓝3D片段合集), https://www.bilibili.com/video/av43370835 (Photoshop 1-minute 红蓝3D 故障 tutorial), https://www.bilibili.com/video/av1613921 and https://www.bilibili.com/video/av1619846 (红蓝3D glasses demos), https://www.bilibili.com/video/av268159375 (3D红蓝眼镜 typography)
- https://www.pinterest.com/search/pins/?q=anaglyph%203d%20red%20cyan%20portrait (contact sheet of the first results, `refs/ref_2.png`): red/cyan portraits, posters and stereo photos. The split is widest on near features.
- https://www.pinterest.com/search/pins/?q=anaglyph%203d%20red%20cyan: Pinterest board noted in discovery D2.
- https://github.com/gyng/ditherer: browser image/video filter gallery with a "Retro 3D" anaglyph preset.
- https://www.youtube.com/watch?v=LMUI6U-ixoY: "Convert Normal Video Into Amazing 3D Anaglyph (Red-Cyan)".
- https://www.storyblocks.com/resources/tutorials/3d-glasses-anaglyph-effect: Storyblocks, "After Effects Tutorial: 3D Glasses Anaglyph Effect". The red channel is offset from green + blue, so with red/cyan glasses each eye sees its own view.
- http://www.terragon.de/video/tutorials/side-by-side-to-anaglyph-red/cyan/: converting a side-by-side stereo pair into red/cyan.
- https://www.cloudacm.com/?p=3075: building anaglyph video from a stereo pair with FFmpeg.

How it differs from taken styles: **30 Spider-Verse comic offset** misregisters CMYK print plates by a flat, uniform amount with halftone and ink lines. Here only the red channel splits from cyan, and the offset follows depth (people near, wall far, opposite signs), like a real stereo pair. **27 Signal Relief** is a scanline / emboss TV look with no depth. It also differs from the RGB-split glitch edits (05), which jitter at random.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). Each frame is split into two depth layers. The room has the people filled out of it with normalized convolution, and its disparity ramps from behind the screen at the top wall to nearer at the floor. The people layer gets a disparity from face size (Apple Vision face boxes from `../94-xray-skeleton-scan/pose.json`, median over ±3 frames), so the woman close to the lens splits widest, plus a little rounding from the matte's distance transform. Left and right views are rendered by shifting each layer and compositing people over the room. Red comes from the left view (mostly luma, so skin is not red-washed) and green + blue from the right view, then light contrast, a vignette and fine grain. It is a real stereo pair: with red/cyan glasses the people stand in front of the wall.

## Prompt

```text
I'm uploading one video clip. Convert it into a RED-CYAN ANAGLYPH 3D frame-by-frame animation: every frame should look like a stereo 3D picture made for red/cyan paper glasses, with the red/cyan split driven by depth, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Red-cyan anaglyph 3D photograph, stereoscopic image for red/cyan glasses, depth-scaled red and cyan fringing, slightly muted film colour.
Transform the footage into an anaglyph built from:
* TWO VIEWS of the same moment, a LEFT-EYE view and a RIGHT-EYE view, a few centimetres apart
* the RED channel taken from the LEFT view
* the GREEN + BLUE (CYAN) channels taken from the RIGHT view
* every edge split into a RED fringe on one side and a CYAN fringe on the other
* the split WIDTH set by DEPTH: near things split wide, far things split narrow
* the PEOPLE nearest the camera with the widest split
* the BACK WALL / window split slightly in the OPPOSITE direction (it sits behind the screen)
* objects at middle depth almost aligned (the screen plane)
* slightly muted, filmic colour so the red and cyan read clearly
* light contrast, a soft vignette and fine grain
The result should feel like someone:
SHOT THE SCENE WITH A TWO-LENS STEREO CAMERA
→ PRINTED THE LEFT EYE IN RED
→ PRINTED THE RIGHT EYE IN CYAN
→ LAID ONE OVER THE OTHER
→ HANDED OUT PAPER 3D GLASSES
→ PLAYED IT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, IN STEREO
The people stay PHOTOGRAPHIC.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT turn them into a painting, cartoon or 3D render.
Do NOT beautify or re-sculpt faces.
DEPTH RULES (WHAT MAKES IT ANAGLYPH, NOT GLITCH)
* Work out the depth order of the scene first: hands reaching toward the lens and faces close to the camera are nearest, then the people, then the planter and cabinets, then the back wall and window.
* The red/cyan offset is horizontal only. Never vertical.
* The offset grows smoothly with nearness: a face close to the lens may split by about 2–3% of the frame width; people standing back by about 1–1.5%; the back wall by about 0.5% the other way.
* Within one person the offset is nearly the same everywhere, slightly more on the nose and chest than on the outline (bodies are round, not flat cut-outs).
* Behind each person's edge, the background they uncover in each eye is real background, not a smear and not a duplicate of the person.
* The red side and the cyan side swap between foreground and background (because the wall sits behind the screen plane).
COLOUR
* Left view feeds red; use mostly its brightness (luma), so skin does not turn red.
* Right view feeds green and blue unchanged.
* Overall colour is slightly muted and filmic, never neon.
* Where the two views agree (the screen plane), colours look nearly normal.
* Fringes are pure red and pure cyan.
PALETTE
Muted natural colour, plus pure red (#FF2020-ish) and cyan (#00E5FF-ish) fringes.
Do NOT add magenta, yellow, green or blue fringes; only red and cyan.
OBJECT CONTINUITY
If the character holds an object, it splits with the hand at the same depth.
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
The depth split follows each person as they move: when someone steps toward the lens their split widens smoothly; when they step back it narrows.
NO frozen offset from a previous frame.
NO split that jumps in width between consecutive frames.
FRAME-TO-FRAME STEREO LIFE
THIS IS CRITICAL.
It must feel like real 3D footage, not a random glitch.
Allow between consecutive frames:
* grain to change every frame
* the split to change ONLY when depth really changes
Keep FIXED:
* the red-left / cyan-right channel order
* the screen plane (what sits at zero offset)
* the colour grade
DO NOT
Do NOT use a flat, uniform RGB offset over the whole frame (that is a glitch / Spider-Verse look).
Do NOT jitter or flicker the offset randomly.
Do NOT add CMYK halftone dots, comic ink lines or print misregistration.
Do NOT add scanlines, VHS noise or datamosh blocks.
Do NOT offset vertically.
Do NOT turn the whole frame red or cyan.
Do NOT show 3D glasses in the picture.
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
* NO colour change
* NO channel split or stereo views
* NO grain or vignette
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
Do NOT begin the anaglyph transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – RED-CYAN ANAGLYPH STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the depth order you found (nearest to farthest), which object you will put on the screen plane, and the largest and smallest offsets you will use.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people and the room are exactly that frame.
Apply every style rule above, with the SAME channel order, screen plane and grade on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the depth split or the channel order broke — regenerate those frames only.
The final video must feel like A RED-CYAN 3D MOVIE: put on paper glasses and the people stand out in front of the wall, 12 frames per second.
The image should deliberately contain:
* red fringes on one side and cyan fringes on the other side of every edge
* the widest split on the nearest person
* a small opposite split on the back wall
* muted filmic colour, light grain and a soft vignette.
Avoid a flat RGB-split glitch.
```
