# 23 — Boogley Doodle Creatures

**Look:** The footage stays a real, lightly graded phone video, but a small cast of flat 2D cartoon creatures lives in it. They are chunky bean-shaped blobs in saturated orange, yellow, cyan, pink and green. They have thick dark outlines, one cel-shade crescent, googly eyes and stubby limbs. A white hand-drawn doodle sticker character (black wobbly ink on grid paper) joins them. The creatures peek in from the frame edge, ride on shoulders and heads, cling to the TV, patrol the planter and hide behind the people. The people correctly pass in front of them. Their outlines boil on twos like hand-drawn animation.

**Also called / where it trends:** "Boogley characters trend", "cartoon characters in real life", "googly-eye creatures", "2D characters in real footage", "doodle overlay trend", "mixed reality cartoon edit". The characters are by @theboogley. epicuts.studio's reel sold them as a "huge Boogley characters pack" for After Effects ("Comment TREND"), and the trend runs on Instagram Reels and TikTok edits that composite cartoon creatures into everyday footage.

**References:**
- https://www.instagram.com/epicuts.studio/reel/Dd_eKlMsGKz/ (screenshots: `refs/ref_1.png` post page with the orange Boogley creatures in the shot; `refs/ref_2.png` 12-frame contact sheet of the reel). "Comment TREND to get access to the huge Boogley characters pack" by **epicuts.studio**, with characters by **@theboogley**. The pack and its tutorial are gated behind a comment, so there was no public prompt. This prompt is written from the visible result. The cast here is an ORIGINAL set in the same spirit, not a copy of the Boogley characters. Credit: epicuts.studio, @theboogley.
- https://www.instagram.com/epicuts.studio/: creator page.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output. `render.py` (numpy + OpenCV) grades the footage a little warmer and richer. It draws the creatures procedurally: wobbly bean outlines re-seeded every 2 frames, a darker rim, a cel crescent and highlight, googly eyes that blink, plus arms, legs and a hop/squash. The cast sits in front of or behind the people according to the person masks:
- a cyan antenna blob on the TV
- a yellow pup on the planter
- an orange creature that peeks in from the left, climbs onto a shoulder, then rides a head or hides in the gap between people
- a pink one, a green one and a doodle frog sticker in the corners

## Prompt

