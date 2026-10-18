# 34 — Cross-Stitch Embroidery

**Look:** every frame is a hand-stitched cross-stitch picture on cream aida cloth. The image is charted onto a fixed stitch grid, and each square is one X made of two crossing strands of cotton thread, in a limited palette of thread colours. The threads have a soft sheen and a visible twist. A dark backstitch outlines each person. The top of the room is left unfinished, so the heads come out of bare cloth with half-stitches at the edge. The cloth sits in a wooden embroidery hoop, with a needle, a trailing thread and loose thread ends. Each frame is "re-sewn": the grid stays still, but the stitches, the colour dither at colour edges and the loose threads change.

**Also called / where it trends:** "cross stitch effect", "cross-stitch video effect", "embroidery AI video", "AI embroidery filter", "stitched portrait", "hand-embroidered portrait in a hoop", "pixel embroidery". Embroidery AI videos (a portrait that becomes embroidery in a hoop) are a 2026 Reels / YouTube Shorts / TikTok / Pinterest trend. Custom cross-stitch portraits in hoops are a large Pinterest and Etsy niche. There are browser tools that turn a whole clip into moving cross-stitch.

**References:**
- https://www.pinterest.com/search/pins/?q=cross%20stitch%20portrait%20embroidery%20hoop (screenshot `refs/ref_1.png`): photo-realistic cross-stitch portraits in wooden hoops. Note the visible X grid, the bare aida margin and the hoop clamp.
- https://www.pinterest.com/search/pins/?q=cross%20stitch%20close%20up%20aida%20texture%20pixel%20portrait (screenshot `refs/ref_2.png`): close-ups of stitched faces and "unfinished" portraits, where the stitching stops and bare aida shows. This is the source of the unfinished top band.
- https://vayce.app/tools/cross-stitch-video-effect/: a cross-stitch video effect. The frame is a fixed grid of stitches on aida, each cell is snapped to a limited thread palette and drawn as two crossing diagonal threads, and the grid stays still while the colours move.
- https://rohaneditz.com/how-to-create-viral-embroidery-ai-videos/: a guide (2026-08) to the viral "embroidery AI video" trend on Reels / Shorts / TikTok, with a Google Flow prompt (hoop, needle, thread tension, fabric texture, soft studio light).
- https://patternful.ai/ai-embroidery-filter: an AI embroidery filter (stitched needlework look).
- https://www.embroidai.com/create-social-stitch-video: embroidery stitch-out videos for social media.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip, 12 fps, with audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + person masks):
- a fixed 15 px aida grid (108 × 72 stitches) with a 30-colour thread palette from k-means over the clip
- every stitch drawn as two tapered, shaded, twisted threads, with eight variants re-picked every frame
- a Lab dither that re-sews the stitches at colour edges
- a backstitch outline on the person mask
- an unfinished top band with half-stitches
- a wooden hoop, a needle with trailing thread, and loose ends in the bare cloth

## Prompt

