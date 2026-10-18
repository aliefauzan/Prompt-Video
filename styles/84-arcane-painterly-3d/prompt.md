# 84 — Arcane Painterly 3D

**Look:** The clip becomes a shot from a painted-over 3D animated series in the manner of *Arcane*. Faces and clothes are sculpted in a few painted value planes, with visible brushstroke texture that follows the form, gritty dark ink accents along the contours and a little hatching in the deepest shadows. Two hard coloured rim lights cut out every silhouette: teal-cyan from the left, hot magenta-pink from the right. The room becomes a dark, moody painted set with teal shadows, an amber glow from the window and dust drifting in the light. The paint texture steps on twos, like the show's animation.

**Also called / where it trends:** "Arcane style", "Arcane filter" (CapCut "Filter Arcane" templates, one with 270K+ likes), "Arcane AI filter", "Fortiche style", "painterly 3D", "2.5D painted 3D", "Dispatch style", "League of Legends animation style". It trends as CapCut / TikTok filter edits and as AI-filter apps (AI Mirror and others), as Wan video LoRAs on Civitai (Arcane Style for Wan 2.2), and in Midjourney / Stable Diffusion "arcane style" prompts.

**References:**
- https://www.tiktok.com/@jackvsai/video/7669765802563849475 and https://www.tiktok.com/@aimirror.official/video/7441804356124527902: TikTok "Arcane style AI filter" edits. The TikTok search grid (screenshot `refs/ref_1.png`) shows the CapCut "Filter Arcane" tiles at 153.6K and 273.1K likes (from D1).
- https://civitai.com/models/2197303 (screenshot `refs/ref_3.png`): "Arcane Style [WAN 2.2 T2V]" video LoRA ("renders videos in a style similar to the one seen on the Netflix show Arcane", trigger word `ArcaneStyle`).
- https://civitai.com/models/2332126 (D3 screenshot `refs/ref_2.png`): a second painterly-3D (Arcane / Dispatch) video LoRA. It shows 3D-lit characters with brushstroke albedo, harsh rim light and hand-painted texture over the geometry.
- https://en.wikipedia.org/wiki/Arcane_(TV_series): the source show (Fortiche / Riot Games, 2021). Its look is 3D models with hand-painted textures, 2D effects and a painterly, graphic lighting style.

How it differs from the styles already in the library: **51 Ghibli Painted Anime** is soft pastoral watercolour in daylight. **59 3D Kawaii Chibi** is glossy pastel toy 3D. **30 Spider-Verse Comic Offset** is halftone and print offset. **50 Impasto Oil Painting** is thick oil paint all over. This one is painted-on-3D: sculpted value planes, brushstroke albedo, gritty ink accents and dramatic teal / magenta rim light in a dark set.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (the whole clip at 12 fps with the original audio) and `preview.webp`. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). The people are mean-shift smoothed and re-shaded into six value bands with soft painted edges, richer colour and a light sharpen, so they stay crisp against the softer set. Brushstroke texture is cross-brushed dabs (noise smeared at two fixed angles) and it changes on twos. Ink comes from broken Canny contours, XDoG lines on the dark facial features, painted dark accents on eyes, brows and lips, and sparse hatching in the darkest shadows. The two rim lights are read from the matte's edge normal. The room is posterised into flat painted value planes, darkened toward teal and covered with long cross-hatched brush texture, with some depth softness. The window becomes an amber glow that spills into the room, with drifting dust motes. On top: bloom on the hot rims, crisp sharpening, light grain and a vignette.

## Prompt

