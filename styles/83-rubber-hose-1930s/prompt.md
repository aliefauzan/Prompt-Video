# 83 — Rubber-Hose 1930s Cartoon

**Look:** The clip becomes an early-1930s black-and-white theatrical cartoon. The people are inked cels in just four flat paints: white faces and hands, solid inkblot-black hair and dark clothes with white shine ticks, and two flat greys. Thick black brush outlines run around every figure. The figures move with a rubbery "noodle" wave, and the grey watercolour room behind them sways and squashes on a two-beats-a-second rhythm. On top: film flicker, vertical scratches, dust, grain, a rounded academy gate, a heavy vignette, an iris-in at the start and an iris-out at the end.

**Also called / where it trends:** "rubber hose animation", "rubber hose style", "1930s cartoon", "Fleischer style", "Steamboat-era cartoon", "inkblot cartoon", "Cuphead style / Cuphead filter", "old cartoon filter", "vintage cartoon AI". It trends as TikTok AI-filter edits (often tagged with Cuphead) and on AI video generators that sell it as a preset; Morphic has a "Rubber Hose Animation AI Videos" landing page. There is also a long-running rubber-hose revival among illustrators on Instagram.

**References:**
- https://morphic.com/resources/videos/rubber-hose-animation-videos (screenshot `refs/ref_1.png`): Morphic's "Rubber Hose Animation AI Videos" page, with bendy-limbed mascot presets (from D3).
- https://en.wikipedia.org/wiki/Rubber_hose_animation (screenshot `refs/ref_2.png`): what defines the style. Limbs are drawn as flowing curves with no joints, everything moves in curving motion, and it was standard in late-1920s / 1930s American studios (Fleischer, early Disney, Felix, Oswald).
- https://www.tiktok.com/@xbus2604103358/video/7667576183491448094 and https://www.tiktok.com/@remycoup/video/7360735006718774570: TikTok "Cuphead 1930s rubber hose" AI-filter edits. They show rubber limbs, pie eyes, watercolour backgrounds, film scratches and flicker (from D1).
- https://en.wikipedia.org/wiki/Cuphead: the modern game that brought the look back, with hand-inked 1930s-style cels over painted watercolour backgrounds.

How it differs from the styles already in the library: **28 Hand-Cranked Silent Film** keeps the people PHOTOGRAPHIC and only adds the B/W film damage. **52 Retro 90s Cartoon** is a colour 90s TV cartoon. **18 Pencil Sketch** is graphite on paper. This style redraws everyone as flat inked cartoon cels with inkblot blacks and white faces, puts them in a grey watercolour set that dances on the beat, and frames it with an iris.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). The people are quantised into four flat paints, with skin forced to white and the darks to inkblot black. White shine ticks come from local highlights inside the blacks. Ink is drawn on paint boundaries, facial features and a thick silhouette, and it boils each frame. A small travelling sine warp gives the "noodle" wave. The room is five posterised grey washes with pooled pigment edges and paper grain, warped so it leans and squashes on a 6-frame beat. On top: flicker, gate weave, scratches that live 3–5 frames, dust, hairs, grain, vignette, a rounded 1.37:1 gate, and the iris at both ends. Pie eyes and real noodle limbs need a generative model: the prompt asks for them, the local render only hints at them.

## Prompt

