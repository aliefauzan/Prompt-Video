# 40 — Low-Poly 3D (PS1 Render)

**Look:** the clip re-rendered as a PS1-era real-time 3D scene. People become chunky faceted polyhedra: big flat-shaded triangles, each one filled with a single colour and lit from one side, with smaller facets on faces and hands and larger ones on bodies. The mesh is re-triangulated every frame, so the facets "boil". The room becomes a coarse texture-mapped mesh with blurry, low-res, nearest-neighbour textures that swim and warp (affine mapping), vertices that wobble a pixel or two, and dusty blue-grey distance fog. Everything is snapped to a 540x360 framebuffer with 15-bit colour, 4x4 ordered dither and a crunchy nearest-neighbour upscale.

**Also called / where it trends:** "PS1 aesthetic", "PSX graphics", "low poly edit", "PS1 filter", "low-poly character", "y2k 3D", "haunted PS1". Seen in TikTok/CapCut PS1 filters, indie-horror games (the PSX / Haunted PS1 scene), Blender / Godot / three.js PSX shader tutorials, retro-3D music videos, vaporwave and "liminal" edits, and low-poly portrait illustration.

**References:**
- https://www.pinterest.com/search/pins/?q=ps1%20low%20poly%20character%20aesthetic (screenshot `refs/ref_1.png`): PS1 characters, faceted low-poly faces, dithered fog scenes.
- https://www.pinterest.com/search/pins/?q=low%20poly%20triangle%20portrait%20faceted (screenshot `refs/ref_2.png`): faceted triangle portraits, flat-shaded facets that follow the face structure.
- https://github.com/marmitoTH/godot-psx-shaders: Godot PSX shaders covering vertex snapping, affine texture mapping, fog and dither.
- https://github.com/lferreira457/threejs-psx-shader: a three.js PSX shader with the same PS1 artefacts in WebGL.
- https://github.com/mourad-bakhali/psx_shader_effect: a PSX shader that explains vertex wobble as a lack of sub-pixel / float precision.
- https://fawkek.itch.io/psx-retro-tools: PSX retro tools (dither, colour depth, resolution downscale).
- https://www.youtube.com/watch?v=cUiyph17F3A: a PS1-style graphics tutorial.
- https://www.youtube.com/watch?v=tcRA2I8oqpk: a PS1 / low-poly look tutorial.

**Example:** `example.png` (six frames of the test clip), `before_after.png` (frame 049), `example.mp4` (full clip). Local approximation rendered with `render.py` (numpy + OpenCV Delaunay + person masks); the 6 sheet frames are in `frames/`. Distinct from 11 Pixel Art (that one uses square pixels and a palette; this one uses triangles and 3D shading) and from 21 Stained Glass (no lead lines, no glow; faceted 3D geometry).

## Prompt

