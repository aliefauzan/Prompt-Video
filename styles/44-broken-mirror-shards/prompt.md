# 44 — Broken Mirror Shards

**Look:** The scene seen in a shattered mirror. A white crushed impact point sits on the main person's face or chest. Straight radial cracks run out to the frame edges, and straight chord cracks cut concentric rings of glass between them. Each shard reflects the scene with its own small tilt, scale and shift, so a face breaks into pieces that don't quite line up. About half the shards show a moment 1–4 frames earlier, and a few have fallen out and show the dark mirror backing. Crack seams are dark with a thin bright glass edge, and a glint sweeps across the glass. A new impact (a new shatter) starts every 3 seconds, and its cracks spread over 3 frames.

**Also called / where it trends:** "broken mirror effect", "broken glass reflection", "shattered mirror edit", "glass shatter transition", "cracked screen effect". Higgsfield ships it as the **Broken mirror** preset (Mixed Media and Effects), Melies lists it among its "viral looks", and CapCut has broken-glass templates that circulate on TikTok and Reels.

**References:**
- https://melies.co/cinematic-techniques/viral-looks (`refs/ref_1.png`): Melies "viral looks" page, Broken Mirror entry. Source of the core rule: one reflection split into misaligned shards with fractured identity.
- https://higgsfield.ai/effects/examples/broken-mirror (`refs/ref_2.png`): Higgsfield "Broken glass reflection effect" example. Source of the radial crack pattern and per-shard offsets.
- https://higgsfield.ai/mixed-media: Higgsfield Mixed Media preset list, which includes "Broken mirror" and "Fragments".
- https://www.capcut.com/explore/broken-glass-effect: CapCut broken-glass effect explore page (templates and tutorials).
- https://www.tiktok.com/@kyvnme/video/7457874096425094405: @kyvnme, broken glass edit on TikTok.
- https://www.vetriveo.in/2026/02/bgm173.html: broken-mirror AI photo prompt write-up (Feb 2026).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV). The impact point is set on the upper body of the largest person in each section. A shard map is built from 14–19 straight radial cracks, straight ring chords at random radii (some missing) and a few long crossing cracks. Each shard remaps the frame with its own rotation (±4.5°), scale (0.95–1.06) and shift, and sometimes uses a frame 1–4 frames back. Each shard gets its own silver tint and gain, and 10% of shards near the impact show the dark backing. Seams are drawn as a dark core with an offset highlight. A crushed white impact, a moving glint, an edge tarnish vignette and fine grain finish it. There are five sections, and the cracks spread over each section's first 3 frames.

## Prompt

