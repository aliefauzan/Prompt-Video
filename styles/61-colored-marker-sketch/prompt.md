# 61 — Colored Marker Sketch

**Look:** every frame becomes a page from an illustrator's sketchbook done in alcohol markers and coloured pencil: visible wobbly sepia / indigo pencil linework (silhouettes, features, folds, with a faint doubled construction line), fills laid in long diagonal chisel-tip MARKER STREAKS that overlap into darker bands, a second coat of the same marker in the shadows and a cool-grey marker in the darkest darks, loose diagonal coloured-pencil HATCHING in the shadows broken up by the paper tooth, and highlights left as bare warm-white paper. Fills miss or overshoot the lines. The people are fully coloured; the room is lighter, looser and fades out to bare paper toward the edges, like an unfinished sketch. Lines and strokes are re-drawn on twos so the whole page boils gently.

**Also called / where it trends:** "colored sketch", "marker sketch", "Copic marker illustration", "color pencil + marker drawing", "sketchbook style", "sketch color video filter", "urban sketch portrait" — AI style presets (frameloop, Hooked, Pixoate), Pinterest Copic / marker portrait and sketchbook boards, TikTok / Reels "drawn in markers" edits (2026). Not graphite pencil (style 18): this is in full colour with marker streaks. Not watercolour (style 19): no wet washes or blooms — opaque-edged streaks, line-led, paper white.