```text
I'm uploading one video clip. Convert it into a hand-stitched CROSS-STITCH EMBROIDERY frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a real piece of counted cross-stitch, built from:
* cream / ecru AIDA cloth with a visible square weave and holes at every grid corner
* one X-shaped cross-stitch per grid square: two crossing strands of cotton thread
* a FIXED stitch grid (about 100–110 stitches across the frame)
* a LIMITED palette of stranded-cotton colours (about 25–35 colours)
* soft thread sheen: each strand rounded and lighter along its ridge
* visible 2-ply twist in every strand
* threads tapering where they dive into the holes
* small gaps where the cream cloth peeks between stitches
* a dark BACKSTITCH outline around each person
* an UNFINISHED area of bare aida, with half-stitches at its edge
* a wooden embroidery HOOP holding the cloth
* a needle, a trailing thread and a few loose thread ends
* soft raking daylight across the fabric
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ CHARTED IT ONTO A STITCH GRID
→ PICKED A THREAD COLOUR FOR EVERY SQUARE
→ STRETCHED AIDA CLOTH IN A WOODEN HOOP
→ STITCHED EVERY SQUARE AS AN X BY HAND
→ BACKSTITCHED THE OUTLINES
→ PHOTOGRAPHED THE HOOP FROM ABOVE
→ RE-STITCHED IT FOR THE NEXT FRAME
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — STITCHED, NOT REDRAWN
The MAIN HUMAN SUBJECT becomes cross-stitch, charted directly from the real frame.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing and clothing pattern (stripes, prints, batik)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT turn them into a cartoon or a chibi figure.
Do NOT simplify them into a cute pattern character.
The likeness comes from the real photo, square by square, like a photo-realistic cross-stitch portrait.
STITCH GRID
* every stitch sits on the SAME grid in every frame: the cloth does not move
* one stitch per square, one colour per stitch
* the bottom strand runs "/" and the top strand "\" in every stitch, as a real stitcher works
* stitches nearly fill their square, with only small gaps of cloth showing
* the grid must be fine enough that faces stay recognizable (eyes, brows, mouth and glasses readable)
Do NOT use round dots, pixels, beads or knitting.
Do NOT use satin stitch or free embroidery for the figures.
THREAD
* cotton thread, matte with a soft sheen, never plastic or metallic
* each strand slightly rounded and shaded, with visible twist
* small irregularities: one strand a little thicker, a stitch slightly tilted
* the colour of a strand stays even along its length
BACKSTITCH OUTLINE
* a dark brown / near-black backstitch runs along the outline of each person
* it follows the grid lines, one short straight stitch per square side
* it is slightly uneven, as if sewn by hand
UNFINISHED AREA
* part of the room (for example the top band of the wall) is still bare aida cloth
* stitching stops in a ragged edge, with some half-stitches (only "/") at the border
* the people are always fully stitched: their heads come out of the bare cloth
* loose thread ends and the parked needle sit in the bare cloth, never over a face
HOOP AND SET
* a light wooden embroidery hoop holds the cloth; its ring shows at the sides and corners of the frame
* outside the hoop: a little gathered cloth and a wooden table
* the cloth dips and darkens slightly near the ring
* soft daylight from the upper left, gentle falloff to the lower right
PALETTE RULES
Use a limited stranded-cotton palette taken from the footage:
* skin tones in 3–5 thread colours
* hair in 2–3 dark browns / near-black
* each garment in 2–4 thread colours, keeping its pattern
* the room in soft, slightly simplified thread colours
Saturate slightly, like real cotton floss.
Do NOT use gradients inside one stitch.
Do NOT use neon or metallic thread.
LAYER ORDER
A typical frame reads:
WOODEN TABLE
↓
AIDA CLOTH IN THE HOOP
↓
CROSS-STITCHES (bottom strand, then top strand)
↓
BACKSTITCH OUTLINES
↓
LOOSE THREADS + NEEDLE
↓
HOOP RING + SOFT DAYLIGHT.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object and stitch it.
Examples:
* phone
* glasses
* chair
* bag
* microphone
* clothing accessory
If an object is essential to the action, chart it in its own thread colours.
Do NOT let it dissolve into the background.
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
The STITCHES boil.
The HUMAN MOTION does NOT.
The CLOTH and GRID do NOT move.
If the head moves:
the stitched head moves across the grid with it.
If the hand moves:
the stitched hand follows.
If the body turns:
the stitches and backstitch outline follow.
If the character interacts with an object:
the object moves exactly with the original action.
NO stitches lagging behind the body.
NO stitches from the previous frame.
NO grid that slides, warps or rescales.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame must look like the picture was RE-STITCHED.
Allow:
* each strand to sit slightly differently in its square
* thread sheen and twist to change
* the colour of stitches at colour borders to flip between neighbouring threads
* half-stitches at the unfinished edge to come and go
* loose thread ends to shift and curl differently
* the needle and its thread to move every couple of seconds
This creates a gentle, tactile BOILING embroidery animation.
CONTROLLED BOIL
The boil must stay SMALL.
The grid never moves.
The colour of each element (skin, hair, shirt, wall) stays the SAME thread colour across frames.
Faces keep the same stitches for the eyes, brows and mouth.
Do NOT let colours flicker across large areas.
Do NOT let the unfinished area jump around.
DO NOT
Do NOT make it a pixel-art or mosaic filter: every square must be a real thread X with cloth showing.
Do NOT use a clean digital grid of flat squares.
Do NOT use beads, sequins, knitting, crochet or felt.
Do NOT make the threads glossy plastic or metallic.
Do NOT turn the people into cartoon pattern figures.
Do NOT put the needle or loose threads over faces.
Do NOT let the hoop crop faces.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT freeze the same stitches across all frames.
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
* NO stitch grid
* NO thread texture
* NO hoop
* NO colour reduction
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
Do NOT begin the cross-stitch transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – CROSS-STITCH STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the stitches sit exactly on the real pose.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe: the boil only works if every frame is stitched separately.
Lock the look first: generate frame_01 and show it to me with the grid size (stitches across), the thread colour of each element (skin, hair, each garment, wall), the backstitch colour, the unfinished area and the hoop position. Keep those choices for every frame.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, grid, palette or the style rules broke — regenerate those frames only.
The final video must feel like A CROSS-STITCH PICTURE THAT CAME ALIVE: real people, charted and sewn in cotton thread on aida cloth, re-stitched 12 times per second.
The image should deliberately contain:
* visible X stitches on a fixed grid
* cream aida with holes between the stitches
* thread sheen and twist
* a hand-sewn backstitch outline
* an unfinished area with half-stitches
* a wooden hoop, a needle and loose threads
* slight stitch-to-stitch irregularity.
Avoid polished digital perfection.
```
