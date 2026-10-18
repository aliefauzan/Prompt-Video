# 47 — Two-Tone Screen Print

**Look:** A minimalist two-colour fashion-editorial print on bright white paper. People are drawn in fine, slightly wobbly CERULEAN BLUE pen line (features, folds, outlines), with hair as a solid blue shape broken by white strands. Their clothes become flat VIBRANT ORANGE blocks with a crayon-grain lithograph texture. Blue litho blocks stand in for the darkest background areas and a few background details are drawn in blue line; everything else is clean white negative space. Where blue lies over orange it overprints darker, like real ink. Line wobble, pen skips and grain change every frame.

**How it differs from 06 Risograph:** no halftone dots, no grain-heavy riso misregistration and no pink/teal duotone over the whole frame. Here the drawing is fine pen LINE ART plus a few flat orange and blue blocks, with most of the frame left as white paper.

**Also called / where it trends:** "2-Tone Minimalist" in frameloop.ai's Visual Styles library. Related search terms: "two colour screen print illustration", "orange and blue editorial illustration", "minimalist fashion illustration", "lithograph line art", "duotone print portrait". The orange + cerulean pair is a common limited palette in contemporary editorial and fashion illustration and in screen-printed gig and art posters.

**References:**
- https://frameloop.ai/visual-styles: the "2-Tone Minimalist" style card (screenshot `refs/ref_1.png`, the featured row that holds the card). The style detail opens behind a sign-in page; it was NOT signed into. The public style prompt by **frameloop.ai** is credited and expanded here into the full video workflow:
  > Minimalist two-tone screen print illustration, vibrant orange and cerulean blue color palette, bold flat color blocks contrasted with fine line-art detailing, hand-drawn lithograph aesthetic, clean white negative space, pop art influence with contemporary fashion editorial vibes.
- https://assets.frameloop.ai/image/image00ca254c-eade-4b03-ab5e-5d72e370f166.webp: frameloop's sample image for the style (`refs/ref_2.png`): blue line figures with flat orange garments on white.
- https://www.pinterest.com/search/pins/?q=two%20color%20screen%20print%20illustration%20orange%20blue%20portrait: public Pinterest search, not signed in (`refs/ref_3.png`): two-colour orange/blue print portraits for palette and line reference.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV):
- Fine line art is Canny edges on a bilateral-filtered grey image, short fragments dropped, then remapped with a small smooth displacement field and random pen skips per frame.
- Apple Vision landmarks (`faces.json`) draw the pen features (brows, eyes, pupils, nose, jaw) and lips; a face hull with a hairline arc separates skin from hair. Hair is solid blue with white strand streaks.
- Clothing (body minus skin and hair, light stripes left white) is a flat orange litho block printed ±3 px off. Only its darkest folds get blue hatching. Skin gets a light blue stipple only in its own darkest shadows.
- Dark and leafy-green background areas become blue litho blocks, and background edges become blue line. Blue overprints orange by multiply. Line warp and grain are re-seeded per frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a handmade MINIMALIST TWO-TONE SCREEN-PRINT frame-by-frame animation: fine CERULEAN BLUE line art + flat VIBRANT ORANGE colour blocks on clean WHITE paper, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame becomes a minimalist two-tone screen-print illustration:
* exactly TWO inks: VIBRANT ORANGE and CERULEAN BLUE
* bold FLAT colour blocks contrasted with FINE line-art detailing
* hand-drawn lithograph feel: crayon grain inside the blocks, slightly wobbly pen line
* CLEAN WHITE negative space everywhere else
* pop-art influence with a contemporary fashion-editorial mood
* where the two inks overlap they overprint darker, like real screen ink
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ TRACED EVERY PERSON IN FINE BLUE PEN
→ BLOCKED THE CLOTHES IN FLAT ORANGE ON A SECOND SCREEN
→ PULLED BOTH COLOURS ONTO WHITE PAPER
→ LEFT EVERYTHING ELSE BLANK
→ SCANNED EVERY PRINT
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — LINE-ART FIGURES
The people become editorial line drawings that keep the photograph's structure.
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
This is a fashion-editorial illustration traced over the photo, NOT a cartoon or anime.
Keep facial proportions, eye shape, glasses and hairline exact.
LINE ART RULES (BLUE)
All drawing is done in fine cerulean-blue pen line:
* face features: brows, eyes, pupils, nose, lips outline, jaw
* garment outlines and fold lines
* hands and fingers
* a few background edges
Lines are thin, confident and slightly wobbly, with occasional small skips.
Skin stays WHITE paper; only its deepest shadows get a light blue stipple.
HAIR: one SOLID BLUE shape with thin white strand lines cut into it.
COLOUR BLOCK RULES (ORANGE)
CLOTHING becomes flat ORANGE blocks with a lithograph crayon grain.
* light garments: orange block with white pattern gaps (stripes, prints stay readable)
* dark garments: orange block plus sparse blue hatching in the deepest folds only
The orange block may sit a few pixels off the blue line, as in a hand-registered print.
Lips may be orange.
Orange NEVER goes on skin or hair.
BACKGROUND RULES
Keep the room recognizable but nearly empty:
* the darkest background masses (dark walls, plants, shadows) become flat BLUE litho blocks
* a few key edges of the room are drawn in blue line
* everything else is clean WHITE negative space
NO photographic background, NO grey, NO third colour.
OBJECT CONTINUITY
If a person holds an object, draw it in blue line (orange only if it is clothing-like).
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
the line art and the orange blocks follow.
NO floating colour block.
NO previous-frame silhouette.
NO delayed outline.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel separately drawn and printed by hand.
Allow between consecutive frames:
* the pen lines to be redrawn with a slight wobble
* small pen skips to move
* the crayon grain inside the blocks to change
* the orange block edge to shift by a pixel or two
* white hair strands to be redrawn
Keep FIXED in every frame:
* the orange and the blue hues
* the white paper
* which areas are orange, blue or white
Do NOT make the boil so strong that faces flicker or change.
DO NOT
Do NOT use any colour other than orange, cerulean blue and white (and their overprint).
Do NOT use halftone dots or risograph grain over the whole frame.
Do NOT shade with greys or gradients.
Do NOT fill skin with colour.
Do NOT keep the photographic background.
Do NOT make clean vector art.
Do NOT turn the people into cartoons or anime.
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
* NO line art
* NO colour blocks
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
Do NOT begin the two-tone print transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – TWO-TONE SCREEN-PRINT STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input.
For consistency, also give the first approved styled frame as a style reference for all later frames (same orange, same blue, same line weight, same white paper).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, colour on skin, a third colour, or the style rules broke — regenerate those frames only.
The final video must feel like a MOVING FASHION-EDITORIAL PRINT: fine blue line people in flat orange clothes on clean white paper, every frame drawn again.
The image should deliberately contain:
* fine, slightly wobbly cerulean-blue line art
* solid blue hair with white strands
* flat vibrant-orange garment blocks with litho grain
* a few blue blocks for the darkest background
* lots of clean white negative space
* darker overprint where blue crosses orange.
Avoid halftone dots, greys and photographic texture.
```
