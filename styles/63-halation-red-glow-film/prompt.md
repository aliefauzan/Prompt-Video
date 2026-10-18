# 63 — Halation Red-Glow Film (CineStill 800T)

**Look:** The clip becomes a night frame shot on CineStill 800T. The room drops into a dim, cool, cyan-green tungsten-film darkness, and every light source and bright edge grows a red-orange halo. The window becomes a white-hot light box rimmed in red, and the white stripes on the shirt glow pink-red at their edges. Lifted film blacks and visible 800-speed grain sit on a full, unmasked modern frame.

**Also called / where it trends:** "halation", "CineStill look", "800T look", "red glow film", "halation filter", "film halation glow", "night film look". The look comes from CineStill 800T, Kodak Vision3 500T motion-picture stock with its anti-halation rem-jet layer removed. On TikTok and YouTube it is a top colour-grading tutorial (Dehancer, FilmConvert, DaVinci halation OFX, VSCO and Dazz presets), and photographers post #cinestill800t night-street shots on Instagram.

**References:**
- https://www.tiktok.com/search?q=cinestill%20halation%20glow%20film%20look%20video (screenshot `refs/ref_1.png`): TikTok search grid from the discovery sweep. Example posts: https://www.tiktok.com/@zac.freuden/video/7287478187209149703, https://www.tiktok.com/@vsco/video/7522923782730681655 (VSCO's halation filter), https://www.tiktok.com/@peace_gates/video/7237132869800430849.
- https://cinestillfilm.com/blogs/news/cinestill-film-stock-primer (screenshot `refs/ref_2.png`): CineStill's own guide to its stocks. It explains the "signature halation" as red blooming around in-focus, overexposed highlights, strongest in night scenes full of artificial lights.
- https://www.youtube.com/watch?v=vbO4nc4UBpU: YouTube halation glow tutorial (discovery sweep).
- https://thedarkroom.com/web-stories/what-is-halation/: The Darkroom lab explains halation, light bouncing back through the film base.
- https://emulsive.org/reviews/a-word-on-cinestill-800t-35mm-by-phil-harrison: EMULSIVE review of CineStill 800T, with tungsten balance, cyan shadows and red halos.
- https://www.japancamerahunter.com/2019/01/film-review-cinestill-film/: Japan Camera Hunter review, with night-street examples.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). The room drops about 1.5 stops while light sources hold their brightness. Shadows go cyan-green and the people (from the masks) stay warmer. Highlights from the original exposure are blurred at three radii, the bright core is subtracted so only a rim remains, and that halo is added in red-orange. There is a faint warm bloom, lifted film blacks, 800-speed grain that is new every frame and strongest in the shadows, a soft scan and a vignette. Unlike 54 Teal & Orange Anamorphic, it has no letterbox, no bokeh, no flares and no teal/orange split.

## Prompt

```text
I'm uploading one video clip. Convert it into a HALATION RED-GLOW FILM frame-by-frame animation: every frame should look like it was shot at night on CineStill 800T 35mm film, with red halos glowing around every highlight, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
35mm film photograph on CineStill 800T, tungsten-balanced motion-picture stock without rem-jet, night interior, strong red halation, visible film grain.
Transform the footage into a film frame built from:
* RED-ORANGE HALATION glowing around every highlight
* light sources (window, screen, lamps) as WHITE-HOT cores with a RED RIM
* bright edges (white stripes, skin highlights, hair sheen, glasses) with a thin red-pink glow
* a dim, moody NIGHT exposure: the room about one and a half stops darker
* a cool CYAN-GREEN tungsten-film cast in the shadows and walls
* warm but natural skin
* LIFTED, milky film blacks (never pure black)
* visible 800-SPEED GRAIN, stronger in the shadows
* soft film-scan sharpness
* a gentle vignette
* the full frame, no letterbox, no borders
The result should feel like someone:
SWITCHED OFF THE OVERHEAD LIGHTS
→ LOADED CINESTILL 800T INTO A 35MM CAMERA
→ SHOT THE PEOPLE AGAINST THE BRIGHT WINDOW AND SCREEN
→ LET THE HIGHLIGHTS BLEED RED THROUGH THE FILM BASE
→ SCANNED THE NEGATIVES WITH GRAIN INTACT
→ PLAYED THEM BACK FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, ON FILM
The people stay PHOTOGRAPHIC.
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
Do NOT turn them into a painting, cartoon or 3D render.
Do NOT beautify or re-sculpt faces.
HALATION — THE SIGNATURE
* Halation is a RED-ORANGE glow that sits AROUND bright areas, not on top of them.
* The core of a bright light stays white or warm white; the red is the RIM spreading outward.
* The bigger and brighter the light, the wider the halo (the window gets a wide glow, a small reflection gets a thin one).
* The red bleeds onto nearby darker areas: hair edges, shoulders and the wall next to the window turn red where they touch the light.
* Bright clothing (white stripes) gets a thin pink-red edge glow.
* Faces never turn red overall; only their brightest edges pick up a warm fringe.
* The red is a film red: scarlet to orange, never magenta, never pink neon.
NIGHT FILM GRADE
* Darker overall: the scene looks lit by practicals and window light at dusk or night.
* Walls and shadows lean cyan-green and blue-grey.
* Skin stays warm and natural so the people separate from the cool room.
* Highlights keep detail but roll off softly.
* Low-to-medium saturation overall, with the reds of the halation as the strongest colour.
GRAIN AND TEXTURE
* Fine but clearly visible 800-speed grain over the whole frame.
* More grain in the shadows, less in the highlights.
* A soft, slightly rounded film-scan sharpness; no digital oversharpening.
* Light vignette.
BACKGROUND
* The room stays the same room, same layout.
* Every light source in it (window, screen, lamps, reflections) becomes a halation source.
* Do not add new lamps, neon signs or flares.
PALETTE
Cyan-green shadows, blue-grey walls, warm skin, white-hot light, scarlet and orange halation.
Do NOT add purple, magenta, teal-orange grading or neon colours.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand and is graded and halated like the rest.
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
Halos follow their light sources and the bright edges they belong to.
NO halo left behind where a bright edge used to be.
NO halo frozen while the person moves.
FRAME-TO-FRAME FILM LIFE
THIS IS CRITICAL.
It must feel like real film running through a camera, not a still filter.
Allow between consecutive frames:
* grain to change every frame
* halo strength to breathe slightly (±5%)
* tiny exposure flicker (±2%)
Keep FIXED:
* the night grade and the cyan-green cast (no colour pumping)
* the halo colour
* the overall exposure
DO NOT
Do NOT add a letterbox, bokeh or anamorphic flares.
Do NOT use a red colour wash over the whole frame.
Do NOT make halos magenta, pink or neon.
Do NOT put the red ON the highlight core instead of around it.
Do NOT turn faces red.
Do NOT crush the blacks to pure black.
Do NOT add film burns, light leaks or scratches.
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
* NO halation, glow or bloom
* NO grain
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
Do NOT begin the halation film transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – HALATION RED-GLOW FILM STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me which light sources and bright edges in the clip will carry the strongest halation, and how dark the night grade will be.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME grade and halo colour on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, halo placement or grade consistency broke — regenerate those frames only.
The final video must feel like A NIGHT SCENE ON CINESTILL 800T: dim cyan-green room, white-hot lights with red halos, warm faces, 800-speed grain, 12 frames per second.
The image should deliberately contain:
* red-orange halation rims around every highlight
* white-hot light sources
* a dim, cool night grade
* lifted film blacks
* visible film grain.
Avoid flat digital video.
```
