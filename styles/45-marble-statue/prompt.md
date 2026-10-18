# 45 — Marble Statue

**Look:** Every person becomes a carved, polished white marble statue that still moves. Faces, hair and clothes keep their shapes as smooth carved stone, with blank, pupil-less eyes like classical busts. A soft gallery skylight from above shows the form. There is a faint sheen on the high points, light passing just under the surface, and darker crevices. Thin grey veins run through the stone and stay fixed to the body as it moves. The room stays real but dimmed, cooled and desaturated like a museum hall. The first half is Carrara (white, soft grey veins) and the second half is Calacatta (brighter white, darker veins with gold seams).

**Also called / where it trends:** "marble statue effect", "marble statue filter", "turn into a statue", "AI statue", "Greek statue edit", "marble bust trend", "stone statue transformation". It trends as the TikTok marble statue effect (posts at 170–210K views). Higgsfield ships it as the **Marble** preset in Mixed Media, Melies lists it among its viral looks, and statue generators sell it as a one-click effect.

**References:**
- https://melies.co/cinematic-techniques/viral-looks (`refs/ref_1.png`): Melies "viral looks" page, Marble entry. Source of the core rule: the person rendered as polished carved marble that keeps moving.
- https://www.tiktok.com/discover/marble-statue-effect (`refs/ref_2.png`): TikTok discover page "Marble Statue Effect" (screenshot cropped to the post grid). Posts on it:
  - https://www.tiktok.com/@neural.max/video/7323190055848185094: @neural.max, 174.8K views.
  - https://www.tiktok.com/@griggen/video/7486495110197218582: @griggen, 210.4K views.
  - https://www.tiktok.com/@bradthenewsguy/video/7454431669274234158: @bradthenewsguy.
  - https://www.tiktok.com/@belyplantillas/video/7594123019648290066: @belyplantillas (template).
  - https://www.tiktok.com/@cuzzin_al/video/7658303486865542414: @cuzzin_al.
- https://higgsfield.ai/mixed-media: Higgsfield Mixed Media preset list, which includes "Marble".
- https://cliptrend.ai/ai-video-effects/ai-statue-generator: AI statue video effect page.
- https://contra.com/community/kTmoYHX0-i-built-an-ai-video-transform: creator write-up of an AI "person to statue" video transform.
- https://alici.ai/formulas/media/historyrevivedofficial/6c653ed9-d963-5894-aecf-9e79d6650250-roman-emperors-marble-bust-to-human-revival: @historyrevivedofficial, marble bust ↔ human formula (the reverse direction of the same trend).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation made with `render.py` (numpy + OpenCV). The carved form comes from the frame's luminance. Printed cloth stripes are removed with a vertical-line morphological opening, then the result is bilateral-smoothed, CLAHE'd and its darks lifted. A dome normal map from the matte is lit by a soft skylight, with a specular sheen, subsurface blur and ambient occlusion on top. Veins are a procedural turbulence field held in texture coordinates. Those coordinates are carried along by smoothed (near-rigid) Farneback optical flow, so the stone pattern rides on the bodies instead of boiling. The room is desaturated, dimmed and cooled, with a contact shadow. The first half is Carrara and the second half is Calacatta with gold veins. Frames whose matte breaks under motion blur (023, 068) borrow the area that both neighbouring mattes agree on.

## Prompt

