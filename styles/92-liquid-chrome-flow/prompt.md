# 92 — Liquid Chrome Flow

**Look:** Mirror-polished liquid metal flows through the real office. Fat chrome ribbons swell, pinch and ripple across the room, blobs of mercury drift, split and merge, and drips hang from the top edge, all reflecting a bright studio sky, a sharp dark horizon line and the room itself. A lower chrome ribbon wraps round the group at waist height, in front of the middle person and behind the two at the sides. The people stay photographic and untouched; the room is graded slightly cool so the metal pops.

**Also called / where it trends:** "chrome flow", "liquid chrome", "liquid metal effect", "chrome liquid trend", "melting metal effect", "mercury flow", "Y2K liquid chrome 3D". A 2025–26 TikTok and Instagram AI-edit trend (CapCut, Higgsfield, Kling, Hailuo "liquid metal" presets and "how to do the viral chrome flow" tutorials), and a long-running 3D-render look on Pinterest and Behance.

**References:**
- TikTok search "liquid chrome metal effect video ai" (screenshot `refs/ref_1.png`, from the D1 discovery sweep): chrome-flow trend edits and tutorials. Example posts: https://www.tiktok.com/@meowstardaily/video/7680581615130660126, https://www.tiktok.com/@finely.ai/video/7510366938736954646, https://www.tiktok.com/@xbus90971631/video/7681350030183206158.
- https://www.pinterest.com/search/pins/?q=liquid%20chrome%20metal%20flow%20art (screenshot `refs/ref_2.png`): liquid chrome splashes, ribbons, drips and blobs; studio-sky reflections with a hard dark horizon band.
- https://usepromptup.com/prompts/video-higgsfield-viral-turning-metal-melting/: "Turn to chrome, then melt" Higgsfield / Kling prompt for the viral liquid-metal edit.
- https://www.somake.ai/tools/liquid-metal-coverage-video-effects: "liquid metal coverage" video effect (molten chrome flowing over a scene).
- https://www.tomoviee.ai/video-effects/ai-liquid-metal-video-generator.html: liquid metal AI video effect preset page.
- https://miraflow.ai/blog/ai-melting-effect-prompts-2026: 2026 round-up of melting / liquid metal effect prompts.
- Differs from **15 Y2K Chrome / Frutiger Aero** (bubbly chrome type, glossy UI and aqua gradients as graphic design: here it is physical liquid metal moving through the real room), **45 Marble Statue** (turns the person's own material to stone: here the people stay real and the metal is a separate fluid around them) and **44 Broken Mirror Shards** (flat cracked mirror pieces: here the reflective surface is round, fluid and moving).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. A local approximation made with `render.py` (numpy + OpenCV + the person masks). All metal is one smooth metaball field (compact Wyvill kernels): blobs with orbiting satellite droplets, two ribbons made of bead chains along travelling double sine waves whose thickness swells and pinches, and three drips with a pool, a thinning neck and a fat drop. Height is `sqrt(field − threshold)`, so edges turn vertical and crowns stay round; each pixel is shaded as a perfect mirror through a sphere-map lookup into a studio environment (white sky with softboxes, a sharp dark horizon, a dark floor) mixed with a blurred copy of the frame, plus hard specular glints and darker grazing rims. Layering comes from the masks: everything behind the people except the lower ribbon, which is drawn in front only over the mask run of the middle person at waist height and never above the faces. Contact shadows sit on the wall under the metal.

## Prompt

```text
I'm uploading one video clip. Convert it into a LIQUID CHROME FLOW frame-by-frame animation: mirror-polished liquid metal ribbons, blobs and drips flow through the real scene and around the people, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Liquid chrome flow, mirror-polished liquid metal, mercury, molten chrome ribbons and blobs, studio reflections, hyper-real 3D render composited into live footage.
Transform the footage into a frame built from:
* the REAL scene and the REAL people, photographic and untouched
* thick LIQUID CHROME RIBBONS flowing across the room, swelling and pinching like poured mercury
* floating chrome BLOBS that stretch, split off droplets and merge back
* chrome DRIPS hanging from the top edge: a pool, a thinning neck, a heavy drop
* one ribbon that WRAPS around the group at waist height
* PERFECT MIRROR surfaces: bright white sky on the crowns, a sharp DARK HORIZON band along the flanks, dark floor reflections underneath
* the ROOM and the PEOPLE visible, warped, in the reflections
* hard white SPECULAR glints
* dark grazing rims at the silhouettes of the metal
* soft CONTACT SHADOWS on the wall under the metal
* a slightly cool, slightly desaturated room grade so the chrome pops
The result should feel like someone:
FILMED THE SCENE
→ POURED LIQUID MERCURY THROUGH THE AIR AROUND THE PEOPLE
→ LIT IT IN A WHITE PHOTO STUDIO
→ RENDERED IT AS PERFECT CHROME
→ COMPOSITED IT FRAME BY FRAME, PART BEHIND AND PART IN FRONT OF THE PEOPLE
→ PLAYED IT BACK AT 12 FPS.
CHARACTER — PHOTOGRAPHIC, UNTOUCHED
The people stay PHOTOGRAPHIC.
They are NOT turned to chrome.
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
Do NOT put chrome on skin, hair or clothes.
Chrome never crosses a face.
THE METAL — SHAPES
* Ribbons are thick, round in cross-section, flowing in long S-curves; their thickness swells into bulges and pinches into necks along the length.
* Blobs are rounded and soft, never spiky; small droplets orbit them, pinch off and merge back.
* Drips hang from the top edge of the frame, stretch longer and shorter over time, and end in a fat drop.
* Everything is ONE liquid: where shapes touch they merge smoothly with no seam.
THE METAL — SURFACE
* A perfect mirror: no texture, no brushed lines, no rust.
* Crowns reflect a bright white studio sky with soft rectangular softboxes.
* Below the crown a SHARP dark horizon line runs along every shape, then a dark floor reflection.
* The room (window, wall, plant, screen) and the people appear warped inside the reflections.
* Small hard white specular highlights.
* Slightly darker edges where the surface turns away.
* A faint cool steel tint.
LAYERING
* Behind the people: the drips, the blobs and the upper ribbon (passing across the window and wall above shoulder height).
* The lower ribbon passes IN FRONT of the middle person at waist height and BEHIND the people at the sides, so it reads as wrapping around the group.
* Nothing in front of any face, ever.
* Soft shadows on the wall under the metal; a slight darkening on clothes just under the ribbon in front.
ROOM GRADE
Cool and a touch desaturated, a little contrast; the people keep their natural skin tones.
PALETTE
Chrome white, steel grey, deep graphite black, faint cool blue.
The room's own colours, muted.
Do NOT add gold, rainbow oil-slick or neon colours to the metal.
OBJECT CONTINUITY
If the character holds an object, it stays real and in the hand; the chrome flows around it.
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
The people must match the source frame exactly.
The wrapping ribbon stays at the middle person's waist as they move.
NO chrome stuck to a person's body.
NO cut-out halo around the people.
FRAME-TO-FRAME LIQUID FLOW
THIS IS CRITICAL.
It must feel like one continuous liquid simulation, not new metal every frame.
Between consecutive frames:
* ribbons travel along their length a few pixels; bulges roll along them
* blobs drift slowly, wobble, and their droplets orbit
* drips stretch and shrink gradually
* reflections slide over the surfaces as the shapes move
Keep FIXED:
* the number of ribbons, blobs and drips
* the studio environment in the reflections
* the room grade
DO NOT
Do NOT turn the people into chrome or statues.
Do NOT cover faces with metal.
Do NOT make the metal flat grey plastic; it must be a mirror with a hard horizon reflection.
Do NOT use spiky splashes or sharp shards.
Do NOT invent new metal shapes every frame.
Do NOT add rainbow or oil-slick colour.
Do NOT redraw or illustrate the people.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
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
* NO chrome, blobs or drips
* NO colour grade
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
Do NOT begin the liquid chrome transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – LIQUID CHROME FLOW STYLING (AFTER MY CONFIRMATION ONLY)
First, describe the paths of the ribbons, where the blobs and drips start, and which person the lower ribbon passes in front of.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Give each frame the metal's state for its moment, moved on a little from the previous frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, layering or the continuous flow broke — regenerate those frames only.
The final video must feel like LIQUID MERCURY FLOWING THROUGH THE ROOM around real people: mirror chrome ribbons, drifting blobs, hanging drips, 12 frames per second.
The image should deliberately contain:
* thick flowing chrome ribbons with travelling bulges
* merging chrome blobs and droplets
* drips from the top edge
* a ribbon wrapping the group at waist height
* mirror reflections with a sharp dark horizon band
* untouched, photographic people.
Avoid flat grey plastic and chrome on faces.
```
