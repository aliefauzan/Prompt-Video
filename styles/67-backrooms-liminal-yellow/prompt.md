# 67 — Backrooms Liminal Yellow

**Look:** The office becomes Level 0 of the Backrooms. The whole picture sinks into one sickly mono-yellow: olive-brown shadows, mustard mid-tones and pale cream highlights under flat, shadowless fluorescent light. The white walls turn into old yellow wallpaper with thin pinstripes, a small diamond motif and faint damp stains. The window is a blown-out fluorescent light box with a soft hum-like glow. The people stand in it with a yellow cast on their skin, as if they took a wrong turn and noclipped out of reality. The camera is a cheap wide-angle with a slight fluorescent flicker.

**Also called / where it trends:** the Backrooms, Level 0, "backrooms filter", "backrooms color grading", "make your photo look like the Backrooms", liminal space, liminal core, "noclip", 后室 (Bilibili, Douyin). It started as a 2019 4chan creepypasta about an empty yellow office, grew through Kane Pixels' (Kane Parsons) Blender found-footage series (2022, now an A24 film), and lives on TikTok as CapCut grading tutorials (#backrooms, "backrooms liminal filter"), Pinterest liminal-space boards and r/LiminalSpace and r/backrooms on Reddit.

**References:**
- https://www.tiktok.com/@awsalater/video/7654750896219376926: "Backrooms color grading using CapCut" tutorial (TikTok search screenshot `refs/ref_1.png`, from the discovery sweep D1).
- https://www.tiktok.com/@leolikesphotos/video/7106628495865941253: before/after of a real room graded to Backrooms yellow.
- https://www.tiktok.com/@revolve_vr/video/7274690107402145066: "then go to video effects" CapCut backrooms recipe.
- https://www.youtube.com/watch?v=rTLxv_TlzIE: backrooms liminal edit on YouTube.
- https://www.pinterest.com/search/pins/?q=backrooms%20level%200%20yellow%20liminal (screenshot `refs/ref_2.png`): mono-yellow rooms, pinstripe wallpaper, drop-ceiling fluorescent panels, damp carpet, endless corridors.
- https://www.pinterest.com/search/pins/?q=liminal%20space%20backrooms%20fluorescent and https://www.instagram.com/popular/liminal-space/: liminal-space boards.
- https://en.wikipedia.org/wiki/The_Backrooms: origin, Level 0 description ("mono-yellow" wallpaper, humming fluorescent lights, moist carpet), Kane Pixels.
- https://kanepixelsbackrooms.fandom.com/wiki/Backrooms_(place): the Kane Pixels version of the place.
- https://nimaid.blogspot.com/2024/08/color-correcting-backrooms-using-real.html: colour-correcting the original Backrooms photo against real wallpaper and carpet samples (why the room reads so yellow).
- https://bluelabyrinths.com/2024/03/14/semiotics-of-the-end-the-backrooms/: essay on why the empty yellow office feels uncanny.
- Bilibili 后室 edits: https://www.bilibili.com/video/av594183358 , https://www.bilibili.com/video/av707275138 (from discovery sweep D4).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). Local contrast is squashed toward a large blur for flat light, then every pixel is mapped onto a six-stop mono-yellow ramp; the people keep 30 % of their own colour. The white walls (low-saturation background) get a procedural pinstripe + diamond wallpaper and damp blotches, anchored to the room by a phase-correlation camera track. The window becomes a blown-out light box with glow, plus top-down light fall-off, a small fluorescent flicker with an occasional dip, mild barrel distortion, softness and noise.

## Prompt

