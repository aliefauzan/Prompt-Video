# 33 — Aerochrome Infrared

**Look:** The footage looks as if it were shot on Kodak Aerochrome, the discontinued false-colour infrared slide film. Its layers record green, red and near-infrared light and print them as blue, green and red. Anything green and alive (plants, leaves) turns hot pink, crimson or magenta. Cool walls, window light and sky go teal and cyan. Skin glows pale, smooth and luminous, because skin reflects infrared. Olive and khaki fabric shifts to crimson, rose or navy. A punchy slide-film curve, teal shadows, red halation on the highlights and fine grain complete it. This is the Richard Mosse / music-video "pink world" look.

**Also called / where it trends:** "Aerochrome", "Kodak Aerochrome look", "infrared film / IR chrome", "false-colour infrared", "pink foliage", "digital Aerochrome". Kodak discontinued the film in 2009. The look lives on through Kolari Vision's IR Chrome filter, colourist tutorials (Mixing Light), music videos shot with IR Chrome, and pink-foliage edits on Instagram and TikTok.

**References:**
- https://www.pinterest.com/search/pins/?q=kodak%20aerochrome%20portrait: Aerochrome and IR-chrome portraits with pink foliage, teal sky and pale skin (screenshot `refs/ref_1.png`).
- https://kolarivision.com/lambert-grand-music-video-in-ir-chrome/: Kolari Vision, the "Grand" music video by Lambert shot in IR Chrome (screenshot `refs/ref_2.png`).
- https://www.mpb.com/en-us/content/tips-and-techniques/how-to-get-kodak-aerochrome-look-using-digital-infrared: MPB on getting the Aerochrome look with digital infrared. It notes the film was discontinued in 2009, that greens become pink, red or purple, and covers the Kolari IR Chrome filter.
- https://mixinglight.com/color-grading-tutorials/infrared-look-emulating-aerochrome/: Mixing Light, emulating Aerochrome in a colour grade.
- https://hiddenrealms.ch/digital-aerochrome-video/: digital Aerochrome video.
- https://blog.dominey.photography/2020/11/22/the-surprising-true-story-of-kodak-aerochrome/: the history of Kodak Aerochrome.
- https://www.plferrer.photos/digital-aerochrome-tutorial/: digital Aerochrome tutorial.
- https://www.youtube.com/watch?v=2tVM6EGxw8A: Aerochrome look video tutorial.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (whole clip) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). It estimates a near-IR channel from the visible frame: foliage gets very bright IR, warm organics (skin, wood, brown cloth) get IR at or above their red, and cotton gets a lift. Then it swaps the layers IR to red, red to green and green to blue. Blue light lands as teal. Foliage is pushed to hot pink, skin is softened and lifted to a pale glow, and the frame gets ×1.6 saturation, an E-6 S-curve, teal shadows, red halation, per-channel grain and a slight per-frame emulsion breath. Result: teal-cyan room, hot-pink plants, crimson-to-navy olive shirt, pale luminous skin.

## Prompt

