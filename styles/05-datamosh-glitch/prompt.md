# 05 — Datamosh Glitch

**Look:** the clip looks like a corrupted video file: pixels from an old moment get dragged around by the motion of the new one, so people melt and smear into their next pose, stale colour "blooms" stretch along the direction of movement, 24-px macroblocks stay frozen or turn into flat squares, bright runs of pixels are sorted into streaks and drips (pixel sort), the red and blue channels are pulled apart (RGB split), and thin horizontal slices tear sideways. Faces keep re-forming block by block, so everyone stays recognizable between the melts.

**Also called / where it trends:** "datamosh", "datamoshing", "pixel bloom", "I-frame removal", "P-frame duplication", "pixel sorting", "glitchcore", "glitch edit", "corrupted video edit", "RGB split" — music-video edits on TikTok / YouTube Shorts / IG Reels (A$AP Mob "Yamborghini High", Kanye West "Welcome to Heartbreak"), glitchcore / hyperpop edits, Datamosher-Pro, supermosh, After Effects Datamosh 2 + Pixel Sorter tutorials, CapCut glitch templates.

**References:**
- https://www.youtube.com/results?search_query=datamosh+edit+pixel+sort+glitch — screenshot `refs/ref_1.png`: "Learn how to Datamosh in under 5 minutes", "Headmosh #datamosh", "Made with Datamosh", "Create Pixelated & Glitch…" Shorts
- https://videocue.io/looks/datamosh-pixel-sorting-corruption — screenshot `refs/ref_2.png`: VideoCue "Datamosh Pixel Sorting Corruption" look — "horizontal rows resorted by luminance, datamosh i-frame removal smears motion across the frame"
- https://www.adobe.com/uk/express/learn/blog/what-is-datamosh — what datamosh is: removed I-frames project old pixels onto the next shot; duplicated P-frames make pixels "melt or bloom"
- https://www.premiumbeat.com/blog/datamoshing-make-footage-look-trippy/ — Datamoshing 101 (i-frame removal vs d/p-frame duplication; Avidemux / AE plugin workflow)
- https://www.youtube.com/watch?v=UKmhWnFnlh4 — A$AP Mob "Yamborghini High" music-video datamosh effect breakdown
- https://www.youtube.com/watch?v=ylDc5EH5JgA — pixel sorting + datamoshing + glitches tutorial (AE Pixel Sorter, Datamosh, Universe Glitch)
- https://pitchfork.com/thepitch/is-glitchcore-a-tiktok-aesthetic-a-new-microgenre-or-the-latest-iteration-of-glitch-art/ — glitchcore on TikTok; datamosh "best known… for its use in Kanye West's 2009 'Welcome to Heartbreak' video"
- https://github.com/Akascape/Datamosher-Pro — open-source GUI datamosher (30+ glitch modes)
- https://github.com/keijiro/KinoDatamosh — real-time datamosh shader (motion-vector smear model)
- https://github.com/satyarth/pixelsort — pixel sorting reference implementation

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049). Local approximation made with `render.py`: optical flow averaged into 24-px macroblock motion vectors drives a real P-frame simulation (stale reference + high-frequency residual + intra-refresh blocks inside the person matte), with bloom sections, DC-only blocks, pixel sorting, RGB split and slice tears; it simulates every frame in order and writes 6 frames to `frames/` (`render.py ... all` writes all 179).

## Prompt