**References:**
- https://frameloop.ai/visual-styles — Frameloop "Colored Sketch" visual style card, screenshot `refs/ref_1.png`: a portrait in brown/graphite linework, colour-pencil hatching, white paper, lightly coloured street behind. Frameloop's own style prompt: *"color pencil drawing, marker illustration, visible linework"* (this prompt credits and expands it into the full video workflow below; the card's "try it" link goes to a sign-in page)
- https://www.pinterest.com/search/pins/?q=colored%20pencil%20and%20marker%20portrait%20sketch%20copic — Pinterest search, screenshot `refs/ref_2.png`: marker sketchbook portraits with streaky fills, overlap bands, paper white highlights and loose pencil lines
- https://www.hooked.so/tools/sketch-color-video-generator — "Sketch color" video generator
- https://pixoate.com/colorful-sketch — "Colorful sketch" photo-to-drawing style

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (all 179 frames at 12 fps), `preview.webp`. Local approximation rendered with `render.py` (numpy + OpenCV + person masks: mean-shift colour shapes, multiply-blended marker layers built from overlapping diagonal strokes, XDoG + silhouette pencil lines with tooth, hatching, edge fade, re-seeded on twos); the six sheet frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a COLORED MARKER + COLOR PENCIL SKETCH frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
STYLE SOURCE
This look starts from the Frameloop "Colored Sketch" visual style (frameloop.ai/visual-styles), whose style prompt is:
"color pencil drawing, marker illustration, visible linework".
Everything below expands that prompt into a full frame-by-frame video workflow.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a hand-drawn sketchbook page made from:
* warm WHITE SKETCHBOOK PAPER with a fine tooth, visible everywhere
* VISIBLE LINEWORK in coloured pencil: warm sepia / brown on the people, muted indigo on the room
* lines slightly wobbly, varying in pressure, broken by the paper tooth, with an occasional faint doubled construction line
* ALCOHOL-MARKER FILLS laid in long DIAGONAL chisel-tip STREAKS
* where two strokes overlap, the ink doubles: darker STREAK BANDS
* a SECOND COAT of the same marker in the shadows, strokes at a steeper angle
* a cool-grey marker in the darkest darks (hair, black clothes)
* loose diagonal COLOURED-PENCIL HATCHING in shadows, broken by the paper tooth
* HIGHLIGHTS LEFT AS BARE PAPER (cheekbones, forehead, shirt highlights, windows)
* fills that MISS or OVERSHOOT the lines a little
* the people fully coloured, the room lighter and looser, FADING TO BARE PAPER toward the edges (unfinished sketch)
* matte, no gloss, no photographic gradients
The result should feel like someone:
FILMED THE CLIP
→ SKETCHED EVERY FRAME IN COLOURED PENCIL
→ BLOCKED IN THE COLOURS WITH ALCOHOL MARKERS
→ ADDED A SECOND COAT IN THE SHADOWS
→ HATCHED THE DARKS WITH PENCIL
→ LEFT THE HIGHLIGHTS AND THE EDGES AS BARE PAPER
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — SKETCHED PEOPLE
The MAIN HUMAN SUBJECT(S) are drawn as marker sketches of THEMSELVES.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* clothing
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT stylise them into anime, cartoon or caricature.
Do NOT simplify the face into generic features: eyes, brows, nose, mouth and glasses must be drawn as the real person's.
Do NOT beautify or reshape faces.
LINEWORK RULES
* silhouette contour: the strongest line, sepia brown, slightly wobbly
* inner lines: eyes, brows, nostrils, mouth, ears, hairline, collar, sleeves, folds — thinner, lighter
* glasses: drawn as clean pencil lines
* the room: thinner indigo lines, fewer of them, fading out toward the edges
* lines never perfectly clean vector lines; pressure varies and the paper tooth breaks them
* no heavy black ink outline
MARKER RULES
* each area gets the marker colour that matches its real colour, slightly cleaner and brighter
* first coat: light tone over everything except the highlights, long diagonal strokes (about 30° from horizontal)
* overlap bands between neighbouring strokes are visible and darker
* second coat: same marker, steeper strokes, only in the mid-shadows
* third coat: cool grey marker only in the deepest darks
* stroke ends are visible; some strokes stop short of the line, some overshoot it
* stripes and prints stay, drawn with marker
PALETTE RULES
Marker-sketch colours:
* skin: peach / light sienna markers, warm sienna in the shadows
* hair: dark brown + cool grey, strands left as paper streaks
* clothes: each garment's own colour in its marker version (brick red, sage / forest green, sand / beige, navy)
* room: light cool blue-greys, sky blue windows, a few pale accents
* lines: sepia brown and muted indigo pencil
* paper: warm off-white
No neon, no full black areas, no muddy photographic colours.
BACKGROUND OPTIONS
SKETCHED ORIGINAL ROOM:
the real room drawn lightly — a few indigo lines and pale marker streaks in the middle, fading to bare paper at the edges.
BARE SKETCHBOOK PAGE (for selected sections, optional):
the room dropped completely: the coloured people on bare paper with only a light marker shadow at their feet.
The people stay exactly where they are in the original frame.
LAYER ORDER
A typical frame reads:
WARM SKETCHBOOK PAPER
↓
FIRST MARKER COAT (diagonal streaks, highlights left white)
↓
SECOND MARKER COAT (shadows)
↓
GREY MARKER (deepest darks)
↓
COLOURED-PENCIL HATCHING
↓
COLOURED-PENCIL LINEWORK
↓
PAPER TOOTH SHOWING THROUGH EVERYTHING.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object, sketched and coloured like the person.
Examples:
* phone
* cup
* chair
* bag
* microphone
* headphones
If the object is essential to the person's action, draw it fully coloured together with the person.
Do NOT accidentally leave it as bare paper or drop it.
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
The DRAWING changes.
The HUMAN MOTION does NOT change.
If the head moves:
the sketched head moves exactly with it.
If the hand moves:
the hand is drawn in its new position in that same frame.
If the body turns:
the lines and marker strokes follow the new pose in that same frame.
If the character interacts with an object:
the object moves exactly with the original action.
NO lagging lines.
NO ghost contours from previous frames.
SKETCH BOIL — FRAME-TO-FRAME RULES
THIS IS CRITICAL.
The look is hand-drawn animation, so the drawing BOILS — but in a controlled way:
* lines, marker strokes and hatching are RE-DRAWN ON TWOS (new strokes every 2 frames, held for 2 frames)
* stroke direction, stroke width, colours and coverage stay the SAME every time; only the exact stroke placement varies
* the people's colours never change between frames
* the unfinished fade toward the edges stays in the same place
Do NOT let the colours flicker.
Do NOT let strokes change direction from one drawing to the next.
Do NOT let the room appear and disappear.
DO NOT
Do NOT make it a graphite pencil drawing (it must be in full colour with marker streaks).
Do NOT make it watercolour: no wet washes, no blooms, no colour bleeding.
Do NOT make it a smooth digital painting or airbrushed gradient.
Do NOT fill the whole page edge to edge: leave bare paper at the edges and in the highlights.
Do NOT use a heavy black ink outline.
Do NOT turn it into anime or a cartoon.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT add text, signatures, logos, watermarks or UI.
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
* NO linework
* NO marker fills
* NO hatching
* NO paper texture
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
Do NOT begin the marker-sketch transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – MARKER SKETCH STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Before generating, make and show me ONE style plate (frame 1 drawn in this style) and lock: line colours, marker colour per person and garment, stroke angle for each coat, how far the room fades out.
Use the style plate and the previous styled frame as consistency references for every frame. Keep the boil ON TWOS: for every even-numbered frame, use the odd frame before it as a strong reference so its strokes are held wherever nothing moved, and only the parts the motion changed are re-drawn; each odd frame starts a fresh drawing.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, colours or the stroke rules broke — regenerate those frames only.
The final video must feel like a SKETCHBOOK THAT ANIMATES: real people, drawn in coloured pencil and streaky markers, boiling gently on twos.
The image should deliberately contain:
* visible, slightly wobbly coloured-pencil linework
* long diagonal marker streaks with darker overlap bands
* a second marker coat in the shadows
* loose coloured-pencil hatching broken by the paper tooth
* bare paper in the highlights and at the edges
* warm off-white sketchbook paper.
Avoid clutter: no doodles, arrows, colour swatches or notes on the page.
```
