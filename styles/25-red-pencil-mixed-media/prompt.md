# 25 — Red Pencil Mixed Media

**Look:** The room stays a full-colour photograph. Each person is cut out and replaced by a hand-drawn graphite sketch on white paper. Faces, hair and skin are in black-and-white pencil with hatching and contour lines, with the photo tones kept underneath so they stay recognizable. Their clothes are filled with RED coloured-pencil hatching. The cut-out has a torn white paper rim, a soft drop shadow and a broken red pencil contour, so it looks like a paper drawing pasted onto the live footage. The strokes are redrawn every frame, so the drawing boils.

**Also called / where it trends:** "mixed media edit", "paper sketch video", "sketch cutout trend", "pencil drawing on real video", "drawing come to life", "red pencil sketch edit". stevenwommack (6.7M followers) tried @thezamizafar's mixed-media tutorial and prompt inside invideo's agent. It spreads on Instagram Reels as "comment MIX for the prompt" posts, the same invideo frame-by-frame workflow as the Punk Photocopy Collage.

**References:**
- https://www.instagram.com/stevenwommack/reel/DegkiPHRb_d/ (screenshots: `refs/ref_1.png` post page, a black-and-white pencil girl with red pencil on a colour background; `refs/ref_2.png` final-result frames; `refs/ref_3.png` 12-frame contact sheet of the reel). "I tried @thezamizafar's mixed media tutorial with her prompt inside of @invideo.io… paper sketch video" by **stevenwommack**. The original tutorial and prompt are by **@thezamizafar**. The prompt is DM-gated ("Comment "mix""), so it is not public and was NOT copied. This prompt is written from the visible result, in the same staged invideo structure as stevenwommack's public Punk Photocopy Collage prompt (`_source/reference_prompt_punk_collage.txt`). Credit: @thezamizafar (look and original prompt), stevenwommack (invideo version).
- https://www.instagram.com/stevenwommack/: creator page ("Free Mobile Video Editing Tips and Tricks").

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV):
- The background is the original frame with saturation ×1.2.
- People are a colour-dodge pencil sketch mixed with stretched photo tone, graphite hatch and cross-hatch textures (noise smeared along 48° and −42°), DoG contour lines and paper tooth.
- Faces and hair are found from the top-most skin blob under each silhouette head, plus dark hair near it. They stay graphite.
- Everything else inside the person gets red coloured-pencil hatching at 62°, denser on darker cloth, with red fold lines.
- The cut-out has a jagged torn edge, a 5–14 px white paper rim, a drop shadow and a broken, doubled red pencil contour. All strokes are re-seeded per frame.

## Prompt

```text
I'm uploading one video clip. Convert it into a handmade MIXED-MEDIA PAPER SKETCH frame-by-frame animation: GRAPHITE + RED COLOURED PENCIL people, cut out on white paper, over the ORIGINAL full-colour footage, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every person becomes a hand-drawn paper cut-out laid over the real scene:
* black-and-white GRAPHITE pencil drawing of the person
* visible pencil hatching and cross-hatching in the shadows
* confident contour lines and fold lines
* the photo's light and shade kept underneath, so faces stay recognizable
* RED COLOURED PENCIL filling the clothes, as visible diagonal strokes
* white paper tooth showing through the strokes
* a TORN WHITE PAPER rim around the cut-out
* a soft drop shadow under the paper
* a broken, slightly doubled RED pencil contour around the paper edge
* the room / background kept as the ORIGINAL full-colour footage
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ TRACED EACH PERSON IN GRAPHITE ON WHITE PAPER
→ COLOURED THEIR CLOTHES WITH A RED PENCIL
→ TORE THE DRAWING OUT BY HAND
→ PASTED IT BACK ONTO THE COLOUR PHOTO
→ OUTLINED IT IN RED
→ SCANNED EVERYTHING
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — GRAPHITE DRAWING
The people become PENCIL DRAWINGS that keep the photograph's structure.
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
This is a careful observational drawing traced over the photo, NOT a cartoon.
Keep facial proportions, eye shape, glasses and hairline exact.
GRAPHITE RULES
Faces, hair, skin and accessories: graphite ONLY (black, greys, paper white).
Shadows are built from parallel hatching; the deepest shadows add cross-hatching.
Hair is drawn with long directional strokes.
Light areas stay as clean paper.
Contours: darker, slightly varied line weight, occasionally broken.
RED COLOURED PENCIL RULES
The CLOTHES are coloured with ONE red pencil (a warm true red, like a Prismacolor crimson red).
* strokes run diagonally in one main direction
* the paper tooth shows through every stroke
* dark garments: dense, heavy red pressure
* light garments: lighter red strokes, with paper showing
* patterns (stripes, prints) stay readable as red-dense vs red-light areas
* fold lines in the clothes can be drawn in red
Red NEVER goes on faces, skin or hair.
Do NOT flood-fill the red; it must look hand-coloured.
TORN PAPER CUT-OUT
Cut each person out along their silhouette.
The cut edge is torn by hand:
* irregular, slightly jagged
* a white paper rim of uneven width (thin in places, thicker in others)
* tiny paper fibres at the edge
* a soft drop shadow offset down-right onto the photo
NO perfect mask.
NO clean vector edge.
RED PENCIL CONTOUR
Around the paper edge, add a hand-drawn RED pencil line:
* broken into short strokes with small gaps
* sometimes doubled
* slightly outside or on the paper edge, never perfectly registered
* grainy, like pencil on paper
BACKGROUND RULES
The background stays the ORIGINAL colour footage, a touch richer in saturation.
Do NOT sketch, blur or repaint the room.
The contrast between the drawn people and the photographic room IS the style.
OBJECT CONTINUITY
If a person holds an object, draw the object in graphite (red only if it is clothing-like).
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
the cut-out follows.
NO floating cut-out.
NO previous-frame silhouette.
NO delayed outline.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel separately drawn by hand.
Allow between consecutive frames:
* hatching strokes to be redrawn (same direction, new strokes)
* red pencil strokes to be redrawn
* the torn paper edge to wobble
* the white rim width to vary
* the red contour strokes to break in different places
* paper grain to change
Keep FIXED in every frame:
* the hatching directions
* the red hue
* the background footage
Do NOT make the boil so strong that faces flicker or change.
DO NOT
Do NOT turn the people into cartoons or anime.
Do NOT put red on faces, skin or hair.
Do NOT use any colour other than graphite and ONE red inside the cut-out.
Do NOT use a smooth digital sketch filter.
Do NOT flood-fill clothing with flat red.
Do NOT make clean vector outlines.
Do NOT sketch or desaturate the background.
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
* NO sketching
* NO red pencil
* NO paper cutting
* NO outlines
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
Do NOT begin the mixed-media transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – MIXED-MEDIA SKETCH STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input.
For consistency, also give the first approved styled frame as a style reference for all later frames (same hatching angle, same red, same paper).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, red-on-skin, or the style rules broke — regenerate those frames only.
The final video must feel like HAND-DRAWN PAPER PEOPLE moving through a REAL COLOUR WORLD: graphite faces, red-pencil clothes, torn white edges, every frame drawn again.
The image should deliberately contain:
* graphite hatching and cross-hatching
* red coloured-pencil strokes with paper tooth
* recognizable faces kept in graphite
* torn white paper rims
* soft drop shadows
* broken red pencil contours
* untouched colour footage behind.
Avoid a smooth digital sketch filter.
```