```text
I'm uploading one video clip. Convert it into a DATAMOSH / PIXEL-SORT / RGB-SPLIT GLITCH edit, styled frame by frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
Datamosh is a TIME effect (pixels from earlier frames are carried into later ones), so every Seedream generation gets TWO image inputs: the original extracted frame AND the previous STYLED frame. This is how the smear travels from frame to frame.
CORE VISUAL STYLE
Transform the footage into a corrupted, moshed digital video built from:
* DATAMOSH SMEAR: pixels of an older frame dragged along by the motion of the current frame
* PIXEL BLOOM: stale colours stretching and swelling along the direction of movement
* people MELTING into their next pose, then re-forming
* frozen and drifting 16–24 px MACROBLOCKS
* flat single-colour blocks and posterised blocks (starved bitrate)
* PIXEL SORTING: runs of bright pixels sorted into streaks (horizontal) or drips (vertical)
* RGB SPLIT: red shifted one way, blue the other, along edges
* thin horizontal SLICE TEARS shifted sideways
* punchy, slightly oversaturated digital colour with crushed blacks
The result should feel like someone:
EXPORTED THE CLIP AS A COMPRESSED VIDEO FILE
→ DELETED THE KEYFRAMES (I-FRAMES)
→ DUPLICATED SOME MOTION FRAMES (P-FRAMES) OVER AND OVER
→ PIXEL-SORTED PARTS OF THE PICTURE
→ SPLIT THE COLOUR CHANNELS
→ PLAYED THE BROKEN FILE BACK AND SCREEN-RECORDED IT, FRAME BY FRAME.
CHARACTER — PHOTOGRAPHIC PEOPLE, BROKEN SIGNAL
The people stay PHOTOGRAPHIC.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing and clothing patterns
* accessories (glasses, watches)
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw anyone.
Do NOT turn anyone into a cartoon, painting or 3D render.
Do NOT replace faces.
The glitch DESTROYS PIXELS, it does not invent new content.
Every smear, block and streak must be made of colours and textures that really exist in the source frames.
FACES ARE THE ANCHOR
Faces may break into blocks, smear for a moment and carry RGB split, but:
* in most frames every face is readable
* a face never stays melted for more than 3–4 frames in a row
* broken face blocks re-form from the real frame, block by block
* slice tears and heavy pixel sorting stay OFF the faces
DATAMOSH RULES
* MOSH (I-frame removal): start a section from a REFERENCE picture, then move that picture's pixels using the motion of each new source frame. Where people move, they drag the old pixels with them and leave stale pixels behind. New edges and details of the current frame are drawn on top of the old colours.
* TRANSITION MOSH: in at least one section, the reference picture comes from a DIFFERENT moment of the clip (for example a close-up from earlier), so the old close-up melts and flows with the motion of the wide shot until the current picture takes over.
* BLOOM (P-frame duplication): in at least one section, repeat one strong motion again and again for several frames, so the pixels keep flowing in the same direction and swell / stretch beyond the real movement.
* INTRA REFRESH: every frame, a share of 16–24 px blocks inside the people is replaced by the clean current frame, so they re-form gradually.
* Static areas (walls, windows, furniture) stay mostly stable; the mosh lives where there is motion.
Motion moves in BLOCKS, not as smooth liquid: smears have square, stepped edges.
PIXEL SORTING
In selected sections, sort runs of mid-to-bright pixels:
* horizontal sorting: bright windows and walls stretch into long luminous streaks
* vertical sorting: bright areas drip downward
* sorting happens mostly in the BACKGROUND, not over faces
* runs are sorted by brightness, keeping the real colours of the frame
RGB SPLIT AND TEARS
* red channel shifted 4–14 px right, blue channel shifted the same amount left, every frame with a little jitter; strongest in the last section
* 2–6 thin horizontal slices (6–60 px tall) shifted sideways per frame, kept off the face rows
* a few random flat-colour / posterised macroblocks per frame
SECTIONS
Plan the clip in sections, for example:
* 0–1 s: nearly clean picture with light RGB split (the "keyframe")
* 1–3 s: mosh from the first frame — the reaching hand smears and blocks apart
* 3–5 s: fresh reference + horizontal pixel-sorted streaks in the bright background
* 5–8 s: transition mosh — an earlier close-up melts into the wide shot
* 8–10 s: BLOOM — people stretch and melt sideways, strong RGB split
* 10–13 s: mosh + vertical pixel-sort drips
* 13–15 s: mosh from an earlier frame + horizontal sort + strongest RGB split and tears
Each section restarts from a reference picture (a brief moment of recovery), then breaks down again.
FRAME-BY-FRAME CORRUPTION
THIS IS CRITICAL.
The mosh must ACCUMULATE: each styled frame builds on the previous styled frame, moved by the new motion.
Allow, every frame:
* blocks to drift with the motion
* new blocks to freeze or refresh
* pixel-sort thresholds to shift a little
* RGB split to jitter
* slice tears to change position
Do NOT style each frame independently from scratch inside a mosh section — that kills the smear.
Do NOT freeze the whole picture.
PERFECT MOTION TRACKING
The underlying character movement must remain exactly faithful to the source footage.
The PIXELS break.
The HUMAN MOTION does NOT.
If the head moves:
its smear and its re-formed blocks follow the real head position.
If the hand moves toward the camera:
the smear follows the real hand motion.
If the character interacts with an object:
the object moves exactly with the original action.
NO invented motion except the deliberate BLOOM repeat.
NO zoom, crop or reframing.
OBJECT CONTINUITY
Keep every object the people hold or touch (phone, chair, bag, cup, glasses).
Objects may smear and block, but they must not disappear or change.
CHARACTER CONTINUITY LOCK
The SAME people must remain recognizable across the clip.
Never change:
* identity
* facial structure
* hairstyle
* clothing
* accessories
* body proportions
* anatomy
* expression
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.
DO NOT
Do NOT use VHS tracking lines, film grain, film burns or date stamps.
Do NOT use a generic "glitch" preset of random coloured rectangles that ignore the motion.
Do NOT add neon glow, cyberpunk graphics, text, logos or UI.
Do NOT use rainbow gradients or colours that are not in the source.
Do NOT turn the people into liquid, paint or 3D shapes.
Do NOT keep faces melted for long stretches.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace faces.
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
* NO datamosh
* NO pixel sorting
* NO RGB split
* NO slice tears
* NO compression blocks
* NO colour grading
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
Do NOT begin the datamosh transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – DATAMOSH STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro, IN ORDER, one generation per frame.
For each frame give Seedream two inputs:
(1) the original extracted frame (for pose, identity and the new motion),
(2) the previous STYLED frame (the corrupted pixels to carry forward).
For the first frame of each section, use the planned REFERENCE picture as input (2) instead.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames on the timeline (the "duplication" in BLOOM is a visual effect inside the frames, not duplicated timeline clips).
Do NOT restyle a whole shot from one keyframe.
Plan the sections first and list them to me (frame range, reference frame, mode: mosh / transition mosh / bloom, pixel-sort direction, RGB-split strength) before generating.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke (faces melted too long, invented content, smear moving against the real motion) — regenerate those frames only, then regenerate the following frames of that section so the smear chain stays continuous.
The final video must feel like a REAL BROKEN VIDEO FILE that somehow still plays: smearing, blooming, blocky, sorted, split — with the people surfacing again and again.
The image should deliberately contain:
* motion-driven block smears
* pixel bloom
* macroblock artifacts
* pixel-sorted streaks or drips
* RGB split
* slice tears.
Avoid clean, smooth, polished glitch presets.
```
