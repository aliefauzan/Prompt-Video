# 52 — Retro 90s Cartoon

**Look:** A 1990s TV cartoon episode taped off broadcast. The people become flat cel characters with a small, fixed set of paints: one skin paint, one paint per garment and hair, one hard shadow tone and a few hard highlights. They have thick, wobbly black ink outlines and simple solid-black eyes, brows and mouths. Behind them the room is a separately painted background plate in a muted 90s production palette (mustard, teal, brick, dusty purple, cream), with soft gouache texture and slightly wonky perspective. The ink lines boil every frame, dust and hairs sit on the cel for a few frames, and the whole image has standard-definition softness, chroma bleed and a sharpening halo.

**Also called / where it trends:** "90s cartoon", "90s cartoon filter", "Nicktoons style" (Rugrats, Hey Arnold!, Doug, Rocko's Modern Life, Daria), "retro cartoon edit", "vintage 2D cel animation", "Saturday morning cartoon", "90s anime / retro anime" (the same TV-cel era in Japan). It is a preset on AI video tools: frameloop.ai (Retro 90s Cartoon), Media.io's retro anime video generator, and many "90s cartoon edit" prompt pages.

**References:**
- https://frameloop.ai/visual-styles: frameloop's style library (public grid; per-style links go to a sign-in page, which was not used). `refs/ref_1.png` is the **Retro 90s Cartoon** card (its sample is a 90s TV-anime cel). frameloop's own style prompt, credited verbatim: "90s animation style, vintage 2D cel animation, hard cel shading, distinct shadow layers, bold black outlines, high contrast, hand painted background, standard definition". The prompt below expands it into the staged invideo / Seedream frame-by-frame workflow of the Punk Photocopy Collage prompt (`_source/reference_prompt_punk_collage.txt`).
- https://prompt-metadigital.com/prompt/90s-cartoon-edit (`refs/ref_2.png`): a "90s cartoon edit" prompt for a 1990s Nickelodeon-style look (Rugrats / Hey Arnold! / Rocko). It specifies thick uniform black outlines, flat saturated slightly muted colours, hard-edged shadows, and warped wobbly-perspective backgrounds in mustard / teal / brick red / olive / dusty purple. Those are the palette and line notes used here.
- Also seen: https://www.media.io/ai/explore/zone/retro-anime-video-generator (retro anime / 90s cel video generator).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV), working at 810×540 (SD) and then upscaled:
- **Cel colour model:** one fixed palette for the whole clip, learned once with k-means on 4 frames (lightness weighted low, so each garment is one paint), with near-duplicate paints merged and chroma ×2.1. Every frame is matched to it, despeckled, and small paint islands are absorbed into the surrounding paint. All skin-tone paints are folded into one fixed skin paint.
- **Cel shading:** one hard shadow layer with no ink on its edge, and hard highlights.
- **Ink:** only between clearly different paints (not on skin), solid-black facial features, and a thick silhouette line. The ink is displaced by a new noise field every frame (line boil), and paint gain flickers slightly.
- **Background:** posterised, mapped part-way through a mustard / teal / brick / dusty-purple ramp, then warped slightly.
- **Tape finish:** cel dust and hairs that live for about 5 frames, then SD chroma bleed, a sharpening halo and grain.

## Prompt

```text
I'm uploading one video clip. Convert it into a frame-by-frame RETRO 1990s TV CARTOON: flat cel characters with thick black outlines over a painted background, taped off standard-definition TV, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame becomes a frame of a 1990s hand-made TV cartoon:
* people as FLAT CEL characters, painted with a SMALL fixed set of paints
* ONE paint per area (skin, each garment, hair) + ONE HARD shadow tone + a few hard highlights
* THICK, slightly WOBBLY BLACK ink outlines, heavier on the outer contour
* simple solid-black eyes, brows and mouth
* the room as a separately PAINTED BACKGROUND: soft gouache, muted 90s palette (mustard, teal, brick red, olive, dusty purple, cream)
* slightly wonky, hand-drawn perspective in the background
* NO black outlines in the background
* tiny cel dust specks and hairs
* standard-definition TV softness, colour bleed and a slight sharpening halo
The result should feel like someone:
TRACED EACH PERSON ONTO A CEL IN THICK BLACK INK
→ PAINTED THE CEL ON THE BACK WITH A FEW FLAT PAINTS
→ ADDED ONE HARD SHADOW LAYER
→ PAINTED THE ROOM AS A SEPARATE BACKGROUND
→ SHOT THE CELS OVER THE BACKGROUND ON FILM
→ BROADCAST IT ON 90s TV
→ RECORDED IT ON VHS
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — 90s CEL
The people become 90s TV cartoon characters that keep the photograph's structure.
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
Simplify, do not redesign: same face shape, same hairstyle silhouette, same clothes.
Keep glasses, hairline and proportions recognizable.
CEL PAINT RULES
Use a FIXED colour model per character, the same paints in every frame:
* ONE skin paint
* ONE paint per garment, ONE for the hair
* ONE hard-edged shadow tone per paint (darker, slightly cooler)
* hard-edged highlights only on the brightest areas
* NO gradients, NO soft airbrush, NO texture inside the fills
* stripes and patterns simplified into a few flat shapes
Colours are saturated but slightly muted, like 90s cel vinyl paint.
INK RULES
* thick black outer contour, uneven like a brush pen
* thinner black inner lines where two different paints meet
* NO ink lines on shadow edges
* solid black eyes, brows and mouth
* the lines wobble and boil from frame to frame
BACKGROUND RULES
The room keeps its exact layout but becomes a painted background plate:
* soft gouache, slight brush texture
* muted 90s palette: mustard, teal, brick red, olive, dusty purple, cream
* simplified shapes, gently wonky perspective
* NO black outlines in the background
* held still: one painting under the moving cels
TV / VHS FINISH
* standard-definition softness
* colour bleeding slightly sideways
* a light sharpening halo along edges
* fine video grain
* small dust specks and hairs that sit on the cel for a few frames
NOT a modern HD cartoon. NOT flash / vector animation.
OBJECT CONTINUITY
If a person holds an object, draw the object on the cel with the same ink and flat paint.
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
The cel must match the source frame exactly in position, pose and timing.
If the head moves:
the cel follows.
If the hand moves:
the cel follows.
If the body turns:
the cel follows.
NO floating figure.
NO previous-frame silhouette.
NO delayed outline.
FRAME-BY-FRAME BOILING EFFECT
THIS IS CRITICAL.
Every frame should feel re-inked by hand.
Allow between consecutive frames:
* the black outlines to wobble and change thickness slightly
* tiny paint-gain flicker
* cel dust and hairs to appear and disappear every few frames
* video grain to change
Keep FIXED in every frame:
* every character's paint colours (same skin, same clothes)
* the background painting
* the outline colour (black)
Do NOT make the boil so strong that faces flicker or change.
DO NOT
Do NOT use gradients or soft shading inside the cels.
Do NOT use modern clean vector lines or flash animation.
Do NOT use 3D or CGI rendering.
Do NOT put black outlines on the background.
Do NOT change a character's paint colours between frames.
Do NOT leave any photographic detail.
Do NOT make it HD-sharp.
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
* NO cel paint
* NO outlines
* NO VHS / TV effects
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
Do NOT begin the 90s cartoon transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – RETRO 90s CARTOON STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input.
For consistency, also give the first approved styled frame as a style reference for all later frames (same paints for every character, same background painting, same line weight).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, or the style rules broke (colour drift, gradients, photo detail, lost outline) — regenerate those frames only.
The final video must feel like a 1990s TV CARTOON taped off broadcast: flat cel people with thick wobbly black lines moving over a painted background, softened by standard-definition video.
The image should deliberately contain:
* flat cel paint with one hard shadow tone
* thick wobbly black outlines
* solid black facial features
* a muted 90s painted background
* cel dust and hairs
* SD softness, colour bleed and grain
* recognizable people.
Avoid a modern clean vector cartoon.
```
