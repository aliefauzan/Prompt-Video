# 27 — Signal Relief Scanlines

**Look:** The picture is rebuilt from dense vertical electric-blue scan lines on a navy ground. Each line is pushed sideways by the brightness under it, so the people rise out of the field as a ribbed 3D relief with a hard black extrusion. The background lines stay almost straight. This is the 1970s Rutt/Etra video-synthesizer look.

**Also called / where it trends:** "Signal Relief" (Ashok Reddy S's label), "Rutt-Etra effect", "scanline displacement", "luma displace lines", "video synthesizer", "line relief". It trends in AI-restyle reels on Instagram (Figma Weave / invideo workflows) and as a TouchDesigner / After Effects "Rutt Etra" effect on YouTube.

**References:**
- https://www.instagram.com/p/Deme5ygBN_5/ (screenshots `refs/ref_1.png`, `refs/ref_2.png` split view of the look; `refs/ref_3.png` post page with caption): Ashok Reddy S (@ashokreddyai). One clip run through a Figma Weave workflow into ten looks. This one is labelled **Signal Relief**, at about 1.7–2.2 s. Credit: Ashok Reddy S.
- https://www.instagram.com/ashokreddyai/: creator page (founder of @tastematters.ai).
- https://en.wikipedia.org/wiki/Rutt/Etra_Video_Synthesizer: the 1970s Rutt/Etra scan processor; brightness deflects the raster lines.
- https://www.videohistoryproject.org/ruttetra-notes-development: Rutt/Etra development notes (Experimental Television Center).
- https://www.vasulka.org/archive/Artists5/Rutt-E/VidSynthCont.pdf: original Rutt/Etra synthesizer documentation (Vasulka archive).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV). Lines are drawn implicitly: a pixel is on a line when its luma-displaced x-coordinate hits the line grid. It uses 8 px spacing, about 26 px of push on people and 3.5 px on the background, fatter lines in highlights, and a shifted black copy for extrusion. Phosphor glow, noise, tear rows and flicker come last.

## Prompt

```text
I'm uploading one video clip. Convert it into a SIGNAL RELIEF / RUTT-ETRA SCANLINE frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Rebuild every frame out of dense parallel scan lines, like a 1970s analog video synthesizer:
* hundreds of thin, evenly spaced VERTICAL lines
* lines glowing electric BLUE on a deep NAVY / near-black ground
* each line pushed SIDEWAYS by the brightness under it
* bright areas push the line further, dark areas leave it straight
* people rise out of the line field as a ribbed 3D relief
* a hard BLACK extruded shadow offset behind the displaced lines
* background lines almost straight, only slightly bent
* soft CRT glow and fine signal noise
* occasional horizontal tear rows (sync wobble)
The result should feel like someone:
FED THE VIDEO INTO A RUTT/ETRA SCAN PROCESSOR
→ TURNED THE PICTURE INTO RASTER LINES
→ LET BRIGHTNESS BEND EVERY LINE INTO RELIEF
→ FILMED THE GLOWING MONITOR
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — DRAWN ONLY BY THE LINES
There is NO photographic image left.
The person exists ONLY as the shape the bent lines make.
Preserve the person's exact:
* identity
* face shape
* expression
* hairstyle silhouette
* glasses
* clothing shapes and stripes
* pose
* body proportions
* movement
* hand position
* interaction with objects
Faces must stay readable: eyes, nose, mouth and jaw read from line density and bending.
LINE RULES
* Lines run VERTICALLY, top to bottom, across the whole frame.
* Keep a constant spacing of roughly 120–200 lines across the frame width.
* Lines bend sideways, they never break or cross each other.
* Highlights draw slightly THICKER and BRIGHTER lines.
* Shadows draw thinner, dimmer lines that fade into the navy ground.
* The bending is smooth and continuous along each line.
RELIEF DEPTH
* People displace strongly (about 2–3 line spacings at their brightest).
* The background displaces only a little (under half a line spacing).
* This difference lifts the people out of the field like an embossed sheet.
BLACK EXTRUSION
Behind the people's lines, draw a hard BLACK copy of the same displaced lines, offset a few pixels down-right.
It reads as the thickness of an extruded 3D surface.
Only the people get extrusion. The background stays flat.
PALETTE
Keep the palette strictly limited:
* deep NAVY / blue-black ground
* mid ELECTRIC BLUE lines for dark tones
* pale ICE-BLUE to near-white lines for highlights
* pure BLACK extrusion
Do NOT use skin tones, warm colours, rainbow or RGB split.
SIGNAL TEXTURE
* soft phosphor glow around bright lines
* fine analog noise in the ground
* 1–3 thin horizontal tear rows per frame where the lines jump sideways
* slight brightness flicker frame to frame
OBJECT CONTINUITY
If the character holds an object, it appears in the same relief lines and moves exactly with the hand.
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
The line relief must follow the source footage exactly.
If the head turns, the bulge of lines turns with it.
If the hand moves, the displaced lines move with it.
NO frozen relief.
NO relief copied from the previous frame.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame is a new scan.
Allow between consecutive frames:
* the line phase to shift slightly sideways
* signal noise in the bending to change
* tear rows to jump to new heights
* overall brightness to flicker slightly
Keep FIXED:
* line spacing
* line direction
* palette
* extrusion direction
DO NOT
Do NOT keep any photographic texture or colour.
Do NOT use horizontal lines.
Do NOT make a generic CRT scanline overlay on top of the photo.
Do NOT turn it into a wireframe mesh or grid.
Do NOT make it a thermal or heat-map look.
Do NOT add RGB chromatic split.
Do NOT let lines break, cross or tangle.
Do NOT lose the face: it must read from the lines.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing shapes.
Do NOT freeze the scan between frames.
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
* NO scan lines
* NO colour changes
* NO relief or extrusion
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
Do NOT begin the signal relief transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SIGNAL RELIEF STYLING (AFTER MY CONFIRMATION ONLY)
First, confirm the line count, line colours and extrusion offset you will use, and keep them for the whole clip.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the relief is shaped by that exact frame.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing or the style rules broke — regenerate those frames only.
The final video must feel like A LIVE VIDEO SYNTHESIZER SCAN: the people raised out of glowing blue lines, 12 frames per second.
The image should deliberately contain:
* dense vertical blue scan lines
* brightness-driven sideways bending
* a ribbed 3D relief of the people
* a hard black extrusion
* a navy ground
* phosphor glow
* signal noise and tear rows.
Avoid polished digital perfection.
```