```text
I'm uploading one video clip. Convert it into an ARCANE-STYLE PAINTERLY 3D frame-by-frame animation: every frame should look like a frame from a painted-over 3D animated series, with hand-painted textures on sculpted 3D forms, gritty ink accents and dramatic coloured rim light, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Arcane style, painterly 3D animation, hand-painted textures over 3D forms, visible brushstrokes, stylized realistic proportions, gritty ink line accents, dramatic cinematic lighting, strong teal and magenta rim light, moody painted background, atmospheric haze.
Transform the footage into a painted-3D frame built from:
* SCULPTED 3D FORMS: faces, hands and clothes read as solid modelled volumes
* PAINTED VALUE PLANES instead of photographic shading (a few clear light-to-shadow steps)
* VISIBLE BRUSHSTROKE TEXTURE on skin, hair and fabric, following the form
* GRITTY dark INK ACCENTS along contours, eyelids, nostrils, lips and fabric folds
* a little cross-HATCHING in the deepest shadows
* TWO HARD RIM LIGHTS: teal-cyan from the left, hot magenta-pink from the right
* a warm amber key light, deep teal-blue shadows
* a DARK, MOODY PAINTED SET behind the people
* an amber glow from the window and practicals, light spilling into the room
* floating dust motes in the light
* soft bloom on the rims and glows
* painted, stepped animation (texture changes on twos)
The result should feel like someone:
SCANNED THE PEOPLE INTO 3D
→ HAND-PAINTED THEIR TEXTURES WITH VISIBLE BRUSHSTROKES
→ LIT THEM WITH A WARM KEY AND TWO COLOURED RIMS
→ PAINTED OVER EVERY RENDER WITH INK ACCENTS
→ PAINTED THE ROOM AS A MOODY BACKGROUND SET
→ COMPOSITED IT FRAME-BY-FRAME.
CHARACTER — PAINTED 3D
Rebuild each person as a stylized painted-3D character, but keep them unmistakably the SAME person.
Preserve the person's exact:
* identity
* face shape and features
* expression
* hairstyle
* glasses
* clothing and its pattern (stripes stay stripes, the batik pattern stays, painted)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Stylized-realistic proportions like Arcane: real anatomy, slightly sculpted planes on cheekbones, brow and jaw.
Do NOT make chibi, cute or toy-like characters.
Do NOT give anyone a different face, game character face or famous character's look.
PAINT AND TEXTURE
* Skin: warm painted base, 3-4 clear value steps, visible brush marks, a touch of red in ears, nose and cheeks.
* Hair: painted as chunky sculpted locks with brushy strand texture and a hard light edge.
* Fabric: brushy texture that follows folds; patterns painted, not photographic.
* Edges between value planes are soft-painted, not gradient-smooth and not cel-hard.
* The brushstroke texture is attached to the surface and moves with it.
INK ACCENTS
* Thin, dark, slightly dry and broken lines on contours and key features.
* Sparse hatching inside the darkest shadows only.
* Never a full cartoon outline around everything.
LIGHTING
* Warm amber key light on faces.
* Shadow side falls into deep teal-blue.
* Teal-cyan rim light on the LEFT edges of every person; magenta-pink rim light on the RIGHT edges.
* Rims are hard, narrow and bright, with a soft bloom.
* Same light directions on every frame.
BACKGROUND — MOODY PAINTED SET
* Keep the SAME room layout: window, plant box, cupboards, screen, chair, perspective.
* Repaint it darker as a painted set: brushy texture, simplified shapes, slight depth softness.
* Teal-blue shadows; the window becomes a warm amber glow that spills light into the room.
* The screen may glow cool teal.
* Dust motes drift slowly through the light.
PALETTE
Teal, cyan, deep blue-green shadows.
Magenta, hot pink rims.
Amber, warm orange, painted skin tones.
Deep charcoal, never pure black.
Do NOT use pastel or flat grey colours.
OBJECT CONTINUITY
If the character holds an object, it is painted in the same style, lit by the same rims, attached to the hand.
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
The rim lights follow the real silhouette on every frame.
NO painted texture left floating where a person was.
NO background element that pops in or out.
FRAME-TO-FRAME PAINTED LIFE
THIS IS CRITICAL.
It must feel like painted-over 3D animation, not a still filter.
Allow between consecutive frames:
* brushstroke texture to change on twos (every second frame)
* ink accents to shift slightly
* dust motes to drift
* rim and glow bloom to shimmer slightly
Keep FIXED:
* the light directions and rim colours
* each person's paint colours
* the background set and its grade
DO NOT
Do NOT keep the people photographic under a filter.
Do NOT make flat 2D cel anime.
Do NOT make soft watercolour or glossy toy 3D.
Do NOT outline everything with thick black cartoon lines.
Do NOT use halftone or comic print effects.
Do NOT add game characters, logos or tattoos that are not in the source.
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
* NO painting or brush texture
* NO relighting or rim light
* NO background repaint, glow or dust
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
Do NOT begin the Arcane painterly transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – ARCANE PAINTERLY 3D STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the light setup (key direction and colour, left rim colour, right rim colour), each person's main paint colours, and how the background set will be graded.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Keep the same light setup, paint colours and background set on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, lighting or paint consistency broke — regenerate those frames only.
The final video must feel like A SHOT FROM A PAINTED-3D ANIMATED SERIES: sculpted painted forms, brushstrokes, ink accents, teal and magenta rims, a moody amber-lit set, 12 frames per second.
The image should deliberately contain:
* painted value planes on faces and clothes
* visible brushstroke texture
* gritty ink accents
* teal-cyan and magenta-pink rim lights
* a dark painted set with an amber window glow
* drifting dust in the light.
Avoid photographic skin.
```
