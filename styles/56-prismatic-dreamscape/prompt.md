# 56 — Prismatic Dreamscape

**Look:** The clip looks as if it were shot through a glass prism held in front of the lens on a sunny afternoon. Rainbow light leaks sweep diagonally across the frame. A soft prism fold mirrors a blurred slice of the scene at the edge with a rainbow seam. A vivid spectrum stripe falls across a face like sunlight through crystal. Highlights split into red and blue fringes, out-of-focus lights become iridescent discs, and hexagonal rainbow flare ghosts trail from a sun glow. Everything floats in a lifted, overexposed pastel haze of pink, lavender, peach and mint.

**Also called / where it trends:** "Prismatic Dreamscape" (frameloop.ai style name), "prism photography", "prism portrait", "rainbow light leak", "holographic glow", "iridescent dreamy", "ethereal pastel". It trends on Instagram and TikTok through prism-filter and "shoot through a crystal" portrait hacks, Pinterest dreamy-portrait boards, and preset and overlay packs of rainbow light leaks and holographic flares.

**How it differs from 17 (Double Exposure):** double exposure blends a second IMAGE (landscape, forest, city) inside the silhouette of the person, usually in monochrome or muted tones, with a hard silhouette boundary. Prismatic Dreamscape adds no second image and does not use the silhouette as a window. It is about LIGHT: refraction, dispersion, rainbow leaks, iridescent bokeh and pastel overexposure washing over the whole intact frame.

**References:**
- https://frameloop.ai/visual-styles (screenshot `refs/ref_1.png`; the style's sample image `refs/ref_2.png`): the **Prismatic Dreamscape** style card. Its style prompt, credited to frameloop.ai and expanded into the workflow below: *"ethereal dreamy atmosphere, heavy prismatic light leaks, sunlight filtering through prismatic glass, soft glowing bloom, iridescent pastel color palette, magical realism, holographic lens flares, sun-drenched, overexposed colorful highlights."*
- https://lumecube.com/blogs/news/shot-with-lume-series-the-perfect-prism-portrait-with-hayden-dumaw (screenshot `refs/ref_3.png`): Lume Cube, "Shot with Lume Series: The Perfect Prism Portrait with Hayden Dumaw". A real in-camera prism portrait, with a rainbow band refracted across the face and soft refracted ghosts at the frame edge.
- https://www.adobe.com/creativecloud/photography/discover/prism-photography.html: Adobe's guide to prism photography (refraction, rainbow flares and mirrored fragments made by holding a prism near the lens).

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). The background gets a soft-focus blur and 22 iridescent bokeh discs. The frame is lifted and tinted pink→lavender with lavender blacks. Chromatic dispersion pulls 7 radial colour scales apart. Three diagonal rainbow light-leak bands drift slowly. Two prism-fold wedges mirror a blurred slice of the frame with a rainbow seam, weakened over the people. A rainbow stripe tracks the central face at eye level. It adds hexagonal rainbow flare ghosts from a top-left sun glow, sparkles, bloom on highlights and pastel haze.

## Prompt