```text
I'm uploading one video clip. Convert it into a 12 FPS LIVING MARBLE STATUE frame-by-frame animation, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
Seedream works here because each frame is a material change of the same source frame; the previous styled frame keeps the veins in place.
CORE VISUAL STYLE
Every person becomes a polished white marble statue that moves:
* skin, hair, clothes and accessories all carved from ONE block of white marble
* smooth carved surfaces with crisp chiselled edges at the eyes, lips, hairline and folds
* blank, pupil-less eyes like a classical bust
* hair as carved locks and grooves, not strands
* clothes as carved drapery: folds stay, prints and colours go
* thin grey veins running through the stone
* a soft gallery skylight from above-left
* a faint polished sheen on the high points
* light glowing just under the surface (marble translucency)
* darker crevices where the forms meet
* the room kept, but dimmed and cooled like a museum hall
It should look like the TikTok marble statue effect and the Higgsfield "Marble" preset.
The result should feel like someone:
CARVED EVERY PERSON IN THE SHOT FROM WHITE MARBLE
→ POLISHED THE STONE
→ STOOD THE STATUES IN A DIM GALLERY UNDER A SKYLIGHT
→ BROUGHT THEM TO LIFE SO THEY MOVE EXACTLY AS FILMED
→ SHOT IT AT 12 FRAMES PER SECOND
→ ANIMATED IT FRAME-BY-FRAME.
PALETTE RULES
The stone is warm white to cool white (#EDEFF0 to #F4F2EE).
Shadows on the stone are soft grey, never black.
Veins are mid to dark grey (#5A5E62 to #84888C), with soft edges.
In the second half, a few thin gold veins (#C89E5A) run through the stone.
No skin tones, no hair colour and no clothing colour remain on the people.
The room keeps only about 30% of its colour, at half brightness, slightly cool.
CHARACTER — CARVED, STILL RECOGNIZABLE
Preserve the person's exact:
* identity
* face shape
* expression
* hairstyle (as carved stone)
* clothing shape and folds (as carved stone)
* glasses (as carved stone frames)
* pose
* body proportions
* movement
* hand position
* interaction with objects
The statue must be clearly the same person.
Do NOT make them a generic Greek god.
Do NOT add a beard, laurel wreath, toga or plinth.
STONE SURFACE
The surface is smooth and polished, not rough or sandy.
Chisel detail is kept only where the face and body have real form: eyes, nose, lips, ears, collar, folds.
Printed patterns on clothes (stripes, batik, logos) are NOT carved; the cloth is plain stone.
VEINS
Veins are long, soft, branching lines that run in one main diagonal direction, with a second, fainter family crossing them.
They are sparse: most of the stone is clean white.
Veins belong to the STONE, not to the frame: they move with the body.
Do NOT draw veins as map borders, cracks or scribbles.
BACKGROUND
Keep the real room: same walls, windows, screens and furniture.
Desaturate it, dim it to about half brightness, cool it slightly, and darken it toward the floor.
Add a soft contact shadow where the statues meet the room.
Do NOT turn the room into marble.
SECTIONS
Split the clip into 2 halves:
* First half, CARRARA: white stone, soft grey veins.
* Second half, CALACATTA: brighter white stone, darker, bolder veins, plus thin gold veins.
FRAME-TO-FRAME BEHAVIOUR (BOIL RULES)
THIS IS CRITICAL.
The marble is ONE solid material on each body.
Veins stay locked to the same place on the body from frame to frame, moving only as the body moves.
Do NOT generate a new vein pattern every frame.
Allow between consecutive frames:
* the sheen to slide over the stone as the body turns
* very fine grain to change
Keep FIXED:
* the skylight direction
* the stone colour within a section
* the vein layout on each body
OBJECT CONTINUITY
If the character holds or touches an object (phone, cup, bag, microphone), it is carved from the same marble and stays in the hand.
Do NOT drop it.
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
Every statue must match the source frame exactly in position, pose and timing.
Do NOT invent motion that is not in the footage.
DO NOT
Do NOT keep any skin, hair or clothing colour on the people.
Do NOT carve clothing prints, stripes or logos.
Do NOT make the stone grey, dirty, cracked or broken.
Do NOT add pupils or painted eyes.
Do NOT add pedestals, plinths, togas, wreaths or museum labels.
Do NOT turn the background into marble or a white void.
Do NOT let the veins boil, swim or redraw between frames.
Do NOT redraw the people as a different statue.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing shape.
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
* NO marble
* NO veins
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
Do NOT begin the marble-statue transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – MARBLE STATUE STYLING (AFTER MY CONFIRMATION ONLY)
First, plan the sections and list them for me: frame range, marble type, stone colour and vein colour for each half.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame, in playback order.
Give Seedream the current extracted frame as the main image input, plus the previous STYLED frame as a second input so the veins stay on the same places of the body.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, vein lock or the style rules broke — regenerate those frames only.
The final video must feel like LIVING MARBLE STATUES IN A GALLERY: the same people carved in polished white stone, moving exactly as filmed, 12 frames per second.
The image should deliberately contain:
* polished white marble people
* blank carved eyes
* carved hair and drapery
* sparse grey veins locked to the body
* a soft overhead skylight and sheen
* soft translucency and crevice shadows
* a dim, cool, desaturated room.
Avoid polished digital perfection.
```
