# 37 — Claymation Plasticine

**Look:** every frame is a still from a stop-motion claymation film. The people and the room are re-sculpted in soft, matte plasticine. Each colour area is its own rounded clay piece, pressed against its neighbours, with soft creases at the seams, thumbprints, small lumps and modelling-tool marks. Skin is one smooth piece per face, and the eyes, brows, mouth and glasses are pressed-on darker pieces. A warm studio key light gives the clay a waxy sheen. Contact shadows sit under every piece, and the miniature set behind is softly out of focus. The film is shot on twos: each pose holds for two frames, then the clay is re-sculpted, so piece edges wobble and the thumbprints move.

**Also called / where it trends:** "claymation filter", "clay animation effect", "AI claymation video", "plasticine style", "stop-motion clay", "Aardman style", "Wallace & Gromit style", "clay face filter". AI claymation video filters are a 2025–2026 TikTok / Reels / Shorts trend (live claymation face filters, video-to-clay generators). The look comes from Aardman and Laika-style plasticine stop motion.

**References:**
- https://www.pinterest.com/search/pins/?q=claymation%20character%20stop%20motion%20plasticine%20face (screenshot `refs/ref_1.png`): plasticine faces and figures. Note the rounded pieces, thumbprints, matte waxy sheen and pressed-on features.
- https://www.youtube.com/results?search_query=claymation+filter+ai+video+stop+motion&sp=EgIYAQ%253D%253D (screenshot `refs/ref_2.png`): YouTube Shorts of AI claymation filters on real people (the viral trend this style copies).
- https://www.goenhance.ai/tools/ai-claymation-video-maker: an AI claymation video maker (video-to-clay restyle).
- https://morphic.com/resources/videos/claymation-videos: a guide to claymation AI videos with prompt examples (soft clay texture, fingerprints, stop-motion timing).
- https://www.hooked.so/tools/claymation-video-generator: a claymation video generator for short-form social video.
- https://www.facecam.ai/live-ai-filter/claymation: a live claymation AI filter for camera / streaming.
- https://www.media.io/ai/video-to-video/clay-animation: a video-to-video clay animation style.
- https://www.flixly.ai/dashboard/video-tools/claymation: a claymation video tool.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip, 12 fps, with audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + person masks):
- shot on twos (each odd frame's pose held for two frames)
- mean shift + bilateral flattening snapped to a 22-colour clay palette (k-means over the clip)
- every colour patch as its own clay piece, with a rounded height map from the distance to its edge, a body bulge, thumbprint dents, lumps and tool marks
- one unified skin piece per face, plus dark pressed-on feature pieces
- normals lit by a warm key, fill, waxy specular and ambient occlusion in the seams
- contact shadows, a defocused set and a vignette
- piece edges and thumbprints re-sculpted for every pose

## Prompt

```text
I'm uploading one video clip. Convert it into a stop-motion CLAYMATION PLASTICINE frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a real stop-motion clay film, built from:
* soft, matte PLASTICINE / modelling clay for the people, their clothes and the whole set
* every colour area as a separate, ROUNDED clay piece pressed against its neighbours
* soft creases and seams where pieces meet
* THUMBPRINTS, small dents, lumps and modelling-tool marks on every surface
* one smooth clay piece for each face, with eyes, brows, mouth and glasses pressed on as small darker pieces
* chunky hair made of a few rolled and pressed clay pieces, with tool-drawn strands
* clothing as clay sheets, with folds pressed in by hand and patterns as inlaid clay
* a warm STUDIO KEY LIGHT with a soft waxy sheen on the clay, plus a cool fill
* soft CONTACT SHADOWS under every piece
* a miniature SET with a shallow depth of field: the room softly out of focus
* STOP-MOTION timing: shot on twos
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ BUILT THE PEOPLE AND THE ROOM IN PLASTICINE
→ PRESSED ON THE FACES, HAIR AND CLOTHES BY HAND
→ LIT THE MINIATURE SET WITH STUDIO LIGHTS
→ PHOTOGRAPHED ONE FRAME
→ RE-SCULPTED THE POSE FOR THE NEXT FRAME
→ ANIMATED IT FRAME-BY-FRAME ON TWOS.
CHARACTER — SCULPTED, NOT REDRAWN
The MAIN HUMAN SUBJECT becomes a clay puppet, sculpted directly from the real frame.
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
Keep realistic body and head proportions from the footage.
Do NOT give them giant cartoon eyes or a toy-like head.
Do NOT make them a Pixar / 3D CG character.
The likeness comes from the real photo, re-made in clay.
CLAY PIECES
* each colour area is one piece with rounded, slightly bulging edges
* pieces overlap and press into each other with visible seams
* surfaces are matte with a soft waxy highlight, never glossy plastic
* thumbprints and fingerprint ridges on large pieces
* small lumps and flattened spots, as if worked by hand
* thin tool lines for hair strands, fabric folds and wrinkles
FACES
* one smooth skin piece per face (no patchy skin)
* eyes as small dark pressed pieces with a tiny highlight
* brows as rolled clay strips
* the mouth as a pressed shape that follows the real expression
* glasses as thin rolled clay frames
* the expression and gaze must match the footage exactly
SET AND LIGHT
* the room (walls, door, furniture, floor) is built in clay too, in simpler and larger pieces
* the set is softly out of focus, like a miniature shot with a macro lens
* warm key light from the upper left, cool fill, soft shadows
* ambient occlusion in every seam and under every piece
* a gentle vignette
PALETTE RULES
Use a limited plasticine palette taken from the footage:
* skin in 1–2 clay colours per person
* hair in 1–2 dark clay colours
* each garment in its own clay colour, keeping its pattern as inlaid clay
* the room in muted, slightly warm clay colours
About 20–25 colours in total, slightly saturated like real modelling clay.
Do NOT use neon or metallic colours.
LAYER ORDER
A typical frame reads:
CLAY SET (out of focus)
↓
CONTACT SHADOWS
↓
CLAY BODY + CLOTHING PIECES
↓
CLAY FACE + HAIR PIECES
↓
PRESSED-ON FEATURES
↓
THUMBPRINTS + TOOL MARKS
↓
STUDIO LIGHT + WAXY SHEEN + VIGNETTE.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object and sculpt it.
Examples:
* phone
* glasses
* chair
* bag
* microphone
* clothing accessory
If an object is essential to the action, sculpt it as its own clay piece.
Do NOT let it dissolve into the set.
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
The CLAY boils.
The HUMAN MOTION does NOT.
If the head moves:
the clay head moves with it.
If the hand moves:
the clay hand follows.
If the body turns:
the clay pieces follow.
If the character interacts with an object:
the object moves exactly with the original action.
The poses follow the footage on twos: one new pose every 2 frames.
NO clay lagging behind the body.
NO pieces from an older pose.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every new pose must look like the clay was RE-SCULPTED by hand.
Allow:
* piece edges to wobble slightly
* thumbprints and dents to move to new places
* lumps and tool marks to change
* seams to shift a little
* a tiny flicker in exposure between poses, like real stop motion
This creates the classic, tactile stop-motion BOILING look.
CONTROLLED BOIL
The boil must stay SMALL.
The clay colour of each element (skin, hair, each garment, wall) stays the SAME across frames.
Faces keep the same pressed-on features.
Do NOT let pieces change colour or swap places.
Do NOT let faces melt or deform.
DO NOT
Do NOT make it a smooth 3D CG render or a Pixar character.
Do NOT make it glossy plastic, vinyl or a toy figure.
Do NOT make it a soft "clay" blur filter: every surface must have rounded pieces, seams and thumbprints.
Do NOT use cartoon proportions or big eyes.
Do NOT leave the background as a sharp photo.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
Do NOT freeze the same sculpt across all poses.
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
* NO clay texture
* NO re-sculpting
* NO depth of field
* NO frame holding (keep every frame for now)
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
Do NOT begin the claymation transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – CLAYMATION STYLING (AFTER MY CONFIRMATION ONLY)
Style the extracted frames with Seedream 5.0 Pro, ON TWOS:
* style every ODD frame (frame_01, frame_03, frame_05 …) individually, one generation per frame
* use the original extracted frame as the image input for its own generation, so the clay sits exactly on the real pose
* place each styled odd frame in its own timeline slot AND in the next (even) slot, so every pose holds for 2 × 1/12 second
* if the frame count is odd, the last frame is styled on its own
Apply every style rule above.
Keep the frame count, order and 1/12-second slot duration exactly as verified in Stage 2: the timeline length does NOT change.
Do NOT merge, skip, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe: the boil only works if every pose is sculpted separately.
Lock the look first: generate frame_01 and show it to me with the clay colour of each element (skin, hair, each garment, wall, floor), the face features, the light direction and the depth of field. Keep those choices for every pose.
When every frame slot is filled, play the full timeline back once and report:
(a) styled pose count and timeline slot count
(b) timeline duration
(c) any pose where identity, pose, palette or the style rules broke — regenerate those poses only.
The final video must feel like A CLAYMATION FILM OF THE REAL FOOTAGE: real people re-sculpted in plasticine on a miniature set, re-sculpted 6 times per second on twos.
The image should deliberately contain:
* rounded plasticine pieces with seams
* thumbprints, lumps and tool marks
* pressed-on facial features
* a warm studio key with a waxy sheen
* contact shadows and a defocused miniature set
* stop-motion timing on twos
* slight pose-to-pose irregularity.
Avoid polished digital perfection.
```
