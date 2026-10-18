# 59 — 3D Kawaii Chibi

**Look:** every frame becomes a soft 3D kawaii toy render, Pixar-like: the people turn into ultra-cute chibi versions of themselves — big round heads (head inflated about 1.5x on the same body), large glossy dark eyes with two white catchlights, rosy blush, smooth clay-plastic skin and clothes with no pores or fabric noise, simplified pastel colours. Warm sun-drenched golden light with lilac fill, a gentle golden rim glow and soft specular highlights; the room melts into a dreamy pastel soft-focus background with round bokeh discs, sun haze and bloom. Not stop-motion clay: no fingerprints, no wobble, no matte plasticine — it is a clean, glowing CG miniature.

**Also called / where it trends:** "3D kawaii chibi", "chibi 3D render", "Pixar style filter", "3D cartoon me", "mini-me figure", "AI 3D figurine / toy figure trend", "Disney Pixar AI edit" — AI image/video style presets (frameloop, Dreamina, LogoAI mini-me, Tomoviee 3D figure), Pinterest 3D chibi figurine boards, TikTok / Reels "turn yourself into a 3D chibi" edits (2026).

**References:**
- https://frameloop.ai/visual-styles — Frameloop "3D Kawaii Chibi" visual style card, screenshot `refs/ref_1.png`. Frameloop's own style prompt: *"3D kawaii chibi render, smooth clay-like textures and ultra-cute proportions, warm sun-drenched color palette with golden yellows and soft pastels, whimsical volumetric lighting with a gentle glow, dreamy soft-focus background, high-detail miniature aesthetic."* Its sibling card "Pixar Style": *"3D animated movie still, Pixar style, Disney animation, vibrant color palette, soft shadows, volumetric lighting, octane render, Unreal Engine 5, cinematic depth of field"* (this prompt credits and expands both into the full video workflow below; the cards' "try it" links go to a sign-in page)
- https://www.pinterest.com/search/pins/?q=3d%20kawaii%20chibi%20render%20pastel — Pinterest search, screenshot `refs/ref_2.png`: pastel 3D chibi figurines, big heads, glossy eyes, blush, soft studio glow
- https://www.logoai.com/design/mini-me-figure-video — "Mini-me figure" video generator
- https://www.tomoviee.ai/video-effects/ai-3d-figure.html — AI 3D figure / toy-render tool
- https://dreamina.capcut.com/create/ai-chibi-video-generator — Dreamina AI chibi video generator

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (all 179 frames at 12 fps), `preview.webp`. Local approximation rendered with `render.py` (numpy + OpenCV + person masks + Apple Vision face landmarks from `faces.swift` → `faces.json`: temporally smoothed head/eye bulge warps, mean-shift clay albedo, inflated-height toy shading, drawn chibi eyes and blush, inpainted bokeh background); the six sheet frames are in `frames/`.

## Prompt

