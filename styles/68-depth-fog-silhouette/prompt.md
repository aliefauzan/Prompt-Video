# 68 — Depth-Style Fog Silhouette

**Look:** The clip becomes the CapCut "depth style" edit. The people turn into soft charcoal depth-map silhouettes, darkest where the body is thickest and nearest and lighter grey toward thin limbs and edges. Only a faint relief of faces and clothes survives. The room dissolves into bright white fog, with just ghost shapes of the window, TV and furniture left. Low ground fog rolls across the legs and the camera pushes in slowly. Late in the clip the faces ignite with glowing laser-red eyes.

**Also called / where it trends:** "depth style", "depth style edit", "DEPTH STYLE TREND" (CapCut template), "fog depth style trend", "depth style + laser eyes", "depth map edit", "fog silhouette edit". It is a 2026 TikTok / CapCut trend, used for football highlight edits, dance clips and "goated trend" posts. Templates and tutorials circulate on TikTok (one tutorial has 256K likes), CapCut template pages, YouTube Shorts and Instagram Reels.

**References:**
- https://www.tiktok.com/@letsayhey/video/7675064280814783758: "Depth style in 5 seconds!", 256K likes (TikTok search screenshot `refs/ref_1.png`, from the discovery sweep D1; the same search shows the "laser eyes + depth style" tutorial).
- https://www.tiktok.com/@ripedtx_/video/7675956729426873621: "Tutorial on this depth style", CapCut.
- https://www.tiktok.com/@evaned1t/video/7671058197435878677: depth-style trend tutorial.
- https://www.youtube.com/watch?v=ADSs7X1zLQc: depth-style edit tutorial on YouTube.
- https://www.capcut.com/template-detail/DEPTH-STYLE-TREND/7676853793241271569: the "DEPTH STYLE TREND" CapCut template (#depthstyle).
- https://www.capcut.com/explore/depth-style-edit and https://www.capcut.com/create/depth-style-football-highlight-edits: CapCut's own depth-style landing pages (football edits).
- https://capcuttemplate.co.in/depth-style-trend-capcut-template/: template guide (keep the subject centred, short clips, 1080p).
- https://www.pinterest.com/search/pins/?q=depth%20style%20edit%20fog%20silhouette (screenshot `refs/ref_2.png`): the photographic mood the trend borrows, dark figures dissolving into white fog.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks + Apple Vision pupils in `faces.json`, copied from the face pass of style 10). Pseudo-depth for the people comes from the distance transform of the matte (thick = near = dark), plus a faint high-pass relief from the source. The fog light wraps into the edges, and the background is the source blurred and lifted into white fog. Two drifting fog fields make the ground fog and the veil. A 12 % push-in runs over the clip, and from frame 133 the laser-red eyes ignite (glow + horizontal streak); faces the tracker loses for up to 3 frames are held.

## Prompt