```text
I'm uploading one video clip. Convert it into an AEROCHROME INFRARED frame-by-frame animation (the Kodak Aerochrome false-colour infrared film look), matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage as if it were shot on KODAK AEROCHROME false-colour infrared slide film:
* the film's layers record GREEN, RED and NEAR-INFRARED and print them as BLUE, GREEN and RED
* everything GREEN AND ALIVE (plants, leaves, grass) turns HOT PINK, CRIMSON or MAGENTA
* cool surfaces, window light, sky and white walls turn TEAL and CYAN
* SKIN GLOWS: pale, smooth, luminous, slightly cool peach, with blemishes and veins vanishing
* olive, khaki and green fabrics shift to crimson, dusty rose or deep navy
* warm wood and brown cloth turn yellow-orange to peach
* neutral greys stay neutral but lean cool teal
* a punchy SLIDE-FILM contrast curve with TEAL SHADOWS
* RED HALATION glowing around the brightest highlights
* fine slide-film grain, coarser in the shadows
The result should feel like someone:
LOADED A ROLL OF KODAK AEROCHROME III INTO THE CAMERA
→ SHOT THROUGH A YELLOW FILTER
→ LET THE INFRARED LAYER PAINT EVERY LIVING GREEN THING PINK
→ PROCESSED IT AS E-6 SLIDE FILM
→ SCANNED EACH FRAME WITH ITS GRAIN AND HALATION
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — INFRARED-LIT, STILL THEMSELVES
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing and clothing patterns
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Keep the faces REAL and recognizable. Only the colour response changes.
Skin may glow and smooth out, but facial structure, eyes and expression must stay sharp and exact.
Do NOT make skin pink, green or grey; it is pale luminous peach.
Do NOT turn the people into ghosts or glowing silhouettes.
COLOUR MAPPING (THE CORE RULE)
* Map the colours consistently, the way the film does, not by painting random areas:
  - green foliage → hot pink / crimson / magenta
  - blue and cool light → teal / cyan
  - skin → pale luminous peach
  - red objects → yellow-orange
  - olive / khaki / green-grey fabric → crimson, rose or navy, shifted as ONE colour per garment
  - white and grey → neutral, leaning cool teal
* Every instance of the same source colour maps to the same result colour throughout the clip.
* Saturation is high but filmic, not neon.
FILM CHARACTER
* Slide-film S-curve: rich blacks, bright clean highlights.
* Shadows lean teal-cyan.
* A soft red-orange halation glow around windows, lamps and bright highlights.
* Infrared focus is very slightly soft overall.
* A soft vignette.
* Grain in each colour layer, coarser in the shadows.
PALETTE
* Hot pink, crimson, magenta, teal, cyan, pale peach, navy, and a little yellow-orange.
Do NOT leave anything natural green.
Do NOT turn the whole frame pink.
Do NOT use a plain hue rotation or a pink tint over everything.
OBJECT CONTINUITY
If the character interacts with an object (phone, chair, bag), map its colour with the same infrared rules. It moves exactly with the original action.
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
The people's motion must match the source footage exactly on EVERY frame.
The skin glow and colour mapping follow the body.
NO colour patches left behind from the previous frame.
NO garment changing colour between frames.
FRAME-BY-FRAME BOIL
THIS IS CRITICAL.
Every frame is processed individually, like separate film frames, so:
* the grain is new on every frame
* exposure breathes very slightly from frame to frame
* the colour balance of the emulsion drifts a tiny amount per frame
The colour MAPPING stays fixed: pink stays pink, teal stays teal.
DO NOT
Do NOT keep green anywhere.
Do NOT make it a pink filter over the original colours.
Do NOT turn skin pink or green.
Do NOT add a dreamy blur or fog.
Do NOT change one garment's colour halfway through the clip.
Do NOT add flowers, plants or props that are not in the source.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
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
* NO colour remapping
* NO halation
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
Do NOT begin the Aerochrome transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – AEROCHROME STYLING (AFTER MY CONFIRMATION ONLY)
First, list for me the main colours in the scene (plants, walls, window, each garment, skin) and the infrared colour each one will map to. Keep this map fixed for the whole clip.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the pose is exactly that frame.
Apply the colour map and every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing or the colour map broke (green showing, a garment flipping colour, skin going pink) — regenerate those frames only.
The final video must feel like A ROLL OF KODAK AEROCHROME RUN THROUGH A MOVIE CAMERA: hot-pink foliage, teal light, pale glowing skin, garments shifted to crimson and navy, slide-film contrast, red halation and live grain, 12 frames per second.
The image should deliberately contain:
* false-colour infrared mapping
* hot-pink foliage
* teal-cyan cool light
* luminous pale skin
* slide-film contrast
* red halation and grain.
Avoid polished digital perfection.
```
