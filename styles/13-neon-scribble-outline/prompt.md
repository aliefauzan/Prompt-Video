# 13 — Neon Scribble Outline

**Look:** the real footage stays (slightly darkened and contrasty) and glowing hand-drawn neon marker lines are traced around every person: a loose doubled outline with a white-hot core and a coloured bloom, one neon colour per person (electric cyan, hot pink, acid lime, warm yellow), plus scribbled doodles anchored to each head — crowns, halos, stars, sparkles, hearts, spirals, zig-zag energy marks and big arrows. Every line re-wobbles each frame ("boils") like a 12 fps hand-animated overlay, and the doodle set changes every 2 seconds.

**Also called / where it trends:** "neon scribble effect", "glowing scribble / doodle outline", "neon outline edit", "glow sketch", "scribble animation", "doodle edit" (TikTok, Instagram Reels, YouTube Shorts; CapCut "scribble glow" templates and After Effects / Procreate Dreams tutorials). Big on dance, friends-group and music-video edits.

**References:**
- https://www.youtube.com/shorts/4VJpmN4tNlE — "The Best Neon Scribble Effect": doubled glowing outline + head doodles on real footage (refs/ref_2.png)
- https://www.youtube.com/shorts/Oi_55RaTZEI — "Glowing Lines | Scribble Glowing Effect": white core, coloured bloom, boiling lines (refs/ref_3.png)
- https://www.youtube.com/results?search_query=neon+scribble+effect — Shorts grid of the trend (refs/ref_1.png)
- https://www.tiktok.com/@its__zan/video/7583762788351331606 — TikTok doodle-outline edit tutorial
- https://www.tiktok.com/@dariapojar88/video/7488767620921986359 — TikTok "glow sketch" outline edit
- https://www.youtube.com/watch?v=xQxkVpG_5-s , https://www.youtube.com/watch?v=XXu_zlxCrEY — "Cara Membuat Video Scribble Glow Effect di CapCut" and a second CapCut scribble-glow tutorial (Indonesian)
- https://www.youtube.com/shorts/6tXGJWvjwIk , https://www.youtube.com/shorts/NzcZFTqyyvI — CapCut neon outline / scribble shorts
- https://freevisuals.net/ — free neon scribble overlay/template packs used by editors

**Example:** `example.png` (6 frames of the test clip), `before_after.png`. Local approximation in `render.py`: footage darkened, the dilated person-mask contour drawn as a doubled wobbly stroke (white core + 3-level blur glow), colour per nearest head (Apple Vision face boxes via `faces.swift`), head-anchored doodles redrawn with new wobble every frame, a new doodle set every 24 frames, small sparkles in the background kept off the people. All 179 frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a NEON SCRIBBLE OUTLINE frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.

TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.

CORE VISUAL STYLE
Keep the REAL footage and draw a glowing hand-animated neon overlay on top of it, built from:
* the original video, slightly darkened and with more contrast, so the neon reads as light
* a loose, hand-drawn outline around every person, traced like a marker scribble
* the outline drawn TWICE, slightly offset (doubled scribble line)
* each line with a white-hot core and a saturated coloured glow / bloom around it
* ONE neon colour per person: electric cyan, hot pink, acid lime, warm yellow
* doodles anchored to each person's head and shoulders:
  crowns, halos, stars, sparkles, hearts, spirals, zig-zag energy marks, big curved arrows
* uneven marker line weight, round line caps, slightly overshooting line ends
* every line re-drawn every frame with a new wobble ("line boil")
* a few small sparkles in the empty background
The result should feel like someone:
PLAYED THE VIDEO ON A TABLET
→ DIMMED IT A LITTLE
→ TRACED EVERY PERSON WITH A GLOWING NEON MARKER
→ TRACED IT AGAIN, LOOSELY, ON TOP
→ SCRIBBLED DOODLES AROUND EVERY HEAD
→ RE-DREW EVERYTHING ON THE NEXT FRAME
→ ANIMATED IT FRAME-BY-FRAME AT 12 FPS.

CHARACTER — REAL FOOTAGE UNDER NEON
The people stay PHOTOGRAPHIC and UNCHANGED underneath the neon.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing
* skin tone
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT repaint, cartoonize or beautify the people.
Do NOT draw neon lines across faces.
The neon is an OVERLAY around and above the people, not a filter on them.

NEON OUTLINE
* Trace the outer silhouette of every person (head, hair, shoulders, arms, hands, torso) a few pixels OUTSIDE the body edge.
* Draw it as TWO loose strokes slightly offset from each other, the way a fast marker scribble overlaps itself.
* Strokes may overshoot at corners and leave small gaps, like real hand drawing.
* Line weight: medium marker, thicker on the main contour, thinner on the doubled stroke.
* Each person keeps the SAME colour for the whole video (assigned left to right).
* When people overlap, each outline keeps its own colour.

GLOW
* Every line has a white or very pale core.
* Around the core, a saturated coloured glow in that person's colour.
* A wider, softer bloom of the same colour fades into the footage.
* Glow is additive light: it brightens the footage under it, it never paints a solid fill.
* No glow fills inside the body.

