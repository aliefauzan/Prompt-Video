# 30 — Spider-Verse Comic Offset

**Look:** The footage is rendered like a frame from *Into / Across the Spider-Verse*. The people keep their real faces but get flat, punchy cel colour, thick ink contours, diagonal ink hatching in the shadows and a coarse halftone dot screen. The background is printed off-register: the cyan, magenta and yellow plates slide apart, with no depth blur. Kirby-dot energy clusters, short glitch hits and texture animated "on twos" finish the look.

**Also called / where it trends:** "Spider-Verse effect", "Spiderverse filter / edit", "Spider-Verse look", "comic book effect", "chromatic offset / CMYK offset", "animated on twos". It peaked with the June 2023 *Across the Spider-Verse* release: the TikTok "AI Spider-Verse filter", CapCut "Spider-Verse" templates, and After Effects, DaVinci Resolve and Blender tutorials on YouTube. It is still a stock edit style on TikTok and Reels (Miles/Gwen transition edits, "Another Dimension" intros).

**References:**
- https://www.pinterest.com/search/pins/?q=spider%20verse%20comic%20style%20edit%20halftone: Spider-Verse comic edits showing halftone, ink panels and spot colours (screenshot `refs/ref_1.png`).
- https://www.pinterest.com/search/pins/?q=spiderverse%20effect%20photo%20edit%20chromatic%20offset: real-photo "Spider-Verse effect" edits with chromatic offset and glitch shards (screenshot `refs/ref_2.png`).
- https://www.youtube.com/watch?v=QwhaoLvwrXA: Megan Tan, "How To Get The SPIDERVERSE Look – Lighting and Editing Tutorial" (60.8K views). Covers live-action plus animated elements and a CapCut path.
- https://www.youtube.com/watch?v=UqvbPo8o0N8: "Spider-Verse Look: Easy Comic Book Effect Tutorial in After Effects".
- https://www.youtube.com/watch?v=nPJByhw5SNQ: "Spiderverse Effect Tutorial | Free Plugin | DaVinci Resolve 18".
- https://cineversity.maxon.net/en/tutorials/spider-verse-effect-getting-trapcode-particular-on-2s: Cineversity on running effects "on 2s" for the Spider-Verse stutter.
- https://www.reddit.com/r/AfterEffects/comments/13yksf7/how_can_i_recreate_the_spiderverse_effect/: r/AfterEffects thread on recreating the effect.
- https://www.comingsoon.net/guides/news/1295647-spider-man-ai-spider-verse-filter-how-to-do-it-tiktok-iphone-ios-android: the 2023 TikTok AI Spider-Verse filter trend.
- https://www.capcut.com/template-detail/Spider-Verse/7253392439468231937: CapCut "Spider-Verse" template.
- https://www.tiktok.com/@animatographyy/video/7625008186512182560: "Spider-Verse Style Edit Tutorial: Miles & Gwen Transitions" (TikTok, 2026).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (whole clip) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). It does skin-aware bilateral cel colour in 4 tone steps, Canny ink lines plus a matte contour, a 15° dot screen, 45°/-40° hatching, CMY plates split 16 px on the background, Kirby dots in four sections and glitch hits on frames 23-24, 47, 71-72, 98, 121-122, 146 and 169. Texture is seeded per frame pair (on twos).

## Prompt

