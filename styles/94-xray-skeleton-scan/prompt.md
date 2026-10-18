# 94 — X-Ray Skeleton Scan

**Look:** The clip becomes a glowing medical radiograph. The room turns into a dark navy negative with faint cyan edges. Each person is a translucent blue-white body with a bright rim, and their skeleton shows through, bright and moving with them: skull with dark eye sockets and teeth, spine, rib cage, collarbones, arm bones, finger bones, pelvis. A cyan scanner bar sweeps down the frame, and the picture flashes brighter at the start of each sweep.

**Also called / where it trends:** "x-ray effect", "x-ray filter", "x-ray flash effect" / "x-ray flash transition", "skeleton filter", "x-ray scan", "BONE edit". A long-running TikTok and CapCut effect (CapCut template "X-ray effect", many "how to do the x-ray effect" tutorials), now also sold as a one-click AI video preset (Artlist "AI X-Ray Filter", Higgsfield "X-Ray" motion, Kapwing "X-Ray Scan AI Video Effect", Magic Hour "X-Ray" template, Komiko "Convert Skeleton AI"). Creators cut to it on the beat drop, for Halloween, gym and dance edits.

**References:**
- TikTok search "x ray filter video effect" (screenshot `refs/ref_1.png`, from the discovery sweep): x-ray flash transitions, glowing cyan skeleton portraits and "BONE" edits. Posts noted: https://www.tiktok.com/@jerrzyo/video/7666624228719987988, https://www.tiktok.com/@griggen/video/7672078631337823510, https://www.tiktok.com/@itsnotoriously/video/7543845755027574046
- YouTube tutorials: https://www.youtube.com/watch?v=Qd2FQau3owQ, https://www.youtube.com/watch?v=ZVA2Ek20hAo, https://www.youtube.com/watch?v=EbzADoxUttU ("Mind-Blowing X-Ray Effect Tutorial Using CapCut"), https://www.youtube.com/watch?v=agvOBOMyQ9E ("How to Create an X Ray Effect in CapCut")
- https://artlist.io/ai/presets/xray-filter (screenshot `refs/ref_2.png`): Artlist "AI X-Ray Filter". It rebuilds the subject as a skeletal scan that moves with them; the sample shows a blue-grey radiograph with skeleton, organs, translucent clothes and a vertical scan wipe.
- https://higgsfield.ai/motion/5819f36e-5b0a-44ca-800e-98e380266b2d: Higgsfield motion preset "X-Ray". Their summary: shows internal structure or bones through the subject.
- https://www.kapwing.com/kai/create/x-ray-scan-ai-video-effect: Kapwing "X-Ray Scan AI Video Effect".
- https://magichour.ai/templates/details/cmmj50kno0r6m290zt6h83lw3-x-ray: Magic Hour "X-Ray" image-to-video template.
- https://www.capcut.com/template-detail/X-ray-effect/7569478253195398405: CapCut "X-ray effect" template.
- https://www.tiktok.com/@tylersymonemedia/video/7252367516104723758: TikTok "X-Ray Video Editing Tutorial".
- https://www.pinterest.com/search/pins/?q=x-ray%20skeleton%20effect: Pinterest board of x-ray skeleton stills (black translucent body, white bones, blue glow).
- https://www.behance.net/search/projects?search=runway%20restyle: Behance "Day 8: Restyle video into Xray" (Runway restyle project).

How it differs from taken styles: **16 Thermal Camera** maps heat to a false-colour rainbow and shows no anatomy; **39 Lidar Point Cloud** turns surfaces into dots. This is a monochrome cyan radiograph: inverted negative, translucent flesh and bright bones inside the body.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). Apple Vision body, hand and face landmarks (`pose.swift` → `pose.json`) place a procedural skeleton for each person: skull built from the eye line, vertebrae from skull base to pelvis, eleven pairs of rib hoops, clavicles, scapulae, pelvis, humerus, radius + ulna, and finger bones from the hand joints (or a generic hand fan). Joints are averaged across ±2 frames and 1–2 frame detection gaps are bridged. The room is an inverted luminance + edge negative; flesh is a translucent body with a bright rim. A blue LUT, bloom, a scanner bar every 3 s with an exposure flash, radiograph grain, a vignette and a lead "R" marker finish it. The skeleton is a code-drawn diagram, so a real AI pass would give finer anatomy (organs, true skull shape).

## Prompt

