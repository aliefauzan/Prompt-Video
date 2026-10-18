# 86 — PS1 Low-Poly Wobble

**Look:** The clip becomes a cutscene from a mid-90s home console game. Everything is a chunky 240p-class picture of square pixels. The people are hard-edged polygon models wrapped in blurry, point-sampled, few-colour textures that kink and swim along the triangle seams as the camera moves. Every vertex snaps to the pixel grid and shivers a pixel from frame to frame. The room sinks into thick dark draw-distance fog, and the whole image is 15-bit colour with the fixed checkerboard ordered dither of the console.

**Also called / where it trends:** "PS1 graphics", "PS1 aesthetic", "PS1 filter", "PSX style", "PS1/N64 lo-fi 3D", "retro 3D", "low-poly horror", "PS1 风格" (Bilibili). It runs on TikTok and CapCut as a "PS1 filter" for selfie videos (the D1 sweep logged clips with up to ~480K likes). Instagram has a #ps1graphics tag with about 33K reels, and indie horror games and Pinterest boards keep the PSX look alive. On Civitai it is a video LoRA ("PS1 / N64 lo-fi 3D"), and Unreal/Unity "retro shader" packs reproduce it.

How it differs from nearby styles: **40 Low-Poly 3D** has clean flat-shaded facets and no texture, while this keeps a textured image and makes it low-res, warped, dithered and fogged. **11 Pixel Art Dither** is 2D sprite art; this is a 3D render, with polygon silhouettes, affine texture swim, vertex jitter and depth fog.

**References:**
- https://www.pinterest.com/search/pins/?q=ps1%20graphics%20aesthetic (screenshot `refs/ref_1.png`, from the D2 sweep). Mood boards of PSX scenes: point-sampled textures, low-res tables and rooms, fog-filled forests, dark night drives.
- https://pikuma.com/blog/how-to-make-ps1-graphics (screenshot `refs/ref_2.png`). Pikuma, "How PlayStation Graphics & Visual Artefacts Work". It covers affine texture mapping (no perspective correction), integer vertex snapping (wobble), no Z-buffer, 15-bit colour with dithering, and fog.
- Bilibili PS1风格 videos av579370715, av113747729322810, av835651974, and the GitHub repo DaveFace/UnrealRetroShaders (screenshot `refs/ref_3.png`, from the D4 sweep).
- https://civitai.com/models/1643552: a PS1 / N64 lo-fi 3D video LoRA (D3 sweep).
- TikTok: @ember.lite/video/7624261224116604167, @dan.esberg/video/7349281640935394603 and @decaying_sun/video/7675591094083620118. YouTube nJfZ9D6rcVw. All are "ps1 graphics filter" edits from the D1 sweep.
- https://jordanemme.com/blog/the-playstation-texture-wobble/ (why the textures wobble), https://danielilett.com/2021-11-06-tut5-21-ps1-affine-textures/ (affine textures in shader code), https://www.david-colson.com/2021/11/30/ps1-style-renderer.html (building a PS1-style renderer), https://psx-spx.consoledev.net/ps1/gpu/misc/ (the hardware's 4x4 dither matrix).

**Example:** `example.png` shows six frames of the test clip and `before_after.png` shows frame 049. `example.mp4` is the whole clip at 12 fps with the original audio, and `preview.webp` is an animated preview. This is a local approximation made with `render.py` (numpy + OpenCV + the person masks). Each frame is rendered at 270x180 and enlarged 6x with nearest neighbour. Textures are snapped to a shared 28-colour palette (CLUT), at 0.7x resolution for the people and 0.4x for the room, and point-sampled. The image is cut into a triangle mesh, finer on the people. A drifting swim field is interpolated per triangle, so the texture kinks along triangle edges. Vertices snap to whole pixels and jitter by ±1 px every frame. The people are cut as hard polygon silhouettes and get Gouraud-style vertex lighting. Dark blue-grey distance fog fills the room. Colour depth is cut with a fixed screen-space 4x4 Bayer dither. The render cannot rebuild real 3D geometry; a video model can.

## Prompt

