# 22 — Glass Invisibility Cloak

**Look:** Each person turns into a living glass body: a clear, person-shaped lens. You see the room straight through them, bent and magnified by the curve of the body. A ghost of their face, glasses, hair and clothing pattern survives only as ripples in the refraction. A thin cold rim light and a faint chromatic fringe trace the silhouette, and a slow shimmer runs over the glass every frame. The cloak switches on with a sweeping energy band and glitches off for a moment mid-clip. Everything outside the bodies stays the untouched camera footage.

**Also called / where it trends:** "invisibility effect", "invisibility cloak effect", "Predator cloak effect", "glass body effect", "transparent person effect", "displacement map invisibility". The original viral TikTok effect is by @effects_collins. epicuts.studio recreated it in After Effects with a clean plate plus a Displacement Map, and the "can I recreate this viral effect" reel format spread it on Instagram Reels.

**References:**
- https://www.instagram.com/epicuts.studio/reel/Ddi0efGs9U-/ (screenshots: `refs/ref_1.png` post page with caption; `refs/ref_2.png` result frames, glass body visible from 0.4–1.0 s; `refs/ref_3.png` 12-frame contact sheet of the reel). "Can I recreate this VIRAL invisibility effect without any tutorials?" by **epicuts.studio**. The caption credits the original effect to **@effects_collins** (TikTok) and the footage to **@peterle876** (Pinterest). The method is a clean background plate, the person's own luma as a Displacement Map, and edge refraction. The creator shared no written prompt; this prompt is written from the visible result and the described After Effects method. Credit: epicuts.studio, @effects_collins.
- https://www.instagram.com/epicuts.studio/: creator page ("Making you a better video editor", about 162K followers).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with numpy + OpenCV:
- `plate.py` builds one clean background plate. It takes the masked median of the frames where each pixel is free of people, then fills the always-covered holes by row-wise interpolation.
- `render.py` refracts that plate through each person's mask. It uses a distance-transform glass-thickness dome for edge lensing, plus the person's own luminance gradient as the displacement map. It adds a per-channel chromatic split, a rim light only in the outer 7 px, sparkles from fine detail, a per-frame ripple and noise shimmer, a top-to-bottom cloak-on sweep over frames 1–26, and a decloak glitch around frames 104–110.

## Prompt