```text
I'm uploading one video clip. Convert it into a DEPTH-STYLE FOG SILHOUETTE frame-by-frame animation (the CapCut "depth style" trend): every frame should show the people as soft charcoal depth-map silhouettes standing in bright white fog, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Depth-map silhouette in fog: monochrome, high-key, soft, minimal, cinematic, mysterious.
Transform the footage into a depth-style frame built from:
* BRIGHT WHITE FOG filling the whole room
* only GHOST SHAPES of the background left (window, screen, furniture as pale grey forms)
* the people as soft CHARCOAL DEPTH-MAP SILHOUETTES
* nearer / thicker parts of the body DARKER, thin limbs and edges LIGHTER grey
* a faint relief of faces, hair and clothing folds inside the silhouette
* fog light WRAPPING softly into the silhouette edges
* low GROUND FOG rolling across the legs and lower frame
* a thin drifting fog VEIL over everything
* soft bloom, fine grain
* a SLOW PUSH-IN over the whole clip
* in the last part of the clip, glowing LASER-RED EYES
The result should feel like someone:
RAN THE CLIP THROUGH A DEPTH MAP
→ KEPT ONLY THE PEOPLE AS DARK VOLUMES
→ FLOODED THE ROOM WITH WHITE FOG
→ PUSHED THE CAMERA IN SLOWLY
→ LIT THEIR EYES RED ON THE BEAT
→ AND EXPORTED IT AS A TREND EDIT.
CHARACTER — DEPTH SILHOUETTE
The people become shaded silhouettes, but the SAME silhouettes: outline, pose and gesture must be exact.
Preserve the person's exact:
* identity (readable from outline, hair shape and the faint facial relief)
* face shape
* expression (as faint relief)
* hairstyle
* glasses (as faint relief)
* clothing shape
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT turn them into flat black cut-outs with no shading.
Do NOT turn them into 3D mannequins, robots, ghosts or shadow monsters.
Do NOT add colour to the people, except the laser eyes.
DEPTH SHADING
* Tone = distance: the closest, thickest parts (torso, head of the person nearest the camera) are darkest charcoal, almost black.
* People further back are a lighter grey than people in front.
* Thin parts (arms, fingers, hair ends) and outline edges fade lighter, as if the fog eats them.
* Inside the silhouette, keep only a faint low-contrast relief: eye sockets, nose, mouth, collar, folds, stripes on clothing.
* Smooth gradients only; no hard cel edges.
FOG AND BACKGROUND
* The background is almost white (pale grey at most).
* Windows, screens, plants and furniture remain only as soft pale-grey ghost shapes.
* The floor area fades to a soft grey ground.
* Ground fog rolls across the bottom third and over the legs; a thin veil drifts across the whole frame.
CAMERA
* One slow, continuous push-in from the first frame to the last (about 10–15 % scale), centred a little above the middle.
* No shake, no cuts, no speed ramps.
LASER EYES
* From about 11 seconds in (or on the beat I give you), each visible face gets glowing laser-red eyes.
* Each eye: a white-pink hot core, a strong red glow, and a thin horizontal red streak.
* The eyes ignite over 3–4 frames, then stay locked to the pupils as the head moves.
* Before that point: no red anywhere.
PALETTE
White, pale fog grey, mid grey, charcoal, near-black.
The only colour is the laser red.
OBJECT CONTINUITY
If the character holds an object, it becomes part of the silhouette and stays attached to the hand.
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
The silhouettes must match the source frame exactly.
The laser eyes stay on the pupils.
NO silhouette swelling, shrinking or wobbling between frames.
NO eyes sliding off the face.
FRAME-TO-FRAME FOG LIFE
THIS IS CRITICAL.
It must feel like real fog moving through a scene, not a still filter.
Allow between consecutive frames:
* ground fog to drift sideways steadily
* the veil to drift slowly the other way
* fine grain to change every frame
* the laser glow to flicker slightly (±10%)
Keep FIXED:
* the depth shading of each person (no tone pumping)
* the background ghost shapes
* the push-in speed
DO NOT
Do NOT add colour to the room or the people (except the laser eyes).
Do NOT use thermal or false-colour depth palettes.
Do NOT turn the people into point clouds, wireframes or particles.
Do NOT make the background dark: this is high-key white fog.
Do NOT add lightning, sparks, smoke trails or extra effects.
Do NOT add laser eyes before the chosen moment.
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
* NO depth shading or silhouettes
* NO fog
* NO push-in
* NO laser eyes
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
Do NOT begin the depth-style transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – DEPTH-STYLE FOG SILHOUETTE STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the push-in amount and centre, the depth order of the people (nearest to furthest), and the frame where the laser eyes ignite.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the silhouettes are exactly that frame.
Apply every style rule above, with the SAME tones on every frame.
Apply the push-in as a smooth crop/scale after styling, the same curve for every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, tone consistency or laser-eye tracking broke — regenerate those frames only.
The final video must feel like THE DEPTH STYLE TREND: dark depth-map people dissolving into white fog, ground fog drifting, a slow push-in, laser-red eyes on the beat, 12 frames per second.
The image should deliberately contain:
* soft charcoal depth-shaded silhouettes
* bright white fog with ghost shapes of the room
* drifting ground fog
* a slow push-in
* laser-red eyes in the final section.
Avoid colour footage and flat black cut-outs.
```
