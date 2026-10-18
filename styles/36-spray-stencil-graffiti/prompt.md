# 36 — Spray Stencil Graffiti

**Look:** every frame is a Banksy-style spray-paint stencil on a real street wall. The people are cut into a 3-layer stencil (white highlights, mid-grey, black shadows) and sprayed onto an old whitewashed brick wall with peeling paint, grime and torn paste-up posters. The paint has a soft overspray halo of speckle, a few drips run down from heavy black areas, and the layers sit slightly misregistered. The wall stays fixed. Like BLU's wall-painted animations, the faint ghosts of earlier frames stay on the wall, half buffed over with whitewash. A single red heart balloon (the only colour) and a stencilled "STAY STILL" tag finish the piece. Each frame is "re-sprayed": the speckle, the drips, the cut edges and the ghosts change.

**Also called / where it trends:** "Banksy style", "stencil graffiti", "street art stencil effect", "spray paint stencil animation", "graffiti wall animation", "stop-motion street art", "BLU style wall animation". Banksy-style stencil portraits are a lasting Pinterest / Etsy / TikTok trend. Stencil frame-by-frame animations are shared on Reddit and Instagram, and BLU's painted-wall animations ("MUTO", "BIG BANG BIG BOOM") are the classic reference for an animation that lives on a wall.

**References:**
- https://www.pinterest.com/search/pins/?q=banksy%20style%20stencil%20graffiti%20portrait%20wall (screenshot `refs/ref_1.png`): Banksy-style stencil portraits on brick and concrete. Note the 2–3 tone cut, the overspray, the drips and the single red accent.
- https://www.youtube.com/results?search_query=stencil+graffiti+stop+motion+animation+spray+paint (screenshot `refs/ref_2.png`): stop-motion street art, including BLU's wall-painted animations "MUTO" and "BIG BANG BIG BOOM", where each frame is painted over the ghost of the last.
- https://www.reddit.com/r/stencils/comments/1kkan58/stencil_frame_animation/: a stencil frame-by-frame animation, with one cut and sprayed stencil per frame.
- https://www.creativebloq.com/computer-arts/animate-stencil-graffiti-4079547: a tutorial on animating stencil graffiti.
- https://photoshoptrainingchannel.com/banksy-style-photoshop/: Banksy-style stencil in Photoshop: threshold layers, spray texture, drips, wall blend.
- https://www.tiktok.com/@artteacherkim/video/7566774273516326157: a TikTok of a multi-layer spray-paint stencil being cut and sprayed.
- https://gomedia.com/tutorials/animating-spray-paint-and-stencil-effect-in-after-effects/: animating a spray-paint and stencil effect in After Effects.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip, 12 fps, with audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + person masks):
- a fixed brick wall with whitewash, peeling paint, grime and torn paste-up posters
- a 3-layer stencil (white / grey / black) cut from CLAHE + bilateral tone thresholds with bridged, ragged edges
- an overspray speckle halo, drips and per-frame layer misregistration
- ghosts of frames n-5 and n-9 buffed over with whitewash
- a red heart balloon placed where it covers the least, and a "STAY STILL" stencil tag

## Prompt

