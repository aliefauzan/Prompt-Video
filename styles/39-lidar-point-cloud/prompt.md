# 39 — LiDAR Point Cloud

**Look:** the clip rebuilt as a live 3D LiDAR scan floating in black space. People become dense clouds of tiny glowing points, the room becomes a sparser far-plane of points, and a slow virtual-camera orbit adds parallax. Points are coloured by depth (TURBO rainbow: near = red/yellow, far = blue), with a true-colour RGB scan section and an ice-blue INTENSITY "ghost scan" section. Depth-slice contour bands ripple across the bodies. A bright scan line sweeps top to bottom every 2.5 s and lights the points it passes. Points flicker and drop out, and thin missed-beam rows appear. A faint floor grid and a minimal point-cloud viewer HUD (mode, point count, scan %, depth colour bar, XYZ gizmo) sit on top.

**Also called / where it trends:** "LiDAR effect", "point cloud edit", "3D scan effect", "scanner sombre look", "ghost scan", "volumetric capture". Seen in music videos (Radiohead "House of Cards", Unreal-Engine LiDAR videos, Rhizomatiks x Perfume volumetric shows), iPhone LiDAR-scan TikToks, After Effects / Blender point-cloud tutorials, tech-brand and fashion visuals, and club / festival LED content.

**References:**
- https://www.pinterest.com/search/pins/?q=lidar%20point%20cloud%20scan%20aesthetic%20person (screenshot `refs/ref_1.png`): point-cloud portraits, depth-coloured scans, ghost-blue scan bodies.
- https://www.aaronkoblin.com/work/rh/index.html (screenshot `refs/ref_2.png`): Radiohead "House of Cards" (Aaron Koblin), the canonical LiDAR music video with point-cloud faces and dropout.
- https://mondniles.com/en/tutorials/lidar-effect-point-cloud-scan: LiDAR point-cloud effect tutorial covering depth, point density, scan sweep, and the "Ghost Scan" and "Blueprint" presets.
- https://nofilmschool.com/music-video-lidar-point-clouds-unreal-engine: a music video built from LiDAR point clouds in Unreal Engine.
- https://rhizomatiks.com/en/work/perfume-25th-and-20th-anniversary-live-performance/: Rhizomatiks x Perfume, volumetric point-cloud performers.
- https://yunussezer.com/work/olexesh: a point-cloud music video (Olexesh).
- https://github.com/potree/potree: a WebGL point-cloud viewer, the reference for the viewer HUD, EDL glow and depth colouring.
- https://github.com/leonhardrobin/LiDAR-scanner-effect-unity: a "Scanner Sombre"-style LiDAR scanner effect.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (full clip). Local approximation rendered with `render.py` (numpy + OpenCV + PIL + person masks, fake depth from the mattes); the 6 sheet frames are in `frames/`. Distinct from 27 Rutt-Etra (that one uses horizontal scanlines displaced by brightness; this one is discrete 3D points with depth colour and parallax).

## Prompt