```text
I'm uploading one video clip. Convert it into an X-RAY SKELETON SCAN frame-by-frame animation: every frame should look like a glowing medical radiograph of the scene, with each person's skeleton visible inside a translucent body, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Glowing x-ray radiograph, inverted negative, cyan-blue and white on near-black navy, translucent soft tissue, bright bones, medical scanner look.
Transform the footage into an x-ray scan built from:
* an INVERTED NEGATIVE image: dark where the photo was bright, bright where it was dense
* a NEAR-BLACK NAVY background
* the room as a faint CYAN EDGE negative (walls, window, furniture, screen just readable)
* each person as a TRANSLUCENT blue-white BODY with a brighter rim along their outline
* each person's SKELETON clearly visible inside the body, BRIGHT WHITE-CYAN
* SKULL with dark eye sockets, dark nasal hole, teeth rows and jaw
* SPINE as a column of separate vertebrae from skull base to pelvis
* RIB CAGE of curved rib hoops, collarbones, shoulder blades, sternum
* ARM BONES (humerus, radius + ulna) and FINGER BONES with joint gaps
* PELVIS and leg bones where the legs are in frame
* soft BLOOM around the bones
* fine radiograph FILM GRAIN
* a thin CYAN SCANNER BAR that sweeps from top to bottom
* a small lead "R" side marker in a corner, like a real radiograph
The result should feel like someone:
WALKED THE PEOPLE THROUGH A MEDICAL SCANNER
→ EXPOSED EACH FRAME ONTO X-RAY FILM
→ HUNG THE FILM ON A LIGHTBOX
→ SCANNED IT BLUE-WHITE
→ PLAYED THE STACK FRAME-BY-FRAME.
CHARACTER — TRANSLUCENT BODY, SAME PERSON
The people stay in exactly the same place, size and pose.
Preserve the person's exact:
* identity
* face shape and position
* expression (readable faintly through the skull)
* hairstyle (as a faint soft halo)
* glasses (metal frames show bright, like metal on an x-ray)
* clothing (only as a faint translucent trace)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
The body outline must match the source frame exactly.
Do NOT redraw the character as a cartoon skeleton costume.
Do NOT replace the person with a stock skeleton.
Do NOT show a skeleton outside the body outline.
SKELETON RULES
* The skeleton follows the person's real pose: the skull sits inside the head, the spine runs down the body's centre, the arm bones run along the real arms, the finger bones follow the real fingers.
* Skull size and tilt match the face: eye sockets sit where the eyes are, the jaw where the jaw is.
* Bones are bright with an even brighter outer edge (cortex) and a slightly textured inside.
* Joints show as small dark gaps between bones.
* Thin flat bones (skull vault, shoulder blades, pelvis) are dimmer than long bones.
* Body parts outside the frame stay outside; do not invent legs that are not visible.
* Every person in the room gets their own skeleton, including people partly hidden behind others.
* People on the TV / video-call screen stay as flat screen picture (no skeleton).
X-RAY TONE + COLOUR
* Background: near-black navy.
* Room: dim inverted negative with thin cyan edges.
* Soft tissue: translucent blue, brighter at the outline, darker in thick areas.
* Bones: white with a cyan glow.
* Cavities (eye sockets, nasal hole, gaps between teeth): dark.
* Strong contrast, but bones never clip into flat white blobs.
SCANNER BAR + FLASH
* A thin bright cyan line sweeps from top to bottom about every 3 seconds.
* Just behind the line, the image is slightly brighter, and bones inside the band glow more.
* At the start of each sweep the whole frame flashes brighter for 1–2 frames, like an exposure.
* No other overlays, no UI, no text except the small "R" marker.
PALETTE
Near-black navy, deep blue, cyan-blue, pale ice blue, white.
Do NOT add green, orange, red, rainbow or heat-map colours.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand; dense objects (metal, phone) read brighter, soft objects fainter.
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
The body outline and skeleton must match the source frame exactly.
The skeleton moves with the person: when they turn their head, the skull turns; when they raise a hand, the finger bones rise.
NO frozen skeleton from a previous frame.
NO skeleton sliding or lagging behind the body.
NO skeleton that pops in and out between frames.
FRAME-TO-FRAME SCAN LIFE
THIS IS CRITICAL.
It must feel like a live scanner feed, not a still filter.
Allow between consecutive frames:
* film grain to change every frame
* the scanner bar to move down steadily
* bone glow to shimmer slightly (±5%)
Keep FIXED:
* the bone layout of each person (same skull, same ribs, frame to frame)
* the blue colour scale
* the room negative
DO NOT
Do NOT use a false-colour heat map (that is a thermal camera, not an x-ray).
Do NOT turn surfaces into points or wireframes (that is lidar).
Do NOT just invert the frame and tint it blue without a skeleton.
Do NOT paste a static skeleton overlay that ignores the pose.
Do NOT make it gory, bloody or horror.
Do NOT show organs as coloured shapes.
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
* NO inversion or colour change
* NO skeleton
* NO scanner bar, flash or grain
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
Do NOT begin the x-ray transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – X-RAY SKELETON STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me how many people you will give skeletons to, which frames have hands or faces close to the lens, and which frames the scanner flash lands on.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the body outlines and poses are exactly that frame.
Use the previous styled frame as a second reference so each person's skeleton keeps the same bone layout.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the skeleton's position or the colour scale broke — regenerate those frames only.
The final video must feel like A LIVE X-RAY SCAN OF THE SCENE: translucent glowing bodies, bright moving skeletons, navy negative room, a cyan scanner sweep, 12 frames per second.
The image should deliberately contain:
* an inverted navy-and-cyan negative
* translucent bodies with bright rims
* a full, pose-matched skeleton inside every person
* dark eye sockets, teeth and joint gaps
* bloom, radiograph grain and a scanner bar.
Avoid a flat blue tint.
```
