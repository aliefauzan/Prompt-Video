# 49 — Chaotic Red Ink

**Look:** A raw indie-comic ink sketch on a solid flat RED ground. People are left as WHITE paper figures, drawn over with rough, heavy BLACK MARKER: every contour is traced several times with overshooting, jittery lines. Hair is a black mass with white strands scratched into it, and faces get doubled marker features. Dark clothing is red with black hatching, the darkest folds cross-hatched. Nervous scribbles hover beside the heads, tangled knots sit on the contours and stray strokes cut across the frame. The room survives only as dark-red and black edge lines on the red ground, under drifting fields of illegible white cursive scrawl. All line work is redrawn every frame.

**How it differs from 01 Punk Photocopy Collage and 25 Red Pencil Mixed Media:** no photocopy, cut-out collage or photographic footage, and no pencil. The whole frame is redrawn as a marker drawing on a flat red ground, with white illegible handwriting as the background texture.

**Also called / where it trends:** "Chaotic Red Ink" in frameloop.ai's Visual Styles library. Related search terms: "red background ink sketch", "black marker scribble art", "indie comic red and black", "chaotic line art", "neurotic sketch style". Red-and-black scribble illustration is a common look in indie comics, zines and dark manga-inspired fan art on Pinterest and art social media.

**References:**
- https://frameloop.ai/visual-styles: the "Chaotic Red Ink" style card (screenshot `refs/ref_1.png`, the library row that holds the card). The style detail opens behind a sign-in page; it was NOT signed into. The public style prompt by **frameloop.ai** is credited and expanded here into the full video workflow:
  > Chaotic ink sketch style, rough heavy black marker linework, scribbled and erratic overlapping pen strokes, indie comic aesthetic, expressive graphic illustration. Solid flat vibrant red background, high contrast black and white character design. Illegible white scribbled cursive handwriting in the background, raw, unpolished, slightly neurotic energy
- https://assets.frameloop.ai/image/image1a835215-3add-4d1e-8bf2-0c11d5fdbe20.webp: frameloop's sample image for the style (`refs/ref_2.png`): black-and-white marker character on flat red with white scrawl.
- https://www.pinterest.com/search/pins/?q=red%20background%20black%20ink%20sketch%20illustration%20scribble%20manga: public Pinterest search, not signed in (`refs/ref_3.png`): red-ground black-ink scribble illustrations for line energy reference.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV):
- Ground: flat vibrant red, with fields of illegible white "cursive": 30 clusters of random Hershey-script words, slanted and remap-warped, re-warped every three frames.
- People are white paper. Clothing darker than mid grey turns red; deep areas get 50° wavy hatching, the deepest add −40° cross-hatching.
- Hair (dark pixels in a head zone from Apple Vision landmarks in `faces.json`) is black with white Canny strands. Face features are drawn as double marker passes from the landmarks, plus the mouth line and nose.
- Contours are re-traced as jittery, overshooting multi-pass marker polylines. Nervous scribbles sit beside heads, tangled knots on contours and stray strokes across the frame. Background room edges are drawn in dark red and black, with cross-hatching on dark areas. All marks are re-seeded per frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a handmade CHAOTIC RED INK frame-by-frame animation: rough heavy BLACK MARKER sketch, WHITE figures, a SOLID FLAT VIBRANT RED background with illegible WHITE scribbled cursive, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame becomes a chaotic indie-comic ink sketch:
* rough, HEAVY BLACK MARKER linework
* scribbled, erratic, OVERLAPPING pen strokes; contours traced several times
* expressive graphic illustration, indie-comic / zine energy
* a SOLID FLAT VIBRANT RED background
* high-contrast BLACK-AND-WHITE character design
* ILLEGIBLE WHITE scribbled cursive handwriting drifting across the background
* raw, unpolished, slightly NEUROTIC energy
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ PAINTED THE WHOLE SHEET FLAT RED EXCEPT THE PEOPLE
→ ATTACKED IT WITH A FAT BLACK MARKER
→ SCRIBBLED NERVOUS NOTES IN WHITE PEN ALL OVER THE RED
→ SCANNED EVERY PAGE
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — BLACK-AND-WHITE MARKER FIGURES
The people become marker drawings that keep the photograph's structure.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* clothing
* accessories
* glasses
* pose
* body proportions
* movement
* hand position
* interaction with objects
This is a raw expressive sketch traced over the photo; the line is chaotic but the drawing is accurate.
Keep facial proportions, eye shape, glasses and hairline exact.
FIGURE RULES
Figures are WHITE paper.
Contours: heavy black marker, traced 2–3 times, overshooting at corners, slightly jittery.
Hair: a solid BLACK mass with white strand lines scratched into it.
Faces: white, with brows, eyes, pupils, nose and mouth drawn in doubled black marker strokes.
Dark clothing becomes RED with black hatching; the darkest folds are cross-hatched in black.
Light clothing stays white with black fold lines.
SCRIBBLE RULES
Add nervous energy around the figures:
* small tangled scribble clouds beside the heads
* knotted loops on the contours
* a few stray strokes across the frame
Never scribble over the eyes or mouth.
BACKGROUND RULES
The background is a SOLID FLAT VIBRANT RED.
The room survives only as rough edge lines in dark red and black marker; dark areas get loose cross-hatching.
Over the red, fields of ILLEGIBLE WHITE CURSIVE handwriting: slanted, scrawled, no readable words.
NO photographic background, NO gradients, NO other colours.
OBJECT CONTINUITY
If a person holds an object, draw it in black marker (white or red fill).
It moves exactly with the hand.
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
The drawing must match the source frame exactly in position, pose and timing.
If the head moves:
the drawing follows.
If the hand moves:
the drawing follows.
If the body turns:
the marker drawing follows.
NO floating outline.
NO previous-frame silhouette.
NO delayed outline.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel separately drawn by hand.
Allow between consecutive frames:
* every marker line to be redrawn with new jitter and overshoot
* scribbles and knots to be redrawn in new shapes
* stray strokes to appear in new places
* hatching to be redrawn
* the white cursive to wriggle and re-flow slightly
Keep FIXED in every frame:
* the flat red hue
* black, white and red as the only colours
* which areas are white, red or black
* the general placement of the cursive fields
Do NOT make the boil so strong that faces flicker or change.
DO NOT
Do NOT use any colour other than flat red, black, white (and dark red for background lines).
Do NOT keep any photographic texture, cut-out collage or photocopy look.
Do NOT use pencil, graphite or soft shading.
Do NOT write readable words in the cursive.
Do NOT make clean vector lines.
Do NOT turn the people into chibi, anime or caricatures.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
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
* NO marker lines
* NO red ground
* NO handwriting
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
Do NOT begin the red ink transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – CHAOTIC RED INK STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input.
For consistency, also give the first approved styled frame as a style reference for all later frames (same red, same marker weight, same cursive density).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, readable text, photo texture, or the style rules broke — regenerate those frames only.
The final video must feel like a NEUROTIC INK SKETCHBOOK that MOVES: white figures in heavy black marker on flat red, nervous scribbles and white scrawl everywhere, every frame drawn again.
The image should deliberately contain:
* rough heavy black marker lines, traced several times
* white figures with black hair masses
* red clothing with black hatching
* scribble clouds, knots and stray strokes
* a solid flat vibrant red ground
* illegible white cursive handwriting.
Avoid clean lines, photo texture and extra colours.
```