```text
I'm uploading one video clip. Convert it into a 12 FPS BROKEN MIRROR / SHATTERED GLASS REFLECTION frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
Seedream works here because every shard is a slightly shifted copy of the same source frame; the crack map is fixed per section and passed in as an image.
CORE VISUAL STYLE
Every frame looks like the scene reflected in a mirror that has just been hit:
* one crushed white impact point
* straight radial cracks running from the impact to the frame edges
* straight chord cracks cutting rings of glass between the radial cracks
* shards that get bigger the further they are from the impact
* every shard reflecting the scene with its own small tilt, scale and shift
* faces broken across shards that do not line up
* many shards showing a slightly earlier moment
* a few missing shards showing the dark mirror backing
* dark crack seams with a thin bright glass edge
* a silver, slightly cool mirror tone
It should look like the Higgsfield "Broken mirror" preset and the CapCut broken glass edits.
The result should feel like someone:
FILMED THE SCENE IN A WALL MIRROR
→ HIT THE MIRROR ONCE, HARD
→ LET EVERY SHARD TILT A LITTLE IN ITS FRAME
→ KEPT FILMING THE REFLECTION AT 12 FRAMES PER SECOND
→ ANIMATED IT FRAME-BY-FRAME.
PALETTE RULES
Keep the source colours inside the shards.
Each shard gets a small, random shift: brightness ±10%, and a slight cool silver desaturation (0–18%).
The crack seams are near black.
The glass edges and the impact are near white.
Missing shards show a very dark grey backing (about 8%) with fine speckle.
CRACK GEOMETRY
Use 14–20 radial cracks from the impact point, all STRAIGHT.
Between neighbouring radial cracks, add straight chords at growing radii, so the glass breaks into rings of four-sided shards.
Leave some chords out so the rings are broken and uneven.
Add 2–4 long straight cracks that cross the whole sheet.
Near the impact the shards are small and dense; at the frame edges they are large.
Cracks are thin: a 2–4 px dark seam with a 1 px bright edge on one side.
Do NOT draw curved, wavy or hand-drawn cracks.
Do NOT draw a regular grid or honeycomb.
SHARD REFLECTIONS
Each shard shows the SAME scene, but tilted by up to ±4.5°, scaled 0.95–1.06 and shifted by about 25 px on average, all around the impact point.
Neighbouring shards must disagree, so lines and faces visibly break at every crack.
About half the shards reflect the scene 1–4 frames earlier.
The impact is placed on the upper body or face of the main person.
IMPACT
The impact point is a small crushed-white star of powdered glass (about 40 px across).
Very fine spider cracks surround it.
A soft glint sweeps slowly across the glass from frame to frame.
BACKGROUND
The room stays the room, reflected and broken like the people.
Add a faint dark tarnish toward the mirror's edges.
Do NOT replace the background.
SECTIONS AND CRACK GROWTH
Split the clip into 5 sections of about 3 seconds each.
Each section is a NEW impact at a new point, with a new crack pattern.
In each section's first frame, only the radial cracks and the inner rings exist.
By the third frame the full pattern is there.
After that, the crack pattern is LOCKED for the rest of the section.
FRAME-TO-FRAME BEHAVIOUR (BOIL RULES)
THIS IS CRITICAL.
The glass does NOT move within a section: same cracks, same shard tilts, same missing shards.
Only the reflected scene moves behind the cracks, with the real motion of the footage.
Allow between consecutive frames:
* the glint to drift
* grain to change
Keep FIXED within a section:
* the impact point
* every crack line
* every shard's tilt, scale, shift, tint and time offset
OBJECT CONTINUITY
If the character holds or touches an object (phone, cup, bag, microphone), it is reflected and broken like the rest.
Do NOT erase it.
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
The scene inside the shards must match the source frame exactly in position, pose and timing, apart from each shard's fixed small offset.
Do NOT invent motion that is not in the footage.
DO NOT
Do NOT draw curved or wavy cracks.
Do NOT use a jigsaw, grid or honeycomb pattern.
Do NOT let the cracks move, grow or change within a section after frame 3.
Do NOT make shards fly apart or explode.
Do NOT add blood, fire, smoke or debris.
Do NOT add a mirror frame, wall or hands.
Do NOT redraw or illustrate the people.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
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
* NO cracks
* NO shard offsets
* NO colour changes
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
Do NOT begin the broken-mirror transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – BROKEN MIRROR STYLING (AFTER MY CONFIRMATION ONLY)
First, plan the sections and list them for me: frame range and impact point (x, y) for each section.
For each section, make ONE crack map image (black lines on white) and keep it for the whole section; make the two growth stages for its first two frames.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the main image input, the section's crack map as the second, and the earlier frames that some shards reflect as extra inputs.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the crack map or the style rules broke — regenerate those frames only.
The final video must feel like THE SCENE LIVING ON IN A SHATTERED MIRROR: locked straight cracks, misaligned reflected shards, 12 frames per second.
The image should deliberately contain:
* a crushed white impact
* straight radial and ring cracks
* tilted, misaligned shard reflections
* a few time-lagged shards
* a few missing shards with dark backing
* dark seams with bright glass edges
* a drifting glint.
Avoid polished digital perfection.
```