```text
I'm uploading one video clip. Convert it into a GLASS INVISIBILITY CLOAK frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
Seedream works here because every styled frame is built from two image inputs: the current source frame and ONE clean background plate made once at the start of Stage 3. No video model is needed.
CORE VISUAL STYLE
Every person in the shot becomes a transparent, living GLASS BODY:
* a clear person-shaped lens, not a white or frosted statue
* the room BEHIND the person visible straight through the body
* that room bent, magnified and pulled toward the edges by the curve of the body
* a ghost of the face, glasses, hair and clothing pattern surviving ONLY as ripples in the refraction
* a thin cold rim light along the silhouette, brightest on the side facing the main light
* a thin dark refraction line just inside the edge
* a faint chromatic fringe (red / cyan split) at strong bends
* tiny glints on fine detail: eyes, glasses rims, stripes, hair strands
* a slow liquid shimmer that moves across the glass every frame
* the ORIGINAL footage everywhere outside the bodies, untouched
The result should feel like someone:
SHOT THE SCENE
→ SHOT A CLEAN PLATE OF THE EMPTY ROOM
→ CUT EACH PERSON OUT
→ USED THE PERSON'S OWN LIGHT AND SHADOW AS A DISPLACEMENT MAP
→ REFRACTED THE EMPTY ROOM THROUGH THAT SHAPE
→ ADDED A CLOAK SWITCH-ON AND A GLITCH
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — PRESENT, BUT MADE OF GLASS
The person is still THERE, but invisible.
Their silhouette, pose, movement and timing must match the source exactly.
The viewer reads WHO it is from the outline, the hair shape, the glasses and the movement.
Inside the silhouette there is NO skin, NO clothing colour and NO solid face.
There is ONLY the refracted room plus the glass highlights.
Preserve, as refraction shapes, the person's exact:
* silhouette
* hairstyle outline
* glasses
* clothing folds and stripes (as ripple patterns)
* pose
* body proportions
* movement
* hand position
* interaction with objects
REFRACTION RULES
Behind each body, show the CLEAN PLATE (the room without people), never the person's own colours.
The bend is strongest at the silhouette edge, where the glass is thickest at an angle.
Toward the middle of the body the room shows through almost straight, only gently magnified.
The person's own light and dark detail (eyes, nose shadow, glasses, stripes, folds) adds small extra bends.
That detail is how the face and clothes stay faintly readable.
Straight lines in the room (window frames, wall edges, the TV, the planter) must visibly kink and curve where they pass behind a body.
That kink is what sells the effect. Make it obvious at phone size.
GLASS LIGHT
* Rim light: a THIN bright line only along the outer edge, cool white, a few pixels wide.
* Do NOT fill the body with white light, frost or milkiness.
* Chromatic fringe only where the bend is strongest.
* Glints: small, sparse, on fine detail only.
* Overall the glass absorbs a little light: inside the body the room is a touch darker and cooler than outside.
CLOAK SWITCH-ON (OPENING)
Over the first ~2 seconds, the cloak activates.
A horizontal energy band sweeps DOWN each body from head to feet.
Above the band: glass. Below the band: the normal photographic person.
The band itself is an electric cyan-white shimmer with a ragged, noisy edge.
DECLOAK GLITCH (ONE MOMENT MID-CLIP)
Pick one short moment in the middle of the clip (4–7 frames).
On those frames the cloak fails: the real person flickers partly back into view (20–60% visible).
Horizontal slices of the person slip sideways for a frame or two.
Then the glass comes back.
Plan this moment in the Stage 3 section list.
BACKGROUND RULES
Outside the bodies, the frame is the ORIGINAL footage.
No colour grade, no blur, no added effects.
Only a fine camera grain over the whole frame.
OBJECT CONTINUITY
If a person holds or touches an object (phone, cup, bag), the object stays solid and photographic.
It moves exactly with the hand.
Only the person turns to glass.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame from silhouette, hair, glasses and movement.
Never change:
* identity
* silhouette
* hairstyle
* glasses
* clothing shape
* accessories
* body proportions
* anatomy
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.
PERFECT MOTION TRACKING
The glass body must match the source silhouette exactly in position, pose and timing.
If the head moves:
the refraction moves with it.
If the hand moves:
the glass hand moves with it.
If the body turns:
the bends follow the new shape.
NO lagging glass.
NO previous-frame silhouette.
NO glass where the person is not.
FRAME-TO-FRAME BEHAVIOUR
THIS IS CRITICAL.
The glass is alive.
Allow between consecutive frames:
* the shimmer ripples to flow across the body
* glints to sparkle on and off
* the rim light to flicker very slightly
* the grain to change
Keep FIXED in every frame:
* the clean plate behind the glass (same room, same light)
* the strength of the refraction
* the rim light colour
DO NOT
Do NOT make the person a white, milky or frosted statue.
Do NOT show the person's skin or clothing colours inside the glass (except during the switch-on and the glitch).
Do NOT simply lower the person's opacity (no ghostly double exposure).
Do NOT blur the body into a smudge.
Do NOT use a rainbow or neon glow.
Do NOT add a thick outline.
Do NOT change the background outside the bodies.
Do NOT invent a different room behind the person.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT interpolate new in-between frames.
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
* NO clean plate
* NO refraction or glass
* NO cloak sweep or glitch
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
Do NOT begin the glass transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – GLASS CLOAK STYLING (AFTER MY CONFIRMATION ONLY)
1. CLEAN PLATE FIRST.
Generate ONE clean background plate with Seedream 5.0 Pro: the same room, same camera angle, same light, with every person removed.
Give Seedream several extracted frames where different parts of the room are visible as image inputs.
Show me the plate, then continue.
Use this SAME plate for every frame. Never regenerate it per frame.
2. Plan the sections and list them for me: the switch-on frames (the band's position per frame), the normal glass frames, and the decloak-glitch frames with their visibility per frame.
3. Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame (for the silhouette, pose and the person's light/dark detail) and the clean plate (for what shows through the glass).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where the silhouette, timing, refraction or the style rules broke — regenerate those frames only.
The final video must feel like the people are WEARING AN INVISIBILITY CLOAK: present, moving, readable by their outline, but made of clear living glass that bends the room behind them.
The image should deliberately contain:
* the room visibly bent through every body
* kinked straight lines behind the silhouettes
* a thin cold rim light
* a faint chromatic fringe
* sparse glints
* a living shimmer
* a switch-on sweep and one decloak glitch
* untouched footage outside the bodies.
Avoid a milky, frosted, half-transparent look.
```