```text
I'm uploading one video clip. Convert it into a PRISMATIC DREAMSCAPE frame-by-frame animation: every frame should look as if it were shot through prismatic glass in soft sunlight, full of rainbow light leaks, iridescent bloom and pastel haze, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Ethereal dreamy atmosphere, heavy prismatic light leaks, sunlight filtering through prismatic glass, soft glowing bloom, iridescent pastel colour palette, magical realism, holographic lens flares, sun-drenched, overexposed colourful highlights.
Transform the footage into a prismatic dream built from:
* PRISM REFRACTION: a soft mirrored, blurred slice of the scene at one or two frame edges, joined by a rainbow seam
* RAINBOW LIGHT LEAKS sweeping diagonally across the frame
* a vivid SPECTRUM STRIPE falling across a face, like sunlight through crystal
* CHROMATIC DISPERSION: red and blue fringes splitting off bright edges, stronger toward the frame edges
* IRIDESCENT BOKEH: soft discs with rainbow-shifted colour in the background
* HOLOGRAPHIC LENS FLARES: hexagonal rainbow ghosts from a soft sun glow
* soft glowing BLOOM on every highlight
* SUN-DRENCHED, OVEREXPOSED highlights
* a soft PASTEL HAZE over the whole frame
* small sparkles of refracted light
The result should feel like someone:
WAITED FOR GOLDEN AFTERNOON SUN
→ HELD A CRYSTAL PRISM IN FRONT OF THE LENS
→ LET RAINBOWS AND REFLECTIONS SPILL ACROSS THE FRAME
→ OVEREXPOSED A LITTLE
→ GRADED IT IN SOFT PASTELS
→ SHOT IT FRAME-BY-FRAME LIKE A DREAM.
CHARACTER — PHOTOGRAPHIC, BATHED IN LIGHT
The people stay PHOTOGRAPHIC and REAL, only washed with refracted light.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw the character.
Do NOT turn them into a painting, anime or fantasy creature.
Do NOT add wings, glitter makeup, crowns or new clothing.
PRISM REFRACTION
* At one side of the frame (and optionally one corner), a soft wedge shows a mirrored, blurred copy of the neighbouring part of the scene, like the face of a prism held near the lens.
* The wedge boundary carries a thin rainbow seam.
* The wedge is translucent and very soft over people; their faces stay clear.
* The wedge stays in about the same place, shifting only slightly as if the prism moves in a hand.
RAINBOW LIGHT LEAKS AND FACE STRIPE
* 2–3 broad diagonal rainbow bands (red → orange → yellow → green → blue → violet) sweep across the frame, soft-edged and partly transparent.
* They drift slowly from frame to frame.
* One vivid, narrower spectrum stripe crosses the main face around eye or cheek level, following the face as it moves.
* The stripe is bright but translucent: the eyes and expression stay visible through it.
DISPERSION, BOKEH AND FLARES
* Bright edges split into colour fringes (warm on one side, cool on the other), stronger toward the frame edges.
* Background lights and bright spots become soft iridescent discs.
* A soft sun glow sits in one top corner and throws a trail of hexagonal rainbow flare ghosts across the frame.
* Tiny star-like sparkles twinkle on the brightest points.
EXPOSURE AND HAZE
* Lifted, airy exposure: highlights glow and gently clip; blacks lift to soft lavender.
* A thin pastel haze softens the whole image.
* The background is softly out of focus; the people stay sharp.
PALETTE
Pastel pink, lavender, lilac, peach, butter yellow, mint, sky blue, with full-saturation rainbow only inside the leaks, the face stripe and the flare ghosts.
Do NOT use deep black, harsh neon, or a dark moody grade.
OBJECT CONTINUITY
If the character holds an object, it stays attached to the hand, catching the same refracted light.
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
The people must match the source frame exactly.
The face stripe follows the face.
The prism wedge, leaks and flares belong to the LENS, not to the scene: they stay near their place in the frame and drift slowly.
NO rainbow pasted on a face in one frame and gone in the next.
NO leak jumping position between frames.
FRAME-TO-FRAME LIGHT LIFE
THIS IS CRITICAL.
It must feel like real sunlight moving through glass, not a still overlay.
Allow between consecutive frames:
* light leaks to drift and breathe slowly
* the prism wedge to shift a few pixels
* dispersion strength to pulse gently
* flare ghosts to shimmer
* sparkles to twinkle on and off
Keep FIXED:
* the pastel grade and exposure
* the sun position
* the general placement of the wedge and leaks
DO NOT
Do NOT make it a double exposure: no landscape, forest or second picture inside the silhouette.
Do NOT turn the people into a silhouette or cut-out.
Do NOT hide faces under the prism wedge or a solid rainbow.
Do NOT use a hard-edged rainbow sticker.
Do NOT make it neon, dark or cyberpunk.
Do NOT redraw or illustrate the people.
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
* NO prism refraction or light leaks
* NO dispersion, bokeh or flares
* NO pastel grade or haze
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
Do NOT begin the prismatic dreamscape transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – PRISMATIC DREAMSCAPE STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me where the prism wedge, the sun glow and the light-leak bands will sit, and which face will carry the spectrum stripe.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME pastel grade and lens-effect layout in every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, the grade or the effect layout broke — regenerate those frames only.
The final video must feel like A DREAM SEEN THROUGH A PRISM: rainbow leaks, a spectrum across the face, iridescent bloom, pastel haze, 12 frames per second.
The image should deliberately contain:
* prism refraction with a rainbow seam
* diagonal rainbow light leaks
* a spectrum stripe across a face
* chromatic dispersion fringes
* iridescent bokeh and holographic flare ghosts
* overexposed pastel haze.
Avoid flat, dull daylight.
```
