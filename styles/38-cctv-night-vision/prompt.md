# 38 — CCTV Night Vision

**Look:** the clip as recorded by a cheap ceiling-mounted security camera at night: infrared monochrome (IR night mode) with skin glowing pale and clothing dyes washed out, an IR-LED hotspot in the middle falling off to black corners, a fisheye barrel lens, soft D1 sensor resolution with interlace combing, grain, over-sharpening and heavy compression blocks. A green-phosphor night-vision section sits in the middle. On top is a DVR on-screen display: date/time stamp, CAM ID, blinking REC, location label and MOTION DETECTED. Motion-detect boxes track each person and head, and red grid cells light up where something moves. The footage stutters with dropped and duplicated frames and occasional macroblock tears.

**Also called / where it trends:** "CCTV effect", "security cam filter", "surveillance aesthetic", "night vision edit", "found footage cam", "doorbell cam trend". Seen in TikTok/CapCut CCTV templates, music videos (2025-26 surveillance-aesthetic wave of multi-cam grids, date stamps and REC dots), horror and found-footage edits, fashion campaigns and club visuals.

**References:**
- https://www.pinterest.com/search/pins/?q=cctv%20night%20vision%20security%20camera%20aesthetic (screenshot `refs/ref_1.png`): IR night-mode stills, green night vision, OSD stamps, fisheye corridors.
- https://www.epitrite.com/blog/surveillance-aesthetic-music-videos-2026: the surveillance aesthetic in 2026 music videos. Covers multi-cam grids, date stamps, REC, monospace OSD, cold green tint and compression.
- https://www.epitrite.com/blog/live-cams-template-guide: the "live cams" CCTV template trend.
- https://www.creativisionapp.com/tools/cctv-generator/night-vision-video-effect: a consumer night-vision CCTV video generator, showing what the effect looks like.
- https://elements.envato.com/realistic-security-cam-premiere-pro-M9UGQTB: a "Realistic Security Cam" Premiere template with OSD, fisheye, noise and frame drops.
- https://www.richardfarrar.com/how-to-create-a-cctv-effect-in-lightworks/: a CCTV effect tutorial covering desaturation, noise, timestamp and low frame rate.
- https://www.promonews.tv/videos/filter/cctv: music videos shot or styled as CCTV.
- https://github.com/mitsuki31/d31-nightvision: a night-vision shader with green phosphor, noise, vignette and scanlines.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (full clip). Local approximation rendered with `render.py` (numpy + OpenCV + PIL + person masks); the 6 sheet frames are in `frames/`. Distinct from 16 Thermal Camera (no false-colour heat map; this is IR luminance) and from 02 VHS (fixed security cam with DVR OSD, not a consumer tape).

## Prompt

