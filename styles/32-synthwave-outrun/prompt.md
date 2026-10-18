# 32 — Synthwave Outrun

**Look:** The footage is moved into an 1980s retro-futurist night, the world of *Kung Fury*, *Far Cry 3: Blood Dragon* and Kavinsky / The Midnight album covers. The real room is replaced by a violet-to-magenta sky with stars and a huge striped sunset sun. Below the horizon a glowing wireframe grid floor scrolls toward the camera, with wireframe mountains on the skyline. The people stay as they are but are graded in a hot-pink-to-indigo gradient map. They get a cyan rim light on one side, a magenta rim on the other, and a chrome highlight along their edges. Bloom, CRT colour roll and scanlines finish it like a VHS cover.

**Also called / where it trends:** "synthwave", "retrowave", "outrun", "80s aesthetic", "neon grid", "Miami / vaporwave sunset". The look is a steady YouTube and After Effects tutorial genre (retrowave backgrounds, grid loops). It is a staple of r/outrun and of synthwave music-video edits, and the 2025-26 "80s AI video" trend puts people into neon-grid 1980s scenes.

**References:**
- https://www.pinterest.com/search/pins/?q=synthwave%20portrait%20neon%20grid%20sunset%20photo%20edit: portrait edits with a neon grid, striped sun and pink/cyan rim light (screenshot `refs/ref_1.png`).
- https://www.pinterest.com/search/pins/?q=outrun%20retrowave%20aesthetic%20grid%20sun%20chrome: outrun / retrowave artwork with the grid floor, the sun, chrome and wireframe mountains (screenshot `refs/ref_2.png`).
- https://www.premiumbeat.com/blog/create-retrowave-background-loop-after-effects/: PremiumBeat, building a retrowave background loop (grid floor, gradient sun with looping lines, VHS finish). The article calls it "retrowave (sometimes referred to as synthwave or outrun)".
- https://www.reddit.com/r/outrun/comments/a66y4p/how_to_edit_video_footage_to_create_an_80soutrun/: r/outrun, editing live footage into an 80s outrun look.
- https://newretro.net/blogs/main/how-to-create-80s-style-retrowave-synthwave-art-in-adobe-photoshop: NewRetroWave, 80s retrowave/synthwave art in Photoshop.
- https://www.youtube.com/watch?v=XhZuhiGw6Tc: synthwave / retrowave video edit tutorial.
- https://www.lightxeditor.com/blog/80s-ai-video-trend-prompt-ideas-to-turn-yourself-into-a-1980s-hollywood-star/: the 80s AI video trend.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (whole clip) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). The room is replaced by an indigo-to-magenta sky with twinkling stars and a striped sun that sits behind the group (its stripe gaps drift upward). Wireframe mountains sit on a horizon at 60% height, above a perspective grid floor that scrolls every frame. The people get a CLAHE gradient map (indigo, hot pink, peach), cyan/magenta rims from the matte normals, sun top-light and chrome specular edges. Bloom, ±2 px CRT channel roll, rolling scanlines and grain finish the frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a SYNTHWAVE OUTRUN frame-by-frame animation (the 1980s retrowave / outrun look), matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into an 1980s retro-futurist night scene:
* the real background REPLACED by a synthwave world
* a sky graded from deep indigo at the top, through violet, to hot magenta at the horizon
* small stars twinkling in the upper sky
* a huge SUNSET SUN behind the people, graded yellow to orange to pink, cut by horizontal stripe gaps
* glowing WIREFRAME MOUNTAINS on the horizon
* a glowing magenta/cyan PERSPECTIVE GRID FLOOR that scrolls toward the camera
* a bright cyan horizon line
* the people kept real, graded in a hot-pink / indigo / peach gradient map
* a CYAN RIM LIGHT on one side of each person and a MAGENTA RIM on the other
* a thin CHROME highlight along the people's edges
* bloom, CRT colour roll, scanlines and grain, like a VHS cover
The result should feel like someone:
FILMED THE PEOPLE ON A NEON-LIT 1985 SOUNDSTAGE
→ KEYED THEM OVER A RETROWAVE SUNSET
→ RAN THE GRID FLOOR UNDER THEIR FEET
→ LIT THEM WITH CYAN AND MAGENTA GELS
→ PRINTED IT ONTO A VHS TAPE
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — NEON-LIT, STILL THEMSELVES
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing and clothing patterns
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Keep the faces REAL and recognizable. Only the light and colour change.
Do NOT give them 80s costumes, mullets, aviators, leg warmers or shoulder pads.
Do NOT turn them into chrome statues or 3D renders.
LIGHTING ON THE PEOPLE
* Grade the people through a gradient map: shadows deep indigo, mids hot pink, highlights warm peach.
* Keep their local contrast, so faces, folds and clothing patterns stay readable.
* Cyan rim on the left edges, magenta rim on the right edges, following the shape of the body.
* A soft warm top-light from the sun on heads and shoulders.
* A thin, bright chrome specular line right on the outer edge.
* A soft coloured glow spilling from the rims into the air around them.
SKY AND SUN
* The sun sits behind the people, about a third of the frame tall, centred on the group.
* The lower half of the sun is cut by horizontal stripe gaps that drift slowly upward.
* The sun has a soft pink glow around it.
* Stars are a fixed field that twinkles; they do not move.
GRID FLOOR AND MOUNTAINS
* The horizon sits a little below the middle of the frame.
* Below it, a perspective grid of glowing lines: horizontal lines spaced closer near the horizon, converging lines running to a vanishing point.
* The grid scrolls toward the camera continuously, a little on every frame.
* Wireframe mountains in glowing lines sit on the horizon, behind the people and in front of the sun.
* Keep the original room's furniture out of the background. If the people sit on a chair or sofa, keep that object, graded like the people.
VHS FINISH
* Bloom on every light: sun, grid, rims.
* A slight CRT colour roll: red and blue channels shifted a pixel or two sideways, varying per frame.
* Faint horizontal scanlines rolling slowly down.
* Fine grain.
* A soft vignette.
PALETTE
* Indigo, violet, hot magenta, hot pink, cyan, sunset orange and yellow, warm peach.
Do NOT use natural daylight colours.
Do NOT use green.
OBJECT CONTINUITY
If the character interacts with an object (phone, chair, bag), keep the object and light it with the same rim lights. It moves exactly with the original action.
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
The people's motion must match the source footage exactly on EVERY frame.
The rim lights and chrome edge follow the body.
NO halo left behind from the previous frame.
NO cut-out edge artefacts or room fragments around the people.
FRAME-BY-FRAME BOIL
THIS IS CRITICAL.
Every frame is generated individually, so:
* the grid floor advances a little every frame
* the sun stripes drift a little every frame
* the stars twinkle differently every frame
* the CRT roll, scanline position and grain change every frame
The sun, mountains and horizon stay in the same place for the whole clip.
DO NOT
Do NOT keep the original room in the background.
Do NOT add cars, palm trees, logos or text.
Do NOT add 80s costumes or props.
Do NOT make the people chrome or plastic.
Do NOT let the people's colours wash out to a single flat pink.
Do NOT jump the sun or horizon between frames.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
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
* NO background replacement
* NO grid, sun or mountains
* NO rim lights
* NO VHS finish
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
Do NOT begin the synthwave transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SYNTHWAVE STYLING (AFTER MY CONFIRMATION ONLY)
First, generate ONE empty background plate with Seedream 5.0 Pro (sky, stars, striped sun, mountains, grid floor, no people) and show it to me. Fix the sun position and horizon height from this plate for the whole clip.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the pose is exactly that frame, together with the background plate as the style and layout reference.
Advance the grid scroll and the sun-stripe drift by a small fixed step on each frame.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing or the style rules broke (room showing through, sun jumping, grid running backward) — regenerate those frames only.
The final video must feel like A 1985 RETROWAVE ALBUM COVER IN MOTION: the real people, neon-rimmed in cyan and magenta, in front of a striped sunset sun and wireframe mountains, over a scrolling glowing grid, with VHS bloom and scanlines, 12 frames per second.
The image should deliberately contain:
* a striped sunset sun
* a scrolling perspective grid
* wireframe mountains
* cyan / magenta rim light
* chrome edge highlights
* bloom, CRT roll and scanlines.
Avoid polished digital perfection.
```
