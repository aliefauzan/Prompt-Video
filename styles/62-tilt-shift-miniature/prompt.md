# 62 — Tilt-Shift Miniature

**Look:** The real footage stays real, but it reads as a tabletop model. One thin horizontal band across the faces is razor sharp. Everything above and below it melts into heavy lens blur, the people's own hair, chests and hands included. Colours go candy-bright and contrasty, as if the people and the room were painted plastic toys photographed with a macro lens.

**Also called / where it trends:** "tilt-shift", "miniature effect", "fake miniature", "toy town effect", "diorama effect", "tiny world", 移轴摄影 / 微缩 (Bilibili). A long-running TikTok and YouTube tutorial staple (CapCut "Tilt-Shift Lens", DaVinci and After Effects lens-blur tutorials), #tiltshift on Instagram (about 2.5M reels), Pinterest boards and Vimeo staff-pick timelapses. It works best from a high angle, so creators look down on streets, trains and crowds.

**References:**
- https://www.tiktok.com/search?q=tilt%20shift%20miniature%20effect%20video (screenshot `refs/ref_1.png`): TikTok search grid of tilt-shift tutorials and results, from the discovery sweep. Top posts: https://www.tiktok.com/@midioin/video/7356953975456861445 (389.9K likes, a gas station turned into a toy set), https://www.tiktok.com/@antonio_pics_/video/7296333954616003848, https://www.tiktok.com/@the.dailyshort25/video/7664563122413374753.
- https://petapixel.com/2017/01/24/tutorial-fake-tilt-shift-look-post-miniaturize-world/ (screenshot `refs/ref_2.png`): PetaPixel, how to fake the tilt-shift look in post. It covers a gradient-mapped lens blur, a sharp band, more saturation and contrast, and a high viewpoint.
- Bilibili 移轴摄影 微缩 video covers, av116938671916661, av1750216414, av1134010449274844 (screenshot `refs/ref_3.png`, from the discovery sweep).
- https://www.youtube.com/watch?v=vY_0etcrwA0 and https://www.youtube.com/watch?v=L5H0vQwYuLw: YouTube tilt-shift miniature tutorials (discovery sweep).
- https://www.youtube.com/watch?v=y5kGht3azTQ: "Make ANYTHING tiny!" After Effects tilt-shift tutorial. It drives Camera Lens Blur from a gradient blur map, then adds Vibrance "to play up the artificial vibe".
- https://www.pinterest.com/search/pins/?q=tilt%20shift%20miniature and https://www.instagram.com/popular/tilt-shift/: Pinterest and Instagram galleries of the look.
- https://vimeo.com/channels/293484: Vimeo tilt-shift channel (timelapse miniatures).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). The masks place a horizontal focus band across the faces, smoothed over the whole clip so it glides and never jumps. A disc lens blur in linear light ramps up with distance from the band, by vertical position only, not by depth. Toy colour comes from a Lab chroma boost with skin held back, an S-curve and a high-key lift. A light bilateral "plastic" smoothing and sharpening keep the band crisp. A mild keystone fakes a camera tilted down at a tabletop. There is a light vignette and no grain.

## Prompt

