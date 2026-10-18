# 16 — Thermal Camera

**Look:** the clip as seen through a handheld infrared camera: room collapses to cold violet-black, people glow orange-yellow-white in an IRON palette (with RAINBOW and WHITE-HOT sections), soft low-res sensor bloom, faint visible-light edge detail on faces, and a live HUD (spot meter, colour scale bar, °C readouts, person boxes, REC). Sensor noise and readouts flicker every frame.

**Also called / where it trends:** "thermal camera filter", "heat vision edit", "thermal cam trend", "infrared heat map effect", "FLIR edit" — TikTok/CapCut thermal filters and effect templates, IG Reels, music videos (Tinashe "Getting No Sleep" shot with a dual thermal + ALEXA rig, Young Fathers, The Horrors "Ghost", Tycho "See"), club-flyer / poster design ("Thermal Heat" aesthetic).

**References:**
- https://www.pinterest.com/search/pins/?q=thermal%20camera%20aesthetic%20portrait%20heat%20map — screenshot `refs/ref_1.png`: iron/rainbow portraits, HUD boxes, scale bars, crowd heat maps
- https://www.omoro.io/styles/thermal-heat — "Thermal Heat" aesthetic record: thermal palettes in club/music editorial, Richard Mosse *Incoming*
- https://www.instagram.com/reel/DGWdERHvMxj/ — Frame Set: dual thermal + ALEXA rig for Tinashe "Getting No Sleep"
- https://topa.de/thermografie/thermografie-in-musikvideos-waermebildkameras-als-visuelle-kunstform/ — thermography in music videos (2026)
- https://lbbonline.com/news/young-fathers-heat-things-up-using-military-thermal-camera — Young Fathers video shot on a military thermal camera
- https://joepicard.com/tycho-see-music-video — Tycho "See", thermal music video
- https://effect.app/effects/thermal-camera — false-colour thermal video filter (what the consumer effect looks like)
- https://magichour.ai/products/color-grader/thermal-camera — thermal colour-grade preset (iron / rainbow palettes)

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation rendered with `render.py` (numpy + OpenCV + person masks); 17 frames in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a THERMAL CAMERA / INFRARED HEAT-MAP frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into footage that looks genuinely SHOT ON A HANDHELD THERMAL CAMERA, built from:
* false-colour IRON palette (black → indigo → violet → magenta → orange → yellow → white)
* people glowing HOT against a COLD room
* faces and hands hottest
* clothing slightly cooler than skin
* hair cooler than skin
* cold violet / indigo / near-black environment
* soft low-resolution sensor look
* thermal bloom around the hottest areas
* warm "air halo" around bodies
* faint visible-light edge detail (MSX-style) so faces stay readable
* fixed-pattern sensor noise and column stripes
* a live measurement HUD with temperature readouts
* occasional RAINBOW palette and WHITE-HOT palette sections
The result should feel like someone:
POINTED AN INFRARED CAMERA AT THE SCENE
→ LET IT READ EVERY BODY'S HEAT
→ MAPPED TEMPERATURE TO A FALSE-COLOUR PALETTE
→ OVERLAID THE CAMERA'S LIVE HUD
→ RECORDED THE SCREEN
→ PLAYED IT BACK FRAME-BY-FRAME.
CHARACTER — HEAT SIGNATURE
The MAIN HUMAN SUBJECT becomes a glowing heat signature.
Preserve the person's exact:
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
Do NOT redraw the character.
Do NOT turn them into a cartoon, a ghost or a glowing silhouette with no features.
The person remains PHOTOGRAPHIC in shape and detail.
Only the COLOUR is replaced by temperature.
TEMPERATURE MAP OF THE BODY
Assign colour by plausible body heat, not by the original colours:
* face, neck, ears, hands, forearms → HOTTEST (yellow / white-yellow in iron, red in rainbow, white in white-hot)
* torso under clothing → hot (orange / yellow)
* sleeves, trousers, loose fabric → warm (orange / magenta)
* hair → cooler than skin (magenta / violet)
* glasses lenses → COLD (glass blocks infrared: dark violet / blue lenses)
* nose tip and hair ends → slightly cooler
Clothing PATTERNS (stripes, prints, batik) must mostly DISAPPEAR.
Thermal cameras see heat, not dye.
Only faint fabric folds and seams may remain.
Keep enough facial structure (eyes, brows, mouth, nostrils, jaw line) that the person stays recognizable.
Do NOT erase important facial features.
THE ROOM — COLD
The environment stays in the frame, in the exact same layout, but becomes COLD:
* walls, floor, furniture → deep indigo / violet / near-black
* windows → cold dark blue
* screens, monitors, lamps, ceiling lights → warm (magenta / orange) because electronics and bulbs emit heat
* plants → cool
* chairs → cool with faint warm seat where someone sat
Keep the room readable as soft shapes, not a black void.
LOW-RESOLUTION SENSOR LOOK
A real microbolometer is low resolution.
The heat image should be:
* softly blurred
* slightly blocky when you look closely
* smooth gradients between temperatures
* with a crisper visible-light edge overlay embossed on top (MSX style) so outlines and features stay sharp enough to read
It should NOT look like a sharp colour-graded photo with a gradient map.
THERMAL BLOOM AND HALO
Around hot bodies, the air reads slightly warmer:
* a soft warm halo 10–30 px around each person
* hottest spots (faces, hands) bloom slightly
* bloom is soft and heat-like, NOT neon glow lines
SENSOR NOISE
Include real sensor artifacts:
* fine temporal noise that changes every frame
* faint vertical fixed-pattern column stripes
* slight automatic-gain "breathing" (whole image brightness drifts very slightly)
* subtle vignetting
* occasional NUC / recalibration flicker (one frame slightly flatter), rare
PALETTE RULES
PRIMARY PALETTE — IRON:
BLACK / INDIGO / VIOLET (cold) → MAGENTA → ORANGE → YELLOW → WHITE (hot).
SECONDARY PALETTE — RAINBOW (for selected sections):
DARK BLUE → BLUE → CYAN → GREEN → YELLOW → ORANGE → RED → PALE PINK-WHITE (hottest).
THIRD PALETTE — WHITE-HOT (for one short section):
grayscale, BLACK = cold, WHITE = hot.
Use ONE palette per section.
Switch palette only on clear section changes (about every 2–3 seconds), never frame to frame.
Never mix palettes inside one frame (except the scale bar showing the active palette).
Do NOT keep any of the original natural colours (no real skin tones, no real clothing colours).
HUD OVERLAY
Overlay a clean camera HUD in white, thin sans/mono type:
* four corner brackets framing the image
* top-left: camera ID, band "LWIR 8–14µm", palette name, emissivity "E 0.98", running timecode
* top-right: red REC dot (blinking) + "REC"
* right edge: vertical COLOUR SCALE BAR of the active palette with max / min temperatures (e.g. 38.5 / 17.0 °C)
* centre: crosshair spot meter with live readout ("SP1 35.3°C")
* a small red triangle marking the hottest point with "MAX 37.1°C"
* thin green corner-bracket boxes around each person with a label ("HUMAN 36.8°C")
* bottom strip: "MIN / AVG / DIST / NUC OK" readouts
Numbers must be plausible body temperatures (skin 33–37.5 °C, room 17–24 °C).
HUD elements stay in fixed screen positions, except person boxes and the MAX marker, which follow the people.
HUD text must be crisp and legible, not melted AI lettering.
LAYER ORDER
A typical frame reads:
COLD ROOM (indigo / violet heat map)
↓
WARM AIR HALO AROUND BODIES
↓
HOT HUMAN HEAT SIGNATURE (palette-mapped)
↓
VISIBLE-LIGHT EDGE DETAIL (faint)
↓
SENSOR NOISE + VIGNETTE
↓
HUD (brackets, scale bar, readouts, person boxes).
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object in its correct thermal colour.
Examples:
* phone (warm screen, cool case)
* cup (hot if a hot drink)
* chair (cool)
* glasses (cold lenses)
* bag, headphones, microphone (cool to lukewarm)
If the object is essential to the person's action, keep it clearly visible.
Do NOT accidentally remove it.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame.
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
The underlying character movement must remain exactly faithful to the source footage.
The SENSOR flickers.
The HUMAN MOTION does NOT.
If the head moves:
the heat signature follows.
If the hand moves:
the hot hand follows, with no heat trail left behind.
If the body turns:
the temperature map updates (the cooler back of the head, the warmer face).
If the character interacts with an object:
the object moves exactly with the original action.
NO ghost heat silhouettes from previous frames.
NO delayed person boxes.
NO frozen readouts.
FRAME-TO-FRAME SENSOR LIFE
THIS IS CRITICAL.
Every frame should feel like a new live sensor readout.
Allow:
* sensor noise to change every frame
* temperature readouts to fluctuate by ±0.1–0.3 °C
* the MAX marker to hop to the current hottest point
* person boxes to jitter by 1–3 px
* REC dot to blink (on/off about twice per second)
* auto-gain to breathe very slightly
* the timecode to advance exactly with the frames
Do NOT let the palette mapping of the same body part jump wildly between frames.
The face that is yellow-white must stay yellow-white.
DO NOT
Do NOT keep natural colours anywhere in the image.
Do NOT make it a simple gradient-map filter over a sharp photo with all clothing patterns visible.
Do NOT make the background hot or the people cold.
Do NOT turn people into featureless blobs.
Do NOT replace the person's face.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing shape.
Do NOT add neon outlines, glow strokes or sci-fi holograms.
Do NOT add predator-style cloaking, X-ray skeletons or night-vision green.
Do NOT mix iron and rainbow in the same frame.
Do NOT add random garbled HUD text or fake brand logos.
Do NOT make it look like a clean modern colour grade.
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
* NO thermal palette
* NO HUD overlay
* NO heat map
* NO sensor noise
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
Do NOT begin the thermal / heat-map transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – THERMAL CAMERA STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Lock the palette per section exactly as planned (IRON → RAINBOW → IRON → WHITE-HOT → RAINBOW → IRON, switching only at section boundaries).
Keep HUD layout, fonts and positions identical in every frame; only the live numbers, REC blink, person boxes and MAX marker change.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like REAL INFRARED CAMERA FOOTAGE: hot bodies, cold room, soft sensor, live readouts.
The image should deliberately contain:
* low-resolution heat softness
* sensor noise
* column stripes
* auto-gain drift
* thermal bloom
* warm halos
* crisp HUD numbers that update every frame.
Avoid a polished colour-graded look.
```