```text
I'm uploading one video clip. Convert it into a PS1 LOW-POLY WOBBLE frame-by-frame animation: every frame should look like a real-time cutscene rendered by a mid-1990s home console, with low-resolution warped textures, jittering vertices, ordered dither and thick distance fog, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage into a 32-bit-console-era 3D frame built from:
* a LOW internal resolution (about 320x240) shown with SQUARE, unfiltered pixels
* LOW-POLY models: hard, angular polygon silhouettes, no anti-aliasing
* LOW-RES, POINT-SAMPLED textures (blocky texels, no smoothing, no mipmaps)
* AFFINE texture mapping: textures kink and swim along the triangle seams
* VERTEX SNAPPING: every vertex sits on whole pixels and shivers 1 px between frames
* GOURAUD vertex lighting: soft gradients across each polygon, faceted where polygons meet
* few-colour CLUT textures (16–256 colours per texture)
* 15-bit colour with a fixed 4x4 ORDERED DITHER pattern on every gradient
* thick linear DISTANCE FOG fading the room to dark blue-grey
* a slightly dark, moody, late-night game ambience
The result should feel like someone:
SCANNED THE PEOPLE AND THE ROOM INTO LOW-POLY MODELS
→ BAKED THE FOOTAGE INTO TINY TEXTURE PAGES
→ LIT THE SCENE WITH VERTEX LIGHTS
→ RENDERED IT ON 1996 CONSOLE HARDWARE AT 240p
→ WITH NO PERSPECTIVE CORRECTION AND NO Z-BUFFER
→ CAPTURED THE CUTSCENE FRAME BY FRAME.
CHARACTER — LOW-POLY GAME MODEL
Each person becomes a low-poly character model wearing a low-res texture made from their own image.
Preserve the person's exact:
* identity
* face
* expression
* hairstyle
* glasses
* clothing pattern (batik, stripes, plain knit)
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
The face stays recognisable as a low-res texture: eyes, glasses, brows and mouth are a few texels each, readable but crude.
Hair is a chunky angular shell with a painted texture, not strands.
Silhouettes are polygonal: straight edges and corners, no smooth curves, stair-stepped pixel edges.
Do NOT turn the people into smooth modern 3D, clay or a cartoon.
Do NOT beautify or re-sculpt faces.
TEXTURE RULES — WARPED AND BLOCKY
* Textures are low-res and point-sampled, so texels show as small square blocks.
* Straight lines in a texture (shirt stripes, window frames, the screen edge) BEND and KINK where two triangles meet, because the texture is mapped affinely without perspective correction.
* Textures slowly SWIM over the surface as the body or camera moves.
* Colours inside a texture are posterised into a small palette, with flat patches and hard steps.
* The room's textures are lower-res than the people's.
POLYGON + VERTEX RULES
* Each model has a few hundred polygons at most.
* Vertices snap to the pixel grid, so edges crawl and shiver by about one pixel from frame to frame.
* Lighting is per-vertex (Gouraud): soft gradients inside each polygon, with faint facets where polygons meet.
* Small gaps or sparkles may flicker along polygon seams.
* No anti-aliasing anywhere: hard stair-stepped edges.
FOG + LIGHT
* The room is far away in game terms: it fades into thick dark blue-grey fog.
* Fog is thickest at the back wall and top of frame; people in front are mostly clear.
* When a person stands further back, they take on a little fog too.
* Light is dim and moody, like a game set at night; skin stays warm against the cool fog.
COLOUR + DITHER
* 15-bit colour: banded gradients broken up by the console's fixed 4x4 ordered dither (a fine checkerboard / crosshatch pattern).
* The dither pattern is fixed to the SCREEN: it does not crawl or boil.
* Muted, slightly desaturated colours: brown batik, beige-and-white stripes, grey-green knit, warm skin, cool grey room.
PALETTE
Dark blue-grey fog, slate, muted teal-grey walls.
Warm skin, brown batik, beige and cream stripes, grey-green knit, black.
Small amounts of blue from the screen on the wall.
Do NOT add neon, chrome, rainbow or glossy colours.
OBJECT CONTINUITY
If the character holds an object, it becomes part of the same low-poly model, with the same blocky texture, attached to the hand.
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
The models must match the source frame exactly.
If the head turns, the low-poly head turns.
If the hand moves, the low-poly hand moves.
NO frozen previous-frame silhouette.
NO model lagging behind the person.
FRAME-TO-FRAME CONSOLE WOBBLE
THIS IS CRITICAL.
It must feel like real-time 1996 rendering, not a static pixel filter.
Allow between consecutive frames:
* vertices to snap and shiver by about 1 px
* textures to swim and kink slightly along polygon seams
* seam sparkles to appear and disappear
Keep FIXED:
* the internal resolution and pixel size
* the ordered dither pattern (screen-locked, never boiling)
* the palette and fog colour
* the people's identity and pose
DO NOT
Do NOT render smooth high-resolution 3D.
Do NOT use clean flat-shaded facets without texture (that is a different low-poly look).
Do NOT make 2D pixel-art sprites.
Do NOT use bilinear-smoothed or blurry upscaling; pixels must stay square and sharp.
Do NOT add CRT scanlines, VHS noise or chromatic aberration.
Do NOT add game logos, console logos, button icons or HUD text.
Do NOT redraw the people as cartoons.
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
* NO pixelation or downscaling
* NO dither or colour reduction
* NO fog
* NO texture warping
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
Do NOT begin the PS1 transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – PS1 LOW-POLY STYLING (AFTER MY CONFIRMATION ONLY)
First, tell me the internal resolution, the fog colour and the texture palette size you will use, and keep them fixed for the whole clip.
Then style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation, so the people are exactly that frame.
Apply every style rule above, with the SAME resolution, palette, fog and dither on every frame.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT reuse one styled frame for several timeline slots.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose, timing, resolution or palette consistency broke — regenerate those frames only.
The final video must feel like A LOST PS1 CUTSCENE: low-poly people in warped blocky textures, shivering vertices, dithered 15-bit colour, a room drowning in fog, 12 frames per second.
The image should deliberately contain:
* square unfiltered 240p pixels
* hard polygon silhouettes
* affine texture kinks and swim
* 1 px vertex jitter
* a fixed 4x4 ordered dither
* thick dark distance fog.
Avoid modern smooth rendering.
```
