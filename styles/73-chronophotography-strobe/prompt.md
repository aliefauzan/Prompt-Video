# 73 — Chronophotography Strobe (频闪 残影)

**Look:** The office vanishes into a black velvet ground, and the people stand in a hard strobe flash: silvery, nearly monochrome, crisp. Behind each moving person trail several frozen copies of their earlier poses, one per flash, four flashes a second. The copies are dimmer the older they are and overlap like exposures on one photographic plate. There is never a smear between them. The newest pose is always clean and in front. A thin white measuring scale runs along the bottom, as on Étienne-Jules Marey's plates.

**Also called / where it trends:** "频闪" (strobe), "残影" (afterimage), "多重曝光" (multiple exposure), "闪光灯频闪效果" (flash-strobe effect), "一秒拍出多重曝光的运动摄影", "chronophotography", "Marey effect", "stroboscopic photography", "strobe motion", "multiple-exposure dance" — Bilibili photo and Premiere / DaVinci tutorials (strobe-flash dancers on black, MAXPA and Sapphire plugins). It goes back to Marey's 1880s fixed-plate chronophotographs and Harold Edgerton's strobe photographs, and is used in dance and sports edits and the ditherer "Ghost Dance" preset.

**References:**
- https://www.bilibili.com/video/av1003686133, https://www.bilibili.com/video/av1403624324, https://www.bilibili.com/video/av841422349 (contact sheet `refs/ref_1.png`, from the discovery sweep D4): Bilibili 频闪 多重曝光 残影 videos; a dancer repeated as several sharp copies across a black ground, plus a Houdini strobe-photograph tutorial.
- https://www.pinterest.com/search/pins/?q=marey%20chronophotography (screenshot `refs/ref_2.png`): Marey's chronophotographs; white figures and traces repeated on black plates, the fencer and runner series, the measuring scale.
- https://en.wikipedia.org/wiki/Chronophotography: chronophotography, "a set of photographs of a moving object, taken for the purpose of recording and exhibiting successive phases of motion".
- https://www.cinematheque.fr/henri/film/113597-films-chrono-photographiques-etienne-jules-marey-1889-1904/: Cinémathèque française, Marey's chronophotographic films 1889–1904.
- https://www.sciencemuseum.org.uk/objects-and-stories/human-machine: Science Museum on Marey, Muybridge and the "human machine".
- https://motionographer.com/2013/12/03/inout-mt-wolf-midnight-shallows/: Mt. Wolf "Midnight Shallows" music video, a modern strobe-chronophotography piece.

How it differs from taken styles: **26 Slow Shutter Smear** keeps the room and the colour grade and drags streaked ghosts along the motion path (Wong Kar-wai step printing). Here the room is gone, the light is a hard silver strobe, and each copy is a sharp frozen pose with no streak. **17 Double Exposure** dreamily blends two different images; this is many stepped copies of the same people. **72 Time-Slice** cuts time into strips side by side; this stacks moments on top of each other.