DOODLES (ANCHORED TO HEADS)
For each person, draw 3–5 simple doodles in the same neon colour, anchored to their head and shoulders so they MOVE WITH THE PERSON:
* a crown or halo floating just above the head
* 2–3 stars or 4-point sparkles beside the head
* zig-zag "energy" marks rising from the head or shoulders
* a heart or a spiral near the shoulder
* a big curved arrow pointing at the person (on some sections)
Doodles are single-line drawings with the same glow.
Doodles must NEVER cover the face.
Change the doodle set every ~2 seconds (every 24 frames): keep the crown/halo, swap the others.

BACKGROUND
* The room stays real footage, slightly darker than the people.
* Add a few small white sparkles or dots in empty background areas only.
* Do NOT draw outlines around furniture, walls or windows.
* Do NOT add neon to the background except tiny sparkles.

COLOUR RULES
* neon colours: electric cyan, hot pink / magenta, acid lime, warm yellow
* line cores: white
* glow: saturated, the same hue as the line
* footage: natural colours, darkened ~25%, contrast slightly up
Do NOT tint the whole footage one colour.
Do NOT use more than one neon colour per person.

LAYER ORDER
REAL FOOTAGE (darkened, contrast up)
↓
SOFT WIDE COLOURED BLOOM
↓
COLOURED GLOW
↓
WHITE LINE CORES (outlines + doodles)
↓
SMALL BACKGROUND SPARKLES.

OBJECT CONTINUITY
IMPORTANT:
If a character is interacting with an object, preserve that object.
Examples:
* glasses
* phone
* chair
* bag
* lanyard / badge
* clothing accessory
Keep the object real and visible. Include a hand-held object inside the person's neon outline.
Do NOT erase or hide objects under the neon.

CHARACTER CONTINUITY LOCK
The SAME person must remain recognizable in every frame.
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

PERFECT MOTION TRACKING
The underlying character movement must remain exactly faithful to the source footage.
If the head moves:
the outline and the crown follow.
If the hand moves:
the outline around the hand follows.
If the body turns:
the outline follows.
NO floating outlines.
NO previous-frame silhouette.
NO delayed outline.
NO doodles left behind in empty space.

LINE BOIL (FRAME-TO-FRAME)
This is a 12 fps hand-drawn overlay. Between consecutive frames:
* every outline is re-drawn with a NEW small wobble (a few pixels), so the lines "boil"
* the doubled stroke shifts slightly against the main stroke
* doodles keep the same shape and anchor, but re-wobble and may rotate a few degrees
* sparkles twinkle (grow / shrink)
* colours per person stay EXACTLY the same
Do NOT let lines jump far from the silhouette.
Do NOT let the colour assignment swap between people.

DO NOT
Do NOT cartoonize, paint or filter the people.
Do NOT replace the footage with a drawing.
Do NOT use clean vector outlines or perfect geometric shapes.
Do NOT draw lines across faces.
Do NOT fill bodies with colour.
Do NOT use a generic "glow edges" / edge-detect filter on the whole frame.
Do NOT outline the furniture or room.
Do NOT add text, emoji stickers, logos or subtitles.
Do NOT add glitch, VHS or film grain.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
It must feel like a REAL HAND-DRAWN NEON MARKER OVERLAY, re-drawn frame by frame.

STAGE 1 – FRAME EXTRACTION (STRICT)
1. Read the source clip's frame rate and duration.
Report both to me BEFORE doing anything else.
2. Extract frames as follows:
* If the source is 24 fps:
keep every SECOND frame, discard the one in between.
* If the source is 30 fps:
conform to 24 fps first, then keep every second frame.
* Target in both cases:
exactly 12 unique frames per second of source.
Nothing else.
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
Use ONLY the original UNMODIFIED extracted frames.
At this stage:
* NO Seedream generation
* NO neon outlines
* NO doodles
* NO glow
* NO darkening or colour changes
* NO effects
* NO styling
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
THEN STOP AND WAIT
After successfully building and reporting the verification timeline:
STOP.
Do NOT begin Seedream generation.
Do NOT stylize any frames.
Do NOT begin the neon scribble transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.

STAGE 3 – NEON SCRIBBLE EVERY FRAME (ONLY AFTER MY CONFIRMATION)
1. Restyle EVERY extracted frame individually with Seedream 5.0 Pro, using that exact original frame as the image reference.
2. Keep each output at the source resolution and framing. No crop, no zoom, no reframing.
3. The people and the room must stay photographic and match the original frame; ONLY the neon overlay and the slight darkening are added.
4. Replace each clip on the timeline IN PLACE with its neon scribble version. Same order. Same 1/12 second duration.
5. Lock the style sheet before generating: the same neon colour per person, the same line weight, the same glow strength, the same doodle family, in EVERY frame. Re-use the same wording for every frame prompt.
6. Change the doodle set only every 24 frames (2 seconds); in between, keep the same doodles anchored to the same heads with fresh wobble.
7. Check every 12th frame against the original: same faces, same pose, outline hugging the silhouette, no lines on faces. Regenerate any frame that fails.
8. Export at the original duration with the original audio.
```