```text
I'm uploading one video clip. Convert it into a BACKROOMS LIMINAL YELLOW frame-by-frame animation: every frame should look like the people are standing in Level 0 of the Backrooms, an endless empty yellow office under humming fluorescent light, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
The Backrooms, Level 0: liminal space, mono-yellow, flat fluorescent lighting, old wallpaper, damp carpet, uncanny emptiness, late-1990s office.
Transform the footage into a liminal-space frame built from:
* ONE dominant colour: sickly MONO-YELLOW
* olive-brown shadows, mustard mid-tones, pale cream-yellow highlights
* FLAT, SHADOWLESS fluorescent light from above
* old YELLOW WALLPAPER on every wall: thin vertical pinstripes with a small repeating diamond motif
* faint DAMP STAINS and discoloured patches on the wallpaper
* bright windows and light sources turned into BLOWN-OUT FLUORESCENT light boxes
* a soft glow around the lights
* a slight wide-angle lens bulge, slightly soft focus
* fine sensor noise
* a dim fall-off toward the lower corners
The result should feel like someone:
NOCLIPPED OUT OF THE REAL OFFICE
→ INTO AN ENDLESS, EMPTY YELLOW ROOM
→ UNDER BUZZING FLUORESCENT TUBES
→ FILMED IT ON A CHEAP WIDE-ANGLE CAMERA
→ AND THE ROOM ITSELF STAINED EVERYTHING YELLOW.
CHARACTER — REAL, SICKLY LIT
The people stay PHOTOGRAPHIC. They are the same real people, lit by the same flat yellow fluorescent light as the room.
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
Do NOT turn them into a painting, cartoon, 3D render or monster.
Skin takes a sickly yellow cast but still reads as skin.
Clothes keep their pattern and value but shift into the yellow family.
COLOUR — MONO-YELLOW
* The room is almost monochrome: every colour folds into one yellow ramp.
* Shadows: dark olive-brown, never pure black, never blue.
* Mid-tones: dirty mustard / Level 0 wallpaper yellow.
* Highlights: pale cream-yellow; light sources near white.
* People may keep a little of their own colour (about a third), so faces stay human.
* No blue, no green surveillance tint, no teal, no red.
LIGHT
* Flat, even, overhead fluorescent light; almost no cast shadows; low local contrast.
* Slightly brighter at the top of the frame, dimmer in the lower corners.
* Windows and screens become flat, blown-out fluorescent light boxes with a soft glow.
WALLS AND ROOM
* Every flat wall becomes old Level 0 wallpaper: vertical pinstripes about 2–3 cm apart with a small diamond motif between them.
* The wallpaper is faded, slightly stained, with damp blotches.
* The pattern is fixed to the wall: it moves with the room when the camera moves and never swims.
* Furniture, plants and cabinets stay in place but fold into the same yellow ramp.
* Any visible floor reads as damp, flat mustard carpet.
* The room should feel EMPTY and too quiet: no added props, no people, no signs.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand and lit like the rest.
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
The wallpaper, stains and light boxes stay locked to the room as the camera moves.
NO wallpaper pattern sliding over the wall between frames.
NO light box moving away from its window.
FRAME-TO-FRAME FLUORESCENT LIFE
THIS IS CRITICAL.
It must feel like a real camera in a room with old fluorescent tubes, not a still filter.
Allow between consecutive frames:
* fine noise to change every frame
* overall brightness to wobble slightly (±2%), like a 50/60 Hz tube
* about every 3–4 seconds, ONE frame that dips darker (about −7%), then recovers over the next frame
* the glow around the light boxes to shimmer very slightly
Keep FIXED:
* the mono-yellow grade (no colour pumping)
* the wallpaper pattern and stain positions
* the lens distortion
DO NOT
Do NOT add VHS tape lines, tracking errors, timestamps or a REC overlay.
Do NOT add a green night-vision or CCTV look.
Do NOT add monsters, entities, blood or horror props.
Do NOT make it a warm golden-hour or sepia vintage photo: the yellow is fluorescent and sickly, not sunny.
Do NOT leave white walls white.
Do NOT add dramatic shadows or spotlights.
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
* NO colour grade
* NO wallpaper or stains
* NO light boxes, glow or flicker
* NO lens distortion or noise
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
Do NOT begin the Backrooms transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – BACKROOMS LIMINAL YELLOW STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me which surfaces will get the wallpaper, which will become fluorescent light boxes, and on which frames the flicker dips fall.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME grade and the SAME wallpaper on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, grade consistency or wallpaper tracking broke — regenerate those frames only.
The final video must feel like A WRONG TURN INTO LEVEL 0: mono-yellow, flat fluorescent light, stained pinstripe wallpaper, glowing light boxes, a faint flicker, 12 frames per second.
The image should deliberately contain:
* one sickly mono-yellow colour family
* flat, shadowless fluorescent light
* pinstripe-and-diamond wallpaper with damp stains
* blown-out fluorescent light boxes with glow
* a slight wide-angle bulge and fine noise.
Avoid clean, neutral office lighting.
```