```text
I'm uploading one video clip. Convert it into a LIDAR POINT-CLOUD 3D SCAN, frame by frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage so it looks genuinely CAPTURED BY A LIDAR SCANNER AND SHOWN IN A POINT-CLOUD VIEWER, built from:
* tens of thousands of tiny glowing POINTS on pure black
* people as DENSE point clouds, the room as a SPARSER far-plane of points
* NO solid surfaces, NO polygons, NO filled shapes, only dots
* points coloured by DEPTH (near = red / orange / yellow, mid = green / cyan, far = blue / indigo)
* faint depth-slice contour bands rippling across bodies
* a bright horizontal SCAN SWEEP line that travels top to bottom and lights up the points it passes
* points flickering, thinning and dropping out
* thin full-width "missed beam" rows where a scan line returned nothing
* a slight 3D orbit of the virtual camera (parallax between people and room)
* soft glow around dense point clusters
* a faint perspective floor grid
* a minimal point-cloud-viewer HUD
* one true-colour RGB scan section and one ice-blue INTENSITY ghost-scan section
The result should feel like someone:
SCANNED THE ROOM AND THE PEOPLE WITH A LIDAR RIG
→ TURNED EVERY SURFACE INTO MEASURED 3D POINTS
→ THREW AWAY THE SURFACES
→ LOADED THE CLOUD INTO A VIEWER ON A BLACK BACKGROUND
→ SLOWLY ORBITED THE CAMERA
→ RECORDED IT FRAME BY FRAME.
CHARACTER — POINT-CLOUD BODY
The MAIN HUMAN SUBJECTS become dense point clouds that still read as the exact same people.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing silhouette
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the characters.
Do NOT turn them into mannequins, wireframes or solid holograms.
The face must be built from the densest points:
* eyes, brows, nose, mouth and jaw readable through point brightness and density
* bright areas (skin highlights, light fabric) = brighter points
* dark areas (hair, dark fabric) = dimmer, sparser points
* the edge of each body slightly sparser than the centre (surfaces turning away from the scanner)
* clothing stripes and patterns may show faintly through point brightness
THE ROOM — FAR PLANE
The room keeps its exact layout but becomes a sparse cloud:
* walls, window, shelves, plants, chairs and screens as thinner, dimmer points
* coloured by depth as further away (blue / indigo)
* large empty black gaps are fine; the room must not become a solid image
* a faint perspective floor grid under everything
DEPTH AND PARALLAX
* people closer to the camera are warmer in the depth palette than people further back
* bodies bulge toward the camera (chest and face nearer than the outline)
* the virtual camera slowly orbits a few degrees, so near points shift more than far points
* the orbit is smooth and slow, never jumpy
SCAN SWEEP
* a thin bright horizontal line sweeps top to bottom about every 2.5 seconds
* points it passes flash brighter, then fade back over a few frames
* the HUD shows scan progress 0-100%
PALETTE RULES
PRIMARY — DEPTH (TURBO-style):
near red → orange → yellow → green → cyan → blue → indigo far, on pure black.
SECONDARY — RGB SCAN (one section): each point takes the true colour of the surface it sampled, still on black.
THIRD — INTENSITY / ICE (one section): monochrome ice-blue to white points, ghost-scan look.
Switch palette only at section boundaries (about every 4-5 seconds), never frame to frame.
Never mix palettes inside one frame (except the HUD colour bar).
The background is always pure black.
HUD OVERLAY
Thin, minimal viewer HUD in small sans/mono type:
* top-left: "LIDAR SCAN / DEPTH" (or "/ RGB", "/ INTENSITY")
* under it: "PTS 182,406   FRAME 049   63%" (point count, frame number, scan progress)
* right edge: vertical depth colour bar labelled "0.6 m" and "6.0 m" (depth mode only)
* bottom-right: small XYZ axis gizmo (X red, Y green, Z blue)
HUD text must be crisp and legible, in fixed positions.
LAYER ORDER
A typical frame reads:
PURE BLACK
↓
FAINT FLOOR GRID
↓
SPARSE ROOM POINTS (far, blue)
↓
DENSE PEOPLE POINTS (near, warm) + CONTOUR BANDS
↓
SCAN SWEEP LINE + LIT POINTS
↓
SOFT GLOW
↓
HUD.
OBJECT CONTINUITY
IMPORTANT:
If a character interacts with an object, scan that object as points too.
Examples:
* phone
* cup
* chair
* glasses (frames as a thin line of points)
* bag, headphones
If the object is essential to the action, keep it clearly visible.
Do NOT accidentally remove it.
CHARACTER CONTINUITY LOCK
The SAME people must remain recognisable in every frame.
Never change:
* identity
* facial structure
* hairstyle
* clothing silhouette
* accessories
* body proportions
* anatomy
* expression
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.
PERFECT MOTION TRACKING
The underlying human movement must stay exactly faithful to the source footage.
The POINTS flicker.
The HUMAN MOTION does NOT change.
If the head moves:
the head's points move with it.
If a hand moves:
the hand's points follow, with no trail.
NO ghost point clouds from previous frames.
NO points smeared into streaks.
NO frozen HUD numbers.
FRAME-TO-FRAME SCAN LIFE
THIS IS CRITICAL.
Every frame should feel like a new live scan pass.
Allow:
* about 10% of points to flicker on / off every frame
* point count to change slightly every frame
* 1-3 thin missed-beam rows in different places each frame
* the scan sweep to advance steadily
* the virtual camera to keep orbiting smoothly
Keep the sampling pattern of each surface broadly STABLE (the same points mostly stay in place), so it reads as a scan and not as TV static.
Do NOT let faces dissolve into noise.
Do NOT let the palette jump between frames.
DO NOT
Do NOT render solid surfaces, smooth skin or a normal photo under the points.
Do NOT use horizontal displaced scanlines (Rutt-Etra) instead of points.
Do NOT draw wireframes, polygons or meshes.
Do NOT add a coloured or gradient background.
Do NOT add sci-fi hologram flicker, neon outlines or glitch blocks.
Do NOT replace any face.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing shape.
Do NOT add fake brand logos or garbled HUD text.
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
* NO point cloud
* NO depth colouring
* NO scan sweep
* NO HUD overlay
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
Do NOT begin the LiDAR / point-cloud transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – LIDAR POINT-CLOUD STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Lock the palette per section exactly as planned (DEPTH → RGB SCAN → INTENSITY / ICE → DEPTH, switching only at section boundaries).
Keep the HUD layout, font and positions identical in every frame; only the point count, frame number, scan % and mode name change.
Keep the scan sweep timing continuous across all frames (one top-to-bottom pass every 30 frames).
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like a REAL LIDAR CAPTURE PLAYED IN A POINT-CLOUD VIEWER: dots only, depth-coloured, orbiting, sweeping and dropping out.
The image should deliberately contain:
* discrete points on pure black
* depth colouring
* parallax
* scan sweep
* dropout and missed-beam rows
* soft point glow
* a crisp viewer HUD.
Avoid a photo with a dot filter on top.
```