```text
I'm uploading one video clip. Convert it into a SPIDER-VERSE COMIC OFFSET frame-by-frame animation (the "Into / Across the Spider-Verse" look), matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a frame of a comic book brought to life:
* real faces kept, but painted with FLAT, PUNCHY CEL COLOUR in 3–4 tone steps
* THICK BLACK INK CONTOURS around every person and major shape
* diagonal INK HATCHING in the shadows (cross-hatching in the deepest shadows)
* a coarse HALFTONE DOT SCREEN in the mid-shadows
* the background printed OFF-REGISTER: cyan, magenta and yellow plates slid apart
* NO depth-of-field blur: out-of-focus areas are shown as CMYK misregistration instead
* a night-Brooklyn palette in the background: deep indigo, purple, hot magenta, with cyan fringes
* KIRBY DOTS: clusters of black dots with a neon glow, as comic "energy"
* short GLITCH hits: sliced, shifted, RGB-split frames
* texture animated ON TWOS
The result should feel like someone:
PRINTED THE VIDEO FRAME ON A FOUR-COLOUR COMIC PRESS
→ LET THE PLATES SLIP OUT OF REGISTER
→ INKED THE PEOPLE BY HAND WITH CONTOURS AND HATCHING
→ SCREENED THE SHADOWS WITH BEN-DAY DOTS
→ RAN IT THROUGH A MULTIVERSE GLITCH NOW AND THEN
→ ANIMATED IT FRAME-BY-FRAME, ON TWOS.
CHARACTER — INKED, CEL-COLOURED, STILL THEMSELVES
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
Keep the faces REAL and recognizable: the same eyes, nose, mouth and face shape, painted over, not replaced.
Do NOT turn them into generic cartoon characters.
Do NOT give them superhero suits or masks.
CEL COLOUR
* Smooth each area into flat colour, then step it into 3–4 tones: light, mid, shadow, ink.
* Push saturation up: clothes and skin colours get bolder, not neon.
* Keep skin tones natural in hue; faces use softer steps so expressions stay readable.
* No soft airbrushed gradients on the people.
INK LINES
* Thick black outer contour around every person, varying in weight like a brush pen.
* Thinner interior lines for facial features, hair locks, glasses, collar, folds and clothing patterns.
* Line weight wobbles slightly between frame pairs (hand-inked, not vector).
HATCHING AND HALFTONE
* Mid-shadows: a dot screen (about 15°) whose dots grow larger as the shadow deepens.
* Shadows on clothes and the shadow side of faces: diagonal parallel ink hatching.
* Deepest shadows: cross-hatching, then flat ink black.
* On faces keep hatching light and sparse; no dot blobs over the eyes or mouth.
OFF-REGISTER BACKGROUND (the key Spider-Verse trick)
* Keep the original room, but print it as if the cyan, magenta and yellow plates were misaligned by 10–20 px.
* Edges in the room show coloured ghost fringes: cyan on one side, magenta or red on the other.
* Lay a big halftone screen over the background, visible as a dot pattern.
* Grade the background toward night: deep indigo shadows, purple mids, pink-magenta highlights.
* The people have only a HAIRLINE misregistration, so they stay crisp in front of the offset room.
KIRBY DOTS
* In some sections, add clusters of black circles of mixed size near the frame edges and corners.
* Each cluster has a neon glow around it (magenta or yellow), like comic energy crackle.
* Never put Kirby dots over a face.
GLITCH HITS
* About every 2 seconds, one or two frames glitch:
  horizontal slices shifted sideways, a strong RGB split, and one rectangular block re-printed in a different-universe palette (inverted, cyan/magenta duotone, black border).
* The person's pose underneath stays the same as the source frame.
* The very next frame returns to the normal look.
PALETTE
* People: their real colours, saturated and cel-stepped, with black ink.
* Background: indigo / purple / magenta with cyan and yellow plate fringes.
* Accents: hot magenta, cyan, yellow (print primaries).
Do NOT turn the whole frame one colour.
Do NOT use pastel or washed-out colour.
OBJECT CONTINUITY
If the character interacts with an object (phone, chair, bag), ink and colour it with the hand. It moves exactly with the original action.
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
The contours and hatching follow the body.
NO ink lines left behind from the previous frame.
NO halftone or hatching pattern stuck to the screen while the person moves.
ON-TWOS TEXTURE (FRAME-BY-FRAME BOIL)
THIS IS CRITICAL.
Spider-Verse animates on twos. Copy that rhythm in the STYLE, not in the motion:
* The hatching pattern, dot-screen offset, plate misregistration, ink line weight and Kirby dots change every SECOND frame.
* Each pair of frames shares the same texture, then the texture jumps.
* The person's pose still updates on EVERY frame, exactly as in the source.
* Every frame is still generated individually; nothing is copied from a neighbour.
DO NOT
Do NOT use a soft blur or bokeh on the background.
Do NOT make it a clean flat vector cartoon.
Do NOT make it a generic posterize filter.
Do NOT add speech balloons, captions or panel borders.
Do NOT add Spider-Man suits, masks, webs or logos.
Do NOT replace faces with anime or 3D-character faces.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT glitch every frame.
Do NOT keep the same texture for more than two frames.
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
* NO ink lines or hatching
* NO halftone
* NO misregistration
* NO Kirby dots or glitches
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
Do NOT begin the Spider-Verse transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – SPIDER-VERSE STYLING (AFTER MY CONFIRMATION ONLY)
First, list for me which frame numbers will be glitch hits and which sections will carry Kirby dots.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the pose is exactly that frame.
For each frame pair (01–02, 03–04, …) use the same texture seed, so hatching, dots and plate offsets hold for two frames.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing or the style rules broke — regenerate those frames only.
The final video must feel like A COMIC BOOK PRINTED OFF-REGISTER AND BROUGHT TO LIFE: real faces, inked contours, hatched shadows, dot screens, sliding colour plates, Kirby crackle, glitch hits, 12 frames per second with the texture stepping on twos.
The image should deliberately contain:
* thick hand-inked contours
* diagonal hatching
* halftone dots
* CMY plate misregistration
* saturated cel colour
* Kirby-dot energy
* occasional glitch frames.
Avoid polished digital perfection.
```
