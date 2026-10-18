# 04 — Y2K Digicam Flash

**Look:** every frame looks like a 2005 point-and-shoot snapshot taken with the built-in flash: the people are hit by harsh direct flash (blown, pale, shiny skin, flat light, bright clothes), a hard dark flash shadow falls just down-right of each person onto the wall, the room behind them drops into a dim, cool blue-green fluorescent cast with slow-shutter ghosting, and the whole picture is low-megapixel, noisy, over-sharpened, purple-fringed and JPEG-blocky, with an orange seven-segment date stamp ('05 10 18) burned into the bottom-right corner.

**Also called / where it trends:** "digicam aesthetic", "Y2K camera", "2000s digital camera look", "Coolpix / Cyber-shot / IXUS flash pics", "indie sleaze flash", "MySpace photo aesthetic", "digicam girlies" — TikTok #digicam / #y2kcamera (unboxings, "can 7 megapixels look this good?", digicam-filter apps), YouTube Shorts, Instagram accounts named *.JPG; covered by NPR (2024, 2026), The Verge, Ars Technica, Dazed, ABC.

**References:**
- https://www.youtube.com/results?search_query=digicam+flash+aesthetic+2000s+digital+camera+photos — screenshot `refs/ref_1.png`: "#y2kcamera #canon #ixus50", "2000s Digital Cameras", "VIBE KAMERA SONY Y2K" (6.2 M views), "Can 7 Megapixel look this good?"
- https://www.theverge.com/c/24208960/digicam-digital-camera-comeback-2004-gen-z-nikon-coolpix — screenshot `refs/ref_2.png`: The Verge "Crappy cameras are *so* back" — harsh flash of 2004, date stamp in the corner, grainy flatness
- https://www.npr.org/2026/07/18/nx-s1-5896117/retro-digital-camera-analog-reboot — "a bit grainy, sometimes fuzzy, overexposed in the center with a blinding flash, often date-stamped in red or orange"
- https://www.npr.org/2024/12/12/nx-s1-5209770-e1/gen-z-loves-the-digital-compact-cameras-that-millennials-once-coveted — Gen Z digicam trend, "really strong flash"
- https://arstechnica.com/gadgets/2024/11/vintage-digicams-arent-just-a-fad-theyre-an-artistic-statement/ — "flashes a-blazing… washed-out, low-resolution, grainy photos that look a whole lot like 2003"
- https://www.dazeddigital.com/fashion/article/59676/1/digital-cameras-trend-indie-sleaze-miu-miu-tiktok-bella-hadid-instagram-myspace — indie-sleaze / MySpace party flash, "sometimes the wrong white balance is the right one"
- https://www.abc.net.au/news/2025-06-18/why-digital-cameras-are-making-a-comeback/105414664 — "the flash of a digital camera is 100 percent brighter"
- https://www.tiktok.com/discover/digicam-aesthetic — TikTok "Digicam Aesthetic" (14.4 M-view #digitalcamera posts, digicam unboxings)

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation made with `render.py` (numpy + OpenCV: matte-driven flash falloff and hard shadow, cool ambient with ghosting, sensor noise, oversharpening, 4:2:0 JPEG, hand-built seven-segment date stamp); 6 frames in `frames/` (`render.py ... all` renders all 179).

## Prompt

```text
I'm uploading one video clip. Convert it into a Y2K POINT-AND-SHOOT DIGICAM FLASH animation, styled frame by frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform every frame into a mid-2000s compact digital camera snapshot built from:
* harsh DIRECT on-camera FLASH hitting the people
* blown, pale, slightly shiny skin and flat frontal light
* bright, clipped clothes and highlights
* a HARD DARK FLASH SHADOW just behind and down-right of each person
* a dim, underexposed room behind them
* a cool blue-green fluorescent white-balance cast in the background
* slow-shutter GHOSTING: faint trails of the room and of moving limbs
* small-sensor digital NOISE, worst in the dark areas
* over-sharpened edges with thin halos
* purple fringing on bright-against-dark edges
* low-megapixel softness and visible JPEG BLOCK compression
* a slight dark vignette from flash falloff
* an ORANGE seven-segment DATE STAMP in the bottom-right corner
The result should feel like someone:
GRABBED A 3-MEGAPIXEL CYBER-SHOT / COOLPIX / IXUS IN 2005
→ TURNED THE FLASH ON
→ SET THE DATE STAMP
→ SHOT THE SCENE IN BURST MODE, ONE FRAME AFTER ANOTHER
→ SAVED EVERY PHOTO AS A SMALL, HEAVILY COMPRESSED JPEG
→ UPLOADED THEM STRAIGHT TO MYSPACE.
CHARACTER — UNCHANGED PEOPLE, HIT BY FLASH
The people stay PHOTOGRAPHIC and exactly as in the source.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing and clothing patterns
* accessories (glasses, watches)
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw anyone.
Do NOT turn anyone into a cartoon or illustration.
Do NOT beautify, slim or retouch faces.
The flash only changes the LIGHT on the real person.
Faces must stay recognizable even when skin is blown out.
FLASH LIGHT
The flash sits just above the lens, pointing straight at the people:
* faces and skin go bright, pale and slightly overexposed, with shiny hot spots on forehead, nose, cheeks and glasses
* light is flat and frontal: almost no modelling shadows on the faces
* the person closest to the camera is the brightest; people further back get less flash
* a hand reaching toward the camera blows out almost to white
* white and light clothes clip to near-white; dark clothes keep their texture
* the flash falls off quickly: the room right behind the people catches a little light, the far room and the corners stay dim
HARD FLASH SHADOW
Behind each person, cast a sharp, dark, slightly offset shadow onto the wall / furniture behind them:
* offset a little down and to the right of the silhouette
* hard-edged, only slightly soft
* it follows the person's exact silhouette and moves with them every frame
This shadow is the signature of on-camera flash. Do NOT skip it.
Do NOT add a glowing outline or halo around the people.
BACKGROUND / AMBIENT
* the room is underexposed by about 1.5 stops
* colour cast: cool blue-green / cyan fluorescent, "wrong" white balance
* faint slow-shutter ghosting: the room and anything that moved show a soft double image
* keep every object of the original room in place
DIGITAL CAMERA ARTIFACTS
* low-resolution, slightly soft picture (about 1 megapixel worth of real detail)
* luminance and coloured chroma NOISE, stronger in the shadows
* in-camera OVERSHARPENING: thin bright/dark halos on edges
* PURPLE / magenta fringing where bright meets dark
* JPEG compression: 8×8 blocks in flat areas, mosquito noise around edges, smeared colour
* slight darkening toward the corners
It should NOT look like a clean modern smartphone photo with a filter.
It should NOT look like film: no film grain, no light leaks, no scratches.
DATE STAMP
Burn an orange LCD date stamp into the bottom-right corner of EVERY frame:
'05 10 18
* seven-segment digital digits, slightly italic
* bright orange (#FF9628), with a soft orange glow
* about 4–5% of the frame height tall
* same position, size and date in every frame
* it is part of the JPEG: it carries the same compression and softness
Do NOT add other text, logos, battery icons or REC markers.
SECTIONS
The look stays the same through the whole clip.
Flash strength may vary slightly between frames (±10%), like a real flash firing again and again.
FRAME-BY-FRAME BURST BOIL
THIS IS CRITICAL.
Every frame must feel like a separate snapshot.
Allow, every frame:
* sensor noise to change completely
* JPEG block pattern to change
* flash brightness to vary slightly
* ghosting to follow the latest movement
Do NOT freeze the noise.
Do NOT copy the same compression pattern between frames.
PERFECT MOTION TRACKING
The underlying character movement must remain exactly faithful to the source footage.
The CAMERA artifacts change.
The HUMAN MOTION does NOT.
If the head moves:
the flash highlights and the hard shadow follow exactly.
If the hand moves toward the camera:
it blows out brighter as it gets closer, exactly in the source position.
If the character interacts with an object:
the object moves exactly with the original action.
NO shadow lagging behind the person.
NO zoom, crop or reframing.
OBJECT CONTINUITY
Keep every object the people hold or touch (phone, chair, bag, cup, glasses).
Glasses should catch small flash reflections.
Do NOT remove or invent objects.
CHARACTER CONTINUITY LOCK
The SAME people must remain recognizable in every frame.
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
DO NOT
Do NOT make it clean, sharp, HDR or modern.
Do NOT use VHS artifacts (no tracking lines, no REC display) or film artifacts (no grain, burns, sprockets).
Do NOT add a camera-screen, viewfinder or polaroid frame around the picture.
Do NOT use warm golden-hour grading.
Do NOT use neon, glitter, sparkle or Y2K chrome graphics.
Do NOT add a halo or white outline around the people.
Do NOT add red-eye unless it already reads naturally.
Do NOT change the date stamp text.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace or beautify faces.
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
* NO flash relighting
* NO flash shadows
* NO noise or JPEG artifacts
* NO date stamp
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
Do NOT begin the digicam transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – DIGICAM FLASH STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Before generating, tell me the exact flash direction, shadow offset, background cast and date-stamp text you will use, and keep them identical for every frame.
If Seedream cannot keep the date stamp perfectly consistent, generate the flash-lit picture with Seedream and add the date stamp as a locked orange seven-segment text layer on top, then pass it through the same JPEG softness.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like a BURST OF REAL 2005 DIGICAM FLASH PHOTOS played as a video: harsh, bright, cheap, noisy, nostalgic.
The image should deliberately contain:
* blown, flat flash light on the people
* hard flash shadows behind them
* a dim, cool room with ghosting
* sensor noise that changes every frame
* oversharpening halos and purple fringing
* JPEG blocks
* the orange '05 10 18 date stamp.
Avoid modern smartphone perfection.
```