```text
I'm uploading one video clip. Convert it into a 3D KAWAII CHIBI TOY RENDER frame-by-frame animation matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
STYLE SOURCE
This look starts from the Frameloop "3D Kawaii Chibi" visual style (frameloop.ai/visual-styles), whose style prompt is:
"3D kawaii chibi render, smooth clay-like textures and ultra-cute proportions, warm sun-drenched color palette with golden yellows and soft pastels, whimsical volumetric lighting with a gentle glow, dreamy soft-focus background, high-detail miniature aesthetic."
with the finish of its sibling "Pixar Style" card:
"3D animated movie still, Pixar style, Disney animation, vibrant color palette, soft shadows, volumetric lighting, octane render, Unreal Engine 5, cinematic depth of field".
Everything below expands those prompts into a full frame-by-frame video workflow.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a cute 3D animated-feature still made from:
* CHIBI proportions: a big round head (about 1.4–1.6x larger) on the person's own body
* LARGE glossy dark eyes, each with one big and one small white catchlight
* soft rosy BLUSH on the cheeks, a small simple mouth
* SMOOTH clay-plastic surfaces: skin, hair and clothes are soft rounded shapes, no pores, no fabric noise, no stray hairs
* SIMPLIFIED PASTEL colours: each area one clean colour with soft shading
* WARM SUN-DRENCHED key light (golden yellow) from the upper left
* a soft LILAC / pink fill light in the shadows
* a gentle GOLDEN RIM GLOW around heads and shoulders
* soft broad specular highlights (satin vinyl, not wet)
* subsurface warmth in skin and ears
* a DREAMY SOFT-FOCUS background with round pastel bokeh discs
* volumetric sun haze, gentle bloom, a light vignette
* high-detail miniature / collectible-figure finish
The result should feel like someone:
FILMED THE CLIP
→ SCULPTED EACH PERSON AS A CUTE CHIBI FIGURE
→ PAINTED THEM IN SOFT PASTELS
→ LIT THE SET WITH WARM GOLDEN SUNLIGHT
→ RENDERED IT LIKE A PIXAR MOVIE STILL
→ MELTED THE ROOM INTO DREAMY BOKEH
→ ANIMATED IT FRAME-BY-FRAME.
CHARACTER — CHIBI VERSION OF THE SAME PERSON
The MAIN HUMAN SUBJECT(S) become chibi toy versions of THEMSELVES, not new characters.
Preserve the person's exact:
* identity
* face (face shape, skin tone, eye shape and spacing, brows, nose, mouth)
* expression
* hairstyle (shape, parting, length, colour)
* clothing (cut, colour, stripes and prints, simplified)
* accessories (glasses keep their shape and colour)
* pose
* body proportions BELOW the head
* movement
* hand position
* interaction with objects
Enlarge the head and eyes ONLY.
Do NOT change the body below the neck, the pose, or the limbs.
Do NOT replace the person with a generic doll or a famous character.
Do NOT give everyone the same face.
CHIBI FACE RULES
* the head is round and soft, about 1.5x, centred on the original head position
* eyes enlarged about 1.3x, dark iris filling most of the eye, two white catchlights at the upper left
* when the person blinks or squints, draw a happy closed-eye arc instead of open eyes
* soft pink blush ellipses under the eyes
* simplified small nose, gentle soft mouth that follows the real expression
* hair becomes smooth sculpted clumps with a broad sheen
* glasses stay on and keep their real shape, scaled with the head
* skin tone stays the person's own skin tone, only smoother and slightly warmer
PALETTE RULES
Warm, sun-drenched pastels:
* golden yellows, peach, apricot, cream
* soft pink and coral (blush, lips)
* mint and sage greens, powder blue, lilac
* each clothing colour kept, but brightened and softened into its pastel version
* deep shadows never black: warm brown or lilac
No neon, no harsh saturated primaries, no grey photographic shadows.
LIGHTING & MATERIAL
* key: warm golden sunlight, upper left, soft shadows
* fill: lilac / pink, low intensity
* rim: golden glow on hair, cheeks and shoulders facing the light
* specular: broad, soft, satin (vinyl toy), never glittery
* subsurface warmth in skin, ears and fingers
* ambient occlusion in creases (neck, arms against body)
BACKGROUND OPTIONS
DREAMY ORIGINAL ROOM:
keep the real room's layout and colours, but heavily soft-focused (shallow depth of field), pastel-graded, with round bokeh discs from lights and windows.
PASTEL SUN STUDIO (for selected sections, optional):
a seamless warm cream / peach backdrop with a soft golden sun glow and floating bokeh.
The people stay exactly where they are in the original frame.
LAYER ORDER
A typical frame reads:
DREAMY SOFT-FOCUS BACKGROUND + BOKEH
↓
CHIBI CHARACTERS (smooth 3D toy shading)
↓
CHIBI EYES, CATCHLIGHTS, BLUSH
↓
GOLDEN RIM LIGHT + SPECULAR
↓
VOLUMETRIC SUN HAZE + BLOOM
↓
WARM GRADE + LIGHT VIGNETTE.
OBJECT CONTINUITY
IMPORTANT:
If the character is interacting with an object, preserve that object as a cute, smooth 3D toy version.
Examples:
* phone
* cup
* chair
* bag
* microphone
* headphones
If the object is essential to the person's action, keep it sharp together with the person.
Do NOT accidentally blur it into the background or drop it.
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
The RENDER STYLE changes.
The HUMAN MOTION does NOT change.
If the head moves or turns:
the big chibi head moves and turns exactly with it.
If the person blinks:
the chibi eyes blink in that same frame.
If the hand moves:
the hand moves in that same frame.
If the character interacts with an object:
the object moves exactly with the original action.
NO lagging heads.
NO ghost faces from previous frames.
NO flickering eyes.
CHIBI CONSISTENCY
THIS IS CRITICAL.
The chibi design of each person is LOCKED for the whole clip:
* same head scale, same eye size and catchlight positions, same blush
* same pastel colour for each piece of clothing and hair
* same light direction and rim glow
The head size must NOT pulse or breathe between frames.
The eyes must NOT jump in size or position.
Allow, every frame:
* bokeh discs to drift very slowly
* sun haze to shimmer very slightly
DO NOT
Do NOT make it stop-motion claymation: no fingerprints, no tool marks, no wobble, no matte plasticine.
Do NOT make it a flat 2D anime drawing.
Do NOT turn the people into generic dolls, mascots or famous characters.
Do NOT change body proportions below the head.
Do NOT make faces creepy, uncanny or doll-dead: eyes must look alive and match the real gaze.
Do NOT add photo pores, wrinkles or fabric noise.
Do NOT use neon or harsh saturated colours.
Do NOT blow out the yellows.
Do NOT create new poses.
Do NOT change clothing.
Do NOT add text, logos, watermarks or UI.
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
* NO chibi heads
* NO 3D render
* NO pastel grade
* NO bokeh or glow
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
Do NOT begin the chibi transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – 3D KAWAII CHIBI STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Before generating, design and show me ONE chibi character sheet per person (front view from the clip: head scale, eye design, blush, pastel colours for hair, skin and each garment) and lock it.
Use each person's character sheet plus the previous styled frame as consistency references for every frame.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, head scale or eye design broke — regenerate those frames only.
The final video must feel like a CLIP FROM A CUTE 3D ANIMATED FEATURE: the same people, as glowing chibi toys, in warm golden light.
The image should deliberately contain:
* big round chibi heads on the real bodies
* glossy eyes with white catchlights
* rosy blush
* smooth clay-plastic surfaces
* warm golden key light, lilac fill and a golden rim glow
* a dreamy pastel bokeh background
* gentle bloom and sun haze.
Avoid clutter: no extra props, sparkles, stickers or emoji that were not in the source.
```