```text
I'm uploading one video clip. Convert it into CCTV SECURITY CAMERA NIGHT-VISION footage, frame by frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage so it looks genuinely RECORDED BY A CHEAP CEILING-MOUNTED SECURITY CAMERA AT NIGHT, built from:
* infrared night-mode MONOCHROME (cool grey-white, no natural colour)
* skin glowing pale under the IR illuminator
* clothing dye patterns mostly washed out (IR sees fabric, not dye)
* plants reading bright white (foliage reflects infrared)
* an IR-LED hotspot in the centre falling off to dark corners
* a fisheye / barrel-distorted wide lens with strong vignette
* soft low-resolution D1 sensor (720x480 feel) upscaled
* interlace combing on moving edges
* heavy grain, over-sharpening halos and compression macroblocks
* auto-gain "breathing" brightness
* a DVR on-screen display (date, time, CAM ID, REC, location)
* motion-detect boxes and red motion-grid cells
* stuttering playback with dropped / duplicated frames
* one GREEN PHOSPHOR night-vision section in the middle of the clip
The result should feel like someone:
INSTALLED A CHEAP IR SECURITY CAMERA IN THE CORNER OF THE ROOM
→ LET IT RECORD THE NIGHT IN INFRARED
→ THE DVR STAMPED DATE, TIME AND CAMERA ID ON EVERY FRAME
→ MOTION DETECTION BOXED EVERYONE WHO MOVED
→ THE FOOTAGE WAS EXPORTED, COMPRESSED AND PULLED AS EVIDENCE
→ PLAYED BACK FRAME BY FRAME.
CHARACTER — UNDER INFRARED
The MAIN HUMAN SUBJECTS stay PHOTOGRAPHIC people seen through the security camera.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing silhouette
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the characters.
Do NOT turn them into silhouettes, ghosts or cartoons.
Under IR:
* skin → pale, slightly glowing, smooth
* eyes → can look slightly bright or reflective
* hair → mid to dark grey
* dark clothing → may turn lighter grey (many black fabrics reflect IR)
* stripes, prints and batik → mostly fade into flat grey with faint folds
* glasses → lenses may catch a small IR glint
Faces must stay recognisable: eyes, brows, nose, mouth and jaw readable.
THE ROOM — NIGHT, IR-LIT
The room keeps the exact same layout but is lit only by the camera's IR LEDs:
* centre of frame brightest (IR hotspot)
* walls and ceiling fall off to dark grey and near-black in the corners
* windows → dark or blown flat
* screens and monitors → black or faintly glowing
* plants → bright white leaves
* far background → murky, noisy, low detail
LENS AND SENSOR
* barrel / fisheye distortion: straight lines bow outward toward the edges
* strong corner vignette
* soft focus, low resolution, slightly smeared detail
* sharpening halos (white/dark outlines) on high-contrast edges
* visible grain that changes every frame
* blocky compression artefacts in dark and moving areas
* interlace combing (alternating-line tearing) on fast motion
It must NOT look like a clean black-and-white photo.
PALETTE RULES
PRIMARY — IR MONOCHROME:
near-black → cold grey → pale grey-white, with a very slight cool blue-grey cast.
SECONDARY — GREEN PHOSPHOR (one section, about 5 s in the middle):
black → dark green → bright phosphor green → pale green-white highlights, like a night-vision scope.
Mark the switch with one washed-out IR-cut frame (flat, overexposed) at each boundary.
Never mix monochrome and green inside one frame.
Do NOT keep natural colour anywhere, except the red OSD elements.
OSD (ON-SCREEN DISPLAY)
Overlay a DVR OSD in white monospace type with a thin black outline:
* top-left: date and running time "10-18-2026 SAT 02:14:31", with red "MOTION DETECTED" under it when people move
* top-right: "CAM 04" and "IR" / "NV ON" mode tag
* bottom-right: red REC dot (blinking) + "REC"
* bottom-left: location label "3F OFFICE - EAST"
* bottom-centre: amber "FRAME DROP" on dropped frames
The clock advances exactly with real time (1 second per 12 frames).
OSD text must be crisp, legible and in fixed positions.
MOTION DETECTION
* thin rectangular boxes around each person, labelled "PERSON" with a confidence number
* a smaller box around each head
* boxes follow the people tightly, jittering 1-3 px per frame
* red semi-transparent grid cells (coarse 16x9 grid) light up only where a person moved since the previous frames
* still areas stay unboxed
LAYER ORDER
A typical frame reads:
IR-LIT ROOM (dark corners, bright centre)
↓
PEOPLE UNDER INFRARED
↓
FISHEYE + VIGNETTE
↓
LOW-RES SENSOR + INTERLACE + GRAIN + SHARPENING + COMPRESSION
↓
RED MOTION-GRID CELLS
↓
MOTION BOXES + OSD.
OBJECT CONTINUITY
IMPORTANT:
If a character interacts with an object, keep that object in the IR image.
Examples:
* phone (screen may glow faintly)
* cup
* chair
* glasses (small IR glint)
* bag, headphones
If the object is essential to the action, keep it clearly visible.
Do NOT accidentally remove it.
CHARACTER CONTINUITY LOCK
The SAME people must remain recognisable in every frame.
Never change:
* identity
* facial structure
* hairstyle
* clothing silhouette
* accessories
* body proportions
* anatomy
* expression
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.
PERFECT MOTION TRACKING
The underlying human movement must stay exactly faithful to the source footage.
The CAMERA SIGNAL stutters.
The HUMAN MOTION does NOT change.
If the head moves:
the head box follows.
If a hand moves:
the motion cells light up there.
NO ghost people from previous frames (except a deliberately held dropped frame).
NO delayed boxes.
NO frozen clock.
FRAME-TO-FRAME SIGNAL LIFE
THIS IS CRITICAL.
Every frame should feel like a new live surveillance capture.
Allow:
* grain and compression blocks to change every frame
* auto-gain brightness to drift slightly
* REC dot to blink (about once per second)
* boxes to jitter 1-3 px
* about 1 in 10 frames to be a DROPPED frame: repeat the previous image exactly, with "FRAME DROP" shown and only the clock advancing
* about 1 in 20 frames to have a short horizontal macroblock tear across one band
Do NOT let faces flicker into different people.
Do NOT let the room layout shift.
DO NOT
Do NOT keep natural colours.
Do NOT make it a clean black-and-white grade.
Do NOT use a thermal / false-colour heat palette.
Do NOT add VHS tape wobble, tracking bars or chroma bleed.
Do NOT add sci-fi HUD graphics, crosshairs or target locks.
Do NOT add fake brand logos or garbled OSD text.
Do NOT replace any face.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing shape.
Do NOT make the image sharp and high resolution.
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
* NO infrared monochrome
* NO OSD overlay
* NO motion boxes
* NO grain or compression
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
Do NOT begin the CCTV / night-vision transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – CCTV NIGHT-VISION STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
The only allowed repeats are the deliberate DROPPED frames (about 1 in 10), and their OSD clock must still advance.
Lock the palette per section exactly as planned (IR MONOCHROME → washed IR-cut frame → GREEN PHOSPHOR → washed IR-cut frame → IR MONOCHROME).
Keep OSD layout, font and positions identical in every frame; only the clock, REC blink, MOTION / FRAME DROP tags, boxes and motion cells change.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like REAL NIGHT-TIME SECURITY FOOTAGE: IR-lit, fisheyed, stamped, boxed, compressed and stuttering.
The image should deliberately contain:
* low-resolution softness
* grain
* interlace combing
* compression blocks
* vignette and IR falloff
* dropped frames
* a crisp live OSD.
Avoid a polished cinematic look.
```