```text
I'm uploading one video clip. Convert it into a LOW-POLY PS1-ERA 3D RENDER, frame by frame, matching the supplied visual references.
Keep the SAME frame extraction, timing, motion, composition, character identity and continuity workflow.
The STYLE ONLY should change.
Work through the stages below in order. Do not skip ahead.
TOOL LOCK
Use Seedream 5.0 Pro for ALL image generation in this workflow.
Do not substitute another image model, not even as a fallback.
CORE VISUAL STYLE
Transform the footage so it looks genuinely RENDERED IN REAL TIME ON A 1990s 3D GAME CONSOLE, built from:
* chunky LOW-POLY geometry made of visible TRIANGLES
* FLAT SHADING: each triangle filled with ONE colour, no smooth gradients inside a facet
* simple one-direction lighting (lit side brighter, far side darker)
* smaller facets on faces and hands, larger facets on torsos and clothes
* facet edges following real structure (jaw, nose, brow, collar, folds, arms)
* blurry low-resolution nearest-neighbour textures on the room
* AFFINE TEXTURE WARP: textures bend and swim across big triangles
* VERTEX WOBBLE: vertices snap and jitter a pixel or two per frame
* dusty blue-grey distance FOG
* a low internal resolution (about 540x360) shown with hard pixel upscaling
* 15-bit colour with 4x4 ORDERED DITHER patterns in gradients
The result should feel like someone:
MODELLED THE PEOPLE AND THE ROOM AS LOW-POLY 3D MESHES
→ BAKED THE FOOTAGE INTO TINY TEXTURES
→ LIT THEM WITH ONE FLAT LIGHT
→ RENDERED THE SCENE ON A PS1-ERA CONSOLE
→ CAPTURED THE TV OUTPUT
→ PLAYED IT BACK FRAME BY FRAME.
CHARACTER — LOW-POLY BODY
The MAIN HUMAN SUBJECTS become low-poly 3D characters that are still clearly the same people.
Preserve each person's exact:
* identity
* face
* expression
* hairstyle
* clothing silhouette
* accessories
* pose
* body proportions
* movement
* hand position
* interaction with objects
Do NOT redraw them as different game characters.
Do NOT turn them into cartoons, chibis, Minecraft blocks or pixel art.
Build each person from flat triangles:
* face → about 40-120 small facets: brow ridge, eye sockets, nose bridge, cheekbones, mouth and jaw read as planes
* eyes, brows and mouth stay readable as darker facets
* hair → a few large dark facets with sharp edges
* torso and clothes → large facets, colour taken from the clothing (stripes and batik simplify into a few flat bands or patches)
* hands → a handful of facets, fingers simplified
* silhouette → a polygon outline with visible corners, not a smooth curve
Each facet's brightness depends on which way it faces the light.
THE ROOM — TEXTURED LOW-POLY SET
The room keeps its exact layout but becomes a coarse 3D set:
* walls, window, shelves, plants, chairs and screens as large textured triangles
* textures low resolution, nearest-neighbour, slightly smeared
* textures warp along triangle seams (affine mapping, no perspective correction)
* each triangle a little lighter or darker than its neighbour
* distance fog pulling the far room toward a dusty blue-grey
PS1 RENDERING ARTEFACTS
* vertex snapping / wobble: edges and corners shimmer by 1-2 px between frames
* texture swim on the room surfaces
* 4x4 ordered-dither crosshatch in gradients and dark areas
* banding from 15-bit colour
* no anti-aliasing: jagged stair-step triangle edges
* hard nearest-neighbour upscale: visible fat pixels
It must NOT look like a modern smooth 3D render or a polished low-poly illustration.
PALETTE RULES
Keep the scene's own colours, simplified:
* skin → warm flat tones in 3-5 shades per face
* clothing → its real colour in flat bands
* room → slightly desaturated, pushed toward the dusty blue-grey fog with distance
* shadows → darker versions of the facet colour, never black outlines
Colour depth limited (15-bit feel) with visible dither.
Do NOT add neon, outlines or cel-shading ink lines.
LAYER ORDER
A typical frame reads:
FOG-TINTED TEXTURED ROOM MESH
↓
FLAT-SHADED LOW-POLY PEOPLE
↓
LIGHTING PER FACET
↓
540x360 FRAMEBUFFER + 15-BIT COLOUR + ORDERED DITHER
↓
NEAREST-NEIGHBOUR UPSCALE.
No HUD, no text, no UI.
OBJECT CONTINUITY
IMPORTANT:
If a character interacts with an object, model that object as low-poly too.
Examples:
* phone (a flat slab of a few triangles)
* cup (a low-sided cylinder)
* chair
* glasses (thin flat frames)
* bag, headphones
If the object is essential to the action, keep it clearly visible.
Do NOT accidentally remove it.
CHARACTER CONTINUITY LOCK
The SAME people must remain recognisable in every frame.
Never change:
* identity
* facial structure
* hairstyle
* clothing silhouette
* accessories
* body proportions
* anatomy
* expression
* pose
* action
* position
Generation is for VISUAL STYLE ONLY.
PERFECT MOTION TRACKING
The underlying human movement must stay exactly faithful to the source footage.
The MESH boils.
The HUMAN MOTION does NOT change.
If the head turns:
the facets re-light as the planes turn.
If a hand moves:
its facets follow, with no trail.
NO ghost geometry from previous frames.
NO frozen facets while the body moves.
FRAME-TO-FRAME POLYGON BOIL
THIS IS CRITICAL.
Every frame should feel like a fresh real-time render.
Allow:
* people to be RE-TRIANGULATED every frame: facet edges shift and re-split, but always follow the same face and body structure
* vertices to wobble 1-2 px
* room textures to swim slightly along triangle seams
* dither patterns to stay fixed to the screen (they do not crawl)
Do NOT let a face change shape or identity between frames.
Do NOT let colours jump.
Do NOT let facet size change wildly from frame to frame.
DO NOT
Do NOT render smooth skin, soft gradients or photoreal shading.
Do NOT make it pixel art (square pixel sprites, limited palette blocks).
Do NOT make it stained glass (no dark lead lines between facets, no glow).
Do NOT add black outlines or cel shading.
Do NOT make it a modern clean low-poly illustration with perfect gradients.
Do NOT add game HUD, health bars, text or logos.
Do NOT replace any face.
Do NOT create new poses.
Do NOT change anatomy.
Do NOT change clothing shape.
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
* NO low-poly mesh
* NO flat shading
* NO dither or resolution drop
* NO fog
* NO colour changes
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
Do NOT begin the low-poly / PS1 transformation.
Wait until I explicitly confirm that the verification timeline is correct.
Only after my confirmation should you proceed to the image-generation / styling stage.
STAGE 3 – LOW-POLY PS1 STYLING (AFTER MY CONFIRMATION ONLY)
Style EVERY extracted frame individually with Seedream 5.0 Pro.
One generation per frame.
Use the original extracted frame as the image input for its own generation.
Apply every style rule above.
Keep the frame count, order and 1/12-second duration exactly as verified in Stage 2.
Replace each verification clip with its styled version in the same timeline slot.
Do NOT merge, skip, duplicate, reorder or interpolate frames.
Do NOT restyle a whole shot from one keyframe.
Keep the same facet density, light direction, fog colour, framebuffer resolution and dither pattern in every frame.
When every frame is styled, play the full timeline back once and report:
(a) styled frame count
(b) timeline duration
(c) any frame where identity, pose or the style rules broke — regenerate those frames only.
The final video must feel like a REAL PS1-ERA 3D RENDER: flat-shaded triangles, swimming textures, wobbling vertices, fog and dither.
The image should deliberately contain:
* visible flat triangles
* per-facet lighting
* affine texture warp
* vertex wobble
* ordered dither
* low-res fat pixels
* distance fog.
Avoid a smooth modern render.
```