```text
I'm uploading one video clip. Convert it into a TILT-SHIFT MINIATURE frame-by-frame animation: every frame should look like the real scene was shrunk into a tiny tabletop model and photographed through a tilted macro lens, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Tilt-shift miniature photograph, fake miniature effect, macro lens with a tilted plane of focus, toy town diorama look.
Transform the footage into a miniature frame built from:
* ONE thin HORIZONTAL band of razor-sharp focus
* heavy, creamy LENS BLUR above the band
* heavy, creamy LENS BLUR below the band
* blur that grows SMOOTHLY with distance from the band
* blur set by HEIGHT IN THE FRAME, not by depth
* candy-bright, SATURATED colour
* punchy contrast and a bright, sunny, high-key exposure
* clean, slightly PLASTIC, toy-like surfaces
* crisp, model-like edges inside the band
* a slight HIGH-ANGLE, looking-down-at-a-table feel
* a light vignette
* NO grain
The result should feel like someone:
BUILT THE ROOM AND THE PEOPLE AS A TABLETOP MODEL
→ PAINTED EVERYTHING IN GLOSSY TOY COLOURS
→ LIT IT LIKE A SUNNY AFTERNOON
→ PUT A MACRO LENS ON A TILT-SHIFT ADAPTER
→ TILTED THE PLANE OF FOCUS ACROSS THE FACES
→ SHOT IT FRAME-BY-FRAME.
CHARACTER — REAL, BUT TOY-SIZED
The people stay PHOTOGRAPHIC: their real faces, filmed, not redrawn.
They should read as tiny figures in a model only because of focus, colour and angle.
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
Do NOT turn them into plastic figurines, LEGO, clay or 3D renders.
Do NOT shrink or reshape heads or bodies.
THE FOCUS BAND
* The band is a horizontal strip across the frame, about one tenth of the frame height.
* Put it across the FACES. When faces sit at different heights, centre it on the faces and accept that a lower or higher face is a little soft.
* The band moves only slowly and smoothly with the faces, like a focus puller following them; never jump between frames.
* Inside the band: maximum sharpness, fine detail in eyes, glasses and hair.
* Just outside the band: soft. Hair tops, foreheads above the band, chests, hands and legs below it get softer and softer.
* Top edge of the frame and bottom edge of the frame: fully melted, like an out-of-focus tabletop and backdrop.
* People are blurred by HEIGHT exactly like the room. A hand below the band is soft even if it is near the camera.
LENS BLUR
* Real lens blur (disc bokeh), not a smeared Gaussian.
* Bright points bloom into soft round discs.
* No double edges, no cut-out halos around people.
* Blur strength rises gradually; there is no visible line where the band ends.
COLOUR — TOY PAINT
* Saturation clearly boosted: greens, blues, pinks, yellows and browns look like fresh model paint.
* Skin stays natural skin, warm and healthy, just a little brighter. Never orange, never red.
* Whites stay clean and bright; walls and windows go slightly minty or sky-blue.
* Strong S-curve contrast, bright overall, shadows still open.
* No colour wash, no tint over the whole frame.
CAMERA ANGLE
* The look sells best from above. Where possible, let the frame feel like the camera looks down a little at a table: the top of the frame slightly further away and smaller, the bottom slightly closer.
* Keep this subtle and keep every person's pose, proportions and position.
BACKGROUND
* The room stays the same room, same layout.
* It becomes model scenery: plants like model trees, the window like a lit backdrop, the screen like a tiny printed card.
* Do not add or remove objects.
PALETTE
Model-paint greens, sky blue, minty white, sunny yellow, cherry red accents, warm wood brown, natural skin.
Do NOT add neon, purple or teal-orange grading.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand and is blurred or sharp by its height in the frame, like everything else.
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
The focus band follows the faces smoothly.
NO focus band frozen in place while the faces move away.
NO random jumps in blur strength between frames.
FRAME-TO-FRAME STABILITY
THIS IS CRITICAL.
A miniature looks still and clean, so very little should "boil".
Allow between consecutive frames:
* the focus band to drift smoothly with the faces
* tiny natural changes as people move
Keep FIXED:
* the band width and blur strength
* the colour grade (no saturation pumping)
* the camera angle feel
* the vignette
DO NOT
Do NOT blur by depth like a portrait-mode phone photo (sharp people, blurred room).
Do NOT blur in a circle or radial pattern.
Do NOT leave the top or bottom of the frame sharp.
Do NOT add grain, scratches or film damage.
Do NOT make the people into toys, figurines, clay or plastic models.
Do NOT turn skin orange or red.
Do NOT make it look like a cheap blur filter with a hard edge.
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
* NO blur, tilt-shift or focus band
* NO saturation boost
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
Do NOT begin the tilt-shift miniature transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – TILT-SHIFT MINIATURE STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me where the focus band will sit in the first, middle and last frames (which faces it crosses), and how it will move between them.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME band width, blur strength and colour on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, band position or colour consistency broke — regenerate those frames only.
The final video must feel like A REAL ROOM SHRUNK INTO A TOY MODEL: one sharp band across the faces, everything above and below melted, candy colours, 12 frames per second.
The image should deliberately contain:
* a thin horizontal band of sharp focus across the faces
* heavy lens blur above and below it, on the people too
* saturated toy-paint colour
* bright, contrasty, sunny light
* a slight looking-down feel.
Avoid flat, evenly focused video.
```
