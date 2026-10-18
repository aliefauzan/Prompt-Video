# 54 — Teal & Orange Anamorphic

**Look:** The clip becomes a still from a summer blockbuster. Skin, wood and warm fabrics glow orange while everything else falls into teal shadow. The room melts into soft oval bokeh behind sharp people. Blue horizontal anamorphic streaks cross the frame, highlights halate red, 35 mm grain sits on top, and the picture is letterboxed to 2.39:1 scope.

**Also called / where it trends:** "Cinematic" (frameloop.ai style name), "teal and orange", "orange & teal", "blockbuster look / blockbuster grade", "Michael Bay look", "Hollywood grade", "anamorphic look", "movie still LUT". It is the default "make it cinematic" grade in AI image/video tools (frameloop, Higgsfield, Runway presets) and a staple of colour-grading tutorials on YouTube and LUT packs sold to travel creators on Instagram and TikTok.

**References:**
- https://frameloop.ai/visual-styles (screenshot `refs/ref_1.png`; the style's sample image `refs/ref_2.png`): the **Cinematic** style card. Its style prompt, credited to frameloop.ai and expanded into the workflow below: *"Highly detailed cinematic photograph, movie still, shot on 35mm anamorphic lens, shallow depth of field, bokeh. Dramatic volumetric lighting, lens flares. Saturated rich colors, vibrant color grading, teal and orange tones."*
- https://petapixel.com/2017/02/23/orange-teal-look-popular-hollywood/ (screenshot `refs/ref_3.png`): PetaPixel, "What is the 'Orange & Teal Look' and Why is it So Popular?" Skin sits opposite teal on the colour wheel, so pushing everything else teal makes people pop.
- https://noamkroll.com/color-grading-for-the-blockbuster-look-why-it-works-wonders-on-every-shot/: Noam Kroll on grading for the blockbuster look (warm skin, cool shadows, contrast).
- https://juanmelara.com.au/blog/the-summer-blockbuster-colour-grading-tutorial: Juan Melara's summer blockbuster grade breakdown.
- https://shotkit.com/teal-orange-look/: teal/orange LUT and photo examples.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). The room is defocused with a vertically oval kernel, with highlights weighted so they bloom into oval discs. A Lab grade pushes warm hues orange and neutral or cool hues teal. Horizontal blue streaks are drawn from small background highlights plus one practical light above the window. It adds red halation, bloom, 35 mm grain and a vignette. A 2.39:1 window pans smoothly with the heads (from the masks) inside black bars.

## Prompt

```text
I'm uploading one video clip. Convert it into a TEAL & ORANGE ANAMORPHIC BLOCKBUSTER frame-by-frame animation: every frame should look like a still from a big-budget movie shot on 35mm anamorphic lenses, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Highly detailed cinematic photograph, movie still, shot on 35mm anamorphic lens, shallow depth of field, bokeh, dramatic volumetric lighting, lens flares, saturated rich colours, teal and orange grading.
Transform the footage into a blockbuster frame built from:
* a TEAL / ORANGE colour split
* warm ORANGE skin, wood and warm fabrics
* deep TEAL shadows, walls, greys and greens
* creamy warm highlights
* SHALLOW depth of field: the people sharp, the room behind them soft
* OVAL anamorphic bokeh (discs taller than they are wide)
* HORIZONTAL BLUE anamorphic streak flares
* red-orange HALATION around bright edges
* soft bloom
* fine 35mm film grain
* a gentle vignette
* a 2.39:1 SCOPE LETTERBOX with black bars
The result should feel like someone:
LIT THE SCENE LIKE A FILM SET
→ SHOT IT ON 35MM WITH ANAMORPHIC GLASS WIDE OPEN
→ LET THE PRACTICALS FLARE ACROSS THE LENS
→ GRADED IT TEAL AND ORANGE IN THE DI
→ FRAMED IT FOR SCOPE
→ RELEASED IT FRAME-BY-FRAME.
CHARACTER — PHOTOGRAPHIC, GRADED
The people stay PHOTOGRAPHIC and SHARP.
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
COLOUR GRADE — TEAL & ORANGE
* Skin goes warm golden-orange but stays natural skin, not tan paint.
* Warm materials (wood, brown batik, beige) go richer orange.
* Neutral and cool things (white walls, grey and green clothes, plants, screens) go TEAL.
* Shadows lean teal-blue; highlights lean warm cream.
* Strong but filmic contrast: deep shadows that still hold detail, rolled-off highlights.
* Saturated, rich, but never neon.
* The whole frame should read as two families of colour: orange people, teal world.
DEPTH OF FIELD + BOKEH
* Focus on the people's faces.
* The room behind them falls into soft defocus.
* Bright points and the window become OVAL bokeh: vertically stretched discs with slightly brighter rims.
* Edges of the people stay clean; no cut-out halo.
ANAMORPHIC FLARES
* Bright small light sources throw long, thin, HORIZONTAL streaks across the frame.
* The streaks are BLUE / CYAN with a white-hot core.
* Allow 1–3 streaks per frame, mostly in the upper part of the frame, never covering a face.
* Faint oval ghost reflections may sit on the line through the frame centre.
HALATION, BLOOM AND GRAIN
* Bright edges (window light, white shirt stripes, skin highlights) get a thin red-orange glow.
* Soft bloom on the brightest areas.
* Fine 35mm grain over everything, slightly stronger in mid-tones.
SCOPE LETTERBOX
* Frame the picture at 2.39:1 inside the original frame size, with solid black bars top and bottom.
* Choose the vertical position of the scope window so every face stays inside the picture.
* Move that window only slowly and smoothly, like a pan-and-scan; never jump between frames.
PALETTE
Teal, deep blue-green, steel blue.
Orange, amber, golden skin, warm cream.
Black bars.
Do NOT add purple, magenta or neon colours.
OBJECT CONTINUITY
If the character holds an object, it stays sharp, attached to the hand and graded like the rest.
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
The focus stays on them as they move.
The bokeh and flares sit in the background and follow the real light sources.
NO frozen bokeh pattern from a previous frame.
NO streak stuck on screen while its light source moves.
FRAME-TO-FRAME FILM LIFE
THIS IS CRITICAL.
It must feel like real film running through a camera, not a still filter.
Allow between consecutive frames:
* grain to change every frame
* streak brightness to flicker slightly (±10%)
* bokeh discs to breathe a little in brightness
* halation to shimmer slightly
Keep FIXED:
* the teal/orange grade (no colour pumping)
* the scope ratio and bar size
* focus on the people
DO NOT
Do NOT use a flat orange or teal colour wash over the whole frame.
Do NOT turn skin orange-red or plastic.
Do NOT use round spherical bokeh.
Do NOT use vertical or star-shaped flares.
Do NOT cover faces with flares.
Do NOT make it look like a cheap Instagram filter.
Do NOT crop off heads with the letterbox.
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
* NO defocus or bokeh
* NO flares, halation or grain
* NO letterbox
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
Do NOT begin the teal & orange anamorphic transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – TEAL & ORANGE ANAMORPHIC STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me which light sources you will use for the anamorphic streaks, and the vertical position range of the 2.39:1 scope window.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME grade on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, grade consistency or the letterbox broke — regenerate those frames only.
The final video must feel like A SCENE FROM A SUMMER BLOCKBUSTER: orange people, teal world, oval bokeh, blue streaks, scope bars, 12 frames per second.
The image should deliberately contain:
* warm orange skin against teal surroundings
* shallow depth of field with oval bokeh
* horizontal blue anamorphic streaks
* red-orange halation
* fine 35mm grain
* a 2.39:1 letterbox.
Avoid flat digital video.
```