**Why it needs multi-frame context:** every output frame contains the people from five moments: the current frame and the frames 3, 6, 9 and 12 positions back (a 4 Hz strobe at 12 fps). The earlier poses are not in the current frame, so a single-frame model would have to invent them. The prompt makes the generator take those earlier frames as extra image inputs. A video model with the whole clip in context would also work.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks, all 179 frames). The room is crushed to about 5% of its luminance. The people are "flash-lit": 70% desaturated, an S-curve, a lifted floor so dark clothes still read on black, and a slightly cool tint. Masked copies from 12, 9, 6 and 3 frames back are laid down oldest first, at exposure 0.33, 0.45, 0.60 and 0.78, and combined with lighten (max), like exposures adding up on one plate. The mattes are eroded 2 px so no window-white fringe rides on the copies. The current pose goes on top at full exposure. A faint flash-spill halo, a vignette, fine grain that changes every frame and a white graduated scale along the bottom finish the frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a CHRONOPHOTOGRAPHY STROBE (频闪 残影) frame-by-frame animation: on a black ground, every moving person is repeated as several crisp frozen copies of their earlier poses, one per strobe flash, like Étienne-Jules Marey's chronophotographic plates, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
This style NEEDS MULTI-FRAME CONTEXT: every styled frame shows the people at FIVE moments: the current frame and the frames 3, 6, 9 and 12 positions earlier. Those earlier poses are not in the current frame, so they must never be invented or redrawn. Give Seedream all five source frames as image inputs for every generation (or, if a video model with the full clip in context is used, the same frame mapping applies). If you cannot pass several source frames into one generation, SAY SO AND STOP instead of faking it.
CORE VISUAL STYLE
Transform the footage into a strobe chronophotograph built from:
* a near-BLACK velvet ground: the room crushed to almost nothing, only a faint cool trace of it left, like an underexposed plate
* the people lit by a HARD STROBE FLASH: silvery, about 70% desaturated, crisp, high contrast, with dark clothes lifted to a readable charcoal grey
* FIVE exposures per frame: the current pose plus copies from 3, 6, 9 and 12 frames earlier (a strobe firing 4 times per second)
* every copy a SHARP, FROZEN pose: no smear, no streak, no motion blur
* older copies DIMMER: about 78%, 60%, 45% and 33% exposure
* overlapping copies combine like light on one plate: where they overlap, the brighter one wins
* the CURRENT pose always on top, at full exposure, clean and solid
* a faint flash spill on the black around the newest pose
* fine silver film grain and a soft vignette
* a thin WHITE graduated measuring scale (long tick every 10, medium every 5) along the bottom edge, like Marey's rule
The result should feel like someone:
HUNG BLACK VELVET BEHIND THE PEOPLE
→ OPENED THE SHUTTER ON ONE PLATE
→ FIRED A STROBE FOUR TIMES A SECOND
→ LET EVERY FLASH FREEZE ANOTHER COPY OF THE MOTION
→ DEVELOPED THE PLATE IN SILVER
→ PRINTED A NEW PLATE FOR EVERY FRAME.
CHARACTER — PHOTOGRAPHIC, FLASH-LIT
Every copy is the real person from its source frame, only relit.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing
* accessories
* pose (as it was at that flash)
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT beautify or re-sculpt faces.
Do NOT turn the people into silhouettes, outlines or drawings.
THE STROBE COPIES
* Copies come ONLY from the real earlier frames (3, 6, 9, 12 back). Near the start of the clip, where those frames do not exist, use the first frame (the copies then sit under the current pose and are not seen).
* People who stand still: their copies sit almost exactly under the current pose and show only as a slight doubled edge where the handheld camera moved. That is correct.
* People who move (a reaching hand, a lean, a step): their copies fan out behind them in clear steps, one pose per flash.
* Copies never get a halo or a white rim from the old background; only the person is copied.
* No copy is ever stretched, streaked or blended into the next.
FLASH LIGHT AND TONE
* Silver monochrome with a hint of the original colour (skin barely warm, batik barely brown, stripes cream-grey).
* Hard S-curve contrast; whites crisp, never blown out.
* Dark clothes and hair stay readable charcoal against the black, never pure black.
* Slightly cool highlights.
BACKGROUND
* The office is gone: near-black, about 5% of its original brightness, a little cooler.
* No new backdrop, no texture, no stage.
PALETTE
Black, charcoal, silver grey, cool white, faint warm skin and faint brown.
Do NOT add saturated colour, neon, coloured gels or a warm sepia wash.
OBJECT CONTINUITY
If a hand holds an object, the object is copied with the hand at every flash.
CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every copy of every frame.
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
The current pose must match the current source frame exactly.
Each copy must match its own earlier source frame exactly.
NO invented in-between poses.
NO copy taken from a later frame.
FRAME-TO-FRAME BEHAVIOUR
THIS IS CRITICAL.
Between consecutive frames the whole stack moves forward by one frame: the newest copy becomes the current pose, every copy advances, the oldest drops off. The trail must follow the motion continuously.
Allow between consecutive frames:
* grain to change every frame
* the flash spill to breathe very slightly
Keep FIXED:
* the 3-frame strobe spacing and the five exposures
* the exposure levels of the copies
* the black ground
* the silver tone
* the measuring scale (same position, same ticks)
DO NOT
Do NOT motion-blur or smear between copies.
Do NOT keep the office visible.
Do NOT blend two different images like a dreamy double exposure.
Do NOT add speed lines, glow trails or light painting.
Do NOT add colour grades, neon or coloured strobes.
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
* NO black ground or flash relighting
* NO strobe copies from other frames
* NO grain or scale
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
Do NOT begin the chronophotography strobe transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – CHRONOPHOTOGRAPHY STROBE STYLING (AFTER MY CONFIRMATION ONLY)
First, for three sample frames (one near the start, one in the middle, one near the end), list the five source frames that feed each one, and name the stretches of the clip where people move enough for the copies to fan out.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the main image input, plus the frames 3, 6, 9 and 12 positions earlier as extra image inputs, and tell it which exposure level each one gets.
Apply every style rule above, with the SAME spacing, exposures and tone on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where a copy was invented, smeared, taken from the wrong frame, or the current pose is not clean on top — regenerate those frames only.
The final video must feel like A MAREY CHRONOPHOTOGRAPH COME ALIVE: flash-lit silver people on black velvet, crisp stepped copies of every movement, a measuring scale below, 12 frames per second.
The image should deliberately contain:
* a near-black ground
* silver, flash-lit, crisp people
* four dimmer frozen copies trailing every movement
* no smear between copies
* a thin white graduated scale along the bottom.
Avoid motion blur.
```
