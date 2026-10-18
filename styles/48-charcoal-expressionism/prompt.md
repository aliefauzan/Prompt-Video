# 48 — Charcoal Expressionism

**Look:** A dark, dreamlike charcoal drawing on toothy paper. People become velvety near-black silhouettes, with only their faces lifted out of the dark by a soft side light so they stay recognizable. Their edges smudge out into pale drifting fog. The room dissolves into blurred grey shapes behind the fog, with a darker ground plane, a few eraser-lifted light shafts and a luminous haze behind the figures. Broad diagonal charcoal strokes run across the background, vertical strokes rework the bodies, and finger smudges and charcoal dust change every frame while the fog drifts slowly.

**How it differs from 18 Pencil Rotoscope:** no clean pencil contour line and no line drawing on white. This is tonal: masses of soft black charcoal, smudge and fog, with the figures as shadows rather than outlines.

**Also called / where it trends:** "Charcoal Expressionism" in frameloop.ai's Visual Styles library. Related search terms: "dark charcoal drawing", "surreal charcoal landscape", "foggy charcoal figures", "expressionist charcoal illustration", "eerie monochrome drawing". The look draws on expressionist and surrealist charcoal drawing (heavy blacks, smudged fog, lone silhouettes) that is widely re-shared as dark-art mood boards.

**References:**
- https://frameloop.ai/visual-styles: the "Charcoal Expressionism" style card (screenshot `refs/ref_1.png`, the library row that holds the card). The style detail opens behind a sign-in page; it was NOT signed into. The public style prompt by **frameloop.ai** is credited and expanded here into the full video workflow:
  > dark monochrome charcoal illustration, high-contrast velvety blacks, foggy surreal landscape, grainy painterly texture, dreamlike, shadowy minimal silhouettes, eerie cinematic lighting
- https://assets.frameloop.ai/image/imagebb4b1381-ceee-4d25-bbbe-8913cd83c390.webp: frameloop's sample image for the style (`refs/ref_2.png`): dark charcoal silhouettes in a pale foggy landscape.
- https://www.pinterest.com/search/pins/?q=dark%20charcoal%20drawing%20foggy%20figures%20surreal: public Pinterest search, not signed in (`refs/ref_3.png`): charcoal figure drawings in fog for tone and smudge reference.

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV):
- Background: the frame blurred (σ 9) and flattened to mid greys, with a darker ground plane, a fog field that scrolls 2.2 px per frame, eraser-lifted diagonal light shafts, a luminous glow behind the figures and broad −22° charcoal stroke texture.
- People: tone crushed to velvety black, with soft light pools on each face (from Apple Vision boxes in `faces.json`) and a key light from the right. Vertical body strokes and broken soft contour strokes rework the silhouettes. The person mask is blurred (σ 7) so the edges dissolve into fog. Low fog curls in front of the legs.
- Finish: finger smudges (directional smears in random patches), vignette, and laid-paper tooth plus per-frame charcoal dust, strongest in the mid greys and calmer on faces. Strokes and smudges change on twos; dust changes every frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a handmade CHARCOAL EXPRESSIONISM frame-by-frame animation: a dark, dreamlike MONOCHROME CHARCOAL drawing with velvety black figures in a foggy surreal space, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame becomes a dark monochrome charcoal drawing:
* compressed and vine charcoal on toothy paper, black to warm pale grey only
* high-contrast, VELVETY BLACKS
* a FOGGY, surreal, dreamlike space instead of a sharp room
* shadowy, minimal SILHOUETTES for the people
* grainy, painterly texture: visible paper tooth, charcoal dust, broad strokes
* finger SMUDGES and eraser-lifted light
* eerie, cinematic side lighting
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ REDREW IT IN CHARCOAL ON TOOTHY PAPER
→ BUILT THE FIGURES UP AS DEEP BLACK MASSES
→ SMUDGED THEIR EDGES INTO FOG WITH A FINGER
→ LIFTED LIGHT OUT WITH AN ERASER
→ PHOTOGRAPHED EACH DRAWING
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — CHARCOAL SILHOUETTES
The people become dark charcoal figures that keep the photograph's structure.
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
This is an expressionist charcoal drawing over the photo, NOT a cartoon and NOT a clean line drawing.
Keep facial proportions, eye shape, glasses and hairline exact.
FIGURE RULES
Bodies, hair and clothing: deep, velvety near-black charcoal with only faint internal modelling.
Garment patterns may survive as faint lighter marks in the black.
FACES are lifted out of the dark by a soft pool of side light, so every face stays readable: eyes, nose, mouth and glasses modelled in soft greys.
The light comes from ONE side and stays on that side.
Figure edges are SOFT: smudged and dissolving into the surrounding fog, never a clean cut-out.
A few loose, broken charcoal strokes rework the outline; vertical strokes run down the bodies.
BACKGROUND RULES
The room becomes a foggy, surreal space:
* the room's shapes survive only as blurred, flattened grey masses
* a darker ground plane at the bottom
* pale fog, thickest at mid height, glowing behind the figures
* a few soft diagonal light shafts lifted out with an eraser
* broad diagonal charcoal strokes across the space
* heavy darkening toward the corners
* low fog curling in front of the legs
Keep the composition and the position of large shapes, but no sharp detail.
OBJECT CONTINUITY
If a person holds an object, draw it as part of the dark charcoal figure.
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
the silhouette and the face light follow.
NO floating silhouette.
NO previous-frame silhouette.
NO delayed outline.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel separately drawn in charcoal.
Allow between consecutive frames:
* charcoal strokes on the bodies to be redrawn
* broken outline strokes to land in different places
* finger smudges to move
* charcoal dust and grain to change
* the fog to drift slowly in one direction
Keep FIXED in every frame:
* the light direction
* the overall darkness of the figures
* the paper tooth
* the composition of the fog and background masses (they drift, they do not jump)
Do NOT make the boil so strong that faces flicker or change.
DO NOT
Do NOT use any colour; monochrome charcoal only (a faint warm paper tint is allowed).
Do NOT draw clean pencil contour lines or a line drawing on white.
Do NOT keep sharp photographic detail in the background.
Do NOT let faces sink into black; they must stay recognizable.
Do NOT use digital noise or TV static instead of charcoal grain.
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
* NO charcoal
* NO fog
* NO smudging
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
Do NOT begin the charcoal transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – CHARCOAL EXPRESSIONISM STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input.
For consistency, also give the first approved styled frame as a style reference for all later frames (same blacks, same fog brightness, same light direction, same paper tooth).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, lost faces, colour, or the style rules broke — regenerate those frames only.
The final video must feel like a CHARCOAL DREAM that MOVES: velvety black figures with softly lit faces, dissolving into drifting fog, every frame drawn again.
The image should deliberately contain:
* deep velvety charcoal blacks
* softly side-lit, recognizable faces
* smudged edges melting into fog
* pale drifting fog and eraser-lifted light shafts
* broad charcoal strokes and finger smudges
* visible paper tooth and charcoal dust.
Avoid clean lines, colour and digital noise.
```
