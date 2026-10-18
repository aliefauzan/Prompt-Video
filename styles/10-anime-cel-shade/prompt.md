# 10 — Anime Cel Shade

**Look:** the clip redrawn as a 2D TV-anime cel: flat colour fields with one cool shadow tone and one highlight tone, clean dark line art, big glossy anime eyes and cheek blush placed on the real faces, a soft painted background with the window turned into a blue anime sky with cel-shaded cumulus clouds, and manga focus / speed lines behind the subject on fast moves.

**Also called / where it trends:** "real life to anime", "anime filter", "turn yourself into anime", "AI anime edit", "Ghibli filter", "90s cel-shaded anime" (TikTok, YouTube Shorts, Instagram Reels; CapCut / Seedream / Runway / Kling "video to anime" templates). Creators post a split-screen or wipe from the real clip into the anime version.

**References:**
- https://www.youtube.com/shorts/_dnTWl8IcHM — "Anime Filter, Real Life to Anime" split-screen wipe; flat skin, line-art eyes, painted room (refs/ref_3.png)
- https://www.youtube.com/shorts/zL2KTDzzfmc — "90s Cel-Shaded Anime Style" deep dive; hard 2-tone shadows, inked outlines (refs/ref_2.png)
- https://www.youtube.com/results?search_query=real+life+to+anime+AI+video+filter+cel+shaded — Shorts grid of the trend: split before/after, Ghibli filter, live-action-to-anime (refs/ref_1.png)
- https://www.youtube.com/shorts/syoDuRhwC28 — "Create Viral Realistic AI Anime Videos in CapCut (Seedream 5.0 Pro)" — same model as the tool lock
- https://www.youtube.com/shorts/NB9imNNga9M — "This AI Filter Turns You Into a Ghibli Character" (trend example)
- https://www.youtube.com/watch?v=3W-wWCjRWms — "Cell Shading Smoke — anime-style overlays" (cel shading vocabulary for effects)
- https://morphic.com/resources/tools/video-to-anime , https://riffkit.ai/blog/video-to-anime-converter — "video to anime" tools; same shots and cuts, style-only change
- https://github.com/TachibanaYoshino/AnimeGANv2 — classic photo/video-to-anime model (flat colours + lines, painted backgrounds)

**Example:** `example.png` (6 frames of the test clip), `before_after.png`. Local approximation in `render.py` (mean-shift + k-means cel regions with one shadow/highlight split, DoG line art, Apple Vision face landmarks for anime eyes/brows/mouth via `faces.swift`, painted background, generated sky, focus lines when the masks move fast). All 179 frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a hand-painted 2D ANIME CEL frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.

TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.

CORE VISUAL STYLE
Transform the footage into a Japanese TV-anime / anime-film still built from:
* flat cel colour fields
* 2–3 tone shading only: BASE, one SHADOW, one HIGHLIGHT
* hard-edged cel shadow shapes (no soft airbrush gradients on characters)
* cool lavender / blue-violet shadow tint
* clean dark line art of even weight
* slightly heavier outer contour around each character
* anime eyes: dark upper lash line, iris with a white catchlight
* soft pink cheek blush
* simplified nose and mouth
* painted, softly blended background art
* a bright blue anime sky with white cel-shaded cumulus clouds
* manga focus lines / speed lines on fast motion
* gentle highlight bloom (compositing glow)
* clean, slightly saturated anime colour
The result should feel like someone:
PRINTED THE VIDEO FRAME
→ TRACED EVERY PERSON IN CLEAN INK ON A CEL
→ FILLED THE CEL WITH FLAT PAINT
→ ADDED ONE SHADOW AND ONE HIGHLIGHT SHAPE PER COLOUR
→ PAINTED THE ROOM AND SKY AS A SEPARATE BACKGROUND
→ LAID THE CEL OVER THE BACKGROUND
→ SHOT IT ON THE ANIMATION STAND
→ ANIMATED IT FRAME-BY-FRAME.

CHARACTER — ANIME CEL
Every person becomes an anime character drawn ON TOP OF their exact footage pose.
Preserve each person's exact:
* identity
* face shape
* expression
* hairstyle and hair length
* clothing and clothing pattern (stripes stay stripes, batik stays a patterned shirt)
* glasses and accessories
* skin tone (lighten and clean it, do not change ethnicity)
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT invent a new character.
Do NOT change age, gender or body type.
Do NOT make chibi / super-deformed proportions.
The person must stay instantly recognizable as the same person in the footage, just drawn as anime.

CEL SHADING (2–3 TONES)
Every colour region gets:
* one flat BASE colour
* one SHADOW shape (base multiplied by a cool lavender tint)
* optionally one small HIGHLIGHT shape (base lightened), mainly on hair, cheeks, shoulders, folds
Shadow shapes follow the REAL lighting of the footage:
* under the hair fringe
* under the chin and on the neck
* under the arms and on the shirt folds
* on the side of the face turned away from the window
Shadow edges are HARD and CLEAN.
No gradients, no photo texture, no skin pores, no noise inside a cel region.

LINE ART
* thin, clean, even ink lines in very dark plum-brown (not pure black)
* slightly heavier outer contour around each character
* inner lines only where an animator would draw them: hairline and hair clumps, jaw, ears, collar, sleeves, folds, fingers
* glasses frames drawn as clean lines
* NO sketchy, hatched or doubled lines
* NO thick comic-book outlines