```text
I'm uploading one video clip. Convert it into a SPRAY-PAINT STENCIL GRAFFITI frame-by-frame animation on a street wall, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into Banksy-style stencil street art, built from:
* a 3-LAYER STENCIL for every person: white highlights, mid-grey, black shadows
* sharp cut edges with small STENCIL BRIDGES that hold the islands (eyes, glasses, letters)
* matte aerosol paint with a soft OVERSPRAY halo of fine speckle around each layer
* a few paint DRIPS running down from heavy black areas
* slight MISREGISTRATION between the three layers
* an old WALL: whitewashed brick with peeling paint, grime, stains and torn paste-up posters
* the wall, its bricks and its posters FIXED in every frame
* faint GHOSTS of earlier frames still on the wall, half buffed over with whitewash
* ONE accent colour only: a red heart-shaped balloon
* one small stencilled tag in block capitals
* flat overcast daylight on the wall
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ SPLIT IT INTO THREE TONES
→ CUT THREE STENCILS FROM CARD WITH A KNIFE
→ TAPED THEM TO THE WALL
→ SPRAYED WHITE, THEN GREY, THEN BLACK
→ LIFTED THE STENCILS
→ PHOTOGRAPHED THE WALL
→ ROLLED A THIN WHITEWASH OVER IT
→ SPRAYED THE NEXT FRAME ON THE SAME WALL
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — STENCILLED, NOT REDRAWN
The MAIN HUMAN SUBJECT becomes a stencil, cut directly from the real frame.
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
Do NOT turn them into a cartoon or a mural character.
Do NOT exaggerate them into a caricature.
The likeness comes from the real photo, cut into three tones.
STENCIL LAYERS
* WHITE: highlights on the face, hands and light clothing
* GREY: mid-tones
* BLACK: shadows, hair, eyes, glasses, dark clothing and the outline
* each layer is one flat tone with crisp cut edges, never a gradient
* small bridges cross the cut where a real stencil would need them
* the face must read clearly: eyes, brows, nostrils, mouth and glasses as cut shapes
* the background of the room is NOT stencilled: only the people (and the objects they hold) are sprayed
SPRAY PAINT
* matte aerosol, never glossy
* a soft speckled overspray halo just outside every edge
* a little uneven density across large areas
* 2–6 drips per frame running down from heavy black areas
* layers shifted 1–3 px from each other
WALL
* old painted brick in pale whitewash, with mortar lines showing
* patches of peeled paint revealing brick and render
* grime, rain stains and dirt near the ground
* two or three torn paste-up posters with faded text blocks
* the wall never moves, warps or changes between frames
GHOSTS (WALL ANIMATION)
* faint, greyed ghosts of the pose a few frames back stay on the wall
* they are partly covered by a thin whitewash roller pass
* they are much lighter than the current frame
* the current frame is always clearly on top
ACCENT AND TAG
* one red heart-shaped balloon on a string, sprayed through its own stencil, in a quiet empty spot of the wall
* a small stencilled tag in block capitals ("STAY STILL"), low on the wall
* red is the ONLY colour; everything else is white, grey and black
* neither the balloon nor the tag covers a face or a hand
PALETTE RULES
* white
* mid-grey
* black
* the whitewashed wall and brick in muted, dirty tones
* ONE red accent
Do NOT add more colours to the stencil.
Do NOT use neon or bright graffiti colours.
LAYER ORDER
A typical frame reads:
BRICK WALL
↓
WHITEWASH + PEELING PAINT + GRIME
↓
TORN POSTERS
↓
BUFFED GHOSTS OF EARLIER FRAMES
↓
WHITE LAYER
↓
GREY LAYER
↓
BLACK LAYER + DRIPS
↓
RED BALLOON + TAG
↓
OVERSPRAY SPECKLE.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object and stencil it.
Examples:
* phone
* glasses
* chair
* bag
* microphone
* clothing accessory
If an object is essential to the action, cut it into the same three tones.
Do NOT let it dissolve into the wall.
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
The SPRAY boils.
The HUMAN MOTION does NOT.
The WALL does NOT move.
If the head moves:
the stencilled head moves with it.
If the hand moves:
the stencilled hand follows.
If the body turns:
the three layers follow.
If the character interacts with an object:
the object moves exactly with the original action.
Ghosts must come from REAL earlier frames, fainter than the current frame.
NO current-frame stencil lagging behind the body.
NO strong double images.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame must look like it was CUT AND SPRAYED AGAIN.
Allow:
* the cut edges to change slightly
* the bridges to sit in slightly different places
* the overspray speckle to change
* drips to appear, grow and change
* the layer misregistration to shift
* the buffed ghosts to change
This creates a gritty, hand-made street-art BOILING animation.
CONTROLLED BOIL
The boil must stay SMALL.
The wall, bricks and posters stay exactly the same.
The tone of each element (face, hair, each garment) stays in the SAME layer across frames.
The balloon and tag stay in the same place.
Do NOT let tones jump between layers across large areas.
Do NOT let drips cover faces.
DO NOT
Do NOT make it a photo threshold filter pasted on a wall: the paint must sit IN the wall texture with overspray and drips.
Do NOT make it a colourful graffiti piece, a mural or a comic.
Do NOT add more than one accent colour.
Do NOT stencil the room background.
Do NOT move or change the wall.
Do NOT let ghosts overpower the current frame.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT freeze the same spray across all frames.
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
* NO stencil layers
* NO wall
* NO spray texture
* NO ghosts
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
Do NOT begin the stencil transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – STENCIL STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the stencil sits exactly on the real pose.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe: the boil only works if every frame is sprayed separately.
Lock the look first: generate frame_01 and show it to me with the wall (bricks, peel, posters), the layer assignment of each element (face, hair, each garment), the balloon position and the tag text. Use that wall as the fixed background for every frame. For frames 2 onward, add the faint buffed ghost of the frame about half a second earlier.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, wall, layers or the style rules broke — regenerate those frames only.
The final video must feel like A STENCIL ON A STREET WALL THAT CAME ALIVE: real people, cut into three tones and sprayed on the same old wall, re-sprayed 12 times per second.
The image should deliberately contain:
* a 3-tone cut stencil with bridges
* overspray speckle and drips
* slight layer misregistration
* a fixed, weathered brick wall with posters
* faint buffed ghosts of earlier frames
* one red heart balloon and a stencil tag
* slight spray-to-spray irregularity.
Avoid polished digital perfection.
```