```text
I'm uploading one video clip. Convert it into a 1930s RUBBER-HOSE CARTOON frame-by-frame animation: every frame should look like a frame from a black-and-white theatrical cartoon of around 1930-1934, hand-inked on cels over a painted watercolour background and printed on old film, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
1930s rubber hose animation, black and white vintage cartoon, Fleischer-era inkblot characters, flowing jointless limbs, pie-cut eyes, thick brush ink outlines, grey watercolour background, old film print with scratches and flicker.
Transform the footage into a 1930s cartoon frame built from:
* BLACK AND WHITE only (a faint warm silver tone is allowed)
* FOUR flat paints on the characters: black, dark grey, light grey, white
* WHITE faces and hands (classic rubber-hose characters have white faces)
* SOLID INKBLOT BLACK hair and dark clothes, with a few small white shine ticks
* THICK, smooth BLACK BRUSH OUTLINES around every figure, thinner inner lines
* RUBBER-HOSE limbs: arms and legs drawn as smooth flowing tubes, no visible elbows or knees
* PIE-CUT EYES (black oval pupils with a wedge cut out) placed on the real eye positions
* a GREY WATERCOLOUR background: soft washes, pooled pigment edges, paper grain, no outlines
* everything in the set gently BOUNCING on the beat
* FILM DAMAGE: flicker, vertical scratches, dust, hairs, grain
* a heavy vignette, a ROUNDED ACADEMY GATE (1.37:1)
* an IRIS-IN at the first frames and an IRIS-OUT at the last frames
The result should feel like someone:
DREW EVERY FRAME IN PENCIL WITH RUBBERY CURVES
→ INKED IT ONTO CELS WITH A THICK BRUSH
→ PAINTED THE CELS BLACK, GREY AND WHITE
→ LAID THEM OVER A GREY WATERCOLOUR BACKGROUND
→ SHOT THEM ON BLACK-AND-WHITE FILM
→ RAN THE PRINT THROUGH A PROJECTOR FOR NINETY YEARS
→ RELEASED IT FRAME-BY-FRAME.
CHARACTER — RUBBER-HOSE CEL
Redraw each person as a 1930s cartoon character, but keep them unmistakably the SAME person.
Preserve the person's exact:
* identity (face shape, glasses, hairstyle silhouette)
* expression
* hairstyle
* glasses (drawn as two bold round rims)
* clothing and its pattern (stripes stay stripes, the batik becomes a simple black-and-grey pattern)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Faces and hands are painted WHITE with black ink features.
Eyes become pie-cut eyes in the real eye positions, looking the same way as the real eyes.
Mouths stay the real mouth shape, drawn as a bold black line or black shape.
Limbs follow the real pose exactly, but drawn as smooth, bendy tubes with no sharp joints.
Do NOT turn the people into animals, mascots or famous cartoon characters.
Do NOT add gloves, tails, ears or shoes that are not in the source.
CEL PAINT
* White (faces, hands, white stripes): clean paper white.
* Light grey: light clothing.
* Dark grey: mid-tone clothing.
* Black: hair, dark clothing, dark trousers, shadows under the chin.
* NO gradients on the cels. Every paint is flat.
* Black areas get 1-3 small white shine ticks (curved highlight strokes), like 1930s inkblot characters.
* Same paint for each garment on every frame.
INK LINES
* Thick, smooth, rounded black brush lines with a little weight variation.
* Outer silhouette thickest; inner lines (collar, sleeves, stripes, glasses, features) thinner.
* NO lines in the background painting.
BACKGROUND — GREY WATERCOLOUR SET
* Keep the SAME room layout: window, plant box, cupboards, screen, chair, perspective.
* Repaint it as a grey watercolour background: 4-5 soft grey washes, darker pooled pigment at the edges of each wash, visible paper grain.
* Lower contrast than the characters, so the black-and-white cels pop.
* The set gently DANCES: walls, window, furniture and plants lean left and right and squash slightly on a steady beat (about two bounces per second), as in 1930s musical cartoons.
* The bounce is small and smooth; the room never changes shape permanently.
FILM PRINT
* Frame-to-frame flicker of brightness (±5%).
* Thin vertical scratches, white or black, that stay for a few frames and drift.
* Dust specks (white and black) and the odd hair, one frame each, never on faces.
* Coarse grain over everything.
* Small gate weave (1-2 px).
* Heavy vignette and a rounded-corner academy gate (1.37:1) with black outside it.
* An IRIS-IN over the first ~10 frames and an IRIS-OUT over the last ~10 frames: a black circle closing in on (or opening from) the middle of the scene.
PALETTE
Black, white, two flat greys. A faint warm silver tone on the whole print.
Do NOT use any colour.
OBJECT CONTINUITY
If the character holds an object, it is inked and painted on the same cel, attached to the hand.
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
The characters must match the source frame exactly: same silhouette, pose and position.
The background follows the real camera movement of the source, plus the gentle beat bounce.
NO cel left behind from a previous frame.
NO character drifting away from the real pose.
FRAME-TO-FRAME CARTOON LIFE
THIS IS CRITICAL.
It must feel like hand-inked 1930s animation running on old film, not a still filter.
Allow between consecutive frames:
* ink lines to boil by 1-2 px
* a gentle rubbery wave travelling through limbs and bodies
* the set to bounce on the beat
* new grain, dust and flicker every frame
* scratches to stay a few frames, then move on
Keep FIXED:
* the four paints of every garment
* the white faces and the black hair
* the gate shape and vignette
* the beat tempo
DO NOT
Do NOT keep the people photographic (that would be a silent-film look, not a cartoon).
Do NOT use colour, sepia-brown or Technicolor.
Do NOT use pencil-sketch texture or hatching on the characters.
Do NOT use modern clean vector lines or digital gradients.
Do NOT make it a 90s TV cartoon.
Do NOT add famous cartoon characters, logos or title cards.
Do NOT turn people into animals.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT replace the person's face.
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
* NO black-and-white conversion
* NO inking or cel paint
* NO watercolour background or bounce
* NO film damage, gate or iris
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
Do NOT begin the rubber-hose cartoon transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – RUBBER-HOSE CARTOON STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the paint (black / dark grey / light grey / white) you will give each garment and each person's hair, the beat tempo of the set bounce, and which frames get the iris-in and iris-out.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Keep the same paints, background painting, gate and film treatment on every frame; only the bounce phase, boil, damage and iris change.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, paints, the bounce rhythm or the iris broke — regenerate those frames only.
The final video must feel like A 1930s RUBBER-HOSE CARTOON ON A WORN PRINT: white faces, inkblot blacks, thick brush lines, a dancing grey watercolour room, flicker and scratches, iris in and out, 12 frames per second.
The image should deliberately contain:
* black-and-white flat cel paint (four paints only)
* white faces and hands, inkblot-black hair with shine ticks
* thick black brush outlines
* a grey watercolour background that bounces on the beat
* film flicker, scratches, dust and grain
* a rounded academy gate and vignette.
Avoid photographic people.
```