ANIME FACE
Keep the real face position and expression from the footage, then draw it the anime way:
* eyes slightly enlarged, with a heavy dark upper lid / lash line, thin lower lid
* dark iris with a darker pupil and ONE white catchlight dot
* closed or smiling eyes become a single curved line
* simple strong eyebrows
* nose as a tiny tick or small shadow
* mouth as a simple line; an open mouth becomes a flat dark-rose shape
* soft pink blush ovals under the eyes
Do NOT replace the face with a generic anime face.
The eye spacing, face shape, smile and expression must match the footage.

SKIN AND HAIR
* skin: ONE clean light tone per person + one cel shadow (lavender-rose), no texture
* hair: deep dark base, clumped into anime hair strands at the edges, one cool sheen highlight band
* keep each person's real skin tone family; anime cleans it, it does not whiten it

BACKGROUND — PAINTED
The room stays in the same place but is repainted as anime BACKGROUND ART:
* softly blended painted surfaces (wood panels, wall, plants, screen, chair)
* fewer details, simplified shapes, light ink only on major edges
* airy, slightly cool, saturated colour
* backgrounds may keep soft gradients; ONLY the characters are flat cels
BRIGHT WINDOWS / OVEREXPOSED AREAS → ANIME SKY
Replace blown-out windows with a saturated blue anime sky:
* gradient from deep blue at the top to pale blue near the horizon
* big white cumulus clouds with flat lavender cel shadows on their undersides
* clouds drift very slowly from frame to frame
Keep window frames, blinds and the screen in place.

FOCUS / SPEED LINES
When a person moves fast toward or across the camera (hand reaching out, leaning in, head turning):
* add white manga focus lines radiating from the frame edges toward the subject, or
* add parallel speed lines behind the moving limb
These lines sit BEHIND the characters, never over faces.
They appear only on fast moments and disappear when the motion calms.

COLOUR RULES
Keep the palette anime-clean:
* skin: light peach / warm beige families, rose shadows
* hair: near-black / deep brown with cool sheen
* clothes: their real colours, cleaned and slightly more saturated
* shadows: always tinted cool (lavender / blue-violet), never grey or muddy
* sky: saturated cerulean + pure white clouds
Do NOT introduce random neon colours.
Do NOT desaturate into a grey look.

LAYER ORDER
PAINTED BACKGROUND + ANIME SKY
↓
FOCUS / SPEED LINES (only on fast motion)
↓
CHARACTER CELS (flat base + shadow + highlight)
↓
LINE ART + FACE DRAWING
↓
SOFT HIGHLIGHT BLOOM.

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
Draw the object in the same cel style, in the same place, moving exactly with the original action.
Do NOT drop objects while redrawing the character.

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
the drawing follows.
If the hand moves:
the line art follows.
If the body turns:
the cel shapes follow.
NO floating outlines.
NO previous-frame silhouette.
NO delayed line art.

ON-MODEL CONSISTENCY (LIGHT LINE BOIL ONLY)
Anime is CLEAN. The drawing must stay ON MODEL from frame to frame.
Allow only:
* line weight to vary very slightly (hand-inked feel)
* shadow shape edges to shift a few pixels as the light on the body changes
* clouds to drift slowly
* focus lines to be redrawn every frame (they flicker, as in real anime)
Do NOT let colours, eye size, face shape or palette change between consecutive frames.
Do NOT let the background repaint itself differently every frame.

DO NOT
Do NOT make it photographic.
Do NOT use a generic cartoon or oil-painting filter.
Do NOT use posterized photo blotches; cel regions must be clean designed shapes.
Do NOT add skin texture, pores or photo noise inside the cels.
Do NOT use soft airbrush shading on characters.
Do NOT make 3D / Pixar / CGI rendering.
Do NOT make chibi or exaggerated proportions.
Do NOT replace the person's face or change identity.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing.
Do NOT add text, logos or subtitles.
Do NOT add neon glow, glitch or film grain.
It must feel like a CLEAN, HAND-INKED, HAND-PAINTED ANIME CEL.

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
* NO anime conversion
* NO line art
* NO cel shading
* NO sky replacement
* NO speed lines
* NO colour changes
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
Do NOT begin the anime transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.

STAGE 3 – ANIME CEL EVERY FRAME (ONLY AFTER MY CONFIRMATION)
1. Restyle EVERY extracted frame individually with Seedream 5.0 Pro, using that exact original frame as the image reference.
2. Keep each output at the source resolution and framing. No crop, no zoom, no reframing.
3. Replace each clip on the timeline IN PLACE with its anime version. Same order. Same 1/12 second duration.
4. Lock the style sheet before generating: the same skin tone, hair colour, line colour, shadow tint, eye design and clothing colours for each person in EVERY frame. Re-use the same wording for every frame prompt.
5. Lock the background: the same painted room and the same sky; only the clouds drift slowly.
6. Add focus / speed lines only on frames with fast motion.
7. Check every 12th frame against the original: same pose, same expression, same position. Regenerate any frame that is off-model or off-pose.
8. Export at the original duration with the original audio.
```