```text
I'm uploading one video clip. Convert it into a REAL FOOTAGE + LIVING 2D DOODLE CREATURES frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The people and the room stay real. Only the added cartoon cast and a light grade are new.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
Seedream works here because every styled frame is the current source frame plus ONE fixed character sheet given as image inputs; no video model is needed.
CORE VISUAL STYLE
Real footage, with a small cast of FLAT 2D CARTOON CREATURES living in it:
* chunky bean / blob / gumdrop bodies
* saturated flat fills: ORANGE, YELLOW, CYAN, HOT PINK, LIME GREEN
* thick dark outlines (deep brown or near-black), slightly wobbly, hand-drawn
* ONE simple cel-shade crescent on the shadow side and ONE small highlight
* big GOOGLY EYES (white with a black pupil), each looking somewhere specific
* tiny mouths, stubby arms and legs, optional antenna
* ONE white doodle sticker character: black wobbly ink on white or grid paper, with a thin white sticker border
* the people and room kept PHOTOGRAPHIC, with a light social-media grade (a little warmer, a little more saturated)
The result should feel like someone:
FILMED A NORMAL PHONE CLIP
→ DREW A FEW CARTOON CREATURES ON PAPER
→ ANIMATED THEM ON TWOS
→ HID THEM BEHIND THE PEOPLE AND THE FURNITURE
→ LET THEM CLIMB ON SHOULDERS AND HEADS
→ COMPOSITED EVERYTHING FRAME-BY-FRAME.
THE PEOPLE — UNCHANGED
The people are NOT stylized.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* clothing
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the people.
Do NOT cartoonize the people or the room.
THE CAST
Design 4–6 ORIGINAL creatures plus 1 doodle sticker character, in the style of the references.
Each creature has a FIXED design: one body colour, shape, eye size, limb style and antenna (or none).
Sizes vary: some are as big as a head, some are as small as a hand.
The doodle sticker character is drawn with black ink on white grid paper, with its own white sticker border.
Do NOT copy any existing trademarked character exactly.
STAGING — THE CREATURES LIVE IN THE SCENE
Each creature has a job and a place, planned per section:
* one PEEKS in from a frame edge, then climbs onto a person's shoulder
* one RIDES on top of someone's head, bouncing with their steps
* one CLINGS to a background object (a TV, a shelf, a lamp)
* one PATROLS along furniture (a planter, a desk, a sofa back) and walks behind the people
* the sticker character STANDS in a corner, slightly tilted, as if stuck on the lens
A creature sitting on a person follows that person's exact movement: head, shoulder, lean.
DEPTH AND OCCLUSION
THIS IS CRITICAL.
Creatures BEHIND a person are hidden by that person, edge-accurately.
When a person walks past a creature, the person covers it.
Creatures IN FRONT (on a shoulder, peeking from the edge, the sticker) sit over the person.
Every creature sits ON a surface: feet on the planter, hands on the TV edge, bottom on the shoulder.
Add a small soft contact shadow where it touches something.
No creature floats in mid-air unless it is jumping.
CREATURE ANIMATION
Creatures move with simple cartoon timing:
* hops with squash on landing and stretch in the air
* waving arms
* looking at the people or at the camera
* a blink now and then
* peeking out from behind someone, then hiding again
Animate ON TWOS: each creature pose holds for 2 frames.
LINE AND FILL RULES
Outlines: thick, dark, slightly uneven, hand-drawn.
Fills: flat, saturated, no gradients, no 3D rendering, no fur, no glossy plastic.
One cel shadow shape, one highlight, nothing more.
The doodle character: black ink lines only, on paper, with visible grid lines.
GRADE AND BACKGROUND RULES
Keep the original footage, room and camera motion.
Apply only a light grade: slightly warmer, slightly more saturated, a touch more contrast.
Do NOT blur, paint or redraw the background.
OBJECT CONTINUITY
If a person holds an object, the object stays photographic and moves exactly with the hand.
A creature may react to it (look at it, hop toward it) but never changes it.
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
The SAME creatures must remain the same designs in every frame: colour, shape, eyes, limbs.
Generation is for adding the cast and the light grade ONLY.
PERFECT MOTION TRACKING
A creature on a head or shoulder moves with that head or shoulder exactly.
A creature behind a person is hidden by the person's current silhouette, not an old one.
NO sliding creatures.
NO creatures drifting off their surface.
NO creature crossing in front of a person it is supposed to be behind.
FRAME-TO-FRAME BEHAVIOUR
THIS IS CRITICAL.
The creatures BOIL like hand-drawn animation.
Allow between consecutive pose changes:
* the outline to wobble slightly
* line thickness to vary slightly
* the cel-shadow edge to shift a little
Keep FIXED in every frame:
* each creature's design and colours
* the people and the room
* the grade
DO NOT
Do NOT stylize, cartoonize or repaint the people or the room.
Do NOT render the creatures in 3D, with fur, gloss or realistic lighting.
Do NOT use gradients inside the creatures.
Do NOT let creatures float or slide.
Do NOT let a creature cover a face for long.
Do NOT change a creature's design between frames.
Do NOT add more creatures than planned.
Do NOT add text, logos or UI.
Do NOT create new poses for the people.
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
* NO grade
* NO creatures or stickers
* NO character sheet
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
Do NOT begin adding creatures.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – CREATURE CAST + COMPOSITING (AFTER MY CONFIRMATION ONLY)
1. CHARACTER SHEET FIRST.
Generate ONE character sheet with Seedream 5.0 Pro showing every creature and the doodle sticker character: front view, a few poses each, their colours labelled.
Show it to me and WAIT for my OK before styling frames.
Use this SAME sheet as an image input for every frame. Never redesign the cast.
2. Plan the sections and list them for me: frame range, where each creature is, what it is doing, and whether it is in front of or behind each person.
3. Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame plus the character sheet.
Keep each creature pose for 2 frames (animation on twos), but still generate every frame so the line boil and the people's motion stay exact.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where a creature floats, slides, changes design, or breaks occlusion, or where a person changed — regenerate those frames only.
The final video must feel like the cartoon creatures REALLY LIVE IN THIS ROOM: hiding behind people, riding on them, peeking at the camera, drawn by hand and boiling on twos.
The image should deliberately contain:
* real, lightly graded footage
* flat saturated cartoon creatures with thick wobbly outlines
* googly eyes with clear eye lines
* correct occlusion behind people
* contact with real surfaces
* one doodle sticker character
* hand-drawn line boil.
Avoid glossy 3D mascots.
```
