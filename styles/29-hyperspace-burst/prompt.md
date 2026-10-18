# 29 — Hyperspace Burst

**Look:** Every frame is pulled into light speed from a burst centre on the main subject's face. The room smears radially and blows out to white. The people repeat as stacked outward echo copies with inky stepped outlines and blue/green/red prism fringes, while the face at the centre stays sharp.

**Also called / where it trends:** "Hyperspace Burst" (Ashok Reddy S's label), "light speed effect", "warp speed transition", "radial burst", "zoom burst echo", "prism zoom". It trends in AI-restyle reels on Instagram (Figma Weave / invideo workflows) and as light-speed / warp transitions on YouTube and TikTok.

**References:**
- https://www.instagram.com/p/Deme5ygBN_5/ (screenshots `refs/ref_1.png`, `refs/ref_2.png` the look at about 9.6 s and 9.9 s; `refs/ref_3.png` post page with caption): Ashok Reddy S (@ashokreddyai), one clip run through a Figma Weave workflow into ten looks. This one is labelled **Hyperspace Burst**, at about 9.5–9.9 s: radial outward smear, white blown edges, prism fringes, stacked echo outlines. Credit: Ashok Reddy S.
- https://www.instagram.com/ashokreddyai/: creator page.
- https://www.youtube.com/watch?v=FVqwMvgNXpY: YouTube video on the hyperspace / light-speed jump effect (found via Exa search).
- https://www.youtube.com/watch?v=jy0OzfDELT0: YouTube video on the light-speed burst look (found via Exa search).
- https://limot.dev/effects/light-speed-burst/: "Light Speed Burst" effect page.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV). It finds the main person blob (area × centrality) and puts the burst centre at its head. It zoom-smears the background and screens it toward white. Seven per-channel zoomed echoes of the people are darken-stacked (prism split), then joined with a radial smear. The sharp lead person is kept near the centre, with an edge fringe and bloom on top.

## Prompt

```text
I'm uploading one video clip. Convert it into a HYPERSPACE BURST / LIGHT-SPEED STREAK frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame looks like it is being pulled into light speed:
* a burst centre on the main subject's face
* everything smeared RADIALLY outward from that centre
* the background blown out to bright WHITE
* the people repeated as discrete ECHO copies pushed outward
* the echoes stacked so hair and dark clothing leave inky stepped outlines
* PRISM fringes: each echo splits into blue, green and red edges
* the face at the burst centre stays sharp and readable
* parts of the body further out go translucent and streaky
* soft bloom on the brightest areas
The result should feel like someone:
PUT THE CAMERA ON THE SUBJECT'S FACE
→ HIT THE JUMP TO LIGHT SPEED
→ LET EVERY EDGE STRETCH OUTWARD INTO WHITE
→ STACKED THE ECHOES WITH A PRISM SPLIT
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, BURSTING
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
Do NOT turn them into a cartoon or 3D render.
BURST CENTRE
* Place the burst centre on the MAIN subject's face (the largest, most central person).
* The face at the centre stays sharp.
* The further a point is from the centre, the longer its streak.
* The centre follows the main subject's face exactly as it moves in the footage.
ECHO COPIES
* Repeat the people 5–8 times as copies pushed outward along the burst, each a little larger than the last.
* The far copies are paler, the near copies darker.
* Stack them so the DARKEST layer wins: dark hair, glasses and clothing leave clear stepped outlines.
* Between the copies, a soft radial smear joins them so they read as motion.
PRISM FRINGE
* The red, green and blue of each echo separate slightly along the burst direction.
* Fringes are thin coloured edges, strongest at the far echoes.
* The lead person at the centre has only a hairline fringe.
WHITE-OUT BACKGROUND
* The room smears radially and then blows out toward bright white.
* Near the edges of the frame it is almost pure white.
* Keep a trace of the room's shapes in the smear near the centre.
PALETTE
Keep the original colours of the people.
The background goes to warm white.
Colour fringes are the only added colours.
Do NOT add neon, blue space tints or star fields.
OBJECT CONTINUITY
If the character holds an object, it bursts with the hand and stays attached to it.
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
The lead person must match the source frame exactly.
The burst centre follows the main face.
Echoes come from the current pose only, pushed outward; they are NOT earlier frames.
NO echoes frozen from previous frames.
NO burst centre stuck in one place while the face moves.
FRAME-BY-FRAME PULSE
THIS IS CRITICAL.
Every frame is its own burst.
Allow between consecutive frames:
* burst strength (streak length) to pulse by about ±20%
* the centre to jitter a few pixels around the face
* bloom and white-out to breathe slightly
* fine noise to change
Keep FIXED:
* the burst always pointing outward from the main face
* the white-out background
* the prism order (blue outermost, red innermost)
DO NOT
Do NOT use a flat zoom blur over the whole frame.
Do NOT blur the face at the burst centre.
Do NOT add drawn speed lines, star fields or space backgrounds.
Do NOT add lens-flare graphics.
Do NOT darken the background.
Do NOT use the same echo layout on every frame.
Do NOT redraw or illustrate the people.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT freeze the burst between frames.
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
* NO radial smear or echoes
* NO white-out
* NO prism fringes
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
Do NOT begin the hyperspace burst transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – HYPERSPACE BURST STYLING (AFTER MY CONFIRMATION ONLY)
First, confirm for me which person is the main subject the burst centres on, and the burst strength range you will use.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the person at the centre is exactly that frame.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing or the style rules broke — regenerate those frames only.
The final video must feel like A JUMP TO LIGHT SPEED ON EVERY FRAME: the face sharp, everything else streaking outward into white with prism echoes, 12 frames per second.
The image should deliberately contain:
* a sharp face at the burst centre
* radial outward streaks
* stepped dark echo outlines
* prism colour fringes
* a white-out background
* soft bloom
* a frame-to-frame pulse.
Avoid polished digital perfection.
```
