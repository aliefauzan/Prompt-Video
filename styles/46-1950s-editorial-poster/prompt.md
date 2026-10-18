# 46 — 1950s Editorial Poster

**Look:** The clip becomes a mid-century travel poster, screen-printed in two inks on aged cream paper. Black is laid down with bold, tapered brush strokes: hair as solid black shapes, faces drawn with a few elegant ink lines (brows, lash lines, nose hook, jaw). Poppy red fills the clothes and some flat background shapes, and it sits slightly out of register, so the red block drifts a few pixels off the black line, like a cheap 1950s offset print. Skin and highlights stay as bare cream paper. The paper is stained and fibrous, the ink is ragged at the edges with pinholes, and a small red signature sits in the corner. Line wobble, ink grain and the red offset change every frame.

**Also called / where it trends:** "1950s Editorial Poster" in frameloop.ai's Visual Styles library. Related search terms: "mid-century modern illustration", "vintage travel poster", "1950s advertising art", "retro editorial illustration", "two-colour screen print poster". The look follows the mid-century travel and magazine posters of the 1950s (flat shapes, brush ink, limited spot colours), which are widely re-shared as poster and mood-board pins.

**References:**
- https://frameloop.ai/visual-styles: the "1950s Editorial Poster" style card (screenshot `refs/ref_1.png`, the library row that holds the card). The style detail opens behind a sign-in page; it was NOT signed into. The public style prompt by **frameloop.ai** is credited and expanded here into the full video workflow:
  > mid-century modern editorial illustration, 1950s vintage travel poster aesthetic, bold expressive ink brushwork, screen-printed texture on aged cream paper, limited tri-tone palette of poppy red and black on beige, minimalist flat shapes with offset color fills, elegant gestural lines, retro advertising art style, high contrast, clean negative space
- https://assets.frameloop.ai/image/imageafbb1aa2-3928-433d-814c-2c798a77872f.webp: frameloop's sample image for the style (`refs/ref_2.png`): red, black and cream poster figures with brush-ink line.
- https://www.pinterest.com/search/pins/?q=1950s%20travel%20poster%20illustration%20red%20black%20cream: public Pinterest search, not signed in (`refs/ref_3.png`): mid-century red/black/cream poster art for palette and brush reference.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV):
- Apple Vision face landmarks (`faces.json`, made with `faces.swift`) give each face hull, hairline arc and neck. Skin is kept as cream paper and red is blocked from the face core.
- The black plate is hair (dark pixels inside a head zone), deep shadows, a dark background, DoG contour lines and a tapered brush outline traced from the person mask, plus inked brows, lash lines, pupils and nose from the landmarks.
- The red plate is the clothing (body minus skin and hair; light stripes stay paper) plus warm and mid-dark background blocks. It is printed 8–14 px off register. Lips print in red, in register.
- Both inks get ragged edges, pinholes and uneven pull on aged cream paper with stains, fibres and a vignette. There is a cream margin and a red "Lou '57" signature. Ink noise and offset are re-seeded per frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a handmade 1950s EDITORIAL TRAVEL-POSTER frame-by-frame animation: bold BLACK brush ink + flat POPPY RED, screen-printed on AGED CREAM paper, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame becomes a mid-century modern editorial illustration:
* 1950s vintage travel-poster / retro advertising art
* bold, expressive BLACK INK BRUSHWORK with thick-thin tapered strokes
* elegant gestural contour lines
* minimalist FLAT shapes
* a limited tri-tone palette: POPPY RED, BLACK, and the BEIGE / CREAM of the paper
* red fills printed slightly OFF-REGISTER from the black line work
* screen-printed ink texture: ragged edges, pinholes, uneven ink pull
* AGED cream paper with faint stains and fibres
* high contrast, clean negative space
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ HAD A 1950s POSTER ARTIST TRACE IT IN BRUSH AND INK
→ CUT A SEPARATE RED SCREEN FOR THE FLAT COLOUR
→ PULLED BOTH INKS BY HAND ON CREAM STOCK, A LITTLE OUT OF REGISTER
→ LET THE PAPER AGE
→ SCANNED EVERY PRINT
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — BRUSH-INK FIGURES
The people become poster illustrations that keep the photograph's structure.
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
This is a stylised editorial illustration traced over the photo, NOT a cartoon or caricature.
Keep facial proportions, eye shape, glasses and hairline exact.
FACE RULES
Faces stay mostly BARE CREAM PAPER.
Draw them with only a few confident ink lines: brows, upper lash lines, pupils, the hook of the nose, the jaw where it meets shadow.
Lips may be printed in poppy red.
Do NOT shade faces with grey; there is no grey ink.
Do NOT put red on cheeks, forehead or skin.
INK RULES
BLACK: hair as solid black shapes with a few paper-white strand gaps; the deepest shadows; contours drawn with a tapered brush; dark background masses.
RED: clothing as flat red shapes; selected flat background shapes (warm surfaces, furniture, a wall); lips.
Light garment patterns (stripes, checks) stay readable as red-vs-paper areas.
PAPER: skin, highlights and all light areas are the bare cream paper.
Only these three tones exist. NO gradients, NO airbrush, NO photographic shading.
OFFSET PRINT RULES
The red plate is printed a few pixels off the black plate (down-right), so a sliver of cream shows between line and fill on one side and red overruns the line on the other.
Keep the offset small and consistent in direction.
Both inks have the texture of a hand-pulled screen print: slightly ragged edges, small pinholes, uneven density.
BACKGROUND RULES
Simplify the room into a few flat poster shapes: black for dark areas, red for warm or mid-dark areas, cream paper for light areas.
Keep the room layout recognizable but graphic, with clean negative space.
Add a narrow cream paper margin around the image and a small hand-lettered red signature in one corner, like a signed 1950s poster.
OBJECT CONTINUITY
If a person holds an object, draw it in the same black-and-red poster treatment.
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
the brush line and the red shapes follow.
NO floating red fill.
NO previous-frame silhouette.
NO delayed outline.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel separately printed by hand.
Allow between consecutive frames:
* the brush contour to wobble slightly
* stroke thickness to vary
* ink grain, pinholes and ragged edges to change
* the red offset to shift by a pixel or two
* paper stains to stay but ink density to vary
Keep FIXED in every frame:
* the red hue and the black
* the cream paper colour and margin
* the offset direction
* which areas are red, black or paper
Do NOT make the boil so strong that faces flicker or change.
DO NOT
Do NOT use any colour other than poppy red, black and cream paper.
Do NOT shade with greys or gradients.
Do NOT put red on faces or skin (lips only).
Do NOT make clean vector art or a perfect digital print.
Do NOT register the red perfectly to the black.
Do NOT turn the people into cartoons, anime or caricatures.
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
* NO ink line work
* NO red fills
* NO paper texture
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
Do NOT begin the poster transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – 1950s EDITORIAL POSTER STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input.
For consistency, also give the first approved styled frame as a style reference for all later frames (same red, same black, same cream paper, same brush weight, same offset).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, red-on-skin, grey shading, or the style rules broke — regenerate those frames only.
The final video must feel like a 1950s TRAVEL POSTER that MOVES: brush-ink figures, flat poppy red, aged cream paper, every frame printed again.
The image should deliberately contain:
* bold tapered black brush strokes
* flat poppy-red shapes, slightly off-register
* bare cream paper for skin and highlights
* a few elegant ink lines on each face
* screen-print ink grain and pinholes
* aged, stained cream paper with a margin
* a small red signature.
Avoid photographic shading and clean vector art.
```
