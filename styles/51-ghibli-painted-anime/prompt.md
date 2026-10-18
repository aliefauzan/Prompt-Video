# 51 — Ghibli Painted Anime

**Look:** A Studio Ghibli film still in motion. The room becomes a hand-painted poster-colour (gouache) background with soft edges, gentle brush texture and a warm afternoon light. Through the window there is a painted summer sky with big cumulus clouds (white tops, lavender bellies) and lush green tree canopy. The people are soft cel characters: flat colour fills, one gentle shadow tone, a hair sheen, and thin warm-brown line art (not black). Faces stay simple and kind, with natural proportions: no big anime eyes, no speed lines and no glossy highlights. The background is held still like a painted plate, and only the cels move.

**Also called / where it trends:** "Ghibli style", "Studio Ghibli filter", "Ghibli AI video", "Miyazaki style", "Ghiblify", "Ghibli trend" (the 2025 GPT-4o image wave, then video filters). It is a standard preset on AI video tools: frameloop.ai (Ghibli Style), VidGuru, Pollo AI and WaveSpeed all ship Ghibli video filters. This style differs from `10-anime-cel-shade`: 10 is a modern TV-anime cel look with hard two-tone shading and black lines. 51 is a painted Ghibli film look: a gouache background with a painted sky and foliage, warm natural light, soft cels and sepia lines.

**References:**
- https://frameloop.ai/visual-styles: frameloop's style library (public grid; per-style links go to a sign-in page, which was not used). `refs/ref_1.png` is the **Ghibli Style** card. frameloop's own style prompt, credited verbatim: "Studio Ghibli style, anime movie still, lush watercolor background, soft lighting, whimsical atmosphere, highly detailed environment, Hayao Miyazaki aesthetic". The prompt below expands it into the staged invideo / Seedream frame-by-frame workflow of the Punk Photocopy Collage prompt (`_source/reference_prompt_punk_collage.txt`).
- https://www.ghibli.jp/works/totoro/ (`refs/ref_2.png`): Studio Ghibli's official still images for *My Neighbor Totoro*, which Ghibli offers for use "within common sense". They are the look reference: painted skies and foliage, soft cels, warm light.
- Also seen: https://www.vidguru.ai/video-effects/ghibli-video-filter, https://pollo.ai/video-effects/ai-studio-ghibli-effect, https://wavespeed.ai/models/wavespeed-ai/ghibli-filter/video (Ghibli video filters).

**Example:** `example.png` (six frames of the test clip) and `before_after.png` (frame 049). This is a local approximation, not Seedream output, made with `render.py` (numpy + OpenCV):
- The background is mean-shift flattened at half resolution, graded greener and warmer, given soft LIC brush texture and paper grain, and washed with a slow warm/cool drift.
- The window glass (found from the bluish blinds, filled to its convex hull) is replaced by a painted sky: a blue gradient, 7 cumulus clusters with flat bottoms and lavender shading, and a fbm tree canopy.
- People are mean-shift cels with one soft shadow tone (reduced on skin), a hair sheen, thin XDoG lines, dark facial-feature blobs and a 2 px silhouette, all in warm sepia ink.
- The finish adds a warm window glow, bloom and light grain.

## Prompt

```text
I'm uploading one video clip. Convert it into a frame-by-frame STUDIO GHIBLI–STYLE PAINTED ANIME film, gouache backgrounds, soft cel characters, warm natural light, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Every frame becomes a still from a hand-made Ghibli-style feature film:
* the room repainted as a POSTER-COLOUR / GOUACHE background painting
* soft painted edges, gentle visible brush texture, no photographic detail
* lush, natural colour: warm creams, sunlit wood, rich greens, clear sky blues
* windows open onto a painted SUMMER SKY with big cumulus clouds and green tree canopy
* warm, soft afternoon light with gentle bloom where the light comes in
* people as SOFT CEL characters: flat colour fills + ONE soft shadow tone
* thin, warm sepia-brown line art (never heavy black)
* simple, kind faces with natural proportions
* a calm, whimsical, nostalgic atmosphere
The result should feel like someone:
PAINTED THE ROOM AS A GOUACHE BACKGROUND
→ PAINTED A SUMMER SKY INTO THE WINDOW
→ TRACED EACH PERSON ONTO A CEL IN THIN BROWN LINE
→ PAINTED THE CELS WITH FLAT COLOURS AND ONE SOFT SHADOW
→ LAID THE CELS OVER THE PAINTED BACKGROUND
→ SHOT THEM UNDER WARM LIGHT
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — GHIBLI CEL
The people become soft, hand-painted anime cels that keep the photograph's structure.
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
Keep natural proportions: NO big anime eyes, NO chibi, NO exaggerated features.
Keep facial proportions, eye shape, glasses and hairline exact.
CEL RULES
* flat colour fills, softened by the film's gentle grain
* ONE soft shadow tone, slightly cooler and more violet than the base colour
* very little shadow on faces; faces stay light and open
* a simple soft sheen band on dark hair
* eyes, brows and mouth as small, simple dark shapes
* thin, even, warm sepia-brown outline; a slightly stronger outer contour
BACKGROUND PAINTING RULES
The room keeps its exact layout, furniture and perspective but is repainted:
* broad gouache areas with soft edges
* subtle brush texture and paper grain
* walls, wood and furniture simplified into painted shapes
* NO black outlines in the background
* plants become lush painted foliage
* screens and posters become simple painted colour panels
The background is HELD: it is one painting under the moving cels.
WINDOW / SKY RULES
Any window or bright opening shows a painted Ghibli summer sky:
* clear blue gradient sky
* big stacked cumulus clouds: bright white tops, soft lavender-grey undersides, flat bottoms
* a band of lush green tree canopy in front
The sky must look painted, not photographic.
LIGHT RULES
Warm, natural, late-afternoon light:
* a soft warm glow from the window side
* gentle bloom on the brightest areas
* no harsh contrast, no neon, no dramatic darkness
OBJECT CONTINUITY
If a person holds an object, paint the object as part of the cel, with the same line and fills.
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
The look is a calm, polished film, so the boil is GENTLE.
Allow between consecutive frames:
* tiny line-thickness variation on the cels
* subtle film-grain change
Keep FIXED in every frame:
* the background painting (identical, held still)
* the sky and clouds
* every character's colours and shadow tone
* the line colour
Do NOT let faces, colours or the background flicker.
DO NOT
Do NOT use big anime eyes, chibi proportions or sparkle highlights.
Do NOT use heavy black outlines.
Do NOT use modern TV-anime hard two-tone shading or glossy highlights.
Do NOT add speed lines, effects or text.
Do NOT leave any photographic detail.
Do NOT make it neon, dark or gritty.
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
* NO painting
* NO cel shading
* NO sky replacement
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
Do NOT begin the Ghibli transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – GHIBLI PAINTED ANIME STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Give Seedream the current extracted frame as the image input.
For consistency, also give the first approved styled frame as a style reference for all later frames (same background painting, same sky, same line colour, same character colours).
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, or the style rules broke (photo detail, anime eyes, background change, colour flicker) — regenerate those frames only.
The final video must feel like a WARM, HAND-PAINTED GHIBLI FILM SCENE: a held gouache background, a painted summer sky, soft cel people moving through warm light.
The image should deliberately contain:
* a gouache-painted room with soft edges and brush texture
* a painted summer sky with cumulus clouds and green canopy in the window
* soft cel people with one gentle shadow tone
* thin warm-brown line art
* warm natural light and gentle bloom
* natural, recognizable faces.
Avoid a generic anime filter.
```
